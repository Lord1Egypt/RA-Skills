/**
 * Synchro incrément 1 — provenance & convergence LWW (offline, sans réseau).
 * winner() pur + contentHash + applyDelta idempotent/convergent + tombstones
 * + provenance posée par storeFact sur les scopes partagés.
 */
import { mkdtempSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { afterEach, beforeEach, describe, expect, it } from 'vitest'
import { ContentStore, Memoria, applyDelta, contentHash, winner, type SyncFact } from '../src/index.js'

describe('winner (LWW déterministe)', () => {
  const base = { updated_at: '2026-06-11T10:00:00.000Z', origin_machine_id: 'a', origin_rev: 1 }
  it('aucun local → apply', () => {
    expect(winner(undefined, base)).toBe('apply')
  })
  it('révision plus haute gagne', () => {
    expect(winner({ ...base, origin_rev: 1 }, { ...base, origin_rev: 2 })).toBe('apply')
    expect(winner({ ...base, origin_rev: 3 }, { ...base, origin_rev: 2 })).toBe('skip')
  })
  it('à révision égale, date la plus récente gagne', () => {
    expect(winner({ ...base, updated_at: '2026-06-11T09:00:00.000Z' }, base)).toBe('apply')
    expect(winner({ ...base, updated_at: '2026-06-11T11:00:00.000Z' }, base)).toBe('skip')
  })
  it('à égalité parfaite de rev+date, machine_id le plus grand gagne (tie-break stable)', () => {
    expect(winner({ ...base, origin_machine_id: 'a' }, { ...base, origin_machine_id: 'b' })).toBe('apply')
    expect(winner({ ...base, origin_machine_id: 'z' }, { ...base, origin_machine_id: 'b' })).toBe('skip')
  })
  it('strictement identique → skip (anti ping-pong)', () => {
    expect(winner(base, base)).toBe('skip')
  })
})

describe('contentHash', () => {
  it('même contenu normalisé → même hash ; scope différent → différent', () => {
    const a = contentHash({ fact: 'Le mot de passe NAS est X', category: 'secret', scope_id: 's1' })
    const b = contentHash({ fact: 'le  mot de passe nas est x', category: 'secret', scope_id: 's1' })
    const c = contentHash({ fact: 'Le mot de passe NAS est X', category: 'secret', scope_id: 's2' })
    expect(a).toBe(b)
    expect(a).not.toBe(c)
  })
})

function syncFact(over: Partial<SyncFact>): SyncFact {
  return {
    id: 'f1', fact: 'fait', category: 'general', fact_type: 'statement', confidence: 0.8, source: 'sync',
    scope_id: 'org', sensitivity: 'normal', visibility: 'shared', tags: '[]', entity_ids: '[]',
    lifecycle_state: 'active', superseded: 0, superseded_by: null,
    origin_machine_id: 'a', origin_rev: 1, content_hash: null, deleted_at: null,
    created_at: '2026-06-11T10:00:00.000Z', updated_at: '2026-06-11T10:00:00.000Z', ...over,
  }
}

describe('applyDelta (convergence)', () => {
  let dir: string
  let store: ContentStore
  beforeEach(() => {
    dir = mkdtempSync(join(tmpdir(), 'memoria-merge-'))
    store = new ContentStore(join(dir, 'c.sqlite'))
  })
  afterEach(() => {
    store.close()
    rmSync(dir, { recursive: true, force: true })
  })

  it('appliquer les mêmes ops dans 2 ordres → état final identique', () => {
    const ops: SyncFact[] = [
      syncFact({ id: 'f1', fact: 'v1', origin_rev: 1 }),
      syncFact({ id: 'f1', fact: 'v2', origin_rev: 2 }),
      syncFact({ id: 'f1', fact: 'v3', origin_rev: 2, origin_machine_id: 'z' }), // gagne sur tie-break machine
      syncFact({ id: 'f2', fact: 'autre', origin_rev: 1 }),
    ]
    applyDelta(store, ops, [])
    const a = store.getFact('f1')!.fact
    const a2 = store.getFact('f2')!.fact

    // 2e magasin, ordre inversé
    const store2 = new ContentStore(join(dir, 'c2.sqlite'))
    applyDelta(store2, [...ops].reverse(), [])
    expect(store2.getFact('f1')!.fact).toBe(a)
    expect(store2.getFact('f2')!.fact).toBe(a2)
    expect(a).toBe('v3') // le plus haut rev, tie-break machine 'z'
    store2.close()
  })

  it('idempotent : ré-appliquer le même delta = no-op', () => {
    const ops = [syncFact({ id: 'f1', origin_rev: 5 })]
    const r1 = applyDelta(store, ops, [])
    const r2 = applyDelta(store, ops, [])
    expect(r1.applied).toBe(1)
    expect(r2.applied).toBe(0)
    expect(r2.skipped_lww).toBe(1)
  })

  it('dédup par content_hash : même contenu sous un autre UUID est ignoré', () => {
    const h = contentHash({ fact: 'secret partagé', category: 'general', scope_id: 'org' })
    applyDelta(store, [syncFact({ id: 'f1', fact: 'secret partagé', content_hash: h })], [])
    const r = applyDelta(store, [syncFact({ id: 'f2-other-uuid', fact: 'secret partagé', content_hash: h })], [])
    expect(r.deduped).toBe(1)
    expect(store.getFact('f2-other-uuid')).toBeNull()
  })

  it('tombstone applique et ne ressuscite pas', () => {
    applyDelta(store, [syncFact({ id: 'f1', origin_rev: 1 })], [])
    const r = applyDelta(store, [], [{ id: 'f1', deleted_at: '2026-06-11T12:00:00.000Z', origin_machine_id: 'a', origin_rev: 2, updated_at: '2026-06-11T12:00:00.000Z' }])
    expect(r.tombstoned).toBe(1)
    // une ré-émission de l'ancien fait (rev plus bas) ne ressuscite pas
    const r2 = applyDelta(store, [syncFact({ id: 'f1', origin_rev: 1 })], [])
    expect(r2.applied).toBe(0)
    expect(store.getMergeFields('f1')).toBeDefined()
  })
})

describe('provenance posée par storeFact', () => {
  let dir: string
  let m: Memoria
  beforeEach(() => {
    dir = mkdtempSync(join(tmpdir(), 'memoria-prov-'))
    m = Memoria.init({ storageRoot: join(dir, 'data'), configPath: join(dir, 'config.toml'), llm: { extraction: null } })
  })
  afterEach(() => {
    m.close()
    rmSync(dir, { recursive: true, force: true })
  })

  it('un fait sur un scope PARTAGÉ porte origine + rev + hash ; un fait privé non', () => {
    const a = m.pairAssistant({ type: 'claude-code' })

    // PRIVÉ : pas de provenance (jamais synchronisé)
    const priv = m.storeFact({ instance: a.assistant_instance_id, content: 'note strictement privée' })
    expect(priv.origin_machine_id ?? null).toBeNull()
    expect(priv.origin_rev ?? 0).toBe(0)
    expect(priv.content_hash ?? null).toBeNull()

    // PARTAGÉ (scope org) : provenance posée
    const own = m.registry.ownCompany()!
    const orgScope = m.registry.getScopeByName(`org:${own.id}`)!
    m.setScopeAccess(a.assistant_id, orgScope.id, { can_read: true, can_write: true })
    const f1 = m.storeFact({ instance: a.assistant_instance_id, scope: orgScope.id, content: 'ligne de commande de déploiement bureau-primobot' })
    const f2 = m.storeFact({ instance: a.assistant_instance_id, scope: orgScope.id, content: 'autre fait partagé' })
    expect(f1.origin_machine_id).toBeTruthy()
    expect(f1.content_hash).toBeTruthy()
    expect(f1.origin_rev).toBeGreaterThan(0)
    // la révision logique est monotone croissante entre deux écritures partagées
    expect((f2.origin_rev ?? 0)).toBeGreaterThan(f1.origin_rev ?? 0)
    // même machine sur les deux
    expect(f2.origin_machine_id).toBe(f1.origin_machine_id)
  })
})
