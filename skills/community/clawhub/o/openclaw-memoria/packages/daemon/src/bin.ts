#!/usr/bin/env node
/**
 * `memoria-daemon [--storage-root <path>] [--port <n>]`
 * Processus de premier plan ; lancé détaché par ensureDaemon()/npx/app bureau.
 */
import { parseArgs } from 'node:util'
import { startDaemon } from './server.js'

const { values } = parseArgs({
  options: {
    'storage-root': { type: 'string' },
    port: { type: 'string' },
  },
})

const running = await startDaemon({
  storageRoot: values['storage-root'],
  port: values.port ? Number.parseInt(values.port, 10) : 0,
})

// eslint-disable-next-line no-console
console.log(`memoria-daemon prêt sur 127.0.0.1:${running.state.port} (storage: ${running.memoria.paths.root})`)

const shutdown = (): void => {
  void running.close().then(() => process.exit(0))
}
process.on('SIGINT', shutdown)
process.on('SIGTERM', shutdown)
