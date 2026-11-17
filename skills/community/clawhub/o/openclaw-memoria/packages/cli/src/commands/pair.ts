/**
 * `memoria pair <type> [--name …]` — crée une instance d'assistant et affiche
 * le code de pairing (TTL 10 min) + la commande à coller dans le chat de
 * l'agent. Démarre le daemon si besoin (le pairing se termine par HTTP).
 */
import { Command, Option } from 'clipanion/lib/advanced/index.js'
import type { AssistantType } from '@memoria/core'
import { DaemonClient, ensureDaemon } from '@memoria/daemon'
import { fail } from '../index.js'

const ASSISTANT_TYPES: readonly AssistantType[] = ['claude-code', 'codex', 'openclaw', 'cursor', 'robot', 'generic']

export class PairCommand extends Command {
  static override paths = [['pair']]
  static override usage = Command.Usage({
    description: 'Connecte un nouvel agent : génère un code de pairing à coller dans son chat.',
    examples: [
      ['Connecter Claude Code', 'memoria pair claude-code'],
      ['Avec un nom affiché', 'memoria pair codex --name "Codex MacBook"'],
    ],
  })

  type = Option.String({ required: true })
  name = Option.String('--name', { description: 'Nom affiché de l’assistant' })
  storageRoot = Option.String('--storage-root', { description: 'Racine du stockage (défaut : résolution standard)' })
  config = Option.String('--config', { description: 'Fichier de découverte (défaut : ~/.memoria/config.toml)' })

  override async execute(): Promise<number> {
    const out = this.context.stdout
    if (!(ASSISTANT_TYPES as readonly string[]).includes(this.type)) {
      return fail(
        this.context.stderr,
        `pair : type inconnu « ${this.type} » — types valides : ${ASSISTANT_TYPES.join(', ')}`,
      )
    }
    try {
      const state = await ensureDaemon({ storageRoot: this.storageRoot, configPath: this.config })
      const client = new DaemonClient(state, state.admin_token)
      const paired = await client.pair(this.type, this.name)

      out.write('\n')
      out.write(frame([
        `Code de pairing : ${paired.pairing_code}`,
        'Expire dans 10 minutes (usage unique)',
      ]))
      out.write('\nColle cette commande dans le chat de l’agent :\n\n')
      out.write(`  ${paired.command}\n\n`)
      out.write(`Instance créée : ${paired.assistant_instance_id}\n`)
      out.write('Une fois le code échangé, l’agent apparaît dans « memoria agents ».\n')
      return 0
    } catch (err) {
      return fail(this.context.stderr, `pair : ${(err as Error).message}`)
    }
  }
}

/** Cadre ASCII propre (pas de dépendance couleur, largeur calculée). */
function frame(lines: string[]): string {
  const width = Math.max(...lines.map(l => l.length))
  const top = `+${'-'.repeat(width + 4)}+\n`
  const body = lines.map(l => `|  ${l.padEnd(width)}  |\n`).join('')
  return `${top}${body}${top}`
}
