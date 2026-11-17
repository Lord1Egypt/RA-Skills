import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, readFile, stat, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { ImagenClient, saveKey, readKey } from './client.mjs';
import { startPanel } from './panel.mjs';

const id = 'a'.repeat(32), key = 'img_live_' + 'b'.repeat(64);
const json = data => new Response(JSON.stringify(data), { headers: { 'content-type':'application/json' } });
async function temporary(t) { const dir = await mkdtemp(path.join(tmpdir(),'imagen-skill-')); t.after(()=>rm(dir,{recursive:true,force:true})); return dir; }

test('credentials are owner-only and invalid keys do not replace them',async t=>{
 const dir=await temporary(t), file=path.join(dir,'key.json');
 await saveKey(key,file); assert.equal(await readKey(file),key);
 assert.equal((await stat(file)).mode & 0o777,0o600);
 await assert.rejects(()=>saveKey('provider-secret',file)); assert.equal(await readKey(file),key);
});
test('no budget means no unlock; retry keys stay stable; original URL stays out of output',async t=>{
 const dir=await temporary(t), file=path.join(dir,'key.json'); await saveKey(key,file);
 const calls=[];
 const client=new ImagenClient({keyFile:file,fetcher:async(url,options)=>{
  calls.push({url,options});
  if(url.endsWith('/entitlement')) return json({unlocked:false});
  if(url.endsWith('/unlock')) return json({newly_unlocked:true});
  if(url.endsWith('/download')) return json({url:'https://storage.example/original?private=secret',expires_at:'soon'});
  return new Response(new Uint8Array([1,2,3]),{headers:{'content-type':'image/png'}});
 }});
 await assert.rejects(()=>client.download(id,path.join(dir,'original.png'),{original:true}),/budget/);
 assert.equal(calls.length,1);
 const result=await client.download(id,path.join(dir,'original.png'),{original:true,maxCredits:1,operationID:'stable-id'});
 assert.equal(result.credits_spent,1); assert.equal(JSON.stringify(result).includes('private=secret'),false);
 assert.deepEqual([...await readFile(result.path)],[1,2,3]);
 assert.equal(JSON.parse(calls.find(c=>c.url.endsWith('/unlock')).options.body).idempotency_key,'stable-id:unlock');
 assert.equal(calls.at(-1).options.headers,undefined,'credentials must not be sent to media origin');
 await assert.rejects(()=>client.download(id,result.path,{original:true,maxCredits:1}),/EEXIST/);
});
test('already unlocked originals do not invoke credit consumption',async t=>{
 const dir=await temporary(t); const routes=[];
 const client=new ImagenClient({keyFile:path.join(dir,'key'),fetcher:async(url)=>{routes.push(url);if(url.endsWith('/entitlement'))return json({unlocked:true});if(url.endsWith('/download'))return json({url:'https://storage.example/img'});return new Response('image',{headers:{'content-type':'image/png'}})}});
 await saveKey(key,client.keyFile);
 const result=await client.download(id,path.join(dir,'out.png'),{original:true});
 assert.equal(result.credits_spent,0);assert.equal(routes.some(r=>r.endsWith('/unlock')),false);
});
test('panel rejects foreign origins and missing sessions; persists only selected public metadata',async t=>{
 const dir=await temporary(t);const client=new ImagenClient({keyFile:path.join(dir,'key')});
 const panel=await startPanel({client,manifest:{items:[{public_id:id,title:'Test'}]},selectionFile:path.join(dir,'selection.json')});t.after(panel.close);
 const url=new URL(panel.url),base=url.origin,headers={'X-Imagen-Session':url.hash.slice(1),'Content-Type':'application/json'};
 assert.equal((await fetch(base+'/state')).status,403);
 assert.equal((await fetch(base+'/state',{headers:{...headers,Origin:'https://evil.example'}})).status,403);
 assert.equal((await fetch(base+'/state',{headers})).status,200);
 assert.equal((await fetch(base+'/selection',{method:'POST',headers,body:JSON.stringify({ids:['unknown']})})).status,400);
 assert.equal((await fetch(base+'/selection',{method:'POST',headers,body:JSON.stringify({ids:[id]})})).status,200);
 const saved=JSON.parse(await readFile(panel.selectionFile));assert.equal(saved.selected[0].public_id,id);assert.equal(JSON.stringify(saved).includes(key),false);
});

test('original-link returns expiry and charge details but never the API key', async t => {
 const dir=await temporary(t);const keyFile=path.join(dir,'key');await saveKey(key,keyFile);
 const client=new ImagenClient({keyFile,fetcher:async url=>{
  if(url.endsWith('/entitlement'))return json({unlocked:false});
  if(url.endsWith('/unlock'))return json({newly_unlocked:true});
  return json({url:'https://storage.example/original?signature=test',expires_at:'2030-01-01T00:00:00Z',downloads_used_today:1,downloads_limit_today:10});
 }});
 const result=await client.originalLink(id,{maxCredits:1,operationID:'link-request-01'});
 assert.equal(result.credits_spent,1);assert.equal(result.temporary,true);assert.equal(result.expires_at,'2030-01-01T00:00:00Z');
 assert.match(result.url,/signature=test/);assert.equal(JSON.stringify(result).includes(key),false);
 await assert.rejects(()=>client.originalLink(id,{maxCredits:1,operationID:'short'}),/operation ID/);
});

test('free search never sends a saved key and HTTP media stays loopback-only', async t => {
 const dir=await temporary(t), keyFile=path.join(dir,'key');await saveKey(key,keyFile);
 const client=new ImagenClient({keyFile,fetcher:async(url,options)=>{
  assert.equal(options.headers.Authorization,undefined);
  return json({items:[],page_info:{total:0}});
 }});
 await client.search({query:'Rome'});
 assert.throws(()=>client.validateMediaURL('http://127.0.0.1/original',true));
 const local=new ImagenClient({api:'http://localhost:18080/api/v1'});
 assert.doesNotThrow(()=>local.validateMediaURL('http://127.0.0.1:59000/file',true));
 assert.throws(()=>local.validateMediaURL('http://remote.example/file',true));
});
