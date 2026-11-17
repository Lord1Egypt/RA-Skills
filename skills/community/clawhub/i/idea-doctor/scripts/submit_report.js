#!/usr/bin/env node
/**
 * submit_report.js — 商业点子体检官壳包提交脚本（壳包随包件）
 * 零第三方依赖（仅 node 内置 http/https/fs/path）。对齐服务端 402 契约：Payment-Needed 头 = base64url(JSON 账单)；重试携 Payment-Proof 头。
 * 纪律：
 *  - 端点已于 2026-11-14 对外开放；如当前端点与内置生产端点不一致或网络不可达，不发任何网络请求，退出码 2（ENDPOINT_NOT_OPEN；die(2) 分支行为不变）——设计行为，不是故障；偶发不可达＝服务器维护窗口，照实等待重试即可。
 *  - 不打印点子内容（idea 文本等 PII 不进 stdout/日志），只打印条数、字节数与状态码。
 *  - 客户端超时 20s。
 * 用法：
 *   node submit_report.js --in my_questionnaire.json [--remove 12,31] [--add "自定义措辞"] [--proof <Payment-Proof 值|文件路径>] [--out 体检报告.md]
 *   （--remove/--add 不随请求提交服务端——生产契约只消费 idea/scores/econ/competitors，脚本仅提示 OPTIONS_LOCAL_ONLY，自定义措辞以生成后报告本地编辑为准）
 * 定价口径（服务端按条数定价、用户传入 price/goods 字段一律无视）：1 条 ¥4.90；2-10 条 ¥9.90；>10 拒单说明上限。
 */
'use strict';
const fs = require('fs');
const path = require('path');
const http = require('http');
const https = require('https');

const ENDPOINT = 'https://linkkhub.top/idea/generate';
const endpoint = ENDPOINT;
const ARG = {};
const argv = process.argv.slice(2);
for (let i = 0; i < argv.length; i++) {
  if (argv[i].startsWith('--')) { const k = argv[i].slice(2); ARG[k] = argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[++i] : true; }
}
function die(code, msg, hint) { console.error(JSON.stringify({ ok: false, code, msg, hint: hint || null })); process.exit(code); }

if (endpoint !== ENDPOINT) {
  die(2, 'ENDPOINT_NOT_OPEN', '端点已于 2026-11-14 对外开放；当前端点与内置生产端点不一致或网络不可达时不发任何网络请求，退出码 2（ENDPOINT_NOT_OPEN）——设计行为，不是故障；偶发不可达＝服务器维护窗口，照实等待重试即可。');
}
if (!/^https:\/\//.test(endpoint) && !/^http:\/\/127\.0\.0\.1:/.test(endpoint)) {
  die(2, 'ENDPOINT_NOT_HTTPS', '生产端点必须为 https（本机回环地址仅限发布方自测）。');
}
if (!ARG.in) die(2, 'MISSING_INPUT', '用法：--in my_questionnaire.json');

let q;
try { q = JSON.parse(fs.readFileSync(path.resolve(ARG.in), 'utf8')); } catch (e) { die(1, 'QUESTIONNAIRE_READ_ERROR', '读取/解析问卷失败：' + ARG.in); }
if (q._input) q = q._input; // 允许直接传模板文件（将提示空字段）

// 壳侧预校验（缺项不猜值不代填；字段对齐服务端引擎归一化入口：生产契约只消费 idea/scores/econ/competitors；价格由服务端按条数定）
const rawIdeas = Array.isArray(q.ideas) ? q.ideas : (typeof q.idea === 'string' || q.idea ? [q] : []);
if (!rawIdeas.length) die(1, 'QUESTIONNAIRE_MISSING_FIELDS', '至少提供 1 个点子：ideas 数组（1-10 条）或 idea 字段（不代填不猜测）', '补齐后重试');
if (rawIdeas.length > 10) die(1, 'QUESTIONNAIRE_BATCH_LIMIT', '一次最多 10 个点子，更多请分批购买（对齐服务端 400 BATCH_TOO_LARGE 拒单语义，壳侧先闸不发单）', '1 条 ¥4.90；2-10 条 ¥9.90；>10 拒单说明上限');
const ECON_KEYS = ['price', 'pay_rate', 'reach', 'fixed_monthly'];
const SCORE_KEYS = ['pain', 'moat', 'willingness', 'delivery', 'acquisition'];
const missing = [];
const ideas = rawIdeas.map((it, i) => {
  const o = (it && typeof it === 'object') ? it : { idea: it };
  const text = String(o.idea == null ? '' : o.idea).trim();
  if (!text) missing.push('ideas[' + i + '].idea');
  else if (text.length < 10) die(1, 'QUESTIONNAIRE_INVALID_IDEA', '点子描述太短（至少 10 字）：ideas[' + i + ']（对齐服务端 422 INVALID_INPUT 文案；不打印点子内容）', '补足描述后重试');
  const out = { idea: text };
  const ec = (o.econ && typeof o.econ === 'object') ? o.econ : {};
  const econ = {};
  ECON_KEYS.forEach((k) => { const v = ec[k]; if (typeof v === 'number' && isFinite(v) && v >= 0) econ[k] = v; else missing.push('ideas[' + i + '].econ.' + k); });
  out.econ = econ;
  const sc = (o.scores && typeof o.scores === 'object') ? o.scores : {};
  const scores = {};
  SCORE_KEYS.forEach((k) => { const v = sc[k]; if (v === null || v === undefined) return; if (typeof v === 'number' && isFinite(v) && v >= 0 && v <= 10) scores[k] = v; else die(1, 'QUESTIONNAIRE_INVALID_SCORE', 'preset_scores 只收 0-10 数值：ideas[' + i + '].scores.' + k, '缺省该维由引擎按默认 3 分口径，可直接删掉该字段'); });
  if (Object.keys(scores).length) out.scores = scores;
  const ownComp = Array.isArray(o.competitors) && o.competitors.length ? o.competitors : (Array.isArray(q.competitors) && q.competitors.length ? q.competitors : null);
  if (ownComp) out.competitors = ownComp;
  return out;
});
if (missing.length) die(1, 'QUESTIONNAIRE_MISSING_FIELDS', '问卷缺项/非法（不代填不猜测）：' + missing.join(','), 'idea 文本必填≥10字；econ 四数值必填（0 可以）');

// 契约对齐（v0.2.0 · 公开契约口径）：提交的 payload 由服务端引擎归一化入口消费：
// 顶层 ideas[]（每条 {idea(≥10字,≤2000截断), scores, econ}）或 idea 字段；competitors 每条优先、顶层作默认；>10 条 400 BATCH_TOO_LARGE；空/太短 422 INVALID_INPUT；均不发账单。
const payloadObj = { ideas };
if (ARG.remove || ARG.add) { console.error(JSON.stringify({ ok: true, code: 'OPTIONS_LOCAL_ONLY', msg: '--remove/--add 不随请求提交（生产契约不消费 options），自定义措辞以生成后报告文件本地编辑为准' })); }
const payload = JSON.stringify(payloadObj);
if (Buffer.byteLength(payload) > 64 * 1024) die(1, 'PAYLOAD_TOO_LARGE', '请求体超 64KB（服务端读取上限 65536 字节，超限截断致 422），请勿夹带大附件。');

let proof = null;
if (ARG.proof && ARG.proof !== true) {
  try { const t = fs.readFileSync(path.resolve(String(ARG.proof)), 'utf8').trim(); proof = t; }
  catch (e) { proof = String(ARG.proof); } // 允许直接传凭证串
}

const u = new URL(endpoint);
const lib = u.protocol === 'https:' ? https : http;
const headers = { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(payload) };
if (proof) headers['Payment-Proof'] = proof;

const req = lib.request({ hostname: u.hostname, port: u.port || (u.protocol === 'https:' ? 443 : 80), path: u.pathname + (u.search || ''), method: 'POST', headers, timeout: 20000 }, (res) => {
  let body = '';
  res.on('data', (c) => (body += c));
  res.on('end', () => {
    const out = { ok: res.statusCode === 200, status: res.statusCode, ideaCount: ideas.length, reqBytes: Buffer.byteLength(payload), respBytes: Buffer.byteLength(body) };
    let data = null;
    try { data = JSON.parse(body); } catch (e) { data = null; }
    if (res.statusCode === 402) {
      const bill = res.headers['payment-needed'];
      let billJson = null;
      if (bill) { try { billJson = JSON.parse(Buffer.from(bill, 'base64url').toString('utf8')); } catch (e) { out.billDecodeError = true; } }
      out.next = '按账单完成支付宝 402 支付后，携 --proof <Payment-Proof> 重试即出报告（A 路径扫码/B 路径智能体自动付，见 SKILL.md §二第0步）';
      out.billBody = data; // 服务端 body：{code:"Payment-Needed", out_trade_no, amount, currency, goods_name, order_reused?（同参复用已有订单不重出）}
      out.bill = billJson || (bill ? bill : null); // Payment-Needed 头解码：{protocol:{out_trade_no,amount,currency,resource_id,pay_before,seller_signature,seller_sign_type:"RSA2",seller_unique_id}, method:{...}}
      console.log(JSON.stringify(out));
      process.exit(3);
    }
    if (res.statusCode === 200 && data && data.content) {
      const md = data.content.report_markdown || '';
      const outFile = path.resolve(ARG.out || '点子体检报告.md');
      fs.writeFileSync(outFile, md, 'utf8');
      out.reportFile = outFile;
      out.verdict = data.content.verdict; out.totalScore = data.content.total_score; out.sku = data.content.sku;
      out.outTradeNo = data.out_trade_no; out.tradeNo = data.trade_no;
      out.alreadyFulfilled = data.already_fulfilled === true; // 落库值不硬编：true=已履约单复用既有结果直接返回，不重复交付、不二次计费（响应防重：重提交不重生成资源）
      out.notice = '服务端即用即删（原始点子文本不落盘，只存参数哈希；Payment-Proof 只存 sha256 摘要）；报告仅存于您的本地。改问卷请重新提交（无历史找回）。';
      console.log(JSON.stringify(out));
      process.exit(0);
    }
    if (data && data.code) out.code = data.code; // 400 BATCH_TOO_LARGE / 422 INVALID_INPUT / 500 CONFIG_MISSING|FULFILLMENT_PERSIST_FAILED / 502 FULFILLMENT_CONFIRM_FAILED——码与文案照服务端源透出
    if (data && data.message) out.message = data.message;
    if (res.statusCode === 502 || res.statusCode === 500) out.hint = '勿重复支付：稍后使用同一 Payment-Proof 重试（服务端响应防重，重提交不重生成资源）';
    console.log(JSON.stringify(out));
    process.exit(1);
  });
});
req.on('timeout', () => { req.destroy(new Error('客户端 20s 超时（勿立即重复支付，先核账单状态）')); });
req.on('error', (e) => die(1, 'NETWORK_ERROR', e.message, '网络不可达（端点已于 2026-11-14 对外开放，偶发不可达＝服务器维护窗口，照实等待重试即可）；本脚本除该端点外不发起任何网络请求'));
req.write(payload);
req.end();

// [变更记录 2026-11-12 · v0.2.0] 新基线首版；端点 https://linkkhub.top/idea/generate。
// [变更记录 2026-11-14 · v0.2.1] 对外中性化版：用户可见文案中性化；端点预留口径、退出码 2 设计行为、402/Proof 契约、定价口径（1 条 ¥4.90／2-10 条 ¥9.90／>10 拒单、用户传入 price/goods 字段一律无视）原文零变。
// [变更记录 2026-11-15] 用户面文案与端点状态描述按事实修订（端点已于 2026-11-14 对外开放）；分支逻辑、退出码、402/Proof 契约、定价口径零改动。
