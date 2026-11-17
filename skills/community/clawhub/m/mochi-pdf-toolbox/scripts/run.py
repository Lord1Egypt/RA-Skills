import math
from PIL import Image,ImageOps,ImageDraw
from pypdf import PdfReader,PdfWriter
import pypdfium2 as pdfium
from io_utils import require,read_file,source,write_json,archive,cli

def pages(spec,count):
 if spec is None:return list(range(count))
 require(isinstance(spec,str) and len(spec)<=4000,'pages must be a 1-based range such as 1-3,5');result=[]
 for token in spec.split(','):
  pair=token.strip().split('-');require(len(pair) in [1,2] and all(x.isdecimal() for x in pair),'Invalid page range');a=int(pair[0]);b=int(pair[-1]);require(1<=a<=b<=count,'Page range is outside the document');result.extend(range(a-1,b))
 require(0<len(result)<=500,'Select 1..500 pages');return result
def reader(ws,value,sources,modify=True):
 p=read_file(ws,value,50*1024*1024);sources.append(source(ws,p));r=PdfReader(str(p),strict=True);require(not r.is_encrypted,'Use an unlocked input PDF');require(0<len(r.pages)<=500,'PDF must contain 1..500 pages')
 if modify:require(not r.get_fields() and not r.trailer['/Root'].get('/Perms'),'This operation requires a PDF without interactive fields or document signatures; use inspect or render for this file')
 return p,r
def raster(file,index,scale=1.5):
 doc=pdfium.PdfDocument(str(file))
 try:
  page=doc[index]
  try:
   w,h=page.get_size();require(w*h*scale*scale<=25_000_000,'Rendered page exceeds 25 megapixels');bitmap=page.render(scale=scale,draw_annots=True)
   try:return bitmap.to_pil().convert('RGB').copy()
   finally:bitmap.close()
  finally:page.close()
 finally:doc.close()
def blank(file,index,reader):
 page=reader.pages[index]
 if page.get('/Annots') or (page.extract_text() or '').strip():return False
 image=raster(file,index,2);return all(low>=250 for low,high in image.getextrema())
def preview(file,out):
 r=PdfReader(str(file));count=min(8,len(r.pages));sheet=Image.new('RGB',(720,250*math.ceil(count/3)),'#eeeeee')
 for n in range(count):
  im=raster(file,n);im.thumbnail((220,220));x=(n%3)*240;y=(n//3)*250;sheet.paste(im,(x+(240-im.width)//2,y));ImageDraw.Draw(sheet).text((x+8,y+228),'Page '+str(n+1),fill='black')
 sheet.save(out/'preview.jpg',quality=85)
def write_pdf(writer,path):
 require(0<len(writer.pages)<=500,'Output must contain 1..500 pages')
 with path.open('xb') as f:writer.write(f)
 actual=PdfReader(str(path),strict=True);require(len(actual.pages)==len(writer.pages),'Output page-count verification failed');writer.close()
def process(ws,j,out):
 action=j.get('action');require(action in ['inspect','merge','extract','reorder','split','rotate','compress','render','images-to-pdf','remove-blank'],'Unsupported PDF action');sources=[];outputs=[];mapping=[];details={};opened=[]
 try:
  if action=='images-to-pdf':
   values=j.get('images');require(isinstance(values,list) and 1<=len(values)<=20,'Provide 1..20 images');frames=[]
   for value in values:
    p=read_file(ws,value,20*1024*1024);sources.append(source(ws,p))
    with Image.open(p) as raw:
     require(raw.width*raw.height<=25_000_000 and not getattr(raw,'is_animated',False),'Use a single-frame image up to 25 megapixels');im=ImageOps.exif_transpose(raw).convert('RGBA');canvas=Image.new('RGBA',im.size,'white');canvas.alpha_composite(im);im=canvas.convert('RGB');im.thumbnail((1240,1754));page=Image.new('RGB',(1240,1754),'white');page.paste(im,((1240-im.width)//2,(1754-im.height)//2));frames.append(page)
   dest=out/'result.pdf';frames[0].save(dest,'PDF',save_all=True,append_images=frames[1:],resolution=150.0);require(len(PdfReader(str(dest)).pages)==len(frames),'Image PDF page-count mismatch');outputs=[dest];details={'pages':len(frames),'pageLayout':'A4-like portrait at 150 dpi'}
  elif action=='merge':
   documents=j.get('documents');require(isinstance(documents,list) and 2<=len(documents)<=30,'Provide 2..30 PDFs');writer=PdfWriter()
   for item in documents:
    require(isinstance(item,dict),'documents must contain {file,pages?}');p,r=reader(ws,item.get('file'),sources);opened.append(r);indices=pages(item.get('pages'),len(r.pages));require(len(writer.pages)+len(indices)<=500,'Merged output exceeds 500 pages');writer.append(r,pages=indices,import_outline=False);mapping.extend({'file':sources[-1]['path'],'sourcePage':n+1} for n in indices)
   dest=out/'result.pdf';write_pdf(writer,dest);outputs=[dest]
  else:
   p,r=reader(ws,j.get('file'),sources,modify=action not in ['inspect','render']);opened.append(r);count=len(r.pages);details={'inputPages':count};selected=pages(j.get('pages'),count)
   if action=='inspect':
    require(len(selected)<=100 or not j.get('findBlank',False),'Blank detection is limited to 100 pages per run');details.update(encrypted=False,interactiveFields=bool(r.get_fields()),documentSignature=bool(r.trailer['/Root'].get('/Perms')),pageSizes=[[float(page.mediabox.width),float(page.mediabox.height)] for page in r.pages],blankCandidates=[n+1 for n in selected if blank(p,n,r)] if j.get('findBlank',False) else None);preview(p,out)
   elif action=='render':
    require(len(selected)<=40,'Render at most 40 pages per run');scale=j.get('scale',1.5);require(type(scale) in [int,float] and math.isfinite(scale) and 0.5<=scale<=3,'scale: 0.5..3')
    for n in selected:
     dest=out/(f'page-{n+1:04d}.png');raster(p,n,scale).save(dest);outputs.append(dest);mapping.append({'output':dest.name,'sourcePage':n+1})
   elif action=='split':
    groups=j.get('groups');step=j.get('pagesPerFile',1)
    if groups is not None:require(isinstance(groups,list) and 1<=len(groups)<=100,'groups: 1..100 page-range strings');selections=[pages(s,count) for s in groups]
    else:require(type(step) is int and 1<=step<=500,'pagesPerFile: 1..500');selections=[list(range(n,min(n+step,count))) for n in range(0,count,step)]
    require(len(selections)<=100 and sum(map(len,selections))<=1000,'Split output budget exceeded')
    for n,indices in enumerate(selections,1):
     writer=PdfWriter();writer.append(r,pages=indices,import_outline=False);dest=out/(f'part-{n:03d}.pdf');write_pdf(writer,dest);outputs.append(dest);mapping.append({'output':dest.name,'sourcePages':[v+1 for v in indices]})
   else:
    writer=PdfWriter()
    if action in ['extract','reorder']:
     require(j.get('pages') is not None,'Provide pages');indices=selected
    elif action=='remove-blank':
     confirmed=j.get('confirmedPages');require(isinstance(confirmed,list) and confirmed and len(set(confirmed))==len(confirmed),'Provide confirmedPages from inspected blank candidates');require(all(type(n) is int and 1<=n<=count for n in confirmed),'Invalid confirmed blank page');require(len(confirmed)<=100,'Check at most 100 blank pages');require(all(blank(p,n-1,r) for n in confirmed),'A confirmed page contains text, annotations or visible marks');indices=[n for n in range(count) if n+1 not in confirmed];details['removedBlankPages']=confirmed
    else:indices=list(range(count))
    require(indices,'Cannot remove every page');writer.append(r,pages=indices,import_outline=False)
    if action=='rotate':
     degrees=j.get('degrees');require(type(degrees) is int and degrees in [90,180,270,-90,-180,-270],'degrees: +/-90, +/-180, +/-270')
     for n in set(selected):writer.pages[n].rotate(degrees)
    if action=='compress':
     for page in writer.pages:page.compress_content_streams()
     details['compression']='lossless content-stream compression'
    dest=out/'result.pdf';write_pdf(writer,dest);outputs=[dest];mapping=[{'sourcePage':n+1} for n in indices]
  if outputs and outputs[0].suffix=='.pdf':preview(outputs[0],out)
  details.update(action=action,outputs=[{'file':p.name,'bytes':p.stat().st_size,'pages':len(PdfReader(str(p)).pages) if p.suffix=='.pdf' else None} for p in outputs],mapping=mapping,sources=sources,originalsModified=False)
  if action=='compress':details['savedBytes']=sources[0]['bytes']-outputs[0].stat().st_size
  write_json(out/'manifest.json',details)
  if len(outputs)>1:archive(out,'results.zip',[*outputs,out/'manifest.json'])
  return {**details,'sources':sources}
 finally:
  for r in opened:r.close()
if __name__=='__main__':cli('mochi-pdf-toolbox',process)
