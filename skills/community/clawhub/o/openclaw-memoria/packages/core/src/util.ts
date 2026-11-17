import { createHash, randomUUID, randomBytes } from 'node:crypto'

export function newId(): string {
  return randomUUID()
}

export function nowISO(): string {
  return new Date().toISOString()
}

export function sha256Hex(input: string | Buffer): string {
  return createHash('sha256').update(input).digest('hex')
}

/** Token opaque pour instances/pairing — 32 octets url-safe. */
export function newToken(): string {
  return randomBytes(32).toString('base64url')
}

/** Code de pairing court lisible (à copier-coller dans le chat de l'agent). */
export function newPairingCode(): string {
  // 8 caractères sans ambiguïté (pas de 0/O/1/I/l)
  const alphabet = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789'
  const bytes = randomBytes(8)
  let out = ''
  for (const b of bytes) out += alphabet[b % alphabet.length]
  return `${out.slice(0, 4)}-${out.slice(4)}`
}

/**
 * Estimation de tokens sans dépendance (≈ 4 caractères/token).
 * Sert au CAP DUR du budget d'injection — mieux vaut surestimer légèrement.
 */
export function estimateTokens(text: string): number {
  return Math.ceil(text.length / 3.6)
}

export function toJson(value: unknown): string {
  return JSON.stringify(value ?? null)
}

export function fromJsonArray(raw: string | null | undefined): string[] {
  if (!raw) return []
  try {
    const parsed: unknown = JSON.parse(raw)
    return Array.isArray(parsed) ? parsed.map(String) : []
  } catch {
    return []
  }
}

/** Sérialisation Float32 little-endian pour les embeddings (format legacy conservé). */
export function vectorToBuffer(vec: ReadonlyArray<number> | Float32Array): Buffer {
  const f32 = vec instanceof Float32Array ? vec : Float32Array.from(vec)
  return Buffer.from(f32.buffer, f32.byteOffset, f32.byteLength)
}

export function bufferToVector(buf: Buffer): Float32Array {
  return new Float32Array(buf.buffer, buf.byteOffset, buf.byteLength / 4)
}
