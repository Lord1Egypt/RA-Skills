#!/usr/bin/env node
/**
 * NewsToday — 用户注册 / 偏好设置
 *
 * 用法:
 *   node register.js <userId> [language] [topics] [channel]
 *
 * 参数:
 *   userId    必填，字母/数字/-/_，1-128 字符
 *   language  可选，zh（默认）或 en
 *   topics    可选，逗号分隔的偏好话题（如 科技,财经,国际）
 *             可选值: 科技 财经 国际 社会 娱乐 体育
 *   channel   可选，telegram/feishu/slack/discord（默认 telegram）
 *
 * 示例:
 *   node register.js alice
 *   node register.js bob zh 科技,财经,国际
 *   node register.js carol en tech,finance,international telegram
 */

const fs = require('fs');
const path = require('path');

const USERS_DIR = path.join(__dirname, '../data/users');

const ALLOWED_TOPICS_ZH = ['科技', '财经', '国际', '社会', '娱乐', '体育'];
const ALLOWED_TOPICS_EN = ['tech', 'finance', 'international', 'society', 'entertainment', 'sports'];
const TOPIC_MAP = { tech: '科技', finance: '财经', international: '国际', society: '社会', entertainment: '娱乐', sports: '体育' };
const ALLOWED_CHANNELS = new Set(['telegram', 'feishu', 'slack', 'discord']);

function sanitizeId(value) {
  if (typeof value !== 'string' || !/^[a-zA-Z0-9_-]{1,128}$/.test(value)) {
    console.error('❌ 无效的 userId：只允许字母、数字、- 和 _，长度 1-128');
    process.exit(1);
  }
  return value;
}

function safeUserPath(userId) {
  const resolved = path.resolve(USERS_DIR, `${userId}.json`);
  if (!resolved.startsWith(path.resolve(USERS_DIR) + path.sep)) {
    console.error('❌ 非法路径');
    process.exit(1);
  }
  return resolved;
}

function sanitizeLanguage(value) {
  if (value !== 'zh' && value !== 'en') {
    console.error('❌ 无效的语言：请使用 zh 或 en');
    process.exit(1);
  }
  return value;
}

function sanitizeTopics(value, language) {
  const allowed = language === 'en' ? ALLOWED_TOPICS_EN : ALLOWED_TOPICS_ZH;
  const raw = value.split(',').map(t => t.trim()).filter(Boolean);
  const weights = {};
  for (const t of raw) {
    const mapped = TOPIC_MAP[t] || t;
    if (!ALLOWED_TOPICS_ZH.includes(mapped)) {
      console.error(`❌ 无效的话题：${t}。可用值：${[...ALLOWED_TOPICS_ZH, ...ALLOWED_TOPICS_EN].join(', ')}`);
      process.exit(1);
    }
    weights[mapped] = 1.0;
  }
  // 未指定的话题给默认权重 0.5
  for (const t of ALLOWED_TOPICS_ZH) {
    if (!(t in weights)) weights[t] = 0.5;
  }
  return weights;
}

const DEFAULT_TOPICS = { 科技: 0.8, 财经: 0.8, 国际: 0.7, 社会: 0.6, 娱乐: 0.3, 体育: 0.3 };

const args = process.argv.slice(2);
if (!args[0]) {
  console.log(`用法:
  node register.js <userId> [language] [topics] [channel]

参数:
  userId    字母/数字/-/_，1-128 字符
  language  zh（默认）或 en
  topics    逗号分隔偏好话题（如 科技,财经,国际）
  channel   telegram/feishu/slack/discord（默认 telegram）

示例:
  node register.js alice
  node register.js bob zh 科技,财经,国际
  node register.js carol en tech,finance,international`);
  process.exit(1);
}

const userId   = sanitizeId(args[0]);
const language = args[1] ? sanitizeLanguage(args[1]) : 'zh';
const topics   = args[2] ? sanitizeTopics(args[2], language) : { ...DEFAULT_TOPICS };
const rawCh    = args[3] || 'telegram';
if (!ALLOWED_CHANNELS.has(rawCh)) {
  console.error(`❌ 无效渠道：${rawCh}。支持：${[...ALLOWED_CHANNELS].join(', ')}`);
  process.exit(1);
}
const channel = rawCh;

fs.mkdirSync(USERS_DIR, { recursive: true });
const filePath = safeUserPath(userId);
const now = new Date().toISOString();

let existing = null;
if (fs.existsSync(filePath)) {
  try { existing = JSON.parse(fs.readFileSync(filePath, 'utf8')); } catch (_) {}
}

const profile = {
  userId,
  language,
  topics,
  channel,
  push: existing?.push || { enabled: false },
  createdAt: existing?.createdAt || now,
  updatedAt: now
};

fs.writeFileSync(filePath, JSON.stringify(profile, null, 2), 'utf8');

const topList = Object.entries(topics).filter(([,w]) => w >= 0.7).map(([t]) => t).join('、');

console.log(`
✅ 注册成功

👤 用户：${userId}
🌐 语言：${language === 'zh' ? '中文' : 'English'}
📌 重点话题：${topList || '默认'}
📡 推送渠道：${channel}

下一步：
  调整话题偏好：node scripts/preference.js set ${userId} <话题> <权重0-1>
  开启每日推送：node scripts/push-toggle.js on ${userId}
  获取今日早报：node scripts/morning-push.js ${userId}`);
