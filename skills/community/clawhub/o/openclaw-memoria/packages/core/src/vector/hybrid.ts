/**
 * Recherche hybride FTS + vectoriel (spec §10) — fusion RRF.
 *
 * RÈGLE ABSOLUE : le vectoriel ne contourne JAMAIS les permissions. Les ids
 * remontés par le KNN repassent par les MÊMES pré-filtres SQL que le FTS
 * (superseded / lifecycle / sensibilité / scopes autorisés) via une jointure
 * sur facts. Sans extension vec ou sans vecteur de requête → résultat = FTS
 * seul, identique à searchFacts.
 */
import type { ContentStore, FtsHit, FtsSearchOptions, FactRow } from '../storage/content.js'
import { isVecAvailable, knn } from './vec-table.js'

export interface HybridSearchOptions extends FtsSearchOptions {
  /** Vecteur de la requête (même modèle que l'index !) ; absent = FTS seul. */
  queryVector?: Float32Array
  dimensions?: number
}

const RRF_K = 60

export function hybridSearchFacts(store: ContentStore, query: string, opts: HybridSearchOptions = {}): FtsHit[] {
  const ftsHits = store.searchFacts(query, opts)

  const vector = opts.queryVector
  if (!vector || !isVecAvailable(store.db)) return ftsHits
  const dimensions = opts.dimensions ?? vector.length

  const limit = opts.limit ?? 50
  const knnHits = knn(store.db, dimensions, vector, limit * 2)
  if (knnHits.length === 0) return ftsHits

  // Re-filtrage permissions des candidats vectoriels (mêmes clauses que searchFacts)
  const lifecycleStates = opts.includeDormant ? ['active', 'dormant'] : ['active']
  const maxSens = opts.maxSensitivity ?? 'normal'
  const sensRank = maxSens === 'critical' ? 2 : maxSens === 'sensitive' ? 1 : 0

  const conditions = [
    `f.id IN (${knnHits.map(() => '?').join(',')})`,
    `f.superseded = 0`,
    `f.lifecycle_state IN (${lifecycleStates.map(() => '?').join(',')})`,
    `(CASE f.sensitivity WHEN 'normal' THEN 0 WHEN 'sensitive' THEN 1 ELSE 2 END) <= ?`,
  ]
  const params: unknown[] = [...knnHits.map(h => h.fact_id), ...lifecycleStates, sensRank]
  if (opts.scopeIds && opts.scopeIds.length > 0) {
    conditions.push(`f.scope_id IN (${opts.scopeIds.map(() => '?').join(',')})`)
    params.push(...opts.scopeIds)
  }
  const allowedRows = store.db
    .prepare(`SELECT f.* FROM facts f WHERE ${conditions.join(' AND ')}`)
    .all(...params) as FactRow[]
  const allowedById = new Map(allowedRows.map(r => [r.id, r]))

  // Fusion RRF : score(d) = Σ 1/(k + rang) par branche, ramené ~0..1 par ×k/2
  const scores = new Map<string, { row: FactRow; score: number }>()
  // On GARDE la pertinence lexicale par couverture (searchFacts, content.ts) :
  // le RRF pur ne classe que par RANG et écrase la magnitude lexicale, ce qui
  // enterre les faits qui couvrent BEAUCOUP de termes de la requête derrière des
  // faits génériques ne partageant qu'un mot fréquent. On la ré-injecte plus bas.
  const lexRelById = new Map<string, number>()
  ftsHits.forEach((hit, rank) => {
    lexRelById.set(hit.row.id, hit.relevance)
    scores.set(hit.row.id, { row: hit.row, score: (RRF_K / 2) * (1 / (RRF_K + rank + 1)) })
  })
  let vecRank = 0
  for (const hit of knnHits) {
    const row = allowedById.get(hit.fact_id)
    if (!row) continue // bloqué par permissions — le vectoriel ne les contourne pas
    const inc = (RRF_K / 2) * (1 / (RRF_K + vecRank + 1))
    vecRank++
    const existing = scores.get(row.id)
    if (existing) existing.score += inc
    else scores.set(row.id, { row, score: inc })
  }

  // Pertinence finale = fusion RRF (rang) MODULÉE par la couverture lexicale
  // (magnitude). Un fait qui couvre tous les termes de la requête garde ~100 %
  // de son RRF ; un hit purement vectoriel (aucun terme lexical) tombe à 40 %,
  // sans disparaître. Corrige l'enfouissement des règles très spécifiques.
  return [...scores.values()]
    .sort((a, b) => b.score - a.score)
    .slice(0, limit)
    .map(s => {
      const rrf = Math.min(1, s.score)
      const lex = lexRelById.get(s.row.id) ?? 0
      return { row: s.row, relevance: rrf * (0.4 + 0.6 * lex) }
    })
}
