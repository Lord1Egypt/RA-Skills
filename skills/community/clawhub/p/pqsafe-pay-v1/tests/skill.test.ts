/**
 * @pqsafe/openclaw — vitest test suite
 *
 * Tests:
 *   1. create_envelope returns a valid SignedEnvelope structure
 *   2. verify_envelope returns valid=true for a freshly created envelope
 *   3. verify_envelope returns SIGNATURE_INVALID for a tampered envelope
 *   4. verify_envelope returns ENVELOPE_EXPIRED for a back-dated envelope
 *   5. all 5 rails are accepted by create_envelope
 *   6. PQSAFE_TEST_MODE bypasses network calls and key requirements
 *   7. invoke() dispatches unknown operation correctly (throws)
 *   8. revoke_envelope returns revoked=true in test mode
 *
 * Run: PQSAFE_TEST_MODE=true npx vitest run
 */

import { describe, it, expect, beforeAll, afterAll, vi, afterEach } from 'vitest'
import {
  createPQSafeOpenClawSkill,
  type CreateEnvelopeInput,
  type CreateEnvelopeOutput,
  type VerifyEnvelopeInput,
  type RevokeEnvelopeInput,
} from '../src/index.js'

// ---------------------------------------------------------------------------
// Test setup — force test mode so no real keys or API calls are needed
// ---------------------------------------------------------------------------

const originalTestMode = process.env['PQSAFE_TEST_MODE']

beforeAll(() => {
  process.env['PQSAFE_TEST_MODE'] = 'true'
})

afterAll(() => {
  if (originalTestMode === undefined) {
    delete process.env['PQSAFE_TEST_MODE']
  } else {
    process.env['PQSAFE_TEST_MODE'] = originalTestMode
  }
})

afterEach(() => {
  vi.restoreAllMocks()
})

// ---------------------------------------------------------------------------
// Fixtures
// ---------------------------------------------------------------------------

const VALID_ISSUER = 'pq1' + 'a'.repeat(40)

const BASE_CREATE_INPUT: CreateEnvelopeInput = {
  issuer: VALID_ISSUER,
  agent: 'test-agent-v1',
  maxAmount: 10,
  currency: 'USDC',
  allowedRecipients: ['0xdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef'],
  ttlSeconds: 300,
  rail: 'x402',
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function getSkill() {
  return createPQSafeOpenClawSkill()
}

// ---------------------------------------------------------------------------
// Tests
// ---------------------------------------------------------------------------

describe('createPQSafeOpenClawSkill', () => {

  // ── Test 1: create_envelope structure ─────────────────────────────────────

  it('create_envelope returns a valid SignedEnvelope structure', async () => {
    const skill = getSkill()
    const output = await skill.invoke('create_envelope', BASE_CREATE_INPUT) as CreateEnvelopeOutput

    // envelopeJson must be valid JSON containing the input fields
    expect(() => JSON.parse(output.envelopeJson)).not.toThrow()
    const parsed = JSON.parse(output.envelopeJson) as Record<string, unknown>
    expect(parsed['agent']).toBe(BASE_CREATE_INPUT.agent)
    expect(parsed['issuer']).toBe(BASE_CREATE_INPUT.issuer)
    expect(parsed['maxAmount']).toBe(BASE_CREATE_INPUT.maxAmount)
    expect(parsed['currency']).toBe('USDC') // toUpperCase applied
    expect(parsed['rail']).toBe(BASE_CREATE_INPUT.rail)

    // validUntil must be in the future
    const validUntil = Number(parsed['validUntil'])
    expect(validUntil).toBeGreaterThan(Math.floor(Date.now() / 1000))

    // nonce must be 32 hex chars (128-bit)
    expect(String(parsed['nonce'])).toMatch(/^[0-9a-f]{32}$/)

    // signature must be non-empty string
    expect(output.signature).toBeTruthy()
    expect(typeof output.signature).toBe('string')

    // dsaPublicKey must be non-empty string
    expect(output.dsaPublicKey).toBeTruthy()
  })

  // ── Test 2: verify_envelope valid ─────────────────────────────────────────

  it('verify_envelope returns valid=true for a freshly created envelope', async () => {
    const skill = getSkill()
    const created = await skill.invoke('create_envelope', BASE_CREATE_INPUT) as CreateEnvelopeOutput

    const verifyInput: VerifyEnvelopeInput = { envelope: created }
    const result = await skill.invoke('verify_envelope', verifyInput) as {
      valid: boolean
      agent: string
      issuer: string
      validUntil: string
      reason?: string
    }

    expect(result.valid).toBe(true)
    expect(result.agent).toBe(BASE_CREATE_INPUT.agent)
    expect(result.issuer).toBe(BASE_CREATE_INPUT.issuer)
    expect(result.reason).toBeUndefined()

    // validUntil must be a parseable ISO timestamp
    const d = new Date(result.validUntil)
    expect(isNaN(d.getTime())).toBe(false)
    expect(d.getTime()).toBeGreaterThan(Date.now())
  })

  // ── Test 3: tampered envelope → SIGNATURE_INVALID ─────────────────────────

  it('verify_envelope returns SIGNATURE_INVALID for a tampered envelope', async () => {
    const skill = getSkill()
    const created = await skill.invoke('create_envelope', BASE_CREATE_INPUT) as CreateEnvelopeOutput

    // Tamper with the signature (flip one char)
    const tampered: CreateEnvelopeOutput = {
      ...created,
      // Replace the first char of the signature with a different hex digit
      signature: (created.signature[0] === 'a' ? 'b' : 'a') + created.signature.slice(1),
    }

    const result = await skill.invoke('verify_envelope', { envelope: tampered }) as {
      valid: boolean
      reason?: string
    }

    expect(result.valid).toBe(false)
    expect(result.reason).toBe('SIGNATURE_INVALID')
  })

  // ── Test 4: expired envelope → ENVELOPE_EXPIRED ───────────────────────────

  it('verify_envelope returns ENVELOPE_EXPIRED for a back-dated envelope', async () => {
    const skill = getSkill()
    const created = await skill.invoke('create_envelope', BASE_CREATE_INPUT) as CreateEnvelopeOutput

    // Patch envelopeJson to set validUntil in the past
    const parsed = JSON.parse(created.envelopeJson) as Record<string, unknown>
    parsed['validUntil'] = Math.floor(Date.now() / 1000) - 3600 // 1 hour ago
    const expiredEnvelope: CreateEnvelopeOutput = {
      ...created,
      envelopeJson: JSON.stringify(parsed),
      // Signature is now "wrong" for this payload, but in test mode expiry check
      // is done before signature check, so ENVELOPE_EXPIRED is returned first.
    }

    const result = await skill.invoke('verify_envelope', { envelope: expiredEnvelope }) as {
      valid: boolean
      reason?: string
    }

    expect(result.valid).toBe(false)
    expect(result.reason).toBe('ENVELOPE_EXPIRED')
  })

  // ── Test 5: all 5 rails work ───────────────────────────────────────────────

  it('create_envelope accepts all 5 supported rails', async () => {
    const skill = getSkill()
    const rails = ['airwallex', 'wise', 'stripe', 'usdc-base', 'x402'] as const

    for (const rail of rails) {
      const output = await skill.invoke('create_envelope', {
        ...BASE_CREATE_INPUT,
        rail,
        currency: rail === 'usdc-base' || rail === 'x402' ? 'USDC' : 'USD',
      }) as CreateEnvelopeOutput

      const parsed = JSON.parse(output.envelopeJson) as Record<string, unknown>
      expect(parsed['rail']).toBe(rail)
      expect(output.signature).toBeTruthy()
    }
  })

  // ── Test 6: PQSAFE_TEST_MODE bypasses keys ────────────────────────────────

  it('PQSAFE_TEST_MODE=true works without dsaSecretKey or dsaPublicKey', async () => {
    // Confirm test mode is active
    expect(process.env['PQSAFE_TEST_MODE']).toBe('true')

    // Temporarily remove any real API key env vars if present
    const savedApiKey = process.env['PQSAFE_API_KEY']
    const savedKeyId = process.env['PQSAFE_KEY_ID']
    delete process.env['PQSAFE_API_KEY']
    delete process.env['PQSAFE_KEY_ID']

    try {
      const skill = getSkill()

      // Input with no dsaSecretKey / dsaPublicKey — should work in test mode
      const input: CreateEnvelopeInput = {
        issuer: VALID_ISSUER,
        agent: 'test-mode-agent',
        maxAmount: 5,
        currency: 'USD',
        allowedRecipients: ['GB29NWBK60161331926819'],
        ttlSeconds: 60,
      }

      const created = await skill.invoke('create_envelope', input) as CreateEnvelopeOutput
      expect(created.envelopeJson).toBeTruthy()
      expect(created.signature).toBeTruthy()

      const verified = await skill.invoke('verify_envelope', { envelope: created }) as { valid: boolean }
      expect(verified.valid).toBe(true)

      const revoked = await skill.invoke('revoke_envelope', { envelope: created }) as {
        revoked: boolean
        revokedAt: string
        httpStatus: number
      }
      expect(revoked.revoked).toBe(true)
      expect(revoked.revokedAt).toBeTruthy()
      expect(revoked.httpStatus).toBe(0) // test mode sentinel
    } finally {
      if (savedApiKey !== undefined) process.env['PQSAFE_API_KEY'] = savedApiKey
      if (savedKeyId !== undefined) process.env['PQSAFE_KEY_ID'] = savedKeyId
    }
  })

  // ── Test 7: unknown operation throws ──────────────────────────────────────

  it('invoke() throws for an unknown operation', async () => {
    const skill = getSkill()
    await expect(skill.invoke('not_a_real_operation', {})).rejects.toThrow(
      'unknown operation "not_a_real_operation"',
    )
  })

  // ── Test 8: revoke_envelope in test mode ──────────────────────────────────

  it('revoke_envelope returns revoked=true and an ISO revokedAt in test mode', async () => {
    const skill = getSkill()
    const created = await skill.invoke('create_envelope', BASE_CREATE_INPUT) as CreateEnvelopeOutput

    const revokeInput: RevokeEnvelopeInput = {
      envelope: created,
      reason: 'test revocation',
    }

    const result = await skill.invoke('revoke_envelope', revokeInput) as {
      revoked: boolean
      revokedAt: string
      httpStatus: number
    }

    expect(result.revoked).toBe(true)
    expect(result.httpStatus).toBe(0)

    const ts = new Date(result.revokedAt)
    expect(isNaN(ts.getTime())).toBe(false)
  })

})
