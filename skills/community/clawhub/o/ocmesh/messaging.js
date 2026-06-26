/**
 * messaging.js
 * Encrypted agent-to-agent DMs via Nostr NIP-04.
 * v0.2: typed messages, delivery receipts, thread tracking, webhook push.
 */

const { finishEvent, nip04 } = require('nostr-tools');
const { publish, subscribe } = require('./nostr');
const { DM_KIND } = require('./relays');
const { parse, MESSAGE_TYPES } = require('./protocol');
const { touchThread } = require('./threads');
const { handleReceipt, sendDelivered } = require('./receipts');
const webhook = require('./webhook');
const db = require('./db');

let identity = null;

function start(id) {
  identity = id;

  subscribe({
    kinds: [DM_KIND],
    '#p': [identity.pk],
    since: Math.floor(Date.now() / 1000) - 60,
  });

  console.log('[messaging] Listening for encrypted DMs');
}

async function send(toPk, content) {
  const encrypted = await nip04.encrypt(identity.sk, toPk, content);
  const now = Math.floor(Date.now() / 1000);

  const event = finishEvent({
    kind: DM_KIND,
    created_at: now,
    tags: [['p', toPk]],
    content: encrypted,
  }, identity.sk);

  publish(event);
  console.log(`[messaging] Sent DM to ${toPk.slice(0, 16)}...`);
  return event.id;
}

async function handleDmEvent(event) {
  if (!event || !identity) return;
  if (event.pubkey === identity.pk) return;

  const toPk = event.tags?.find(([k]) => k === 'p')?.[1];
  if (toPk !== identity.pk) return;

  try {
    const decrypted = await nip04.decrypt(identity.sk, event.pubkey, event.content);

    const existing = db.prepare('SELECT id FROM messages WHERE id = ?').get(event.id);
    if (existing) return;

    const parsed = parse(decrypted);
    const msgType = parsed?.type || 'text';

    // Handle receipt messages — don't store as normal messages
    if (msgType === MESSAGE_TYPES.DELIVERED || msgType === MESSAGE_TYPES.READ) {
      handleReceipt(db, event, parsed);
      return;
    }

    // Handle ping → auto pong
    if (msgType === MESSAGE_TYPES.PING) {
      const { create } = require('./protocol');
      await send(event.pubkey, create(MESSAGE_TYPES.PONG, {}));
      return;
    }

    // Store message
    db.prepare(`
      INSERT INTO messages (id, from_pk, to_pk, content, msg_type, received_at, read, delivered)
      VALUES (?, ?, ?, ?, ?, ?, 0, 0)
    `).run(event.id, event.pubkey, identity.pk, decrypted, msgType, Date.now());

    console.log(`[messaging] New ${msgType} from ${event.pubkey.slice(0, 16)}...`);

    // Update thread
    touchThread(event.pubkey, decrypted, Date.now());

    // Auto-add peer if new
    const peer = db.prepare('SELECT pk FROM peers WHERE pk = ?').get(event.pubkey);
    if (!peer) {
      const now = Date.now();
      db.prepare(`
        INSERT INTO peers (pk, first_seen, last_seen, handshake, meta)
        VALUES (?, ?, ?, 1, ?)
      `).run(event.pubkey, now, now, JSON.stringify({ via: 'dm' }));
    } else {
      db.prepare('UPDATE peers SET last_seen = ?, handshake = 1 WHERE pk = ?')
        .run(Date.now(), event.pubkey);
    }

    // Send delivery receipt
    await sendDelivered(event.pubkey, event.id);

    // Webhook push
    await webhook.fire('message.received', {
      id: event.id,
      from: event.pubkey,
      type: msgType,
      content: decrypted,
      ts: Date.now(),
    });

  } catch (err) {
    console.error('[messaging] Failed to handle DM:', err.message);
  }
}

module.exports = { start, send, handleDmEvent };
