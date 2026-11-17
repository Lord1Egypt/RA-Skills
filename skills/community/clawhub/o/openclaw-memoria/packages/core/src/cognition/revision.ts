/**
 * Couche REVISION (couches 18+24, bucket D « sur validation », spec §12).
 *
 * Objectif produit : la mémoire accumule, avec le temps, des faits PÉRIMÉS,
 * CONTREDITS par un fait plus récent, ou DUPLIQUÉS. Cette couche les REPÈRE et
 * les PROPOSE à la révision — elle NE supersède RIEN automatiquement. C'est le
 * rôle « ménage de la mémoire » historique du plugin, remis sous contrôle humain.
 *
 * RÈGLE D'OR (gravée, comme patterns/contradiction, bucket D) : `propose()` ne
 * MODIFIE/ne SUPPRIME AUCUN fait. Il ne fait qu'INSÉRER des `revision_proposals`
 * en status 'proposed'. La SEULE méthode qui touche un fait est `accept()`, et
 * UNIQUEMENT sur appel explicite (validation humaine). Aucune mort silencieuse :
 * si le LLM optionnel (via detectContradiction) échoue, l'heuristique reprend.
 *
 * BUG LEGACY RÉPARÉ (revision.ts:178-181 du legacy) : l'action 'split' écrivait
 * `superseded_by = 'split:<id>'` — une chaîne qui n'est PAS un id de fait existant,
 * cassant toute navigation de chaîne de supersession. EN V3 : `accept()` n'écrit
 * dans `superseded_by` QUE le `replacement_fact_id` réel (un fact.id existant) ou
 * NULL pour un obsolète sans remplaçant — jamais une chaîne fabriquée.
 *
 * Deux sources de propositions, 0 LLM requis (le LLM est seulement un confirmateur
 * optionnel via detectContradiction) :
 *  (a) CONTRADICTION — un fait existant contredit par un fait PLUS RÉCENT du même
 *      scope (réutilise `detectContradiction`). Le plus ANCIEN est proposé
 *      'contradicted' ; le plus récent en est le `replacement`.
 *  (b) DOUBLON — deux faits quasi-identiques (texte normalisé égal) du même
 *      scope : le plus ANCIEN est proposé 'duplicate', le plus récent = remplaçant.
 *
 * Le créneau 'obsolete' (kind autorisé par le schéma) est réservé : un fait que
 * l'intégrateur veut proposer à la révision pour péremption (sans remplaçant).
 * `propose()` ne le génère pas tout seul (pas de notion de péremption pure ici),
 * mais `accept()` le gère (supersession SANS replacement).
 */
import type { Database } from 'better-sqlite3'
import type { ContentStore } from '../storage/content.js'
import type { LlmProvider } from '../llm/provider.js'
import { runMigrations, type Migration } from '../storage/migrations.js'
import { newId, nowISO } from '../util.js'
import { normalizeText } from '../storage/content.js'
import { detectContradiction } from './contradiction.js'

/**
 * Migration ADDITIVE de la table `revision_proposals` (versions 90-99, réservées à
 * cette couche). Partage `schema_migrations` du tronc ; le créneau 90-99 évite
 * toute collision (contenu v1-2, cognition ≥10, topics 20-29, patterns 30-39,
 * procedural 40-49, feedback 50-59, clusters 60-69). L'intégrateur concatène ce
 * tableau ; en attendant, `ensureRevisionSchema` l'applique paresseusement.
 */
export const revisionMigrations: Migration[] = [
  {
    version: 90,
    name: 'revision-proposals-initial',
    up(db) {
      db.exec(`
        -- REVISION_PROPOSALS : propositions de ménage de la mémoire (bucket D).
        --  fact_id              = le fait CONCERNÉ (l'ancien, candidat à supersession) ;
        --  kind                 = obsolete | contradicted | duplicate ;
        --  reason               = raison lisible (FR sobre) pour l'UI de revue ;
        --  replacement_fact_id  = le fait qui REMPLACE (plus récent), ou NULL (obsolète pur) ;
        --  status               = proposed (défaut) | accepted | dismissed ;
        -- AUCUNE colonne ne touche aux faits : la table ne fait que PROPOSER.
        CREATE TABLE revision_proposals (
          id TEXT PRIMARY KEY,
          fact_id TEXT NOT NULL,
          kind TEXT NOT NULL
            CHECK (kind IN ('obsolete','contradicted','duplicate')),
          reason TEXT NOT NULL DEFAULT '',
          replacement_fact_id TEXT,
          status TEXT NOT NULL DEFAULT 'proposed'
            CHECK (status IN ('proposed','accepted','dismissed')),
          created_at TEXT NOT NULL
        );
        CREATE INDEX idx_revision_fact ON revision_proposals(fact_id);
        CREATE INDEX idx_revision_status ON revision_proposals(status);
      `)
    },
  },
]

/** Applique le schéma revision (idempotent — re-run sans effet). */
export function ensureRevisionSchema(db: Database): number {
  return runMigrations(db, revisionMigrations)
}

export type RevisionKind = 'obsolete' | 'contradicted' | 'duplicate'
export type RevisionStatus = 'proposed' | 'accepted' | 'dismissed'

export interface RevisionProposal {
  id: string
  fact_id: string
  kind: RevisionKind
  reason: string
  replacement_fact_id: string | null
  status: RevisionStatus
  created_at: string
}

export interface ProposeOptions {
  /** Nombre max de faits actifs scannés (les plus récents d'abord). Défaut 100. */
  limit?: number
  /** Confiance minimale d'une contradiction retenue (transmis à detectContradiction). Défaut 0.6. */
  minContradictionConfidence?: number
  /** Si vrai et un LLM est fourni, confirme les contradictions limites. Défaut false. */
  useLlm?: boolean
}

export interface ProposeResult {
  /** Propositions nouvellement créées sur cet appel. */
  created: number
  /** Propositions ignorées car le fait avait déjà une proposition (idempotence). */
  skippedExisting: number
  /** Toutes les propositions 'proposed' après ce passage (triées). */
  proposals: RevisionProposal[]
}

export interface AcceptResult {
  /** false si la proposition n'existe pas / n'est plus 'proposed' (no-op annoncé). */
  applied: boolean
  /** Id du fait marqué superseded (= proposal.fact_id), ou null si no-op. */
  supersededFactId: string | null
  proposal: RevisionProposal | null
}

export interface RevisionEngineOptions {
  store: ContentStore
  /** LLM confirmateur de contradiction (optionnel). null/absent → heuristique pure. */
  llm?: LlmProvider | null
}

interface ActiveFactRow {
  id: string
  fact: string
  scope_id: string
  created_at: string
  superseded: number
}

const DEFAULT_LIMIT = 100
const DEFAULT_MIN_CONTRADICTION = 0.6

export class RevisionEngine {
  private readonly store: ContentStore
  private readonly llm: LlmProvider | null

  constructor(opts: RevisionEngineOptions) {
    this.store = opts.store
    this.llm = opts.llm ?? null
    // Schéma appliqué paresseusement (idempotent) : la couche est utilisable même
    // avant que l'intégrateur ne câble la migration au tronc.
    ensureRevisionSchema(this.store.db)
  }

  get db(): Database {
    return this.store.db
  }

  /**
   * Scanne les faits ACTIFS (superseded = 0, lifecycle_state = 'active'), les plus
   * récents d'abord, et PROPOSE des révisions. NE TOUCHE AUCUN fait (bucket D) :
   *
   *  (a) CONTRADICTION — pour chaque fait, on demande à `detectContradiction` quels
   *      faits EXISTANTS du même scope le contredisent. On ne propose la
   *      supersession que de l'ANCIEN (created_at < celui du fait courant), avec le
   *      fait courant (plus récent) en `replacement` → kind 'contradicted'.
   *  (b) DOUBLON — deux faits du même scope au texte NORMALISÉ identique : le plus
   *      ancien est proposé 'duplicate', le plus récent = remplaçant.
   *
   * IDEMPOTENT : un fait qui a DÉJÀ une proposition (quel que soit son status :
   * proposed, accepted ou dismissed) n'est pas re-proposé. Un fait dismissed reste
   * donc tranquille (respect de la décision humaine).
   */
  async propose(opts: ProposeOptions = {}): Promise<ProposeResult> {
    const limit = Math.max(1, opts.limit ?? DEFAULT_LIMIT)
    const minConf = opts.minContradictionConfidence ?? DEFAULT_MIN_CONTRADICTION

    // Faits actifs, du plus RÉCENT au plus ancien (le récent est le « remplaçant »
    // potentiel ; on borne au `limit`).
    const facts = this.db
      .prepare(
        `SELECT id, fact, scope_id, created_at, superseded
         FROM facts
         WHERE superseded = 0 AND lifecycle_state = 'active'
         ORDER BY created_at DESC, id DESC
         LIMIT ?`,
      )
      .all(limit) as ActiveFactRow[]

    // Faits déjà couverts par une proposition (n'importe quel status) → idempotence.
    const alreadyProposed = new Set(
      (this.db.prepare('SELECT DISTINCT fact_id FROM revision_proposals').all() as Array<{ fact_id: string }>).map(
        r => r.fact_id,
      ),
    )

    // On collecte d'abord (peut faire des appels LLM async → hors transaction), puis
    // on insère en une transaction. Clé d'unicité : le fait ANCIEN (candidat à la
    // supersession) — on ne propose chaque ancien qu'UNE fois par passe.
    interface Candidate {
      factId: string
      kind: RevisionKind
      reason: string
      replacementFactId: string | null
    }
    const candidates = new Map<string, Candidate>()
    const skipped = new Set<string>() // faits déjà couverts par une proposition existante
    const seenDuplicateText = new Map<string, string>() // texte normalisé → id du fait le + récent vu

    for (const fresh of facts) {
      // (b) DOUBLON : deux faits du même scope au texte normalisé identique. On
      //     parcourt du plus récent au plus ancien → le premier vu (le plus récent)
      //     devient le remplaçant des suivants (plus anciens).
      const dupKey = `${fresh.scope_id} ${normalizeText(fresh.fact).trim()}`
      const newer = seenDuplicateText.get(dupKey)
      if (newer && newer !== fresh.id) {
        if (alreadyProposed.has(fresh.id)) {
          skipped.add(fresh.id)
        } else if (!candidates.has(fresh.id)) {
          candidates.set(fresh.id, {
            factId: fresh.id,
            kind: 'duplicate',
            reason: `Doublon quasi-exact d'un fait plus récent : « ${truncate(fresh.fact)} »`,
            replacementFactId: newer,
          })
        }
        // Un doublon est déjà traité comme doublon : on ne le re-juge pas pour
        // contradiction (même texte → pas de contradiction).
        continue
      }
      seenDuplicateText.set(dupKey, fresh.id)

      // (a) CONTRADICTION : faits EXISTANTS du même scope qui contredisent ce fait.
      //     detectContradiction ne modifie rien — il propose des candidats. On ne
      //     retient que ceux STRICTEMENT plus anciens (l'ancien est superseded, le
      //     fait courant = remplaçant).
      let contradictions
      try {
        contradictions = await detectContradiction(
          this.store,
          fresh.fact,
          fresh.scope_id,
          { minConfidence: minConf, useLlm: opts.useLlm ?? false },
          this.llm,
        )
      } catch (err) {
        // detectContradiction encapsule déjà ses propres erreurs LLM ; si malgré
        // tout il lève, on log (pas de mort silencieuse) et on continue le scan.
        console.warn(
          `[memoria:revision] détection de contradiction en échec (fait ${fresh.id}) — ignoré :`,
          (err as Error).message,
        )
        continue
      }

      for (const c of contradictions) {
        const older = this.db
          .prepare('SELECT id, created_at, superseded FROM facts WHERE id = ?')
          .get(c.existingFactId) as { id: string; created_at: string; superseded: number } | undefined
        if (!older || older.superseded === 1) continue
        // On ne supersède QUE l'ancien : il faut que l'existant soit antérieur au
        // fait courant (départage stable par id si created_at égal).
        const olderIsOlder =
          older.created_at < fresh.created_at || (older.created_at === fresh.created_at && older.id < fresh.id)
        if (!olderIsOlder) continue
        if (alreadyProposed.has(older.id)) {
          skipped.add(older.id)
          continue
        }
        if (candidates.has(older.id)) continue
        candidates.set(older.id, {
          factId: older.id,
          kind: 'contradicted',
          reason: c.reason,
          replacementFactId: fresh.id,
        })
      }
    }

    // Insertion en transaction (cohérence) — toujours en status 'proposed'.
    const ts = nowISO()
    let created = 0
    const insert = this.db.prepare(
      `INSERT INTO revision_proposals (id, fact_id, kind, reason, replacement_fact_id, status, created_at)
       VALUES (?, ?, ?, ?, ?, 'proposed', ?)`,
    )
    const tx = this.db.transaction((rows: Candidate[]) => {
      for (const c of rows) {
        insert.run(newId(), c.factId, c.kind, c.reason, c.replacementFactId, ts)
        created++
      }
    })
    tx([...candidates.values()])

    return { created, skippedExisting: skipped.size, proposals: this.listProposals() }
  }

  /** Propositions 'proposed', triées par création puis fait. */
  listProposals(): RevisionProposal[] {
    const rows = this.db
      .prepare(
        `SELECT * FROM revision_proposals WHERE status = 'proposed'
         ORDER BY created_at ASC, fact_id ASC`,
      )
      .all() as RevisionProposal[]
    return rows
  }

  /** Lecture d'une proposition par id, ou null. */
  getProposal(proposalId: string): RevisionProposal | null {
    const row = this.db.prepare('SELECT * FROM revision_proposals WHERE id = ?').get(proposalId) as
      | RevisionProposal
      | undefined
    return row ?? null
  }

  /**
   * APPLIQUE une révision — LA SEULE méthode qui modifie un fait, et UNIQUEMENT sur
   * cet appel explicite (validation humaine). Marque le fait `superseded = 1` et
   * `superseded_by = replacement_fact_id` (un fact.id RÉEL, jamais une chaîne
   * fabriquée — réparation du bug legacy 'split:'), puis passe la proposition en
   * 'accepted'. No-op annoncé (applied=false) si la proposition n'existe pas ou
   * n'est plus 'proposed'. Le fait de REMPLACEMENT n'est JAMAIS touché.
   */
  accept(proposalId: string): AcceptResult {
    const ts = nowISO()
    const tx = this.db.transaction((): AcceptResult => {
      const proposal = this.getProposal(proposalId)
      if (!proposal || proposal.status !== 'proposed') {
        return { applied: false, supersededFactId: null, proposal: proposal ?? null }
      }
      // Marque l'ANCIEN fait superseded. superseded_by = remplaçant réel (ou NULL
      // pour un obsolète sans remplaçant). On NE touche jamais le remplaçant.
      this.db
        .prepare(
          `UPDATE facts SET superseded = 1, superseded_by = ?, updated_at = ?
           WHERE id = ? AND superseded = 0`,
        )
        .run(proposal.replacement_fact_id, ts, proposal.fact_id)
      this.db
        .prepare("UPDATE revision_proposals SET status = 'accepted' WHERE id = ?")
        .run(proposalId)
      return { applied: true, supersededFactId: proposal.fact_id, proposal: this.getProposal(proposalId) }
    })
    return tx()
  }

  /**
   * ÉCARTE une proposition : status 'dismissed'. NE MODIFIE AUCUN fait. Le fait
   * concerné ne sera PLUS re-proposé par `propose()` (respect de la décision
   * humaine). Retourne false (no-op) si la proposition n'existe pas / n'est plus
   * 'proposed'.
   */
  dismiss(proposalId: string): boolean {
    const proposal = this.getProposal(proposalId)
    if (!proposal || proposal.status !== 'proposed') return false
    this.db.prepare("UPDATE revision_proposals SET status = 'dismissed' WHERE id = ?").run(proposalId)
    return true
  }

  /** Statistiques diagnostic UI (par status). */
  stats(): { total: number; proposed: number; accepted: number; dismissed: number } {
    const total = (this.db.prepare('SELECT COUNT(*) AS c FROM revision_proposals').get() as { c: number }).c
    const byStatus = this.db
      .prepare('SELECT status, COUNT(*) AS c FROM revision_proposals GROUP BY status')
      .all() as Array<{ status: RevisionStatus; c: number }>
    const map = new Map(byStatus.map(r => [r.status, r.c]))
    return {
      total,
      proposed: map.get('proposed') ?? 0,
      accepted: map.get('accepted') ?? 0,
      dismissed: map.get('dismissed') ?? 0,
    }
  }
}

function truncate(s: string, max = 120): string {
  return s.length <= max ? s : `${s.slice(0, max - 1)}…`
}
