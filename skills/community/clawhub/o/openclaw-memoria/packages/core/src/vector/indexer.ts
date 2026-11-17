/**
 * Indexeur d'embeddings (bucket B — async, jamais dans le chemin de réponse).
 * Vérité = table `embeddings` (model/dimensions gravés) ; l'index vec0 est
 * reconstructible. Idempotent : ne ré-embedde jamais un fait déjà couvert
 * pour CE modèle.
 */
import type { ContentStore } from '../storage/content.js'
import type { EmbeddingProvider } from '../llm/provider.js'
import { newId, nowISO, vectorToBuffer } from '../util.js'
import { ensureVecTable, removeVectors, upsertVector } from './vec-table.js'

export interface IndexerRunResult {
  indexed: number
  remaining: number
  vec_available: boolean
}

export class EmbeddingIndexer {
  private readonly store: ContentStore
  private readonly provider: EmbeddingProvider
  private readonly batchSize: number

  constructor(opts: { store: ContentStore; provider: EmbeddingProvider; batchSize?: number }) {
    this.store = opts.store
    this.provider = opts.provider
    this.batchSize = opts.batchSize ?? 16
  }

  /** Faits actifs sans embedding pour ce modèle. */
  pendingFacts(limit = this.batchSize): Array<{ id: string; fact: string }> {
    return this.store.db
      .prepare(
        `SELECT f.id, f.fact FROM facts f
         WHERE f.superseded = 0
           AND NOT EXISTS (
             SELECT 1 FROM embeddings e
             WHERE e.owner_type = 'fact' AND e.owner_id = f.id AND e.model = ?
           )
         ORDER BY f.created_at
         LIMIT ?`,
      )
      .all(this.provider.model, limit) as Array<{ id: string; fact: string }>
  }

  pendingCount(): number {
    const r = this.store.db
      .prepare(
        `SELECT COUNT(*) AS c FROM facts f
         WHERE f.superseded = 0
           AND NOT EXISTS (
             SELECT 1 FROM embeddings e
             WHERE e.owner_type = 'fact' AND e.owner_id = f.id AND e.model = ?
           )`,
      )
      .get(this.provider.model) as { c: number }
    return r.c
  }

  /**
   * Un lot : embed → table embeddings → index vec0. Erreur provider = THROW
   * (l'appelant décide : retry plus tard) — jamais d'avalement.
   */
  async runOnce(): Promise<IndexerRunResult> {
    const batch = this.pendingFacts()
    if (batch.length === 0) {
      return { indexed: 0, remaining: 0, vec_available: ensureVecTable(this.store.db, this.provider.dimensions) }
    }

    const vectors = await this.provider.embed(batch.map(f => f.fact))
    if (vectors.length !== batch.length) {
      throw new Error(`embed : ${vectors.length} vecteurs pour ${batch.length} textes`)
    }

    const vecOk = ensureVecTable(this.store.db, this.provider.dimensions)
    const insert = this.store.db.prepare(
      `INSERT OR REPLACE INTO embeddings (id, owner_type, owner_id, model, dimensions, vector, created_at)
       VALUES (?, 'fact', ?, ?, ?, ?, ?)`,
    )
    const tx = this.store.db.transaction(() => {
      for (let i = 0; i < batch.length; i++) {
        const vec = vectors[i]!
        if (vec.length !== this.provider.dimensions) {
          throw new Error(
            `embed : vecteur ${vec.length}d pour un modèle déclaré ${this.provider.dimensions}d (${this.provider.model}) — interdit`,
          )
        }
        insert.run(newId(), batch[i]!.id, this.provider.model, this.provider.dimensions, vectorToBuffer(vec), nowISO())
        if (vecOk) upsertVector(this.store.db, this.provider.dimensions, batch[i]!.id, vec)
      }
    })
    tx()

    return { indexed: batch.length, remaining: this.pendingCount(), vec_available: vecOk }
  }

  /** Boucle jusqu'à épuisement (réindexation complète, embedding_jobs). */
  async runAll(maxBatches = 1000): Promise<IndexerRunResult> {
    let last: IndexerRunResult = { indexed: 0, remaining: this.pendingCount(), vec_available: false }
    let total = 0
    for (let i = 0; i < maxBatches && (i === 0 || last.remaining > 0); i++) {
      last = await this.runOnce()
      total += last.indexed
      if (last.indexed === 0) break
    }
    return { ...last, indexed: total }
  }

  /** Nettoyage à l'oubli (hard-delete) : embeddings + index. */
  removeFor(factIds: string[]): void {
    if (factIds.length === 0) return
    const placeholders = factIds.map(() => '?').join(',')
    this.store.db
      .prepare(`DELETE FROM embeddings WHERE owner_type = 'fact' AND owner_id IN (${placeholders})`)
      .run(...factIds)
    removeVectors(this.store.db, this.provider.dimensions, factIds)
  }
}
