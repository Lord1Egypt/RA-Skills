#!/usr/bin/env node

/**
 * Web Admin Server - 子代理管理界面后端
 * 
 * 功能：
 * 1. 提供静态文件服务（HTML/CSS/JS）
 * 2. 提供 API 接口管理子代理和配额
 * 3. 实时数据更新
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

const PORT = process.env.WEB_ADMIN_PORT || 3456;
const BASE_DIR = path.join(process.env.HOME, '.openclaw/workspace/web-admin');
const ROUTER_DB = path.join(process.env.HOME, '.openclaw/skills/multi-user-privacy/.router-db.json');
const QUOTA_DB = path.join(process.env.HOME, '.openclaw/skills/multi-user-privacy/.quota-db.json');

/**
 * 数据管理器
 */
class DataManager {
    constructor() {
        this.load();
    }
    
    load() {
        try {
            if (fs.existsSync(ROUTER_DB)) {
                this.routerData = JSON.parse(fs.readFileSync(ROUTER_DB, 'utf-8'));
            } else {
                this.routerData = {};
            }
        } catch (e) {
            console.error('[DataManager] 加载 router DB 失败:', e.message);
            this.routerData = {};
        }
        
        try {
            if (fs.existsSync(QUOTA_DB)) {
                this.quotaData = JSON.parse(fs.readFileSync(QUOTA_DB, 'utf-8'));
            } else {
                this.quotaData = {};
            }
        } catch (e) {
            console.error('[DataManager] 加载 quota DB 失败:', e.message);
            this.quotaData = {};
        }
    }
    
    save() {
        try {
            const routerDir = path.dirname(ROUTER_DB);
            if (!fs.existsSync(routerDir)) {
                fs.mkdirSync(routerDir, { recursive: true });
            }
            fs.writeFileSync(ROUTER_DB, JSON.stringify(this.routerData, null, 2), 'utf-8');
        } catch (e) {
            console.error('[DataManager] 保存 router DB 失败:', e.message);
        }
        
        try {
            const quotaDir = path.dirname(QUOTA_DB);
            if (!fs.existsSync(quotaDir)) {
                fs.mkdirSync(quotaDir, { recursive: true });
            }
            fs.writeFileSync(QUOTA_DB, JSON.stringify(this.quotaData, null, 2), 'utf-8');
        } catch (e) {
            console.error('[DataManager] 保存 quota DB 失败:', e.message);
        }
    }
    
    getAllData() {
        return {
            router: this.routerData,
            quota: this.quotaData
        };
    }
    
    updateQuota(userId, quota) {
        if (!this.quotaData[userId]) {
            this.quotaData[userId] = {
                used: {
                    disk: 0,
                    tokens: 0,
                    messages: 0,
                    lastReset: new Date().toISOString()
                },
                createdAt: new Date().toISOString()
            };
        }
        
        this.quotaData[userId] = {
            ...this.quotaData[userId],
            ...quota
        };
        
        this.save();
        return true;
    }
    
    createUser(userId, userName, quota) {
        if (this.routerData[userId]) {
            return { success: false, error: '用户已存在' };
        }
        
        this.routerData[userId] = {
            userId,
            userName,
            sessionKey: `session_${Date.now()}`,
            label: `${userName}的专属助手`,
            createdAt: new Date().toISOString(),
            lastActiveAt: new Date().toISOString(),
            messageCount: 0,
            status: 'active'
        };
        
        this.updateQuota(userId, quota);
        
        return { success: true };
    }
    
    deleteUser(userId) {
        if (!this.routerData[userId]) {
            return { success: false, error: '用户不存在' };
        }
        
        delete this.routerData[userId];
        delete this.quotaData[userId];
        
        this.save();
        return { success: true };
    }
}

const dataManager = new DataManager();

/**
 * HTTP 服务器
 */
const server = http.createServer((req, res) => {
    const parsedUrl = url.parse(req.url, true);
    const pathname = parsedUrl.pathname;
    
    // CORS 头
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    
    // 处理 OPTIONS 预检请求
    if (req.method === 'OPTIONS') {
        res.writeHead(200);
        res.end();
        return;
    }
    
    // API 路由
    if (pathname.startsWith('/api/')) {
        handleApi(req, res, parsedUrl);
    } else {
        // 静态文件服务
        serveStatic(req, res, pathname);
    }
});

/**
 * 处理 API 请求
 */
function handleApi(req, res, parsedUrl) {
    const pathname = parsedUrl.pathname;
    
    if (req.method === 'GET') {
        if (pathname === '/api/data') {
            // 获取所有数据
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify(dataManager.getAllData()));
        } else if (pathname === '/api/health') {
            // 健康检查
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ status: 'ok', timestamp: new Date().toISOString() }));
        } else {
            res.writeHead(404, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: 'API not found' }));
        }
    } else if (req.method === 'POST') {
        let body = '';
        
        req.on('data', chunk => {
            body += chunk.toString();
        });
        
        req.on('end', () => {
            try {
                const data = JSON.parse(body);
                
                if (pathname === '/api/quota') {
                    // 更新配额
                    const { userId, quota } = data;
                    if (!userId) {
                        res.writeHead(400, { 'Content-Type': 'application/json' });
                        res.end(JSON.stringify({ success: false, error: '缺少 userId' }));
                        return;
                    }
                    
                    const success = dataManager.updateQuota(userId, quota);
                    res.writeHead(200, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify({ success }));
                    
                } else if (pathname === '/api/user') {
                    // 创建用户
                    const { userId, userName, quota } = data;
                    if (!userId || !userName) {
                        res.writeHead(400, { 'Content-Type': 'application/json' });
                        res.end(JSON.stringify({ success: false, error: '缺少 userId 或 userName' }));
                        return;
                    }
                    
                    const result = dataManager.createUser(userId, userName, quota);
                    res.writeHead(200, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify(result));
                    
                } else {
                    res.writeHead(404, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify({ success: false, error: 'API not found' }));
                }
            } catch (e) {
                res.writeHead(400, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ success: false, error: 'Invalid JSON' }));
            }
        });
    } else if (req.method === 'DELETE') {
        if (pathname === '/api/user') {
            let body = '';
            
            req.on('data', chunk => {
                body += chunk.toString();
            });
            
            req.on('end', () => {
                try {
                    const data = JSON.parse(body);
                    const { userId } = data;
                    
                    if (!userId) {
                        res.writeHead(400, { 'Content-Type': 'application/json' });
                        res.end(JSON.stringify({ success: false, error: '缺少 userId' }));
                        return;
                    }
                    
                    const result = dataManager.deleteUser(userId);
                    res.writeHead(200, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify(result));
                } catch (e) {
                    res.writeHead(400, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify({ success: false, error: 'Invalid JSON' }));
                }
            });
        } else {
            res.writeHead(404, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ success: false, error: 'API not found' }));
        }
    } else {
        res.writeHead(405, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'Method not allowed' }));
    }
}

/**
 * 提供静态文件
 */
function serveStatic(req, res, pathname) {
    // 默认指向 index.html
    if (pathname === '/') {
        pathname = '/index.html';
    }
    
    const filePath = path.join(BASE_DIR, pathname);
    const ext = path.extname(filePath);
    
    // 检查文件是否存在
    if (!fs.existsSync(filePath)) {
        res.writeHead(404, { 'Content-Type': 'text/html' });
        res.end('<h1>404 - File Not Found</h1>');
        return;
    }
    
    // 设置 Content-Type
    const contentTypes = {
        '.html': 'text/html',
        '.css': 'text/css',
        '.js': 'application/javascript',
        '.json': 'application/json',
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.gif': 'image/gif',
        '.svg': 'image/svg+xml'
    };
    
    const contentType = contentTypes[ext] || 'application/octet-stream';
    res.setHeader('Content-Type', contentType);
    
    // 读取并返回文件
    fs.createReadStream(filePath)
        .pipe(res);
}

// 启动服务器
server.listen(PORT, () => {
    console.log(`
╔════════════════════════════════════════════════════════╗
║   OpenClaw Web Admin Server                            ║
║                                                        ║
║   🌐 访问地址：http://localhost:${PORT}                  ║
║   📊 数据文件：${ROUTER_DB}                            ║
║   ⚙️  配额文件：${QUOTA_DB}                            ║
║                                                        ║
║   按 Ctrl+C 停止服务                                    ║
╚════════════════════════════════════════════════════════╝
    `);
});

// 优雅退出
process.on('SIGINT', () => {
    console.log('\n👋 正在关闭服务器...');
    server.close(() => {
        console.log('✅ 服务器已关闭');
        process.exit(0);
    });
});
