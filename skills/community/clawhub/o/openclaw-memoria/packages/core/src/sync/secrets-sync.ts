/**
 * Coffre inter-machines (SYNC §3.4) : les VALEURS de secrets ne traversent le
 * réseau que chiffrées GVK (AES-256-GCM, même format qu'aes-vault.ts). La GVK
 * elle-même ne voyage qu'UNE fois, scellée par scrypt(code-de-pairing) à TTL court.
 *
 * Aucune valeur en clair ne sort jamais d'ici sans la bonne clé : tag GCM
 * invalide → null (jamais de plaintext corrompu).
 */
import { createCipheriv, createDecipheriv, scryptSync } from 'node:crypto'

const ALGO = 'aes-256-gcm'
const IV_BYTES = 12
const SCRYPT_SALT = 'memoria-sync-gvk-v1' // sel fixe : le secret est le code one-shot, pas le sel

export interface Envelope {
  iv: string
  tag: string
  data: string
}

/** Chiffre une valeur de secret avec la GVK → enveloppe transportable. */
export function sealValue(value: string, gvk: Buffer): Envelope {
  const iv = randomIv()
  const cipher = createCipheriv(ALGO, gvk, iv)
  const data = Buffer.concat([cipher.update(value, 'utf8'), cipher.final()])
  const tag = cipher.getAuthTag()
  return { iv: iv.toString('base64'), tag: tag.toString('base64'), data: data.toString('base64') }
}

/** Déchiffre une enveloppe. Mauvaise clé / tag invalide → null (jamais de crash). */
export function openEnvelope(env: Envelope, gvk: Buffer): string | null {
  try {
    const decipher = createDecipheriv(ALGO, gvk, Buffer.from(env.iv, 'base64'))
    decipher.setAuthTag(Buffer.from(env.tag, 'base64'))
    const out = Buffer.concat([decipher.update(Buffer.from(env.data, 'base64')), decipher.final()])
    return out.toString('utf8')
  } catch {
    return null
  }
}

/** Scelle la GVK avec le code de pairing (scrypt) — transport unique au bootstrap. */
export function sealGvk(gvk: Buffer, pairingCode: string): string {
  const key = scryptSync(pairingCode, SCRYPT_SALT, 32)
  const env = sealValue(gvk.toString('base64'), key)
  return `${env.iv}:${env.tag}:${env.data}`
}

/** Descelle la GVK reçue avec le code de pairing. Mauvais code → null. */
export function openGvk(sealed: string, pairingCode: string): Buffer | null {
  const parts = sealed.split(':')
  if (parts.length !== 3) return null
  const [iv, tag, data] = parts as [string, string, string]
  const key = scryptSync(pairingCode, SCRYPT_SALT, 32)
  const b64 = openEnvelope({ iv, tag, data }, key)
  return b64 === null ? null : Buffer.from(b64, 'base64')
}

function randomIv(): Buffer {
  // crypto.randomBytes via webcrypto pour rester homogène avec le reste du module sync
  const arr = new Uint8Array(IV_BYTES)
  globalThis.crypto.getRandomValues(arr)
  return Buffer.from(arr)
}
