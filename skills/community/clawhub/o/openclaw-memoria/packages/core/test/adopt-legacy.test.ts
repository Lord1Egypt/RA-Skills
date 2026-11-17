/**
 * adoptLegacyInto : la quarantaine d'import devient la mémoire PRIVÉE d'une
 * instance, recallable. Déplacement (quarantaine vidée), pas duplication.
 */
import { mkdtempSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { afterEach, beforeEach, describe, expect, it } from 'vitest'
import { Memoria, createSyntheticLegacyDb, importLegacyDb } from '../src/index.js'

let root: string
let m: Memoria
let legacyPath: string

beforeEach(() => {
  root = mkdtempSync(join(tmpdir(), 'memoria-adopt-'))
  m = Memoria.init({ storageRoot: root, configPath: join(root, 'config.toml'), llm: { extraction: null } })
  legacyPath = join(root, 'legacy.db')
  createSyntheticLegacyDb(legacyPath, { factCount: 40, procedureCount: 6 })
})

afterEach(() => {
  m.close()
  rmSync(root, { recursive: true, force: true })
})

describe('adoptLegacyInto', () => {
  it('importe en quarantaine puis adopte dans la mémoire privée → recallable', () => {
    const koda = m.pairAssistant({ type: 'openclaw', display_name: 'Koda' })
    const rep = importLegacyDb({ legacyPath, memoria: m })
    expect(rep.facts_imported).toBeGreaterThan(0)

    // en quarantaine : pas recallable
    const before = m.recall({ instance: koda.assistant_instance_id, query: 'Directus Cloudflare Vercel' })
    expect(before.items).toHaveLength(0)

    const adopted = m.adoptLegacyInto(koda.assistant_instance_id)
    expect(adopted.facts).toBe(rep.facts_imported)

    // quarantaine vidée
    const legacyScope = m.registry.getScopeByName('legacy_to_review')!
    const legacyDb = m['openContent'](m.registry.dbForScope(legacyScope.id)!.path)
    expect(legacyDb.countFacts()).toBe(0)

    // mémoire privée de Koda peuplée et recallable
    const kodaDb = m['openContent'](m.paths.assistantDb(koda.assistant_instance_id))
    expect(kodaDb.countFacts()).toBe(adopted.facts)
    const recall = m.recall({ instance: koda.assistant_instance_id, query: 'Directus Cloudflare deploiement', limit: 50 })
    expect(recall.items.length).toBeGreaterThan(0)

    // audit neutre tracé
    expect(m.registry.auditTail(20).some(e => e.action === 'adopt_legacy')).toBe(true)
  })

  it('un autre agent ne voit pas la mémoire privée adoptée (isolation respectée)', () => {
    const koda = m.pairAssistant({ type: 'openclaw' })
    const claude = m.pairAssistant({ type: 'claude-code' })
    importLegacyDb({ legacyPath, memoria: m })
    m.adoptLegacyInto(koda.assistant_instance_id)

    const fromClaude = m.recall({ instance: claude.assistant_instance_id, query: 'Directus Cloudflare deploiement', limit: 50 })
    expect(fromClaude.items).toHaveLength(0)
  })
})
