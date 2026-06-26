import * as fs from "node:fs";
import * as path from "node:path";

const HOOK_LOG = path.join(require("node:os").homedir(), ".openclaw/workspace/hooks/session-sleep-wake/hook.log");
const log = (msg: string) => {
  const ts = new Date().toISOString();
  fs.appendFileSync(HOOK_LOG, `[${ts}] ${msg}\n`);
};

interface HookEvent {
  type: string;
  action: string;
  sessionKey?: string;
  workspaceDir?: string;
  context?: {
    workspaceDir?: string;
    bootstrapFiles?: Array<{ path: string; content: string; isInline: boolean }>;
    [key: string]: unknown;
  };
}

const handler = async (event: HookEvent) => {
  // 记录所有事件，方便调试
  log(`[hook] Fired: type=${event.type} action=${event.action} sessionKey=${event.sessionKey}`);

  // 注意：只监听 agent:bootstrap
  // agent:bootstrap 在 /new 或 /reset 触发 session reset 时，bootstrap 文件注入之前 firing
  if (event.type !== "agent" || event.action !== "bootstrap") {
    log(`[hook] Skipped: not agent:bootstrap`);
    return;
  }

  // workspaceDir 直接在 event 顶层（不在 context 里）
  const workspaceDir = event.workspaceDir || event.context?.workspaceDir;
  const sessionKey = event.sessionKey;
  if (!sessionKey || !workspaceDir) {
    log(`[hook] Skipped: missing sessionKey=${sessionKey} or workspaceDir=${workspaceDir}`);
    return;
  }

  const previewDir = path.join(workspaceDir, "previews");
  const previewPath = path.join(previewDir, `${sessionKey}.md`);
  log(`[hook] Preview path: ${previewPath} exists=${fs.existsSync(previewPath)}`);

  if (!fs.existsSync(previewPath)) {
    log(`[hook] No preview file, skipping`);
    return;
  }

  const content = fs.readFileSync(previewPath, "utf-8");

  // 提取状态，支持"## 状态: pending"或"## 状态\npending"等多种格式
  const statusMatch = content.match(/##\s*状态[\r\n]+([^\s#][^\r\n]*)/i);
  const status = statusMatch ? statusMatch[1].trim().toLowerCase() : "unknown";
  log(`[hook] Preview status: "${status}"`);

  if (status !== "pending") {
    log(`[hook] Status is "${status}", skipping`);
    return;
  }

  // 提取各段内容
  const extract = (regex: RegExp): string => {
    const m = content.match(regex);
    return m ? m[1].trim().replace(/^[\s-]+/gm, "") : "（无）";
  };

  const summary = extract(/##\s*本次 session 摘要[\r\n]+([\s\S]*?)(?=##\s*未完成|##\s*醒来|##\s*关键)/i);
  const items = extract(/##\s*未完成事项[\r\n]+([\s\S]*?)(?=##\s*醒来|##\s*关键)/i);
  const nextStep = extract(/##\s*醒来后第一步[\r\n]+([\s\S]*?)(?=##\s*关键)/i);
  const context = extract(/##\s*关键上下文[\r\n]+([\s\S]*?)(?=##\s*状态|$)/i);

  const recoveryText = [
    "🌙 检测到上次 session 有未完成事项，恢复上下文：",
    "",
    `**上次 session 摘要**：${summary}`,
    "",
    `**未完成事项**：\n${items}`,
    "",
    `**醒来后第一步**：${nextStep}`,
    "",
    `**关键上下文**：${context}`,
    "",
    "请根据上述信息，继续处理未完成的事项。",
  ].join("\n");

  log(`[hook] Recovery text length: ${recoveryText.length} chars`);

  // 注入到 bootstrapFiles
  if (event.context && Array.isArray(event.context.bootstrapFiles)) {
    event.context.bootstrapFiles.unshift({
      path: `memory:session-recovery/${sessionKey}.md`,
      content: recoveryText,
      isInline: true,
    });
    log(`[hook] Injected via bootstrapFiles (count=${event.context.bootstrapFiles.length})`);
  } else {
    log(`[hook] bootstrapFiles not available, context keys: ${JSON.stringify(Object.keys(event.context || {}))}`);
  }

  log(`[hook] Done for session ${sessionKey}`);
};

export default handler;
