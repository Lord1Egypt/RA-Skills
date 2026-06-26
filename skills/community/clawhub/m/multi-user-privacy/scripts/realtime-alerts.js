#!/usr/bin/env node

/**
 * 实时告警监控器
 * 
 * 功能：
 * 1. 实时监控告警日志
 * 2. 发送通知给管理员
 * 3. 生成告警统计
 * 
 * 用法：
 * node scripts/realtime-alerts.js              # 启动监控
 * node scripts/realtime-alerts.js --list       # 查看未处理告警
 * node scripts/realtime-alerts.js --ack=xxx    # 确认告警
 */

const fs = require('fs');
const path = require('path');

const ALERT_LOG = path.join(process.env.HOME, '.openclaw/logs/privacy-alerts.json');
const BEHAVIOR_DB = path.join(process.env.HOME, '.openclaw/logs/behavior-db.json');

// 告警类型
const ALERT_TYPES = {
  PRIVACY_VIOLATION: '隐私违规',
  SUSPICIOUS_ACTIVITY: '可疑行为',
  UNAUTHORIZED_ACCESS: '未授权访问',
  RATE_LIMIT_EXCEEDED: '频率超限'
};

/**
 * 加载告警数据
 */
function loadAlerts() {
  try {
    if (fs.existsSync(ALERT_LOG)) {
      const content = fs.readFileSync(ALERT_LOG, 'utf-8');
      return content.split('\n').filter(l => l.trim()).map(l => JSON.parse(l));
    }
  } catch (e) {
    console.error('加载告警日志失败:', e.message);
  }
  return [];
}

/**
 * 加载行为数据库
 */
function loadBehaviorDB() {
  try {
    if (fs.existsSync(BEHAVIOR_DB)) {
      return JSON.parse(fs.readFileSync(BEHAVIOR_DB, 'utf-8'));
    }
  } catch (e) {
    // 忽略
  }
  return { users: {}, alerts: [] };
}

/**
 * 发送告警通知（可扩展为邮件、短信、Webhook 等）
 */
function sendAlertNotification(alert) {
  const alertType = ALERT_TYPES[alert.type] || alert.type;
  
  console.log('\n' + '='.repeat(60));
  console.log('🚨 隐私安全告警');
  console.log('='.repeat(60));
  console.log(`类型：${alertType}`);
  console.log(`用户：${alert.userId}`);
  console.log(`时间：${alert.timestamp}`);
  console.log(`详情：`, JSON.stringify(alert.details, null, 2));
  console.log('='.repeat(60) + '\n');
  
  // TODO: 可以扩展为：
  // - 发送邮件
  // - 发送短信
  // - 发送 Webhook（钉钉、企业微信等）
  // - 推送消息到 Feishu
}

/**
 * 实时监控模式
 */
function startMonitoring() {
  console.log('🔍 开始实时监控隐私告警...\n');
  
  let lastAlertTime = Date.now();
  
  // 每 5 秒检查一次
  setInterval(() => {
    const alerts = loadAlerts();
    const newAlerts = alerts.filter(a => {
      const alertTime = new Date(a.timestamp).getTime();
      return alertTime > lastAlertTime;
    });
    
    if (newAlerts.length > 0) {
      newAlerts.forEach(alert => {
        sendAlertNotification(alert);
      });
      
      lastAlertTime = Date.now();
    }
  }, 5000);
  
  console.log('✅ 监控已启动，按 Ctrl+C 停止\n');
}

/**
 * 查看未处理告警
 */
function listUnacknowledged() {
  const db = loadBehaviorDB();
  const unackAlerts = db.alerts.filter(a => !a.acknowledged);
  
  if (unackAlerts.length === 0) {
    console.log('✅ 没有未处理的告警\n');
    return;
  }
  
  console.log(`\n📋 未处理告警 (${unackAlerts.length}条)\n`);
  
  unackAlerts.forEach((alert, i) => {
    const alertType = ALERT_TYPES[alert.type] || alert.type;
    console.log(`${i + 1}. [${alert.id}]`);
    console.log(`   类型：${alertType}`);
    console.log(`   用户：${alert.userId}`);
    console.log(`   时间：${new Date(alert.timestamp).toLocaleString()}`);
    console.log(`   详情：`, JSON.stringify(alert.details, null, 2));
    console.log();
  });
}

/**
 * 确认告警
 */
function acknowledgeAlert(alertId) {
  const db = loadBehaviorDB();
  const alert = db.alerts.find(a => a.id === alertId);
  
  if (!alert) {
    console.log(`❌ 未找到告警：${alertId}\n`);
    return;
  }
  
  alert.acknowledged = true;
  alert.acknowledgedAt = Date.now();
  
  saveBehaviorDB(db);
  console.log(`✅ 告警已确认：${alertId}\n`);
}

/**
 * 保存行为数据库
 */
function saveBehaviorDB(db) {
  const dir = path.dirname(BEHAVIOR_DB);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  fs.writeFileSync(BEHAVIOR_DB, JSON.stringify(db, null, 2), 'utf-8');
}

/**
 * 生成告警统计
 */
function generateStats() {
  const db = loadBehaviorDB();
  const alerts = loadAlerts();
  
  console.log('\n📊 隐私安全统计\n');
  console.log('='.repeat(60));
  
  // 告警统计
  console.log(`总告警数：${db.alerts.length}`);
  console.log(`未处理：${db.alerts.filter(a => !a.acknowledged).length}`);
  console.log(`已处理：${db.alerts.filter(a => a.acknowledged).length}`);
  
  // 按类型统计
  const byType = {};
  db.alerts.forEach(a => {
    byType[a.type] = (byType[a.type] || 0) + 1;
  });
  
  console.log('\n按类型统计:');
  Object.entries(byType).forEach(([type, count]) => {
    const typeName = ALERT_TYPES[type] || type;
    console.log(`  ${typeName}: ${count}`);
  });
  
  // 用户行为统计
  console.log('\n用户行为统计:');
  Object.entries(db.users).forEach(([userId, stats]) => {
    console.log(`  ${userId}:`);
    console.log(`    总操作：${stats.totalActions}`);
    console.log(`    失败尝试：${stats.failedAttempts.length}`);
    console.log(`    被封禁：${stats.isBanned ? '是' : '否'}`);
  });
  
  console.log('='.repeat(60) + '\n');
}

// CLI 入口
const args = process.argv.slice(2);

if (args.includes('--list')) {
  listUnacknowledged();
} else if (args.some(a => a.startsWith('--ack='))) {
  const alertId = args.find(a => a.startsWith('--ack=')).split('=')[1];
  acknowledgeAlert(alertId);
} else if (args.includes('--stats')) {
  generateStats();
} else {
  startMonitoring();
}
