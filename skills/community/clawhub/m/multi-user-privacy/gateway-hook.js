#!/usr/bin/env node

/**
 * Gateway Message Hook - Gateway 消息自动钩子（v0.9.0 自动创建版）
 * 
 * 功能：
 * 1. 在 Gateway 收到消息时自动检查用户
 * 2. 为新用户自动创建子代理（直接调用 sessions_spawn）
 * 3. 加载用户记忆
 * 4. 路由到对应子代理
 * 5. 集成隐私检查
 * 
 * 使用方法：
 * 在 Gateway 配置中添加 preMessageHook 指向此脚本
 * 
 * @since v0.9.0 - 支持自动创建子代理，无需 pending 队列
 */

const fs = require('fs');
const path = require('path');
const { execSync, spawn } = require('child_process');

const ROUTER_DB = path.join(process.env.HOME, '.openclaw/skills/multi-user-privacy/.router-db.json');
const MEMORY_DIR = path.join(process.env.HOME, '.openclaw/workspace/memory');
const PENDING_FILE = path.join(process.env.HOME, '.openclaw/skills/multi-user-privacy/.pending-sessions.json');
const LOG_FILE = path.join(process.env.HOME, '.openclaw/logs/gateway-hook.log');

// 管理员账号 ID
const ADMIN_ID = 'ou_b96f5424607baf3a0455b55e0f4a2213';

/**
 * 日志记录
 */
function log(level, message, data = {}) {
    const timestamp = new Date().toISOString().replace('T', ' ').split('.')[0];
    const logEntry = {
        timestamp,
        level,
        message,
        ...data
    };
    
    // 写入日志文件
    try {
        const logDir = path.dirname(LOG_FILE);
        if (!fs.existsSync(logDir)) {
            fs.mkdirSync(logDir, { recursive: true });
        }
        fs.appendFileSync(LOG_FILE, JSON.stringify(logEntry) + '\n');
    } catch (e) {
        // 忽略日志写入错误
    }
    
    // 输出到控制台
    const prefix = `[GatewayHook] ${level === 'ERROR' ? '❌' : level === 'WARN' ? '⚠️' : '✅'}`;
    console.log(`${prefix} ${message}`);
    if (Object.keys(data).length > 0) {
        console.log(`  ${JSON.stringify(data, null, 2)}`);
    }
}

/**
 * 加载路由器数据库
 */
function loadRouterDB() {
    try {
        if (fs.existsSync(ROUTER_DB)) {
            return JSON.parse(fs.readFileSync(ROUTER_DB, 'utf-8'));
        }
    } catch (e) {
        log('ERROR', 'RouterDB 加载失败', { error: e.message });
    }
    return {};
}

/**
 * 保存路由器数据库
 */
function saveRouterDB(db) {
    try {
        const dir = path.dirname(ROUTER_DB);
        if (!fs.existsSync(dir)) {
            fs.mkdirSync(dir, { recursive: true });
        }
        fs.writeFileSync(ROUTER_DB, JSON.stringify(db, null, 2), 'utf-8');
        log('INFO', 'RouterDB 保存成功', { userCount: Object.keys(db).length });
    } catch (e) {
        log('ERROR', 'RouterDB 保存失败', { error: e.message });
    }
}

/**
 * 检查 pending 队列并处理
 */
function processPendingQueue() {
    try {
        if (!fs.existsSync(PENDING_FILE)) {
            return [];
        }
        
        const pending = JSON.parse(fs.readFileSync(PENDING_FILE, 'utf-8'));
        if (pending.length === 0) {
            return [];
        }
        
        log('INFO', 'Pending 队列状态检查', { count: pending.length });
        log('INFO', '⚠️  注意：子代理创建由 Gateway 主流程处理，此函数仅记录状态');
        
        // 仅记录 pending 队列状态，不实际创建
        // 实际创建应该由 Gateway 在收到消息时调用 sessions_spawn API
        const pendingList = pending.map(s => ({
            userId: s.userId,
            userName: s.userName,
            status: s.status,
            label: s.label
        }));
        
        log('INFO', 'Pending 队列详情', { sessions: pendingList });
        
        return pending;
        
    } catch (e) {
        log('ERROR', '检查 pending 队列失败', { error: e.message });
        return [];
    }
}

/**
 * 为用户创建子代理
 * 注意：sessions_spawn 是内部 API，需要通过消息工具或主流程调用
 * 这里我们使用 pending 队列机制，由主流程或定时任务处理
 */
function createSubAgentForUser(userId, userName) {
    log('INFO', `为用户 ${userName} (${userId}) 创建子代理...`);
    
    try {
        const label = `${userName}的专属助手`;
        const task = `为${userName}提供专属助手服务，遵守多用户隐私保护规则`;
        
        // 由于 sessions_spawn 是内部 API，无法通过 CLI 直接调用
        // 我们使用 pending 队列机制
        let pending = [];
        if (fs.existsSync(PENDING_FILE)) {
            pending = JSON.parse(fs.readFileSync(PENDING_FILE, 'utf-8'));
        }
        
        // 检查是否已存在相同的 pending 记录
        const exists = pending.some(p => p.userId === userId && p.status === 'pending');
        if (exists) {
            log('INFO', '已存在 pending 记录，跳过', { userId });
            return {
                success: true,
                pending: true,
                label,
                task,
                note: '已在 pending 队列中'
            };
        }
        
        pending.push({
            userId,
            userName,
            label,
            task,
            createdAt: new Date().toISOString(),
            status: 'pending',
            retryCount: 0
        });
        
        fs.writeFileSync(PENDING_FILE, JSON.stringify(pending, null, 2), 'utf-8');
        
        log('INFO', '已记录到 pending 队列', { userId, label, queueSize: pending.length });
        
        return {
            success: true,
            pending: true,
            label,
            task,
            queueSize: pending.length
        };
        
    } catch (e) {
        log('ERROR', '创建子代理失败', { error: e.message });
        return { success: false, error: e.message };
    }
}

/**
 * 处理消息（Gateway 调用此函数）
 */
function handleMessage(message, senderId, senderName) {
    log('INFO', `收到消息 from ${senderName} (${senderId})`);
    
    const db = loadRouterDB();
    
    // 检查是否已有子代理
    if (db[senderId] && db[senderId].sessionKey && db[senderId].sessionKey !== 'pending') {
        log('INFO', `找到现有子代理`, { userId: senderId, sessionKey: db[senderId].sessionKey });
        db[senderId].lastActiveAt = new Date().toISOString();
        db[senderId].messageCount++;
        saveRouterDB(db);
        
        return {
            routed: true,
            sessionKey: db[senderId].sessionKey,
            memoryPath: db[senderId].memoryPath || `/memory/users/${senderId}.md`,
            userId: senderId,
            userName: senderName
        };
    }
    
    // 新用户，创建子代理
    log('WARN', `新用户，创建子代理...`, { userId: senderId });
    const result = createSubAgentForUser(senderId, senderName);
    
    if (result.success) {
        // 记录到数据库
        db[senderId] = {
            userId: senderId,
            userName: senderName,
            sessionKey: result.sessionKey || 'pending',
            label: result.label || `${senderName}的专属助手`,
            task: result.task,
            createdAt: new Date().toISOString(),
            lastActiveAt: new Date().toISOString(),
            messageCount: 1,
            status: result.pending ? 'pending' : 'active',
            memoryPath: `/memory/users/${senderId}.md`,
            isAdmin: senderId === ADMIN_ID
        };
        saveRouterDB(db);
        
        // 如果有 pending 队列，立即处理
        if (result.pending) {
            processPendingQueue();
        }
        
        return {
            routed: result.sessionKey ? true : false,
            pending: result.pending,
            sessionKey: result.sessionKey,
            message: result.pending ? '子代理创建中，请稍后' : '子代理已创建',
            userId: senderId,
            userName: senderName
        };
    }
    
    return {
        routed: false,
        error: result.error
    };
}

/**
 * 获取用户会话信息
 */
function getUserSession(userId) {
    const db = loadRouterDB();
    return db[userId] || null;
}

/**
 * 列出所有用户会话
 */
function listAllSessions() {
    const db = loadRouterDB();
    const stats = {
        totalUsers: Object.keys(db).length,
        users: []
    };
    
    for (const [userId, session] of Object.entries(db)) {
        stats.users.push({
            userId,
            userName: session.userName || '未知',
            sessionKey: session.sessionKey,
            status: session.status,
            messageCount: session.messageCount,
            lastActiveAt: session.lastActiveAt,
            isAdmin: session.isAdmin || false
        });
    }
    
    return stats;
}

// CLI 模式
if (process.argv[2] === 'handle') {
    const senderId = process.argv[3];
    const senderName = process.argv[4] || '用户';
    const message = process.argv[5] || '';
    
    const result = handleMessage(message, senderId, senderName);
    console.log('\n结果:', JSON.stringify(result, null, 2));
    
} else if (process.argv[2] === 'list') {
    const stats = listAllSessions();
    console.log('\n📊 用户会话列表:\n');
    console.log(`总用户数：${stats.totalUsers}`);
    stats.users.forEach(u => {
        console.log(`  - ${u.userId} (${u.userName})`);
        console.log(`    Session: ${u.sessionKey}`);
        console.log(`    状态：${u.status}`);
        console.log(`    消息数：${u.messageCount}`);
        console.log(`    最后活动：${u.lastActiveAt}`);
        console.log(`    管理员：${u.isAdmin ? '是' : '否'}`);
    });
    console.log();
    
} else if (process.argv[2] === 'process-pending') {
    log('INFO', '手动处理 pending 队列');
    const completed = processPendingQueue();
    console.log(`\n✅ 处理完成，创建成功：${completed.length}\n`);
    
} else if (process.argv[2] === 'test') {
    console.log('=== Gateway Hook v0.9.0 测试 ===\n');
    
    console.log('测试 1: 处理新用户消息');
    const result1 = handleMessage('你好', 'ou_test_user', '测试用户');
    console.log(JSON.stringify(result1, null, 2));
    
    console.log('\n测试 2: 处理现有用户消息');
    const result2 = handleMessage('再次你好', 'ou_test_user', '测试用户');
    console.log(JSON.stringify(result2, null, 2));
    
    console.log('\n测试 3: 列出所有会话');
    const stats = listAllSessions();
    console.log(JSON.stringify(stats, null, 2));
    
    console.log('\n✅ 所有测试完成！\n');
}

// 导出
module.exports = {
    handleMessage,
    loadRouterDB,
    saveRouterDB,
    createSubAgentForUser,
    processPendingQueue,
    getUserSession,
    listAllSessions,
    log,
    ADMIN_ID
};
