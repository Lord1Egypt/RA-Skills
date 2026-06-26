// ─── OpenNexum 通知模板 ─────────────────────────────────────────────────────
//
// 所有通知统一走模板函数，不使用内联字符串。
// 每个通知类型一个函数，不设 alias。

const SEP = '━━━━━━━━━━━━━━━';

// ─── Shared Types ────────────────────────────────────────────────────────────

export interface CriterionResult {
  id: string;
  passed: boolean;
  reason?: string;
}

export interface EscalationHistoryItem {
  iteration: number;
  feedback: string;
  criteriaResults?: CriterionResult[];
}

// ─── Shared Helpers ──────────────────────────────────────────────────────────

function formatElapsed(ms: number): string {
  if (ms < 1000) return `${ms}ms`;
  const secs = Math.floor(ms / 1000);
  if (secs < 60) return `${secs}s`;
  const mins = Math.floor(secs / 60);
  const rem = secs % 60;
  return rem > 0 ? `${mins}m${rem}s` : `${mins}m`;
}

function shortHash(hash: string | undefined): string {
  return hash?.trim() ? hash.trim().slice(0, 7) : 'unknown';
}

function formatTokens(input: number, output: number): string | null {
  if (input === 0 && output === 0) return null;
  return `${input.toLocaleString('en-US')} in / ${output.toLocaleString('en-US')} out`;
}

function formatCriteriaLines(results: CriterionResult[]): string[] {
  if (results.length === 0) return ['（无）'];
  return results.map((c) => {
    const icon = c.passed ? '✅' : '❌';
    const reason = c.reason?.trim() || (c.passed ? '通过' : '未提供原因');
    return `  ${icon} ${c.id}: ${reason}`;
  });
}

function formatProgress(progress: string, batchProgress?: string): string {
  return batchProgress
    ? `📊 ${batchProgress}  |  总体: ${progress}`
    : `📊 总体: ${progress}`;
}

// ─── ① 派发任务 ──────────────────────────────────────────────────────────────

export interface DispatchOptions {
  taskId: string;
  taskName: string;
  agent: string;
  model?: string;
  scopeCount: number;
  deliverablesCount: number;
  progress: string;
  batchProgress?: string;
}

export function formatDispatch(opts: DispatchOptions): string {
  return [
    `🚀 派发任务 — ${opts.taskId}`,
    SEP,
    `📋 任务内容: ${opts.taskName}`,
    `🤖 Agent: ${opts.agent}`,
    ...(opts.model ? [`🧠 模型: ${opts.model}`] : []),
    `📁 Scope: ${opts.scopeCount} 个文件`,
    `📦 Deliverables: ${opts.deliverablesCount} 项`,
    formatProgress(opts.progress, opts.batchProgress),
    SEP,
  ].join('\n');
}

// ─── ② 代码编写完成 [1/2] ────────────────────────────────────────────────────

export interface GeneratorDoneOptions {
  taskId: string;
  taskName: string;
  agent: string;
  model?: string;
  inputTokens?: number;
  outputTokens?: number;
  scopeFiles?: string[];
  commitHash?: string;
  commitMessage?: string;
  iteration?: number;
  elapsedMs?: number;
}

export function formatGeneratorDone(opts: GeneratorDoneOptions): string {
  const tokenStr = formatTokens(opts.inputTokens ?? 0, opts.outputTokens ?? 0);

  return [
    `🔨 [1/2] 代码编写完成 — ${opts.taskId}`,
    SEP,
    `📋 任务内容: ${opts.taskName}`,
    `🤖 Agent: ${opts.agent}`,
    ...(opts.model ? [`🧠 模型: ${opts.model}`] : []),
    ...(opts.scopeFiles ? [`📁 Scope: ${opts.scopeFiles.length} 个文件`] : []),
    ...(tokenStr ? [`🪙 Token: ${tokenStr}`] : []),
    ...(opts.elapsedMs != null ? [`⏱️ 用时: ${formatElapsed(opts.elapsedMs)}`] : []),
    `🧾 Commit: ${shortHash(opts.commitHash)}`,
    ...(opts.commitMessage ? [`💬 提交信息: ${opts.commitMessage}`] : []),
    `🔁 迭代: 第${(opts.iteration ?? 0) + 1}次`,
    '⏳ 等待代码审查',
    SEP,
  ].join('\n');
}

// ─── ③ 审查通过 [2/2] ────────────────────────────────────────────────────────

export interface ReviewPassedOptions {
  taskId: string;
  taskName: string;
  evaluator: string;
  model?: string;
  elapsedMs: number;
  iteration: number;
  passCount: number;
  totalCount: number;
  unlockedTasks: string[];
  progress: string;
  batchProgress?: string;
}

export function formatReviewPassed(opts: ReviewPassedOptions): string {
  return [
    `✅ [2/2] 审查通过 — ${opts.taskId}`,
    SEP,
    `📋 任务内容: ${opts.taskName}`,
    `🤖 Agent: ${opts.evaluator}`,
    ...(opts.model ? [`🧠 模型: ${opts.model}`] : []),
    `⏱️ 用时: ${formatElapsed(opts.elapsedMs)}`,
    `🔁 迭代: 第${opts.iteration + 1}次`,
    `🎯 Criteria: ${opts.passCount}/${opts.totalCount}`,
    `🔓 解锁任务: ${opts.unlockedTasks.length > 0 ? opts.unlockedTasks.join(', ') : '无'}`,
    formatProgress(opts.progress, opts.batchProgress),
    SEP,
  ].join('\n');
}

// ─── ④ 审查失败 [2/2] ────────────────────────────────────────────────────────

export interface ReviewFailedOptions {
  taskId: string;
  taskName: string;
  evaluator: string;
  model?: string;
  iteration: number;
  passCount: number;
  totalCount: number;
  criteriaResults: CriterionResult[];
  feedback: string;
  autoRetryHint?: string;
}

export function formatReviewFailed(opts: ReviewFailedOptions): string {
  const failCount = opts.criteriaResults.filter((c) => !c.passed).length;

  return [
    `❌ [2/2] 审查失败 — ${opts.taskId} (第${opts.iteration + 1}次)`,
    SEP,
    `📋 任务内容: ${opts.taskName}`,
    `🤖 Agent: ${opts.evaluator}`,
    ...(opts.model ? [`🧠 模型: ${opts.model}`] : []),
    `🎯 Criteria: ${opts.passCount}/${opts.totalCount} 通过，${failCount} 失败`,
    '📌 Criteria 结果:',
    ...formatCriteriaLines(opts.criteriaResults),
    `💬 Feedback: ${opts.feedback || '无'}`,
    `🔄 ${opts.autoRetryHint ?? '系统将自动触发下一次 retry'}`,
    SEP,
  ].join('\n');
}

// ─── ⑤ 任务升级 ──────────────────────────────────────────────────────────────

export interface EscalationOptions {
  taskId: string;
  taskName: string;
  evaluator: string;
  reason?: string;
  note?: string;
  history: EscalationHistoryItem[];
  retryCommand: string;
}

export function formatEscalation(opts: EscalationOptions): string {
  const historyLines =
    opts.history.length > 0
      ? opts.history.flatMap((entry) => [
          `  • 第${entry.iteration + 1}次: ${entry.feedback || '无详细反馈'}`,
          ...formatCriteriaLines(entry.criteriaResults ?? []).map((l) => `  ${l}`),
        ])
      : ['  （无）'];

  return [
    `🚨 任务升级 — ${opts.taskId}`,
    SEP,
    `📋 任务内容: ${opts.taskName}`,
    `🤖 Agent: ${opts.evaluator}`,
    ...(opts.reason ? [`🧯 升级原因: ${opts.reason}`] : []),
    ...(opts.note ? [`📝 备注: ${opts.note}`] : []),
    '🧾 历史失败原因:',
    ...historyLines,
    `🛠 可用命令: ${opts.retryCommand}`,
    SEP,
  ].join('\n');
}

// ─── ⑥ commit 缺失警告 ──────────────────────────────────────────────────────

export interface CommitMissingOptions {
  taskId: string;
  taskName: string;
  headHash: string;
}

export function formatCommitMissing(opts: CommitMissingOptions): string {
  return [
    `⚠️ 代码编写完成，但未检测到新 commit`,
    SEP,
    `📋 任务内容: ${opts.taskName}`,
    `🆔 ID: ${opts.taskId}`,
    `📍 HEAD: \`${shortHash(opts.headHash)}\`（与 base_commit 相同）`,
    '❗ 请检查 generator 是否执行了 git commit + push',
    SEP,
  ].join('\n');
}

// ─── ⑦ 卡死告警 ──────────────────────────────────────────────────────────────

export interface StuckTaskInfo {
  id: string;
  name: string;
  status: string;
  stuckMinutes: number;
  sessionAlive: boolean | null;
}

export function formatHealthAlert(stuck: StuckTaskInfo[]): string {
  const lines = stuck.map((t) => {
    const sessionTag =
      t.sessionAlive === true
        ? '（session 仍在运行）'
        : t.sessionAlive === false
        ? '（session 已结束）'
        : '';
    return `  🔴 ${t.id} [${t.status}] 已卡 ${t.stuckMinutes} 分钟 ${sessionTag}\n     ${t.name}`;
  });

  return [
    `🚨 卡死告警 — ${stuck.length} 个任务疑似卡死`,
    SEP,
    ...lines,
    '',
    '请检查: nexum status --project <dir>',
    SEP,
  ].join('\n');
}

// ─── ⑧ 批次完成 ──────────────────────────────────────────────────────────────

export interface BatchDoneOptions {
  batchName: string;
  tasks: Array<{
    taskId: string;
    taskName: string;
    status: 'done' | 'fail';
    elapsedMs: number;
  }>;
  totalElapsedMs?: number;
}

export function formatBatchDone(opts: BatchDoneOptions): string {
  const taskLines = opts.tasks.map((t) => {
    const icon = t.status === 'done' ? '✅' : '❌';
    return `  ${icon} ${t.taskId} — ${t.taskName} (${formatElapsed(t.elapsedMs)})`;
  });

  const doneCount = opts.tasks.filter((t) => t.status === 'done').length;

  return [
    `🎉 批次完成 — ${opts.batchName}`,
    SEP,
    `📊 结果: ${doneCount}/${opts.tasks.length} 通过`,
    ...(opts.totalElapsedMs != null ? [`⏱️ 总用时: ${formatElapsed(opts.totalElapsedMs)}`] : []),
    '',
    ...taskLines,
    SEP,
  ].join('\n');
}
