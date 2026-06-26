/**
 * @pqsafe/openclaw — PQSafe AgentPay integration for OpenClaw agents.
 *
 * Built on `@pqsafe/agent-pay` — see github.com/PQSafe/pqsafe
 *
 * Exposes three OpenClaw skill operations:
 *   create_envelope  — build + ML-DSA-65 sign a SpendEnvelope
 *   verify_envelope  — verify signature + temporal validity
 *   revoke_envelope  — contact PQSafe revocation endpoint
 *
 * ML-DSA-65 = NIST FIPS 204 (formerly Dilithium3)
 * Security level: NIST Level 3 (quantum-resistant)
 * Key sizes: pubkey 1952 B · secret key 4032 B · signature 3309 B
 *
 * AP2-PQ profile: https://pqsafe.xyz/ap2-pq-rfc
 *
 * @see https://docs.pqsafe.xyz/agent-pay
 */
export type { SignedEnvelope, PaymentRequest, PaymentResult, Rail, CreateEnvelopeParams, SpendEnvelope, } from '@pqsafe/agent-pay';
/**
 * Rail values supported by the PQSafe AgentPay router.
 * (Re-exported from @pqsafe/agent-pay for convenience — same values.)
 *
 * Live sandbox (real money in sandbox mode):
 *   airwallex  — Airwallex multi-currency
 *   wise       — Wise international transfers
 *
 * Mock-ready (test harness available, not yet live sandbox):
 *   stripe     — Stripe payment processing
 *   usdc-base  — USDC on Base L2
 *   x402       — HTTP 402 micropayment standard
 */
export type OpenClawRail = 'airwallex' | 'wise' | 'stripe' | 'usdc-base' | 'x402';
/** Input for the create_envelope operation */
export interface CreateEnvelopeInput {
    /** PQSafe address of the human issuer (pq1 + 20-byte keccak hex) */
    issuer: string;
    /** Agent identifier — free-form string (e.g. "travel-agent-v1") */
    agent: string;
    /** Maximum total amount the agent may spend in the given currency */
    maxAmount: number;
    /** ISO 4217 currency code or crypto token symbol (3–5 chars) */
    currency: string;
    /**
     * Allowlist of allowed payment recipients (rail-specific format).
     * At least one recipient must be specified; empty list blocks all payments.
     */
    allowedRecipients: string[];
    /**
     * Seconds before the envelope becomes active (default: 0 = immediately).
     */
    startsInSeconds?: number;
    /** Time-to-live in seconds from now (default: 3600 = 1 hour, max: 86400) */
    ttlSeconds?: number;
    /** Constrain to a specific payment rail (optional; omit to let router choose) */
    rail?: OpenClawRail;
    /**
     * Hex-encoded ML-DSA-65 secret key (4032 bytes = 8064 hex chars).
     * Required in production. Omit when PQSAFE_TEST_MODE=true.
     */
    dsaSecretKey?: string;
    /**
     * Hex-encoded ML-DSA-65 public key (1952 bytes = 3904 hex chars).
     * Required in production. Omit when PQSAFE_TEST_MODE=true.
     */
    dsaPublicKey?: string;
}
/** Output of the create_envelope operation */
export interface CreateEnvelopeOutput {
    /** Canonical deterministic JSON of the SpendEnvelope (UTF-8, JCS) */
    envelopeJson: string;
    /** ML-DSA-65 signature over envelopeJson bytes, hex-encoded */
    signature: string;
    /** ML-DSA-65 public key of the issuer, hex-encoded */
    dsaPublicKey: string;
}
/** Input for the verify_envelope operation */
export interface VerifyEnvelopeInput {
    /** The full SignedEnvelope to verify */
    envelope: {
        envelopeJson: string;
        signature: string;
        dsaPublicKey: string;
    };
    /** Optional: override the public key to verify against (instead of the embedded one) */
    dsaPublicKey?: string;
}
/** Output of the verify_envelope operation */
export interface VerifyEnvelopeOutput {
    /** True if signature is valid, envelope not expired, and not yet active-window-only-expired */
    valid: boolean;
    /** The parsed agent field from the envelope */
    agent: string;
    /** The issuer address from the envelope */
    issuer: string;
    /** ISO timestamp: validUntil (Unix → ISO) */
    validUntil: string;
    /** Reason string if valid=false */
    reason?: string;
}
/** Input for the revoke_envelope operation */
export interface RevokeEnvelopeInput {
    /** The full SignedEnvelope to revoke (needed to compute the envelope hash) */
    envelope: {
        envelopeJson: string;
        signature: string;
        dsaPublicKey: string;
    };
    /** Optional human-readable reason stored in the audit log */
    reason?: string;
}
/** Output of the revoke_envelope operation */
export interface RevokeEnvelopeOutput {
    revoked: boolean;
    /** ISO timestamp of revocation */
    revokedAt: string;
    /** HTTP status returned by the revocation endpoint (or 0 in test mode) */
    httpStatus: number;
}
export interface PQSafeOpenClawConfig {
    /**
     * Base URL of the PQSafe REST API.
     * Used only for revoke_envelope (which must reach the revocation registry).
     * @default "https://api.pqsafe.xyz/v1"
     */
    apiUrl?: string;
    /** Optional fetch timeout in milliseconds for revocation calls. @default 30000 */
    timeoutMs?: number;
}
export interface OpenClawContext {
    log?: {
        debug?: (msg: string, meta?: Record<string, unknown>) => void;
        info?: (msg: string, meta?: Record<string, unknown>) => void;
        error?: (msg: string, meta?: Record<string, unknown>) => void;
    };
}
export interface OpenClawSkillHandler {
    skillId: string;
    version: string;
    invoke(operationId: string, input: unknown, ctx?: OpenClawContext): Promise<unknown>;
    healthCheck?(): Promise<{
        healthy: boolean;
        latencyMs?: number;
    }>;
}
/**
 * Create a PQSafe OpenClaw skill handler.
 *
 * Register the returned object with your OpenClaw agent:
 * ```ts
 * import { createPQSafeOpenClawSkill } from '@pqsafe/openclaw'
 * const pqsafe = createPQSafeOpenClawSkill()
 * agent.registerSkill(pqsafe)
 * ```
 *
 * Set PQSAFE_TEST_MODE=true to bypass network calls and ML-DSA key requirements
 * (useful for local development and CI).
 */
export declare function createPQSafeOpenClawSkill(config?: PQSafeOpenClawConfig): OpenClawSkillHandler;
export default createPQSafeOpenClawSkill;
//# sourceMappingURL=index.d.ts.map