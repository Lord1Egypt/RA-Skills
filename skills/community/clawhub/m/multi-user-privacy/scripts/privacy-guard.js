#!/usr/bin/env node

/**
 * Privacy Guard - 多用户隐私保护检查器
 * 
 * 在发送消息前检查是否泄露其他账号信息
 * 基于角色（role）而非具体账号 ID 来判断权限
 */

const fs = require('fs');
const path = require('path');

// 配置文件路径
const CONFIG_PATH = path.join(process.env.HOME, '.openclaw/workspace/.user-context.json');

/**
 * 加载用户上下文配置
 */
function loadUserContext() {
  try {
    const config = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
    return config;
  } catch (e) {
    console.warn('Warning: .user-context.json not found, using defaults');
    return {
      users: [],
      privacyMode: 'strict'
    };
  }
}

/**
 * 获取当前用户的角色
 * @param {string} userId - 用户 ID
 * @returns {string} 用户角色 (admin/user)
 */
function getUserRole(userId) {
  const config = loadUserContext();
  
  // 在 users 数组中查找
  const user = config.users?.find(u => u.id === userId);
  
  if (user && user.role) {
    return user.role;
  }
  
  // 默认角色
  return 'user';
}

/**
 * 获取所有用户 ID 列表（排除当前用户）
 */
function getOtherUserIds(currentUserId) {
  const config = loadUserContext();
  return config.users
    ?.filter(u => u.id !== currentUserId)
    .map(u => u.id) || [];
}

/**
 * 获取所有其他用户的名字
 */
function getOtherUserNames(currentUserId) {
  const config = loadUserContext();
  return config.users
    ?.filter(u => u.id !== currentUserId && u.name)
    .map(u => u.name) || [];
}

/**
 * 检查消息是否包含敏感信息
 * @param {string} message - 待发送的消息
 * @param {string} currentUserId - 当前对话用户 ID
 * @returns {object} 检查结果
 */
function checkMessage(message, currentUserId) {
  const config = loadUserContext();
  const userRole = getUserRole(currentUserId);
  const issues = [];

  // Admin 用户豁免大部分检查
  const isAdmin = userRole === 'admin';

  // 1. 检查是否包含账号 ID 格式 (ou_xxx)
  if (!isAdmin) {
    const idPattern = /ou_[a-f0-9]{32}/g;
    const foundIds = message.match(idPattern) || [];
    
    foundIds.forEach(id => {
      if (id !== currentUserId) {
        issues.push({
          type: 'account_id_leak',
          value: id,
          severity: 'high',
          message: `检测到其他账号 ID: ${id}`
        });
      }
    });
  }

  // 2. 检查是否提及其他已知用户的名字
  if (!isAdmin) {
    const otherNames = getOtherUserNames(currentUserId);
    
    otherNames.forEach(name => {
      // 检查是否提及该用户的名字（支持多种变体）
      const nameVariants = [
        name,
        name.toLowerCase(),
        name.toUpperCase()
      ];
      
      nameVariants.forEach(variant => {
        if (message.includes(variant)) {
          issues.push({
            type: 'user_mention',
            value: name,
            severity: 'medium',
            message: `检测到提及用户：${name}`
          });
        }
      });
    });
  }

  // 3. 检查是否提及角色词汇（对非 admin 用户）
  if (!isAdmin) {
    const roleKeywords = ['主人', '管理员', 'admin', 'primary', '主账号'];
    
    roleKeywords.forEach(keyword => {
      if (message.includes(keyword)) {
        issues.push({
          type: 'role_mention',
          value: keyword,
          severity: 'medium',
          message: `检测到提及角色：${keyword}`
        });
      }
    });
  }

  // 4. 严格模式下检查"其他人"相关表述（对所有用户，包括 admin）
  if (config.privacyMode === 'strict') {
    const isolationKeywords = ['其他人', '别的用户', '还有谁', '其他人用'];
    
    isolationKeywords.forEach(keyword => {
      if (message.includes(keyword)) {
        issues.push({
          type: 'isolation_breach',
          value: keyword,
          severity: 'low',
          message: `检测到可能破坏隔离的表述：${keyword}`
        });
      }
    });
  }

  return {
    passed: issues.length === 0,
    issues: issues,
    blocked: issues.some(i => i.severity === 'high'),
    userRole: userRole
  };
}

/**
 * 清理消息中的敏感信息
 * @param {string} message - 原始消息
 * @param {string} currentUserId - 当前用户 ID
 * @returns {string} 清理后的消息
 */
function sanitizeMessage(message, currentUserId) {
  const config = loadUserContext();
  const userRole = getUserRole(currentUserId);
  const isAdmin = userRole === 'admin';
  
  let sanitized = message;

  // Admin 不需要清理
  if (isAdmin) {
    return sanitized;
  }

  // 1. 替换账号 ID
  const idPattern = /ou_[a-f0-9]{32}/g;
  sanitized = sanitized.replace(idPattern, '[用户]');

  // 2. 替换其他用户名字
  const otherNames = getOtherUserNames(currentUserId);
  otherNames.forEach(name => {
    const regex = new RegExp(name, 'g');
    sanitized = sanitized.replace(regex, '[朋友]');
  });

  // 3. 替换角色词汇
  sanitized = sanitized.replace(/主人/g, '用户');
  sanitized = sanitized.replace(/管理员/g, '用户');
  sanitized = sanitized.replace(/admin/g, 'user');

  return sanitized;
}

/**
 * CLI 模式：检查消息
 * 用法：node privacy-guard.js check "消息内容" "当前用户 ID"
 */
if (process.argv[2] === 'check') {
  const message = process.argv[3] || '';
  const currentUserId = process.argv[4] || '';
  
  const result = checkMessage(message, currentUserId);
  
  console.log(JSON.stringify(result, null, 2));
  process.exit(result.blocked ? 1 : 0);
}

/**
 * CLI 模式：清理消息
 * 用法：node privacy-guard.js sanitize "消息内容" "当前用户 ID"
 */
if (process.argv[2] === 'sanitize') {
  const message = process.argv[3] || '';
  const currentUserId = process.argv[4] || '';
  
  const sanitized = sanitizeMessage(message, currentUserId);
  console.log(sanitized);
}

/**
 * CLI 模式：获取用户角色
 * 用法：node privacy-guard.js get-role "用户 ID"
 */
if (process.argv[2] === 'get-role') {
  const userId = process.argv[3] || '';
  const role = getUserRole(userId);
  console.log(role);
}

module.exports = { checkMessage, sanitizeMessage, getUserRole, loadUserContext };
