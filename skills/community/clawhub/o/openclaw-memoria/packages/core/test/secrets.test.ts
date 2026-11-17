/**
 * Tests secrets (spec §9, D2 — gate dur) : coffre AES round-trip, chiffrement
 * réel sur disque, clé machine régénérée → null propre, redaction par pattern,
 * anti-faux-positifs, keychain macOS (local uniquement, jamais en CI).
 */
import { mkdtempSync, readFileSync, rmSync, statSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { randomBytes } from 'node:crypto'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import {
  AesVaultProvider,
  KeychainMacProvider,
  RegexRedactor,
  createSecretProvider,
} from '../src/secrets/index.js'

let dir: string

beforeEach(() => {
  dir = mkdtempSync(join(tmpdir(), 'memoria-secrets-'))
})

afterEach(() => {
  rmSync(dir, { recursive: true, force: true })
  vi.restoreAllMocks()
})

describe('AesVaultProvider — coffre fallback', () => {
  it('round-trip set / get / delete', () => {
    const vault = new AesVaultProvider(dir, { env: {} })
    expect(vault.isAvailable()).toBe(true)
    expect(vault.get('absent')).toBeNull()

    vault.set('anthropic-key', 'REDACTED-SECRET')
    expect(vault.get('anthropic-key')).toBe('REDACTED-SECRET')
    expect(vault.locationFor('anthropic-key')).toBe('vault:secrets.enc#anthropic-key')

    // update en place
    vault.set('anthropic-key', 'nouvelle-valeur')
    expect(vault.get('anthropic-key')).toBe('nouvelle-valeur')

    vault.delete('anthropic-key')
    expect(vault.get('anthropic-key')).toBeNull()
    // delete idempotent
    vault.delete('anthropic-key')
  })

  it('chiffrement réel : le fichier ne contient jamais la valeur en clair', () => {
    const vault = new AesVaultProvider(dir, { env: {} })
    const value = 'super-secret-plaintext-XYZ'
    vault.set('clef', value)

    const onDisk = readFileSync(join(dir, 'secrets.enc'), 'utf8')
    expect(onDisk).not.toContain(value)
    expect(onDisk).toContain('"entries"') // mais le format JSON est bien là

    // permissions 600 sur le coffre ET la clé machine
    expect(statSync(join(dir, 'secrets.enc')).mode & 0o777).toBe(0o600)
    expect(statSync(join(dir, 'vault.key')).mode & 0o777).toBe(0o600)
  })

  it('clé machine régénérée → get retourne null proprement (avec warn, sans throw)', () => {
    const warn = vi.spyOn(console, 'warn').mockImplementation(() => {})
    const vault = new AesVaultProvider(dir, { env: {} })
    vault.set('clef', 'valeur-perdue')

    // simulation réinstall machine : vault.key remplacée
    writeFileSync(join(dir, 'vault.key'), randomBytes(32).toString('base64'), 'utf8')

    const fresh = new AesVaultProvider(dir, { env: {} })
    expect(fresh.get('clef')).toBeNull()
    expect(warn).toHaveBeenCalledOnce()
    expect(String(warn.mock.calls[0]?.[0])).toContain('indéchiffrable')
  })

  it('MEMORIA_VAULT_KEY prime sur la clé machine', () => {
    const env = { MEMORIA_VAULT_KEY: 'ma-passphrase-de-test' }
    const a = new AesVaultProvider(dir, { env })
    a.set('clef', 'valeur-env')

    // même passphrase → lisible ; clé machine (env vide) → null + warn
    expect(new AesVaultProvider(dir, { env }).get('clef')).toBe('valeur-env')
    const warn = vi.spyOn(console, 'warn').mockImplementation(() => {})
    expect(new AesVaultProvider(dir, { env: {} }).get('clef')).toBeNull()
    expect(warn).toHaveBeenCalled()
  })

  it('coffre corrompu → erreur explicite (jamais écrasé en silence)', () => {
    const vault = new AesVaultProvider(dir, { env: {} })
    vault.set('clef', 'valeur')
    writeFileSync(join(dir, 'secrets.enc'), 'pas du json{{{', 'utf8')
    expect(() => vault.get('clef')).toThrow(/coffre illisible/)
    expect(() => vault.set('autre', 'x')).toThrow(/coffre illisible/)
  })
})

describe('createSecretProvider — factory', () => {
  it('force=aes-vault → AesVaultProvider même sur macOS', () => {
    const p = createSecretProvider(dir, { force: 'aes-vault', env: {} })
    expect(p.kind).toBe('aes-vault')
  })

  it('force=keychain-macos → KeychainMacProvider', () => {
    const p = createSecretProvider(dir, { force: 'keychain-macos' })
    expect(p.kind).toBe('keychain-macos')
  })

  it('auto : keychain si dispo, sinon vault', () => {
    const p = createSecretProvider(dir, { env: {} })
    const expected = new KeychainMacProvider().isAvailable() ? 'keychain-macos' : 'aes-vault'
    expect(p.kind).toBe(expected)
  })
})

describe('RegexRedactor — chaque pattern redacte (valeur jamais en sortie)', () => {
  const redactor = new RegexRedactor()

  /** Vérifie : valeur absente du texte de sortie + kind détecté + placeholder posé. */
  function expectRedacted(text: string, value: string, kind: string): void {
    const r = redactor.redact(text)
    expect(r.text).not.toContain(value)
    const hit = r.found.find(f => f.kind === kind)
    expect(hit, `kind '${kind}' attendu dans ${JSON.stringify(r.found)}`).toBeDefined()
    expect(hit?.value).toBe(value)
    expect(r.text).toContain(`[secret:${hit?.name}]`)
  }

  it('Anthropic', () => {
    const v = 'REDACTED-SECRET'
    expectRedacted(`ma clé est ${v} ok`, v, 'anthropic')
  })

  it('OpenAI (classique + project)', () => {
    const v1 = 'REDACTED-SECRET'
    expectRedacted(`OPENAI_API_KEY ${v1}`, v1, 'openai')
    const v2 = 'REDACTED-SECRET'
    expectRedacted(`clé projet ${v2}`, v2, 'openai')
  })

  it('AWS access key + secret en contexte aws', () => {
    const access = 'REDACTED-SECRET'
    expectRedacted(`access ${access} fin`, access, 'aws-access-key')

    const secret = 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'
    expectRedacted(`aws_secret_access_key = ${secret}`, secret, 'aws-secret-key')
  })

  it('GitHub (ghp_ / github_pat_)', () => {
    const v1 = 'REDACTED-SECRET'
    expectRedacted(`token github ${v1}`, v1, 'github')
    const v2 = 'github_pat_11ABCDEFG0abcdefghijklmnopqrstuvwxyz'
    expectRedacted(`pat: ${v2}`, v2, 'github')
  })

  it('Google', () => {
    const v = `AIzaSy${'A'.repeat(33)}` // AIza + 35 caractères
    expectRedacted(`clé google ${v} ici`, v, 'google')
  })

  it('Slack', () => {
    // construit par concaténation : ne doit JAMAIS ressembler à un vrai token
    // dans le source (GitHub Push Protection scanne les fixtures)
    const v = ['xoxb', '1234567890', 'ABCDEFabcdef123456'].join('-')
    expectRedacted(`bot slack ${v}`, v, 'slack')
  })

  it('JWT (3 segments base64url)', () => {
    const v =
      'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4ifQ.dBjftJeZ4CVPmB92K27uhbUJU1p1r_wW1gFWFOEjXk'
    expectRedacted(`Authorization: Bearer ${v}`, v, 'jwt')
  })

  it('bloc PEM (multi-lignes)', () => {
    const v = `REDACTED-SECRET`
    expectRedacted(`voici la clé :\n${v}\nfin`, v, 'pem-private-key')
  })

  it('token générique (password/secret/api_key + valeur longue)', () => {
    expectRedacted('password: Hunter2Hunter2!', 'Hunter2Hunter2!', 'generic-token')
    expectRedacted('export API_KEY=abc123def456ghi789', 'abc123def456ghi789', 'generic-token')
    expectRedacted('"secret": "longue-valeur-cachee-42"', 'longue-valeur-cachee-42', 'generic-token')
  })

  it('même valeur deux fois → un seul nom, une seule entrée found', () => {
    const v = 'REDACTED-SECRET'
    const r = redactor.redact(`début ${v} puis encore ${v} fin`)
    expect(r.found).toHaveLength(1)
    expect(r.text).not.toContain(v)
    expect(r.text.split(`[secret:${r.found[0]?.name}]`)).toHaveLength(3)
  })

  it('deux secrets du même kind → noms distincts, stables par valeur (hash)', () => {
    const r = redactor.redact(
      'a: REDACTED-SECRET b: REDACTED-SECRET',
    )
    expect(r.found).toHaveLength(2)
    const names = r.found.map(f => f.name)
    expect(names[0]).toMatch(/^anthropic-[0-9a-f]{8}$/)
    expect(names[1]).toMatch(/^anthropic-[0-9a-f]{8}$/)
    expect(names[0]).not.toBe(names[1])
    // stabilité inter-exécutions : même valeur → même nom (anti-écrasement coffre)
    const again = redactor.redact('a: REDACTED-SECRET')
    expect(again.found[0]?.name).toBe(names[0])
  })
})

describe('RegexRedactor — anti-faux-positifs', () => {
  const redactor = new RegexRedactor()

  it('hash git, UUID, URL, texte normal : rien n’est redacté', () => {
    const samples = [
      'commit 3f2b8a9c1d4e5f60718293a4b5c6d7e8f9012345 sur main',
      'id 550e8400-e29b-41d4-a716-446655440000 créé hier',
      'voir https://docs.example.com/guide/installation?page=2&lang=fr',
      'le secret est bien gardé, le mot de passe sera changé demain',
      'sk-court non plus, ni AKIA tout seul, ni eyJtropCourt.x.y',
      'fichier /usr/local/bin/security taille 1234567890123 octets',
    ]
    for (const s of samples) {
      const r = redactor.redact(s)
      expect(r.text, `faux positif sur : ${s}`).toBe(s)
      expect(r.found).toHaveLength(0)
    }
  })

  it('un placeholder déjà posé n’est pas re-redacté', () => {
    const r1 = new RegexRedactor().redact('api_key = REDACTED-SECRET')
    expect(r1.found).toHaveLength(1)
    expect(r1.found[0]?.kind).toBe('anthropic')
    // repasser le texte redacté → stable (idempotent)
    const r2 = new RegexRedactor().redact(r1.text)
    expect(r2.found).toHaveLength(0)
    expect(r2.text).toBe(r1.text)
  })
})

// Keychain : test réel UNIQUEMENT en local macOS (jamais en CI), service dédié
// + cleanup pour ne pas polluer le trousseau.
const keychainTestable = process.platform === 'darwin' && process.env['CI'] === undefined

describe.skipIf(!keychainTestable)('KeychainMacProvider — macOS local uniquement', () => {
  const service = `memoria-test-${process.pid}-${Date.now()}`
  const provider = new KeychainMacProvider({ service })
  const name = 'test-secret'

  afterEach(() => {
    provider.delete(name) // cleanup quoi qu'il arrive (delete idempotent)
  })

  it('isAvailable + locationFor', () => {
    expect(provider.isAvailable()).toBe(true)
    expect(provider.locationFor(name)).toBe(`keychain:${service}/${name}`)
  })

  it('round-trip set / get / update / delete', () => {
    expect(provider.get(name)).toBeNull()
    provider.set(name, 'valeur keychain 1')
    expect(provider.get(name)).toBe('valeur keychain 1')
    provider.set(name, 'valeur keychain 2') // -U : update en place
    expect(provider.get(name)).toBe('valeur keychain 2')
    provider.delete(name)
    expect(provider.get(name)).toBeNull()
  })
})
