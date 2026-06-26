#!/usr/bin/env node
/**
 * 测试单个账号
 */

const { loadConfig, fetchTweets, getUsername } = require('./lib/utils');

async function main() {
  const username = process.argv[2];

  if (!username) {
    console.error('❌ 请提供用户名');
    console.error('   用法: openclaw x-monitor test <username>');
    process.exit(1);
  }

  const cleanUsername = username.replace(/^@/, '').trim();

  console.log(`🧪 测试 @${cleanUsername}`);
  console.log('');

  try {
    const config = await loadConfig();

    console.log('1️⃣ 检查配置...');
    const exists = config.accounts.some(a =>
      getUsername(a).toLowerCase() === cleanUsername.toLowerCase()
    );

    if (!exists) {
      console.log('   ⚠️ 账号不在监控列表中');
      console.log('   💡 建议: openclaw x-monitor add', cleanUsername);
    } else {
      console.log('   ✅ 账号在监控列表中');
    }

    console.log('');
    console.log('2️⃣ 测试 X.com 连接...');

    try {
      const profile = await fetchTweets(cleanUsername);

      if (profile && profile.tweets && profile.tweets.length > 0) {
        console.log(`   ✅ 成功获取 ${profile.tweets.length} 条推文`);
        console.log('');
        console.log('   最新推文:');
        const latest = profile.tweets[0];
        console.log(`   "${latest.text.slice(0, 80)}${latest.text.length > 80 ? '...' : ''}"`);
        console.log(`   ⏰ ${new Date(latest.created_at).toLocaleString('zh-CN')}`);
        console.log(`   ❤️ ${latest.likes || 0} | 🔄 ${latest.retweets || 0}`);
      } else {
        console.log('   ⚠️ 未获取到推文');
      }
    } catch (err) {
      console.log('   ❌ 连接失败:', err.message);
      console.log('   💡 检查: JS-Eyes 是否已连接，浏览器是否已登录 X.com');
    }

    console.log('');
    console.log('✅ 测试完成');
  } catch (err) {
    console.error('❌ 测试失败:', err.message);
    console.error('   请先运行: openclaw x-monitor init');
    process.exit(1);
  }
}

main();
