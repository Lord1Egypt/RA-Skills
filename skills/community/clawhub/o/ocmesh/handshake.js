/**
 * handshake.js
 * Auto-handshake new peers with a typed INTRO message.
 * v0.2: sends structured intro with capabilities, fires webhook on completion.
 */

const { MESSAGE_TYPES, create } = require('./protocol');
const webhook = require('./webhook');
const db = require('./db');

let identity = null;
let sendFn = null;
let ownProfile = null;

function start(id, messagingSend, getOwnProfileFn) {
  identity = id;
  sendFn = messagingSend;
  ownProfile = getOwnProfileFn;
}

async function handshakeNewPeer(pk) {
  const peer = db.prepare('SELECT handshake FROM peers WHERE pk = ?').get(pk);
  if (!peer || peer.handshake === 1) return;

  console.log(`[handshake] Initiating with ${pk.slice(0, 16)}...`);

  const profile = ownProfile ? ownProfile() : {};

  const intro = create(MESSAGE_TYPES.INTRO, {
    name: profile.name || `ocmesh-agent-${identity.pk.slice(0, 8)}`,
    capabilities: profile.capabilities || ['chat', 'task'],
    from: identity.pk,
  });

  try {
    await sendFn(pk, intro);
    db.prepare('UPDATE peers SET handshake = 1 WHERE pk = ?').run(pk);
    console.log(`[handshake] Complete with ${pk.slice(0, 16)}...`);

    await webhook.fire('peer.handshaked', { pk, ts: Date.now() });
  } catch (err) {
    console.error(`[handshake] Failed:`, err.message);
  }
}

module.exports = { start, handshakeNewPeer };
