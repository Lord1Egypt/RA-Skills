"""Bounded passive readers with an optional caller-provided PDF text extractor."""
import re,posixpath,shutil,subprocess
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path,PurePosixPath
from urllib.parse import unquote,urlsplit
from zipfile import ZipFile

class ReaderError(ValueError):pass

MAX_FILE=50*1024*1024
MAX_TEXT=12*1024*1024


def decode(raw):
    if raw.startswith((b'\xff\xfe',b'\xfe\xff')):return raw.decode('utf-16')
    try:return raw.decode('utf-8-sig')
    except UnicodeDecodeError:return raw.decode('gb18030')


def xml(raw):
    if b'<!doctype' in raw.replace(b'\x00',b'').lower() or b'<!entity' in raw.replace(b'\x00',b'').lower():raise ReaderError('XML entities/DTDs are not accepted.')
    return ET.fromstring(raw)


def tag(node):return node.tag.rsplit('}',1)[-1]


class Archive:
    def __init__(self,path):
        self.z=ZipFile(path)
        entries=self.z.infolist()
        if len(entries)>3000 or sum(x.file_size for x in entries)>80*1024*1024:self.z.close();raise ReaderError('Archive exceeds extraction budget.')
        names=set()
        for x in entries:
            p=PurePosixPath(x.filename)
            if x.filename in names or p.is_absolute() or '..' in p.parts or '\\' in x.filename or x.file_size>20*1024*1024 or x.flag_bits&1:
                self.z.close();raise ReaderError('Unsafe, encrypted, duplicate or oversized archive entry.')
            names.add(x.filename)
        self.names=names
    def read(self,name):return self.z.read(name)
    def close(self):self.z.close()


class HTML(HTMLParser):
    def __init__(self):super().__init__(convert_charrefs=True);self.skip=0;self.heading='';self.buf=[];self.blocks=[];self.current=None;self.stack=[];self.section=0
    def flush(self):
        value=' '.join(''.join(self.buf).split());self.buf=[]
        if value:
            if self.current:
                self.heading=value;self.section+=1;level=int(self.current[1])
                while self.stack and self.stack[-1][0]>=level:self.stack.pop()
                self.stack.append((level,str(self.section),value))
            self.blocks.append((self.heading,value,[(x[1],x[2]) for x in self.stack]))
    def handle_starttag(self,name,attrs):
        void=name in ('br','img','hr','meta','link','input','source','wbr')
        if self.skip:
            if not void:self.skip+=1
            return
        attrs=dict(attrs)
        if name in ('head','script','style','template','noscript','iframe','object') or 'hidden' in attrs:
            if not void:self.skip=1
            return
        if name in ('p','div','li','article','section','br','tr') or re.fullmatch('h[1-6]',name):self.flush()
        if re.fullmatch('h[1-6]',name):self.current=name
    def handle_startendtag(self,name,attrs):
        if name=='br' and not self.skip:self.buf.append('\n')
    def handle_endtag(self,name):
        if self.skip:self.skip-=1;return
        if name in ('p','div','li','article','section','tr') or re.fullmatch('h[1-6]',name):self.flush()
        if re.fullmatch('h[1-6]',name):self.current=None
    def handle_data(self,value):
        if not self.skip:self.buf.append(value)


def html_blocks(value):
    parser=HTML();parser.feed(value);parser.flush();return parser.blocks


def read(path, *, max_file=MAX_FILE, pdf_ocr=None):
    path=Path(path);kind=path.suffix.lower().lstrip('.');units=[];warnings=[];missing=[];total_pages=None
    if path.stat().st_size>max_file:raise ReaderError(f'File exceeds the {max_file//(1024*1024)} MiB import budget; split it first.')
    used=0
    def add(value,locator,heading='',page=None,ancestry=None):
        nonlocal used
        ancestry=ancestry or [(heading or 'root',heading)]
        value=value.strip()
        for offset in range(0,len(value),2400):
            piece=value[offset:offset+2400]
            if piece.strip():units.append({'id':f'u{len(units)+1:06d}','text':piece,'locator':locator+f' · part {offset//2400+1}', 'heading':heading,'page':page,'section_path':[x[0] for x in ancestry],'heading_path':[x[1] for x in ancestry]})
            used+=len(piece)
            if used>MAX_TEXT:raise ReaderError('Extracted text exceeds budget; select/split a smaller document.')
    if kind in ('txt','md','markdown'):
        value=decode(path.read_bytes());heading='';buf=[];line=1;stack=[];occurrence=0
        for i,row in enumerate(value.splitlines()+[''],1):
            h=re.match(r'^#{1,6}\s+(.+)$',row) if kind!='txt' else None
            if h or not row.strip():
                if buf:add('\n'.join(buf),f'{heading or "Text"} · lines {line}-{i-1}',heading,ancestry=[(x[1],x[2]) for x in stack]);buf=[]
                if h:
                    heading=h.group(1);occurrence+=1;level=len(row)-len(row.lstrip('#'))
                    while stack and stack[-1][0]>=level:stack.pop()
                    stack.append((level,str(occurrence),heading))
                line=i+1
            else:buf.append(row)
    elif kind in ('html','htm','xhtml'):
        for i,(h,value,anc) in enumerate(html_blocks(decode(path.read_bytes())),1):add(value,f'{h or "HTML"} · block {i}',h,ancestry=anc)
        warnings.append('HTML text extraction: verify the main article; layout/media/CSS are not reproduced.')
    elif kind in ('srt','vtt'):
        value=decode(path.read_bytes())
        for block in re.split(r'\r?\n\s*\r?\n',value):
            rows=block.splitlines();idx=next((i for i,x in enumerate(rows) if '-->' in x),None)
            if idx is not None:
                text=re.sub('<[^>]+>','', '\n'.join(rows[idx+1:]));add(text,rows[idx].strip(),'Transcript')
        warnings.append('Transcript evidence only; audio/video was not inspected or transcribed.')
    elif kind=='pdf':
        from pypdf import PdfReader
        with path.open('rb') as stream:
            reader=PdfReader(stream)
            if reader.is_encrypted:raise ReaderError('Encrypted PDF needs an accessible user-provided copy; no password/DRM bypass.')
            total_pages=len(reader.pages)
            if total_pages>1500:raise ReaderError('PDF exceeds 1500 pages; split the intended range first.')
            for i,p in enumerate(reader.pages,1):
                if pdf_ocr and i in pdf_ocr:
                    value = pdf_ocr[i](path, i)
                else:
                    try:value=p.extract_text() or ''
                    except Exception:value=''
                if value.strip():add(value,f'PDF page {i}',page=i)
                else:missing.append(i)
        if pdf_ocr:warnings.append('Selected PDF pages use OCR. Verify the original page visually before citing, especially formulas and tables.')
        if missing:warnings.append('Unreadable/empty PDF pages require OCR or a text copy; they are excluded.')
        warnings.append('Text extraction does not establish formula, table or image accuracy; visually check relevant originals.')
    elif kind in ('docx','epub','pptx'):
        archive=Archive(path)
        try:
            if kind=='docx':
                tree=xml(archive.read('word/document.xml'));heading='';stack=[];occurrence=0
                for i,p in enumerate((n for n in tree.iter() if tag(n)=='p'),1):
                    value=''.join(n.text or '' for n in p.iter() if tag(n)=='t')
                    styles=[next(iter(n.attrib.values()),'') for n in p.iter() if tag(n)=='pStyle']
                    if any(re.search('heading|标题',s,re.I) for s in styles):
                        heading=value;occurrence+=1;match=re.search(r'(\d+)',styles[0]);level=int(match[1]) if match else 1
                        while stack and stack[-1][0]>=level:stack.pop()
                        stack.append((level,str(occurrence),value))
                    add(value,f'{heading or "Word"} · paragraph {i}',heading,ancestry=[(x[1],x[2]) for x in stack])
                warnings.append('DOCX uses heading/paragraph locators, not original page numbers; tables/media/formulas need original inspection.')
            elif kind=='pptx':
                # Follow presentation order when the package supplies it.
                if 'ppt/presentation.xml' in archive.names and 'ppt/_rels/presentation.xml.rels' in archive.names:
                    rels={n.attrib['Id']:n.attrib['Target'] for n in xml(archive.read('ppt/_rels/presentation.xml.rels'))}
                    slides=[]
                    for n in xml(archive.read('ppt/presentation.xml')).iter():
                        if tag(n)=='sldId':
                            rid=next((v for k,v in n.attrib.items() if k.endswith('}id')),None)
                            target=rels.get(rid,'');slides.append(posixpath.normpath(posixpath.join('ppt',target)))
                else:slides=sorted((n for n in archive.names if re.fullmatch(r'ppt/slides/slide\d+.xml',n)),key=lambda n:int(re.search(r'(\d+)\.xml',n).group(1)))
                for i,name in enumerate(slides,1):
                    if name not in archive.names:raise ReaderError('Slide reference is outside this package.')
                    value='\n'.join(n.text or '' for n in xml(archive.read(name)).iter() if tag(n)=='t');add(value,f'Slide {i}',f'Slide {i}')
                warnings.append('Slide text only; charts, speaker notes, images and animations are not interpreted.')
            else:
                if 'META-INF/encryption.xml' in archive.names:raise ReaderError('Encrypted EPUB requires a DRM-free authorized copy; no decryption performed.')
                container=xml(archive.read('META-INF/container.xml'));opf=next((n.attrib.get('full-path') for n in container.iter() if tag(n)=='rootfile'),None)
                if opf not in archive.names:raise ReaderError('EPUB package path is invalid.')
                tree=xml(archive.read(opf));items={n.attrib['id']:n.attrib for n in tree.iter() if tag(n)=='item'}
                for i,n in enumerate((n for n in tree.iter() if tag(n)=='itemref'),1):
                    item=items.get(n.attrib.get('idref'),{});href=unquote(item.get('href','').split('#')[0])
                    if urlsplit(href).scheme or href.startswith('/'):raise ReaderError('EPUB references must remain in the package.')
                    name=posixpath.normpath(posixpath.join(posixpath.dirname(opf),href))
                    if name not in archive.names:raise ReaderError('EPUB spine reference is missing.')
                    for h,value,anc in html_blocks(decode(archive.read(name))):add(value,f'EPUB chapter {i} · {h or name}',h or f'Chapter {i}',ancestry=[(f'chapter{i}.{sid}',title) for sid,title in anc] or [(f'chapter{i}',f'Chapter {i}')])
                warnings.append('EPUB spine text only; images/math/media require original inspection.')
        finally:archive.close()
    elif kind in ('doc','rtf'):
        antiword=shutil.which('antiword') if kind=='doc' else None;native=shutil.which('textutil')
        if antiword:argv=[antiword,'-t',str(path.resolve())]
        elif native:argv=[native,'-convert','txt','-stdout','-noload','-nostore',str(path.resolve())]
        else:return {'kind':kind,'status':'needs_conversion','units':[],'warnings':['Install a trusted antiword/textutil converter or provide DOCX/TXT; no converter was executed.'],'missing_pages':[],'total_pages':None}
        p=subprocess.run(argv,capture_output=True,timeout=25)
        if p.returncode:raise ReaderError('Trusted Word conversion failed; provide DOCX/TXT. Existing material versions remain intact.')
        value=decode(p.stdout)
        for i,para in enumerate(re.split(r'\n\s*\n',value),1):add(para,f'Converted {kind.upper()} paragraph {i}')
        warnings.append('Converted text only; original Word pagination/layout is not claimed.')
    else:return {'kind':kind,'status':'unsupported','units':[],'warnings':['Provide PDF, TXT, Markdown, HTML, DOCX, EPUB, PPTX or SRT/VTT; use an authorized conversion for other books/media. Audio/video requires an actual transcript.'],'missing_pages':[],'total_pages':None}
    result = {'kind':kind,'status':('partial' if missing else 'ready') if units else 'failed','units':units,'warnings':warnings or ([] if units else ['No readable text extracted.']),'missing_pages':missing,'total_pages':total_pages}
    if kind == 'pdf' and pdf_ocr:
        result['ocr_pages'] = sorted(set(pdf_ocr).difference(missing))
    return result
