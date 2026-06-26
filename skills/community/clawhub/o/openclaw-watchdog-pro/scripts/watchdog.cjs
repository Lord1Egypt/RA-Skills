#!/usr/bin/env node
/**
 * OpenClaw Watchdog - 跨平台配置备份与网关监控
 * 功能：
 * 1. 修改 openclaw.json 前自动备份
 * 2. 每分钟检查 gateway 状态，宕机时自动恢复并重启
 * 
 * 跨平台支持：Linux / macOS / Windows
 */

const { execSync, spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');
const net = require('net');

// 默认配置
const DEFAULT_CONFIG = {
    checkIntervalMs: 60000,     // 检查间隔：1 分钟
    retryDelayMs: 5000,         // 重试延迟：5 秒
    maxBackups: 5,              // 最大备份数
    gatewayStartTimeoutMs: 30000, // gateway 启动超时：30 秒
    logLevel: 'info',           // 日志级别：debug, info, warn, error
    
    // 错误监控配置
    errorThreshold: 30,         // 错误数阈值，超过则告警
    errorWindowMs: 30 * 60 * 1000, // 监控窗口：30 分钟
    spikeRatio: 3,              // 突增倍数（3x vs 上次检查）
    errorLogPath: null,         // 日志路径（自动检测）
    extraPatterns: '',          // 自定义正则模式
};

// 路径配置
const HOME_DIR = os.homedir();
const CONFIG_DIR = process.env.OPENCLAW_CONFIG_DIR || path.join(HOME_DIR, '.openclaw');
const CONFIG_FILE = path.join(CONFIG_DIR, 'openclaw.json');
const BACKUP_DIR = path.join(CONFIG_DIR, 'backups');
const LOG_FILE = path.join(CONFIG_DIR, 'watchdog.log');
const PID_FILE = path.join(CONFIG_DIR, 'watchdog.pid');
const STATE_FILE = path.join(CONFIG_DIR, 'watchdog.state.json');

// 运行时状态
let state = {
    startTime: Date.now(),
    consecutiveFailures: 0,
    consecutiveRecoveries: 0,  // 连续恢复失败次数
    lastCheck: null,
    lastBackup: null,
    lastRecovery: null,
    lastDoctorFix: null,       // 上次 doctor --fix 时间
    totalChecks: 0,
    totalRecoveries: 0,
    totalDoctorFixes: 0        // doctor --fix 调用次数
};

// 日志级别
const LOG_LEVELS = { debug: 0, info: 1, warn: 2, error: 3 };

// 日志函数
function log(message, level = 'info') {
    const config = loadConfig();
    if (LOG_LEVELS[level] < LOG_LEVELS[config.logLevel]) return;
    
    const timestamp = new Date().toISOString().replace('T', ' ').substring(0, 19);
    const line = `[${timestamp}] [${level.toUpperCase()}] ${message}`;
    
    try {
        fs.appendFileSync(LOG_FILE, line + '\n');
        if (level === 'error' || config.logLevel === 'debug') {
            console.error(line);
        } else if (config.logLevel === 'debug') {
            console.log(line);
        }
    } catch (e) {
        console.error(`[ERROR] 写入日志失败：${e.message}`);
    }
}

// 加载用户配置
function loadConfig() {
    const configPath = path.join(CONFIG_DIR, 'watchdog.config.json');
    try {
        if (fs.existsSync(configPath)) {
            const userConfig = JSON.parse(fs.readFileSync(configPath, 'utf8'));
            return { ...DEFAULT_CONFIG, ...userConfig };
        }
    } catch (e) {
        log(`加载配置失败：${e.message}`, 'warn');
    }
    return DEFAULT_CONFIG;
}

// 保存配置
function saveConfig(config) {
    const configPath = path.join(CONFIG_DIR, 'watchdog.config.json');
    fs.writeFileSync(configPath, JSON.stringify(config, null, 2), 'utf8');
    log('配置已保存');
}

// 保存状态
function saveState() {
    try {
        fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2), 'utf8');
    } catch (e) {
        log(`保存状态失败：${e.message}`, 'debug');
    }
}

// 加载状态
function loadState() {
    try {
        if (fs.existsSync(STATE_FILE)) {
            const saved = JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
            state = { ...state, ...saved };
        }
    } catch (e) {
        log(`加载状态失败：${e.message}`, 'debug');
    }
}

// 确保目录存在
function ensureDir(dir) {
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
        log(`创建目录：${dir}`, 'debug');
    }
}

// 执行命令（返回 { success, stdout, stderr }）
function runCommand(cmd, options = {}) {
    const { silent = false, timeout = 10000 } = options;
    try {
        const stdout = execSync(cmd, {
            encoding: 'utf8',
            timeout,
            stdio: silent ? 'ignore' : ['ignore', 'pipe', 'pipe']
        });
        return { success: true, stdout, stderr: '' };
    } catch (e) {
        return {
            success: false,
            stdout: e.stdout || '',
            stderr: e.stderr || e.message
        };
    }
}

// 备份配置
function backupConfig() {
    log('开始备份配置');
    
    if (!fs.existsSync(CONFIG_FILE)) {
        log('配置文件不存在', 'error');
        return false;
    }
    
    ensureDir(BACKUP_DIR);
    
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').substring(0, 19);
    const backupFile = path.join(BACKUP_DIR, `openclaw.${timestamp}.json`);
    
    try {
        // 验证 JSON 有效性
        const content = fs.readFileSync(CONFIG_FILE, 'utf8');
        JSON.parse(content); // 验证格式
        
        fs.copyFileSync(CONFIG_FILE, backupFile);
        log(`备份完成：${backupFile}`);
        
        state.lastBackup = new Date().toISOString();
        saveState();
        
        // 清理旧备份
        cleanupBackups();
        return true;
    } catch (e) {
        log(`备份失败：${e.message}`, 'error');
        return false;
    }
}

// 清理旧备份
function cleanupBackups() {
    try {
        const config = loadConfig();
        const backups = fs.readdirSync(BACKUP_DIR)
            .filter(f => f.startsWith('openclaw.') && f.endsWith('.json'))
            .map(f => {
                const filePath = path.join(BACKUP_DIR, f);
                return {
                    name: f,
                    path: filePath,
                    mtime: fs.statSync(filePath).mtimeMs
                };
            })
            .sort((a, b) => b.mtime - a.mtime);
        
        // 删除超出数量的旧备份
        const toDelete = backups.slice(config.maxBackups);
        toDelete.forEach(b => {
            fs.unlinkSync(b.path);
            log(`清理旧备份：${b.name}`, 'debug');
        });
        
        if (toDelete.length > 0) {
            log(`清理了 ${toDelete.length} 个旧备份`);
        }
    } catch (e) {
        log(`清理备份失败：${e.message}`, 'warn');
    }
}

// 检查 gateway 状态（WebSocket 探针）
function checkGateway() {
    return new Promise((resolve) => {
        const config = loadConfig();
        const port = config.gatewayPort || 18789;
        const host = config.gatewayHost || '127.0.0.1';
        
        // 尝试 TCP 连接 + WebSocket 握手
        const socket = new net.Socket();
        const timeout = 3000;
        
        socket.setTimeout(timeout);
        
        socket.on('connect', () => {
            // 发送 WebSocket 握手请求
            const wsHandshake = `GET / HTTP/1.1\r\nHost: ${host}:${port}\r\nConnection: Upgrade\r\nUpgrade: websocket\r\nSec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\nSec-WebSocket-Version: 13\r\n\r\n`;
            socket.write(wsHandshake);
        });
        
        socket.on('data', (data) => {
            const response = data.toString();
            if (response.includes('101 Switching Protocols') || response.includes('Upgrade')) {
                socket.destroy();
                resolve(true);
            } else {
                socket.destroy();
                resolve(false);
            }
        });
        
        socket.on('timeout', () => {
            socket.destroy();
            resolve(false);
        });
        
        socket.on('error', (err) => {
            socket.destroy();
            resolve(false);
        });
        
        socket.connect(port, host);
    });
}

// 同步版本的 WebSocket 探针（用于监控循环）
function checkGatewaySync() {
    const port = 18789;
    const host = '127.0.0.1';
    
    return new Promise((resolve) => {
        const socket = new net.Socket();
        socket.setTimeout(3000);
        
        socket.on('connect', () => {
            const wsHandshake = `GET / HTTP/1.1\r\nHost: ${host}:${port}\r\nConnection: Upgrade\r\nUpgrade: websocket\r\nSec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\nSec-WebSocket-Version: 13\r\n\r\n`;
            socket.write(wsHandshake);
        });
        
        socket.on('data', (data) => {
            const response = data.toString();
            socket.destroy();
            resolve(response.includes('101 Switching Protocols') || response.includes('Upgrade'));
        });
        
        socket.on('timeout', () => { socket.destroy(); resolve(false); });
        socket.on('error', () => { socket.destroy(); resolve(false); });
        
        socket.connect(port, host);
    });
}

// 停止 gateway
function stopGateway() {
    log('停止 gateway...');
    runCommand('openclaw gateway stop', { silent: true, timeout: 10000 });
    // 等待进程退出
    return new Promise(resolve => setTimeout(resolve, 3000));
}

// 启动 gateway
function startGateway() {
    log('启动 gateway...');
    const result = runCommand('openclaw gateway start', { timeout: 10000 });
    if (result.success) {
        log('gateway 启动命令执行成功');
        return true;
    } else {
        log(`gateway 启动失败：${result.stderr}`, 'error');
        return false;
    }
}

// 验证 gateway 是否真正运行
function verifyGatewayRunning() {
    // 等待 gateway 完全启动
    return new Promise((resolve) => {
        const config = loadConfig();
        const timeout = config.gatewayStartTimeoutMs;
        const startTime = Date.now();
        
        const check = () => {
            if (checkGateway()) {
                resolve(true);
            } else if (Date.now() - startTime > timeout) {
                log('gateway 启动超时', 'error');
                resolve(false);
            } else {
                setTimeout(check, 1000);
            }
        };
        
        setTimeout(check, 2000); // 先等 2 秒再开始检查
    });
}

// 运行 doctor --fix 进行修复
async function runDoctorFix() {
    log('⚠️  多次恢复失败，尝试运行 openclaw doctor --fix...', 'warn');
    
    const result = runCommand('openclaw doctor --fix --non-interactive', { 
        silent: false, 
        timeout: 60000 
    });
    
    if (result.success) {
        log('doctor --fix 执行成功');
        state.lastDoctorFix = new Date().toISOString();
        state.totalDoctorFixes++;
        return true;
    } else {
        log(`doctor --fix 执行失败：${result.stderr}`, 'error');
        return false;
    }
}

// 错误模式检测
function detectErrorPatterns() {
    const config = loadConfig();
    const patterns = {
        '429/限流': /429|rate.?limit|too many requests/i,
        '5xx服务端错误': /5\d{2}|server error|internal error|bad gateway/i,
        '认证/权限': /401|403|unauthorized|forbidden|token expired|permission denied/i,
        '网络错误': /ETIMEDOUT|ECONNREFUSED|ECONNRESET|ENOTFOUND|socket hang up|connection/i,
        '消息投递失败': /sendMessage failed|deliver failed|fetch failed|send failed/i,
    };
    
    // 添加自定义模式
    if (config.extraPatterns) {
        patterns['自定义'] = new RegExp(config.extraPatterns, 'i');
    }
    
    // 查找日志文件
    let logPath = config.errorLogPath;
    if (!logPath) {
        const possiblePaths = [
            path.join(CONFIG_DIR, 'logs', `openclaw-${getDateStr()}.log`),
            `/tmp/openclaw/openclaw-${getDateStr()}.log`,
            path.join(os.homedir(), '.openclaw', 'logs', `openclaw-${getDateStr()}.log`),
        ];
        for (const p of possiblePaths) {
            if (fs.existsSync(p)) {
                logPath = p;
                break;
            }
        }
    }
    
    if (!logPath || !fs.existsSync(logPath)) {
        return null; // 没有日志文件
    }
    
    // 读取最近 N 分钟的日志
    const windowMs = config.errorWindowMs || (30 * 60 * 1000);
    const cutoffTime = Date.now() - windowMs;
    
    try {
        const content = fs.readFileSync(logPath, 'utf8');
        const lines = content.split('\n');
        const recentLines = [];
        
        for (const line of lines) {
            // 简单时间戳提取 (格式: 2026-03-24 16:30:00)
            const timeMatch = line.match(/^(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2})/);
            if (timeMatch) {
                const lineTime = new Date(`${timeMatch[1]}T${timeMatch[2]}`).getTime();
                if (lineTime >= cutoffTime) {
                    recentLines.push(line);
                }
            } else if (line.includes('ERROR') || line.includes('error') || line.includes('Failed')) {
                recentLines.push(line);
            }
        }
        
        // 统计各类错误
        const errorCounts = {};
        let totalErrors = 0;
        
        for (const patternName in patterns) {
            errorCounts[patternName] = 0;
        }
        
        for (const line of recentLines) {
            for (const [patternName, pattern] of Object.entries(patterns)) {
                if (pattern.test(line)) {
                    errorCounts[patternName]++;
                    totalErrors++;
                    break;
                }
            }
        }
        
        // 计算错误率
        const errorRate = totalErrors / (windowMs / 60000); // errors per minute
        
        // 获取上次错误数
        const lastErrorCount = state.lastErrorCount || 0;
        
        // 检测突增
        const spikeMultiplier = lastErrorCount > 0 ? totalErrors / lastErrorCount : 0;
        const isSpike = spikeMultiplier >= config.spikeRatio;
        
        // 检测错误集中度
        let maxConcentration = 0;
        let dominantError = null;
        if (totalErrors > 0) {
            for (const [type, count] of Object.entries(errorCounts)) {
                const concentration = count / totalErrors;
                if (concentration > maxConcentration) {
                    maxConcentration = concentration;
                    dominantError = type;
                }
            }
        }
        const isConcentrated = maxConcentration >= 0.8;
        
        // 更新状态
        state.lastErrorCount = totalErrors;
        
        return {
            totalErrors,
            errorRate: errorRate.toFixed(2),
            errorCounts,
            isSpike,
            spikeMultiplier: spikeMultiplier.toFixed(1),
            isConcentrated,
            dominantError,
            maxConcentration: (maxConcentration * 100).toFixed(0),
            windowMinutes: windowMs / 60000,
            threshold: config.errorThreshold,
            needsAlert: totalErrors > config.errorThreshold || isSpike
        };
    } catch (e) {
        log(`错误检测失败：${e.message}`, 'warn');
        return null;
    }
}

// 辅助函数：获取日期字符串
function getDateStr() {
    const now = new Date();
    return now.toISOString().substring(0, 10);
}

// 恢复配置并重启
async function recoverAndRestart() {
    log('=== 开始恢复流程 ===');
    state.consecutiveRecoveries++;
    
    const maxRetriesBeforeDoctor = 3;  // 连续 3 次恢复失败后调用 doctor
    
    try {
        const backups = fs.readdirSync(BACKUP_DIR)
            .filter(f => f.startsWith('openclaw.') && f.endsWith('.json'))
            .map(f => {
                const filePath = path.join(BACKUP_DIR, f);
                return {
                    name: f,
                    path: filePath,
                    mtime: fs.statSync(filePath).mtimeMs
                };
            })
            .sort((a, b) => b.mtime - a.mtime);
        
        if (backups.length === 0) {
            log('错误：未找到备份文件', 'error');
            return false;
        }
        
        const latestBackup = backups[0];
        log(`使用备份：${latestBackup.name}`);
        
        // 验证备份文件有效性
        try {
            const content = fs.readFileSync(latestBackup.path, 'utf8');
            JSON.parse(content);
            log('备份文件验证通过');
        } catch (e) {
            log(`备份文件损坏：${e.message}`, 'error');
            return false;
        }
        
        // 停止 gateway
        await stopGateway();
        
        // 恢复配置
        fs.copyFileSync(latestBackup.path, CONFIG_FILE);
        log('配置已恢复');
        
        // 启动 gateway
        if (await startGateway()) {
            // 验证是否真正运行
            if (await verifyGatewayRunning()) {
                log('=== gateway 重启成功 ===');
                state.lastRecovery = new Date().toISOString();
                state.totalRecoveries++;
                state.consecutiveFailures = 0;
                state.consecutiveRecoveries = 0;  // 重置连续恢复失败计数
                saveState();
                return true;
            } else {
                log('gateway 启动后验证失败', 'error');
                // 连续恢复失败，尝试 doctor --fix
                if (state.consecutiveRecoveries >= maxRetriesBeforeDoctor) {
                    log(`连续 ${maxRetriesBeforeDoctor} 次恢复失败，调用 doctor --fix`, 'warn');
                    await runDoctorFix();
                    state.consecutiveRecoveries = 0;  // 重置计数
                }
                saveState();
                return false;
            }
        } else {
            log('gateway 启动命令失败', 'error');
            // 连续恢复失败，尝试 doctor --fix
            if (state.consecutiveRecoveries >= maxRetriesBeforeDoctor) {
                log(`连续 ${maxRetriesBeforeDoctor} 次恢复失败，调用 doctor --fix`, 'warn');
                await runDoctorFix();
                state.consecutiveRecoveries = 0;
            }
            saveState();
            return false;
        }
    } catch (e) {
        log(`恢复失败：${e.message}`, 'error');
        // 连续恢复失败，尝试 doctor --fix
        if (state.consecutiveRecoveries >= maxRetriesBeforeDoctor) {
            log(`连续 ${maxRetriesBeforeDoctor} 次恢复失败，调用 doctor --fix`, 'warn');
            await runDoctorFix();
            state.consecutiveRecoveries = 0;
        }
        saveState();
        return false;
    }
}

// 包装 openclaw 命令
function wrapOpenclaw(args) {
    const modifyCommands = ['wizard', 'config', 'auth', 'models', 'acp', 'gateway', 'skill', 'install', 'plugins'];
    const cmdStr = args.join(' ');
    
    if (modifyCommands.some(cmd => cmdStr.includes(cmd))) {
        log(`检测到配置修改命令：${cmdStr}`);
        backupConfig();
    }
    
    try {
        const result = execSync(`openclaw ${args.join(' ')}`, {
            encoding: 'utf8',
            stdio: 'inherit'
        });
        process.exit(0);
    } catch (e) {
        process.exit(e.status || 1);
    }
}

// 监控循环
async function monitorLoop() {
    const config = loadConfig();
    log(`看门狗启动 (检查间隔：${config.checkIntervalMs / 1000}秒)`);
    log(`配置目录：${CONFIG_DIR}`);
    log(`备份目录：${BACKUP_DIR}`);
    
    // 保存 PID
    fs.writeFileSync(PID_FILE, process.pid.toString());
    log(`PID: ${process.pid}`);
    
    // 优雅退出处理
    process.on('SIGINT', () => {
        log('收到 SIGINT，正在关闭...');
        fs.unlinkSync(PID_FILE);
        saveState();
        process.exit(0);
    });
    
    process.on('SIGTERM', () => {
        log('收到 SIGTERM，正在关闭...');
        fs.unlinkSync(PID_FILE);
        saveState();
        process.exit(0);
    });
    
    // 主循环
    const check = async () => {
        state.totalChecks++;
        state.lastCheck = new Date().toISOString();
        
        // 1. WebSocket 探针检测 gateway
        const isHealthy = await checkGatewaySync();
        
        if (!isHealthy) {
            log('警告：gateway 无响应', 'warn');
            state.consecutiveFailures++;
            
            if (state.consecutiveFailures >= 2) {
                log(`连续 ${state.consecutiveFailures} 次失败，触发恢复`, 'warn');
                await recoverAndRestart();
                state.consecutiveFailures = 0;
            }
        } else {
            if (state.consecutiveFailures > 0) {
                log('gateway 已恢复正常', 'info');
            }
            state.consecutiveFailures = 0;
        }
        
        // 2. 错误模式检测
        const errorReport = detectErrorPatterns();
        if (errorReport && errorReport.needsAlert) {
            const { totalErrors, errorRate, isSpike, spikeMultiplier, isConcentrated, dominantError, maxConcentration, windowMinutes, threshold } = errorReport;
            
            let alertMsg = `⚠️ Gateway 错误告警 (最近 ${windowMinutes} 分钟)\n`;
            alertMsg += `  错误数: ${totalErrors} (阈值: ${threshold}, ${errorRate}/min)\n`;
            
            if (isSpike) {
                alertMsg += `  📈 错误突增: ${spikeMultiplier}x\n`;
            }
            
            if (isConcentrated && dominantError) {
                alertMsg += `  ⚠️ 单一错误 "${dominantError}" 占比 ${maxConcentration}%\n`;
            }
            
            alertMsg += `  错误分类:\n`;
            for (const [type, count] of Object.entries(errorReport.errorCounts)) {
                if (count > 0) {
                    alertMsg += `    ${type}: ${count}\n`;
                }
            }
            
            log(alertMsg, 'warn');
            
            // 保存错误告警状态
            state.lastErrorAlert = new Date().toISOString();
        }
        
        saveState();
        setTimeout(check, config.checkIntervalMs);
    };
    
    // 首次检查延迟 5 秒
    setTimeout(check, 5000);
}

// 显示状态
function showStatus() {
    loadState();
    console.log('OpenClaw Watchdog 状态');
    console.log('====================');
    console.log(`运行时长：${Math.round((Date.now() - state.startTime) / 1000 / 60)} 分钟`);
    console.log(`总检查次数：${state.totalChecks}`);
    console.log(`总恢复次数：${state.totalRecoveries}`);
    console.log(`连续恢复失败：${state.consecutiveRecoveries}`);
    console.log(`Doctor --fix 次数：${state.totalDoctorFixes}`);
    console.log(`最后检查：${state.lastCheck || '无'}`);
    console.log(`最后备份：${state.lastBackup || '无'}`);
    console.log(`最后恢复：${state.lastRecovery || '无'}`);
    console.log(`最后 Doctor Fix：${state.lastDoctorFix || '无'}`);
    console.log(`最后错误告警：${state.lastErrorAlert || '无'}`);
    console.log(`连续失败：${state.consecutiveFailures}`);
    
    // 检查当前 gateway 状态（简单 TCP 检测）
    const gatewayOk = new Promise((resolve) => {
        const socket = new net.Socket();
        socket.setTimeout(2000);
        socket.on('connect', () => { socket.destroy(); resolve(true); });
        socket.on('timeout', () => { socket.destroy(); resolve(false); });
        socket.on('error', () => { socket.destroy(); resolve(false); });
        socket.connect(18789, '127.0.0.1');
    });
    gatewayOk.then(ok => console.log(`Gateway 状态：${ok ? '✓ 正常' : '✗ 异常'}`));
    
    // 显示错误监控状态
    const errorStats = detectErrorPatterns();
    if (errorStats) {
        console.log('\n--- 错误监控 ---');
        console.log(`最近 ${errorStats.windowMinutes} 分钟错误数: ${errorStats.totalErrors} (阈值: ${errorStats.threshold})`);
        console.log(`错误率: ${errorStats.errorRate}/min`);
        if (errorStats.isSpike) {
            console.log(`📈 突增: ${errorStats.spikeMultiplier}x`);
        }
        if (errorStats.isConcentrated) {
            console.log(`⚠️ 单一错误 "${errorStats.dominantError}" 占比 ${errorStats.maxConcentration}%`);
        }
        for (const [type, count] of Object.entries(errorStats.errorCounts)) {
            if (count > 0) {
                console.log(`  ${type}: ${count}`);
            }
        }
    }
    
    // 显示备份文件
    if (fs.existsSync(BACKUP_DIR)) {
        const backups = fs.readdirSync(BACKUP_DIR)
            .filter(f => f.startsWith('openclaw.') && f.endsWith('.json'))
            .sort()
            .reverse()
            .slice(0, 5);
        console.log(`\n最近备份 (${backups.length}):`);
        backups.forEach(b => console.log(`  - ${b}`));
    }
}

// 检测是否已安装服务
function checkInstallation() {
    const platform = os.platform();
    
    if (platform === 'linux') {
        // 检查 systemd 服务
        if (fs.existsSync('/etc/systemd/system/openclaw-watchdog.service')) {
            try {
                const status = execSync('systemctl is-active openclaw-watchdog', { encoding: 'utf8' });
                return status.trim() === 'active';
            } catch (e) {
                return false;
            }
        }
        // 检查 cron
        try {
            const crontab = execSync('crontab -l', { encoding: 'utf8' });
            if (crontab.includes('watchdog.cjs')) {
                return true;
            }
        } catch (e) {
            // 无 crontab
        }
    }
    
    if (platform === 'darwin') {
        const plistPath = path.join(HOME_DIR, 'Library', 'LaunchAgents', 'com.openclaw.watchdog.plist');
        return fs.existsSync(plistPath);
    }
    
    if (platform === 'win32') {
        try {
            execSync('schtasks /query /tn "OpenClaw Watchdog"', { encoding: 'utf8', stdio: 'ignore' });
            return true;
        } catch (e) {
            return false;
        }
    }
    
    return false;
}

// 显示安装提示
function showInstallHint() {
    if (!checkInstallation()) {
        console.log('\n⚠️  看门狗服务未运行！');
        console.log('   请运行安装脚本以配置自动启动：\n');
        console.log('   node /usr/lib/node_modules/openclaw/skills/openclaw-watchdog/scripts/install.cjs\n');
        console.log('   或手动启动：node .../watchdog.cjs monitor &\n');
    }
}

// 初始化
function init() {
    ensureDir(CONFIG_DIR);
    ensureDir(BACKUP_DIR);
    log('初始化完成');
    
    // 创建默认配置（如果不存在）
    const configPath = path.join(CONFIG_DIR, 'watchdog.config.json');
    if (!fs.existsSync(configPath)) {
        saveConfig(DEFAULT_CONFIG);
    }
}

// 命令行接口
async function main() {
    const args = process.argv.slice(2);
    const command = args[0];
    
    init();
    
    // 非 monitor 命令时检查安装状态
    if (command !== 'monitor' && !command) {
        showInstallHint();
    }
    
    switch (command) {
        case 'backup':
            backupConfig();
            showInstallHint();
            break;
        case 'check':
            // 使用 TCP 快速检测 gateway 端口
            const isUp = await checkGatewaySync();
            if (isUp) {
                console.log('✓ gateway 运行正常');
                process.exit(0);
            } else {
                console.log('✗ gateway 无响应');
                process.exit(1);
            }
            break;
        case 'check-errors':
            // 检查错误模式
            const errorReport = detectErrorPatterns();
            if (!errorReport) {
                console.log('⚠️ 无法获取日志文件');
                process.exit(1);
            }
            if (errorReport.needsAlert) {
                console.log(`🔴 告警: 最近 ${errorReport.windowMinutes} 分钟 ${errorReport.totalErrors} 个错误 (${errorReport.errorRate}/min, 阈值: ${errorReport.threshold})`);
                if (errorReport.isSpike) console.log(`📈 突增: ${errorReport.spikeMultiplier}x`);
                if (errorReport.isConcentrated) console.log(`⚠️ 单一错误 "${errorReport.dominantError}" 占比 ${errorReport.maxConcentration}%`);
                console.log('错误分类:');
                for (const [type, count] of Object.entries(errorReport.errorCounts)) {
                    if (count > 0) console.log(`  ${type}: ${count}`);
                }
                process.exit(1);
            } else {
                console.log(`✓ 正常: 最近 ${errorReport.windowMinutes} 分钟 ${errorReport.totalErrors} 个错误`);
                process.exit(0);
            }
            break;
        case 'recover':
            await recoverAndRestart();
            break;
        case 'status':
            showStatus();
            showInstallHint();
            break;
        case 'config':
            if (args[1] === 'edit') {
                const config = loadConfig();
                console.log('当前配置:');
                console.log(JSON.stringify(config, null, 2));
                console.log(`\n编辑配置：${path.join(CONFIG_DIR, 'watchdog.config.json')}`);
            } else if (args[1] === 'reset') {
                saveConfig(DEFAULT_CONFIG);
                console.log('配置已重置');
            } else {
                console.log('用法：watchdog config [edit|reset]');
            }
            break;
        case 'wrap':
            wrapOpenclaw(args.slice(1));
            break;
        case 'monitor':
        default:
            loadState();
            await monitorLoop();
            break;
    }
}

main().catch(e => {
    log(`致命错误：${e.message}`, 'error');
    console.error(e);
    process.exit(1);
});
