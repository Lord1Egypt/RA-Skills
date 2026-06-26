const fs = require('fs').promises;
const path = require('path');
const crypto = require('crypto');

const CONFIG_DIR = path.join(process.env.HOME || process.env.USERPROFILE, '.openclaw', 'x-monitor');
const STATE_DIR = path.join(CONFIG_DIR, 'state');
const LOG_DIR = path.join(CONFIG_DIR, 'logs');
const CONFIG_FILE = path.join(CONFIG_DIR, 'config.json');

async function loadConfig() {
  try {
    const data = await fs.readFile(CONFIG_FILE, 'utf8');
    return JSON.parse(data);
  } catch (err) {
    console.error('❌ 配置加载失败:', err.message);
    console.error('   请先运行: openclaw x-monitor init');
    process.exit(1);
  }
}

async function saveConfig(config) {
  await fs.writeFile(CONFIG_FILE, JSON.stringify(config, null, 2));
}

async function loadState(username) {
  const stateFile = path.join(STATE_DIR, `${username}.json`);
  try {
    const data = await fs.readFile(stateFile, 'utf8');
    return JSON.parse(data);
  } catch {
    return { tweets: [], lastCheck: null };
  }
}

async function saveState(username, state) {
  await fs.mkdir(STATE_DIR, { recursive: true });
  const stateFile = path.join(STATE_DIR, `${username}.json`);
  await fs.writeFile(stateFile, JSON.stringify(state, null, 2));
}

function hashContent(text) {
  return crypto.createHash('sha256').update(text || '').digest('hex').slice(0, 16);
}

/**
 * 获取账号的用户名（兼容字符串和对象两种格式）
 */
function getUsername(account) {
  return typeof account === 'string' ? account : account.username;
}

/**
 * 获取推文（通过 OpenClaw 注入的 x_get_profile）
 * --mock 参数可在非 OpenClaw 环境下返回模拟数据用于调试
 */
async function fetchTweets(username) {
  if (typeof x_get_profile === 'function') {
    return await x_get_profile({ username });
  }
  if (process.argv.includes('--mock')) {
    console.log(`   📡 [mock] 正在获取 @${username} 的推文...`);
    await new Promise(resolve => setTimeout(resolve, 300));
    return {
      username,
      tweets: [
        {
          id: `mock_${Date.now()}_1`,
          text: `Mock tweet from @${username} at ${new Date().toISOString()}`,
          created_at: new Date().toISOString(),
          likes: 42,
          retweets: 7
        }
      ]
    };
  }
  throw new Error('x_get_profile 不可用，请确保在 OpenClaw 环境中运行，或使用 --mock 参数测试');
}

/**
 * 去重判断：根据 deduplication.method 支持三种策略
 */
function isNewTweet(tweet, hash, knownIds, knownHashes, method) {
  switch (method) {
    case 'id_only':
      return !knownIds.has(tweet.id);
    case 'hash_only':
      return !knownHashes.has(hash);
    case 'id_and_hash':
    default:
      return !knownIds.has(tweet.id) && !knownHashes.has(hash);
  }
}

/**
 * 按 historyDays 清理过期状态记录
 */
function pruneExpiredTweets(tweets, historyDays) {
  const days = historyDays || 30;
  const cutoff = Date.now() - days * 86400000;
  return tweets.filter(t => new Date(t.discoveredAt).getTime() > cutoff);
}

/**
 * 格式化通知消息
 */
function formatMessage(username, tweet, config) {
  const maxLength = config.notification?.summaryLength || 100;
  const summary = tweet.text.slice(0, maxLength);
  const hasMore = tweet.text.length > maxLength;

  return `🐦 **@${username}** 新推文\n\n${summary}${hasMore ? '...' : ''}\n\n[查看原文](https://x.com/${username}/status/${tweet.id})\n\n⏰ ${new Date(tweet.created_at).toLocaleString('zh-CN')}`;
}

/**
 * 发送通知：OpenClaw 环境走 openclaw_send_message，否则降级为 console
 */
async function sendNotification(username, tweet, config) {
  const channels = config.notification?.channels || ['feishu'];
  const message = formatMessage(username, tweet, config);

  for (const channel of channels) {
    if (typeof openclaw_send_message === 'function') {
      await openclaw_send_message({ channel, content: message });
      console.log(`      ✅ ${channel}: 消息已发送`);
    } else {
      console.log(`      [通知-${channel}] ${message.split('\n')[0]}`);
    }
  }
}

module.exports = {
  CONFIG_DIR,
  STATE_DIR,
  LOG_DIR,
  CONFIG_FILE,
  loadConfig,
  saveConfig,
  loadState,
  saveState,
  hashContent,
  getUsername,
  fetchTweets,
  isNewTweet,
  pruneExpiredTweets,
  formatMessage,
  sendNotification
};
