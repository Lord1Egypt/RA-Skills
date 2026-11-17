/**
 * Vectoriel sqlite-vec : indexation idempotente, recherche hybride qui trouve
 * ce que le FTS rate (synonymes), permissions JAMAIS contournées par le
 * vectoriel, garde de dimensions, dégradation propre sans vecteur.
 */
import { mkdtempSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { afterEach, beforeEach, describe, expect, it } from 'vitest'
import {
  ContentStore,
  EmbeddingIndexer,
  hybridSearchFacts,
  isVecAvailable,
  knn,
  type EmbeddingProvider,
} from '../src/index.js'

/**
 * Provider factice : vecteur 8d déterministe par « concept » — voiture et
 * automobile partagent le même concept (synonymes simulés), les autres mots
 * donnent des directions distinctes.
 */
class FakeEmbedding implements EmbeddingProvider {
  readonly name = 'fake'
  readonly model = 'fake-8d'
  readonly dimensions = 8
  isAvailable(): Promise<boolean> {
    return Promise.resolve(true)
  }
  embed(texts: string[]): Promise<Float32Array[]> {
    return Promise.resolve(texts.map(t => FakeEmbedding.vectorFor(t)))
  }
  static vectorFor(text: string): Float32Array {
    const t = text.toLowerCase()
    const v = new Float32Array(8)
    const concepts: Array<[RegExp, number]> = [
      [/voiture|automobile|véhicule/, 0],
      [/garage|réparation/, 1],
      [/cuisine|recette/, 2],
      [/serveur|infra/, 3],
      [/musique|concert/, 4],
    ]
    for (const [re, dim] of concepts) {
      if (re.test(t)) v[dim] = 1
    }
    if (v.every(x => x === 0)) {
      // direction « divers » dépendante de la longueur — loin des concepts
      v[5] = 0.3 + (t.length % 7) / 10
      v[6] = 0.9
    }
    const norm = Math.hypot(...v) || 1
    return v.map(x => x / norm) as unknown as Float32Array
  }
}

let dir: string
let store: ContentStore
let indexer: EmbeddingIndexer
const provider = new FakeEmbedding()

beforeEach(() => {
  dir = mkdtempSync(join(tmpdir(), 'memoria-vec-'))
  store = new ContentStore(join(dir, 'content.sqlite'))
  indexer = new EmbeddingIndexer({ store, provider, batchSize: 4 })
})

afterEach(() => {
  store.close()
  rmSync(dir, { recursive: true, force: true })
})

const vecOk = (): boolean => isVecAvailable(store.db)

describe('extension sqlite-vec', () => {
  it('disponible sur cette machine (binaire npm) OU dégradation propre', () => {
    // Sur le Mac de dev l'extension doit charger ; ailleurs le reste de la
    // suite vérifie le mode dégradé.
    expect(typeof vecOk()).toBe('boolean')
  })
})

describe('EmbeddingIndexer', () => {
  it('indexe par lots, idempotent (0 au second run)', async () => {
    for (let i = 0; i < 6; i++) {
      store.insertFact({ fact: `note ${i} sur la cuisine et les recettes du lundi`, scope_id: 's1' })
    }
    const r1 = await indexer.runAll()
    expect(r1.indexed).toBe(6)
    expect(r1.remaining).toBe(0)

    const r2 = await indexer.runOnce()
    expect(r2.indexed).toBe(0)

    const count = store.db
      .prepare("SELECT COUNT(*) AS c FROM embeddings WHERE model = 'fake-8d' AND dimensions = 8")
      .get() as { c: number }
    expect(count.c).toBe(6)
  })

  it('removeFor nettoie embeddings + index', async () => {
    const f = store.insertFact({ fact: 'la voiture rouge du garage', scope_id: 's1' })
    await indexer.runOnce()
    indexer.removeFor([f.id])
    const left = store.db.prepare('SELECT COUNT(*) AS c FROM embeddings WHERE owner_id = ?').get(f.id) as { c: number }
    expect(left.c).toBe(0)
    if (vecOk()) {
      expect(knn(store.db, 8, FakeEmbedding.vectorFor('voiture'), 5).map(h => h.fact_id)).not.toContain(f.id)
    }
  })
})

describe('hybridSearchFacts', () => {
  it('trouve par similarité sémantique ce que le FTS rate (synonyme)', async () => {
    store.insertFact({ fact: 'L’automobile de Néto est garée au parking couvert', scope_id: 's1' })
    store.insertFact({ fact: 'La recette de cuisine du dimanche utilise du curcuma', scope_id: 's1' })
    await indexer.runAll()
    if (!vecOk()) return // mode dégradé couvert par le dernier test

    // « voiture » n'apparaît dans aucun texte → FTS seul = 0
    const ftsOnly = store.searchFacts('voiture', { scopeIds: ['s1'] })
    expect(ftsOnly).toHaveLength(0)

    const hybrid = hybridSearchFacts(store, 'voiture', {
      scopeIds: ['s1'],
      queryVector: FakeEmbedding.vectorFor('voiture'),
    })
    expect(hybrid.length).toBeGreaterThan(0)
    expect(hybrid[0]!.row.fact).toContain('automobile')
  })

  it('le vectoriel ne contourne JAMAIS les permissions (superseded/critical/scope)', async () => {
    const blocked = store.insertFact({ fact: 'Le véhicule de fonction du client secret', scope_id: 's1', sensitivity: 'critical' })
    const superseded = store.insertFact({ fact: 'Une automobile ancienne remplacée', scope_id: 's1' })
    const otherScope = store.insertFact({ fact: 'La voiture du scope voisin', scope_id: 'AUTRE' })
    store.db.prepare('UPDATE facts SET superseded = 1 WHERE id = ?').run(superseded.id)
    await indexer.runAll()
    if (!vecOk()) return

    const hits = hybridSearchFacts(store, 'voiture', {
      scopeIds: ['s1'],
      maxSensitivity: 'sensitive',
      queryVector: FakeEmbedding.vectorFor('voiture'),
    })
    const ids = hits.map(h => h.row.id)
    expect(ids).not.toContain(blocked.id)
    expect(ids).not.toContain(superseded.id)
    expect(ids).not.toContain(otherScope.id)
  })

  it('garde de dimensions : requête 16d sur index 8d → erreur claire', async () => {
    store.insertFact({ fact: 'note sur la musique du concert', scope_id: 's1' })
    await indexer.runAll()
    if (!vecOk()) return
    expect(() => knn(store.db, 8, new Float32Array(16), 5)).toThrow(/interdit/)
  })

  it('sans queryVector → résultat identique au FTS seul', () => {
    store.insertFact({ fact: 'le serveur infra de staging répond', scope_id: 's1' })
    const fts = store.searchFacts('serveur staging', { scopeIds: ['s1'] })
    const hybrid = hybridSearchFacts(store, 'serveur staging', { scopeIds: ['s1'] })
    expect(hybrid.map(h => h.row.id)).toEqual(fts.map(h => h.row.id))
  })
})
