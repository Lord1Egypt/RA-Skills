/**
 * groups.js
 * Multi-agent group conversations.
 *
 * Groups are implemented as a shared Nostr channel (NIP-28, kind 40/42).
 * The group creator publishes a kind-40 channel creation event.
 * Messages to the group are kind-42 events referencing the channel.
 * All members subscribe to the channel and receive messages.
 */

const { finishEvent } = require('nostr-tools');
const { publish, subscribe } = require('./nostr');
const { nip04 } = require('nostr-tools');
const db = require('./db');

let identity = null;

db.exec(`
  CREATE TABLE IF NOT EXISTS groups (
    id          TEXT PRIMARY KEY,   -- channel event id
    name        TEXT NOT NULL,
    about       TEXT,
    creator_pk  TEXT NOT NULL,
    created_at  INTEGER NOT NULL,
    member_pks  TEXT                -- JSON array
  );

  CREATE TABLE IF NOT EXISTS group_messages (
    id          TEXT PRIMARY KEY,
    group_id    TEXT NOT NULL,
    from_pk     TEXT NOT NULL,
    content     TEXT NOT NULL,
    received_at INTEGER NOT NULL
  );
`);

function start(id) {
  identity = id;

  // Subscribe to group channel messages we're part of
  const myGroups = db.prepare('SELECT id FROM groups').all();
  for (const group of myGroups) {
    subscribeToGroup(group.id);
  }

  console.log(`[groups] Monitoring ${myGroups.length} group(s)`);
}

async function createGroup(name, about, memberPks = []) {
  const now = Math.floor(Date.now() / 1000);

  const event = finishEvent({
    kind: 40,
    created_at: now,
    tags: [],
    content: JSON.stringify({ name, about, picture: null }),
  }, identity.sk);

  publish(event);

  const allMembers = [...new Set([identity.pk, ...memberPks])];

  db.prepare(`
    INSERT INTO groups (id, name, about, creator_pk, created_at, member_pks)
    VALUES (?, ?, ?, ?, ?, ?)
  `).run(event.id, name, about || null, identity.pk, Date.now(), JSON.stringify(allMembers));

  subscribeToGroup(event.id);

  console.log(`[groups] Created group "${name}" with id ${event.id.slice(0, 12)}...`);
  return { id: event.id, name, about, members: allMembers };
}

async function sendToGroup(groupId, content) {
  const group = db.prepare('SELECT * FROM groups WHERE id = ?').get(groupId);
  if (!group) throw new Error(`Group not found: ${groupId}`);

  const now = Math.floor(Date.now() / 1000);

  const event = finishEvent({
    kind: 42,
    created_at: now,
    tags: [['e', groupId, '', 'root']],
    content,
  }, identity.sk);

  publish(event);

  // Store own message
  db.prepare(`
    INSERT OR IGNORE INTO group_messages (id, group_id, from_pk, content, received_at)
    VALUES (?, ?, ?, ?, ?)
  `).run(event.id, groupId, identity.pk, content, Date.now());

  console.log(`[groups] Sent to group ${groupId.slice(0, 12)}...`);
  return event.id;
}

function subscribeToGroup(groupId) {
  subscribe({
    kinds: [42],
    '#e': [groupId],
    since: Math.floor(Date.now() / 1000) - 3600,
  });
}

function handleGroupMessage(event) {
  if (!event || event.kind !== 42) return;

  const rootTag = event.tags.find(([k, , , marker]) => k === 'e' && marker === 'root');
  if (!rootTag) return;

  const groupId = rootTag[1];
  const group = db.prepare('SELECT id FROM groups WHERE id = ?').get(groupId);
  if (!group) return; // not a group we know

  const existing = db.prepare('SELECT id FROM group_messages WHERE id = ?').get(event.id);
  if (existing) return;

  db.prepare(`
    INSERT INTO group_messages (id, group_id, from_pk, content, received_at)
    VALUES (?, ?, ?, ?, ?)
  `).run(event.id, groupId, event.pubkey, event.content, Date.now());

  console.log(`[groups] Message in group ${groupId.slice(0, 12)}... from ${event.pubkey.slice(0, 12)}...`);
}

function listGroups() {
  return db.prepare('SELECT * FROM groups ORDER BY created_at DESC').all().map(g => ({
    ...g,
    member_pks: g.member_pks ? JSON.parse(g.member_pks) : [],
  }));
}

function getGroupMessages(groupId, limit = 50) {
  return db.prepare(`
    SELECT * FROM group_messages WHERE group_id = ? ORDER BY received_at DESC LIMIT ?
  `).all(groupId, limit).reverse();
}

module.exports = {
  start,
  createGroup,
  sendToGroup,
  handleGroupMessage,
  listGroups,
  getGroupMessages,
};
