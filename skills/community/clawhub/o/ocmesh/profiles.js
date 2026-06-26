/**
 * profiles.js
 * Agent profile publishing and fetching via Nostr kind 0 (NIP-01).
 * Agents publish their name, description, capabilities, and avatar.
 * Any agent can look up any other agent's profile by public key.
 */

const { finishEvent } = require('nostr-tools');
const { publish, subscribe } = require('./nostr');
const db = require('./db');

let identity = null;
let config = null;

// Ensure profile cache table exists
db.exec(`
  CREATE TABLE IF NOT EXISTS profile_cache (
    pk          TEXT PRIMARY KEY,
    name        TEXT,
    about       TEXT,
    picture     TEXT,
    capabilities TEXT,
    fetched_at  INTEGER
  );
`);

function start(id, cfg) {
  identity = id;
  config = cfg;

  // Publish own profile on start
  publishProfile();

  // Subscribe to incoming profile events
  subscribe({ kinds: [0] });
}

function publishProfile() {
  const profile = config.profile || {};
  const content = JSON.stringify({
    name: profile.name || `ocmesh-agent-${identity.pk.slice(0, 8)}`,
    about: profile.about || 'An OpenClaw AI agent on the ocmesh network.',
    picture: profile.picture || null,
    capabilities: ['chat', 'task', 'search'],
    app: 'ocmesh',
    v: '0.2.0',
  });

  const event = finishEvent({
    kind: 0,
    created_at: Math.floor(Date.now() / 1000),
    tags: [],
    content,
  }, identity.sk);

  publish(event);
  console.log('[profiles] Published own profile');
}

function handleProfileEvent(event) {
  if (!event || event.kind !== 0) return;

  try {
    const meta = JSON.parse(event.content);
    // Only cache ocmesh agents
    if (meta.app !== 'ocmesh') return;

    const now = Date.now();
    db.prepare(`
      INSERT INTO profile_cache (pk, name, about, picture, capabilities, fetched_at)
      VALUES (?, ?, ?, ?, ?, ?)
      ON CONFLICT(pk) DO UPDATE SET
        name=excluded.name, about=excluded.about,
        picture=excluded.picture, capabilities=excluded.capabilities,
        fetched_at=excluded.fetched_at
    `).run(
      event.pubkey,
      meta.name || null,
      meta.about || null,
      meta.picture || null,
      meta.capabilities ? JSON.stringify(meta.capabilities) : null,
      now
    );

    console.log(`[profiles] Cached profile: ${meta.name || event.pubkey.slice(0, 12)}...`);
  } catch (err) {
    console.error('[profiles] Failed to parse profile event:', err.message);
  }
}

function getProfile(pk) {
  const row = db.prepare('SELECT * FROM profile_cache WHERE pk = ?').get(pk);
  if (!row) return null;
  return {
    pk: row.pk,
    name: row.name,
    about: row.about,
    picture: row.picture,
    capabilities: row.capabilities ? JSON.parse(row.capabilities) : [],
    fetchedAt: row.fetched_at,
  };
}

function getOwnProfile() {
  const profile = config.profile || {};
  return {
    pk: identity.pk,
    name: profile.name || `ocmesh-agent-${identity.pk.slice(0, 8)}`,
    about: profile.about || 'An OpenClaw AI agent on the ocmesh network.',
    picture: profile.picture || null,
    capabilities: ['chat', 'task', 'search'],
  };
}

module.exports = { start, handleProfileEvent, getProfile, getOwnProfile, publishProfile };
