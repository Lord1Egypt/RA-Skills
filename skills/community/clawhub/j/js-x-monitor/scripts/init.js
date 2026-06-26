#!/usr/bin/env node
/**
 * X-Monitor 初始化脚本
 */

const fs = require('fs').promises;
const { CONFIG_DIR, STATE_DIR, LOG_DIR, CONFIG_FILE } = require('./lib/utils');

const DEFAULT_CONFIG = {
  accounts: [],
  notification: {
    channels: ['feishu'],
    includeRetweets: false,
    includeReplies: false,
    summaryLength: 100
  },
  deduplication: {
    method: 'id_and_hash',
    historyDays: 30
  },
  checkInterval: 3600
};

async function main() {
  console.log('🚀 X-Monitor 初始化');
  console.log('');

  try {
    await fs.mkdir(CONFIG_DIR, { recursive: true });
    await fs.mkdir(STATE_DIR, { recursive: true });
    await fs.mkdir(LOG_DIR, { recursive: true });

    try {
      await fs.access(CONFIG_FILE);
      console.log('⚠️ 配置文件已存在:', CONFIG_FILE);
      console.log('   如需重置，请手动删除后重新运行 init');
    } catch {
      await fs.writeFile(CONFIG_FILE, JSON.stringify(DEFAULT_CONFIG, null, 2));
      console.log('✅ 配置文件已创建:', CONFIG_FILE);
    }

    console.log('');
    console.log('📁 目录结构');
    console.log('   配置:', CONFIG_DIR);
    console.log('   状态:', STATE_DIR);
    console.log('   日志:', LOG_DIR);
    console.log('');
    console.log('📝 下一步');
    console.log('   1. 编辑配置:', CONFIG_FILE);
    console.log('   2. 添加账号: openclaw x-monitor add <username>');
    console.log('   3. 启动监控: openclaw x-monitor start');
    console.log('');
    console.log('✅ 初始化完成');
  } catch (err) {
    console.error('❌ 初始化失败:', err.message);
    process.exit(1);
  }
}

main();
