import fs from 'node:fs';
import path from 'node:path';
import {hash,now,writeJson,priceProposal,revenueSuggestion,enqueue,approve,scanAssets,createContent} from './core.mjs';
import {executeAction} from './browser.mjs';
import {noteOperation,contentHash} from './notes.mjs';
import {modelDraft} from './model.mjs';

export async function runPricing(w,s,settings,license,execute=executeAction){
  if(license.plan==='FREE')return {module:'pricing',status:'FREE_ADVISORY_ONLY'};
  const policyFile=path.join(w.base,'pricing-policy.json');if(!fs.existsSync(policyFile))return {module:'pricing',status:'NOT_CONFIGURED'};
  const original=JSON.parse(fs.readFileSync(policyFile));
  if(original.mode!=='AUTOMATIC'||original.hotel_id!==s.hotel.id||settings.pricing_policy_hash!==hash(original))return {module:'pricing',status:'POLICY_AUTHORIZATION_REQUIRED'};
  if(s.source.type!=='LIVE')return {module:'pricing',status:'LIVE_SOURCE_REQUIRED'};
  const results=[];
  for(const rate of s.rates||[]){
    if(!original.dates?.includes(rate.date)||!original.room_ids?.includes(rate.room_id))continue;
    try{
      let policy={...original};if(policy.strategy==='MULTI_SIGNAL')policy={...policy,...revenueSuggestion(s,rate,policy)};
      if(policy.target_fen===rate.price_fen)continue;
      const prior=w.db.prepare('SELECT * FROM actions WHERE hotel_id=?').all(s.hotel.id),p=priceProposal(s,rate,policy,prior,license),a=enqueue(w,p);
      if(!p.eligible){results.push({id:a.id,status:'BLOCKED',errors:p.errors});continue;}
      if(a.status==='AWAITING_APPROVAL')approve(w,a.id,a.content_hash);
      if(['AWAITING_APPROVAL','APPROVED','BLOCKED_RETRYABLE'].includes(a.status))results.push(await execute(w,a.id));
    }catch(e){results.push({object_id:rate.room_id,status:'FAILED',reason:e.message});}
  }
  return {module:'pricing',status:'RUN_COMPLETE',results};
}

export async function runContent(w,s,settings,license,operate=noteOperation){
  if(license.plan!=='SUPREME')return {module:'content',status:'SUPREME_REQUIRED'};
  const c=settings.content_schedule;if(!c?.enabled)return {module:'content',status:'NOT_CONFIGURED'};
  const tz=c.timezone||'Asia/Shanghai',date=new Intl.DateTimeFormat('en-CA',{timeZone:tz,year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date());
  const hour=Number(new Intl.DateTimeFormat('en-GB',{timeZone:tz,hour:'2-digit',hourCycle:'h23'}).format(new Date()));
  if(hour<(c.hour??10))return {module:'content',status:'NOT_DUE'};
  const file=path.join(w.base,'content',`daily-${date}.json`);
  // At most one new content item per current date; never queue missed days.
  if(fs.existsSync(file))return {module:'content',status:'ALREADY_PREPARED',file};
  const folder=path.resolve(c.asset_folder||path.join(w.base,'assets')),manifest=path.join(folder,'manifest.json');
  if(!fs.existsSync(folder)||!fs.existsSync(manifest))return {module:'content',status:'NEEDS_MATERIALS',missing:['授权素材目录及manifest.json']};
  const assets=scanAssets(w,folder,JSON.parse(fs.readFileSync(manifest)));
  const pf=path.join(w.base,'persona.json'),persona=fs.existsSync(pf)?JSON.parse(fs.readFileSync(pf)):null;
  const topics=c.topics||persona?.topics||['入住前的真实信息'];const topic=topics[Number(date.slice(-2))%topics.length];
  let draft=createContent(s,topic,w.db.prepare('SELECT * FROM assets').all(),persona);
  if(draft.status!=='DRAFT_READY')return {module:'content',...draft,assets};
  if(c.mode==='MODEL'){
    try{const generated=await modelDraft(w,s,topic,persona);draft={...draft,...generated};}
    catch(e){draft.model_error=e.message;draft.status='AWAITING_APPROVAL';draft.mode='RULE_FALLBACK';}
  }else draft.mode='RULE_FACTS_ONLY';
  draft.schedule_date=date;writeJson(file,draft);
  const p=c.publish_policy;
  const factsHash=hash((s.facts||[]).filter(f=>f.verified===true));
  const policyValid=p?.hotel_id===s.hotel.id&&p?.account_id&&p.facts_hash===factsHash&&p.persona_hash===(persona?hash(persona):null)&&Array.isArray(p.allowed_asset_hashes)&&draft.assets.every(a=>p.allowed_asset_hashes.includes(a.hash))&&p.authorized_topics?.includes(topic)&&Date.parse(p.valid_until)>Date.now()&&Number.isFinite(Date.parse(p.valid_until));
  // Broad topic/fact/asset authorization is sufficient for unchanged rule content.
  // New model prose remains a reviewable draft, never silently auto-approved.
  if(c.auto_submit===true&&policyValid&&draft.mode==='RULE_FACTS_ONLY'&&s.source.type!=='MOCK'){
    const mapping=path.join(w.base,'adapter-content.json');
    if(!fs.existsSync(mapping)||JSON.parse(fs.readFileSync(mapping)).account_id!==p.account_id)return {module:'content',status:'DRAFT_READY',file,submission:'ACCOUNT_MAPPING_REQUIRED'};
    draft.approval={content_hash:contentHash(draft),hotel_id:s.hotel.id,valid_until:p.valid_until,policy_hash:hash(p)};writeJson(file,draft);
    const submission=await operate(w,file,'submit');
    if(submission.status==='LIVE_WRITE_PASS'){
      const backend=await operate(w,file,'readback');const current=JSON.parse(fs.readFileSync(file));
      const publicResult=current.public_url?await operate(w,file,'public'):{status:'PUBLIC_URL_PENDING'};
      return {module:'content',file,submission,backend,public:publicResult};
    }
    return {module:'content',file,submission};
  }
  return {module:'content',status:draft.status,file,publish_status:'NOT_SUBMITTED',auto_submit:c.auto_submit===true?'POLICY_OR_REVIEW_REQUIRED':'NOT_ENABLED'};
}
