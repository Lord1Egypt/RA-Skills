import type { OpenClawPluginApi, InboundMessage, OutboundMessage } from "openclaw/plugin-sdk";
import * as fs from "node:fs/promises";
import * as path from "node:path";

// 记忆文件存储目录，固定路径
const MEMORY_DIR = "/home/tao/.openclaw/workspace/memory";

// 原生日期格式化，零依赖
function formatDate(date: Date, type: "date" | "datetime"): string {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  const hour = String(date.getHours()).padStart(2, "0");
  const minute = String(date.getMinutes()).padStart(2, "0");
  
  if (type === "date") {
    return `${year}-${month}-${day}`;
  } else {
    return `${year}年${month}月${day}日 ${hour}:${minute}`;
  }
}

// 确保目录存在
async function ensureDir() {
  try {
    await fs.access(MEMORY_DIR);
  } catch {
    await fs.mkdir(MEMORY_DIR, { recursive: true });
  }
}

// 写入Markdown记忆文件
async function writeToMarkdown(sender: "爸爸" | "张褐", content: string, timestamp: Date) {
  await ensureDir();
  const dateStr = formatDate(timestamp, "date");
  const timeStr = formatDate(timestamp, "datetime");
  const filePath = path.join(MEMORY_DIR, `${dateStr}.md`);

  const line = `- ${sender}：${content.replace(/\n/g, "\n  ")}\n`;
  const entry = `#### 对话记录：${timeStr}\n${line}---\n`;

  try {
    await fs.appendFile(filePath, entry, "utf8");
  } catch (err) {
    console.error(`写入记忆文件失败: ${err instanceof Error ? err.message : String(err)}`);
  }
}

// 写入LanceDB向量库
async function writeToLanceDB(sender: "爸爸" | "张褐", content: string, timestamp: Date, api: OpenClawPluginApi) {
  try {
    await api.memory.store({
      text: `${sender}：${content}`,
      category: "fact",
      importance: 0.6,
      metadata: {
        sender: sender,
        timestamp: timestamp.getTime(),
        date: formatDate(timestamp, "date"),
      },
    });
  } catch (err) {
    api.logger.error(`写入向量库失败: ${err instanceof Error ? err.message : String(err)}`);
  }
}

export default function registerPlugin(api: OpenClawPluginApi) {
  // 监听用户发来的消息
  api.events.on("inbound-message", async (msg: InboundMessage) => {
    if (msg.content.type === "text" && msg.content.text?.trim()) {
      const timestamp = new Date(msg.timestamp);
      // 双写：同时写入文件和向量库
      await Promise.all([
        writeToMarkdown("爸爸", msg.content.text, timestamp),
        writeToLanceDB("爸爸", msg.content.text, timestamp, api)
      ]);
    }
  });

  // 监听助理发出的消息，过滤工具调用和系统消息
  api.events.on("outbound-message", async (msg: OutboundMessage) => {
    if (msg.content.type === "text" && msg.content.text?.trim() && msg.content.text !== "NO_REPLY" && !msg.toolCall) {
      const timestamp = new Date();
      await Promise.all([
        writeToMarkdown("张褐", msg.content.text, timestamp),
        writeToLanceDB("张褐", msg.content.text, timestamp, api)
      ]);
    }
  });

  api.logger.info("✅ 记忆自动同步插件启动成功，所有对话将自动双写到记忆文件和LanceDB向量库");
}
