/**
 * Couches cognitives bucket B (async, spec §12) — graphe entités/relations,
 * observations, expansion gouvernée au recall, decay, et import legacy.
 *
 * Garanties prouvées ici (pas juste « ça compile ») :
 *  - processFact peuple entités/relations/observations ET est IDEMPOTENT ;
 *  - expandEntities RESPECTE les scopes autorisés (anti-fuite via graphe = 0) ;
 *  - decay affaiblit/élague selon le temps ;
 *  - importLegacyCognition ramène les bons counts, idempotent.
 *
 * Tout est sans réseau (provider factice), DB en tmpdir.
 */
import Database from 'better-sqlite3'
import { mkdtempSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { afterEach, beforeEach, describe, expect, it } from 'vitest'
import { ContentStore } from '../src/storage/content.js'
import { CognitionEngine } from '../src/cognition/index.js'
import { applyDecay, expandByEntities } from '../src/cognition/graph.js'
import { ensureCognitionSchema } from '../src/storage/cognition-schema.js'
import { importLegacyCognition } from '../src/migration/import-cognition.js'
import type { LlmProvider } from '../src/llm/provider.js'

let dir: string
let store: ContentStore

beforeEach(() => {
  dir = mkdtempSync(join(tmpdir(), 'memoria-cognition-'))
  store = new ContentStore(join(dir, 'content.sqlite'))
})

afterEach(() => {
  store.close()
  rmSync(dir, { recursive: true, force: true })
})

/** Provider LLM factice : renvoie un JSON {entities, relations} déterministe. */
class FakeGraphLlm implements LlmProvider {
  readonly name = 'fake-graph'
  readonly model = 'fake'
  constructor(private readonly payload: unknown) {}
  isAvailable(): Promise<boolean> {
    return Promise.resolve(true)
  }
  complete(): Promise<string> {
    return Promise.resolve(JSON.stringify(this.payload))
  }
}

function countEntities(s: ContentStore): number {
  return (s.db.prepare('SELECT COUNT(*) AS c FROM entities').get() as { c: number }).c
}
function countRelations(s: ContentStore): number {
  return (s.db.prepare('SELECT COUNT(*) AS c FROM relations').get() as { c: number }).c
}

describe('CognitionEngine.processFact', () => {
  it('peuple entités, relations et observation depuis UN fait (heuristique, sans LLM)', async () => {
    const fact = store.insertFact({
      fact: 'Le projet PixConsent utilise Firebase pour la synchronisation Team',
      category: 'config',
      scope_id: 's1',
    })
    const engine = new CognitionEngine({ store })
    const r = await engine.processFact(fact.id)

    expect(r.processed).toBe(true)
    expect(r.via).toBe('heuristic')
    // PixConsent (CamelCase) + Firebase + Team + Le-projet-… → plusieurs entités
    expect(r.entities).toBeGreaterThanOrEqual(2)
    expect(countEntities(store)).toBe(r.entities)
    // ≥2 entités co-occurrentes → au moins une relation de co-occurrence
    expect(countRelations(store)).toBeGreaterThanOrEqual(1)
    // une observation agrégée a été créée pour ce fait
    expect(r.observation_created).toBe(true)
    expect((store.db.prepare('SELECT COUNT(*) AS c FROM observations').get() as { c: number }).c).toBe(1)
    // le lien fact↔entité existe (table de jointure, pas le LIKE)
    const links = store.db.prepare('SELECT COUNT(*) AS c FROM fact_entities WHERE fact_id = ?').get(fact.id) as {
      c: number
    }
    expect(links.c).toBe(r.entities)
  })

  it('utilise le LLM injecté quand disponible (relations typées)', async () => {
    const fact = store.insertFact({ fact: 'Igara dépend de IgaraKit', category: 'config', scope_id: 's1' })
    const llm = new FakeGraphLlm({
      entities: [
        { name: 'Igara', type: 'project' },
        { name: 'IgaraKit', type: 'tool' },
      ],
      relations: [{ from: 'Igara', to: 'IgaraKit', type: 'depends_on' }],
    })
    const engine = new CognitionEngine({ store, llm })
    const r = await engine.processFact(fact.id)
    expect(r.via).toBe('llm')
    expect(r.entities).toBe(2)
    // 1 relation typée depends_on + co-occurrence sur la même paire = 1 ligne
    expect(countRelations(store)).toBe(1)
    const rel = store.db.prepare('SELECT kind FROM relations').get() as { kind: string }
    expect(rel.kind).toBe('depends_on')
  })

  it('est IDEMPOTENT : re-process ne duplique ni entités ni relations', async () => {
    const fact = store.insertFact({
      fact: 'AutoCare cible le marché Brésil avec Firebase',
      category: 'decision',
      scope_id: 's1',
    })
    const engine = new CognitionEngine({ store })
    const first = await engine.processFact(fact.id)
    const e1 = countEntities(store)
    const rel1 = countRelations(store)
    const obs1 = (store.db.prepare('SELECT COUNT(*) AS c FROM observations').get() as { c: number }).c

    const second = await engine.processFact(fact.id)
    expect(countEntities(store)).toBe(e1) // pas de nouvelle entité
    expect(countRelations(store)).toBe(rel1) // pas de nouvelle relation (renforcée)
    expect((store.db.prepare('SELECT COUNT(*) AS c FROM observations').get() as { c: number }).c).toBe(obs1)
    expect(second.observation_created).toBe(false)
    expect(first.entities).toBe(e1)

    // mention_count a été incrémenté (renforcement), pas dupliqué
    const mentions = store.db.prepare('SELECT MAX(mention_count) AS m FROM entities').get() as { m: number }
    expect(mentions.m).toBeGreaterThanOrEqual(2)
    // le poids de la relation a augmenté au re-process (cap 1.0 jamais dépassé)
    const w = store.db.prepare('SELECT MAX(weight) AS w FROM relations').get() as { w: number }
    expect(w.w).toBeGreaterThan(0.5)
    expect(w.w).toBeLessThanOrEqual(1.0)
  })

  it('no-op annoncé sur fait inexistant (pas de throw, processed=false)', async () => {
    const engine = new CognitionEngine({ store })
    const r = await engine.processFact('inexistant')
    expect(r.processed).toBe(false)
    expect(r.entities).toBe(0)
  })

  it('bascule sur heuristique si le LLM throw (jamais de mort silencieuse)', async () => {
    const fact = store.insertFact({ fact: 'Le NAS QNAP héberge les sauvegardes', category: 'outil', scope_id: 's1' })
    const llm: LlmProvider = {
      name: 'broken',
      model: 'x',
      isAvailable: () => Promise.resolve(true),
      complete: () => Promise.reject(new Error('boom')),
    }
    const engine = new CognitionEngine({ store, llm })
    const r = await engine.processFact(fact.id)
    expect(r.processed).toBe(true)
    expect(r.via).toBe('heuristic')
    expect(r.entities).toBeGreaterThanOrEqual(1) // NAS/QNAP détectés en ALLCAPS
  })
})

describe('CognitionEngine.expandEntities (anti-fuite par scope)', () => {
  it('respecte STRICTEMENT les scopes autorisés : un fait hors scope n’est jamais remonté', async () => {
    // Entité partagée « Acme » entre clientA et clientB (collision réaliste).
    const a1 = store.insertFact({ fact: 'Le client Acme déploie sur Vercel', category: 'client', scope_id: 'clientA' })
    const a2 = store.insertFact({ fact: 'Acme préfère les builds Vercel signés', category: 'client', scope_id: 'clientA' })
    const b1 = store.insertFact({ fact: 'Acme veut un audit Vercel mensuel', category: 'client', scope_id: 'clientB' })

    const engine = new CognitionEngine({ store })
    await engine.processFact(a1.id)
    await engine.processFact(a2.id)
    await engine.processFact(b1.id)

    // Expansion depuis a1, autorisée UNIQUEMENT sur clientA :
    const fromA = engine.expandEntities([a1.id], ['clientA'])
    const idsA = fromA.map(r => r.fact_id)
    // a2 (même scope, entités partagées) peut remonter ; b1 (clientB) JAMAIS.
    expect(idsA).not.toContain(b1.id)
    expect(idsA.every(id => id === a2.id)).toBe(true)

    // Expansion depuis b1, autorisée UNIQUEMENT sur clientB :
    const fromB = engine.expandEntities([b1.id], ['clientB'])
    const idsB = fromB.map(r => r.fact_id)
    // aucun fait de clientA ne fuit dans le contexte clientB
    expect(idsB).not.toContain(a1.id)
    expect(idsB).not.toContain(a2.id)
  })

  it('un germe hors scope autorisé ne sert même pas de point de départ', async () => {
    const a1 = store.insertFact({ fact: 'Bureau utilise Convex et Qonto', category: 'outil', scope_id: 'clientA' })
    const a2 = store.insertFact({ fact: 'Convex pilote le CRM Bureau', category: 'outil', scope_id: 'clientA' })
    const engine = new CognitionEngine({ store })
    await engine.processFact(a1.id)
    await engine.processFact(a2.id)

    // On tente de partir de a1 mais on n'autorise QUE clientB → aucun germe valide.
    const out = engine.expandEntities([a1.id], ['clientB'])
    expect(out).toHaveLength(0)
  })

  it('exclut les faits superseded de l’expansion (filtre dur, pas de status)', async () => {
    const f1 = store.insertFact({ fact: 'JamBoard utilise Firebase Auth', category: 'config', scope_id: 's1' })
    const f2 = store.insertFact({ fact: 'Firebase Auth gère JamBoard SIWA', category: 'config', scope_id: 's1' })
    const engine = new CognitionEngine({ store })
    await engine.processFact(f1.id)
    await engine.processFact(f2.id)
    // f2 superseded → exclu de l'ensemble autorisé
    store.db.prepare('UPDATE facts SET superseded = 1 WHERE id = ?').run(f2.id)

    const out = engine.expandEntities([f1.id], ['s1'])
    expect(out.map(r => r.fact_id)).not.toContain(f2.id)
  })

  it('expandByEntities (bas niveau) ne remonte jamais hors de allowedFactIds', async () => {
    const f1 = store.insertFact({ fact: 'Memoria utilise SQLite et FTS5', category: 'config', scope_id: 's1' })
    const f2 = store.insertFact({ fact: 'SQLite porte FTS5 dans Memoria', category: 'config', scope_id: 's1' })
    const engine = new CognitionEngine({ store })
    await engine.processFact(f1.id)
    await engine.processFact(f2.id)
    // allowedFactIds délibérément vide pour f2 → expansion interdite de le remonter
    const allowed = new Set([f1.id])
    const out = expandByEntities(store.db, [f1.id], allowed)
    expect(out.map(r => r.fact_id)).not.toContain(f2.id)
  })
})

describe('decay du graphe (GE-2 — branché et testable)', () => {
  it('affaiblit selon le temps, élague sous le seuil, laisse intact ce qui est récent', async () => {
    // Trois entités pour fabriquer des relations contrôlées.
    ensureCognitionSchema(store.db) // schéma appliqué (pas d'engine ici)
    const now = Date.parse('2026-06-10T12:00:00.000Z')
    store.db
      .prepare('INSERT INTO entities (id, name, type, mention_count, created_at) VALUES (?,?,?,?,?)')
      .run('e1', 'Alpha', 'concept', 1, new Date(now).toISOString())
    store.db
      .prepare('INSERT INTO entities (id, name, type, mention_count, created_at) VALUES (?,?,?,?,?)')
      .run('e2', 'Beta', 'concept', 1, new Date(now).toISOString())
    store.db
      .prepare('INSERT INTO entities (id, name, type, mention_count, created_at) VALUES (?,?,?,?,?)')
      .run('e3', 'Gamma', 'concept', 1, new Date(now).toISOString())

    const insertRel = store.db.prepare(
      `INSERT INTO relations (id, from_entity, to_entity, kind, weight, context, created_at, last_accessed_at)
       VALUES (?,?,?,?,?,?,?,?)`,
    )
    const old100 = new Date(now - 100 * 86_400_000).toISOString()
    const old200 = new Date(now - 200 * 86_400_000).toISOString()
    const today = new Date(now).toISOString()
    // Relation accédée il y a 100j, poids 0.5 → ≈ 0.5 × 0.995^100 ≈ 0.30
    insertRel.run('r1', 'e1', 'e2', 'related_to', 0.5, '[]', old100, old100)
    // Relation faible (0.06) très vieille → élaguée
    insertRel.run('r2', 'e1', 'e3', 'related_to', 0.06, '[]', old200, old200)
    // Relation accédée aujourd'hui → inchangée
    insertRel.run('r3', 'e2', 'e3', 'related_to', 0.8, '[]', today, today)

    const result = applyDecay(store.db, undefined, now)
    expect(result.pruned).toBe(1)

    const r1 = store.db.prepare('SELECT weight FROM relations WHERE id = ?').get('r1') as { weight: number } | undefined
    expect(r1).toBeDefined()
    expect(r1!.weight).toBeGreaterThan(0.28)
    expect(r1!.weight).toBeLessThan(0.32)

    const r2 = store.db.prepare('SELECT weight FROM relations WHERE id = ?').get('r2')
    expect(r2).toBeUndefined() // élaguée

    const r3 = store.db.prepare('SELECT weight FROM relations WHERE id = ?').get('r3') as { weight: number }
    expect(r3.weight).toBeCloseTo(0.8, 5) // intacte
  })

  it('onFactSuperseded retire le fait du graphe et nettoie les jointures', async () => {
    const f1 = store.insertFact({ fact: 'Stripe paie Primask en mode live', category: 'config', scope_id: 's1' })
    const engine = new CognitionEngine({ store })
    await engine.processFact(f1.id)
    const linksBefore = (
      store.db.prepare('SELECT COUNT(*) AS c FROM fact_entities WHERE fact_id = ?').get(f1.id) as { c: number }
    ).c
    expect(linksBefore).toBeGreaterThan(0)

    engine.onFactSuperseded(f1.id)
    const linksAfter = (
      store.db.prepare('SELECT COUNT(*) AS c FROM fact_entities WHERE fact_id = ?').get(f1.id) as { c: number }
    ).c
    expect(linksAfter).toBe(0)
    // idempotent : rappeler ne casse rien
    expect(() => engine.onFactSuperseded(f1.id)).not.toThrow()
  })
})

// ---------------------------------------------------------------------------
// Import des couches cognitives legacy v3.34
// ---------------------------------------------------------------------------

/** Mini DB legacy v3.34 avec entities/relations/observations/self_observations/topics. */
function createLegacyCognitionDb(path: string): {
  entities: number
  relations: number
  observations: number
  selfObservations: number
  topics: number
} {
  const db = new Database(path)
  try {
    db.exec(`
      CREATE TABLE entities (
        id TEXT PRIMARY KEY, name TEXT NOT NULL, type TEXT NOT NULL DEFAULT 'concept',
        attributes TEXT DEFAULT '{}', created_at INTEGER NOT NULL, access_count INTEGER DEFAULT 0
      );
      CREATE TABLE relations (
        id TEXT PRIMARY KEY, source_id TEXT NOT NULL, target_id TEXT NOT NULL,
        relation TEXT NOT NULL, weight REAL DEFAULT 1.0, context TEXT,
        created_at INTEGER NOT NULL, last_accessed_at INTEGER
      );
      CREATE TABLE observations (
        id TEXT PRIMARY KEY, topic TEXT NOT NULL, summary TEXT NOT NULL,
        evidence_ids TEXT DEFAULT '[]', revision INTEGER DEFAULT 1, confidence REAL DEFAULT 0.8,
        created_at INTEGER NOT NULL, updated_at INTEGER NOT NULL,
        last_accessed_at INTEGER, access_count INTEGER DEFAULT 0, embedding BLOB
      );
      CREATE TABLE self_observations (
        id INTEGER PRIMARY KEY AUTOINCREMENT, domain TEXT NOT NULL,
        signal TEXT NOT NULL CHECK(signal IN ('success','correction','frustration','retry')),
        detail TEXT NOT NULL DEFAULT '', created_at INTEGER NOT NULL
      );
      CREATE TABLE topics (
        id TEXT PRIMARY KEY, name TEXT NOT NULL, keywords TEXT DEFAULT '[]',
        fact_count INTEGER DEFAULT 0, first_seen INTEGER NOT NULL, last_seen INTEGER NOT NULL,
        access_count INTEGER DEFAULT 0, importance_score REAL DEFAULT 0.0
      );
    `)
    const base = Date.parse('2026-01-15T10:00:00.000Z')
    const ents = [
      ['ent_neto', 'Néto', 'person'],
      ['ent_pix', 'PixConsent', 'project'],
      ['ent_fire', 'Firebase', 'tool'],
      ['ent_vercel', 'Vercel', 'tool'],
    ]
    const ie = db.prepare(
      'INSERT INTO entities (id, name, type, attributes, created_at, access_count) VALUES (?,?,?,?,?,?)',
    )
    for (const [i, [id, name, type]] of ents.entries()) ie.run(id, name, type, '{}', base, i)
    const rels: Array<[string, string, string, string, number]> = [
      ['r1', 'ent_neto', 'ent_pix', 'works_on', 0.7],
      ['r2', 'ent_pix', 'ent_fire', 'uses', 0.9],
      // doublon dans l'autre sens (la fusion non-dirigée doit le réconcilier) :
      ['r3', 'ent_fire', 'ent_pix', 'uses', 0.4],
    ]
    const ir = db.prepare(
      'INSERT INTO relations (id, source_id, target_id, relation, weight, context, created_at, last_accessed_at) VALUES (?,?,?,?,?,?,?,?)',
    )
    for (const [id, s, t, rel, w] of rels) ir.run(id, s, t, rel, w, '["fact_x"]', base, base)
    const obs: Array<[string, string, string]> = [
      ['obs1', 'PixConsent deploy', 'PixConsent se déploie via Vercel et stocke sur Firebase'],
      ['obs2', 'Néto préférences', 'Néto préfère les commits signés et le français'],
    ]
    const io = db.prepare(
      'INSERT INTO observations (id, topic, summary, evidence_ids, revision, confidence, created_at, updated_at) VALUES (?,?,?,?,?,?,?,?)',
    )
    for (const [id, topic, summary] of obs) io.run(id, topic, summary, '[]', 2, 0.85, base, base)
    const iso = db.prepare(
      'INSERT INTO self_observations (domain, signal, detail, created_at) VALUES (?,?,?,?)',
    )
    iso.run('build', 'success', 'build Vercel vert', base)
    iso.run('build', 'correction', 'cache npm corrompu corrigé', base)
    iso.run('recall', 'frustration', 'fait introuvable', base)
    const it = db.prepare(
      'INSERT INTO topics (id, name, keywords, fact_count, first_seen, last_seen, importance_score) VALUES (?,?,?,?,?,?,?)',
    )
    it.run('top1', 'Déploiement', '["vercel","firebase"]', 5, base, base, 0.9)
    it.run('top2', 'Préférences Néto', '["fr","commits"]', 3, base, base, 0.7)
    return { entities: ents.length, relations: rels.length, observations: obs.length, selfObservations: 3, topics: 2 }
  } finally {
    db.close()
  }
}

describe('importLegacyCognition', () => {
  it('ramène les bons counts (entités/relations/observations/self-obs/topics)', () => {
    const legacyPath = join(dir, 'legacy-cognition.sqlite')
    const summary = createLegacyCognitionDb(legacyPath)
    const legacyDb = new Database(legacyPath, { readonly: true })

    const report = importLegacyCognition({ legacyDb, targetStore: store, scopeId: 'legacy_to_review' })
    legacyDb.close()

    expect(report.errors).toEqual([])
    // 4 entités distinctes
    expect(report.entities_read).toBe(summary.entities)
    expect(report.entities_imported).toBe(4)
    expect(countEntities(store)).toBe(4)

    // 3 relations legacy mais r2 et r3 = MÊME paire non-dirigée (pix↔fire) →
    // 2 lignes en cible (neto-pix, pix-fire), une fusionnée.
    expect(report.relations_read).toBe(summary.relations)
    expect(report.relations_imported).toBe(2)
    expect(report.relations_skipped).toBe(1)
    expect(countRelations(store)).toBe(2)

    // observations (2) + self_observations (3 signaux distincts) = 5 observations
    expect(report.observations_read).toBe(summary.observations)
    expect(report.self_observations_read).toBe(summary.selfObservations)
    expect(report.observations_imported).toBe(5)
    expect((store.db.prepare('SELECT COUNT(*) AS c FROM observations').get() as { c: number }).c).toBe(5)

    // topics
    expect(report.topics_read).toBe(summary.topics)
    expect(report.topics_imported).toBe(2)
    expect((store.db.prepare('SELECT COUNT(*) AS c FROM topics').get() as { c: number }).c).toBe(2)

    // la fusion non-dirigée a retenu le poids le plus fort (0.9) pour pix↔fire
    const w = store.db.prepare('SELECT MAX(weight) AS w FROM relations').get() as { w: number }
    expect(w.w).toBeCloseTo(0.9, 5)
  })

  it('est IDEMPOTENT : ré-importer la même DB ne duplique rien', () => {
    const legacyPath = join(dir, 'legacy-cognition2.sqlite')
    createLegacyCognitionDb(legacyPath)

    const first = importLegacyCognition({
      legacyDb: new Database(legacyPath, { readonly: true }),
      targetStore: store,
      scopeId: 'legacy_to_review',
    })
    expect(first.entities_imported).toBe(4)

    const eAfter1 = countEntities(store)
    const relAfter1 = countRelations(store)
    const obsAfter1 = (store.db.prepare('SELECT COUNT(*) AS c FROM observations').get() as { c: number }).c
    const topAfter1 = (store.db.prepare('SELECT COUNT(*) AS c FROM topics').get() as { c: number }).c

    const second = importLegacyCognition({
      legacyDb: new Database(legacyPath, { readonly: true }),
      targetStore: store,
      scopeId: 'legacy_to_review',
    })
    // Tout est reconnu comme déjà présent → 0 nouvel insert.
    expect(second.entities_imported).toBe(0)
    expect(second.relations_imported).toBe(0)
    expect(second.observations_imported).toBe(0)
    expect(second.topics_imported).toBe(0)

    expect(countEntities(store)).toBe(eAfter1)
    expect(countRelations(store)).toBe(relAfter1)
    expect((store.db.prepare('SELECT COUNT(*) AS c FROM observations').get() as { c: number }).c).toBe(obsAfter1)
    expect((store.db.prepare('SELECT COUNT(*) AS c FROM topics').get() as { c: number }).c).toBe(topAfter1)
  })

  it('tolère un schéma legacy partiel (table relations absente)', () => {
    const legacyPath = join(dir, 'legacy-partial.sqlite')
    const db = new Database(legacyPath)
    db.exec(`
      CREATE TABLE entities (id TEXT PRIMARY KEY, name TEXT NOT NULL, type TEXT DEFAULT 'concept', created_at INTEGER NOT NULL);
      CREATE TABLE observations (id TEXT PRIMARY KEY, topic TEXT NOT NULL, summary TEXT NOT NULL, created_at INTEGER NOT NULL, updated_at INTEGER NOT NULL);
    `)
    const base = Date.parse('2026-01-15T10:00:00.000Z')
    db.prepare('INSERT INTO entities (id, name, type, created_at) VALUES (?,?,?,?)').run('e1', 'Solo', 'project', base)
    db.prepare('INSERT INTO observations (id, topic, summary, created_at, updated_at) VALUES (?,?,?,?,?)').run(
      'o1',
      'sujet',
      'contenu de test',
      base,
      base,
    )
    db.close()

    const report = importLegacyCognition({
      legacyDb: new Database(legacyPath, { readonly: true }),
      targetStore: store,
      scopeId: 'legacy_to_review',
    })
    expect(report.errors).toEqual([])
    expect(report.entities_imported).toBe(1)
    expect(report.relations_read).toBe(0) // table absente → 0, pas d'erreur
    expect(report.observations_imported).toBe(1)
  })
})
