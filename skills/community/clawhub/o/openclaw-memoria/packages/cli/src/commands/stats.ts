/**
 * `memoria stats` — compteurs globaux (souvenirs, bases, instances).
 */
import { Command, Option } from 'clipanion/lib/advanced/index.js'
import { fail, findAliveDaemon, resolveCommon, withLocalMemoria } from '../index.js'

interface StatsPayload {
  facts: number
  databases: number
  instances: number
}

export class StatsCommand extends Command {
  static override paths = [['stats']]
  static override usage = Command.Usage({
    description: 'Affiche les compteurs globaux : souvenirs, bases de données, instances.',
  })

  storageRoot = Option.String('--storage-root', { description: 'Racine du stockage (défaut : résolution standard)' })
  config = Option.String('--config', { description: 'Fichier de découverte (défaut : ~/.memoria/config.toml)' })

  override async execute(): Promise<number> {
    const opts = { storageRoot: this.storageRoot, configPath: this.config }
    const out = this.context.stdout
    try {
      const { storageRoot } = resolveCommon(opts)
      const daemon = await findAliveDaemon(opts)
      let stats: StatsPayload
      if (daemon) {
        stats = (await daemon.client.stats()) as StatsPayload
      } else {
        out.write('⚠ note : daemon arrêté — lecture locale directe\n')
        stats = withLocalMemoria(opts, memoria => memoria.stats())
      }
      out.write(`Statistiques Memoria — ${storageRoot}\n`)
      out.write(`  Souvenirs : ${stats.facts}\n`)
      out.write(`  Bases     : ${stats.databases}\n`)
      out.write(`  Instances : ${stats.instances}\n`)
      return 0
    } catch (err) {
      return fail(this.context.stderr, `stats : ${(err as Error).message}`)
    }
  }
}
