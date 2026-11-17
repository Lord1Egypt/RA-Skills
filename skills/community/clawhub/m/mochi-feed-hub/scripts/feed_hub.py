"""RSS/Atom with conditional retrieval, unread state and durable new-item notices."""
import urllib.request, urllib.parse, urllib.error, uuid
from core import *
from dav import NoRedirect
def parse_feed(raw):
    import feedparser
    if len(raw)>5*1024*1024: raise ValueError('Feed exceeds 5 MiB')
    if b'<!DOCTYPE' in raw.upper() or b'<!ENTITY' in raw.upper(): raise ValueError('Feed XML entities rejected')
    feed=feedparser.parse(raw)
    if feed.bozo and not feed.entries: raise ValueError('Invalid RSS/Atom feed')
    out=[]
    for e in feed.entries[:2000]:
        link=e.get('link','')
        if link and urllib.parse.urlsplit(link).scheme not in ('https','http'): link=''
        key=e.get('id') or link or digest((e.get('title','')+e.get('published','')).encode())
        out.append({'key':key,'title':e.get('title',''),'link':link,'summary':e.get('summary',''),'published':e.get('published',e.get('updated',''))})
    return {'title':feed.feed.get('title',''),'entries':out}
def ingest(st,id,raw,notify=True):
    p=parse_feed(raw); count=0
    for e in p['entries']:
        key=digest((id+'|'+e['key']).encode()); old=st.get('item',key)
        item={**e,'id':key,'feedId':id,'read':old.get('read',False) if old else False}; st.put('item',key,item)
        if not old:
            count+=1
            if notify: st.notice('feed:'+key,{'type':'feed-item','itemId':key,'feedId':id,'title':item['title'],'link':item['link']})
    return {'title':p['title'],'newItems':count}
def handle(st,r):
    action=r['action']
    if action=='add':
        u=urllib.parse.urlsplit(r['url'])
        if u.scheme!='https' or u.username or u.password or u.fragment: raise ValueError('Supply a plain HTTPS feed URL')
        id=ident(r.get('id',digest(r['url'].encode())[:24])); old=st.get('feed',id)
        if old and old['url']!=r['url']: raise ValueError('Feed ID already belongs to another URL')
        return st.put('feed',id,old or {'id':id,'url':r['url'],'initialized':False})
    if action=='feeds': return st.all('feed')
    if action=='import-file': return ingest(st,ident(r['feedId']),local(st.root,r['file'],True).read_bytes(),r.get('notify',False))
    if action=='poll':
        reports=[]
        for f in st.all('feed'):
            if r.get('feedId') and f['id']!=r['feedId']: continue
            headers={'User-Agent':'MochiLab Feed Hub/1.0','Accept':'application/atom+xml, application/rss+xml, application/xml'}
            if f.get('etag'): headers['If-None-Match']=f['etag']
            if f.get('modified'): headers['If-Modified-Since']=f['modified']
            try:
                op=urllib.request.build_opener(NoRedirect())
                with op.open(urllib.request.Request(f['url'],headers=headers),timeout=25) as res:
                    b=res.read(5*1024*1024+1); report=ingest(st,f['id'],b,f['initialized']); f.update(initialized=True,etag=res.headers.get('ETag'),modified=res.headers.get('Last-Modified'),checkedAt=stamp()); st.put('feed',f['id'],f); reports.append({'id':f['id'],**report})
            except urllib.error.HTTPError as e:
                reports.append({'id':f['id'],'unchanged':e.code==304,'httpStatus':e.code})
            except Exception as e: reports.append({'id':f['id'],'errorType':type(e).__name__})
        return {'feeds':reports,'notifications':st.pending()}
    if action=='search':
        q=r.get('query','').casefold(); return [v for v in st.all('item') if (not r.get('unread',False) or not v['read']) and (not r.get('feedId') or v['feedId']==r['feedId']) and q in (v['title']+' '+v['summary']).casefold()][:bounded(r.get('limit',100),1,1000)]
    if action=='mark':
        for id in r['ids']:
            item=st.get('item',id)
            if not item: raise ValueError('Feed item missing')
            item['read']=bool(r.get('read',True)); st.put('item',id,item)
        return {'updated':len(r['ids'])}
    if action=='ack': return st.ack(r['noticeIds'])
    if action=='opml-export':
        import xml.etree.ElementTree as ET
        root=ET.Element('opml',version='2.0'); body=ET.SubElement(root,'body')
        for f in st.all('feed'): ET.SubElement(body,'outline',text=f['id'],type='rss',xmlUrl=f['url'])
        p=local(st.root,r.get('output','exports/feeds.opml')); atomic(p,ET.tostring(root,encoding='utf8',xml_declaration=True)); return {'file':str(p)}
    if action=='opml-import':
        from dav import xml
        root=xml(local(st.root,r['file'],True).read_bytes()); ids=[]
        for e in root.iter('outline'):
            if e.get('xmlUrl'): ids.append(handle(st,{'action':'add','url':e.get('xmlUrl')})['id'])
        return {'feedIds':ids}
    raise ValueError('Unknown feed action')
if __name__=='__main__': runmain(handle,'feed-hub')
