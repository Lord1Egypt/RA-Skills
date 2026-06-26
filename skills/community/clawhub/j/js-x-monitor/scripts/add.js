#!/usr/bin/env node
/**
 * 添加监控账号
 */

const { loadConfig, saveConfig, getUsername } = require('./lib/utils');

async function main() {
  const username = process.argv[2];

  if (!username) {
    console.error('❌ 请提供用户名');
    console.error('   用法: openclaw x-monitor add <username>');
    process.exit(1);
  }

  const cleanUsername = username.replace(/^@/, '').trim();

  if (!cleanUsername) {
    console.error('❌ 用户名不能为空');
    process.exit(1);
  }

  try {
    const config = await loadConfig();

    const exists = config.accounts.some(a =>
      getUsername(a).toLowerCase() === cleanUsername.toLowerCase()
    );

    if (exists) {
      console.log(`⚠️ @${cleanUsername} 已在监控列表中`);
      return;
    }

    config.accounts.push({
      username: cleanUsername,
      enabled: true,
      addedAt: new Date().toISOString()
    });

    await saveConfig(config);

    console.log(`✅ 已添加 @${cleanUsername} 到监控列表`);
    console.log(`   当前监控 ${config.accounts.length} 个账号`);
    console.log('');
    console.log('📝 提示');
    console.log('   启动监控: openclaw x-monitor start');
    console.log('   测试账号: openclaw x-monitor test', cleanUsername);
  } catch (err) {
    console.error('❌ 添加失败:', err.message);
    console.error('   请先运行: openclaw x-monitor init');
    process.exit(1);
  }
}

main();
