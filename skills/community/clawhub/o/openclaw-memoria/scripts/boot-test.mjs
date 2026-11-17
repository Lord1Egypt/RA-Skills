/**
 * Boot-test CI : démarre RÉELLEMENT le daemon sur un storage temporaire,
 * vérifie health + pairing bout-en-bout, puis s'arrête.
 * (Remplace l'ancien smoke test qui « skippait » les imports en échec.)
 */
import { mkdtempSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'

const { startDaemon } = await import('../packages/daemon/dist/index.js')

const root = mkdtempSync(join(tmpdir(), 'memoria-boot-'))
let exitCode = 0
try {
  const daemon = await startDaemon({ storageRoot: root, configPath: join(root, 'config.toml') })
  const res = await fetch(`http://127.0.0.1:${daemon.state.port}/v1/health`)
  const health = await res.json()
  if (!health.ok) throw new Error('health KO')

  // pairing bout-en-bout
  const pairRes = await fetch(`http://127.0.0.1:${daemon.state.port}/v1/admin/pair`, {
    method: 'POST',
    headers: { 'content-type': 'application/json', authorization: `Bearer ${daemon.state.admin_token}` },
    body: JSON.stringify({ type: 'generic' }),
  })
  const paired = await pairRes.json()
  if (!paired.pairing_code) throw new Error('pairing KO')

  const completeRes = await fetch(`http://127.0.0.1:${daemon.state.port}/v1/pairing/complete`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ code: paired.pairing_code }),
  })
  const done = await completeRes.json()
  if (!done.instance_token) throw new Error('complete pairing KO')

  await daemon.close()
  console.log('boot-test OK — daemon démarré, health vert, pairing complet')
} catch (err) {
  console.error('boot-test ÉCHEC :', err)
  exitCode = 1
} finally {
  rmSync(root, { recursive: true, force: true })
}
process.exit(exitCode)
