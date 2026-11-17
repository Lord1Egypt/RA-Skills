import io,math,warnings
from PIL import Image,ImageOps,ImageDraw,ImageFont
from io_utils import require,read_file,source,write_json,archive,cli
Image.MAX_IMAGE_PIXELS=25_000_000
warnings.simplefilter('error',Image.DecompressionBombWarning)
FORMATS={'jpeg':('JPEG','.jpg'),'png':('PNG','.png'),'webp':('WEBP','.webp')}
def positive(v,name,high=8000):require(type(v) is int and 1<=v<=high,name+' is outside its allowed range');return v
def process(ws,j,out):
 files=j.get('files');require(isinstance(files,list) and 1<=len(files)<=200,'Provide 1..200 image files');fmt=j.get('format','jpeg');require(fmt in FORMATS,'format: jpeg, png or webp');mode=j.get('mode','contain');require(mode in ['contain','pad','crop'],'mode: contain, pad or crop')
 size=(positive(j.get('width',1600),'width'),positive(j.get('height',1600),'height'));require(size[0]*size[1]<=25_000_000,'Target exceeds 25 megapixels')
 max_bytes=j.get('maxBytes');require(max_bytes is None or type(max_bytes) is int and 1024<=max_bytes<=20*1024*1024,'maxBytes: 1024..20971520');quality=j.get('quality',90);require(type(quality) is int and 15<=quality<=95,'quality: 15..95');require(type(j.get('allowUpscale',False)) is bool,'allowUpscale must be boolean')
 watermark=j.get('watermark');sources=[];logo=None;font=None
 if watermark is not None:
  require(isinstance(watermark,dict),'watermark must be an object');require(bool(watermark.get('text'))!=bool(watermark.get('image')),'Watermark needs either text or image')
  opacity=watermark.get('opacity',0.35);require(type(opacity) in [int,float] and math.isfinite(opacity) and 0<opacity<=1,'opacity: 0..1');require(watermark.get('position','bottom-right') in ['bottom-right','bottom-left','center'],'Unsupported watermark position')
  if watermark.get('image'):
   p=read_file(ws,watermark['image'],20*1024*1024);sources.append(source(ws,p))
   with Image.open(p) as im:require(not getattr(im,'is_animated',False),'Animated watermarks are unsupported');logo=ImageOps.exif_transpose(im).convert('RGBA')
  else:
   text=watermark['text'];require(isinstance(text,str) and 0<len(text)<=120 and '\n' not in text,'Watermark text: 1..120 characters, one line');font_size=positive(watermark.get('fontSize',32),'fontSize',300)
   if watermark.get('font'):
    p=read_file(ws,watermark['font'],20*1024*1024);sources.append(source(ws,p));font=ImageFont.truetype(str(p),font_size)
   else:require(text.isascii(),'Supply a local font for non-ASCII watermark text');font=ImageFont.load_default(size=font_size)
 rows=[];thumbnails=[];paths=[]
 for index,value in enumerate(files,1):
  p=read_file(ws,value,20*1024*1024);s=source(ws,p);sources.append(s)
  with Image.open(p) as raw:
   require(raw.format in ['JPEG','PNG','WEBP','TIFF','BMP'],'Supported inputs: JPEG, PNG, WEBP, TIFF, BMP');require(not getattr(raw,'is_animated',False) and getattr(raw,'n_frames',1)==1,'Use a single-frame image');require(raw.width*raw.height<=25_000_000,'Image exceeds 25 megapixels');raw.load();im=ImageOps.exif_transpose(raw).convert('RGBA');original_size=im.size
  background=j.get('background','#ffffff');require(isinstance(background,str) and len(background)<=30,'Invalid background color')
  if mode=='crop':
   require(j.get('allowUpscale',False) or min(size[0]/im.width,size[1]/im.height)<=1,'Crop would upscale; enable allowUpscale or use pad');im=ImageOps.fit(im,size,method=Image.Resampling.LANCZOS)
  else:
   bounds=size if j.get('allowUpscale',False) else (min(size[0],im.width),min(size[1],im.height));im=ImageOps.contain(im,bounds,Image.Resampling.LANCZOS)
   if mode=='pad':
    canvas=Image.new('RGBA',size,background);canvas.alpha_composite(im,((size[0]-im.width)//2,(size[1]-im.height)//2));im=canvas
  if watermark:
   if logo:mark=logo.copy();mark.thumbnail((max(1,int(im.width*.25)),max(1,int(im.height*.25))))
   else:
    bbox=font.getbbox(watermark['text']);mark=Image.new('RGBA',(max(1,bbox[2]-bbox[0]+8),max(1,bbox[3]-bbox[1]+8)),(0,0,0,0));ImageDraw.Draw(mark).text((4-bbox[0],4-bbox[1]),watermark['text'],font=font,fill=watermark.get('color','#000000'))
   require(mark.width<=im.width and mark.height<=im.height,'Watermark is larger than the output image');mark.putalpha(mark.getchannel('A').point(lambda a:round(a*opacity)));margin=min(16,max(0,min(im.size)//20));pos=watermark.get('position','bottom-right');xy=((im.width-mark.width)//2,(im.height-mark.height)//2) if pos=='center' else (max(0,im.width-mark.width-margin) if pos=='bottom-right' else margin,max(0,im.height-mark.height-margin));im.alpha_composite(mark,xy)
  if fmt=='jpeg':canvas=Image.new('RGBA',im.size,background);canvas.alpha_composite(im);im=canvas.convert('RGB')
  im.info.clear();selected=None
  for shrink in range(9):
   qualities=list(range(quality,14,-5)) if fmt!='png' else [quality]
   for q in qualities:
    stream=io.BytesIO();options={'quality':q,'optimize':True} if fmt=='jpeg' else {'quality':q,'method':4} if fmt=='webp' else {'optimize':True};im.save(stream,FORMATS[fmt][0],**options);data=stream.getvalue()
    if max_bytes is None or len(data)<=max_bytes:selected=(data,q);break
   if selected:break
   new_size=(max(1,int(im.width*.8)),max(1,int(im.height*.8)));require(new_size!=im.size,'Cannot meet requested byte limit');im=im.resize(new_size,Image.Resampling.LANCZOS)
  require(selected is not None,'Cannot meet byte limit in the processing budget');data,q=selected;dest=out/(f'{index:04d}'+FORMATS[fmt][1]);dest.write_bytes(data);paths.append(dest)
  thumb=Image.new('RGB',(220,190),'white');matte=Image.new('RGBA',im.size,'white');matte.alpha_composite(im.convert('RGBA'));preview=matte.convert('RGB');preview.thumbnail((200,155));thumb.paste(preview,((220-preview.width)//2,5));ImageDraw.Draw(thumb).text((8,168),f'{index:04d}  {im.width}x{im.height}',fill='black');thumbnails.append(thumb)
  rows.append({'index':index,'source':s['path'],'inputSize':list(original_size),'output':dest.name,'outputSize':list(im.size),'bytes':len(data),'quality':q if fmt!='png' else None,'resizedForByteLimit':shrink>0})
 sheet=Image.new('RGB',(880,190*math.ceil(len(thumbnails[:40])/4)),'#eeeeee')
 for n,thumb in enumerate(thumbnails[:40]):sheet.paste(thumb,((n%4)*220,(n//4)*190))
 sheet.save(out/'preview.jpg',quality=85);write_json(out/'manifest.json',{'images':rows,'previewCount':min(40,len(rows)),'sources':sources,'originalsModified':False});archive(out,'images.zip',[*paths,out/'manifest.json',out/'preview.jpg']);return {'count':len(rows),'images':rows,'sources':sources,'originalsModified':False}
if __name__=='__main__':cli('mochi-image-batch',process)
