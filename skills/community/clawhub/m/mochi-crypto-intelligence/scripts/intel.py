#!/usr/bin/env python3
"""Mochi Crypto Intelligence: public-source collection and explicit local research state.
Python3.10+, standard library only. No model, credential, paid service or background worker.
"""
import argparse, contextlib, datetime as dt, email.utils, hashlib, html, ipaddress, json, os
import re, socket, sys, tempfile, time, unicodedata, urllib.error, urllib.parse, urllib.request
import urllib.robotparser, xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
VERSION = '1.0.0'
UA = 'MochiCryptoIntelligence/1.0 (+https://mochi.bz; public research)'
CATALOG = Path(__file__).resolve().parent.parent / 'references' / 'sources.json'
MAX_BYTES = 2 * 1024 * 1024
UTC = dt.timezone.utc

def now(): return dt.datetime.now(UTC).isoformat(timespec='seconds').replace('+00:00', 'Z')
def load(path): return json.loads(Path(path).read_text(encoding='utf-8-sig'))
def digest(s): return hashlib.sha256(s.encode('utf-8')).hexdigest()
def save(path, obj):
    p = Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix='.'+p.name+'-', dir=str(p.parent))
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(obj, f, ensure_ascii=False, indent=2); f.write('\n'); f.flush(); os.fsync(f.fileno())
        os.replace(tmp, p)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)

def canonical(url):
    u = urllib.parse.urlsplit(url.strip())
    if u.scheme.lower() != 'https' or not u.hostname or u.username or u.password:
        raise ValueError('Only credential-free public HTTPS URLs are supported')
    if u.port not in (None, 443): raise ValueError('Only HTTPS port443 is supported')
    if any(k.lower() in {'api_key','apikey','access_token','token','auth','signature'} for k,v in urllib.parse.parse_qsl(u.query)):
        raise ValueError('Credential-like query parameter; use a public source URL')
    host = u.hostname.encode('idna').decode().lower()
    if ':' in host: host = '['+host+']'
    q = [(k,v) for k,v in urllib.parse.parse_qsl(u.query, keep_blank_values=True)
         if not k.lower().startswith('utm_') and k.lower() not in {'fbclid','gclid','mc_cid','mc_eid'}]
    return urllib.parse.urlunsplit(('https',host,u.path or '/',urllib.parse.urlencode(q),''))

def public_url(url):
    url = canonical(url); host = urllib.parse.urlsplit(url).hostname
    addresses = socket.getaddrinfo(host,443,type=socket.SOCK_STREAM)
    if not addresses or any(not ipaddress.ip_address(a[4][0].split('%')[0]).is_global for a in addresses):
        raise ValueError('Non-public network destination refused')
    return url

class Redirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        newurl = public_url(urllib.parse.urljoin(req.full_url,newurl))
        # Cross-origin redirects are returned for browser review; no hidden new-origin fetch.
        if urllib.parse.urlsplit(req.full_url).netloc != urllib.parse.urlsplit(newurl).netloc:
            raise ValueError('Cross-origin redirect requires source/browser review: '+newurl)
        return super().redirect_request(req,fp,code,msg,headers,newurl)

class Fetcher:
    def __init__(self, timeout=12):
        self.timeout=timeout; self.robots={}; self.last={}; self.opener=urllib.request.build_opener(Redirects())
    def request(self,url,cap=MAX_BYTES):
        url=public_url(url)
        req=urllib.request.Request(url, headers={'User-Agent':UA,'Accept':'text/html,application/rss+xml,application/atom+xml,application/xml,text/plain;q=0.8','Accept-Encoding':'identity'})
        with self.opener.open(req,timeout=self.timeout) as r:
            content=r.read(cap+1)
            if len(content)>cap: raise ValueError('Source exceeds byte limit; use host browser or a specific article')
            encoding=r.headers.get_content_charset() or 'utf-8'
            return content.decode(encoding,errors='replace'), r.geturl(), r.headers.get('Content-Type','')
    def get(self,url):
        url=public_url(url); u=urllib.parse.urlsplit(url); origin=u.scheme+'://'+u.netloc
        if origin not in self.robots:
            rp=urllib.robotparser.RobotFileParser(origin+'/robots.txt')
            try: body,_,_=self.request(origin+'/robots.txt',262144); rp.parse(body.splitlines())
            except urllib.error.HTTPError as e:
                if e.code==404: rp.parse([])
                else: raise ValueError('robots unavailable (HTTP'+str(e.code)+'); use permitted browser/source')
            self.robots[origin]=rp
        rp=self.robots[origin]
        if not rp.can_fetch(UA,url): raise ValueError('robots.txt disallows collector access')
        delay=rp.crawl_delay(UA) or rp.crawl_delay('*') or 1
        if delay>3: raise ValueError('Long crawl delay; defer this source instead of rapid polling')
        pause=delay-(time.monotonic()-self.last.get(origin,0))
        if pause>0: time.sleep(pause)
        try: return self.request(url)
        finally: self.last[origin]=time.monotonic()

def plain(text): return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',text or ''))).strip()
def date_value(value):
    if not value: return None
    value=value.strip()
    if re.fullmatch(r'\d{4}-\d{2}-\d{2}',value): return value # date precision stays a date
    try: parsed=dt.datetime.fromisoformat(value.replace('Z','+00:00'))
    except ValueError:
        try: parsed=email.utils.parsedate_to_datetime(value)
        except (ValueError,TypeError,OverflowError): return None
    if parsed.tzinfo is None: return None # do not invent the source timezone
    return parsed.astimezone(UTC).isoformat(timespec='seconds').replace('+00:00','Z')

class Page(HTMLParser):
    def __init__(self,base):
        super().__init__(convert_charrefs=True);self.base=base;self.hidden=0;self.title_depth=0;self.title=[];self.text=[];self.links=[];self.feeds=[];self.current=None;self.published=None;self.article_depth=0;self.main_depth=0;self.article_text=[];self.main_text=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag in {'script','style','noscript','svg'}: self.hidden+=1
        if tag=='title': self.title_depth+=1
        if tag=='article': self.article_depth+=1
        if tag=='main': self.main_depth+=1
        if self.hidden:return
        if tag=='meta' and (a.get('property') or a.get('name')) in {'article:published_time','datePublished','pubdate'}:
            self.published=date_value(a.get('content')) or self.published
        if tag=='link' and 'alternate' in a.get('rel','') and a.get('type') in {'application/rss+xml','application/atom+xml'}:
            self.feeds.append(urllib.parse.urljoin(self.base,a.get('href','')))
        if tag=='a':self.current=[urllib.parse.urljoin(self.base,a.get('href','')),[]]
        if tag in {'p','div','h1','h2','h3','li','br','article','section'}:self.text.append('\n')
    def handle_endtag(self,tag):
        if tag in {'script','style','noscript','svg'} and self.hidden:self.hidden-=1
        if tag=='title' and self.title_depth:self.title_depth-=1
        if tag=='article' and self.article_depth:self.article_depth-=1
        if tag=='main' and self.main_depth:self.main_depth-=1
        if tag=='a' and self.current:
            u,label=self.current;self.current=None
            try:u=canonical(u)
            except ValueError:return
            title=plain(' '.join(label))
            if title:self.links.append({'url':u,'title':title[:500]})
    def handle_data(self,data):
        if self.hidden:return
        if self.title_depth:self.title.append(data)
        self.text.append(data)
        if self.article_depth:self.article_text.append(data)
        if self.main_depth:self.main_text.append(data)
        if self.current:self.current[1].append(data)

def parse_document(body,url):
    if '<!ENTITY' in body.upper() or '<!DOCTYPE' in body.upper() and not re.search(r'<!doctype\s+html',body,re.I):
        raise ValueError('XML DTD/entity declarations are not accepted')
    root=None
    try:root=ET.fromstring(body)
    except ET.ParseError:pass
    if root is not None and root.tag.split('}')[-1] in {'rss','feed','RDF'}:
        def find(node,names):
            for child in node:
                if child.tag.split('}')[-1] in names and child.text:return plain(child.text)
            return ''
        items=[]
        for node in root.iter():
            if node.tag.split('}')[-1] not in {'item','entry'}:continue
            link=''
            for child in node:
                if child.tag.split('}')[-1]=='link' and child.attrib.get('rel','alternate')=='alternate':
                    link=child.attrib.get('href') or child.text or '';break
            if not link.strip():continue
            try:link=canonical(urllib.parse.urljoin(url,link.strip()))
            except ValueError:continue
            title=find(node,{'title'})
            if not title:continue
            published=find(node,{'published','pubDate','date'})
            # modified/updated dates are not publication dates.
            updated=find(node,{'updated','modified'})
            items.append({'title':title,'url':link,'published_at':date_value(published),'published_raw':published or None,
                          'updated_at':date_value(updated),'excerpt':find(node,{'summary','description','encoded','content'})[:650],
                          'verification':'candidate_feed_entry'})
        return {'format':'feed','items':items,'links':[],'feeds':[]}
    p=Page(url);p.feed(body)
    links=list({v['url']:v for v in p.links}.values())
    return {'format':'html','title':plain(' '.join(p.title)),'published_at':p.published,
            'excerpt':plain(' '.join(p.article_text or p.main_text or p.text))[:10000],'links':links[:150],'feeds':list(dict.fromkeys(p.feeds))[:8],
            'verification':'page_read_not_claim_verified'}

def dedupe(items):
    out={}
    for item in items:
        item=dict(item);item['url']=canonical(item['url']);key=item['url']
        if key not in out:out[key]=item
    return list(out.values())

def source_rows(args):
    rows=load(args.catalog)['sources']
    ids={x for x in (getattr(args,'ids','') or '').split(',') if x}
    if ids:
        found={r['id'] for r in rows};missing=ids-found
        if missing:raise ValueError('Unknown source IDs: '+','.join(sorted(missing)))
        rows=[r for r in rows if r['id'] in ids]
    return rows

def collect(args):
    fetch=Fetcher(args.timeout);results=[];candidates=[]
    for source in source_rows(args):
        url=source.get('feed') or source['url'];entry={'source_id':source['id'],'requested_url':url,'observed_at':now()}
        try:
            body,final,ctype=fetch.get(url);data=parse_document(body,final)
            candidates+= [dict(i,source_id=source['id'],observed_at=entry['observed_at']) for i in data.get('items',[])[:args.limit]]
            if data['format']=='html':data['links']=data['links'][:args.limit]
            entry.update(status='ok',final_url=final,content_type=ctype,document=data)
        except (OSError,ValueError,urllib.error.URLError) as e:
            status=getattr(e,'code',None);entry.update(status='gap',http_status=status,reason=str(e)[:300])
        results.append(entry)
    obj={'schema':1,'collected_at':now(),'candidate_only':True,'coverage':results,'candidates':dedupe(candidates)}
    save(args.out,obj);return {'output':str(args.out),'sources':len(results),'ok':sum(x['status']=='ok' for x in results),'gaps':sum(x['status']=='gap' for x in results),'candidates':len(obj['candidates'])}

def events_input(path):
    data=load(path);events=data.get('events') if isinstance(data,dict) else None
    if not isinstance(events,list):raise ValueError('Input must contain an events list')
    seen=set();out=[]
    for e in events:
        e=dict(e);key=e.get('event_key','')
        if not re.fullmatch(r'[a-z0-9][a-z0-9._-]{2,159}',key) or key in seen:raise ValueError('Missing, duplicate or invalid event_key')
        seen.add(key)
        for field in ['title','summary','stage','evidence']:
            if not isinstance(e.get(field),str) or not e[field].strip():raise ValueError('Missing event '+field)
        if e['stage'] not in {'rumor','proposed','announced','scheduled','executed','cancelled','disputed'}:raise ValueError('Invalid stage')
        if e['evidence'] not in {'unverified','attributed','primary','corroborated','disputed'}:raise ValueError('Invalid evidence label')
        if not isinstance(e.get('sources'),list) or not e['sources']:raise ValueError('Each event requires at least one source')
        sources=[]
        for s in e['sources']:
            s=dict(s);s['url']=canonical(s['url'])
            if not isinstance(s.get('publisher'),str) or not s['publisher'].strip():raise ValueError('Source publisher required')
            if not isinstance(s.get('checked_at'),str) or 'T' not in s['checked_at'] or not date_value(s['checked_at']):raise ValueError('Timezone-aware checked_at required')
            if not isinstance(s.get('supports'),str) or not s['supports'].strip():raise ValueError('Describe exactly what this source supports')
            sources.append(s)
        for field in ['published_at','event_at']:
            if e.get(field) and not date_value(e[field]):raise ValueError('Unparseable/ambiguous '+field)
        e['sources']=sources;out.append(e)
    return out

def event_fingerprint(e):
    # Evidence revisions matter. Fetch/check times and source ordering do not create fake news.
    relevant={k:e.get(k) for k in ['title','summary','stage','evidence','published_at','event_at','impact','uncertainties']}
    relevant['sources']=sorted([{'url':s['url'],'publisher':s['publisher'],'supports':s['supports']} for s in e['sources']],key=lambda s:(s['url'],s['supports']))
    return digest(json.dumps(relevant,ensure_ascii=False,sort_keys=True))

@contextlib.contextmanager
def locked(path):
    p=Path(str(path)+'.lock');p.parent.mkdir(parents=True,exist_ok=True)
    try:fd=os.open(p,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
    except FileExistsError:raise ValueError('State is in use (or an interrupted lock exists); inspect before retrying')
    try:os.write(fd,str(os.getpid()).encode());os.close(fd);yield
    finally:p.unlink(missing_ok=True)

def ingest(args):
    events=events_input(args.input);statepath=Path(args.state)
    if not args.commit:
        state=load(statepath) if statepath.exists() else {'schema':1,'events':{}}
        return diff_events(state,events)[1]
    with locked(statepath):
        existed=statepath.exists();state=load(statepath) if existed else {'schema':1,'events':{}}
        state,report=diff_events(state,events)
        if existed:
            backup=Path(str(statepath)+'.bak-'+dt.datetime.now(UTC).strftime('%Y%m%dT%H%M%S')+'-'+os.urandom(3).hex())
            save(backup,load(statepath))
        save(statepath,state)
    return dict(report,state=str(statepath),committed=True)

def diff_events(state,events):
    if state.get('schema')!=1 or not isinstance(state.get('events'),dict):raise ValueError('Unsupported state; original left untouched')
    # JSON copy prevents a dry-run from mutating the caller's state object.
    state=json.loads(json.dumps(state));new=[];updated=[];unchanged=[];stamp=now()
    for e in events:
        key=e['event_key'];fp=event_fingerprint(e);old=state['events'].get(key)
        if old is None:new.append(key)
        elif fp!=old['fingerprint']:updated.append(key)
        else:unchanged.append(key);continue
        history=(old.get('history',[])+[{'changed_at':old['last_changed'],'event':old['event']}]) if old else []
        state['events'][key]={'fingerprint':fp,'first_seen':old['first_seen'] if old else stamp,'last_changed':stamp,'event':e,'history':history}
    # Missing from today's partial coverage is never retracted, cancelled or deleted.
    state['updated_at']=stamp
    return state,{'new':new,'updated':updated,'unchanged':unchanged,'state_changed':bool(new or updated),'committed':False,'not_seen_is_not_deleted':True}

def watch(args):
    if args.set is not None:
        rows=[x.strip() for x in args.set.split(',') if x.strip()]
        if not rows:raise ValueError('Provide project names or chain:contract identities')
        save(args.file,{'schema':1,'updated_at':now(),'projects':list(dict.fromkeys(rows))})
    return load(args.file) if Path(args.file).exists() else {'schema':1,'projects':[]}

def main(argv=None):
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('--version',action='version',version=VERSION);sub=a.add_subparsers(dest='command',required=True)
    p=sub.add_parser('sources');p.add_argument('--catalog',type=Path,default=CATALOG);p.add_argument('--ids',default='')
    p=sub.add_parser('collect');p.add_argument('--catalog',type=Path,default=CATALOG);p.add_argument('--ids',required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--limit',type=int,default=15);p.add_argument('--timeout',type=int,default=12)
    p=sub.add_parser('parse');p.add_argument('--input',type=Path,required=True);p.add_argument('--base',required=True);p.add_argument('--out',type=Path,required=True)
    p=sub.add_parser('read');p.add_argument('url');p.add_argument('--out',type=Path,required=True)
    p=sub.add_parser('ingest');p.add_argument('--input',type=Path,required=True);p.add_argument('--state',type=Path,required=True);p.add_argument('--commit',action='store_true')
    p=sub.add_parser('watchlist');p.add_argument('--file',type=Path,required=True);p.add_argument('--set')
    args=a.parse_args(argv)
    if args.command=='sources':result={'sources':source_rows(args)}
    elif args.command=='collect':
        if not 1<=args.limit<=50 or not 1<=args.timeout<=30:raise ValueError('limit1..50, timeout1..30 required')
        result=collect(args)
    elif args.command=='parse':
        if args.input.stat().st_size>MAX_BYTES:raise ValueError('Input exceeds byte limit')
        result=parse_document(args.input.read_text(encoding='utf-8-sig'),canonical(args.base));save(args.out,result);result={'output':str(args.out),'format':result['format'],'items':len(result.get('items',[]))}
    elif args.command=='read':
        body,final,ctype=Fetcher().get(args.url);obj=parse_document(body,final);obj.update(retrieved_at=now(),url=final,content_type=ctype);save(args.out,obj);result={'output':str(args.out),'format':obj['format'],'retrieved_at':obj['retrieved_at']}
    elif args.command=='ingest':result=ingest(args)
    else:result=watch(args)
    print(json.dumps(result,ensure_ascii=False,indent=2));return 0
if __name__=='__main__':
    try:sys.exit(main())
    except (ValueError,OSError,KeyError,TypeError,json.JSONDecodeError,ET.ParseError) as e:
        print(json.dumps({'error':str(e)},ensure_ascii=False),file=sys.stderr);sys.exit(2)
