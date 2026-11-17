import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import crypto from 'node:crypto';
import {ROOT,writeJson,verifyLicense,now,hash} from './core.mjs';

export function deviceId(){
  const dir=path.join(os.homedir(),'.openlx-ctrip-device'),file=path.join(dir,'id');
  fs.mkdirSync(dir,{recursive:true,mode:0o700});if(!fs.existsSync(file))fs.writeFileSync(file,crypto.randomUUID(),{mode:0o600,flag:'wx'});
  return fs.readFileSync(file,'utf8').trim();
}
function enrollment(w){
  const f=path.join(w.base,'license.json');if(!fs.existsSync(f))return null;
  const e=JSON.parse(fs.readFileSync(f)),hotel=JSON.parse(fs.readFileSync(path.join(w.base,'hotel.json'))).hotel_id;
  const p=verifyLicense(e,fs.readFileSync(path.join(ROOT,'assets/license-public.txt'),'utf8'),hotel,0);
  if(!p)return null;assertEnrollmentBinding(e,p,deviceId());
  return {envelope:e,payload:p,token:e.enrollment.token,file:f};
}
export function assertEnrollmentBinding(e,p,device){
  if(p.device_id!==device||p.refresh_origin!=='https://ctrip.openlx.cn'||!e.enrollment?.token||hash(e.enrollment.token)!==p.device_token_hash||e.enrollment.device_id!==device)throw Error('DEVICE_ENROLLMENT_IDENTITY_MISMATCH');
}
async function call(e,operation,body={}){
  const r=await fetch(e.payload.refresh_origin+'/api/device/'+operation,{method:'POST',headers:{'Content-Type':'application/json',Authorization:'Bearer '+e.token},body:JSON.stringify(body),redirect:'error',signal:AbortSignal.timeout(10000)});
  const data=await r.json();if(!r.ok||!data.success)throw Error(data.error||'LICENSE_SERVICE_ERROR');return data.data;
}
export async function refreshLicense(w,force=false){
  const e=enrollment(w);if(!e)return {status:'NO_DEVICE_ENROLLMENT',remote_writes:0};
  if(!force&&Date.parse(e.payload.offline_valid_until)-Date.now()>6*3600000)return {status:'LICENSE_FRESH'};
  const fresh=await call(e,'refresh');const checked=verifyLicense(fresh,fs.readFileSync(path.join(ROOT,'assets/license-public.txt'),'utf8'),e.payload.hotel_id);
  if(!checked||checked.device_id!==deviceId())throw Error('LICENSE_REFRESH_INVALID');writeJson(e.file,{...fresh,enrollment:e.envelope.enrollment});return {status:'LICENSE_REFRESHED',at:now(),expires_at:checked.expires_at};
}
export async function acquireWriter(w){
  const e=enrollment(w);if(!e)throw Error('REGISTERED_DEVICE_ENROLLMENT_REQUIRED');
  const lease=await call(e,'lease',{operation:'acquire'});return leaseController(e,lease,call);
}
export function leaseController(e,lease,request){
  const verify=r=>{if(r.hotel_id!==e.payload.hotel_id||r.device_id!==e.payload.device_id||r.user_id!==e.payload.user_id||!r.lease_id||r.lease_id!==lease.lease_id||!Number.isFinite(r.expires_at)||r.expires_at<=Date.now())throw Error('WRITER_LEASE_IDENTITY_OR_EXPIRY_MISMATCH');};
  verify(lease);let lost=false,pending=null;
  const renew=()=>{if(lost)return Promise.reject(Error('WRITER_LEASE_LOST'));if(pending)return pending;
    pending=(async()=>{try{const r=await request(e,'lease',{operation:'renew',lease_id:lease.lease_id});verify(r);if(lost)throw Error('WRITER_LEASE_LOST');}catch(err){lost=true;throw err;}})().finally(()=>{pending=null;});return pending;
  };
  const interval=setInterval(()=>renew().catch(()=>{}),30000);interval.unref();
  return {scope:'SERVER_HOTEL',assert:renew,release:async()=>{lost=true;clearInterval(interval);if(pending)try{await pending;}catch{}try{await request(e,'lease',{operation:'release',lease_id:lease.lease_id});}catch{}}};
}
