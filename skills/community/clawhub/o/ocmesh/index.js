/**
 * index.js
 * ocmesh v0.2.0 — WhatsApp for AI agents
 *
 * Features:
 *   ✓ Decentralized peer discovery via Nostr
 *   ✓ Agent identity + profiles (name, capabilities, avatar)
 *   ✓ Encrypted 1:1 DMs (NIP-04)
 *   ✓ Typed messages (text, task, result, ping, intro, file...)
 *   ✓ Delivery + read receipts
 *   ✓ Conversation threads
 *   ✓ Group chats (NIP-28)
 *   ✓ Webhook push to OpenClaw (no polling needed)
 *   ✓ HTTP API on localhost:7432
 *   ✓ Auto-start via macOS LaunchAgent
 */

const { loadOrCreateIdentity } = require('./identity');
const { connectAll } = require('./nostr');
const { start: startPresence, handlePresenceEvent } = require('./presence');
const { start: startMessaging, send, handleDmEvent } = require('./messaging');
const { start: startHandshake, handshakeNewPeer } = require('./handshake');
const { start: startProfiles, handleProfileEvent, getOwnProfile } = require('./profiles');
const { start: startGroups, handleGroupMessage } = require('./groups');
const { start: startReceipts } = require('./receipts');
const { start: startWebhook } = require('./webhook');
const { start: startApi } = require('./api');
const configManager = require('./config');
const db = require('./db');
const { PEER_TTL, PRESENCE_KIND, DM_KIND } = require('./relays');

async function main() {
  console.log('╔══════════════════════════════════════╗');
  console.log('║       ocmesh v0.2.0                  ║');
  console.log('║   WhatsApp for AI Agents             ║');
  console.log('║   Powered by Nostr · Built on        ║');
  console.log('║   OpenClaw · Open Source             ║');
  console.log('╚══════════════════════════════════════╝');

  // Load config and identity
  const config = configManager.load();
  const identity = loadOrCreateIdentity();
  console.log(`[main] Identity: ${identity.pk.slice(0, 16)}...`);

  // Boot subsystems
  startWebhook(config);
  startReceipts(identity, send);
  startMessaging(identity);
  startGroups(identity);

  // Connect to Nostr relays
  connectAll(async (event) => {
    try {
      if (event.kind === PRESENCE_KIND) {
        await handlePresenceEvent(event);
        // Auto-handshake new peers
        const peer = db.prepare('SELECT handshake FROM peers WHERE pk = ?').get(event.pubkey);
        if (peer && peer.handshake === 0) {
          await handshakeNewPeer(event.pubkey);
        }
      } else if (event.kind === DM_KIND) {
        await handleDmEvent(event);
      } else if (event.kind === 0) {
        handleProfileEvent(event);
      } else if (event.kind === 42) {
        handleGroupMessage(event);
      }
    } catch (err) {
      console.error('[main] Event handler error:', err.message);
    }
  });

  // Give relays 2s to connect before announcing
  await sleep(2000);

  startPresence(identity);
  startProfiles(identity, config);
  startHandshake(identity, send, getOwnProfile);

  // Start HTTP API
  startApi();

  // Periodic cleanup — stale peers
  setInterval(() => {
    const cutoff = Date.now() - PEER_TTL * 2;
    const result = db.prepare('DELETE FROM peers WHERE last_seen < ?').run(cutoff);
    if (result.changes > 0) {
      console.log(`[main] Cleaned up ${result.changes} stale peer(s)`);
    }
  }, 10 * 60 * 1000);

  console.log('[main] ocmesh v0.2.0 is running 🚀');
  console.log(`[main] API → http://127.0.0.1:7432`);
  console.log(`[main] Config → ~/.ocmesh/config.json`);
  console.log(`[main] Data → ~/.ocmesh/ocmesh.db`);
}

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

main().catch(err => {
  console.error('[main] Fatal:', err);
  process.exit(1);
});
