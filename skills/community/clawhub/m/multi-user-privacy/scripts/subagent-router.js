#!/usr/bin/env node

/**
 * SubAgent Router - 子代理自动路由
 * 
 * 功能：
 * 1. 自动为每个用户创建专属子代理
 * 2. 消息自动路由到对应子代理
 * 3. 完全自动化，无需审核
 */

const fs = require('fs');
const path = require('path');

const ROUTER_DB = path.join(process.env.HOME, '.openclaw/skills/multi-user-privacy/.router-db.json');

/**
 * 子代理路由器
 */
class SubAgentRouter {
    constructor() {
        this.userSessions = this.loadRouterDB();
    }
    
    /**
     * 加载路由器数据库
     */
    loadRouterDB() {
        try {
            if (fs.existsSync(ROUTER_DB)) {
                return JSON.parse(fs.readFileSync(ROUTER_DB, 'utf-8'));
            }
        } catch (e) {
            console.warn('[SubAgentRouter] 加载数据库失败:', e.message);
        }
        return {};
    }
    
    /**
     * 保存路由器数据库
     */
    saveRouterDB() {
        try {
            const dir = path.dirname(ROUTER_DB);
            if (!fs.existsSync(dir)) {
                fs.mkdirSync(dir, { recursive: true });
            }
            fs.writeFileSync(ROUTER_DB, JSON.stringify(this.userSessions, null, 2), 'utf-8');
        } catch (e) {
            console.error('[SubAgentRouter] 保存数据库失败:', e.message);
        }
    }
    
    /**
     * 获取或创建用户子代理
     */
    async getUserSession(userId) {
        // 检查是否已有子代理
        if (this.userSessions[userId]) {
            console.log(`[SubAgentRouter] ✅ 找到现有子代理：${userId}`);
            return this.userSessions[userId];
        }
        
        // 创建新子代理
        console.log(`[SubAgentRouter] 🆕 创建新子代理：${userId}`);
        
        // 注意：实际创建需要调用 sessions_spawn
        // 这里模拟创建过程
        const session = {
            userId,
            createdAt: new Date().toISOString(),
            lastActiveAt: new Date().toISOString(),
            messageCount: 0,
            status: 'active'
        };
        
        this.userSessions[userId] = session;
        this.saveRouterDB();
        
        return session;
    }
    
    /**
     * 更新用户活动状态
     */
    updateActivity(userId) {
        if (!this.userSessions[userId]) {
            this.userSessions[userId] = {
                userId,
                createdAt: new Date().toISOString(),
                lastActiveAt: new Date().toISOString(),
                messageCount: 0,
                status: 'active'
            };
        }
        
        this.userSessions[userId].lastActiveAt = new Date().toISOString();
        this.userSessions[userId].messageCount++;
        this.saveRouterDB();
    }
    
    /**
     * 列出所有用户子代理
     */
    listAllUsers() {
        const stats = {
            totalUsers: Object.keys(this.userSessions).length,
            users: []
        };
        
        for (const [userId, session] of Object.entries(this.userSessions)) {
            stats.users.push({
                userId,
                createdAt: session.createdAt,
                lastActiveAt: session.lastActiveAt,
                messageCount: session.messageCount,
                status: session.status
            });
        }
        
        return stats;
    }
    
    /**
     * 删除用户子代理
     */
    removeUser(userId) {
        if (this.userSessions[userId]) {
            delete this.userSessions[userId];
            this.saveRouterDB();
            console.log(`✅ 用户 ${userId} 已删除`);
        } else {
            console.log(`❌ 未找到用户：${userId}`);
        }
    }
}

// CLI 入口
const command = process.argv[2];

if (command === 'list') {
    const router = new SubAgentRouter();
    const stats = router.listAllUsers();
    console.log('\n📊 子代理统计:\n');
    console.log(`总用户数：${stats.totalUsers}`);
    console.log('\n用户列表:');
    stats.users.forEach(u => {
        console.log(`  - ${u.userId}: ${u.messageCount} 条消息 (状态：${u.status})`);
    });
    console.log();
} else if (command === 'remove') {
    const userId = process.argv[3];
    const router = new SubAgentRouter();
    router.removeUser(userId);
} else if (command === 'clear') {
    const router = new SubAgentRouter();
    router.userSessions = {};
    router.saveRouterDB();
    console.log('✅ 路由器数据库已清空');
} else {
    console.log(`
SubAgent Router - 子代理自动路由

用法:
  node subagent-router.js list      # 查看所有用户
  node subagent-router.js remove <id> # 删除用户
  node subagent-router.js clear     # 清空数据库

功能:
  - 自动为每个用户创建专属子代理
  - 消息自动路由到对应子代理
  - 完全自动化，无需审核
    `);
}

// 导出
module.exports = { SubAgentRouter };
