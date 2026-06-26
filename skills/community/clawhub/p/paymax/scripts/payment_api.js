#!/usr/bin/env node
/**
 * payment_api.js - 调用收款码 API 获取 tradeCode（Node.js 版本，仅使用内置模块）
 *
 * 用法：
 *   node payment_api.js --amount 50 [--order_type tip] [--payee "主播小明"] [--description "打赏主播小明50元"]
 *
 * 输出（成功）：
 *   SUCCESS
 *   tradeCode=62254562871846512
 *   tradeLink=https://pay-h5.4199191.xyz/pyment/62254562871846512
 *
 * 输出（失败）：
 *   FAIL
 *   message=错误原因描述
 */

const https = require('https');
const http = require('http');

const API_URL = 'https://pay.4199191.xyz/code';
const TIMEOUT_MS = 30000;

function parseArgs() {
  const args = process.argv.slice(2);
  const result = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--') && i + 1 < args.length) {
      const key = args[i].slice(2);
      result[key] = args[i + 1];
      i++;
    }
  }
  return result;
}

function fail(message) {
  process.stdout.write('FAIL\n');
  process.stdout.write(`message=${message}\n`);
  process.exit(1);
}

function success(tradeCode, tradeLink) {
  process.stdout.write('SUCCESS\n');
  process.stdout.write(`tradeCode=${tradeCode}\n`);
  process.stdout.write(`tradeLink=${tradeLink}\n`);
  process.exit(0);
}

const args = parseArgs();
const payload = {};
if (args.amount !== undefined) payload.amount = parseFloat(args.amount);
if (args.order_type !== undefined) payload.order_type = args.order_type;
if (args.payee !== undefined) payload.payee = args.payee;
if (args.description !== undefined) payload.description = args.description;

const body = JSON.stringify(payload);
const url = new URL(API_URL);
const lib = url.protocol === 'https:' ? https : http;

const options = {
  hostname: url.hostname,
  port: url.port || (url.protocol === 'https:' ? 443 : 80),
  path: url.pathname,
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Content-Length': Buffer.byteLength(body),
  },
};

const req = lib.request(options, (res) => {
  let raw = '';
  res.setEncoding('utf8');
  res.on('data', (chunk) => { raw += chunk; });
  res.on('end', () => {
    let result;
    try {
      result = JSON.parse(raw);
    } catch (e) {
      fail('响应解析失败，请稍后重试');
      return;
    }
    if (result.resultCode === 1) {
      const data = result.data || {};
      success(data.tradeCode || '', data.tradeLink || '');
    } else {
      fail(result.message || '未知错误');
    }
  });
});

req.setTimeout(TIMEOUT_MS, () => {
  req.destroy();
  fail('请求超时，请稍后重试');
});

req.on('error', (e) => {
  if (e.code === 'ECONNREFUSED' || e.code === 'ENOTFOUND') {
    fail('网络连接失败，请检查网络后重试');
  } else {
    fail('支付服务暂时不可用，请稍后重试');
  }
});

req.write(body);
req.end();
