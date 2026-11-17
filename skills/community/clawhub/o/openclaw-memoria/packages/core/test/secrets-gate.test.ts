/**
 * QW1 — gate secrets en défense en profondeur : un secret posé EN DIRECT via
 * storeFact (pas seulement la capture) ne touche jamais la base. + nouveaux
 * patterns (Stripe, Google OAuth, connection strings, webhooks).
 */
import { mkdtempSync, rmSync, readdirSync, readFileSync, statSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { afterEach, beforeEach, describe, expect, it } from 'vitest'
import { Memoria, RegexRedactor } from '../src/index.js'

describe('RegexRedactor — patterns ajoutés (audit QW1)', () => {
  const r = new RegexRedactor()
  // Fixtures construites par concaténation : ne JAMAIS écrire un jeton qui
  // ressemble à un vrai secret en littéral (GitHub Push Protection les bloque).
  const cases: Array<[string, string]> = [
    ['stripe', `la clé est ${'sk_live_' + '51HxYzABCdef1234567890ABCD'} pour Primask`],
    ['stripe-session', `session ${'cs_live_' + 'a1b2c3d4e5f6g7h8i9j0k1l2m3'} ouverte`],
    ['stripe-webhook', `webhook ${'whsec_' + 'aBcDeF1234567890aBcDeF1234'} configuré`],
    ['google-oauth', `token ${'ya29.' + 'A0ARrdaM-abcdefghij1234567890'} reçu`],
    ['connection-string', `postgres://admin:${'S3cretPass'}@db.primo.fr:5432/prod`],
  ]
  for (const [label, text] of cases) {
    it(`redacte ${label}`, () => {
      const out = r.redact(text)
      expect(out.found.length).toBeGreaterThan(0)
      // la valeur sensible n'apparaît plus
      const secret = out.found[0]!.value
      expect(out.text).not.toContain(secret)
    })
  }
})

describe('gate storeFact (défense en profondeur)', () => {
  let root: string
  let m: Memoria
  beforeEach(() => {
    root = mkdtempSync(join(tmpdir(), 'memoria-gate-'))
    m = Memoria.init({ storageRoot: root, configPath: join(root, 'config.toml'), llm: { extraction: null }, secretsVault: 'aes-vault' })
  })
  afterEach(() => {
    m.close()
    rmSync(root, { recursive: true, force: true })
  })

  it('un secret posé via storeFact EN DIRECT n’est jamais stocké en clair', () => {
    const a = m.pairAssistant({ type: 'claude-code' })
    const KEY = 'sk_live_' + '51ABCdef1234567890PRIMOSTUDIO' // concat : pas de littéral
    m.storeFact({ instance: a.assistant_instance_id, content: `La clé Stripe de prod est ${KEY}` })

    // la valeur n'apparaît dans AUCUN fichier du stockage
    const offenders: string[] = []
    const walk = (dir: string): void => {
      for (const name of readdirSync(dir)) {
        const p = join(dir, name)
        if (statSync(p).isDirectory()) walk(p)
        else if (readFileSync(p).includes(KEY)) offenders.push(p)
      }
    }
    walk(root)
    expect(offenders).toEqual([])

    // mais la référence est au coffre + récupérable
    const refs = m.listSecrets()
    expect(refs.length).toBe(1)
    expect(m['secretProvider'].get(refs[0]!.name)).toBe(KEY)

    // et le recall ne renvoie jamais la valeur
    const r = m.recall({ instance: a.assistant_instance_id, query: 'clé stripe prod' })
    expect(r.items.every(i => !i.content.includes(KEY))).toBe(true)
  })
})
