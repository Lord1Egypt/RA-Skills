/**
 * Scoring GLOBAL du recall (spec §6.1, étape 3) :
 *   score = pertinence(FTS/cosine) × récence × confiance × usage × lifecycle
 *           × hot-tier × BOOST(active_context)
 * Le boost de contexte est une PERTINENCE, jamais une permission — le filtre
 * dur d'exclusion s'applique AVANT (pré-filtre SQL + filtre client).
 */
import type { ActiveContext } from '../types.js'
import type { FactRow } from '../storage/content.js'

export interface ScoreParts {
  relevance: number
  recency: number
  confidence: number
  usage: number
  lifecycle: number
  /** Couche 2 « hot-tier » : un fait consulté récemment est « chaud ». */
  hot: number
  boost: number
  total: number
}

const RECENCY_HALF_LIFE_DAYS = 90
const RECENCY_FLOOR = 0.15
const HOT_HALF_LIFE_DAYS = 3 // un accès « refroidit » en ~3 jours
const RELEVANCE_EXPONENT = 1.8 // la pertinence doit dominer les modulateurs
const USAGE_COEF = 0.12 // pente du bonus d'usage (log)
const USAGE_MAX = 1.3 // plafond du bonus d'usage (anti auto-renforcement)
const HOT_MAX_BONUS = 0.25 // bonus « chaud » max (était 0.5 → auto-renforçait trop)
const PROCEDURE_BOOST = 1.25 // sur une requête impérative, une procédure/how-to prime

/**
 * Requête « impérative / how-to » : l'utilisateur cherche QUOI FAIRE, pas un
 * simple fait. On booste alors les souvenirs de type procédure. Heuristique
 * légère multilingue (FR/EN) — mots d'action et interrogatifs de procédure.
 */
const PROCEDURAL_MARKERS =
  /\b(comment|commen|faut|dois|fermer|ferme|cliqu|ouvrir|ouvre|remplir|saisir|étape|etape|procédure|procedure|comment faire|how|close|click|open|fill|step|should i|proc[eé]der)\b/i

export function isProceduralQuery(query: string): boolean {
  return PROCEDURAL_MARKERS.test(query)
}

export function scoreFact(
  row: FactRow,
  relevance: number,
  context: ActiveContext | undefined,
  now: number,
  proceduralQuery = false,
): ScoreParts {
  const ageDays = Math.max(0, (now - Date.parse(row.created_at)) / 86_400_000)
  const recency = Math.max(RECENCY_FLOOR, Math.exp((-Math.LN2 * ageDays) / RECENCY_HALF_LIFE_DAYS))
  const confidence = clamp(row.confidence, 0.05, 1)
  // Bonus d'usage PLAFONNÉ : sans borne, les faits souvent rappelés grimpaient
  // sans fin (touchFacts ré-incrémente à chaque recall) et enterraient les faits
  // récents mais très pertinents — le riche s'enrichissait.
  const usage = Math.min(USAGE_MAX, 1 + Math.log1p(row.used_count + 0.5 * row.recall_count) * USAGE_COEF)
  const lifecycle = row.lifecycle_state === 'active' ? 1 : row.lifecycle_state === 'dormant' ? 0.3 : 0

  // HOT-TIER (couche 2) : boost transitoire des faits récemment ACCÉDÉS.
  // Le recall met à jour last_accessed_at ; un fait « chaud » remonte un temps,
  // puis refroidit (≠ récence de création, qui est figée).
  let hot = 1
  if (row.last_accessed_at) {
    const sinceAccess = Math.max(0, (now - Date.parse(row.last_accessed_at)) / 86_400_000)
    hot = 1 + HOT_MAX_BONUS * Math.exp((-Math.LN2 * sinceAccess) / HOT_HALF_LIFE_DAYS)
  }

  // BOOST de contexte PLAFONNÉ (audit QW4) : il ne doit jamais faire passer un
  // fait peu pertinent devant un fait très pertinent. Borne dure à ×2, et le
  // relevance_weight (feedback) reste un facteur SÉPARÉ et borné, pas un
  // multiplicateur du boost qui le ferait exploser.
  let boost = 1
  if (context) {
    if (context.project_id && row.project_id === context.project_id) boost *= 1.6
    if (context.client_org_id && row.client_org_id === context.client_org_id) boost *= 1.4
    if (context.org_id && row.org_id === context.org_id) boost *= 1.2
  }
  boost = Math.min(boost, 2)
  const weight = clamp(row.relevance_weight, 0.3, 1.6)

  // BOOST PROCÉDURE : sur une requête impérative (« comment fermer… »), une
  // règle de type procédure/how-to est ce que l'agent doit appliquer → petit
  // avantage. Neutre (×1) sur les requêtes factuelles ou les faits non-procédure.
  const isProcedure = row.category === 'procedure' || row.fact_type === 'howto' || row.fact_type === 'procedure'
  const procedure = proceduralQuery && isProcedure ? PROCEDURE_BOOST : 1

  // La PERTINENCE domine (exposant) ; les autres facteurs modulent.
  const total = Math.pow(Math.max(relevance, 1e-6), RELEVANCE_EXPONENT) * recency * confidence * usage * lifecycle * hot * boost * weight * procedure
  return { relevance, recency, confidence, usage, lifecycle, hot, boost: boost * weight * procedure, total }
}

/**
 * FILTRE DUR anti-fuite inter-clients (décision v2.1 #3) :
 * un fait rattaché à un client n'est visible QUE si l'active_context déclare
 * CE client. Pas de contexte client déclaré → données client masquées.
 * (Les scopes globaux user/org/privé restent accessibles si policy OK.)
 */
export function passesClientIsolation(row: Pick<FactRow, 'client_org_id'>, context: ActiveContext | undefined): boolean {
  if (!row.client_org_id) return true
  return context?.client_org_id === row.client_org_id
}

function clamp(v: number, min: number, max: number): number {
  return Math.min(max, Math.max(min, v))
}
