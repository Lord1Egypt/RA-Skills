import { wecomFetch } from "../../http.js";
import { LIMITS, monitorState } from "../../monitor/state.js";
import { toWeComMarkdownV2 } from "../../wecom_msg_adapter/markdown_adapter.js";

const activeReplyStore = monitorState.activeReplyStore;

export function storeActiveReply(streamId: string, responseUrl?: string, proxyUrl?: string): void {
  activeReplyStore.store(streamId, responseUrl, proxyUrl);
}

export function getActiveReplyUrl(streamId: string): string | undefined {
  return activeReplyStore.getUrl(streamId);
}

export async function useActiveReplyOnce(
  streamId: string,
  fn: (params: { responseUrl: string; proxyUrl?: string }) => Promise<void>,
): Promise<void> {
  return activeReplyStore.use(streamId, async (params) => {
    await new Promise((resolve) => setTimeout(resolve, 1000));
    await fn(params);
  });
}

// markdown_v2 触发模式: 标题 / 粗体 / 链接 / 行内代码或代码块 / 引用 / 列表 / 表格
const MARKDOWN_PATTERNS = /^#{1,6}\s|\*\*[^*\n]+\*\*|\[[^\]\n]+\]\([^)\s]+\)|`[^`\n]+`|```|^>\s|^\s*[-*+]\s|\|.*\|/m;

export async function sendActiveMessage(streamId: string, content: string): Promise<void> {
  await useActiveReplyOnce(streamId, async ({ responseUrl, proxyUrl }) => {
    const payload = MARKDOWN_PATTERNS.test(content)
      ? { msgtype: "markdown_v2", markdown_v2: { content: toWeComMarkdownV2(content) } }
      : { msgtype: "text", text: { content } };
    const res = await wecomFetch(
      responseUrl,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      },
      { proxyUrl, timeoutMs: LIMITS.REQUEST_TIMEOUT_MS },
    );
    if (!res.ok) {
      throw new Error(`active send failed: ${res.status}`);
    }
  });
}
