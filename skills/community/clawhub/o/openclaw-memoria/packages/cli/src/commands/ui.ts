/**
 * `memoria ui` — ouvre l'interface web dans le navigateur. C'est aussi la
 * commande PAR DÉFAUT : taper `memoria` sans argument fait la même chose
 * (l'aide reste accessible via `memoria --help` / `-h`, chemins explicites
 * du HelpCommand de clipanion).
 *
 * Si le daemon est arrêté, on le démarre comme `memoria start` (ensureDaemon
 * attend son health). L'URL est TOUJOURS affichée en clair : si l'ouverture
 * du navigateur échoue, on le dit et l'utilisateur copie l'URL — jamais
 * d'échec silencieux.
 */
import { spawn } from 'node:child_process'
import { Command, Option } from 'clipanion/lib/advanced/index.js'
import { ensureDaemon, type DaemonState } from '@memoria/daemon'
import { fail, findAliveDaemon, resolveCommon } from '../index.js'

/** Commande d'ouverture selon la plateforme : `open` macOS, `xdg-open` Linux. */
export function openerFor(platform: NodeJS.Platform): string {
  return platform === 'darwin' ? 'open' : 'xdg-open'
}

/**
 * Ouvre une URL dans le navigateur par défaut. Tout échec (binaire absent,
 * code de sortie non nul) est REJETÉ — c'est l'appelant qui décide quoi en
 * dire, rien n'est avalé. `opener` est injectable pour les tests.
 */
export function openInBrowser(url: string, opener: string = openerFor(process.platform)): Promise<void> {
  return new Promise((resolve, reject) => {
    const child = spawn(opener, [url], { stdio: 'ignore' })
    child.once('error', err => reject(new Error(`« ${opener} » indisponible : ${err.message}`)))
    child.once('exit', code => {
      if (code === 0) resolve()
      else reject(new Error(`« ${opener} » a échoué (code ${String(code)})`))
    })
  })
}

export class UiCommand extends Command {
  static override paths = [['ui'], Command.Default]
  static override usage = Command.Usage({
    description: 'Ouvre l’interface web de Memoria (commande par défaut : « memoria » seul fait pareil).',
    details: 'Démarre le daemon s’il est arrêté, construit l’adresse http://127.0.0.1:<port>/ui/ avec le token admin, l’affiche en clair puis l’ouvre dans le navigateur.',
    examples: [
      ['Ouvrir l’interface', 'memoria ui'],
      ['Pareil, en plus court', 'memoria'],
    ],
  })

  storageRoot = Option.String('--storage-root', { description: 'Racine du stockage (défaut : résolution standard)' })
  config = Option.String('--config', { description: 'Fichier de découverte (défaut : ~/.memoria/config.toml)' })

  /** Injectables pour les tests : ouverture navigateur + démarrage du daemon. */
  openUrl: (url: string) => Promise<void> = url => openInBrowser(url)
  ensureDaemonFn: typeof ensureDaemon = ensureDaemon

  override async execute(): Promise<number> {
    const out = this.context.stdout
    const opts = { storageRoot: this.storageRoot, configPath: this.config }
    try {
      const alive = await findAliveDaemon(opts)
      let state: DaemonState
      if (alive) {
        state = alive.state
      } else {
        out.write('Le service Memoria est arrêté — démarrage…\n')
        const { storageRoot } = resolveCommon(opts)
        state = await this.ensureDaemonFn({ storageRoot, configPath: opts.configPath })
        out.write(`✓ Daemon démarré sur 127.0.0.1:${state.port} (pid ${state.pid}).\n`)
      }

      const url = `http://127.0.0.1:${state.port}/ui/#token=${state.admin_token}`
      out.write(`Interface : ${url}\n`)
      try {
        await this.openUrl(url)
        out.write('✓ Interface ouverte dans le navigateur.\n')
      } catch (err) {
        // Pas une erreur fatale : l'URL est affichée au-dessus, on le DIT.
        out.write(`⚠ Ouverture automatique impossible (${(err as Error).message}) — copie l’adresse ci-dessus dans ton navigateur.\n`)
      }
      return 0
    } catch (err) {
      return fail(this.context.stderr, `ui : ${(err as Error).message}`)
    }
  }
}
