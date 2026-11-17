/**
 * Coffre fallback universel (spec §9, D2) : fichier chiffré AES-256-GCM.
 * - Clé dérivée (scrypt) depuis $MEMORIA_VAULT_KEY si défini, sinon depuis une
 *   clé machine auto-générée `<secretsDir>/vault.key` (chmod 600).
 * - Format `<secretsDir>/secrets.enc` : JSON {version, salt, entries:{name:{iv,tag,data}}}.
 * - Si la clé machine change (réinstall, copie partielle), `get` retourne null
 *   AVEC un warn — jamais de plaintext corrompu, jamais d'échec silencieux.
 */
import {
  chmodSync,
  existsSync,
  mkdirSync,
  readFileSync,
  renameSync,
  writeFileSync,
} from 'node:fs'
import { join } from 'node:path'
import { createCipheriv, createDecipheriv, randomBytes, scryptSync } from 'node:crypto'
import type { SecretProvider } from './types.js'

const VAULT_VERSION = 1
const IV_BYTES = 12
const KEY_BYTES = 32
const SALT_BYTES = 16

interface VaultEntry {
  iv: string
  tag: string
  data: string
}

interface VaultFile {
  version: number
  salt: string
  entries: Record<string, VaultEntry>
}

export interface AesVaultOptions {
  /** Environnement injectable pour les tests (lit MEMORIA_VAULT_KEY). */
  env?: NodeJS.ProcessEnv
}

export class AesVaultProvider implements SecretProvider {
  readonly kind = 'aes-vault'
  private readonly vaultPath: string
  private readonly keyPath: string
  private readonly env: NodeJS.ProcessEnv

  constructor(secretsDir: string, opts: AesVaultOptions = {}) {
    this.vaultPath = join(secretsDir, 'secrets.enc')
    this.keyPath = join(secretsDir, 'vault.key')
    this.env = opts.env ?? process.env
    mkdirSync(secretsDir, { recursive: true })
  }

  /** Fallback universel : toujours disponible. */
  isAvailable(): boolean {
    return true
  }

  set(name: string, value: string): void {
    const vault = this.loadVault()
    const key = this.deriveKey(Buffer.from(vault.salt, 'base64'))
    const iv = randomBytes(IV_BYTES)
    const cipher = createCipheriv('aes-256-gcm', key, iv)
    const data = Buffer.concat([cipher.update(value, 'utf8'), cipher.final()])
    vault.entries[name] = {
      iv: iv.toString('base64'),
      tag: cipher.getAuthTag().toString('base64'),
      data: data.toString('base64'),
    }
    this.writeVault(vault)
  }

  get(name: string): string | null {
    if (!existsSync(this.vaultPath)) return null
    const vault = this.loadVault()
    const entry = vault.entries[name]
    if (!entry) return null
    try {
      const key = this.deriveKey(Buffer.from(vault.salt, 'base64'))
      const decipher = createDecipheriv('aes-256-gcm', key, Buffer.from(entry.iv, 'base64'))
      decipher.setAuthTag(Buffer.from(entry.tag, 'base64'))
      const plain = Buffer.concat([
        decipher.update(Buffer.from(entry.data, 'base64')),
        decipher.final(),
      ])
      return plain.toString('utf8')
    } catch {
      // GCM auth tag invalide = clé différente (vault.key régénérée ou
      // MEMORIA_VAULT_KEY changé) ou fichier altéré. Null propre + warn.
      console.warn(
        `[memoria] secret '${name}' indéchiffrable (clé du coffre changée ?) — get() retourne null`,
      )
      return null
    }
  }

  delete(name: string): void {
    if (!existsSync(this.vaultPath)) return
    const vault = this.loadVault()
    if (!(name in vault.entries)) return
    delete vault.entries[name]
    this.writeVault(vault)
  }

  locationFor(name: string): string {
    return `vault:secrets.enc#${name}`
  }

  /** Charge le coffre, ou en initialise un neuf (sel frais) s'il n'existe pas. */
  private loadVault(): VaultFile {
    if (!existsSync(this.vaultPath)) {
      return { version: VAULT_VERSION, salt: randomBytes(SALT_BYTES).toString('base64'), entries: {} }
    }
    const raw = readFileSync(this.vaultPath, 'utf8')
    let parsed: unknown
    try {
      parsed = JSON.parse(raw)
    } catch (err) {
      // On THROW (pas de coffre vide implicite) : écraser un fichier corrompu
      // détruirait les secrets existants.
      throw new Error(`coffre illisible (${this.vaultPath}) : ${(err as Error).message}`)
    }
    const vault = parsed as VaultFile
    if (vault.version !== VAULT_VERSION || typeof vault.salt !== 'string' || typeof vault.entries !== 'object') {
      throw new Error(`coffre invalide ou version inconnue (${this.vaultPath})`)
    }
    return vault
  }

  private writeVault(vault: VaultFile): void {
    // Écriture temp + rename : un crash en cours d'écriture ne corrompt pas le coffre.
    const tmp = `${this.vaultPath}.tmp`
    writeFileSync(tmp, JSON.stringify(vault), { encoding: 'utf8', mode: 0o600 })
    renameSync(tmp, this.vaultPath)
    chmodSync(this.vaultPath, 0o600)
  }

  /** Passphrase = $MEMORIA_VAULT_KEY sinon clé machine (créée au premier usage). */
  private passphrase(): string {
    const fromEnv = this.env['MEMORIA_VAULT_KEY']
    if (fromEnv && fromEnv.length > 0) return fromEnv
    if (!existsSync(this.keyPath)) {
      writeFileSync(this.keyPath, randomBytes(KEY_BYTES).toString('base64'), {
        encoding: 'utf8',
        mode: 0o600,
      })
      chmodSync(this.keyPath, 0o600)
    }
    return readFileSync(this.keyPath, 'utf8').trim()
  }

  private deriveKey(salt: Buffer): Buffer {
    return scryptSync(this.passphrase(), salt, KEY_BYTES)
  }
}
