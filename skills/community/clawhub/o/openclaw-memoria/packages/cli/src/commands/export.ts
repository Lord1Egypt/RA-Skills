/**
 * `memoria export [--agent <type>]` — exporte la mémoire des agents en
 * fichiers Markdown lisibles (un par thème), sous `<stockage>/exports/<agent>/`.
 * Couche markdown-sync (20), opt-in. Fonctionne en local direct (lecture seule
 * pour l'agent : on écrit des .md, pas la DB).
 */
import { join } from 'node:path'
import { Command, Option } from 'clipanion/lib/advanced/index.js'
import { fail, resolveCommon, withLocalMemoria } from '../index.js'

export class ExportCommand extends Command {
  static override paths = [['export']]
  static override usage = Command.Usage({
    description: 'Exporte la mémoire des agents en fichiers Markdown (un par thème).',
  })

  agent = Option.String('--agent', { description: 'Limiter à un type d’agent (claude-code, codex, openclaw)' })
  flat = Option.Boolean('--flat', false, { description: 'Un seul MEMORY.md par agent (au lieu d’un fichier par thème)' })
  storageRoot = Option.String('--storage-root', { description: 'Racine du stockage' })
  config = Option.String('--config', { description: 'Fichier de découverte' })

  override async execute(): Promise<number> {
    const opts = { storageRoot: this.storageRoot, configPath: this.config }
    const out = this.context.stdout
    try {
      const { storageRoot } = resolveCommon(opts)
      return withLocalMemoria(opts, memoria => {
        const agents = memoria
          .listAgents()
          .filter(a => !a.instance.revoked_at && a.assistant_type !== 'generic')
          .filter(a => !this.agent || a.assistant_type === this.agent)
        if (agents.length === 0) {
          out.write('Aucun agent à exporter.\n')
          return 0
        }
        for (const a of agents) {
          const dir = join(storageRoot, 'exports', a.assistant_type)
          const r = memoria.exportMarkdown(a.instance.id, dir, !this.flat)
          out.write(`✓ ${a.assistant_type} : ${r.facts} souvenirs → ${r.files.length} fichier(s) dans ${dir}\n`)
        }
        return 0
      })
    } catch (err) {
      return fail(out, (err as Error).message)
    }
  }
}
