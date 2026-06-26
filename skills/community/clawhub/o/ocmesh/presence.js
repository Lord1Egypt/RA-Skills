/**
 * presence.js
 * Presence announcements and peer discovery via Nostr kind 31337.
 * v0.2: fires webhook on new peer discovery.
 */

const { finishEvent } = require('nostr-tools');
const { publish, subscribe } = require('./nostr');
const { PRESENCE_KIND, ANNOUNCE_INTERVAL, DISCOVERY_INTERVAL, PEER_TTL } = require('./relays');
const webhook = require('./webhook');
const db = require('./db');

let identity = null;

function start(id) {
  identity = id;
  announce();
  discover();
  setInterval(announce, ANNOUNCE_INTERVAL);
  setInterval(discover, DISCOVERY_INTERVAL);
}

function announce() {
  const event = finishEvent({
    kind: PRESENCE_KIND,
    created_at: Math.floor(Date.now() / 1000),
    tags: [
      ['d', 'ocmesh-presence'],
      ['app', 'ocmesh'],
      ['v', '0.2.0'],
    ],
    content: 'ocmesh-agent-online',
  }, identity.sk);

  publish(event);
  console.log('[presence] Announced online');
}

function discover() {
  const since = Math.floor((Date.now() - PEER_TTL) / 1000);
  subscribe({ kinds: [PRESENCE_KIND], since });
  console.log('[presence] Discovery scan started');
}

async function handlePresenceEvent(event) {
  if (!event?.pubkey) return;
  if (identity && event.pubkey === identity.pk) return;

  const isOcmesh = event.tags?.some(([k, v]) => k === 'app' && v === 'ocmesh');
  if (!isOcmesh) return;

  const now = Date.now();
  const existing = db.prepare('SELECT pk FROM peers WHERE pk = ?').get(event.pubkey);

  if (existing) {
    db.prepare('UPDATE peers SET last_seen = ? WHERE pk = ?').run(now, event.pubkey);
  } else {
    const version = event.tags?.find(([k]) => k === 'v')?.[1];
    db.prepare(`
      INSERT INTO peers (pk, first_seen, last_seen, handshake, meta)
      VALUES (?, ?, ?, 0, ?)
    `).run(event.pubkey, now, now, JSON.stringify({ version }));

    console.log(`[presence] New peer: ${event.pubkey.slice(0, 16)}...`);

    await webhook.fire('peer.discovered', {
      pk: event.pubkey,
      version,
      ts: now,
    });
  }
}

module.exports = { start, handlePresenceEvent };
