#!/usr/bin/env node
/**
 * NewsToday — 话题偏好管理
 *
 * 用法:
 *   node preference.js show <userId>              查看当前偏好
 *   node preference.js set <userId> <话题> <权重>  设置话题权重（0.0 - 1.0）
 *   node preference.js reset <userId>             重置为默认偏好
 *
 * 话题: 科技 财经 国际 社会 娱乐 体育
 * 权重: 0.0（不感兴趣）~ 1.0（最感兴趣）
 */

const fs = require('fs');
const path = require('path');

const USERS_DIR = path.join(__dirname, '../data/users');
const ALLOWED_TOPICS = ['科技', '财经', '国际', '社会', '娱乐', '体育'];
const TOPIC_MAP = { tech: '科技', finance: '财经', international: '国际', society: '社会', entertainment: '娱乐', sports: '体育' };
const DEFAULT_TOPICS = { 科技: 0.8, 财经: 0.8, 国际: 0.7, 社会: 0.6, 娱乐: 0.3, 体育: 0.3 };

function sanitizeId(value) {
  if (typeof value !== 'string' || !/^[a-zA-Z0-9_-]{1,128}$/.test(value)) {
    console.error('❌ 无效的 userId');
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

function loadUser(userId) {
  const f = safeUserPath(userId);
  if (!fs.existsSync(f)) {
    console.error(`❌ 未找到用户 ${userId}，请先运行: node register.js ${userId}`);
    process.exit(1);
  }
  return JSON.parse(fs.readFileSync(f, 'utf8'));
}

function saveUser(userId, data) {
  fs.writeFileSync(safeUserPath(userId), JSON.stringify(data, null, 2), 'utf8');
}

function bar(weight) {
  const filled = Math.round(weight * 10);
  return '█'.repeat(filled) + '░'.repeat(10 - filled);
}

const args = process.argv.slice(2);
const command = args[0];
const userId  = args[1] ? sanitizeId(args[1]) : null;

if (!command || !userId) {
  console.log(`用法:
  node preference.js show <userId>
  node preference.js set <userId> <话题> <权重0-1>
  node preference.js reset <userId>`);
  process.exit(1);
}

switch (command) {
  case 'show': {
    const user = loadUser(userId);
    const topics = user.topics || DEFAULT_TOPICS;
    console.log(`\n📌 话题偏好 — ${userId}\n${'━'.repeat(30)}`);
    for (const t of ALLOWED_TOPICS) {
      const w = topics[t] ?? 0.5;
      console.log(`  ${t.padEnd(4)}  ${bar(w)}  ${(w * 10).toFixed(0)}/10`);
    }
    console.log('━'.repeat(30));
    console.log(`语言：${user.language === 'en' ? 'English' : '中文'}  渠道：${user.channel || 'telegram'}`);
    break;
  }

  case 'set': {
    const rawTopic = args[2];
    const rawWeight = args[3];
    if (!rawTopic || rawWeight === undefined) {
      console.error('用法: node preference.js set <userId> <话题> <权重0-1>');
      process.exit(1);
    }
    const topic = TOPIC_MAP[rawTopic] || rawTopic;
    if (!ALLOWED_TOPICS.includes(topic)) {
      console.error(`❌ 无效话题：${rawTopic}。可用：${ALLOWED_TOPICS.join(', ')}`);
      process.exit(1);
    }
    const weight = parseFloat(rawWeight);
    if (isNaN(weight) || weight < 0 || weight > 1) {
      console.error('❌ 权重须在 0.0 ~ 1.0 之间');
      process.exit(1);
    }
    const user = loadUser(userId);
    user.topics = user.topics || { ...DEFAULT_TOPICS };
    user.topics[topic] = weight;
    user.updatedAt = new Date().toISOString();
    saveUser(userId, user);
    console.log(`✅ 已设置「${topic}」权重为 ${weight.toFixed(1)}`);
    break;
  }

  case 'reset': {
    const user = loadUser(userId);
    user.topics = { ...DEFAULT_TOPICS };
    user.updatedAt = new Date().toISOString();
    saveUser(userId, user);
    console.log(`✅ 话题偏好已重置为默认值`);
    break;
  }

  default:
    console.error(`❌ 未知命令: ${command}`);
    process.exit(1);
}
