/**
 * Crypto de synchro (sécurité-critique) : HMAC anti-rejeu/MITM + scellage GVK.
 */
import { randomBytes } from 'node:crypto'
import { describe, expect, it } from 'vitest'
import {
  newNonce,
  openEnvelope,
  openGvk,
  sealGvk,
  sealValue,
  signRequest,
  verifyRequest,
  type SigParts,
} from '../src/index.js'

const CPK = randomBytes(32)
const parts = (over: Partial<SigParts> = {}): SigParts => ({
  method: 'GET',
  path: '/v1/sync/pull?scope=org&since=0',
  body: '',
  ts: new Date().toISOString(),
  nonce: newNonce(),
  ...over,
})

describe('signRequest / verifyRequest', () => {
  it('signature valide acceptée', () => {
    const p = parts()
    const sig = signRequest(CPK, p)
    expect(verifyRequest(CPK, sig, p, () => false).ok).toBe(true)
  })

  it('corps altéré → signature refusée', () => {
    const p = parts({ body: '{"a":1}' })
    const sig = signRequest(CPK, p)
    const tampered = { ...p, body: '{"a":2}' }
    expect(verifyRequest(CPK, sig, tampered, () => false)).toMatchObject({ ok: false, reason: 'bad_sig' })
  })

  it('mauvaise clé → refusée', () => {
    const p = parts()
    const sig = signRequest(CPK, p)
    expect(verifyRequest(randomBytes(32), sig, p, () => false).ok).toBe(false)
  })

  it('horodatage hors fenêtre (±60 s) → refusé', () => {
    const old = parts({ ts: new Date(Date.now() - 120_000).toISOString() })
    const sig = signRequest(CPK, old)
    expect(verifyRequest(CPK, sig, old, () => false)).toMatchObject({ ok: false, reason: 'stale_ts' })
  })

  it('rejeu (nonce déjà vu) → refusé', () => {
    const p = parts()
    const sig = signRequest(CPK, p)
    expect(verifyRequest(CPK, sig, p, () => true)).toMatchObject({ ok: false, reason: 'replay' })
  })

  it('path différent → refusé (lie la signature à la ressource)', () => {
    const p = parts({ path: '/v1/sync/pull?scope=org' })
    const sig = signRequest(CPK, p)
    expect(verifyRequest(CPK, sig, { ...p, path: '/v1/sync/secrets?scope=org' }, () => false).ok).toBe(false)
  })
})

describe('scellage des valeurs (GVK)', () => {
  it('round-trip seal/open', () => {
    const gvk = randomBytes(32)
    const env = sealValue('mot-de-passe-NAS', gvk)
    expect(JSON.stringify(env)).not.toContain('mot-de-passe-NAS') // jamais en clair
    expect(openEnvelope(env, gvk)).toBe('mot-de-passe-NAS')
  })

  it('mauvaise GVK → null (jamais de plaintext corrompu, pas de crash)', () => {
    const env = sealValue('secret', randomBytes(32))
    expect(openEnvelope(env, randomBytes(32))).toBeNull()
  })
})

describe('scellage de la GVK par le code de pairing (scrypt)', () => {
  it('round-trip sealGvk/openGvk avec le bon code', () => {
    const gvk = randomBytes(32)
    const sealed = sealGvk(gvk, 'AB12-CD34')
    expect(sealed).not.toContain(gvk.toString('hex'))
    expect(openGvk(sealed, 'AB12-CD34')?.equals(gvk)).toBe(true)
  })

  it('mauvais code → null', () => {
    const sealed = sealGvk(randomBytes(32), 'AB12-CD34')
    expect(openGvk(sealed, 'WRONG-CODE')).toBeNull()
  })
})
