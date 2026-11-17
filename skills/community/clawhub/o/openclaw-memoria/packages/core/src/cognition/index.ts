/**
 * CognitionEngine — couches cognitives bucket B (async, spec §12).
 *
 * Tourne EN ASYNC, hors du chemin de réponse du recall : l'intégrateur appelle
 * `processFact(factId)` après capture (fire-and-forget, comme indexEmbeddings)
 * et `expandEntities(...)` au recall (SQL pur, 0 LLM).
 *
 * Responsabilités :
 *  - processFact : extrait entités+relations+observations d'UN fait ; idempotent
 *    (re-process ne duplique ni entité ni relation) ;
 *  - expandEntities : à partir de faits germes, propose des faits LIÉS par
 *    entités partagées, STRICTEMENT bornés aux scopes autorisés (anti-fuite) ;
 *  - decay : affaiblit/élague les arêtes (job quotidien daemon).
 *
 * Le LLM est OPTIONNEL : sans provider (ou indisponible), l'extraction d'entités
 * retombe sur l'heuristique FR/EN — le graphe se peuple quand même.
 */
import type { Database } from 'better-sqlite3'
import type { ContentStore } from '../storage/content.js'
import type { LlmProvider } from '../llm/provider.js'
import { ensureCognitionSchema } from '../storage/cognition-schema.js'
import {
  heuristicEntities,
  llmExtract,
  upsertEntity,
  type Extraction,
} from './entities.js'
import {
  applyDecay,
  expandByEntities,
  graphStats,
  linkFactEntity,
  onFactSuperseded,
  reinforceCooccurrence,
  upsertRelation,
  type DecayConfig,
  type GraphStats,
} from './graph.js'
import {
  observationStats,
  upsertObservation,
  type ObservationStats,
} from './observations.js'

export interface CognitionEngineOptions {
  store: ContentStore
  /** LLM d'extraction graphe (optionnel). null/absent → heuristique pure. */
  llm?: LlmProvider | null
}

export interface ProcessFactResult {
  fact_id: string
  entities: number
  relations: number
  observation_created: boolean
  /** false si le fait n'existe pas / est vide (no-op annoncé). */
  processed: boolean
  /** 'llm' si l'extraction a utilisé le LLM, 'heuristic' sinon. */
  via: 'llm' | 'heuristic'
}

export interface ExpandResult {
  fact_id: string
  score: number
  hops: number
}

export class CognitionEngine {
  private readonly store: ContentStore
  private readonly llm: LlmProvider | null

  constructor(opts: CognitionEngineOptions) {
    this.store = opts.store
    this.llm = opts.llm ?? null
    // Schéma cognition appliqué paresseusement (idempotent) : la cognition est
    // utilisable même avant que l'intégrateur ne câble les migrations au tronc.
    ensureCognitionSchema(this.store.db)
  }

  get db(): Database {
    return this.store.db
  }

  /**
   * Peuple entités/relations/observation pour UN fait (async, post-capture).
   * IDEMPOTENT : entités dédupliquées par nom (NOCASE), liens fact↔entité par PK
   * composite, observation upsert par sujet → re-process ne duplique rien.
   * Erreur LLM = NON avalée : log + bascule heuristique (jamais de mort
   * silencieuse — règle V3, le pattern qui a tué Hebbian).
   */
  async processFact(factId: string): Promise<ProcessFactResult> {
    const empty: ProcessFactResult = {
      fact_id: factId,
      entities: 0,
      relations: 0,
      observation_created: false,
      processed: false,
      via: 'heuristic',
    }
    const fact = this.store.getFact(factId)
    if (!fact || !fact.fact.trim()) return empty

    // 1. Extraction — LLM si dispo, sinon heuristique (jamais silencieux).
    let extraction: Extraction
    let via: 'llm' | 'heuristic' = 'heuristic'
    if (this.llm) {
      try {
        const result = await llmExtract(this.llm, fact.fact)
        if (result) {
          extraction = result
          via = 'llm'
        } else {
          extraction = { entities: heuristicEntities(fact.fact), relations: [] }
        }
      } catch (err) {
        console.warn(`[memoria] extraction graphe LLM en échec (fait ${factId}) — heuristique :`, (err as Error).message)
        extraction = { entities: heuristicEntities(fact.fact), relations: [] }
      }
    } else {
      extraction = { entities: heuristicEntities(fact.fact), relations: [] }
    }

    // 2. Persistance graphe (transaction → cohérence + idempotence).
    let entityCount = 0
    let relationCount = 0
    const persist = this.db.transaction(() => {
      // Nom normalisé → id d'entité (upsert dédupliqué).
      const nameToId = new Map<string, string>()
      for (const e of extraction.entities) {
        const id = upsertEntity(this.db, e.name, e.type)
        nameToId.set(e.name.toLowerCase(), id)
        linkFactEntity(this.db, factId, id)
        entityCount++
      }
      // Relations typées explicites (LLM) — bornées aux entités connues.
      for (const r of extraction.relations) {
        const fromId = nameToId.get(r.from.toLowerCase())
        const toId = nameToId.get(r.to.toLowerCase())
        if (!fromId || !toId || fromId === toId) continue
        upsertRelation(this.db, fromId, toId, r.type, factId)
        relationCount++
      }
      // Renforcement de co-occurrence (GE-1) : toutes les paires d'entités du
      // fait. Les arêtes sont non-dirigées + dédupliquées → re-process ne crée
      // pas de doublon, il renforce (poids croissant cap 1.0).
      reinforceCooccurrence(this.db, [...nameToId.values()], factId)
    })
    persist()

    // 3. Observation agrégée par catégorie+sujet (upsert idempotent).
    const subject = observationSubject(fact.category, fact.fact)
    const obs = upsertObservation(this.db, {
      subject,
      content: fact.fact,
      confidence: fact.confidence,
    })

    return {
      fact_id: factId,
      entities: entityCount,
      relations: relationCount,
      observation_created: obs.created,
      processed: true,
      via,
    }
  }

  /**
   * Expansion graphe au recall (§6.1 étape 4). À partir de `seedFactIds`,
   * retourne des fact_ids LIÉS par entités partagées — STRICTEMENT bornés aux
   * scopes autorisés (`allowedScopeIds`). Un fait hors scope autorisé n'est
   * JAMAIS remonté (anti-fuite = 0). SQL pur, 0 LLM → utilisable dans le chemin
   * de réponse.
   */
  expandEntities(
    seedFactIds: string[],
    allowedScopeIds: Iterable<string>,
    opts: { maxHops?: number; maxFacts?: number } = {},
  ): ExpandResult[] {
    const scopes = [...allowedScopeIds]
    if (scopes.length === 0 || seedFactIds.length === 0) return []
    // Pré-filtre permissions transposé en ensemble de fact_ids autorisés :
    // actifs (superseded = 0) ET dans un scope autorisé. C'est l'équivalent
    // local du filtre DUR §6.1 — le graphe ne voit JAMAIS au-delà.
    const placeholders = scopes.map(() => '?').join(',')
    const allowedRows = this.db
      .prepare(`SELECT id FROM facts WHERE superseded = 0 AND scope_id IN (${placeholders})`)
      .all(...scopes) as Array<{ id: string }>
    const allowed = new Set(allowedRows.map(r => r.id))
    return expandByEntities(this.db, seedFactIds, allowed, opts)
  }

  /** Decay du graphe (job quotidien daemon) — affaiblit/élague les arêtes. */
  decay(config?: DecayConfig, now?: number): { decayed: number; pruned: number } {
    return applyDecay(this.db, config, now)
  }

  /** Propagation de supersession (retrait du graphe + jointures). */
  onFactSuperseded(factId: string): number {
    return onFactSuperseded(this.db, factId)
  }

  stats(): GraphStats & { observations: ObservationStats } {
    return { ...graphStats(this.db), observations: observationStats(this.db) }
  }
}

/**
 * Clé d'agrégation d'observation : catégorie + premiers mots significatifs du
 * fait. Volontairement grossière (V1) — deux faits proches partagent un sujet
 * et s'agrègent ; l'affinage par embedding est Phase 6.
 */
function observationSubject(category: string, factText: string): string {
  const words = factText
    .normalize('NFD')
    .replace(/\p{M}+/gu, '')
    .toLowerCase()
    .split(/[^\p{L}\p{N}]+/u)
    .filter(w => w.length > 3)
    .slice(0, 3)
  const tail = words.length > 0 ? words.join(' ') : 'general'
  return `${category}: ${tail}`
}

export {
  // Sous-modules — exposés pour l'intégrateur (wiring) et les tests.
  heuristicEntities,
  llmExtract,
  parseExtraction,
  upsertEntity,
  normalizeEntityType,
  normalizeRelationType,
  ENTITY_TYPES,
  RELATION_TYPES,
} from './entities.js'
export type {
  EntityType,
  RelationType,
  ExtractedEntity,
  ExtractedRelation,
  Extraction as GraphExtraction,
  EntityRow,
} from './entities.js'
export {
  upsertRelation,
  reinforceCooccurrence,
  expandByEntities,
  applyDecay,
  onFactSuperseded,
  linkFactEntity,
  graphStats,
  DEFAULT_DECAY,
} from './graph.js'
export type { RelationRow, DecayConfig, GraphStats } from './graph.js'
export { upsertObservation, getObservation, observationStats } from './observations.js'
export type { ObservationRow, UpsertObservationInput, ObservationStats } from './observations.js'
export { cognitionMigrations, ensureCognitionSchema } from '../storage/cognition-schema.js'
export { TopicEngine, topicMigrations, ensureTopicSchema, topicKeywords } from './topics.js'
export type { TopicSummary, AssignResult, TopicEngineOptions, TopicRelation, TopicGraph } from './topics.js'
export { PatternEngine, patternMigrations, ensurePatternSchema, significantTokens } from './patterns.js'
export type { Pattern, DetectOptions, DetectResult, ConsolidateResult, PatternEngineOptions } from './patterns.js'
export { ProceduralEngine, proceduralMigrations, ensureProceduralSchema } from './procedural.js'
export type { Procedure as ProceduralProcedure, ProcedureMatch, StoreProcedureInput, RecordExecutionInput, ProceduralEngineOptions } from './procedural.js'
export { FeedbackEngine, feedbackMigrations, ensureFeedbackSchema } from './feedback.js'
export type { FeedbackEngineOptions } from './feedback.js'
export { ClusterEngine, clusterMigrations, ensureClusterSchema } from './clusters.js'
export type { ClusterEngineOptions } from './clusters.js'
export { detectContradiction } from './contradiction.js'
export type { Contradiction, DetectContradictionOptions } from './contradiction.js'
export { SelfObservationEngine, selfObservationMigrations, ensureSelfObservationSchema, SELF_OBSERVATION_KINDS } from './self-observation.js'
export type { SelfObservation, SelfObservationKind, SelfObservationEngineOptions } from './self-observation.js'
export { dialectic } from './dialectic.js'
export type { DialecticResult, DialecticOptions } from './dialectic.js'
export { MarkdownSync } from './markdown-sync.js'
export type { MarkdownSyncOptions, ExportOptions } from './markdown-sync.js'
export { RevisionEngine, revisionMigrations, ensureRevisionSchema } from './revision.js'
export type { RevisionProposal, RevisionKind, RevisionStatus, RevisionEngineOptions } from './revision.js'
export { AutoSkillEngine } from './auto-skill.js'
export type { AutoSkillEngineOptions, SkillSource } from './auto-skill.js'
