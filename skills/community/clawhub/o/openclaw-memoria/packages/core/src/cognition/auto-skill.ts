/**
 * Couche AUTO-SKILL (couche 23, bucket D « sur validation », spec §12).
 *
 * Objectif produit : quand un PATTERN a été ACCEPTÉ (l'humain a validé une
 * récurrence : « tu consolides toujours en Hello-Primo avant de pousser »), ou
 * qu'une PROCÉDURE revient régulièrement, on peut en faire une « skill » — une
 * procédure CONSOLIDÉE, réutilisable et retrouvable au recall. Cette couche
 * PROPOSE ces skills ; elle n'en crée AUCUNE sans validation explicite.
 *
 * RÈGLE D'OR (bucket D, gravée) : `propose()` ne crée RIEN en base — il retourne
 * des propositions {label, steps, source} en mémoire. La SEULE écriture est
 * `accept(proposal)`, qui INSÈRE une procédure dans la table `procedures` du tronc
 * (via ProceduralEngine.storeProcedure → l'INSERT déclenche les triggers FTS
 * `procedures_ai`, donc la skill est immédiatement retrouvable par matchProcedures).
 *
 * 0 LLM : la consolidation est purement structurelle (patterns acceptés +
 * procédures récurrentes → étapes). Aucun appel réseau, aucune mort silencieuse.
 *
 * Deux sources de propositions :
 *  (1) PATTERNS ACCEPTÉS (table `patterns` status='accepted', couche 22) — chaque
 *      pattern accepté = une récurrence validée → on en dérive une skill dont les
 *      étapes sont les formulations distinctes des faits membres (le canonical en
 *      tête).
 *  (2) PROCÉDURES RÉCURRENTES (table `procedures`) — des procédures actives qui
 *      partagent un même thème (même 1er token de trigger/nom) et qui ont fait
 *      leurs preuves (quality_score correct) → proposition d'une skill de synthèse.
 *      (Source secondaire, conservatrice : elle ne déclenche que sur un vrai
 *      regroupement, pour éviter de re-proposer une procédure isolée déjà existante.)
 */
import type { Database } from 'better-sqlite3'
import type { ContentStore } from '../storage/content.js'
import { ProceduralEngine, type Procedure } from './procedural.js'
import { ensurePatternSchema } from './patterns.js'

export type SkillSource = 'pattern' | 'procedures'

export interface SkillProposal {
  /** Libellé court et lisible de la skill proposée. */
  label: string
  /** Étapes consolidées (≥1) — le savoir-faire à exécuter. */
  steps: string[]
  /** D'où vient la proposition (pour l'UI de revue et la traçabilité). */
  source: SkillSource
  /** Id de l'élément source (pattern accepté ou procédure pivot) — traçabilité. */
  source_id: string
  /** Scope de la skill à créer (hérité de la source ; défaut fourni à propose()). */
  scope_id: string
  /** Description optionnelle (déclencheurs, contexte). */
  description?: string
  /** Patterns déclencheurs proposés (alimentent la FTS de matchProcedures). */
  trigger_patterns?: string[]
}

export interface ProposeSkillOptions {
  /** Scope par défaut des skills issues de patterns (les patterns n'ont pas de scope propre). Défaut 's'. */
  defaultScopeId?: string
  /**
   * quality_score minimal d'une procédure pour entrer dans un regroupement (source
   * 2). Défaut 0.5 (= neutre : une procédure sans échec connu passe).
   */
  minProcedureQuality?: number
  /** Taille minimale d'un regroupement de procédures pour proposer une skill (source 2). Défaut 2. */
  minProcedureGroup?: number
}

export interface AcceptSkillResult {
  /** false si la proposition est invalide (label/steps vides) — no-op annoncé. */
  applied: boolean
  /** La procédure créée (retrouvable par matchProcedures), ou null si no-op. */
  procedure: Procedure | null
}

export interface AutoSkillEngineOptions {
  store: ContentStore
}

const DEFAULT_SCOPE = 's'
const DEFAULT_MIN_QUALITY = 0.5
const DEFAULT_MIN_GROUP = 2

interface PatternRow {
  id: string
  label: string
  canonical_fact: string
  member_fact_ids: string
  status: string
}

export class AutoSkillEngine {
  private readonly store: ContentStore
  private readonly procedural: ProceduralEngine

  constructor(opts: AutoSkillEngineOptions) {
    this.store = opts.store
    // La couche s'appuie sur le schéma patterns (couche 22) et procedural (couche
    // 6). On garantit le schéma patterns (idempotent) ; ProceduralEngine garantit
    // le sien dans son constructeur.
    ensurePatternSchema(this.store.db)
    this.procedural = new ProceduralEngine({ store: this.store })
  }

  get db(): Database {
    return this.store.db
  }

  /**
   * PROPOSE des skills (procédures consolidées) à partir des patterns ACCEPTÉS et
   * des procédures récurrentes. NE crée RIEN en base — retourne des propositions.
   *
   * Idempotence pratique : on n'inclut pas un pattern dont une skill homonyme
   * existe déjà (même name de procédure) — évite de re-proposer une skill déjà
   * créée par un `accept` précédent.
   */
  propose(opts: ProposeSkillOptions = {}): SkillProposal[] {
    const defaultScope = opts.defaultScopeId ?? DEFAULT_SCOPE
    const minQuality = opts.minProcedureQuality ?? DEFAULT_MIN_QUALITY
    const minGroup = Math.max(2, opts.minProcedureGroup ?? DEFAULT_MIN_GROUP)

    const proposals: SkillProposal[] = []

    // Noms de procédures déjà existantes → on évite de re-proposer une skill déjà
    // créée (matérialisée comme procédure du même nom).
    const existingNames = new Set(
      (this.db.prepare('SELECT name FROM procedures').all() as Array<{ name: string }>).map(r =>
        r.name.trim().toLowerCase(),
      ),
    )

    // (1) PATTERNS ACCEPTÉS → une skill par pattern.
    const patterns = this.db
      .prepare("SELECT id, label, canonical_fact, member_fact_ids, status FROM patterns WHERE status = 'accepted'")
      .all() as PatternRow[]

    for (const p of patterns) {
      const label = skillLabel(p.label, p.canonical_fact)
      if (existingNames.has(label.toLowerCase())) continue
      const steps = this.stepsFromPattern(p)
      if (steps.length === 0) continue
      proposals.push({
        label,
        steps,
        source: 'pattern',
        source_id: p.id,
        scope_id: defaultScope,
        description: `Skill consolidée depuis un motif récurrent validé : ${p.label}`,
        trigger_patterns: dedupeNonEmpty([p.label, label]),
      })
    }

    // (2) PROCÉDURES RÉCURRENTES → regroupement par thème (1er token significatif du
    //     nom) ; un groupe de ≥ minGroup procédures fiables propose une skill de
    //     synthèse. Conservateur : ne déclenche que sur un vrai regroupement.
    const procs = this.db
      .prepare(
        `SELECT id, name, description, steps, trigger_patterns, scope_id, quality_score
         FROM procedures
         WHERE lifecycle_state = 'active'`,
      )
      .all() as Array<{
      id: string
      name: string
      description: string
      steps: string
      trigger_patterns: string
      scope_id: string
      quality_score: number
    }>

    const groups = new Map<string, typeof procs>()
    for (const pr of procs) {
      if (pr.quality_score < minQuality) continue
      const key = themeKey(pr.name)
      if (!key) continue
      const arr = groups.get(key) ?? []
      arr.push(pr)
      groups.set(key, arr)
    }

    for (const [key, group] of groups) {
      if (group.length < minGroup) continue
      const label = `skill ${key}`
      if (existingNames.has(label.toLowerCase())) continue
      // Étapes consolidées = union ordonnée des étapes des procédures du groupe.
      const steps = dedupeNonEmpty(group.flatMap(g => parseJsonArray(g.steps)))
      if (steps.length === 0) continue
      proposals.push({
        label,
        steps,
        source: 'procedures',
        source_id: group.map(g => g.id).sort().join(','),
        scope_id: group[0]!.scope_id,
        description: `Skill de synthèse de ${group.length} procédures du thème « ${key} »`,
        trigger_patterns: dedupeNonEmpty([key, ...group.flatMap(g => parseJsonArray(g.trigger_patterns))]).slice(0, 8),
      })
    }

    return proposals
  }

  /**
   * ACCEPTE une proposition de skill : CRÉE la procédure dans la table `procedures`
   * du tronc (via storeProcedure → INSERT → triggers FTS `procedures_ai`). La skill
   * est immédiatement retrouvable par `matchProcedures`. No-op annoncé
   * (applied=false) si la proposition est vide (label/steps manquants) — on ne crée
   * jamais une procédure dégénérée.
   */
  accept(proposal: SkillProposal): AcceptSkillResult {
    const label = (proposal.label ?? '').trim()
    const steps = (proposal.steps ?? []).map(s => s.trim()).filter(s => s.length > 0)
    if (!label || steps.length === 0) {
      return { applied: false, procedure: null }
    }
    const procedure = this.procedural.storeProcedure({
      name: label,
      description: proposal.description ?? '',
      steps,
      trigger_patterns: proposal.trigger_patterns ?? [label],
      scope_id: proposal.scope_id || DEFAULT_SCOPE,
      lifecycle_state: 'active',
    })
    return { applied: true, procedure }
  }

  // --- interne -------------------------------------------------------------

  /**
   * Étapes d'une skill issues d'un pattern : les formulations DISTINCTES de ses
   * faits membres (le canonical en tête), normalisées légèrement. Une seule
   * occurrence par formulation (dédup insensible à la casse/espaces).
   */
  private stepsFromPattern(p: PatternRow): string[] {
    const memberIds = parseJsonArray(p.member_fact_ids)
    const out: string[] = []
    const canon = (p.canonical_fact ?? '').trim()
    if (canon) out.push(canon)
    if (memberIds.length > 0) {
      const placeholders = memberIds.map(() => '?').join(',')
      const rows = this.db
        .prepare(`SELECT id, fact FROM facts WHERE id IN (${placeholders})`)
        .all(...memberIds) as Array<{ id: string; fact: string }>
      // Conserver l'ordre des membres (member_fact_ids), pas l'ordre SQL.
      const byId = new Map(rows.map(r => [r.id, r.fact]))
      for (const id of memberIds) {
        const f = byId.get(id)
        if (f) out.push(f.trim())
      }
    }
    return dedupeNonEmpty(out)
  }
}

// ---------------------------------------------------------------------------
// Helpers purs
// ---------------------------------------------------------------------------

/** Libellé de skill : le label du pattern s'il est parlant, sinon début du canonical. */
function skillLabel(patternLabel: string, canonical: string): string {
  const label = (patternLabel ?? '').trim()
  if (label.length >= 3) return label
  const c = (canonical ?? '').trim()
  return c.length > 0 ? c.split(/\s+/u).slice(0, 6).join(' ') : 'skill'
}

/** Clé de thème d'une procédure : 1er mot significatif (>2 car.) du nom, normalisé. */
function themeKey(name: string): string {
  const norm = (name ?? '')
    .toLowerCase()
    .normalize('NFD')
    .replace(/\p{M}+/gu, '')
  const first = norm.split(/[^\p{L}\p{N}]+/u).find(w => w.length > 2)
  return first ?? ''
}

/** Dédup en conservant l'ordre, sur clé normalisée (casse/espaces), vides exclus. */
function dedupeNonEmpty(values: string[]): string[] {
  const seen = new Set<string>()
  const out: string[] = []
  for (const v of values) {
    const trimmed = (v ?? '').trim()
    if (!trimmed) continue
    const key = trimmed.toLowerCase().replace(/\s+/g, ' ')
    if (seen.has(key)) continue
    seen.add(key)
    out.push(trimmed)
  }
  return out
}

function parseJsonArray(raw: string | null | undefined): string[] {
  if (!raw) return []
  try {
    const parsed: unknown = JSON.parse(raw)
    return Array.isArray(parsed) ? parsed.map(String) : []
  } catch {
    return []
  }
}
