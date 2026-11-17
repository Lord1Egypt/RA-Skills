import https from 'node:https';
import dns from 'node:dns/promises';
import net from 'node:net';
import zlib from 'node:zlib';

export const LIMITS=Object.freeze({redirects:3,wireBytes:524288,bodyBytes:1048576,timeoutMs:15000});
export function publicAddress(address){
 if(net.isIP(address)===4){
  const [a,b,c]=address.split('.').map(Number);
  return !(address==='168.63.129.16'||a===0||a===10||a===127||a>=224||(a===100&&b>=64&&b<=127)||(a===169&&b===254)||(a===172&&b>=16&&b<=31)||(a===192&&(b===168||(b===0&&(c===0||c===2))||(b===88&&c===99)))||(a===198&&(b===18||b===19||(b===51&&c===100)))||(a===203&&b===0&&c===113));
 }
 if(net.isIP(address)!==6)return false;
 const [first,second]=address.split(':').map(x=>parseInt(x||'0',16));
 return first>=0x2000&&first<0x3ffe&&first!==0x2002&&!(first===0x2001&&(second<0x200||second===0xdb8));
}
const SECRET_KEY=/(?:^(?:key|token|secret|password|passwd|pass|pwd|auth|authorization|credential|signature|sig|session|sessionid|sid|code|ticket|jwt)$|(?:^|[_-])(?:api[_-]?key|access[_-]?token|refresh[_-]?token|key|token|auth|secret|password|signature|credential|session)(?:$|[_-])|^x-amz-|^x-goog-)/i;
export function publicUrl(value){
 if(typeof value!=='string'||value.length>2048||/[\s\\\u0000-\u001f\u007f]/u.test(value))throw Error('Use a public HTTPS URL without whitespace or control characters');
 let u;try{u=new URL(value);}catch{throw Error('Invalid public URL');}
 const host=u.hostname.replace(/^\[|\]$/g,'').toLowerCase();
 if(u.protocol!=='https:'||u.username||u.password||(u.port&&u.port!=='443')||net.isIP(host)||!host.includes('.')||host.endsWith('.')||/(?:^|\.)(?:localhost|local|internal|home|lan|test|invalid)$|\.home\.arpa$/i.test(host))throw Error('Only public HTTPS domain names on port443 are supported');
 for(const [key,v] of u.searchParams){if(SECRET_KEY.test(key)||/^(?:sk-[a-z0-9_-]{12,}|bearer\s|eyJ[a-z0-9_-]+\.[a-z0-9_-]+\.[a-z0-9_-]+$)/i.test(v))throw Error('Credential-like query parameters are not accepted');}
 u.hash='';return u;
}
async function deadline(promise,ms){let timer;try{return await Promise.race([promise,new Promise((_,reject)=>{timer=setTimeout(()=>reject(Error('Network deadline exceeded')),Math.max(1,ms));})]);}finally{clearTimeout(timer);}}
function readResponse(response,req,limits){
 return new Promise((resolve,reject)=>{
  const chunks=[];let wire=0,body=0,stream=response;
  const encoding=String(response.headers['content-encoding']||'identity').toLowerCase();
  if(encoding==='gzip')stream=response.pipe(zlib.createGunzip());
  else if(encoding==='deflate')stream=response.pipe(zlib.createInflate());
  else if(encoding==='br')stream=response.pipe(zlib.createBrotliDecompress());
  else if(encoding!=='identity'){response.destroy();reject(Error('Unsupported response encoding'));return;}
  const fail=error=>{stream.destroy();response.destroy();req.destroy(error);reject(error);};
  response.on('data',chunk=>{wire+=chunk.length;if(wire>limits.wireBytes)fail(Error('Response exceeds download limit'));});
  response.on('aborted',()=>reject(Error('Response interrupted')));response.on('error',reject);stream.on('error',reject);
  stream.on('data',chunk=>{body+=chunk.length;if(body>limits.bodyBytes)fail(Error('Response exceeds expanded body limit'));else chunks.push(chunk);});
  stream.on('end',()=>resolve(Buffer.concat(chunks)));
 });
}
async function requestPublic(url,address,remainingMs,limits){
 return new Promise((resolve,reject)=>{
  const req=https.get(url,{agent:false,minVersion:'TLSv1.2',rejectUnauthorized:true,lookup:(_host,opts,callback)=>opts.all?callback(null,[address]):callback(null,address.address,address.family),headers:{'User-Agent':'MochiLab-Public-Reader/1.0 (+https://mochilab.bz)','Accept':'text/html,application/xhtml+xml,text/plain;q=0.9','Accept-Encoding':'gzip, deflate, br'}},response=>{
   const status=response.statusCode||0;
   if([301,302,303,307,308].includes(status)){const headers={location:response.headers.location};response.destroy();resolve({status,headers,body:Buffer.alloc(0)});return;}
   readResponse(response,req,limits).then(body=>resolve({status,headers:{'content-type':response.headers['content-type']||''},body}),reject);
  });
  const timer=setTimeout(()=>req.destroy(Error('Network deadline exceeded')),Math.max(1,remainingMs));
  req.on('error',reject);req.on('close',()=>clearTimeout(timer));
 });
}
export async function fetchPublic(value,options={}){
 const limits=LIMITS,lookup=options.lookup||dns.lookup,request=options.request||requestPublic;
 const started=Date.now(),end=started+Math.min(limits.timeoutMs,Math.max(10,options.timeoutMs||limits.timeoutMs));
 let url=publicUrl(value);const requestedUrl=url.href,redirects=[];
 for(let hop=0;;hop++){
  const addresses=await deadline(lookup(url.hostname,{all:true,verbatim:true}),Math.min(4000,end-Date.now()));
  if(!Array.isArray(addresses)||!addresses.length||addresses.some(x=>!publicAddress(x.address)))throw Error('DNS includes a private or reserved address');
  if(Date.now()>=end)throw Error('Network deadline exceeded');
  const pinned=addresses.find(x=>x.family===4)||addresses[0];
  const response=await deadline(request(url,pinned,end-Date.now(),limits),end-Date.now());
  if(!response||!Number.isInteger(response.status)||!Buffer.isBuffer(response.body)||response.body.length>limits.bodyBytes)throw Error('Invalid bounded HTTP response');
  if([301,302,303,307,308].includes(response.status)){
   if(hop>=limits.redirects)throw Error('Redirect limit exceeded');
   if(typeof response.headers.location!=='string')throw Error('Redirect has no location');
   const next=publicUrl(new URL(response.headers.location,url).href);
   redirects.push({url:url.href,status:response.status,next:next.href});url=next;continue;
  }
  return {requestedUrl,finalUrl:url.href,status:response.status,elapsedMs:Date.now()-started,redirects,tlsValidated:true,contentType:String(response.headers['content-type']||''),body:response.body};
 }
}
export function utf8(buffer){try{return new TextDecoder('utf-8',{fatal:true}).decode(buffer).replace(/^\ufeff/,'');}catch{throw Error('Only UTF-8 pages are supported');}}
