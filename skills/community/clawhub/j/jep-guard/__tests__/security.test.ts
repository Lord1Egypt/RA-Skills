import fs from 'fs';
import os from 'os';
import path from 'path';
import net from 'net';
import nacl from 'tweetnacl';
import {GuardDaemon} from '../src/daemon/server';
import {PolicyEngineService} from '../src/daemon/policy';
import {AuditStreamService} from '../src/daemon/audit';
import {JEPCore} from '../src/core/jep-core';

const transport=require('../transport');
const ipcTest=process.env.RUN_IPC_TESTS==='1'?test:test.skip;
let home:string,folder:string,daemon:GuardDaemon|undefined;
let homedir:jest.SpyInstance;
beforeEach(()=>{
  home=fs.mkdtempSync(path.join(os.tmpdir(),'jep-security-'));
  homedir=jest.spyOn(os,'homedir').mockReturnValue(home);
  folder=path.join(home,'.jep-guard');fs.mkdirSync(folder,{mode:0o700});fs.mkdirSync(path.join(folder,'keys'),{mode:0o700});
  const key=nacl.sign.keyPair();
  fs.writeFileSync(path.join(folder,'keys','worker.json'),JSON.stringify({seed:Buffer.from(key.secretKey.subarray(0,32)).toString('base64')}),{mode:0o600});
  fs.writeFileSync(path.join(folder,'allowed-skills.json'),JSON.stringify([{name:'worker',version:'1',pubkey:Buffer.from(key.publicKey).toString('base64'),capabilities:['read']}]),{mode:0o600});
  fs.writeFileSync(path.join(folder,'config.json'),JSON.stringify({mode:'full'}),{mode:0o600});
  fs.writeFileSync(path.join(folder,'policy.json'),JSON.stringify([{id:'allow-read',match:{action:'read',target:'/safe/*',skill:'worker'},decision:'allow'}]),{mode:0o600});
});
afterEach(()=>{daemon?.stop();daemon=undefined;homedir.mockRestore();fs.rmSync(home,{recursive:true,force:true});});

ipcTest('authenticated request grants a bound capability and records owned completion',async()=>{
  daemon=new GuardDaemon('full');await daemon.start();
  const payload={action:'read',target:'/safe/file',context:{args:['--read']}};
  const result=await transport.guardCall('JUDGE','worker',payload);
  expect(result.action).toBe('allow');
  expect(result.event.who).toBe('jep-guard-daemon');
  expect(()=>transport.verifyCapability(result,'worker',{...payload,target:'/secret'})).toThrow();
  const completed=await transport.guardCall('VERIFY','worker',{target_event:result.event.nonce,verdict:'approved'});
  expect(completed.success).toBe(true);
  await expect(transport.guardCall('VERIFY','worker',{target_event:result.event.nonce,verdict:'approved'})).rejects.toThrow();
});

test('protection blocks offline daemon and corrupt config',async()=>{
  const hooks=require('../openclaw.hooks');
  await expect(hooks.preExec({action:'read',target:'/safe/file'},{skillId:'worker'})).rejects.toThrow();
  fs.writeFileSync(path.join(folder,'config.json'),'bad-json');
  await expect(hooks.preExec({action:'read',target:'/safe/file'},{skillId:'worker'})).rejects.toThrow();
});

ipcTest('review policy and unassigned capability do not allow execution',async()=>{
  fs.writeFileSync(path.join(folder,'policy.json'),JSON.stringify([{id:'review',match:{},decision:'review'}]));
  daemon=new GuardDaemon('full');await daemon.start();
  await expect(transport.guardCall('JUDGE','worker',{action:'read',target:'/safe/file'})).rejects.toThrow('did not grant');
  await expect(transport.guardCall('JUDGE','worker',{action:'shell_exec',target:'/safe/file'})).rejects.toThrow('capabilities');
});

ipcTest('wrong caller key is rejected and registration cannot overwrite identities',async()=>{
  daemon=new GuardDaemon('full');await daemon.start();
  await expect(transport.guardCall('REGISTER_SKILL','worker',{name:'worker',version:'1',capabilities:['shell_exec']})).rejects.toThrow();
  fs.writeFileSync(path.join(folder,'keys','worker.json'),JSON.stringify({seed:Buffer.from(nacl.randomBytes(32)).toString('base64')}));
  await expect(transport.guardCall('JUDGE','worker',{action:'read',target:'/safe/file'})).rejects.toThrow('Unauthenticated');
});

ipcTest('socket challenge rejects replay or unsigned frames',async()=>{
  daemon=new GuardDaemon('full');await daemon.start();
  const result=await new Promise<string>((resolve,reject)=>{
    const client=net.createConnection(daemon!.socketPath);let buffer='',challenged=false;
    client.on('error',reject);client.on('data',chunk=>{
      buffer+=chunk.toString();
      if(!challenged && buffer.includes('\n')) {
        challenged=true;buffer='';
        client.write(JSON.stringify({method:'JUDGE',skill:'worker',payload:{action:'read',target:'/safe/file'},challenge:'0'.repeat(64),sig:'fake'})+'\n');
      }
    });client.on('end',()=>resolve(buffer));
  });
  expect(JSON.parse(result).error).toBe('Unauthenticated request');
});

test('policy glob treats regex metacharacters literally',async()=>{
  const engine=new PolicyEngineService();engine.addRule({id:'a',match:{action:'read',target:'/safe/a.b'},decision:'allow'});
  const skill:any={skill_id:'worker'};
  expect((await engine.evaluate({requester:'worker',action:'read',target:'/safe/axb',type:'system_call'},skill)).decision).toBe('deny');
});

test('filtered export excludes unrelated audit records',async()=>{
  const stream=new AuditStreamService(folder);
  await stream.emit(new JEPCore('one').createJudge({action:'read'}));
  await stream.emit(new JEPCore('two').createJudge({action:'write'}));
  const result=JSON.parse(stream.export('json',await stream.query({agent:'one'})));
  expect(result).toHaveLength(1);expect(result[0].who).toBe('one');
});

ipcTest('legacy unauthenticated cross-skill routing is explicitly blocked',async()=>{
  daemon=new GuardDaemon('full');await daemon.start();
  await expect(transport.guardCall('DELEGATE','worker',{target:'../victim'})).rejects.toThrow('legacy cross-skill');
});

 test('gate handles allow and review with a valid signature without IPC',async()=>{
  const {CausalGateService}=require('../src/daemon/gate');
  const {SkillRegistryService}=require('../src/daemon/registry');
  const core=new JEPCore('jep-guard-daemon');
  fs.writeFileSync(path.join(folder,'daemon-publickey'),core.publicKey,{mode:0o600});
  const registry=new SkillRegistryService(folder),policy=new PolicyEngineService(path.join(folder,'policy.json'));
  const gate=new CausalGateService(core,registry,policy,{evaluateAll:async()=>[]});
  const payload={action:'read',target:'/safe/file',context:{}};
  const result=await gate.process({requester:'worker',...payload,type:'system_call'});
  expect(transport.verifyCapability(result,'worker',payload)).toBe(result);
  expect(()=>transport.verifyCapability({...result,capabilityToken:'junk'},'worker',payload)).toThrow();
  expect(()=>transport.verifyCapability({...result,action:'review'},'worker',payload)).toThrow();
  policy.addRule({id:'r',match:{},decision:'review'});
  expect((await gate.process({requester:'worker',...payload,type:'system_call'})).action).toBe('review');
 });
 test('registry binds identity to an operator-approved key',()=>{
   const {SkillRegistryService}=require('../src/daemon/registry');
   const registry=new SkillRegistryService(folder);
   const seed=Buffer.from(JSON.parse(fs.readFileSync(path.join(folder,'keys/worker.json'),'utf8')).seed,'base64');
   const key=nacl.sign.keyPair.fromSeed(seed);
   const sig=Buffer.from(nacl.sign.detached(Buffer.from('challenge'),key.secretKey)).toString('base64');
   expect(registry.verifySignature('worker','challenge',sig)).toBe(true);
   expect(registry.verifySignature('worker','other',sig)).toBe(false);
   expect(()=>registry.register({name:'worker',version:'2',capabilities:['read']})).toThrow();
 });
