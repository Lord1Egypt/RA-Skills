import net from 'net';
import path from 'path';
import fs from 'fs';
import {randomBytes} from 'crypto';
import {JEPCore} from '../core/jep-core';
import {canonicalize} from '../core/canonical';
import {SkillRegistryService} from './registry';
import {PolicyEngineService} from './policy';
import {CausalGateService} from './gate';
import {ReputationEngineService} from './reputation';
import {AuditStreamService} from './audit';
import {ExtensionLoaderService} from '../extensions/loader';

export class GuardDaemon {
  public socketPath:string;
  private server?:net.Server;
  private core:JEPCore;
  private registry:SkillRegistryService;
  private audit:AuditStreamService;
  private gate:CausalGateService;
  private grants=new Map<string,string>();
  private connections=new Set<net.Socket>();
  private listening=false;
  constructor(private mode:string) {
    if(mode!=='full')throw new Error('Daemon requires explicit full mode');
    const {dir,secureDir,readPrivate}=require('../../transport');
    const folder=dir();secureDir(folder);
    this.socketPath=path.join(folder,'guard.sock');
    const keyfile=path.join(folder,'daemon-seed');
    if(!fs.existsSync(keyfile))fs.writeFileSync(keyfile,randomBytes(32).toString('base64'),{mode:0o600,flag:'wx'});
    const seed=Buffer.from(readPrivate(keyfile).trim(),'base64');
    this.core=new JEPCore('jep-guard-daemon',seed);
    const publicfile=path.join(folder,'daemon-publickey');
    if(fs.existsSync(publicfile)) {
      if(readPrivate(publicfile).trim()!==this.core.publicKey)throw new Error('Daemon key pin mismatch');
    } else fs.writeFileSync(publicfile,this.core.publicKey,{mode:0o600,flag:'wx'});
    this.registry=new SkillRegistryService(folder);
    this.audit=new AuditStreamService(folder);
    const policy=new PolicyEngineService(path.join(folder,'policy.json'));
    const extensions=new ExtensionLoaderService({core:this.core,registry:this.registry,policy,reputation:new ReputationEngineService(),audit:this.audit});
    this.gate=new CausalGateService(this.core,this.registry,policy,extensions);
  }
  async start():Promise<void> {
    // Never unlink someone else's/live socket automatically. Operator removes stale sockets explicitly.
    if(fs.existsSync(this.socketPath))throw new Error('Socket already exists; check for a running daemon');
    this.server=net.createServer(socket=>{
      if(this.connections.size>=64){socket.destroy();return;}
      this.connections.add(socket);
      socket.on('close',()=>this.connections.delete(socket));
      socket.on('error',()=>socket.destroy());
      socket.setTimeout(5000,()=>socket.destroy());
      const challenge=randomBytes(32).toString('hex');
      socket.write(JSON.stringify({challenge})+'\n');
      let buffer=Buffer.alloc(0),handled=false;
      socket.on('data',async chunk=>{
        if(handled)return;
        buffer=Buffer.concat([buffer,chunk]);
        if(buffer.length>65536){handled=true;socket.destroy();return;}
        const newline=buffer.indexOf(10);if(newline<0)return;
        handled=true;
        try {
          if(newline!==buffer.length-1)throw new Error('One request per connection');
          const {sig,...req}=JSON.parse(buffer.subarray(0,newline).toString('utf8'));
          if(req.challenge!==challenge || !req.payload || typeof req.payload!=='object' || Array.isArray(req.payload) || !this.registry.verifySignature(req.skill,canonicalize(req),sig))throw new Error('Unauthenticated request');
          const result=await this.handleRequest(req);
          socket.end(JSON.stringify(result)+'\n');
        } catch(err) {socket.end(JSON.stringify({error:err instanceof Error?err.message:'Request rejected'})+'\n');}
      });
    });
    await new Promise<void>((resolve,reject)=>{
      this.server!.once('error',reject);
      this.server!.listen(this.socketPath,()=>{
        try {fs.chmodSync(this.socketPath,0o600);this.listening=true;resolve();}catch(e){this.server!.close();reject(e);}
      });
    });
  }
  stop():void {
    for(const socket of this.connections)socket.destroy();
    this.server?.close();
    if(this.listening && fs.existsSync(this.socketPath))fs.unlinkSync(this.socketPath);
    this.listening=false;
  }
  private async handleRequest(req:any):Promise<any> {
    switch(req.method) {
      case 'REGISTER_SKILL':
        if(req.payload.name!==req.skill)throw new Error('Identity mismatch');
        return {success:true,skill_id:this.registry.register(req.payload).skill_id};
      case 'JUDGE': {
        if(typeof req.payload.action!=='string'||typeof req.payload.target!=='string')throw new Error('Action and target are required');
        const identity=this.registry.get(req.skill)!;
        if(!identity.capabilities.includes(req.payload.action))throw new Error('Action is outside assigned capabilities');
        const result=await this.gate.process({requester:req.skill,action:req.payload.action,target:req.payload.target,type:'system_call',context:req.payload.context});
        if(result.event)await this.audit.emit(result.event);
        if(result.action==='allow')this.grants.set(result.event!.nonce,req.skill);
        return result;
      }
      case 'VERIFY':
      case 'TERMINATE': {
        const target=req.payload.target_event;
        if(typeof target!=='string'||this.grants.get(target)!==req.skill)throw new Error('No active owned grant');
        // Consume before asynchronous audit to prevent duplicate completion races.
        this.grants.delete(target);
        const payload={...req.payload,requester:req.skill,source:'authenticated_client_report'};
        const event=req.method==='VERIFY'?this.core.createVerify(payload,undefined,[target]):this.core.createTerminate(payload,undefined,[target]);
        await this.audit.emit(event);
        this.core.updateStatus(target,'completed');
        return {success:true,event};
      }
      case 'DELEGATE': throw new Error('Authenticated receiver transport is required; legacy cross-skill routing is disabled');
      default: throw new Error('Unknown method');
    }
  }
}
