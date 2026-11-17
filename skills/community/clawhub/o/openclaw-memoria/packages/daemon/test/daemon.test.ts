/**
 * Tests daemon : santé, auth 3 niveaux, pairing bout-en-bout par HTTP,
 * singleton lock-file. DoD P1 : « daemon démarre en singleton ».
 */
import { mkdtempSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { afterEach, beforeEach, describe, expect, it } from 'vitest'
import { DaemonClient, startDaemon, type RunningDaemon } from '../src/index.js'

let root: string
let daemon: RunningDaemon

beforeEach(async () => {
  root = mkdtempSync(join(tmpdir(), 'memoria-daemon-'))
  daemon = await startDaemon({ storageRoot: root, configPath: join(root, 'config.toml') })
})

afterEach(async () => {
  await daemon.close()
  rmSync(root, { recursive: true, force: true })
})

describe('daemon', () => {
  it('répond au health check', async () => {
    const client = new DaemonClient(daemon.state)
    const health = await client.health()
    expect(health?.ok).toBe(true)
    expect(health?.daemon_id).toBe(daemon.state.daemon_id)
  })

  it('singleton : un second daemon sur le même storage_root est refusé', async () => {
    await expect(startDaemon({ storageRoot: root, configPath: join(root, 'config.toml') })).rejects.toThrow(/déjà/)
  })

  it('admin sans token → 401 ; avec token → OK', async () => {
    const anonymous = new DaemonClient(daemon.state)
    await expect(anonymous.stats()).rejects.toThrow(/401/)

    const admin = new DaemonClient(daemon.state, daemon.state.admin_token)
    const stats = (await admin.stats()) as { instances: number }
    expect(stats.instances).toBe(0)
  })

  it('flux complet par HTTP : pair → complete → store → recall', async () => {
    const admin = new DaemonClient(daemon.state, daemon.state.admin_token)
    const paired = await admin.pair('claude-code', 'Claude Code')
    expect(paired.pairing_code).toBeTruthy()

    // l'agent échange son code (sans aucun token)
    const anonymous = new DaemonClient(daemon.state)
    const done = await anonymous.completePairing(paired.pairing_code)
    expect(done.instance_token).toBeTruthy()

    // puis utilise son token d'instance
    const agent = new DaemonClient(daemon.state, done.instance_token)
    await agent.storeFact({ content: 'le mot de passe wifi du studio est dans le coffre', category: 'infra' })
    const recall = await agent.recall({ query: 'wifi studio' })
    expect(recall.items.length).toBe(1)

    // un token bidon est rejeté
    const intruder = new DaemonClient(daemon.state, 'token-bidon')
    await expect(intruder.recall({ query: 'wifi' })).rejects.toThrow(/401/)
  })

  it('révocation par l’admin coupe l’agent', async () => {
    const admin = new DaemonClient(daemon.state, daemon.state.admin_token)
    const paired = await admin.pair('codex')
    const done = await new DaemonClient(daemon.state).completePairing(paired.pairing_code)
    const agent = new DaemonClient(daemon.state, done.instance_token)
    await agent.storeFact({ content: 'note temporaire' })

    await admin.revoke(paired.assistant_instance_id)
    await expect(agent.recall({ query: 'note' })).rejects.toThrow(/401/)
  })
})
