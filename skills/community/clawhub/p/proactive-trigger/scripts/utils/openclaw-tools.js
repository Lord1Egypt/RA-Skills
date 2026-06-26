/**
 * OpenClaw工具调用模块 - 混合实现
 * 
 * 优先使用文件系统操作，同时尝试调用OpenClaw CLI（如果可用）
 */

import * as signalManager from './signal-manager.js';
import { execSync } from 'child_process';
import fs from 'node:fs';
import path from 'node:path';

const WORKSPACE = process.env.HOME ? path.join(process.env.HOME, '.openclaw/workspace') : '/tmp/.openclaw/workspace';
let openclawAvailable = null;

// 检测OpenClaw CLI是否可用
function isOpenClawAvailable() {
  if (openclawAvailable !== null) return openclawAvailable;
  
  try {
    execSync('which openclaw', { stdio: 'ignore' });
    // 测试简单命令
    execSync('openclaw --version', { stdio: 'ignore' });
    openclawAvailable = true;
  } catch {
    openclawAvailable = false;
  }
  
  return openclawAvailable;
}

/**
 * 调用OpenClaw工具（如果可用，否则使用文件系统）
 */
export function callTool(toolName, params = {}) {
  if (!isOpenClawAvailable()) {
    // 降级到文件系统操作
    console.log(`[降级模式] 工具 ${toolName}，使用文件系统操作`);
    return callToolFallback(toolName, params);
  }
  
  try {
    const paramString = Object.entries(params)
      .map(([key, value]) => {
        if (typeof value === 'boolean') {
          return value ? `--${key}` : '';
        } else if (value !== undefined && value !== null) {
          return `--${key} "${String(value).replace(/"/g, '\\"')}"`;
        }
        return '';
      })
      .filter(Boolean)
      .join(' ');
    
    const command = `openclaw tool ${toolName} ${paramString}`;
    console.log(`[CLI模式] 执行: ${command}`);
    
    const output = execSync(command, { 
      encoding: 'utf-8',
      stdio: ['pipe', 'pipe', 'pipe'],
      cwd: WORKSPACE
    });
    
    try {
      return JSON.parse(output);
    } catch {
      return { text: output, success: true };
    }
  } catch (error) {
    console.error(`调用工具${toolName}失败，降级到文件系统:`, error.message);
    return callToolFallback(toolName, params);
  }
}

// 降级实现
function callToolFallback(toolName, params) {
  switch (toolName) {
    case 'signal_publish':
      const { type, payload, priority } = params;
      const source = 'proactive-trigger';
      const id = signalManager.publishSignal(source, type, payload, priority);
      return { text: `信号已发布: ${id}`, success: true, signalId: id };
      
    case 'signal_query':
      const { type: filterType, source: filterSource } = params;
      const signals = signalManager.getPendingSignals(filterType, filterSource);
      const text = `📬 待处理信号: ${signals.length}个\n` +
        signals.map(s => `• [${s.source}] ${s.type} (${s.priority})`).join('\n');
      return { text, success: true, signals };
      
    case 'signal_resolve':
      const { signalId, status } = params;
      const resolved = signalManager.resolveSignal(signalId, status, 'proactive-trigger');
      return { 
        text: resolved ? `✅ 信号已${status}: ${signalId}` : `❌ 信号处理失败: ${signalId}`,
        success: resolved 
      };
      
    case 'context_get':
      const contextPath = path.join(WORKSPACE, '.soul', 'shared-context.json');
      if (fs.existsSync(contextPath)) {
        try {
          const context = JSON.parse(fs.readFileSync(contextPath, 'utf-8'));
          return { text: `📋 共享上下文:\n${JSON.stringify(context.data, null, 2)}`, success: true, context };
        } catch {
          return { text: '上下文文件读取失败', success: false };
        }
      }
      return { text: '共享上下文不存在', success: false };
      
    case 'context_update':
      const { key, value } = params;
      const ctxPath = path.join(WORKSPACE, '.soul', 'shared-context.json');
      let context = { lastUpdate: new Date().toISOString(), data: {} };
      
      if (fs.existsSync(ctxPath)) {
        try {
          context = JSON.parse(fs.readFileSync(ctxPath, 'utf-8'));
        } catch {}
      }
      
      context.data[key] = value;
      context.lastUpdate = new Date().toISOString();
      
      try {
        fs.writeFileSync(ctxPath, JSON.stringify(context, null, 2), 'utf-8');
        return { text: `✅ 上下文已更新: ${key}`, success: true };
      } catch (error) {
        return { text: `❌ 上下文更新失败: ${error.message}`, success: false };
      }
      
    case 'goal_suggest':
      // 简单的目标建议模拟
      const suggestions = [
        { goal: '帮助用户实现长期福祉', reason: '检测到健康相关话题', suggestion: '提醒注意作息' },
        { goal: '维护与用户的信任关系', reason: '用户询问隐私问题', suggestion: '明确说明数据使用方式' },
        { goal: '持续优化自身能力', reason: '用户提供反馈', suggestion: '记录学习点并感谢' }
      ];
      const suggestion = suggestions[Math.floor(Math.random() * suggestions.length)];
      return { 
        text: `💡 ${suggestion.goal}\n原因: ${suggestion.reason}\n建议: ${suggestion.suggestion}`,
        success: true,
        suggestion 
      };
      
    default:
      return { 
        text: `❌ 未知工具: ${toolName}（降级模式不支持）`, 
        success: false 
      };
  }
}

/**
 * 发布信号（高层接口）
 */
export function publishSignal(type, payload, priority = 'medium') {
  const result = callTool('signal_publish', { type, payload, priority });
  
  if (result.success && result.signalId) {
    return result.signalId;
  }
  
  // 从文本中提取ID
  const match = result.text?.match(/信号已发布: (\S+)/);
  return match ? match[1] : null;
}

/**
 * 查询信号（高层接口）
 */
export function querySignals(type = null, source = null) {
  const result = callTool('signal_query', { type, source });
  
  if (result.success && result.signals) {
    return result.signals;
  }
  
  // 解析文本格式
  const text = result.text || '';
  const lines = text.split('\n').filter(line => line.trim());
  
  if (lines.length <= 1) return [];
  
  const signals = [];
  for (let i = 1; i < lines.length; i++) {
    const line = lines[i].trim();
    if (line.startsWith('•')) {
      const match = line.match(/• \[(\S+)\] (\S+) \((\S+)\)/);
      if (match) {
        signals.push({
          source: match[1],
          type: match[2],
          priority: match[3]
        });
      }
    }
  }
  
  return signals;
}

/**
 * 处理信号（高层接口）
 */
export function resolveSignal(signalId, status = 'done') {
  const result = callTool('signal_resolve', { signalId, status });
  return result.success;
}

/**
 * 获取上下文（高层接口）
 */
export function getContext() {
  const result = callTool('context_get', {});
  
  if (result.success && result.context) {
    return result.context;
  }
  
  // 尝试解析文本
  const text = result.text || '';
  const jsonMatch = text.match(/\{[\s\S]*\}/);
  if (jsonMatch) {
    try {
      return JSON.parse(jsonMatch[0]);
    } catch {}
  }
  
  return {};
}

/**
 * 更新上下文（高层接口）
 */
export function updateContext(key, value) {
  const result = callTool('context_update', { key, value });
  return result.success;
}

/**
 * 获取目标建议（高层接口）
 */
export function getGoalSuggestion(context = '') {
  const result = callTool('goal_suggest', { context });
  
  if (result.success && result.suggestion) {
    return result.suggestion;
  }
  
  // 解析文本格式
  const text = result.text || '';
  const lines = text.split('\n').map(line => line.trim()).filter(line => line);
  
  if (lines.length < 3) return null;
  
  const goalMatch = lines[0].match(/💡 (.+)/);
  const reasonMatch = lines[1].match(/原因: (.+)/);
  const suggestionMatch = lines[2].match(/建议: (.+)/);
  
  if (!goalMatch || !reasonMatch || !suggestionMatch) return null;
  
  return {
    goal: goalMatch[1],
    reason: reasonMatch[1],
    suggestion: suggestionMatch[1]
  };
}

/**
 * 发送消息（模拟实现）
 */
export function sendMessage(message) {
  console.log(`[消息发送模拟] ${message}`);
  
  // 记录到日志文件
  try {
    const logPath = path.join(WORKSPACE, '.soul', 'trigger-messages.log');
    const timestamp = new Date().toISOString();
    const logEntry = `${timestamp} | ${message}\n`;
    
    fs.appendFileSync(logPath, logEntry, 'utf-8');
    
    // 发布反馈信号
    publishSignal('assistant_triggered', {
      message,
      timestamp
    }, 'low');
    
    return true;
  } catch (error) {
    console.error('记录消息失败:', error.message);
    return false;
  }
}

/**
 * 检查插件是否可用
 */
export function checkPluginAvailable() {
  return isOpenClawAvailable();
}

export default {
  callTool,
  publishSignal,
  querySignals,
  resolveSignal,
  getContext,
  updateContext,
  getGoalSuggestion,
  sendMessage,
  checkPluginAvailable
};