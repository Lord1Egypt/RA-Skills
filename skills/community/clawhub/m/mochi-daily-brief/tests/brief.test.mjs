import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import https from 'node:https';
import { EventEmitter } from 'node:events';
import { Readable } from 'node:stream';
import { gzipSync } from 'node:zlib';
import { publicAddress,publicUrl,fetchXml,parseXml,parseFeed,sourceDate,localDay,canonical,selectItems,collect,save,main } from '../scripts/brief.mjs';

const source={name:'Fixture official feed',url:'https://news.example.com/rss.xml'};
const now=new Date('2026-10-22T01:00:00Z');
const item=(title='AI model update',date='2026-10-21T17:00:00.000Z',url='https://news.example.com/a')=>({title,publishedAt:date,url,snippet:'A factual excerpt.',source:source.name,feedUrl:source.url});
const rss=(title='AI model update',date='Wed, 21 Oct 2026 17:00:00 GMT')=>`<?xml version="1.0"?><rss version="2.0"><channel><item><title>${title}</title><link>https://news.example.com/a?utm_source=test</link><pubDate>${date}</pubDate><description><![CDATA[<p>AI tools &amp; safety.</p><script>doNotExecute()</script>]]></description></item></channel></rss>`;
async function temporary(t){const dir=await fs.mkdtemp(path.join(os.tmpdir(),'mochi-brief-test-'));t.after(()=>fs.rm(dir,{recursive:true,force:true}));return dir;}
const options=workspace=>({workspace,now,days:2,timeZone:'Asia/Shanghai',language:'en',limit:8,topics:[],sources:[source]});

test('public networking rejects loopback, private, metadata, documentation, transition and reserved addresses',()=>{
  for(const ip of ['127.0.0.1','10.0.0.4','172.31.9.1','192.168.0.1','169.254.169.254','100.64.0.1','192.0.0.8','192.0.2.1','198.18.1.1','198.51.100.1','203.0.113.8','224.0.0.1','255.255.255.255','::1','fc00::1','fe80::1','::ffff:127.0.0.1','2001:db8::1','2001:20::1','2002:7f00:1::','3fff::1'])assert.equal(publicAddress(ip),false,ip);
  for(const ip of ['8.8.8.8','192.0.66.2','104.18.28.7','2606:4700:4700::1111','2001:4860:4860::8888'])assert.equal(publicAddress(ip),true,ip);
});
test('feed and article URLs require public HTTPS domain, no credentials, custom ports or malformed host',()=>{
  for(const url of ['http://example.com/rss','https://localhost/a','https://x.internal/a','https://127.0.0.1/a','https://[::1]/','https://example.com:8443/','https://user:pass@example.com/','https://example.com\\@evil.com/','https://example.com/\nabc','file:///etc/passwd','javascript:alert(1)'])assert.throws(()=>publicUrl(url),undefined,url);
  assert.equal(publicUrl('https://news.example.com/a#part').href,'https://news.example.com/a');
});
test('mixed public and private DNS answers fail before a request',async()=>{
  await assert.rejects(fetchXml(source.url,{lookup:async()=>[{address:'8.8.8.8',family:4},{address:'10.0.0.4',family:4}]}),/non-public/);
});
function transport(t,responses){let count=0;const calls=[];const original=https.get;
  https.get=(url,settings,callback)=>{calls.push({url:String(url),settings});const req=new EventEmitter();req.destroy=error=>{if(error)req.emit('error',error);req.emit('close');};
    const reply=responses[Math.min(count++,responses.length-1)];setImmediate(()=>{const response=Readable.from([reply.body??'']);response.statusCode=reply.status??200;response.headers=reply.headers??{};response.on('end',()=>req.emit('close'));response.on('close',()=>req.emit('close'));callback(response);});return req;};
  t.after(()=>{https.get=original;});return calls;
}
test('HTTPS transport pins a validated address, keeps TLS validation and supports gzip',async t=>{
  const calls=transport(t,[{body:gzipSync(Buffer.from(rss())),headers:{'content-encoding':'gzip'}}]);
  const xml=await fetchXml(source.url,{lookup:async()=>[{address:'8.8.8.8',family:4}]});assert.equal(parseFeed(xml,source).length,1);
  assert.equal(calls[0].settings.rejectUnauthorized,true);assert.equal(calls[0].settings.agent,false);
  calls[0].settings.lookup('other.invalid',{all:true},(error,addresses)=>{assert.equal(error,null);assert.deepEqual(addresses,[{address:'8.8.8.8',family:4}]);});
});
test('redirects recheck DNS and never connect to private destinations',async t=>{
  const calls=transport(t,[{status:302,headers:{location:'https://private.example.com/feed'}}]);
  await assert.rejects(fetchXml(source.url,{lookup:async host=>[{address:host.startsWith('private')?'10.1.2.3':'8.8.8.8',family:4}]}),/non-public/);assert.equal(calls.length,1);
});
test('redirects cannot downgrade to HTTP or continue indefinitely',async t=>{
  const calls=transport(t,[{status:302,headers:{location:'http://news.example.com/feed'}}]);
  await assert.rejects(fetchXml(source.url,{lookup:async()=>[{address:'8.8.8.8',family:4}]}),/HTTPS/);assert.equal(calls.length,1);
});
test('redirect count has a hard bound',async t=>{
  const calls=transport(t,[{status:302,headers:{location:'/next'}}]);await assert.rejects(fetchXml(source.url,{lookup:async()=>[{address:'8.8.8.8',family:4}]}),/Redirect limit/);assert.equal(calls.length,4);
});
test('wire byte limit stops oversized feeds',async t=>{
  transport(t,[{body:Buffer.alloc(1024*1024+1,65)}]);await assert.rejects(fetchXml(source.url,{lookup:async()=>[{address:'8.8.8.8',family:4}]}),/byte limit/);
});
test('decompressed byte limit stops compressed expansion',async t=>{
  transport(t,[{body:gzipSync(Buffer.alloc(2*1024*1024+1,65)),headers:{'content-encoding':'gzip'}}]);await assert.rejects(fetchXml(source.url,{lookup:async()=>[{address:'8.8.8.8',family:4}]}),/XML byte limit/);
});
test('bad UTF-8 fails explicitly',async t=>{
  transport(t,[{body:Buffer.from([255,255])}]);await assert.rejects(fetchXml(source.url,{lookup:async()=>[{address:'8.8.8.8',family:4}]}),/UTF-8/);
});
test('broken compressed data fails explicitly',async t=>{
  transport(t,[{body:Buffer.from('not gzip'),headers:{'content-encoding':'gzip'}}]);await assert.rejects(fetchXml(source.url,{lookup:async()=>[{address:'8.8.8.8',family:4}]}),/header|compression|gzip/i);
});
test('RSS normalizes dates, strips HTML/scripts and decodes entities',()=>{
  const entries=parseFeed(rss('AI &amp; safety'),source);assert.equal(entries.length,1);assert.equal(entries[0].title,'AI & safety');assert.equal(entries[0].publishedAt,'2026-10-21T17:00:00.000Z');assert.equal(entries[0].snippet,'AI tools & safety.');
});
test('Atom namespaces, alternate links, summary and mixed inline text work',()=>{
  const xml='<feed xmlns="http://www.w3.org/2005/Atom"><entry><title>AI <b>model</b> update</title><link rel="self" href="https://news.example.com/self"/><link rel="alternate" href="https://news.example.com/article"/><updated>2026-10-22T08:00:00+08:00</updated><summary>Useful summary</summary></entry></feed>';
  const [entry]=parseFeed(xml,source);assert.equal(entry.title,'AI model update');assert.equal(entry.url,'https://news.example.com/article');assert.equal(entry.publishedAt,'2026-10-22T00:00:00.000Z');
});
test('XML rejects actual DTD/entity definitions but permits inert HTML doctype inside CDATA',()=>{
  assert.throws(()=>parseXml('<!DOCTYPE rss [<!ENTITY leak SYSTEM "file:///etc/passwd">]><rss/>'),/DTD/);
  assert.equal(parseFeed(rss().replace('<p>','<!DOCTYPE html><p>'),source).length,1);
});
test('XML rejects broken structure, duplicate attributes, oversized and excessively nested content',()=>{
  for(const xml of ['<rss><channel></rss>','<rss a="1" a="2"/>','outside<rss/>','<rss/><feed/>','<rss><!ENTITY x "y"></rss>','<rss/> trailing','<rss>'+ '<x>'.repeat(40)+'</x>'.repeat(40)+'</rss>'])assert.throws(()=>parseXml(xml));
  assert.throws(()=>parseXml('a'.repeat(2*1024*1024+1)),/Oversized/);
});
test('undated, invalid-date and non-HTTPS article entries are omitted rather than invented',()=>{
  assert.equal(parseFeed(rss().replace('Wed, 21 Oct 2026 17:00:00 GMT','yesterday'),source).length,0);
  assert.equal(parseFeed(rss().replace('https://news.example.com/a','http://news.example.com/a'),source).length,0);
  assert.equal(sourceDate('2026-02-30T00:00:00Z'),null);assert.equal(sourceDate('2026-10-22T10:00:00'),null);
  assert.equal(sourceDate('2026-10-22T24:00:00Z'),null);assert.equal(sourceDate('Fri, 30 Feb 2026 12:00:00 GMT'),null);
});
test('time-window uses calendar days in chosen timezone, not UTC or a rolling duration',()=>{
  const records=[item('Early local today','2026-10-21T16:01:00.000Z'),item('Local yesterday','2026-10-21T15:59:00.000Z','https://news.example.com/b')];
  assert.equal(selectItems(records,{now,days:1,timeZone:'Asia/Shanghai'}).items.length,1);assert.equal(selectItems(records,{now,days:1,timeZone:'UTC'}).items.length,0);assert.equal(selectItems(records,{now,days:2,timeZone:'Asia/Shanghai'}).items.length,2);
  assert.equal(localDay(new Date('2026-03-08T07:01:00Z'),'America/New_York'),'2026-03-08');assert.equal(selectItems([],{now:new Date('2026-03-09T00:00:00Z'),days:2,timeZone:'America/New_York'}).startDate,'2026-03-07');
});
test('future items are excluded, chronological order and limit are deterministic',()=>{
  const records=[item('Future','2026-10-22T02:00:00.000Z'),item('Second','2026-10-22T00:00:00.000Z','https://news.example.com/b'),item('First','2026-10-22T00:30:00.000Z','https://news.example.com/c')];
  const selected=selectItems(records,{now,days:2,limit:1});assert.deepEqual(selected.items.map(x=>x.title),['First']);assert.equal(selected.items[0].id,1);
});
test('tracking parameters, fragments, query order and normalized headlines deduplicate',()=>{
  assert.equal(canonical('https://news.example.com/a/?b=2&utm_source=x&a=1#part'),'https://news.example.com/a?a=1&b=2');
  const records=[item('AI model update'),item('A different title',undefined,'https://news.example.com/a?utm_medium=rss'),item('AI: Model Update!',undefined,'https://news.example.com/c')];assert.equal(selectItems(records,{now,days:2}).items.length,1);
});
test('topic matching is OR, respects Latin word boundaries and supports Chinese',()=>{
  const records=[item('Daily tools'),item('AI release',undefined,'https://news.example.com/b'),item('开源模型升级',undefined,'https://news.example.com/c')];
  assert.deepEqual(selectItems(records,{now,days:2,topics:['AI','开源']}).items.map(x=>x.title),['AI release','开源模型升级']);
});
test('collect records partial source failure and preserves provenance without changing workspace files',async t=>{
  const workspace=await temporary(t);await fs.writeFile(path.join(workspace,'notes.md'),'Keep me');const o=options(workspace);o.sources.push({name:'Broken feed',url:'https://broken.example.com/rss'});
  const e=await collect(o,async url=>url===source.url?rss():'<rss>broken');assert.equal(e.items.length,1);assert.equal(e.coverage.filter(x=>x.status==='failed').length,1);assert.equal(e.items[0].source,source.name);assert.equal(await fs.readFile(path.join(workspace,'notes.md'),'utf8'),'Keep me');assert.equal(JSON.parse(await fs.readFile(e.evidenceFile,'utf8')).runId,e.runId);
});
test('save writes cited Markdown with deterministic source dates and failure disclosure',async t=>{
  const workspace=await temporary(t);const e=await collect(options(workspace),async()=>rss());await fs.writeFile(e.draftFile,'## Highlights\n\n- An AI update was announced. [1]\n\n## Interpretation\n\nReview the original announcement before choosing tools. [1]');
  const result=await save({workspace,evidenceFile:e.evidenceFile});const markdown=await fs.readFile(result.file,'utf8');assert.match(markdown,/An AI update/);assert.match(markdown,/Sources and dates/);assert.match(markdown,/2026-10-21T17:00:00.000Z/);assert.match(markdown,/Asia\/Shanghai/);assert.match(markdown,/https:\/\/news.example.com\/a/);assert.match(markdown,/not full-article verification/);
});
test('no matching content produces an honest result without reading a fabricated model draft',async t=>{
  const workspace=await temporary(t);const e=await collect({...options(workspace),topics:['quantum']},async()=>rss());assert.equal(e.items.length,0);await fs.writeFile(e.draftFile,'A fabricated major event happened.');const result=await save({workspace,evidenceFile:e.evidenceFile});const text=await fs.readFile(result.file,'utf8');assert.match(text,/No matching dated items/);assert.doesNotMatch(text,/fabricated major event/);
});
test('semantic exclusions remove uncited candidates from the final source appendix',async t=>{
  const workspace=await temporary(t);const xml=rss().replace('</channel>','<item><title>Unrelated biology tools</title><link>https://news.example.com/biology</link><pubDate>Wed, 21 Oct 2026 16:00:00 GMT</pubDate></item></channel>');const e=await collect(options(workspace),async()=>xml);assert.equal(e.items.length,2);await fs.writeFile(e.draftFile,'An AI model update was announced. [1]');const result=await save({workspace,evidenceFile:e.evidenceFile});const markdown=await fs.readFile(result.file,'utf8');assert.equal(result.items,1);assert.equal(result.collectedItems,2);assert.doesNotMatch(markdown,/Unrelated biology/);assert.match(markdown,/- \[1\]/);
});
test('all semantically rejected candidates produce a deterministic empty report',async t=>{
  const workspace=await temporary(t);const e=await collect(options(workspace),async()=>rss());await fs.writeFile(e.draftFile,'NO_MATCHING_ITEMS');const result=await save({workspace,evidenceFile:e.evidenceFile});const markdown=await fs.readFile(result.file,'utf8');assert.equal(result.items,0);assert.equal(result.collectedItems,1);assert.match(markdown,/No matching dated items/);assert.doesNotMatch(markdown,/AI model update/);
});
test('all failed sources are clearly disclosed and never imply the world had no news',async t=>{
  const workspace=await temporary(t);const e=await collect(options(workspace),async()=>{throw Error('Network timeout');});const result=await save({workspace,evidenceFile:e.evidenceFile});const text=await fs.readFile(result.file,'utf8');assert.match(text,/0\/1 successful/);assert.match(text,/Network timeout/);assert.equal(result.failedSources,1);
});
test('save never overwrites an existing report, including an unrelated same-name file',async t=>{
  const workspace=await temporary(t);const e=await collect(options(workspace),async()=>rss());await fs.writeFile(e.draftFile,'A short summary. [1]');const output=path.join(workspace,'daily-briefs');await fs.mkdir(output);const expected=path.join(output,`${e.date}-${e.language}-${e.runId}.md`);await fs.writeFile(expected,'Unrelated original file');await assert.rejects(save({workspace,evidenceFile:e.evidenceFile}),/EEXIST/);assert.equal(await fs.readFile(expected,'utf8'),'Unrelated original file');
});
test('save rejects missing, invalid-reference, URL-bearing or HTML drafts',async t=>{
  const workspace=await temporary(t);const e=await collect(options(workspace),async()=>rss());await assert.rejects(save({workspace,evidenceFile:e.evidenceFile}),/ENOENT/);
  for(const draft of ['Unsupported facts. [99]','No source citation.','[1] https://evil.example.com','<script>bad()</script> [1]','[1] [click](javascript:alert(1))','[1] ![image](file:///etc/passwd)']){await fs.writeFile(e.draftFile,draft);await assert.rejects(save({workspace,evidenceFile:e.evidenceFile}),/valid/);}
});
test('evidence from another workspace and symlink output directories are refused',async t=>{
  const workspace=await temporary(t),other=await temporary(t);const e=await collect(options(workspace),async()=>rss());await fs.writeFile(e.draftFile,'Cited fact. [1]');await assert.rejects(save({workspace:other,evidenceFile:e.evidenceFile}),/inside this workspace/);
  await fs.symlink(other,path.join(workspace,'daily-briefs'),process.platform==='win32'?'junction':'dir');await assert.rejects(save({workspace,evidenceFile:e.evidenceFile}),/Symbolic-link/);assert.equal((await fs.readdir(other)).filter(x=>x.endsWith('.md')).length,0);
});
test('CLI rejects malformed options without networking or creating output',async t=>{
  const workspace=await temporary(t);
  for(const args of [['collect','--workspace',workspace,'--days','0'],['collect','--workspace',workspace,'--timezone','Moon/Sea'],['collect','--workspace',workspace,'--limit','21'],['collect','--workspace',workspace,'--language','unknown'],['collect','--workspace',workspace,'--workspace',workspace],['collect','--workspace',workspace,'--extra','x']])await assert.rejects(main(args));
  assert.deepEqual(await fs.readdir(workspace),[]);
});
