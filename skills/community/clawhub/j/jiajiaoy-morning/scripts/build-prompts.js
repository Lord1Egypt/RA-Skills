#!/usr/bin/env node
/**
 * jiajiaoy-morning — 早间简报 prompt 构建器
 *
 * 读取用户配置，依次运行各模块脚本，输出 JSON 数组供 agent 执行。
 *
 * 用法：
 *   node build-prompts.js <userId>               # 输出 JSON
 *   node build-prompts.js <userId> --cron-message # 输出单条 cron payload 消息
 */

'use strict';

const { execSync } = require('child_process');
const fs   = require('fs');
const path = require('path');

const USERS_DIR   = path.join(__dirname, '../data/users');
const SKILLS_BASE = path.join(__dirname, '../../');

// ── 依赖检查 ──────────────────────────────────────────────────────────────────
const REQUIRED_SKILLS = [
  { slug: 'newstoady',    script: 'scripts/morning-push.js' },
  { slug: 'dailytech',   script: 'scripts/morning-push.js' },
  { slug: 'dailyfinance',script: 'scripts/morning-push.js' },
  { slug: 'weather-daily',script: 'scripts/morning-push.js' },
  { slug: 'yunshi',      script: 'scripts/daily-push.js' },
  { slug: 'daily-history',script: 'scripts/morning-push.js' },
  { slug: 'daily-recipe',script: 'scripts/morning-push.js' },
  { slug: 'daily-quote', script: 'scripts/morning-push.js' },
  { slug: 'daily-mindful',script: 'scripts/morning-push.js' },
  { slug: 'daily-fitness',script: 'scripts/morning-push.js' },
  { slug: 'english-daily',script: 'scripts/daily-push.js' },
];

const missing = REQUIRED_SKILLS.filter(dep =>
  !fs.existsSync(path.join(SKILLS_BASE, dep.slug, dep.script))
);

if (missing.length > 0) {
  const skillsDir = path.resolve(SKILLS_BASE);
  console.error('❌ 缺少依赖 skill，请先安装：\n');
  console.error(`cd "${skillsDir}"\n`);
  missing.forEach(dep => {
    console.error(`clawhub install ${dep.slug}`);
  });
  console.error('\n安装完成后重新运行本脚本。');
  process.exit(1);
}

function sanitizeId(v) {
  if (typeof v !== 'string' || !/^[a-zA-Z0-9_@-]{1,128}$/.test(v)) {
    console.error('❌ 无效的 userId'); process.exit(1);
  }
  return v;
}

function safeUserPath(userId) {
  const resolved = path.resolve(USERS_DIR, `${userId}.json`);
  if (!resolved.startsWith(path.resolve(USERS_DIR) + path.sep)) {
    console.error('❌ 非法路径'); process.exit(1);
  }
  return resolved;
}

const args    = process.argv.slice(2);
const userId  = sanitizeId(args[0] || '8603011439');
const cronMsg = args.includes('--cron-message');

// ── 读取用户配置 ──────────────────────────────────────────────────────────────
let config = null;
const configPath = safeUserPath(userId);
if (fs.existsSync(configPath)) {
  config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
}
const mods = config?.modules?.morning || {};

// ── 模块定义（含开关 key） ─────────────────────────────────────────────────────
const ALL_MODULES = [
  {
    key: 'news',
    name: '早报',
    emoji: '📰',
    script: `${SKILLS_BASE}newstoady/scripts/morning-push.js`,
    args: ['--lang', 'zh'],
    searchRequired: true,
    group: 1,
  },
  {
    key: 'tech',
    name: '科技新闻',
    emoji: '💻',
    script: `${SKILLS_BASE}dailytech/scripts/morning-push.js`,
    args: [userId],
    searchRequired: true,
    group: 1,
  },
  {
    key: 'finance',
    name: '财经新闻',
    emoji: '💰',
    script: `${SKILLS_BASE}dailyfinance/scripts/morning-push.js`,
    args: [userId],
    searchRequired: true,
    group: 1,
  },
  {
    key: 'weather',
    name: '天气',
    emoji: '🌤️',
    script: `${SKILLS_BASE}weather-daily/scripts/morning-push.js`,
    args: [userId],
    searchRequired: true,
    group: 1,
  },
  {
    key: 'yunshi',
    name: '今日运势',
    emoji: '🔮',
    script: `${SKILLS_BASE}yunshi/scripts/daily-push.js`,
    args: ['--test', userId],
    searchRequired: false,
    group: 2,
  },
  {
    key: 'history',
    name: '历史上的今天',
    emoji: '📅',
    script: `${SKILLS_BASE}daily-history/scripts/morning-push.js`,
    args: [userId],
    searchRequired: true,
    group: 2,
  },
  {
    key: 'recipe',
    name: '今日菜谱',
    emoji: '🍳',
    script: `${SKILLS_BASE}daily-recipe/scripts/morning-push.js`,
    args: [userId],
    searchRequired: false,
    group: 2,
  },
  {
    key: 'quote',
    name: '每日名言',
    emoji: '💬',
    script: `${SKILLS_BASE}daily-quote/scripts/morning-push.js`,
    args: [userId],
    searchRequired: false,
    group: 3,
  },
  {
    key: 'mindful',
    name: '正念冥想',
    emoji: '🧘',
    script: `${SKILLS_BASE}daily-mindful/scripts/morning-push.js`,
    args: [userId],
    searchRequired: false,
    group: 3,
  },
  {
    key: 'fitness',
    name: '每日运动',
    emoji: '💪',
    script: `${SKILLS_BASE}daily-fitness/scripts/morning-push.js`,
    args: [userId],
    searchRequired: false,
    group: 3,
  },
  {
    key: 'english',
    name: '每日英语',
    emoji: '📚',
    script: `${SKILLS_BASE}english-daily/scripts/daily-push.js`,
    args: [userId],
    searchRequired: false,
    group: 3,
  },
];

// 如果有用户配置，按配置过滤；没有配置则全开
const MODULES = config
  ? ALL_MODULES.filter(m => mods[m.key] !== false)
  : ALL_MODULES;

// ── 执行脚本 ──────────────────────────────────────────────────────────────────
function runScript(scriptPath, scriptArgs) {
  try {
    const cmd = `node "${scriptPath}" ${scriptArgs.map(a => `"${a}"`).join(' ')}`;
    const output = execSync(cmd, { timeout: 10000, encoding: 'utf8', stdio: ['pipe','pipe','pipe'] });
    return { ok: true, prompt: output.trim() };
  } catch (err) {
    const stderr = err.stderr ? err.stderr.toString().trim() : '';
    return { ok: false, error: stderr || err.message };
  }
}

// ── 执行所有模块 ──────────────────────────────────────────────────────────────
const results = [];
for (const mod of MODULES) {
  const res = runScript(mod.script, mod.args);
  results.push({
    key:            mod.key,
    module:         mod.name,
    emoji:          mod.emoji,
    group:          mod.group,
    prompt:         res.ok ? res.prompt : null,
    searchRequired: mod.searchRequired,
    error:          res.ok ? undefined : res.error,
  });
}

// ── 输出模式 ──────────────────────────────────────────────────────────────────
if (cronMsg) {
  // --cron-message：输出供 cron payload 使用的 agent 指令
  const now = new Date();
  const WEEKDAYS = ['星期日','星期一','星期二','星期三','星期四','星期五','星期六'];
  const dateStr = `${now.getFullYear()}年${now.getMonth()+1}月${now.getDate()}日 ${WEEKDAYS[now.getDay()]}`;
  const name = config?.name || userId;

  const groups = { 1: [], 2: [], 3: [] };
  for (const r of results) {
    if (r.prompt) groups[r.group].push(`${r.emoji} ${r.module}\n${r.prompt}`);
    else if (r.error) groups[r.group].push(`${r.emoji} ${r.module}\n⚠️ 加载失败，跳过`);
  }

  const GROUP_LABELS = {
    1: '📡 今日资讯',
    2: '🌿 生活情报',
    3: '✨ 成长能量',
  };

  let msgs = [];
  for (const [g, items] of Object.entries(groups)) {
    if (items.length === 0) continue;
    msgs.push(`━━━━━ ${GROUP_LABELS[g]} ━━━━━\n${items.join('\n\n')}`);
  }

  console.log(`请执行每日早间简报（jiajiaoy-morning skill）。

步骤：
1. 运行脚本获取所有模块的执行指令：
\`\`\`bash
node ${__filename} ${userId}
\`\`\`

2. 将 JSON 中每个模块的 prompt 依次执行（searchRequired=true 的需要 WebSearch）

3. 按 group 字段分 3 组，每组汇总后各发送一条消息：
   - 消息1（group=1）：📰早报 + 💻科技 + 💰财经 + 🌤️天气
   - 消息2（group=2）：🔮运势 + 📅历史 + 🍳菜谱
   - 消息3（group=3）：💬名言 + 🧘正念 + 💪运动 + 📚英语

4. 每条消息头部加：🌅 早安 ${name}！${dateStr}

某个模块报错时跳过，不影响其余正常发送。`);
} else {
  // 默认：输出 JSON
  process.stdout.write(JSON.stringify(results, null, 2));
}
