import { SkillIdentity } from '../core/types';
import fs from 'fs';
import path from 'path';
import os from 'os';
import {JEPCrypto} from '../core/crypto';

export class SkillRegistryService {
  private skills = new Map<string, SkillIdentity>();
  constructor(configDir?:string) {
    const dir=configDir || path.join(os.homedir(),'.jep-guard');
    const {secureDir,readPrivate,validId}=require('../../transport');
    secureDir(dir);
    const file=path.join(dir,'allowed-skills.json');
    if(fs.existsSync(file)) {
      const entries=JSON.parse(readPrivate(file));
      if(!Array.isArray(entries)||entries.length>128) throw new Error('Invalid skill allowlist');
      for(const entry of entries) {
        if(!validId(entry.name)||typeof entry.pubkey!=='string'||Buffer.from(entry.pubkey,'base64').length!==32||!Array.isArray(entry.capabilities)||entry.capabilities.some((c:any)=>typeof c!=='string')) throw new Error('Invalid trusted skill');
        if(this.skills.has(entry.name))throw new Error('Duplicate skill identity');
        const identity:SkillIdentity={skill_id:entry.name,name:entry.name,version:entry.version||'1',pubkey:entry.pubkey,capabilities:entry.capabilities,risk_level:'high',installed_at:Date.now(),last_seen:Date.now(),extensions:[],metadata:{source:'operator-allowlist'}};
        this.skills.set(entry.name,identity);
      }
    }
  }
  register(manifest:Partial<SkillIdentity>&{name:string;version:string}):SkillIdentity {
    const existing=this.get(manifest.name);
    if(!existing || (manifest.pubkey && manifest.pubkey!==existing.pubkey) || manifest.version!==existing.version || JSON.stringify(manifest.capabilities||[])!==JSON.stringify(existing.capabilities)) throw new Error('Operator approval required for registration changes');
    return existing;
  }
  get(skillId:string):SkillIdentity|undefined {const entry=this.skills.get(skillId);return entry?JSON.parse(JSON.stringify(entry)):undefined;}
  list():SkillIdentity[]{return [...this.skills.keys()].map(k=>this.get(k)!);}
  verifySignature(skillId:string,message:string,signature:string):boolean {
    const entry=this.skills.get(skillId);
    return !!entry && JEPCrypto.verify(message,signature,entry.pubkey);
  }
}
