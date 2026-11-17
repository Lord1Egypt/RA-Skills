#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {pathToFileURL} from 'node:url';
import {hash,now,writeJson,openWorkspace,validateSnapshot,recordAttempt,entitlement,priceProposal} from './core.mjs';
import {acquireWriter} from './licensing.mjs';

const homes={ebooking:'https://ebooking.ctrip.com/',content:'https://we.ctrip.com/publish/publishHome'};
const allowed=(url,channel)=>{const u=new URL(url);return u.protocol==='https:'&&(channel==='ebooking'?['ebooking.ctrip.com','ebooking.trip.com']:['we.ctrip.com']).includes(u.hostname);};
export async function context(base,channel){
  if(!homes[channel])throw Error('INVALID_CHANNEL');
  const {chromium}=await import('playwright');
  return chromium.launchPersistentContext(path.join(base,'profiles',channel),{channel:'chrome',headless:false,acceptDownloads:false,viewport:{width:1366,height:900}});
}
export function loadMap(base,channel) {
  const p=path.join(base,`adapter-${channel}.json`);
  if(!fs.existsSync(p))throw Error('NEEDS_ACCOUNT_MAPPING');
  const m=JSON.parse(fs.readFileSync(p));
  if(!m.account_id||!m.hotel_id||!m.identity?.account||!m.identity?.hotel||!m.verified_at||!m.evidence_reference)throw Error('MAPPING_EVIDENCE_REQUIRED');
  if(Date.now()-Date.parse(m.verified_at)>30*86400000||!Number.isFinite(Date.parse(m.verified_at)))throw Error('MAPPING_STALE');
  return m;
}
export async function identity(page,m,channel) {
  if(!allowed(page.url(),channel))throw Error('UNEXPECTED_DOMAIN');
  const account=(await page.locator(m.identity.account).innerText()).trim(),hotel=(await page.locator(m.identity.hotel).innerText()).trim();
  if(account!==m.account_label||hotel!==m.hotel_label)throw Error('ACCOUNT_OR_HOTEL_MISMATCH');
}
function parseValue(v,type){if(type==='integer'){if(!/^-?\d+$/.test(v.trim()))throw Error('INVALID_INTEGER_FIELD');return Number(v);}if(type==='fen'){const clean=v.replace(/[¥￥,\s]/g,'');if(!/^\d+(\.\d{1,2})?$/.test(clean))throw Error('INVALID_MONEY_FIELD');return Math.round(Number(clean)*100);}if(type==='boolean')return v.trim()==='true';return v.trim();}
export async function readSnapshot(w,channel='ebooking') {
  const m=loadMap(w.base,channel),conf=JSON.parse(fs.readFileSync(path.join(w.base,'hotel.json')));
  if(m.hotel_id!==conf.hotel_id)throw Error('HOTEL_MISMATCH');
  const ctx=await context(w.base,channel);
  try{
    const page=ctx.pages()[0]||await ctx.newPage();
    const s={hotel:{id:conf.hotel_id,name:conf.hotel_name},observed_at:now(),source:{type:'LIVE',account_id:m.account_id,reference:m.evidence_reference},price_authority:m.price_authority||null,inventory_authority:m.inventory_authority||null,read_failures:[]};
    for(const [domain,rule] of Object.entries(m.reads||{})){
      if(!['rooms','rates','inventory','orders','reviews','promotions','competitors','events','facts'].includes(domain))continue;
      try{
        if(!allowed(rule.url,channel))throw Error('INVALID_DOMAIN');await page.goto(rule.url,{waitUntil:'domcontentloaded'});await identity(page,m,channel);
        const rows=page.locator(rule.rows),count=await rows.count(),values=[];
        for(let i=0;i<Math.min(count,500);i++){const obj={};for(const [name,f]of Object.entries(rule.fields)){const loc=rows.nth(i).locator(f.selector);const value=f.attribute?await loc.getAttribute(f.attribute):await loc.innerText();obj[name]=parseValue(value||'',f.type);}values.push(obj);}s[domain]=values;
      }catch(e){s[domain]=null;s.read_failures.push({domain,status:'FAILED',reason:e.message});}
    }
    if(!Object.keys(m.reads||{}).length)throw Error('NO_READ_MAPPINGS');
    validateSnapshot(s,conf.hotel_id);writeJson(path.join(w.base,'snapshot.json'),s);writeJson(path.join(w.base,'snapshots',hash(s)+'.json'),s);return s;
  }finally{await ctx.close();}
}
async function executeCheckedAction(w,id) {
  const a=w.db.prepare('SELECT * FROM actions WHERE id=?').get(id);if(!a)throw Error('ACTION_NOT_FOUND');
  const p=JSON.parse(a.payload);
  if(p.environment!=='LIVE')throw Error('LIVE_SOURCE_REQUIRED');
  if(!['APPROVED','BLOCKED_RETRYABLE'].includes(a.status)||a.approval_hash!==a.content_hash||hash(p)!==a.content_hash)throw Error('FINAL_CONTENT_APPROVAL_REQUIRED');
  if(w.db.prepare("SELECT value FROM settings WHERE key='paused'").get()?.value==='1')throw Error('WRITE_PAUSED');
  if(p.eligible===false)throw Error('INELIGIBLE_ACTION');
  const conf=JSON.parse(fs.readFileSync(path.join(w.base,'hotel.json')));
  if(conf.hotel_id!==a.hotel_id)throw Error('HOTEL_MISMATCH');
  if(p.mode==='POSITIVE_OPT_IN'&&p.authorization_until&&Date.parse(p.authorization_until)<=Date.now())throw Error('AUTH_EXPIRED');
  if(p.kind==='INVENTORY'&&p.mode==='AUTOMATIC'&&entitlement(w.base,a.hotel_id).plan!=='SUPREME')throw Error('SUPREME_REQUIRED');
  const channel=p.channel||'ebooking',m=loadMap(w.base,channel);
  if(m.account_id!==p.account_id||m.hotel_id!==a.hotel_id)throw Error('ACCOUNT_OR_HOTEL_MISMATCH');
  const rule=m.writes?.[p.kind]?.[p.object_id];
  if(!rule?.url||!rule.current||!rule.input||!rule.submit||!rule.readback||!rule.identity||!rule.identity_value)throw Error('NEEDS_ACTION_MAPPING');
  if(!allowed(rule.url,channel))throw Error('INVALID_DOMAIN');
  if(p.kind==='PRICE'){
    const s=JSON.parse(fs.readFileSync(path.join(w.base,'snapshot.json')));
    const check=priceProposal(s,p.rate,p.policy,w.db.prepare('SELECT * FROM actions').all(),entitlement(w.base,a.hotel_id));if(!check.eligible)throw Error(check.errors.join(','));
  }
  const owner=crypto.randomUUID();try{w.db.prepare('INSERT INTO locks VALUES(?,?,?)').run(a.hotel_id,owner,now());}catch{throw Error('HOTEL_WRITER_BUSY');}
  let ctx,lease,clicked=false;
  try{
    if(entitlement(w.base,a.hotel_id).plan!=='FREE')lease=await acquireWriter(w);
    ctx=await context(w.base,channel);const page=ctx.pages()[0]||await ctx.newPage();await page.goto(rule.url,{waitUntil:'domcontentloaded'});await identity(page,m,channel);
    if((await page.locator(rule.identity).innerText()).trim()!==rule.identity_value)throw Error('TARGET_OBJECT_MISMATCH');
    const field=page.locator(rule.current);const raw=rule.current_is_input?await field.inputValue():await field.innerText();const before=parseValue(raw,rule.value_type);
    if(before!==p.before)throw Error('OLD_VALUE_CONFLICT');
    if(w.db.prepare("SELECT value FROM settings WHERE key='paused'").get()?.value==='1')throw Error('WRITE_PAUSED');
    const fill=rule.value_type==='fen'?(p.after/100).toFixed(2):String(p.after);
    await page.locator(rule.input).fill(fill);await identity(page,m,channel);
    if(lease)await lease.assert();
    recordAttempt(w,a,'SUBMITTING',{before,expected_after:p.after,object_id:p.object_id});clicked=true;
    await page.locator(rule.submit).click();
    if(rule.readback_url){if(!allowed(rule.readback_url,channel))throw Error('INVALID_READBACK_DOMAIN');await page.goto(rule.readback_url,{waitUntil:'domcontentloaded'});}else await page.reload({waitUntil:'domcontentloaded'});
    await identity(page,m,channel);
    if((await page.locator(rule.identity).innerText()).trim()!==rule.identity_value)throw Error('READBACK_OBJECT_MISMATCH');
    const got=page.locator(rule.readback),after=parseValue(rule.readback_is_input?await got.inputValue():await got.innerText(),rule.value_type);
    if(after!==p.after)throw Error('READBACK_MISMATCH');
    recordAttempt(w,a,'VERIFIED',{object_id:p.object_id,before,after,source_url:page.url(),observed_at:now(),public_readback:'NOT_RUN'});
    return {id,status:'LIVE_WRITE_PASS',backend_readback:'BACKEND_READBACK_PASS',public_readback:'NOT_RUN'};
  }catch(e){recordAttempt(w,a,clicked?'UNKNOWN_PENDING_READBACK':'FAILED',{reason:e.message});return {id,status:clicked?'UNKNOWN_PENDING_READBACK':'FAILED',reason:e.message};}
  finally{if(ctx)await ctx.close();if(lease)await lease.release();w.db.prepare('DELETE FROM locks WHERE hotel_id=? AND owner=?').run(a.hotel_id,owner);}
}
export async function executeAction(w,id){
  try{return await executeCheckedAction(w,id);}catch(e){
    const a=w.db.prepare('SELECT * FROM actions WHERE id=?').get(id);
    if(a){const event={reason:e.message,phase:'PREFLIGHT',remote_writes:0};
      if(['APPROVED','BLOCKED_RETRYABLE'].includes(a.status))recordAttempt(w,a,'BLOCKED_RETRYABLE',event);
      else w.db.prepare('INSERT INTO attempts(action_id,environment,status,evidence,created_at) VALUES(?,?,?,?,?)').run(a.id,JSON.parse(a.payload).environment,'PREFLIGHT_REJECTED',JSON.stringify(event),now());
    }
    return {id,status:'PREFLIGHT_REJECTED',reason:e.message,remote_writes:0};
  }
}
export async function readbackAction(w,id){
  const a=w.db.prepare('SELECT * FROM actions WHERE id=?').get(id);if(!a)throw Error('ACTION_NOT_FOUND');const p=JSON.parse(a.payload);
  if(p.environment!=='LIVE')throw Error('LIVE_SOURCE_REQUIRED');
  const conf=JSON.parse(fs.readFileSync(path.join(w.base,'hotel.json'))),m=loadMap(w.base,p.channel||'ebooking');
  if(conf.hotel_id!==a.hotel_id||m.hotel_id!==a.hotel_id||m.account_id!==p.account_id)throw Error('ACCOUNT_OR_HOTEL_MISMATCH');
  const r=m.writes?.[p.kind]?.[p.object_id];if(!r?.readback||!r?.identity||!r?.identity_value)throw Error('READBACK_MAPPING_REQUIRED');
  const url=r.readback_url||r.url,channel=p.channel||'ebooking';if(!allowed(url,channel))throw Error('INVALID_DOMAIN');
  const owner=crypto.randomUUID();try{w.db.prepare('INSERT INTO locks VALUES(?,?,?)').run(a.hotel_id,owner,now());}catch{throw Error('HOTEL_WRITER_BUSY');}
  let ctx;try{ctx=await context(w.base,channel);const page=ctx.pages()[0]||await ctx.newPage();await page.goto(url,{waitUntil:'domcontentloaded'});await identity(page,m,channel);
    if((await page.locator(r.identity).innerText()).trim()!==r.identity_value)throw Error('READBACK_OBJECT_MISMATCH');
    const f=page.locator(r.readback),value=parseValue(r.readback_is_input?await f.inputValue():await f.innerText(),r.value_type);
    const state=value===p.after?'VERIFIED':value===p.before?'NOT_APPLIED':'CONFLICT';
    recordAttempt(w,a,state,{phase:'READBACK',object_id:p.object_id,before:p.before,expected_after:p.after,observed:value,source_url:page.url(),observed_at:now(),remote_writes:0});
    return {id,status:state,backend_readback:'BACKEND_READBACK_PASS',remote_writes:0};
  }finally{if(ctx)await ctx.close();w.db.prepare('DELETE FROM locks WHERE hotel_id=? AND owner=?').run(a.hotel_id,owner);}
}
export async function main(argv=process.argv.slice(2)) {
  const {args}=await import('./ops.mjs');const a=args(argv),channel=a.channel||'ebooking';if(!a.workspace)throw Error('缺少--workspace');
  const w=openWorkspace(a.workspace);
  try{
    if(a._[0]==='read')return await readSnapshot(w,channel);
    if(a._[0]==='execute')return await executeAction(w,a.id);
    if(a._[0]==='readback')return await readbackAction(w,a.id);
    const ctx=await context(w.base,channel),page=ctx.pages()[0]||await ctx.newPage();
    try{
      await page.goto(homes[channel],{waitUntil:'domcontentloaded'});
      if(a._[0]==='login') {console.log('请在专属Chrome完成登录并关闭窗口；不会提交业务动作。');await new Promise(resolve=>ctx.on('close',resolve));return {status:'WINDOW_CLOSED',account_permission:'NOT_ASSESSED'};}
      if(a._[0]==='capture'){const text=await page.locator('body').innerText();const file=path.join(w.base,'evidence',`${channel}-${Date.now()}.txt`);fs.mkdirSync(path.dirname(file),{recursive:true,mode:0o700});fs.writeFileSync(file,text,{mode:0o600});return {status:'LOCAL_CAPTURE',file,structured_read:'NOT_VERIFIED'};}
      throw Error('命令需为login、capture、read或execute');
    }finally{await ctx.close();}
  }finally{w.close();}
}
if(import.meta.url===pathToFileURL(process.argv[1]).href)main().then(x=>console.log(JSON.stringify(x,null,2))).catch(e=>{console.error(JSON.stringify({status:'FAILED',error:e.message}));process.exitCode=1;});
