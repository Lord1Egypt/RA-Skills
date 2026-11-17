import fs from 'node:fs';
import {createHash,randomUUID} from 'node:crypto';
import {transact,assert,text,integer,safePath} from './store.mjs';
import {fetchPublic,publicUrl,utf8} from './public-net.mjs';
import {entities} from './html-text.mjs';
import {exportFiles,md} from './files.mjs';
const slug='mochi-web-watch',hash=v=>createHash('sha256').update(typeof v==='string'?v:JSON.stringify(v)).digest('hex');
const blocked=new Set(['script','style','noscript','template','nav','header','footer','aside','svg']);
const voids=new Set(['br','hr','img','meta','link','input','source','wbr','area','base','embed','param','track','col']);
const blocks=new Set(['p','div','li','tr','section','article','main','h1','h2','h3','h4','br','hr']);
function attributes(tag){const r={};for(const m of tag.matchAll(/([\w:-]+)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+))/g))r[m[1].toLowerCase()]=entities(m[2]??m[3]??m[4]);return r;}
function strings(v,label,max=20){assert(Array.isArray(v)&&v.length<=max,label+': provide up to '+max+' strings');return v.map(x=>text(x,label,200));}
export function extract(html,scope={tag:'body'},ignore=[]){
 assert(typeof html==='string'&&Buffer.byteLength(html)<=1048576,'Page exceeds 1 MiB');assert(scope&&typeof scope==='object'&&!Array.isArray(scope),'scope must be an object');assert(Object.keys(scope).every(k=>['tag','id'].includes(k)),'scope uses tag or id');assert((scope.tag!==undefined)!==(scope.id!==undefined),'Choose scope.tag or scope.id');if(scope.tag)assert(['body','main','article'].includes(scope.tag),'scope.tag: body, main or article');if(scope.id)text(scope.id,'scope.id',100);
 const stack=[];let found=0,selected=0,skip=0,parts=[];
 for(const token of html.matchAll(/<!--[\s\S]*?-->|<[^>"']*(?:"[^"]*"[^>"']*|'[^']*'[^>"']*)*>|[^<]+/g)){
  const value=token[0];if(value.startsWith('<!--')||value.startsWith('<!')||value.startsWith('<?'))continue;
  if(value[0]!=='<'){if(selected&&skip===0)parts.push(value);continue;}
  const match=/^<\s*(\/?)\s*([\w:-]+)/.exec(value);if(!match)continue;const closing=!!match[1],tag=match[2].toLowerCase();
  if(closing){const at=stack.findLastIndex(x=>x.tag===tag);if(at>=0){if(selected&&blocks.has(tag)&&skip===0)parts.push('\n');for(const entry of stack.splice(at)){if(entry.selected)selected--;if(entry.blocked)skip--;}}continue;}
  const a=attributes(value),isSelected=scope.tag===tag||scope.id!==undefined&&a.id===scope.id,isBlocked=blocked.has(tag);if(isSelected){found++;selected++;}if(isBlocked)skip++;if(selected&&skip===0&&blocks.has(tag))parts.push('\n');
  if(voids.has(tag)||/\/\s*>$/.test(value)){if(isSelected)selected--;if(isBlocked)skip--;}else stack.push({tag,selected:isSelected,blocked:isBlocked});
 }
 assert(found===1,found?'Scope matches more than one element':'Scope was not found; use the correct tag/id');let lines=entities(parts.join('')).replace(/\r/g,'').split('\n').map(x=>x.normalize('NFKC').replace(/[\u0000-\u001f\u007f]+/g,' ').replace(/\s+/g,' ').trim()).filter(Boolean);const ignored=strings(ignore,'ignoreLinesContains');lines=lines.filter(line=>!ignored.some(term=>line.includes(term)));const result=lines.join('\n');assert(result&&result.length<=60000,'Selected region is empty or exceeds 60000 characters');return result;
}
export function difference(before,after){
 const left=before.split('\n'),right=after.split('\n'),subtract=(a,b)=>{const counts=new Map();for(const line of b)counts.set(line,(counts.get(line)||0)+1);return a.filter(line=>{const n=counts.get(line)||0;if(n){counts.set(line,n-1);return false;}return true;});};const added=subtract(right,left),removed=subtract(left,right);return {added,removed,orderOnly:!added.length&&!removed.length&&before!==after};
}
function route(value){assert(value&&typeof value==='object','Provide delivery route');return Object.fromEntries(['agentId','channel','accountId','to'].map(k=>[k,text(value[k],k,300)]));}
function summary(w){return {id:w.id,title:w.title,url:w.url,status:w.status,intervalMinutes:w.intervalMinutes,baselineHash:w.baseline.hash,lastChangedAt:w.lastChangedAt,scheduled:!!w.scheduler,pending:w.events.filter(e=>e.state==='pending').length};}
const pending=w=>w.events.filter(e=>e.state==='pending').map(e=>({...e,delivery:w.delivery}));
function handle(i,s,c){
 if(i.action==='list')return {result:{watches:s.records.map(summary)}};
 if(i.action==='_snapshot'){const w=s.records.find(x=>x.id===i.id);assert(w,'Watch not found');return {result:{watch:structuredClone(w)}};}
 if(i.action==='add'){
  assert(s.records.length<10,'At most 10 subscriptions per workspace');assert(/^[a-z0-9][a-z0-9_-]{0,63}$/.test(i.id||''),'id: lowercase letters, numbers, hyphen or underscore');assert(!s.records.some(x=>x.id===i.id),'Watch ID already exists');
  const w={id:i.id,title:text(i.title,'title',200),url:i.url,scope:i.scope,ignoreLinesContains:strings(i.ignoreLinesContains||[],'ignoreLinesContains'),includeKeywords:strings(i.includeKeywords||[],'includeKeywords'),intervalMinutes:integer(i.intervalMinutes??60,15,10080),status:'active',baseline:i.snapshot,events:[],createdAt:c.now,creationRequest:i.requestId,creationInputHash:i.userHash};if(i.delivery)w.delivery=route(i.delivery);s.records.push(w);return {changed:true,result:{watch:summary(w),baselineCreated:true,notificationCreated:false}};
 }
 const w=s.records.find(x=>x.id===i.id);assert(w,'Watch not found');
 if(i.action==='show')return {result:{watch:summary(w),scope:w.scope,ignoreLinesContains:w.ignoreLinesContains,includeKeywords:w.includeKeywords,delivery:w.delivery,scheduler:w.scheduler,events:w.events}};
 if(i.action==='pending')return {result:{events:pending(w)}};
 if(i.action==='dismiss'){const e=w.events.find(x=>x.id===i.eventId);assert(e&&e.state==='pending','Pending event not found');e.state='dismissed';e.dismissedAt=c.now;e.reason=text(i.reason,'reason',500);return {changed:true,result:{id:w.id,eventId:e.id,state:e.state,notificationSent:false}};}
 if(i.action==='pause'||i.action==='resume'){w.status=i.action==='pause'?'paused':'active';return {changed:true,result:{watch:summary(w)}};}
 if(i.action==='check'){
  assert(hash(w)===i.expected,'Subscription changed during fetch; run check again');if(w.status==='paused')return {result:{id:w.id,paused:true,changed:false,events:[]}};
  if(w.baseline.hash===i.snapshot.hash)return {result:{id:w.id,checkedAt:c.now,changed:false,events:pending(w)}};
  const diff=difference(w.baseline.text,i.snapshot.text),relevant=!w.includeKeywords.length||[...diff.added,...diff.removed].some(line=>w.includeKeywords.some(term=>line.toLowerCase().includes(term.toLowerCase())));const event={id:randomUUID(),checkedAt:c.now,fromHash:w.baseline.hash,toHash:i.snapshot.hash,added:diff.added.slice(0,20).map(x=>x.slice(0,500)),removed:diff.removed.slice(0,20).map(x=>x.slice(0,500)),addedCount:diff.added.length,removedCount:diff.removed.length,truncated:diff.added.length>20||diff.removed.length>20||[...diff.added,...diff.removed].some(x=>x.length>500),orderOnly:diff.orderOnly,state:relevant?'pending':'filtered',sourceUrl:w.url};
  const unresolved=w.events.filter(e=>e.state==='pending');assert(unresolved.length<20,'Deliver or acknowledge pending events before saving more changes');w.events=[...unresolved,...w.events.filter(e=>e.state!=='pending').slice(-19),event].sort((a,b)=>a.checkedAt.localeCompare(b.checkedAt));w.baseline=i.snapshot;w.lastChangedAt=c.now;return {changed:true,result:{id:w.id,checkedAt:c.now,changed:true,eventId:event.id}};
 }
 if(i.action==='ack'){
  const e=w.events.find(x=>x.id===i.eventId);assert(e&&e.state==='pending','Pending event not found');const receipt=i.receipt;assert(receipt&&receipt.confirmedByDeliveryTool===true,'Provide the real delivery-tool receipt');assert(JSON.stringify(route(receipt.delivery))===JSON.stringify(w.delivery),'Delivery route differs from this watch');e.state='delivered';e.receipt={toolCallId:text(receipt.toolCallId,'toolCallId',300),deliveredAt:c.now};return {changed:true,result:{id:w.id,eventId:e.id,state:e.state}};
 }
 if(i.action==='schedule-spec'){assert(w.delivery,'Add a delivery route before scheduling');return {result:{id:w.id,agentId:w.delivery.agentId,intervalMinutes:w.intervalMinutes,pollInput:{action:'check',id:w.id},delivery:w.delivery,instructions:'Use the native host scheduler for this agent. Poll silently, send only pending events through the specified channel/account/recipient, then ack each successful send using its tool receipt. No changes means no message.'}};}
 if(i.action==='record-schedule'){
  const r=i.receipt;assert(w.delivery&&r&&r.confirmedByScheduler===true,'Provide native scheduler receipt');assert(JSON.stringify(route(r.delivery))===JSON.stringify(w.delivery)&&r.intervalMinutes===w.intervalMinutes,'Scheduler route or interval mismatch');assert(Number.isSafeInteger(r.nextRunAtMs)&&r.nextRunAtMs>Date.now(),'Next run must be in the future');w.scheduler={jobId:text(r.jobId,'jobId',300),intervalMinutes:r.intervalMinutes,nextRunAtMs:r.nextRunAtMs,recordedAt:c.now};return {changed:true,result:{watch:summary(w)}};
 }
 if(i.action==='export')return exportFiles('web-watch',{'changes.md':`# ${md(w.title)}\n\nSource: ${w.url}\n\nBaseline: ${w.baseline.hash}\n\n`+w.events.map(e=>`## ${e.checkedAt} / ${e.state}\n\nAdded (${e.addedCount}):\n`+e.added.map(x=>'- '+md(x)).join('\n')+'\n\nRemoved ('+e.removedCount+'):\n'+e.removed.map(x=>'- '+md(x)).join('\n')+'\n').join('\n'),'baseline.txt':w.baseline.text+'\n','changes.json':JSON.stringify({watch:summary(w),events:w.events},null,2)+'\n'},{watch:summary(w)});
 throw Error('Unsupported watch action');
}
export async function execute(workspace,input,fetcher=fetchPublic){
 assert(input&&typeof input==='object'&&!Array.isArray(input),'Input must be an object');assert(!String(input.action).startsWith('_'),'Unsupported internal action');let i={...input};
 if(i.action==='add'||i.action==='check'){
  if(i.action==='add'){const rows=transact(workspace,slug,{action:'list'},handle).watches;const prior=rows.find(x=>x.id===i.id);if(prior){const saved=transact(workspace,slug,{action:'_snapshot',id:i.id},handle).watch;assert(saved.creationRequest===i.requestId&&saved.creationInputHash===hash(input),'Watch ID already exists with different input');return {ok:true,watch:summary(saved),baselineReused:true,replayed:true};}i.userHash=hash(input);}
  let w;if(i.action==='check'){w=transact(workspace,slug,{action:'_snapshot',id:i.id},handle).watch;if(w.status==='paused')return {ok:true,id:w.id,paused:true,changed:false,events:[]};}
  const url=w?.url??text(i.url,'url',2048);publicUrl(url);const scope=w?.scope??i.scope??{tag:'body'},ignore=w?.ignoreLinesContains??i.ignoreLinesContains??[];const response=await fetcher(url);assert(response.status===200,'Source returned HTTP '+response.status);assert(/text\/html|application\/xhtml\+xml/i.test(response.contentType),'Expected an HTML page');const value=extract(utf8(response.body),scope,ignore);const snapshot={text:value,hash:hash(value),fetchedAt:new Date().toISOString(),finalUrl:response.finalUrl};i={...i,url,scope,snapshot};if(w)i={...i,expected:hash(w),requestId:'poll-'+randomUUID()};
 }
 const result=transact(workspace,slug,i,handle);if(i.action==='check')result.events=transact(workspace,slug,{action:'pending',id:i.id},handle).events;return result;
}
export async function main(){try{const args=process.argv.slice(2);assert(args.length===4&&args[0]==='--workspace'&&args[2]==='--input','Use --workspace DIRECTORY --input RELATIVE_JSON');const p=safePath(args[1],args[3],true);assert(fs.statSync(p).size<=1048576,'Input exceeds 1 MiB');const result=await execute(args[1],JSON.parse(fs.readFileSync(p,'utf8')));console.log(JSON.stringify(result,null,2));}catch(e){console.error(JSON.stringify({ok:false,error:e.message}));process.exitCode=1;}}
