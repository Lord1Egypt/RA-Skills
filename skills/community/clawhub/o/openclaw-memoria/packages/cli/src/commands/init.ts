/**
 * `memoria init` — crée config.toml + l'arborescence, démarre le daemon,
 * affiche les prochaines étapes (pair, UI web).
 */
import { existsSync } from 'node:fs'
import { Command, Option } from 'clipanion/lib/advanced/index.js'
import {
  DEFAULT_CONFIG_PATH,
  ensureStorageTree,
  loadConfigFile,
  resolveStorageRoot,
  saveConfigFile,
} from '@memoria/core'
import { ensureDaemon } from '@memoria/daemon'
import { fail } from '../index.js'

export class InitCommand extends Command {
  static override paths = [['init']]
  static override usage = Command.Usage({
    description: 'Initialise Memoria : config.toml, arborescence de stockage, daemon.',
    examples: [
      ['Initialisation standard (~/.memoria/data)', 'memoria init'],
      ['Stockage sur un autre volume', 'memoria init --storage-root /Volumes/Data/memoria'],
    ],
  })

  storageRoot = Option.String('--storage-root', { description: 'Racine du stockage (défaut : ~/.memoria/data)' })
  config = Option.String('--config', { description: 'Fichier de découverte (défaut : ~/.memoria/config.toml)' })

  override async execute(): Promise<number> {
    const out = this.context.stdout
    try {
      const configPath = this.config ?? DEFAULT_CONFIG_PATH
      const resolved = resolveStorageRoot({ storageRoot: this.storageRoot, configPath })
      const existing = existsSync(configPath) ? loadConfigFile(configPath) : null

      // storage_path persisté = tous les clients (MCP, UI, daemon) retrouvent la même racine.
      if (!existing || existing.storage_path !== resolved.storageRoot) {
        saveConfigFile({ ...(existing ?? {}), storage_path: resolved.storageRoot }, configPath)
        out.write(`✓ config écrite : ${configPath}\n`)
      } else {
        out.write(`✓ config existante : ${configPath}\n`)
      }

      ensureStorageTree(resolved.storageRoot)
      out.write(`✓ stockage prêt : ${resolved.storageRoot}\n`)

      const state = await ensureDaemon({ storageRoot: resolved.storageRoot, configPath })
      out.write(`✓ daemon actif : 127.0.0.1:${state.port} (pid ${state.pid})\n`)

      out.write('\nProchaines étapes :\n')
      out.write('  1. memoria pair claude-code   — connecter un premier agent (code à coller)\n')
      out.write('  2. npx @memoria/web           — ouvrir l’interface web\n')
      out.write('  3. memoria doctor             — vérifier la santé du stockage\n')
      return 0
    } catch (err) {
      return fail(this.context.stderr, `init : ${(err as Error).message}`)
    }
  }
}
