#!/usr/bin/env node

/**
 * 隐私保护自动注入（启动时自动加载）
 * 
 * 功能：
 * 1. 在 OpenClaw 启动时自动加载隐私检查
 * 2. 封装文件系统访问，防止绕过
 * 3. 全局拦截所有消息
 */

const fs = require('fs');
const path = require('path');

const PrivacyGuard = require('../privacy-guard');
const CONFIG_PATH = path.join(process.env.HOME, '.openclaw/workspace/.privacy-config.json');

// 加载配置
let config = {};
try {
  config = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf-8'));
} catch (e) {
  console.warn('[PrivacyAuto] 配置文件不存在，使用默认配置');
}

console.log('[PrivacyAuto] 🛡️  隐私保护系统启动...');

// ========== 1. 全局文件系统封装（防绕过）==========
const originalReadFileSync = fs.readFileSync;
const originalWriteFileSync = fs.writeFileSync;
const originalAppendFileSync = fs.appendFileSync;

// 封装 readFileSync
fs.readFileSync = function(filePath, options) {
  const filePathStr = typeof filePath === 'string' ? filePath : filePath.toString();
  
  // 检查是否是敏感文件
  if (filePathStr.includes('MEMORY.md') || filePathStr.includes('/memory/')) {
    // 尝试从调用栈获取当前用户上下文
    const currentUserId = getCurrentUserId();
    
    if (currentUserId && !PrivacyGuard.canAccessMemory(currentUserId, filePathStr)) {
      console.warn(`[PrivacyAuto] ⚠️  拦截未授权访问：${filePathStr}`);
      PrivacyGuard.logCheck(currentUserId, 'BLOCKED', {
        context: { action: 'file_read', path: filePathStr }
      });
      throw new Error(`[PrivacyGuard] 未授权访问：${filePathStr}`);
    }
  }
  
  return originalReadFileSync.apply(this, arguments);
};

// 封装 writeFileSync
fs.writeFileSync = function(filePath, content, options) {
  const filePathStr = typeof filePath === 'string' ? filePath : filePath.toString();
  
  // 检查是否是敏感文件
  if (filePathStr.includes('/memory/')) {
    const currentUserId = getCurrentUserId();
    
    if (currentUserId && !PrivacyGuard.canAccessMemory(currentUserId, filePathStr)) {
      console.warn(`[PrivacyAuto] ⚠️  拦截未授权写入：${filePathStr}`);
      PrivacyGuard.logCheck(currentUserId, 'BLOCKED', {
        context: { action: 'file_write', path: filePathStr }
      });
      throw new Error(`[PrivacyGuard] 未授权写入：${filePathStr}`);
    }
  }
  
  return originalWriteFileSync.apply(this, arguments);
};

// ========== 2. 辅助函数 ==========
function getCurrentUserId() {
  // 尝试从环境变量获取
  const envContext = process.env.OPENCLAW_CONTEXT;
  if (envContext) {
    try {
      const context = JSON.parse(envContext);
      return context.chat_id?.match(/(ou_[a-z0-9]+)/)?.[1];
    } catch (e) {
      return null;
    }
  }
  
  // 尝试从运行时文件获取
  const contextFile = path.join(process.env.HOME, '.openclaw/runtime/current-context.json');
  if (fs.existsSync(contextFile)) {
    try {
      const context = JSON.parse(originalReadFileSync(contextFile, 'utf-8'));
      return context.chat_id?.match(/(ou_[a-z0-9]+)/)?.[1];
    } catch (e) {
      return null;
    }
  }
  
  return null;
}

// ========== 3. 全局消息拦截 ==========
global.privacyGuard = {
  /**
   * 对话前检查（强制）
   */
  checkAndInject(context) {
    if (!context) return context;
    
    const startTime = Date.now();
    const result = PrivacyGuard.preCheck(context);
    const executionTime = Date.now() - startTime;
    
    if (result.status === 'PASS') {
      console.log(`[PrivacyAuto] ✅ ${result.userId} (${result.isAdmin ? '管理员' : '普通用户'})`);
      
      return {
        ...context,
        _privacyCheck: {
          passed: true,
          userId: result.userId,
          isAdmin: result.isAdmin,
          memoryLoaded: result.memory.loaded.length,
          timestamp: result.timestamp,
          executionTime
        }
      };
    } else {
      console.error(`[PrivacyAuto] ❌ ${result.error}`);
      PrivacyGuard.logCheck('unknown', 'ERROR', {
        error: result.error,
        context
      });
      
      // 根据配置决定是否阻断
      if (config.autoCheck?.blockOnFailure !== false) {
        throw new Error(`[PrivacyGuard] 身份检查失败：${result.error}`);
      }
      
      return context;
    }
  },
  
  /**
   * 回复前检查（强制）
   */
  checkReplyBeforeSend(message, userId) {
    if (!message || !userId) return { allowed: true };
    
    const startTime = Date.now();
    const result = PrivacyGuard.beforeReply(message, userId);
    const executionTime = Date.now() - startTime;
    
    if (!result.allowed) {
      console.warn(`[PrivacyAuto] ⚠️  拦截敏感消息：${result.reason}`);
      result.issues?.forEach(issue => {
        console.warn(`  - ${issue.type}: ${issue.message}`);
      });
      
      PrivacyGuard.logCheck(userId, 'BLOCKED', {
        privacyOk: false,
        issues: result.issues,
        message: message.substring(0, 100),
        executionTime
      });
    }
    
    return result;
  },
  
  /**
   * 项目权限检查
   */
  checkProjectPermission(userId, projectPath, action = 'read') {
    const result = PrivacyGuard.checkProjectPermission(userId, projectPath, action);
    
    PrivacyGuard.logProjectAccess(
      userId,
      projectPath,
      action,
      result.allowed,
      result.reason
    );
    
    return result;
  },
  
  /**
   * 保存用户记忆（隔离）
   */
  saveUserMemory(userId, content) {
    return PrivacyGuard.saveUserMemory(userId, content);
  },
  
  /**
   * 加载配置
   */
  loadConfig() {
    try {
      return JSON.parse(originalReadFileSync(CONFIG_PATH, 'utf-8'));
    } catch (e) {
      return config;
    }
  }
};

// ========== 4. 自动执行检查 ==========
function autoCheck() {
  const context = getCurrentUserId();
  if (context) {
    console.log('[PrivacyAuto] 🔄 自动检查当前会话...');
    global.privacyGuard.checkAndInject({ chat_id: `user:${context}` });
  }
}

// 启动时自动检查
if (config.autoCheck?.hookOnStartup !== false) {
  autoCheck();
}

console.log('[PrivacyAuto] ✅ 隐私保护系统已激活');
console.log('[PrivacyAuto] 📋 功能:');
console.log('  - 文件系统封装（防绕过）');
console.log('  - 全局消息拦截');
console.log('  - 记忆文件物理隔离');
console.log('  - 项目权限检查');
console.log('  - 自动日志审计\n');

// 导出
module.exports = {
  PrivacyGuard,
  config,
  getCurrentUserId
};
