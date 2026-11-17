#!/usr/bin/env node

/**
 * wc3-code — LLM 子会话调用工具（生成的 skill 包内置）。
 *
 * 【重要】本工具不再直接 spawn Code CLI，而是 POST 到本地 pipeline serve（:3460）的 /api/llm，
 * 由 serve（daemon，干净环境启动）代跑模型。原因：skill.mjs 直接 spawn 会继承宿主 Agent 注入的
 * 环境变量，在 workbuddy 等宿主里劫持登录态/配置目录。收口走 HTTP 后环境劫持从根上消失。
 *
 * CLI 接口保持不变（--prompt/--prompt-file/--output/--schema/--resume/--timeout），
 * skill 里的 callClaude/callClaudeWithFile 封装无需改动。
 */

import { readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';

const DEFAULT_TIMEOUT = 600; // 秒；仅作客户端 AbortController 兜底，真正超时由 serve 端控制
const LLM_ENDPOINT = process.env.WC3_LLM_ENDPOINT || 'http://127.0.0.1:3460/api/llm';

function parseArgs() {
  const args = process.argv.slice(2);
  const result = { prompt: null, promptFile: null, output: null, schema: null, timeout: DEFAULT_TIMEOUT, resume: null };
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--prompt' && args[i + 1]) result.prompt = args[++i];
    else if (args[i] === '--prompt-file' && args[i + 1]) result.promptFile = args[++i];
    else if (args[i] === '--output' && args[i + 1]) result.output = resolve(args[++i]);
    else if (args[i] === '--schema' && args[i + 1]) result.schema = args[++i]; // 兼容内联 JSON 与文件路径，读取时区分
    else if (args[i] === '--timeout' && args[i + 1]) result.timeout = parseInt(args[++i], 10);
    else if (args[i] === '--resume' && args[i + 1]) result.resume = args[++i];
    else if (args[i] === '--help' || args[i] === '-h') { printUsage(); process.exit(0); }
  }
  return result;
}

function printUsage() {
  process.stderr.write(`wc3-code — LLM 子会话调用工具（经本地 serve :3460 代跑）

Usage:
  wc3-code --prompt "..." --output result.json
  wc3-code --prompt-file prompt.md --output result.json
  wc3-code --prompt-file prompt.md --output result.json --schema schema.json
  wc3-code --resume <session-id> --prompt "继续..." --output result.json

Options:
  --prompt       直接传入 prompt 文本
  --prompt-file  从文件读取 prompt
  --output       结果输出文件路径（同时也输出到 stdout）
  --schema       JSON Schema 文件路径（serve 端校验失败自动 retry）
  --timeout      客户端超时秒数（默认 600；serve 端另有兜底超时）
  --resume       复用已有 session ID
  -h, --help     显示帮助

Endpoint: ${LLM_ENDPOINT}（可用 WC3_LLM_ENDPOINT 覆盖）
`);
}

async function main() {
  const opts = parseArgs();

  if (!opts.prompt && !opts.promptFile) {
    process.stderr.write('Error: --prompt or --prompt-file required\n');
    process.exit(1);
  }
  if (!opts.output) {
    process.stderr.write('Error: --output required\n');
    process.exit(1);
  }

  let prompt = opts.prompt;
  if (opts.promptFile) {
    prompt = readFileSync(resolve(opts.promptFile), 'utf-8');
  }

  const payload = { prompt };
  if (opts.resume) payload.resume = opts.resume;
  if (opts.schema) {
    try {
      // 兼容两种传法：① 内联 JSON 字符串（生成器 distill 常见写法）；② JSON Schema 文件路径。
      // 先尝试直接解析——若以 { / [ 开头则是内联 JSON；否则当作文件路径读取。
      const s = String(opts.schema).trim();
      if (s.startsWith('{') || s.startsWith('[')) {
        payload.schema = JSON.parse(s);
      } else {
        payload.schema = JSON.parse(readFileSync(resolve(opts.schema), 'utf-8'));
      }
    } catch (err) {
      process.stderr.write(`Error reading schema: ${err.message}\n`);
      process.exit(1);
    }
  }

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), opts.timeout * 1000);

  let resp;
  try {
    resp = await fetch(LLM_ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
      signal: controller.signal,
    });
  } catch (err) {
    clearTimeout(timer);
    if (err.name === 'AbortError') {
      process.stderr.write(`Error: 请求超时（${opts.timeout}s）\n`);
    } else {
      process.stderr.write(`Error: 无法连接 pipeline serve（${LLM_ENDPOINT}）：${err.message}\n请确认本地 serve 已启动。\n`);
    }
    process.exit(1);
  }
  clearTimeout(timer);

  let data;
  try {
    data = await resp.json();
  } catch (err) {
    process.stderr.write(`Error: serve 返回非 JSON：${err.message}\n`);
    process.exit(1);
  }

  if (!resp.ok) {
    process.stderr.write(`Error: serve ${resp.status}: ${data.error || JSON.stringify(data)}\n`);
    process.exit(1);
  }

  // result：有 schema 时是 JSON 对象，否则是文本。统一写盘 + stdout（契约同旧版）。
  const outputContent = typeof data.result === 'string'
    ? data.result
    : JSON.stringify(data.result, null, 2);
  writeFileSync(opts.output, outputContent, 'utf-8');
  process.stdout.write(outputContent);
  process.exit(0);
}

main();
