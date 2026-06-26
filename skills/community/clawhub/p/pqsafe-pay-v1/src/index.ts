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
// Re-export core types from @pqsafe/agent-pay so callers don't need a
// separate import for the most common types.
// ---------------------------------------------------------------------------

export type {
  SignedEnvelope,
  PaymentRequest,
  PaymentResult,
  Rail,
  CreateEnvelopeParams,
  SpendEnvelope,
} from '@pqsafe/agent-pay'

// ---------------------------------------------------------------------------
// Plugin-specific types
// ---------------------------------------------------------------------------

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
export type OpenClawRail = 'airwallex' | 'wise' | 'stripe' | 'usdc-base' | 'x402'

/** Input for the create_envelope operation */
export interface CreateEnvelopeInput {
  /** PQSafe address of the human issuer (pq1 + 20-byte keccak hex) */
  issuer: string
  /** Agent identifier — free-form string (e.g. "travel-agent-v1") */
  agent: string
  /** Maximum total amount the agent may spend in the given currency */
  maxAmount: number
  /** ISO 4217 currency code or crypto token symbol (3–5 chars) */
  currency: string
  /**
   * Allowlist of allowed payment recipients (rail-specific format).
   * At least one recipient must be specified; empty list blocks all payments.
   */
  allowedRecipients: string[]
  /**
   * Seconds before the envelope becomes active (default: 0 = immediately).
   */
  startsInSeconds?: number
  /** Time-to-live in seconds from now (default: 3600 = 1 hour, max: 86400) */
  ttlSeconds?: number
  /** Constrain to a specific payment rail (optional; omit to let router choose) */
  rail?: OpenClawRail
  /**
   * Hex-encoded ML-DSA-65 secret key (4032 bytes = 8064 hex chars).
   * Required in production. Omit when PQSAFE_TEST_MODE=true.
   */
  dsaSecretKey?: string
  /**
   * Hex-encoded ML-DSA-65 public key (1952 bytes = 3904 hex chars).
   * Required in production. Omit when PQSAFE_TEST_MODE=true.
   */
  dsaPublicKey?: string
}

/** Output of the create_envelope operation */
export interface CreateEnvelopeOutput {
  /** Canonical deterministic JSON of the SpendEnvelope (UTF-8, JCS) */
  envelopeJson: string
  /** ML-DSA-65 signature over envelopeJson bytes, hex-encoded */
  signature: string
  /** ML-DSA-65 public key of the issuer, hex-encoded */
  dsaPublicKey: string
}

/** Input for the verify_envelope operation */
export interface VerifyEnvelopeInput {
  /** The full SignedEnvelope to verify */
  envelope: {
    envelopeJson: string
    signature: string
    dsaPublicKey: string
  }
  /** Optional: override the public key to verify against (instead of the embedded one) */
  dsaPublicKey?: string
}

/** Output of the verify_envelope operation */
export interface VerifyEnvelopeOutput {
  /** True if signature is valid, envelope not expired, and not yet active-window-only-expired */
  valid: boolean
  /** The parsed agent field from the envelope */
  agent: string
  /** The issuer address from the envelope */
  issuer: string
  /** ISO timestamp: validUntil (Unix → ISO) */
  validUntil: string
  /** Reason string if valid=false */
  reason?: string
}

/** Input for the revoke_envelope operation */
export interface RevokeEnvelopeInput {
  /** The full SignedEnvelope to revoke (needed to compute the envelope hash) */
  envelope: {
    envelopeJson: string
    signature: string
    dsaPublicKey: string
  }
  /** Optional human-readable reason stored in the audit log */
  reason?: string
}

/** Output of the revoke_envelope operation */
export interface RevokeEnvelopeOutput {
  revoked: boolean
  /** ISO timestamp of revocation */
  revokedAt: string
  /** HTTP status returned by the revocation endpoint (or 0 in test mode) */
  httpStatus: number
}

// ---------------------------------------------------------------------------
// Config
// ---------------------------------------------------------------------------

export interface PQSafeOpenClawConfig {
  /**
   * Base URL of the PQSafe REST API.
   * Used only for revoke_envelope (which must reach the revocation registry).
   * @default "https://api.pqsafe.xyz/v1"
   */
  apiUrl?: string

  /** Optional fetch timeout in milliseconds for revocation calls. @default 30000 */
  timeoutMs?: number
}

// ---------------------------------------------------------------------------
// Mock helpers (PQSAFE_TEST_MODE)
// ---------------------------------------------------------------------------

const TEST_PUBKEY = 'a'.repeat(3904)
const TEST_SIG = 'b'.repeat(6618)

function mockSignedEnvelope(input: CreateEnvelopeInput): CreateEnvelopeOutput {
  const now = Math.floor(Date.now() / 1000)
  const nonce = 'c'.repeat(32)
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
  }
  return {
    envelopeJson: JSON.stringify(envelope),
    signature: TEST_SIG,
    dsaPublicKey: TEST_PUBKEY,
  }
}

function mockVerify(input: VerifyEnvelopeInput): VerifyEnvelopeOutput {
  // In test mode: check expiry from the parsed envelopeJson, but accept any signature.
  let parsed: Record<string, unknown>
  try {
    parsed = JSON.parse(input.envelope.envelopeJson) as Record<string, unknown>
  } catch {
    return { valid: false, agent: '', issuer: '', validUntil: '', reason: 'MALFORMED_ENVELOPE' }
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
    }
  }

  const validUntil = Number(parsed['validUntil'] ?? 0)
  const now = Math.floor(Date.now() / 1000)
  if (now > validUntil) {
    return {
      valid: false,
      agent: String(parsed['agent'] ?? ''),
      issuer: String(parsed['issuer'] ?? ''),
      validUntil: new Date(validUntil * 1000).toISOString(),
      reason: 'ENVELOPE_EXPIRED',
    }
  }

  return {
    valid: true,
    agent: String(parsed['agent'] ?? ''),
    issuer: String(parsed['issuer'] ?? ''),
    validUntil: new Date(validUntil * 1000).toISOString(),
  }
}

function mockRevoke(_input: RevokeEnvelopeInput): RevokeEnvelopeOutput {
  return {
    revoked: true,
    revokedAt: new Date().toISOString(),
    httpStatus: 0,
  }
}

// ---------------------------------------------------------------------------
// Core operations (production paths)
// ---------------------------------------------------------------------------

async function prodCreateEnvelope(input: CreateEnvelopeInput): Promise<CreateEnvelopeOutput> {
  const { createEnvelope, signEnvelope } = await import('@pqsafe/agent-pay')
  const { hexToBytes } = await import('@noble/hashes/utils.js' as string)

  if (!input.dsaSecretKey) {
    throw new Error(
      'PQSafe: dsaSecretKey is required for create_envelope in production. ' +
      'Set PQSAFE_TEST_MODE=true for local development.',
    )
  }
  if (!input.dsaPublicKey) {
    throw new Error(
      'PQSafe: dsaPublicKey is required for create_envelope in production. ' +
      'Set PQSAFE_TEST_MODE=true for local development.',
    )
  }

  const secretKey = hexToBytes(input.dsaSecretKey)
  const publicKey = hexToBytes(input.dsaPublicKey)

  const envelope = createEnvelope({
    issuer: input.issuer,
    agent: input.agent,
    maxAmount: input.maxAmount,
    currency: input.currency,
    allowedRecipients: input.allowedRecipients,
    startsInSeconds: input.startsInSeconds,
    ttlSeconds: input.ttlSeconds,
    rail: input.rail,
  })

  return signEnvelope(envelope, secretKey, publicKey)
}

async function prodVerifyEnvelope(input: VerifyEnvelopeInput): Promise<VerifyEnvelopeOutput> {
  const { verifyEnvelope } = await import('@pqsafe/agent-pay')
  const { hexToBytes } = await import('@noble/hashes/utils.js' as string)

  const overridePubKey = input.dsaPublicKey ? hexToBytes(input.dsaPublicKey) : undefined

  try {
    const envelope = verifyEnvelope(input.envelope, overridePubKey)
    return {
      valid: true,
      agent: envelope.agent,
      issuer: envelope.issuer,
      validUntil: new Date(envelope.validUntil * 1000).toISOString(),
    }
  } catch (err: unknown) {
    const msg = err instanceof Error ? err.message : String(err)
    let reason = 'SIGNATURE_INVALID'
    if (msg.includes('expired')) reason = 'ENVELOPE_EXPIRED'
    else if (msg.includes('not yet active')) reason = 'ENVELOPE_NOT_YET_ACTIVE'
    else if (msg.includes('schema invalid')) reason = 'MALFORMED_ENVELOPE'

    // Best-effort parse for output fields
    let agent = ''
    let issuer = ''
    let validUntil = ''
    try {
      const parsed = JSON.parse(input.envelope.envelopeJson) as Record<string, unknown>
      agent = String(parsed['agent'] ?? '')
      issuer = String(parsed['issuer'] ?? '')
      validUntil = parsed['validUntil']
        ? new Date(Number(parsed['validUntil']) * 1000).toISOString()
        : ''
    } catch { /* ignore */ }

    return { valid: false, agent, issuer, validUntil, reason }
  }
}

async function prodRevokeEnvelope(
  input: RevokeEnvelopeInput,
  apiUrl: string,
  timeoutMs: number,
): Promise<RevokeEnvelopeOutput> {
  // Compute the SHA-256 envelope hash server-side by sending the full envelope.
  // The revocation endpoint accepts { envelopeJson, signature, dsaPublicKey, reason? }.
  const controller = new AbortController()
  const timer = setTimeout(() => controller.abort(), timeoutMs)

  let response: Response
  try {
    response = await fetch(`${apiUrl}/envelopes/revoke`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        signedEnvelope: input.envelope,
        reason: input.reason,
      }),
      signal: controller.signal,
    })
  } finally {
    clearTimeout(timer)
  }

  if (!response.ok) {
    const body = await response.text().catch(() => '(no body)')
    throw new Error(
      `PQSafe: revoke request failed — HTTP ${response.status}: ${body}`,
    )
  }

  const data = (await response.json()) as Record<string, unknown>
  return {
    revoked: true,
    revokedAt: String(data['revokedAt'] ?? new Date().toISOString()),
    httpStatus: response.status,
  }
}

// ---------------------------------------------------------------------------
// OpenClaw skill types (minimal — avoids a hard dep on @openclaw/sdk)
// ---------------------------------------------------------------------------

export interface OpenClawContext {
  log?: {
    debug?: (msg: string, meta?: Record<string, unknown>) => void
    info?: (msg: string, meta?: Record<string, unknown>) => void
    error?: (msg: string, meta?: Record<string, unknown>) => void
  }
}

export interface OpenClawSkillHandler {
  skillId: string
  version: string
  invoke(operationId: string, input: unknown, ctx?: OpenClawContext): Promise<unknown>
  healthCheck?(): Promise<{ healthy: boolean; latencyMs?: number }>
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
export function createPQSafeOpenClawSkill(
  config: PQSafeOpenClawConfig = {},
): OpenClawSkillHandler {
  const apiUrl = (config.apiUrl ?? 'https://api.pqsafe.xyz/v1').replace(/\/$/, '')
  const timeoutMs = config.timeoutMs ?? 30_000
  const testMode = process.env['PQSAFE_TEST_MODE'] === 'true'

  async function handleCreateEnvelope(
    input: CreateEnvelopeInput,
    ctx?: OpenClawContext,
  ): Promise<CreateEnvelopeOutput> {
    ctx?.log?.info?.('pqsafe.pay.v1: create_envelope', {
      agent: input.agent,
      issuer: input.issuer,
      rail: input.rail ?? 'any',
      currency: input.currency,
      maxAmount: input.maxAmount,
    })

    if (testMode) return mockSignedEnvelope(input)
    return prodCreateEnvelope(input)
  }

  async function handleVerifyEnvelope(
    input: VerifyEnvelopeInput,
    ctx?: OpenClawContext,
  ): Promise<VerifyEnvelopeOutput> {
    ctx?.log?.debug?.('pqsafe.pay.v1: verify_envelope')

    if (testMode) return mockVerify(input)
    return prodVerifyEnvelope(input)
  }

  async function handleRevokeEnvelope(
    input: RevokeEnvelopeInput,
    ctx?: OpenClawContext,
  ): Promise<RevokeEnvelopeOutput> {
    ctx?.log?.info?.('pqsafe.pay.v1: revoke_envelope', { reason: input.reason })

    if (testMode) return mockRevoke(input)
    return prodRevokeEnvelope(input, apiUrl, timeoutMs)
  }

  return {
    skillId: 'pqsafe.pay.v1',
    version: '0.1.0',

    async invoke(
      operationId: string,
      input: unknown,
      ctx?: OpenClawContext,
    ): Promise<unknown> {
      switch (operationId) {
        case 'create_envelope':
          return handleCreateEnvelope(input as CreateEnvelopeInput, ctx)
        case 'verify_envelope':
          return handleVerifyEnvelope(input as VerifyEnvelopeInput, ctx)
        case 'revoke_envelope':
          return handleRevokeEnvelope(input as RevokeEnvelopeInput, ctx)
        default:
          throw new Error(
            `pqsafe.pay.v1: unknown operation "${operationId}". ` +
            'Valid operations: create_envelope, verify_envelope, revoke_envelope',
          )
      }
    },

    async healthCheck(): Promise<{ healthy: boolean; latencyMs?: number }> {
      if (testMode) return { healthy: true, latencyMs: 0 }

      const controller = new AbortController()
      const timer = setTimeout(() => controller.abort(), 5_000)
      const start = Date.now()
      try {
        const res = await fetch(`${apiUrl}/health`, { signal: controller.signal })
        clearTimeout(timer)
        return { healthy: res.ok, latencyMs: Date.now() - start }
      } catch {
        clearTimeout(timer)
        return { healthy: false }
      }
    },
  }
}

export default createPQSafeOpenClawSkill
