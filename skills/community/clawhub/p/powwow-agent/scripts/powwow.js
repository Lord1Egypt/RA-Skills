#!/usr/bin/env node
/**
 * PowPow Agent Skill CLI
 * 把 OpenClaw agent 放上泡泡地图：登录 / 创建数字人 / 管理订阅 / 与地图访客对话
 * 零依赖（Node 18+ 原生 fetch）；凭据保存在 skill 根目录 credentials.json（勿提交/发布）
 */

'use strict';

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const BASE_URL = (process.env.POWPOW_API_BASE || 'https://global.powpow.online').replace(/\/+$/, '');
const SINK_URL = `${BASE_URL}/api/openclaw/webhook/sink`;
const CRED_FILE = path.join(__dirname, '..', 'credentials.json');
const CHANNEL_PLUGIN = 'clawhub:@durenzidu/openclaw-channel-powpow';

// ----------------------------------------------------------------------------
// 凭据
// ----------------------------------------------------------------------------

function loadCred() {
  try {
    return JSON.parse(fs.readFileSync(CRED_FILE, 'utf8'));
  } catch {
    return null;
  }
}

function saveCred(cred) {
  fs.writeFileSync(CRED_FILE, JSON.stringify(cred, null, 2) + '\n');
}

function authHeader(cred) {
  if (!cred?.token) {
    fail('未登录。先执行：node scripts/powwow.js login --username <邮箱> --password <密码>');
  }
  return { Authorization: `Bearer ${cred.token}` };
}

// ----------------------------------------------------------------------------
// 工具
// ----------------------------------------------------------------------------

// fail() 抛出的哨兵：消息已打印、退出码已设，顶层只负责兜底退出
const FAIL_SENTINEL = Symbol('cli-fail');

function fail(msg) {
  console.error(msg);
  // 不同步 process.exit：Node(<=24.13, Win) 强退会撕裂 undici keep-alive 句柄
  // 触发 libuv assertion。抛哨兵中断执行，由顶层统一非零退出。
  process.exitCode = 1;
  throw FAIL_SENTINEL;
}

function parseArgs(argv) {
  const cmd = argv[0] || 'help';
  const flags = {};
  for (let i = 1; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith('--')) {
      const key = a.slice(2);
      const next = argv[i + 1];
      if (next !== undefined && !next.startsWith('--')) {
        flags[key] = next;
        i++;
      } else {
        flags[key] = true;
      }
    }
  }
  return { cmd, flags };
}

async function api(method, url, body, headers = {}) {
  let res;
  try {
    res = await fetch(BASE_URL + url, {
      method,
      headers: { 'Content-Type': 'application/json', 'Connection': 'close', ...headers },
      body: body ? JSON.stringify(body) : undefined,
      signal: AbortSignal.timeout(30000),
    });
  } catch (err) {
    return { ok: false, status: 0, data: { error: `网络请求失败：${err.message}` } };
  }
  const data = await res.json().catch(() => null);
  return { ok: res.ok, status: res.status, data };
}

function ensureOk(result, action) {
  if (!result.ok || !result.data?.success) {
    if (result.status === 401) {
      fail(`${action}失败：登录已过期或未登录（HTTP 401）。请重新执行 login 命令。`);
    }
    fail(`${action}失败 (HTTP ${result.status})：${result.data?.error || '未知错误'}`);
  }
}

// ----------------------------------------------------------------------------
// register：网页引导（平台 API 注册当前不开放，统一走官方注册管道，防刷一致）
// ----------------------------------------------------------------------------

function cmdRegister() {
  return [
    'PowPow 账号注册需在浏览器完成（约 1 分钟，一辈子一次）：',
    '',
    '  1. 打开注册页：' + BASE_URL + '/register',
    '  2. 完成注册后回到这里，执行：',
    '     node scripts/powwow.js login --username <你的邮箱或用户名> --password <你的密码>',
    '  3. 然后创建你的第一个地图数字人：',
    '     node scripts/powwow.js create --name "名字" --description "人设描述"',
    '',
    '（升级钩子：平台未来开放 API 注册后，此命令将支持 --username/--password 自动注册。）',
  ].join('\n');
}

// ----------------------------------------------------------------------------
// login
// ----------------------------------------------------------------------------

async function cmdLogin(flags) {
  const username = flags.username || process.env.POWPOW_USERNAME;
  const password = flags.password || process.env.POWPOW_PASSWORD;
  if (!username || !password) {
    fail('需要 --username 与 --password，或设置环境变量 POWPOW_USERNAME / POWPOW_PASSWORD');
  }
  const result = await api('POST', '/api/openclaw/auth/login', { username, password });
  ensureOk(result, '登录');
  const d = result.data.data;
  const prev = loadCred();
  const cred = {
    userId: d.user_id,
    username: d.username,
    nickname: d.nickname || d.username,
    token: d.token,
    expiresAt: d.expires_at,
    digitalHumans: prev?.digitalHumans || [],
  };
  saveCred(cred);
  return [
    '登录成功！',
    '',
    `用户名: ${d.username}`,
    `用户ID: ${d.user_id}`,
    `Token 有效期至: ${d.expires_at}`,
    '',
    '下一步：node scripts/powwow.js create --name "名字" --description "人设描述"',
  ].join('\n');
}

// ----------------------------------------------------------------------------
// status
// ----------------------------------------------------------------------------

async function cmdStatus() {
  const cred = loadCred();
  if (!cred) {
    return '未登录。先执行：node scripts/powwow.js login --username <邮箱> --password <密码>';
  }
  const result = await api('GET', `/api/openclaw/users/${cred.userId}/badges`, null, authHeader(cred));
  ensureOk(result, '查询徽章');
  const badges = result.data.data?.count ?? '?';
  const lines = [
    `用户: ${cred.nickname}（${cred.username}）`,
    `用户ID: ${cred.userId}`,
    `徽章: ${badges} 枚（创建数字人消耗 2 枚/个，续期 1 枚/30 天）`,
    `数字人: ${(cred.digitalHumans || []).length} 个（本机记录）`,
    `Token 过期: ${cred.expiresAt}`,
  ];
  if (cred.expiresAt && new Date(cred.expiresAt) < new Date()) {
    lines.push('\n提示：Token 已过期，请重新执行 login。');
  }
  return lines.join('\n');
}

// ----------------------------------------------------------------------------
// subscribe（可选付费项：PayPal 承担外部费用，参见 SKILL.md）
// ----------------------------------------------------------------------------

async function cmdSubscribe(flags) {
  const action = flags.action || 'plans';
  if (action === 'plans') {
    const result = await api('GET', '/api/subscription/plans');
    const plans = result.data?.plans || (Array.isArray(result.data) ? result.data : null);
    if (!Array.isArray(plans) || plans.length === 0) {
      return '暂无可用订阅计划，或获取失败。';
    }
    let out = '可用订阅计划（可选，不订阅也可使用基础功能）:\n\n';
    for (const p of plans) {
      out += `计划: ${p.name}\nID: ${p.id}\n价格: $${p.price}/${p.interval}\n试用: ${p.trialDays ?? p.trial_days ?? '-'} 天\n\n`;
    }
    out += `创建订阅: node scripts/powwow.js subscribe --action create --planId <ID>`;
    return out;
  }
  if (action === 'create') {
    const cred = loadCred();
    if (!flags.planId) {
      return '需要 --planId。先用 --action plans 查看可用计划。';
    }
    const result = await api('POST', '/api/subscription/create', { planId: flags.planId }, authHeader(cred));
    ensureOk(result, '创建订阅');
    const d = result.data;
    return [
      '订阅创建成功！',
      '',
      `订阅ID: ${d.subscriptionId ?? '-'}`,
      `状态: ${d.status ?? '-'}`,
      '',
      '请在浏览器中打开以下链接完成 PayPal 支付:',
      d.approveUrl ?? '(未返回支付链接)',
      '',
      '支付完成后，订阅将自动生效。',
    ].join('\n');
  }
  return '未知操作。使用 --action plans 查看计划，或 --action create --planId <ID> 创建订阅。';
}

// ----------------------------------------------------------------------------
// create：avatar 必填（平台契约，参照 powpow-integration 同款策略）+ 徽章预检
// ----------------------------------------------------------------------------

const DEFAULT_AVATAR_URL = 'https://global.powpow.online/logo.png';

async function checkImageUrl(url) {
  try {
    const res = await fetch(url, { method: 'HEAD', signal: AbortSignal.timeout(15000), headers: { 'Connection': 'close' } });
    if (!res.ok) {
      fail(`头像 URL 不可用（HTTP ${res.status}）：${url}`);
    }
    return url;
  } catch (err) {
    fail(`头像 URL 校验失败：${err.message}`);
  }
}

async function cmdCreate(flags) {
  const cred = loadCred();
  const name = flags.name;
  const description = flags.description;
  if (!name || !description) {
    fail('需要 --name 与 --description');
  }
  const avatarUrl = await checkImageUrl(
    typeof flags.avatar === 'string' && flags.avatar ? flags.avatar : DEFAULT_AVATAR_URL
  );

  // 徽章预检（创建消耗 2 枚，删除不退）
  const bal = await api('GET', `/api/badges/balance?userId=${cred.userId}`, null, authHeader(cred));
  const current = bal.data?.balance?.balance ?? null;
  if (typeof current === 'number' && current < 2) {
    fail(`徽章余额不足：当前 ${current} 枚，创建需要 2 枚。`);
  }

  const webhookToken = typeof flags.webhookToken === 'string' && flags.webhookToken
    ? flags.webhookToken
    : 'powwow-' + crypto.randomBytes(16).toString('hex');
  const webhookUrl = typeof flags.webhookUrl === 'string' && flags.webhookUrl
    ? flags.webhookUrl
    : SINK_URL;
  const body = {
    userId: cred.userId,
    name,
    description,
    avatarUrl,
    lat: flags.lat ? Number(flags.lat) : 39.9042,
    lng: flags.lng ? Number(flags.lng) : 116.4074,
    locationName: flags.locationName || 'Beijing',
    webhookUrl,
    webhookToken,
  };
  const result = await api('POST', '/api/openclaw/digital-humans', body, authHeader(cred));
  if (result.status === 402) {
    fail('创建失败：徽章不足（创建数字人消耗 2 枚）。用 status 命令查看余额；可通过签到活动或订阅获取徽章。');
  }
  ensureOk(result, '创建数字人');
  const dh = result.data.data;
  const expiresAt = dh.expiresAt ?? dh.expires_at ?? '';
  const badgesRemaining = dh.badgesRemaining ?? dh.badges_remaining ?? '?';

  cred.digitalHumans = cred.digitalHumans || [];
  cred.digitalHumans.push({ id: dh.id, name: dh.name, webhookToken, expiresAt });
  saveCred(cred);

  const pluginConfig = JSON.stringify(
    {
      channels: {
        powpow: {
          enabled: true,
          digitalHumanId: dh.id,
          webhookToken,
          dmPolicy: 'open',
          pollIntervalMs: 3000,
        },
      },
    },
    null,
    2
  );
  return [
    '数字人创建成功！',
    '',
    `名称: ${dh.name}`,
    `ID: ${dh.id}`,
    `头像: ${avatarUrl}`,
    `位置: ${body.locationName} (${body.lat}, ${body.lng})`,
    `有效期至: ${expiresAt}（30 天，续期 1 枚徽章）`,
    `剩余徽章: ${badgesRemaining} 枚`,
    `WebhookToken（已保存到本机 credentials.json）: ${webhookToken}`,
    '',
    '在地图上查看: ' + BASE_URL + '/map',
    '',
    '══════════════════════════════════════════════════',
    '下一步：安装 OpenClaw 渠道插件，让 agent 常驻接管这个数字人',
    '',
    '  1. 安装插件:',
    `     openclaw plugins install ${CHANNEL_PLUGIN}`,
    '',
    '  2. 在 OpenClaw 配置中加入（或用 setup 向导等价填入）:',
    pluginConfig,
    '',
    '  3. 重启 OpenClaw，agent 即开始以该数字人身份收发地图访客消息',
    '══════════════════════════════════════════════════',
  ].join('\n');
}

// ----------------------------------------------------------------------------
// list
// ----------------------------------------------------------------------------

async function cmdList() {
  const cred = loadCred();
  const result = await api('GET', `/api/openclaw/users/${cred.userId}/digital-humans`, null, authHeader(cred));
  if (!result.ok || !Array.isArray(result.data)) {
    fail(`获取列表失败 (HTTP ${result.status})：${result.data?.error || '未知错误'}`);
  }
  const list = result.data;
  if (list.length === 0) {
    return '暂无数字人。用 create 命令创建一个吧！';
  }
  let out = `我的数字人（${list.length}）:\n\n`;
  for (const dh of list) {
    const expired = dh.expiresAt && new Date(dh.expiresAt) < new Date() ? ' [已过期]' : '';
    out += `${dh.name}（ID: ${dh.id}）\n  位置: ${dh.locationName ?? '-'} | 状态: ${dh.isActive ? '活跃' : '未激活'}${expired}\n  类型: ${dh.type ?? '-'} | 到期: ${dh.expiresAt ?? '-'}\n\n`;
  }
  return out;
}

// ----------------------------------------------------------------------------
// chat：history（拉对话）/ send（以 agent 身份回帖）
// ----------------------------------------------------------------------------

async function cmdChat(flags) {
  const action = flags.action || 'history';
  const dhId = flags.id || flags.digitalHumanId;
  if (!dhId) {
    fail('需要 --id <数字人ID>（可用 list 命令查看）');
  }
  const tokenOverride = typeof flags.token === 'string' && flags.token ? flags.token : null;
  if (action === 'history') {
    return chatHistory(dhId, tokenOverride);
  }
  if (action === 'send') {
    if (!flags.message) {
      fail('action=send 需要 --message <内容>');
    }
    return chatSend(dhId, String(flags.message), tokenOverride);
  }
  fail('未知 action。使用 --action history 或 --action send');
}

async function chatHistory(dhId, tokenOverride) {
  // 历史接口已鉴权：优先 --token / 本机该数字人的 webhookToken，回退登录 Bearer
  const cred = loadCred() || {};
  const dh = (cred.digitalHumans || []).find(d => d.id === dhId);
  const headers = {};
  if (tokenOverride || dh?.webhookToken) {
    headers['X-Webhook-Token'] = tokenOverride || dh.webhookToken;
  } else if (cred.token) {
    headers['Authorization'] = `Bearer ${cred.token}`;
  }
  // order=desc 取最近 20 条，展示时反转回时间正序
  const result = await api('GET', `/api/openclaw/chat/history?digitalHumanId=${encodeURIComponent(dhId)}&order=desc&limit=20`, undefined, headers);
  if (!result.ok || !result.data?.success) {
    if (result.status === 401) {
      fail('获取历史失败 (HTTP 401)：无读取权限。请先登录（login 命令）；若数字人不是经本 skill 创建，用 --token <webhookToken> 传入。');
    }
    fail(`获取历史失败 (HTTP ${result.status})：${result.data?.error || '未知错误'}`);
  }
  const messages = (result.data.data?.messages || []).slice().reverse();
  if (messages.length === 0) {
    return `数字人 ${dhId} 暂无对话记录。`;
  }
  let out = `数字人 ${dhId} 最近 ${messages.length} 条消息:\n\n`;
  for (const m of messages) {
    const who = m.role === 'user' ? '访客' : '数字人';
    out += `[${who}] ${m.content}\n`;
  }
  out += `\n回复消息: node scripts/powwow.js chat --id ${dhId} --action send --message "内容"`;
  return out;
}

async function chatSend(dhId, message, tokenOverride) {
  const cred = loadCred() || {};
  const dh = (cred.digitalHumans || []).find(d => d.id === dhId);
  const token = tokenOverride || dh?.webhookToken;
  if (!token) {
    fail('缺少 webhookToken：本机 credentials.json 中没有该数字人的记录。若数字人不是经本 skill 创建，用 --token <webhookToken> 传入（数字人详情/webhook 配置中获取）。');
  }
  // 先取最新会话以保证续接（order=desc 取最新一条，历史接口已鉴权需带 token）
  const hist = await api('GET', `/api/openclaw/chat/history?digitalHumanId=${encodeURIComponent(dhId)}&order=desc&limit=1`, undefined, {
    'X-Webhook-Token': token,
  });
  const sessionId = hist.data?.data?.messages?.[0]?.sessionId;
  const body = {
    digital_human_id: dhId,
    message,
    webhook_token: token,
    ...(sessionId ? { session_id: sessionId } : {}),
  };
  const result = await api('POST', '/api/openclaw/webhook/receive', body, {
    'X-Webhook-Token': token,
  });
  if (result.status === 401) {
    fail('回帖被拒（401）：webhookToken 与平台记录不一致。请核对 --token / 本机 credentials.json 中的 token，或重新创建数字人。');
  }
  ensureOk(result, '发送回复');
  const d = result.data.data;
  return [
    '回复已送达！',
    `消息ID: ${d.message_id}`,
    `会话ID: ${d.session_id ?? sessionId ?? '-'}（访客聊天窗约 3 秒内可见）`,
  ].join('\n');
}

// ----------------------------------------------------------------------------
// help
// ----------------------------------------------------------------------------

function cmdHelp() {
  return [
    'PowPow Agent CLI - 把你的 OpenClaw agent 放上泡泡地图',
    '',
    '命令:',
    '  register                                        注册引导（网页完成，一次即可）',
    '  login --username <邮箱> --password <密码>        登录（凭据保存本机，24h 过期自动重新登录即可）',
    '  status                                          当前登录状态与徽章余额',
    '  subscribe [--action plans|create --planId <ID>]  订阅计划（可选付费项，PayPal 支付）',
    '  create --name <n> --description <d> [--lat --lng --locationName --avatar <URL>]',
    '                                            创建地图数字人（默认平台头像，消耗 2 枚徽章，',
    '                                            自动生成 token、输出插件安装引导）',
    '  list                                            我的数字人列表',
    '  chat --id <ID> [--action history|send]           查看对话 / 以数字人身份回复',
    '        [--message <内容>] [--token <webhookToken>]',
    '                                            --token：数字人非本 skill 创建时手动传入',
    '  help                                            本帮助',
    '',
    `官网: ${BASE_URL}`,
    `地图: ${BASE_URL}/map`,
    `渠道插件: openclaw plugins install ${CHANNEL_PLUGIN}`,
  ].join('\n');
}

// ----------------------------------------------------------------------------
// 主入口
// ----------------------------------------------------------------------------

async function main() {
  const { cmd, flags } = parseArgs(process.argv.slice(2));
  switch (cmd) {
    case 'register': console.log(cmdRegister()); break;
    case 'login': console.log(await cmdLogin(flags)); break;
    case 'status': console.log(await cmdStatus()); break;
    case 'subscribe': console.log(await cmdSubscribe(flags)); break;
    case 'create': console.log(await cmdCreate(flags)); break;
    case 'list': console.log(await cmdList()); break;
    case 'chat': console.log(await cmdChat(flags)); break;
    case 'help':
    default: console.log(cmdHelp()); break;
  }
}

main().catch(err => {
  if (err !== FAIL_SENTINEL) {
    console.error(`执行出错：${err.message}`);
    process.exitCode = 1;
  }
  // 兜底：若仍有 ref 状态的句柄挂着，1 秒后强制退出
  setTimeout(() => process.exit(process.exitCode || 1), 1000);
});
