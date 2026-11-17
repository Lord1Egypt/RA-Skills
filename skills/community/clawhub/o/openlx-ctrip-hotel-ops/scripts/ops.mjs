#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import {pathToFileURL} from 'node:url';
import {deviceId,refreshLicense} from './licensing.mjs';
import {ROOT,catalog,hash,now,openWorkspace,writeJson,validateSnapshot,renderReport,reviewDraft,priceProposal,enqueue,approve,scanAssets,createContent,validatePersona,entitlement,verifyLicense,operationalProposal,revenueSuggestion,distillPersona} from './core.mjs';

export function args(argv){const out={_:[]};for(let i=0;i<argv.length;i++){if(argv[i].startsWith('--'))out[argv[i].slice(2)]=argv[i+1]&&!argv[i+1].startsWith('--')?argv[++i]:true;else out._.push(argv[i]);}return out;}
export async function main(argv=process.argv.slice(2)) {
  const a=args(argv),cmd=a._[0]||'help';
  if(cmd==='device')return {device_id:deviceId(),label:os.hostname(),note:'在官网会员中心登记此设备ID后下载许可证；不要复制该电脑的设备身份文件到其他电脑'};
  if(cmd==='help')return {commands:['doctor','device','refresh-license','init','import','report','reviews','prices','authorize-pricing','revenue','propose','approve','execute','readback','status','pause','resume','assets','content','persona','distill','license','run'],usage:'node scripts/ops.mjs <command> --workspace <directory>',docs:'https://ctrip.openlx.cn/docs'};
  if(cmd==='doctor')return {version:catalog.version,node:process.version,platform:os.platform(),arch:os.arch(),node_supported:Number(process.versions.node.split('.')[0])>22||Number(process.versions.node.split('.')[0])===22&&Number(process.versions.node.split('.')[1])>=20,sqlite:'AVAILABLE',chrome:os.platform()==='darwin'?fs.existsSync('/Applications/Google Chrome.app'): '需本机核验',browser_dependency:fs.existsSync(path.join(ROOT,'node_modules/playwright'))?'INSTALLED':'npm ci后可用',account_read:'NOT_RUN',account_write:'NOT_RUN',public_readback:'NOT_RUN'};
  if(!a.workspace)throw Error('缺少--workspace');
  const w=openWorkspace(a.workspace);
  try{
    const configFile=path.join(w.base,'hotel.json');
    if(cmd==='init'){
      if(fs.existsSync(configFile))throw Error('工作区已初始化，保留现有资料');
      if(!a.hotel||!a.name)throw Error('需要--hotel与--name');
      validateSnapshot({hotel:{id:a.hotel,name:a.name},source:{type:'USER_EXPORT'},observed_at:now()},a.hotel);
      writeJson(configFile,{hotel_id:a.hotel,hotel_name:a.name,created_at:now(),positive_review_opt_in:false});
      return {status:'INITIALIZED',workspace:w.base,hotel_id:a.hotel};
    }
    if(!fs.existsSync(configFile))throw Error('请先init初始化门店');
    const config=JSON.parse(fs.readFileSync(configFile));
    const snapFile=path.join(w.base,'snapshot.json');
    const snapshot=()=>validateSnapshot(JSON.parse(fs.readFileSync(snapFile)),config.hotel_id);
    const lic=()=>entitlement(w.base,config.hotel_id);
    if(cmd==='refresh-license')return await refreshLicense(w,true);
    if(cmd==='import'){
      const s=validateSnapshot(JSON.parse(fs.readFileSync(a.file)),config.hotel_id);
      writeJson(path.join(w.base,'snapshots',hash(s)+'.json'),s);writeJson(snapFile,s);
      return {status:'IMPORTED',source_type:s.source.type,observed_at:s.observed_at,hash:hash(s)};
    }
    if(cmd==='report'){
      const s=snapshot(),out=path.join(w.base,'reports',now().replace(/[:.]/g,'-')+'.html');
      fs.mkdirSync(path.dirname(out),{recursive:true,mode:0o700});
      const history=fs.readdirSync(path.join(w.base,'snapshots')).filter(f=>f.endsWith('.json')).map(f=>JSON.parse(fs.readFileSync(path.join(w.base,'snapshots',f)))).filter(x=>x.hotel.id===s.hotel.id).sort((a,b)=>Date.parse(a.observed_at)-Date.parse(b.observed_at));
      fs.writeFileSync(out,renderReport(s,lic(),history),{mode:0o600});return {status:'REPORT_GENERATED',file:out,plan:lic().plan,source_type:s.source.type,remote_writes:0};
    }
    if(cmd==='reviews'){
      const s=snapshot();return {actions:(s.reviews||[]).filter(r=>!r.replied).map(r=>{const draft=reviewDraft(r,s);return enqueue(w,{kind:'REVIEW',hotel_id:s.hotel.id,object_id:String(r.id),environment:s.source.type,account_id:s.source.account_id||null,before:'',after:draft.reply,eligible:!!r.id&&!!r.text,draft,review_hash:hash(r),mode:draft.auto?'POSITIVE_OPT_IN':'CONFIRMED'});}),remote_writes:0};
    }
    if(cmd==='prices'){
      const s=snapshot(),policy=JSON.parse(fs.readFileSync(a.file)),prior=w.db.prepare('SELECT * FROM actions WHERE hotel_id=?').all(s.hotel.id);
      return {actions:(s.rates||[]).filter(r=>policy.dates?.includes(r.date)&&policy.room_ids?.includes(r.room_id)).map(r=>enqueue(w,priceProposal(s,r,policy,prior,lic()))),remote_writes:0};
    }
    if(cmd==='authorize-pricing'){
      const policy=JSON.parse(fs.readFileSync(a.file));if(hash(policy)!==a.hash||policy.hotel_id!==config.hotel_id||policy.mode!=='AUTOMATIC')throw Error('FINAL_POLICY_HASH_AND_HOTEL_REQUIRED');
      writeJson(path.join(w.base,'pricing-policy.json'),policy);writeJson(configFile,{...config,pricing_policy_hash:hash(policy)});return {status:'POLICY_AUTHORIZED',policy_hash:hash(policy),live_execution:'NOT_RUN'};
    }
    if(cmd==='propose')return enqueue(w,operationalProposal(snapshot(),JSON.parse(fs.readFileSync(a.file))));
    if(cmd==='revenue'){
      if(lic().plan!=='SUPREME')throw Error('SUPREME_LICENSE_REQUIRED');const s=snapshot(),p=JSON.parse(fs.readFileSync(a.file));return {suggestions:(s.rates||[]).map(r=>({rate:r,...revenueSuggestion(s,r,p)})),remote_writes:0};
    }
    if(cmd==='approve')return approve(w,a.id,a.hash);
    if(cmd==='pause'||cmd==='resume'){w.db.prepare('INSERT INTO settings VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value').run('paused',cmd==='pause'?'1':'0');return {status:cmd==='pause'?'WRITE_PAUSED':'WRITE_RESUMED'};}
    if(cmd==='status')return {hotel_id:config.hotel_id,license:lic().plan,paused:w.db.prepare("SELECT value FROM settings WHERE key='paused'").get()?.value==='1',actions:w.db.prepare('SELECT id,kind,object_id,status,content_hash,updated_at FROM actions ORDER BY created_at DESC').all(),attempts:w.db.prepare('SELECT * FROM attempts ORDER BY id DESC LIMIT 100').all()};
    if(cmd==='execute'){
      const {executeAction}=await import('./browser.mjs');return await executeAction(w,a.id);
    }
    if(cmd==='readback'){const {readbackAction}=await import('./browser.mjs');return await readbackAction(w,a.id);}
    if(cmd==='assets'){
      const folder=path.resolve(a.folder||path.join(w.base,'assets'));
      const mf=path.join(folder,'manifest.json');return {assets:scanAssets(w,folder,fs.existsSync(mf)?JSON.parse(fs.readFileSync(mf)):{}),remote_writes:0};
    }
    if(cmd==='persona'){
      const license=lic();if(license.plan!=='SUPREME'||license.billing_cycle!=='annual')throw Error('SUPREME_ANNUAL_LICENSE_REQUIRED');
      const p=validatePersona(JSON.parse(fs.readFileSync(a.file)));writeJson(path.join(w.base,'persona.json'),p);return {status:'PERSONA_IMPORTED',human_delivery:'NOT_VERIFIED'};
    }
    if(cmd==='distill'){
      const license=lic();if(license.plan!=='SUPREME'||license.billing_cycle!=='annual')throw Error('SUPREME_ANNUAL_LICENSE_REQUIRED');const p=distillPersona(snapshot(),JSON.parse(fs.readFileSync(a.file)));const out=path.join(w.base,'persona-draft.json');writeJson(out,p);return {status:'PERSONA_DRAFT_READY',file:out,human_delivery:'NOT_VERIFIED'};
    }
    if(cmd==='content'){
      if(lic().plan!=='SUPREME')throw Error('SUPREME_LICENSE_REQUIRED');
      const personaFile=path.join(w.base,'persona.json'),s=snapshot();
      const persona=fs.existsSync(personaFile)?JSON.parse(fs.readFileSync(personaFile)):null;
      let content=createContent(s,a.topic||'入住前的小提示',w.db.prepare('SELECT * FROM assets').all(),persona);
      if(a.model&&content.status==='DRAFT_READY'){const {modelDraft}=await import('./model.mjs');content={...content,...await modelDraft(w,s,a.topic||'入住前的小提示',persona)};}
      const out=path.join(w.base,'content',`${content.id||now().replace(/[:.]/g,'-')}.json`);writeJson(out,content);return {...content,file:out,remote_writes:0};
    }
    if(cmd==='license'){
      const envelope=JSON.parse(fs.readFileSync(a.file));
      const payload=verifyLicense(envelope,fs.readFileSync(path.join(ROOT,'assets/license-public.txt'),'utf8'),config.hotel_id);
      if(!payload||payload.device_id!==deviceId())throw Error('INVALID_EXPIRED_OR_WRONG_DEVICE_LICENSE');writeJson(path.join(w.base,'license.json'),envelope);return {status:'LICENSE_IMPORTED',plan:payload.plan,expires_at:payload.expires_at};
    }
    if(cmd==='run'){
      const {runOnce}=await import('./scheduler.mjs');return await runOnce(w);
    }
    throw Error('未知命令，请运行help');
  }finally{w.close();}
}
if(import.meta.url===pathToFileURL(process.argv[1]).href) main().then(result=>console.log(JSON.stringify(result,null,2))).catch(error=>{console.error(JSON.stringify({status:'FAILED',error:error.message}));process.exitCode=1;});
