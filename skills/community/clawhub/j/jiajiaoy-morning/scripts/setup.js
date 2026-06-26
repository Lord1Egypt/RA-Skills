#!/usr/bin/env node
/**
 * jiajiaoy-morning — 首次安装向导
 *
 * 输出一段结构化问卷 prompt，由 agent 向用户提问后
 * 将回答传回：node setup.js --save '<json>'
 *
 * 用法：
 *   node setup.js                        # 输出问卷 prompt（供 agent 展示给用户）
 *   node setup.js --save '<json>'        # 保存用户回答并输出 cron 指令
 *   node setup.js --show <userId>        # 查看用户当前配置
 */

'use strict';

const fs   = require('fs');
const path = require('path');

const USERS_DIR   = path.join(__dirname, '../data/users');
const TEMPLATE    = path.join(USERS_DIR, 'template.json');
const SKILLS_BASE = path.join(__dirname, '../../');

// ── 依赖检查（与 build-prompts.js 保持一致）────────────────────────────────────
const REQUIRED_SKILLS = [
  'newstoady', 'dailytech', 'dailyfinance', 'weather-daily',
  'yunshi', 'daily-history', 'daily-recipe', 'daily-quote',
  'daily-mindful', 'daily-fitness', 'english-daily',
];
const missingSkills = REQUIRED_SKILLS.filter(slug =>
  !fs.existsSync(path.join(SKILLS_BASE, slug))
);
if (missingSkills.length > 0) {
  const skillsDir = path.resolve(SKILLS_BASE);
  console.error('❌ 缺少依赖 skill，请先安装：\n');
  console.error(`cd "${skillsDir}"\n`);
  missingSkills.forEach(slug => console.error(`clawhub install ${slug}`));
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

// ── 问卷 prompt（输出给 agent，让 agent 问用户）──────────────────────────────
function printSetupPrompt() {
  console.log(`请按以下步骤帮用户完成 jiajiaoy-morning 早晚简报设置，**逐项询问**，收集完后用 JSON 汇总：

---
**📋 jiajiaoy-morning 设置向导**

请依次询问用户以下问题（可以一次性列出让用户回答）：

**基本信息**
1. 你的名字是？（用于问候语）
2. 所在城市？（用于天气，默认：上海）
3. 早间简报接收渠道？（telegram / feishu，默认：telegram）
4. Telegram 用户ID 或 飞书 OpenID？
5. 晚间运势接收渠道？（同早间 / 单独设置，默认同早间）

**早间模块选择（08:00推送）**
6. 以下模块哪些要开启？（默认全开，可以说"全开"或列出不要的）
   - 📰 早报（今日新闻）
   - 💻 科技新闻
   - 💰 财经新闻
   - 🌤️ 天气
   - 🔮 今日运势
   - 📅 历史上的今天
   - 🍳 今日菜谱
   - 💬 每日名言
   - 🧘 正念冥想
   - 💪 每日运动
   - 📚 每日英语

**晚间模块选择（18:00推送）**
7. 是否开启 🔮 明日运势（18:00推送）？（默认：开启）

---
收集完所有回答后，将答案整理为以下 JSON 格式，然后运行：
\`\`\`bash
node <skills目录>/jiajiaoy-morning/scripts/setup.js --save '<JSON>'
\`\`\`

JSON 格式：
{
  "userId": "<telegram_id 或 feishu_openid>",
  "name": "<名字>",
  "city": "<城市>",
  "morningChannel": "telegram 或 feishu",
  "morningTo": "<接收ID>",
  "eveningChannel": "telegram 或 feishu",
  "eveningTo": "<接收ID>",
  "modules": {
    "news": true, "tech": true, "finance": true, "weather": true,
    "yunshi": true, "history": true, "recipe": true, "quote": true,
    "mindful": true, "fitness": true, "english": true,
    "yunshi_tomorrow": true
  }
}`);
}

// ── 保存配置并输出 cron 指令 ────────────────────────────────────────────────
function saveConfig(jsonStr) {
  let input;
  try {
    input = JSON.parse(jsonStr);
  } catch (e) {
    console.error('❌ JSON 解析失败：', e.message);
    process.exit(1);
  }

  const userId = sanitizeId(input.userId || '');
  const template = JSON.parse(fs.readFileSync(TEMPLATE, 'utf8'));
  const now = new Date().toISOString().split('T')[0];

  const config = {
    ...template,
    userId,
    name:     input.name     || userId,
    city:     input.city     || '上海',
    language: input.language || 'zh',
    channels: {
      morning: { channel: input.morningChannel || 'telegram', to: input.morningTo || userId },
      evening: { channel: input.eveningChannel || input.morningChannel || 'telegram', to: input.eveningTo || input.morningTo || userId },
    },
    modules: {
      morning: {
        news:    input.modules?.news    !== false,
        tech:    input.modules?.tech    !== false,
        finance: input.modules?.finance !== false,
        weather: input.modules?.weather !== false,
        yunshi:  input.modules?.yunshi  !== false,
        history: input.modules?.history !== false,
        recipe:  input.modules?.recipe  !== false,
        quote:   input.modules?.quote   !== false,
        mindful: input.modules?.mindful !== false,
        fitness: input.modules?.fitness !== false,
        english: input.modules?.english !== false,
      },
      evening: {
        yunshi_tomorrow: input.modules?.yunshi_tomorrow !== false,
      },
    },
    createdAt: now,
    updatedAt: now,
  };

  fs.mkdirSync(USERS_DIR, { recursive: true });
  fs.writeFileSync(safeUserPath(userId), JSON.stringify(config, null, 2));

  // 输出 cron 指令供 agent 执行
  const SKILL = __dirname;
  const morningCh  = config.channels.morning.channel;
  const morningTo  = config.channels.morning.to;
  const eveningCh  = config.channels.evening.channel;
  const eveningTo  = config.channels.evening.to;

  console.log(`✅ 用户配置已保存：${userId}（${config.name}）\n`);
  console.log(`📋 请执行以下命令注册定时任务：\n`);

  console.log(`# 早间简报 08:00`);
  console.log(`openclaw cron add \\`);
  console.log(`  --name "jiajiaoy-morning-${userId}" \\`);
  console.log(`  --agent cosmo \\`);
  console.log(`  --schedule "0 8 * * *" \\`);
  console.log(`  --tz "Asia/Shanghai" \\`);
  console.log(`  --timeout 480 \\`);
  console.log(`  --channel ${morningCh} \\`);
  console.log(`  --to ${morningTo} \\`);
  console.log(`  --message "$(node ${SKILL}/build-prompts.js ${userId} --cron-message)"\n`);

  if (config.modules.evening.yunshi_tomorrow) {
    console.log(`# 晚间明日运势 18:00`);
    console.log(`openclaw cron add \\`);
    console.log(`  --name "jiajiaoy-evening-yunshi-${userId}" \\`);
    console.log(`  --agent cosmo \\`);
    console.log(`  --schedule "0 18 * * *" \\`);
    console.log(`  --tz "Asia/Shanghai" \\`);
    console.log(`  --timeout 120 \\`);
    console.log(`  --channel ${eveningCh} \\`);
    console.log(`  --to ${eveningTo} \\`);
    console.log(`  --message "$(node ${SKILL}/evening-push.js ${userId})"\n`);
  }

  console.log(`\n已开启模块：`);
  const mods = config.modules.morning;
  const labels = { news:'📰早报', tech:'💻科技', finance:'💰财经', weather:'🌤️天气', yunshi:'🔮今日运势', history:'📅历史', recipe:'🍳菜谱', quote:'💬名言', mindful:'🧘正念', fitness:'💪运动', english:'📚英语' };
  Object.entries(mods).forEach(([k, v]) => {
    console.log(`  ${v ? '✓' : '✗'} ${labels[k] || k}`);
  });
  if (config.modules.evening.yunshi_tomorrow) {
    console.log(`  ✓ 🔮明日运势（18:00）`);
  }
}

// ── 查看用户配置 ──────────────────────────────────────────────────────────────
function showConfig(userId) {
  const f = safeUserPath(sanitizeId(userId));
  if (!fs.existsSync(f)) {
    console.log(`❌ 用户 ${userId} 未注册。运行 node setup.js 开始设置。`);
    process.exit(1);
  }
  const c = JSON.parse(fs.readFileSync(f, 'utf8'));
  console.log(`👤 ${c.name}（${c.userId}）`);
  console.log(`🏙️  城市：${c.city}`);
  console.log(`📡 早间：${c.channels.morning.channel} → ${c.channels.morning.to}`);
  console.log(`📡 晚间：${c.channels.evening.channel} → ${c.channels.evening.to}`);
  console.log(`\n已开启模块：`);
  const labels = { news:'📰早报', tech:'💻科技', finance:'💰财经', weather:'🌤️天气', yunshi:'🔮今日运势', history:'📅历史', recipe:'🍳菜谱', quote:'💬名言', mindful:'🧘正念', fitness:'💪运动', english:'📚英语' };
  Object.entries(c.modules.morning).forEach(([k, v]) => {
    console.log(`  ${v ? '✓' : '✗'} ${labels[k] || k}`);
  });
  console.log(`  ${c.modules.evening.yunshi_tomorrow ? '✓' : '✗'} 🔮明日运势（18:00）`);
}

// ── 入口 ──────────────────────────────────────────────────────────────────────
const args = process.argv.slice(2);
if (args[0] === '--save' && args[1]) {
  saveConfig(args[1]);
} else if (args[0] === '--show' && args[1]) {
  showConfig(args[1]);
} else {
  printSetupPrompt();
}
