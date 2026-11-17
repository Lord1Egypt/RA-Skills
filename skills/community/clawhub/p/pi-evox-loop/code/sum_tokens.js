#!/usr/bin/env node
/** 汇总指定 session 目录下所有 Pi session 文件的 token 用量与工具调用统计 */
import { readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';

const dir = process.argv[2];
if (!dir) { console.error('usage: node sum_tokens.js <session-dir>'); process.exit(2); }

let files = [];
try { files = readdirSync(dir).filter((f) => f.endsWith('.jsonl')); } catch { /* dir missing */ }
if (files.length === 0) { console.log('no session files'); process.exit(0); }

let total = { input: 0, output: 0, cacheRead: 0, cacheWrite: 0, totalTokens: 0 };
let assistantMsgs = 0, toolCalls = 0, toolErrors = 0, turns = 0;

for (const f of files) {
  for (const line of readFileSync(join(dir, f), 'utf8').split(/\r?\n/)) {
    if (!line.trim()) continue;
    let e; try { e = JSON.parse(line); } catch { continue; }
    if (e.type !== 'message') continue;
    const m = e.message ?? {};
    turns++;
    if (m.role === 'assistant') {
      assistantMsgs++;
      const u = m.usage ?? {};
      total.input += u.input ?? 0;
      total.output += u.output ?? 0;
      total.cacheRead += u.cacheRead ?? 0;
      total.cacheWrite += u.cacheWrite ?? 0;
      total.totalTokens += u.totalTokens ?? 0;
      for (const b of m.content ?? []) if (b.type === 'toolCall') toolCalls++;
      if (m.stopReason === 'error') toolErrors++;
    }
    if (m.role === 'toolResult' && m.isError) toolErrors++;
  }
}
console.log(JSON.stringify({ files: files.length, turns, assistantMsgs, toolCalls, toolErrors, usage: total }, null, 2));
