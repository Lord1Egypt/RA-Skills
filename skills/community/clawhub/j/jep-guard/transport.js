'use strict';
const fs=require('fs'),path=require('path'),os=require('os'),net=require('net');
const nacl=require('tweetnacl');
const canonical=require('canonicalize');
const {createHash}=require('crypto');
const dir=()=>path.join(os.homedir(),'.jep-guard');
const validId=id=>typeof id==='string' && /^[A-Za-z0-9][A-Za-z0-9_.-]{0,127}$/.test(id);
function secureDir(p) {
  fs.mkdirSync(p,{recursive:true,mode:0o700});
  const s=fs.lstatSync(p);
  if (!s.isDirectory() || s.isSymbolicLink() || (s.mode&0o077) || (process.getuid && s.uid!==process.getuid())) throw Error('Guard directory must be owned by this user and mode 0700');
}
function readPrivate(p) {
  const fd=fs.openSync(p,fs.constants.O_RDONLY|fs.constants.O_NOFOLLOW);
  try {const s=fs.fstatSync(fd);if(!s.isFile() || s.size>262144 || (s.mode&0o077) || (process.getuid && s.uid!==process.getuid())) throw Error('Invalid Guard file permissions');return fs.readFileSync(fd,'utf8');} finally {fs.closeSync(fd);}
}
function verify(message,sig,key) {
  try {const s=Buffer.from(sig,'base64'),k=Buffer.from(key,'base64');return s.length===64 && k.length===32 && nacl.sign.detached.verify(Buffer.from(message),s,k);}catch{return false;}
}
function requestDigest(skill,payload) {return createHash('sha256').update(canonical({skill,payload})).digest('hex');}
function verifyCapability(result,skill,payload) {
  if(result?.action!=='allow' || typeof result.capabilityToken!=='string' || !result.event?.nonce) throw Error('Guard did not grant execution');
  const token=JSON.parse(Buffer.from(result.capabilityToken,'base64').toString('utf8'));
  const {sig,...claims}=token;
  const key=readPrivate(path.join(dir(),'daemon-publickey')).trim();
  const now=Math.floor(Date.now()/1000);
  if(!verify(canonical(claims),sig,key) || claims.type!=='jep-cap' || claims.agent!==skill || claims.event_id!==result.event.nonce || claims.request_digest!==requestDigest(skill,payload) || !Number.isInteger(claims.expires_at) || !Number.isInteger(claims.issued_at) || claims.issued_at>now+5 || claims.expires_at<=now || claims.expires_at-claims.issued_at>60) throw Error('Invalid capability');
  return result;
}
async function guardCall(method,skill,payload,timeout=5000) {
  if(!validId(skill)) throw Error('Invalid skill ID');
  secureDir(dir());
  const seed=Buffer.from(JSON.parse(readPrivate(path.join(dir(),'keys',skill+'.json'))).seed,'base64');
  if(seed.length!==32) throw Error('Invalid signing seed');
  const keys=nacl.sign.keyPair.fromSeed(seed);
  const socketPath=path.join(dir(),'guard.sock');
  const st=fs.lstatSync(socketPath);
  if(!st.isSocket() || st.isSymbolicLink() || (st.mode&0o077) || (process.getuid && st.uid!==process.getuid())) throw Error('Untrusted Guard socket');
  return new Promise((resolve,reject)=>{
    let data='',size=0,challengeReceived=false,settled=false;
    const client=net.createConnection(socketPath);
    const finish=(err,value)=>{if(settled)return;settled=true;clearTimeout(timer);client.destroy();err?reject(err):resolve(value);};
    const timer=setTimeout(()=>finish(Error('Guard timeout')),Math.min(timeout,10000));
    client.on('error',err=>finish(err));
    client.on('end',()=>{if(!settled)finish(Error('Incomplete Guard response'));});
    client.on('data',chunk=>{
      size+=chunk.length;if(size>262144)return finish(Error('Response too large'));
      data+=chunk.toString('utf8');
      while(data.includes('\n')) {
        const index=data.indexOf('\n'),line=data.slice(0,index);data=data.slice(index+1);
        try {
          const message=JSON.parse(line);
          if(!challengeReceived) {
            if(!/^[a-f0-9]{64}$/.test(message.challenge))throw Error('Invalid challenge');
            challengeReceived=true;
            const request={method,skill,payload,challenge:message.challenge};
            const sig=Buffer.from(nacl.sign.detached(Buffer.from(canonical(request)),keys.secretKey)).toString('base64');
            const frame=JSON.stringify({...request,sig})+'\n';
            if(Buffer.byteLength(frame)>65536)throw Error('Request too large');
            client.write(frame);
          } else {
            if(message.error)throw Error(message.error);
            if(method==='JUDGE')verifyCapability(message,skill,payload);
            finish(null,message);
          }
        } catch(err) {finish(err);}
      }
    });
  });
}
module.exports={guardCall,verifyCapability,verify,requestDigest,secureDir,readPrivate,validId,dir};
