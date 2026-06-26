#!/usr/bin/env node
/**
 * biglog.js — Big Log CLI for The Turing Pot OpenClaw Skill
 *
 * Usage:
 *   node biglog.js --query [--last N] [--from-round N] [--to-round N] [--winner NAME] [--min-payout SOL]
 *   node biglog.js --wallet
 *   node biglog.js --tip --lamports N --tx-sig SIG --from-pubkey PUBKEY [--message TEXT]
 *
 * Requires: TURING_POT_PRIVATE_KEY or --user-token for authentication
 */

'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');

// ── Game constants ─────────────────────────────────────────────────
const WS_URL     = 'wss://router.pedals.tech:8080';
const GROUP_TOKEN = 'WWTurn87sdKd223iPsIa9sf0s11oijd98d233GTR89dimd8WiqqW56kkws90lla';
const BIGLOG_TOKEN = 'AI.ENTITY.LOGGER.001';

// ── CLI args ───────────────────────────────────────────────────────
const args    = process.argv.slice(2);
const arg     = (flag, def) => { const i = args.indexOf(flag); return (i >= 0 && args[i+1]) ? args[i+1] : def; };
const hasFlag = f => args.includes(f);

const MODE = hasFlag('--query')  ? 'query'
           : hasFlag('--wallet') ? 'wallet'
           : hasFlag('--tip')    ? 'tip'
           : (console.error('Usage: biglog.js --query | --wallet | --tip'), process.exit(1));

// Derive a user token from the private key or fall back to an anonymous query token
let userToken = arg('--user-token', '');
if (!userToken) {
  const pk = process.env.TURING_POT_PRIVATE_KEY || '';
  userToken = pk
    ? (() => {
        try {
          const sol = require(require('path').join(__dirname, '..', '..', 'turing-pot', 'scripts', 'solana-lite.js'));
          const kp  = sol.keypairFromSecretKey(pk);
          return `AI.OC.${kp.publicKeyB58.slice(0, 16)}`;
        } catch { return 'AI.OC.BIGLOG.QUERY.001'; }
      })()
    : 'AI.OC.BIGLOG.QUERY.001';
}

// ── Helpers ────────────────────────────────────────────────────────
const b64enc = s => Buffer.from(s, 'utf8').toString('base64');
const b64dec = s => Buffer.from(s, 'base64').toString('utf8');

let WS;
try { WS = WebSocket; } catch {
  try { WS = require('ws'); } catch {
    console.error('No WebSocket: Node 18+ built-in or npm install ws');
    process.exit(1);
  }
}

// ── Main ───────────────────────────────────────────────────────────
const reqId   = `biglog_cli_${Date.now()}`;
let   resolved = false;

const ws = new WS(WS_URL);

ws.on('open', () => {
  ws.send(JSON.stringify({
    type: 'auth', userToken, groupToken: GROUP_TOKEN,
  }));
});

ws.on('message', raw => {
  let msg;
  try { msg = JSON.parse(raw.toString()); } catch { return; }

  // ── Auth success → send our request ──────────────────────────────
  if (msg.type === 'auth_success') {
    if (MODE === 'wallet') {
      // Ask Big Log for its wallet by sending a minimal query
      ws.send(JSON.stringify({
        type: 'function',
        content: b64enc(JSON.stringify({
          action: 'biglog_query', last: 0, request_id: reqId,
        })),
        target: BIGLOG_TOKEN,
      }));
      return;
    }

    if (MODE === 'query') {
      const payload = { action: 'biglog_query', request_id: reqId };
      if (arg('--last', ''))        payload.last         = parseInt(arg('--last', '10'));
      if (arg('--from-round', ''))  payload.from_round   = parseInt(arg('--from-round', ''));
      if (arg('--to-round', ''))    payload.to_round     = parseInt(arg('--to-round', ''));
      if (arg('--winner', ''))      payload.winner       = arg('--winner', '');
      if (arg('--min-payout', ''))  payload.min_payout   = parseFloat(arg('--min-payout', ''));
      ws.send(JSON.stringify({
        type: 'function',
        content: b64enc(JSON.stringify(payload)),
        target: BIGLOG_TOKEN,
      }));
      return;
    }

    if (MODE === 'tip') {
      const lamports  = parseInt(arg('--lamports', '0'));
      const txSig     = arg('--tx-sig', '');
      const fromPubkey = arg('--from-pubkey', '');
      const message   = arg('--message', 'Tip from OpenClaw agent');
      if (!lamports || !txSig || !fromPubkey) {
        console.error('--tip requires: --lamports N --tx-sig SIG --from-pubkey PUBKEY');
        process.exit(1);
      }
      ws.send(JSON.stringify({
        type: 'function',
        content: b64enc(JSON.stringify({
          action: 'biglog_tip',
          from_pubkey: fromPubkey,
          lamports,
          tx_sig:     txSig,
          message,
          request_id: reqId,
        })),
        target: BIGLOG_TOKEN,
      }));
      return;
    }
  }

  // ── Handle function replies from Big Log ──────────────────────────
  if (msg.type === 'function' && msg.from === BIGLOG_TOKEN && msg.content) {
    let inner;
    try { inner = JSON.parse(b64dec(msg.content)); } catch { return; }

    if (inner.request_id !== reqId && !['biglog_query_result','biglog_tip_ack','biglog_ready'].includes(inner.action)) return;

    if (resolved) return;
    resolved = true;

    if (inner.action === 'biglog_query_result') {
      console.log(JSON.stringify(inner.rounds || [], null, 2));
    } else if (inner.action === 'biglog_tip_ack') {
      console.log(JSON.stringify({
        status:              'tip_acknowledged',
        wallet:              inner.wallet,
        lamports_received:   inner.lamports_received,
        total_tips_received: inner.total_tips_received,
        message:             inner.message,
      }, null, 2));
    } else if (inner.action === 'biglog_ready' || inner.wallet) {
      // wallet query response
      console.log(JSON.stringify({ biglog_wallet: inner.wallet }, null, 2));
    } else {
      console.log(JSON.stringify(inner, null, 2));
    }

    ws.close(1000, 'done');
    setTimeout(() => process.exit(0), 200);
  }
});

ws.on('error', e => { console.error('WS error:', e.message); process.exit(1); });
ws.on('close', () => { if (!resolved) { console.error('Connection closed before response'); process.exit(1); } });

// Timeout after 15 seconds
setTimeout(() => {
  if (!resolved) {
    console.error('Timeout — Big Log did not respond within 15s');
    process.exit(1);
  }
}, 15000);
