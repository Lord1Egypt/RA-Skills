import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs/promises';import path from 'node:path';import os from 'node:os';
import {inspect,check} from '../scripts/site-check.mjs';
const temp=()=>fs.mkdtemp(path.join(os.tmpdir(),'mochi-site-check-test-'));
const response=(url,html,status=200)=>({requestedUrl:url,finalUrl:url,status,elapsedMs:25,redirects:[],tlsValidated:true,contentType:'text/html; charset=utf-8',body:Buffer.from(html)});
test('metadata parsing uses static HTML and reports real bounded GET observations',()=>{
 const r=inspect(response('https://example.org/path','<title>A &amp; B</title><meta content="A description" name="description"><meta name="robots" content="noindex, nofollow"><link href="/canonical" rel="canonical">'));
 assert.equal(r.status,200);assert.equal(r.title,'A & B');assert.equal(r.description,'A description');assert.equal(r.robots,'noindex, nofollow');assert.equal(r.canonical,'https://example.org/canonical');assert.equal(r.tlsValidated,true);assert.deepEqual(r.findings,[]);
});
test('unsafe canonicals are omitted, nonHTML and bad UTF8 are not invented metadata',()=>{
 const r=inspect(response('https://example.org/','<link rel="canonical" href="https://example.org/?token=secret">',404));assert.equal(r.canonical,null);assert.ok(r.findings.includes('HTTP status is outside 2xx'));assert.match(r.findings.join(','),/Canonical is not/);assert.equal(r.robots,null);
 assert.match(inspect({...response('https://example.org/','{}'),contentType:'application/json'}).findings.join(','),/Not an HTML/);assert.match(inspect({...response('https://example.org/',''),body:Buffer.from([0xff])}).findings.join(','),/UTF-8/);
});
test('one-off check retains successful and failed results, caps concurrency and escapes Markdown',async()=>{
 const workspace=await temp(),urlsFile=path.join(workspace,'urls.json');await fs.writeFile(urlsFile,JSON.stringify(['https://example.org/a','https://example.org/b','https://example.org/c']));let active=0,max=0;
 const out=await check({workspace,urlsFile,lang:'en'},async url=>{active++;max=Math.max(max,active);await new Promise(r=>setTimeout(r,5));active--;if(url.endsWith('/b'))throw Error('CERT_HAS_EXPIRED');return response(url,'<title>&lt;img src=x onerror=x&gt; | ```</title>');});assert.ok(max<=2);assert.equal(out.results.length,3);assert.equal(out.results[1].status,null);assert.equal(out.results[1].tlsValidated,null);
 const md=await fs.readFile(out.markdownFile,'utf8');assert.match(md,/CERT\\_HAS\\_EXPIRED/);assert.match(md,/\\<img/);assert.match(md,/\\\|/);assert.match(md,/\\`\\`\\`/);const raw=JSON.parse(await fs.readFile(out.jsonFile,'utf8'));assert.match(raw.results[0].title,/<img/);assert.equal(raw.results[0].description,'');
});
test('inputs are explicit and all validated before network; no crawling or bypass flags',async()=>{
 const workspace=await temp(),urlsFile=path.join(workspace,'urls.json');let calls=0;const fetcher=async()=>{calls++;throw Error('Should not run');};await fs.writeFile(urlsFile,'["https://example.org/","http://example.org/private"]');await assert.rejects(check({workspace,urlsFile},fetcher));assert.equal(calls,0);
 await fs.writeFile(urlsFile,JSON.stringify(Array(6).fill('https://example.org/')));await assert.rejects(check({workspace,urlsFile},fetcher),/one to five/);assert.equal(calls,0);
});
test('Chinese human-readable report localizes missing fields and errors without altering raw evidence',async()=>{
 const workspace=await temp(),urlsFile=path.join(workspace,'urls.json');await fs.writeFile(urlsFile,'["https://example.org/","https://example.org/error"]');const out=await check({workspace,urlsFile,lang:'zh-CN'},async url=>{if(url.endsWith('/error'))throw Error('CERT_HAS_EXPIRED');return response(url,'<title>Original publisher title</title>');});
 const md=await fs.readFile(out.markdownFile,'utf8');assert.match(md,/未找到 description 元信息/);assert.match(md,/未找到可用的 canonical/);assert.match(md,/HTML 未声明/);assert.match(md,/证书已过期/);assert.doesNotMatch(md,/not found|No meta description|Observations/);assert.match(md,/Original publisher title/);assert.deepEqual(out.results[0].findings,['No meta description found','No usable canonical found']);assert.equal(out.results[1].error,'CERT_HAS_EXPIRED');
});
