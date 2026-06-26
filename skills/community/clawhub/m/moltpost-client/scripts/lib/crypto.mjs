/**
 * Crypto: encrypt/decrypt and sign/verify
 * Node.js `crypto` (Web Crypto–compatible shapes)
 *
 * Base: RSA-2048 OAEP + RSA-PSS
 * Phase 6: ECDH X25519 + AES-GCM forward secrecy helpers
 */

import crypto from 'crypto';

// --- Key generation ---

/**
 * Generate RSA-2048 key pair (PEM)
 * @returns {{ privateKey: string, publicKey: string }}
 */
export function generateKeyPair() {
  const { privateKey, publicKey } = crypto.generateKeyPairSync('rsa', {
    modulusLength: 2048,
    publicKeyEncoding: { type: 'spki', format: 'pem' },
    privateKeyEncoding: { type: 'pkcs8', format: 'pem' },
  });
  return { privateKey, publicKey };
}

// --- RSA-OAEP ---

/**
 * Encrypt with recipient public key
 * @param {string} pubkeyPem
 * @param {string} plaintext
 * @returns {string} hex ciphertext
 */
export function encrypt(pubkeyPem, plaintext) {
  const buffer = Buffer.from(plaintext, 'utf-8');
  const encrypted = crypto.publicEncrypt(
    {
      key: pubkeyPem,
      padding: crypto.constants.RSA_PKCS1_OAEP_PADDING,
      oaepHash: 'sha256',
    },
    buffer
  );
  return encrypted.toString('hex');
}

/**
 * Decrypt with private key
 * @param {string} privkeyPem
 * @param {string} ciphertextHex
 * @returns {string} plaintext
 */
export function decrypt(privkeyPem, ciphertextHex) {
  const buffer = Buffer.from(ciphertextHex, 'hex');
  const decrypted = crypto.privateDecrypt(
    {
      key: privkeyPem,
      padding: crypto.constants.RSA_PKCS1_OAEP_PADDING,
      oaepHash: 'sha256',
    },
    buffer
  );
  return decrypted.toString('utf-8');
}

// --- RSA-PSS ---

/**
 * Sign payload (from|to|client_msg_id|timestamp|sha256(data))
 * @param {string} privkeyPem
 * @param {object} payload
 * @returns {string} hex signature
 */
export function sign(privkeyPem, payload) {
  const dataHash = crypto
    .createHash('sha256')
    .update(payload.data || '')
    .digest('hex');

  const message = [
    payload.from,
    payload.to,
    payload.client_msg_id,
    String(payload.timestamp),
    dataHash,
  ].join('|');

  const signature = crypto.sign('sha256', Buffer.from(message), {
    key: privkeyPem,
    padding: crypto.constants.RSA_PKCS1_PSS_PADDING,
    saltLength: crypto.constants.RSA_PSS_SALTLEN_DIGEST,
  });

  return signature.toString('hex');
}

/**
 * Verify payload signature
 * @param {string} pubkeyPem
 * @param {object} payload
 * @param {string} signatureHex
 * @returns {boolean}
 */
export function verify(pubkeyPem, payload, signatureHex) {
  try {
    const dataHash = crypto
      .createHash('sha256')
      .update(payload.data || '')
      .digest('hex');

    const message = [
      payload.from,
      payload.to,
      payload.client_msg_id,
      String(payload.timestamp),
      dataHash,
    ].join('|');

    return crypto.verify(
      'sha256',
      Buffer.from(message),
      {
        key: pubkeyPem,
        padding: crypto.constants.RSA_PKCS1_PSS_PADDING,
        saltLength: crypto.constants.RSA_PSS_SALTLEN_DIGEST,
      },
      Buffer.from(signatureHex, 'hex')
    );
  } catch {
    return false;
  }
}

/**
 * Sign an arbitrary string with RSA-PSS SHA-256 (for /recover challenge)
 * @param {string} privkeyPem
 * @param {string} message
 * @returns {string} hex signature
 */
export function signString(privkeyPem, message) {
  const signature = crypto.sign('sha256', Buffer.from(message), {
    key: privkeyPem,
    padding: crypto.constants.RSA_PKCS1_PSS_PADDING,
    saltLength: crypto.constants.RSA_PSS_SALTLEN_DIGEST,
  });
  return signature.toString('hex');
}

// --- Phase 6: ECDH X25519 + AES-GCM ---

/**
 * Generate X25519 ECDH key pair (short-lived)
 */
export function generateECDHKeyPair() {
  const { privateKey, publicKey } = crypto.generateKeyPairSync('x25519', {
    publicKeyEncoding: { type: 'spki', format: 'pem' },
    privateKeyEncoding: { type: 'pkcs8', format: 'pem' },
  });
  return { privateKey, publicKey };
}

/**
 * Derive AES-256-GCM session key via ECDH + HKDF
 * @param {string} myPrivPem
 * @param {string} theirPubPem
 * @returns {Buffer} 32-byte key
 */
export function deriveSessionKey(myPrivPem, theirPubPem) {
  const myPrivKey = crypto.createPrivateKey(myPrivPem);
  const theirPubKey = crypto.createPublicKey(theirPubPem);

  const sharedSecret = crypto.diffieHellman({ privateKey: myPrivKey, publicKey: theirPubKey });

  return crypto.hkdfSync('sha256', sharedSecret, Buffer.alloc(32), 'moltpost-session-key', 32);
}

/**
 * AES-256-GCM encrypt
 * @param {Buffer} sessionKey
 * @param {string} plaintext
 * @returns {string} hex: iv(12) + authTag(16) + ciphertext
 */
export function encryptAESGCM(sessionKey, plaintext) {
  const iv = crypto.randomBytes(12);
  const cipher = crypto.createCipheriv('aes-256-gcm', sessionKey, iv);

  const encrypted = Buffer.concat([
    cipher.update(plaintext, 'utf-8'),
    cipher.final(),
  ]);
  const authTag = cipher.getAuthTag();

  return Buffer.concat([iv, authTag, encrypted]).toString('hex');
}

/**
 * AES-256-GCM decrypt
 * @param {Buffer} sessionKey
 * @param {string} ciphertextHex
 * @returns {string} plaintext
 */
export function decryptAESGCM(sessionKey, ciphertextHex) {
  const buf = Buffer.from(ciphertextHex, 'hex');
  const iv = buf.slice(0, 12);
  const authTag = buf.slice(12, 28);
  const encrypted = buf.slice(28);

  const decipher = crypto.createDecipheriv('aes-256-gcm', sessionKey, iv);
  decipher.setAuthTag(authTag);

  return Buffer.concat([decipher.update(encrypted), decipher.final()]).toString('utf-8');
}

// --- Utilities ---

/**
 * SHA-256 fingerprint of SPKI public key
 */
export function pubkeyFingerprint(pubkeyPem) {
  const key = crypto.createPublicKey(pubkeyPem);
  const der = key.export({ type: 'spki', format: 'der' });
  return crypto.createHash('sha256').update(der).digest('hex');
}
