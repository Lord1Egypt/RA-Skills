/**
 * RegistryStore — `registry.sqlite`, gouvernance uniquement (spec §3.1).
 * Identités, instances, scopes, policies, pairing, audit neutre, secret_refs,
 * annuaire des DB. AUCUN fait ici.
 */
import type { Database } from 'better-sqlite3'
import { openDatabase } from './sqlite.js'
import { runMigrations } from './migrations.js'
import { registryMigrations } from './registry-schema.js'
import { fromJsonArray, newId, newPairingCode, newToken, nowISO, sha256Hex, toJson } from '../util.js'
import type {
  Assistant,
  AssistantInstance,
  AssistantType,
  AuditEntry,
  DbRegistryEntry,
  HumanUser,
  MemoryScope,
  Organization,
  Pairing,
  Person,
  PersonIdentifier,
  PersonProfile,
  Project,
  ScopeKind,
  ScopePolicy,
  SecretAccess,
  SyncPeer,
} from '../types.js'

function rowToPeer(r: Record<string, unknown>): SyncPeer {
  return {
    id: String(r['id']),
    machine_id: String(r['machine_id']),
    display_name: String(r['display_name']),
    role: r['role'] as 'hub' | 'spoke',
    host: (r['host'] as string | null) ?? null,
    peer_token_hash: String(r['peer_token_hash']),
    cpk_location: String(r['cpk_location']),
    allowed_scopes: fromJsonArray(String(r['allowed_scopes'] ?? '[]')),
    last_seen_at: (r['last_seen_at'] as string | null) ?? null,
    added_at: String(r['added_at']),
    revoked_at: (r['revoked_at'] as string | null) ?? null,
  }
}

const PAIRING_TTL_MS = 10 * 60 * 1000 // 10 minutes

/**
 * Normalise un identifiant pour le matching d'interlocuteur :
 * - téléphone/WhatsApp : ne garde que `+` et chiffres ;
 * - e-mail/Telegram/handle : minuscule + trim, @ initial retiré pour les handles.
 */
export function normalizeIdentifier(kind: PersonIdentifier['kind'], value: string): string {
  const v = value.trim()
  if (!v) return ''
  if (kind === 'phone' || kind === 'whatsapp') return v.replace(/[^\d+]/g, '')
  if (kind === 'email') return v.toLowerCase()
  if (kind === 'telegram' || kind === 'handle') return v.replace(/^@/, '').toLowerCase()
  return v.toLowerCase()
}

export class RegistryStore {
  readonly db: Database
  readonly path: string

  constructor(path: string) {
    const opened = openDatabase(path)
    this.db = opened.db
    this.path = path
    runMigrations(this.db, registryMigrations)
  }

  // -------------------------------------------------------------- bootstrap

  /**
   * Garantit l'état P1 : 1 human_user actif + 1 organisation own_company +
   * les scopes de base (`user`, `legacy_to_review`). Idempotent.
   */
  bootstrap(displayName = 'Utilisateur'): { user: HumanUser; ownCompany: Organization } {
    const tx = this.db.transaction(() => {
      let user = this.db.prepare('SELECT * FROM human_users LIMIT 1').get() as HumanUser | undefined
      if (!user) {
        user = {
          id: newId(),
          display_name: displayName,
          local_profile_name: null,
          created_at: nowISO(),
        }
        this.db
          .prepare('INSERT INTO human_users (id, display_name, local_profile_name, created_at) VALUES (?, ?, ?, ?)')
          .run(user.id, user.display_name, user.local_profile_name, user.created_at)
      }
      let org = this.db.prepare("SELECT * FROM organizations WHERE org_type = 'own_company' LIMIT 1").get() as
        | Organization
        | undefined
      if (!org) {
        org = { id: newId(), name: 'Mon organisation', org_type: 'own_company', parent_org_id: null, created_at: nowISO() }
        this.db
          .prepare('INSERT INTO organizations (id, name, org_type, parent_org_id, created_at) VALUES (?, ?, ?, ?, ?)')
          .run(org.id, org.name, org.org_type, org.parent_org_id, org.created_at)
      }
      this.ensureScope('user', 'user', { owner_user_id: user.id })
      this.ensureScope('legacy_to_review', 'legacy_to_review', {})
      this.ensureScope('org', `org:${org.id}`, { org_id: org.id })
      return { user, ownCompany: org }
    })
    return tx()
  }

  ensureScope(
    type: ScopeKind,
    name: string,
    refs: Partial<Pick<MemoryScope, 'owner_user_id' | 'org_id' | 'client_org_id' | 'project_id'>>,
  ): MemoryScope {
    const existing = this.db.prepare('SELECT * FROM memory_scopes WHERE type = ? AND name = ?').get(type, name) as
      | MemoryScope
      | undefined
    if (existing) return existing
    const scope: MemoryScope = {
      id: newId(),
      type,
      name,
      owner_user_id: refs.owner_user_id ?? null,
      org_id: refs.org_id ?? null,
      client_org_id: refs.client_org_id ?? null,
      project_id: refs.project_id ?? null,
      created_at: nowISO(),
    }
    this.db
      .prepare(
        'INSERT INTO memory_scopes (id, type, name, owner_user_id, org_id, client_org_id, project_id, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
      )
      .run(scope.id, scope.type, scope.name, scope.owner_user_id, scope.org_id, scope.client_org_id, scope.project_id, scope.created_at)
    return scope
  }

  /**
   * Adopte un scope d'un PAIR (synchro) : aligne l'identité de scope entre
   * machines. Pour les scopes SINGLETON (user/org/legacy), repointe le scope
   * local (vide sur une machine neuve) vers l'id du hub ; sinon crée la ligne.
   * Sans ça, chaque machine a des ids de scope différents → la synchro casse.
   */
  adoptScope(def: { id: string; type: ScopeKind; name: string }): MemoryScope {
    const byId = this.getScope(def.id)
    if (byId) return byId
    const SINGLETON: ScopeKind[] = ['user', 'org', 'legacy_to_review']
    if (SINGLETON.includes(def.type)) {
      const local = this.db.prepare('SELECT id FROM memory_scopes WHERE type = ? LIMIT 1').get(def.type) as { id: string } | undefined
      if (local) {
        // machine neuve : repointer l'id local vers celui du hub (un seul scope de ce type)
        this.db.prepare('UPDATE memory_scopes SET id = ?, name = ? WHERE id = ?').run(def.id, def.name, local.id)
        return this.getScope(def.id)!
      }
    }
    this.db
      .prepare('INSERT OR IGNORE INTO memory_scopes (id, type, name, owner_user_id, org_id, client_org_id, project_id, created_at) VALUES (?, ?, ?, NULL, NULL, NULL, NULL, ?)')
      .run(def.id, def.type, def.name, nowISO())
    return this.getScope(def.id)!
  }

  createProject(name: string, ownerOrgId: string, clientOrgId?: string | null): Project {
    const project: Project = {
      id: newId(),
      name,
      owner_org_id: ownerOrgId,
      client_org_id: clientOrgId ?? null,
      status: 'active',
      created_at: nowISO(),
    }
    this.db
      .prepare('INSERT INTO projects (id, name, owner_org_id, client_org_id, status, created_at) VALUES (?, ?, ?, ?, ?, ?)')
      .run(project.id, project.name, project.owner_org_id, project.client_org_id, project.status, project.created_at)
    return project
  }

  getProject(id: string): Project | null {
    return (this.db.prepare('SELECT * FROM projects WHERE id = ?').get(id) as Project | undefined) ?? null
  }

  ownCompany(): Organization | null {
    return (
      (this.db.prepare("SELECT * FROM organizations WHERE org_type = 'own_company' LIMIT 1").get() as
        | Organization
        | undefined) ?? null
    )
  }

  createOrganization(name: string, orgType: Organization['org_type'], parentOrgId?: string | null): Organization {
    const org: Organization = {
      id: newId(),
      name,
      org_type: orgType,
      parent_org_id: parentOrgId ?? null,
      created_at: nowISO(),
    }
    this.db
      .prepare('INSERT INTO organizations (id, name, org_type, parent_org_id, created_at) VALUES (?, ?, ?, ?, ?)')
      .run(org.id, org.name, org.org_type, org.parent_org_id, org.created_at)
    return org
  }

  // ---------------------------------------------------------------- personnes (interlocuteurs)

  createPerson(input: { display_name: string; relation?: string | null; notes?: string | null; org_id?: string | null; user_id?: string | null }): Person {
    const now = nowISO()
    const p: Person = {
      id: newId(),
      display_name: input.display_name,
      notes: input.notes ?? null,
      relation: input.relation ?? null,
      org_id: input.org_id ?? null,
      user_id: input.user_id ?? null,
      created_at: now,
      updated_at: now,
    }
    this.db
      .prepare('INSERT INTO persons (id, display_name, notes, relation, org_id, user_id, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)')
      .run(p.id, p.display_name, p.notes, p.relation, p.org_id, p.user_id, p.created_at, p.updated_at)
    return p
  }

  updatePerson(id: string, patch: Partial<Pick<Person, 'display_name' | 'notes' | 'relation' | 'org_id'>>): Person | null {
    const cur = this.getPersonRow(id)
    if (!cur) return null
    const next: Person = {
      ...cur,
      display_name: patch.display_name ?? cur.display_name,
      notes: patch.notes !== undefined ? patch.notes : cur.notes,
      relation: patch.relation !== undefined ? patch.relation : cur.relation,
      org_id: patch.org_id !== undefined ? patch.org_id : cur.org_id,
      updated_at: nowISO(),
    }
    this.db
      .prepare('UPDATE persons SET display_name = ?, notes = ?, relation = ?, org_id = ?, updated_at = ? WHERE id = ?')
      .run(next.display_name, next.notes, next.relation, next.org_id, next.updated_at, id)
    return next
  }

  deletePerson(id: string): boolean {
    const info = this.db.prepare('DELETE FROM persons WHERE id = ?').run(id)
    return info.changes > 0
  }

  private getPersonRow(id: string): Person | null {
    return (this.db.prepare('SELECT * FROM persons WHERE id = ?').get(id) as Person | undefined) ?? null
  }

  getPerson(id: string): PersonProfile | null {
    const p = this.getPersonRow(id)
    if (!p) return null
    return { ...p, identifiers: this.identifiersOf(id) }
  }

  listPersons(): PersonProfile[] {
    const rows = this.db.prepare('SELECT * FROM persons ORDER BY display_name COLLATE NOCASE').all() as Person[]
    return rows.map(p => ({ ...p, identifiers: this.identifiersOf(p.id) }))
  }

  private identifiersOf(personId: string): PersonIdentifier[] {
    return this.db.prepare('SELECT * FROM person_identifiers WHERE person_id = ? ORDER BY created_at').all(personId) as PersonIdentifier[]
  }

  addIdentifier(personId: string, kind: PersonIdentifier['kind'], value: string, label?: string | null): PersonIdentifier {
    const normalized = normalizeIdentifier(kind, value)
    if (!normalized) throw new Error('identifiant vide')
    const ident: PersonIdentifier = {
      id: newId(),
      person_id: personId,
      kind,
      value: normalized,
      label: label ?? null,
      created_at: nowISO(),
    }
    // un identifiant = au plus une personne : on réattribue proprement si déjà pris
    this.db.prepare('DELETE FROM person_identifiers WHERE kind = ? AND value = ?').run(kind, normalized)
    this.db
      .prepare('INSERT INTO person_identifiers (id, person_id, kind, value, label, created_at) VALUES (?, ?, ?, ?, ?, ?)')
      .run(ident.id, ident.person_id, ident.kind, ident.value, ident.label, ident.created_at)
    return ident
  }

  removeIdentifier(id: string): boolean {
    return this.db.prepare('DELETE FROM person_identifiers WHERE id = ?').run(id).changes > 0
  }

  /** Reconnaît un interlocuteur par un identifiant (Telegram/mail/tel…). */
  findPersonByIdentifier(kind: PersonIdentifier['kind'], value: string): PersonProfile | null {
    const normalized = normalizeIdentifier(kind, value)
    if (!normalized) return null
    const row = this.db.prepare('SELECT person_id FROM person_identifiers WHERE kind = ? AND value = ?').get(kind, normalized) as
      | { person_id: string }
      | undefined
    return row ? this.getPerson(row.person_id) : null
  }

  getScope(id: string): MemoryScope | null {
    return (this.db.prepare('SELECT * FROM memory_scopes WHERE id = ?').get(id) as MemoryScope | undefined) ?? null
  }

  getScopeByName(name: string): MemoryScope | null {
    return (this.db.prepare('SELECT * FROM memory_scopes WHERE name = ?').get(name) as MemoryScope | undefined) ?? null
  }

  listScopes(): MemoryScope[] {
    return this.db.prepare('SELECT * FROM memory_scopes ORDER BY created_at').all() as MemoryScope[]
  }

  // -------------------------------------------------------- assistants & instances

  ensureAssistant(type: AssistantType, displayName: string, ownerUserId: string): Assistant {
    const existing = this.db
      .prepare('SELECT * FROM assistants WHERE type = ? AND display_name = ?')
      .get(type, displayName) as (Omit<Assistant, 'default_scopes'> & { default_scopes: string }) | undefined
    if (existing) return { ...existing, default_scopes: fromJsonArray(existing.default_scopes) }
    const a: Assistant = {
      id: newId(),
      type,
      display_name: displayName,
      owner_user_id: ownerUserId,
      default_scopes: [],
      created_at: nowISO(),
    }
    this.db
      .prepare('INSERT INTO assistants (id, type, display_name, owner_user_id, default_scopes, created_at) VALUES (?, ?, ?, ?, ?, ?)')
      .run(a.id, a.type, a.display_name, a.owner_user_id, toJson(a.default_scopes), a.created_at)
    return a
  }

  getAssistant(id: string): Assistant | null {
    const row = this.db.prepare('SELECT * FROM assistants WHERE id = ?').get(id) as
      | (Omit<Assistant, 'default_scopes'> & { default_scopes: string })
      | undefined
    return row ? { ...row, default_scopes: fromJsonArray(row.default_scopes) } : null
  }

  listAssistants(): Assistant[] {
    const rows = this.db.prepare('SELECT * FROM assistants ORDER BY created_at').all() as Array<
      Omit<Assistant, 'default_scopes'> & { default_scopes: string }
    >
    return rows.map(r => ({ ...r, default_scopes: fromJsonArray(r.default_scopes) }))
  }

  createInstance(assistantId: string, machineId: string, profileId?: string | null): AssistantInstance {
    const inst: AssistantInstance = {
      id: newId(),
      assistant_id: assistantId,
      machine_id: machineId,
      profile_id: profileId ?? null,
      created_at: nowISO(),
      last_seen_at: null,
      token_hash: null,
      revoked_at: null,
    }
    this.db
      .prepare(
        'INSERT INTO assistant_instances (id, assistant_id, machine_id, profile_id, created_at, last_seen_at, token_hash, revoked_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
      )
      .run(inst.id, inst.assistant_id, inst.machine_id, inst.profile_id, inst.created_at, null, null, null)
    return inst
  }

  getInstance(id: string): AssistantInstance | null {
    return (
      (this.db.prepare('SELECT * FROM assistant_instances WHERE id = ?').get(id) as AssistantInstance | undefined) ??
      null
    )
  }

  listInstances(): AssistantInstance[] {
    return this.db.prepare('SELECT * FROM assistant_instances ORDER BY created_at').all() as AssistantInstance[]
  }

  touchInstance(id: string): void {
    this.db.prepare('UPDATE assistant_instances SET last_seen_at = ? WHERE id = ?').run(nowISO(), id)
  }

  revokeInstance(id: string): void {
    this.db.prepare('UPDATE assistant_instances SET revoked_at = ?, token_hash = NULL WHERE id = ?').run(nowISO(), id)
    this.db
      .prepare("UPDATE pairings SET status = 'revoked' WHERE assistant_instance_id = ? AND status = 'pending'")
      .run(id)
  }

  /** Suppression DÉFINITIVE d'une instance + son scope privé + policies + pairings + enregistrement DB. */
  deleteInstance(id: string): void {
    const tx = this.db.transaction(() => {
      const privateScope = this.getScopeByName(`private:${id}`)
      this.db.prepare('DELETE FROM pairings WHERE assistant_instance_id = ?').run(id)
      this.db.prepare('DELETE FROM db_registry WHERE assistant_instance_id = ?').run(id)
      if (privateScope) {
        this.db.prepare('DELETE FROM assistant_scope_policy WHERE scope_id = ?').run(privateScope.id)
        this.db.prepare('DELETE FROM db_registry WHERE scope_id = ?').run(privateScope.id)
        this.db.prepare('DELETE FROM memory_scopes WHERE id = ?').run(privateScope.id)
      }
      this.db.prepare('DELETE FROM assistant_instances WHERE id = ?').run(id)
    })
    tx()
  }

  /** Authentifie un token d'instance → instance non révoquée, ou null. */
  verifyInstanceToken(token: string): AssistantInstance | null {
    const hash = sha256Hex(token)
    const inst = this.db
      .prepare('SELECT * FROM assistant_instances WHERE token_hash = ? AND revoked_at IS NULL')
      .get(hash) as AssistantInstance | undefined
    return inst ?? null
  }

  // ------------------------------------------------------------------ pairing

  /** Crée un pairing : code court TTL 10 min à coller dans le chat de l'agent. */
  createPairing(instanceId: string): { pairing: Pairing; code: string } {
    const code = newPairingCode()
    const pairing: Pairing = {
      id: newId(),
      assistant_instance_id: instanceId,
      code_hash: sha256Hex(code),
      status: 'pending',
      created_at: nowISO(),
      expires_at: new Date(Date.now() + PAIRING_TTL_MS).toISOString(),
    }
    this.db
      .prepare('INSERT INTO pairings (id, assistant_instance_id, code_hash, status, created_at, expires_at) VALUES (?, ?, ?, ?, ?, ?)')
      .run(pairing.id, pairing.assistant_instance_id, pairing.code_hash, pairing.status, pairing.created_at, pairing.expires_at)
    return { pairing, code }
  }

  /** Échange code → token d'instance (one-shot, expire après TTL). */
  completePairing(code: string): { instance: AssistantInstance; token: string } | null {
    const hash = sha256Hex(code.trim().toUpperCase())
    const pairing = this.db
      .prepare("SELECT * FROM pairings WHERE code_hash = ? AND status = 'pending'")
      .get(hash) as Pairing | undefined
    if (!pairing) return null
    if (new Date(pairing.expires_at).getTime() < Date.now()) {
      this.db.prepare("UPDATE pairings SET status = 'expired' WHERE id = ?").run(pairing.id)
      return null
    }
    const token = newToken()
    const tx = this.db.transaction(() => {
      this.db.prepare("UPDATE pairings SET status = 'completed' WHERE id = ?").run(pairing.id)
      this.db
        .prepare('UPDATE assistant_instances SET token_hash = ?, last_seen_at = ? WHERE id = ?')
        .run(sha256Hex(token), nowISO(), pairing.assistant_instance_id)
    })
    tx()
    const instance = this.getInstance(pairing.assistant_instance_id)
    if (!instance) return null
    return { instance, token }
  }

  // ------------------------------------------------------------------ policies

  setPolicy(policy: ScopePolicy): void {
    this.db
      .prepare(
        `INSERT INTO assistant_scope_policy (assistant_id, scope_id, can_read, can_write, can_share, secret_access)
         VALUES (?, ?, ?, ?, ?, ?)
         ON CONFLICT(assistant_id, scope_id) DO UPDATE SET
           can_read = excluded.can_read, can_write = excluded.can_write,
           can_share = excluded.can_share, secret_access = excluded.secret_access`,
      )
      .run(
        policy.assistant_id,
        policy.scope_id,
        policy.can_read ? 1 : 0,
        policy.can_write ? 1 : 0,
        policy.can_share ? 1 : 0,
        policy.secret_access,
      )
  }

  getPolicy(assistantId: string, scopeId: string): ScopePolicy | null {
    const row = this.db
      .prepare('SELECT * FROM assistant_scope_policy WHERE assistant_id = ? AND scope_id = ?')
      .get(assistantId, scopeId) as
      | { assistant_id: string; scope_id: string; can_read: number; can_write: number; can_share: number; secret_access: SecretAccess }
      | undefined
    if (!row) return null
    return {
      assistant_id: row.assistant_id,
      scope_id: row.scope_id,
      can_read: row.can_read === 1,
      can_write: row.can_write === 1,
      can_share: row.can_share === 1,
      secret_access: row.secret_access,
    }
  }

  /** Scopes lisibles par un assistant (policy can_read). */
  readableScopes(assistantId: string): MemoryScope[] {
    return this.db
      .prepare(
        `SELECT s.* FROM memory_scopes s
         JOIN assistant_scope_policy p ON p.scope_id = s.id
         WHERE p.assistant_id = ? AND p.can_read = 1`,
      )
      .all(assistantId) as MemoryScope[]
  }

  // ------------------------------------------------------------------ db registry

  registerDb(entry: Omit<DbRegistryEntry, 'id'>): DbRegistryEntry {
    const existing = this.db.prepare('SELECT * FROM db_registry WHERE path = ?').get(entry.path) as
      | DbRegistryEntry
      | undefined
    if (existing) return existing
    const e: DbRegistryEntry = { id: newId(), ...entry }
    this.db
      .prepare('INSERT INTO db_registry (id, kind, path, assistant_instance_id, scope_id) VALUES (?, ?, ?, ?, ?)')
      .run(e.id, e.kind, e.path, e.assistant_instance_id, e.scope_id)
    return e
  }

  listDbs(): DbRegistryEntry[] {
    return this.db.prepare('SELECT * FROM db_registry').all() as DbRegistryEntry[]
  }

  dbForScope(scopeId: string): DbRegistryEntry | null {
    return (
      (this.db.prepare("SELECT * FROM db_registry WHERE scope_id = ? AND kind = 'shared'").get(scopeId) as
        | DbRegistryEntry
        | undefined) ?? null
    )
  }

  dbForInstance(instanceId: string): DbRegistryEntry | null {
    return (
      (this.db
        .prepare("SELECT * FROM db_registry WHERE assistant_instance_id = ? AND kind = 'assistant'")
        .get(instanceId) as DbRegistryEntry | undefined) ?? null
    )
  }

  // ------------------------------------------------------------------ secret refs

  /** Référence de secret (la VALEUR vit au coffre, jamais ici). Upsert par nom. */
  upsertSecretRef(name: string, location: string, service?: string | null): void {
    this.db
      .prepare(
        `INSERT INTO secret_refs (id, name, service, location, scope_id, allowed_assistants, sensitivity, last_verified_at, created_at)
         VALUES (?, ?, ?, ?, NULL, '[]', 'critical', ?, ?)
         ON CONFLICT(name) DO UPDATE SET location = excluded.location, last_verified_at = excluded.last_verified_at`,
      )
      .run(newId(), name, service ?? null, location, nowISO(), nowISO())
  }

  listSecretRefs(): Array<{ name: string; service: string | null; location: string; created_at: string }> {
    return this.db
      .prepare('SELECT name, service, location, created_at FROM secret_refs ORDER BY created_at DESC')
      .all() as Array<{ name: string; service: string | null; location: string; created_at: string }>
  }

  // ------------------------------------------------------------------ settings

  getSetting(key: string): string | null {
    const row = this.db.prepare('SELECT value FROM settings WHERE key = ?').get(key) as { value: string } | undefined
    return row?.value ?? null
  }

  setSetting(key: string, value: string): void {
    this.db
      .prepare(
        `INSERT INTO settings (key, value, updated_at) VALUES (?, ?, ?)
         ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = excluded.updated_at`,
      )
      .run(key, value, nowISO())
  }

  // ------------------------------------------------------------------ synchro (pairs, nonces, curseurs)

  addPeer(input: {
    machine_id: string
    display_name: string
    role: 'hub' | 'spoke'
    host?: string | null
    peer_token: string
    cpk_location: string
    allowed_scopes?: string[]
  }): SyncPeer {
    const peer: SyncPeer = {
      id: newId(),
      machine_id: input.machine_id,
      display_name: input.display_name,
      role: input.role,
      host: input.host ?? null,
      peer_token_hash: sha256Hex(input.peer_token),
      cpk_location: input.cpk_location,
      allowed_scopes: input.allowed_scopes ?? [],
      last_seen_at: null,
      added_at: nowISO(),
      revoked_at: null,
    }
    this.db
      .prepare(
        `INSERT INTO sync_peers (id, machine_id, display_name, role, host, peer_token_hash, cpk_location, allowed_scopes, last_seen_at, added_at, revoked_at)
         VALUES (@id, @machine_id, @display_name, @role, @host, @peer_token_hash, @cpk_location, @allowed_scopes, @last_seen_at, @added_at, @revoked_at)
         ON CONFLICT(machine_id) DO UPDATE SET
           display_name=excluded.display_name, role=excluded.role, host=excluded.host,
           peer_token_hash=excluded.peer_token_hash, cpk_location=excluded.cpk_location,
           allowed_scopes=excluded.allowed_scopes, revoked_at=NULL`,
      )
      .run({ ...peer, allowed_scopes: toJson(peer.allowed_scopes) })
    return peer
  }

  listPeers(includeRevoked = false): SyncPeer[] {
    const sql = includeRevoked
      ? 'SELECT * FROM sync_peers ORDER BY added_at'
      : 'SELECT * FROM sync_peers WHERE revoked_at IS NULL ORDER BY added_at'
    return (this.db.prepare(sql).all() as Array<Record<string, unknown>>).map(rowToPeer)
  }

  getPeerByMachineId(machineId: string): SyncPeer | null {
    const r = this.db.prepare('SELECT * FROM sync_peers WHERE machine_id = ?').get(machineId) as Record<string, unknown> | undefined
    return r ? rowToPeer(r) : null
  }

  /** Authentifie un pair par son token (jamais comparé en clair en base). */
  verifyPeerToken(token: string): SyncPeer | null {
    const hash = sha256Hex(token)
    const r = this.db.prepare('SELECT * FROM sync_peers WHERE peer_token_hash = ? AND revoked_at IS NULL').get(hash) as
      | Record<string, unknown>
      | undefined
    return r ? rowToPeer(r) : null
  }

  touchPeer(machineId: string, host?: string | null): void {
    this.db.prepare('UPDATE sync_peers SET last_seen_at = ?, host = COALESCE(?, host) WHERE machine_id = ?').run(nowISO(), host ?? null, machineId)
  }

  revokePeer(machineId: string): boolean {
    return this.db.prepare('UPDATE sync_peers SET revoked_at = ? WHERE machine_id = ? AND revoked_at IS NULL').run(nowISO(), machineId).changes > 0
  }

  /**
   * Enregistre un nonce de synchro. Renvoie true si NOUVEAU (accepté), false si
   * déjà vu (rejeu). Purge au passage les nonces périmés (TTL 5 min).
   */
  recordSyncNonce(nonce: string, ttlMs = 5 * 60_000): boolean {
    const now = Date.now()
    this.db.prepare('DELETE FROM sync_nonces WHERE seen_at < ?').run(new Date(now - ttlMs).toISOString())
    try {
      this.db.prepare('INSERT INTO sync_nonces (nonce, seen_at) VALUES (?, ?)').run(nonce, new Date(now).toISOString())
      return true
    } catch {
      return false // PRIMARY KEY violation = déjà vu
    }
  }

  getCursor(peerMachineId: string, scopeId: string): { watermark: string; last_push_at: string } {
    const r = this.db.prepare('SELECT watermark, last_push_at FROM sync_cursor WHERE peer_machine_id = ? AND scope_id = ?').get(peerMachineId, scopeId) as
      | { watermark: string; last_push_at: string }
      | undefined
    return r ?? { watermark: '1970-01-01T00:00:00.000Z', last_push_at: '1970-01-01T00:00:00.000Z' }
  }

  setCursor(peerMachineId: string, scopeId: string, patch: { watermark?: string; last_push_at?: string }): void {
    const cur = this.getCursor(peerMachineId, scopeId)
    this.db
      .prepare(
        `INSERT INTO sync_cursor (peer_machine_id, scope_id, watermark, last_push_at, last_sync_at)
         VALUES (?, ?, ?, ?, ?)
         ON CONFLICT(peer_machine_id, scope_id) DO UPDATE SET watermark=excluded.watermark, last_push_at=excluded.last_push_at, last_sync_at=excluded.last_sync_at`,
      )
      .run(peerMachineId, scopeId, patch.watermark ?? cur.watermark, patch.last_push_at ?? cur.last_push_at, nowISO())
  }

  // ------------------------------------------------------------------ audit

  /** Audit NEUTRE : action + hash — jamais de contenu (spec §11). */
  audit(entry: Omit<AuditEntry, 'id' | 'ts'>): void {
    this.db
      .prepare('INSERT INTO audit_log (ts, actor_type, actor_id, action, target_id_hash, scope_id, reason) VALUES (?, ?, ?, ?, ?, ?, ?)')
      .run(nowISO(), entry.actor_type, entry.actor_id, entry.action, entry.target_id_hash, entry.scope_id, entry.reason)
  }

  auditTail(limit = 100): AuditEntry[] {
    return this.db.prepare('SELECT * FROM audit_log ORDER BY id DESC LIMIT ?').all(limit) as AuditEntry[]
  }

  close(): void {
    this.db.close()
  }
}
