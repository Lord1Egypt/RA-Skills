export interface AgentIdentity {
    agentId: string;
    publicKey: string;
}
/**
 * Ensures an identity exists, generating one if needed.
 * Returns the agent identity (without private key).
 */
export declare function ensureIdentity(): AgentIdentity;
/**
 * Signs raw data with the instance's Ed25519 private key.
 * CR-1: Uses crypto.sign(null, ...) for Ed25519.
 *
 * WARNING: This is a low-level function. For P2P attestations, use signMessage()
 * which includes timestamp and nonce for replay attack prevention.
 */
export declare function signData(data: string): string;
/**
 * SignedMessage wraps data with timestamp and nonce for replay prevention.
 * TRM-4: Prevents replay attacks in P2P attestations.
 */
export interface SignedMessage {
    /** The actual data being signed */
    data: string;
    /** ISO timestamp when message was created */
    timestamp: string;
    /** Random nonce (16 bytes hex) to ensure uniqueness */
    nonce: string;
    /** Agent ID of the signer */
    agentId: string;
    /** Base64-encoded Ed25519 signature of the canonical JSON */
    signature: string;
}
/**
 * Options for message verification.
 */
export interface VerifyMessageOptions {
    /** Maximum age of message in milliseconds (default: 5 minutes) */
    maxAgeMs?: number;
    /** Set of seen nonces to prevent replay (caller maintains this) */
    seenNonces?: Set<string>;
}
/**
 * Result of message verification.
 */
export interface VerifyMessageResult {
    valid: boolean;
    error?: string;
    data?: string;
    agentId?: string;
}
/**
 * Creates a signed message with timestamp and nonce for replay prevention.
 * TRM-4: Use this for P2P attestations instead of raw signData().
 * CR-10: Uses canonical JSON with sorted keys for cross-language compatibility.
 *
 * @param data The data to sign
 * @returns SignedMessage with timestamp, nonce, and signature
 */
export declare function signMessage(data: string): SignedMessage;
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
export declare function verifyMessage(message: SignedMessage, publicKey: string, options?: VerifyMessageOptions): VerifyMessageResult;
/**
 * Verifies a signature using the provided public key.
 * CR-1: Uses crypto.verify(null, ...) for Ed25519.
 */
export declare function verifySignature(data: string, signature: string, publicKey: string): boolean;
/**
 * Gets the current agent ID without loading the full identity.
 * Convenience method for attaching to validation requests.
 */
export declare function getAgentId(): string;
/**
 * Creates a signed attestation for a validation.
 * The attestation includes the pattern CID, stance, and timestamp.
 */
export declare function createValidationAttestation(patternCid: string, stance: string, context: string): {
    attestation: string;
    signature: string;
    agentId: string;
};
//# sourceMappingURL=identity.d.ts.map