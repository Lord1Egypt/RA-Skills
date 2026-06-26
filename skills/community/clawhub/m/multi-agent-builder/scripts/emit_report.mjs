#!/usr/bin/env node
import fs from 'fs';
import path from 'path';

const args = Object.fromEntries(process.argv.slice(2).map((v,i,a)=>v.startsWith('--')?[v.slice(2),a[i+1]]:null).filter(Boolean));
const team=args.team; const roles=(args.roles||'').split(',').map(s=>s.trim()).filter(Boolean);
const leaderId = args['leader-id'] || `${team}-team-leader`;
if(!team||!roles.length) throw new Error('missing --team/--roles');
const roleIdMap = new Map(roles.map(r => [r, (r==='team-leader' ? leaderId : r)]));
const root=`/root/.openclaw/workspace-${team}`;
const contracts=roles.map(r0=>{
  const r = roleIdMap.get(r0);
  const idp=path.join(root,r,'IDENTITY.md');
  let name=r;
  if(fs.existsSync(idp)){
    for(const line of fs.readFileSync(idp,'utf8').split(/\r?\n/)) if(line.trim().startsWith('- display_name:')) name=line.split(':').slice(1).join(':').trim();
  }
  return {agent_id:r, display_name:name};
});
console.log(JSON.stringify({
  team,
  contracts,
  stage_deliverables:{
    Requirement:path.join(root,'shared/requirements'),
    Architecture:path.join(root,'shared/architecture'),
    UX:path.join(root,'shared/design'),
    Implementation:path.join(root,'shared/implementation'),
    QA:path.join(root,'shared/qa')
  },
  binding_blueprints:['single-bot','multi-bot-group']
},null,2));
