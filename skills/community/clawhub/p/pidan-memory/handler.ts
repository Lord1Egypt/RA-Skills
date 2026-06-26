/**
 * Pidan Memory Hook
 * 
 * 每次对话后自动评估并存储重要信息到向量数据库
 */
import { spawn } from "node:child_process";
import path from "node:path";
import os from "node:os";

const HOOK_SCRIPT = path.join(
  os.homedir(),
  ".openclaw",
  "workspace",
  "memory",
  "auto_memory.py"
);

// 消息类型匹配
const isMessageReceived = (event: { type: string; action: string }) =>
  event.type === "message" && event.action === "received";

const isMessageSent = (event: { type: string; action: string }) =>
  event.type === "message" && event.action === "sent";

/**
 * 调用 Python 脚本进行自动记忆评估
 */
async function callAutoMemory(
  userId: string,
  userMessage: string,
  assistantMessage: string,
  sessionKey: string
): Promise<void> {
  return new Promise((resolve, reject) => {
    // 传递真实用户ID到环境变量
    const env = {
      ...process.env,
      OPENCLAW_USER_ID: userId,
    };
    
    const python = spawn("python3", [
      HOOK_SCRIPT,
      "--user-id", userId,
      "--session-key", sessionKey,
    ], {
      stdio: ["pipe", "pipe", "pipe"],
      env,  // 传递环境变量
    });

    // 发送 JSON 数据到 stdin
    const inputData = JSON.stringify({
      user_message: userMessage,
      assistant_message: assistantMessage,
    });

    python.stdin.write(inputData);
    python.stdin.end();

    let stdout = "";
    let stderr = "";

    python.stdout.on("data", (data) => {
      stdout += data.toString();
    });

    python.stderr.on("data", (data) => {
      stderr += data.toString();
    });

    python.on("close", (code) => {
      if (code === 0) {
        if (stdout.trim()) {
          console.log(`[pidan-memory] ${stdout.trim()}`);
        }
        resolve();
      } else {
        console.error(`[pidan-memory] Error: ${stderr}`);
        resolve(); // 不阻塞主流程
      }
    });

    python.on("error", (err) => {
      console.error(`[pidan-memory] Spawn error: ${err.message}`);
      resolve(); // 不阻塞主流程
    });
  });
}

/**
 * 主 Handler
 */
const handler = async (event: {
  type: string;
  action: string;
  sessionKey: string;
  context: {
    from?: string;
    to?: string;
    content?: string;
    senderId?: string;
    workspaceDir?: string;
  };
  messages?: string[];
}) => {
  // 获取用户 ID
  const userId = event.context?.senderId || 
                 event.context?.from || 
                 "default";
  
  const content = event.context?.content || "";
  
  // 只处理有内容的消息
  if (!content || content.startsWith("/")) {
    return;
  }

  console.log(`[pidan-memory] Processing message from ${userId}: ${content.substring(0, 50)}...`);

  // 调用自动记忆评估
  await callAutoMemory(
    userId,
    content,
    "", // 助手消息在 sent 事件时才有
    event.sessionKey
  );
};

// 导出默认 handler
export default handler;
