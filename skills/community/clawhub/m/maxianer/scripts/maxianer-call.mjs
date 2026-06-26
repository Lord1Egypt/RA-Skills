#!/usr/bin/env node
/**
 * 马仙儿 API 调用脚本
 * 
 * 用法:
 *   node maxianer-call.mjs fate '{"birthDate":"1980-05-14","birthHour":"子","gender":"male","birthPlace":"荣县"}'
 *   node maxianer-call.mjs engines
 *   node maxianer-call.mjs event '{"engine":"liuyao","lines":[7,8,7,9,7,8],"question":{"type":"财运"}}'
 *   node maxianer-call.mjs dream '{"dreamDescription":"梦见蛇缠身"}'
 *   node maxianer-call.mjs report '{"birthDate":"1980-05-14","birthHour":"子","gender":"male","llmSections":[...]}'
 */

const API_URL = (process.env.MAXIANER_API_URL || 'http://34.84.114.113:3333').replace(/\/$/, '');
const API_KEY = process.env.MAXIANER_API_KEY || 'mx-2026-openclaw-shared';

const [,, endpoint, jsonArg] = process.argv;

if (!endpoint) {
  console.error('用法: node maxianer-call.mjs <endpoint> [json_body]');
  console.error('endpoint: fate | event | dream | engines | report');
  process.exit(1);
}

const ENDPOINTS = {
  fate:    { method: 'POST', path: '/api/skill/fate' },
  event:   { method: 'POST', path: '/api/skill/event' },
  dream:   { method: 'POST', path: '/api/skill/dream' },
  engines: { method: 'GET',  path: '/api/skill/engines' },
  report:  { method: 'POST', path: '/api/skill/report' },
};

const ep = ENDPOINTS[endpoint];
if (!ep) {
  console.error(`未知端点: ${endpoint}，可选: ${Object.keys(ENDPOINTS).join(', ')}`);
  process.exit(1);
}

let body = null;
if (jsonArg) {
  try {
    body = JSON.parse(jsonArg);
  } catch (e) {
    console.error(`JSON 解析失败: ${e.message}`);
    process.exit(1);
  }
}

const headers = { 'Content-Type': 'application/json' };
if (API_KEY) headers['Authorization'] = `Bearer ${API_KEY}`;

const opts = { method: ep.method, headers };
if (body && ep.method === 'POST') opts.body = JSON.stringify(body);

try {
  const res = await fetch(`${API_URL}${ep.path}`, opts);
  const text = await res.text();
  
  if (!res.ok) {
    console.error(`API 错误 (${res.status}): ${text}`);
    process.exit(1);
  }
  
  // Pretty-print JSON, pass through HTML
  try {
    const data = JSON.parse(text);
    console.log(JSON.stringify(data, null, 2));
  } catch {
    console.log(text);
  }
} catch (e) {
  console.error(`请求失败: ${e.message}`);
  console.error(`请确保马仙儿服务正在运行（${API_URL}）`);
  process.exit(1);
}
