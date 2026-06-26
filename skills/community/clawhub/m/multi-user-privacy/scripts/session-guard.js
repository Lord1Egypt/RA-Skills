#!/usr/bin/env node

/**
 * Session Guard - Session 会话管理
 * 
 * 功能：
 * 1. 为每个用户创建/查找专属 session
 * 2. 确保对话上下文隔离
 * 3. Session 不匹配时发出警告
 */

const fs = require('fs');
const path = require('path');

const SESSION_DB = path.join(process.env.HOME, '.openclaw/skills/multi-user-privacy/.session-db.json');

/**
 * Session 管理器
 */
class SessionManager {
    constructor() {
        this.sessions = this.loadSessionDB();
    }
    
    /**
     * 加载 Session 数据库
     */
    loadSessionDB() {
        try {
            if (fs.existsSync(SESSION_DB)) {
                return JSON.parse(fs.readFileSync(SESSION_DB, 'utf-8'));
            }
        } catch (e) {
            console.warn('[SessionGuard] 加载 Session 数据库失败:', e.message);
        }
        return {};
    }
    
    /**
     * 保存 Session 数据库
     */
    saveSessionDB() {
        try {
            const dir = path.dirname(SESSION_DB);
            if (!fs.existsSync(dir)) {
                fs.mkdirSync(dir, { recursive: true });
            }
            fs.writeFileSync(SESSION_DB, JSON.stringify(this.sessions, null, 2), 'utf-8');
        } catch (e) {
            console.error('[SessionGuard] 保存 Session 数据库失败:', e.message);
        }
    }
    
    /**
     * 获取或创建用户 Session
     */
    async getSession(userId) {
        // 检查是否已有 session
        if (this.sessions[userId]) {
            console.log(`[SessionGuard] ✅ 找到现有 session: ${userId}`);
            return this.sessions[userId];
        }
        
        // 创建新 session
        console.log(`[SessionGuard] 🆕 创建新 session: ${userId}`);
        const session = {
            userId,
            createdAt: new Date().toISOString(),
            lastActiveAt: new Date().toISOString(),
            messageCount: 0
        };
        
        this.sessions[userId] = session;
        this.saveSessionDB();
        
        return session;
    }
    
    /**
     * 更新 Session 活动状态
     */
    updateSessionActivity(userId) {
        if (!this.sessions[userId]) {
            this.sessions[userId] = {
                userId,
                createdAt: new Date().toISOString(),
                lastActiveAt: new Date().toISOString(),
                messageCount: 0
            };
        }
        
        this.sessions[userId].lastActiveAt = new Date().toISOString();
        this.sessions[userId].messageCount++;
        this.saveSessionDB();
    }
    
    /**
     * 检查 Session 是否匹配
     */
    checkSessionMatch(currentUserId, expectedUserId) {
        return currentUserId === expectedUserId;
    }
    
    /**
     * 获取所有 Session 统计
     */
    getSessionStats() {
        const stats = {
            totalSessions: Object.keys(this.sessions).length,
            sessions: []
        };
        
        for (const [userId, session] of Object.entries(this.sessions)) {
            stats.sessions.push({
                userId,
                createdAt: session.createdAt,
                lastActiveAt: session.lastActiveAt,
                messageCount: session.messageCount
            });
        }
        
        return stats;
    }
}

// CLI 入口
const command = process.argv[2];

if (command === 'stats') {
    const manager = new SessionManager();
    const stats = manager.getSessionStats();
    console.log('\n📊 Session 统计:\n');
    console.log(`总 Session 数：${stats.totalSessions}`);
    console.log('\nSession 列表:');
    stats.sessions.forEach(s => {
        console.log(`  - ${s.userId}: ${s.messageCount} 条消息 (最后活跃：${s.lastActiveAt})`);
    });
    console.log();
} else if (command === 'clear') {
    const manager = new SessionManager();
    manager.sessions = {};
    manager.saveSessionDB();
    console.log('✅ Session 数据库已清空');
} else {
    console.log(`
Session Guard - Session 会话管理

用法:
  node session-guard.js stats    # 查看 Session 统计
  node session-guard.js clear    # 清空 Session 数据库

功能:
  - 为每个用户创建专属 session 记录
  - 跟踪用户活动状态
  - 检查 session 匹配
    `);
}

// 导出
module.exports = { SessionManager };
