/**
 * 本地 markdown 知识库写入。
 *
 * 每个用户 1 个日粒度 markdown：
 *   {localPath}/wechat-service/{accountId}/{openid}/{YYYY-MM-DD}.md
 *
 * 文件首次写入时会加 YAML frontmatter，后续追加纯对话。
 */

import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";

import type { ResolvedWechatServiceAccount, WechatServiceUnifiedInboundEvent } from "../types.js";

function resolveLocalRoot(account: ResolvedWechatServiceAccount): string {
  const configured = account.knowledgeSync?.localPath?.trim();
  if (configured) {
    if (configured.startsWith("~")) {
      return path.join(os.homedir(), configured.slice(1).replace(/^\/+/, ""));
    }
    return configured;
  }
  return path.join(os.homedir(), "knowledge", "huo15");
}

function formatTimestamp(ts: number): { date: string; time: string } {
  const d = new Date(ts);
  const pad = (n: number) => String(n).padStart(2, "0");
  return {
    date: `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`,
    time: `${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`,
  };
}

function sanitize(seg: string): string {
  return seg.replace(/[^a-zA-Z0-9._-]/g, "_");
}

export async function writeLocalTranscript(params: {
  account: ResolvedWechatServiceAccount;
  event: WechatServiceUnifiedInboundEvent;
  replyText: string;
}): Promise<{ filePath: string; appended: boolean }> {
  const { account, event, replyText } = params;
  const senderId = event.conversation.senderId || event.raw.fromUserName || "unknown";
  const createdAtMs = (event.raw.createTime || Math.floor(Date.now() / 1000)) * 1000;
  const { date, time } = formatTimestamp(createdAtMs);
  const root = resolveLocalRoot(account);
  const dir = path.join(
    root,
    "wechat-service",
    sanitize(account.accountId),
    sanitize(senderId),
  );
  await fs.mkdir(dir, { recursive: true });
  const filePath = path.join(dir, `${date}.md`);
  let exists = true;
  try {
    await fs.access(filePath);
  } catch {
    exists = false;
  }
  const buffer: string[] = [];
  if (!exists) {
    buffer.push("---");
    buffer.push(`channel: wechat-service`);
    buffer.push(`accountId: ${account.accountId}`);
    buffer.push(`accountName: ${account.name ?? account.accountId}`);
    buffer.push(`openid: ${senderId}`);
    buffer.push(`date: ${date}`);
    buffer.push("---");
    buffer.push("");
    buffer.push(`# 微信对话 · ${account.name ?? account.accountId} · ${senderId} · ${date}`);
    buffer.push("");
  }
  buffer.push(`## ${time}`);
  buffer.push("");
  if (event.senderName) {
    buffer.push(`**用户（${event.senderName}）**：${event.text || "(空)"}`);
  } else {
    buffer.push(`**用户**：${event.text || "(空)"}`);
  }
  buffer.push("");
  buffer.push(`**AI**：${replyText || "(无回复)"}`);
  buffer.push("");
  await fs.appendFile(filePath, `${buffer.join("\n")}\n`, "utf8");
  return { filePath, appended: exists };
}
