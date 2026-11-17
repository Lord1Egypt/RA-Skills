/**
 * engine/evolver-bridge.mjs — evolver 后端
 *
 * 把既有的 Evolver CLI 调用封装为与 light 后端一致的接口：
 *   ingestDistill / distillManual / approve
 * 全部 argv 直调（不经过 shell），行为与 0.7.0 起的编排器一致。
 */
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';

export const EVOLVER_ENTRY_REL = 'node_modules/@evomap/evolver/bin/evolver.js';

/** CLI 是否可用（入口文件存在） */
export function available(root) {
  try { return fs.existsSync(path.join(root, EVOLVER_ENTRY_REL)); } catch { return false; }
}

function runCli(root, args, { silent = false, mergeStderr = false, allowFail = false, timeout = 60000 } = {}) {
  const entry = path.join(root, EVOLVER_ENTRY_REL);
  const r = spawnSync(process.execPath, [entry, ...args], {
    cwd: root, encoding: 'utf8', maxBuffer: 1 << 26, timeout,
  });
  if (r.error) {
    // 超时 / 启动失败：allowFail 调用方（inject/approve 为尽力而为）静默返回，其余抛出可读错误
    if (allowFail) return '';
    const err = new Error(`evolver CLI 调用失败（${r.error.code || 'error'}）：${String(r.error.message).slice(0, 200)}`);
    err.code = r.error.code;
    throw err;
  }
  const out = (r.stdout ?? '') + (mergeStderr ? (r.stderr ?? '') : '');
  if (!allowFail && r.status !== 0) {
    const err = new Error(`evolver exit ${r.status}: ${String(r.stderr ?? '').trim().slice(0, 200)}`);
    err.status = r.status;
    throw err;
  }
  return out;
}

/** transcript → 起草 gene（evolver ingest --distill） */
export function ingestDistill(root, transcriptPath) {
  const raw = runCli(root, ['ingest', '--distill', transcriptPath], { mergeStderr: true });
  const m = raw.match(/drafted UNPROVEN gene (gene_distilled_\w+)/);
  return { geneId: m ? m[1] : null, raw };
}

/** 手工蒸馏（LLM 精修路径） */
export function distillManual(root, { category = 'repair', signals = 'read,bash,exception', strategy, summary }) {
  const raw = runCli(root, ['distill', '--category', category, '--signals', signals,
    '--strategy', strategy, '--summary', summary], { mergeStderr: true });
  const m = raw.match(/gene_[a-z0-9_]+/);
  return { geneId: m ? m[0] : null, raw };
}

/** 注入块（evolver inject session-start；仅含 summary 标签，真正可执行的修法由调用方另行拼装） */
export function injectSessionStart(root) {
  // 注意：evolver 的正确用法是子命令 + 位置参数（inject session-start），不是 --session-start
  return runCli(root, ['inject', 'session-start'], { silent: true, allowFail: true }) || '';
}

/** 审核通过（台账写入） */
export function approve(root, geneId) {
  runCli(root, ['review', '--approve', geneId], { silent: true, allowFail: true });
  return { ok: true };
}
