/**
 * Patterns — récurrences (couche 22 legacy, bucket D « sur validation », spec §12).
 *
 * Objectif produit : repérer ce que l'utilisateur dit/fait de RÉCURRENT
 * (« tu as dit 5× que tu préfères X ») et le PROPOSER pour consolidation — JAMAIS
 * appliqué automatiquement. C'est le rôle historique du plugin : identifier le
 * récurrent pour le consolider, sous contrôle humain.
 *
 * RÈGLE D'OR (bucket D, gravée) : `detect()` ne MODIFIE jamais les faits — pas de
 * supersede auto, pas de suppression. Il ne fait que PROPOSER (status 'proposed').
 * La consolidation est une action EXPLICITE et réversible (`consolidate`), qui
 * marque les membres `superseded` UNIQUEMENT sur appel direct. Cette couche corrige
 * le « plus gros gaspillage LLM » du legacy (≤30 appels bloquants/run, sorties
 * mortes, superseding destructif non validé) : ici 0 LLM, 0 superseding implicite.
 *
 * Heuristique (PAS de LLM requis) : regroupement par similarité textuelle sur les
 * tokens normalisés (minuscules, sans diacritiques, mots significatifs) —
 * Jaccard > 0.6 — OU topic partagé + même sujet/prédicat. Un groupe de
 * ≥ minOccurrences faits similaires = un pattern.
 *
 * Idempotence : `detect()` réconcilie par EMPREINTE de l'ensemble des membres ET
 * par label proche — re-détecter ne duplique pas, met à jour les occurrences. Un
 * pattern 'dismissed' n'est JAMAIS reproposé.
 */
import type { Database } from 'better-sqlite3'
import type { ContentStore } from '../storage/content.js'
import { isContentWord } from '../storage/content.js'
import { runMigrations, type Migration } from '../storage/migrations.js'
import { newId, nowISO } from '../util.js'

/**
 * Migration ADDITIVE de la table `patterns` (versions 30-39, réservées à cette
 * couche). Elle partage la table `schema_migrations` du tronc + cognition ; le
 * créneau 30-39 évite toute collision avec le contenu (v1) et la cognition (v≥10).
 * L'intégrateur concatène ce tableau à la suite (ContentStore le câblera ; en
 * attendant, `ensurePatternSchema` l'applique paresseusement).
 */
export const patternMigrations: Migration[] = [
  {
    version: 30,
    name: 'patterns-initial',
    up(db) {
      db.exec(`
        -- PATTERNS : récurrences proposées à la consolidation (bucket D).
        --  member_fact_ids = JSON array des faits regroupés (preuves) ;
        --  occurrences     = taille du groupe (= longueur de member_fact_ids) ;
        --  confidence      = f(occurrences, cohésion) ∈ [0,1] ;
        --  status          = proposed (défaut) | accepted | dismissed ;
        --  kind            = preference | habit | convention | fact ;
        --  canonical_fact  = formulation représentative (le membre le + récent/complet).
        -- AUCUNE colonne ne touche aux faits : la table ne fait que PROPOSER.
        CREATE TABLE patterns (
          id TEXT PRIMARY KEY,
          label TEXT NOT NULL,
          canonical_fact TEXT NOT NULL,
          member_fact_ids TEXT NOT NULL DEFAULT '[]',
          occurrences INTEGER NOT NULL DEFAULT 0,
          confidence REAL NOT NULL DEFAULT 0,
          status TEXT NOT NULL DEFAULT 'proposed'
            CHECK (status IN ('proposed','accepted','dismissed')),
          kind TEXT NOT NULL DEFAULT 'fact'
            CHECK (kind IN ('preference','habit','convention','fact')),
          created_at TEXT NOT NULL,
          updated_at TEXT NOT NULL,
          reviewed_at TEXT
        );
        -- Empreinte de l'ensemble des membres → réconciliation idempotente de detect().
        CREATE UNIQUE INDEX idx_patterns_fingerprint ON patterns(member_fact_ids);
        CREATE INDEX idx_patterns_status ON patterns(status);
      `)
    },
  },
]

/**
 * Applique le schéma patterns à une DB de contenu (idempotent — re-run sans
 * effet). Partage `schema_migrations` (versions 30-39 → pas de collision).
 */
export function ensurePatternSchema(db: Database): number {
  return runMigrations(db, patternMigrations)
}

export type PatternStatus = 'proposed' | 'accepted' | 'dismissed'
export type PatternKind = 'preference' | 'habit' | 'convention' | 'fact'

export interface PatternRow {
  id: string
  label: string
  canonical_fact: string
  member_fact_ids: string
  occurrences: number
  confidence: number
  status: PatternStatus
  kind: PatternKind
  created_at: string
  updated_at: string
  reviewed_at: string | null
}

/** Pattern hydraté (member_fact_ids parsé) — forme exposée à l'UI/daemon. */
export interface Pattern {
  id: string
  label: string
  canonical_fact: string
  member_fact_ids: string[]
  occurrences: number
  confidence: number
  status: PatternStatus
  kind: PatternKind
  created_at: string
  updated_at: string
  reviewed_at: string | null
}

export interface DetectOptions {
  /** Taille minimale d'un groupe pour devenir un pattern (défaut 3). */
  minOccurrences?: number
  /** Seuil de similarité Jaccard sur tokens normalisés (défaut 0.6). */
  jaccardThreshold?: number
}

export interface DetectResult {
  /** Patterns nouvellement proposés sur cet appel. */
  created: number
  /** Patterns existants mis à jour (occurrences/membres). */
  updated: number
  /** Groupes ignorés car déjà 'dismissed' (non reproposés). */
  skippedDismissed: number
  /** Tous les patterns 'proposed' après détection (triés). */
  proposed: Pattern[]
}

export interface ConsolidateResult {
  pattern_id: string
  /** Faits membres marqués superseded par la consolidation. */
  superseded: string[]
  /** Vrai si la consolidation a été appliquée (pattern accepté + membres actifs). */
  applied: boolean
}

const DEFAULT_MIN_OCCURRENCES = 3
const DEFAULT_JACCARD = 0.45
/** Mot considéré significatif au-delà de cette longueur (aligné queryTokens). */
const MIN_TOKEN_LEN = 3
const MAX_LABEL_KEYWORDS = 4

/** Forme interne d'un fait candidat pendant la détection. */
interface Candidate {
  id: string
  text: string
  category: string
  createdAt: string
  topicId: string | null
  tokens: Set<string>
  /** Sujet + prédicat grossiers (2 premiers tokens significatifs). */
  subjectPredicate: string
}

export interface PatternEngineOptions {
  store: ContentStore
}

export class PatternEngine {
  private readonly store: ContentStore

  constructor(opts: PatternEngineOptions) {
    this.store = opts.store
    // Schéma appliqué paresseusement (idempotent) : la couche est utilisable même
    // avant que l'intégrateur ne câble la migration au tronc.
    ensurePatternSchema(this.store.db)
  }

  get db(): Database {
    return this.store.db
  }

  /**
   * Scanne les faits ACTIFS (superseded = 0, lifecycle_state = 'active'),
   * regroupe les faits sémantiquement proches/récurrents, et PROPOSE un pattern
   * par groupe de ≥ minOccurrences. N'applique RIEN aux faits (bucket D).
   *
   * Réconciliation idempotente : un groupe dont l'ensemble de membres correspond
   * à un pattern existant (par empreinte) le met à jour ; un label proche d'un
   * pattern existant le met à jour aussi (pas de doublon). Un pattern 'dismissed'
   * couvrant ce groupe est respecté (jamais reproposé).
   */
  detect(opts: DetectOptions = {}): DetectResult {
    const minOcc = Math.max(2, opts.minOccurrences ?? DEFAULT_MIN_OCCURRENCES)
    const jaccard = opts.jaccardThreshold ?? DEFAULT_JACCARD

    const candidates = this.loadCandidates()
    const groups = clusterCandidates(candidates, jaccard)

    let created = 0
    let updated = 0
    let skippedDismissed = 0

    const tx = this.db.transaction(() => {
      for (const group of groups) {
        if (group.length < minOcc) continue
        const outcome = this.upsertPattern(group)
        if (outcome === 'created') created++
        else if (outcome === 'updated') updated++
        else skippedDismissed++
      }
    })
    tx()

    return { created, updated, skippedDismissed, proposed: this.listProposed() }
  }

  /** Patterns 'proposed', triés par occurrences puis confiance décroissantes. */
  listProposed(): Pattern[] {
    const rows = this.db
      .prepare(
        `SELECT * FROM patterns WHERE status = 'proposed'
         ORDER BY occurrences DESC, confidence DESC, created_at ASC`,
      )
      .all() as PatternRow[]
    return rows.map(hydrate)
  }

  /** Lecture d'un pattern par id (hydraté), ou null. */
  getPattern(patternId: string): Pattern | null {
    const row = this.db.prepare('SELECT * FROM patterns WHERE id = ?').get(patternId) as PatternRow | undefined
    return row ? hydrate(row) : null
  }

  /**
   * Accepte un pattern : status 'accepted' + reviewed_at. NE consolide RIEN
   * (pas de supersede) — l'intégrateur appelle `consolidate` séparément s'il
   * veut appliquer. Retourne le pattern mis à jour, ou null si introuvable.
   */
  accept(patternId: string): Pattern | null {
    return this.setStatus(patternId, 'accepted')
  }

  /**
   * Écarte un pattern : status 'dismissed' + reviewed_at. Ne sera PLUS reproposé
   * par `detect()` (même si les faits restent récurrents). Réversible via la DB,
   * mais jamais ré-émis automatiquement. Retourne le pattern, ou null.
   */
  dismiss(patternId: string): Pattern | null {
    return this.setStatus(patternId, 'dismissed')
  }

  /**
   * Consolidation EXPLICITE et réversible (bucket D, étape de validation). Marque
   * les faits membres ENCORE actifs comme superseded — UNIQUEMENT sur cet appel
   * direct, jamais depuis `detect()`. Pré-condition : le pattern doit être
   * 'accepted' (sinon no-op annoncé, applied=false). Le `canonical_fact` n'est PAS
   * créé ici : c'est à l'intégrateur (engine/memoria) de décider d'insérer le fait
   * de référence et de chaîner superseded_by — cette couche ne possède pas la
   * gouvernance de scope/sensibilité d'un nouveau fait.
   */
  consolidate(patternId: string): ConsolidateResult {
    const pattern = this.getPattern(patternId)
    if (!pattern || pattern.status !== 'accepted') {
      return { pattern_id: patternId, superseded: [], applied: false }
    }
    const ts = nowISO()
    const superseded: string[] = []
    const tx = this.db.transaction(() => {
      const stmt = this.db.prepare(
        'UPDATE facts SET superseded = 1, updated_at = ? WHERE id = ? AND superseded = 0',
      )
      for (const factId of pattern.member_fact_ids) {
        const r = stmt.run(ts, factId)
        if (r.changes > 0) superseded.push(factId)
      }
    })
    tx()
    return { pattern_id: patternId, superseded, applied: true }
  }

  /**
   * Réaction à l'oubli/suppression de faits (hard-delete §11 ou supersession) :
   * retire les faits des membres de TOUS les patterns, recompte occurrences, et
   * SUPPRIME un pattern qui retombe sous le seuil (plus assez de preuves pour
   * proposer). Retourne {updated, removed}.
   */
  onForget(factIds: string[], opts: { minOccurrences?: number } = {}): { updated: number; removed: number } {
    if (factIds.length === 0) return { updated: 0, removed: 0 }
    const minOcc = Math.max(2, opts.minOccurrences ?? DEFAULT_MIN_OCCURRENCES)
    const forget = new Set(factIds)
    let updated = 0
    let removed = 0

    const tx = this.db.transaction(() => {
      const rows = this.db.prepare('SELECT * FROM patterns').all() as PatternRow[]
      for (const row of rows) {
        const members = parseMembers(row.member_fact_ids)
        const kept = members.filter(id => !forget.has(id))
        if (kept.length === members.length) continue // aucun membre concerné
        if (kept.length < minOcc) {
          this.db.prepare('DELETE FROM patterns WHERE id = ?').run(row.id)
          removed++
          continue
        }
        // canonical_fact inchangé : c'est une formulation libre, pas un id de
        // membre — onForget ne touche qu'aux preuves (membres/occurrences).
        this.db
          .prepare(
            `UPDATE patterns SET member_fact_ids = ?, occurrences = ?, confidence = ?, updated_at = ?
             WHERE id = ?`,
          )
          .run(
            fingerprintMembers(kept),
            kept.length,
            confidenceFor(kept.length, row.confidence),
            nowISO(),
            row.id,
          )
        updated++
      }
    })
    tx()
    return { updated, removed }
  }

  /** Statistiques (proposés/acceptés/écartés) — diagnostic UI. */
  stats(): { total: number; proposed: number; accepted: number; dismissed: number } {
    const total = (this.db.prepare('SELECT COUNT(*) AS c FROM patterns').get() as { c: number }).c
    const byStatus = this.db
      .prepare('SELECT status, COUNT(*) AS c FROM patterns GROUP BY status')
      .all() as Array<{ status: PatternStatus; c: number }>
    const map = new Map(byStatus.map(r => [r.status, r.c]))
    return {
      total,
      proposed: map.get('proposed') ?? 0,
      accepted: map.get('accepted') ?? 0,
      dismissed: map.get('dismissed') ?? 0,
    }
  }

  // --- interne -------------------------------------------------------------

  /** Charge les faits actifs en candidats (tokens normalisés pré-calculés). */
  private loadCandidates(): Candidate[] {
    const rows = this.db
      .prepare(
        `SELECT id, fact, category, topic_id, created_at
         FROM facts
         WHERE superseded = 0 AND lifecycle_state = 'active'`,
      )
      .all() as Array<{ id: string; fact: string; category: string; topic_id: string | null; created_at: string }>
    const out: Candidate[] = []
    for (const r of rows) {
      const tokens = significantTokens(r.fact)
      if (tokens.size === 0) continue // fait sans contenu exploitable
      out.push({
        id: r.id,
        text: r.fact,
        category: r.category,
        createdAt: r.created_at,
        topicId: r.topic_id,
        tokens,
        subjectPredicate: subjectPredicateOf(r.fact),
      })
    }
    return out
  }

  /**
   * UPSERT idempotent d'un pattern à partir d'un groupe. Logique de
   * réconciliation, dans l'ordre :
   *  1. empreinte EXACTE des membres connue → si 'dismissed' on respecte (skip),
   *     sinon on met à jour (no-op si rien ne change) ;
   *  2. label proche d'un pattern existant (membres recouvrants) → mise à jour de
   *     ses membres/occurrences (le groupe a grossi/évolué) ;
   *  3. sinon → nouveau pattern 'proposed'.
   */
  private upsertPattern(group: Candidate[]): 'created' | 'updated' | 'skipped' {
    const sortedByRecency = [...group].sort((a, b) => (a.createdAt < b.createdAt ? 1 : -1))
    const canonical = sortedByRecency[0]! // le plus récent (= le plus représentatif)
    const memberIds = group.map(c => c.id).sort()
    const fingerprint = fingerprintMembers(memberIds)
    const label = labelFor(group)
    const kind = kindFor(group)
    const occurrences = group.length
    const confidence = confidenceFor(occurrences, cohesion(group))
    const ts = nowISO()

    // 1. Empreinte exacte connue.
    const byFingerprint = this.db
      .prepare('SELECT * FROM patterns WHERE member_fact_ids = ?')
      .get(fingerprint) as PatternRow | undefined
    if (byFingerprint) {
      if (byFingerprint.status === 'dismissed') return 'skipped'
      this.db
        .prepare(
          `UPDATE patterns SET label = ?, canonical_fact = ?, occurrences = ?, confidence = ?, kind = ?, updated_at = ?
           WHERE id = ?`,
        )
        .run(label, canonical.text, occurrences, confidence, kind, ts, byFingerprint.id)
      return 'updated'
    }

    // 2. Pattern existant qui recouvre ce groupe (membres en intersection forte) —
    //    le groupe a évolué (un fait de plus/de moins). On évite un doublon.
    const overlap = this.findOverlapping(memberIds)
    if (overlap) {
      if (overlap.status === 'dismissed') return 'skipped'
      this.db
        .prepare(
          `UPDATE patterns SET label = ?, canonical_fact = ?, member_fact_ids = ?, occurrences = ?, confidence = ?, kind = ?, updated_at = ?
           WHERE id = ?`,
        )
        .run(label, canonical.text, fingerprint, occurrences, confidence, kind, ts, overlap.id)
      return 'updated'
    }

    // 3. Nouveau pattern proposé.
    this.db
      .prepare(
        `INSERT INTO patterns (id, label, canonical_fact, member_fact_ids, occurrences, confidence, status, kind, created_at, updated_at, reviewed_at)
         VALUES (?, ?, ?, ?, ?, ?, 'proposed', ?, ?, ?, NULL)`,
      )
      .run(newId(), label, canonical.text, fingerprint, occurrences, confidence, kind, ts, ts)
    return 'created'
  }

  /**
   * Cherche un pattern dont les membres recouvrent FORTEMENT ce groupe (Jaccard
   * d'ensembles de membres > 0.5) — signe d'un même thème dont le groupe a varié.
   * Évite de reproposer un quasi-doublon à chaque nouveau fait.
   */
  private findOverlapping(memberIds: string[]): PatternRow | undefined {
    const target = new Set(memberIds)
    const rows = this.db.prepare('SELECT * FROM patterns').all() as PatternRow[]
    for (const row of rows) {
      const members = new Set(parseMembers(row.member_fact_ids))
      if (members.size === 0) continue
      const j = jaccardSets(target, members)
      if (j > 0.5) return row
    }
    return undefined
  }

  private setStatus(patternId: string, status: PatternStatus): Pattern | null {
    const ts = nowISO()
    const r = this.db
      .prepare('UPDATE patterns SET status = ?, reviewed_at = ?, updated_at = ? WHERE id = ?')
      .run(status, ts, ts, patternId)
    if (r.changes === 0) return null
    return this.getPattern(patternId)
  }
}

// ---------------------------------------------------------------------------
// Heuristiques pures (testables isolément, 0 LLM, 0 réseau)
// ---------------------------------------------------------------------------

/** Mots-outils FR/EN à ignorer dans la similarité (n'apportent pas de thème). */
const STOPWORDS = new Set([
  'pour', 'avec', 'dans', 'plus', 'mais', 'que', 'qui', 'les', 'des', 'une', 'mon', 'mes',
  'son', 'ses', 'est', 'sont', 'sur', 'par', 'pas', 'tout', 'tous', 'toujours', 'jamais',
  'the', 'and', 'for', 'with', 'this', 'that', 'have', 'has', 'are', 'was', 'were', 'you',
  'your', 'always', 'never', 'all', 'any',
])

/** Tokens significatifs normalisés (minuscules, sans diacritiques, > 3 car., hors stopwords). */
export function significantTokens(text: string): Set<string> {
  const normalized = text
    .toLowerCase()
    .normalize('NFD')
    .replace(/\p{M}+/gu, '')
  const tokens = normalized
    .split(/[^\p{L}\p{N}]+/u)
    .map(t => t.trim())
    .filter(t => t.length >= MIN_TOKEN_LEN && !STOPWORDS.has(t) && isContentWord(t))
  return new Set(tokens)
}

/** Similarité de Jaccard entre deux ensembles de tokens (|∩| / |∪|). */
export function jaccardSets(a: Set<string>, b: Set<string>): number {
  if (a.size === 0 || b.size === 0) return 0
  let inter = 0
  const [small, large] = a.size <= b.size ? [a, b] : [b, a]
  for (const t of small) if (large.has(t)) inter++
  const union = a.size + b.size - inter
  return union === 0 ? 0 : inter / union
}

/** Sujet+prédicat grossier d'un fait : 2 premiers tokens significatifs joints. */
function subjectPredicateOf(text: string): string {
  return [...significantTokens(text)].slice(0, 2).join(' ')
}

/**
 * Deux faits sont « similaires » si :
 *  - Jaccard de leurs tokens > seuil, OU
 *  - ils partagent un topic non-nul ET partagent le même sujet/prédicat grossier.
 */
function similar(a: Candidate, b: Candidate, jaccardThreshold: number): boolean {
  if (jaccardSets(a.tokens, b.tokens) > jaccardThreshold) return true
  if (
    a.topicId !== null &&
    a.topicId === b.topicId &&
    a.subjectPredicate.length > 0 &&
    a.subjectPredicate === b.subjectPredicate
  ) {
    return true
  }
  return false
}

/**
 * Clustering glouton par similarité (composantes connexes d'un graphe de
 * similarité). Déterministe : on parcourt les candidats dans l'ordre, chaque
 * non-assigné démarre un groupe et absorbe transitivement ses voisins similaires.
 */
function clusterCandidates(candidates: Candidate[], jaccardThreshold: number): Candidate[][] {
  const assigned = new Set<string>()
  const groups: Candidate[][] = []
  for (const seed of candidates) {
    if (assigned.has(seed.id)) continue
    const group: Candidate[] = [seed]
    assigned.add(seed.id)
    // Expansion transitive : on ré-évalue contre tous les membres déjà dans le
    // groupe (un fait proche d'un membre rejoint le groupe).
    let grew = true
    while (grew) {
      grew = false
      for (const cand of candidates) {
        if (assigned.has(cand.id)) continue
        if (group.some(m => similar(m, cand, jaccardThreshold))) {
          group.push(cand)
          assigned.add(cand.id)
          grew = true
        }
      }
    }
    groups.push(group)
  }
  return groups
}

/** Cohésion d'un groupe = Jaccard moyen des paires (0..1). 1 fait → 1.0. */
function cohesion(group: Candidate[]): number {
  if (group.length < 2) return 1
  let sum = 0
  let pairs = 0
  for (let i = 0; i < group.length; i++) {
    for (let j = i + 1; j < group.length; j++) {
      sum += jaccardSets(group[i]!.tokens, group[j]!.tokens)
      pairs++
    }
  }
  return pairs === 0 ? 0 : sum / pairs
}

/**
 * Confiance = f(occurrences, cohésion). Croît avec le nombre de preuves
 * (saturation douce) et la cohésion du groupe ; bornée [0,1].
 */
export function confidenceFor(occurrences: number, cohesionOrPrior: number): number {
  // Part « masse » : 3 occ ≈ 0.5, 5 ≈ 0.64, 10 ≈ 0.78 (1 - 1/(1+ln(occ))).
  const mass = 1 - 1 / (1 + Math.log(1 + Math.max(0, occurrences - 1)))
  const coh = clamp01(cohesionOrPrior)
  const score = 0.6 * mass + 0.4 * coh
  return Math.round(clamp01(score) * 1000) / 1000
}

/**
 * Label = thème commun : keywords partagés par le plus de membres (intersection
 * pondérée), à défaut les keywords du fait canonique. Court et lisible.
 */
function labelFor(group: Candidate[]): string {
  const freq = new Map<string, number>()
  for (const c of group) for (const t of c.tokens) freq.set(t, (freq.get(t) ?? 0) + 1)
  const ranked = [...freq.entries()]
    .filter(([, n]) => n >= Math.max(2, Math.ceil(group.length / 2)))
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .slice(0, MAX_LABEL_KEYWORDS)
    .map(([t]) => t)
  if (ranked.length > 0) return ranked.join(' ')
  // Repli : premiers tokens du fait canonique (le plus récent).
  const canonical = [...group].sort((a, b) => (a.createdAt < b.createdAt ? 1 : -1))[0]!
  return [...canonical.tokens].slice(0, MAX_LABEL_KEYWORDS).join(' ') || 'pattern'
}

/**
 * kind : dérive du type des faits du groupe (catégorie dominante). Aligné sur les
 * catégories legacy (preference/erreur/savoir) + conventions de code.
 */
function kindFor(group: Candidate[]): PatternKind {
  const counts = new Map<PatternKind, number>()
  for (const c of group) {
    const k = kindOfCategory(c.category)
    counts.set(k, (counts.get(k) ?? 0) + 1)
  }
  let best: PatternKind = 'fact'
  let bestN = -1
  for (const [k, n] of counts) {
    if (n > bestN) {
      best = k
      bestN = n
    }
  }
  return best
}

function kindOfCategory(category: string): PatternKind {
  const c = category.toLowerCase()
  if (c.includes('pref')) return 'preference'
  if (c.includes('habit') || c.includes('routine') || c.includes('workflow')) return 'habit'
  if (c.includes('convention') || c.includes('regle') || c.includes('rule') || c.includes('style')) return 'convention'
  return 'fact'
}

/** Empreinte stable d'un ensemble de membres : ids triés sérialisés JSON. */
export function fingerprintMembers(memberIds: string[]): string {
  return JSON.stringify([...memberIds].sort())
}

function parseMembers(raw: string): string[] {
  try {
    const parsed: unknown = JSON.parse(raw)
    return Array.isArray(parsed) ? parsed.map(String) : []
  } catch {
    return []
  }
}

function hydrate(row: PatternRow): Pattern {
  return { ...row, member_fact_ids: parseMembers(row.member_fact_ids) }
}

function clamp01(n: number): number {
  if (!Number.isFinite(n)) return 0
  return Math.min(1, Math.max(0, n))
}
