/**
 * Couche DIALECTIC (couche 21, bucket C « Opt-in » — spec §12).
 *
 * Objectif produit : un OUTIL explicite (`memoria dialectic "question"`) qui
 * confronte les points de vue PRÉSENTS DANS LA MÉMOIRE sur une question. Il
 * répartit les faits pertinents en POUR / CONTRE / NUANCE selon leur polarité
 * (négations, marqueurs d'opposition « mais/cependant/par contre », valeurs
 * opposées) et produit une SYNTHÈSE courte.
 *
 * Légende du legacy (port-map module 8, bug 3) : `DialecticMemory` était
 * instanciée et exposée mais JAMAIS appelée (couche morte, fan-out maison inutile).
 * En V3 c'est un outil opt-in : il PASSE PAR le pipeline de lecture du store
 * (searchFacts → mêmes pré-filtres permissions/scopes, anti-fuite) et ne réinvente
 * pas son propre fan-out. Il réutilise les helpers de `contradiction.ts`
 * (subjectTokens/hasNegation) plutôt que de dupliquer la détection de polarité.
 *
 * RÈGLE D'OR BUCKET C (gravée) : `dialectic` ne tourne JAMAIS automatiquement
 * dans le chemin de réponse du recall, et ne MODIFIE/ne SUPPRIME RIEN. Il LIT
 * seulement (searchFacts) et retourne une analyse. 0 LLM par défaut : la synthèse
 * est heuristique. Un LLM optionnel injecté produit une vraie synthèse — son
 * échec est LOGGUÉ et on retombe sur la synthèse heuristique (pas de mort
 * silencieuse).
 */
import type { ContentStore, FactRow } from '../storage/content.js'
import type { LlmProvider } from '../llm/provider.js'
import { normalizeText } from '../storage/content.js'
import { hasNegation, subjectTokens } from './contradiction.js'

/** Marqueurs d'OPPOSITION/concession FR/EN : signalent une nuance ou un contre-point. */
const CONTRAST_PATTERNS: RegExp[] = [
  /\bmais\b/u,
  /\bcependant\b/u,
  /\btoutefois\b/u,
  /\bneanmoins\b/u, // néanmoins (normalisé)
  /\bpar contre\b/u,
  /\ben revanche\b/u,
  /\bpourtant\b/u,
  /\bsauf\b/u,
  /\bhowever\b/u,
  /\bbut\b/u,
  /\bthough\b/u,
  /\bwhereas\b/u,
  /\byet\b/u,
]

/** Polarité d'un fait vis-à-vis de la question. */
export type Stance = 'pour' | 'contre' | 'nuance'

export interface DialecticOptions {
  /** Nombre max de faits examinés (pré-sélection FTS). Défaut 20. */
  limit?: number
  /** Restreint aux scopes autorisés (anti-fuite, comme searchFacts). */
  scopeIds?: string[]
  /**
   * LLM optionnel pour une vraie synthèse. Échec/indispo → repli heuristique
   * (jamais silencieux : log).
   */
  llm?: LlmProvider | null
}

export interface DialecticResult {
  question: string
  /** Faits qui vont dans le SENS de la question (affirmatifs, sans opposition). */
  pour: FactRow[]
  /** Faits qui s'OPPOSENT (négation isolée vs le noyau pour, ou valeur opposée). */
  contre: FactRow[]
  /** Faits qui NUANCENT (marqueurs « mais/cependant/par contre »). */
  nuance: FactRow[]
  /** Synthèse courte (heuristique par défaut, LLM si fourni et disponible). */
  synthese: string
}

/**
 * Confronte les faits de la mémoire sur `question`. NE MODIFIE RIEN (lecture
 * seule via searchFacts). Heuristique pure par défaut ; LLM optionnel pour la
 * seule synthèse.
 *
 * Répartition :
 *  - on récupère les faits pertinents par FTS (bornés aux scopes autorisés) ;
 *  - chaque fait porteur d'un marqueur d'opposition (« mais », « cependant »…) →
 *    NUANCE ;
 *  - sinon, on regarde sa polarité : le « camp » majoritaire (le plus de faits
 *    affirmatifs sur le même sujet) devient POUR ; ceux de polarité opposée
 *    (négation isolée, ou valeur numérique en conflit avec le camp pour) → CONTRE.
 *  - la question elle-même peut imposer une polarité de référence : si elle nie,
 *    le « pour » s'aligne sur les faits qui nient comme elle.
 */
export async function dialectic(
  store: ContentStore,
  question: string,
  opts: DialecticOptions = {},
): Promise<DialecticResult> {
  const q = (question ?? '').trim()
  const limit = opts.limit ?? 20
  const empty: DialecticResult = { question: q, pour: [], contre: [], nuance: [], synthese: '' }
  if (!q) {
    return { ...empty, synthese: 'Question vide : rien à confronter.' }
  }

  // 1) Faits pertinents — FTS avec PRÉ-FILTRE permissions du store (anti-fuite :
  //    superseded/lifecycle/sensibilité/scopes). On ne voit jamais au-delà.
  const hits = store.searchFacts(q, { limit, scopeIds: opts.scopeIds })
  const facts = hits.map(h => h.row)
  if (facts.length === 0) {
    return { ...empty, synthese: `Aucun souvenir pertinent sur : « ${q} ».` }
  }

  // 2) Partition POUR / CONTRE / NUANCE.
  const partition = partitionStances(q, facts)

  // 3) Synthèse — LLM optionnel, repli heuristique (jamais silencieux).
  let synthese = heuristicSynthesis(q, partition)
  if (opts.llm) {
    const llmSynthese = await llmSynthesis(opts.llm, q, partition)
    if (llmSynthese) synthese = llmSynthese
  }

  return { question: q, ...partition, synthese }
}

interface Partition {
  pour: FactRow[]
  contre: FactRow[]
  nuance: FactRow[]
}

/** Vrai si le texte contient un marqueur d'opposition/concession. */
export function hasContrast(text: string): boolean {
  const norm = normalizeText(text)
  return CONTRAST_PATTERNS.some(re => re.test(norm))
}

/** Valeurs numériques d'un texte (port 8080, version 2…), pour le clash de valeur. */
function numericValues(text: string): Set<string> {
  const out = new Set<string>()
  for (const m of normalizeText(text).matchAll(/\b\d+(?:[.:]\d+)*\b/gu)) out.add(m[0])
  return out
}

/**
 * Répartit les faits. La question fixe une polarité de RÉFÉRENCE (nie ou non).
 * Un fait :
 *  - avec marqueur d'opposition → NUANCE (priorité, c'est un point mitigé) ;
 *  - de même polarité (négation) que la question → POUR ;
 *  - de polarité inverse, OU portant une valeur numérique en conflit avec le
 *    camp pour sur un sujet partagé → CONTRE ;
 *  - sinon → POUR (il appuie le sujet sans s'y opposer).
 */
function partitionStances(question: string, facts: FactRow[]): Partition {
  const qNeg = hasNegation(question)
  const qTokens = subjectTokens(question)

  const pour: FactRow[] = []
  const contre: FactRow[] = []
  const nuance: FactRow[] = []

  // Premier passage : nuances + polarité par négation. On mémorise les valeurs
  // numériques des faits « pour » pour détecter ensuite un clash de valeur.
  const pourValues: Array<{ values: Set<string>; tokens: Set<string> }> = []

  for (const f of facts) {
    if (hasContrast(f.fact)) {
      nuance.push(f)
      continue
    }
    const fNeg = hasNegation(f.fact)
    // Même polarité que la question → va dans le sens de la question (POUR).
    // Polarité inverse → s'oppose (CONTRE).
    if (fNeg === qNeg) {
      pour.push(f)
      pourValues.push({ values: numericValues(f.fact), tokens: subjectTokens(f.fact) })
    } else {
      contre.push(f)
    }
  }

  // Second passage : clash de VALEUR au sein du camp « pour ». Deux faits
  // affirmatifs sur le MÊME sujet mais avec des nombres DIFFÉRENTS ne peuvent
  // être tous deux « pour » la même réponse : le premier reste pour (référence),
  // les suivants en conflit basculent en CONTRE. Couvre « le port est 8080 » vs
  // « le port est 9090 » : même polarité, valeurs incompatibles.
  if (pourValues.length > 1) {
    const reference = pourValues[0]!
    if (reference.values.size > 0) {
      const kept: FactRow[] = []
      const keptValues: Array<{ values: Set<string>; tokens: Set<string> }> = []
      for (let i = 0; i < pour.length; i++) {
        const f = pour[i]!
        const pv = pourValues[i]!
        const sharedSubject =
          [...pv.tokens].some(t => !/^\d/.test(t) && reference.tokens.has(t)) ||
          (qTokens.size > 0 && [...pv.tokens].some(t => !/^\d/.test(t) && qTokens.has(t)))
        const valueClash =
          i > 0 &&
          pv.values.size > 0 &&
          sharedSubject &&
          ![...pv.values].some(v => reference.values.has(v))
        if (valueClash) {
          contre.push(f)
        } else {
          kept.push(f)
          keptValues.push(pv)
        }
      }
      pour.length = 0
      pour.push(...kept)
    }
  }

  return { pour, contre, nuance }
}

/**
 * Synthèse HEURISTIQUE (0 LLM) : compte les camps et résume l'état du débat.
 * Toujours NON VIDE quand il y a au moins un fait pertinent.
 */
export function heuristicSynthesis(question: string, p: Partition): string {
  const total = p.pour.length + p.contre.length + p.nuance.length
  if (total === 0) return `Aucun souvenir pertinent sur : « ${question} ».`

  const parts: string[] = []
  if (p.pour.length > 0) parts.push(`${p.pour.length} pour`)
  if (p.contre.length > 0) parts.push(`${p.contre.length} contre`)
  if (p.nuance.length > 0) parts.push(`${p.nuance.length} nuance${p.nuance.length > 1 ? 's' : ''}`)
  const tally = parts.join(', ')

  let verdict: string
  if (p.contre.length === 0 && p.nuance.length === 0) {
    verdict = 'la mémoire est unanime : aucun souvenir contradictoire.'
  } else if (p.pour.length === 0 && p.contre.length > 0) {
    verdict = 'les souvenirs vont plutôt à l’encontre de la question.'
  } else if (p.contre.length > 0) {
    verdict = 'les souvenirs se contredisent — un arbitrage humain est utile.'
  } else {
    verdict = 'des nuances existent, mais aucun souvenir frontalement opposé.'
  }

  return `Sur « ${question} » : ${tally}. ${capitalize(verdict)}`
}

/**
 * Synthèse LLM optionnelle : 1 appel borné. Échec/indispo = LOGGUÉ + null (repli
 * heuristique côté appelant). JAMAIS de mort silencieuse.
 */
async function llmSynthesis(
  llm: LlmProvider,
  question: string,
  p: Partition,
): Promise<string | null> {
  let available = false
  try {
    available = await llm.isAvailable()
  } catch (err) {
    console.warn('[memoria:dialectic] LLM indisponible (isAvailable) — synthèse heuristique :', (err as Error).message)
    return null
  }
  if (!available) return null

  const fmt = (label: string, rows: FactRow[]): string =>
    rows.length === 0 ? '' : `${label} :\n` + rows.map(r => `- ${r.fact}`).join('\n')
  const corpus = [fmt('POUR', p.pour), fmt('CONTRE', p.contre), fmt('NUANCE', p.nuance)]
    .filter(Boolean)
    .join('\n\n')

  try {
    const out = await llm.complete({
      system:
        'Tu reçois une question et des souvenirs classés POUR/CONTRE/NUANCE. ' +
        'Rédige UNE synthèse FACTUELLE de 1-2 phrases, en français sobre, sans inventer. ' +
        "Si les souvenirs se contredisent, dis-le explicitement.",
      prompt: `Question : ${question}\n\n${corpus}`,
      maxTokens: 160,
      temperature: 0.2,
    })
    const trimmed = out.trim()
    return trimmed.length > 0 ? trimmed : null
  } catch (err) {
    console.warn('[memoria:dialectic] synthèse LLM en échec — heuristique :', (err as Error).message)
    return null
  }
}

function capitalize(s: string): string {
  return s.length === 0 ? s : s[0]!.toUpperCase() + s.slice(1)
}
