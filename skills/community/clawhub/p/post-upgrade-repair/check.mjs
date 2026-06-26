#!/usr/bin/env node
/**
 * OpenClaw 升级后健康检查脚本（可分享版本）
 * 自动检测常见问题，调用 AI 获取修复方案
 */

import { execSync } from 'child_process';
import { existsSync, readFileSync, writeFileSync } from 'fs';
import { join, dirname } from 'path';
import { homedir } from 'os';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const HOME = homedir();
const OPENCLAW_WORKSPACE = join(HOME, '.openclaw', 'workspace');
const CC_SCRIPT = join(OPENCLAW_WORKSPACE, 'skills', 'openclaw-repair-kit', 'run.mjs');
const CONFIG_PATH = join(HOME, '.openclaw', 'openclaw.json');

// 自动修复已知的配置字段变更
function autoFixConfig() {
  const fixes = [];
  let config;
  try {
    config = JSON.parse(readFileSync(CONFIG_PATH, 'utf8'));
  } catch {
    return fixes;
  }

  let changed = false;
  const feishu = config?.channels?.feishu;

  // 修复1: dmAllowlist → allowFrom（2026.2.24）
  if (feishu?.dmAllowlist && !feishu?.allowFrom) {
    config.channels.feishu.allowFrom = feishu.dmAllowlist;
    delete config.channels.feishu.dmAllowlist;
    fixes.push('✅ 自动修复：飞书 dmAllowlist → allowFrom');
    changed = true;
  }

  // 修复2: streamMode → streaming（2026.2.24）
  const telegram = config?.channels?.telegram;
  if (telegram?.streamMode && !telegram?.streaming) {
    config.channels.telegram.streaming = telegram.streamMode;
    delete config.channels.telegram.streamMode;
    fixes.push('✅ 自动修复：Telegram streamMode → streaming');
    changed = true;
  }

  // 修复3: agents.defaults.model.image 字段移除
  if (config?.agents?.defaults?.model?.image) {
    delete config.agents.defaults.model.image;
    fixes.push('✅ 自动修复��移除 agents.defaults.model.image（新版不支持）');
    changed = true;
  }

  // 修复4: feishu dmPolicy "auto" 不合法
  if (feishu?.dmPolicy === 'auto') {
    config.channels.feishu.dmPolicy = 'allowlist';
    fixes.push('✅ 自动修复：飞书 dmPolicy "auto" → "allowlist"');
    changed = true;
  }

  if (changed) {
    writeFileSync(CONFIG_PATH, JSON.stringify(config, null, 2), 'utf8');
  }

  return fixes;
}

// 自动检测 openclaw 命令
function getOpenclawCmd() {
  try {
    execSync('openclaw --version', { encoding: 'utf8', timeout: 5000, stdio: 'pipe' });
    return 'openclaw';
  } catch {
    // 尝试 npm 全局路径
    const npmPaths = [
      join(HOME, 'AppData', 'Roaming', 'npm', 'node_modules', 'openclaw', 'dist', 'index.js'),
      '/usr/local/lib/node_modules/openclaw/dist/index.js',
      '/usr/lib/node_modules/openclaw/dist/index.js',
    ];
    for (const p of npmPaths) {
      if (existsSync(p)) return `node "${p}"`;
    }
    return null;
  }
}

const openclawCmd = getOpenclawCmd();
if (!openclawCmd) {
  console.error('❌ 找不到 openclaw 命令，请确认 OpenClaw 已安装（npm install -g openclaw）');
  process.exit(1);
}

function run(cmd) {
  try {
    return execSync(`${openclawCmd} ${cmd}`, { encoding: 'utf8', timeout: 15000, stdio: 'pipe' });
  } catch (e) {
    return (e.stdout || '') + (e.stderr || '');
  }
}

console.log('🔍 正在检查 OpenClaw 健康状态...\n');

// 先尝试自动修复已知问题
const autoFixes = autoFixConfig();
if (autoFixes.length > 0) {
  console.log('🔧 自动修复已知配置问题：');
  autoFixes.forEach(f => console.log(' ', f));
  console.log('');
}

const issues = [];

// 1. 检查 config 是否有效
const version = run('--version');
if (version.includes('Invalid config')) {
  const match = version.match(/- (.+)/g);
  issues.push(`❌ 配置文件错误:\n${match ? match.join('\n') : version.trim()}`);
} else {
  console.log(`✅ 版本：${version.trim()}`);
}

// 2. 检查 channels 是否连接
const status = run('status');
const channelSection = status.match(/Channels[\s\S]*?Sessions/)?.[0] || '';
if (channelSection.includes('└──') && !channelSection.match(/│\s+\w+\s+│\s+(true|false)/)) {
  console.log('⚠️  Channels 表格为空。');
  console.log('');
  console.log('👉 【第一步】请先重启 KKClaw，然后重新运行此脚本。');
  console.log('   重启后如果飞书/Telegram 恢复正常，说明是重启生效了，无需继续。');
  console.log('   重启后仍然空白，说明配置有问题，脚本会自动联系 CC 修复。');
  console.log('');
  issues.push('❌ Channels 表格为空，飞书/Telegram 均未连接（如已重启仍未恢复，可能是升级后配置字段变更）');
} else {
  console.log('✅ 频道连接正常');
}

// 3. 检查 memory
const memStatus = run('memory');
if (memStatus.includes('fetch failed') || memStatus.includes('index failed')) {
  issues.push(`❌ 记忆同步失败（通常是 OpenAI embeddings 无法访问）:\n${memStatus.trim()}`);
} else {
  console.log('✅ 记忆状态正常');
}

// 4. 检查 doctor
const doctor = run('doctor');
if (doctor.includes('Config invalid') || doctor.includes('Invalid config') || doctor.includes('Unrecognized key')) {
  issues.push(`❌ Doctor 发现配置问题:\n${doctor.substring(0, 800)}`);
} else {
  console.log('✅ Doctor 检查通过');
}

console.log('');

if (issues.length === 0) {
  console.log('✅ 所有检查通过，OpenClaw 运行正常！');
  process.exit(0);
}

// 发现问题
console.log(`⚠️  发现 ${issues.length} 个问题：\n`);
issues.forEach(i => console.log(i + '\n'));

// 检查 CC 是否可用
if (!existsSync(CC_SCRIPT)) {
  console.log('💡 修复建议：');
  console.log('1. 确认 openclaw-repair-kit 已正确安装到：', join(OPENCLAW_WORKSPACE, 'skills', 'openclaw-repair-kit'));
  console.log('2. 重新运行 node install.mjs 安装');
  process.exit(1);
}

const configPath = join(HOME, '.openclaw', 'openclaw.json');
const problemReport = `OpenClaw 升级后自动检查发现以下问题，请帮我修复：

${issues.join('\n\n')}

当前版本：${version.trim()}

openclaw status 输出（节选）：
${status.substring(0, 1200)}

配置文件路径：${configPath}

请分析问题原因并给出具体的修复步骤。`;

console.log('🔧 正在联系 CC 获取修复方案...\n');

try {
  const result = execSync(
    `node "${CC_SCRIPT}" ${JSON.stringify(problemReport)}`,
    { encoding: 'utf8', timeout: 60000 }
  );
  console.log('📋 CC 的修复方案：\n');
  console.log(result);
} catch (e) {
  console.error('调用 CC 失败:', e.message);
  console.log('\n请手动将上方问题报告发给 CC（claude-code-agent）处理。');
}
