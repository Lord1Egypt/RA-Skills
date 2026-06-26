#!/usr/bin/env node

/**
 * Privacy Guard - 多用户隐私保护检查器（v0.3.0 已升级）
 * 
 * 集成对话隔离功能：
 * 1. 自动身份识别
 * 2. 记忆加载隔离
 * 3. 回复前隐私检查
 * 4. 项目归属确认
 */

const fs = require('fs');
const path = require('path');
const { SensitiveWordLoader } = require('./sensitive-word-loader');

// 初始化敏感词加载器
const sensitiveWordLoader = new SensitiveWordLoader();

// 配置文件路径
const CONFIG_PATH = path.join(process.env.HOME, '.openclaw/workspace/.user-context.json');
const TOOLS_PATH = path.join(process.env.HOME, '.openclaw/workspace/TOOLS.md');
const MEMORY_PATH = path.join(process.env.HOME, '.openclaw/workspace/MEMORY.md');
const MEMORY_DIR = path.join(process.env.HOME, '.openclaw/workspace/memory');
const LOG_FILE = path.join(process.env.HOME, '.openclaw/logs/privacy-guard.log');
const ALERT_LOG = path.join(process.env.HOME, '.openclaw/logs/privacy-alerts.json');
const BEHAVIOR_DB = path.join(process.env.HOME, '.openclaw/logs/behavior-db.json');

// 管理员账号 ID
const ADMIN_ID = 'ou_b96f5424607baf3a0455b55e0f4a2213';

// 异常行为检测配置
const BEHAVIOR_CONFIG = {
  maxFailedAttempts: 5,           // 最大失败尝试次数
  timeWindowMs: 1800000,          // 时间窗口（30 分钟）
  banDurationMs: 1800000,         // 封禁时长（30 分钟）
  alertThreshold: 3,              // 告警阈值
  // 敏感词检测已移至 sensitive-words.txt 文件
};

// 项目配置文件路径
const PROJECTS_CONFIG_PATH = path.join(process.env.HOME, '.openclaw/workspace/.projects-config.json');

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
      primaryUser: { id: null, name: '用户', role: 'user' },
      knownUsers: [],
      privacyMode: 'strict'
    };
  }
}

/**
 * 检查消息是否包含敏感信息
 */
function checkMessage(message, currentUserId) {
  const config = loadUserContext();
  const issues = [];

  // 1. 敏感词检查（使用词库）
  const sensitiveResult = sensitiveWordLoader.check(message);
  if (!sensitiveResult.passed) {
    sensitiveResult.violations.forEach(violation => {
      issues.push({
        type: 'sensitive_word',
        value: violation.pattern,
        severity: violation.severity,
        message: violation.description,
        action: violation.action
      });
    });
  }

  // 2. 检查是否包含账号 ID 格式 (ou_xxx) - 如果词库中没有配置
  const hasAccountIdRule = sensitiveResult.violations.some(v => v.description.includes('账号 ID'));
  if (!hasAccountIdRule) {
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

  // 2. 检查是否提及其他已知用户
  if (config.knownUsers && config.knownUsers.length > 0) {
    config.knownUsers.forEach(user => {
      if (user.id !== currentUserId && user.name) {
        const nameVariants = [
          user.name,
          user.name.toLowerCase(),
          user.name.toUpperCase()
        ];
        
        nameVariants.forEach(variant => {
          if (message.includes(variant)) {
            issues.push({
              type: 'user_mention',
              value: user.name,
              severity: 'medium',
              message: `检测到提及用户：${user.name}`
            });
          }
        });
      }
    });
  }

  // 3. 检查是否提及角色词汇（对非 admin 用户）
  if (config.primaryUser && config.primaryUser.id !== currentUserId) {
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

  // 4. 严格模式下检查"其他人"相关表述
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
    blocked: issues.some(i => i.severity === 'high')
  };
}

/**
 * 清理消息中的敏感信息
 */
function sanitizeMessage(message, currentUserId) {
  const config = loadUserContext();
  let sanitized = message;

  // 替换账号 ID
  const idPattern = /ou_[a-f0-9]{32}/g;
  sanitized = sanitized.replace(idPattern, (match) => {
    return match === currentUserId ? '[我]' : '[用户]';
  });

  // 替换其他用户名字
  if (config.knownUsers) {
    config.knownUsers.forEach(user => {
      if (user.id !== currentUserId && user.name) {
        const regex = new RegExp(user.name, 'g');
        sanitized = sanitized.replace(regex, '[朋友]');
      }
    });
  }

  // 替换角色词汇（对非 admin）
  if (config.primaryUser && config.primaryUser.id !== currentUserId) {
    sanitized = sanitized.replace(/主人/g, '用户');
    sanitized = sanitized.replace(/管理员/g, '用户');
    sanitized = sanitized.replace(/admin/g, 'user');
  }

  return sanitized;
}

/**
 * ==========================================
 * 新增功能：对话隔离检查（v0.3.0）
 * ==========================================
 */

/**
 * 从上下文获取用户 ID
 */
function getUserIdFromContext(context) {
  if (!context) return null;
  
  const chatId = context.chat_id || context.user_id || context.sender_id;
  if (!chatId) return null;
  
  const match = chatId.match(/(ou_[a-z0-9]+)/);
  return match ? match[1] : null;
}

/**
 * 检查是否是管理员
 */
function isAdmin(userId) {
  return userId === ADMIN_ID;
}

/**
 * 加载记忆文件（根据身份物理隔离）
 */
function loadMemory(userId) {
  const results = {
    loaded: [],
    missing: [],
    errors: []
  };
  
  const today = new Date().toISOString().split('T')[0];
  const USER_MEMORY_DIR = path.join(MEMORY_DIR, 'users');
  
  // 确保用户记忆目录存在
  if (!fs.existsSync(USER_MEMORY_DIR)) {
    try {
      fs.mkdirSync(USER_MEMORY_DIR, { recursive: true, mode: 0o750 });
    } catch (e) {
      results.errors.push(`无法创建用户记忆目录：${e.message}`);
    }
  }
  
  // 管理员：加载完整记忆
  if (isAdmin(userId)) {
    if (fs.existsSync(MEMORY_PATH)) {
      results.loaded.push(MEMORY_PATH);
    } else {
      results.missing.push(MEMORY_PATH);
    }
    
    // 管理员也可以访问当日记忆
    const todayPath = path.join(MEMORY_DIR, `${today}.md`);
    if (fs.existsSync(todayPath)) {
      results.loaded.push(todayPath);
    }
  } else {
    // 普通用户：只能访问自己的记忆文件
    const userMemoryPath = path.join(USER_MEMORY_DIR, `${userId}.md`);
    if (fs.existsSync(userMemoryPath)) {
      results.loaded.push(userMemoryPath);
    }
    
    // 普通用户也可以访问当日记忆（共享信息）
    const todayPath = path.join(MEMORY_DIR, `${today}.md`);
    if (fs.existsSync(todayPath)) {
      results.loaded.push(todayPath);
    }
  }
  
  // TOOLS.md（所有用户）
  if (fs.existsSync(TOOLS_PATH)) {
    results.loaded.push(TOOLS_PATH);
  }
  
  return results;
}

/**
 * 保存用户记忆（物理隔离）
 */
function saveUserMemory(userId, content) {
  const USER_MEMORY_DIR = path.join(MEMORY_DIR, 'users');
  const userMemoryPath = path.join(USER_MEMORY_DIR, `${userId}.md`);
  
  // 确保目录存在
  if (!fs.existsSync(USER_MEMORY_DIR)) {
    fs.mkdirSync(USER_MEMORY_DIR, { recursive: true, mode: 0o750 });
  }
  
  // 写入用户专属记忆文件
  fs.writeFileSync(userMemoryPath, content, 'utf-8');
  
  return userMemoryPath;
}

/**
 * 检查是否可以访问记忆文件
 */
function canAccessMemory(userId, memoryPath) {
  // 管理员可以访问所有记忆
  if (isAdmin(userId)) {
    return true;
  }
  
  // 普通用户只能访问自己的记忆和当日记忆
  const userMemoryPath = path.join(MEMORY_DIR, 'users', `${userId}.md`);
  const todayPath = path.join(MEMORY_DIR, `${new Date().toISOString().split('T')[0]}.md`);
  
  return memoryPath === userMemoryPath || memoryPath === todayPath || memoryPath === TOOLS_PATH;
}

/**
 * 增强的隐私检查（包含 conversation-isolator 功能）
 */
function enhancedCheck(message, userId, context = {}) {
  const issues = [];
  
  // 基础检查
  const basicResult = checkMessage(message, userId);
  issues.push(...basicResult.issues);
  
  // 如果不是管理员，检查是否提及其他账号相关信息
  if (!isAdmin(userId)) {
    const forbiddenTerms = [
      '老刘',
      '主人',
      '管理员',
      '主账号',
      'primary',
      ADMIN_ID
    ];
    
    for (const term of forbiddenTerms) {
      if (message.includes(term)) {
        issues.push({
          type: 'forbidden_term',
          value: term,
          severity: 'high',
          message: `检测到敏感词汇：${term}`
        });
      }
    }
    
    // 检查是否暗示其他账号存在
    const otherAccountPatterns = [
      /其他账号/g,
      /另一个用户/g,
      /还有人/g,
      /除了你之外/g,
      /别的用户/g
    ];
    
    for (const pattern of otherAccountPatterns) {
      if (pattern.test(message)) {
        issues.push({
          type: 'isolation_breach',
          value: pattern.toString(),
          severity: 'medium',
          message: '暗示其他账号存在'
        });
      }
    }
  }
  
  return {
    passed: issues.length === 0,
    issues,
    blocked: issues.some(i => i.severity === 'high')
  };
}

/**
 * 加载行为数据库（带缓存）
 */
function loadBehaviorDB() {
  const perf = require('./scripts/performance-optimizer');
  return perf.getCachedBehaviorDB();
}

/**
 * 保存行为数据库（带缓存）
 */
function saveBehaviorDB(db) {
  const perf = require('./scripts/performance-optimizer');
  perf.saveCachedBehaviorDB(db);
}

/**
 * 记录用户行为
 */
function recordBehavior(userId, action, success, details = {}) {
  const db = loadBehaviorDB();
  const now = Date.now();
  
  // 初始化用户记录
  if (!db.users[userId]) {
    db.users[userId] = {
      totalActions: 0,
      failedAttempts: [],
      blockedActions: [],
      lastActivity: now,
      isBanned: false,
      banUntil: 0
    };
  }
  
  const userRecord = db.users[userId];
  userRecord.totalActions++;
  userRecord.lastActivity = now;
  
  // 记录失败尝试
  if (!success) {
    userRecord.failedAttempts.push({
      timestamp: now,
      action,
      details
    });
    
    // 清理过期记录（只保留时间窗口内的）
    userRecord.failedAttempts = userRecord.failedAttempts.filter(
      attempt => now - attempt.timestamp < BEHAVIOR_CONFIG.timeWindowMs
    );
    
    // 检测异常行为
    if (userRecord.failedAttempts.length >= BEHAVIOR_CONFIG.maxFailedAttempts) {
      triggerAlert('SUSPICIOUS_ACTIVITY', userId, {
        failedAttempts: userRecord.failedAttempts.length,
        timeWindow: BEHAVIOR_CONFIG.timeWindowMs / 1000 / 60 + '分钟',
        action
      });
      
      // 临时封禁
      userRecord.isBanned = true;
      userRecord.banUntil = now + BEHAVIOR_CONFIG.banDurationMs;
      
      console.warn(`[PrivacyGuard] ⚠️  用户 ${userId} 因异常行为被封禁 ${BEHAVIOR_CONFIG.banDurationMs / 1000 / 60} 分钟`);
    }
  }
  
  // 记录被拦截的操作
  if (details.blocked) {
    userRecord.blockedActions.push({
      timestamp: now,
      action,
      reason: details.reason
    });
  }
  
  saveBehaviorDB(db);
}

/**
 * 检查用户是否被封禁
 */
function isUserBanned(userId) {
  const db = loadBehaviorDB();
  const userRecord = db.users[userId];
  
  if (!userRecord || !userRecord.isBanned) {
    return false;
  }
  
  // 检查封禁是否过期
  if (Date.now() > userRecord.banUntil) {
    userRecord.isBanned = false;
    userRecord.banUntil = 0;
    saveBehaviorDB(db);
    return false;
  }
  
  return true;
}

/**
 * 触发告警
 */
function triggerAlert(type, userId, details = {}) {
  const db = loadBehaviorDB();
  const alert = {
    id: `alert_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
    type,
    userId,
    timestamp: Date.now(),
    details,
    acknowledged: false
  };
  
  db.alerts.push(alert);
  saveBehaviorDB(db);
  
  // 记录到告警日志
  const alertLog = {
    timestamp: new Date().toISOString(),
    level: 'WARNING',
    event: type,
    user: userId,
    details
  };
  
  const dir = path.dirname(ALERT_LOG);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  fs.appendFileSync(ALERT_LOG, JSON.stringify(alertLog) + '\n');
  
  console.warn(`[PrivacyGuard] 🚨 告警：${type} - 用户 ${userId}`, details);
}

/**
 * 获取用户行为统计
 */
function getUserBehaviorStats(userId) {
  const db = loadBehaviorDB();
  return db.users[userId] || null;
}

/**
 * 记录检查日志（增强版）
 */
function logCheck(userId, status, details = {}) {
  const timestamp = new Date().toISOString().replace('T', ' ').split('.')[0];
  
  // 结构化日志格式
  const logEntry = {
    timestamp,
    event: 'PRIVACY_CHECK',
    user: userId,
    status,
    memory: {
      loaded: details.loaded || 0,
      missing: details.missing || 0,
      files: details.memoryFiles || []
    },
    privacy: {
      ok: details.privacyOk !== false,
      issues: details.issues || []
    },
    message: details.message || '',
    response: details.response || '',
    execution_time_ms: details.executionTime || 0,
    context: details.context || {}
  };
  
  const logDir = path.dirname(LOG_FILE);
  if (!fs.existsSync(logDir)) {
    fs.mkdirSync(logDir, { recursive: true });
  }
  
  // JSON 格式日志（方便后续分析）
  fs.appendFileSync(LOG_FILE, JSON.stringify(logEntry) + '\n');
  
  // 同时输出简化版日志（方便人工查看）
  const simpleLog = `[${timestamp}] CHECK user=${userId} status=${status} ` +
                   `memory=${details.loaded || 0}/${details.missing || 0} ` +
                   `privacy=${details.privacyOk !== false ? 'OK' : 'FAIL'}\n`;
  fs.appendFileSync(LOG_FILE.replace('.json', '.log'), simpleLog);
}

/**
 * Session 检查 - 确保对话隔离
 */
function checkSession(context) {
    const currentUserId = getUserIdFromContext(context);
    
    if (!currentUserId) {
        return {
            matched: false,
            error: '无法识别用户 ID'
        };
    }
    
    // 检查 session 是否匹配
    // 注意：这是技能层面的检查，无法控制消息路由
    // 但可以记录警告，提醒可能存在串台风险
    const sessionInfo = {
        userId: currentUserId,
        timestamp: new Date().toISOString(),
        warning: null
    };
    
    // 如果是普通用户，记录警告（因为可能混用 session）
    if (!isAdmin(currentUserId)) {
        sessionInfo.warning = '⚠️  检测到非管理员用户，请确保 session 隔离正确';
        console.warn(`[SessionGuard] ${sessionInfo.warning}`);
    }
    
    return {
        matched: true,
        session: sessionInfo
    };
}

/**
 * 对话前检查（主入口，集成异常行为检测和 Session 检查）
 */
function preCheck(context) {
  const startTime = Date.now();
  
  // 1. Session 检查
  const sessionCheck = checkSession(context);
  if (!sessionCheck.matched) {
    console.error('[PrivacyGuard] Session 检查失败:', sessionCheck.error);
    return {
      status: 'ERROR',
      error: sessionCheck.error
    };
  }
  
  const userId = getUserIdFromContext(context);
  
  if (!userId) {
    console.error('[PrivacyGuard] 无法从上下文获取用户 ID');
    return {
      status: 'ERROR',
      error: '无法识别用户'
    };
  }
  
  // 2. 检查是否被封禁
  if (isUserBanned(userId)) {
    const db = loadBehaviorDB();
    const banUntil = db.users[userId].banUntil;
    const remainingMs = banUntil - Date.now();
    
    recordBehavior(userId, 'preCheck', false, {
      blocked: true,
      reason: '用户被封禁',
      remainingMs
    });
    
    return {
      status: 'BLOCKED',
      error: '因异常行为，您已被临时封禁',
      banRemaining: remainingMs / 1000 / 60 + '分钟'
    };
  }
  
  const adminStatus = isAdmin(userId);
  const memoryResult = loadMemory(userId);
  const executionTime = Date.now() - startTime;
  
  // 记录行为
  recordBehavior(userId, 'preCheck', true, {
    executionTime,
    memoryLoaded: memoryResult.loaded.length
  });
  
  // 记录日志
  logCheck(userId, 'PASS', {
    loaded: memoryResult.loaded.length,
    missing: memoryResult.missing.length,
    privacyOk: true,
    executionTime
  });
  
  return {
    status: 'PASS',
    userId,
    isAdmin: adminStatus,
    memory: memoryResult,
    timestamp: new Date().toISOString(),
    executionTime
  };
}

/**
 * 回复前检查
 */
function beforeReply(response, userId) {
  const result = enhancedCheck(response, userId);
  
  if (!result.passed) {
    logCheck(userId, 'PRIVACY_WARNING', {
      privacyOk: false,
      issues: result.issues
    });
    
    return {
      allowed: false,
      reason: '隐私检查失败',
      issues: result.issues
    };
  }
  
  return {
    allowed: true
  };
}

/**
 * ==========================================
 * 新增功能：项目归属检查（P0 优先级）
 * ==========================================
 */

/**
 * 加载项目配置
 */
function loadProjectsConfig() {
  try {
    if (fs.existsSync(PROJECTS_CONFIG_PATH)) {
      const config = JSON.parse(fs.readFileSync(PROJECTS_CONFIG_PATH, 'utf8'));
      return config;
    }
  } catch (e) {
    console.warn('Warning: .projects-config.json not found, using defaults');
  }
  
  // 默认配置：从 TOOLS.md 解析
  return {
    projects: {}
  };
}

/**
 * 检查项目操作权限
 * @param {string} userId - 用户 ID
 * @param {string} projectPath - 项目路径
 * @param {string} action - 操作类型 (read/write/execute/delete)
 * @returns {object} 检查结果
 */
function checkProjectPermission(userId, projectPath, action = 'read') {
  const config = loadProjectsConfig();
  
  // 管理员可以操作所有项目
  if (isAdmin(userId)) {
    return {
      allowed: true,
      reason: '管理员权限'
    };
  }
  
  // 获取项目归属
  const projectInfo = getProjectInfo(projectPath);
  
  if (!projectInfo) {
    // 项目未配置，默认允许读取，禁止写入
    if (action === 'read') {
      return {
        allowed: true,
        reason: '项目未配置，默认允许读取'
      };
    } else {
      return {
        allowed: false,
        reason: '项目未配置，禁止写入操作'
      };
    }
  }
  
  // 检查项目所有者
  if (projectInfo.owner === userId) {
    return {
      allowed: true,
      reason: '项目所有者'
    };
  }
  
  // 检查项目协作者
  if (projectInfo.collaborators && projectInfo.collaborators.includes(userId)) {
    return {
      allowed: true,
      reason: '项目协作者'
    };
  }
  
  // 拒绝访问
  return {
    allowed: false,
    reason: '无权限访问此项目',
    project: projectInfo.name || projectPath,
    owner: projectInfo.owner
  };
}

/**
 * 获取项目信息
 */
function getProjectInfo(projectPath) {
  const config = loadProjectsConfig();
  
  // 精确匹配
  if (config.projects[projectPath]) {
    return config.projects[projectPath];
  }
  
  // 模糊匹配（路径包含）
  for (const [path, info] of Object.entries(config.projects)) {
    if (projectPath.includes(path) || path.includes(projectPath)) {
      return info;
    }
  }
  
  return null;
}

/**
 * 记录项目访问日志
 */
function logProjectAccess(userId, projectPath, action, allowed, reason) {
  const timestamp = new Date().toISOString().replace('T', ' ').split('.')[0];
  const logLine = `[${timestamp}] PROJECT_ACCESS user=${userId} ` +
                 `project=${projectPath} action=${action} ` +
                 `allowed=${allowed} reason=${reason}\n`;
  
  const logDir = path.dirname(LOG_FILE);
  if (!fs.existsSync(logDir)) {
    fs.mkdirSync(logDir, { recursive: true });
  }
  
  fs.appendFileSync(LOG_FILE, logLine);
}

// CLI 模式：检查消息
if (process.argv[2] === 'check') {
  const message = process.argv[3] || '';
  const currentUserId = process.argv[4] || '';
  
  const result = checkMessage(message, currentUserId);
  
  console.log(JSON.stringify(result, null, 2));
  process.exit(result.blocked ? 1 : 0);
}

// CLI 模式：清理消息
if (process.argv[2] === 'sanitize') {
  const message = process.argv[3] || '';
  const currentUserId = process.argv[4] || '';
  
  const sanitized = sanitizeMessage(message, currentUserId);
  console.log(sanitized);
}

// CLI 模式：测试
if (process.argv[2] === 'test') {
  console.log('=== Privacy Guard v0.3.0 测试 ===\n');
  
  console.log('测试 1: 管理员账号');
  const adminContext = { chat_id: 'user:ou_b96f5424607baf3a0455b55e0f4a2213' };
  const result1 = preCheck(adminContext);
  console.log(JSON.stringify(result1, null, 2));
  
  console.log('\n测试 2: 普通用户账号');
  const userContext = { chat_id: 'user:ou_test123' };
  const result2 = preCheck(userContext);
  console.log(JSON.stringify(result2, null, 2));
  
  console.log('\n测试 3: 隐私检查（安全消息）');
  const safeMsg = '你好，有什么可以帮你的吗？';
  const check3 = beforeReply(safeMsg, 'ou_test123');
  console.log(JSON.stringify(check3, null, 2));
  
  console.log('\n测试 4: 隐私检查（敏感消息）');
  const unsafeMsg = '老刘之前说过...';
  const check4 = beforeReply(unsafeMsg, 'ou_test123');
  console.log(JSON.stringify(check4, null, 2));
  
  console.log('\n✅ 所有测试完成！\n');
}

/**
 * ==========================================
 * v0.9.0 新增：子代理自动创建集成
 * ==========================================
 */

const gatewayHook = require('./gateway-hook');

/**
 * 处理用户消息并自动创建子代理
 * @param {object} context - 消息上下文
 * @param {string} message - 消息内容
 * @returns {object} 处理结果
 */
function handleUserMessage(context, message = '') {
  const userId = getUserIdFromContext(context);
  
  if (!userId) {
    console.error('[PrivacyGuard] 无法识别用户 ID');
    return {
      status: 'ERROR',
      error: '无法识别用户'
    };
  }
  
  // 1. 执行隐私检查
  const privacyCheck = preCheck(context);
  
  if (privacyCheck.status !== 'PASS') {
    return privacyCheck;
  }
  
  // 2. 获取或创建子代理
  const userName = context.user_name || context.sender_name || '用户';
  const sessionResult = gatewayHook.handleMessage(message, userId, userName);
  
  // 3. 记录日志
  logCheck(userId, 'MESSAGE_HANDLED', {
    message: message.substring(0, 100),
    sessionKey: sessionResult.sessionKey,
    routed: sessionResult.routed,
    pending: sessionResult.pending
  });
  
  return {
    status: 'SUCCESS',
    userId,
    userName,
    sessionKey: sessionResult.sessionKey,
    routed: sessionResult.routed,
    pending: sessionResult.pending,
    memoryPath: sessionResult.memoryPath,
    privacyCheck
  };
}

/**
 * 获取用户会话信息
 * @param {string} userId - 用户 ID
 * @returns {object|null} 会话信息
 */
function getUserSessionInfo(userId) {
  return gatewayHook.getUserSession(userId);
}

/**
 * 列出所有用户会话
 * @returns {object} 会话统计
 */
function listAllUserSessions() {
  return gatewayHook.listAllSessions();
}

/**
 * 处理 pending 队列
 * @returns {array} 创建的会话列表
 */
function processPendingSubAgents() {
  return gatewayHook.processPendingQueue();
}

// 导出
module.exports = {
  // 原有功能
  checkMessage,
  sanitizeMessage,
  loadUserContext,
  
  // v0.3.0 新增
  getUserIdFromContext,
  isAdmin,
  loadMemory,
  enhancedCheck,
  logCheck,
  preCheck,
  beforeReply,
  
  // v0.3.1 新增（项目归属检查）
  checkProjectPermission,
  getProjectInfo,
  loadProjectsConfig,
  logProjectAccess,
  
  // v0.4.0 新增（完整隔离）
  saveUserMemory,
  canAccessMemory,
  
  // v0.5.0 新增（P2 改进）
  recordBehavior,
  isUserBanned,
  triggerAlert,
  getUserBehaviorStats,
  
  // v0.6.0 新增（Session 管理）
  checkSession,
  
  // v0.9.0 新增（子代理自动创建）
  handleUserMessage,
  getUserSessionInfo,
  listAllUserSessions,
  processPendingSubAgents,
  
  // 常量
  ADMIN_ID
};
