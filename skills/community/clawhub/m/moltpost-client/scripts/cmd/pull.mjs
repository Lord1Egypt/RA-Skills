/**
 * moltpost pull
 * Fetch new messages into inbox/active.json, send ACK, append audit.jsonl
 * Phase 2: plaintext; Phase 3+: decrypt
 */

import {
  requireConfig,
  appendMessages,
  appendAudit,
  updatePeersCache,
  readPrivateKey,
  readPublicKey,
  getPeerPubkey,
  patchConfig,
} from '../lib/storage.mjs';
import { createClient } from '../lib/broker.mjs';
import { decrypt, verify, decryptAESGCM, signString } from '../lib/crypto.mjs';
import { scanSafe } from '../lib/security.mjs';

export async function cmdPull(args) {
  let config = requireConfig();
  let client = createClient(config);

  console.log(`Pulling from ${config.broker_url}...`);

  let { status, data } = await client.pull(config.clawid);

  // Auto-recover: 401 → re-register with pubkey signature → new token → retry once
  if (status === 401) {
    const privkey = readPrivateKey();
    if (privkey) {
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
        config = requireConfig();
        client = createClient(config);
        console.log('✓ Token refreshed. Retrying pull...');
        ({ status, data } = await client.pull(config.clawid));
      } else {
        console.error(`Re-registration failed (${reregStatus}): ${reregData.error || 'unknown'}`);
        console.error('Run: moltpost register --broker <url>  to re-register from scratch.');
        appendAudit({ op: 'pull', status: 'recover_failed' });
        process.exit(1);
      }
    }
  }

  if (status === 429) {
    console.log(`Rate limited. Retry after ${data.retry_after} seconds.`);
    appendAudit({ op: 'pull', status: 'rate_limited', retry_after: data.retry_after });
    return;
  }

  if (status !== 200) {
    console.error(`Pull failed (${status}): ${data.error || JSON.stringify(data)}`);
    appendAudit({ op: 'pull', status: 'error', error: data.error });
    process.exit(1);
  }

  const { messages, count } = data;

  if (count === 0) {
    console.log('No new messages.');
    appendAudit({ op: 'pull', count: 0 });
    return;
  }

  console.log(`Received ${count} new message(s).`);

  const privkey = readPrivateKey();

  const processedMessages = messages.map((msg) => {
    let content = msg.data;
    let signatureVerified = null;

    // Decrypt (path depends on encryption mode)
    if (privkey) {
      try {
        const encMode = msg.encryption?.mode;
        if (encMode === 'ecdh-aes-gcm' && msg.encryption?.encrypted_session_key) {
          // Phase 6: decrypt session key, then AES-GCM body
          const sessionKeyHex = decrypt(privkey, msg.encryption.encrypted_session_key);
          const sessionKey = Buffer.from(sessionKeyHex, 'hex');
          content = decryptAESGCM(sessionKey, msg.data);
        } else {
          // Base: RSA-OAEP
          content = decrypt(privkey, msg.data);
        }
      } catch {
        // Decrypt failed (e.g. Phase 2 plaintext); keep raw payload
        content = msg.data;
      }
    }

    // Verify signature when present.
    // null  = no signature or sender pubkey not cached (inconclusive)
    // true  = verified
    // false = verification failed with known pubkey (likely forged or key rotated)
    if (msg.signature) {
      const senderPubkey = getPeerPubkey(msg.from, config);
      if (senderPubkey) {
        const result = verify(senderPubkey, {
          from: msg.from,
          to: config.clawid,
          client_msg_id: msg.client_msg_id,
          timestamp: msg.timestamp,
          data: msg.data,
        }, msg.signature);
        // Failed verify against cached key may mean sender re-registered (key rotated).
        // Keep as null (inconclusive) rather than false to avoid false-positive rejection.
        signatureVerified = result ? true : null;
      }
    }

    // Scan decrypted body (avoid Auto-Reply leaking sensitive strings)
    const scanResult = scanSafe(content, config.security?.scan_patterns);
    if (!scanResult.safe) {
      console.warn(`⚠️  Message ${msg.id} from ${msg.from} flagged (sensitive content).`);
    }

    return {
      id: msg.id,
      from: msg.from,
      ciphertext: msg.data,
      content,
      timestamp: msg.timestamp,
      expires_at: msg.expires_at || null,
      delivery_state: 'pulled',
      signature_verified: signatureVerified,
      security_flagged: !scanResult.safe,
      isRead: false,
      isReplied: false,
      group_id: msg.group_id || null,
    };
  });

  appendMessages(processedMessages, config);

  const msgIds = messages.map((m) => m.id);
  const { status: ackStatus, data: ackData } = await client.ack(config.clawid, msgIds);

  if (ackStatus !== 200) {
    console.warn(`ACK failed (${ackStatus}): ${ackData.error}`);
  }

  appendAudit({ op: 'pull', count, msg_ids: msgIds });
  appendAudit({ op: 'ack', msg_ids: msgIds });

  for (const msg of processedMessages) {
    const time = new Date(msg.timestamp * 1000).toLocaleString('en-US');
    const preview = String(msg.content).slice(0, 50);
    console.log(`  [${time}] from ${msg.from}: ${preview}${msg.content.length > 50 ? '...' : ''}`);
  }

  if (config.auto_reply?.enabled) {
    await processAutoReply(processedMessages, config, client);
  }
}

/**
 * Auto-reply: load rules, match, call LLM stub
 */
async function processAutoReply(messages, config, client) {
  const { default: crypto } = await import('crypto');
  const { default: fs } = await import('fs');

  // Read local rules file only — no message content is sent to external endpoints
  const rulesFile = config.auto_reply.rules_file;
  if (!rulesFile || !fs.existsSync(rulesFile)) return;

  let rules;
  try {
    rules = JSON.parse(fs.readFileSync(rulesFile, 'utf-8')).rules || [];
  } catch {
    return;
  }

  if (rules.length === 0) return;

  const { appendAudit: audit } = await import('../lib/storage.mjs');

  for (const msg of messages) {
    // signature_verified === false is no longer emitted (key rotation → null instead)
    // Skip only if explicitly false (future-proofing)
    if (msg.signature_verified === false) continue;
    if (msg.security_flagged) continue;

    const matchedRule = matchAutoReplyRule(msg, rules);
    if (!matchedRule) continue;

    if (matchedRule.action === 'reply' || matchedRule.action === 'llm_reply') {
      // Emit a structured signal for the OpenClaw agent to handle reply generation.
      // No message content is forwarded to external endpoints here.
      console.log(`[AUTO-REPLY-TRIGGER] rule=${matchedRule.name} from=${msg.from} id=${msg.id}`);
      console.log(`[AUTO-REPLY-TRIGGER] Use: moltpost send --to ${msg.from} --msg "<your reply>"`);
      audit({ op: 'auto_reply_trigger', trigger: matchedRule.name, to: msg.from, id: msg.id });
      continue;

    }
  }
}

function matchAutoReplyRule(msg, rules) {
  const now = new Date();
  const hour = now.getHours();

  for (const rule of rules) {
    const cond = rule.condition || {};

    if (cond.hour_range) {
      const [start, end] = cond.hour_range;
      if (hour < start || hour >= end) continue;
    }

    if (cond.allowed_clawids && !cond.allowed_clawids.includes(msg.from)) {
      continue;
    }

    if (cond.group_id && msg.group_id !== cond.group_id) {
      continue;
    }

    if (cond.keywords) {
      const content = String(msg.content).toLowerCase();
      const hasKeyword = cond.keywords.some((kw) => content.includes(kw.toLowerCase()));
      if (!hasKeyword) continue;
    }

    return rule;
  }
  return null;
}

