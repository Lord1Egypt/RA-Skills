#!/usr/bin/env node

/**
 * OpenClaw 监控告警系统
 * 
 * 功能：
 * 1. 监控子代理运行状态
 * 2. 监控配额使用情况
 * 3. 实现飞书消息告警
 * 4. 配置告警阈值
 */

const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');
const https = require('https');

// 路径配置
const HOME = process.env.HOME || '/home/user';
const WORKSPACE = path.join(HOME, '.openclaw', 'workspace');
const OPENCLAW_DIR = path.join(HOME, '.openclaw');

// 文件路径
const CONFIG_FILE = path.join(WORKSPACE, 'monitoring', 'alert-config.json');
const STATE_FILE = path.join(WORKSPACE, 'monitoring', 'monitor-state.json');
const ALERT_LOG_FILE = path.join(WORKSPACE, 'logs', 'alert.log');
const RUNS_FILE = path.join(OPENCLAW_DIR, 'subagents', 'runs.json');
const QUOTA_DB_FILE = path.join(OPENCLAW_DIR, 'skills', 'multi-user-privacy', '.quota-db.json');
const OPENCLAW_CONFIG = path.join(OPENCLAW_DIR, 'openclaw.json');

/**
 * 日志记录
 */
function log(message, level = 'INFO') {
  const timestamp = new Date().toISOString().replace('T', ' ').slice(0, 19);
  const logLine = `[${timestamp}] [${level}] ${message}`;
  console.log(logLine);
  
  // 写入日志文件
  const logDir = path.dirname(ALERT_LOG_FILE);
  if (!fs.existsSync(logDir)) {
    fs.mkdirSync(logDir, { recursive: true });
  }
  fs.appendFileSync(ALERT_LOG_FILE, logLine + '\n');
}

/**
 * 读取 JSON 文件
 */
function readJsonFile(filePath) {
  try {
    if (!fs.existsSync(filePath)) {
      return null;
    }
    const content = fs.readFileSync(filePath, 'utf8');
    return JSON.parse(content);
  } catch (error) {
    log(`读取文件失败 ${filePath}: ${error.message}`, 'ERROR');
    return null;
  }
}

/**
 * 写入 JSON 文件
 */
function writeJsonFile(filePath, data) {
  try {
    const dir = path.dirname(filePath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf8');
    return true;
  } catch (error) {
    log(`写入文件失败 ${filePath}: ${error.message}`, 'ERROR');
    return false;
  }
}

/**
 * 发送飞书消息
 */
async function sendFeishuAlert(message, title = '监控告警') {
  try {
    const config = readJsonFile(CONFIG_FILE);
    if (!config || !config.notification.enabled) {
      log('告警通知已禁用', 'WARN');
      return false;
    }

    const openclawConfig = readJsonFile(OPENCLAW_CONFIG);
    if (!openclawConfig || !openclawConfig.channels || !openclawConfig.channels.feishu) {
      log('飞书渠道未配置', 'ERROR');
      return false;
    }

    const { appId, appSecret } = openclawConfig.channels.feishu;
    
    // 获取 tenant_access_token
    const tenantToken = await getTenantAccessToken(appId, appSecret);
    if (!tenantToken) {
      log('获取 tenant_access_token 失败', 'ERROR');
      return false;
    }

    // 发送消息
    const recipientUserId = config.notification.recipientUserId || 'ou_b96f5424607baf3a0455b55e0f4a2213';
    
    const messageData = {
      receive_id: recipientUserId,
      msg_type: 'interactive',
      content: JSON.stringify({
        config: {
          wide_screen_mode: true
        },
        header: {
          template: 'red',
          title: {
            tag: 'plain_text',
            content: `🚨 ${title}`
          }
        },
        elements: [
          {
            tag: 'markdown',
            content: message
          }
        ]
      })
    };

    const result = await makeRequest(
      'POST',
      'https://open.feishu.cn/open-apis/im/v1/messages',
      {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${tenantToken}`
      },
      messageData
    );

    if (result && result.code === 0) {
      log(`飞书告警发送成功：${title}`, 'INFO');
      return true;
    } else {
      log(`飞书告警发送失败：${result?.msg || '未知错误'}`, 'ERROR');
      return false;
    }
  } catch (error) {
    log(`发送飞书消息异常：${error.message}`, 'ERROR');
    return false;
  }
}

/**
 * 获取 tenant_access_token
 */
async function getTenantAccessToken(appId, appSecret) {
  try {
    const result = await makeRequest(
      'POST',
      'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal',
      { 'Content-Type': 'application/json' },
      { app_id: appId, app_secret: appSecret }
    );
    
    if (result && result.code === 0) {
      return result.tenant_access_token;
    }
    return null;
  } catch (error) {
    log(`获取 tenant_access_token 失败：${error.message}`, 'ERROR');
    return null;
  }
}

/**
 * HTTP 请求封装
 */
function makeRequest(method, url, headers, data) {
  return new Promise((resolve, reject) => {
    const urlObj = new URL(url);
    const options = {
      hostname: urlObj.hostname,
      port: 443,
      path: urlObj.pathname + urlObj.search,
      method: method,
      headers: headers
    };

    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(body));
        } catch (e) {
          resolve(body);
        }
      });
    });

    req.on('error', reject);
    
    if (data) {
      req.write(JSON.stringify(data));
    }
    req.end();
  });
}

/**
 * 监控子代理运行状态
 */
function monitorSubagents() {
  log('检查子代理运行状态...', 'INFO');
  
  const runsData = readJsonFile(RUNS_FILE);
  if (!runsData || !runsData.runs) {
    log('未找到子代理运行记录', 'WARN');
    return { status: 'unknown', active: 0, alerts: [] };
  }

  const config = readJsonFile(CONFIG_FILE);
  const thresholds = config?.thresholds?.subagents || {};
  
  const now = Date.now();
  const maxRunningTimeMs = (thresholds.maxRunningTimeHours || 2) * 60 * 60 * 1000;
  const stuckThresholdMs = (thresholds.stuckThresholdMinutes || 30) * 60 * 1000;
  
  const activeRuns = [];
  const alerts = [];
  
  for (const [runId, run] of Object.entries(runsData.runs)) {
    if (!run.startedAt) continue;
    
    const runningTime = now - run.startedAt;
    const runningTimeHours = (runningTime / (60 * 60 * 1000)).toFixed(2);
    
    // 检查运行时间是否超限
    if (runningTime > maxRunningTimeMs) {
      alerts.push({
        type: 'subagent_timeout',
        runId,
        label: run.label || 'Unknown',
        task: run.task?.slice(0, 50) || 'Unknown',
        runningTimeHours,
        message: `子代理运行超时 (${runningTimeHours}h)`
      });
    }
    
    // 检查是否应该归档但未归档
    const archiveAtMs = run.archiveAtMs || 0;
    if (archiveAtMs > 0 && now > archiveAtMs && !run.cleanupHandled) {
      alerts.push({
        type: 'subagent_stuck',
        runId,
        label: run.label || 'Unknown',
        message: '子代理已完成但未清理'
      });
    }
    
    activeRuns.push({
      runId,
      label: run.label,
      task: run.task,
      runningTimeHours,
      createdAt: new Date(run.createdAt).toISOString()
    });
  }
  
  // 检查并发数是否超限
  const maxConcurrent = thresholds.maxConcurrent || 10;
  if (activeRuns.length > maxConcurrent) {
    alerts.push({
      type: 'subagent_concurrent_exceeded',
      count: activeRuns.length,
      max: maxConcurrent,
      message: `并发子代理数超限 (${activeRuns.length}/${maxConcurrent})`
    });
  }
  
  log(`发现 ${activeRuns.length} 个活跃子代理，${alerts.length} 个告警`, 'INFO');
  
  return {
    status: 'ok',
    active: activeRuns.length,
    runs: activeRuns,
    alerts
  };
}

/**
 * 监控配额使用情况
 */
function monitorQuotas() {
  log('检查配额使用情况...', 'INFO');
  
  const quotaData = readJsonFile(QUOTA_DB_FILE);
  if (!quotaData) {
    log('未找到配额数据', 'WARN');
    return { status: 'unknown', users: [], alerts: [] };
  }

  const config = readJsonFile(CONFIG_FILE);
  const thresholds = config?.thresholds?.quota || {};
  
  const tokenThreshold = thresholds.tokenUsagePercent || 80;
  const messageThreshold = thresholds.messageUsagePercent || 80;
  const diskThreshold = thresholds.diskUsagePercent || 80;
  
  const alerts = [];
  const users = [];
  
  for (const [userId, quota] of Object.entries(quotaData)) {
    const userQuotas = {
      userId,
      tokenUsage: 0,
      messageUsage: 0,
      diskUsage: 0,
      alerts: []
    };
    
    // 计算 Token 使用率
    if (quota.tokenQuota && quota.used?.tokens !== undefined) {
      const tokenPercent = Math.round((quota.used.tokens / quota.tokenQuota) * 100);
      userQuotas.tokenUsage = tokenPercent;
      
      if (tokenPercent >= 100) {
        alerts.push({
          type: 'quota_exceeded',
          userId,
          resource: 'token',
          usage: quota.used.tokens,
          quota: quota.tokenQuota,
          percent: tokenPercent,
          message: `Token 配额已用尽 (${quota.used.tokens}/${quota.tokenQuota})`
        });
      } else if (tokenPercent >= tokenThreshold) {
        alerts.push({
          type: 'quota_warning',
          userId,
          resource: 'token',
          usage: quota.used.tokens,
          quota: quota.tokenQuota,
          percent: tokenPercent,
          message: `Token 配额即将用尽 (${tokenPercent}%)`
        });
      }
    }
    
    // 计算消息使用率
    if (quota.messageQuota && quota.used?.messages !== undefined) {
      const messagePercent = Math.round((quota.used.messages / quota.messageQuota) * 100);
      userQuotas.messageUsage = messagePercent;
      
      if (messagePercent >= 100) {
        alerts.push({
          type: 'quota_exceeded',
          userId,
          resource: 'message',
          usage: quota.used.messages,
          quota: quota.messageQuota,
          percent: messagePercent,
          message: `消息配额已用尽 (${quota.used.messages}/${quota.messageQuota})`
        });
      } else if (messagePercent >= messageThreshold) {
        alerts.push({
          type: 'quota_warning',
          userId,
          resource: 'message',
          usage: quota.used.messages,
          quota: quota.messageQuota,
          percent: messagePercent,
          message: `消息配额即将用尽 (${messagePercent}%)`
        });
      }
    }
    
    // 计算磁盘使用率
    if (quota.diskQuotaMB && quota.used?.disk !== undefined) {
      const diskPercent = Math.round((quota.used.disk / quota.diskQuotaMB) * 100);
      userQuotas.diskUsage = diskPercent;
      
      if (diskPercent >= 100) {
        alerts.push({
          type: 'quota_exceeded',
          userId,
          resource: 'disk',
          usage: quota.used.disk,
          quota: quota.diskQuotaMB,
          percent: diskPercent,
          message: `磁盘配额已用尽 (${quota.used.disk}MB/${quota.diskQuotaMB}MB)`
        });
      } else if (diskPercent >= diskThreshold) {
        alerts.push({
          type: 'quota_warning',
          userId,
          resource: 'disk',
          usage: quota.used.disk,
          quota: quota.diskQuotaMB,
          percent: diskPercent,
          message: `磁盘配额即将用尽 (${diskPercent}%)`
        });
      }
    }
    
    users.push(userQuotas);
  }
  
  log(`检查 ${users.length} 个用户配额，${alerts.length} 个告警`, 'INFO');
  
  return {
    status: 'ok',
    users,
    alerts
  };
}

/**
 * 监控 Gateway 健康状态
 */
async function monitorGateway() {
  log('检查 Gateway 健康状态...', 'INFO');
  
  const config = readJsonFile(CONFIG_FILE);
  const gatewayConfig = config?.thresholds?.gateway || {};
  
  if (!gatewayConfig.checkHealth) {
    log('Gateway 健康检查已禁用', 'INFO');
    return { status: 'disabled', healthy: true, alerts: [] };
  }
  
  const endpoint = gatewayConfig.healthEndpoint || 'http://localhost:3000/health';
  const consecutiveFailuresThreshold = gatewayConfig.consecutiveFailures || 3;
  
  // 读取之前的失败计数
  const state = readJsonFile(STATE_FILE) || {};
  const gatewayFailures = state.gatewayFailures || 0;
  
  try {
    // 简化的健康检查 - 检查进程是否运行
    const watchdogState = readJsonFile(path.join(WORKSPACE, 'watchdog-state.json'));
    const isRunning = watchdogState?.isGatewayRunning || false;
    
    if (isRunning) {
      // 重置失败计数
      if (gatewayFailures > 0) {
        state.gatewayFailures = 0;
        writeJsonFile(STATE_FILE, state);
      }
      
      log('Gateway 运行正常', 'INFO');
      return { status: 'ok', healthy: true, alerts: [] };
    } else {
      const newFailures = gatewayFailures + 1;
      state.gatewayFailures = newFailures;
      writeJsonFile(STATE_FILE, state);
      
      const alerts = [];
      if (newFailures >= consecutiveFailuresThreshold) {
        alerts.push({
          type: 'gateway_down',
          failures: newFailures,
          message: `Gateway 已宕机 (连续失败 ${newFailures} 次)`
        });
        log(`Gateway 宕机 (连续失败 ${newFailures} 次)`, 'ERROR');
      } else {
        log(`Gateway 健康检查失败 (${newFailures}/${consecutiveFailuresThreshold})`, 'WARN');
      }
      
      return { status: 'unhealthy', healthy: false, alerts };
    }
  } catch (error) {
    const newFailures = gatewayFailures + 1;
    state.gatewayFailures = newFailures;
    writeJsonFile(STATE_FILE, state);
    
    log(`Gateway 健康检查异常：${error.message}`, 'ERROR');
    return { 
      status: 'error', 
      healthy: false, 
      alerts: [{
        type: 'gateway_error',
        error: error.message,
        message: `Gateway 健康检查异常：${error.message}`
      }]
    };
  }
}

/**
 * 格式化告警消息
 */
function formatAlertMessage(alerts) {
  if (alerts.length === 0) {
    return null;
  }
  
  let message = '**监控告警**\n\n';
  
  // 按类型分组
  const grouped = {};
  for (const alert of alerts) {
    if (!grouped[alert.type]) {
      grouped[alert.type] = [];
    }
    grouped[alert.type].push(alert);
  }
  
  for (const [type, typeAlerts] of Object.entries(grouped)) {
    switch (type) {
      case 'subagent_timeout':
        message += '⏰ **子代理运行超时**\n';
        for (const alert of typeAlerts) {
          message += `- ${alert.label || 'Unknown'}: ${alert.runningTimeHours}h\n`;
        }
        message += '\n';
        break;
        
      case 'subagent_stuck':
        message += '🔒 **子代理卡住**\n';
        for (const alert of typeAlerts) {
          message += `- ${alert.label || 'Unknown'}: ${alert.message}\n`;
        }
        message += '\n';
        break;
        
      case 'subagent_concurrent_exceeded':
        message += `🚦 **并发数超限**: ${typeAlerts[0].count}/${typeAlerts[0].max}\n\n`;
        break;
        
      case 'quota_warning':
        message += '⚠️ **配额即将用尽**\n';
        for (const alert of typeAlerts) {
          message += `- ${alert.userId.slice(0, 8)}... ${alert.resource}: ${alert.percent}%\n`;
        }
        message += '\n';
        break;
        
      case 'quota_exceeded':
        message += '❌ **配额已用尽**\n';
        for (const alert of typeAlerts) {
          message += `- ${alert.userId.slice(0, 8)}... ${alert.resource}: ${alert.usage}/${alert.quota}\n`;
        }
        message += '\n';
        break;
        
      case 'gateway_down':
        message += `💥 **Gateway 宕机**: ${typeAlerts[0].message}\n\n`;
        break;
        
      default:
        for (const alert of typeAlerts) {
          message += `- ${alert.message}\n`;
        }
        message += '\n';
    }
  }
  
  message += `\n_时间：${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}_`;
  
  return message;
}

/**
 * 执行一次完整监控
 */
async function runMonitor() {
  log('========== 开始监控检查 ==========', 'INFO');
  
  const allAlerts = [];
  
  // 1. 监控子代理
  const subagentResult = monitorSubagents();
  allAlerts.push(...subagentResult.alerts);
  
  // 2. 监控配额
  const quotaResult = monitorQuotas();
  allAlerts.push(...quotaResult.alerts);
  
  // 3. 监控 Gateway
  const gatewayResult = await monitorGateway();
  allAlerts.push(...gatewayResult.alerts);
  
  // 4. 发送告警
  if (allAlerts.length > 0) {
    const message = formatAlertMessage(allAlerts);
    if (message) {
      await sendFeishuAlert(message, `监控告警 (${allAlerts.length}项)`);
    }
  } else {
    log('本次检查无告警', 'INFO');
  }
  
  // 5. 更新状态
  const state = {
    lastCheck: new Date().toISOString(),
    subagents: {
      active: subagentResult.active,
      status: subagentResult.status
    },
    quotas: {
      usersChecked: quotaResult.users?.length || 0,
      status: quotaResult.status
    },
    gateway: gatewayResult,
    alertsCount: allAlerts.length,
    lastAlerts: allAlerts
  };
  
  writeJsonFile(STATE_FILE, state);
  
  log('========== 监控检查完成 ==========', 'INFO');
  
  return state;
}

/**
 * 持续监控模式
 */
function startMonitoring() {
  const config = readJsonFile(CONFIG_FILE);
  const intervalSeconds = config?.checkIntervalSeconds || 60;
  
  log(`启动监控服务，检查间隔：${intervalSeconds}秒`, 'INFO');
  
  // 立即执行一次
  runMonitor();
  
  // 定时执行
  setInterval(() => {
    runMonitor();
  }, intervalSeconds * 1000);
}

/**
 * 显示状态
 */
function showStatus() {
  const state = readJsonFile(STATE_FILE);
  const config = readJsonFile(CONFIG_FILE);
  
  console.log('\n📊 OpenClaw 监控状态\n');
  console.log('═'.repeat(50));
  
  if (state) {
    console.log(`最后检查：${state.lastCheck ? new Date(state.lastCheck).toLocaleString('zh-CN') : '无'}`);
    console.log(`子代理状态：${state.subagents?.status || 'unknown'} (${state.subagents?.active || 0} 个活跃)`);
    console.log(`配额检查：${state.quotas?.status || 'unknown'} (${state.quotas?.usersChecked || 0} 个用户)`);
    console.log(`Gateway 状态：${state.gateway?.healthy ? '✅ 正常' : '❌ 异常'}`);
    console.log(`当前告警：${state.alertsCount || 0} 项`);
  } else {
    console.log('暂无监控数据');
  }
  
  console.log('\n配置信息:');
  console.log(`检查间隔：${config?.checkIntervalSeconds || 60}秒`);
  console.log(`告警通知：${config?.notification?.enabled ? '✅ 已启用' : '❌ 已禁用'}`);
  console.log('═'.repeat(50) + '\n');
}

// 主程序
const args = process.argv.slice(2);
const command = args[0];

switch (command) {
  case 'start':
    startMonitoring();
    break;
    
  case 'check':
  case 'run':
    runMonitor().then(() => {
      process.exit(0);
    });
    break;
    
  case 'status':
    showStatus();
    break;
    
  case 'help':
  case '-h':
  case '--help':
  default:
    console.log(`
📊 OpenClaw 监控告警系统

用法：node monitor.js <命令>

命令:
  start     启动持续监控服务
  check     执行一次监控检查
  status    查看监控状态
  help      显示帮助信息

示例:
  node monitor.js start    # 启动监控服务
  node monitor.js check    # 执行一次检查
  node monitor.js status   # 查看状态
`);
}
