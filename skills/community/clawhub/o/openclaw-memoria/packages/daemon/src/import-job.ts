/**
 * Job d'import ASYNCHRONE dans le daemon (mission B3) : le daemon est le seul
 * processus better-sqlite3 sur les DB → plus de conflit avec un script externe.
 *
 * Règles :
 *  - UN seul job à la fois (la route renvoie 409 sinon) ;
 *  - progression lisible à tout moment (GET /v1/admin/import_status, polling) ;
 *  - legacy : import TOUJOURS depuis un snapshot (better-sqlite3 backup → tmpdir),
 *    jamais la base vivante, puis adoptLegacyInto(instance, { reindex: true }) ;
 *  - aucune mort silencieuse : échec fatal → state 'error' + message précis ;
 *    erreurs non bloquantes (fenêtre/fichier) → status.errors, job 'done'.
 */
import DatabaseCtor from 'better-sqlite3'
import { mkdtempSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { importLegacyDb, nowISO, type Memoria } from '@memoria/core'

export type ImportJobState = 'idle' | 'running' | 'done' | 'error'
export type ImportJobKind = 'transcripts' | 'legacy'

export interface ImportJobProgress {
  files_done: number
  files_total: number
  facts_imported: number
}

export interface ImportJobStatus {
  state: ImportJobState
  kind: ImportJobKind | null
  instance_id: string | null
  progress: ImportJobProgress
  /** Erreur FATALE (state === 'error'). */
  error: string | null
  /** Erreurs non bloquantes consignées pendant le run (fichier/fenêtre en échec). */
  errors: string[]
  started_at: string | null
  finished_at: string | null
}

function idleStatus(): ImportJobStatus {
  return {
    state: 'idle',
    kind: null,
    instance_id: null,
    progress: { files_done: 0, files_total: 0, facts_imported: 0 },
    error: null,
    errors: [],
    started_at: null,
    finished_at: null,
  }
}

export class ImportJobRunner {
  private status: ImportJobStatus = idleStatus()

  constructor(private readonly memoria: Memoria) {}

  /** Copie défensive — le statut interne ne fuit jamais par référence. */
  get current(): ImportJobStatus {
    return { ...this.status, progress: { ...this.status.progress }, errors: [...this.status.errors] }
  }

  get running(): boolean {
    return this.status.state === 'running'
  }

  /** Import de transcripts (claude-code / codex). Le job part en arrière-plan. */
  startTranscripts(input: { instanceId: string; files: string[]; maxWindowsPerFile?: number }): ImportJobStatus {
    this.begin('transcripts', input.instanceId, input.files.length)
    void this.memoria
      .importTranscripts(input.instanceId, input.files, {
        maxWindowsPerFile: input.maxWindowsPerFile,
        onProgress: p => {
          this.status.progress = { files_done: p.filesDone, files_total: p.filesTotal, facts_imported: p.factsImported }
        },
      })
      .then(report => {
        this.status.errors = [...report.errors]
        this.finish({
          files_done: input.files.length,
          files_total: input.files.length,
          facts_imported: report.facts_quarantined,
        })
      })
      .catch((err: unknown) => this.fail(`import transcripts : ${(err as Error).message}`))
    return this.current
  }

  /** Import d'une base legacy OpenClaw (snapshot → quarantaine → adoption). */
  startLegacy(input: { instanceId: string; legacyPath: string }): ImportJobStatus {
    this.begin('legacy', input.instanceId, 1)
    void this.runLegacy(input).catch((err: unknown) => this.fail(`import legacy : ${(err as Error).message}`))
    return this.current
  }

  private async runLegacy(input: { instanceId: string; legacyPath: string }): Promise<void> {
    // 1) SNAPSHOT dans un tmpdir : on n'importe JAMAIS la base vivante (un
    //    OpenClaw encore ouvert dessus ne casse rien), et la source reste intacte.
    const tmp = mkdtempSync(join(tmpdir(), 'memoria-import-legacy-'))
    const snapshot = join(tmp, 'legacy-snapshot.sqlite')
    try {
      const source = new DatabaseCtor(input.legacyPath, { readonly: true, fileMustExist: true })
      try {
        await source.backup(snapshot)
      } finally {
        source.close()
      }

      // 2) Import en quarantaine (pré-vol + backup + vérif/rollback inclus).
      const report = importLegacyDb({ legacyPath: snapshot, memoria: this.memoria })
      if (report.errors.length > 0) {
        this.fail(`import legacy interrompu : ${report.errors.join(' ; ')}`)
        return
      }

      // 3) Adoption immédiate dans la mémoire privée de l'instance (+ réindexation).
      const adopted = this.memoria.adoptLegacyInto(input.instanceId, { reindex: true })
      this.finish({ files_done: 1, files_total: 1, facts_imported: adopted.facts })
    } finally {
      rmSync(tmp, { recursive: true, force: true })
    }
  }

  private begin(kind: ImportJobKind, instanceId: string, filesTotal: number): void {
    if (this.status.state === 'running') {
      // défense en profondeur — la route vérifie déjà et renvoie 409
      throw new Error('un import est déjà en cours')
    }
    this.status = {
      state: 'running',
      kind,
      instance_id: instanceId,
      progress: { files_done: 0, files_total: filesTotal, facts_imported: 0 },
      error: null,
      errors: [],
      started_at: nowISO(),
      finished_at: null,
    }
  }

  private finish(progress: ImportJobProgress): void {
    this.status.progress = progress
    this.status.state = 'done'
    this.status.finished_at = nowISO()
    console.log(
      `[memoria-daemon] import ${this.status.kind ?? '?'} terminé : ${progress.facts_imported} souvenir(s) ` +
        `(${progress.files_done}/${progress.files_total} fichier(s)${this.status.errors.length > 0 ? `, ${this.status.errors.length} erreur(s) non bloquante(s)` : ''})`,
    )
  }

  private fail(message: string): void {
    this.status.state = 'error'
    this.status.error = message
    this.status.finished_at = nowISO()
    console.warn(`[memoria-daemon] ${message}`)
  }
}
