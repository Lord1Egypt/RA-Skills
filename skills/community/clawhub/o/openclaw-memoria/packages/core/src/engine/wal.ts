/**
 * WalProcessor — consommation/rejeu du WAL (spec §6.2 étapes 1 et 7).
 * Corrige les morts silencieuses du legacy :
 *  - WAL-1 : getUnprocessed/markProcessed n'avaient AUCUN appelant (rejeu décoratif) ;
 *  - WAL-2 : processed restait à 0 → cleanup(7) ne purgeait jamais rien (table illimitée).
 * Garanties ici : chaque entrée pending est traitée exactement une fois par run,
 * échec → retry borné (attempts), abandon = markProcessed + onPermanentFailure
 * (l'appelant audite) — JAMAIS de perte silencieuse, JAMAIS de boucle infinie.
 */
import type { ContentStore } from '../storage/content.js'
import type { WalEntry } from '../types.js'

export type ProcessOutcome =
  /** Entrée consommée avec succès → markProcessed. */
  | { status: 'done'; facts_created: number }
  /**
   * Entrée non traitable MAINTENANT (ex. aucun LLM disponible) : elle RESTE
   * pending SANS tentative comptée — un défaut d'infrastructure ne doit pas
   * consumer le budget de retry ni aboutir à un abandon.
   */
  | { status: 'defer'; reason: string }

export interface WalProcessorOptions {
  store: ContentStore
  processEntry: (entry: WalEntry) => Promise<ProcessOutcome>
  /** Tentatives max avant abandon AUDITÉ (défaut 3). */
  maxAttempts?: number
  /** Appelé à l'abandon définitif d'une entrée (l'appelant audite 'wal_entry_abandoned'). */
  onPermanentFailure?: (entry: WalEntry, error: unknown) => void
  batchSize?: number
  /** Bornes du cleanup post-replay (anti table illimitée du legacy). */
  cleanupMaxRows?: number
  cleanupMaxAgeDays?: number
}

export interface WalRunSummary {
  /** Entrées consommées avec succès. */
  processed: number
  facts_created: number
  /** Entrées laissées pending sans tentative (ex. no-llm). */
  deferred: number
  /** Échecs transitoires (restent pending, attempts incrémenté). */
  failed: number
  /** Abandons définitifs (markProcessed + onPermanentFailure). */
  abandoned: number
}

export interface WalReplaySummary extends WalRunSummary {
  /** Lignes purgées par le cleanup borné post-replay. */
  cleaned: number
}

export class WalProcessor {
  private readonly store: ContentStore
  private readonly processEntry: (entry: WalEntry) => Promise<ProcessOutcome>
  private readonly maxAttempts: number
  private readonly onPermanentFailure: ((entry: WalEntry, error: unknown) => void) | null
  private readonly batchSize: number
  private readonly cleanupMaxRows: number
  private readonly cleanupMaxAgeDays: number

  constructor(opts: WalProcessorOptions) {
    this.store = opts.store
    this.processEntry = opts.processEntry
    this.maxAttempts = opts.maxAttempts ?? 3
    this.onPermanentFailure = opts.onPermanentFailure ?? null
    this.batchSize = opts.batchSize ?? 50
    this.cleanupMaxRows = opts.cleanupMaxRows ?? 5000
    this.cleanupMaxAgeDays = opts.cleanupMaxAgeDays ?? 14
  }

  /**
   * Itère le WAL pending par lots. Chaque entrée est tentée AU PLUS une fois
   * par run (set `handled`) : les entrées en échec/defer ne bouclent pas.
   */
  async processPending(): Promise<WalRunSummary> {
    const summary: WalRunSummary = { processed: 0, facts_created: 0, deferred: 0, failed: 0, abandoned: 0 }
    const handled = new Set<number>()

    for (;;) {
      // La fenêtre grandit avec `handled` pour dépasser les entrées bloquées
      // (échec/defer restent pending et seraient sinon refetchées en tête).
      const batch = this.store
        .walPending(this.batchSize + handled.size)
        .filter(e => !handled.has(e.id))
        .slice(0, this.batchSize)
      if (batch.length === 0) break

      for (const entry of batch) {
        handled.add(entry.id)
        let outcome: ProcessOutcome
        try {
          outcome = await this.processEntry(entry)
        } catch (error) {
          this.handleFailure(entry, error, summary)
          continue
        }
        if (outcome.status === 'done') {
          this.store.walMarkProcessed([entry.id])
          summary.processed++
          summary.facts_created += outcome.facts_created
        } else {
          // Reste pending, AUCUNE tentative comptée — visible via walPendingCount/doctor.
          summary.deferred++
        }
      }
    }
    return summary
  }

  /**
   * Alias documenté de processPending, appelé par le daemon au démarrage
   * (crash-recovery réelle, pas décorative) + cleanup BORNÉ après.
   */
  async replayAtBoot(): Promise<WalReplaySummary> {
    const run = await this.processPending()
    const cleaned = this.store.walCleanup(this.cleanupMaxRows, this.cleanupMaxAgeDays)
    return { ...run, cleaned }
  }

  private handleFailure(entry: WalEntry, error: unknown, summary: WalRunSummary): void {
    this.store.walRecordAttempt(entry.id)
    const attempts = entry.attempts + 1
    const message = truncateError(error)
    if (attempts >= this.maxAttempts) {
      // Abandon AUDITÉ : marqué processed pour sortir de la file (anti-boucle),
      // signalé à l'appelant — jamais une disparition muette.
      this.store.walMarkProcessed([entry.id])
      summary.abandoned++
      console.warn(`[memoria] WAL #${entry.id} abandonné après ${attempts} tentatives : ${message}`)
      try {
        this.onPermanentFailure?.({ ...entry, attempts }, error)
      } catch (callbackError) {
        console.warn(`[memoria] onPermanentFailure a échoué pour WAL #${entry.id} : ${truncateError(callbackError)}`)
      }
    } else {
      summary.failed++
      console.warn(`[memoria] WAL #${entry.id} échec tentative ${attempts}/${this.maxAttempts} : ${message}`)
    }
  }
}

/** Message d'erreur tronqué pour les logs — jamais le contenu complet d'une entrée. */
function truncateError(error: unknown, max = 200): string {
  const msg = error instanceof Error ? error.message : String(error)
  return msg.length > max ? `${msg.slice(0, max)}…` : msg
}
