#!/usr/bin/env node

/**
 * Auto Mount - 技能自动挂载
 * 
 * 功能：
 * 1. 技能安装后自动执行
 * 2. 初始化用户配置
 * 3. 设置默认配额
 * 4. 注册消息钩子
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const SKILL_DIR = path.join(process.env.HOME, '.openclaw/skills/multi-user-privacy');
const CONFIG_FILE = path.join(process.env.HOME, '.openclaw/workspace/.multi-user-config.json');
const USER_CONTEXT_FILE = path.join(process.env.HOME, '.openclaw/workspace/.user-context.json');

/**
 * 初始化配置
 */
function initConfig() {
    console.log('🔧 初始化多用户配置...\n');
    
    // 1. 创建配置文件
    const config = {
        version: '0.8.0',
        enabled: true,
        autoCreateSubAgents: true,
        defaultQuota: {
            diskQuotaMB: 100,
            tokenQuota: 100000,
            messageQuota: 1000,
            sessionTimeoutHours: 24
        },
        adminUserId: 'ou_b96f5424607baf3a0455b55e0f4a2213',
        createdAt: new Date().toISOString()
    };
    
    fs.writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2), 'utf-8');
    console.log('✅ 配置文件已创建：.multi-user-config.json');
    
    // 2. 更新 .user-context.json（如果不存在）
    if (!fs.existsSync(USER_CONTEXT_FILE)) {
        const userContext = {
            primaryUser: {
                id: config.adminUserId,
                name: '老刘',
                role: 'admin'
            },
            knownUsers: [],
            privacyMode: 'strict',
            subAgentEnabled: true
        };
        
        fs.writeFileSync(USER_CONTEXT_FILE, JSON.stringify(userContext, null, 2), 'utf-8');
        console.log('✅ 用户上下文已创建：.user-context.json');
    }
    
    // 3. 创建必要目录
    const dirs = [
        path.join(process.env.HOME, '.openclaw/logs'),
        path.join(process.env.HOME, '.openclaw/workspace/memory/users'),
        path.join(process.env.HOME, '.openclaw/workspace/memory/daily'),
        path.join(process.env.HOME, '.openclaw/workspace/memory/groups')
    ];
    
    dirs.forEach(dir => {
        if (!fs.existsSync(dir)) {
            fs.mkdirSync(dir, { recursive: true });
            console.log(`✅ 目录已创建：${dir}`);
        }
    });
    
    console.log('\n✅ 配置初始化完成！\n');
}

/**
 * 注册消息钩子
 * 注意：隐私检查功能已集成到 privacy-guard.js，无需额外钩子
 */
function registerHooks() {
    console.log('🔗 注册消息钩子...\n');
    console.log('ℹ️  隐私检查功能已集成到 privacy-guard.js\n');
    console.log('✅ 钩子注册完成！\n');
}

/**
 * 初始化已知用户
 */
function initKnownUsers() {
    console.log('👥 初始化已知用户...\n');
    
    // 检查 memory/users 目录
    const usersDir = path.join(process.env.HOME, '.openclaw/workspace/memory/users');
    
    if (!fs.existsSync(usersDir)) {
        fs.mkdirSync(usersDir, { recursive: true });
    }
    
    // 扫描现有用户文件
    const userFiles = fs.readdirSync(usersDir).filter(f => f.endsWith('.md'));
    
    console.log(`发现 ${userFiles.length} 个用户文件`);
    
    userFiles.forEach(file => {
        const userId = file.replace('.md', '');
        const userFile = path.join(usersDir, file);
        const content = fs.readFileSync(userFile, 'utf-8');
        
        // 提取用户名
        const nameMatch = content.match(/^# (.+) \(/);
        const userName = nameMatch ? nameMatch[1] : '未知用户';
        
        console.log(`  - ${userId}: ${userName}`);
    });
    
    console.log('\n✅ 用户初始化完成！\n');
}

/**
 * 显示使用说明
 */
function showUsage() {
    console.log(`
╔═══════════════════════════════════════════════════════════════╗
║     Multi-User Privacy Skill - 自动挂载完成                   ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  ✅ 配置已初始化                                               ║
║  ✅ 钩子已注册                                                 ║
║  ✅ 用户已扫描                                                 ║
║                                                               ║
║  下一步：                                                      ║
║  1. 重启 OpenClaw Gateway（如果正在运行）                     ║
║  2. 发送测试消息验证功能                                       ║
║  3. 查看日志：~/.openclaw/logs/privacy-guard.log              ║
║                                                               ║
║  管理命令：                                                    ║
║  - node subagent-integration.js list     # 查看所有子代理     ║
║  - node subagent-integration.js quota    # 查看配额使用       ║
║  - node subagent-integration.js cleanup  # 清理过期 session   ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
    `);
}

// 主函数
function main() {
    console.log('\n');
    console.log('╔═══════════════════════════════════════════════════════════════╗');
    console.log('║   Multi-User Privacy Skill - 自动挂载脚本                     ║');
    console.log('╚═══════════════════════════════════════════════════════════════╝');
    console.log('\n');
    
    try {
        initConfig();
        registerHooks();
        initKnownUsers();
        showUsage();
        
        console.log('\n✅ 自动挂载完成！\n');
        process.exit(0);
    } catch (e) {
        console.error('\n❌ 自动挂载失败:', e.message);
        console.error(e.stack);
        process.exit(1);
    }
}

// 运行
main();
