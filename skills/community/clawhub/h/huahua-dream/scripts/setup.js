#!/usr/bin/env node
/**
 * OpenClaw Dream — Auto Setup
 *
 * Scans the workspace to detect memory structure, agent config, and session paths.
 * Outputs a dream-config.json that the dream prompt reads at runtime.
 *
 * Usage: node setup.js [--workspace <path>]
 *
 * Security: No network calls. No shell execution. No env sniffing.
 * Only reads filesystem structure and writes config to assets/.
 */

const fs = require('fs');
const path = require('path');

const ASSETS_DIR = path.join(__dirname, '..', 'assets');
const CONFIG_FILE = path.join(ASSETS_DIR, 'dream-config.json');

// Parse args
let workspaceHint = null;
const args = process.argv.slice(2);
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--workspace' && args[i + 1]) {
    workspaceHint = args[i + 1];
    i++;
  }
}

// --- Detection logic ---

function findWorkspace() {
  // Try hint first
  if (workspaceHint && fs.existsSync(workspaceHint)) return workspaceHint;

  // Try common OpenClaw workspace locations
  const candidates = [
    process.cwd(),
    path.join(__dirname, '..', '..', '..'),  // skill is at workspace/skills/openclaw-dream
  ];

  for (const dir of candidates) {
    const resolved = path.resolve(dir);
    // A workspace should have at least one of these
    if (fs.existsSync(path.join(resolved, 'MEMORY.md')) ||
        fs.existsSync(path.join(resolved, 'SOUL.md')) ||
        fs.existsSync(path.join(resolved, 'memory'))) {
      return resolved;
    }
  }
  return null;
}

function findMemoryDir(workspace) {
  const memDir = path.join(workspace, 'memory');
  if (fs.existsSync(memDir) && fs.statSync(memDir).isDirectory()) return memDir;
  return null;
}

function findIdentityFiles(workspace) {
  const files = {};
  for (const name of ['MEMORY.md', 'SOUL.md', 'IDENTITY.md', 'USER.md', 'LEARN.md']) {
    const p = path.join(workspace, name);
    if (fs.existsSync(p)) files[name] = p;
  }
  return files;
}

function findAgentSessions(workspace) {
  // Walk up from workspace to find .openclaw/agents/
  let dir = workspace;
  while (true) {
    const agentsDir = path.join(dir, '.openclaw', 'agents');
    if (fs.existsSync(agentsDir)) {
      // Find agent dirs with sessions/
      const agents = fs.readdirSync(agentsDir).filter(d => {
        const sessDir = path.join(agentsDir, d, 'sessions');
        return fs.existsSync(sessDir) && fs.statSync(sessDir).isDirectory();
      });
      if (agents.length > 0) {
        // Pick the agent with the most session files (likely the primary agent)
        let best = null;
        let bestCount = 0;
        for (const agent of agents) {
          const sessDir = path.join(agentsDir, agent, 'sessions');
          const files = fs.readdirSync(sessDir).filter(f => f.endsWith('.jsonl'));
          if (files.length > bestCount) {
            bestCount = files.length;
            best = { agentId: agent, sessionsPath: sessDir };
          }
        }
        if (best) return best;
      }
    }
    const parent = path.dirname(dir);
    if (parent === dir) break;  // reached filesystem root
    dir = parent;
  }
  return null;
}

function findDreamsDir(memoryDir) {
  if (!memoryDir) return null;
  const dreamsDir = path.join(memoryDir, 'dreams');
  if (fs.existsSync(dreamsDir)) return dreamsDir;
  return null;
}

// --- Run ---

const workspace = findWorkspace();
if (!workspace) {
  console.error('❌ Could not detect workspace. Run from your workspace directory or pass --workspace <path>');
  process.exit(1);
}

const memoryDir = findMemoryDir(workspace);
const identityFiles = findIdentityFiles(workspace);
const sessionInfo = findAgentSessions(workspace);
const dreamsDir = findDreamsDir(memoryDir);

const config = {
  version: 1,
  workspace: workspace,
  memoryDir: memoryDir,
  dreamsDir: dreamsDir || (memoryDir ? path.join(memoryDir, 'dreams') : null),
  dreamLock: dreamsDir ? path.join(dreamsDir, '.dream-lock') : null,
  identityFiles: identityFiles,
  sessionsPath: sessionInfo ? sessionInfo.sessionsPath : null,
  agentId: sessionInfo ? sessionInfo.agentId : null,
  memoryIndexFile: identityFiles['MEMORY.md'] || null,
  learnFile: identityFiles['LEARN.md'] || null,
  allowMemoryRewrite: null,  // null = not yet decided, will be asked on first dream
  createdAt: new Date().toISOString(),
};

// Report
console.log('🌙 OpenClaw Dream — Setup');
console.log('');
console.log(`Workspace:    ${workspace}`);
console.log(`Memory dir:   ${memoryDir || '❌ not found'}`);
console.log(`Dreams dir:   ${config.dreamsDir || '❌ not found'}`);
console.log(`Sessions:     ${sessionInfo ? `${sessionInfo.sessionsPath} (agent: ${sessionInfo.agentId})` : '❌ not found'}`);
console.log(`Identity files:`);
for (const [name, p] of Object.entries(identityFiles)) {
  console.log(`  ✅ ${name}`);
}
const missing = ['MEMORY.md', 'SOUL.md'].filter(n => !identityFiles[n]);
if (missing.length > 0) {
  console.log(`  ⚠️  Missing: ${missing.join(', ')}`);
}
console.log('');

// Warnings
const warnings = [];
if (!memoryDir) warnings.push('No memory/ directory found. Dream will create one.');
if (!sessionInfo) warnings.push('No session files found. Dream gate check will always skip until sessions accumulate.');
if (!identityFiles['MEMORY.md']) warnings.push('No MEMORY.md found. Dream will create one on first run.');
if (!identityFiles['SOUL.md']) warnings.push('No SOUL.md found. Self-reflection will be limited.');

if (warnings.length > 0) {
  console.log('⚠️  Warnings:');
  warnings.forEach(w => console.log(`   ${w}`));
  console.log('');
}

// Save config
fs.mkdirSync(ASSETS_DIR, { recursive: true });
fs.writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2));
console.log(`✅ Config saved: ${CONFIG_FILE}`);

// === Auto-approve prompt ===
const readline = require('readline');
const rl = readline.createInterface({ input: process.stdin, output: process.stdout });

console.log('');
console.log('🌙 梦境系统授权');
console.log('梦境系统将自动整理你的AI记忆，包括：');
console.log('- 读取会话记录和每日笔记');
console.log('- 更新 MEMORY.md（自动备份）');
console.log('- 标记/删除过期条目');
console.log('- 生成梦境自省报告');
console.log('\n执行频率：每天凌晨3点，约5分钟完成。');
console.log('每次执行后会发送报告，支持回滚。');

rl.question('\n是否授权自动执行？(y/n，默认y): ', (answer) => {
  const autoApprove = answer.toLowerCase() !== 'n';
  config.autoApprove = autoApprove;

  // 重新写入配置
  fs.writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2));

  console.log(autoApprove
    ? '✅ 已授权自动执行。首次执行将在下次 cron 触发时开始。'
    : '⏸️ 未授权自动执行。你可以手动运行或稍后在 dream-config.json 中设置 autoApprove: true。');

  console.log('\nNext: configure a cron job to run the dream. See SKILL.md for details.');
  rl.close();
});
