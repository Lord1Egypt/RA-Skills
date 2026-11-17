#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {pathToFileURL} from 'node:url';
import {openWorkspace,hash,now,writeJson,entitlement} from './core.mjs';
import {context,loadMap,identity} from './browser.mjs';
import {acquireWriter} from './licensing.mjs';

export function contentHash(d){return hash({hotel_id:d.hotel_id,title:d.title,body:d.body,assets:d.assets.map(a=>({hash:a.hash,alt:a.alt})),ai_label:d.ai_label});}
export async function noteOperation(w,file,operation,expectedHash){
  const d=JSON.parse(fs.readFileSync(file)),cfg=JSON.parse(fs.readFileSync(path.join(w.base,'hotel.json')));
  if(d.hotel_id!==cfg.hotel_id)throw Error('HOTEL_MISMATCH');
  if(['approve','upload','save','submit'].includes(operation)&&entitlement(w.base,d.hotel_id).plan!=='SUPREME')throw Error('SUPREME_REQUIRED');
  if(operation==='approve'){
    if(expectedHash!==contentHash(d))throw Error('CONTENT_CHANGED');
    d.approval={content_hash:expectedHash,valid_until:new Date(Date.now()+86400000).toISOString(),hotel_id:d.hotel_id};writeJson(file,d);return {status:'APPROVED',content_hash:expectedHash};
  }
  if(operation==='hash')return {content_hash:contentHash(d),status:d.status};
  const m=loadMap(w.base,'content'),n=m.note;
  if(m.hotel_id!==d.hotel_id||!n?.editor_url)throw Error('NEEDS_NOTE_MAPPING');
  if(!['open','upload','save','submit','readback','public'].includes(operation))throw Error('INVALID_NOTE_OPERATION');
  if(['upload','save','submit'].includes(operation)&&w.db.prepare("SELECT value FROM settings WHERE key='paused'").get()?.value==='1')throw Error('WRITE_PAUSED');
  if(['upload','save','submit'].includes(operation)){
    if(d.approval?.content_hash!==contentHash(d)||Date.parse(d.approval?.valid_until)<=Date.now())throw Error('FINAL_CONTENT_APPROVAL_REQUIRED');
    if(['SUBMITTED','UNDER_REVIEW','PUBLISHED_VERIFIED','UNKNOWN'].includes(d.status))throw Error('READBACK_BEFORE_RETRY');
    for(const a of d.assets){if(hash(fs.readFileSync(a.path))!==a.hash)throw Error('ASSET_CHANGED');const meta=w.db.prepare('SELECT * FROM assets WHERE hash=? AND status=?').get(a.hash,'ELIGIBLE');if(!meta||JSON.parse(meta.metadata).hotel_id!==d.hotel_id)throw Error('ASSET_RIGHTS_REQUIRED');}
  }
  const url=operation==='public'?d.public_url:['readback'].includes(operation)?d.backend_url:(d.backend_url||n.editor_url);
  const u=new URL(url);if(u.protocol!=='https:'||!['we.ctrip.com','you.ctrip.com'].includes(u.hostname)||operation!=='public'&&u.hostname!=='we.ctrip.com')throw Error('INVALID_NOTE_URL');
  const owner=crypto.randomUUID();try{w.db.prepare('INSERT INTO locks VALUES(?,?,?)').run(d.hotel_id,owner,now());}catch{throw Error('HOTEL_WRITER_BUSY');}
  let ctx,lease,submitted=false;const evidence={operation,observed_at:now(),account_id:m.account_id,hotel_id:d.hotel_id,content_hash:contentHash(d)};
  try{
    if(['upload','save','submit'].includes(operation))lease=await acquireWriter(w);
    ctx=await context(w.base,'content');const page=ctx.pages()[0]||await ctx.newPage();await page.goto(url,{waitUntil:'domcontentloaded'});if(operation!=='public')await identity(page,m,'content');
    if(operation==='open'){if(!n.title||!n.body)throw Error('EDITOR_FIELDS_UNMAPPED');await page.locator(n.title).waitFor();await page.locator(n.body).waitFor();evidence.status='LIVE_READ_PASS';}
    if(['upload','save','submit'].includes(operation)){
      if(!n.title||!n.body||!n.upload)throw Error('NOTE_FIELDS_UNMAPPED');await lease.assert();await page.locator(n.title).fill(d.title);await lease.assert();await page.locator(n.body).fill(d.body);await lease.assert();await page.locator(n.upload).setInputFiles(d.assets.map(a=>a.path));
      if(!n.upload_success)throw Error('UPLOAD_READBACK_UNMAPPED');await page.locator(n.upload_success).waitFor({timeout:30000});evidence.upload='LIVE_WRITE_PASS';
      if(n.ai_disclosure){await lease.assert();await page.locator(n.ai_disclosure).check();}
      if(operation==='save'||operation==='submit'){
        const button=operation==='save'?n.save:n.submit;if(!button)throw Error('SUBMIT_UNMAPPED');await identity(page,m,'content');if(lease)await lease.assert();submitted=true;d.status='UNKNOWN';writeJson(file,d);await page.locator(button).click();
        if(!n.object_id||!n.backend_link)throw Error('OBJECT_READBACK_UNMAPPED');await page.locator(n.object_id).waitFor();d.platform_object_id=(await page.locator(n.object_id).innerText()).trim();
        const href=await page.locator(n.backend_link).getAttribute('href');d.backend_url=new URL(href,page.url()).href;d.status=operation==='save'?'DRAFT_SAVED':'SUBMITTED';d.publish_status=operation==='save'?'NOT_SUBMITTED':'SUBMITTED';evidence.object_id=d.platform_object_id;evidence.status='LIVE_WRITE_PASS';
      }else evidence.status='LIVE_WRITE_PASS';
    }
    if(operation==='readback'||operation==='public'){
      const r=operation==='public'?n.public:n.readback;if(!d.platform_object_id||!r?.object_id||!r?.title||!r?.status)throw Error('OBJECT_READBACK_UNMAPPED');
      const id=(await page.locator(r.object_id).innerText()).trim(),title=(await page.locator(r.title).innerText()).trim();
      if(id!==d.platform_object_id||title!==d.title)throw Error('READBACK_OBJECT_MISMATCH');
      const observed=(await page.locator(r.status).innerText()).trim();const mapped=r.states?.[observed];if(!mapped)throw Error('UNKNOWN_PLATFORM_STATUS');
      if(operation==='public'){
        if(mapped!=='PUBLISHED_VERIFIED'||!r.body)throw Error('PUBLIC_NOT_VERIFIED');const body=(await page.locator(r.body).innerText()).replace(/\s+/g,'');if(body!==d.body.replace(/\s+/g,''))throw Error('READBACK_CONTENT_MISMATCH');d.status='PUBLISHED_VERIFIED';d.publish_status='PUBLISHED_VERIFIED';evidence.status='PUBLIC_READBACK_PASS';
      }else{if(!['SUBMITTED','UNDER_REVIEW','REJECTED','DRAFT_SAVED'].includes(mapped))throw Error('INVALID_BACKEND_STATE');d.status=mapped;evidence.status='BACKEND_READBACK_PASS';if(r.public_link){const href=await page.locator(r.public_link).getAttribute('href');if(href)d.public_url=new URL(href,page.url()).href;}}
      evidence.object_id=id;evidence.platform_status=observed;
    }
    d.evidence=[...(d.evidence||[]),evidence];writeJson(file,d);return evidence;
  }catch(e){const status=submitted?'UNKNOWN':'FAILED';d.evidence=[...(d.evidence||[]),{...evidence,status,error:e.message}];if(submitted){d.status='UNKNOWN';d.publish_status='UNKNOWN';}writeJson(file,d);return {...evidence,status,error:e.message};}
  finally{if(ctx)await ctx.close();if(lease)await lease.release();w.db.prepare('DELETE FROM locks WHERE hotel_id=? AND owner=?').run(d.hotel_id,owner);}
}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href){const {args}=await import('./ops.mjs');const a=args(process.argv.slice(2)),w=openWorkspace(a.workspace);try{console.log(JSON.stringify(await noteOperation(w,path.resolve(a.file),a._[0],a.hash),null,2));}catch(e){console.error(JSON.stringify({status:'FAILED',error:e.message}));process.exitCode=1;}finally{w.close();}}
