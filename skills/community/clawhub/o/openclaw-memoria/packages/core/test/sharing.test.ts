/**
 * Partage gouverné (spec §11) : promouvoir des faits privés vers un scope
 * partagé les rend recallables par les agents autorisés — et SEULEMENT eux.
 * suggestIdentityFacts propose, ne décide pas.
 */
import { mkdtempSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { afterEach, beforeEach, describe, expect, it } from 'vitest'
import { Memoria, type PairAssistantResult } from '../src/index.js'

let root: string
let m: Memoria
let koda: PairAssistantResult
let claude: PairAssistantResult

beforeEach(() => {
  root = mkdtempSync(join(tmpdir(), 'memoria-share-'))
  m = Memoria.init({ storageRoot: root, configPath: join(root, 'config.toml'), llm: { extraction: null } })
  koda = m.pairAssistant({ type: 'openclaw', display_name: 'Koda' })
  claude = m.pairAssistant({ type: 'claude-code', display_name: 'Claude Code' })
})

afterEach(() => {
  m.close()
  rmSync(root, { recursive: true, force: true })
})

describe('shareFacts', () => {
  it('promeut un fait privé Koda vers user → Claude Code le retrouve', () => {
    const f = m.storeFact({ instance: koda.assistant_instance_id, content: 'Le nom d’utilisateur de Neto Pompeu est primo_frances' })

    // avant partage : Claude ne voit rien (mémoires privées isolées)
    expect(m.recall({ instance: claude.assistant_instance_id, query: 'nom utilisateur Neto primo_frances' }).items).toHaveLength(0)

    const res = m.shareFacts([f.id], 'user')
    expect(res.shared).toBe(1)
    expect(res.scope).toBe('user')

    // après : les deux agents le retrouvent via le scope user partagé
    expect(m.recall({ instance: claude.assistant_instance_id, query: 'nom utilisateur Neto primo_frances' }).items.length).toBeGreaterThan(0)
    expect(m.recall({ instance: koda.assistant_instance_id, query: 'nom utilisateur Neto primo_frances' }).items.length).toBeGreaterThan(0)

    // déplacement, pas duplication : le fait n'est plus dans la DB privée Koda
    const kodaDb = m['openContent'](m.paths.assistantDb(koda.assistant_instance_id))
    expect(kodaDb.getFact(f.id)).toBeNull()
  })

  it('refuse le partage vers un scope privé ou la quarantaine', () => {
    const f = m.storeFact({ instance: koda.assistant_instance_id, content: 'secret interne' })
    expect(() => m.shareFacts([f.id], `private:${koda.assistant_instance_id}`)).toThrow(/interdit/)
    expect(() => m.shareFacts([f.id], 'legacy_to_review')).toThrow(/interdit/)
  })

  it('un agent SANS can_read sur user ne voit pas le fait partagé', () => {
    const f = m.storeFact({ instance: koda.assistant_instance_id, content: 'préférence partagée de Néto' })
    // retirer l'accès de Claude au scope user
    const userScope = m.registry.getScopeByName('user')!
    m.setScopeAccess(claude.assistant_id, userScope.id, { can_read: false })
    m.shareFacts([f.id], 'user')
    expect(m.recall({ instance: claude.assistant_instance_id, query: 'préférence partagée Néto' }).items).toHaveLength(0)
    // ré-accorder → il voit
    m.setScopeAccess(claude.assistant_id, userScope.id, { can_read: true })
    expect(m.recall({ instance: claude.assistant_instance_id, query: 'préférence partagée Néto' }).items.length).toBeGreaterThan(0)
  })
})

describe('suggestIdentityFacts', () => {
  it('propose les faits sur l’utilisateur, ignore le reste', () => {
    m.storeFact({ instance: koda.assistant_instance_id, content: 'Neto Pompeu préfère les réponses en français', category: 'preference' })
    m.storeFact({ instance: koda.assistant_instance_id, content: 'Le build du projet X utilise make release-x', category: 'procedure' })
    m.storeFact({ instance: koda.assistant_instance_id, content: 'L’email de Néto est contact arobase primo' })

    const candidates = m.suggestIdentityFacts(koda.assistant_instance_id)
    const texts = candidates.map(c => c.content)
    expect(texts.some(t => t.includes('français'))).toBe(true)
    expect(texts.some(t => t.includes('email'))).toBe(true)
    expect(texts.some(t => t.includes('make release-x'))).toBe(false)
  })
})

describe('listScopesWithAccess', () => {
  it('liste les scopes avec leurs lecteurs et le nb de faits', () => {
    const f = m.storeFact({ instance: koda.assistant_instance_id, content: 'fait à partager vers user' })
    m.shareFacts([f.id], 'user')
    const scopes = m.listScopesWithAccess()
    const user = scopes.find(s => s.name === 'user')!
    expect(user.facts).toBe(1)
    expect(user.readers).toContain(koda.assistant_id)
    expect(user.readers).toContain(claude.assistant_id)
  })
})
