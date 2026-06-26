#!/usr/bin/env node
/**
 * OpenClaw Watchdog 安装脚本
 * 自动检测系统并配置持久化运行
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');

const HOME = os.homedir();
const WATCHDOG_SCRIPT = path.join(__dirname, 'watchdog.cjs');
const CONFIG_DIR = process.env.OPENCLAW_CONFIG_DIR || path.join(HOME, '.openclaw');

// 颜色输出
const colors = {
    reset: '\x1b[0m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    red: '\x1b[31m',
    blue: '\x1b[34m'
};

function log(msg, color = 'reset') {
    console.log(`${colors[color]}${msg}${colors.reset}`);
}

function run(cmd) {
    try {
        execSync(cmd, { encoding: 'utf8', stdio: 'pipe' });
        return true;
    } catch (e) {
        return false;
    }
}

function detectSystem() {
    const platform = os.platform();
    
    if (platform === 'linux') {
        // 检测 systemd
        if (fs.existsSync('/run/systemd/system')) {
            return { type: 'systemd', platform };
        }
        // 检测 cron
        if (run('which crontab')) {
            return { type: 'cron', platform };
        }
        return { type: 'manual', platform };
    }
    
    if (platform === 'darwin') {
        return { type: 'launchd', platform };
    }
    
    if (platform === 'win32') {
        return { type: 'schtasks', platform };
    }
    
    return { type: 'manual', platform };
}

function setupSystemd() {
    log('检测到 systemd，创建服务...', 'blue');
    
    const serviceContent = `[Unit]
Description=OpenClaw Watchdog - 配置备份与网关监控
After=network.target openclaw-gateway.service

[Service]
Type=simple
ExecStart=/usr/bin/node ${WATCHDOG_SCRIPT} monitor
Restart=always
RestartSec=10
User=root
WorkingDirectory=${CONFIG_DIR}
StandardOutput=append:${path.join(CONFIG_DIR, 'watchdog.log')}
StandardError=append:${path.join(CONFIG_DIR, 'watchdog.log')}
Environment=OPENCLAW_CONFIG_DIR=${CONFIG_DIR}

[Install]
WantedBy=multi-user.target
`;
    
    const servicePath = '/etc/systemd/system/openclaw-watchdog.service';
    
    try {
        fs.writeFileSync(servicePath, serviceContent);
        log('✓ 服务文件已创建', 'green');
        
        execSync('systemctl daemon-reload', { encoding: 'utf8' });
        log('✓ systemd 配置已重载', 'green');
        
        execSync('systemctl enable openclaw-watchdog', { encoding: 'utf8' });
        log('✓ 服务已启用（开机自启）', 'green');
        
        execSync('systemctl restart openclaw-watchdog', { encoding: 'utf8' });
        log('✓ 服务已启动', 'green');
        
        return true;
    } catch (e) {
        log(`✗ systemd 配置失败：${e.message}`, 'red');
        return false;
    }
}

function setupLaunchd() {
    log('检测到 macOS，创建 launchd 配置...', 'blue');
    
    const plistDir = path.join(HOME, 'Library', 'LaunchAgents');
    const plistPath = path.join(plistDir, 'com.openclaw.watchdog.plist');
    
    // 确保目录存在
    if (!fs.existsSync(plistDir)) {
        fs.mkdirSync(plistDir, { recursive: true });
    }
    
    const plistContent = `<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.openclaw.watchdog</string>
    <key>ProgramArguments</key>
    <array>
        <string>node</string>
        <string>${WATCHDOG_SCRIPT}</string>
        <string>monitor</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>${path.join(CONFIG_DIR, 'watchdog.log')}</string>
    <key>StandardErrorPath</key>
    <string>${path.join(CONFIG_DIR, 'watchdog.log')}</string>
    <key>WorkingDirectory</key>
    <string>${CONFIG_DIR}</string>
</dict>
</plist>
`;
    
    try {
        fs.writeFileSync(plistPath, plistContent);
        log('✓ launchd 配置文件已创建', 'green');
        
        // 卸载旧的（如果存在）
        execSync(`launchctl unload ${plistPath}`, { encoding: 'utf8', stdio: 'ignore' }).catch(() => {});
        
        // 加载新的
        execSync(`launchctl load ${plistPath}`, { encoding: 'utf8' });
        log('✓ 服务已加载并启动', 'green');
        
        return true;
    } catch (e) {
        log(`✗ launchd 配置失败：${e.message}`, 'red');
        return false;
    }
}

function setupCron() {
    log('检测到 cron，创建定时任务...', 'blue');
    
    const cronJob = `* * * * * node ${WATCHDOG_SCRIPT} check || node ${WATCHDOG_SCRIPT} recover`;
    
    try {
        // 获取当前 crontab
        let current = '';
        try {
            current = execSync('crontab -l', { encoding: 'utf8' });
        } catch (e) {
            // 没有 crontab 是正常的
        }
        
        // 检查是否已存在
        if (current.includes('openclaw-watchdog') || current.includes(WATCHDOG_SCRIPT)) {
            log('⚠ cron 任务已存在，跳过', 'yellow');
            return true;
        }
        
        // 添加新任务
        const newCrontab = current + '\n# OpenClaw Watchdog\n' + cronJob + '\n';
        
        // 写入临时文件
        const tmpFile = path.join(os.tmpdir(), 'watchdog-cron-' + process.pid);
        fs.writeFileSync(tmpFile, newCrontab);
        
        // 安装 crontab
        execSync(`crontab ${tmpFile}`, { encoding: 'utf8' });
        fs.unlinkSync(tmpFile);
        
        log('✓ cron 任务已添加', 'green');
        return true;
    } catch (e) {
        log(`✗ cron 配置失败：${e.message}`, 'red');
        return false;
    }
}

function setupWindows() {
    log('检测到 Windows，创建计划任务...', 'blue');
    
    const taskName = 'OpenClaw Watchdog';
    const scriptPath = WATCHDOG_SCRIPT.replace(/\//g, '\\');
    
    try {
        // 删除旧任务（如果存在）
        execSync(`schtasks /delete /tn "${taskName}" /f`, { encoding: 'utf8', stdio: 'ignore' }).catch(() => {});
        
        // 创建新任务（开机启动，最高权限）
        execSync(`schtasks /create /tn "${taskName}" /tr "node ${scriptPath} monitor" /sc onstart /ru SYSTEM /rl highest /f`, { encoding: 'utf8' });
        
        log('✓ 计划任务已创建', 'green');
        return true;
    } catch (e) {
        log(`✗ 计划任务创建失败：${e.message}`, 'red');
        log('  请以管理员身份运行此脚本', 'yellow');
        return false;
    }
}

function setupAlias() {
    log('配置快捷命令...', 'blue');
    
    const aliasCmd = `alias oc='node ${WATCHDOG_SCRIPT} wrap'`;
    const shellConfig = path.join(HOME, '.bashrc');
    
    try {
        let content = '';
        if (fs.existsSync(shellConfig)) {
            content = fs.readFileSync(shellConfig, 'utf8');
        }
        
        if (!content.includes('openclaw-watchdog') && !content.includes('watchdog.cjs wrap')) {
            content += `\n# OpenClaw Watchdog\n${aliasCmd}\n`;
            fs.writeFileSync(shellConfig, content);
            log('✓ bash 别名已添加 (~/.bashrc)', 'green');
        } else {
            log('⚠ bash 别名已存在', 'yellow');
        }
    } catch (e) {
        log(`⚠ bash 别名配置失败：${e.message}`, 'yellow');
    }
    
    // 也添加到 .profile（如果存在）
    const profileConfig = path.join(HOME, '.profile');
    if (fs.existsSync(profileConfig)) {
        try {
            let content = fs.readFileSync(profileConfig, 'utf8');
            if (!content.includes('openclaw-watchdog')) {
                content += `\n# OpenClaw Watchdog\n${aliasCmd}\n`;
                fs.writeFileSync(profileConfig, content);
                log('✓ profile 别名已添加 (~/.profile)', 'green');
            }
        } catch (e) {
            // 忽略
        }
    }
}

function main() {
    log('\n=================================', 'blue');
    log('  OpenClaw Watchdog 安装程序', 'blue');
    log('=================================\n', 'blue');
    
    // 检测系统
    const system = detectSystem();
    log(`检测到系统：${system.platform} (${system.type})`, 'blue');
    
    // 确保配置目录存在
    if (!fs.existsSync(CONFIG_DIR)) {
        fs.mkdirSync(CONFIG_DIR, { recursive: true });
        log(`✓ 创建配置目录：${CONFIG_DIR}`, 'green');
    }
    
    // 根据系统类型安装
    let success = false;
    
    switch (system.type) {
        case 'systemd':
            success = setupSystemd();
            break;
        case 'launchd':
            success = setupLaunchd();
            break;
        case 'cron':
            success = setupCron();
            break;
        case 'schtasks':
            success = setupWindows();
            break;
        default:
            log('⚠ 未检测到支持的初始化系统，使用手动模式', 'yellow');
            success = false;
    }
    
    // 配置别名（非 Windows）
    if (system.platform !== 'win32') {
        setupAlias();
    }
    
    // 总结
    log('\n=================================', 'blue');
    if (success) {
        log('  ✓ 安装完成！看门狗已启动', 'green');
        log('=================================\n', 'blue');
        log('查看状态：node ' + WATCHDOG_SCRIPT + ' status', 'blue');
        log('查看日志：tail -f ' + path.join(CONFIG_DIR, 'watchdog.log'), 'blue');
    } else {
        log('  ⚠ 安装完成（手动模式）', 'yellow');
        log('=================================\n', 'blue');
        log('请手动启动：node ' + WATCHDOG_SCRIPT + ' monitor &', 'blue');
    }
    
    log('\n提示：使用 oc 命令代替 openclaw 可自动备份配置\n');
}

main();
