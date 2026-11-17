#!/usr/bin/env node
/**
 * pi_session_adapter 原型（路线 B · 非生产代码）
 *
 * 输入：Pi session JSONL（~/.pi/agent/sessions/--<path>--/<ts>_<uuid>.jsonl）
 *   - 首行 SessionHeader: {"type":"session","version":3,...}
 *   - 其余 entry: {type,id,parentId,timestamp,...}，id+parentId 构成树
 * 输出：每个 leaf 分支一份 generic-chat 转录（Evolver ingest 原生可识别）
 *   - 文件名契约：<sessionId>[.branch-<leafId>].transcript.jsonl
 *   - 内容契约：OpenAI chat 形状 JSONL（role: user/assistant/tool + tool_calls/tool_call_id）
 *
 * 用法：node pi_session_adapter.js <pi-session.jsonl> [--out <dir>] [--active-only]
 */
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { basename, join, resolve } from 'node:path';
import { platform, arch } from 'node:os';

// ---------- 解析 ----------
function parseSession(path) {
  const lines = readFileSync(path, 'utf8').split(/\r?\n/).filter((l) => l.trim());
  let header = null;
  const entries = [];
  for (const line of lines) {
    let obj;
    try { obj = JSON.parse(line); } catch { continue; } // 容错：跳过坏行
    if (obj.type === 'session') { header = obj; continue; }
    if (obj.id !== undefined) entries.push(obj);
  }
  return { header, entries };
}

// ---------- 树操作 ----------
function findLeaves(entries) {
  const hasChild = new Set();
  for (const e of entries) if (e.parentId) hasChild.add(e.parentId);
  return entries.filter((e) => !hasChild.has(e.id));
}

function branchToRoot(entriesById, leafId) {
  const chain = [];
  let cur = entriesById.get(leafId);
  const guard = new Set();
  while (cur) {
    if (guard.has(cur.id)) break; // 防环
    guard.add(cur.id);
    chain.unshift(cur);
    cur = cur.parentId ? entriesById.get(cur.parentId) : null;
    if (cur === undefined) { // 孤儿：parentId 悬空，挂断点并告警
      console.error(`[adapter:warn] orphan entry ${chain[0]?.id}: missing parent, truncated branch`);
      break;
    }
  }
  return chain;
}

// ---------- 内容块工具 ----------
function textOf(content) {
  if (typeof content === 'string') return content;
  if (Array.isArray(content)) {
    return content
      .filter((b) => b && (b.type === 'text' || b.type === undefined))
      .map((b) => b.text ?? '')
      .join('\n');
  }
  return '';
}

// ---------- entry → generic-chat message(s) ----------
function convertEntry(entry, ctx) {
  const out = [];
  switch (entry.type) {
    case 'message': {
      const m = entry.message ?? {};
      switch (m.role) {
        case 'user':
          out.push({ role: 'user', content: textOf(m.content) });
          break;
        case 'assistant': {
          const msg = { role: 'assistant', content: '' };
          const texts = [];
          const thinkings = [];
          const toolCalls = [];
          for (const b of m.content ?? []) {
            if (b.type === 'text') texts.push(b.text);
            else if (b.type === 'thinking') thinkings.push(b.thinking);
            else if (b.type === 'toolCall') {
              toolCalls.push({
                id: b.id,
                type: 'function',
                function: { name: b.name, arguments: JSON.stringify(b.arguments ?? {}) },
              });
            }
          }
          // stopReason=error 的失败叙述是 AVOID 信号源，必须保留进文本
          if (m.stopReason === 'error' && m.errorMessage) texts.push(`[error] ${m.errorMessage}`);
          if (m.stopReason === 'aborted') texts.push('[aborted] response aborted by user');
          msg.content = texts.join('\n');
          if (thinkings.length) msg.reasoning_content = thinkings.join('\n');
          if (toolCalls.length) msg.tool_calls = toolCalls;
          if (m.model && !ctx.modelCaptured) { ctx.model = m.model; ctx.provider = m.provider; ctx.modelCaptured = true; }
          if (m.usage) ctx.usageTotal = (ctx.usageTotal ?? 0) + (m.usage.totalTokens ?? 0);
          out.push(msg);
          break;
        }
        case 'toolResult': {
          let text = textOf(m.content);
          if (m.isError) text = `ERROR (tool failed): ${text}`; // 工具失败=AVOID 信号，显式标注
          // is_error 显式失败标志：evolver chatMessageToTurns 据此设置 turn.errorMessage，
          // extractSignals 从 errorMessage 挖 strong 错误信号（否则失败只落在 toolResult 文本，产不出 strong 信号）
          out.push({ role: 'tool', tool_call_id: m.toolCallId, content: text, ...(m.isError ? { is_error: true } : {}) });
          break;
        }
        case 'bashExecution': {
          // 用户 ! 命令：映射为 assistant 调用 + tool 结果，保留 exit_code（失败信号）
          const callId = `bash_${entry.id}`;
          out.push({
            role: 'assistant',
            content: '',
            tool_calls: [{ id: callId, type: 'function', function: { name: 'bash', arguments: JSON.stringify({ command: m.command }) } }],
          });
          let result = m.output ?? '';
          if (m.cancelled) result = `[cancelled] ${result}`;
          result = `${result}\nexit_code=${m.exitCode ?? 'unknown'}`;
          const bashFailed = (m.exitCode ?? 0) !== 0 || m.cancelled === true;
          out.push({ role: 'tool', tool_call_id: callId, content: result, ...(bashFailed ? { is_error: true } : {}) });
          break;
        }
        case 'custom':
          out.push({ role: 'user', content: `[extension:${m.customType}] ${textOf(m.content)}` });
          break;
        case 'branchSummary':
          out.push({ role: 'system', content: `[branch_summary meta] ${m.summary}` });
          break;
        case 'compactionSummary':
          out.push({ role: 'system', content: `[compaction_summary meta, ${m.tokensBefore} tokens] ${m.summary}` });
          break;
        default:
          break;
      }
      break;
    }
    case 'compaction': {
      out.push({ role: 'system', content: `[compaction meta, ${entry.tokensBefore ?? '?'} tokens before] ${entry.summary ?? ''}` });
      // retainedTail 是自包含检查点：展开为真实消息，保证蒸馏看到压缩后的活跃上下文
      for (const tail of entry.retainedTail ?? []) {
        const fake = { type: 'message', id: `${entry.id}_tail`, parentId: entry.id, message: tail };
        out.push(...convertEntry(fake, ctx));
      }
      break;
    }
    case 'branch_summary':
      out.push({ role: 'system', content: `[branch_summary meta] ${entry.summary ?? ''}` });
      break;
    case 'custom_message':
      out.push({ role: 'user', content: `[extension:${entry.customType}] ${textOf(entry.content)}` });
      break;
    case 'model_change':
      ctx.model = entry.modelId ?? ctx.model;
      ctx.provider = entry.provider ?? ctx.provider;
      break;
    // custom / label / session_info / thinking_level_change：不进 LLM 上下文，跳过
    default:
      break;
  }
  return out;
}

// ---------- 主流程 ----------
function main() {
  const args = process.argv.slice(2);
  const input = args[0];
  if (!input) {
    console.error('usage: node pi_session_adapter.js <pi-session.jsonl> [--out <dir>] [--active-only]');
    process.exit(2);
  }
  const outDir = resolve(args.includes('--out') ? args[args.indexOf('--out') + 1] : './evolver-inbox');
  const activeOnly = args.includes('--active-only');
  mkdirSync(outDir, { recursive: true });

  const { header, entries } = parseSession(input);
  if (!header) { console.error('[adapter] missing session header'); process.exit(1); }
  const entriesById = new Map(entries.map((e) => [e.id, e]));
  let leaves = findLeaves(entries);
  if (leaves.length === 0) { console.error('[adapter] no entries'); process.exit(1); }
  if (activeOnly && leaves.length > 1) {
    // 活跃分支近似 = 时间戳最新的 leaf
    leaves = [leaves.reduce((a, b) => (String(a.timestamp) > String(b.timestamp) ? a : b))];
  }

  const written = [];
  for (const leaf of leaves) {
    const chain = branchToRoot(entriesById, leaf.id);
    const ctx = {};
    const messages = [];
    // env_fingerprint 头部（Capsule 固化时的环境指纹来源）
    // 隐私（SkillSpector finding 修复）：默认不含 cwd（工作目录可泄露项目/客户身份）；
    // 实验确需 cwd 时显式传 --include-cwd。
    const fpParts = [`platform=${platform()}`, `arch=${arch()}`, `pi_session=${header.id}`];
    if (args.includes('--include-cwd')) fpParts.push(`cwd=${header.cwd ?? 'unknown'}`);
    messages.push({
      role: 'system',
      content: `env_fingerprint: ${fpParts.join(' ')}`,
    });
    for (const e of chain) messages.push(...convertEntry(e, ctx));
    if (ctx.model) messages[0].content += ` model=${ctx.provider ?? ''}/${ctx.model}`;
    if (ctx.usageTotal) messages[0].content += ` total_tokens=${ctx.usageTotal}`;

    const suffix = leaves.length > 1 ? `.branch-${leaf.id}` : '';
    const outPath = join(outDir, `${header.id}${suffix}.transcript.jsonl`);
    writeFileSync(outPath, messages.map((m) => JSON.stringify(m)).join('\n') + '\n');
    written.push({ outPath, turns: messages.length, leaf: leaf.id });
  }
  for (const w of written) console.log(`[adapter] wrote ${w.turns} turns -> ${w.outPath} (leaf=${w.leaf})`);
}

main();
