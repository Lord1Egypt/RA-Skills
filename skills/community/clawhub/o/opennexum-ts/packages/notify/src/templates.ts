const SEP = "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━";

function formatElapsed(ms: number): string {
  if (ms < 1000) return `${ms}ms`;
  const secs = Math.floor(ms / 1000);
  if (secs < 60) return `${secs}s`;
  const mins = Math.floor(secs / 60);
  const rem = secs % 60;
  return `${mins}m${rem}s`;
}

export function formatDispatch(
  taskId: string,
  taskName: string,
  agentId: string,
  scopeCount: number,
  deliverablesCount: number,
  progress: string
): string {
  return [
    `🚀 派发任务`,
    SEP,
    `📋 任务内容: ${taskName}`,
    `🆔 任务ID: ${taskId}`,
    `🤖 Agent: ${agentId}`,
    `📁 Scope: ${scopeCount} 个文件`,
    `📦 Deliverables: ${deliverablesCount} 项`,
    `📊 进度: ${progress}`,
    SEP,
  ].join("\n");
}

export function formatComplete(
  taskId: string,
  taskName: string,
  elapsedMs: number,
  iteration: number,
  passCount: number,
  totalCount: number,
  unlockedTasks: string[],
  progress: string
): string {
  const unlockedLine =
    unlockedTasks.length > 0
      ? `🔓 解锁任务: ${unlockedTasks.join(", ")}`
      : `🔓 解锁任务: 无`;
  return [
    `✅ 任务通过`,
    SEP,
    `📋 任务内容: ${taskName}`,
    `🆔 任务ID: ${taskId}`,
    `⏱️ 用时: ${formatElapsed(elapsedMs)}`,
    `🔁 迭代: ${iteration}`,
    `🎯 Criteria: ${passCount}/${totalCount} 通过`,
    unlockedLine,
    `📊 进度: ${progress}`,
    SEP,
  ].join("\n");
}

export function formatFail(
  taskId: string,
  taskName: string,
  iteration: number,
  passCount: number,
  totalCount: number,
  failCount: number,
  failedCriteria: string[],
  feedbackExcerpt: string
): string {
  const criteriaLines =
    failedCriteria.length > 0
      ? failedCriteria.map((c) => `  • ${c}`).join("\n")
      : "  (none)";
  return [
    `❌ 任务失败`,
    SEP,
    `📋 任务内容: ${taskName}`,
    `🆔 任务ID: ${taskId}`,
    `🔁 迭代: ${iteration}`,
    `🎯 Criteria: ${passCount}/${totalCount} 通过，${failCount} 失败`,
    `💥 失败项:`,
    criteriaLines,
    `💬 Feedback: ${feedbackExcerpt}`,
    SEP,
  ].join("\n");
}

export function formatBatchDone(
  projectName: string,
  tasks: Array<{ taskId: string; taskName: string; status: "done" | "fail"; elapsedMs: number }>
): string {
  const taskLines = tasks
    .map((t) => {
      const icon = t.status === "done" ? "✅" : "❌";
      return `  ${icon} ${t.taskId} — ${t.taskName} (${formatElapsed(t.elapsedMs)})`;
    })
    .join("\n");
  return [
    `🎉 批次完成 — ${projectName}`,
    SEP,
    `📦 任务列表 (${tasks.length}):`,
    taskLines,
    SEP,
  ].join("\n");
}
