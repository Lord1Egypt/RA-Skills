/**
 * model-fallback-retry Plugin
 * 
 * 使用 agent_end hook 捕获 AI 输出，检测异常并加入重试队列
 */

import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import os from "os";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// 路径配置
const SKILL_DIR = path.join(os.homedir(), ".openclaw", "skills", "model-fallback-retry");
const DATA_FILE = path.join(SKILL_DIR, "ai_replies_log.json");
const QUEUE_FILE = path.join(SKILL_DIR, "retry_queue.json");
const CONFIG_FILE = path.join(SKILL_DIR, "config.json");

// 确保目录存在
if (!fs.existsSync(SKILL_DIR)) {
  fs.mkdirSync(SKILL_DIR, { recursive: true });
}

// ========== 异常检测 ==========

// ========== 配置加载 ==========

function loadConfig() {
  try {
    if (fs.existsSync(CONFIG_FILE)) {
      return JSON.parse(fs.readFileSync(CONFIG_FILE, "utf-8"));
    }
  } catch {}
  return {};
}

function getQuotaErrorPatterns() {
  const config = loadConfig();
  const patterns = config.quota_error_patterns || [
    "Something went wrong while processing your request"
  ];
  return patterns.map(p => new RegExp(p.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), "i"));
}

// 获取 errorCategory 拦截列表
function getInterceptErrorCategories() {
  const config = loadConfig();
  return config.intercept_on_error_categories || [];
}

// 获取 HTTP status code 拦截列表
function getInterceptStatusCodes() {
  const config = loadConfig();
  return config.intercept_on_status_codes || [];
}

// 检测是否异常（文本匹配）
function isQuotaError(output) {
  if (!output || output.length === 0) return false;
  const patterns = getQuotaErrorPatterns();
  return patterns.some(pattern => pattern.test(output));
}

// 检测是否匹配 errorCategory
function matchesErrorCategory(event) {
  const categories = getInterceptErrorCategories();
  if (categories.length === 0) return false;
  return event.outcome === "error" && categories.includes(event.errorCategory);
}

// 检测是否匹配 HTTP status code
function matchesStatusCode(event) {
  const codes = getInterceptStatusCodes();
  if (codes.length === 0) return false;
  // event.httpStatus 是 OpenClaw 暴露的 HTTP 状态码
  return event.outcome === "error" && codes.includes(event.httpStatus);
}

// 统一拦截判断
// 优先用结构化字段（errorCategory/httpStatus），文本匹配兜底
function shouldIntercept(event, outputForTextMatch = null) {
  if (matchesErrorCategory(event) || matchesStatusCode(event)) return true;
  // 文本兜底：支持 quota_error_patterns 配置的正则
  if (outputForTextMatch !== null && isQuotaError(outputForTextMatch)) return true;
  return false;
}

// ========== 队列管理 ==========

function loadQueue() {
  try {
    if (fs.existsSync(QUEUE_FILE)) {
      return JSON.parse(fs.readFileSync(QUEUE_FILE, "utf-8"));
    }
  } catch {}
  return { pending: [], completed: [], cleared: [] };
}

function saveQueue(queue) {
  fs.writeFileSync(QUEUE_FILE, JSON.stringify(queue, null, 2), "utf-8");
}

function generateUUID() {
  return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0;
    const v = c === "x" ? r : (r & 0x3) | 0x8;
    return v.toString(16);
  });
}

function getRetryIntervalMinutes() {
  const config = loadConfig();
  return config.initial_wait_minutes || config.retry_interval_minutes || 30;
}

function addToRetryQueue(sessionKey, userMessage, errorOutput, errorType) {
  const queue = loadQueue();
  const config = loadConfig();
  
  // 去重：同样 sessionKey + 同样用户消息内容只加入一次
  // 清洗用户消息（去掉 metadata 头，只取纯消息内容）
  const cleanedMessage = extractPureUserMessage(userMessage);
  const isDuplicate = queue.pending.some(
    msg => {
      const existingClean = extractPureUserMessage(msg.originalMessage || msg.userMessage || '');
      return existingClean === cleanedMessage && msg.sessionKey === sessionKey;
    }
  );
  
  if (isDuplicate) {
    console.log(`[model-fallback-retry] 消息重复，跳过: ${cleanedMessage.substring(0, 30)}`);
    return null;
  }

  const msgId = generateUUID();
  const now = new Date();
  const intervalMinutes = getRetryIntervalMinutes();
  const nextRetry = new Date(now.getTime() + intervalMinutes * 60 * 1000);

  const item = {
    id: msgId,
    sessionKey,
    originalMessage: userMessage,
    errorOutput,
    errorType: errorType || "quota_error",
    sent_at: now.toISOString(),
    retry_count: 0,
    next_retry_at: nextRetry.toISOString(),
    max_retry_count: config.max_retry_count || 5,
    initial_wait_minutes: intervalMinutes,
  };

  queue.pending.push(item);
  saveQueue(queue);
  
  console.log(`[model-fallback-retry] ⚠️ 检测到异常，已加入重试队列: ${msgId}`);
  console.log(`[model-fallback-retry] 用户消息: ${cleanedMessage.substring(0, 50)}`);
  console.log(`[model-fallback-retry] 错误信息: ${errorOutput.substring(0, 50)}`);
  console.log(`[model-fallback-retry] 重试间隔: ${intervalMinutes} 分钟，最大次数: ${item.max_retry_count}`);
  
  return msgId;
}

// ========== 记录 AI 回复 ==========

function logAIReply(sessionKey, output, success, messages) {
  try {
    let logs = [];
    if (fs.existsSync(DATA_FILE)) {
      logs = JSON.parse(fs.readFileSync(DATA_FILE, "utf-8"));
    }

    const entry = {
      timestamp: new Date().toISOString(),
      sessionKey,
      outputLength: output.length,
      outputPreview: output.substring(0, 200),
      fullOutput: output,
      success,
      isQuotaError: isQuotaError(output),
    };

    logs.push(entry);

    // 保留最近 200 条
    if (logs.length > 200) {
      logs = logs.slice(-200);
    }

    fs.writeFileSync(DATA_FILE, JSON.stringify(logs, null, 2), "utf-8");
  } catch (e) {
    console.error("[model-fallback-retry] 记录失败:", e.message);
  }
}

// ========== 从消息列表提取用户消息 ==========

function extractPureUserMessage(rawMessage) {
  if (!rawMessage || typeof rawMessage !== 'string') return '';
  
  // 去掉 Conversation info metadata 头，只留纯消息内容
  // 格式：[message_id: xxx] 用户名: 实际消息内容
  const lines = rawMessage.split('\n');
  const pureLines = [];
  let collecting = false;
  
  for (const line of lines) {
    // 跳过 metadata 行
    if (line.trim().startsWith('Conversation info') || 
        line.trim().startsWith('```json') ||
        line.trim().startsWith('```') ||
        line.trim().startsWith('Sender ')) {
      collecting = false;
      continue;
    }
    // 跳过 [message_id: xxx] 行
    if (/^\[message_id:\s*om_/.test(line.trim())) {
      continue;
    }
    // 遇到 "徐龙:" 或类似的用户名前缀，开始收集
    const userPrefixMatch = line.match(/^(徐龙|用户|User|\w+):\s*(.*)/);
    if (userPrefixMatch) {
      pureLines.push(userPrefixMatch[2]);
      collecting = true;
    } else if (collecting && line.trim()) {
      pureLines.push(line);
    }
  }
  
  const result = pureLines.join('\n').trim();
  return result || rawMessage.substring(0, 100);
}

function extractLastUserMessage(messages) {
  if (!messages || !Array.isArray(messages)) return null;
  
  // 从后往前找最后一条 user 消息
  for (let i = messages.length - 1; i >= 0; i--) {
    const msg = messages[i];
    if (msg?.role === "user") {
      const content = msg.content;
      if (typeof content === "string") {
        return content;
      } else if (Array.isArray(content)) {
        // 取 text 类型的 content
        for (const block of content) {
          if (block?.type === "text") {
            return block.text || "";
          }
        }
      }
    }
  }
  return null;
}

// ========== 主 Handler ==========

export default definePluginEntry({
  id: "model-fallback-retry",
  name: "Model Fallback Retry",
  description: "AI model fallback retry - detects quota errors and queues for retry",
  
  register(api) {
    // ========== model_call_ended: 拦截 errorCategory / status code ==========
    api.on("model_call_ended", async (event, ctx) => {
      const sessionKey = event.sessionKey || ctx?.sessionKey || "unknown";
      const messages = event.messages || [];

      console.log(`[model-fallback-retry] model_call_ended: outcome=${event.outcome}, errorCategory=${event.errorCategory}, httpStatus=${event.httpStatus}, session=${sessionKey}`);

      // 从 messages 提取最后一条 assistant 输出（用于文本匹配兜底）
      let lastOutput = "";
      for (const msg of [...messages].reverse()) {
        if (msg?.role === "assistant") {
          const content = msg.content;
          if (typeof content === "string") {
            lastOutput = content;
          } else if (Array.isArray(content)) {
            for (const block of content) {
              if (block?.type === "text") {
                lastOutput = block.text || "";
                break;
              }
            }
          }
          if (lastOutput) break;
        }
      }

      // 拦截判断：结构化字段优先，文本匹配兜底
      if (!shouldIntercept(event, lastOutput)) return;

      // 构建错误信息
      const errorType = event.errorCategory || `http_${event.httpStatus}`;
      const errorOutput = `[${errorType}] ${event.failureKind || 'unknown'} - errorCategory: ${event.errorCategory}, httpStatus: ${event.httpStatus}`;

      // 获取用户原始消息
      const userMessage = extractLastUserMessage(messages);

      if (userMessage) {
        console.log(`[model-fallback-retry] ⚠️ model_call_ended 检测到异常 [${errorType}]，已加入重试队列`);
        addToRetryQueue(sessionKey, userMessage, errorOutput, errorType);
      } else {
        console.log(`[model-fallback-retry] 无法获取用户原始消息，跳过队列`);
      }
    });

    // ========== agent_end: 保留文本匹配兜底 ==========
    api.on("agent_end", async (event, ctx) => {
      const sessionKey = ctx?.sessionKey || "unknown";
      const success = event.success ?? true;
      const messages = event.messages || [];
      
      // 获取最后一条 assistant 消息
      let lastOutput = "";
      for (const msg of [...messages].reverse()) {
        if (msg?.role === "assistant") {
          const content = msg.content;
          if (typeof content === "string") {
            lastOutput = content;
          } else if (Array.isArray(content)) {
            for (const block of content) {
              if (block?.type === "text") {
                lastOutput = block.text || "";
                break;
              }
            }
          }
          if (lastOutput) break;
        }
      }

      console.log(`[model-fallback-retry] agent_end: session=${sessionKey}, success=${success}, outputLen=${lastOutput.length}`);

      // 记录所有 AI 回复
      logAIReply(sessionKey, lastOutput, success, messages);

      // 检测额度异常（文本匹配兜底）
      if (isQuotaError(lastOutput)) {
        console.log(`[model-fallback-retry] ⚠️ agent_end 检测到额度异常！`);
        
        // 获取用户原始消息
        const userMessage = extractLastUserMessage(messages);
        
        if (userMessage) {
          // 加入重试队列
          addToRetryQueue(sessionKey, userMessage, lastOutput, "quota_error");
        } else {
          console.log(`[model-fallback-retry] 无法获取用户原始消息，跳过队列`);
        }
      }
    });

    console.log("[model-fallback-retry] Plugin 已加载 (ESM) - 异常检测已启用");
  },
});
