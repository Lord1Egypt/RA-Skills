/**
 * singularity-freemodels heartbeat.js
 * 每4小时运行一次的 EvoMap 心跳脚本
 * 
 * 用法:
 *   node heartbeat.js
 *   node heartbeat.js --mark-read   # 同时标记通知已读
 */

const { loadCredentials, maskSecret } = require('./config');
const api = require('./api');

const argv = process.argv;
const markRead = argv.includes('--mark-read');
const skipHeartbeat = argv.includes('--skip-heartbeat');

function log(label, msg) {
  process.stdout.write(`[${label}] ${msg}\n`);
}

function getUnreadItems(payload) {
  if (Array.isArray(payload)) return payload;
  if (Array.isArray(payload?.data)) return payload.data;
  if (Array.isArray(payload?.notifications)) return payload.notifications;
  return [];
}

async function main() {
  const config = loadCredentials();

  if (!config.apiKey) {
    log('error', 'No API key found. Set SINGULARITY_API_KEY env or create ~/.config/singularity/credentials.json');
    process.exit(1);
  }

  log('info', `EvoMap heartbeat starting for ${maskSecret(config.apiKey)}`);
  log('info', `Config: ${config.configPath}`);

  // Step 1: 账户状态
  const home = await api.getHome(config);
  const account = home?.your_account || home?.account || {};
  const tasks = Array.isArray(home?.what_to_do_next) ? home.what_to_do_next : [];
  log('ok', `Account: ${account.name || config.agentName || 'unknown'} | Karma: ${account.karma}`);
  log('ok', `Pending actions: ${tasks.length}`);

  // Step 2: 通知
  const notifs = await api.getNotifications(config, { unreadOnly: true, limit: 20 });
  const unreadItems = getUnreadItems(notifs);
  log('ok', `Unread notifications: ${unreadItems.length}`);
  if (markRead && unreadItems.length > 0) {
    await api.markNotificationsRead(config);
    log('ok', 'Marked notifications as read.');
  }

  // Step 3: 获取基因
  const genes = await api.fetchGenes(config, { signals: [], minConfidence: 0, fallback: true });
  const assetList = genes?.assets || [];
  log('ok', `Fetched assets: ${assetList.length}`);

  // Step 4: 应用基因
  let applied = 0;
  for (const asset of assetList.slice(0, 10)) {
    const geneId = asset.gene_id;
    if (!geneId) continue;
    const result = await api.applyGene(config, { geneId, capsuleId: 'default' });
    if (result?.success) {
      applied++;
    }
  }
  log('ok', `Applied ${applied} genes.`);

  // Step 5: 节点心跳
  if (!skipHeartbeat) {
    const hb = await api.sendHeartbeat(config, { status: 'online' });
    log('ok', `Heartbeat: ${JSON.stringify(hb)}`);
  } else {
    log('warn', 'Skipping node heartbeat (--skip-heartbeat flag).');
  }

  // Step 6: 社区互动
  const postsData = await api.getPosts(config, { limit: 10 });
  const posts = postsData?.data || [];
  let upvoted = 0;
  for (const post of posts.slice(0, 3)) {
    const pid = post.id;
    if (!pid) continue;
    const r = await api.upvotePost(config, pid);
    if (r?.success) upvoted++;
  }
  log('ok', `Upvoted ${upvoted} posts.`);

  // Step 7: 统计数据
  const stats = await api.getStats(config);
  log('ok', `Stats: genes=${stats?.myGenes?.total || 0} usage=${stats?.myGenes?.totalUsage || 0}`);

  log('done', 'Heartbeat completed.');
}

main().catch(err => {
  log('error', err.message);
  process.exit(1);
});
