/**
 * Synchro incréments 2-5 — bout-en-bout EN MÉMOIRE (sans daemon HTTP réel).
 * Un FetchLike simule les routes /v1/sync/* du hub : pairing+HMAC, pull/push,
 * snapshot, secrets. Prouve : pairing, auth (token/HMAC/rejeu), convergence
 * des faits Koda↔Luna, et le COFFRE inter-machines (valeur descellée chez Luna).
 */
import { mkdtempSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { afterEach, beforeEach, describe, expect, it } from 'vitest'
import { Memoria, type FetchLike } from '../src/index.js'

/**
 * Route un FetchLike vers le SyncEngine du hub, en imitant exactement ce que
 * fera le daemon : pas d'auth sur /pairing/complete, auth (token+HMAC+nonce)
 * sur le reste. `path` (avec query) = ce qui a été signé côté spoke.
 */
function hubFetch(hub: Memoria): FetchLike {
  return async (url, init) => {
    const u = new URL(url)
    const path = u.pathname + u.search
    const body = init.body ?? ''
    const json = (status: number, payload: unknown) => ({ ok: status < 400, status, json: async () => payload })
    try {
      if (u.pathname === '/v1/sync/pairing/complete' && init.method === 'POST') {
        return json(200, hub.sync.completePairing(JSON.parse(body) as never))
      }
      // routes authentifiées
      const h = init.headers ?? {}
      const peer = hub.sync.authenticate(
        (h['authorization'] ?? '').replace(/^Bearer\s+/, ''),
        h['x-memoria-sig'],
        { method: init.method, path, body, ts: h['x-memoria-ts'] ?? '', nonce: h['x-memoria-nonce'] ?? '' },
      )
      void peer
      if (u.pathname === '/v1/sync/snapshot') {
        return json(200, hub.sync.snapshot(u.searchParams.get('scope')!, u.searchParams.get('since') ?? undefined))
      }
      if (u.pathname === '/v1/sync/pull') {
        return json(200, hub.sync.collectDelta(u.searchParams.get('scope')!, u.searchParams.get('since') ?? '1970-01-01T00:00:00.000Z'))
      }
      if (u.pathname === '/v1/sync/push') {
        const b = JSON.parse(body) as { scope_id: string; facts: never[]; tombstones: never[] }
        return json(200, hub.sync.applyIncoming(b.scope_id, b.facts, b.tombstones))
      }
      if (u.pathname === '/v1/sync/secrets') {
        const secrets = hub.sync.serveSecrets(u.searchParams.get('scope')!).map(s => ({ name: s.name, env: s.env }))
        return json(200, { secrets })
      }
      return json(404, { error: 'route inconnue' })
    } catch (err) {
      return json(401, { error: (err as Error).message })
    }
  }
}

let dir: string
let hub: Memoria
let spoke: Memoria
let orgScopeId: string
let hubAddr: string

beforeEach(() => {
  dir = mkdtempSync(join(tmpdir(), 'memoria-sync-'))
  hub = Memoria.init({
    storageRoot: join(dir, 'hub'),
    configPath: join(dir, 'hub.toml'),
    llm: { extraction: null },
  })
  spoke = Memoria.init({
    storageRoot: join(dir, 'spoke'),
    configPath: join(dir, 'spoke.toml'),
    llm: { extraction: null },
  })
  // le hub a un scope org partagé avec un fait + une politique d'écriture pour son agent
  const a = hub.pairAssistant({ type: 'openclaw', display_name: 'Koda' })
  const own = hub.registry.ownCompany()!
  const orgScope = hub.registry.getScopeByName(`org:${own.id}`)!
  orgScopeId = orgScope.id
  hub.setScopeAccess(a.assistant_id, orgScope.id, { can_read: true, can_write: true })
  hub.storeFact({ instance: a.assistant_instance_id, scope: orgScope.id, content: 'Déploiement bureau-primobot : git config user Hello-Primo avant commit' })
  // configurer le rôle hub
  ;(hub as unknown as { resolved: { config: { sync?: unknown } } }).resolved.config.sync = { role: 'hub', listen_lan: '0.0.0.0:47600', scopes: ['org'] }
  ;(spoke as unknown as { resolved: { config: { sync?: unknown } } }).resolved.config.sync = { role: 'spoke', scopes: ['org'] }
  hubAddr = '192.168.1.20:47600'
})

afterEach(() => {
  hub.close()
  spoke.close()
  rmSync(dir, { recursive: true, force: true })
})

describe('pairing + bootstrap', () => {
  it('le spoke s’appaire, descelle les clés et récupère les faits partagés du hub', async () => {
    const inv = hub.sync.invite('Luna (iMac)')
    expect(inv.code).toMatch(/^[A-Z0-9]{4}-[A-Z0-9]{4}$/)

    const report = await spoke.sync.join({ hub: hubAddr, code: inv.code, fetchImpl: hubFetch(hub) })
    expect(report.facts).toBeGreaterThanOrEqual(1)

    // le fait de Koda est arrivé dans la copie locale de Luna
    const local = spoke.sharedContentStore(orgScopeId)!
    const got = local.db.prepare("SELECT fact FROM facts WHERE scope_id = ?").all(orgScopeId) as Array<{ fact: string }>
    expect(got.some(f => /bureau-primobot/.test(f.fact))).toBe(true)
  })

  it('un code invalide est refusé', async () => {
    hub.sync.invite()
    await expect(spoke.sync.join({ hub: hubAddr, code: 'AAAA-BBBB', fetchImpl: hubFetch(hub) })).rejects.toThrow()
  })
})

describe('pull / push (convergence Koda↔Luna)', () => {
  it('un nouveau fait du hub est tiré par le spoke', async () => {
    await spoke.sync.join({ hub: hubAddr, code: hub.sync.invite().code, fetchImpl: hubFetch(hub) })
    // le hub apprend un nouveau fait
    const a = hub.listAgents().find(x => x.assistant_type === 'openclaw')!
    hub.storeFact({ instance: a.instance.id, scope: orgScopeId, content: 'Le mot de passe du NAS QNAP tourne tous les 90 jours' })

    const r = await spoke.sync.pull(orgScopeId, hubFetch(hub))
    expect(r.applied).toBeGreaterThanOrEqual(1)
    const local = spoke.sharedContentStore(orgScopeId)!
    const got = local.db.prepare('SELECT fact FROM facts WHERE scope_id = ?').all(orgScopeId) as Array<{ fact: string }>
    expect(got.some(f => /NAS QNAP/.test(f.fact))).toBe(true)
  })

  it('un fait écrit côté spoke est poussé vers le hub', async () => {
    await spoke.sync.join({ hub: hubAddr, code: hub.sync.invite().code, fetchImpl: hubFetch(hub) })
    // Luna doit pouvoir écrire dans le scope org : on lui donne une instance + policy
    const la = spoke.pairAssistant({ type: 'openclaw', display_name: 'Luna' })
    spoke.setScopeAccess(la.assistant_id, orgScopeId, { can_read: true, can_write: true })
    spoke.storeFact({ instance: la.assistant_instance_id, scope: orgScopeId, content: 'Luna a généré le visuel Instagram du 14 juin' })

    const r = await spoke.sync.push(orgScopeId, hubFetch(hub))
    expect(r.applied).toBeGreaterThanOrEqual(1)
    const hubStore = hub.sharedContentStore(orgScopeId)!
    const got = hubStore.db.prepare('SELECT fact FROM facts WHERE scope_id = ?').all(orgScopeId) as Array<{ fact: string }>
    expect(got.some(f => /visuel Instagram/.test(f.fact))).toBe(true)
  })

  it('pull idempotent : un 2e pull immédiat n’applique rien', async () => {
    await spoke.sync.join({ hub: hubAddr, code: hub.sync.invite().code, fetchImpl: hubFetch(hub) })
    const a = hub.listAgents().find(x => x.assistant_type === 'openclaw')!
    hub.storeFact({ instance: a.instance.id, scope: orgScopeId, content: 'fait à tirer une seule fois' })
    await spoke.sync.pull(orgScopeId, hubFetch(hub))
    const second = await spoke.sync.pull(orgScopeId, hubFetch(hub))
    expect(second.applied).toBe(0)
  })
})

describe('coffre inter-machines', () => {
  it('un secret partagé sur le hub est descellé localement chez le spoke (jamais en clair sur le réseau)', async () => {
    // le hub référence un secret + le scelle en enveloppe GVK, syncable
    hub.registry.upsertSecretRef('nas-admin-password', 'aes-vault:memoria/nas-admin-password', 'generic-token')
    const refId = (hub.registry.db.prepare('SELECT id FROM secret_refs WHERE name = ?').get('nas-admin-password') as { id: string }).id
    hub.sync.shareSecret(refId, orgScopeId, 'S3cr3t-NAS-Koda', { syncable: true })

    // les enveloppes servies ne contiennent JAMAIS le plaintext
    const served = hub.sync.serveSecrets(orgScopeId)
    expect(JSON.stringify(served)).not.toContain('S3cr3t-NAS-Koda')

    // au bootstrap, Luna déchiffre avec la GVK reçue et range la valeur dans SON coffre
    await spoke.sync.join({ hub: hubAddr, code: hub.sync.invite().code, fetchImpl: hubFetch(hub) })
    expect(spoke.secrets.get('nas-admin-password')).toBe('S3cr3t-NAS-Koda')
  })
})

describe('sécurité de l’auth', () => {
  it('un mauvais token est refusé', async () => {
    await spoke.sync.join({ hub: hubAddr, code: hub.sync.invite().code, fetchImpl: hubFetch(hub) })
    // falsifier le token stocké → 401
    const hubPeer = spoke.registry.listPeers().find(p => p.role === 'hub')!
    spoke.registry.setSetting(`sync.peer_token.${hubPeer.machine_id}`, 'mauvais-token')
    await expect(spoke.sync.pull(orgScopeId, hubFetch(hub))).rejects.toThrow()
  })

  it('un rejeu (même nonce) est refusé côté hub', async () => {
    await spoke.sync.join({ hub: hubAddr, code: hub.sync.invite().code, fetchImpl: hubFetch(hub) })
    // on capture une requête signée et on la rejoue telle quelle
    let captured: { url: string; init: { method: string; headers?: Record<string, string>; body?: string } } | null = null
    const capturing: FetchLike = async (url, init) => {
      captured = { url, init }
      return hubFetch(hub)(url, init)
    }
    await spoke.sync.pull(orgScopeId, capturing)
    expect(captured).not.toBeNull()
    // rejeu : même méthode/headers/nonce → le hub doit refuser (nonce déjà vu)
    const replay = await hubFetch(hub)(captured!.url, captured!.init)
    expect(replay.status).toBe(401)
  })
})
