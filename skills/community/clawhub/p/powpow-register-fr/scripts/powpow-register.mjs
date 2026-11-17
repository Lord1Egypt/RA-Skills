#!/usr/bin/env node
/**
 * powpow-register.mjs — PowPow 注册助手 v2.0.0 核心脚本
 *
 * 零依赖（Node >= 18），所有请求只发往 PowPow 官方域名 https://global.powpow.online。
 *
 * 凭证安全规则（与 powpow-cli 家族一致）：
 * - 密码绝不落盘、绝不出现在命令行参数（进程列表可见）。register / refresh-login
 *   通过环境变量 POWPOW_REGISTER_PASSWORD 传入。
 * - 状态文件（系统临时目录）只保存：邮箱、用户名、昵称、JWT token、订单号、流程步骤。
 * - token 是短期会话凭据，流程结束（cleanup）即删除。
 *
 * 子命令：
 *   gen-password                       生成一个符合平台规则的随机强密码（无状态，仅打印一次）
 *   prepare-suggest [--username U] [--nickname N] [--email E]
 *                                      把与用户确认好的建议信息记入状态文件
 *   send-code --email <邮箱>           发送 6 位邮箱验证码（10 分钟有效，1 次/分钟）
 *   register --code <验证码> [--username U] [--nickname N] [--phone P] [--avatar <图片路径>]
 *                                      提交注册（multipart，支持头像直传）。
 *                                      需环境变量 POWPOW_REGISTER_PASSWORD；username 缺省读状态文件
 *   login-link [--target pending|home] 生成一键登录链接（pending=订阅页；home=首页）
 *   create-order --package <monthly|quarterly|yearly> [--provider alipay|paypal]
 *                                      创建支付订单：默认支付宝，--provider paypal 时走 PayPal 订阅
 *   query                              查询订单/订阅状态（paid/pending/closed/unknown/ACTIVE）
 *   refresh-login                      付款后重新登录，换取带 ACTIVE 订阅声明的新 JWT
 *                                      （需环境变量 POWPOW_REGISTER_PASSWORD）
 *   whoami                             验证当前 token，返回账号与订阅状态
 *   status                             查看流程进度（不含任何凭据）
 *   cleanup                            删除状态文件（流程结束/用户要求时调用）
 *
 * 退出码：0 成功；1 业务失败；2 参数错误
 */

import { writeFileSync, readFileSync, existsSync, unlinkSync, mkdtempSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';
import crypto from 'node:crypto';

const BASE_URL = 'https://global.powpow.online';
const STATE_FILE = join(tmpdir(), 'powpow-register-state.json');
const PASSWORD_ENV = 'POWPOW_REGISTER_PASSWORD';

// ---------- 状态文件 ----------

function loadState() {
  try {
    return JSON.parse(readFileSync(STATE_FILE, 'utf8'));
  } catch {
    return {};
  }
}

function saveState(patch) {
  const s = { ...loadState(), ...patch };
  writeFileSync(STATE_FILE, JSON.stringify(s, null, 2), { mode: 0o600 });
  return s;
}

// ---------- HTTP ----------

function extractCookies(res) {
  const raw =
    typeof res.headers.getSetCookie === 'function'
      ? res.headers.getSetCookie()
      : (res.headers.get('set-cookie') || '').split(/,(?=[^;]+=)/).filter(Boolean);
  const jar = {};
  for (const line of raw) {
    const [pair] = line.split(';');
    const eq = pair.indexOf('=');
    if (eq > 0) jar[pair.slice(0, eq).trim()] = pair.slice(eq + 1).trim();
  }
  return jar;
}

async function api(path, { method = 'GET', body, form, headers = {} } = {}) {
  const init = { method, headers: { ...headers } };
  if (body !== undefined) {
    init.headers['Content-Type'] = 'application/json';
    init.body = JSON.stringify(body);
  } else if (form !== undefined) {
    init.body = form;
  }
  const res = await fetch(`${BASE_URL}${path}`, init);
  const cookies = extractCookies(res);
  let data = null;
  try {
    data = await res.json();
  } catch {
    data = null;
  }
  return { status: res.status, ok: res.ok, data, cookies };
}

class DieSignal extends Error {}

function die(msg, code = 1) {
  console.log(`ERROR: ${msg}`);
  process.exitCode = code;
  // 不用 process.exit()：网络请求刚结束时强制退出会与连接池句柄竞态
  // （Windows 上触发 libuv 断言）。设退出码后抛信号量，让事件循环自然排空。
  throw new DieSignal();
}

function ok(msg, extra = {}) {
  console.log(JSON.stringify({ success: true, message: msg, ...extra }, null, 2));
}

// ---------- 工具 ----------

function genPassword() {
  // 随机 24 位，保证满足平台规则（含大小写字母 + 数字），去易混淆字符
  const upper = 'ABCDEFGHJKLMNPQRSTUVWXYZ';
  const lower = 'abcdefghijkmnpqrstuvwxyz';
  const digits = '23456789';
  const all = upper + lower + digits;
  const pick = (set) => set[crypto.randomInt(set.length)];
  return pick(upper) + pick(lower) + pick(digits) + Array.from({ length: 21 }, () => pick(all)).join('');
}

function requireState(...keys) {
  const s = loadState();
  const missing = keys.filter((k) => !s[k]);
  if (missing.length > 0) {
    die(`状态缺失：${missing.join('、')}。请按流程顺序执行（可先跑 status 查看进度）。`);
  }
  return s;
}

function arg(name, { required = false } = {}) {
  const i = process.argv.indexOf(`--${name}`);
  if (i === -1 || i + 1 >= process.argv.length) {
    if (required) die(`缺少必填参数 --${name}`, 2);
    return undefined;
  }
  return process.argv[i + 1];
}

function requirePassword() {
  const p = process.env[PASSWORD_ENV];
  if (!p) {
    die(`请通过环境变量 ${PASSWORD_ENV} 传入密码（不要写在命令行参数里，进程列表可见）。`);
  }
  return p;
}

// ---------- 子命令 ----------

function cmdGenPassword() {
  ok('随机强密码（请立即让用户保存，不会再次显示）', { password: genPassword() });
}

function cmdPrepareSuggest() {
  const patch = {};
  for (const k of ['username', 'nickname', 'email']) {
    const v = arg(k);
    if (v) patch[k] = v;
  }
  if (Object.keys(patch).length === 0) die('至少提供一个 --username/--nickname/--email', 2);
  saveState(patch);
  ok('建议信息已记录');
}

async function cmdSendCode() {
  const email = arg('email', { required: true });
  const r = await api('/api/auth/register/send-code', { method: 'POST', body: { email } });
  if (r.status === 429) die('发送太频繁，请 1 分钟后再试。');
  if (!r.ok) die(r.data?.error || `发送失败（HTTP ${r.status}）`);
  saveState({ email, step: 'code-sent', codeSentAt: new Date().toISOString() });
  ok('验证码已发送，请查收邮箱（注意垃圾邮件文件夹），10 分钟内有效', { email });
}

async function cmdRegister() {
  const state = requireState('email');
  const code = arg('code', { required: true });
  const username = arg('username') || state.username;
  const nickname = arg('nickname') || state.nickname || '';
  const phone = arg('phone') || '';
  const avatarPath = arg('avatar');
  const password = requirePassword();

  if (!username) die('缺少用户名（--username 或先执行 prepare-suggest）', 2);

  const form = new FormData();
  form.append('username', username);
  form.append('password', password);
  form.append('email', state.email);
  form.append('emailVerificationCode', code);
  if (nickname) form.append('nickname', nickname);
  if (phone) form.append('phone', phone);
  if (avatarPath) {
    const buf = readFileSync(avatarPath);
    const lower = avatarPath.toLowerCase();
    const mime = lower.endsWith('.png') ? 'image/png'
      : lower.endsWith('.webp') ? 'image/webp'
        : lower.endsWith('.gif') ? 'image/gif' : 'image/jpeg';
    form.append('avatar', new Blob([buf], { type: mime }), avatarPath.split(/[\\/]/).pop());
  }

  const r = await api('/api/auth/register', { method: 'POST', form });
  if (r.status === 429) die('注册请求过于频繁，请稍后再试。');
  if (!r.ok) die(String(r.data?.error || `注册失败（HTTP ${r.status}）`));

  const token = r.cookies['powpow_token'] || '';
  if (!token) die('注册成功但未捕获到会话 cookie（平台响应异常）');
  saveState({
    username: r.data?.user?.username || username,
    nickname: r.data?.user?.nickname || nickname,
    userId: r.data?.userId,
    token,
    step: 'registered-pending',
    registeredAt: new Date().toISOString(),
  });
  ok('注册成功，可生成一键登录链接（target=home 直达首页；target=pending 直达订阅页）', {
    accountStatus: 'pending_payment',
    username: r.data?.user?.username,
    avatarUrl: r.data?.user?.avatarUrl,
  });
}

function cmdLoginLink() {
  const state = requireState('token');
  const target = arg('target') || 'pending';
  const redirect = target === 'home' ? '/' : '/subscription';
  const url = `${BASE_URL}/api/auth/me?token=${encodeURIComponent(state.token)}&redirect=${encodeURIComponent(redirect)}`;
  ok(
    target === 'home' ? '登录链接（直达首页；免费测试期内点开即用，测试期结束则会落到订阅页）' : 'pending 登录链接（直达订阅页，用于支付流程）',
    { url }
  );
}

async function cmdCreateOrder() {
  const state = requireState('token');
  const provider = (arg('provider') || 'alipay').toLowerCase();
  const pkg = arg('package') || 'monthly';

  if (provider !== 'alipay' && provider !== 'paypal') {
    die('支付渠道只能是 alipay 或 paypal', 2);
  }

  // ---------- 支付宝通道 ----------
  if (provider === 'alipay') {
    if (!pkg || !['monthly', 'quarterly', 'yearly'].includes(pkg)) {
      die('支付宝套餐须为 monthly / quarterly / yearly', 2);
    }
    const r = await api('/api/payment/alipay/create-order', {
      method: 'POST',
      body: { package: pkg },
      headers: { Authorization: `Bearer ${state.token}` },
    });
    if (r.status === 401) die('登录态失效，请重新执行 refresh-login。');
    if (!r.ok) die(r.data?.error || `创建订单失败（HTTP ${r.status}）`);
    const html = r.data?.paymentHtml || '';
    if (!html) die('平台未返回支付页内容');
    const dir = mkdtempSync(join(tmpdir(), 'powpow-pay-'));
    const file = join(dir, 'alipay-checkout.html');
    writeFileSync(file, html);
    saveState({
      provider: 'alipay',
      outTradeNo: r.data.outTradeNo,
      package: pkg,
      amount: r.data.amount,
      orderStep: 'pending',
      orderCreatedAt: new Date().toISOString(),
    });
    ok('支付页已生成，请让用户在浏览器打开完成付款', {
      checkoutFile: file,
      outTradeNo: r.data.outTradeNo,
      planName: r.data.planName,
      amount: r.data.amount,
    });
    return;
  }

  // ---------- PayPal 通道 ----------
  const plansRes = await api('/api/subscription/plans', {
    headers: { Authorization: `Bearer ${state.token}` },
  });
  if (plansRes.status === 401) die('登录态失效，请重新执行 refresh-login。');
  if (!plansRes.ok) die(plansRes.data?.error || `拉取 PayPal 计划失败（HTTP ${plansRes.status}）`);
  const plan = (plansRes.data?.plans || [])[0];
  if (!plan?.id) die('当前没有可用的 PayPal 订阅计划，请改用支付宝或联系支持');

  const r = await api('/api/subscription/create', {
    method: 'POST',
    body: { planId: plan.id },
    headers: { Authorization: `Bearer ${state.token}` },
  });
  if (r.status === 401) die('登录态失效，请重新执行 refresh-login。');
  if (r.status === 409) {
    die('你已有一个待处理或有效的 PayPal 订阅，请直接在浏览器里完成它，或 1 小时后再试。');
  }
  if (!r.ok) die(r.data?.error || `创建 PayPal 订阅失败（HTTP ${r.status}）`);

  const approveUrl = r.data?.approveUrl || '';
  if (!approveUrl) die('平台未返回 PayPal 授权链接');

  const dir = mkdtempSync(join(tmpdir(), 'powpow-pay-'));
  const file = join(dir, 'paypal-approve.html');
  writeFileSync(
    file,
    `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Redirect to PayPal</title>
</head>
<body>
  <p>正在跳转到 PayPal 完成签约…</p>
  <script>location.replace(${JSON.stringify(approveUrl)});</script>
  <p>若未自动跳转，<a href="${approveUrl}" target="_blank" rel="noopener noreferrer">点击这里打开 PayPal</a>。</p>
</body>
</html>`
  );

  saveState({
    provider: 'paypal',
    subscriptionId: r.data.subscriptionId,
    approveUrl,
    planName: plan.name,
    planPrice: `${plan.price} ${plan.currency || 'USD'}/${(plan.interval || 'MONTH').toLowerCase()}`,
    orderStep: 'pending',
    orderCreatedAt: new Date().toISOString(),
  });

  ok('PayPal 订阅已创建，请在浏览器打开授权链接完成签约', {
    checkoutFile: file,
    subscriptionId: r.data.subscriptionId,
    approveUrl,
    planName: plan.name,
    planPrice: `${plan.price} ${plan.currency || 'USD'}`,
    interval: plan.interval,
  });
}

async function cmdQuery() {
  const state = requireState('token');
  const provider = state.provider || 'alipay';

  if (provider === 'alipay') {
    requireState('outTradeNo');
    const r = await api(`/api/payment/alipay/query?outTradeNo=${encodeURIComponent(state.outTradeNo)}`, {
      headers: { Authorization: `Bearer ${state.token}` },
    });
    if (r.status === 401) die('登录态失效，请重新执行 refresh-login。');
    if (!r.ok) die(r.data?.error || `查询失败（HTTP ${r.status}）`);
    if (r.data.status === 'paid') saveState({ orderStep: 'paid' });
    ok(`订单状态：${r.data.status}`, { status: r.data.status });
    return;
  }

  // PayPal 轮询
  const r = await api('/api/subscription/create', {
    headers: { Authorization: `Bearer ${state.token}` },
  });
  if (r.status === 401) die('登录态失效，请重新执行 refresh-login。');
  if (!r.ok) die(r.data?.error || `查询订阅失败（HTTP ${r.status}）`);

  const active = r.data?.activeSubscription?.subscription;
  if (active?.status === 'ACTIVE') {
    saveState({ orderStep: 'paid' });
    ok('订阅状态：ACTIVE（已激活）', {
      status: 'ACTIVE',
      subscriptionId: active.paypalSubscriptionId,
      expiresAt: active.currentPeriodEnd,
    });
    return;
  }

  const pending = (r.data?.allSubscriptions || []).find(
    (s) => s.subscription?.status === 'PENDING'
  );
  const status = pending?.subscription?.status || 'PENDING';
  ok(`订阅状态：${status}（等待 PayPal 授权或 webhook 确认）`, {
    status,
    subscriptionId: pending?.subscription?.paypalSubscriptionId,
  });
}

async function cmdRefreshLogin() {
  const state = requireState('username');
  const password = requirePassword();
  const r = await api('/api/auth/login', { method: 'POST', body: { step: 1, username: state.username, password } });
  if (r.status === 403 && r.data?.status === 'pending_payment') {
    die('账号仍是 pending（未完成订阅）。请先完成支付，再执行本命令。');
  }
  if (r.status === 423) die('账户被临时锁定（多次失败），请 30 分钟后再试。');
  if (!r.ok) die(r.data?.error || `登录失败（HTTP ${r.status}）`);
  const token = r.cookies['powpow_token'] || '';
  if (!token) die('登录成功但未捕获到会话 cookie');
  saveState({ token, step: 'active', refreshedAt: new Date().toISOString() });
  ok('已换取正式登录态（含最新订阅声明），可生成直达首页的一键登录链接（target=home）', {
    username: r.data?.user?.username,
  });
}

async function cmdWhoami() {
  const state = requireState('token');
  const r = await api('/api/auth/me', { headers: { Authorization: `Bearer ${state.token}` } });
  if (!r.ok) die(r.data?.error || `会话无效（HTTP ${r.status}）`);
  const u = r.data?.user || {};
  ok('会话有效', {
    username: u.username,
    accountStatus: u.accountStatus,
    subscriptionStatus: u.subscriptionStatus,
    subscriptionExpiresAt: u.subscriptionExpiresAt,
  });
}

function cmdStatus() {
  const s = loadState();
  if (!Object.keys(s).length) {
    ok('尚无流程状态（未开始）');
    return;
  }
  const safe = { ...s };
  delete safe.token;
  ok('当前流程状态', safe);
}

function cmdCleanup() {
  if (existsSync(STATE_FILE)) unlinkSync(STATE_FILE);
  ok('状态文件已删除（本机临时目录中的会话凭据已清理）');
}

// ---------- 入口 ----------

const [, , command] = process.argv;
const commands = {
  'gen-password': cmdGenPassword,
  'prepare-suggest': cmdPrepareSuggest,
  'send-code': cmdSendCode,
  register: cmdRegister,
  'login-link': cmdLoginLink,
  'create-order': cmdCreateOrder,
  query: cmdQuery,
  'refresh-login': cmdRefreshLogin,
  whoami: cmdWhoami,
  status: cmdStatus,
  cleanup: cmdCleanup,
};

if (!command || !commands[command]) {
  console.log(`用法：powpow-register.mjs <gen-password|prepare-suggest|send-code|register|login-link|create-order|query|refresh-login|whoami|status|cleanup> [参数]
常用：--provider alipay|paypal（默认 alipay）
所有请求仅发往 ${BASE_URL}。详细参数说明见文件头部注释或 references/agent-flow.md。`);
  process.exit(2);
}

try {
  await Promise.resolve(commands[command]());
} catch (e) {
  if (!(e instanceof DieSignal)) {
    process.exitCode = 1;
    console.log(`ERROR: ${e?.message || '未知错误'}`);
  }
}
