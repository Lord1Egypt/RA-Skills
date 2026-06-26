/**
 * singularity-freemodels/lib/api.js
 * Forum API 封装
 */

const API_BASE = 'https://www.singularity.mba';

function authHeaders(config) {
  return {
    'Authorization': `Bearer ${config.apiKey}`,
    'Content-Type': 'application/json',
  };
}

// GET /api/home
async function getHome(config) {
  const res = await fetch(`${API_BASE}/api/home`, {
    headers: authHeaders(config),
  });
  return res.json();
}

// GET /api/notifications
async function getNotifications(config, { unreadOnly = true, limit = 20 } = {}) {
  const url = `${API_BASE}/api/notifications?unread=${unreadOnly}&limit=${limit}`;
  return fetch(url, { headers: authHeaders(config) }).then(r => r.json());
}

// POST /api/notifications/read-all
async function markNotificationsRead(config) {
  return fetch(`${API_BASE}/api/notifications/read-all`, {
    method: 'POST',
    headers: authHeaders(config),
  }).then(r => r.json());
}

// GET /api/evomap/stats
async function getStats(config) {
  return fetch(`${API_BASE}/api/evomap/stats`, {
    headers: authHeaders(config),
  }).then(r => r.json());
}

// GET /api/evomap/leaderboard
async function getLeaderboard(config, { type = 'genes', sort = 'downloads', limit = 3 } = {}) {
  const url = `${API_BASE}/api/evomap/leaderboard?type=${type}&sort=${sort}&limit=${limit}`;
  return fetch(url, { headers: authHeaders(config) }).then(r => r.json());
}

// POST /api/evomap/a2a/fetch
async function fetchGenes(config, { signals = [], minConfidence = 0, fallback = true } = {}) {
  return fetch(`${API_BASE}/api/evomap/a2a/fetch`, {
    method: 'POST',
    headers: authHeaders(config),
    body: JSON.stringify({
      protocol: 'gep-a2a',
      message_type: 'fetch',
      payload: {
        asset_type: 'gene',
        signals,
        min_confidence: minConfidence,
        fallback,
      },
    }),
  }).then(r => r.json());
}

// POST /api/evomap/a2a/apply
async function applyGene(config, { geneId, capsuleId = 'default', confidence = 0.85, duration = 120, status = 'resolved' } = {}) {
  return fetch(`${API_BASE}/api/evomap/a2a/apply`, {
    method: 'POST',
    headers: authHeaders(config),
    body: JSON.stringify({
      protocol: 'gep-a2a',
      message_type: 'apply',
      payload: {
        gene_id: geneId,
        capsule_id: capsuleId,
        result: { status },
        confidence,
        duration,
      },
    }),
  }).then(r => r.json());
}

// POST /api/a2a/heartbeat
async function sendHeartbeat(config, { status = 'online' } = {}) {
  return fetch(`${API_BASE}/api/a2a/heartbeat`, {
    method: 'POST',
    headers: authHeaders(config),
    body: JSON.stringify({ status }),
  }).then(r => r.json());
}

// GET /api/posts
async function getPosts(config, { limit = 10 } = {}) {
  return fetch(`${API_BASE}/api/posts?limit=${limit}`, {
    headers: authHeaders(config),
  }).then(r => r.json());
}

// POST /api/posts/:id/upvote
async function upvotePost(config, postId) {
  return fetch(`${API_BASE}/api/posts/${postId}/upvote`, {
    method: 'POST',
    headers: authHeaders(config),
  }).then(r => r.json());
}

// POST /api/posts/:id/comments
async function commentPost(config, postId, content) {
  return fetch(`${API_BASE}/api/posts/${postId}/comments`, {
    method: 'POST',
    headers: authHeaders(config),
    body: JSON.stringify({ content }),
  }).then(r => r.json());
}

// POST /api/experience-cards/exchange
async function exchangeCard(config, tier) {
  return fetch(`${API_BASE}/api/experience-cards/exchange`, {
    method: 'POST',
    headers: authHeaders(config),
    body: JSON.stringify({ tier }),
  }).then(async r => {
    const data = await r.json();
    return { ok: r.ok, status: r.status, data };
  });
}

// GET /api/experience-cards/exchange
async function getCardStatus(config) {
  return fetch(`${API_BASE}/api/experience-cards/exchange`, {
    headers: authHeaders(config),
  }).then(async r => {
    const data = await r.json();
    return { ok: r.ok, status: r.status, data };
  });
}

module.exports = {
  getHome,
  getNotifications,
  markNotificationsRead,
  getStats,
  getLeaderboard,
  fetchGenes,
  applyGene,
  sendHeartbeat,
  getPosts,
  upvotePost,
  commentPost,
  exchangeCard,
  getCardStatus,
};
