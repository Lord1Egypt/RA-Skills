/**
 * 壁纸桥接服务器稳定性监控
 * 每30秒检查一次，记录状态，自动重启
 */

const http = require('http');
const { spawn, exec } = require('child_process');
const fs = require('fs');
const path = require('path');

const config = {
    healthUrl: 'http://127.0.0.1:8765/health',
    gatewayUrl: 'http://127.0.0.1:18789/v1/models',
    checkInterval: 30000,  // 30秒检查一次
    logFile: path.join(__dirname, 'wallpaper-monitor.log'),
    maxRetries: 3,
    retryDelay: 5000
};

let state = {
    lastCheck: null,
    consecutiveFailures: 0,
    totalChecks: 0,
    totalFailures: 0,
    totalRestarts: 0,
    startTime: Date.now(),
    serverProcess: null
};

// 日志
function log(msg) {
    const timestamp = new Date().toISOString();
    const line = `[${timestamp}] ${msg}`;
    console.log(line);
    fs.appendFileSync(config.logFile, line + '\n');
}

// 检查服务
async function checkService(url, name) {
    return new Promise((resolve) => {
        const req = http.get(url, { timeout: 5000 }, (res) => {
            resolve({ ok: res.statusCode === 200, status: res.statusCode });
        });
        req.on('error', (e) => resolve({ ok: false, error: e.message }));
        req.on('timeout', () => {
            req.destroy();
            resolve({ ok: false, error: 'timeout' });
        });
    });
}

// 检查并重启
async function healthCheck() {
    state.lastCheck = Date.now();
    state.totalChecks++;
    
    // 检查桥接服务器
    const bridge = await checkService(config.healthUrl, 'Bridge');
    const gateway = await checkService(config.gatewayUrl, 'Gateway');
    
    if (bridge.ok && gateway.ok) {
        state.consecutiveFailures = 0;
        const uptime = Math.round((Date.now() - state.startTime) / 1000 / 60);
        log(`✅ 正常运行 | 检查次数: ${state.totalChecks} | 运行时间: ${uptime}分钟`);
    } else {
        state.consecutiveFailures++;
        state.totalFailures++;
        
        const issues = [];
        if (!bridge.ok) issues.push(`桥接:${bridge.error || bridge.status}`);
        if (!gateway.ok) issues.push(`网关:${gateway.error || gateway.status}`);
        
        log(`❌ 连接失败 (${state.consecutiveFailures}次): ${issues.join(', ')}`);
        
        // 连续失败超过阈值，尝试重启
        if (state.consecutiveFailures >= config.maxRetries) {
            log(`🔄 尝试重启桥接服务器...`);
            await restartBridge();
        }
    }
    
    // 写入状态文件
    writeStatus();
}

// 重启桥接服务器
async function restartBridge() {
    return new Promise((resolve) => {
        // Windows下用taskkill
        exec('taskkill /F /IM node.exe /FI "WINDOWTITLE eq wallpaper-server*"', (err) => {
            // 忽略错误，可能没有进程
            
            setTimeout(() => {
                // 启动新进程
                const serverPath = path.join(__dirname, 'wallpaper-server.js');
                state.serverProcess = spawn('node', [serverPath], {
                    detached: true,
                    stdio: 'inherit',
                    windowsHide: true
                });
                
                state.serverProcess.unref();
                state.totalRestarts++;
                state.consecutiveFailures = 0;
                
                log(`🔄 已重启桥接服务器 (累计重启: ${state.totalRestarts})`);
                resolve();
            }, 2000);
        });
    });
}

// 写入状态文件
function writeStatus() {
    const status = {
        ...state,
        lastCheck: new Date(state.lastCheck).toISOString(),
        startTime: new Date(state.startTime).toISOString(),
        uptimeMinutes: Math.round((Date.now() - state.startTime) / 1000 / 60),
        uptimeHours: Math.round((Date.now() - state.startTime) / 1000 / 3600 * 10) / 10
    };
    
    fs.writeFileSync(
        path.join(__dirname, 'wallpaper-status.json'),
        JSON.stringify(status, null, 2)
    );
}

// 主循环
function start() {
    log('═══════════════════════════════════════');
    log('🚀 壁纸桥接服务器监控启动');
    log('═══════════════════════════════════════');
    log(`检查间隔: ${config.checkInterval / 1000}秒`);
    log(`最大重试: ${config.maxRetries}次`);
    log('');
    
    // 立即检查一次
    healthCheck();
    
    // 定时检查
    setInterval(healthCheck, config.checkInterval);
    
    // 每小时报告
    setInterval(() => {
        const hours = Math.round((Date.now() - state.startTime) / 1000 / 3600 * 10) / 10;
        log(`📊 小时报告: 运行${hours}小时 | 检查${state.totalChecks}次 | 失败${state.totalFailures}次 | 重启${state.totalRestarts}次`);
    }, 3600000);
}

// 启动
start();