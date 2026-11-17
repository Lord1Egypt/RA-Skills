#!/usr/bin/env node
import https from 'node:https';
import dns from 'node:dns/promises';
import net from 'node:net';
import fs from 'node:fs/promises';
import path from 'node:path';
import { constants } from 'node:fs';
import { randomUUID } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import zlib from 'node:zlib';

export const SOURCES = [
  { name: 'OpenAI News', url: 'https://openai.com/news/rss.xml' },
  { name: 'GitHub Changelog', url: 'https://github.blog/changelog/feed/' },
  { name: 'Google AI', url: 'https://blog.google/technology/ai/rss/' }
];
const MAX_XML = 2 * 1024 * 1024, MAX_WIRE = 1024 * 1024;
export function publicAddress(address) {
  if (net.isIP(address) === 4) {
    const [a,b,c] = address.split('.').map(Number);
    return !(a === 0 || a === 10 || a === 127 || a >= 224 || (a === 169 && b === 254) || (a === 172 && b >= 16 && b <= 31) || (a === 192 && (b === 168 || (b === 0 && (c === 0 || c === 2)) || (b === 88 && c === 99))) || (a === 100 && b >= 64 && b <= 127) || (a === 198 && (b === 18 || b === 19 || (b === 51 && c === 100))) || (a === 203 && b === 0 && c === 113));
  }
  // Admit native global unicast only; exclude documentation and transition ranges.
  if (net.isIP(address) !== 6) return false;
  const [first,second] = address.split(':').map(x=>Number.parseInt(x||'0',16));
  return first >= 0x2000 && first < 0x3ffe && !(first===0x2001&&(second<0x200||second===0xdb8)) && first!==0x2002;
}
export function publicUrl(value) {
  if (typeof value !== 'string' || value.length > 2048 || /[\s\\\u0000-\u001f\u007f]/u.test(value)) throw Error('Unsafe feed or article URL');
  const url = new URL(value);
  if (url.protocol !== 'https:' || url.username || url.password || (url.port && url.port !== '443') || net.isIP(url.hostname.replace(/^\[|\]$/g,'')) || !url.hostname.includes('.') || /\.(?:local|localhost|internal|home|lan|test|invalid)$/i.test(url.hostname)) throw Error('Public HTTPS domain on port 443 required');
  url.hash = ''; return url;
}
async function deadline(promise, ms) {
  let timer;
  try { return await Promise.race([promise,new Promise((_,reject)=>{timer=setTimeout(()=>reject(Error('Network timeout')),ms);})]); }
  finally { clearTimeout(timer); }
}
export async function fetchXml(value, options = {}) {
  const lookup = options.lookup || dns.lookup;
  const end = Date.now() + 18000;
  async function request(current, redirects) {
    const url = publicUrl(current);
    const addresses = await deadline(lookup(url.hostname,{all:true,verbatim:true}),Math.max(1,Math.min(6000,end-Date.now())));
    if (!addresses.length || addresses.some(x=>!publicAddress(x.address))) throw Error('DNS includes a non-public address');
    if (Date.now() >= end) throw Error('Network timeout');
    const address = addresses.find(x=>x.family===4) || addresses[0];
    const result = await new Promise((resolve,reject)=>{
      const req = https.get(url,{agent:false,minVersion:'TLSv1.2',rejectUnauthorized:true,lookup:(_host,opts,callback)=>opts.all?callback(null,[address]):callback(null,address.address,address.family),headers:{'User-Agent':'MochiLab-Daily-Brief/1.0 (+https://mochilab.bz)','Accept':'application/rss+xml, application/atom+xml, application/xml, text/xml','Accept-Encoding':'gzip, deflate, br'}},response=>{
        const status = response.statusCode || 0;
        if ([301,302,303,307,308].includes(status)) { const location=response.headers.location;response.destroy();resolve({location});return; }
        if (status !== 200) { response.destroy();reject(Error('HTTP '+status));return; }
        let wire=0, expanded=0; const chunks=[];
        response.on('data',chunk=>{wire+=chunk.length;if(wire>MAX_WIRE)req.destroy(Error('Feed exceeds compressed byte limit'));});
        let stream=response;
        const encoding=(response.headers['content-encoding'] || 'identity').toLowerCase();
        if(encoding==='gzip')stream=response.pipe(zlib.createGunzip());
        else if(encoding==='deflate')stream=response.pipe(zlib.createInflate());
        else if(encoding==='br')stream=response.pipe(zlib.createBrotliDecompress());
        else if(encoding!=='identity'){response.destroy();reject(Error('Unsupported content encoding'));return;}
        stream.on('data',chunk=>{expanded+=chunk.length;if(expanded>MAX_XML){stream.destroy(Error('Feed exceeds XML byte limit'));req.destroy();}else chunks.push(chunk);});
        stream.on('error',reject);response.on('error',reject);
        stream.on('end',()=>{try{resolve({xml:new TextDecoder('utf-8',{fatal:true}).decode(Buffer.concat(chunks))});}catch{reject(Error('Feed is not valid UTF-8'));}});
      });
      const timer=setTimeout(()=>req.destroy(Error('Network timeout')),Math.max(1,end-Date.now()));
      req.on('error',reject);req.on('close',()=>clearTimeout(timer));
    });
    if ('location' in result) {
      if (!result.location || redirects >= 3) throw Error('Redirect limit or missing redirect target');
      return request(new URL(result.location,url).href,redirects+1);
    }
    return result.xml;
  }
  return request(value,0);
}
function entities(text) {
  return text.replace(/&(#x[0-9a-f]+|#\d+|amp|lt|gt|quot|apos);/gi,(_,key)=>{
    const known={amp:'&',lt:'<',gt:'>',quot:'"',apos:"'"};if(key[0]!=='#')return known[key.toLowerCase()];
    const n=key[1].toLowerCase()==='x'?parseInt(key.slice(2),16):parseInt(key.slice(1),10);return n>0&&n<=0x10ffff&&!(n>=0xd800&&n<=0xdfff)?String.fromCodePoint(n):'';
  });
}
export function parseXml(xml) {
  if(Buffer.byteLength(xml)>MAX_XML)throw Error('Oversized XML is not supported');
  const root={name:'#document',children:[],parts:[],attrs:{}},stack=[root];let offset=0,nodes=0;
  while(offset<xml.length){
    if(xml.startsWith('<!--',offset)){const end=xml.indexOf('-->',offset+4);if(end<0)throw Error('Broken XML comment');offset=end+3;continue;}
    if(xml.startsWith('<![CDATA[',offset)){const end=xml.indexOf(']]>',offset+9);if(end<0)throw Error('Broken CDATA');stack.at(-1).parts.push(xml.slice(offset+9,end));offset=end+3;continue;}
    if(xml.startsWith('<?',offset)){const end=xml.indexOf('?>',offset+2);if(end<0)throw Error('Broken XML declaration');offset=end+2;continue;}
    if(xml[offset]!=='<'){let end=xml.indexOf('<',offset);if(end<0)end=xml.length;stack.at(-1).parts.push(entities(xml.slice(offset,end)));offset=end;continue;}
    let end=offset+1,quote='';for(;end<xml.length;end++){const c=xml[end];if(quote){if(c===quote)quote='';}else if(c==='"'||c==="'")quote=c;else if(c==='>')break;}
    if(end>=xml.length)throw Error('Broken XML tag');const tag=xml.slice(offset+1,end);offset=end+1;
    if(/^!\s*(?:DOCTYPE|ENTITY)/i.test(tag))throw Error('DTD/entities are not supported');
    if(tag.startsWith('/')){const name=tag.slice(1).trim();if(stack.length<2||stack.at(-1).fullName!==name)throw Error('Mismatched XML closing tag');stack.pop();continue;}
    const match=/^([A-Za-z_][\w:.-]*)([\s\S]*?)(\/?)$/.exec(tag);if(!match)throw Error('Unsupported XML markup');
    const node={fullName:match[1],name:match[1].split(':').at(-1).toLowerCase(),attrs:{},children:[],parts:[]};
    let attributes=match[2];while(attributes.trim()){
      const a=/^\s+([A-Za-z_][\w:.-]*)\s*=\s*(["'])([\s\S]*?)\2/.exec(attributes);if(!a)throw Error('Broken XML attribute');if(Object.hasOwn(node.attrs,a[1]))throw Error('Duplicate XML attribute');node.attrs[a[1]]=entities(a[3]);attributes=attributes.slice(a[0].length);
    }
    stack.at(-1).children.push(node);stack.at(-1).parts.push(node);if(++nodes>20000)throw Error('XML node limit');if(!match[3]){stack.push(node);if(stack.length>32)throw Error('XML depth limit');}
  }
  if(stack.length!==1||root.children.length!==1||root.parts.some(x=>typeof x==='string'&&x.trim()))throw Error('Broken XML document');return root.children[0];
}
function text(node) {return node ? node.parts.map(x=>typeof x==='string'?x:text(x)).join(' ') : '';}
function child(node,name){return node.children.find(x=>x.name===name);}
function plain(value,max=400){return Array.from(entities(value.replace(/<script\b[^>]*>[\s\S]*?<\/script\s*>|<style\b[^>]*>[\s\S]*?<\/style\s*>/gi,' ').replace(/<[^>]*>/g,' ')).replace(/[\u0000-\u001f\u007f]/g,' ').replace(/\s+/g,' ').trim()).slice(0,max).join('');}
export function sourceDate(raw) {
  const value=raw.trim();
  const iso=/^(\d{4})-(\d\d)-(\d\d)T(\d\d):(\d\d)(?::(\d\d)(?:\.\d+)?)?(Z|[+-](\d\d):(\d\d))$/i.exec(value);
  const rfc=/^(?:[A-Za-z]{3},\s*)?(\d{1,2})\s+([A-Za-z]{3})\s+(\d{4})\s+(\d\d):(\d\d)(?::(\d\d))?\s+(GMT|UTC|UT|[+-](\d\d)(\d\d))$/i.exec(value);
  let year,month,day,hour,minute,second,tzh,tzm;
  if(iso){[,year,month,day,hour,minute,second,,tzh,tzm]=iso;month=Number(month)-1;}
  else if(rfc){[,day,month,year,hour,minute,second,,tzh,tzm]=rfc;month=['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec'].indexOf(month.toLowerCase());}
  else return null;
  const date=new Date(Date.UTC(+year,month,+day));
  if(+year<1000||month<0||date.getUTCMonth()!==month||date.getUTCDate()!==+day||+hour>23||+minute>59||+(second||0)>59||+(tzh||0)>23||+(tzm||0)>59)return null;
  const time=Date.parse(value);return Number.isFinite(time)?new Date(time).toISOString():null;
}
export function parseFeed(xml,source) {
  const root=parseXml(xml);let entries;
  if(root.name==='rss'){const channel=child(root,'channel');if(!channel)throw Error('RSS channel missing');entries=channel.children.filter(x=>x.name==='item');}
  else if(root.name==='feed')entries=root.children.filter(x=>x.name==='entry');else throw Error('Only RSS 2.0 and Atom feeds are supported');
  return entries.slice(0,500).map(entry=>{
    const title=plain(text(child(entry,'title')),240);let url='';const links=entry.children.filter(x=>x.name==='link');
    const link=links.find(x=>x.attrs.href&&(!x.attrs.rel||x.attrs.rel==='alternate'))||links[0];
    try{url=publicUrl(link?.attrs.href||text(link)).href;}catch{return null;}
    const date=sourceDate(text(child(entry,'pubdate')||child(entry,'published')||child(entry,'updated')||child(entry,'date')));
    if(!title||!date)return null;
    return {title,url,publishedAt:date,source:source.name,feedUrl:source.url,snippet:plain(text(child(entry,'description')||child(entry,'summary')||child(entry,'content')))};
  }).filter(Boolean);
}
export function localDay(date,timeZone){const p=new Intl.DateTimeFormat('en-CA',{timeZone,year:'numeric',month:'2-digit',day:'2-digit'}).formatToParts(date);return ['year','month','day'].map(k=>p.find(x=>x.type===k).value).join('-');}
function dayNumber(value){return Date.parse(value+'T00:00:00Z')/86400000;}
export function canonical(value){const url=publicUrl(value);for(const key of [...url.searchParams.keys()])if(/^utm_|^(?:fbclid|gclid|mc_cid|mc_eid)$/i.test(key))url.searchParams.delete(key);url.searchParams.sort();url.pathname=url.pathname.replace(/\/$/,'')||'/';return url.href;}
export function selectItems(items,{now=new Date(),days=1,timeZone='UTC',limit=8,topics=[]}={}){
  const today=localDay(now,timeZone),first=dayNumber(today)-days+1,urls=new Set(),titles=new Set(),selected=[];
  for(const item of [...items].sort((a,b)=>b.publishedAt.localeCompare(a.publishedAt))){
    const date=new Date(item.publishedAt),day=dayNumber(localDay(date,timeZone));if(day<first||day>dayNumber(today)||date.getTime()>now.getTime()+300000)continue;
    const corpus=(item.title+' '+item.snippet).normalize('NFKC').toLowerCase();
    if(topics.length&&!topics.some(topic=>{const t=topic.normalize('NFKC').toLowerCase();return /[\p{Script=Han}]/u.test(t)?corpus.includes(t):new RegExp('(^|[^\\p{L}\\p{N}])'+t.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+'($|[^\\p{L}\\p{N}])','u').test(corpus);}))continue;
    const key=canonical(item.url),title=item.title.normalize('NFKC').toLowerCase().replace(/[^\p{L}\p{N}]/gu,'');if(urls.has(key)||titles.has(title))continue;urls.add(key);titles.add(title);selected.push({...item,url:key,id:selected.length+1});if(selected.length>=limit)break;
  }
  return {date:today,startDate:new Date(first*86400000).toISOString().slice(0,10),items:selected};
}
async function noLinks(target){let current=path.resolve(target);for(;;){try{const s=await fs.lstat(current);if(s.isSymbolicLink())throw Error('Symbolic-link output paths are not supported');}catch(e){if(e.code!=='ENOENT')throw e;}const parent=path.dirname(current);if(parent===current)break;current=parent;}}
async function folder(workspace,leaf){const root=path.resolve(workspace);await noLinks(root);const info=await fs.stat(root);if(!info.isDirectory())throw Error('Workspace must be an existing directory');const dir=path.join(root,leaf);await noLinks(dir);await fs.mkdir(dir,{recursive:true});await noLinks(dir);return dir;}
async function exclusive(file,content){await noLinks(file);const handle=await fs.open(file,constants.O_WRONLY|constants.O_CREAT|constants.O_EXCL|(constants.O_NOFOLLOW||0),0o600);try{await handle.writeFile(content,'utf8');}finally{await handle.close();}}
export async function collect(options,fetcher=fetchXml){
  const sources=options.sources||SOURCES,items=[],coverage=[];
  for(let index=0;index<sources.length;index+=3)await Promise.all(sources.slice(index,index+3).map(async source=>{try{const entries=parseFeed(await fetcher(source.url),source);items.push(...entries);coverage.push({name:source.name,url:source.url,status:'ok',parsedItems:entries.length});}catch(e){coverage.push({name:source.name,url:source.url,status:'failed',error:String(e.message).replace(/[\r\n]/g,' ').slice(0,180)});}}));
  const selected=selectItems(items,options),runId=randomUUID(),dir=await folder(options.workspace,'.mochi-daily-brief');
  const evidence={schema:'mochi-daily-brief.evidence.v1',runId,generatedAt:(options.now||new Date()).toISOString(),language:options.language||'zh-CN',timeZone:options.timeZone||'UTC',days:options.days||1,limit:options.limit||8,topics:options.topics||[],...selected,coverage};
  const evidenceFile=path.join(dir,'evidence-'+runId+'.json'),draftFile=path.join(dir,'draft-'+runId+'.md');await exclusive(evidenceFile,JSON.stringify(evidence,null,2)+'\n');return {evidenceFile,draftFile,...evidence};
}
function md(value){return value.replace(/[\\`*_[\]<>]/g,'\\$&').replace(/[\r\n]/g,' ');}
export async function save({workspace,evidenceFile}){
  const dir=await folder(workspace,'.mochi-daily-brief'),resolved=path.resolve(evidenceFile);
  if(path.dirname(resolved)!==dir||!/^evidence-[a-f0-9-]{36}\.json$/.test(path.basename(resolved)))throw Error('Choose the evidence file created inside this workspace');
  await noLinks(resolved);if((await fs.stat(resolved)).size>256*1024)throw Error('Evidence file too large');const e=JSON.parse(await fs.readFile(resolved,'utf8'));
  if(e.schema!=='mochi-daily-brief.evidence.v1'||!/^\d{4}-\d\d-\d\d$/.test(e.date)||!/^\d{4}-\d\d-\d\d$/.test(e.startDate)||!['zh-CN','en'].includes(e.language)||!Array.isArray(e.items)||e.items.length>20||!Array.isArray(e.coverage)||e.coverage.length>8||path.basename(resolved)!=='evidence-'+e.runId+'.json')throw Error('Evidence format invalid');
  for(let i=0;i<e.items.length;i++){const x=e.items[i];if(x.id!==i+1||typeof x.title!=='string'||typeof x.source!=='string'||!sourceDate(x.publishedAt))throw Error('Evidence item invalid');publicUrl(x.url);}
  const english=e.language==='en',emptyText=english?'No matching dated items were found in the requested window. No news summary was invented.':'本次时间范围与主题内未找到有明确日期的内容，未编造新闻摘要。';let draft,selectedItems=e.items;
  if(!e.items.length)draft=emptyText;
  else{
    const draftFile=path.join(dir,'draft-'+e.runId+'.md');await noLinks(draftFile);if((await fs.stat(draftFile)).size>50000)throw Error('Draft too large');draft=(await fs.readFile(draftFile,'utf8')).trim();
    if(draft==='NO_MATCHING_ITEMS'){draft=emptyText;selectedItems=[];}
    else{
      const refs=[...draft.matchAll(/\[(\d+)\]/g)].map(x=>Number(x[1]));if(!draft||!refs.length||refs.some(n=>n<1||n>e.items.length)||/https?:\/\/|<[^>]*>|!?\[[^\]\n]*\]\s*\(/i.test(draft))throw Error('Draft must use valid [source-number] references, without raw URLs, Markdown links or HTML');
      selectedItems=e.items.filter(x=>refs.includes(x.id));
    }
  }
  const failed=e.coverage.filter(x=>x.status!=='ok');const lines=['<!-- mochi-daily-brief:v1 '+e.runId+' -->','# '+(english?'My Daily Brief':'我的每日简报')+' · '+e.date,'',`- ${english?'Window':'时间范围'}: ${e.startDate} — ${e.date} (${md(e.timeZone)})`,`- ${english?'Collected':'采集时间'}: ${e.generatedAt}`,`- ${english?'Feed coverage':'订阅源状态'}: ${e.coverage.length-failed.length}/${e.coverage.length} ${english?'successful':'可用'}`,'',draft,'','## '+(english?'Sources and dates':'来源与日期'),''];
  for(const item of selectedItems)lines.push(`- [${item.id}] [${md(item.title)}](${item.url.replace(/\(/g,'%28').replace(/\)/g,'%29')}) — ${md(item.source)} · ${item.publishedAt}`);
  if(!selectedItems.length)lines.push(english?'No eligible items.':'没有符合条件的条目。');
  if(failed.length){lines.push('','## '+(english?'Collection limitations':'采集限制'),'');for(const source of failed)lines.push('- '+md(source.name)+': '+md(source.error||'Unavailable'));}
  lines.push('',english?'Based on RSS/Atom metadata and short excerpts, not full-article verification. Feeds may be delayed or incomplete.':'依据 RSS/Atom 的日期、元数据与短摘录整理，未逐篇核验全文；订阅源可能延迟或不完整。','');
  const output=await folder(workspace,'daily-briefs'),file=path.join(output,e.date+'-'+e.language+'-'+e.runId+'.md');await exclusive(file,lines.join('\n'));return {file,items:selectedItems.length,collectedItems:e.items.length,failedSources:failed.length};
}
function integer(value,min,max,name){if(!/^\d+$/.test(value)||Number(value)<min||Number(value)>max)throw Error(name+' is out of range');return Number(value);}
export async function main(argv){
  const [command,...args]=argv,options={days:1,limit:8,timeZone:'UTC',language:'zh-CN',topics:[]};
  if(command==='help'||command==='--help'||!command){console.log('collect --workspace PATH [--days 1..30] [--limit 1..20] [--timezone IANA] [--language zh-CN|en] [--topics AI,security] [--feeds FILE]\nsave --workspace PATH --evidence FILE\nUses public RSS/Atom only; no schedule, model API call, or message delivery.');return;}
  const seen=new Set();for(let i=0;i<args.length;i+=2){const key=args[i],value=args[i+1];if(!value||seen.has(key))throw Error('Missing or duplicate option');seen.add(key);if(key==='--workspace')options.workspace=path.resolve(value);else if(key==='--days')options.days=integer(value,1,30,'days');else if(key==='--limit')options.limit=integer(value,1,20,'limit');else if(key==='--timezone')options.timeZone=value;else if(key==='--language')options.language=value;else if(key==='--topics')options.topics=value.split(',').map(x=>x.trim()).filter(Boolean);else if(key==='--feeds')options.feeds=value;else if(key==='--evidence')options.evidenceFile=value;else throw Error('Unknown option: '+key);}
  if(!options.workspace)throw Error('--workspace is required');if(!['zh-CN','en'].includes(options.language)||options.topics.length>8||options.topics.some(x=>x.length>60))throw Error('Invalid language or topic limit');localDay(new Date(),options.timeZone);
  if(command==='save'){if(!options.evidenceFile||[...seen].some(x=>!['--workspace','--evidence'].includes(x)))throw Error('save accepts workspace and evidence only');console.log(JSON.stringify(await save(options),null,2));return;}
  if(command!=='collect'||options.evidenceFile)throw Error('Use collect or save');
  if(options.feeds){if((await fs.stat(options.feeds)).size>16000)throw Error('Feed configuration too large');options.sources=JSON.parse(await fs.readFile(options.feeds,'utf8'));if(!Array.isArray(options.sources)||!options.sources.length||options.sources.length>8||options.sources.some(x=>!x||typeof x.name!=='string'||!x.name.trim()||x.name.length>100||typeof x.url!=='string'))throw Error('Use one to eight named feeds');for(const x of options.sources)publicUrl(x.url);}
  console.log(JSON.stringify(await collect(options),null,2));
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url))main(process.argv.slice(2)).catch(error=>{console.error('Daily brief stopped: '+error.message);process.exitCode=1;});
