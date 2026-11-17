/**
 * Couches FEEDBACK (7) + EXPERTISE (8) — bucket A « Actif », spec §12.
 *
 * Objectif produit : la mémoire s'AMÉLIORE par l'usage RÉEL. Quand des faits
 * servent vraiment à répondre (signal positif), ils remontent au recall ; quand
 * ils sont remontés mais inutiles, ils redescendent doucement ; et l'agent
 * accumule de l'EXPERTISE dans les domaines où ses souvenirs confirment leur
 * utilité (« où l'agent est fort »).
 *
 * RÈGLE D'OR (gravée) : cette couche ne touche JAMAIS le CONTENU d'un fait
 * (jamais `facts.fact`, jamais supersession, jamais suppression). Elle n'agit
 * que sur les POIDS et COMPTEURS de recall :
 *   - `usefulness`        : score cumulé d'utilité (signal positif).
 *   - `used_count`        : nb de fois réellement utilisé dans une réponse.
 *   - `relevance_weight`  : multiplicateur de pertinence au recall, borné
 *                           [PLANCHER, CAP] = [0.3, 2.0]. C'est LUI qui fait
 *                           remonter ce qui sert et redescendre ce qui ne sert pas.
 *
 * EXPERTISE : table `expertise(domain UNIQUE, level, evidence_count)`. Le
 * « domaine » = la catégorie/topic d'un fait. `level` monte avec les signaux
 * positifs confirmés dans le domaine (saturation douce, borné [0,1]),
 * `evidence_count` = nb de signaux observés. `topDomains` reflète où l'agent
 * est « expert ».
 *
 * Migrations réservées versions 50-59 (sans collision : tronc v1, cognition ≥10,
 * topics 20-29, patterns 30-39). Les colonnes `facts.usefulness/recall_count/
 * used_count/relevance_weight` EXISTENT déjà au tronc — cette couche n'ajoute
 * QUE la table `expertise`. Le constructeur applique `ensureFeedbackSchema`
 * (idempotent) pour rester utilisable seul, avant câblage par l'intégrateur.
 */
import type { Database } from 'better-sqlite3'
import type { ContentStore } from '../storage/content.js'
import { runMigrations, type Migration } from '../storage/migrations.js'
import { newId, nowISO } from '../util.js'

/** Bornes du poids de pertinence (recall) — un fait jamais à 0 (cap regain), jamais trop dominant. */
export const RELEVANCE_FLOOR = 0.3
export const RELEVANCE_CAP = 2.0

/** Niveau d'expertise borné [0,1] (0 = novice, 1 = expert confirmé). */
export const EXPERTISE_MAX = 1.0

/**
 * Migration ADDITIVE de la table `expertise` (versions 50-59, réservées à cette
 * couche). Partage `schema_migrations` du tronc ; le créneau 50-59 évite toute
 * collision (contenu v1, cognition ≥10, topics 20-29, patterns 30-39). NE crée
 * PAS de colonnes sur `facts` : elles existent déjà au tronc.
 */
export const feedbackMigrations: Migration[] = [
  {
    version: 50,
    name: 'expertise-initial',
    up(db) {
      db.exec(`
        -- EXPERTISE par domaine (= catégorie/topic d'un fait).
        --  domain         : clé lisible du domaine (UNIQUE) ;
        --  level          : niveau de maîtrise ∈ [0,1], monte avec les signaux
        --                   positifs confirmés (saturation douce) ;
        --  evidence_count : nb de signaux observés (utiles + inutiles) ;
        --  updated_at     : dernière mise à jour.
        -- Reflète OÙ l'agent est « expert » (topDomains). Ne touche aucun fait.
        CREATE TABLE expertise (
          id TEXT PRIMARY KEY,
          domain TEXT NOT NULL UNIQUE,
          level REAL NOT NULL DEFAULT 0,
          evidence_count INTEGER NOT NULL DEFAULT 0,
          updated_at TEXT NOT NULL
        );
        CREATE INDEX idx_expertise_level ON expertise(level DESC);
      `)
    },
  },
]

/** Applique le schéma feedback/expertise (idempotent — re-run sans effet). */
export function ensureFeedbackSchema(db: Database): number {
  return runMigrations(db, feedbackMigrations)
}

export interface ExpertiseRow {
  id: string
  domain: string
  level: number
  evidence_count: number
  updated_at: string
}

/** Domaine d'expertise hydraté (forme exposée à l'UI/daemon). */
export interface Expertise {
  domain: string
  level: number
  evidence_count: number
  updated_at: string
}

export interface ReinforceOptions {
  /** true = faits RÉELLEMENT utilisés dans la réponse (signal +). false = remontés mais inutiles (decay léger). */
  used: boolean
}

export interface ReinforceResult {
  /** Faits effectivement mis à jour (existants, non superseded). */
  updated: string[]
  /** Domaines (catégories) touchés par ce signal, avec leur niveau d'expertise après MAJ. */
  domains: string[]
}

export interface DecayUnusedOptions {
  /** Faits inactifs depuis au moins ce nb de jours (sur last_accessed_at, à défaut created_at). */
  olderThanDays?: number
  /** Facteur multiplicatif appliqué à relevance_weight (0<factor<1). Défaut 0.95. */
  factor?: number
}

export interface FeedbackStats {
  /** Faits avec relevance_weight > 1 (boostés par l'usage réel). */
  reinforced: number
  /** Faits avec relevance_weight < 1 (atténués). */
  attenuated: number
  /** Faits jamais utilisés (used_count = 0). */
  neverUsed: number
  /** Somme des used_count (volume de signaux positifs). */
  totalUses: number
  /** Nb de domaines d'expertise suivis. */
  domains: number
  /** Niveau d'expertise moyen sur les domaines suivis. */
  avgExpertise: number
}

// --- Constantes d'ajustement (calibrage doux, testable) --------------------

/** Gain de relevance_weight par usage utile confirmé. */
const REINFORCE_STEP = 0.25
/** Gain d'usefulness par usage utile (score cumulé non borné — diagnostic/tri). */
const USEFULNESS_STEP = 1.0
/** Atténuation de relevance_weight quand remonté mais INUTILE (multiplicatif). */
const UNUSED_PENALTY = 0.85
/** Pas d'expertise par signal positif confirmé dans un domaine (avant saturation). */
const EXPERTISE_STEP = 0.15

export interface FeedbackEngineOptions {
  store: ContentStore
}

export class FeedbackEngine {
  private readonly store: ContentStore

  constructor(opts: FeedbackEngineOptions) {
    this.store = opts.store
    // Schéma appliqué paresseusement (idempotent) : utilisable même avant que
    // l'intégrateur ne câble la migration au tronc. Les colonnes facts existent
    // déjà au tronc → on ne crée QUE la table expertise.
    ensureFeedbackSchema(this.store.db)
  }

  get db(): Database {
    return this.store.db
  }

  /**
   * Signal d'usage RÉEL. `used:true` = ces faits ont servi à répondre (signal
   * positif) → monte usefulness + used_count + relevance_weight (cap 2.0) et
   * crédite l'expertise du domaine. `used:false` = remontés au recall mais
   * inutiles → léger decay de relevance_weight (plancher 0.3), sans toucher au
   * contenu ni supprimer. Ne traite que des faits existants et non superseded.
   */
  reinforce(factIds: string[], opts: ReinforceOptions): ReinforceResult {
    const ids = dedupe(factIds)
    if (ids.length === 0) return { updated: [], domains: [] }
    const ts = nowISO()
    const updated: string[] = []
    const domainHits = new Map<string, number>()

    const tx = this.db.transaction(() => {
      // Sélection des faits ACTIFS concernés (non superseded). On lit la
      // catégorie = domaine pour créditer l'expertise.
      const placeholders = ids.map(() => '?').join(',')
      const rows = this.db
        .prepare(`SELECT id, category, relevance_weight FROM facts WHERE id IN (${placeholders}) AND superseded = 0`)
        .all(...ids) as Array<{ id: string; category: string; relevance_weight: number }>

      const upUseful = this.db.prepare(
        `UPDATE facts SET
           usefulness = usefulness + ?,
           used_count = used_count + 1,
           relevance_weight = MIN(?, relevance_weight + ?),
           last_accessed_at = ?,
           updated_at = ?
         WHERE id = ?`,
      )
      const upUnused = this.db.prepare(
        `UPDATE facts SET
           relevance_weight = MAX(?, relevance_weight * ?),
           updated_at = ?
         WHERE id = ?`,
      )

      for (const r of rows) {
        if (opts.used) {
          upUseful.run(USEFULNESS_STEP, RELEVANCE_CAP, REINFORCE_STEP, ts, ts, r.id)
          domainHits.set(r.category, (domainHits.get(r.category) ?? 0) + 1)
        } else {
          upUnused.run(RELEVANCE_FLOOR, UNUSED_PENALTY, ts, r.id)
        }
        updated.push(r.id)
      }
    })
    tx()

    // L'expertise ne monte QUE sur signal positif confirmé (faits utiles).
    const domains: string[] = []
    if (opts.used) {
      for (const [domain, hits] of domainHits) {
        this.updateExpertise(domain, EXPERTISE_STEP * hits)
        domains.push(domain)
      }
    }
    return { updated, domains }
  }

  /**
   * Decay DOUX des faits jamais réutilisés depuis longtemps : leur
   * relevance_weight décline (plancher 0.3) pour qu'ils soient MOINS prioritaires
   * au recall — JAMAIS supprimés. N'affecte QUE les vieux faits non utilisés
   * (used_count = 0) plus anciens que `olderThanDays` (sur last_accessed_at, à
   * défaut created_at). Retourne le nb de faits atténués.
   */
  decayUnused(opts: DecayUnusedOptions = {}): number {
    const olderThanDays = opts.olderThanDays ?? 30
    const factor = clampFactor(opts.factor ?? 0.95)
    const cutoff = new Date(Date.now() - olderThanDays * 86_400_000).toISOString()
    const ts = nowISO()

    // COALESCE(last_accessed_at, created_at) = « dernière activité » du fait.
    // On n'atténue que ce qui est ENCORE au-dessus du plancher (no-op sinon).
    const r = this.db
      .prepare(
        `UPDATE facts SET
           relevance_weight = MAX(?, relevance_weight * ?),
           updated_at = ?
         WHERE superseded = 0
           AND used_count = 0
           AND COALESCE(last_accessed_at, created_at) < ?
           AND relevance_weight > ?`,
      )
      .run(RELEVANCE_FLOOR, factor, ts, cutoff, RELEVANCE_FLOOR)
    return r.changes
  }

  // --- EXPERTISE -----------------------------------------------------------

  /**
   * Crédite (ou débite) un domaine. `delta` positif = preuve d'utilité
   * confirmée → le niveau monte (saturation douce vers 1.0, jamais au-delà) ;
   * `delta` négatif = atténuation (plancher 0). evidence_count compte CHAQUE
   * signal (|delta| > 0). Upsert idempotent sur `domain` (UNIQUE). Domaine vide
   * ignoré. Retourne le niveau après MAJ.
   */
  updateExpertise(domain: string, delta: number): number {
    const key = domain.trim()
    if (key.length === 0 || !Number.isFinite(delta)) {
      const cur = this.getExpertise(domain)
      return cur?.level ?? 0
    }
    const ts = nowISO()
    const existing = this.db.prepare('SELECT level, evidence_count FROM expertise WHERE domain = ?').get(key) as
      | { level: number; evidence_count: number }
      | undefined

    // Saturation douce vers EXPERTISE_MAX : un delta positif comble une fraction
    // du chemin restant (gros gains tôt, marginaux ensuite) → reflète une vraie
    // courbe d'apprentissage. Delta négatif = pénalité linéaire au plancher 0.
    const prev = existing?.level ?? 0
    const next = delta >= 0
      ? clamp(prev + delta * (EXPERTISE_MAX - prev), 0, EXPERTISE_MAX)
      : clamp(prev + delta, 0, EXPERTISE_MAX)
    const evidence = (existing?.evidence_count ?? 0) + (delta !== 0 ? 1 : 0)

    if (existing) {
      this.db
        .prepare('UPDATE expertise SET level = ?, evidence_count = ?, updated_at = ? WHERE domain = ?')
        .run(next, evidence, ts, key)
    } else {
      this.db
        .prepare('INSERT INTO expertise (id, domain, level, evidence_count, updated_at) VALUES (?, ?, ?, ?, ?)')
        .run(newId(), key, next, evidence, ts)
    }
    return next
  }

  /** Lit l'expertise d'un domaine (hydratée), ou null si jamais observé. */
  getExpertise(domain: string): Expertise | null {
    const row = this.db
      .prepare('SELECT domain, level, evidence_count, updated_at FROM expertise WHERE domain = ?')
      .get(domain.trim()) as ExpertiseRow | undefined
    return row ? { domain: row.domain, level: row.level, evidence_count: row.evidence_count, updated_at: row.updated_at } : null
  }

  /** Domaines les plus maîtrisés (niveau décroissant, départage par preuves). */
  topDomains(limit = 10): Expertise[] {
    const rows = this.db
      .prepare(
        `SELECT domain, level, evidence_count, updated_at FROM expertise
         WHERE level > 0
         ORDER BY level DESC, evidence_count DESC, domain ASC
         LIMIT ?`,
      )
      .all(Math.max(0, limit)) as ExpertiseRow[]
    return rows.map(r => ({ domain: r.domain, level: r.level, evidence_count: r.evidence_count, updated_at: r.updated_at }))
  }

  // --- Diagnostic ----------------------------------------------------------

  /** Statistiques d'usage (tableau de bord « % souvenirs utiles », spec §13). */
  stats(): FeedbackStats {
    const f = this.db
      .prepare(
        `SELECT
           SUM(CASE WHEN relevance_weight > 1 THEN 1 ELSE 0 END) AS reinforced,
           SUM(CASE WHEN relevance_weight < 1 THEN 1 ELSE 0 END) AS attenuated,
           SUM(CASE WHEN used_count = 0 THEN 1 ELSE 0 END) AS neverUsed,
           COALESCE(SUM(used_count), 0) AS totalUses
         FROM facts WHERE superseded = 0`,
      )
      .get() as { reinforced: number | null; attenuated: number | null; neverUsed: number | null; totalUses: number }
    const e = this.db
      .prepare('SELECT COUNT(*) AS c, COALESCE(AVG(level), 0) AS avg FROM expertise')
      .get() as { c: number; avg: number }
    return {
      reinforced: f.reinforced ?? 0,
      attenuated: f.attenuated ?? 0,
      neverUsed: f.neverUsed ?? 0,
      totalUses: f.totalUses ?? 0,
      domains: e.c,
      avgExpertise: e.avg,
    }
  }
}

// --- Helpers purs -----------------------------------------------------------

function dedupe(ids: string[]): string[] {
  return [...new Set(ids.filter(id => typeof id === 'string' && id.length > 0))]
}

function clamp(n: number, lo: number, hi: number): number {
  if (!Number.isFinite(n)) return lo
  return Math.min(hi, Math.max(lo, n))
}

/** Facteur de decay strictement dans ]0,1[ (jamais ≥1, jamais ≤0). */
function clampFactor(factor: number): number {
  if (!Number.isFinite(factor)) return 0.95
  return Math.min(0.999, Math.max(0.001, factor))
}
