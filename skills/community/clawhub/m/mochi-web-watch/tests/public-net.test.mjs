import test from 'node:test';
import assert from 'node:assert/strict';
import https from 'node:https';
import {Readable} from 'node:stream';
import {EventEmitter} from 'node:events';
import {gzipSync} from 'node:zlib';
import {publicAddress,publicUrl,fetchPublic,LIMITS,utf8} from '../scripts/public-net.mjs';
const publicDns=async()=>[{address:'93.184.215.14',family:4}];
const response=(status=200,headers={})=>({status,headers:{'content-type':'text/html',...headers},body:Buffer.from('<title>Example</title>')});
test('only public HTTPS domains and port443 are admitted',()=>{
 for(const url of ['http://example.org','file:///etc/passwd','https://127.0.0.1','https://2130706433','https://[::1]','https://user:pass@example.org/','https://example.org:8443','https://a.local','https://a.internal','https://localhost','https://example.org./','https://example.org/\n'])assert.throws(()=>publicUrl(url));
 assert.equal(publicUrl('https://example.org:443/path#heading').href,'https://example.org/path');
});
test('private, reserved, multicast, metadata and transition IPs are refused',()=>{
 for(const ip of ['0.1.2.3','10.0.0.1','100.64.0.1','127.1.1.1','168.63.129.16','169.254.169.254','172.16.0.1','172.31.255.254','192.0.0.9','192.0.2.1','192.88.99.1','192.168.1.1','198.18.0.1','198.19.2.1','198.51.100.1','203.0.113.1','224.0.0.1','240.0.0.1','255.255.255.255','::1','::ffff:8.8.8.8','64:ff9b::808:808','fc00::1','fe80::1','ff02::1','2001:db8::1','2001:20::1','2002:0808:0808::1','3ffe::1','3fff::1'])assert.equal(publicAddress(ip),false,ip);
 for(const ip of ['8.8.8.8','93.184.215.14','2606:4700::1111','2001:4860:4860::8888'])assert.equal(publicAddress(ip),true,ip);
});
test('credential-style query names/values never enter output',()=>{
 for(const query of ['token=abc','apiKey=x','client_secret=x','access_token=x','sessionid=abc','X-Amz-Signature=abc','%70assword=x','x_token=x','q=sk-abcdefghijklmnop'])assert.throws(()=>publicUrl('https://example.org/?'+query));
 assert.equal(publicUrl('https://example.org/?topic=learning').search,'?topic=learning');
});
test('mixed private/public DNS rejects before any request',async()=>{
 let called=false;await assert.rejects(fetchPublic('https://example.org',{lookup:async()=>[...(await publicDns()),{address:'10.0.0.1',family:4}],request:async()=>{called=true;return response();}}),/DNS/);assert.equal(called,false);
});
test('each redirect is checked again and DNS pin is supplied to transport',async()=>{
 let lookups=0,requests=0;
 const r=await fetchPublic('https://example.org',{lookup:async()=>{lookups++;return publicDns();},request:async(url,pin)=>{requests++;assert.equal(pin.address,'93.184.215.14');return requests===1?response(302,{location:'https://www.example.org/next'}):response();}});
 assert.equal(lookups,2);assert.equal(requests,2);assert.equal(r.redirects.length,1);assert.equal(r.finalUrl,'https://www.example.org/next');
});
test('private redirect and rebinding target are refused without a second request',async()=>{
 let calls=0;await assert.rejects(fetchPublic('https://example.org',{lookup:publicDns,request:async()=>{calls++;return response(302,{location:'https://169.254.169.254/latest/meta-data'});}}),/domain/);assert.equal(calls,1);
 let dnsCalls=0;calls=0;await assert.rejects(fetchPublic('https://example.org',{lookup:async()=>++dnsCalls===1?publicDns():[{address:'127.0.0.1',family:4}],request:async()=>{calls++;return response(302,{location:'https://example.org/again'});}}),/DNS/);assert.equal(calls,1);
});
test('three redirects, deadline and body limit are enforced',async()=>{
 let calls=0;await assert.rejects(fetchPublic('https://example.org',{lookup:publicDns,request:async()=>{calls++;return response(302,{location:'/again'});}}),/Redirect limit/);assert.equal(calls,4);
 await assert.rejects(fetchPublic('https://example.org',{lookup:()=>new Promise(()=>{}),timeoutMs:15}),/deadline/);
 await assert.rejects(fetchPublic('https://example.org',{lookup:publicDns,request:async()=>({...response(),body:Buffer.alloc(LIMITS.bodyBytes+1)})}),/bounded/);
 assert.throws(()=>utf8(Buffer.from([0xff,0xfe])),/UTF-8/);
});
test('real request primitive pins lookup, validates TLS and limits gzip expansion',async()=>{
 const original=https.get;let inspected=false;
 https.get=(url,options,callback)=>{
  assert.equal(options.rejectUnauthorized,true);assert.equal(options.minVersion,'TLSv1.2');assert.equal(options.agent,false);
  options.lookup('example.org',{all:true},(error,addresses)=>{assert.equal(error,null);assert.equal(addresses[0].address,'93.184.215.14');inspected=true;});
  const req=new EventEmitter(),incoming=Readable.from([gzipSync(Buffer.alloc(LIMITS.bodyBytes+100))]);incoming.statusCode=200;incoming.headers={'content-type':'text/html','content-encoding':'gzip'};
  req.destroy=error=>{incoming.destroy();queueMicrotask(()=>{req.emit('error',error);req.emit('close');});};incoming.on('end',()=>req.emit('close'));queueMicrotask(()=>callback(incoming));return req;
 };
 try{await assert.rejects(fetchPublic('https://example.org',{lookup:publicDns}),/expanded body/);assert.equal(inspected,true);}finally{https.get=original;}
});
test('certificate errors propagate instead of retrying with TLS disabled',async()=>{
 const original=https.get;let calls=0;https.get=()=>{calls++;const req=new EventEmitter();req.destroy=()=>{};queueMicrotask(()=>{req.emit('error',Error('CERT_HAS_EXPIRED'));req.emit('close');});return req;};
 try{await assert.rejects(fetchPublic('https://example.org',{lookup:publicDns}),/CERT_HAS_EXPIRED/);assert.equal(calls,1);}finally{https.get=original;}
});
test('wire download cap aborts the actual transport before accepting an oversized body',async()=>{
 const original=https.get;let aborted=false;https.get=(_url,_options,callback)=>{const req=new EventEmitter(),incoming=Readable.from([Buffer.alloc(LIMITS.wireBytes+1)]);incoming.statusCode=200;incoming.headers={'content-type':'text/plain'};req.destroy=error=>{aborted=true;incoming.destroy();queueMicrotask(()=>{req.emit('error',error);req.emit('close');});};incoming.on('end',()=>req.emit('close'));queueMicrotask(()=>callback(incoming));return req;};
 try{await assert.rejects(fetchPublic('https://example.org',{lookup:publicDns}),/download limit/);assert.equal(aborted,true);}finally{https.get=original;}
});
