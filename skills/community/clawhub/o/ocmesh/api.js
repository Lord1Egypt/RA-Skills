/**
 * api.js
 * HTTP API — localhost:7432
 * v0.2: profiles, threads, groups, receipts, typed messages, config.
 */

const express = require('express');
const db = require('./db');
const { send } = require('./messaging');
const { create, MESSAGE_TYPES } = require('./protocol');
const { getProfile, getOwnProfile, publishProfile } = require('./profiles');
const threads = require('./threads');
const groups = require('./groups');
const { sendRead } = require('./receipts');
const { PEER_TTL } = require('./relays');
const configManager = require('./config');

const app = express();
app.use(express.json());
const PORT = 7432;

// ─── Status ───────────────────────────────────────────────────────────────────

app.get('/status', (req, res) => {
  const identity = db.prepare('SELECT pk FROM identity LIMIT 1').get();
  const totalPeers = db.prepare('SELECT COUNT(*) as c FROM peers').get().c;
  const onlinePeers = db.prepare('SELECT COUNT(*) as c FROM peers WHERE last_seen > ?')
    .get(Date.now() - PEER_TTL).c;
  const unread = db.prepare('SELECT COUNT(*) as c FROM messages WHERE read = 0').get().c;
  const totalMessages = db.prepare('SELECT COUNT(*) as c FROM messages').get().c;
  const groupCount = db.prepare('SELECT COUNT(*) as c FROM groups').get().c;

  res.json({
    ok: true,
    version: '0.2.0',
    publicKey: identity?.pk ?? null,
    peers: { total: totalPeers, online: onlinePeers },
    messages: { total: totalMessages, unread },
    groups: groupCount,
    uptime: Math.floor(process.uptime()),
  });
});

// ─── Identity & Profile ───────────────────────────────────────────────────────

app.get('/identity', (req, res) => {
  const identity = db.prepare('SELECT pk FROM identity LIMIT 1').get();
  res.json({ publicKey: identity?.pk ?? null });
});

app.get('/profile', (req, res) => {
  res.json(getOwnProfile());
});

app.post('/profile', (req, res) => {
  const cfg = configManager.load();
  const { name, about, picture } = req.body;
  if (name) cfg.profile.name = name;
  if (about) cfg.profile.about = about;
  if (picture) cfg.profile.picture = picture;
  configManager.save(cfg);
  publishProfile();
  res.json({ ok: true, profile: cfg.profile });
});

app.get('/profile/:pk', (req, res) => {
  const profile = getProfile(req.params.pk);
  if (!profile) return res.status(404).json({ error: 'Profile not found (not yet cached)' });
  res.json(profile);
});

// ─── Peers ────────────────────────────────────────────────────────────────────

app.get('/peers', (req, res) => {
  const { online } = req.query;
  const peers = online === 'true'
    ? db.prepare('SELECT * FROM peers WHERE last_seen > ? ORDER BY last_seen DESC')
        .all(Date.now() - PEER_TTL)
    : db.prepare('SELECT * FROM peers ORDER BY last_seen DESC').all();

  res.json({ peers: peers.map(p => formatPeer(p)) });
});

app.get('/peers/:pk', (req, res) => {
  const peer = db.prepare('SELECT * FROM peers WHERE pk = ?').get(req.params.pk);
  if (!peer) return res.status(404).json({ error: 'peer not found' });
  const profile = getProfile(req.params.pk);
  res.json({ ...formatPeer(peer), profile });
});

// ─── Threads ──────────────────────────────────────────────────────────────────

app.get('/threads', (req, res) => {
  const allThreads = threads.getAll();
  const enriched = allThreads.map(t => {
    const profile = getProfile(t.peer_pk);
    return { ...t, profile };
  });
  res.json({ threads: enriched });
});

app.get('/threads/:pk', (req, res) => {
  const msgs = threads.getThread(req.params.pk);
  const profile = getProfile(req.params.pk);
  res.json({ peer: req.params.pk, profile, messages: msgs });
});

app.post('/threads/:pk/read', async (req, res) => {
  const { pk } = req.params;
  // Get unread messages from this peer to send read receipts
  const unreadMsgs = db.prepare(
    'SELECT id FROM messages WHERE from_pk = ? AND read = 0'
  ).all(pk);

  threads.markRead(pk);

  for (const msg of unreadMsgs) {
    await sendRead(pk, msg.id);
  }

  res.json({ ok: true, markedRead: unreadMsgs.length });
});

// ─── Messages ─────────────────────────────────────────────────────────────────

app.get('/messages', (req, res) => {
  const { unread, from, type } = req.query;
  let query = 'SELECT * FROM messages WHERE 1=1';
  const params = [];

  if (unread === 'true') { query += ' AND read = 0'; }
  if (from) { query += ' AND from_pk = ?'; params.push(from); }
  if (type) { query += ' AND msg_type = ?'; params.push(type); }

  query += ' ORDER BY received_at DESC LIMIT 100';
  res.json({ messages: db.prepare(query).all(...params) });
});

app.post('/messages/read', (req, res) => {
  const { id } = req.body;
  if (id) {
    db.prepare('UPDATE messages SET read = 1 WHERE id = ?').run(id);
  } else {
    db.prepare('UPDATE messages SET read = 1').run();
  }
  res.json({ ok: true });
});

// ─── Send ─────────────────────────────────────────────────────────────────────

app.post('/send', async (req, res) => {
  const { to, content, type } = req.body;
  if (!to || !content) return res.status(400).json({ error: 'to and content required' });

  try {
    // If type specified, wrap in protocol envelope
    const payload = type ? create(type, { body: content }) : content;
    const id = await send(to, payload);
    res.json({ ok: true, id });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Convenience: send a task to an agent
app.post('/send/task', async (req, res) => {
  const { to, action, params } = req.body;
  if (!to || !action) return res.status(400).json({ error: 'to and action required' });

  try {
    const payload = create(MESSAGE_TYPES.TASK, { action, params: params || {} });
    const id = await send(to, payload);
    res.json({ ok: true, id });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Convenience: ping a peer
app.post('/ping/:pk', async (req, res) => {
  try {
    const id = await send(req.params.pk, create(MESSAGE_TYPES.PING, {}));
    res.json({ ok: true, id, note: 'pong will arrive as an incoming message' });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// ─── Groups ───────────────────────────────────────────────────────────────────

app.get('/groups', (req, res) => {
  res.json({ groups: groups.listGroups() });
});

app.post('/groups', async (req, res) => {
  const { name, about, members } = req.body;
  if (!name) return res.status(400).json({ error: 'name required' });

  try {
    const group = await groups.createGroup(name, about, members || []);
    res.json({ ok: true, group });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.get('/groups/:id', (req, res) => {
  const msgs = groups.getGroupMessages(req.params.id);
  res.json({ messages: msgs });
});

app.post('/groups/:id/send', async (req, res) => {
  const { content } = req.body;
  if (!content) return res.status(400).json({ error: 'content required' });

  try {
    const id = await groups.sendToGroup(req.params.id, content);
    res.json({ ok: true, id });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// ─── Config ───────────────────────────────────────────────────────────────────

app.get('/config', (req, res) => {
  const cfg = configManager.load();
  // Redact secret
  if (cfg.webhook?.secret) cfg.webhook.secret = '***';
  res.json(cfg);
});

app.patch('/config', (req, res) => {
  const cfg = configManager.load();
  const { webhook, mesh, profile } = req.body;
  if (webhook) Object.assign(cfg.webhook, webhook);
  if (mesh) Object.assign(cfg.mesh, mesh);
  if (profile) Object.assign(cfg.profile, profile);
  configManager.save(cfg);
  res.json({ ok: true });
});

// ─── Helpers ──────────────────────────────────────────────────────────────────

function formatPeer(p) {
  return {
    pk: p.pk,
    online: p.last_seen > Date.now() - PEER_TTL,
    handshaked: p.handshake === 1,
    firstSeen: p.first_seen,
    lastSeen: p.last_seen,
    meta: p.meta ? JSON.parse(p.meta) : {},
  };
}

function start() {
  app.listen(PORT, '127.0.0.1', () => {
    console.log(`[api] HTTP API v0.2.0 → http://127.0.0.1:${PORT}`);
  });
}

module.exports = { start };
