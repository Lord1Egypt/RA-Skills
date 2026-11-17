/**
 * `memoria daemon` — daemon au premier plan (Ctrl-C pour arrêter).
 * `memoria start`  — daemon détaché via ensureDaemon (réutilise un vivant).
 * `memoria stop`   — SIGTERM au PID de daemon.json + vérification de la mort.
 */
import { Command, Option } from 'clipanion/lib/advanced/index.js'
import { ensureDaemon, readDaemonState, startDaemon } from '@memoria/daemon'
import { fail, resolveCommon } from '../index.js'

/** `kill(pid, 0)` : l'échec EST l'information (process mort) — pas un cas d'erreur. */
function pidAlive(pid: number): boolean {
  try {
    process.kill(pid, 0)
    return true
  } catch {
    return false
  }
}

export class DaemonCommand extends Command {
  static override paths = [['daemon']]
  static override usage = Command.Usage({
    description: 'Démarre le daemon Memoria au premier plan (Ctrl-C pour arrêter).',
  })

  storageRoot = Option.String('--storage-root', { description: 'Racine du stockage (défaut : résolution standard)' })
  config = Option.String('--config', { description: 'Fichier de découverte (défaut : ~/.memoria/config.toml)' })
  port = Option.String('--port', { description: 'Port d’écoute (défaut : éphémère, persisté dans daemon.json)' })

  override async execute(): Promise<number> {
    const out = this.context.stdout
    let port: number | undefined
    if (this.port !== undefined) {
      port = Number.parseInt(this.port, 10)
      if (!Number.isFinite(port) || port < 0 || port > 65535) {
        return fail(this.context.stderr, `daemon : port invalide « ${this.port} »`)
      }
    }
    try {
      const running = await startDaemon({
        storageRoot: this.storageRoot,
        configPath: this.config,
        ...(port !== undefined ? { port } : {}),
      })
      out.write(`Daemon Memoria prêt sur 127.0.0.1:${running.state.port} (stockage : ${running.memoria.paths.root})\n`)
      out.write('Ctrl-C pour arrêter.\n')
      await new Promise<void>(resolve => {
        process.once('SIGINT', () => resolve())
        process.once('SIGTERM', () => resolve())
      })
      await running.close()
      out.write('Daemon arrêté proprement.\n')
      return 0
    } catch (err) {
      return fail(this.context.stderr, `daemon : ${(err as Error).message}`)
    }
  }
}

export class StartCommand extends Command {
  static override paths = [['start']]
  static override usage = Command.Usage({
    description: 'Démarre le daemon en arrière-plan (réutilise un daemon déjà vivant).',
  })

  storageRoot = Option.String('--storage-root', { description: 'Racine du stockage (défaut : résolution standard)' })
  config = Option.String('--config', { description: 'Fichier de découverte (défaut : ~/.memoria/config.toml)' })

  override async execute(): Promise<number> {
    const out = this.context.stdout
    const opts = { storageRoot: this.storageRoot, configPath: this.config }
    try {
      const { storageRoot } = resolveCommon(opts)
      const before = readDaemonState(storageRoot)
      const alreadyAlive = before !== null && pidAlive(before.pid)

      const state = await ensureDaemon({ storageRoot, configPath: opts.configPath })
      if (alreadyAlive && before !== null && before.pid === state.pid) {
        out.write(`Daemon déjà actif sur 127.0.0.1:${state.port} (pid ${state.pid}).\n`)
      } else {
        out.write(`Daemon démarré sur 127.0.0.1:${state.port} (pid ${state.pid}).\n`)
      }
      return 0
    } catch (err) {
      return fail(this.context.stderr, `start : ${(err as Error).message}`)
    }
  }
}

export class StopCommand extends Command {
  static override paths = [['stop']]
  static override usage = Command.Usage({
    description: 'Arrête le daemon (SIGTERM au PID de daemon.json, avec vérification).',
  })

  storageRoot = Option.String('--storage-root', { description: 'Racine du stockage (défaut : résolution standard)' })
  config = Option.String('--config', { description: 'Fichier de découverte (défaut : ~/.memoria/config.toml)' })

  override async execute(): Promise<number> {
    const out = this.context.stdout
    const { storageRoot } = resolveCommon({ storageRoot: this.storageRoot, configPath: this.config })

    const state = readDaemonState(storageRoot)
    if (!state) {
      out.write(`Aucun daemon enregistré pour ${storageRoot} (pas de daemon.json) — rien à arrêter.\n`)
      return 0
    }
    if (!pidAlive(state.pid)) {
      out.write(`Le daemon (pid ${state.pid}) est déjà arrêté — daemon.json était périmé.\n`)
      return 0
    }

    try {
      process.kill(state.pid, 'SIGTERM')
    } catch (err) {
      return fail(this.context.stderr, `stop : impossible d’envoyer SIGTERM au pid ${state.pid} : ${(err as Error).message}`)
    }

    // Vérification : on attend la mort réelle du process (jusqu'à 5 s).
    const deadline = Date.now() + 5_000
    while (Date.now() < deadline) {
      await new Promise(resolve => setTimeout(resolve, 100))
      if (!pidAlive(state.pid)) {
        out.write(`✓ Daemon arrêté (pid ${state.pid}).\n`)
        return 0
      }
    }
    return fail(
      this.context.stderr,
      `stop : le daemon (pid ${state.pid}) ne s’est pas arrêté après SIGTERM (5 s) — en dernier recours : kill -9 ${state.pid}`,
    )
  }
}
