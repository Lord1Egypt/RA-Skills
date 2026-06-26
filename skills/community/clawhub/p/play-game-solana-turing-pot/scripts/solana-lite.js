/**
 * solana-lite.js — Pure Node.js Solana wallet utilities
 *
 * Zero npm dependencies. Uses only Node.js built-ins:
 *   crypto  (Ed25519 sign, SHA-256, SHA-512 via PBKDF2)
 *   https   (RPC calls)
 *
 * Covers exactly what the Turing Pot player needs:
 *   - base58 decode / encode
 *   - Keypair from 64-byte secret key (base58 string)
 *   - getBalance(pubkey)   → lamports (number)
 *   - getLatestBlockhash() → { blockhash, lastValidBlockHeight }
 *   - buildTransferTx(from, to, lamports, blockhash, feePayer) → Buffer
 *   - signTx(txBuf, keypair) → Buffer
 *   - sendRawTransaction(signedTxBuf) → signature (base58 string)
 *
 * Node.js 18+ required (for Ed25519 in crypto and native fetch).
 */

'use strict';

const crypto = require('crypto');
const https  = require('https');

// ─────────────────────────────────────────────────────────────────────────────
// Base58
// ─────────────────────────────────────────────────────────────────────────────

const B58_ALPHA = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz';
const B58_MAP   = new Uint8Array(256).fill(255);
for (let i = 0; i < B58_ALPHA.length; i++) B58_MAP[B58_ALPHA.charCodeAt(i)] = i;

function b58decode(str) {
  // Count leading '1's → leading zero bytes
  let leadingZeros = 0;
  for (const ch of str) { if (ch === '1') leadingZeros++; else break; }

  const digits = new Uint8Array(str.length);
  for (let i = 0; i < str.length; i++) {
    const v = B58_MAP[str.charCodeAt(i)];
    if (v === 255) throw new Error(`Invalid base58 character: '${str[i]}'`);
    digits[i] = v;
  }

  // Convert base58 big-endian digit array → bytes
  const result = [];
  for (let i = 0; i < digits.length; i++) {
    let carry = digits[i];
    for (let j = result.length - 1; j >= 0; j--) {
      carry += result[j] * 58;
      result[j] = carry & 0xff;
      carry >>= 8;
    }
    while (carry > 0) { result.unshift(carry & 0xff); carry >>= 8; }
  }

  const out = Buffer.alloc(leadingZeros + result.length);
  for (let i = 0; i < result.length; i++) out[leadingZeros + i] = result[i];
  return out;
}

function b58encode(buf) {
  const bytes = buf instanceof Buffer ? buf : Buffer.from(buf);

  let leadingZeros = 0;
  for (const b of bytes) { if (b === 0) leadingZeros++; else break; }

  const digits = [0];
  for (const byte of bytes) {
    let carry = byte;
    for (let j = digits.length - 1; j >= 0; j--) {
      carry += digits[j] << 8;
      digits[j] = carry % 58;
      carry = Math.floor(carry / 58);
    }
    while (carry > 0) { digits.unshift(carry % 58); carry = Math.floor(carry / 58); }
  }

  return '1'.repeat(leadingZeros) + digits.map(d => B58_ALPHA[d]).join('');
}

// ─────────────────────────────────────────────────────────────────────────────
// Keypair
// ─────────────────────────────────────────────────────────────────────────────

/**
 * Load a keypair from a base58-encoded 64-byte secret key.
 * Solana secret keys are [32-byte private scalar | 32-byte public key].
 *
 * Returns { secretKey: Buffer(64), publicKey: Buffer(32), publicKeyB58: string }
 */
function keypairFromSecretKey(base58SecretKey) {
  const secret = b58decode(base58SecretKey);
  if (secret.length !== 64) {
    throw new Error(`Expected 64-byte secret key, got ${secret.length} bytes. ` +
                    `Make sure you're providing the full keypair (not just the seed).`);
  }
  const publicKey = secret.slice(32); // last 32 bytes are the public key
  return {
    secretKey:     secret,
    publicKey:     publicKey,
    publicKeyB58:  b58encode(publicKey),
  };
}

// ─────────────────────────────────────────────────────────────────────────────
// Ed25519 signing
// ─────────────────────────────────────────────────────────────────────────────

/**
 * Sign a message buffer with an Ed25519 private key.
 * Node.js 15+ supports Ed25519 natively via crypto.sign().
 * We import the raw 32-byte seed (first half of the 64-byte secret key).
 *
 * Returns a 64-byte signature Buffer.
 */
function ed25519Sign(message, secretKey64) {
  // The seed is the first 32 bytes of the Solana secret key
  const seed = secretKey64.slice(0, 32);

  // Import as a raw Ed25519 private key (PKCS#8 wrapping required by Node crypto)
  // PKCS#8 header for Ed25519: 30 2e 02 01 00 30 05 06 03 2b 65 70 04 22 04 20 <32 bytes seed>
  const pkcs8Header = Buffer.from('302e020100300506032b657004220420', 'hex');
  const pkcs8Key    = Buffer.concat([pkcs8Header, seed]);

  const privateKey  = crypto.createPrivateKey({ key: pkcs8Key, format: 'der', type: 'pkcs8' });
  const signature   = crypto.sign(null, message, privateKey);
  return Buffer.from(signature);
}

// ─────────────────────────────────────────────────────────────────────────────
// Solana transaction wire format
//
// "Legacy" transaction format (pre-versioned):
//
//   [compact-u16: num_signatures]
//   [num_signatures × 64 bytes: signatures (zeroed until signed)]
//   [1 byte: num_required_signatures]
//   [1 byte: num_readonly_signed]
//   [1 byte: num_readonly_unsigned]
//   [compact-u16: num_accounts]
//   [num_accounts × 32 bytes: account pubkeys]
//   [32 bytes: recent_blockhash]
//   [compact-u16: num_instructions]
//   per instruction:
//     [1 byte: program_id_index into accounts array]
//     [compact-u16: num_accounts_for_ix]
//     [num_accounts_for_ix bytes: account indices]
//     [compact-u16: data_len]
//     [data_len bytes: instruction data]
//
// compact-u16 encoding: variable-length, 1–3 bytes.
//   values 0–127: one byte
//   values 128–16383: two bytes (low 7 bits | 0x80, high bits)
// ─────────────────────────────────────────────────────────────────────────────

function compactU16(n) {
  if (n < 0 || n > 65535) throw new Error(`compactU16 out of range: ${n}`);
  if (n <= 0x7f) return Buffer.from([n]);
  if (n <= 0x3fff) return Buffer.from([(n & 0x7f) | 0x80, (n >> 7) & 0x7f]);
  return Buffer.from([(n & 0x7f) | 0x80, ((n >> 7) & 0x7f) | 0x80, (n >> 14) & 0x03]);
}

/**
 * Build and sign a minimal SOL transfer (System Program transfer instruction).
 *
 * System Program transfer instruction data:
 *   [4 bytes LE: instruction index = 2]
 *   [8 bytes LE: lamports (u64)]
 *
 * Accounts for transfer:
 *   0: from (signer, writable)
 *   1: to   (writable)
 *   2: System Program (11111111111111111111111111111111)
 *
 * @param {object} keypair       - from keypairFromSecretKey()
 * @param {string} toB58         - destination public key (base58)
 * @param {number} lamports      - amount in lamports
 * @param {string} recentBlockhash - base58 blockhash
 * @returns {Buffer}             - signed transaction, ready to base64-encode and submit
 */
function buildSignedTransferTx(keypair, toB58, lamports, recentBlockhash) {
  const fromPubkey   = keypair.publicKey;            // Buffer(32)
  const toPubkey     = b58decode(toB58);             // Buffer(32)
  const systemProgram = Buffer.alloc(32);            // 32 zero bytes = 11111...
  const blockhash    = b58decode(recentBlockhash);   // Buffer(32)

  if (toPubkey.length   !== 32) throw new Error('Invalid destination pubkey');
  if (blockhash.length  !== 32) throw new Error('Invalid blockhash');
  if (!Number.isInteger(lamports) || lamports <= 0) throw new Error('lamports must be a positive integer');

  // Deduplicated ordered account list:
  // index 0: from   (signer, writable)
  // index 1: to     (writable, not signer)
  // index 2: system program (not writable, not signer)
  const accounts = [fromPubkey, toPubkey, systemProgram];

  // System transfer instruction data: [2 (u32 LE)] + [lamports (u64 LE)]
  const ixData = Buffer.alloc(12);
  ixData.writeUInt32LE(2, 0);               // instruction index 2 = Transfer
  // Write lamports as u64 LE — safe for values up to Number.MAX_SAFE_INTEGER
  const lo = lamports >>> 0;
  const hi = Math.floor(lamports / 0x100000000);
  ixData.writeUInt32LE(lo, 4);
  ixData.writeUInt32LE(hi, 8);

  // ── Assemble message ──────────────────────────────────────────────
  const msgParts = [];

  // Header: [num_required_sigs=1, num_readonly_signed=0, num_readonly_unsigned=1]
  msgParts.push(Buffer.from([1, 0, 1]));

  // Account addresses
  msgParts.push(compactU16(accounts.length));
  for (const acc of accounts) msgParts.push(acc);

  // Recent blockhash
  msgParts.push(blockhash);

  // Instructions (1 instruction)
  msgParts.push(compactU16(1));

  // Instruction: program_id_index=2 (system program), accounts=[0,1], data
  msgParts.push(Buffer.from([2]));                // program_id index
  msgParts.push(compactU16(2));                   // 2 account indices
  msgParts.push(Buffer.from([0, 1]));             // from=0, to=1
  msgParts.push(compactU16(ixData.length));
  msgParts.push(ixData);

  const message = Buffer.concat(msgParts);

  // ── Sign ──────────────────────────────────────────────────────────
  const signature = ed25519Sign(message, keypair.secretKey);

  // ── Assemble transaction ──────────────────────────────────────────
  const txParts = [];
  txParts.push(compactU16(1));       // 1 signature
  txParts.push(signature);           // 64-byte signature
  txParts.push(message);

  return Buffer.concat(txParts);
}

// ─────────────────────────────────────────────────────────────────────────────
// JSON-RPC helpers
// ─────────────────────────────────────────────────────────────────────────────

/**
 * Make a Solana JSON-RPC POST request.
 * Uses native https (no fetch needed, works Node 14+).
 */
function rpcCall(rpcUrl, method, params) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify({
      jsonrpc: '2.0', id: 1, method, params,
    });

    const url    = new URL(rpcUrl);
    const options = {
      hostname: url.hostname,
      port:     url.port || 443,
      path:     url.pathname + url.search,
      method:   'POST',
      headers:  {
        'Content-Type':   'application/json',
        'Content-Length': Buffer.byteLength(body),
      },
    };

    const proto = url.protocol === 'http:' ? require('http') : https;
    const req = proto.request(options, res => {
      const chunks = [];
      res.on('data', d => chunks.push(d));
      res.on('end', () => {
        try {
          const json = JSON.parse(Buffer.concat(chunks).toString());
          if (json.error) reject(new Error(`RPC error ${json.error.code}: ${json.error.message}`));
          else resolve(json.result);
        } catch (e) { reject(e); }
      });
    });

    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

/**
 * Get the SOL balance for a base58 public key.
 * Returns balance in lamports (number).
 */
async function getBalance(rpcUrl, pubkeyB58) {
  const result = await rpcCall(rpcUrl, 'getBalance', [
    pubkeyB58,
    { commitment: 'confirmed' },
  ]);
  return result.value; // lamports
}

/**
 * Get the latest blockhash.
 * Returns { blockhash: string, lastValidBlockHeight: number }
 */
async function getLatestBlockhash(rpcUrl) {
  const result = await rpcCall(rpcUrl, 'getLatestBlockhash', [
    { commitment: 'confirmed' },
  ]);
  return result.value; // { blockhash, lastValidBlockHeight }
}

/**
 * Send a signed transaction to the network.
 * @param {Buffer} signedTx - fully signed transaction buffer
 * Returns the transaction signature as a base58 string.
 */
async function sendRawTransaction(rpcUrl, signedTx) {
  const encoded = signedTx.toString('base64');
  const sig = await rpcCall(rpcUrl, 'sendTransaction', [
    encoded,
    { encoding: 'base64', preflightCommitment: 'confirmed' },
  ]);
  return sig; // base58 transaction signature
}

/**
 * Convenience: build, sign, and send a SOL transfer in one call.
 *
 * @param {object} keypair    - from keypairFromSecretKey()
 * @param {string} toB58      - destination pubkey (base58)
 * @param {number} lamports   - amount in lamports
 * @param {string} rpcUrl     - Solana RPC endpoint
 * @returns {string}          - transaction signature (base58)
 */
async function transfer(keypair, toB58, lamports, rpcUrl) {
  const { blockhash } = await getLatestBlockhash(rpcUrl);
  const signedTx      = buildSignedTransferTx(keypair, toB58, lamports, blockhash);
  const sig           = await sendRawTransaction(rpcUrl, signedTx);
  return sig;
}

// ─────────────────────────────────────────────────────────────────────────────
// Exports
// ─────────────────────────────────────────────────────────────────────────────

module.exports = {
  // Base58
  b58decode,
  b58encode,

  // Keypair
  keypairFromSecretKey,

  // Transactions
  buildSignedTransferTx,

  // RPC
  getBalance,
  getLatestBlockhash,
  sendRawTransaction,

  // Convenience
  transfer,
};
