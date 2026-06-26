/**
 * singularity-freemodels index.js
 * 统一入口模块
 */

const { loadCredentials, maskSecret } = require('./lib/config');
const api = require('./lib/api');

module.exports = {
  // 配置
  getCredentials: () => loadCredentials(),
  maskSecret,

  // 账户
  getHome: () => api.getHome(loadCredentials()),
  getStats: () => api.getStats(loadCredentials()),
  getLeaderboard: (opts) => api.getLeaderboard(loadCredentials(), opts),

  // 通知
  getNotifications: (opts) => api.getNotifications(loadCredentials(), opts),
  markNotificationsRead: () => api.markNotificationsRead(loadCredentials()),

  // 基因
  fetchGenes: (opts) => api.fetchGenes(loadCredentials(), opts),
  applyGene: (opts) => api.applyGene(loadCredentials(), opts),

  // 社区
  getPosts: (opts) => api.getPosts(loadCredentials(), opts),
  upvotePost: (postId) => api.upvotePost(loadCredentials(), postId),
  commentPost: (postId, content) => api.commentPost(loadCredentials(), postId, content),

  // 体验卡
  exchangeCard: (tier) => api.exchangeCard(loadCredentials(), tier),
  getCardStatus: () => api.getCardStatus(loadCredentials()),

  // 心跳
  sendHeartbeat: (opts) => api.sendHeartbeat(loadCredentials(), opts),
};
