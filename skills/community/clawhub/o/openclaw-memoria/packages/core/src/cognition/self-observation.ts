/**
 * Couche SELF-OBSERVATION (couche 19, bucket C « Opt-in » — spec §12).
 *
 * Objectif produit : l'agent observe SON PROPRE comportement — où il est FORT,
 * où il est FAIBLE, ses HABITUDES, ses ANGLES MORTS. C'est radicalement
 * différent des `observations` (couche 9) qui portent sur des SUJETS EXTERNES
 * (« le client X préfère… ») : ici le sujet est l'agent lui-même (« je me trompe
 * souvent sur les chemins ESM », « je déploie bien sur Vercel »).
 *
 * RÈGLE D'OR BUCKET C (gravée, comme contradiction/patterns) : cette couche est
 * OPT-IN. Elle ne tourne JAMAIS automatiquement dans le chemin de réponse du
 * recall, et ne MODIFIE/ne SUPPRIME JAMAIS un fait. `deriveFromHistory` PROPOSE
 * des auto-observations à partir de l'historique procédural/patterns — elle ne
 * s'auto-valide pas (les observations dérivées sont enregistrées telles quelles,
 * c'est l'agent/UI qui les interprète, jamais une mutation de la mémoire).
 *
 * 0 LLM : tout est SQL pur + heuristique. La couche est utilisable sans réseau.
 *
 * Migrations réservées versions 70-79 (sans collision : tronc v1, cognition ≥10,
 * topics 20-29, patterns 30-39, procedural 40-49, feedback 50-59, clusters 60-69).
 * Le constructeur applique `ensureSelfObservationSchema` (idempotent) pour rester
 * utilisable seul, avant câblage par l'intégrateur.
 */
import type { Database } from 'better-sqlite3'
import type { ContentStore } from '../storage/content.js'
import { runMigrations, type Migration } from '../storage/migrations.js'
import { newId, nowISO } from '../util.js'
import { normalizeText } from '../storage/content.js'

/** Nature d'une auto-observation : où l'agent se situe sur lui-même. */
export type SelfObservationKind = 'strength' | 'weakness' | 'habit' | 'blindspot'

/** Valeurs autorisées pour `kind` (CHECK SQL + garde JS). */
export const SELF_OBSERVATION_KINDS: readonly SelfObservationKind[] = [
  'strength',
  'weakness',
  'habit',
  'blindspot',
]

/**
 * Migration ADDITIVE : table `self_observations` (versions 70-79, réservées à
 * cette couche). Partage `schema_migrations` du tronc ; le créneau 70-79 évite
 * toute collision avec les couches déjà câblées. Le legacy stockait des SIGNAUX
 * bruts horodatés sans rétention (croissance illimitée — bug §module8) ; le
 * modèle V3 est un UPSERT par observation normalisée (evidence_count++), borné
 * par construction : ré-observer la même chose n'ajoute pas de ligne.
 */
export const selfObservationMigrations: Migration[] = [
  {
    version: 70,
    name: 'self-observations-initial',
    up(db) {
      db.exec(`
        -- SELF-OBSERVATIONS : l'agent sur lui-même (≠ observations externes).
        --  instance_id    : agent concerné ('' = global, agnostique d'instance) ;
        --  observation    : phrase lisible (« je me trompe sur les chemins ESM ») ;
        --  norm_key       : clé normalisée (minuscules, sans accents, espaces
        --                   réduits) calculée en JS → match stable et indexable
        --                   AU-DELÀ de NOCASE (qui n'égalise pas é/É) ;
        --  kind           : strength | weakness | habit | blindspot ;
        --  evidence_count : nb de fois observé (UPSERT par clé normalisée) ;
        --  confidence     : confiance ∈ [0,1], lissée à chaque ré-observation.
        -- AUCUNE colonne ne référence/touche un fait : descriptif pur, bucket C.
        CREATE TABLE self_observations (
          id TEXT PRIMARY KEY,
          instance_id TEXT NOT NULL DEFAULT '',
          observation TEXT NOT NULL,
          norm_key TEXT NOT NULL,
          kind TEXT NOT NULL CHECK (kind IN ('strength','weakness','habit','blindspot')),
          evidence_count INTEGER NOT NULL DEFAULT 1,
          confidence REAL NOT NULL DEFAULT 0.6,
          created_at TEXT NOT NULL,
          updated_at TEXT NOT NULL
        );
        -- Unicité par (instance, clé normalisée) → l'UPSERT ne duplique jamais,
        -- même si casse/accents/espaces diffèrent.
        CREATE UNIQUE INDEX idx_self_obs_key ON self_observations(instance_id, norm_key);
        CREATE INDEX idx_self_obs_kind ON self_observations(kind);
      `)
    },
  },
]

/** Applique le schéma self-observation (idempotent — re-run sans effet). */
export function ensureSelfObservationSchema(db: Database): number {
  return runMigrations(db, selfObservationMigrations)
}

export interface SelfObservationRow {
  id: string
  instance_id: string
  observation: string
  /** Clé normalisée interne (dédup) — non exposée dans `SelfObservation`. */
  norm_key: string
  kind: SelfObservationKind
  evidence_count: number
  confidence: number
  created_at: string
  updated_at: string
}

/** Auto-observation hydratée (forme exposée à l'UI/daemon/tests). */
export interface SelfObservation {
  id: string
  instance_id: string
  observation: string
  kind: SelfObservationKind
  evidence_count: number
  confidence: number
  created_at: string
  updated_at: string
}

export interface RecordSelfObservationInput {
  observation: string
  kind: SelfObservationKind
  /** Confiance ∈ [0,1] de l'observation (défaut 0.6). */
  confidence?: number
  /** Agent concerné ('' = global). Défaut ''. */
  instanceId?: string
}

export interface ListSelfObservationsOptions {
  kind?: SelfObservationKind
  instanceId?: string
  limit?: number
}

/**
 * Source d'historique pour `deriveFromHistory`. On reste DÉCOUPLÉ des engines
 * concrets (procedural/patterns) : l'intégrateur passe des vues minimales déjà
 * lues, la couche ne rouvre pas la DB et ne dépend d'aucun autre module cognitif.
 */
export interface ProcedureSignal {
  /** Libellé de la procédure (sert à formuler l'observation). */
  name: string
  success_count: number
  failure_count: number
}

export interface PatternSignal {
  /** Description de la récurrence détectée. */
  description: string
  /** Occurrences observées (force de la récurrence). */
  occurrences: number
}

export interface DeriveFromHistoryInput {
  procedures?: ProcedureSignal[]
  patterns?: PatternSignal[]
}

export interface DeriveFromHistoryOptions {
  /** Min d'exécutions pour juger une procédure (anti-bruit). Défaut 3. */
  minExecutions?: number
  /** Taux d'échec au-delà duquel on propose une « weakness ». Défaut 0.5. */
  weaknessFailureRate?: number
  /** Taux de succès au-delà duquel on propose une « strength ». Défaut 0.8. */
  strengthSuccessRate?: number
  /** Occurrences min d'un pattern pour proposer une « habit ». Défaut 3. */
  habitOccurrences?: number
  /** Agent concerné. Défaut ''. */
  instanceId?: string
}

export interface DeriveFromHistoryResult {
  /** Auto-observations PROPOSÉES (enregistrées via record, jamais validées par l'agent). */
  proposed: SelfObservation[]
}

export interface SelfObservationEngineOptions {
  store: ContentStore
}

export class SelfObservationEngine {
  private readonly store: ContentStore

  constructor(opts: SelfObservationEngineOptions) {
    this.store = opts.store
    // Schéma appliqué paresseusement (idempotent) : la couche est utilisable
    // seule, avant que l'intégrateur ne câble la migration au tronc.
    ensureSelfObservationSchema(this.store.db)
  }

  get db(): Database {
    return this.store.db
  }

  /**
   * Enregistre une auto-observation. UPSERT par (instance, observation
   * normalisée) : nouvelle observation → insert (evidence_count = 1) ; déjà vue →
   * evidence_count + 1, confiance lissée (moyenne mobile bornée [0,1]). Le `kind`
   * est rafraîchi sur la valeur la plus récente. Ré-enregistrer la MÊME phrase ne
   * crée JAMAIS de doublon. Observation vide rejetée (pas de mort silencieuse).
   */
  record(input: RecordSelfObservationInput): SelfObservation {
    const observation = (input.observation ?? '').trim()
    if (observation.length < 2) {
      throw new Error('self-observation invalide : observation non vide requise')
    }
    if (!SELF_OBSERVATION_KINDS.includes(input.kind)) {
      throw new Error(`self-observation invalide : kind inconnu « ${input.kind} »`)
    }
    const instanceId = (input.instanceId ?? '').trim()
    const confidence = clamp01(input.confidence ?? 0.6)
    const normKey = normalizeObservation(observation)
    const ts = nowISO()

    const tx = this.db.transaction((): SelfObservation => {
      const existing = this.db
        .prepare('SELECT * FROM self_observations WHERE instance_id = ? AND norm_key = ?')
        .get(instanceId, normKey) as SelfObservationRow | undefined

      if (existing) {
        // Confiance = moyenne mobile (poids = nb de preuves) → stable, ne sursaute
        // pas sur une nouvelle observation isolée.
        const n = existing.evidence_count
        const blended = clamp01((existing.confidence * n + confidence) / (n + 1))
        this.db
          .prepare(
            `UPDATE self_observations
               SET evidence_count = evidence_count + 1, confidence = ?, kind = ?, updated_at = ?
             WHERE id = ?`,
          )
          .run(blended, input.kind, ts, existing.id)
        return this.getById(existing.id)!
      }

      const id = newId()
      this.db
        .prepare(
          `INSERT INTO self_observations
             (id, instance_id, observation, norm_key, kind, evidence_count, confidence, created_at, updated_at)
           VALUES (?, ?, ?, ?, ?, 1, ?, ?, ?)`,
        )
        .run(id, instanceId, observation, normKey, input.kind, confidence, ts, ts)
      return this.getById(id)!
    })
    return tx()
  }

  /**
   * Liste les auto-observations (filtre optionnel par kind/instance), triées par
   * preuve puis confiance décroissantes (les plus établies d'abord).
   */
  list(opts: ListSelfObservationsOptions = {}): SelfObservation[] {
    const conditions: string[] = []
    const params: unknown[] = []
    if (opts.kind) {
      conditions.push('kind = ?')
      params.push(opts.kind)
    }
    if (opts.instanceId !== undefined) {
      conditions.push('instance_id = ?')
      params.push(opts.instanceId.trim())
    }
    const where = conditions.length > 0 ? `WHERE ${conditions.join(' AND ')}` : ''
    const limit = Math.max(1, opts.limit ?? 100)
    const rows = this.db
      .prepare(
        `SELECT * FROM self_observations
         ${where}
         ORDER BY evidence_count DESC, confidence DESC, created_at ASC
         LIMIT ?`,
      )
      .all(...params, limit) as SelfObservationRow[]
    return rows.map(hydrate)
  }

  /** Lecture par id (hydratée), ou null. */
  getById(id: string): SelfObservation | null {
    const row = this.db.prepare('SELECT * FROM self_observations WHERE id = ?').get(id) as
      | SelfObservationRow
      | undefined
    return row ? hydrate(row) : null
  }

  /**
   * Oublie une auto-observation par id. Retourne true si une ligne a été retirée.
   * (L'oubli porte sur l'auto-observation, JAMAIS sur un fait : bucket C.)
   */
  forget(id: string): boolean {
    const r = this.db.prepare('DELETE FROM self_observations WHERE id = ?').run(id)
    return r.changes > 0
  }

  /**
   * Dérive des auto-observations de l'HISTORIQUE (procédures, patterns), 0 LLM :
   *  - procédure à fort taux d'ÉCHEC (≥ weaknessFailureRate, ≥ minExecutions) →
   *    propose une « weakness » (« je rate souvent : <nom> ») ;
   *  - procédure à fort taux de SUCCÈS (≥ strengthSuccessRate, ≥ minExecutions) →
   *    propose une « strength » (« je réussis bien : <nom> ») ;
   *  - pattern récurrent (≥ habitOccurrences) → propose une « habit ».
   *
   * Ces propositions sont ENREGISTRÉES via `record` (donc upsert idempotent : un
   * second appel sur le même historique ne crée pas de doublon, il renforce). La
   * couche PROPOSE — elle ne valide rien, ne touche aucun fait. Heuristique pure.
   */
  deriveFromHistory(
    input: DeriveFromHistoryInput,
    opts: DeriveFromHistoryOptions = {},
  ): DeriveFromHistoryResult {
    const minExec = Math.max(1, opts.minExecutions ?? 3)
    const weaknessRate = clamp01(opts.weaknessFailureRate ?? 0.5)
    const strengthRate = clamp01(opts.strengthSuccessRate ?? 0.8)
    const habitOcc = Math.max(1, opts.habitOccurrences ?? 3)
    const instanceId = opts.instanceId

    const proposed: SelfObservation[] = []

    for (const proc of input.procedures ?? []) {
      const name = (proc.name ?? '').trim()
      if (!name) continue
      const success = Math.max(0, proc.success_count | 0)
      const failure = Math.max(0, proc.failure_count | 0)
      const total = success + failure
      if (total < minExec) continue // pas assez d'historique pour juger

      const failureRate = failure / total
      const successRate = success / total

      if (failureRate >= weaknessRate) {
        // Confiance = part d'échec, pondérée par le volume (plus de preuves =
        // plus sûr), bornée. L'observation est PROPOSÉE, pas une vérité gravée.
        const confidence = clamp01(0.4 + 0.6 * failureRate) * volumeFactor(total)
        proposed.push(
          this.record({
            observation: `Je me trompe souvent sur la procédure « ${name} » (taux d'échec ${pct(failureRate)})`,
            kind: 'weakness',
            confidence,
            instanceId,
          }),
        )
      } else if (successRate >= strengthRate) {
        const confidence = clamp01(0.4 + 0.6 * successRate) * volumeFactor(total)
        proposed.push(
          this.record({
            observation: `Je réussis bien la procédure « ${name} » (taux de succès ${pct(successRate)})`,
            kind: 'strength',
            confidence,
            instanceId,
          }),
        )
      }
    }

    for (const pat of input.patterns ?? []) {
      const description = (pat.description ?? '').trim()
      if (!description) continue
      const occurrences = Math.max(0, pat.occurrences | 0)
      if (occurrences < habitOcc) continue
      const confidence = clamp01(0.4 + 0.1 * occurrences)
      proposed.push(
        this.record({
          observation: `Habitude récurrente : ${description} (${occurrences} occurrences)`,
          kind: 'habit',
          confidence,
          instanceId,
        }),
      )
    }

    return { proposed }
  }

  /** Statistiques diagnostic (total + répartition par kind). */
  stats(): { total: number; byKind: Record<SelfObservationKind, number> } {
    const total = (this.db.prepare('SELECT COUNT(*) AS c FROM self_observations').get() as { c: number }).c
    const rows = this.db
      .prepare('SELECT kind, COUNT(*) AS c FROM self_observations GROUP BY kind')
      .all() as Array<{ kind: SelfObservationKind; c: number }>
    const byKind: Record<SelfObservationKind, number> = {
      strength: 0,
      weakness: 0,
      habit: 0,
      blindspot: 0,
    }
    for (const r of rows) byKind[r.kind] = r.c
    return { total, byKind }
  }
}

// ---------------------------------------------------------------------------
// Helpers purs (testables isolément, 0 réseau)
// ---------------------------------------------------------------------------

/** Normalisation d'une observation (alignée sur normalizeText du store). */
export function normalizeObservation(text: string): string {
  return normalizeText(text).replace(/\s+/g, ' ').trim()
}

function hydrate(row: SelfObservationRow): SelfObservation {
  return {
    id: row.id,
    instance_id: row.instance_id,
    observation: row.observation,
    kind: row.kind,
    evidence_count: row.evidence_count,
    confidence: row.confidence,
    created_at: row.created_at,
    updated_at: row.updated_at,
  }
}

/** Saturation douce sur le volume de preuves ∈ [0,1] : 3 exécutions ≈ 0.6, 10 ≈ 0.86. */
function volumeFactor(total: number): number {
  return 1 - Math.exp((-Math.LN2 * Math.max(0, total)) / 3)
}

function pct(ratio: number): string {
  return `${Math.round(clamp01(ratio) * 100)} %`
}

function clamp01(n: number): number {
  if (!Number.isFinite(n)) return 0
  return Math.min(1, Math.max(0, n))
}
