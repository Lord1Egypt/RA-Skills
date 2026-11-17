/**
 * Selective — dédup AVANT stockage, PAR SCOPE (spec §6.2 étape 4).
 * Corrige le legacy SEL-2 : les faits dormants participent au dedup
 * (l'ancien searchFacts filtrait `lifecycle_state != 'dormant'`, donc un
 * doublon d'un fait dormant était re-stocké en double).
 */
import { rowToFact, type ContentStore, type FactRow } from '../storage/content.js'
import type { Fact } from '../types.js'

export interface DuplicateMatch {
  kind: 'exact' | 'near'
  existing: Fact
}

/** Seuil Jaccard au-delà duquel deux faits sont considérés near-dup. */
const NEAR_DUP_JACCARD = 0.85
/** Candidats FTS examinés pour le near-dup (0 appel LLM — heuristique pure). */
const NEAR_DUP_CANDIDATES = 3

/** Normalisation canonique : lowercase, ponctuation/espaces compactés en un séparateur. */
export function normalizeFact(text: string): string {
  return text
    .toLowerCase()
    .replace(/[^\p{L}\p{N}]+/gu, ' ')
    .trim()
}

export function jaccardSimilarity(a: ReadonlySet<string>, b: ReadonlySet<string>): number {
  if (a.size === 0 && b.size === 0) return 1
  let inter = 0
  for (const t of a) if (b.has(t)) inter++
  const union = a.size + b.size - inter
  return union === 0 ? 0 : inter / union
}

/**
 * Cherche un doublon de `factText` dans le scope `scopeId` de la DB `store` :
 *  (a) égalité exacte sur texte normalisé — TOUS les états lifecycle (dormants inclus) ;
 *  (b) near-dup : top-3 FTS du scope puis similarité Jaccard sur tokens > 0.85.
 * Retourne null si aucun doublon. Aucun appel LLM.
 */
export function findDuplicate(store: ContentStore, scopeId: string, factText: string): DuplicateMatch | null {
  const normalized = normalizeFact(factText)
  if (!normalized) return null

  // (a) exact — scan du scope (non superseded), dormants/archivés INCLUS.
  // Volume borné par scope ; si un scope devient massif, un index sur un
  // hash normalisé pourra remplacer ce scan (décision différée, P2 assume le scan).
  const rows = store.db
    .prepare('SELECT * FROM facts WHERE scope_id = ? AND superseded = 0')
    .all(scopeId) as FactRow[]
  for (const row of rows) {
    if (normalizeFact(row.fact) === normalized) {
      return { kind: 'exact', existing: rowToFact(row) }
    }
  }

  // (b) near-dup — FTS borné au scope, dormants inclus, sensibilité non filtrée
  // (le dedup est interne : il n'expose pas de contenu au lecteur).
  const tokens = new Set(normalized.split(' '))
  const hits = store.searchFacts(factText, {
    limit: NEAR_DUP_CANDIDATES,
    includeDormant: true,
    maxSensitivity: 'critical',
    scopeIds: [scopeId],
  })
  for (const hit of hits) {
    const candidate = new Set(normalizeFact(hit.row.fact).split(' '))
    if (jaccardSimilarity(tokens, candidate) > NEAR_DUP_JACCARD) {
      return { kind: 'near', existing: rowToFact(hit.row) }
    }
  }
  return null
}
