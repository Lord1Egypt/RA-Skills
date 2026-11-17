import fs from 'node:fs';
import path from 'node:path';
import {randomUUID,createHash} from 'node:crypto';
export const assert=(ok,message)=>{if(!ok)throw new Error(message);};
export const text=(v,label='text',max=12000)=>{assert(typeof v==='string'&&v.trim()&&v.length<=max,`${label}: provide nonempty text (max ${max})`);return v.trim();};
export const date=(v)=>{assert(typeof v==='string'&&/^\d{4}-\d{2}-\d{2}$/.test(v)&&new Date(v+'T00:00:00Z').toISOString().slice(0,10)===v,'date: use a real YYYY-MM-DD date');return v;};
export const integer=(v,min=0,max=1000000)=>{assert(Number.isSafeInteger(v)&&v>=min&&v<=max,`integer: expected ${min}..${max}`);return v;};
export const minor=(v)=>{assert((typeof v==='string'||typeof v==='number')&&/^\d+(?:\.\d{1,2})?$/.test(String(v)),'amount: use a nonnegative decimal with at most two places');const [a,b='']=String(v).split('.');const n=Number(a)*100+Number(b.padEnd(2,'0'));assert(Number.isSafeInteger(n)&&n<=1e12,'amount is too large');return n;};
export const currency=v=>{assert(['CNY','USD','EUR','GBP','HKD','SGD','AUD','CAD','CHF','NZD'].includes(v),'Supported currencies: CNY, USD, EUR, GBP, HKD, SGD, AUD, CAD, CHF, NZD (two decimal places)');return v;};
export const id=()=>randomUUID();
export const addDays=(d,n)=>new Date(Date.parse(date(d)+'T00:00:00Z')+n*86400000).toISOString().slice(0,10);
export function safePath(workspace,relative,mustExist=false){
 assert(typeof relative==='string'&&!path.isAbsolute(relative),'Use a workspace-relative path');
 const root=fs.realpathSync(workspace),target=path.resolve(root,relative),rel=path.relative(root,target);
 assert(!rel.startsWith('..'+path.sep)&&rel!=='..'&&!path.isAbsolute(rel),'Path is outside this workspace');
 let cur=root;
 for(const part of rel.split(path.sep).filter(Boolean)){
  cur=path.join(cur,part);
  if(fs.existsSync(cur)){const s=fs.lstatSync(cur);assert(!s.isSymbolicLink(),'Linked paths are not supported');const actual=fs.realpathSync(cur);assert(actual===root||actual.startsWith(root+path.sep),'Resolved path is outside workspace');}
 }
 if(mustExist)assert(fs.existsSync(target),'File does not exist');return target;
}
export function transact(workspace,slug,input,handler){
 assert(/^mochi-[a-z0-9-]+$/.test(slug),'Invalid Skill namespace');
 assert(input&&typeof input==='object'&&!Array.isArray(input),'Input must be an object');
 const dir=safePath(workspace,`.mochilab/${slug}`);fs.mkdirSync(dir,{recursive:true,mode:0o700});safePath(workspace,`.mochilab/${slug}`,true);
 const file=path.join(dir,'state.json'),lock=path.join(dir,'write.lock');
 assert(!fs.existsSync(lock),'Workspace data is busy; wait for the other run');
 let fd;try{fd=fs.openSync(lock,'wx',0o600);}catch{throw new Error('Workspace data is busy; wait for the other run');}
 try{
  safePath(workspace,`.mochilab/${slug}/state.json`);
  if(fs.existsSync(file))assert(fs.statSync(file).size<=8*1024*1024,'State file exceeds 8 MiB');
  const state=fs.existsSync(file)?JSON.parse(fs.readFileSync(file,'utf8')):{schema:1,slug,records:[],operations:[]};
  assert(state.schema===1&&state.slug===slug&&Array.isArray(state.records)&&Array.isArray(state.operations),'Unexpected state format');
  const hash=createHash('sha256').update(JSON.stringify(input)).digest('hex');
  if(input.requestId){text(input.requestId,'requestId',200);const prev=state.operations.find(x=>x.id===input.requestId);if(prev){assert(prev.hash===hash,'requestId was already used with different input');for(const f of prev.result.files||[]){const p=safePath(workspace,f.path,true);assert(createHash('sha256').update(fs.readFileSync(p)).digest('hex')===f.sha256,'Saved export changed or is missing; use a new requestId to export again');}return {...prev.result,replayed:true};}}
  const out=handler(input,state,{workspace,now:new Date().toISOString()});assert(out&&typeof out==='object','Invalid operation result');
  const result={ok:true,...out.result};let exportDirectory;
  try{
  if(out.artifacts){
   assert(out.changed&&input.requestId,'Exports require a unique requestId');
   const files=Object.entries(out.artifacts);assert(files.length>0&&files.length<=6,'Export 1..6 files');
   for(const [name,value] of files){assert(/^[a-zA-Z0-9_-]+\.(md|csv|json|ics|txt)$/.test(name),'Invalid export filename');assert(typeof value==='string'&&Buffer.byteLength(value)<=2*1024*1024,'Export exceeds 2 MiB');}
   const relative=`.mochilab/${slug}/exports/${id()}`;exportDirectory=safePath(workspace,relative);fs.mkdirSync(exportDirectory,{recursive:true,mode:0o700});safePath(workspace,relative,true);
   result.files=[];
   for(const [name,value] of files){const p=safePath(workspace,relative+'/'+name),bytes=Buffer.from(value);fs.writeFileSync(p,bytes,{flag:'wx',mode:0o600});result.files.push({path:relative+'/'+name,bytes:bytes.length,sha256:createHash('sha256').update(bytes).digest('hex')});}
  }
  if(out.changed){
   assert(input.requestId,'Mutating operations require a unique requestId');
   state.operations.push({id:input.requestId,hash,result});state.updatedAt=new Date().toISOString();
   const bytes=JSON.stringify(state,null,2)+'\n';assert(Buffer.byteLength(bytes)<=8*1024*1024,'State reached 8 MiB; inspect stored data before adding more');
   const tmp=path.join(dir,`.pending-${id()}`);try{const out=fs.openSync(tmp,'wx',0o600);try{fs.writeFileSync(out,bytes);fs.fsyncSync(out);}finally{fs.closeSync(out);}fs.renameSync(tmp,file);}finally{if(fs.existsSync(tmp))fs.unlinkSync(tmp);}
  }
  return result;
  }catch(error){if(exportDirectory&&fs.existsSync(exportDirectory))fs.rmSync(exportDirectory,{recursive:true,force:true});throw error;}
 }finally{fs.closeSync(fd);fs.unlinkSync(lock);}
}
export function cli(slug,handler){
 try{
  const args=process.argv.slice(2),opts={};for(let i=0;i<args.length;i+=2){assert(['--workspace','--input'].includes(args[i])&&args[i+1]&&!opts[args[i]],'Use --workspace EXISTING_DIRECTORY --input INPUT_JSON');opts[args[i]]=args[i+1];}
  assert(opts['--workspace']&&opts['--input'],'Use --workspace EXISTING_DIRECTORY --input INPUT_JSON');
  const workspace=fs.realpathSync(opts['--workspace']);assert(fs.statSync(workspace).isDirectory(),'Workspace must be a directory');
  const source=safePath(workspace,opts['--input'],true);assert(fs.statSync(source).isFile()&&fs.statSync(source).size<=2*1024*1024,'Input must be a JSON file up to 2 MiB');
  const input=JSON.parse(fs.readFileSync(source,'utf8'));console.log(JSON.stringify(transact(workspace,slug,input,handler),null,2));
 }catch(e){console.error(JSON.stringify({ok:false,error:e.message}));process.exitCode=1;}
}
