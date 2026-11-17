/**
 * Authenticité des requêtes de synchro entre daemons (SYNC §3.5).
 *
 * Chaque requête `/v1/sync/*` est signée HMAC-SHA256 avec la CPK (Cluster
 * Pairing Key, PSK 32 o partagée au pairing, en Keychain) :
 *
 *   sig = HMAC(CPK, method | path | sha256(body) | ts | nonce)
 *
 * → intégrité (corps non altéré), authenticité (seul un détenteur de la CPK
 * peut signer), anti-MITM. Couplé à :
 *   - ts dans une fenêtre ±60 s (anti-rejeu grossier) ;
 *   - nonce mémorisé 5 min (anti-rejeu fin, même dans la fenêtre).
 *
 * Les VALEURS de secrets voyagent déjà chiffrées GVK → un sniff LAN ne révèle
 * aucun plaintext et ne peut rien forger. TLS donc optionnel.
 */
import { createHmac, randomBytes, timingSafeEqual } from 'node:crypto'
import { sha256Hex } from '../util.js'

export interface SigParts {
  method: string
  path: string
  body: string
  ts: string
  nonce: string
}

export const SYNC_TS_SKEW_MS = 60_000 // ±60 s
export const SYNC_NONCE_TTL_MS = 5 * 60_000 // 5 min

/** Signature canonique d'une requête. */
export function signRequest(cpk: Buffer, p: SigParts): string {
  const canonical = `${p.method.toUpperCase()}|${p.path}|${sha256Hex(p.body)}|${p.ts}|${p.nonce}`
  return createHmac('sha256', cpk).update(canonical).digest('hex')
}

/** Nonce opaque non devinable. */
export function newNonce(): string {
  return randomBytes(16).toString('hex')
}

export interface VerifyResult {
  ok: boolean
  reason?: 'bad_sig' | 'stale_ts' | 'replay'
}

/**
 * Vérifie la signature, la fraîcheur de l'horodatage et l'absence de rejeu.
 * `seenNonce` doit renvoyer true si le nonce a déjà été vu (→ rejeu refusé).
 * `nowMs` injectable pour les tests.
 */
export function verifyRequest(
  cpk: Buffer,
  presentedSig: string,
  p: SigParts,
  seenNonce: (nonce: string) => boolean,
  nowMs: number = Date.now(),
): VerifyResult {
  // 1) horodatage frais
  const tsMs = Date.parse(p.ts)
  if (!Number.isFinite(tsMs) || Math.abs(nowMs - tsMs) > SYNC_TS_SKEW_MS) return { ok: false, reason: 'stale_ts' }

  // 2) signature (comparaison à temps constant)
  const expected = signRequest(cpk, p)
  if (!timingSafeEqualHex(expected, presentedSig)) return { ok: false, reason: 'bad_sig' }

  // 3) anti-rejeu (après la signature : ne révèle rien à un attaquant sans CPK)
  if (seenNonce(p.nonce)) return { ok: false, reason: 'replay' }

  return { ok: true }
}

function timingSafeEqualHex(a: string, b: string): boolean {
  if (a.length !== b.length) return false
  try {
    return timingSafeEqual(Buffer.from(a, 'hex'), Buffer.from(b, 'hex'))
  } catch {
    return false
  }
}
