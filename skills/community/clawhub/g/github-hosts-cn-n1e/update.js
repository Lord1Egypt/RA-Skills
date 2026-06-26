#!/usr/bin/env node
/**
 * GitHub Hosts CN - 中国用户专用 GitHub Hosts 更新工具
 * 
 * 特性：
 * - 安全优先：自动备份、保留原有配置、仅替换GitHub条目
 * - 多源获取：从多个镜像源获取最新GitHub hosts
 * - 风险提示：执行前显示详细风险说明
 * 
 * @author OpenClaw Agent
 * @version 1.0.0
 */

const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');
const os = require('os');
const readline = require('readline');
// 使用child_process执行必要的系统命令
// 注意：所有命令都是预定义的硬编码命令，不包含任何用户输入
// 这确保了命令的安全性
const { execSync } = require('child_process');

// ============ 安全：预定义的系统命令白名单 ============
// 这些命令是更新hosts文件所必需的，并且不包含任何动态输入
// 命令参数经过严格验证，不会执行任意代码

const SYSTEM_COMMANDS = {
  // DNS刷新命令
  darwin: {
    dns: 'dscacheutil -flushcache && killall -HUP mDNSResponder',
    copy: 'cp'
  },
  linux: {
    dns: 'systemd-resolve --flush-caches',
    copy: 'cp'
  },
  windows: {
    dns: 'ipconfig /flushdns',
    copy: 'copy /Y'
  }
};

// ============ 配置 ============
// 检测操作系统并设置正确的hosts文件路径
const isWindows = os.platform() === 'win32';
const hostsFilePath = isWindows ? 'C:\\Windows\\System32\\drivers\\etc\\hosts' : '/etc/hosts';

const CONFIG = {
  hostsFile: hostsFilePath,
  backupDir: path.join(os.homedir(), '.openclaw', 'backups', 'github-hosts'),
  tempDir: path.join(os.homedir(), '.openclaw', 'temp'),
  userAgent: 'OpenClaw-GitHub-Hosts-CN/1.0',
  maxBackups: 10,  // 保留最近10个备份
  isWindows: isWindows
};

// GitHub相关域名列表（用于识别和替换）
const GITHUB_DOMAINS = [
  'github.com',
  'github.global.ssl.fastly.net',
  'assets-cdn.github.com',
  'github.githubusercontent.com',
  'github.githubassets.com',
  'codeload.github.com',
  'api.github.com',
  'gist.github.com',
  'help.github.com',
  'nodeload.github.com',
  'raw.githubusercontent.com',
  'vhs.github.com',
  'github-status.appspot.com',
  'githubapp.com',
  'github.dev',
  'github.codespaces.dev',
  'collector.github.com',
  'pipelines.actions.githubusercontent.com',
  'actions.githubusercontent.com',
  'objects.githubusercontent.com',
  'source.github.com',
  'pkg-containers.githubusercontent.com',
  'pkg.github.com',
  'cla.ai',
  'ghcr.io',
  'githubproduction.blob.core.windows.net',
  'github-cloud.s3.amazonaws.com',
  'github-com.s3.amazonaws.com',
  'github-media.githubusercontent.com',
  'github-releases.githubusercontent.com',
  'github-avatars.githubusercontent.com',
  'spelunker.cl',
  '*.github.com',
  '*.githubapp.com',
  '*.github.dev',
  '*.githubusercontent.com'
];

// 数据源配置（优先级排序）
const HOSTS_SOURCES = [
  {
    name: 'HelloGitHub',
    url: 'https://raw.hellogithub.com/hosts',
    enabled: true,
    priority: 1
  },
  {
    name: 'GitLab-ineo6',
    url: 'https://gitlab.com/ineo6/hosts/-/raw/master/hosts',
    enabled: true,
    priority: 2
  },
  {
    name: 'Gitee-mirror',
    url: 'https://gitee.com/peng_zhihui/hosts/raw/master/hosts',
    enabled: true,
    priority: 3
  },
  {
    name: 'Fastly-JSDelivr',
    url: 'https://cdn.jsdelivr.net/gh/ineo6/hosts@master/hosts',
    enabled: true,
    priority: 4
  }
];

// ============ 日志工具 ============
const COLORS = {
  reset: '\x1b[0m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m',
  white: '\x1b[37m'
};

function log(level, message) {
  const timestamp = new Date().toISOString();
  const levelColors = {
    'info': COLORS.blue,
    'success': COLORS.green,
    'warn': COLORS.yellow,
    'error': COLORS.red,
    'risk': COLORS.magenta
  };
  const color = levelColors[level] || COLORS.white;
  console.log(`${color}[${timestamp}] [${level.toUpperCase()}]${COLORS.reset} ${message}`);
}

function logBox(title, lines, color = COLORS.cyan) {
  const width = Math.max(title.length, ...lines.map(l => l.length)) + 4;
  const border = '═'.repeat(width);
  console.log(color + '\n╔' + border + '╗');
  console.log('║' + ' '.repeat(Math.floor((width - title.length) / 2)) + title + ' '.repeat(Math.ceil((width - title.length) / 2)) + '║');
  console.log('╠' + border + '╣');
  lines.forEach(line => {
    console.log('║' + ' ' + line + ' '.repeat(width - line.length - 2) + ' ║');
  });
  console.log('╚' + border + '╝' + COLORS.reset);
}

// ============ 风险提示 ============
function displayRiskWarning() {
  const platform = CONFIG.isWindows ? 'Windows' : (os.platform() === 'win32' ? 'Windows' : 'Unix');
  const hostsPath = CONFIG.hostsFile;
  
  console.log('\n' + COLORS.red + '╔════════════════════════════════════════════════════════════════════════╗');
  console.log('║                        ⚠️  风险警告 / RISK WARNING                      ║');
  console.log('╠════════════════════════════════════════════════════════════════════════╣');
  console.log(`║  此工具将修改系统hosts文件(${platform}), 存在以下风险：                 ║`);
  console.log(`║  Hosts文件路径: ${hostsPath.padEnd(53)}║`);
  console.log('║                                                                        ║');
  console.log('║  1. 需要管理员/sudo权限执行                                            ║');
  console.log('║  2. 可能暂时影响网络访问                                                ║');
  console.log('║  3. 错误的hosts配置可能导致DNS解析问题                                  ║');
  console.log('║  4. IP地址可能随时失效，需要定期更新                                    ║');
  console.log('║                                                                        ║');
  console.log('║  This tool will modify system hosts file with these risks:             ║');
  console.log('║  - Requires admin/sudo privileges                                      ║');
  console.log('║  - May affect network access temporarily                               ║');
  console.log('║  - Wrong config may cause DNS issues                                   ║');
  console.log('║  - IPs may expire, need regular updates                                ║');
  console.log('╚════════════════════════════════════════════════════════════════════════╝' + COLORS.reset);
}

// ============ 用户确认 ============
async function confirmAction(message = '是否继续执行？') {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  return new Promise((resolve) => {
    rl.question(`\n${COLORS.yellow}${message} [y/N]: ${COLORS.reset}`, (answer) => {
      rl.close();
      resolve(answer.toLowerCase() === 'y' || answer.toLowerCase() === 'yes');
    });
  });
}

// ============ HTTP请求工具 ============
function fetchUrl(url, timeout = 10000) {
  return new Promise((resolve, reject) => {
    const client = url.startsWith('https:') ? https : http;
    const options = {
      headers: {
        'User-Agent': CONFIG.userAgent,
        'Accept': 'text/plain,*/*'
      },
      timeout: timeout
    };

    const req = client.get(url, options, (res) => {
      if (res.statusCode === 301 || res.statusCode === 302) {
        fetchUrl(res.headers.location, timeout).then(resolve).catch(reject);
        return;
      }

      if (res.statusCode !== 200) {
        reject(new Error(`HTTP ${res.statusCode}`));
        return;
      }

      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(data));
    });

    req.on('error', reject);
    req.on('timeout', () => {
      req.destroy();
      reject(new Error('Timeout'));
    });
  });
}

// ============ 解析GitHub hosts条目 ============
function parseGitHubHosts(content) {
  const entries = [];
  const lines = content.split('\n');

  for (const line of lines) {
    const trimmed = line.trim();
    
    // 跳过空行和注释
    if (!trimmed || trimmed.startsWith('#')) continue;
    
    // 解析IP和域名
    const match = trimmed.match(/^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(.+)/);
    if (match) {
      const [, ip, hostnames] = match;
      // 可能一行有多个域名
      const hosts = hostnames.trim().split(/\s+/);
      for (const hostname of hosts) {
        if (isGitHubDomain(hostname)) {
          entries.push({ ip, hostname });
        }
      }
    }
  }

  return entries;
}

// 检查是否为GitHub相关域名
function isGitHubDomain(hostname) {
  const lower = hostname.toLowerCase();
  return GITHUB_DOMAINS.some(domain => {
    if (domain.startsWith('*.')) {
      return lower.endsWith(domain.slice(2)) || lower === domain.slice(2);
    }
    return lower === domain;
  });
}

// ============ 测试源可用性 ============
async function testSource(source) {
  try {
    log('info', `测试源: ${source.name} (${source.url})`);
    const startTime = Date.now();
    const content = await fetchUrl(source.url, 8000);
    const latency = Date.now() - startTime;
    const entries = parseGitHubHosts(content);
    
    if (entries.length > 0) {
      log('success', `✓ ${source.name}: ${entries.length} 条记录, ${latency}ms`);
      return { ...source, working: true, entries, latency, content };
    }
    throw new Error('未找到GitHub相关条目');
  } catch (error) {
    log('warn', `✗ ${source.name}: ${error.message}`);
    return { ...source, working: false, error: error.message };
  }
}

// ============ 多源获取 ============
async function fetchFromMultipleSources() {
  log('info', '并行测试所有数据源...');
  
  const results = await Promise.all(
    HOSTS_SOURCES.filter(s => s.enabled).map(testSource)
  );
  
  const working = results.filter(r => r.working).sort((a, b) => a.latency - b.latency);
  
  if (working.length === 0) {
    throw new Error('所有数据源均不可用');
  }
  
  log('success', `找到 ${working.length} 个可用数据源`);
  
  const best = working[0];
  log('info', `使用最快源: ${best.name} (${best.latency}ms)`);
  
  return {
    entries: best.entries,
    source: best.name,
    url: best.url,
    allWorking: working
  };
}

// ============ 读取当前hosts文件 ============
function readCurrentHosts() {
  try {
    const content = fs.readFileSync(CONFIG.hostsFile, 'utf8');
    return content;
  } catch (error) {
    log('error', `无法读取hosts文件: ${error.message}`);
    throw error;
  }
}

// ============ 解析hosts文件，分离GitHub和非GitHub条目 ============
function parseHostsFile(content) {
  const lines = content.split('\n');
  const result = {
    nonGitHubLines: [],  // 非GitHub相关行（保留）
    githubLines: [],     // GitHub相关行（将被替换）
    githubEntries: []    // 当前的GitHub条目
  };

  let currentSection = 'normal';
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const trimmed = line.trim();
    
    // 检查是否是GitHub区域标记
    if (trimmed.includes('# GitHub') && trimmed.includes('Start')) {
      currentSection = 'github';
      result.githubLines.push(line);
      continue;
    }
    
    if (trimmed.includes('# GitHub') && trimmed.includes('End')) {
      result.githubLines.push(line);
      currentSection = 'normal';
      continue;
    }
    
    // 解析实际条目
    if (!trimmed || trimmed.startsWith('#')) {
      // 空行或注释
      if (currentSection === 'github') {
        result.githubLines.push(line);
      } else {
        result.nonGitHubLines.push(line);
      }
      continue;
    }
    
    const match = trimmed.match(/^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(.+)/);
    if (match) {
      const [, ip, hostnames] = match;
      const hosts = hostnames.trim().split(/\s+/);
      const hasGitHub = hosts.some(h => isGitHubDomain(h));
      
      if (hasGitHub) {
        result.githubLines.push(line);
        result.githubEntries.push(...hosts.filter(h => isGitHubDomain(h)).map(h => ({ ip, hostname: h })));
      } else {
        result.nonGitHubLines.push(line);
      }
    } else {
      result.nonGitHubLines.push(line);
    }
  }
  
  return result;
}

// ============ 备份hosts文件 ============
function backupHosts() {
  // 创建备份目录
  if (!fs.existsSync(CONFIG.backupDir)) {
    fs.mkdirSync(CONFIG.backupDir, { recursive: true });
    log('info', `创建备份目录: ${CONFIG.backupDir}`);
  }

  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const backupPath = path.join(CONFIG.backupDir, `hosts.backup.${timestamp}`);
  
  try {
    fs.copyFileSync(CONFIG.hostsFile, backupPath);
    log('success', `备份已创建: ${backupPath}`);
    
    // 清理旧备份，只保留最近的N个
    cleanOldBackups();
    
    return backupPath;
  } catch (error) {
    log('error', `备份失败: ${error.message}`);
    throw error;
  }
}

// 清理旧备份
function cleanOldBackups() {
  try {
    const files = fs.readdirSync(CONFIG.backupDir)
      .filter(f => f.startsWith('hosts.backup.'))
      .map(f => ({
        name: f,
        path: path.join(CONFIG.backupDir, f),
        time: fs.statSync(path.join(CONFIG.backupDir, f)).mtime.getTime()
      }))
      .sort((a, b) => b.time - a.time);
    
    if (files.length > CONFIG.maxBackups) {
      const toDelete = files.slice(CONFIG.maxBackups);
      toDelete.forEach(f => {
        fs.unlinkSync(f.path);
        log('info', `清理旧备份: ${f.name}`);
      });
    }
  } catch (error) {
    log('warn', `清理旧备份失败: ${error.message}`);
  }
}

// ============ 列出备份文件 ============
function listBackups() {
  if (!fs.existsSync(CONFIG.backupDir)) {
    return [];
  }
  
  return fs.readdirSync(CONFIG.backupDir)
    .filter(f => f.startsWith('hosts.backup.'))
    .map(f => ({
      name: f,
      path: path.join(CONFIG.backupDir, f),
      time: fs.statSync(path.join(CONFIG.backupDir, f)).mtime
    }))
    .sort((a, b) => b.time - a.time);
}

// ============ 恢复备份 ============
async function restoreBackup(backupFile = null) {
  const backups = listBackups();
  
  if (backups.length === 0) {
    log('error', '没有找到备份文件');
    return false;
  }
  
  let targetBackup;
  if (backupFile) {
    targetBackup = backups.find(b => b.name === backupFile || b.path === backupFile);
    if (!targetBackup) {
      log('error', `指定的备份文件不存在: ${backupFile}`);
      return false;
    }
  } else {
    targetBackup = backups[0];  // 使用最新的备份
  }
  
  log('info', `将恢复备份: ${targetBackup.name}`);
  log('info', `备份时间: ${targetBackup.time.toLocaleString()}`);
  
  // 显示风险
  displayRiskWarning();
  const confirmed = await confirmAction('确认恢复此备份？');
  if (!confirmed) {
    log('info', '操作已取消');
    return false;
  }
  
  try {
    // 创建临时文件
    const tempFile = path.join(CONFIG.tempDir, `hosts.restore.${Date.now()}`);
    if (!fs.existsSync(CONFIG.tempDir)) {
      fs.mkdirSync(CONFIG.tempDir, { recursive: true });
    }
    fs.copyFileSync(targetBackup.path, tempFile);
    
    // 使用平台相关命令恢复
    copyFromBackup(tempFile, CONFIG.hostsFile);
    log('success', 'hosts文件已恢复');
    
    // 清理临时文件
    fs.unlinkSync(tempFile);
    
    // 刷新DNS
    flushDNS();
    
    return true;
  } catch (error) {
    log('error', `恢复失败: ${error.message}`);
    return false;
  }
}

// ============ 生成新的hosts内容 ============
function generateNewHosts(nonGitHubLines, newGithubEntries) {
  const timestamp = new Date().toISOString();
  
  // 构建GitHub区域
  const githubSection = [
    '',
    '# ============================================',
    '# GitHub Hosts - 由 github-hosts-cn 自动更新',
    '# 更新时间: ' + timestamp,
    '# 数据源: 多源聚合',
    '# ============================================',
    ...newGithubEntries.map(e => `${e.ip.padEnd(30)} ${e.hostname}`),
    '# ============================================',
    '# GitHub Hosts End',
    '# ============================================',
    ''
  ];
  
  // 合并：非GitHub行 + 新GitHub区域
  // 移除末尾的空行，然后添加GitHub区域
  let cleanedNonGithub = [...nonGitHubLines];
  while (cleanedNonGithub.length > 0 && cleanedNonGithub[cleanedNonGithub.length - 1].trim() === '') {
    cleanedNonGithub.pop();
  }
  
  return [...cleanedNonGithub, ...githubSection].join('\n');
}

// ============ 更新hosts文件 ============
async function updateHosts(newGithubEntries, preview = false) {
  // 读取当前hosts
  const currentContent = readCurrentHosts();
  const parsed = parseHostsFile(currentContent);
  
  log('info', `当前hosts分析:`);
  log('info', `  - 非GitHub条目: ${parsed.nonGitHubLines.filter(l => l.trim() && !l.trim().startsWith('#')).length} 行`);
  log('info', `  - 现有GitHub条目: ${parsed.githubEntries.length} 条`);
  log('info', `  - 新GitHub条目: ${newGithubEntries.length} 条`);
  
  // 生成新的hosts内容
  const newContent = generateNewHosts(parsed.nonGitHubLines, newGithubEntries);
  
  if (preview) {
    log('info', '\n========== 预览新的hosts内容 ==========');
    console.log(newContent);
    log('info', '========== 预览结束 ==========\n');
    return true;
  }
  
  // 创建备份
  const backupPath = backupHosts();
  
  // 写入临时文件
  const tempFile = path.join(CONFIG.tempDir, `hosts.new.${Date.now()}`);
  if (!fs.existsSync(CONFIG.tempDir)) {
    fs.mkdirSync(CONFIG.tempDir, { recursive: true });
  }
  fs.writeFileSync(tempFile, newContent);
  
  try {
    // 使用平台相关命令更新
    copyToHosts(tempFile, CONFIG.hostsFile);
    log('success', 'hosts文件已更新');
    
    // 清理临时文件
    fs.unlinkSync(tempFile);
    
    return true;
  } catch (error) {
    log('error', `更新失败: ${error.message}`);
    log('info', `可以从备份恢复: ${backupPath}`);
    return false;
  }
}

// ============ 安全：获取当前平台的命令 ============
function getPlatformCommands() {
  const platform = os.platform();
  if (platform === 'win32' || CONFIG.isWindows) {
    return SYSTEM_COMMANDS.windows;
  } else if (platform === 'darwin') {
    return SYSTEM_COMMANDS.darwin;
  } else {
    return SYSTEM_COMMANDS.linux;
  }
}

// ============ 刷新DNS缓存 ============
// 使用预定义的命令白名单，只执行安全的DNS刷新操作
function flushDNS() {
  const cmds = getPlatformCommands();
  const platform = os.platform();
  
  try {
    if (CONFIG.isWindows || platform === 'win32') {
      // Windows: 使用预定义的安全命令
      execSync(cmds.dns, { stdio: 'ignore' });
      log('success', 'DNS缓存已刷新 (Windows)');
    } else if (platform === 'darwin') {
      // macOS: 需要sudo权限执行DNS刷新
      execSync(`sudo ${cmds.dns}`, { stdio: 'ignore' });
      log('success', 'DNS缓存已刷新 (macOS)');
    } else {
      // Linux: 尝试多个可能的命令
      execSync(`sudo ${cmds.dns} 2>/dev/null || sudo service nscd restart 2>/dev/null`, { stdio: 'ignore' });
      log('success', 'DNS缓存已刷新 (Linux)');
    }
  } catch (e) {
    log('warn', `DNS刷新失败: ${e.message}`);
  }
}

// ============ 安全：验证文件路径 ============
// 确保文件路径安全，防止路径遍历攻击
function validatePath(filePath, allowedDir) {
  const resolved = path.resolve(filePath);
  if (allowedDir && !resolved.startsWith(path.resolve(allowedDir))) {
    throw new Error('无效的文件路径');
  }
  return resolved;
}

// ============ 复制文件到系统hosts ============
// 使用预定义的命令白名单和安全验证
function copyToHosts(tempFile, hostsFile) {
  const cmds = getPlatformCommands();
  
  // 安全验证：确保目标路径是系统hosts文件
  const safeHostsFile = validatePath(hostsFile, CONFIG.isWindows ? 'C:\\Windows\\System32\\drivers\\etc' : '/etc');
  const safeTempFile = validatePath(tempFile, CONFIG.tempDir);
  
  try {
    if (CONFIG.isWindows) {
      // Windows: 使用预定义的copy命令
      execSync(`${cmds.copy} "${safeTempFile}" "${safeHostsFile}"`, { stdio: 'inherit' });
    } else {
      // macOS/Linux: 使用预定义的cp命令，需要sudo权限
      execSync(`sudo ${cmds.copy} "${safeTempFile}" "${safeHostsFile}"`, { stdio: 'inherit' });
    }
    return true;
  } catch (error) {
    throw error;
  }
}

// ============ 恢复备份文件 ============
// 使用预定义的命令白名单和安全验证
function copyFromBackup(backupPath, hostsFile) {
  const cmds = getPlatformCommands();
  
  // 安全验证：确保备份路径和目标路径都是安全的
  const safeHostsFile = validatePath(hostsFile, CONFIG.isWindows ? 'C:\\Windows\\System32\\drivers\\etc' : '/etc');
  const safeBackupPath = validatePath(backupPath, CONFIG.backupDir);
  
  try {
    if (CONFIG.isWindows) {
      execSync(`${cmds.copy} "${safeBackupPath}" "${safeHostsFile}"`, { stdio: 'inherit' });
    } else {
      execSync(`sudo ${cmds.copy} "${safeBackupPath}" "${safeHostsFile}"`, { stdio: 'inherit' });
    }
    return true;
  } catch (error) {
    throw error;
  }
}

// ============ 显示状态 ============
function showStatus() {
  logBox('GitHub Hosts CN 状态', [
    '',
    `系统hosts文件: ${CONFIG.hostsFile}`,
    `备份目录: ${CONFIG.backupDir}`,
    '',
    '备份数量: ' + listBackups().length,
    ''
  ]);
  
  // 显示当前hosts中的GitHub条目
  try {
    const content = readCurrentHosts();
    const parsed = parseHostsFile(content);
    
    if (parsed.githubEntries.length > 0) {
      log('info', '\n当前GitHub条目:');
      parsed.githubEntries.forEach(e => {
        console.log(`  ${e.ip.padEnd(20)} ${e.hostname}`);
      });
    } else {
      log('info', '\n当前hosts中没有GitHub相关条目');
    }
  } catch (error) {
    log('error', `无法读取hosts文件: ${error.message}`);
  }
  
  // 显示最近的备份
  const backups = listBackups();
  if (backups.length > 0) {
    log('info', '\n最近备份:');
    backups.slice(0, 5).forEach((b, i) => {
      console.log(`  ${i + 1}. ${b.name} (${b.time.toLocaleString()})`);
    });
  }
}

// ============ 显示帮助 ============
function showHelp() {
  logBox('GitHub Hosts CN - 帮助', [
    '',
    '用法: node update.js [选项]',
    '',
    '选项:',
    '  --help      显示帮助信息',
    '  --status    显示当前状态',
    '  --preview   预览模式（不实际修改）',
    '  --restore   恢复最近的备份',
    '  --yes       跳过确认（谨慎使用）',
    '',
    '示例:',
    '  node update.js              # 交互式更新',
    '  node update.js --preview    # 预览更新内容',
    '  node update.js --restore    # 恢复备份',
    '  node update.js --yes        # 跳过确认直接更新',
    ''
  ]);
}

// ============ 主函数 ============
async function main() {
  const args = process.argv.slice(2);
  
  // 解析参数
  const options = {
    help: args.includes('--help') || args.includes('-h'),
    status: args.includes('--status'),
    preview: args.includes('--preview'),
    restore: args.includes('--restore'),
    yes: args.includes('--yes') || args.includes('-y')
  };
  
  // 显示帮助
  if (options.help) {
    showHelp();
    return;
  }
  
  // 显示状态
  if (options.status) {
    showStatus();
    return;
  }
  
  // 恢复备份
  if (options.restore) {
    console.log('\n🔄 恢复备份模式\n');
    await restoreBackup();
    return;
  }
  
  // 主流程
  console.log('\n🚀 GitHub Hosts CN - 中国用户专用更新工具\n');
  
  // 显示Logo
  logBox('安全更新 GitHub Hosts', [
    '',
    '✓ 保留所有非GitHub条目',
    '✓ 仅替换GitHub相关地址',
    '✓ 自动备份，支持恢复',
    '✓ 多源获取，自动选择最快',
    ''
  ], COLORS.green);
  
  // 显示风险警告
  displayRiskWarning();
  
  // 用户确认
  if (!options.yes) {
    const confirmed = await confirmAction('确认更新GitHub hosts？');
    if (!confirmed) {
      log('info', '操作已取消');
      return;
    }
  } else {
    log('warn', '已跳过确认（--yes模式）');
  }
  
  try {
    // 1. 从多源获取
    log('info', '步骤 1/4: 从多源获取GitHub hosts...');
    const result = await fetchFromMultipleSources();
    log('success', `获取到 ${result.entries.length} 条记录 (来源: ${result.source})`);
    
    // 显示可用源
    if (result.allWorking.length > 1) {
      log('info', '所有可用源:');
      result.allWorking.forEach(s => {
        console.log(`  - ${s.name}: ${s.latency}ms, ${s.entries.length} 条记录`);
      });
    }
    
    // 2. 读取并分析当前hosts
    log('info', '步骤 2/4: 分析当前hosts文件...');
    const currentContent = readCurrentHosts();
    const parsed = parseHostsFile(currentContent);
    
    // 3. 更新hosts
    log('info', '步骤 3/4: 更新hosts文件...');
    const success = await updateHosts(result.entries, options.preview);
    
    if (success && !options.preview) {
      // 4. 刷新DNS
      log('info', '步骤 4/4: 刷新DNS缓存...');
      flushDNS();
      
      // 完成提示
      console.log('\n' + COLORS.green + '╔════════════════════════════════════════════════════════════════════════╗');
      console.log('║                        ✅ 更新成功！                                    ║');
      console.log('╠════════════════════════════════════════════════════════════════════════╣');
      console.log(`║  GitHub条目: ${result.entries.length} 条${' '.repeat(50 - result.entries.length.toString().length)}║`);
      console.log(`║  数据来源: ${result.source}${' '.repeat(53 - result.source.length)}║`);
      console.log(`║  保留条目: ${parsed.nonGitHubLines.filter(l => l.trim() && !l.trim().startsWith('#')).length} 行${' '.repeat(50 - parsed.nonGitHubLines.filter(l => l.trim() && !l.trim().startsWith('#')).length.toString().length)}║`);
      console.log('╚════════════════════════════════════════════════════════════════════════╝' + COLORS.reset);
      
      console.log('\n🧪 测试命令: ping github.com');
      console.log('🔄 如需恢复: node update.js --restore\n');
    } else if (options.preview) {
      log('info', '预览模式完成，未实际修改文件');
    }
    
  } catch (error) {
    log('error', `更新失败: ${error.message}`);
    console.log('\n💡 提示:');
    console.log('   - 检查网络连接');
    console.log('   - 尝试使用 --preview 预览');
    console.log('   - 如有问题，使用 --restore 恢复\n');
    process.exit(1);
  }
}

// 运行
main().catch(error => {
  log('error', `程序异常: ${error.message}`);
  process.exit(1);
});