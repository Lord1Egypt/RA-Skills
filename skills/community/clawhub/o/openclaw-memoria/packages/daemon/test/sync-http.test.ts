/**
 * Synchro inter-machines SUR HTTP RÉEL : deux daemons (hub + spoke) dans le même
 * process, reliés par de vraies sockets. Valide le listener LAN, le pairing, la
 * bootstrap, le pull, ET la régression anti-DNS-rebinding (admin/memory jamais
 * servis sur le port LAN).
 */
import { mkdtempSync, rmSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { afterEach, beforeEach, describe, expect, it } from 'vitest'
import { startDaemon, type RunningDaemon } from '../src/index.js'

const LAN_PORT = 47733
let dir: string
let hub: RunningDaemon
let spoke: RunningDaemon
let orgScopeId: string

beforeEach(async () => {
  dir = mkdtempSync(join(tmpdir(), 'memoria-synchttp-'))
  const hubRoot = join(dir, 'hub')
  const spokeRoot = join(dir, 'spoke')
  // config hub : listener LAN sur 127.0.0.1:LAN_PORT
  writeFileSync(join(dir, 'hub.toml'), `[sync]\nenabled = true\nrole = "hub"\nlisten_lan = "127.0.0.1:${LAN_PORT}"\nscopes = ["org"]\n`)
  writeFileSync(join(dir, 'spoke.toml'), `[sync]\nenabled = true\nrole = "spoke"\nscopes = ["org"]\n`)

  hub = await startDaemon({ storageRoot: hubRoot, configPath: join(dir, 'hub.toml') })
  spoke = await startDaemon({ storageRoot: spokeRoot, configPath: join(dir, 'spoke.toml') })

  // un fait partagé sur le hub (scope org)
  const a = hub.memoria.pairAssistant({ type: 'openclaw', display_name: 'Koda' })
  const own = hub.memoria.registry.ownCompany()!
  const orgScope = hub.memoria.registry.getScopeByName(`org:${own.id}`)!
  orgScopeId = orgScope.id
  hub.memoria.setScopeAccess(a.assistant_id, orgScope.id, { can_read: true, can_write: true })
  hub.memoria.storeFact({ instance: a.assistant_instance_id, scope: orgScope.id, content: 'Commande de déploiement bureau-primobot : git config user Hello-Primo' })
  // laisser le listener LAN se lier
  await new Promise(r => setTimeout(r, 200))
})

afterEach(async () => {
  await hub.close()
  await spoke.close()
  rmSync(dir, { recursive: true, force: true })
})

describe('synchro sur HTTP réel', () => {
  it('le spoke s’appaire au hub sur le LAN et récupère le fait partagé', async () => {
    const inv = hub.memoria.sync.invite('Luna (iMac)')
    const report = await spoke.memoria.sync.join({ hub: `127.0.0.1:${LAN_PORT}`, code: inv.code })
    expect(report.facts).toBeGreaterThanOrEqual(1)

    const local = spoke.memoria.sharedContentStore(orgScopeId)!
    const rows = local.db.prepare('SELECT fact FROM facts WHERE scope_id = ?').all(orgScopeId) as Array<{ fact: string }>
    expect(rows.some(r => /bureau-primobot/.test(r.fact))).toBe(true)
  })

  it('une nouveauté du hub est tirée ensuite par le spoke', async () => {
    await spoke.memoria.sync.join({ hub: `127.0.0.1:${LAN_PORT}`, code: hub.memoria.sync.invite().code })
    const a = hub.memoria.listAgents().find(x => x.assistant_type === 'openclaw')!
    hub.memoria.storeFact({ instance: a.instance.id, scope: orgScopeId, content: 'Le mot de passe du NAS tourne tous les 90 jours' })
    const r = await spoke.memoria.sync.pull(orgScopeId)
    expect(r.applied).toBeGreaterThanOrEqual(1)
  })

  it('régression anti-rebinding : /v1/admin et /v1/memory refusés sur le port LAN', async () => {
    const admin = await fetch(`http://127.0.0.1:${LAN_PORT}/v1/admin/stats`)
    expect(admin.status).toBe(403)
    const mem = await fetch(`http://127.0.0.1:${LAN_PORT}/v1/memory/recall`, { method: 'POST', body: '{}' })
    expect(mem.status).toBe(403)
  })

  it('une requête de synchro sans signature est refusée (401)', async () => {
    const res = await fetch(`http://127.0.0.1:${LAN_PORT}/v1/sync/pull?scope=${encodeURIComponent(orgScopeId)}&since=0`)
    expect(res.status).toBe(401)
  })
})
