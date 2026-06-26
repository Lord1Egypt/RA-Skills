#!/usr/bin/env node

/**
 * Quota Manager CLI - 配额管理命令行工具
 * 
 * 用法:
 *   node scripts/quota-manager.js set <user_id> [options]  # 设置用户配额
 *   node scripts/quota-manager.js reset <user_id>          # 重置用户配额
 *   node scripts/quota-manager.js list                     # 列出所有用户配额
 *   node scripts/quota-manager.js info <user_id>           # 查看用户配额详情
 */

const fs = require('fs');
const path = require('path');

const QUOTA_DB = path.join(process.env.HOME, '.openclaw/skills/multi-user-privacy/.quota-db.json');
const ADMIN_ID = 'ou_b96f5424607baf3a0455b55e0f4a2213';

const DEFAULT_QUOTA = {
  diskQuotaMB: 100,
  tokenQuota: 100000,
  messageQuota: 1000,
  sessionTimeoutHours: 24,
  maxConcurrentSessions: 5,
  isAdmin: false
};

const ADMIN_QUOTA = {
  diskQuotaMB: -1,
  tokenQuota: -1,
  messageQuota: -1,
  sessionTimeoutHours: -1,
  maxConcurrentSessions: -1,
  isAdmin: true
};

function loadQuotaDB() {
  try {
    if (fs.existsSync(QUOTA_DB)) {
      return JSON.parse(fs.readFileSync(QUOTA_DB, 'utf-8'));
    }
  } catch (e) {
    console.error('加载配额数据库失败:', e.message);
  }
  return {};
}

function saveQuotaDB(db) {
  try {
    const dir = path.dirname(QUOTA_DB);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    fs.writeFileSync(QUOTA_DB, JSON.stringify(db, null, 2), 'utf-8');
    console.log('✅ 配额数据库已保存');
  } catch (e) {
    console.error('保存配额数据库失败:', e.message);
  }
}

function setQuota(userId, options = {}) {
  const db = loadQuotaDB();
  
  // 管理员自动使用无限配额
  const baseQuota = (userId === ADMIN_ID) ? ADMIN_QUOTA : DEFAULT_QUOTA;
  
  db[userId] = {
    ...baseQuota,
    ...options,
    used: {
      disk: 0,
      tokens: 0,
      messages: 0,
      lastReset: new Date().toISOString()
    },
    createdAt: new Date().toISOString()
  };
  
  saveQuotaDB(db);
  console.log(`✅ 已为用户 ${userId} 设置配额`);
  console.log(`   磁盘：${db[userId].diskQuotaMB === -1 ? '∞' : db[userId].diskQuotaMB + 'MB'}`);
  console.log(`   Token: ${db[userId].tokenQuota === -1 ? '∞' : db[userId].tokenQuota}`);
  console.log(`   消息：${db[userId].messageQuota === -1 ? '∞' : db[userId].messageQuota} 条/天`);
}

function resetQuota(userId) {
  const db = loadQuotaDB();
  
  if (!db[userId]) {
    console.log(`⚠️  用户 ${userId} 不存在`);
    return;
  }
  
  db[userId].used = {
    disk: 0,
    tokens: 0,
    messages: 0,
    lastReset: new Date().toISOString()
  };
  
  saveQuotaDB(db);
  console.log(`✅ 已重置用户 ${userId} 的配额使用量`);
}

function listQuotas() {
  const db = loadQuotaDB();
  const users = Object.keys(db);
  
  console.log(`\n📊 配额数据库 (${users.length} 个用户)\n`);
  
  users.forEach(userId => {
    const quota = db[userId];
    const isAdmin = userId === ADMIN_ID || quota.isAdmin === true;
    
    console.log(`${isAdmin ? '👑' : '👤'} ${userId}`);
    console.log(`   磁盘：${quota.used.disk}MB / ${quota.diskQuotaMB === -1 ? '∞' : quota.diskQuotaMB + 'MB'}`);
    console.log(`   Token: ${quota.used.tokens} / ${quota.tokenQuota === -1 ? '∞' : quota.tokenQuota}`);
    console.log(`   消息：${quota.used.messages} / ${quota.messageQuota === -1 ? '∞' : quota.messageQuota}`);
    console.log(`   创建：${quota.createdAt}`);
    console.log();
  });
}

function getQuotaInfo(userId) {
  const db = loadQuotaDB();
  
  if (!db[userId]) {
    console.log(`⚠️  用户 ${userId} 不存在`);
    return;
  }
  
  const quota = db[userId];
  const isAdmin = userId === ADMIN_ID || quota.isAdmin === true;
  
  console.log(`\n📊 用户 ${userId} 配额详情\n`);
  console.log(`身份：${isAdmin ? '管理员 (无限配额) 👑' : '普通用户'}`);
  console.log(`创建时间：${quota.createdAt}`);
  console.log();
  console.log('配额限制:');
  console.log(`  磁盘：${quota.diskQuotaMB === -1 ? '∞' : quota.diskQuotaMB + 'MB'}`);
  console.log(`  Token: ${quota.tokenQuota === -1 ? '∞' : quota.tokenQuota}`);
  console.log(`  消息：${quota.messageQuota === -1 ? '∞' : quota.messageQuota} 条/天`);
  console.log(`  Session 超时：${quota.sessionTimeoutHours === -1 ? '∞' : quota.sessionTimeoutHours + '小时'}`);
  console.log(`  最大并发：${quota.maxConcurrentSessions === -1 ? '∞' : quota.maxConcurrentSessions}`);
  console.log();
  console.log('使用情况:');
  console.log(`  磁盘：${quota.used.disk}MB`);
  console.log(`  Token: ${quota.used.tokens}`);
  console.log(`  消息：${quota.used.messages}`);
  console.log(`  最后重置：${quota.used.lastReset}`);
  console.log();
}

// CLI 入口
const command = process.argv[2];
const userId = process.argv[3];

if (command === 'set') {
  if (!userId) {
    console.log('用法：node quota-manager.js set <user_id> [options]');
    console.log('选项:');
    console.log('  --disk=100       磁盘配额 (MB), -1 表示无限');
    console.log('  --token=100000   Token 配额');
    console.log('  --message=1000   消息配额 (条/天)');
    console.log('  --admin          设置为管理员 (无限配额)');
    process.exit(1);
  }
  
  const options = {};
  process.argv.slice(4).forEach(arg => {
    if (arg.startsWith('--disk=')) {
      options.diskQuotaMB = parseInt(arg.split('=')[1]);
    } else if (arg.startsWith('--token=')) {
      options.tokenQuota = parseInt(arg.split('=')[1]);
    } else if (arg.startsWith('--message=')) {
      options.messageQuota = parseInt(arg.split('=')[1]);
    } else if (arg === '--admin') {
      options.isAdmin = true;
      options.diskQuotaMB = -1;
      options.tokenQuota = -1;
      options.messageQuota = -1;
    }
  });
  
  setQuota(userId, options);
  
} else if (command === 'reset') {
  if (!userId) {
    console.log('用法：node quota-manager.js reset <user_id>');
    process.exit(1);
  }
  resetQuota(userId);
  
} else if (command === 'list') {
  listQuotas();
  
} else if (command === 'info') {
  if (!userId) {
    console.log('用法：node quota-manager.js info <user_id>');
    process.exit(1);
  }
  getQuotaInfo(userId);
  
} else {
  console.log(`
配额管理器 - Quota Manager

用法:
  node quota-manager.js set <user_id> [options]   # 设置用户配额
  node quota-manager.js reset <user_id>           # 重置用户配额
  node quota-manager.js list                      # 列出所有用户配额
  node quota-manager.js info <user_id>            # 查看用户配额详情

示例:
  # 设置普通用户配额
  node quota-manager.js set ou_xxx123 --disk=100 --token=100000 --message=1000
  
  # 设置管理员 (无限配额)
  node quota-manager.js set ou_xxx123 --admin
  
  # 重置用户配额使用量
  node quota-manager.js reset ou_xxx123
  
  # 查看配额使用情况
  node quota-manager.js info ou_xxx123
  `);
}
