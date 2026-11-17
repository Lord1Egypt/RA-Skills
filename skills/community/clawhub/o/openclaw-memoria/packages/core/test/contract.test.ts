/**
 * Tests du contrat core (spec §15 P1 DoD) :
 * init / pairing / storeFact / recall / forget / isolation.
 * Chaque chemin « actif » doit prouver qu'il S'EXÉCUTE (règle anti-mort-silencieuse).
 */
import { mkdtempSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { afterEach, beforeEach, describe, expect, it } from 'vitest'
import { Memoria } from '../src/index.js'

let root: string
let m: Memoria

beforeEach(() => {
  root = mkdtempSync(join(tmpdir(), 'memoria-test-'))
  m = Memoria.init({ storageRoot: root, configPath: join(root, 'config.toml') })
})

afterEach(() => {
  m.close()
  rmSync(root, { recursive: true, force: true })
})

describe('init & bootstrap', () => {
  it('crée l’arborescence et le registry', () => {
    const report = m.doctor()
    expect(report.storage_root).toBe(root)
    expect(report.databases.some(d => d.kind === 'registry' && d.exists)).toBe(true)
  })

  it('bootstrap idempotent : 1 user, 1 own_company', () => {
    const m2 = Memoria.init({ storageRoot: root, configPath: join(root, 'config.toml') })
    m2.close()
    const users = m.registry.db.prepare('SELECT COUNT(*) AS c FROM human_users').get() as { c: number }
    const orgs = m.registry.db
      .prepare("SELECT COUNT(*) AS c FROM organizations WHERE org_type = 'own_company'")
      .get() as { c: number }
    expect(users.c).toBe(1)
    expect(orgs.c).toBe(1)
  })
})

describe('pairing', () => {
  it('pairAssistant → code → completePairing → token valide', () => {
    const paired = m.pairAssistant({ type: 'claude-code' })
    expect(paired.pairing_code).toMatch(/^[A-Z2-9]{4}-[A-Z2-9]{4}$/)
    expect(paired.command).toContain(paired.pairing_code)

    const done = m.completePairing(paired.pairing_code)
    expect(done).not.toBeNull()
    expect(done!.assistant_instance_id).toBe(paired.assistant_instance_id)

    const inst = m.authenticate(done!.instance_token)
    expect(inst?.id).toBe(paired.assistant_instance_id)
  })

  it('un code ne marche qu’une fois', () => {
    const paired = m.pairAssistant({ type: 'codex' })
    expect(m.completePairing(paired.pairing_code)).not.toBeNull()
    expect(m.completePairing(paired.pairing_code)).toBeNull()
  })

  it('revoke coupe l’authentification', () => {
    const paired = m.pairAssistant({ type: 'codex' })
    const done = m.completePairing(paired.pairing_code)!
    m.revokeInstance(paired.assistant_instance_id)
    expect(m.authenticate(done.instance_token)).toBeNull()
    expect(() => m.storeFact({ instance: paired.assistant_instance_id, content: 'x' })).toThrow(/révoquée/)
  })
})

describe('storeFact & recall', () => {
  it('round-trip : capturer puis retrouver', () => {
    const a = m.pairAssistant({ type: 'claude-code' })
    m.storeFact({
      instance: a.assistant_instance_id,
      content: 'La commande de build du projet Memoria est npm run build',
      category: 'procedure',
      tags: ['build', 'memoria'],
    })
    const result = m.recall({ instance: a.assistant_instance_id, query: 'commande build memoria' })
    expect(result.items.length).toBeGreaterThan(0)
    expect(result.items[0]!.content).toContain('npm run build')
    expect(result.tokens).toBeGreaterThan(0)
  })

  it('le recall incrémente recall_count (compteurs vivants, pas morts)', () => {
    const a = m.pairAssistant({ type: 'claude-code' })
    const fact = m.storeFact({ instance: a.assistant_instance_id, content: 'Néto préfère le café sans sucre' })
    m.recall({ instance: a.assistant_instance_id, query: 'café sucre' })
    const store = m['openContent'](m.paths.assistantDb(a.assistant_instance_id))
    const updated = store.getFact(fact.id)!
    expect(updated.recall_count).toBe(1)
    expect(updated.last_accessed_at).not.toBeNull()
  })

  it('budget tokens : cap dur respecté', () => {
    const a = m.pairAssistant({ type: 'claude-code' })
    for (let i = 0; i < 30; i++) {
      m.storeFact({
        instance: a.assistant_instance_id,
        content: `Note longue numéro ${i} à propos du déploiement vercel : ${'détail '.repeat(40)}`,
      })
    }
    const result = m.recall({ instance: a.assistant_instance_id, query: 'déploiement vercel', token_budget: 200 })
    expect(result.tokens).toBeLessThanOrEqual(200)
    expect(result.items.length).toBeGreaterThan(0)
    expect(result.totalFound).toBeGreaterThan(result.items.length)
  })
})

describe('isolation', () => {
  it('2 agents : mémoires privées isolées par défaut', () => {
    const a = m.pairAssistant({ type: 'claude-code' })
    const b = m.pairAssistant({ type: 'codex' })
    m.storeFact({ instance: a.assistant_instance_id, content: 'secret de fabrication du moteur alpha' })
    const result = m.recall({ instance: b.assistant_instance_id, query: 'secret fabrication moteur alpha' })
    expect(result.items).toHaveLength(0)
  })

  it('ANTI-FUITE inter-clients : fait client A invisible en contexte client B (taux = 0)', () => {
    const a = m.pairAssistant({ type: 'claude-code' })
    const inst = a.assistant_instance_id
    // organisations clientes réelles + scope client A partagé, lisible par l'assistant
    const orgA = m.registry.createOrganization('Client A', 'client')
    const orgB = m.registry.createOrganization('Client B', 'client')
    const clientA = m.registry.ensureScope('client', 'client:A', { client_org_id: orgA.id })
    m.registry.setPolicy({
      assistant_id: a.assistant_id,
      scope_id: clientA.id,
      can_read: true,
      can_write: true,
      can_share: false,
      secret_access: 'none',
    })
    m.storeFact({
      instance: inst,
      scope: clientA.id,
      content: 'Le tarif négocié avec le client A est de 900€/jour',
      client_org_id: orgA.id,
    })

    // contexte client B → la donnée client A DOIT être invisible
    const inB = m.recall({
      instance: inst,
      query: 'tarif négocié client',
      active_context: { client_org_id: orgB.id },
    })
    expect(inB.items).toHaveLength(0)

    // sans contexte client déclaré → invisible aussi (défaut sûr)
    const noCtx = m.recall({ instance: inst, query: 'tarif négocié client' })
    expect(noCtx.items).toHaveLength(0)

    // contexte client A → visible
    const inA = m.recall({
      instance: inst,
      query: 'tarif négocié client',
      active_context: { client_org_id: orgA.id },
    })
    expect(inA.items.length).toBeGreaterThan(0)
  })
})

describe('forget (hard-delete)', () => {
  it('efface le fait + FTS + traces, et l’audit ne contient pas le contenu', () => {
    const a = m.pairAssistant({ type: 'claude-code' })
    const fact = m.storeFact({ instance: a.assistant_instance_id, content: 'souvenir compromettant à effacer' })
    const before = m.recall({ instance: a.assistant_instance_id, query: 'souvenir compromettant' })
    expect(before.items.length).toBe(1)

    const { deleted } = m.forget({ ids: [fact.id] })
    expect(deleted).toBe(1)

    const after = m.recall({ instance: a.assistant_instance_id, query: 'souvenir compromettant' })
    expect(after.items).toHaveLength(0)

    // FTS vraiment nettoyé (pas de fantôme : requête directe sur l'index)
    const store = m['openContent'](m.paths.assistantDb(a.assistant_instance_id))
    const ghosts = store.db.prepare("SELECT COUNT(*) AS c FROM facts_fts WHERE facts_fts MATCH 'compromettant'").get() as { c: number }
    expect(ghosts.c).toBe(0)

    // audit neutre : jamais le contenu
    const audit = m.registry.auditTail(50)
    expect(audit.some(e => e.action === 'forget')).toBe(true)
    for (const entry of audit) {
      expect(entry.reason ?? '').not.toContain('compromettant')
    }
  })

  it('refuse un filtre vide et exige confirm_bulk pour le massif', () => {
    expect(() => m.forget({})).toThrow(/filtre vide/)
    expect(() => m.forget({ scope_id: 'x' })).toThrow(/confirm_bulk/)
  })
})
