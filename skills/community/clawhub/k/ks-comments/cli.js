#!/usr/bin/env node
'use strict';
/**
 * cli.js — 快手视频评论分步采集 CLI (能力: ks_comments 会话制, 自包含)。
 *
 * 交互协议 (对齐 xhs-comments v2, 2026-10-15):
 *   1. start  建会话 (免费: 节点 probe 探测视频标题/互动数/评论总数, 短链自动还原),
 *             返回评论总数与预估页数 → 必须把数字报给用户确认后再开始计费采集
 *   2. step --page          采一页主评论 (约 10-20 条+内嵌预览回复) = 扣 1 点
 *      step --expand --root 对指定主评论点一次展开回复 = 扣 1 点
 *      每步返回增量结果 + has_more_main / 可展开列表, 由 AI 询问用户是否继续
 *   3. finish 主动结束会话 (空闲 20 分钟服务端也会自动过期并释放采集节点)
 *
 * 与 xhs-comments 的差异: 端点前缀 /ks/comments/sessions; 展开参数为 root_cid
 * (主评论 cid); 可展开列表字段为 root_cid / sub_count / subs_collected。
 *
 * 输出规约: stdout 只输出 JSON, 提示走 stderr。
 * 退出码: 0 成功 / 1 参数错误 / 2 认证失败 / 3 点数不足 / 4 网络错误 / 5 其它。
 */
const fs = require('fs');
const path = require('path');
const { ApiClient, BizError, allowInsecureTls } = require('./src/client');
const { loadConfig, saveConfig, resolveConfig, maskToken, configPaths, DEFAULT_BASE_URL } = require('./src/config');
const { UsageError, printOk, printFail, exitWithError, parsePositiveNumber } = require('./src/output');

const CAPABILITY = 'ks_comments';
const VERSION = '1.0.0';
const DOWNLOAD_TIMEOUT_MS = 60000; // 导出 CSV 下载超时

// ---------------------------------------------------------------- 参数解析

const VALUE_FLAGS = new Set(['session', 'root', 'url', 'page', 'page-size', 'status',
  'token', 'base-url', 'access-token', 'out']);
const BOOL_FLAGS = new Set(['help', 'link', 'check', 'version', 'expand']);

function camel(s) {
  return s.replace(/-([a-z])/g, (_, c) => c.toUpperCase());
}

function parseArgs(argv) {
  const opts = {};
  const positional = [];
  for (let i = 0; i < argv.length; i++) {
    let arg = argv[i];
    if (!arg.startsWith('-')) {
      positional.push(arg);
      continue;
    }
    if (!arg.startsWith('--')) throw new UsageError(`未知参数: ${arg}`);
    let inline;
    const eq = arg.indexOf('=');
    if (eq > 2) {
      inline = arg.slice(eq + 1);
      arg = arg.slice(0, eq);
    }
    const name = arg.slice(2);
    if (VALUE_FLAGS.has(name)) {
      let value = inline !== undefined ? inline : argv[i + 1];
      if (value === undefined || value.startsWith('--')) {
        // 无值形态: 该 flag 在部分命令里作布尔开关用 (如 step --page 显式采下一页)
        opts[camel(name)] = true;
      } else {
        if (inline === undefined) i++;
        opts[camel(name)] = value;
      }
    } else if (BOOL_FLAGS.has(name)) {
      if (inline !== undefined) throw new UsageError(`参数 ${arg} 不接受值`);
      opts[camel(name)] = true;
    } else {
      throw new UsageError(`未知参数: ${arg}`);
    }
  }
  const cmd = positional.shift() || '';
  return { cmd, args: positional, opts };
}

const USAGE = `快手视频评论分步采集 CLI (会话制, 按步计费: 每步 1 点数)

用法: node cli.js <命令> [参数]

采集流程命令:
  start --url <视频链接>            建立采集会话（免费：节点打开视频探测标题/互动数/评论总数）
                                    支持 kuaishou.com/short-video/<id> 直链、/f/<串> 分享页与
                                    v.kuaishou.com 短链（短链由节点浏览器打开后自动还原）
                                    返回 session_id、视频文案、评论总数、预估页数
  step --session <id> --page        采集下一页主评论（约 10-20 条+内嵌预览回复，扣 1 点）
  step --session <id> --expand --root <主评论cid>
                                    对指定主评论展开一次回复（扣 1 点）
  status --session <id>             查询会话状态/累计采集量/点数余额
  comments --session <id> [--page N] [--page-size N]
                                    分页拉取本会话已累计的评论明细（免费）
  export --session <id> [--out <文件路径>]
                                    下载会话累计结果 CSV（免费）
  finish --session <id>             主动结束会话（释放采集节点；空闲 20 分钟也会自动过期）
  sessions [--status active] [--page N]
                                    列出自己的会话

账号命令:
  register --link                   生成注册二维码/链接（推荐；注册即送 10 点数）
  register --check --access-token <串>  用户完成注册后确认并保存 token
  login --link                      生成登录二维码/链接（推荐）
  login --check --access-token <串> 用户完成授权后确认并保存 token
  quota                             查询点数与个人信息
  logout                            登出当前账号
  config set base-url <url>         设置后端服务地址
  config set insecure true|false    忽略 HTTPS 证书校验（自签证书时开）
  config show                       查看当前配置（token 脱敏）
  version                           显示版本

全局参数: --token <token>（临时覆盖）  --base-url <url>（默认 ${DEFAULT_BASE_URL}）`;

// ---------------------------------------------------------------- 公共

function requireToken(cfg) {
  if (!cfg.token) throw new BizError(1002, '未登录：缺少 token');
}

function requireSessionId(opts) {
  const sid = opts.session;
  if (!sid || !/^[0-9a-f]{32}$/.test(sid)) {
    throw new UsageError('需要 --session <32位会话id>（由 start 命令返回）');
  }
  return sid;
}

// ---------------------------------------------------------------- 账号命令

async function cmdSessionLink(cfg, scene) {
  const client = new ApiClient({ baseUrl: cfg.baseUrl });
  const data = await client.createCliSession();
  const isRegister = scene === 'register';
  const pageUrl = cfg.baseUrl + (isRegister ? data.register_path : data.login_path);
  const qrUrl = cfg.baseUrl + (isRegister ? data.register_qr_path : data.qr_path);
  const action = isRegister ? '注册' : '登录';
  process.stderr.write(
    `请把下面这段${action}引导原样发给用户：\n` +
    '----\n' +
    (isRegister
      ? '需要先注册账号（注册即送 10 免费点数，不注册无法使用采集服务）。请用手机扫码或打开链接注册：\n\n'
      : '需要先登录。请用手机扫码或打开链接登录账号：\n\n') +
    `${action}方式（二选一）\n` +
    `二维码图片：${qrUrl}\n` +
    `${action}链接：${pageUrl}\n` +
    `access_token（${action}后校验用）：${data.access_token}\n` +
    `扫码/${action}完成后告诉我一声，我会执行校验并保存凭证：\n\n` +
    `node cli.js ${scene} --check --access-token "${data.access_token}"\n` +
    '----\n');
  printOk({
    qr_url: qrUrl,
    [isRegister ? 'register_url' : 'login_url']: pageUrl,
    access_token: data.access_token,
    expires_in: data.expires_in,
  });
}

async function cmdSessionCheck(cfg, opts, scene) {
  const action = scene === 'register' ? '注册' : '登录';
  const accessToken = opts.accessToken;
  if (!accessToken || !/^[0-9a-f]{16,64}$/.test(accessToken)) {
    throw new UsageError(`${scene} --check 需要 --access-token（${scene} --link 下发的十六进制串）`);
  }
  const client = new ApiClient({ baseUrl: cfg.baseUrl });
  const data = await client.checkCliSession(accessToken);
  if (data.status === 'pending') {
    printFail('LOGIN_PENDING', `用户尚未完成${action}，请提醒用户完成扫码/链接${action}后再执行本命令`);
    process.exit(2);
  }
  if (data.status !== 'ready' || !data.token) {
    printFail('LOGIN_EXPIRED', `${action}会话已过期或已使用，请重新执行 ${scene} --link 发起${action}`);
    process.exit(2);
  }
  saveConfig({ base_url: cfg.baseUrl, token: data.token });
  process.stderr.write(`${action}成功，token 已保存到配置文件\n`);
  printOk({ phone: data.phone, quota_balance: data.quota_balance });
}

async function cmdQuota(opts) {
  const cfg = resolveConfig(opts);
  requireToken(cfg);
  const client = new ApiClient({ baseUrl: cfg.baseUrl, token: cfg.token });
  printOk(await client.profile());
}

async function cmdLogout(opts) {
  const cfg = resolveConfig(opts);
  if (!cfg.token) throw new BizError(1002, '未登录：本地没有已保存的 token');
  const client = new ApiClient({ baseUrl: cfg.baseUrl, token: cfg.token });
  try {
    await client.logout();
  } catch (err) {
    process.stderr.write(`服务端登出异常（已忽略，继续清除本地 token）: ${err.message}\n`);
  }
  saveConfig({ token: '' });
  process.stderr.write('已登出，本地 token 已清除；可执行 login --link 登录其他账号\n');
  printOk({ logged_out: true });
}

async function cmdConfig(args, opts) {
  const sub = args[0];
  if (sub === 'set' && args[1] === 'base-url') {
    const url = args[2];
    if (!url || !/^https?:\/\//.test(url)) throw new UsageError('config set base-url 需要 http(s):// 开头的地址');
    saveConfig({ base_url: url.replace(/\/+$/, '') });
    process.stderr.write(`base_url 已保存到 ${configPaths.configPath}\n`);
    printOk({ base_url: loadConfig().base_url });
    return;
  }
  if (sub === 'set' && args[1] === 'insecure') {
    const v = args[2];
    if (v !== 'true' && v !== 'false') throw new UsageError('config set insecure 需要 true 或 false');
    saveConfig({ insecure: v === 'true' });
    process.stderr.write(`insecure 已保存到 ${configPaths.configPath}\n`);
    printOk({ insecure: loadConfig().insecure === true });
    return;
  }
  if (sub === 'show') {
    const cfg = resolveConfig(opts);
    printOk({
      base_url: cfg.baseUrl,
      insecure: cfg.insecure,
      token: maskToken(cfg.token),
      config_path: configPaths.configPath,
    });
    return;
  }
  throw new UsageError('config 仅支持: config set base-url <url> / config set insecure true|false / config show');
}

// ---------------------------------------------------------------- 会话命令

async function cmdStart(opts) {
  const url = opts.url;
  if (!url) throw new UsageError('start 需要 --url <快手视频链接>（kuaishou.com/short-video/<id> 直链或 v.kuaishou.com 短链，节点自动还原）');
  const cfg = resolveConfig(opts);
  requireToken(cfg);
  const client = new ApiClient({ baseUrl: cfg.baseUrl, token: cfg.token });
  process.stderr.write('建立采集会话（节点探测视频信息，免费）...\n');
  const data = await client.createKsCommentSession(url);
  // 引导 AI: 必须把评论数/预估页数报给用户确认后再开始计费步进
  const total = data.metrics && data.metrics.comment_count;
  process.stderr.write(
    `会话已建立 session_id=${data.session_id}\n` +
    `视频《${data.title || '(无文案)'}》评论总数: ${total || '未知'}, ` +
    `预估 ${data.estimated_pages == null ? '?' : data.estimated_pages} 页主评论 (每页约 10 条 = 1 点)。\n` +
    '请把评论数和预估页数告知用户, 确认后再执行 step 开始计费采集；' +
    '每页采完会返回可展开回复的主评论列表, 由用户决定是否展开 (每次展开 1 点)。\n');
  printOk(data);
}

async function cmdStep(opts) {
  const sessionId = requireSessionId(opts);
  const cfg = resolveConfig(opts);
  requireToken(cfg);
  const client = new ApiClient({ baseUrl: cfg.baseUrl, token: cfg.token });
  let data;
  if (opts.expand) {
    const root = opts.root;
    if (!root) throw new UsageError('step --expand 需要 --root <主评论cid>（取自上一步返回的 expandable 列表）');
    process.stderr.write(`展开回复: session=${sessionId} root=${root}（扣 1 点）...\n`);
    data = await client.stepKsCommentSession(sessionId, 'expand', root);
    if (data.no_more) {
      process.stderr.write('该主评论的回复已全部展开完（本次未扣费）。\n');
    } else {
      process.stderr.write(
        `本次展开 ${(data.comments || []).length} 条回复, 该主评论累计 ${data.subs_collected_for_root} 条, ` +
        `约剩 ${data.subs_remaining_estimate == null ? '?' : data.subs_remaining_estimate} 条, ` +
        `${data.sub_has_more ? '还有更多（继续展开需再扣 1 点, 请先询问用户）' : '已全部展开'}。\n`);
    }
  } else {
    process.stderr.write(`采集下一页主评论: session=${sessionId}（扣 1 点）...\n`);
    data = await client.stepKsCommentSession(sessionId, 'page');
    if (data.no_more) {
      process.stderr.write('主评论已全部采完（本次未扣费）。\n');
    } else {
      const ex = Array.isArray(data.expandable) ? data.expandable : [];
      process.stderr.write(
        `第 ${data.page_no} 页: ${(data.comments || []).length} 条主评论 ` +
        `(累计 ${data.mains_collected} 主 + ${data.subs_collected} 子), ` +
        `${data.has_more_main ? '还有下一页' : '已是最后一页'}。\n` +
        (ex.length
          ? `本页有 ${ex.length} 条主评论含可展开回复: ` +
            ex.map((e) => `${e.root_cid}(共${e.sub_count}条,已采${e.subs_collected})`).join(', ') +
            ' — 是否展开请询问用户（每次展开 1 点）。\n'
          : '本页主评论均无可展开回复。\n'));
    }
  }
  printOk(data);
}

async function cmdStatus(opts) {
  const sessionId = requireSessionId(opts);
  const cfg = resolveConfig(opts);
  requireToken(cfg);
  const client = new ApiClient({ baseUrl: cfg.baseUrl, token: cfg.token });
  printOk(await client.getKsCommentSession(sessionId));
}

async function cmdComments(opts) {
  const sessionId = requireSessionId(opts);
  const cfg = resolveConfig(opts);
  requireToken(cfg);
  const client = new ApiClient({ baseUrl: cfg.baseUrl, token: cfg.token });
  // 无值形态 (--page 不带数字) 视为开关, 用默认页码 (parseArgs 对缺值 value-flag 置 true)
  const page = opts.page === true ? 1 : parsePositiveNumber(opts.page, 'page', 1);
  const pageSize = opts.pageSize === true ? 100 : parsePositiveNumber(opts.pageSize, 'page-size', 100);
  printOk(await client.listKsSessionComments(sessionId, page, pageSize));
}

async function cmdFinish(opts) {
  const sessionId = requireSessionId(opts);
  const cfg = resolveConfig(opts);
  requireToken(cfg);
  const client = new ApiClient({ baseUrl: cfg.baseUrl, token: cfg.token });
  const data = await client.finishKsCommentSession(sessionId);
  process.stderr.write(`会话已结束 (status=${data.status})，采集节点已释放。\n`);
  printOk(data);
}

async function cmdListSessions(opts) {
  const cfg = resolveConfig(opts);
  requireToken(cfg);
  const client = new ApiClient({ baseUrl: cfg.baseUrl, token: cfg.token });
  const page = opts.page === true ? 1 : parsePositiveNumber(opts.page, 'page', 1);
  printOk(await client.listKsCommentSessions(page, 20, opts.status || ''));
}

async function cmdExport(opts) {
  const sessionId = requireSessionId(opts);
  const cfg = resolveConfig(opts);
  requireToken(cfg);
  const dlCtrl = new AbortController();
  const dlTimer = setTimeout(() => dlCtrl.abort(), DOWNLOAD_TIMEOUT_MS);
  let buf;
  try {
    const res = await fetch(
      `${cfg.baseUrl}/api/v1/ks/comments/sessions/${encodeURIComponent(sessionId)}/export`,
      { headers: { Authorization: `Bearer ${cfg.token}` }, signal: dlCtrl.signal });
    if (!res.ok) {
      let msg = `HTTP ${res.status}`;
      try { msg = (await res.json()).message || msg; } catch { /* 非信封 */ }
      printFail('EXPORT_FAILED', `导出失败: ${msg}`);
      process.exit(5);
    }
    buf = Buffer.from(await res.arrayBuffer());
  } catch (err) {
    printFail('EXPORT_FAILED', err && err.name === 'AbortError'
      ? `下载超时（${DOWNLOAD_TIMEOUT_MS / 1000}s），请检查网络后重试`
      : `下载失败: ${err && err.message ? err.message : err}`);
    process.exit(5);
  } finally {
    clearTimeout(dlTimer);
  }
  const out = opts.out || `${sessionId}_ks_comments.csv`;
  try {
    fs.mkdirSync(path.dirname(path.resolve(out)), { recursive: true });
  } catch { /* 目录已存在 */ }
  if (fs.existsSync(out)) {
    process.stderr.write(`[warn] 目标文件已存在，将覆盖: ${out}\n`);
  }
  fs.writeFileSync(out, buf);
  process.stderr.write(`已下载: ${out}\n`);
  printOk({ session_id: sessionId, file: out, size: buf.length });
}

// ---------------------------------------------------------------- 入口

async function main() {
  const { cmd, args, opts } = parseArgs(process.argv.slice(2));
  if (opts.version) {
    printOk({ name: 'ks-comments', version: VERSION, capability: CAPABILITY });
    return;
  }
  if (opts.help || !cmd) throw new UsageError('缺少命令');
  if (resolveConfig(opts).insecure) allowInsecureTls();
  switch (cmd) {
    case 'version': return printOk({ name: 'ks-comments', version: VERSION, capability: CAPABILITY });
    case 'register':
      if (opts.link) return cmdSessionLink(resolveConfig(opts), 'register');
      if (opts.check) return cmdSessionCheck(resolveConfig(opts), opts, 'register');
      throw new UsageError('register 仅支持 --link / --check (终端注册会被 2003 拒绝)');
    case 'login':
      if (opts.link) return cmdSessionLink(resolveConfig(opts), 'login');
      if (opts.check) return cmdSessionCheck(resolveConfig(opts), opts, 'login');
      throw new UsageError('login 仅支持 --link / --check (终端登录会被 2003 拒绝)');
    case 'start': return cmdStart(opts);
    case 'step': return cmdStep(opts);
    case 'status': return cmdStatus(opts);
    case 'comments': return cmdComments(opts);
    case 'finish': return cmdFinish(opts);
    case 'sessions': return cmdListSessions(opts);
    case 'export': return cmdExport(opts);
    case 'quota': return cmdQuota(opts);
    case 'logout': return cmdLogout(opts);
    case 'config': return cmdConfig(args, opts);
    default: throw new UsageError(`未知命令: ${cmd}`);
  }
}

main().catch((e) => exitWithError(e, { usage: USAGE }));
