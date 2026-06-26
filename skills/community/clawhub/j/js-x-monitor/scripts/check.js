#!/usr/bin/env node
/**
 * X-Monitor 核心监控脚本
 * 定时检查所有配置的 X.com 账号，发现新推文推送通知
 *
 * 使用方法:
 *   node scripts/check.js              # 检查所有账号
 *   node scripts/check.js <username>   # 检查单个账号
 */

const {
  loadConfig,
  loadState,
  saveState,
  hashContent,
  getUsername,
  fetchTweets,
  isNewTweet,
  pruneExpiredTweets,
  sendNotification
} = require('./lib/utils');

/**
 * 合并账号级配置与全局配置，账号级优先
 */
function mergeAccountConfig(account, globalConfig) {
  if (typeof account === 'string') return globalConfig;
  return {
    ...globalConfig,
    notification: {
      ...globalConfig.notification,
      channels: account.notifyChannel
        ? [account.notifyChannel]
        : globalConfig.notification?.channels
    }
  };
}

/**
 * 根据配置过滤转推和回复
 */
function filterTweets(tweets, config) {
  let result = tweets;
  if (!config.notification?.includeRetweets) {
    result = result.filter(t => !t.is_retweet);
  }
  if (!config.notification?.includeReplies) {
    result = result.filter(t => !t.is_reply);
  }
  return result;
}

/**
 * 检查单个账号
 */
async function checkAccount(account, globalConfig) {
  const username = getUsername(account);
  const effectiveConfig = mergeAccountConfig(account, globalConfig);

  console.log(`\n🔍 检查 @${username}...`);

  try {
    console.log(`   📡 正在获取 @${username} 的推文...`);
    const profile = await fetchTweets(username);

    if (!profile || !profile.tweets || profile.tweets.length === 0) {
      console.log('   ⚠️ 未获取到推文');
      return { newTweets: 0, notified: 0 };
    }

    const tweets = filterTweets(profile.tweets, effectiveConfig);

    const state = await loadState(username);
    const knownIds = new Set(state.tweets.map(t => t.id));
    const knownHashes = new Set(state.tweets.map(t => t.hash));
    const dedupMethod = globalConfig.deduplication?.method || 'id_and_hash';

    const newTweets = [];
    for (const tweet of tweets) {
      const hash = hashContent(tweet.text);
      if (isNewTweet(tweet, hash, knownIds, knownHashes, dedupMethod)) {
        newTweets.push({
          ...tweet,
          hash,
          discoveredAt: new Date().toISOString()
        });
      }
    }

    console.log(`   📊 获取 ${tweets.length} 条推文，发现 ${newTweets.length} 条新推文`);

    let notifiedCount = 0;
    for (const tweet of newTweets) {
      try {
        await sendNotification(username, tweet, effectiveConfig);
        notifiedCount++;
        tweet.notified = true;
        tweet.notifiedAt = new Date().toISOString();
      } catch (err) {
        console.error('   ❌ 通知发送失败:', err.message);
        tweet.notified = false;
      }
    }

    const allTweets = [...newTweets, ...state.tweets];
    const historyDays = globalConfig.deduplication?.historyDays;
    state.tweets = pruneExpiredTweets(allTweets, historyDays);
    state.lastCheck = new Date().toISOString();
    await saveState(username, state);

    return { newTweets: newTweets.length, notified: notifiedCount };
  } catch (err) {
    console.error('   ❌ 检查失败:', err.message);
    return { newTweets: 0, notified: 0, error: err.message };
  }
}

async function main() {
  console.log('🚀 X-Monitor 监控任务');
  console.log('⏰', new Date().toLocaleString('zh-CN'));
  console.log('');

  const config = await loadConfig();

  let accounts = config.accounts || [];

  const userArg = process.argv.slice(2).find(a => !a.startsWith('--'));
  if (userArg) {
    const cleanUser = userArg.replace(/^@/, '').trim();
    const found = accounts.find(a =>
      getUsername(a).toLowerCase() === cleanUser.toLowerCase()
    );

    if (!found) {
      console.error(`❌ 账号 @${cleanUser} 不在监控列表中`);
      console.error('   添加账号: openclaw x-monitor add', cleanUser);
      process.exit(1);
    }

    accounts = [found];
  }

  accounts = accounts.filter(a => {
    if (typeof a === 'string') return true;
    return a.enabled !== false;
  });

  if (accounts.length === 0) {
    console.log('⚠️ 没有启用的监控账号');
    console.log('   添加账号: openclaw x-monitor add <username>');
    return;
  }

  console.log(`📋 检查 ${accounts.length} 个账号`);
  console.log('');

  let totalNew = 0;
  let totalNotified = 0;

  for (const account of accounts) {
    const result = await checkAccount(account, config);
    totalNew += result.newTweets;
    totalNotified += result.notified;
  }

  console.log('\n📊 统计');
  console.log(`   新推文: ${totalNew}`);
  console.log(`   已通知: ${totalNotified}`);
  console.log('');
  console.log('✅ 完成');
}

main().catch(err => {
  console.error('❌ 监控任务失败:', err);
  process.exit(1);
});
