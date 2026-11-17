"""One offline HTML document; only the learner's outbound source links use network."""
from omni_locale import source_labels
import base64
from html import escape
from pathlib import Path
from omni_locale import language,subtitle

def serialize(data,plan,config,image,date,key):
    image=Path(image)
    if image.suffix.lower() not in ('.png','.jpg','.jpeg'):
        raise ValueError('HTML figures need PNG or JPEG.')
    mime='image/png' if image.suffix.lower()=='.png' else 'image/jpeg'
    uri='data:'+mime+';base64,'+base64.b64encode(image.read_bytes()).decode('ascii')
    labels=source_labels(config); e=escape
    figure='<figure><img src="'+uri+'" alt="'+e(data['figure']['caption'],quote=True)+'"><figcaption>'+e(data['figure']['caption'])+'<br><small>'+e(data['figure']['credit'])+'</small></figcaption></figure>'
    parts=[]
    for i,s in enumerate(data['sections']):
        parts.append('<section><h2>'+e(s['title'])+'</h2>'+''.join('<p>'+e(p).replace('\n','<br>')+'</p>' for p in s['body'].split('\n\n'))+'</section>')
        if i==min(1,len(data['sections'])-1):parts.append(figure)
    sources=''.join('<li><span>['+e(s['id'])+'] </span>'+('<a href="'+e(s['url'],quote=True)+'">'+e(s['title'])+'</a>' if s.get('url') else e(s['title']))+' — '+e(s['note'])+'<br><small>'+e(s['publisher'])+' | '+e(labels['published'])+': '+e(s['published_at'])+' | '+e(labels['checked'])+': '+e(s['checked_at'])+'</small></li>' for s in data['sources'])
    css='''*{box-sizing:border-box}html{color-scheme:light}body{margin:0;background:#f3f6f5;color:#173747;font:18px/1.75 Georgia,"Noto Serif CJK SC","Hiragino Mincho ProN","Apple SD Gothic Neo","Geeza Pro",serif}main{max-width:880px;margin:32px auto;background:#fff;padding:clamp(20px,5vw,58px);border-radius:12px}h1{font-size:clamp(28px,5vw,40px);line-height:1.3}h2{font-size:25px;line-height:1.4;margin-block-start:1.4em}p,li{overflow-wrap:anywhere}header>p,small{color:#52686e}a{color:#166c73;text-decoration-thickness:1px;text-underline-offset:3px}figure{margin:28px 0;text-align:center}img{max-width:100%;max-height:440px;height:auto;object-fit:contain}figcaption{font-size:15px}li{margin-block:16px}ol{padding-inline-start:1.5em}html[dir=rtl] body{font-family:"Geeza Pro","Noto Naskh Arabic",serif}@media(max-width:600px){main{margin:0;border-radius:0}body{font-size:17px}}@media print{body{background:#fff}main{margin:0;padding:0;max-width:none}figure,li{break-inside:avoid}}'''
    return '<!doctype html>\n<html lang="'+labels['code']+'" dir="'+labels['dir']+'"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+e(data['title'])+'</title><style>'+css+'</style></head><body><main><header><h1>'+e(data['title'])+'</h1><p>'+e(subtitle(data,plan,config,date,key))+'</p></header>'+''.join(parts)+'<section><h2>'+e(labels['further'])+'</h2><p>'+e(labels['optional'])+'</p><ol>'+sources+'</ol></section></main></body></html>\n'
