#!/usr/bin/env node
'use strict';
// Portable NIP-07 "Sign in with Nostr" signer — zero npm dependencies.
// Only Node.js built-ins (crypto, fs, os, path, http/https) + BigInt math.
// Same identity model as the full repo: HMAC-SHA256(master, domain) linking
// keys from ~/.config/nostr-auth/master.key.
//
// Usage:
//   node nostr_auth.js pubkey [--domain d]
//   node nostr_auth.js sign '<event-json>' [--domain d] [--callback url] [--dry-run] [--json]
//   node nostr_auth.js --challenge <str> [--relay url] [--callback url] [--dry-run] [--json]
const fs = require('fs');
const os = require('os');
const path = require('path');
const http = require('http');
const https = require('https');
const { createHash, createHmac, webcrypto } = require('crypto');

const VERSION = '1.0.0';
const HOME = process.env.NOSTR_AUTH_KEYFILE || path.join(os.homedir(), '.config', 'nostr-auth', 'master.key');

// --- secp256k1 / BIP-340 schnorr (BigInt) -----------------------------------
const P = 2n ** 256n - 2n ** 32n - 977n;
const N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141n;
const GX = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798n;
const GY = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8n;
const INFINITY = { x: 0n, y: 0n, z: 0n };

function mod(a, m) { const r = a % m; return r < 0n ? r + m : r; }
function powMod(b, e, m) {
  let r = 1n; b = mod(b, m);
  while (e > 0n) { if (e & 1n) r = (r * b) % m; b = (b * b) % m; e >>= 1n; }
  return r;
}
function inverse(a, m) { return powMod(a, m - 2n, m); }
function bigFrom(buf) { return BigInt('0x' + (buf.length ? Buffer.from(buf).toString('hex') : '0')); }
function buf32(big, label) {
  if (big < 0n) throw new Error(`${label} must be non-negative`);
  const hex = big.toString(16).padStart(64, '0');
  if (hex.length > 64) throw new Error(`${label} overflows 32 bytes`);
  return Buffer.from(hex, 'hex');
}
function sha256(...chunks) { const h = createHash('sha256'); chunks.forEach((c) => h.update(c)); return h.digest(); }
function taggedHash(tag, ...chunks) {
  const th = sha256(Buffer.from(tag, 'utf8'));
  return sha256(th, th, ...chunks);
}
function jacFrom(pt) { return { x: pt.x, y: pt.y, z: 1n }; }
function jacTo(j) {
  if (j.z === 0n) return null;
  const zi = inverse(j.z, P), zi2 = mod(zi * zi, P);
  return { x: mod(j.x * zi2, P), y: mod(j.y * zi2 * zi, P) };
}
function jacDouble(j) {
  if (j.z === 0n || j.y === 0n) return INFINITY;
  const s = mod(4n * j.x * j.y * j.y, P);
  const m = mod(3n * j.x * j.x, P);
  const x3 = mod(m * m - 2n * s, P);
  const y4 = mod(j.y * j.y, P);
  return { x: x3, y: mod(m * (s - x3) - 8n * y4 * y4, P), z: mod(2n * j.y * j.z, P) };
}
function jacAdd(a, b) {
  if (a.z === 0n) return b;
  if (b.z === 0n) return a;
  const z1z1 = mod(a.z * a.z, P), z2z2 = mod(b.z * b.z, P);
  const u1 = mod(a.x * z2z2, P), u2 = mod(b.x * z1z1, P);
  const s1 = mod(a.y * b.z * z2z2, P), s2 = mod(b.y * a.z * z1z1, P);
  const h = mod(u2 - u1, P);
  if (h === 0n) return s1 === s2 ? jacDouble(a) : INFINITY;
  const I = mod(4n * h * h, P), J = mod(h * I, P), r = mod(2n * (s2 - s1), P), v = mod(u1 * I, P);
  const x3 = mod(r * r - J - 2n * v, P);
  return { x: x3, y: mod(r * (v - x3) - 2n * s1 * J, P), z: mod((mod((a.z + b.z) * (a.z + b.z), P) - z1z1 - z2z2) * h, P) };
}
function scalarMul(k, pt) {
  let res = INFINITY, add = jacFrom(pt), n = k;
  while (n > 0n) { if (n & 1n) res = jacAdd(res, add); add = jacDouble(add); n >>= 1n; }
  return jacTo(res);
}
const G = { x: GX, y: GY };
function isEvenY(pt) { return mod(pt.y, 2n) === 0n; }
function getPublicKey(priv) {
  const d = bigFrom(priv);
  if (d === 0n || d >= N) throw new Error('private key out of range');
  const pt = scalarMul(d, G);
  return { xBytes: buf32(pt.x, 'pubkey x'), compressed: Buffer.from([isEvenY(pt) ? 2 : 3, ...buf32(pt.x, 'pubkey x')]).toString('hex'), evenY: isEvenY(pt) };
}
function sign(msg, priv) {
  if (msg.length !== 32) throw new Error('message must be 32 bytes');
  if (priv.length !== 32) throw new Error('private key must be 32 bytes');
  const d0 = bigFrom(priv);
  if (d0 === 0n || d0 >= N) throw new Error('private key out of range');
  const pubP = scalarMul(d0, G);
  const d = isEvenY(pubP) ? d0 : N - d0;
  const t = d ^ bigFrom(taggedHash('BIP0340/aux', Buffer.alloc(32)));
  const rand = taggedHash('BIP0340/nonce', buf32(t, 't'), buf32(pubP.x, 'px'), msg);
  const kp = bigFrom(rand) % N;
  if (kp === 0n) throw new Error('nonce zero; retry with different key material');
  const rP = scalarMul(kp, G);
  const k = isEvenY(rP) ? kp : N - kp;
  const e = bigFrom(taggedHash('BIP0340/challenge', buf32(rP.x, 'rx'), buf32(pubP.x, 'px'), msg)) % N;
  const s = mod(k + e * d, N);
  return Buffer.concat([buf32(rP.x, 'rx'), buf32(s, 's')]);
}

// --- bech32 (npub only) -------------------------------------------------------
const CHARSET = 'qpzry9x8gf2tvdw0s3jn54khce6mua7l';
const GENERATOR = [0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3];
function polymod(values) {
  let chk = 1;
  for (const v of values) {
    const top = chk >>> 25;
    chk = ((chk & 0x1ffffff) << 5) ^ v;
    for (let i = 0; i < 5; i++) if ((top >>> i) & 1) chk ^= GENERATOR[i];
  }
  return chk;
}
function hrpExpand(hrp) {
  const out = [];
  for (let i = 0; i < hrp.length; i++) out.push(hrp.charCodeAt(i) >>> 5);
  out.push(0);
  for (let i = 0; i < hrp.length; i++) out.push(hrp.charCodeAt(i) & 31);
  return out;
}
function bech32Encode(hrp, bytes) {
  let acc = 0, bits = 0;
  const data = [];
  for (const b of bytes) {
    acc = (acc << 8) | b; bits += 8;
    while (bits >= 5) { bits -= 5; data.push((acc >>> bits) & 31); }
  }
  if (bits > 0) data.push((acc << (5 - bits)) & 31);
  const values = [...hrpExpand(hrp), ...data, 0, 0, 0, 0, 0, 0];
  const pm = polymod(values) ^ 1;
  const checksum = [];
  for (let p = 0; p < 6; p++) checksum.push((pm >>> (5 * (5 - p))) & 31);
  return hrp + '1' + [...data, ...checksum].map((v) => CHARSET[v]).join('');
}
function toNpub(priv) { return bech32Encode('npub', getPublicKey(priv).xBytes); }

// --- keys -----------------------------------------------------------------------
function hexToBytes(hex) {
  const h = String(hex).trim().replace(/^0x/i, '');
  if (h.length % 2) throw new Error('Invalid hex: odd length');
  if (!/^[0-9a-fA-F]*$/.test(h)) throw new Error('Invalid hex');
  return Buffer.from(h, 'hex');
}
function randomBytes(n) {
  const a = new Uint8Array(n);
  webcrypto.getRandomValues(a);
  return Buffer.from(a);
}
function resolveMaster(opts) {
  if (opts.key) return hexToBytes(opts.key);
  const file = opts.keyfile || HOME;
  let existing = null;
  try { existing = hexToBytes(fs.readFileSync(file, 'utf8').trim()); } catch (e) { if (e.code !== 'ENOENT') throw e; }
  if (existing && !opts.generate) return existing;
  const fresh = randomBytes(32);
  fs.mkdirSync(path.dirname(file), { recursive: true, mode: 0o700 });
  fs.writeFileSync(file, fresh.toString('hex') + '\n', { mode: 0o600 });
  return fresh;
}
function deriveLinkingKey(master, domain, singleKey) {
  if (singleKey) return Buffer.from(master);
  let key = createHmac('sha256', master).update(Buffer.from(String(domain), 'utf8')).digest();
  while (bigFrom(key) >= N) key = createHmac('sha256', master).update(key).digest();
  return key;
}

// --- nostr event -------------------------------------------------------------------
function serializeEvent(ev) {
  return JSON.stringify([0, ev.pubkey, ev.created_at, ev.kind, ev.tags, ev.content]);
}
function eventId(ev) { return createHash('sha256').update(Buffer.from(serializeEvent(ev), 'utf8')).digest('hex'); }
function signEvent(template, priv) {
  const ev = {
    kind: Number(template.kind),
    tags: template.tags || [],
    content: String(template.content || ''),
    created_at: template.created_at != null ? Number(template.created_at) : Math.floor(Date.now() / 1000),
    pubkey: getPublicKey(priv).xBytes.toString('hex'),
  };
  ev.id = eventId(ev);
  ev.sig = Buffer.from(sign(Buffer.from(ev.id, 'hex'), priv)).toString('hex');
  return ev;
}
function normalizeDomain(input) {
  if (!input) return null;
  const s = String(input).trim().toLowerCase().replace(/^[/.]+/, '').replace(/[/.:]+$/, '');
  try { return new URL(s.includes('://') ? s : 'https://' + s).hostname; } catch (e) { return s; }
}

// --- request ------------------------------------------------------------------------
function postJSON(urlInput, payload) {
  return new Promise((resolve, reject) => {
    const url = new URL(urlInput);
    const mod = url.protocol === 'https:' ? https : http;
    const body = Buffer.from(payload, 'utf8');
    const req = mod.request(url, {
      method: 'POST', timeout: 15000,
      headers: { 'Content-Type': 'application/json', 'Content-Length': body.length, Accept: 'application/json', 'User-Agent': `nostr-auth/${VERSION}` },
    }, (res) => {
      const chunks = [];
      res.on('data', (c) => chunks.push(c));
      res.on('end', () => resolve({ status: res.statusCode, body: Buffer.concat(chunks).toString('utf8') }));
    });
    req.on('timeout', () => req.destroy(new Error('Request timed out')));
    req.on('error', reject);
    req.end(body);
  });
}

// --- CLI ----------------------------------------------------------------------------
function parseArgs(argv) {
  const o = { singleKey: false, dryRun: false, json: false, _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    const val = () => argv[++i];
    switch (a) {
      case '--event': o.event = val(); break;
      case '--challenge': o.challenge = val(); break;
      case '--relay': o.relay = val(); break;
      case '--domain': o.domain = val(); break;
      case '--callback': o.callback = val(); break;
      case '--key': o.key = val(); break;
      case '--keyfile': o.keyfile = val(); break;
      case '--generate': o.generate = true; break;
      case '--single-key': o.singleKey = true; break;
      case '--dry-run': o.dryRun = true; break;
      case '--json': o.json = true; break;
      case '-q': case '--quiet': o.quiet = true; break;
      case '-h': case '--help': o.help = true; break;
      case '--version': o.version = true; break;
      default:
        if (a.startsWith('-')) throw new Error(`Unknown option: ${a}`);
        o._.push(a);
    }
  }
  return o;
}

async function main() {
  const o = parseArgs(process.argv.slice(2));
  if (o.version) { console.log(VERSION); return; }
  if (o.help) {
    console.log(`nostr-auth (portable) v${VERSION}
  pubkey [--domain d]
  sign '<event-json>' [--domain d] [--callback url] [--dry-run] [--json]
  --challenge <str> [--relay url] [--callback url] [--dry-run] [--json]`);
    return;
  }

  const master = resolveMaster(o);
  const domain = normalizeDomain(o.domain || o.relay || (() => { try { return o.callback ? new URL(o.callback).hostname : 'nostr'; } catch (e) { return 'nostr'; } })());
  const priv = deriveLinkingKey(master, o.singleKey ? '<single-key>' : domain, o.singleKey);
  const pub = getPublicKey(priv);

  if (o._[0] === 'pubkey') {
    const out = { domain, pubkey: pub.xBytes.toString('hex'), pubkeyCompressed: pub.compressed, npub: toNpub(priv), singleKey: o.singleKey };
    console.log(o.json ? JSON.stringify(out, null, 2) : `domain : ${out.domain}\npubkey : ${out.pubkey}\nnpub   : ${out.npub}`);
    return;
  }

  let template;
  if (o.challenge) {
    template = { kind: 22242, tags: [['challenge', o.challenge], ...(o.relay ? [['relay', o.relay]] : [])], content: '' };
  } else {
    template = JSON.parse(o.event !== undefined ? o.event : o._[0]);
    if (!template || template.kind == null) throw new Error('Event template must include "kind"');
  }

  const event = signEvent(template, priv);
  if (!o.quiet) console.error(`domain   : ${domain}`);
  if (!o.quiet) console.error(`pubkey   : ${pub.xBytes.toString('hex')}`);
  if (!o.quiet) console.error(`npub     : ${toNpub(priv)}`);
  if (!o.quiet) console.error(`event id : ${event.id}`);

  if (o.dryRun) {
    console.log(o.json ? JSON.stringify({ domain, pubkey: pub.xBytes.toString('hex'), npub: toNpub(priv), event, dryRun: true }, null, 2) : JSON.stringify({ domain, eventId: event.id, dryRun: true }));
    return;
  }
  if (!o.callback) {
    console.log(o.json ? JSON.stringify({ domain, pubkey: pub.xBytes.toString('hex'), npub: toNpub(priv), event }, null, 2) : JSON.stringify(event));
    return;
  }

  const res = await postJSON(o.callback, JSON.stringify({ event }));
  let parsed = null;
  try { parsed = JSON.parse(res.body); } catch (e) {}
  if (res.status < 200 || res.status >= 300 || parsed === null) {
    console.error(`nostr-auth: callback returned non-JSON or HTTP ${res.status}`);
    process.exit(4);
  }
  console.log(JSON.stringify(parsed));
  process.exit(parsed && parsed.status === 'OK' ? 0 : 3);
}

main().catch((e) => {
  console.error(`nostr-auth: ${e.message}`);
  process.exit(1);
});