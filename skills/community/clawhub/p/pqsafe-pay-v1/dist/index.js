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
// ---------------------------------------------------------------------------
// Mock helpers (PQSAFE_TEST_MODE)
// ---------------------------------------------------------------------------
const TEST_PUBKEY = 'a'.repeat(3904);
const TEST_SIG = 'b'.repeat(6618);
function mockSignedEnvelope(input) {
    const now = Math.floor(Date.now() / 1000);
    const nonce = 'c'.repeat(32);
    const envelope = {
        version: 1,
        issuer: input.issuer,
        agent: input.agent,
        maxAmount: input.maxAmount,
        currency: input.currency.toUpperCase(),
        allowedRecipients: input.allowedRecipients,
        validFrom: now + (input.startsInSeconds ?? 0),
        validUntil: now + (input.ttlSeconds ?? 3600),
        nonce,
        ...(input.rail ? { rail: input.rail } : {}),
    };
    return {
        envelopeJson: JSON.stringify(envelope),
        signature: TEST_SIG,
        dsaPublicKey: TEST_PUBKEY,
    };
}
function mockVerify(input) {
    // In test mode: check expiry from the parsed envelopeJson, but accept any signature.
    let parsed;
    try {
        parsed = JSON.parse(input.envelope.envelopeJson);
    }
    catch {
        return { valid: false, agent: '', issuer: '', validUntil: '', reason: 'MALFORMED_ENVELOPE' };
    }
    // Tamper detection: check if the embedded signature is the test sentinel.
    // In test mode, any non-test signature is treated as tampered.
    if (input.envelope.signature !== TEST_SIG) {
        return {
            valid: false,
            agent: String(parsed['agent'] ?? ''),
            issuer: String(parsed['issuer'] ?? ''),
            validUntil: new Date((Number(parsed['validUntil'] ?? 0)) * 1000).toISOString(),
            reason: 'SIGNATURE_INVALID',
        };
    }
    const validUntil = Number(parsed['validUntil'] ?? 0);
    const now = Math.floor(Date.now() / 1000);
    if (now > validUntil) {
        return {
            valid: false,
            agent: String(parsed['agent'] ?? ''),
            issuer: String(parsed['issuer'] ?? ''),
            validUntil: new Date(validUntil * 1000).toISOString(),
            reason: 'ENVELOPE_EXPIRED',
        };
    }
    return {
        valid: true,
        agent: String(parsed['agent'] ?? ''),
        issuer: String(parsed['issuer'] ?? ''),
        validUntil: new Date(validUntil * 1000).toISOString(),
    };
}
function mockRevoke(_input) {
    return {
        revoked: true,
        revokedAt: new Date().toISOString(),
        httpStatus: 0,
    };
}
// ---------------------------------------------------------------------------
// Core operations (production paths)
// ---------------------------------------------------------------------------
async function prodCreateEnvelope(input) {
    const { createEnvelope, signEnvelope } = await import('@pqsafe/agent-pay');
    const { hexToBytes } = await import('@noble/hashes/utils.js');
    if (!input.dsaSecretKey) {
        throw new Error('PQSafe: dsaSecretKey is required for create_envelope in production. ' +
            'Set PQSAFE_TEST_MODE=true for local development.');
    }
    if (!input.dsaPublicKey) {
        throw new Error('PQSafe: dsaPublicKey is required for create_envelope in production. ' +
            'Set PQSAFE_TEST_MODE=true for local development.');
    }
    const secretKey = hexToBytes(input.dsaSecretKey);
    const publicKey = hexToBytes(input.dsaPublicKey);
    const envelope = createEnvelope({
        issuer: input.issuer,
        agent: input.agent,
        maxAmount: input.maxAmount,
        currency: input.currency,
        allowedRecipients: input.allowedRecipients,
        startsInSeconds: input.startsInSeconds,
        ttlSeconds: input.ttlSeconds,
        rail: input.rail,
    });
    return signEnvelope(envelope, secretKey, publicKey);
}
async function prodVerifyEnvelope(input) {
    const { verifyEnvelope } = await import('@pqsafe/agent-pay');
    const { hexToBytes } = await import('@noble/hashes/utils.js');
    const overridePubKey = input.dsaPublicKey ? hexToBytes(input.dsaPublicKey) : undefined;
    try {
        const envelope = verifyEnvelope(input.envelope, overridePubKey);
        return {
            valid: true,
            agent: envelope.agent,
            issuer: envelope.issuer,
            validUntil: new Date(envelope.validUntil * 1000).toISOString(),
        };
    }
    catch (err) {
        const msg = err instanceof Error ? err.message : String(err);
        let reason = 'SIGNATURE_INVALID';
        if (msg.includes('expired'))
            reason = 'ENVELOPE_EXPIRED';
        else if (msg.includes('not yet active'))
            reason = 'ENVELOPE_NOT_YET_ACTIVE';
        else if (msg.includes('schema invalid'))
            reason = 'MALFORMED_ENVELOPE';
        // Best-effort parse for output fields
        let agent = '';
        let issuer = '';
        let validUntil = '';
        try {
            const parsed = JSON.parse(input.envelope.envelopeJson);
            agent = String(parsed['agent'] ?? '');
            issuer = String(parsed['issuer'] ?? '');
            validUntil = parsed['validUntil']
                ? new Date(Number(parsed['validUntil']) * 1000).toISOString()
                : '';
        }
        catch { /* ignore */ }
        return { valid: false, agent, issuer, validUntil, reason };
    }
}
async function prodRevokeEnvelope(input, apiUrl, timeoutMs) {
    // Compute the SHA-256 envelope hash server-side by sending the full envelope.
    // The revocation endpoint accepts { envelopeJson, signature, dsaPublicKey, reason? }.
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeoutMs);
    let response;
    try {
        response = await fetch(`${apiUrl}/envelopes/revoke`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                signedEnvelope: input.envelope,
                reason: input.reason,
            }),
            signal: controller.signal,
        });
    }
    finally {
        clearTimeout(timer);
    }
    if (!response.ok) {
        const body = await response.text().catch(() => '(no body)');
        throw new Error(`PQSafe: revoke request failed — HTTP ${response.status}: ${body}`);
    }
    const data = (await response.json());
    return {
        revoked: true,
        revokedAt: String(data['revokedAt'] ?? new Date().toISOString()),
        httpStatus: response.status,
    };
}
// ---------------------------------------------------------------------------
// Factory
// ---------------------------------------------------------------------------
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
export function createPQSafeOpenClawSkill(config = {}) {
    const apiUrl = (config.apiUrl ?? 'https://api.pqsafe.xyz/v1').replace(/\/$/, '');
    const timeoutMs = config.timeoutMs ?? 30_000;
    const testMode = process.env['PQSAFE_TEST_MODE'] === 'true';
    async function handleCreateEnvelope(input, ctx) {
        ctx?.log?.info?.('pqsafe.pay.v1: create_envelope', {
            agent: input.agent,
            issuer: input.issuer,
            rail: input.rail ?? 'any',
            currency: input.currency,
            maxAmount: input.maxAmount,
        });
        if (testMode)
            return mockSignedEnvelope(input);
        return prodCreateEnvelope(input);
    }
    async function handleVerifyEnvelope(input, ctx) {
        ctx?.log?.debug?.('pqsafe.pay.v1: verify_envelope');
        if (testMode)
            return mockVerify(input);
        return prodVerifyEnvelope(input);
    }
    async function handleRevokeEnvelope(input, ctx) {
        ctx?.log?.info?.('pqsafe.pay.v1: revoke_envelope', { reason: input.reason });
        if (testMode)
            return mockRevoke(input);
        return prodRevokeEnvelope(input, apiUrl, timeoutMs);
    }
    return {
        skillId: 'pqsafe.pay.v1',
        version: '0.1.0',
        async invoke(operationId, input, ctx) {
            switch (operationId) {
                case 'create_envelope':
                    return handleCreateEnvelope(input, ctx);
                case 'verify_envelope':
                    return handleVerifyEnvelope(input, ctx);
                case 'revoke_envelope':
                    return handleRevokeEnvelope(input, ctx);
                default:
                    throw new Error(`pqsafe.pay.v1: unknown operation "${operationId}". ` +
                        'Valid operations: create_envelope, verify_envelope, revoke_envelope');
            }
        },
        async healthCheck() {
            if (testMode)
                return { healthy: true, latencyMs: 0 };
            const controller = new AbortController();
            const timer = setTimeout(() => controller.abort(), 5_000);
            const start = Date.now();
            try {
                const res = await fetch(`${apiUrl}/health`, { signal: controller.signal });
                clearTimeout(timer);
                return { healthy: res.ok, latencyMs: Date.now() - start };
            }
            catch {
                clearTimeout(timer);
                return { healthy: false };
            }
        },
    };
}
export default createPQSafeOpenClawSkill;
//# sourceMappingURL=index.js.map