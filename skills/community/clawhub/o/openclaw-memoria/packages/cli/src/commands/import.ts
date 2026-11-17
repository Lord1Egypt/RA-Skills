/**
 * `memoria import --instance <id> (--transcripts | --legacy <chemin>) [--max-windows N]`
 * — MINCE client des routes daemon /v1/admin/import_start + /v1/admin/import_status
 * (mission B5). Le job tourne DANS le daemon (un seul processus better-sqlite3
 * sur les DB) ; ici on ne fait qu'afficher la progression en ligne.
 */
import { Command, Option } from 'clipanion/lib/advanced/index.js'
import type { ImportJobStatus } from '@memoria/daemon'
import { fail, findAliveDaemon } from '../index.js'

export class ImportCommand extends Command {
  static override paths = [['import']]
  static override usage = Command.Usage({
    description: 'Importe les souvenirs d’un agent : conversations (transcripts) ou mémoire legacy OpenClaw.',
    details:
      'Le job tourne dans le daemon (« memoria start » d’abord). Transcripts : les souvenirs arrivent DORMANTS et attendent ta validation dans l’écran Revue. Legacy : la mémoire est adoptée directement en privé pour l’instance.',
    examples: [
      ['Conversations Claude Code / Codex', 'memoria import --instance <id> --transcripts'],
      ['Mémoire legacy OpenClaw', 'memoria import --instance <id> --legacy ~/.openclaw/workspace/memory/memoria.db'],
    ],
  })

  instance = Option.String('--instance', { required: true, description: 'Instance cible (voir « memoria agents »)' })
  transcripts = Option.Boolean('--transcripts', false, { description: 'Importer les conversations de l’agent' })
  legacy = Option.String('--legacy', { description: 'Chemin de la base legacy OpenClaw (memoria.db)' })
  maxWindows = Option.String('--max-windows', { description: 'Fenêtres max analysées par fichier (transcripts)' })
  pollMs = Option.String('--poll-ms', { description: 'Intervalle de rafraîchissement en ms (défaut : 1000)' })
  storageRoot = Option.String('--storage-root', { description: 'Racine du stockage' })
  config = Option.String('--config', { description: 'Fichier de découverte' })

  override async execute(): Promise<number> {
    const out = this.context.stdout
    if (this.transcripts && this.legacy) {
      return fail(this.context.stderr, 'import : choisis UNE source — --transcripts OU --legacy <chemin>, pas les deux.')
    }
    if (!this.transcripts && !this.legacy) {
      return fail(this.context.stderr, 'import : indique la source — --transcripts (conversations) ou --legacy <chemin> (mémoire OpenClaw).')
    }
    const maxWindows = this.maxWindows !== undefined ? Number(this.maxWindows) : undefined
    if (maxWindows !== undefined && (!Number.isFinite(maxWindows) || maxWindows < 1)) {
      return fail(this.context.stderr, 'import : --max-windows doit être un entier ≥ 1.')
    }
    const pollMs = Math.max(10, this.pollMs !== undefined ? Number(this.pollMs) || 1000 : 1000)

    const daemon = await findAliveDaemon({ storageRoot: this.storageRoot, configPath: this.config })
    if (!daemon) {
      return fail(this.context.stderr, 'import : le daemon ne tourne pas — lance « memoria start » d’abord (le job d’import tourne dans le daemon).')
    }

    const kind = this.transcripts ? 'transcripts' : 'legacy'
    try {
      await daemon.client.importStart({
        instance_id: this.instance,
        kind,
        ...(this.legacy ? { legacy_path: this.legacy } : {}),
        ...(maxWindows !== undefined ? { max_windows_per_file: Math.floor(maxWindows) } : {}),
      })
      out.write(kind === 'transcripts' ? 'Import des conversations lancé…\n' : 'Import de la mémoire legacy lancé…\n')

      let status: ImportJobStatus
      for (;;) {
        await new Promise(r => setTimeout(r, pollMs))
        status = await daemon.client.importStatus()
        out.write(`\r  ${progressLine(status)}          `)
        if (status.state === 'done' || status.state === 'error') break
      }
      out.write('\n')

      if (status.state === 'error') {
        return fail(this.context.stderr, `import : ${status.error ?? 'erreur inconnue (voir le journal du daemon)'}`)
      }
      out.write(`✓ ${status.progress.facts_imported} souvenir(s) importé(s) (${status.progress.files_done}/${status.progress.files_total} fichier(s)).\n`)
      if (kind === 'transcripts') {
        out.write('  Ils sont DORMANTS : valide-les dans l’écran Revue (« memoria » → Revue) pour les activer.\n')
      } else {
        out.write('  Mémoire legacy adoptée directement en privé pour cette instance (active immédiatement).\n')
      }
      if (status.errors.length > 0) {
        out.write(`⚠ ${status.errors.length} erreur(s) non bloquante(s) pendant l’import :\n`)
        for (const e of status.errors.slice(0, 10)) out.write(`  - ${e}\n`)
        if (status.errors.length > 10) out.write(`  … et ${status.errors.length - 10} autre(s).\n`)
      }
      return 0
    } catch (err) {
      return fail(this.context.stderr, `import : ${(err as Error).message}`)
    }
  }
}

/** Ligne de progression : « 3/12 fichiers — 27 souvenirs ». */
function progressLine(status: ImportJobStatus): string {
  const p = status.progress
  return `${p.files_done}/${p.files_total} fichier(s) — ${p.facts_imported} souvenir(s)`
}
