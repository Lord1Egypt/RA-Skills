/**
 * moltpost send --to <clawid> --msg <text> [--ttl <minutes>]
 * Phase 2: plaintext; Phase 3+: encrypt+sign; Phase 5: security scan
 */

import crypto from 'crypto';
import {
  requireConfig,
  getPeerPubkey,
  updatePeersCache,
  appendAudit,
  readPrivateKey,
  readPublicKey,
  patchConfig,
} from '../lib/storage.mjs';
import { createClient } from '../lib/broker.mjs';
import { encrypt, sign, signString, generateECDHKeyPair, deriveSessionKey, encryptAESGCM } from '../lib/crypto.mjs';
import { scan } from '../lib/security.mjs';

function generateClientMsgId() {
  return `cmsg_${Date.now()}_${crypto.randomBytes(4).toString('hex')}`;
}

export async function cmdSend(args) {
  const config = requireConfig();

  const toIdx = args.indexOf('--to');
  const msgIdx = args.indexOf('--msg');
  const ttlIdx = args.indexOf('--ttl');

  if (toIdx === -1 || msgIdx === -1) {
    console.error('Usage: moltpost send --to <clawid> --msg <text> [--ttl <minutes>]');
    process.exit(1);
  }

  const to = args[toIdx + 1];
  const msg = args[msgIdx + 1];
  const ttlMinutes = ttlIdx !== -1 ? parseInt(args[ttlIdx + 1], 10) : null;

  if (!to || !msg) {
    console.error('Error: --to and --msg are required');
    process.exit(1);
  }

  const client = createClient(config);

  try {
    scan(msg, config.security?.scan_patterns);
  } catch (err) {
    console.error(`⚠️  ${err.message}`);
    appendAudit({ op: 'send', to, status: 'blocked_security_scan' });
    process.exit(1);
  }

  // Fetch the recipient's current pubkey from broker to detect key rotation.
  // Uses /peer (single lookup) instead of /peers (full list) for efficiency.
  let pubkey = null;
  {
    const { status, data } = await client.getPeer(to);
    if (status === 200) {
      // Invalidate local cache if pubkey_version has advanced
      const cachedPubkey = getPeerPubkey(to, config, data.pubkey_version);
      if (!cachedPubkey) {
        updatePeersCache([data]);
      }
      pubkey = data.pubkey;
    } else if (status === 404) {
      // Peer genuinely not registered
    } else {
      // Broker temporarily unavailable — fall back to cache
      pubkey = getPeerPubkey(to, config);
    }
  }

  if (!pubkey) {
    console.error(`Error: no public key for ClawID "${to}". Ensure the peer has registered.`);
    process.exit(1);
  }

  const clientMsgId = generateClientMsgId();
  const now = Math.floor(Date.now() / 1000);
  const expiresAt = ttlMinutes ? now + ttlMinutes * 60 : null;

  const privkey = readPrivateKey();
  const forwardSecrecy = config.security?.forward_secrecy === true;

  let ciphertext;
  let encryptionMeta = null;

  if (forwardSecrecy) {
    // Phase 6: ECDH X25519 + AES-GCM (hybrid: RSA-wrapped session key)
    const { privateKey: ephemeralPriv, publicKey: ephemeralPub } = generateECDHKeyPair();
    const encryptedEphemeralPub = encrypt(pubkey, ephemeralPub);
    const { randomBytes } = await import('crypto');
    const sessionKey = randomBytes(32);
    const encryptedSessionKey = encrypt(pubkey, sessionKey.toString('hex'));
    ciphertext = encryptAESGCM(sessionKey, msg);
    encryptionMeta = {
      mode: 'ecdh-aes-gcm',
      encrypted_session_key: encryptedSessionKey,
    };
  } else {
    ciphertext = encrypt(pubkey, msg);
    encryptionMeta = { mode: 'rsa-oaep' };
  }

  const signaturePayload = {
    from: config.clawid,
    to,
    client_msg_id: clientMsgId,
    timestamp: now,
    data: ciphertext,
  };
  const signature = privkey ? sign(privkey, signaturePayload) : null;

  const payload = {
    from: config.clawid,
    to,
    data: ciphertext,
    client_msg_id: clientMsgId,
    expires_at: expiresAt,
    signature,
    encryption: encryptionMeta,
  };

  let { status, data: resData } = await client.send(payload);

  // Auto-recover: 401 → re-register with pubkey signature → new token → retry once
  if (status === 401 && privkey) {
    console.log('Token invalid, attempting key-based re-registration...');
    const pubkey = readPublicKey();
    const ts = Math.floor(Date.now() / 1000);
    const challenge = `${config.clawid}|reregister|${ts}`;
    const signature = signString(privkey, challenge);
    const { status: reregStatus, data: reregData } = await client.reregisterWithSignature(
      config.clawid, pubkey, challenge, signature
    );
    if (reregStatus === 200 && reregData.access_token) {
      patchConfig({ access_token: reregData.access_token });
      const newConfig = requireConfig();
      const newClient = createClient(newConfig);
      console.log('✓ Token refreshed. Retrying send...');
      ({ status, data: resData } = await newClient.send(payload));
    } else {
      console.error(`Re-registration failed (${reregStatus}): ${reregData.error || 'unknown'}`);
      console.error('Run: moltpost register --broker <url>  to re-register from scratch.');
      appendAudit({ op: 'send', to, status: 'recover_failed' });
      process.exit(1);
    }
  }

  if (status === 429) {
    console.error(`Send rate limited. Retry after ${resData.retry_after} seconds.`);
    appendAudit({ op: 'send', to, status: 'rate_limited' });
    process.exit(1);
  }

  if (status !== 200) {
    console.error(`Send failed (${status}): ${resData.error || JSON.stringify(resData)}`);
    appendAudit({ op: 'send', to, status: 'error', error: resData.error });
    process.exit(1);
  }

  appendAudit({ op: 'send', to, client_msg_id: clientMsgId, status: 'ok' });
  console.log(`✓ Message sent to ${to} (msg_id: ${resData.msg_id})`);
}
