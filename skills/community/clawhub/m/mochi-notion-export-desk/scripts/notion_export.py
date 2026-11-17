from helpers import *
import zipfile,posixpath

def handle(s,r):
 require(r.get('action')=='index','Action: index');p=local(s.root,r['file'],'file');readbytes(p,16*1024*1024);pages=[];tables=[];skipped=[];total=0;seen=set()
 with zipfile.ZipFile(p) as z:
  require(len(z.infolist())<=2000,'Too many ZIP entries')
  for e in z.infolist():
   n=e.filename.replace('\\','/');require(not n.startswith('/') and '..' not in n.split('/') and not re.match(r'^[A-Za-z]:',n),'Unsafe archive path');require(n.casefold() not in seen,'Duplicate archive path');seen.add(n.casefold());require(not stat.S_ISLNK(e.external_attr>>16),'Link entry unsupported');total+=e.file_size;require(total<=32*1024*1024 and e.file_size<=4*1024*1024,'Export too large');require(e.file_size<=1000*max(1,e.compress_size),'Excessive compression ratio');require(not e.flag_bits&1,'Encrypted ZIP unsupported')
   if e.is_dir():continue
   suffix=Path(n).suffix.lower()
   if suffix=='.md':
    raw=z.read(e);t=raw.decode('utf-8-sig');title=next((x.lstrip('# ').strip() for x in t.splitlines() if x.strip()),Path(n).stem);pages.append({'path':n,'title':title[:500],'characters':len(t),'sha256':sha(raw),'links':re.findall(r'\[[^\]]*\]\(([^)]+)\)',t),'text':t})
   elif suffix=='.csv':
    raw=z.read(e);reader=csv.DictReader(io.StringIO(raw.decode('utf-8-sig')));fields=reader.fieldnames;require(fields and len(fields)==len(set(fields)),'Invalid CSV headers');rows=list(reader);require(len(rows)<=50000 and all(None not in x and None not in x.values() for x in rows),'Invalid CSV rows');tables.append({'path':n,'columns':fields,'rows':len(rows),'sha256':sha(raw)})
   else:skipped.append(n)
 require(pages or tables,'Export has no Markdown or CSV; choose Markdown & CSV in Notion export settings')
 md='# Notion export index\n\n'+'\n\n'.join('## '+x['title']+'\nSource: '+x['path']+'\n\n'+x['text'] for x in pages)
 for x in pages:x.pop('text')
 return file_report(s,{'pages':pages,'tables':tables,'skipped':skipped,'sourceArchiveSha256':sha(readbytes(p)),'remoteChanges':False,'scope':'Indexes an existing Markdown & CSV export, not a Notion API sync or complete workspace backup.'},'notion-index.md',md.encode())
