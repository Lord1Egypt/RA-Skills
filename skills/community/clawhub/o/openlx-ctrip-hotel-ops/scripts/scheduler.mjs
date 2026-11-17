import fs from 'node:fs';
import path from 'node:path';
import {now,writeJson,hash,reviewDraft,enqueue,approve,renderReport,entitlement} from './core.mjs';
import {readSnapshot,executeAction} from './browser.mjs';
import {runPricing,runContent} from './automation.mjs';
import {refreshLicense} from './licensing.mjs';

export async function runOnce(w) {
  const results=[];const settings=JSON.parse(fs.readFileSync(path.join(w.base,'hotel.json')));
  const stateFile=path.join(w.base,'scheduler.json');const state=fs.existsSync(stateFile)?JSON.parse(fs.readFileSync(stateFile)):{};
  const interval=Math.max(15,settings.review_scan_minutes||60)*60000;
  if(state.last_attempt_at&&Date.now()-Date.parse(state.last_attempt_at)<interval)return {status:'NOT_DUE',next_at:new Date(Date.parse(state.last_attempt_at)+interval).toISOString()};
  const started=now();let s,readSucceeded=false,fallback=false;
  try{results.push({module:'license',...await refreshLicense(w)});}catch(e){results.push({module:'license',status:'REFRESH_UNAVAILABLE',reason:e.message,note:'按已有签名有效期继续；免费报告和数据保留'});}
  try{s=await readSnapshot(w);readSucceeded=Object.keys(s).some(k=>Array.isArray(s[k])&&k!=='read_failures');results.push({module:'read',status:readSucceeded?'LIVE_READ_PARTIAL_OR_COMPLETE':'FAILED',failures:s.read_failures});}catch(e){results.push({module:'read',status:'FAILED',reason:e.message});if(fs.existsSync(path.join(w.base,'snapshot.json'))){s=JSON.parse(fs.readFileSync(path.join(w.base,'snapshot.json')));fallback=true;}}
  if(s){
    const license=entitlement(w.base,s.hotel.id);
    if(readSucceeded&&!fallback&&settings.positive_review_opt_in===true&&Date.parse(settings.review_authorization_until)>Date.now()&&s.source.type==='LIVE'&&Date.now()-Date.parse(s.observed_at)<interval){
      for(const r of s.reviews||[]){const d=reviewDraft(r,s);if(!d.auto||r.replied)continue;
        try{const a=enqueue(w,{kind:'REVIEW',hotel_id:s.hotel.id,object_id:String(r.id),environment:'LIVE',account_id:s.source.account_id,before:'',after:d.reply,eligible:true,review_hash:hash(r),mode:'POSITIVE_OPT_IN',authorization_until:settings.review_authorization_until});if(a.status==='AWAITING_APPROVAL')approve(w,a.id,a.content_hash);if(['AWAITING_APPROVAL','APPROVED'].includes(a.status))results.push(await executeAction(w,a.id));}catch(e){results.push({module:'review',object_id:r.id,status:'FAILED',reason:e.message});}}
    }
    if(readSucceeded&&!fallback){try{results.push(await runPricing(w,s,settings,license));}catch(e){results.push({module:'pricing',status:'FAILED',reason:e.message});}}
    try{results.push(await runContent(w,s,settings,license));}catch(e){results.push({module:'content',status:'FAILED',reason:e.message});}
    const file=path.join(w.base,'reports','latest.html');fs.mkdirSync(path.dirname(file),{recursive:true,mode:0o700});
    const historyDir=path.join(w.base,'snapshots'),history=fs.existsSync(historyDir)?fs.readdirSync(historyDir).filter(x=>x.endsWith('.json')).map(x=>JSON.parse(fs.readFileSync(path.join(historyDir,x)))).filter(x=>x.hotel.id===s.hotel.id).sort((a,b)=>Date.parse(a.observed_at)-Date.parse(b.observed_at)):[];
    fs.writeFileSync(file,renderReport(s,license,history),{mode:0o600});
    const date=now().slice(0,10);fs.copyFileSync(file,path.join(w.base,'reports',`daily-${date}.html`));
    if(license.plan!=='FREE'){const monday=new Date();monday.setUTCDate(monday.getUTCDate()-((monday.getUTCDay()+6)%7));fs.copyFileSync(file,path.join(w.base,'reports',`weekly-${monday.toISOString().slice(0,10)}.html`));}
    results.push({module:'report',status:'GENERATED',file,observed_at:s.observed_at});
  }
  writeJson(stateFile,{last_attempt_at:started,last_successful_read_at:readSucceeded?s.observed_at:(state.last_successful_read_at||null),fallback_used:fallback,report_source_type:s?.source?.type||null,report_observed_at:s?.observed_at||null,results});
  return {status:'RUN_COMPLETE',results,next_at:new Date(Date.now()+interval).toISOString(),offline_backfill:'ONE_CATCHUP_ONLY'};
}
