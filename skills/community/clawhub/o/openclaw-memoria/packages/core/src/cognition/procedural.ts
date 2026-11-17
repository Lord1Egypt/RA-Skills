/**
 * Couche PROCEDURAL (« comment faire les choses », couche 6, bucket A, spec §12).
 *
 * Objectif produit : pour une TÂCHE (« déployer sur Vercel », « publier un
 * article Directus »), retrouver la BONNE procédure — celle qui a le mieux
 * marché par le passé — et APPRENDRE de chaque exécution (succès/échec). C'est
 * le savoir-faire opératoire de l'assistant, distinct des faits (savoir) et des
 * patterns (récurrences proposées).
 *
 * 0 LLM sur le chemin de réponse : `matchProcedures` est de la recherche FTS5
 * pure + scoring SQL/JS. L'apprentissage (`recordExecution`) est un simple UPDATE
 * de compteurs. Aucun appel réseau.
 *
 * BUGS LEGACY RÉPARÉS (gravés dans le schéma V3 + ici dans le code) :
 *  - procedural.ts:1053 — `failure_reasons` lue/écrite mais absente du schéma
 *    legacy → SQLITE_ERROR avalé par un catch muet, motifs d'échec perdus en
 *    silence. EN V3 : la colonne EXISTE (content-schema.ts) ; `recordExecution`
 *    l'écrit réellement, avec une FENÊTRE GLISSANTE de 10 entrées horodatées.
 *    AUCUN catch muet : si la colonne manquait, l'exception remonterait.
 *  - procedural.ts:296 — `rebuildFts()` réinsérait dans `procedures_fts` SANS la
 *    colonne `rowid` (table external-content) → rowids auto-assignés désalignés,
 *    le JOIN de recherche retournait les MAUVAISES procédures. EN V3 : on ne
 *    rebuild JAMAIS la FTS à la main. La synchro passe par les TRIGGERS
 *    `procedures_ai/ad/au` (content-schema.ts) qui portent le rowid explicite.
 *    `storeProcedure` fait un UPSERT (INSERT ... ON CONFLICT DO UPDATE) qui
 *    déclenche le trigger `procedures_au` → la FTS reste alignée, jamais de
 *    fantôme. Si jamais un rebuild était nécessaire, ce serait via la commande
 *    FTS5 `INSERT INTO procedures_fts(procedures_fts) VALUES('rebuild')`, qui
 *    gère le rowid correctement — jamais un SELECT sans rowid.
 *
 * Migration 40-49 (créneau réservé) : colonnes additives `quality_score`
 * (taux de succès lissé, mémoïsé pour le tri) et `last_used_at` (récence, pour
 * le scoring). Idempotente, défensive (la table `procedures` vient du tronc).
 */
import type { Database } from 'better-sqlite3'
import type { ContentStore } from '../storage/content.js'
import { runMigrations, type Migration } from '../storage/migrations.js'
import { fromJsonArray, newId, nowISO, toJson } from '../util.js'
import { normalizeText, queryTokens, toFtsQuery } from '../storage/content.js'

/**
 * Migration ADDITIVE de la table `procedures` (versions 40-49, réservées à cette
 * couche). Partage `schema_migrations` du tronc ; le créneau 40-49 évite toute
 * collision (contenu v1, cognition ≥10, topics 20-29, patterns 30-39).
 * L'intégrateur concatène ce tableau ; en attendant, `ensureProceduralSchema`
 * l'applique paresseusement (constructeur de l'engine).
 */
export const proceduralMigrations: Migration[] = [
  {
    version: 40,
    name: 'procedural-quality-columns',
    up(db) {
      // Colonnes ajoutées de façon DÉFENSIVE : la table `procedures` est créée
      // par le tronc (content-schema.ts). On ne (re)crée jamais la table ni la
      // FTS ici — seulement des colonnes de scoring.
      const cols = (db.pragma('table_info(procedures)') as Array<{ name: string }>).map(c => c.name)
      if (!cols.includes('quality_score')) {
        db.exec('ALTER TABLE procedures ADD COLUMN quality_score REAL NOT NULL DEFAULT 0.5')
      }
      if (!cols.includes('last_used_at')) {
        db.exec("ALTER TABLE procedures ADD COLUMN last_used_at TEXT")
      }
      // Index de tri (taux de succès) — best-effort, ne casse pas si déjà là.
      db.exec('CREATE INDEX IF NOT EXISTS idx_procedures_quality ON procedures(quality_score DESC)')
    },
  },
]

/** Applique le schéma procedural (idempotent — re-run sans effet). */
export function ensureProceduralSchema(db: Database): number {
  return runMigrations(db, proceduralMigrations)
}

export type ProcedureLifecycleState = 'active' | 'dormant' | 'archived'
export type ExecutionOutcome = 'success' | 'failure'

/** Fenêtre glissante des motifs d'échec conservés (anti-table illimitée). */
export const FAILURE_REASONS_WINDOW = 10

/** Ligne brute de `procedures` (colonnes JSON sous forme de chaîne). */
export interface ProcedureRow {
  id: string
  name: string
  description: string
  steps: string
  trigger_patterns: string
  success_count: number
  failure_count: number
  failure_reasons: string
  scope_id: string
  assistant_instance_id: string | null
  project_id: string | null
  lifecycle_state: ProcedureLifecycleState
  quality_score: number
  last_used_at: string | null
  created_at: string
  updated_at: string
}

/** Procédure hydratée (champs JSON parsés) — forme exposée à l'UI/recall. */
export interface Procedure {
  id: string
  name: string
  description: string
  steps: string[]
  trigger_patterns: string[]
  success_count: number
  failure_count: number
  failure_reasons: string[]
  scope_id: string
  assistant_instance_id: string | null
  project_id: string | null
  lifecycle_state: ProcedureLifecycleState
  /** Taux de succès lissé (Laplace) ∈ [0,1] — fiabilité de la procédure. */
  quality_score: number
  last_used_at: string | null
  created_at: string
  updated_at: string
}

export interface StoreProcedureInput {
  id?: string
  name: string
  description?: string
  steps?: string[]
  trigger_patterns?: string[]
  scope_id: string
  assistant_instance_id?: string | null
  project_id?: string | null
  lifecycle_state?: ProcedureLifecycleState
}

export interface MatchOptions {
  limit?: number
  /** Restreint aux scopes autorisés (anti-fuite, comme searchFacts). */
  scopeIds?: string[]
  /** Inclure les procédures dormantes/archivées (défaut : actives seulement). */
  includeInactive?: boolean
}

export interface ProcedureMatch {
  procedure: Procedure
  /** Pertinence FTS normalisée [0,1] (couverture de requête × bm25). */
  relevance: number
  /** Score combiné [0,1] : récence × taux de succès × pertinence. */
  score: number
}

export interface RecordExecutionInput {
  procedureId: string
  outcome: ExecutionOutcome
  /** Sortie d'erreur (sur failure) → motif horodaté append à failure_reasons. */
  errorOutput?: string
}

export interface RecordExecutionResult {
  /** false si la procédure n'existe pas (no-op annoncé, pas de throw). */
  applied: boolean
  procedure: Procedure | null
}

export interface ProceduralEngineOptions {
  store: ContentStore
}

export class ProceduralEngine {
  private readonly store: ContentStore

  constructor(opts: ProceduralEngineOptions) {
    this.store = opts.store
    // Schéma appliqué paresseusement (idempotent) : la couche est utilisable
    // même avant que l'intégrateur ne câble la migration au tronc.
    ensureProceduralSchema(this.store.db)
  }

  get db(): Database {
    return this.store.db
  }

  /**
   * Crée ou met à jour une procédure (UPSERT par id). L'UPSERT
   * (`ON CONFLICT(id) DO UPDATE`) déclenche le trigger `procedures_au` qui
   * resynchronise `procedures_fts` avec le rowid explicite — JAMAIS de rebuild
   * manuel (réparation du bug procedural.ts:296). Les compteurs d'exécution ne
   * sont PAS touchés par un re-store (ils n'appartiennent qu'à recordExecution).
   */
  storeProcedure(input: StoreProcedureInput): Procedure {
    const ts = nowISO()
    const id = input.id ?? newId()
    const steps = toJson(input.steps ?? [])
    const triggers = toJson(input.trigger_patterns ?? [])

    this.db
      .prepare(
        `INSERT INTO procedures (
           id, name, description, steps, trigger_patterns,
           success_count, failure_count, failure_reasons,
           scope_id, assistant_instance_id, project_id,
           lifecycle_state, quality_score, last_used_at,
           created_at, updated_at
         ) VALUES (
           @id, @name, @description, @steps, @trigger_patterns,
           0, 0, '[]',
           @scope_id, @assistant_instance_id, @project_id,
           @lifecycle_state, 0.5, NULL,
           @created_at, @updated_at
         )
         ON CONFLICT(id) DO UPDATE SET
           name = excluded.name,
           description = excluded.description,
           steps = excluded.steps,
           trigger_patterns = excluded.trigger_patterns,
           scope_id = excluded.scope_id,
           assistant_instance_id = excluded.assistant_instance_id,
           project_id = excluded.project_id,
           lifecycle_state = excluded.lifecycle_state,
           updated_at = excluded.updated_at`,
      )
      .run({
        id,
        name: input.name,
        description: input.description ?? '',
        steps,
        trigger_patterns: triggers,
        scope_id: input.scope_id,
        assistant_instance_id: input.assistant_instance_id ?? null,
        project_id: input.project_id ?? null,
        lifecycle_state: input.lifecycle_state ?? 'active',
        created_at: ts,
        updated_at: ts,
      })

    return this.getProcedure(id)!
  }

  /**
   * Recherche la procédure la plus pertinente pour une requête de TÂCHE.
   * FTS5 sur `procedures_fts` (name/description/trigger_patterns), puis SCORE :
   *
   *   score = pertinence × tauxSucces × recence
   *
   *  - pertinence : couverture de requête × bm25 normalisé (comme searchFacts) ;
   *  - tauxSucces : success/(success+failure) lissé Laplace (= quality_score) —
   *    la procédure qui a le MIEUX marché remonte à pertinence égale ;
   *  - recence : décroissance douce sur last_used_at (récent = mieux).
   *
   * Pré-filtre DUR dans le SQL (scopes autorisés + lifecycle) — anti-fuite,
   * aligné §6.1. 0 LLM → utilisable sur le chemin de réponse.
   */
  matchProcedures(query: string, opts: MatchOptions = {}): ProcedureMatch[] {
    const match = toFtsQuery(query)
    if (!match) return []
    const limit = opts.limit ?? 10
    const lifecycleStates = opts.includeInactive ? ['active', 'dormant', 'archived'] : ['active']

    const conditions: string[] = [`p.lifecycle_state IN (${lifecycleStates.map(() => '?').join(',')})`]
    const params: unknown[] = [...lifecycleStates]
    if (opts.scopeIds && opts.scopeIds.length > 0) {
      conditions.push(`p.scope_id IN (${opts.scopeIds.map(() => '?').join(',')})`)
      params.push(...opts.scopeIds)
    }

    const sql = `
      SELECT p.*, -bm25(procedures_fts) AS fts_relevance
      FROM procedures_fts
      JOIN procedures p ON p.rowid = procedures_fts.rowid
      WHERE procedures_fts MATCH ?
        AND ${conditions.join(' AND ')}
      ORDER BY fts_relevance DESC
      LIMIT ?
    `
    const rows = this.db.prepare(sql).all(match, ...params, limit * 4) as Array<
      ProcedureRow & { fts_relevance: number }
    >
    if (rows.length === 0) return []

    const tokens = queryTokens(query)
    const maxBm25 = Math.max(...rows.map(r => Math.max(0, r.fts_relevance)), 1e-9)
    const now = Date.now()

    const matches: ProcedureMatch[] = rows.map(r => {
      // Couverture : combien de tokens de la requête apparaissent dans le texte
      // indexé (name + description + trigger_patterns), comme searchFacts.
      const haystack = normalizeText(`${r.name} ${r.description} ${r.trigger_patterns}`)
      const matched = tokens.filter(t => haystack.includes(t)).length
      const coverage = tokens.length > 0 ? matched / tokens.length : 0
      const bm25Norm = Math.max(0, r.fts_relevance) / maxBm25
      const relevance = coverage * (0.3 + 0.7 * bm25Norm)

      const successRate = successRateOf(r.success_count, r.failure_count)
      const recency = recencyScore(r.last_used_at, now)

      // Score multiplicatif : une procédure non pertinente reste basse même si
      // elle a un bon taux de succès ; à pertinence proche, le taux de succès et
      // la récence départagent. quality_score (mémoïsé) === successRate calculé.
      const score = relevance * (0.55 + 0.45 * successRate) * (0.7 + 0.3 * recency)

      return { procedure: hydrate(r), relevance, score }
    })

    matches.sort((a, b) => b.score - a.score || b.relevance - a.relevance)
    return matches.slice(0, limit)
  }

  /**
   * Enregistre une exécution : incrémente success_count / failure_count, met à
   * jour quality_score (taux de succès lissé) et last_used_at. Sur ÉCHEC, append
   * un motif horodaté à `failure_reasons` (JSON) en FENÊTRE GLISSANTE de 10 :
   * le 11e échec évince le plus ancien. La FTS reste alignée (failure_reasons
   * n'est pas indexée ; aucune colonne FTS-trackée — name/description/triggers —
   * n'est modifiée → aucun fantôme).
   *
   * RÉPARE procedural.ts:1053 : ici la colonne EXISTE et est réellement écrite,
   * sans catch muet. Si elle manquait, l'exception remonterait (pas avalée).
   * No-op annoncé (applied=false) si la procédure n'existe pas.
   */
  recordExecution(input: RecordExecutionInput): RecordExecutionResult {
    const { procedureId, outcome, errorOutput } = input
    const ts = nowISO()

    const tx = this.db.transaction((): RecordExecutionResult => {
      const row = this.db.prepare('SELECT * FROM procedures WHERE id = ?').get(procedureId) as
        | ProcedureRow
        | undefined
      if (!row) return { applied: false, procedure: null }

      const success = outcome === 'success' ? row.success_count + 1 : row.success_count
      const failure = outcome === 'failure' ? row.failure_count + 1 : row.failure_count

      // Fenêtre glissante des motifs d'échec : append + garder les 10 derniers.
      let failureReasons = fromJsonArray(row.failure_reasons)
      if (outcome === 'failure') {
        const reason = formatFailureReason(ts, errorOutput)
        failureReasons = [...failureReasons, reason].slice(-FAILURE_REASONS_WINDOW)
      }

      const quality = successRateOf(success, failure)

      // UPDATE qui NE TOUCHE PAS name/description/trigger_patterns → le trigger
      // procedures_au (sur ces 3 colonnes) ne se déclenche pas, la FTS ne bouge
      // pas. failure_reasons/compteurs ne sont pas indexés : 0 fantôme.
      this.db
        .prepare(
          `UPDATE procedures
             SET success_count = ?, failure_count = ?, failure_reasons = ?,
                 quality_score = ?, last_used_at = ?, updated_at = ?
           WHERE id = ?`,
        )
        .run(success, failure, toJson(failureReasons), quality, ts, ts, procedureId)

      const updated = this.db.prepare('SELECT * FROM procedures WHERE id = ?').get(procedureId) as ProcedureRow
      return { applied: true, procedure: hydrate(updated) }
    })

    return tx()
  }

  /** Liste les procédures (actives par défaut), triées par fiabilité puis récence. */
  listProcedures(opts: { scopeIds?: string[]; includeInactive?: boolean } = {}): Procedure[] {
    const lifecycleStates = opts.includeInactive ? ['active', 'dormant', 'archived'] : ['active']
    const conditions: string[] = [`lifecycle_state IN (${lifecycleStates.map(() => '?').join(',')})`]
    const params: unknown[] = [...lifecycleStates]
    if (opts.scopeIds && opts.scopeIds.length > 0) {
      conditions.push(`scope_id IN (${opts.scopeIds.map(() => '?').join(',')})`)
      params.push(...opts.scopeIds)
    }
    const rows = this.db
      .prepare(
        `SELECT * FROM procedures
         WHERE ${conditions.join(' AND ')}
         ORDER BY quality_score DESC, (last_used_at IS NULL), last_used_at DESC, created_at DESC`,
      )
      .all(...params) as ProcedureRow[]
    return rows.map(hydrate)
  }

  /** Lecture d'une procédure par id (hydratée), ou null. */
  getProcedure(id: string): Procedure | null {
    const row = this.db.prepare('SELECT * FROM procedures WHERE id = ?').get(id) as ProcedureRow | undefined
    return row ? hydrate(row) : null
  }

  /** Statistiques diagnostic UI (total / fiabilité moyenne / actives). */
  stats(): { total: number; active: number; avgQuality: number } {
    const total = (this.db.prepare('SELECT COUNT(*) AS c FROM procedures').get() as { c: number }).c
    const active = (
      this.db.prepare("SELECT COUNT(*) AS c FROM procedures WHERE lifecycle_state = 'active'").get() as {
        c: number
      }
    ).c
    const avg = (
      this.db.prepare('SELECT AVG(quality_score) AS a FROM procedures').get() as { a: number | null }
    ).a
    return { total, active, avgQuality: avg ?? 0 }
  }
}

// ---------------------------------------------------------------------------
// Helpers purs (testables isolément, 0 réseau)
// ---------------------------------------------------------------------------

/**
 * Taux de succès LISSÉ (Laplace add-one) : (s+1)/(s+f+2). Une procédure sans
 * exécution vaut 0.5 (neutre) ; 5/0 ≈ 0.86, 0/5 ≈ 0.14. Évite qu'un unique
 * succès écrase tout (1/1 = 0.5 plutôt que 1.0).
 */
export function successRateOf(success: number, failure: number): number {
  const s = Math.max(0, success)
  const f = Math.max(0, failure)
  return (s + 1) / (s + f + 2)
}

/**
 * Récence ∈ [0,1] : décroissance exponentielle de demi-vie 30 jours sur
 * last_used_at. Jamais utilisée → 0.5 (neutre, ni pénalisée ni avantagée).
 */
export function recencyScore(lastUsedAt: string | null, now: number = Date.now()): number {
  if (!lastUsedAt) return 0.5
  const t = Date.parse(lastUsedAt)
  if (!Number.isFinite(t)) return 0.5
  const ageDays = Math.max(0, (now - t) / 86_400_000)
  return Math.exp((-Math.LN2 * ageDays) / 30)
}

/** Motif d'échec horodaté : `[YYYY-MM-DD] <message>` (compact, lisible UI). */
export function formatFailureReason(ts: string, errorOutput?: string): string {
  const date = ts.slice(0, 10)
  const msg = (errorOutput ?? '').trim().replace(/\s+/g, ' ').slice(0, 200) || 'échec sans détail'
  return `[${date}] ${msg}`
}

function hydrate(row: ProcedureRow): Procedure {
  return {
    ...row,
    steps: fromJsonArray(row.steps),
    trigger_patterns: fromJsonArray(row.trigger_patterns),
    failure_reasons: fromJsonArray(row.failure_reasons),
  }
}
