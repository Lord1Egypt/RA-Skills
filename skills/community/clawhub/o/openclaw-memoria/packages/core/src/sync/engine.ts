/**
 * SyncEngine — synchro inter-machines hub-and-spoke (SYNC-INTER-MACHINES.md).
 *
 * HUB (Koda/Mac Studio) : détient les scopes partagés canoniques, sert
 * `/v1/sync/*` sur le LAN derrière peer_token + HMAC. SPOKE (Luna/iMac, Claude
 * Code) : copie locale complète, tire (pull) et pousse (push) vers le hub.
 *
 * Aucune valeur de secret en clair sur le réseau (enveloppes GVK). Best-effort :
 * jamais bloquant, jamais dans le chemin recall/store_fact.
 */
import type { ContentStore } from '../storage/content.js'
import type { RegistryStore } from '../storage/registry.js'
import type { SecretProvider } from '../secrets/types.js'
import type { MemoryScope, SyncPeer } from '../types.js'
import { newToken, nowISO, sha256Hex } from '../util.js'
import { clusterPairingKey, groupVaultKey, setClusterPairingKey, setGroupVaultKey } from '../secrets/index.js'
import { applyDelta, type ApplyReport, type SyncFact, type Tombstone } from './merge.js'
import { newNonce, signRequest, verifyRequest, type SigParts } from './peer-auth.js'
import { openEnvelope, openGvk, sealGvk, sealValue, type Envelope } from './secrets-sync.js'

export interface SyncConfig {
  enabled?: boolean
  role?: 'hub' | 'spoke'
  machine_id?: string
  hub?: string
  listen_lan?: string
  interval_sec?: number
  tls?: boolean
  scopes?: string[]
  relay_path?: string
  discovery_file?: string
}

export interface SyncDeps {
  registry: RegistryStore
  secrets: SecretProvider
  machineId: string
  config: SyncConfig
  sharedStore: (scopeId: string) => ContentStore | null
  listSyncableScopes: (whitelist: readonly string[]) => MemoryScope[]
  persistConfig: () => void
  setSyncConfig: (patch: Record<string, unknown>) => void
}

const DEFAULT_SCOPES = ['user', 'org', 'client', 'project', 'shared_topic'] as const
const INVITE_TTL_MS = 10 * 60_000
const PAGE = 500

export interface SyncDelta {
  scope_id: string
  facts: SyncFact[]
  tombstones: Tombstone[]
  next_cursor: string
  has_more: boolean
}

export class SyncEngine {
  constructor(private readonly deps: SyncDeps) {}

  private get registry(): RegistryStore {
    return this.deps.registry
  }

  get role(): 'hub' | 'spoke' {
    return this.deps.config.role ?? 'spoke'
  }

  get machineId(): string {
    return this.deps.machineId
  }

  private scopeWhitelist(): readonly string[] {
    return this.deps.config.scopes ?? DEFAULT_SCOPES
  }

  /** Scopes synchronisables locaux (jamais private/legacy). */
  syncScopes(): MemoryScope[] {
    return this.deps.listSyncableScopes(this.scopeWhitelist())
  }

  // ============================================================ HUB : pairing & auth

  /** (hub) Génère une invitation one-shot (code + adresse LAN). */
  invite(displayName?: string): { code: string; expires_at: string; hub_lan: string | null } {
    const code = `${rand4()}-${rand4()}`
    const expires_at = new Date(Date.now() + INVITE_TTL_MS).toISOString()
    this.registry.setSetting(
      'sync.pending_invite',
      JSON.stringify({ code_hash: sha256Hex(code), expires_at, display_name: displayName ?? 'machine' }),
    )
    return { code, expires_at, hub_lan: this.deps.config.listen_lan ?? null }
  }

  /** (hub) Le spoke présente le code → on crée le pair + on renvoie ses clés. */
  completePairing(input: { code: string; machine_id: string; display_name?: string; host?: string }): {
    peer_token: string
    cpk: string
    sealed_gvk: string
    hub_machine_id: string
    scopes: Array<{ id: string; type: string; name: string }>
  } {
    const raw = this.registry.getSetting('sync.pending_invite')
    if (!raw) throw new Error('aucune invitation de synchro en attente')
    const inv = JSON.parse(raw) as { code_hash: string; expires_at: string; display_name: string }
    if (Date.parse(inv.expires_at) < Date.now()) {
      this.registry.setSetting('sync.pending_invite', '')
      throw new Error('invitation de synchro expirée')
    }
    if (sha256Hex(input.code) !== inv.code_hash) throw new Error('code de synchro invalide')

    const gvk = groupVaultKey(this.deps.secrets)
    const cpk = clusterPairingKey(this.deps.secrets)
    const peerToken = newToken()
    const scopes = this.syncScopes().map(s => ({ id: s.id, type: s.type, name: s.name }))
    this.registry.addPeer({
      machine_id: input.machine_id,
      display_name: input.display_name ?? inv.display_name,
      role: 'spoke',
      host: input.host ?? null,
      peer_token: peerToken,
      cpk_location: this.deps.secrets.locationFor('__cluster_pairing_key'),
      allowed_scopes: scopes.map(s => s.id),
    })
    this.registry.setSetting('sync.pending_invite', '') // one-shot consommé
    this.registry.audit({ actor_type: 'system', actor_id: 'sync', action: 'sync_peer_paired', target_id_hash: sha256Hex(input.machine_id), scope_id: null, reason: null })
    return {
      peer_token: peerToken,
      cpk: cpk.toString('hex'),
      sealed_gvk: sealGvk(gvk, input.code),
      hub_machine_id: this.machineId,
      scopes,
    }
  }

  /**
   * (hub) Authentifie une requête `/v1/sync/*` : peer_token + HMAC + anti-rejeu.
   * Lève une erreur explicite si refusée. Renvoie le pair.
   */
  authenticate(peerToken: string | undefined, sig: string | undefined, parts: SigParts): SyncPeer {
    if (!peerToken) throw new SyncAuthError('peer_token requis')
    const peer = this.registry.verifyPeerToken(peerToken)
    if (!peer) throw new SyncAuthError('peer inconnu ou révoqué')
    if (!sig) throw new SyncAuthError('signature requise')
    const cpk = clusterPairingKey(this.deps.secrets)
    const result = verifyRequest(cpk, sig, parts, n => !this.registry.recordSyncNonce(n))
    if (!result.ok) throw new SyncAuthError(`signature refusée (${result.reason})`)
    this.registry.touchPeer(peer.machine_id, peer.host)
    return peer
  }

  // ============================================================ HUB : delta & snapshot

  /** (hub) Faits d'un scope modifiés après `since` (pagination par updated_at). */
  collectDelta(scopeId: string, since: string, limit = PAGE): SyncDelta {
    const store = this.deps.sharedStore(scopeId)
    if (!store) return { scope_id: scopeId, facts: [], tombstones: [], next_cursor: since, has_more: false }
    const rows = store.db
      .prepare(
        `SELECT * FROM facts WHERE scope_id = ? AND updated_at > ? ORDER BY updated_at ASC LIMIT ?`,
      )
      .all(scopeId, since, limit + 1) as Array<Record<string, unknown>>
    const has_more = rows.length > limit
    const page = rows.slice(0, limit)
    const facts: SyncFact[] = []
    const tombstones: Tombstone[] = []
    for (const r of page) {
      if (r['deleted_at']) {
        tombstones.push({ id: String(r['id']), deleted_at: String(r['deleted_at']), origin_machine_id: (r['origin_machine_id'] as string) ?? null, origin_rev: Number(r['origin_rev'] ?? 0), updated_at: String(r['updated_at']) })
      } else {
        facts.push(toSyncFact(r))
      }
    }
    const last = page.at(-1)
    const next_cursor = last ? String(last['updated_at']) : since
    return { scope_id: scopeId, facts, tombstones, next_cursor, has_more }
  }

  /** (hub) Snapshot complet d'un scope (bootstrap/réconciliation). */
  snapshot(scopeId: string, since = '1970-01-01T00:00:00.000Z', limit = PAGE): SyncDelta {
    return this.collectDelta(scopeId, since, limit)
  }

  /** (hub ou spoke) Applique un delta entrant sur la copie locale du scope. */
  applyIncoming(scopeId: string, facts: SyncFact[], tombstones: Tombstone[]): ApplyReport & { hub_watermark: string } {
    const store = this.deps.sharedStore(scopeId)
    if (!store) return { applied: 0, skipped_lww: 0, deduped: 0, tombstoned: 0, hub_watermark: nowISO() }
    const report = applyDelta(store, facts, tombstones)
    const wm = store.db.prepare('SELECT MAX(updated_at) AS m FROM facts WHERE scope_id = ?').get(scopeId) as { m: string | null }
    return { ...report, hub_watermark: wm.m ?? nowISO() }
  }

  // ============================================================ HUB : secrets

  /** (hub) Enveloppes chiffrées GVK des secrets partagés d'un scope (jamais de plaintext). */
  serveSecrets(scopeId: string): Array<{ ref_id: string; name: string; service: string | null; sensitivity: string; env: Envelope }> {
    const rows = this.registry.db
      .prepare(
        `SELECT sse.ref_id, sse.iv, sse.tag, sse.data, sr.name, sr.service, sr.sensitivity
         FROM shared_secret_envelopes sse JOIN secret_refs sr ON sr.id = sse.ref_id
         WHERE sse.scope_id = ? AND sse.syncable = 1`,
      )
      .all(scopeId) as Array<{ ref_id: string; iv: string; tag: string; data: string; name: string; service: string | null; sensitivity: string }>
    return rows.map(r => ({ ref_id: r.ref_id, name: r.name, service: r.service, sensitivity: r.sensitivity, env: { iv: r.iv, tag: r.tag, data: r.data } }))
  }

  /** (hub) Marque un secret existant comme partageable : scelle sa valeur en enveloppe GVK. */
  shareSecret(refId: string, scopeId: string, value: string, opts: { syncable?: boolean } = {}): void {
    const gvk = groupVaultKey(this.deps.secrets)
    const env = sealValue(value, gvk)
    this.registry.db
      .prepare(
        `INSERT INTO shared_secret_envelopes (ref_id, scope_id, syncable, iv, tag, data, updated_at)
         VALUES (?, ?, ?, ?, ?, ?, ?)
         ON CONFLICT(ref_id) DO UPDATE SET scope_id=excluded.scope_id, syncable=excluded.syncable, iv=excluded.iv, tag=excluded.tag, data=excluded.data, updated_at=excluded.updated_at`,
      )
      .run(refId, scopeId, opts.syncable ? 1 : 0, env.iv, env.tag, env.data, nowISO())
  }

  // ============================================================ SPOKE : join / pull / push

  /** (spoke) S'appaire au hub puis bootstrap (snapshot + secrets). 1 commande. */
  async join(opts: { hub: string; code: string; fetchImpl?: FetchLike }): Promise<{ scopes: number; facts: number; secrets: number }> {
    const f = opts.fetchImpl ?? globalFetch()
    const res = await f(`http://${opts.hub}/v1/sync/pairing/complete`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ code: opts.code, machine_id: this.machineId, display_name: this.machineId }),
    })
    if (!res.ok) throw new Error(`pairing refusé par le hub (${res.status})`)
    const data = (await res.json()) as {
      peer_token: string; cpk: string; sealed_gvk: string; hub_machine_id: string
      scopes: Array<{ id: string; type: string; name: string }>
    }

    // installer les clés du groupe
    setClusterPairingKey(this.deps.secrets, Buffer.from(data.cpk, 'hex'))
    const gvk = openGvk(data.sealed_gvk, opts.code)
    if (!gvk) throw new Error('échec du descellement de la clé de coffre (code invalide ?)')
    setGroupVaultKey(this.deps.secrets, gvk)

    // ADOPTER les scopes du hub → aligner les identités de scope entre machines
    for (const s of data.scopes) this.registry.adoptScope({ id: s.id, type: s.type as never, name: s.name })

    // enregistrer le hub comme pair (hash) + garder le token EN CLAIR localement
    // (le spoke doit le présenter en Bearer ; registry.sqlite est local + protégé).
    this.registry.addPeer({
      machine_id: data.hub_machine_id,
      display_name: `hub (${opts.hub})`,
      role: 'hub',
      host: opts.hub,
      peer_token: data.peer_token,
      cpk_location: this.deps.secrets.locationFor('__cluster_pairing_key'),
      allowed_scopes: data.scopes.map(s => s.id),
    })
    this.registry.setSetting(`sync.peer_token.${data.hub_machine_id}`, data.peer_token)
    this.deps.setSyncConfig({ enabled: true, role: 'spoke', hub: opts.hub })
    this.deps.persistConfig()

    return this.bootstrap({ hub: opts.hub, scopes: data.scopes.map(s => s.id), fetchImpl: f })
  }

  /** (spoke) Récupère l'historique complet des scopes + les secrets (1re fois). */
  async bootstrap(opts: { hub: string; scopes: string[]; fetchImpl?: FetchLike }): Promise<{ scopes: number; facts: number; secrets: number }> {
    const f = opts.fetchImpl ?? globalFetch()
    let totalFacts = 0
    let totalSecrets = 0
    for (const scopeId of opts.scopes) {
      // snapshot paginé
      let cursor = '1970-01-01T00:00:00.000Z'
      for (;;) {
        const delta = await this.signedGet<SyncDelta>(opts.hub, `/v1/sync/snapshot?scope=${encodeURIComponent(scopeId)}&since=${encodeURIComponent(cursor)}`, f)
        const r = this.applyIncoming(scopeId, delta.facts, delta.tombstones)
        totalFacts += r.applied
        cursor = delta.next_cursor
        this.registry.setCursor(hubKey(opts.hub), scopeId, { watermark: cursor })
        if (!delta.has_more) break
      }
      // secrets du scope
      const secrets = await this.signedGet<{ secrets: Array<{ name: string; env: Envelope }> }>(opts.hub, `/v1/sync/secrets?scope=${encodeURIComponent(scopeId)}`, f)
      const gvk = groupVaultKey(this.deps.secrets)
      for (const s of secrets.secrets) {
        const value = openEnvelope(s.env, gvk)
        if (value !== null) {
          this.deps.secrets.set(s.name, value)
          totalSecrets++
        }
      }
    }
    return { scopes: opts.scopes.length, facts: totalFacts, secrets: totalSecrets }
  }

  /** (spoke) Tire les nouveautés d'un scope depuis le hub. */
  async pull(scopeId: string, fetchImpl?: FetchLike): Promise<{ applied: number }> {
    const hub = this.hubPeer()
    if (!hub?.host) return { applied: 0 }
    const f = fetchImpl ?? globalFetch()
    const cur = this.registry.getCursor(hubKey(hub.host), scopeId)
    let applied = 0
    let since = cur.watermark
    for (;;) {
      const delta = await this.signedGet<SyncDelta>(hub.host, `/v1/sync/pull?scope=${encodeURIComponent(scopeId)}&since=${encodeURIComponent(since)}`, f)
      const r = this.applyIncoming(scopeId, delta.facts, delta.tombstones)
      applied += r.applied + r.tombstoned
      since = delta.next_cursor
      this.registry.setCursor(hubKey(hub.host), scopeId, { watermark: since })
      if (!delta.has_more) break
    }
    return { applied }
  }

  /** (spoke) Pousse ses changements locaux d'un scope vers le hub. */
  async push(scopeId: string, fetchImpl?: FetchLike): Promise<{ applied: number; skipped_lww: number }> {
    const hub = this.hubPeer()
    if (!hub?.host) return { applied: 0, skipped_lww: 0 }
    const f = fetchImpl ?? globalFetch()
    const cur = this.registry.getCursor(hubKey(hub.host), scopeId)
    const delta = this.collectDelta(scopeId, cur.last_push_at)
    if (delta.facts.length === 0 && delta.tombstones.length === 0) return { applied: 0, skipped_lww: 0 }
    const resp = await this.signedPost<{ applied: number; skipped_lww: number; hub_watermark: string }>(
      hub.host,
      '/v1/sync/push',
      { scope_id: scopeId, peer_machine_id: this.machineId, facts: delta.facts, tombstones: delta.tombstones },
      f,
    )
    this.registry.setCursor(hubKey(hub.host), scopeId, { last_push_at: delta.next_cursor })
    return { applied: resp.applied, skipped_lww: resp.skipped_lww }
  }

  /** (spoke) Une passe complète : pull + push sur tous les scopes. */
  async syncAll(fetchImpl?: FetchLike): Promise<{ pulled: number; pushed: number }> {
    let pulled = 0
    let pushed = 0
    for (const scope of this.syncScopes()) {
      pulled += (await this.pull(scope.id, fetchImpl)).applied
      pushed += (await this.push(scope.id, fetchImpl)).applied
    }
    return { pulled, pushed }
  }

  /** Une passe best-effort (appelée au boot + par le timer). Jamais throw. */
  async tick(fetchImpl?: FetchLike): Promise<{ pulled: number; pushed: number } | null> {
    if (this.deps.config.enabled === false) return null
    if (this.role !== 'spoke') return null // le hub est canonique : il ne tire pas
    if (!this.hubPeer()?.host) return null
    try {
      return await this.syncAll(fetchImpl)
    } catch {
      return null // skip + warn géré par l'appelant (best-effort)
    }
  }

  /** (spoke) Se déconnecte du hub : révoque le pair local, GARDE les données reçues. */
  leave(): void {
    const hub = this.hubPeer()
    if (hub) this.registry.revokePeer(hub.machine_id)
    this.deps.setSyncConfig({ enabled: false })
    this.deps.persistConfig()
  }

  /** Liste des pairs (UI admin). */
  peers(): SyncPeer[] {
    return this.registry.listPeers()
  }

  // ------------------------------------------------------------ internes

  private hubPeer(): SyncPeer | null {
    return this.registry.listPeers().find(p => p.role === 'hub') ?? null
  }

  private async signedGet<T>(host: string, path: string, f: FetchLike): Promise<T> {
    const res = await f(`http://${host}${path}`, { method: 'GET', headers: this.signHeaders('GET', path, '') })
    if (!res.ok) throw new Error(`sync GET ${path} → ${res.status}`)
    return (await res.json()) as T
  }

  private async signedPost<T>(host: string, path: string, body: unknown, f: FetchLike): Promise<T> {
    const payload = JSON.stringify(body)
    const res = await f(`http://${host}${path}`, { method: 'POST', headers: { 'content-type': 'application/json', ...this.signHeaders('POST', path, payload) }, body: payload })
    if (!res.ok) throw new Error(`sync POST ${path} → ${res.status}`)
    return (await res.json()) as T
  }

  /** En-têtes Bearer + HMAC pour une requête vers le hub. */
  private signHeaders(method: string, path: string, body: string): Record<string, string> {
    const hub = this.hubPeer()
    const token = hub ? this.registry.getSetting(`sync.peer_token.${hub.machine_id}`) : null
    // le token du hub est stocké au join (settings, chmod du registry) ; à défaut, en-tête vide → 401 clair
    const ts = nowISO()
    const nonce = newNonce()
    const cpk = clusterPairingKey(this.deps.secrets)
    const sig = signRequest(cpk, { method, path, body, ts, nonce })
    return {
      authorization: `Bearer ${token ?? ''}`,
      'x-memoria-ts': ts,
      'x-memoria-nonce': nonce,
      'x-memoria-sig': sig,
    }
  }
}

export class SyncAuthError extends Error {}

export type FetchLike = (url: string, init: { method: string; headers?: Record<string, string>; body?: string }) => Promise<{ ok: boolean; status: number; json: () => Promise<unknown> }>

function globalFetch(): FetchLike {
  return globalThis.fetch as unknown as FetchLike
}

function hubKey(host: string): string {
  return `hub:${host}`
}

function rand4(): string {
  const A = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'
  const b = globalThis.crypto.getRandomValues(new Uint8Array(4))
  return Array.from(b, x => A[x % A.length]).join('')
}

function toSyncFact(r: Record<string, unknown>): SyncFact {
  return {
    id: String(r['id']),
    fact: String(r['fact']),
    category: String(r['category']),
    fact_type: String(r['fact_type']),
    confidence: Number(r['confidence']),
    source: String(r['source']),
    scope_id: String(r['scope_id']),
    sensitivity: String(r['sensitivity']),
    visibility: String(r['visibility']),
    tags: String(r['tags'] ?? '[]'),
    entity_ids: String(r['entity_ids'] ?? '[]'),
    lifecycle_state: String(r['lifecycle_state']),
    superseded: Number(r['superseded'] ?? 0),
    superseded_by: (r['superseded_by'] as string) ?? null,
    origin_machine_id: (r['origin_machine_id'] as string) ?? null,
    origin_rev: Number(r['origin_rev'] ?? 0),
    content_hash: (r['content_hash'] as string) ?? null,
    deleted_at: (r['deleted_at'] as string) ?? null,
    created_at: String(r['created_at']),
    updated_at: String(r['updated_at']),
  }
}
