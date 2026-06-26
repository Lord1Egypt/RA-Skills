#!/usr/bin/env node
import fs from 'fs';
import path from 'path';

const args = Object.fromEntries(process.argv.slice(2).map((v,i,a)=>v.startsWith('--')?[v.slice(2),a[i+1]]:null).filter(Boolean));
const cfgPath = args.config || '/root/.openclaw/openclaw.json';
const team = args.team; const roles=(args.roles||'').split(',').map(s=>s.trim()).filter(Boolean); const accountId=args['account-id']||'';
const leaderId = args['leader-id'] || `${team}-team-leader`;
if(!team||!roles.length) throw new Error('missing --team/--roles');
const roleIdMap = new Map(roles.map(r => [r, (r==='team-leader' ? leaderId : r)]));
const resolvedRoleIds = roles.map(r=>roleIdMap.get(r));
const cfg=JSON.parse(fs.readFileSync(cfgPath,'utf8'));
const issues=[];
const amap = new Map((cfg.agents?.list||[]).filter(a=>a&&a.id).map(a=>[a.id,a]));
for(const rid0 of roles){
  const rid=roleIdMap.get(rid0);
  const a=amap.get(rid); if(!a){issues.push(`missing agent: ${rid}`); continue;}
  const sa=a.subagents?.allowAgents||[];
  if(rid0==='team-leader'){
    for(const x0 of roles.filter(r=>r!=='team-leader')){
      const x=roleIdMap.get(x0);
      if(!sa.includes(x)) issues.push(`team-leader missing allowAgents: ${x}`);
    }
  } else if(!sa.includes(leaderId)) issues.push(`${rid} missing allowAgents: ${leaderId}`);
}
if(accountId){
  const ok=(cfg.bindings||[]).some(b=>b.agentId===leaderId && b.match?.accountId===accountId);
  if(!ok) issues.push('missing team-leader binding');
}
const root=`/root/.openclaw/workspace-${team}`;
for(const d of ['requirements','architecture','design','implementation','qa']) if(!fs.existsSync(path.join(root,'shared',d))) issues.push(`missing shared/${d}`);
for(const rid0 of roles){
  const rid=roleIdMap.get(rid0);
  const wd=path.join(root,rid);
  for(const fn of ['SOUL.md','AGENTS.md','IDENTITY.md','USER.md']){
    const p=path.join(wd,fn); if(!fs.existsSync(p)) {issues.push(`missing ${rid}/${fn}`); continue;}
    if(fn!=='USER.md' && fs.readFileSync(p,'utf8').trim().length<40) issues.push(`placeholder-like ${rid}/${fn}`);
  }
}
console.log(JSON.stringify({status:issues.length?'partially_ready':'ready',team,leaderId,issues},null,2));
