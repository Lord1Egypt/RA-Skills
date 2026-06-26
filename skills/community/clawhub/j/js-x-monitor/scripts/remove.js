#!/usr/bin/env node
/**
 * 移除监控账号
 */

const { loadConfig, saveConfig, getUsername } = require('./lib/utils');

async function main() {
  const username = process.argv[2];

  if (!username) {
    console.error('❌ 请提供用户名');
    console.error('   用法: openclaw x-monitor remove <username>');
    process.exit(1);
  }

  const cleanUsername = username.replace(/^@/, '').trim().toLowerCase();

  try {
    const config = await loadConfig();

    const initialCount = config.accounts.length;
    config.accounts = config.accounts.filter(a =>
      getUsername(a).toLowerCase() !== cleanUsername
    );

    if (config.accounts.length === initialCount) {
      console.log(`⚠️ @${username} 不在监控列表中`);
      return;
    }

    await saveConfig(config);

    console.log(`✅ 已移除 @${username}`);
    console.log(`   当前监控 ${config.accounts.length} 个账号`);
  } catch (err) {
    console.error('❌ 移除失败:', err.message);
    process.exit(1);
  }
}

main();
