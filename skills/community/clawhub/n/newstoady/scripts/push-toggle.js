#!/usr/bin/env node
/**
 * NewsToday — 推送开关
 *
 * 用法:
 *   node push-toggle.js on <userId>   开启推送
 *   node push-toggle.js off <userId>  关闭推送
 *   node push-toggle.js status <userId>  查看状态
 *
 * 选项:
 *   --morning HH:MM   早报时间（默认 08:00）
 *   --evening HH:MM   晚报时间（默认 20:00）
 *   --channel <name>  推送渠道（默认 telegram）
 */

const fs = require('fs');
const path = require('path');

const USERS_DIR = path.join(__dirname, '../data/users');

// 只允许字母、数字、连字符、下划线，最长 128 字符
function sanitizeId(value, label) {
  if (typeof value !== 'string' || !/^[a-zA-Z0-9_-]{1,128}$/.test(value)) {
    console.error(`❌ 无效的 ${label}：只允许字母、数字、- 和 _，长度 1-128`);
    process.exit(1);
  }
  return value;
}

// 校验 HH:MM 格式，返回 { h, m } 整数
function sanitizeTime(value, label) {
  if (typeof value !== 'string' || !/^\d{1,2}:\d{2}$/.test(value)) {
    console.error(`❌ 无效的 ${label}：格式应为 HH:MM，如 08:00`);
    process.exit(1);
  }
  const [h, m] = value.split(':').map(Number);
  if (h < 0 || h > 23 || m < 0 || m > 59) {
    console.error(`❌ 无效的 ${label}：小时 0-23，分钟 0-59`);
    process.exit(1);
  }
  return { h, m };
}

// 验证文件路径确实在 USERS_DIR 内（防路径穿越）
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
  if (!fs.existsSync(f)) return null;
  return JSON.parse(fs.readFileSync(f, 'utf8'));
}

function saveUser(userId, data) {
  fs.mkdirSync(USERS_DIR, { recursive: true });
  fs.writeFileSync(safeUserPath(userId), JSON.stringify(data, null, 2), 'utf8');
}

const ALLOWED_CHANNELS = new Set(['telegram', 'feishu', 'slack', 'discord']);

function enablePush(userId, opts = {}) {
  userId = sanitizeId(userId, 'userId');

  // 一次性读取用户档案，仅提取原始标量值用于构建 cron 命令
  // push 脚本本身不读文件，偏好通过 CLI 参数传入
  const profile = loadUser(userId);
  const defaultChannel = profile?.channel || 'telegram';
  const defaultTz = 'Asia/Shanghai'; // 不从文件读取 tz，避免不可信数据进入 cron 配置

  // 从档案中提取 lang（仅允许 zh/en）和 topics（仅白名单话题名）
  const ALLOWED_TOPICS = new Set(['科技','财经','国际','社会','娱乐','体育']);
  const profileLang = profile?.language === 'en' ? 'en' : 'zh';
  const profileTopics = profile?.topics
    ? Object.entries(profile.topics)
        .filter(([t, w]) => ALLOWED_TOPICS.has(t) && typeof w === 'number' && w >= 0.7)
        .map(([t]) => t)
        .join(',')
    : '';

  // 构建 push 脚本的 CLI 参数（lang 和 topics 均经过白名单过滤）
  const pushArgs = `--lang ${profileLang}${profileTopics ? ` --topics ${profileTopics}` : ''}`;

  const { h: mh, m: mm } = sanitizeTime(opts.morning || '08:00', 'morning');
  const { h: eh, m: em } = sanitizeTime(opts.evening || '20:00', 'evening');
  const rawChannel = opts.channel || defaultChannel;
  if (!ALLOWED_CHANNELS.has(rawChannel)) {
    console.error(`❌ 不支持的渠道：${rawChannel}。支持：${[...ALLOWED_CHANNELS].join(', ')}`);
    process.exit(1);
  }
  const channel = rawChannel;

  const morningCron = `${mm} ${mh} * * *`;
  const eveningCron = `${em} ${eh} * * *`;

  const sessionKey = `agent:main:${channel}:direct:${userId}`;

  // 早报 cron（lang/topics 已嵌入命令，push 脚本无需再读文件）
  const morningConfig = {
    name: `newstoday-morning-${userId}`,
    cronExpr: morningCron,
    tz: defaultTz,
    session: 'isolated',
    sessionKey,
    channel,
    to: userId,
    announce: true,
    timeoutSeconds: 120,
    message: `node ${path.join(__dirname, 'morning-push.js')} ${pushArgs}`
  };
  console.log(`__OPENCLAW_CRON_ADD__:${JSON.stringify(morningConfig)}`);

  // 晚报 cron
  const eveningConfig = {
    name: `newstoday-evening-${userId}`,
    cronExpr: eveningCron,
    tz: defaultTz,
    session: 'isolated',
    sessionKey,
    channel,
    to: userId,
    announce: true,
    timeoutSeconds: 120,
    message: `node ${path.join(__dirname, 'evening-push.js')} ${pushArgs}`
  };
  console.log(`__OPENCLAW_CRON_ADD__:${JSON.stringify(eveningConfig)}`);

  // 突发新闻检测 cron（每2小时，08:00-22:00）
  const breakingConfig = {
    name: `newstoday-breaking-${userId}`,
    cronExpr: '0 8,10,12,14,16,18,20,22 * * *',
    tz: defaultTz,
    session: 'isolated',
    sessionKey,
    channel,
    to: userId,
    announce: false,
    timeoutSeconds: 60,
    message: `node ${path.join(__dirname, 'breaking-alert.js')} ${pushArgs}`
  };
  console.log(`__OPENCLAW_CRON_ADD__:${JSON.stringify(breakingConfig)}`);

  const morningDisplay = `${String(mh).padStart(2,'0')}:${String(mm).padStart(2,'0')}`;
  const eveningDisplay = `${String(eh).padStart(2,'0')}:${String(em).padStart(2,'0')}`;

  // 更新用户档案中的推送状态（合并，不覆盖话题偏好等字段）
  const updated = {
    ...(profile || {}),
    userId,
    channel,
    push: { enabled: true, morningTime: morningDisplay, eveningTime: eveningDisplay, enabledAt: new Date().toISOString() },
    updatedAt: new Date().toISOString()
  };
  saveUser(userId, updated);

  console.log(`
✅ 每日推送已开启

⏰ 早报：每天 ${morningDisplay}（个性化10条要闻 + RSS）
🌙 晚报：每天 ${eveningDisplay}（收官 + 明日预告）
🚨 突发：每2小时检测（08:00-22:00，有重大事件才提醒）
📡 渠道：${channel}

关闭推送：node push-toggle.js off ${userId}`);
}

function disablePush(userId) {
  userId = sanitizeId(userId, 'userId');
  const user = loadUser(userId);
  if (!user) {
    console.log(`❌ 未找到用户 ${userId} 的推送记录`);
    return;
  }

  console.log(`__OPENCLAW_CRON_RM__:newstoday-morning-${userId}`);
  console.log(`__OPENCLAW_CRON_RM__:newstoday-evening-${userId}`);
  console.log(`__OPENCLAW_CRON_RM__:newstoday-breaking-${userId}`);

  const updated = { ...user, push: { ...(user.push || {}), enabled: false, disabledAt: new Date().toISOString() }, updatedAt: new Date().toISOString() };
  saveUser(userId, updated);
  console.log(`✅ 推送已关闭`);
}

function showStatus(userId) {
  userId = sanitizeId(userId, 'userId');
  const user = loadUser(userId);
  if (!user) {
    console.log(`❌ 未找到用户 ${userId} 的推送记录`);
    return;
  }
  const push = user.push || {};
  const topTopics = Object.entries(user.topics || {})
    .filter(([,w]) => w >= 0.7).map(([t]) => t).join('、') || '默认';

  console.log(`
📡 推送状态 — ${userId}
━━━━━━━━━━━━━━━━━━━━━━━
状态：${push.enabled ? '✅ 开启中' : '❌ 已关闭'}
早报：${push.morningTime || '08:00'}
晚报：${push.eveningTime || '20:00'}
突发：每2小时检测（重大事件才提醒）
渠道：${user.channel || 'telegram'}
语言：${user.language === 'en' ? 'English' : '中文'}
重点话题：${topTopics}
开启于：${push.enabledAt ? push.enabledAt.split('T')[0] : '未知'}
━━━━━━━━━━━━━━━━━━━━━━━`);
}

module.exports = { enablePush, disablePush, showStatus };

if (require.main !== module) return;

const args = process.argv.slice(2);
const command = args[0];
const userId = args[1];

if (!command || !userId) {
  console.log(`用法:
  node push-toggle.js on <userId> [--morning 08:00] [--evening 20:00] [--channel telegram]
  node push-toggle.js off <userId>
  node push-toggle.js status <userId>`);
  process.exit(1);
}

const opts = {};
const mi = args.indexOf('--morning');
if (mi !== -1) opts.morning = args[mi + 1];
const ei = args.indexOf('--evening');
if (ei !== -1) opts.evening = args[ei + 1];
const ci = args.indexOf('--channel');
if (ci !== -1) opts.channel = args[ci + 1];

switch (command) {
  case 'on':     enablePush(userId, opts); break;
  case 'off':    disablePush(userId); break;
  case 'status': showStatus(userId); break;
  default:
    console.log(`❌ 未知命令: ${command}`);
    process.exit(1);
}
