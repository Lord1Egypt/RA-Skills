/**
 * identity.js
 * Generates and persists a Nostr keypair for this ocmesh instance.
 * Uses nostr-tools v1 API (generatePrivateKey / getPublicKey).
 */

const { generatePrivateKey, getPublicKey } = require('nostr-tools');
const db = require('./db');

function loadOrCreateIdentity() {
  const row = db.prepare('SELECT sk, pk FROM identity LIMIT 1').get();

  if (row) {
    return {
      sk: row.sk,   // hex string in v1
      pk: row.pk,
    };
  }

  // First run — generate fresh keypair
  const sk = generatePrivateKey();  // returns hex string
  const pk = getPublicKey(sk);

  db.prepare('INSERT INTO identity (sk, pk) VALUES (?, ?)').run(sk, pk);

  console.log('[identity] Generated new keypair');
  console.log(`[identity] Public key: ${pk}`);

  return { sk, pk };
}

module.exports = { loadOrCreateIdentity };
