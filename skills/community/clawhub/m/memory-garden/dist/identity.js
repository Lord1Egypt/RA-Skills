"use strict";
// Instance identity management for Memory Garden MCP skill
// CR-1: Use crypto.sign/verify for Ed25519 (not createSign/createVerify)
// IR-1: Configurable identity dir for test isolation
// IR-5: Atomic identity generation with single file + temp rename
// TR-2: Permission check at identity load time
// CR-4: Safe HOME resolution with fallback
// CR-9: Try-catch around JSON.parse
// CR-10: Canonical JSON with sorted keys
Object.defineProperty(exports, "__esModule", { value: true });
exports.ensureIdentity = ensureIdentity;
exports.signData = signData;
exports.signMessage = signMessage;
exports.verifyMessage = verifyMessage;
exports.verifySignature = verifySignature;
exports.getAgentId = getAgentId;
exports.createValidationAttestation = createValidationAttestation;
const crypto_1 = require("crypto");
const fs_1 = require("fs");
const path_1 = require("path");
// CR-4: Safe HOME resolution with fallback to USERPROFILE (Windows)
function getHomeDir() {
    const home = process.env.HOME || process.env.USERPROFILE;
    if (!home) {
        throw new Error('HOME environment variable not set. ' +
            'Set MG_IDENTITY_DIR environment variable to specify identity directory explicitly.');
    }
    return home;
}
// IR-1: Configurable via env var for test isolation
// CR-4: Use safe HOME resolution
const IDENTITY_DIR = process.env.MG_IDENTITY_DIR ||
    (0, path_1.join)(getHomeDir(), '.memory-garden', 'identity');
const IDENTITY_FILE = (0, path_1.join)(IDENTITY_DIR, 'identity.json');
// CR-10: Canonical JSON with sorted keys for cross-language signature compatibility
function canonicalJson(obj) {
    const sorted = {};
    for (const key of Object.keys(obj).sort()) {
        sorted[key] = obj[key];
    }
    return JSON.stringify(sorted);
}
/**
 * Ensures an identity exists, generating one if needed.
 * Returns the agent identity (without private key).
 */
function ensureIdentity() {
    if (!(0, fs_1.existsSync)(IDENTITY_DIR)) {
        (0, fs_1.mkdirSync)(IDENTITY_DIR, { recursive: true, mode: 0o700 });
    }
    if (!(0, fs_1.existsSync)(IDENTITY_FILE)) {
        generateIdentity();
    }
    return loadIdentity();
}
/**
 * Generates a new Ed25519 identity and stores it atomically.
 * IR-5: Uses temp file + rename for atomicity.
 */
function generateIdentity() {
    const { publicKey, privateKey } = (0, crypto_1.generateKeyPairSync)('ed25519', {
        publicKeyEncoding: { type: 'spki', format: 'pem' },
        privateKeyEncoding: { type: 'pkcs8', format: 'pem' },
    });
    // Generate agent ID from public key hash
    const hash = (0, crypto_1.createHash)('sha256').update(publicKey).digest('hex');
    const agentId = `mg_${hash.substring(0, 16)}`;
    const identity = {
        privateKey,
        publicKey,
        agentId,
        createdAt: new Date().toISOString(),
    };
    // Atomic write: temp file + rename
    const tempFile = `${IDENTITY_FILE}.tmp`;
    (0, fs_1.writeFileSync)(tempFile, JSON.stringify(identity, null, 2), { mode: 0o600 });
    (0, fs_1.renameSync)(tempFile, IDENTITY_FILE);
    console.log(`[memory-garden] Generated new identity: ${agentId}`);
}
/**
 * Loads and returns the agent identity.
 * TR-2: Verifies file permissions before loading (defense in depth).
 * CR-9: Try-catch around JSON.parse for corrupted file handling.
 */
function loadIdentity() {
    // TR-2: Check permissions (defense in depth)
    // Note: Permission check only works reliably on Unix-like systems
    if (process.platform !== 'win32') {
        const stats = (0, fs_1.statSync)(IDENTITY_FILE);
        const mode = stats.mode & 0o777;
        // Allow 0o600 (owner read/write) or 0o400 (owner read)
        if (mode !== 0o600 && mode !== 0o400) {
            console.warn(`[memory-garden] Identity file has permissions ${mode.toString(8)}, ` +
                `expected 0600. Consider running: chmod 600 ${IDENTITY_FILE}`);
        }
    }
    // CR-9: Try-catch around JSON.parse
    let data;
    try {
        data = JSON.parse((0, fs_1.readFileSync)(IDENTITY_FILE, 'utf-8'));
    }
    catch (e) {
        throw new Error(`Failed to parse identity file: ${IDENTITY_FILE}. ` +
            `File may be corrupted. Delete it and restart to regenerate. ` +
            `Original error: ${e instanceof Error ? e.message : String(e)}`);
    }
    return {
        agentId: data.agentId,
        publicKey: data.publicKey,
    };
}
/**
 * Gets the private key for signing operations.
 * Internal use only - never expose this.
 * CR-9: Try-catch around JSON.parse for corrupted file handling.
 */
function getPrivateKey() {
    let data;
    try {
        data = JSON.parse((0, fs_1.readFileSync)(IDENTITY_FILE, 'utf-8'));
    }
    catch (e) {
        throw new Error(`Failed to parse identity file: ${IDENTITY_FILE}. ` +
            `File may be corrupted. Delete it and restart to regenerate. ` +
            `Original error: ${e instanceof Error ? e.message : String(e)}`);
    }
    return data.privateKey;
}
/**
 * Signs raw data with the instance's Ed25519 private key.
 * CR-1: Uses crypto.sign(null, ...) for Ed25519.
 *
 * WARNING: This is a low-level function. For P2P attestations, use signMessage()
 * which includes timestamp and nonce for replay attack prevention.
 */
function signData(data) {
    const privateKey = getPrivateKey();
    const signature = (0, crypto_1.sign)(null, Buffer.from(data), privateKey);
    return signature.toString('base64');
}
// =============================================================================
// TRM-4: Replay Attack Prevention
// =============================================================================
/**
 * Default message validity window (5 minutes).
 * Messages with timestamps older than this are rejected.
 */
const DEFAULT_MESSAGE_VALIDITY_MS = 5 * 60 * 1000;
/**
 * Creates a signed message with timestamp and nonce for replay prevention.
 * TRM-4: Use this for P2P attestations instead of raw signData().
 * CR-10: Uses canonical JSON with sorted keys for cross-language compatibility.
 *
 * @param data The data to sign
 * @returns SignedMessage with timestamp, nonce, and signature
 */
function signMessage(data) {
    const identity = ensureIdentity();
    const timestamp = new Date().toISOString();
    const nonce = (0, crypto_1.randomBytes)(16).toString('hex');
    // CR-10: Create canonical payload with sorted keys
    const payload = {
        agentId: identity.agentId,
        data,
        nonce,
        timestamp,
    };
    const canonical = canonicalJson(payload);
    const signature = signData(canonical);
    return {
        ...payload,
        signature,
    };
}
/**
 * Verifies a signed message, checking timestamp freshness and signature validity.
 * TRM-4: Prevents replay attacks by validating timestamp and optional nonce tracking.
 * CR-10: Uses canonical JSON with sorted keys for cross-language compatibility.
 *
 * CR-8: IMPORTANT - Nonce Tracking Requirement:
 * For security-critical paths (P2P attestations, cross-peer messages),
 * callers MUST provide a seenNonces Set to enable full replay protection.
 * Without nonce tracking, only timestamp validation is performed, which
 * allows replays within the validity window.
 *
 * @example
 * // Security-critical usage (full replay protection):
 * const seenNonces = new Set<string>();
 * const result = verifyMessage(msg, pubKey, { seenNonces });
 *
 * // Low-risk usage (timestamp-only, replays allowed within window):
 * const result = verifyMessage(msg, pubKey);
 *
 * @param message The signed message to verify
 * @param publicKey The signer's public key (PEM format)
 * @param options Verification options (max age, seen nonces)
 * @returns VerifyMessageResult with validity status and any error
 */
function verifyMessage(message, publicKey, options = {}) {
    const { maxAgeMs = DEFAULT_MESSAGE_VALIDITY_MS, seenNonces } = options;
    // 1. Check timestamp freshness
    const messageTime = new Date(message.timestamp).getTime();
    const now = Date.now();
    if (isNaN(messageTime)) {
        return { valid: false, error: 'Invalid timestamp format' };
    }
    if (now - messageTime > maxAgeMs) {
        return { valid: false, error: `Message expired (older than ${maxAgeMs}ms)` };
    }
    if (messageTime > now + 60000) {
        // Allow 1 minute clock skew
        return { valid: false, error: 'Message timestamp is in the future' };
    }
    // 2. Check nonce uniqueness (if tracking enabled)
    // CR-8: Without seenNonces, only timestamp validation is performed
    if (seenNonces) {
        const nonceKey = `${message.agentId}:${message.nonce}`;
        if (seenNonces.has(nonceKey)) {
            return { valid: false, error: 'Nonce already used (replay detected)' };
        }
        seenNonces.add(nonceKey);
    }
    // 3. Reconstruct canonical payload and verify signature
    // CR-10: Use canonical JSON with sorted keys
    const payload = {
        agentId: message.agentId,
        data: message.data,
        nonce: message.nonce,
        timestamp: message.timestamp,
    };
    const canonical = canonicalJson(payload);
    const signatureValid = verifySignature(canonical, message.signature, publicKey);
    if (!signatureValid) {
        return { valid: false, error: 'Invalid signature' };
    }
    return {
        valid: true,
        data: message.data,
        agentId: message.agentId,
    };
}
/**
 * Verifies a signature using the provided public key.
 * CR-1: Uses crypto.verify(null, ...) for Ed25519.
 */
function verifySignature(data, signature, publicKey) {
    try {
        return (0, crypto_1.verify)(null, Buffer.from(data), publicKey, Buffer.from(signature, 'base64'));
    }
    catch {
        return false;
    }
}
/**
 * Gets the current agent ID without loading the full identity.
 * Convenience method for attaching to validation requests.
 */
function getAgentId() {
    const identity = ensureIdentity();
    return identity.agentId;
}
/**
 * Creates a signed attestation for a validation.
 * The attestation includes the pattern CID, stance, and timestamp.
 */
function createValidationAttestation(patternCid, stance, context) {
    const identity = ensureIdentity();
    const timestamp = new Date().toISOString();
    const attestation = JSON.stringify({
        patternCid,
        stance,
        context,
        timestamp,
        agentId: identity.agentId,
    });
    const signature = signData(attestation);
    return {
        attestation,
        signature,
        agentId: identity.agentId,
    };
}
//# sourceMappingURL=identity.js.map