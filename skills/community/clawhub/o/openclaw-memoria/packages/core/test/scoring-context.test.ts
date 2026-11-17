/**
 * Couche 2 (hot-tier) + couche 9 (context-tree).
 * - hot-tier : un fait récemment ACCÉDÉ remonte transitoirement.
 * - context-tree : déclarer un projet remonte sa hiérarchie (client + org).
 */
import { mkdtempSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { afterEach, beforeEach, describe, expect, it } from 'vitest'
import { Memoria, scoreFact, type FactRow } from '../src/index.js'

function rowOf(over: Partial<FactRow>): FactRow {
  const now = new Date().toISOString()
  return {
    id: 'f', fact: 'x', category: 'general', fact_type: 'statement', confidence: 0.8, source: 'manual',
    assistant_instance_id: null, user_id: null, org_id: null, client_org_id: null, project_id: null,
    topic_id: null, scope_id: 's', sensitivity: 'normal', visibility: 'private', tags: '[]', entity_ids: '[]',
    lifecycle_state: 'active', superseded: 0, superseded_by: null, usefulness: 0, recall_count: 0,
    used_count: 0, relevance_weight: 1, created_at: now, updated_at: now, last_accessed_at: null, ...over,
  }
}

describe('hot-tier (couche 2)', () => {
  it('un fait accédé à l’instant marque > un fait jamais accédé', () => {
    const now = Date.now()
    const cold = scoreFact(rowOf({ last_accessed_at: null }), 1, undefined, now)
    const hot = scoreFact(rowOf({ last_accessed_at: new Date(now).toISOString() }), 1, undefined, now)
    expect(hot.hot).toBeGreaterThan(cold.hot)
    expect(hot.total).toBeGreaterThan(cold.total)
  })

  it('la chaleur retombe avec le temps écoulé depuis l’accès', () => {
    const now = Date.now()
    const recent = scoreFact(rowOf({ last_accessed_at: new Date(now - 86_400_000).toISOString() }), 1, undefined, now)
    const old = scoreFact(rowOf({ last_accessed_at: new Date(now - 30 * 86_400_000).toISOString() }), 1, undefined, now)
    expect(recent.hot).toBeGreaterThan(old.hot)
  })

  it('QW4 : la pertinence domine le boost de contexte', () => {
    const now = Date.now()
    // fait TRÈS pertinent mais hors-contexte
    const relevant = scoreFact(rowOf({ project_id: null }), 1.0, { project_id: 'P' }, now)
    // fait PEU pertinent mais dans le contexte projet
    const inContext = scoreFact(rowOf({ project_id: 'P' }), 0.25, { project_id: 'P' }, now)
    expect(relevant.total).toBeGreaterThan(inContext.total)
  })
})

describe('context-tree (couche 9)', () => {
  let root: string
  let m: Memoria

  beforeEach(() => {
    root = mkdtempSync(join(tmpdir(), 'memoria-ctxtree-'))
    m = Memoria.init({ storageRoot: root, configPath: join(root, 'config.toml'), llm: { extraction: null } })
  })
  afterEach(() => {
    m.close()
    rmSync(root, { recursive: true, force: true })
  })

  it('déclarer un projet rend visibles les faits de son client (hiérarchie)', () => {
    const a = m.pairAssistant({ type: 'claude-code' })
    const own = m.registry.ownCompany()!
    const clientOrg = m.registry.createOrganization('Client Z', 'client')
    const project = m.registry.createProject('Projet Z', own.id, clientOrg.id)
    const clientScope = m.registry.ensureScope('client', 'client:z', { client_org_id: clientOrg.id })
    m.registry.setPolicy({ assistant_id: a.assistant_id, scope_id: clientScope.id, can_read: true, can_write: true, can_share: false, secret_access: 'none' })
    m.storeFact({ instance: a.assistant_instance_id, scope: clientScope.id, client_org_id: clientOrg.id, content: 'Le tarif du client Z est de 1200 euros par jour' })

    // contexte = juste le projet → son client est résolu via l'arbre → visible
    const inProject = m.recall({ instance: a.assistant_instance_id, query: 'tarif client euros', active_context: { project_id: project.id } })
    expect(inProject.items.some(i => i.content.includes('1200'))).toBe(true)

    // sans contexte → masqué (anti-fuite)
    const noCtx = m.recall({ instance: a.assistant_instance_id, query: 'tarif client euros' })
    expect(noCtx.items).toHaveLength(0)
  })
})
