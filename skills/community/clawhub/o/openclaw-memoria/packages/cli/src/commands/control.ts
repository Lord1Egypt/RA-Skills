/**
 * Commandes de contrôle (spec §2.1, panneau Réglages) :
 *  - `memoria enable` / `memoria disable` : kill-switch global (pause Memoria).
 *  - `memoria autostart [on|off]`         : lancement auto au login (launchd).
 *  - `memoria move --to <chemin>`         : déplace TOUTE la mémoire (clé USB).
 *
 * Toutes passent par le daemon vivant quand il existe ; `move` exige au
 * contraire un daemon ARRÊTÉ (les DB ne peuvent être déplacées ouvertes) et
 * l'arrête lui-même proprement avant de bouger les fichiers.
 */
import { Command, Option } from 'clipanion/lib/advanced/index.js'
import { autostartStatus, disableAutostart, enableAutostart, moveStorage, setEnabled } from '@memoria/core'
import { currentVersion, daemonBinPath, pullAndBuild, readDaemonState, scheduleRestart } from '@memoria/daemon'
import { fail, findAliveDaemon, resolveCommon } from '../index.js'

function pidAlive(pid: number): boolean {
  try {
    process.kill(pid, 0)
    return true
  } catch {
    return false
  }
}

export class EnableCommand extends Command {
  static override paths = [['enable']]
  static override usage = Command.Usage({ description: 'Réactive Memoria (lève la pause : capture et recall reprennent).' })
  storageRoot = Option.String('--storage-root', { description: 'Racine du stockage' })
  config = Option.String('--config', { description: 'Fichier de découverte' })

  override async execute(): Promise<number> {
    const opts = { storageRoot: this.storageRoot, configPath: this.config }
    try {
      const daemon = await findAliveDaemon(opts)
      if (daemon) await daemon.client.setEnabled(true)
      else setEnabled(true, resolveCommon(opts).configPath)
      this.context.stdout.write('✓ Memoria activé.\n')
      return 0
    } catch (err) {
      return fail(this.context.stderr, `enable : ${(err as Error).message}`)
    }
  }
}

export class DisableCommand extends Command {
  static override paths = [['disable']]
  static override usage = Command.Usage({
    description: 'Met Memoria en pause : le daemon reste joignable mais ne lit ni n’écrit plus de mémoire.',
  })
  storageRoot = Option.String('--storage-root', { description: 'Racine du stockage' })
  config = Option.String('--config', { description: 'Fichier de découverte' })

  override async execute(): Promise<number> {
    const opts = { storageRoot: this.storageRoot, configPath: this.config }
    try {
      const daemon = await findAliveDaemon(opts)
      if (daemon) await daemon.client.setEnabled(false)
      else setEnabled(false, resolveCommon(opts).configPath)
      this.context.stdout.write('✓ Memoria en pause (capture et recall suspendus). « memoria enable » pour reprendre.\n')
      return 0
    } catch (err) {
      return fail(this.context.stderr, `disable : ${(err as Error).message}`)
    }
  }
}

export class AutostartCommand extends Command {
  static override paths = [['autostart']]
  static override usage = Command.Usage({
    description: 'Lancement automatique au login (launchd). « on » installe, « off » retire, sans argument affiche l’état.',
  })
  mode = Option.String({ required: false })
  storageRoot = Option.String('--storage-root', { description: 'Racine du stockage' })
  config = Option.String('--config', { description: 'Fichier de découverte' })

  override async execute(): Promise<number> {
    const out = this.context.stdout
    const opts = { storageRoot: this.storageRoot, configPath: this.config }
    try {
      if (this.mode === undefined) {
        const s = autostartStatus()
        if (!s.supported) out.write('Lancement auto : non pris en charge sur cette plateforme (macOS uniquement).\n')
        else out.write(`Lancement auto : ${s.installed ? 'installé' : 'absent'}${s.loaded ? ' (chargé)' : ''}\n  plist : ${s.plistPath}\n`)
        return 0
      }
      if (this.mode === 'on') {
        const { storageRoot } = resolveCommon(opts)
        const s = enableAutostart({
          programArguments: [process.execPath, daemonBinPath(), '--storage-root', storageRoot],
          workingDirectory: storageRoot,
        })
        out.write(`✓ Lancement auto installé — le daemon démarrera à chaque login.\n  plist : ${s.plistPath}\n`)
        return 0
      }
      if (this.mode === 'off') {
        disableAutostart()
        out.write('✓ Lancement auto retiré.\n')
        return 0
      }
      return fail(this.context.stderr, `autostart : argument « ${this.mode} » inconnu (attendu : on | off | rien).`)
    } catch (err) {
      return fail(this.context.stderr, `autostart : ${(err as Error).message}`)
    }
  }
}

export class UpdateCommand extends Command {
  static override paths = [['update']]
  static override usage = Command.Usage({
    description: 'Met Memoria à jour (git pull + build) et redémarre le daemon.',
  })
  storageRoot = Option.String('--storage-root', { description: 'Racine du stockage' })
  config = Option.String('--config', { description: 'Fichier de découverte' })

  override async execute(): Promise<number> {
    const out = this.context.stdout
    try {
      const v = await currentVersion()
      out.write(`Version actuelle : ${v.version}${v.sha ? ` (${v.sha})` : ''}\n`)
      if (!v.is_git) return fail(this.context.stderr, 'update : installation non-git — mets à jour via ton gestionnaire de paquets.')
      out.write('Téléchargement + reconstruction…\n')
      const r = await pullAndBuild()
      out.write(`${r.message}\n`)
      if (r.ok && r.changed) {
        const { storageRoot } = resolveCommon({ storageRoot: this.storageRoot, configPath: this.config })
        scheduleRestart(storageRoot)
        out.write('Le daemon redémarre dans quelques secondes (memoria stop && start).\n')
      }
      return r.ok ? 0 : 1
    } catch (err) {
      return fail(this.context.stderr, `update : ${(err as Error).message}`)
    }
  }
}

export class MoveCommand extends Command {
  static override paths = [['move']]
  static override usage = Command.Usage({
    description: 'Déplace TOUTE la mémoire vers un nouvel emplacement (ex. clé USB) et met à jour config.toml.',
    details: 'Le daemon est arrêté automatiquement (les DB ne peuvent bouger ouvertes), puis « memoria start » le relancera au nouvel emplacement.',
  })
  to = Option.String('--to', { required: true, description: 'Dossier de destination (vide ou inexistant)' })
  storageRoot = Option.String('--storage-root', { description: 'Racine du stockage source' })
  config = Option.String('--config', { description: 'Fichier de découverte' })

  override async execute(): Promise<number> {
    const out = this.context.stdout
    const opts = { storageRoot: this.storageRoot, configPath: this.config }
    try {
      const { storageRoot, configPath } = resolveCommon(opts)
      // 1) arrêter le daemon s'il vit (sinon DB ouvertes = déplacement risqué)
      const state = readDaemonState(storageRoot)
      if (state && pidAlive(state.pid)) {
        out.write(`Arrêt du daemon (pid ${state.pid}) avant déplacement…\n`)
        process.kill(state.pid, 'SIGTERM')
        const deadline = Date.now() + 5_000
        while (Date.now() < deadline && pidAlive(state.pid)) await new Promise(r => setTimeout(r, 100))
        if (pidAlive(state.pid)) return fail(this.context.stderr, `move : le daemon (pid ${state.pid}) ne s’est pas arrêté — réessaie après « memoria stop ».`)
      }
      // 2) déplacer + réécrire config.toml
      const { from, to } = moveStorage({ from: storageRoot, to: this.to, configPath })
      out.write(`✓ Mémoire déplacée :\n  de : ${from}\n  à  : ${to}\nconfig.toml mis à jour. Lance « memoria start » pour redémarrer au nouvel emplacement.\n`)
      return 0
    } catch (err) {
      return fail(this.context.stderr, `move : ${(err as Error).message}`)
    }
  }
}
