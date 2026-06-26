#!/usr/bin/env node
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const args = Object.fromEntries(process.argv.slice(2).map((v,i,a)=>v.startsWith('--')?[v.slice(2),a[i+1]]:null).filter(Boolean));
const cfgPath = args.config || '/root/.openclaw/openclaw.json';
const team = args.team;
const roles = (args.roles||'').split(',').map(s=>s.trim()).filter(Boolean);
const leaderId = args['leader-id'] || `${team}-team-leader`;
const roleIdMap = new Map(roles.map(r => [r, (r==='team-leader' ? leaderId : r)]));
const channel = args.channel || 'telegram';
const accountId = args['account-id'] || '';
const locale = args.locale || 'zh-CN';
const model = args.model || 'openai-codex/gpt-5.3-codex';
if (!team || roles.length===0) throw new Error('missing --team/--roles');

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const PRESET = {
  'team-leader': {zh:'团队负责人', emoji:'🧭'},
  'product-manager': {zh:'产品经理', emoji:'📌'},
  'tech-architect': {zh:'技术架构师', emoji:'🏗️'},
  'fullstack-engineer': {zh:'全栈工程师', emoji:'🛠️'},
  'qa-engineer': {zh:'测试工程师', emoji:'✅'},
  'ux-designer': {zh:'交互设计师', emoji:'🎨'}
};
const FALLBACKS = ['openai-codex/gpt-5.4','openai-codex/gpt-5.3-codex','openai-codex/gpt-5.3','bailian/kimi-k2.5','moonshot/kimi-k2.5','glmcode/glm-4.7','openrouter/openai/gpt-5.2'];

const originalRaw = fs.readFileSync(cfgPath,'utf8');
const cfg = JSON.parse(originalRaw);
cfg.agents ??= {}; cfg.agents.list ??= []; cfg.bindings ??= [];
if (!Array.isArray(cfg.agents.list)) throw new Error('invalid config: agents.list must be array');
if (!Array.isArray(cfg.bindings)) throw new Error('invalid config: bindings must be array');
const teamRoot = `/root/.openclaw/workspace-${team}`;
fs.mkdirSync(teamRoot,{recursive:true});
for (const d of ['requirements','architecture','design','implementation','qa']) fs.mkdirSync(path.join(teamRoot,'shared',d),{recursive:true});

const resolvedRoleIds = roles.map(r => roleIdMap.get(r));
cfg.agents.list = cfg.agents.list.filter(a => !resolvedRoleIds.includes(a?.id));

const teamDirectoryLines = roles.map(r0 => {
  const r = roleIdMap.get(r0);
  const p = PRESET[r0] || { zh: r0 };
  const n = locale.startsWith('zh') ? p.zh : r0;
  return `- **${r}（${n}）**`;
}).join('\n');

for (const rid0 of roles){
  const rid = roleIdMap.get(rid0);
  const p = PRESET[rid0] || {zh:rid0, emoji:'🤖'};
  const displayBase = locale.startsWith('zh') ? p.zh : rid0;
  const display = rid0==='team-leader' ? `${displayBase}（${team}）` : displayBase;
  const agent = {
    id: rid,
    workspace: `${teamRoot}/${rid}`,
    model: {primary:model, fallbacks:FALLBACKS},
    identity: {name: display, emoji: p.emoji},
    tools: {profile:'full'},
    subagents: {allowAgents: rid0==='team-leader' ? roles.filter(x=>x!=='team-leader').map(x=>roleIdMap.get(x)) : [leaderId]}
  };
  cfg.agents.list.push(agent);

  fs.mkdirSync(agent.workspace,{recursive:true});
  let soul;
  let agents;
  if (rid0 === 'team-leader') {
    const soulTpl = fs.readFileSync(path.join(__dirname, '..', 'references', 'team-leader-template.md'), 'utf8');
    const agentsTpl = fs.readFileSync(path.join(__dirname, '..', 'references', 'team-leader-agents-template.md'), 'utf8');
    soul = soulTpl
      .replaceAll('{{LEADER_ID}}', rid)
      .replaceAll('{{TEAM_DISPLAY}}', locale.startsWith('zh') ? `${team}团队` : team)
      .replaceAll('{{TEAM_ROOT}}', teamRoot);
    agents = agentsTpl
      .replaceAll('{{LEADER_ID}}', rid)
      .replaceAll('{{TEAM_DIRECTORY}}', teamDirectoryLines);
  } else {
    soul = `# SOUL.md - ${rid}\n\n你是${display}，按行业顶尖专家标准工作。\n\n## 角色定位\n- 专注本角色职责，输出可执行、可验证的专业交付物\n\n## 核心职责\n- 交付本角色阶段成果\n- 与上下游协作并按协议回传\n- 发现风险立即上报\n\n## 输出标准\n- 聊天只发摘要+路径，不贴大段原始内容\n`;
    agents = `# AGENTS.md - ${rid}\n\n## 协作机制\n- 控制平面: sessions_send/sessions_spawn\n- 状态机: accepted/blocked/done\n- 回传闭环: 完成后回传给委派方\n\n## 共享目录\n- ${teamRoot}/shared/\n`;
  }
  const identity = `# IDENTITY.md\n\n- display_name: ${display}\n- agent_id: ${rid}\n- locale: ${locale}\n`;
  fs.writeFileSync(path.join(agent.workspace,'SOUL.md'),soul);
  fs.writeFileSync(path.join(agent.workspace,'AGENTS.md'),agents);
  fs.writeFileSync(path.join(agent.workspace,'IDENTITY.md'),identity);
  fs.writeFileSync(path.join(agent.workspace,'USER.md'),'# USER.md\n');
}

if (accountId){
  cfg.bindings = cfg.bindings.filter(b => !(resolvedRoleIds.includes(b?.agentId) && b?.match?.accountId===accountId));
  cfg.bindings.push({agentId:leaderId, match:{channel, accountId}});
}

// atomic + rollback-safe write
const out = JSON.stringify(cfg, null, 2);
JSON.parse(out); // ensure serializable JSON
const bakPath = `${cfgPath}.bak.materialize`;
const tmpPath = `${cfgPath}.tmp.materialize`;
if (!fs.existsSync(bakPath)) fs.writeFileSync(bakPath, originalRaw);
fs.writeFileSync(tmpPath, out);
fs.renameSync(tmpPath, cfgPath);
console.log(JSON.stringify({ok:true,team,leaderId,roles:resolvedRoleIds,shared:`${teamRoot}/shared`, backup:bakPath}));
