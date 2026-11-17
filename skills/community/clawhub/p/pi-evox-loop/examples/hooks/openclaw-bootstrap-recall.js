/**
 * OpenClaw 宿主钩子示例 —— 任务开始时自动召回经验库
 *
 * 事件：agent:bootstrap（工作区文件注入「前」）
 * 行为：调用 evolver-recall.mjs，把命中到的修法作为一个**虚拟引导文件**注入。
 *
 * 接入方式（按你的 OpenClaw 安装调整路径）：
 *   1. 把本文件放到钩子进程能加载的位置（示例：~/.openclaw/hooks/evox-recall/handler.js）
 *   2. 在钩子配置里注册 `agent:bootstrap` 事件指向本 handler
 *   3. 重启网关使钩子生效（OpenClaw 改 handler 通常需要重启）
 *
 * 纪律（很重要，别改掉）：
 *   - 空库 / 没命中 → **零注入**（绝不在没命中时塞"教程"或任意基因）
 *   - 任何异常 → **零注入**（钩子绝不能让宿主启动失败）
 *   - 子代理会话跳过（避免污染）
 *
 * 对应文档：SKILL.md「宿主接入契约」第 1 步。
 */

const { execFileSync } = require('node:child_process');
const fs = require('node:fs');
const path = require('node:path');

// ── 按你的实际安装改这三个路径 ──────────────────────────────────────────
const RECALL_SCRIPT = process.env.EVOX_RECALL_SCRIPT || '<技能目录>/code/evolver-recall.mjs';
const HITS_DIR = process.env.EVOX_HITS_DIR || '<技能目录>/experiments';
const CACHE_FILE = path.join(__dirname, '.evox-last-task.json');
// ────────────────────────────────────────────────────────────────────────

const FOOTER = String.fromCharCode(10) + '[修好坑后立刻沉淀: light-cli draft --error <报错> --context <在做什么> --commit | 用了修法: evolver-recall --register-hit --gene <id> --note ...]' + String.fromCharCode(10);
const FILE_NAME = 'EVOX_INHERITED_FIXES.md';
const FILE_PATH = FILE_NAME;
const MAX_TOTAL = 3000;
const TIMEOUT_MS = 15000;

/**
 * 缓存最近的用户任务文本。
 * 为什么需要：`agent:bootstrap` 通常发生在**用户消息落库之前**，
 * 当场取不到任务文本；所以先缓存、下次 bootstrap 再用（对靶的关键）。
 */
function cacheTask(sessionKey, text) {
  try {
    fs.writeFileSync(CACHE_FILE, JSON.stringify({ sessionKey, text: String(text).slice(0, 2000), ts: Date.now() }));
  } catch { /* 缓存失败不影响主流程 */ }
}

function cachedTask(sessionKey) {
  try {
    const j = JSON.parse(fs.readFileSync(CACHE_FILE, 'utf8'));
    if (j && j.sessionKey === sessionKey && typeof j.text === 'string') return j.text;
  } catch { /* 无缓存 */ }
  return '';
}

/** 从任意形状的消息事件里挖出文本（字段名随宿主版本而异，故多路径探测） */
function extractMessageText(event, depth = 0) {
  if (!event || typeof event !== 'object' || depth > 4) return '';
  for (const k of ['text', 'content', 'body', 'bodyText', 'message', 'raw']) {
    const v = event[k];
    if (typeof v === 'string' && v.trim().length >= 3) return v.trim();
    if (Array.isArray(v)) {
      const t = v.filter((b) => b && (b.type === 'text' || b.type === undefined)).map((b) => b.text || '').join(' ');
      if (t.trim().length >= 3) return t.trim();
    }
  }
  for (const k of ['context', 'message', 'data', 'payload']) {
    const t = extractMessageText(event[k], depth + 1);
    if (t) return t;
  }
  return '';
}

const HEADER = [
  '## EvoX inherited fixes (auto-recalled)',
  '',
  'Recalled from your validated experience store (approved entries only).',
  'Apply them when relevant to the current task.',
  '',
].join('\n');

/** 只保留 recall 输出里的「修法行」（形如 [#1|gene_xxx] [repair] ...） */
function extractFixes(stdout) {
  const out = [];
  for (const raw of String(stdout || '').split('\n')) {
    const s = raw.trim();
    if (/^\[#\d+\|/.test(s)) out.push(s);
  }
  return out;
}

function collectContent(query) {
  const args = [RECALL_SCRIPT, '--agent', 'openclaw'];
  // 关键：把用户的真实诉求传进去（对靶）。没有 query 时 recall 会不注入——这是对的。
  if (query) args.push('--query', String(query).slice(0, 2000));
  let stdout = '';
  try {
    stdout = execFileSync(process.execPath, args, {
      encoding: 'utf8', timeout: TIMEOUT_MS, maxBuffer: 4 * 1024 * 1024,
      env: Object.assign({}, process.env, { EVOX_HITS_DIR: HITS_DIR }),
    });
  } catch { return null; } // 任何异常 → 零注入
  const fixes = extractFixes(stdout);
  if (fixes.length === 0) return null;
  let body = fixes.join('\n');
  if (body.length > MAX_TOTAL) body = body.slice(0, MAX_TOTAL) + '\n…';
  return HEADER + body + FOOTER;
}

const handler = async (event) => {
  if (!event || typeof event !== 'object') return;

  // 消息事件：先缓存该会话的用户文本，供下次 bootstrap 对靶
  if (event.type === 'message') {
    try {
      const text = extractMessageText(event);
      const sk = String(event.sessionKey || '');
      if (text && sk && !sk.includes(':subagent:')) cacheTask(sk, text);
    } catch { /* 忽略 */ }
    return;
  }

  if (event.type !== 'agent' || event.action !== 'bootstrap') return;
  if (!event.context || typeof event.context !== 'object') return;

  const sessionKey = String(event.sessionKey || '');
  if (sessionKey.includes(':subagent:')) return;

  const files = event.context.bootstrapFiles;
  if (!Array.isArray(files)) return;

  const isMine = (f) => f && typeof f === 'object' && f.path === FILE_PATH && f.virtual === true;
  // 退让：已存在同名「真实」文件时不覆盖用户文件
  if (files.some((f) => f && typeof f === 'object' && f.path === FILE_PATH && !isMine(f))) return;

  const query = cachedTask(sessionKey);
  const content = collectContent(query);
  if (!content) return; // 没命中 → 零注入

  const next = files.filter((f) => !isMine(f));
  next.push({ name: FILE_NAME, path: FILE_PATH, content, missing: false, virtual: true });
  event.context.bootstrapFiles = next;
};

module.exports = handler;
module.exports.default = handler;
