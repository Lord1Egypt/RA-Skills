#!/usr/bin/env node
/**
 * `memoria-mcp connect | serve` — point d'entrée CLI.
 * `serve` parle MCP (JSON-RPC) sur stdout : tout message humain part sur stderr.
 */
import { parseArgs } from 'node:util'
import { connect } from './connect.js'
import { disconnect } from './disconnect.js'
import { serve } from './serve.js'

const HELP = `memoria-mcp — connecte un agent (Claude Code, Codex…) à la mémoire Memoria

Usage :
  memoria-mcp connect --code XXXX-XXXX [--no-register] [--storage-root <chemin>]
      Échange le code de pairing contre un token d'instance, le sauvegarde, PUIS
      enregistre AUTOMATIQUEMENT le serveur MCP auprès de ton agent (Claude Code,
      Codex, OpenClaw). Une seule commande, rien d'autre. --no-register affiche
      l'enregistrement manuel sans l'appliquer.

  memoria-mcp disconnect [--instance <id>] [--storage-root <chemin>]
      Déconnexion complète : retire le serveur MCP de la config de l'agent,
      révoque l'instance côté daemon, supprime les credentials locaux. Sans
      --instance : déconnecte l'unique agent connu.

  memoria-mcp serve --instance <id> [--storage-root <chemin>]
      Démarre le serveur MCP stdio de cet agent (lancé par Claude Code/Codex,
      pas à la main). Relaye memoria_recall / memoria_store_fact /
      memoria_capture_turn / memoria_set_context vers le daemon local.

Options :
  --code <XXXX-XXXX>        code de pairing one-shot (connect)
  --no-register             ne pas enregistrer auto le serveur MCP (connect)
  --instance <id>           identifiant d'instance (serve / disconnect)
  --storage-root <chemin>   racine de stockage Memoria (défaut : config.toml)
  -h, --help                cette aide
`

const [command, ...rest] = process.argv.slice(2)

switch (command) {
  case 'connect': {
    const { values } = parseArgs({
      args: rest,
      options: {
        code: { type: 'string' },
        register: { type: 'boolean', default: true },
        'storage-root': { type: 'string' },
      },
    })
    if (!values.code) {
      console.error('memoria-mcp connect : --code XXXX-XXXX requis (affiché par l’UI Memoria)')
      process.exit(2)
    }
    try {
      const result = await connect({ code: values.code, register: values.register, storageRoot: values['storage-root'] })
      console.log(result.message)
    } catch (err) {
      console.error(`memoria-mcp connect : ${(err as Error).message}`)
      process.exit(1)
    }
    break
  }

  case 'disconnect': {
    const { values } = parseArgs({
      args: rest,
      options: {
        instance: { type: 'string' },
        'storage-root': { type: 'string' },
      },
    })
    try {
      const result = await disconnect({ instanceId: values.instance, storageRoot: values['storage-root'] })
      console.log(result.message)
    } catch (err) {
      console.error(`memoria-mcp disconnect : ${(err as Error).message}`)
      process.exit(1)
    }
    break
  }

  case 'serve': {
    const { values } = parseArgs({
      args: rest,
      options: {
        instance: { type: 'string' },
        'storage-root': { type: 'string' },
      },
    })
    if (!values.instance) {
      console.error('memoria-mcp serve : --instance <id> requis (voir memoria-mcp connect)')
      process.exit(2)
    }
    try {
      await serve({ instanceId: values.instance, storageRoot: values['storage-root'] })
    } catch (err) {
      console.error(`memoria-mcp serve : ${(err as Error).message}`)
      process.exit(1)
    }
    break
  }

  case undefined:
  case 'help':
  case '--help':
  case '-h':
    console.log(HELP)
    break

  default:
    console.error(`memoria-mcp : commande inconnue « ${command} »\n`)
    console.error(HELP)
    process.exit(2)
}
