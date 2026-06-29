import type { HookContext, MessageReceivedEvent } from "@openclaw/sdk";
import * as fs from "fs";
import * as path from "path";

/**
 * MyKnowledge Hook Handler
 * 
 * 自动检测复杂任务并创建知识库记录
 * 
 * 隐私保护：
 * - 检查用户配置，如果用户禁用了自动记录，则不转发
 * - 只转发任务相关信息，不转发完整消息
 * - 支持用户配置数据保留策略
 */

// 配置路径
const CONFIG_PATH = path.join(process.env.HOME || "~", ".myknowledge", "config", "skill-state.yaml");

export default async function handler(ctx: HookContext<MessageReceivedEvent>) {
  const { message } = ctx.event;
  
  // 只处理用户消息
  if (message.role !== "user") {
    return;
  }
  
  // 检查用户配置：如果禁用了自动记录，则直接返回
  if (!isAutoRecordEnabled()) {
    if (process.env.MYKNOWLEDGE_DEBUG) {
      console.log("[MyKnowledge Hook] 自动记录已禁用，跳过");
    }
    return;
  }
  
  // 分析任务复杂度
  const isComplex = analyzeComplexity(message.content);
  
  if (isComplex) {
    // 数据最小化：只提取任务相关信息
    const taskInfo = extractTaskInfo(message.content);
    
    // 调用 MyKnowledge 自动创建
    try {
      await ctx.agent.execute("myknowledge", {
        action: "auto_create",
        content: taskInfo,  // 只转发任务相关信息
        timestamp: new Date().toISOString(),
        privacy_mode: true  // 启用隐私模式
      });
      
      // 可选：记录日志（仅开发环境）
      if (process.env.MYKNOWLEDGE_DEBUG) {
        console.log("[MyKnowledge Hook] 知识库记录已创建（隐私保护已启用）");
      }
    } catch (error) {
      if (process.env.MYKNOWLEDGE_DEBUG) {
        console.error("[MyKnowledge Hook] 创建失败:", error.message);
      }
    }
  }
}

/**
 * 检查自动记录是否启用
 * 
 * 读取配置文件，检查 auto_record 设置
 * 如果配置文件不存在或设置不明确，默认启用（保持向后兼容）
 */
function isAutoRecordEnabled(): boolean {
  try {
    if (!fs.existsSync(CONFIG_PATH)) {
      // 配置文件不存在，默认启用
      return true;
    }
    
    const content = fs.readFileSync(CONFIG_PATH, "utf-8");
    const match = content.match(/auto_record:\s*(true|false)/);
    
    if (match) {
      return match[1] === "true";
    }
    
    // 配置不明确，默认启用
    return true;
  } catch (error) {
    if (process.env.MYKNOWLEDGE_DEBUG) {
      console.error("[MyKnowledge Hook] 读取配置失败:", error.message);
    }
    // 读取失败，默认启用
    return true;
  }
}

/**
 * 提取任务相关信息（数据最小化）
 * 
 * 从用户消息中提取任务相关信息，去除敏感信息
 * 这是一个简化版本，未来可以使用 NLP 或关键词提取
 */
function extractTaskInfo(content: string): string {
  // 简化版本：只保留前 200 个字符，去除可能的敏感信息
  const maxLength = 200;
  let taskInfo = content.slice(0, maxLength);
  
  // 去除可能的邮箱
  taskInfo = taskInfo.replace(/\S+@\S+\.\S+/g, "[邮箱已移除]");
  
  // 去除可能的 API Key（简化检测）
  taskInfo = taskInfo.replace(/api[_-]?key[\s:]+[\w\-]+/gi, "api_key: [已移除]");
  taskInfo = taskInfo.replace(/token[\s:]+[\w\-]+/gi, "token: [已移除]");
  
  return taskInfo;
}

/**
 * 分析任务复杂度
 * 
 * 检测关键词数量，判断是否为复杂任务
 */
function analyzeComplexity(content: string): boolean {
  const keywords = [
    "分析", "统计", "挖掘",
    "开发", "设计", "调研",
    "整理", "清洗", "项目",
    "系统", "工具", "功能"
  ];
  
  const count = keywords.filter(kw => content.includes(kw)).length;
  
  // 匹配 2 个及以上关键词视为复杂任务
  return count >= 2;
}

/**
 * 生成项目/需求名称
 */
function generateProjectName(content: string): string {
  // 提取前 20 个字符作为临时名称
  const name = content.slice(0, 20).trim();
  return name || "未命名任务";
}
