/**
 * Memoria — le moteur (spec §4). Aucune dépendance d'hôte.
 * P1 : identité/pairing, storeFact, recall fan-out gouverné, forget hard-delete,
 * doctor/stats. Capture pipeline (WAL→redaction→extraction) arrive en P2,
 * MCP/UI en P3 — voir docs/v3/STATUS.md.
 */
import { existsSync, rmSync, statSync } from 'node:fs'
import { hostname } from 'node:os'
import { dirname, join, relative } from 'node:path'
import DatabaseCtor from 'better-sqlite3'
import { importLegacyCognition } from '../migration/import-cognition.js'
import { importTranscripts } from '../migration/import-transcripts.js'
import {
  ensureStorageTree,
  resolveStorageRoot,
  saveConfigFile,
  storagePaths,
  type ResolveOptions,
  type ResolvedConfig,
} from '../config.js'
import { RegistryStore } from '../storage/registry.js'
import { isOnNetworkVolume } from '../storage/network-guard.js'
import { ContentStore, rowToFact, type FactRow, type FtsHit, type FtsSearchOptions } from '../storage/content.js'
import { EmbeddingIndexer, hybridSearchFacts } from '../vector/index.js'
import {
  CognitionEngine,
  TopicEngine,
  PatternEngine,
  ProceduralEngine,
  FeedbackEngine,
  ClusterEngine,
  SelfObservationEngine,
  RevisionEngine,
  AutoSkillEngine,
  MarkdownSync,
  dialectic,
  type TopicSummary,
  type TopicGraph,
  type Pattern,
  type ProcedureMatch,
  type ProceduralProcedure,
  type SelfObservation,
  type RevisionProposal,
  type DialecticResult,
} from '../cognition/index.js'
import { estimateTokens, newId, nowISO, sha256Hex } from '../util.js'
import { createSecretProvider, RegexRedactor } from '../secrets/index.js'
import type { SecretProvider } from '../secrets/types.js'
import { resolveLlmProfile } from '../llm/index.js'
import type { LlmOptions } from '../llm/detect.js'
import type { EmbeddingProvider, LlmProvider } from '../llm/provider.js'
import { CapturePipeline, type CaptureTurnInput, type CaptureTurnResult } from './capture.js'
import type { WalReplaySummary } from './wal.js'
import { isProceduralQuery, passesClientIsolation, scoreFact } from './scoring.js'
import { localMachineId, nextRev } from '../sync/clock.js'
import { contentHash } from '../sync/merge.js'
import { SyncEngine } from '../sync/engine.js'
import type {
  AssistantInstance,
  AssistantType,
  CaptureMode,
  DoctorReport,
  Fact,
  ForgetFilter,
  MemoryScope,
  Person,
  PersonIdentifier,
  PersonProfile,
  RecallInput,
  RecallItem,
  RecallResult,
  StoreFactInput,
} from '../types.js'

/** État d'un moteur (extraction ou embeddings) dans le bilan de santé LLM. */
export interface LlmEngineHealth {
  provider: string
  model: string
  available: boolean
  /** Pourquoi le moteur est indisponible — TOUJOURS présent quand available=false. */
  reason?: string
}

/** Bilan de santé LLM (GET /v1/admin/llm_health) — anti-mort-silencieuse. */
export interface LlmHealthReport {
  extraction: LlmEngineHealth
  embeddings: LlmEngineHealth
  /** Entrées WAL en attente d'extraction, toutes instances confondues. */
  wal_pending: number
  options: LlmOptions
}

export interface PairAssistantInput {
  type: AssistantType
  display_name?: string
  machine?: string
  profile?: string | null
}

export interface PairAssistantResult {
  assistant_id: string
  assistant_instance_id: string
  pairing_code: string
  /** Commande à copier-coller dans le chat de l'agent (D4). */
  command: string
}

export interface MemoriaInitOptions extends ResolveOptions {
  userDisplayName?: string
  /**
   * Override du profil LLM (tests, daemon piloté). `undefined` = résolution
   * automatique (Ollama/Anthropic selon config) au premier captureTurn.
   * `{ extraction: null }` = capture sans LLM (WAL seul).
   */
  llm?: { extraction: LlmProvider | null; embeddings?: EmbeddingProvider | null }
  /** Coffre forcé (tests : 'aes-vault' pour ne jamais toucher le Keychain réel). */
  secretsVault?: 'keychain-macos' | 'aes-vault'
}

const DEFAULT_TOKEN_BUDGET = 1500
const DEFAULT_RECALL_LIMIT = 12

export class Memoria {
  readonly resolved: ResolvedConfig
  readonly paths: ReturnType<typeof storagePaths>
  readonly registry: RegistryStore
  private readonly pool = new Map<string, ContentStore>()
  private closed = false

  private readonly secretProvider: SecretProvider
  private readonly redactor = new RegexRedactor()
  private syncEngine?: SyncEngine
  private readonly llmOverride: MemoriaInitOptions['llm']
  private pipelinePromise: Promise<CapturePipeline> | null = null
  private profilePromise: Promise<{ extraction: LlmProvider | null; embeddings: EmbeddingProvider | null }> | null = null
  private readonly indexers = new WeakMap<ContentStore, EmbeddingIndexer>()
  private readonly cognitionEngines = new WeakMap<ContentStore, CognitionEngine>()
  private readonly topicEngines = new WeakMap<ContentStore, TopicEngine>()
  private readonly patternEngines = new WeakMap<ContentStore, PatternEngine>()
  private readonly proceduralEngines = new WeakMap<ContentStore, ProceduralEngine>()
  private readonly feedbackEngines = new WeakMap<ContentStore, FeedbackEngine>()
  private readonly clusterEngines = new WeakMap<ContentStore, ClusterEngine>()
  private readonly selfObsEngines = new WeakMap<ContentStore, SelfObservationEngine>()
  private readonly revisionEngines = new WeakMap<ContentStore, RevisionEngine>()

  private constructor(resolved: ResolvedConfig, opts: MemoriaInitOptions) {
    this.resolved = resolved
    this.paths = storagePaths(resolved.storageRoot)
    ensureStorageTree(resolved.storageRoot)
    this.registry = new RegistryStore(this.paths.registry)
    this.registry.bootstrap(opts.userDisplayName)
    this.registry.registerDb({ kind: 'registry', path: this.paths.registry, assistant_instance_id: null, scope_id: null })
    this.secretProvider = createSecretProvider(this.paths.secretsDir, { force: opts.secretsVault })
    this.llmOverride = opts.llm
  }

  /** Point d'entrée unique. `Memoria.init({ storageRoot })` pour les tests/daemon. */
  static init(opts: MemoriaInitOptions = {}): Memoria {
    const resolved = resolveStorageRoot(opts)
    return new Memoria(resolved, opts)
  }

  // ------------------------------------------------------------ identité & connexion

  pairAssistant(input: PairAssistantInput): PairAssistantResult {
    this.assertOpen()
    const { user } = this.registry.bootstrap()
    const assistant = this.registry.ensureAssistant(input.type, input.display_name ?? input.type, user.id)
    const instance = this.registry.createInstance(assistant.id, input.machine ?? hostname(), input.profile)

    // Scope privé de l'instance + provision de sa DB
    const privateScope = this.registry.ensureScope('private', `private:${instance.id}`, {})
    const dbPath = this.paths.assistantDb(instance.id)
    this.openContent(dbPath)
    this.registry.registerDb({ kind: 'assistant', path: dbPath, assistant_instance_id: instance.id, scope_id: privateScope.id })

    // Policies par défaut : privé = lecture/écriture ; `user` = lecture (partage volontaire en P5)
    this.registry.setPolicy({
      assistant_id: assistant.id,
      scope_id: privateScope.id,
      can_read: true,
      can_write: true,
      can_share: false,
      secret_access: 'none',
    })
    const userScope = this.registry.getScopeByName('user')
    if (userScope) {
      this.registry.setPolicy({
        assistant_id: assistant.id,
        scope_id: userScope.id,
        can_read: true,
        can_write: false,
        can_share: false,
        secret_access: 'none',
      })
    }

    const { code } = this.registry.createPairing(instance.id)
    this.registry.audit({
      actor_type: 'user',
      actor_id: 'local',
      action: 'pair_assistant',
      target_id_hash: sha256Hex(instance.id),
      scope_id: privateScope.id,
      reason: `type=${input.type}`,
    })
    return {
      assistant_id: assistant.id,
      assistant_instance_id: instance.id,
      pairing_code: code,
      command: `npx -y @memoria/mcp connect --code ${code}`,
    }
  }

  completePairing(code: string): { assistant_instance_id: string; instance_token: string; assistant_type: string } | null {
    this.assertOpen()
    const result = this.registry.completePairing(code)
    if (!result) return null
    this.registry.audit({
      actor_type: 'assistant',
      actor_id: result.instance.id,
      action: 'complete_pairing',
      target_id_hash: sha256Hex(result.instance.id),
      scope_id: null,
      reason: null,
    })
    const assistant = this.registry.getAssistant(result.instance.assistant_id)
    return {
      assistant_instance_id: result.instance.id,
      instance_token: result.token,
      assistant_type: assistant?.type ?? 'generic',
    }
  }

  revokeInstance(instanceId: string): void {
    this.assertOpen()
    this.registry.revokeInstance(instanceId)
    this.registry.audit({
      actor_type: 'user',
      actor_id: 'local',
      action: 'revoke_instance',
      target_id_hash: sha256Hex(instanceId),
      scope_id: null,
      reason: null,
    })
  }

  /**
   * Supprime DÉFINITIVEMENT un agent : révoque, ferme et efface sa DB de mémoire
   * privée, retire son scope privé et son enregistrement. Irréversible (≠ révoquer
   * qui garde la mémoire). Audit neutre.
   */
  deleteInstance(instanceId: string): { deleted: boolean } {
    this.assertOpen()
    const instance = this.registry.getInstance(instanceId)
    if (!instance) return { deleted: false }
    const dbPath = this.paths.assistantDb(instanceId)
    // fermer la connexion du pool avant d'effacer le fichier
    const store = this.pool.get(dbPath)
    if (store) {
      store.close()
      this.pool.delete(dbPath)
    }
    for (const suffix of ['', '-wal', '-shm']) rmSync(`${dbPath}${suffix}`, { force: true })
    rmSync(dirname(dbPath), { recursive: true, force: true })
    this.registry.deleteInstance(instanceId)
    this.registry.audit({
      actor_type: 'user',
      actor_id: 'local',
      action: 'delete_instance',
      target_id_hash: sha256Hex(instanceId),
      scope_id: null,
      reason: null,
    })
    return { deleted: true }
  }

  // ------------------------------------------------------------ kill-switch & stockage

  /** Memoria actif ? (kill-switch global). Absent = true par défaut. */
  isEnabled(): boolean {
    return this.resolved.config.enabled !== false
  }

  /**
   * Bascule le kill-switch global et le persiste. À false, le daemon refuse
   * capture ET recall (no-op annoncé) sans se fermer : « pause » de Memoria.
   */
  setEnabled(enabled: boolean): boolean {
    this.assertOpen()
    this.resolved.config.enabled = enabled
    saveConfigFile(this.resolved.config, this.resolved.configPath)
    this.registry.audit({
      actor_type: 'user',
      actor_id: 'local',
      action: enabled ? 'memoria_enabled' : 'memoria_disabled',
      target_id_hash: null,
      scope_id: null,
      reason: null,
    })
    return enabled
  }

  /** Emplacement courant de la mémoire (pour l'UI « déplacer vers clé USB »). */
  storageInfo(): { root: string; config_path: string; on_network_volume: boolean } {
    return {
      root: this.paths.root,
      config_path: this.resolved.configPath,
      on_network_volume: isOnNetworkVolume(this.paths.root),
    }
  }

  // ------------------------------------------------------------ interlocuteurs (personnes)

  listPersons(): PersonProfile[] {
    this.assertOpen()
    return this.registry.listPersons()
  }

  getPerson(id: string): PersonProfile | null {
    this.assertOpen()
    return this.registry.getPerson(id)
  }

  createPerson(input: { display_name: string; relation?: string | null; notes?: string | null; org_id?: string | null }): Person {
    this.assertOpen()
    const p = this.registry.createPerson(input)
    this.registry.audit({ actor_type: 'user', actor_id: 'local', action: 'person_create', target_id_hash: sha256Hex(p.id), scope_id: null, reason: null })
    return p
  }

  updatePerson(id: string, patch: Partial<Pick<Person, 'display_name' | 'notes' | 'relation' | 'org_id'>>): Person | null {
    this.assertOpen()
    return this.registry.updatePerson(id, patch)
  }

  deletePerson(id: string): boolean {
    this.assertOpen()
    const ok = this.registry.deletePerson(id)
    if (ok) this.registry.audit({ actor_type: 'user', actor_id: 'local', action: 'person_delete', target_id_hash: sha256Hex(id), scope_id: null, reason: null })
    return ok
  }

  addPersonIdentifier(personId: string, kind: PersonIdentifier['kind'], value: string, label?: string | null): PersonIdentifier {
    this.assertOpen()
    return this.registry.addIdentifier(personId, kind, value, label)
  }

  removePersonIdentifier(id: string): boolean {
    this.assertOpen()
    return this.registry.removeIdentifier(id)
  }

  /**
   * Reconnaît l'interlocuteur courant via un ou plusieurs identifiants
   * (Telegram/WhatsApp/mail/handle…). Renvoie la personne + ses faits connus
   * pour que l'agent sache à QUI il parle. Aucun identifiant → null (= owner par défaut).
   */
  identifyInterlocutor(input: {
    phone?: string
    email?: string
    telegram?: string
    whatsapp?: string
    handle?: string
    name?: string
  }): { person: PersonProfile; known: string[] } | null {
    this.assertOpen()
    const tries: Array<[PersonIdentifier['kind'], string | undefined]> = [
      ['telegram', input.telegram],
      ['whatsapp', input.whatsapp],
      ['phone', input.phone],
      ['email', input.email],
      ['handle', input.handle],
    ]
    let person: PersonProfile | null = null
    for (const [kind, value] of tries) {
      if (!value) continue
      person = this.registry.findPersonByIdentifier(kind, value)
      if (person) break
    }
    // repli par nom exact (display_name) si aucun identifiant ne matche
    if (!person && input.name) {
      const match = this.registry.listPersons().find(p => p.display_name.toLowerCase() === input.name!.trim().toLowerCase())
      if (match) person = match
    }
    if (!person) return null
    return { person, known: this.knownAboutPerson(person.display_name) }
  }

  /**
   * Comme identifyInterlocutor, mais CRÉE la personne au premier contact si aucun
   * identifiant connu ne matche (auto-enregistrement des interlocuteurs, ex.
   * nouveau numéro WhatsApp/Telegram). Le premier identifiant fourni sert de clé.
   * `created` indique si une nouvelle personne a été créée. Sans aucun identifiant
   * fourni → comportement identique à identifyInterlocutor (pas de création).
   */
  identifyOrCreateInterlocutor(input: {
    phone?: string
    email?: string
    telegram?: string
    whatsapp?: string
    handle?: string
    name?: string
    relation?: string | null
  }): { person: PersonProfile; known: string[]; created: boolean } | null {
    this.assertOpen()
    const existing = this.identifyInterlocutor(input)
    if (existing) return { ...existing, created: false }

    // Aucune personne connue : on tente la création si on a AU MOINS un identifiant.
    const tries: Array<[PersonIdentifier['kind'], string | undefined]> = [
      ['telegram', input.telegram],
      ['whatsapp', input.whatsapp],
      ['phone', input.phone],
      ['email', input.email],
      ['handle', input.handle],
    ]
    const idents = tries.filter((t): t is [PersonIdentifier['kind'], string] => Boolean(t[1]))
    if (idents.length === 0) return null // rien pour identifier → owner par défaut

    const display = input.name?.trim() || idents[0]![1]
    const person = this.registry.createPerson({ display_name: display, relation: input.relation ?? null })
    for (const [kind, value] of idents) {
      // addIdentifier a un index unique (kind,value) : en cas de course, on ignore.
      try {
        this.registry.addIdentifier(person.id, kind, value)
      } catch {
        /* identifiant déjà rattaché ailleurs — on garde la personne créée */
      }
    }
    this.registry.audit({ actor_type: 'assistant', actor_id: 'local', action: 'person_autocreate', target_id_hash: sha256Hex(person.id), scope_id: null, reason: null })
    const profile = this.registry.getPerson(person.id)
    if (!profile) throw new Error('person auto-create: profil introuvable après création')
    return { person: profile, known: this.knownAboutPerson(profile.display_name), created: true }
  }

  /** Faits connus mentionnant cette personne (cross-agent, scopes partagés). */
  private knownAboutPerson(name: string, limit = 8): string[] {
    const hits = this.globalSearch(name, limit)
    return hits.map(h => h.fact)
  }

  /** Texte court « tu parles à X » pour l'injection de contexte (recall). */
  describeInterlocutor(personId: string): string | null {
    const p = this.registry.getPerson(personId)
    if (!p) return null
    const bits = [p.display_name]
    if (p.relation) bits.push(`(${p.relation})`)
    let line = `Tu parles à ${bits.join(' ')}.`
    if (p.notes) line += ` ${p.notes}`
    return line
  }

  /** Authentifie un token d'instance (utilisé par le daemon). */
  authenticate(token: string): AssistantInstance | null {
    this.assertOpen()
    const inst = this.registry.verifyInstanceToken(token)
    if (inst) this.registry.touchInstance(inst.id)
    return inst
  }

  // ------------------------------------------------------------------- mémoire

  storeFact(input: StoreFactInput): Fact {
    this.assertOpen()
    const instance = this.mustInstance(input.instance)
    const scope = this.resolveTargetScope(instance, input.scope)

    if (scope.type !== 'private') {
      const policy = this.registry.getPolicy(instance.assistant_id, scope.id)
      if (!policy?.can_write) {
        throw new Error(`écriture refusée : l'assistant n'a pas can_write sur le scope « ${scope.name} »`)
      }
    }

    // GATE SECRETS — défense en profondeur (audit QW1) : tout fait, même posé
    // en direct (store_fact MCP) ou issu d'un import, passe par la redaction
    // AVANT le stockage. La valeur détectée part au coffre, jamais dans facts.
    const content = this.redactBeforeStore(input.content)

    // PROVENANCE (synchro) : les faits d'un scope PARTAGÉ portent l'origine
    // (machine + révision logique) + un hash de contenu, pour la convergence LWW
    // inter-machines. Les faits privés n'en ont pas besoin (jamais synchronisés).
    const shared = scope.type !== 'private'
    const category = input.category ?? 'general'
    const provenance = shared
      ? {
          origin_machine_id: localMachineId(this.registry),
          origin_rev: nextRev(this.registry),
          content_hash: contentHash({ fact: content, category, scope_id: scope.id }),
        }
      : {}

    const store = this.storeForScope(scope, instance)
    const fact = store.insertFact({
      fact: content,
      category: input.category,
      fact_type: input.fact_type,
      confidence: input.confidence,
      source: input.source ?? 'manual',
      assistant_instance_id: instance.id,
      org_id: input.org_id ?? scope.org_id,
      client_org_id: input.client_org_id ?? scope.client_org_id,
      project_id: input.project_id ?? scope.project_id,
      scope_id: scope.id,
      sensitivity: input.sensitivity,
      tags: input.tags,
      visibility: scope.type === 'private' ? 'private' : 'shared',
      ...provenance,
    })
    this.registry.audit({
      actor_type: 'assistant',
      actor_id: instance.id,
      action: 'store_fact',
      target_id_hash: sha256Hex(fact.id),
      scope_id: scope.id,
      reason: null,
    })
    return fact
  }

  /**
   * Recall fan-out gouverné (spec §6.1) :
   * scopes autorisés → pré-filtre SQL par DB → fusion → scoring global →
   * filtre dur client → budget tokens GLOBAL → compteurs d'usage.
   */
  recall(input: RecallInput): RecallResult {
    this.assertOpen()
    return this.performRecall(input, (store, query, searchOpts) => store.searchFacts(query, searchOpts))
  }

  /**
   * Recall HYBRIDE (FTS + vectoriel, spec §10) : embedde la requête puis fusion
   * RRF par DB. Sans provider d'embeddings / sans extension vec / en cas
   * d'échec d'embedding → identique à recall() (dégradation annoncée).
   */
  async recallSemantic(input: RecallInput): Promise<RecallResult> {
    this.assertOpen()
    const provider = await this.ensureEmbeddings()
    if (!provider) return this.recall(input)
    let queryVector: Float32Array | undefined
    try {
      queryVector = (await provider.embed([input.query]))[0]
    } catch (err) {
      console.warn('[memoria] embedding de requête en échec — recall FTS seul :', (err as Error).message)
    }
    if (!queryVector) return this.recall(input)
    const vec = queryVector
    return this.performRecall(input, (store, query, searchOpts) =>
      hybridSearchFacts(store, query, { ...searchOpts, queryVector: vec, dimensions: provider.dimensions }),
    )
  }

  private performRecall(
    input: RecallInput,
    search: (store: ContentStore, query: string, opts: FtsSearchOptions) => FtsHit[],
  ): RecallResult {
    const instance = this.mustInstance(input.instance)
    const budget = input.token_budget ?? DEFAULT_TOKEN_BUDGET
    const limit = input.limit ?? DEFAULT_RECALL_LIMIT

    // CONTEXT-TREE (couche 9) : un contexte « projet » remonte sa hiérarchie
    // (projet → client → organisation) → le boost s'applique à tous les niveaux.
    const context = this.expandContextTree(input.active_context)
    const searchTargets = this.resolveReadTargets(instance)
    const now = Date.now()
    const procedural = isProceduralQuery(input.query) // boost procédures sur requête impérative
    const candidates: Array<{ item: RecallItem; store: ContentStore }> = []
    let totalFound = 0

    for (const target of searchTargets) {
      const store = this.openContent(target.dbPath)
      const hits = search(store, input.query, {
        limit: 50,
        includeDormant: input.include_dormant ?? false,
        maxSensitivity: 'sensitive',
        scopeIds: target.scopeIds,
      })
      totalFound += hits.length
      for (const hit of hits) {
        // FILTRE DUR anti-fuite inter-clients — jamais un boost, une exclusion.
        if (!passesClientIsolation(hit.row, context)) continue
        const parts = scoreFact(hit.row, hit.relevance, context, now, procedural)
        if (parts.total <= 0) continue
        candidates.push({
          store,
          item: {
            kind: 'fact',
            id: hit.row.id,
            content: hit.row.fact,
            category: hit.row.category,
            scope_id: hit.row.scope_id,
            source_db: relative(this.paths.root, target.dbPath),
            score: parts.total,
            created_at: hit.row.created_at,
          },
        })
      }
    }

    // --- Expansion graphe (bucket B au recall, §6.1 étape 4) : SQL pur, 0 LLM.
    // L'anti-fuite est garantie par expandEntities (bornée aux scopes autorisés).
    if (input.expand_graph !== false && candidates.length > 0) {
      const existing = new Set(candidates.map(c => c.item.id))
      const storeScopes = new Map<ContentStore, { scopeIds: string[]; dbPath: string }>()
      for (const target of searchTargets) {
        storeScopes.set(this.openContent(target.dbPath), { scopeIds: target.scopeIds, dbPath: target.dbPath })
      }
      const seedsByStore = new Map<ContentStore, string[]>()
      for (const c of candidates) {
        const arr = seedsByStore.get(c.store) ?? []
        if (arr.length < 8) arr.push(c.item.id)
        seedsByStore.set(c.store, arr)
      }
      for (const [store, seeds] of seedsByStore) {
        const meta = storeScopes.get(store)
        if (!meta || seeds.length === 0) continue
        const expanded = this.cognitionFor(store, null).expandEntities(seeds, meta.scopeIds, { maxHops: 2, maxFacts: 8 })
        for (const ex of expanded) {
          if (existing.has(ex.fact_id)) continue
          const row = store.db.prepare('SELECT * FROM facts WHERE id = ?').get(ex.fact_id) as FactRow | undefined
          if (!row) continue
          if (!passesClientIsolation(row, context)) continue
          // relevance dérivée du lien graphe, fortement escomptée (un voisin n'est
          // jamais aussi pertinent qu'un hit direct) ; on garde recency/confiance.
          const parts = scoreFact(row, Math.min(0.4, ex.score) * 0.5, context, now, procedural)
          if (parts.total <= 0) continue
          existing.add(ex.fact_id)
          candidates.push({
            store,
            item: {
              kind: 'fact',
              id: row.id,
              content: row.fact,
              category: row.category,
              scope_id: row.scope_id,
              source_db: relative(this.paths.root, meta.dbPath),
              score: parts.total,
              created_at: row.created_at,
            },
          })
        }
      }
    }

    candidates.sort((a, b) => b.item.score - a.item.score)

    // CAP DUR de tokens (corrige format.ts legacy : aucun cap global)
    const selected: Array<{ item: RecallItem; store: ContentStore }> = []
    let tokens = 0
    for (const c of candidates) {
      if (selected.length >= limit) break
      const cost = estimateTokens(c.item.content)
      if (tokens + cost > budget && selected.length > 0) continue
      tokens += cost
      selected.push(c)
    }

    // Compteurs d'usage par DB d'origine
    const byStore = new Map<ContentStore, string[]>()
    for (const s of selected) {
      const arr = byStore.get(s.store) ?? []
      arr.push(s.item.id)
      byStore.set(s.store, arr)
    }
    for (const [store, ids] of byStore) store.touchFacts(ids)

    this.registry.audit({
      actor_type: 'assistant',
      actor_id: instance.id,
      action: 'recall',
      target_id_hash: null,
      scope_id: null,
      reason: `returned=${selected.length}`,
    })

    return {
      items: selected.map(s => s.item),
      totalFound,
      tokens,
      scopes_searched: searchTargets.flatMap(t => t.scopeNames),
    }
  }

  /**
   * Capture WAL-first (spec §6.2) : redaction → WAL → extraction → dédup →
   * store. Respecte le capture_mode global : `incognito` = AUCUNE écriture.
   */
  async captureTurn(input: CaptureTurnInput): Promise<CaptureTurnResult & { mode: CaptureMode }> {
    this.assertOpen()
    this.mustInstance(input.instance)
    const mode = this.getCaptureMode()
    if (mode === 'incognito') {
      return { appended: 0, processed: 0, facts_created: 0, deferred: 0, failed: 0, abandoned: 0, mode }
    }
    const pipeline = await this.ensurePipeline()
    const result = await pipeline.captureTurn(input)
    // Bucket B ASYNC (jamais dans le chemin de réponse) : embeddings + cognition.
    if (result.facts_created > 0) {
      void this.indexEmbeddings(input.instance).catch((err: unknown) =>
        console.warn('[memoria] indexation embeddings en échec :', (err as Error).message),
      )
      void this.processCognition(input.instance).catch((err: unknown) =>
        console.warn('[memoria] traitement cognitif en échec :', (err as Error).message),
      )
    }
    return { ...result, mode }
  }

  /**
   * Traite les faits sans graphe (entités/relations/observations) d'une
   * instance. Async, bucket B — appelé après capture (fire-and-forget) et au
   * boot du daemon. LLM d'extraction optionnel (heuristique sinon).
   */
  async processCognition(instanceId?: string): Promise<{ processed: number }> {
    this.assertOpen()
    const { extraction } = await this.ensureProfile()
    const targets = instanceId
      ? [this.registry.dbForInstance(instanceId)].filter(Boolean)
      : this.registry.listDbs().filter(e => e.kind !== 'registry')
    let processed = 0
    for (const entry of targets) {
      if (!entry || !existsSync(entry.path)) continue
      const store = this.openContent(entry.path)
      const engine = this.cognitionFor(store, extraction)
      // faits actifs sans entité encore liée
      const pending = store.db
        .prepare(
          `SELECT f.id FROM facts f
           WHERE f.superseded = 0
             AND NOT EXISTS (SELECT 1 FROM fact_entities fe WHERE fe.fact_id = f.id)
           LIMIT 2000`,
        )
        .all() as Array<{ id: string }>
      for (const row of pending) {
        const r = await engine.processFact(row.id)
        if (r.processed) processed++
      }
      // TOPICS : ranger les faits par thème APRÈS que les entités existent (entité-first).
      await this.topicFor(store, extraction).assignPending(2000)
    }
    return { processed }
  }

  /** Thèmes (couche 14) : liste des sujets d'une instance, triés par importance. */
  listTopics(instanceId: string, minFacts = 1): TopicSummary[] {
    this.assertOpen()
    const db = this.registry.dbForInstance(instanceId)
    if (!db || !existsSync(db.path)) return []
    return this.topicFor(this.openContent(db.path), null).listTopics({ minFacts })
  }

  topicFacts(instanceId: string, topicId: string, limit = 50): Array<{ id: string; fact: string; category: string; created_at: string }> {
    this.assertOpen()
    const db = this.registry.dbForInstance(instanceId)
    if (!db || !existsSync(db.path)) return []
    return this.topicFor(this.openContent(db.path), null)
      .factsForTopic(topicId, { limit })
      .map(f => ({ id: f.id, fact: f.fact, category: f.category, created_at: f.created_at }))
  }

  /** Graphe des thèmes (couche 14) : qui est lié à qui, et par quoi. Lecture, 0 LLM. */
  topicRelations(instanceId: string, minFacts = 2): TopicGraph {
    this.assertOpen()
    const db = this.registry.dbForInstance(instanceId)
    if (!db || !existsSync(db.path)) return { nodes: [], edges: [] }
    return this.topicFor(this.openContent(db.path), null).relations({ minFacts })
  }

  /** Récurrences (couche 22) : détecte + liste les patterns proposés d'une instance. */
  detectPatterns(instanceId: string, minOccurrences = 3): { proposed: number } {
    this.assertOpen()
    const db = this.registry.dbForInstance(instanceId)
    if (!db || !existsSync(db.path)) return { proposed: 0 }
    const result = this.patternFor(this.openContent(db.path)).detect({ minOccurrences })
    return { proposed: result.proposed.length }
  }

  listPatterns(instanceId: string): Pattern[] {
    this.assertOpen()
    const db = this.registry.dbForInstance(instanceId)
    if (!db || !existsSync(db.path)) return []
    return this.patternFor(this.openContent(db.path)).listProposed()
  }

  decidePattern(instanceId: string, patternId: string, decision: 'accept' | 'dismiss'): { ok: boolean } {
    this.assertOpen()
    const db = this.registry.dbForInstance(instanceId)
    if (!db || !existsSync(db.path)) return { ok: false }
    const engine = this.patternFor(this.openContent(db.path))
    const result = decision === 'accept' ? engine.accept(patternId) : engine.dismiss(patternId)
    this.registry.audit({
      actor_type: 'user',
      actor_id: 'local',
      action: `pattern_${decision}`,
      target_id_hash: sha256Hex(patternId),
      scope_id: null,
      reason: null,
    })
    return { ok: result !== null }
  }

  /**
   * Context-tree (couche 9) : complète un contexte partiel via la hiérarchie du
   * registre. Déclarer un projet remonte implicitement son client et son
   * organisation → le boost de pertinence s'applique à tout l'arbre, et les
   * faits du client du projet redeviennent visibles (cohérent : le projet EST
   * pour ce client).
   */
  private expandContextTree(context: import('../types.js').ActiveContext | undefined): import('../types.js').ActiveContext | undefined {
    if (!context?.project_id) return context
    const project = this.registry.getProject(context.project_id)
    if (!project) return context
    return {
      ...context,
      client_org_id: context.client_org_id ?? project.client_org_id ?? undefined,
      org_id: context.org_id ?? project.owner_org_id,
    }
  }

  private topicFor(store: ContentStore, llm: import('../llm/provider.js').LlmProvider | null): TopicEngine {
    let engine = this.topicEngines.get(store)
    if (!engine) {
      engine = new TopicEngine({ store, llm })
      this.topicEngines.set(store, engine)
    }
    return engine
  }

  private patternFor(store: ContentStore): PatternEngine {
    let engine = this.patternEngines.get(store)
    if (!engine) {
      engine = new PatternEngine({ store })
      this.patternEngines.set(store, engine)
    }
    return engine
  }

  private proceduralFor(store: ContentStore): ProceduralEngine {
    let engine = this.proceduralEngines.get(store)
    if (!engine) {
      engine = new ProceduralEngine({ store })
      this.proceduralEngines.set(store, engine)
    }
    return engine
  }

  private feedbackFor(store: ContentStore): FeedbackEngine {
    let engine = this.feedbackEngines.get(store)
    if (!engine) {
      engine = new FeedbackEngine({ store })
      this.feedbackEngines.set(store, engine)
    }
    return engine
  }

  private clusterFor(store: ContentStore): ClusterEngine {
    let engine = this.clusterEngines.get(store)
    if (!engine) {
      engine = new ClusterEngine({ store })
      this.clusterEngines.set(store, engine)
    }
    return engine
  }

  private selfObsFor(store: ContentStore): SelfObservationEngine {
    let engine = this.selfObsEngines.get(store)
    if (!engine) {
      engine = new SelfObservationEngine({ store })
      this.selfObsEngines.set(store, engine)
    }
    return engine
  }

  private revisionFor(store: ContentStore): RevisionEngine {
    let engine = this.revisionEngines.get(store)
    if (!engine) {
      engine = new RevisionEngine({ store })
      this.revisionEngines.set(store, engine)
    }
    return engine
  }

  // ---------------------------------------------------- couches profondes (vague 7)

  /** Self-observation (couche 19) : l'agent observe son propre comportement. */
  selfObservations(instanceId: string, kind?: SelfObservation['kind']): SelfObservation[] {
    this.assertOpen()
    const db = this.registry.dbForInstance(instanceId)
    if (!db || !existsSync(db.path)) return []
    return this.selfObsFor(this.openContent(db.path)).list(kind ? { kind } : {})
  }

  /** Dérive forces/faiblesses/habitudes depuis procédures + patterns (opt-in, propose). */
  deriveSelfObservations(instanceId: string): { proposed: number } {
    this.assertOpen()
    const db = this.registry.dbForInstance(instanceId)
    if (!db || !existsSync(db.path)) return { proposed: 0 }
    const store = this.openContent(db.path)
    const procedures = this.proceduralFor(store).listProcedures().map(p => ({
      name: p.name,
      success_count: p.success_count,
      failure_count: p.failure_count,
    }))
    const patterns = this.patternFor(store).listProposed().map(p => ({ description: p.label, occurrences: p.occurrences }))
    const r = this.selfObsFor(store).deriveFromHistory({ procedures, patterns }, { instanceId })
    return { proposed: r.proposed.length }
  }

  /** Dialectic (couche 21) : confronte les points de vue de la mémoire (opt-in, lecture seule). */
  async dialectic(instanceId: string, question: string, limit = 12): Promise<DialecticResult> {
    this.assertOpen()
    const instance = this.mustInstance(instanceId)
    const targets = this.resolveReadTargets(instance)
    // Sur la DB privée (la principale) ; scopes autorisés transmis pour l'anti-fuite.
    const store = this.openContent(this.paths.assistantDb(instanceId))
    const scopeIds = targets.flatMap(t => t.scopeIds)
    return dialectic(store, question, { limit, scopeIds })
  }

  /** Revision (couches 18/24) : propose le ménage de la mémoire (contradits/doublons), sans rien modifier. */
  async proposeRevisions(instanceId: string, limit = 100): Promise<{ proposed: number }> {
    this.assertOpen()
    const db = this.registry.dbForInstance(instanceId)
    if (!db || !existsSync(db.path)) return { proposed: 0 }
    const r = await this.revisionFor(this.openContent(db.path)).propose({ limit })
    return { proposed: r.proposals.length }
  }

  listRevisions(instanceId: string): RevisionProposal[] {
    this.assertOpen()
    const db = this.registry.dbForInstance(instanceId)
    if (!db || !existsSync(db.path)) return []
    return this.revisionFor(this.openContent(db.path)).listProposals()
  }

  /** Applique (supersède) ou écarte une proposition de révision — SUR VALIDATION explicite. */
  decideRevision(instanceId: string, proposalId: string, decision: 'accept' | 'dismiss'): { ok: boolean } {
    this.assertOpen()
    const db = this.registry.dbForInstance(instanceId)
    if (!db) return { ok: false }
    const engine = this.revisionFor(this.openContent(db.path))
    const ok = decision === 'accept' ? engine.accept(proposalId).applied : engine.dismiss(proposalId)
    this.registry.audit({
      actor_type: 'user',
      actor_id: 'local',
      action: `revision_${decision}`,
      target_id_hash: sha256Hex(proposalId),
      scope_id: null,
      reason: null,
    })
    return { ok }
  }

  /** Auto-skill (couche 23) : propose des procédures consolidées depuis les récurrences (sur validation). */
  proposeSkills(instanceId: string): Array<{ label: string; steps: string[]; source: string }> {
    this.assertOpen()
    const db = this.registry.dbForInstance(instanceId)
    if (!db || !existsSync(db.path)) return []
    const proposals = new AutoSkillEngine({ store: this.openContent(db.path) }).propose()
    return proposals.map(p => ({ label: p.label, steps: p.steps, source: p.source }))
  }

  /** Markdown sync (couche 20, opt-in) : exporte la mémoire d'une instance en .md lisibles. */
  exportMarkdown(instanceId: string, outDir: string, byTopic = true): { files: string[]; facts: number } {
    this.assertOpen()
    const db = this.registry.dbForInstance(instanceId)
    if (!db || !existsSync(db.path)) return { files: [], facts: 0 }
    return new MarkdownSync({ store: this.openContent(db.path), outDir }).export({ byTopic })
  }

  // ---------------------------------------------------------- procédures (couche 6)

  /** Retrouve les meilleures procédures pour une tâche (FTS + taux de succès), gouverné. */
  matchProcedures(instanceId: string, query: string, limit = 5): ProcedureMatch[] {
    this.assertOpen()
    const instance = this.mustInstance(instanceId)
    const targets = this.resolveReadTargets(instance)
    const out: ProcedureMatch[] = []
    for (const target of targets) {
      const store = this.openContent(target.dbPath)
      out.push(...this.proceduralFor(store).matchProcedures(query, { scopeIds: target.scopeIds, limit }))
    }
    return out.sort((a, b) => b.score - a.score).slice(0, limit)
  }

  /** Apprentissage : enregistre le résultat d'exécution d'une procédure. */
  recordProcedureExecution(instanceId: string, procedureId: string, outcome: 'success' | 'failure', errorOutput?: string): boolean {
    this.assertOpen()
    const db = this.registry.dbForInstance(instanceId)
    if (!db) return false
    return this.proceduralFor(this.openContent(db.path)).recordExecution({ procedureId, outcome, errorOutput }).applied
  }

  listProcedures(instanceId: string): ProceduralProcedure[] {
    this.assertOpen()
    const db = this.registry.dbForInstance(instanceId)
    if (!db || !existsSync(db.path)) return []
    return this.proceduralFor(this.openContent(db.path)).listProcedures()
  }

  // ---------------------------------------------------------- feedback (couches 7-8)

  /** Renforce/atténue des faits selon leur usage réel dans une réponse. */
  reinforceFacts(instanceId: string, factIds: string[], used: boolean): void {
    this.assertOpen()
    const db = this.registry.dbForInstance(instanceId)
    if (!db) return
    this.feedbackFor(this.openContent(db.path)).reinforce(factIds, { used })
  }

  /** Domaines d'expertise de l'agent (où il « sait » le plus). */
  topExpertise(instanceId: string, limit = 10): Array<{ domain: string; level: number; evidence_count: number }> {
    this.assertOpen()
    const db = this.registry.dbForInstance(instanceId)
    if (!db || !existsSync(db.path)) return []
    return this.feedbackFor(this.openContent(db.path)).topDomains(limit)
  }

  /**
   * Amorce l'expertise depuis les thèmes existants : l'agent « maîtrise » les
   * sujets sur lesquels il a accumulé le plus de souvenirs. Le signal d'usage
   * (reinforce) l'affinera ensuite. Idempotent (recalcul complet).
   */
  bootstrapExpertise(instanceId: string): { domains: number } {
    this.assertOpen()
    const db = this.registry.dbForInstance(instanceId)
    if (!db || !existsSync(db.path)) return { domains: 0 }
    const store = this.openContent(db.path)
    const feedback = this.feedbackFor(store)
    const topics = this.topicFor(store, null).listTopics({ minFacts: 3 })
    let domains = 0
    for (const t of topics.slice(0, 30)) {
      feedback.updateExpertise(t.name, Math.log1p(t.fact_count))
      domains++
    }
    return { domains }
  }

  // ---------------------------------------------------------- clusters (couche 16)

  rebuildClusters(instanceId: string): { clusters: number } {
    this.assertOpen()
    const db = this.registry.dbForInstance(instanceId)
    if (!db || !existsSync(db.path)) return { clusters: 0 }
    const r = this.clusterFor(this.openContent(db.path)).rebuild()
    return { clusters: r.clusters }
  }

  listClusters(instanceId: string, minSize = 3): Array<{ id: string; label: string; size: number }> {
    this.assertOpen()
    const db = this.registry.dbForInstance(instanceId)
    if (!db || !existsSync(db.path)) return []
    return this.clusterFor(this.openContent(db.path))
      .listClusters({ minSize })
      .map(c => ({ id: c.id, label: c.label, size: c.size }))
  }

  /**
   * Importe le graphe cognitif (entités/relations/observations/topics) d'une
   * base legacy v3.34 vers la mémoire PRIVÉE d'une instance. Complète
   * `importLegacyDb` (qui ne ramène que faits + procédures). La base legacy est
   * ouverte en lecture seule. Idempotent.
   */
  importCognitionInto(legacyPath: string, instanceId: string): import('../migration/import-cognition.js').ImportCognitionReport {
    this.assertOpen()
    this.mustInstance(instanceId)
    const privateScope = this.registry.getScopeByName(`private:${instanceId}`)
    if (!privateScope) throw new Error(`scope privé introuvable pour l'instance ${instanceId}`)
    const store = this.openContent(this.paths.assistantDb(instanceId))
    const legacy = new DatabaseCtor(legacyPath, { readonly: true })
    try {
      const report = importLegacyCognition({ legacyDb: legacy, targetStore: store, scopeId: privateScope.id })
      this.registry.audit({
        actor_type: 'user',
        actor_id: 'local',
        action: 'import_cognition',
        target_id_hash: sha256Hex(instanceId),
        scope_id: privateScope.id,
        reason: `entities=${report.entities_imported};relations=${report.relations_imported};observations=${report.observations_imported}`,
      })
      return report
    } finally {
      legacy.close()
    }
  }

  /**
   * Importe des transcripts (Claude Code / Codex / Markdown) vers la mémoire
   * d'une instance, en QUARANTAINE (faits dormants + revue). Réutilise le LLM
   * d'extraction du profil. Idempotent par hash de fichier.
   */
  async importTranscripts(
    instanceId: string,
    files: string[],
    opts: {
      sinceDate?: string
      maxWindowsPerFile?: number
      dryRun?: boolean
      onProgress?: import('../migration/import-transcripts.js').ImportTranscriptsInput['onProgress']
    } = {},
  ): Promise<import('../migration/import-transcripts.js').ImportTranscriptsReport> {
    this.assertOpen()
    this.mustInstance(instanceId)
    const { extraction } = await this.ensureProfile()
    const report = await importTranscripts({
      files,
      memoria: this,
      instanceId,
      extraction,
      sinceDate: opts.sinceDate,
      maxWindowsPerFile: opts.maxWindowsPerFile,
      dryRun: opts.dryRun,
      onProgress: opts.onProgress,
    })
    if (!opts.dryRun && report.facts_quarantined > 0) {
      this.registry.audit({
        actor_type: 'user',
        actor_id: 'local',
        action: 'import_transcripts',
        target_id_hash: sha256Hex(instanceId),
        scope_id: null,
        reason: `quarantined=${report.facts_quarantined};files=${report.files_read}`,
      })
    }
    return report
  }

  /** Decay du graphe (job quotidien) sur toutes les DB de contenu. */
  decayCognition(): { decayed: number; pruned: number } {
    this.assertOpen()
    let decayed = 0
    let pruned = 0
    for (const entry of this.registry.listDbs()) {
      if (entry.kind === 'registry' || !existsSync(entry.path)) continue
      const r = this.cognitionFor(this.openContent(entry.path), null).decay()
      decayed += r.decayed
      pruned += r.pruned
    }
    return { decayed, pruned }
  }

  private cognitionFor(store: ContentStore, llm: import('../llm/provider.js').LlmProvider | null): CognitionEngine {
    let engine = this.cognitionEngines.get(store)
    if (!engine) {
      engine = new CognitionEngine({ store, llm })
      this.cognitionEngines.set(store, engine)
    }
    return engine
  }

  /**
   * Indexe les faits sans embedding (une instance, ou toutes). Appelé après
   * chaque capture (fire-and-forget) et au boot du daemon. Sans provider
   * d'embeddings → no-op.
   */
  async indexEmbeddings(instanceId?: string): Promise<{ indexed: number }> {
    this.assertOpen()
    const provider = await this.ensureEmbeddings()
    if (!provider) return { indexed: 0 }
    let indexed = 0
    const targets = instanceId
      ? [this.registry.dbForInstance(instanceId)].filter(Boolean)
      : this.registry.listDbs().filter(e => e.kind !== 'registry')
    for (const entry of targets) {
      if (!entry || !existsSync(entry.path)) continue
      const store = this.openContent(entry.path)
      let indexer = this.indexers.get(store)
      if (!indexer) {
        indexer = new EmbeddingIndexer({ store, provider })
        this.indexers.set(store, indexer)
      }
      const run = await indexer.runAll()
      indexed += run.indexed
    }
    return { indexed }
  }

  /** Rejeu du WAL au boot (daemon) : aucune entrée pending n'est oubliée. */
  async replayWal(): Promise<Array<{ instance: string; summary: WalReplaySummary }>> {
    this.assertOpen()
    const pipeline = await this.ensurePipeline()
    const out: Array<{ instance: string; summary: WalReplaySummary }> = []
    for (const inst of this.registry.listInstances()) {
      if (inst.revoked_at) continue
      const db = this.registry.dbForInstance(inst.id)
      if (!db || !existsSync(db.path)) continue
      const summary = await pipeline.replayAtBoot(inst.id)
      out.push({ instance: inst.id, summary })
    }
    return out
  }

  /**
   * Un moteur d'extraction est-il configuré ET joignable ? Sert de garde-fou
   * AVANT de lancer un job d'import (422 côté daemon : « Configure d'abord un
   * moteur d'intelligence ») — plutôt qu'un job qui tourne pour rien.
   */
  async hasExtraction(): Promise<boolean> {
    this.assertOpen()
    const { extraction } = await this.ensureProfile()
    if (!extraction) return false
    try {
      return await extraction.isAvailable()
    } catch (err) {
      console.warn(`[memoria] disponibilité du moteur d'extraction : ${(err as Error).message}`)
      return false
    }
  }

  /** Profil LLM résolu UNE fois (override tests/daemon > résolution auto). */
  private ensureProfile(): Promise<{ extraction: LlmProvider | null; embeddings: EmbeddingProvider | null }> {
    this.profilePromise ??= (async () => {
      if (this.llmOverride !== undefined) {
        return { extraction: this.llmOverride.extraction, embeddings: this.llmOverride.embeddings ?? null }
      }
      const profile = await resolveLlmProfile(this.resolved.config)
      return { extraction: profile.extraction, embeddings: profile.embeddings }
    })()
    return this.profilePromise
  }

  private async ensureEmbeddings(): Promise<EmbeddingProvider | null> {
    return (await this.ensureProfile()).embeddings
  }

  /** Pipeline de capture construit une fois (résolution LLM comprise). */
  private ensurePipeline(): Promise<CapturePipeline> {
    this.pipelinePromise ??= (async () => {
      const { extraction } = await this.ensureProfile()
      return new CapturePipeline({
        openStore: id => this.openContent(this.paths.assistantDb(id)),
        // ID du scope (pas le nom) : findDuplicate compare facts.scope_id
        defaultScope: id => {
          const scope = this.registry.getScopeByName(`private:${id}`)
          if (!scope) throw new Error(`scope privé introuvable pour l'instance ${id}`)
          return scope.id
        },
        storeFact: input => this.storeCaptured(input),
        audit: entry => this.registry.audit(entry),
        redactor: this.redactor,
        secretSink: s => {
          this.secretProvider.set(s.name, s.value)
          this.registry.upsertSecretRef(s.name, this.secretProvider.locationFor(s.name), s.kind)
        },
        extraction,
      })
    })()
    return this.pipelinePromise
  }

  /**
   * Écriture issue de la CAPTURE : en mode review-first le fait naît DORMANT
   * (invisible au recall) + entre en file de revue ; l'approbation l'active.
   */
  private storeCaptured(input: StoreFactInput): Fact {
    const fact = this.storeFact({ ...input, source: input.source ?? 'capture' })
    if (this.getCaptureMode() !== 'review-first') return fact

    const store = this.openContent(this.paths.assistantDb(input.instance))
    store.db.prepare("UPDATE facts SET lifecycle_state = 'dormant' WHERE id = ?").run(fact.id)
    const sourceId = this.ensureReviewSource(store, input.instance)
    store.db
      .prepare(
        `INSERT INTO memory_import_items (id, source_id, target_memory_id, target_type, proposed_scope_id, status, confidence)
         VALUES (?, ?, ?, 'fact', ?, 'pending', ?)`,
      )
      .run(newId(), sourceId, fact.id, fact.scope_id, fact.confidence)
    return { ...fact, lifecycle_state: 'dormant' }
  }

  /** Source unique « capture-review » par instance (provenance des items en revue). */
  private ensureReviewSource(store: ContentStore, instanceId: string): string {
    const hash = sha256Hex(`capture-review:${instanceId}`)
    const existing = store.db.prepare('SELECT id FROM memory_sources WHERE source_hash = ?').get(hash) as
      | { id: string }
      | undefined
    if (existing) return existing.id
    const id = newId()
    store.db
      .prepare(
        `INSERT INTO memory_sources (id, source_type, source_path, source_hash, imported_at, metadata)
         VALUES (?, 'capture-review', NULL, ?, ?, ?)`,
      )
      .run(id, hash, new Date().toISOString(), JSON.stringify({ instance: instanceId }))
    return id
  }

  /** File de revue : items pending (capture review-first ET quarantaine d'import). */
  listReview(opts: { limit?: number } = {}): Array<{
    id: string
    fact_id: string
    content: string
    category: string
    confidence: number
    source_type: string
    source_db: string
    created_at: string
    topics: string[]
  }> {
    this.assertOpen()
    const limit = Math.min(opts.limit ?? 100, 500)
    const out: ReturnType<Memoria['listReview']> = []
    for (const entry of this.registry.listDbs()) {
      if (entry.kind === 'registry' || !existsSync(entry.path)) continue
      const store = this.openContent(entry.path)
      const topicEngine = this.topicFor(store, null)
      const rows = store.db
        .prepare(
          `SELECT i.id, i.target_memory_id AS fact_id, i.confidence, s.source_type,
                  f.fact AS content, f.category, f.created_at
           FROM memory_import_items i
           JOIN memory_sources s ON s.id = i.source_id
           JOIN facts f ON f.id = i.target_memory_id
           WHERE i.status = 'pending' AND i.target_type = 'fact'
           ORDER BY f.created_at DESC LIMIT ?`,
        )
        .all(limit) as Array<Omit<ReturnType<Memoria['listReview']>[number], 'source_db' | 'topics'>>
      for (const row of rows) {
        out.push({
          ...row,
          source_db: relative(this.paths.root, entry.path),
          topics: topicEngine.topicsForFact(row.fact_id).map(t => t.name),
        })
      }
    }
    return out.slice(0, limit)
  }

  /** Approuve (active) ou rejette (hard-delete) des items de revue. */
  reviewDecision(itemIds: string[], decision: 'accepted' | 'rejected'): { updated: number } {
    this.assertOpen()
    if (itemIds.length === 0) return { updated: 0 }
    let updated = 0
    for (const entry of this.registry.listDbs()) {
      if (entry.kind === 'registry' || !existsSync(entry.path)) continue
      const store = this.openContent(entry.path)
      const placeholders = itemIds.map(() => '?').join(',')
      const rows = store.db
        .prepare(
          `SELECT id, target_memory_id FROM memory_import_items WHERE id IN (${placeholders}) AND status = 'pending'`,
        )
        .all(...itemIds) as Array<{ id: string; target_memory_id: string }>
      if (rows.length === 0) continue
      const tx = store.db.transaction(() => {
        const factIds = rows.map(r => r.target_memory_id)
        if (decision === 'accepted') {
          const fp = factIds.map(() => '?').join(',')
          store.db.prepare(`UPDATE facts SET lifecycle_state = 'active' WHERE id IN (${fp})`).run(...factIds)
        } else {
          store.hardDeleteFacts(factIds)
        }
        const ip = rows.map(() => '?').join(',')
        store.db
          .prepare(
            `UPDATE memory_import_items SET status = ?, reviewed_by = 'local', reviewed_at = ? WHERE id IN (${ip})`,
          )
          .run(decision, new Date().toISOString(), ...rows.map(r => r.id))
      })
      tx()
      updated += rows.length
      this.registry.audit({
        actor_type: 'user',
        actor_id: 'local',
        action: `review_${decision}`,
        target_id_hash: sha256Hex(rows.map(r => r.target_memory_id).sort().join(',')),
        scope_id: null,
        reason: `items=${rows.length}`,
      })
    }
    return { updated }
  }

  /**
   * Nombre de faits encore en quarantaine legacy (`legacy_to_review`).
   * Garde-fou des imports : le scope est UNIQUE — on refuse d'importer une 2e
   * base legacy tant que la quarantaine n'est pas vidée (adoptLegacyInto).
   */
  legacyQuarantineCount(): number {
    this.assertOpen()
    const scope = this.registry.getScopeByName('legacy_to_review')
    if (!scope) return 0
    const entry = this.registry.dbForScope(scope.id)
    if (!entry || !existsSync(entry.path)) return 0
    return this.openContent(entry.path).countFacts()
  }

  /**
   * Adopte la quarantaine (`legacy_to_review`) vers la mémoire PRIVÉE d'une
   * instance : les souvenirs hérités deviennent réellement à elle et
   * recallables. Déplacement (copie dans la DB privée + retrait de la
   * quarantaine), pas duplication. Réversible via le backup d'import.
   */
  adoptLegacyInto(instanceId: string, opts: { reindex?: boolean } = {}): { facts: number; procedures: number } {
    this.assertOpen()
    const instance = this.mustInstance(instanceId)
    const legacyScope = this.registry.getScopeByName('legacy_to_review')
    if (!legacyScope) return { facts: 0, procedures: 0 }
    const legacyDbEntry = this.registry.dbForScope(legacyScope.id)
    if (!legacyDbEntry || !existsSync(legacyDbEntry.path)) return { facts: 0, procedures: 0 }

    const source = this.openContent(legacyDbEntry.path)
    const targetPath = this.paths.assistantDb(instanceId)
    const target = this.openContent(targetPath)
    const privateScope = this.registry.getScopeByName(`private:${instanceId}`)
    if (!privateScope) throw new Error(`scope privé introuvable pour l'instance ${instanceId}`)

    const factRows = source.db.prepare('SELECT * FROM facts').all() as FactRow[]
    const procRows = source.db.prepare('SELECT * FROM procedures').all() as Array<Record<string, unknown>>

    const factCols = source.db.pragma('table_info(facts)') as Array<{ name: string }>
    const procCols = source.db.pragma('table_info(procedures)') as Array<{ name: string }>
    const factColNames = factCols.map(c => c.name)
    const procColNames = procCols.map(c => c.name)

    const insertFact = target.db.prepare(
      `INSERT OR IGNORE INTO facts (${factColNames.join(',')}) VALUES (${factColNames.map(c => '@' + c).join(',')})`,
    )
    const insertProc = procColNames.length
      ? target.db.prepare(
          `INSERT OR IGNORE INTO procedures (${procColNames.join(',')}) VALUES (${procColNames.map(c => '@' + c).join(',')})`,
        )
      : null

    const move = target.db.transaction(() => {
      let f = 0
      for (const row of factRows) {
        insertFact.run({ ...row, scope_id: privateScope.id, assistant_instance_id: instanceId, visibility: 'private', lifecycle_state: 'active' })
        f++
      }
      let p = 0
      if (insertProc) {
        for (const row of procRows) {
          insertProc.run({ ...row, scope_id: privateScope.id, assistant_instance_id: instanceId })
          p++
        }
      }
      return { f, p }
    })
    const moved = move()

    // Vide la quarantaine (le backup d'import reste la sécurité de rollback)
    source.db.exec('DELETE FROM memory_import_items; DELETE FROM facts; DELETE FROM procedures; DELETE FROM memory_sources;')

    this.registry.audit({
      actor_type: 'user',
      actor_id: 'local',
      action: 'adopt_legacy',
      target_id_hash: sha256Hex(instanceId),
      scope_id: privateScope.id,
      reason: `facts=${moved.f};procedures=${moved.p}`,
    })

    if (opts.reindex) {
      void this.indexEmbeddings(instanceId).catch((err: unknown) =>
        console.warn('[memoria] réindexation post-adoption en échec :', (err as Error).message),
      )
    }
    void instance
    return { facts: moved.f, procedures: moved.p }
  }

  // ------------------------------------------------------------------ partage

  /**
   * Promeut des faits vers un scope PARTAGÉ (`user`/`org`/…) : ils quittent la
   * mémoire privée de leur agent et deviennent recallables par tout agent
   * autorisé sur ce scope (spec §11, partage gouverné). Déplacement, pas copie.
   */
  shareFacts(factIds: string[], targetScopeRef: string): { shared: number; scope: string } {
    this.assertOpen()
    if (factIds.length === 0) return { shared: 0, scope: targetScopeRef }
    const scope = this.registry.getScope(targetScopeRef) ?? this.registry.getScopeByName(targetScopeRef)
    if (!scope) throw new Error(`scope cible inconnu : ${targetScopeRef}`)
    if (scope.type === 'private' || scope.type === 'legacy_to_review') {
      throw new Error(`partage interdit vers un scope ${scope.type}`)
    }
    const targetPath = this.sharedDbPathPublic(scope)
    const target = this.openContent(targetPath)
    this.registry.registerDb({ kind: 'shared', path: targetPath, assistant_instance_id: null, scope_id: scope.id })

    const idSet = new Set(factIds)
    let shared = 0
    for (const entry of this.registry.listDbs()) {
      if (entry.kind === 'registry' || entry.path === targetPath || !existsSync(entry.path)) continue
      const store = this.openContent(entry.path)
      const placeholders = [...idSet].map(() => '?').join(',')
      const rows = store.db.prepare(`SELECT * FROM facts WHERE id IN (${placeholders})`).all(...idSet) as FactRow[]
      if (rows.length === 0) continue
      const cols = (store.db.pragma('table_info(facts)') as Array<{ name: string }>).map(c => c.name)
      const insert = target.db.prepare(
        `INSERT OR IGNORE INTO facts (${cols.join(',')}) VALUES (${cols.map(c => '@' + c).join(',')})`,
      )
      const tx = target.db.transaction(() => {
        for (const row of rows) {
          insert.run({
            ...row,
            scope_id: scope.id,
            visibility: 'shared',
            org_id: scope.org_id ?? row.org_id,
            client_org_id: scope.client_org_id ?? row.client_org_id,
            project_id: scope.project_id ?? row.project_id,
          })
          shared++
        }
      })
      tx()
      store.hardDeleteFacts(rows.map(r => r.id))
    }
    if (shared > 0) {
      this.registry.audit({
        actor_type: 'user',
        actor_id: 'local',
        action: 'share_facts',
        target_id_hash: sha256Hex([...idSet].sort().join(',')),
        scope_id: scope.id,
        reason: `shared=${shared}`,
      })
    }
    return { shared, scope: scope.name }
  }

  /** Scopes + agents qui peuvent les lire (matrice de partage UI). */
  // ------------------------------------------------------------ synchro inter-machines

  /** ContentStore d'un scope PARTAGÉ (ouvre/enregistre la DB locale). null si privé/inconnu. */
  sharedContentStore(scopeId: string): ContentStore | null {
    this.assertOpen()
    const scope = this.registry.getScope(scopeId)
    if (!scope || scope.type === 'private' || scope.type === 'legacy_to_review') return null
    const path = this.sharedDbPathPublic(scope)
    const store = this.openContent(path)
    this.registry.registerDb({ kind: 'shared', path, assistant_instance_id: null, scope_id: scope.id })
    return store
  }

  /** Scopes synchronisables présents localement (types whitelistés). */
  syncableScopes(whitelist: readonly string[]): MemoryScope[] {
    this.assertOpen()
    return this.registry.listScopes().filter(s => whitelist.includes(s.type))
  }

  /** Configure cette machine comme HUB de synchro (persiste). Redémarrage requis pour le listener LAN. */
  configureSyncHub(listenLan: string, scopes?: string[]): void {
    this.assertOpen()
    this.resolved.config.sync = {
      ...this.resolved.config.sync,
      enabled: true,
      role: 'hub',
      machine_id: localMachineId(this.registry),
      listen_lan: listenLan,
      ...(scopes ? { scopes } : {}),
    }
    saveConfigFile(this.resolved.config, this.resolved.configPath)
    this.syncEngine = undefined // re-construire avec la nouvelle config
  }

  /** Coffre local (pour le module de synchro — clés GVK/CPK + valeurs scellées). */
  get secrets(): SecretProvider {
    return this.secretProvider
  }

  /** Moteur de synchro inter-machines (lazy). Construit avec la config [sync]. */
  get sync(): SyncEngine {
    if (!this.syncEngine) {
      this.syncEngine = new SyncEngine({
        registry: this.registry,
        secrets: this.secretProvider,
        machineId: localMachineId(this.registry),
        config: this.resolved.config.sync ?? {},
        sharedStore: (scopeId: string) => this.sharedContentStore(scopeId),
        listSyncableScopes: (whitelist: readonly string[]) => this.syncableScopes(whitelist),
        persistConfig: () => saveConfigFile(this.resolved.config, this.resolved.configPath),
        setSyncConfig: (patch: Record<string, unknown>) => {
          this.resolved.config.sync = { ...this.resolved.config.sync, ...patch }
        },
      })
    }
    return this.syncEngine
  }

  listScopesWithAccess(): Array<{ id: string; type: string; name: string; readers: string[]; facts: number }> {
    this.assertOpen()
    return this.registry.listScopes().map(scope => {
      const readers = this.registry
        .listAssistants()
        .filter(a => this.registry.getPolicy(a.id, scope.id)?.can_read)
        .map(a => a.id)
      let facts = 0
      const dbEntry = scope.type === 'private' ? null : this.registry.dbForScope(scope.id)
      if (dbEntry && existsSync(dbEntry.path)) {
        facts = (this.openContent(dbEntry.path).db.prepare('SELECT COUNT(*) AS c FROM facts WHERE scope_id = ?').get(scope.id) as { c: number }).c
      }
      return { id: scope.id, type: scope.type, name: scope.name, readers, facts }
    })
  }

  /** Accorde/retire à un assistant l'accès à un scope (matrice de partage). */
  setScopeAccess(
    assistantId: string,
    scopeId: string,
    perms: { can_read?: boolean; can_write?: boolean; can_share?: boolean; secret_access?: 'none' | 'refs_only' | 'value_on_request' },
  ): void {
    this.assertOpen()
    const current = this.registry.getPolicy(assistantId, scopeId)
    this.registry.setPolicy({
      assistant_id: assistantId,
      scope_id: scopeId,
      can_read: perms.can_read ?? current?.can_read ?? false,
      can_write: perms.can_write ?? current?.can_write ?? false,
      can_share: perms.can_share ?? current?.can_share ?? false,
      secret_access: perms.secret_access ?? current?.secret_access ?? 'none',
    })
    this.registry.audit({
      actor_type: 'user',
      actor_id: 'local',
      action: 'set_scope_access',
      target_id_hash: sha256Hex(`${assistantId}:${scopeId}`),
      scope_id: scopeId,
      reason: JSON.stringify(perms),
    })
  }

  /**
   * Repère, dans la mémoire d'une instance, les faits qui parlent de
   * l'utilisateur (identité/préférences) — candidats à promouvoir vers `user`.
   * Ne décide RIEN : retourne des propositions que l'utilisateur valide.
   */
  suggestIdentityFacts(instanceId: string, limit = 50): Array<{ id: string; content: string; category: string; score: number }> {
    this.assertOpen()
    const db = this.registry.dbForInstance(instanceId)
    if (!db || !existsSync(db.path)) return []
    const store = this.openContent(db.path)
    const rows = store.db.prepare('SELECT * FROM facts WHERE superseded = 0').all() as FactRow[]
    const user = this.registry.bootstrap().user
    const nameTokens = user.display_name.toLowerCase().split(/\s+/).filter(t => t.length > 2)
    const cues = [
      ...nameTokens,
      'utilisateur', 'préfère', 'prefere', 'aime', 'déteste', 'deteste', 'veut', 'identité', 'identity',
      'son nom', 'mon nom', 'email', 'courriel', 'téléphone', 'adresse', 'anniversaire', 'langue',
      'pompeu', 'neto', 'primo',
    ]
    const identityCats = new Set(['identity', 'preference', 'profil', 'profile', 'user', 'savoir'])
    const scored = rows
      .map(r => {
        const text = r.fact.toLowerCase()
        let score = 0
        for (const cue of cues) if (text.includes(cue)) score += cue.length > 4 ? 2 : 1
        if (identityCats.has(r.category.toLowerCase())) score += 1
        return { id: r.id, content: r.fact, category: r.category, score }
      })
      .filter(c => c.score >= 2)
      .sort((a, b) => b.score - a.score)
      .slice(0, limit)
    return scored
  }

  /** Variante publique de sharedDbPath (utilisée par shareFacts). */
  private sharedDbPathPublic(scope: MemoryScope): string {
    return this.sharedDbPath(scope)
  }

  /** Hard-delete gouverné (spec §11). */
  forget(filter: ForgetFilter): { deleted: number } {
    this.assertOpen()
    const hasIds = (filter.ids?.length ?? 0) > 0
    if (!hasIds && !filter.query && !filter.category && !filter.scope_id) {
      throw new Error('forget : filtre vide refusé')
    }
    if (!hasIds && !filter.query && filter.confirm_bulk !== true) {
      throw new Error('forget : suppression en masse — confirm_bulk requis')
    }

    let deleted = 0
    for (const entry of this.registry.listDbs()) {
      if (entry.kind === 'registry') continue
      const store = this.openContent(entry.path)
      let ids = filter.ids ?? []
      if (!hasIds) {
        const conditions: string[] = []
        const params: unknown[] = []
        if (filter.scope_id) {
          conditions.push('scope_id = ?')
          params.push(filter.scope_id)
        }
        if (filter.category) {
          conditions.push('category = ?')
          params.push(filter.category)
        }
        let rows: Array<{ id: string }>
        if (filter.query) {
          rows = store
            .searchFacts(filter.query, { limit: 500, includeDormant: true, maxSensitivity: 'critical', scopeIds: filter.scope_id ? [filter.scope_id] : undefined })
            .map(h => ({ id: h.row.id }))
          if (filter.category) rows = rows.filter(r => store.getFact(r.id)?.category === filter.category)
        } else {
          rows = store.db
            .prepare(`SELECT id FROM facts${conditions.length ? ` WHERE ${conditions.join(' AND ')}` : ''}`)
            .all(...params) as Array<{ id: string }>
        }
        ids = rows.map(r => r.id)
      }
      if (ids.length === 0) continue
      // Nettoyer thèmes + récurrences AVANT le hard-delete (lisent fact_topics).
      this.topicFor(store, null).onForget(ids)
      this.patternFor(store).onForget(ids)
      const n = store.hardDeleteFacts(ids)
      deleted += n
      if (n > 0) {
        this.registry.audit({
          actor_type: 'user',
          actor_id: 'local',
          action: 'forget',
          target_id_hash: sha256Hex(ids.slice().sort().join(',')),
          scope_id: filter.scope_id ?? null,
          reason: `deleted=${n}`,
        })
      }
    }
    return { deleted }
  }

  // -------------------------------------------------------------------- admin

  /**
   * Navigation admin dans la mémoire (UI web) : faits d'une instance (sa DB
   * privée) ou de toutes les DB, récents d'abord ou filtrés FTS.
   */
  browseFacts(opts: { instance?: string; q?: string; limit?: number } = {}): Array<Fact & { source_db: string; topics: string[] }> {
    this.assertOpen()
    const limit = Math.min(opts.limit ?? 50, 200)
    const targets: string[] = []
    if (opts.instance) {
      const db = this.registry.dbForInstance(opts.instance)
      if (db) targets.push(db.path)
    } else {
      for (const entry of this.registry.listDbs()) {
        if (entry.kind !== 'registry' && existsSync(entry.path)) targets.push(entry.path)
      }
    }
    const out: Array<Fact & { source_db: string; topics: string[] }> = []
    for (const path of targets) {
      const store = this.openContent(path)
      const label = relative(this.paths.root, path)
      const topicEngine = this.topicFor(store, null)
      const withTopics = (row: FactRow): Fact & { source_db: string; topics: string[] } => ({
        ...rowToFact(row),
        source_db: label,
        topics: topicEngine.topicsForFact(row.id).map(t => t.name),
      })
      if (opts.q) {
        for (const hit of store.searchFacts(opts.q, { limit, includeDormant: true, maxSensitivity: 'critical' })) {
          out.push(withTopics(hit.row))
        }
      } else {
        const rows = store.db
          .prepare('SELECT * FROM facts ORDER BY created_at DESC LIMIT ?')
          .all(limit) as FactRow[]
        for (const row of rows) out.push(withTopics(row))
      }
    }
    out.sort((a, b) => (a.created_at < b.created_at ? 1 : -1))
    return out.slice(0, limit)
  }

  /**
   * Recherche GLOBALE : un seul champ qui interroge la mémoire de TOUS les agents
   * (+ scopes partagés) d'un coup, chaque résultat étiqueté de l'agent dont il
   * vient. « Où, chez n'importe quel agent, ai-je vu X ? » Lecture pure.
   */
  globalSearch(q: string, limit = 80): Array<Fact & { source_db: string; topics: string[]; agent_type: string; instance: string | null }> {
    this.assertOpen()
    // carte chemin-relatif → (type, instance) pour étiqueter les résultats
    const byDb = new Map<string, { type: string; instance: string }>()
    for (const a of this.listAgents()) {
      if (a.db_path) byDb.set(relative(this.paths.root, a.db_path), { type: a.assistant_type, instance: a.instance.id })
    }
    return this.browseFacts({ q, limit }).map(f => {
      const owner = byDb.get(f.source_db)
      return { ...f, agent_type: owner?.type ?? 'partagé', instance: owner?.instance ?? null }
    })
  }

  /**
   * Détection des moteurs d'IA disponibles (onboarding/réglages §14) :
   * Ollama (modèles présents), LM Studio, clé Anthropic. Sans réseau bloquant.
   */
  async detectProviders(): Promise<{
    ollama: { available: boolean; models: string[]; base_url: string }
    lmstudio: { available: boolean; models: string[]; base_url: string }
    anthropic: { available: boolean }
    openai: { available: boolean }
    openrouter: { available: boolean }
  }> {
    this.assertOpen()
    const { resolveAnthropicApiKey, resolveOpenAiApiKey, DEFAULT_OLLAMA_BASE_URL, DEFAULT_LMSTUDIO_BASE_URL, lmstudioListModels } =
      await import('../llm/index.js')
    const ollamaBase = DEFAULT_OLLAMA_BASE_URL
    let ollamaModels: string[] = []
    let ollamaUp = false
    try {
      const res = await fetch(`${ollamaBase}/api/tags`, { signal: AbortSignal.timeout(1500) })
      if (res.ok) {
        ollamaUp = true
        const data = (await res.json()) as { models?: Array<{ name: string }> }
        ollamaModels = (data.models ?? []).map(m => m.name)
      }
    } catch {
      ollamaUp = false
    }
    const lm = await lmstudioListModels()
    return {
      ollama: { available: ollamaUp, models: ollamaModels, base_url: ollamaBase },
      lmstudio: { available: lm.up, models: lm.models, base_url: DEFAULT_LMSTUDIO_BASE_URL },
      anthropic: { available: resolveAnthropicApiKey({}) !== null },
      openai: { available: resolveOpenAiApiKey({ flavor: 'openai' }) !== null },
      openrouter: { available: resolveOpenAiApiKey({ flavor: 'openrouter' }) !== null },
    }
  }

  /** Nombre TOTAL d'entrées WAL en attente d'extraction, toutes instances confondues. */
  walPendingTotal(): number {
    this.assertOpen()
    let pending = 0
    for (const entry of this.registry.listDbs()) {
      if (entry.kind === 'registry' || !existsSync(entry.path)) continue
      pending += this.openContent(entry.path).walPendingCount()
    }
    return pending
  }

  /**
   * Santé LLM (GET /v1/admin/llm_health) — LA source de vérité anti-mort-
   * silencieuse : moteur d'extraction/embeddings effectifs (résolution FRAÎCHE,
   * pas le mémo : l'utilisateur vient peut-être de télécharger un modèle),
   * entrées WAL en attente, et inventaire des options disponibles.
   */
  async llmHealth(opts: { ollamaBaseUrl?: string; lmstudioBaseUrl?: string } = {}): Promise<LlmHealthReport> {
    this.assertOpen()
    const {
      DEFAULT_ANTHROPIC_MODEL,
      DEFAULT_LOCAL_EXTRACTION_MODEL,
      DEFAULT_OLLAMA_EMBEDDING_MODEL,
      DEFAULT_OPENAI_MODEL,
      DEFAULT_OPENROUTER_MODEL,
      detectLlmOptions,
      modelMatches,
      resolveLlmProfile,
    } = await import('../llm/index.js')

    const options = await detectLlmOptions({ ollamaBaseUrl: opts.ollamaBaseUrl, lmstudioBaseUrl: opts.lmstudioBaseUrl })
    const profile = await resolveLlmProfile(this.resolved.config, {
      ollamaBaseUrl: opts.ollamaBaseUrl,
      lmstudioBaseUrl: opts.lmstudioBaseUrl,
    })

    // ---- extraction : disponible (provider résolu) ou indisponible AVEC raison
    let extraction: LlmEngineHealth
    if (profile.extraction) {
      extraction = { provider: profile.extraction.name, model: profile.extraction.model, available: true }
    } else {
      const explicit = this.resolved.config.llm?.extraction
      const profileName = this.resolved.config.llm?.profile ?? '100-local'
      const provider = explicit?.provider ?? (profileName === 'cloud' ? 'anthropic' : 'ollama')
      const defaults: Record<string, string> = {
        ollama: DEFAULT_LOCAL_EXTRACTION_MODEL,
        lmstudio: '(premier modèle chargé)',
        anthropic: DEFAULT_ANTHROPIC_MODEL,
        openai: DEFAULT_OPENAI_MODEL,
        openrouter: DEFAULT_OPENROUTER_MODEL,
      }
      const model = explicit?.model ?? defaults[provider] ?? '(inconnu)'
      let reason: string
      switch (provider) {
        case 'ollama': {
          if (!options.ollama.serverUp) {
            reason = 'serveur Ollama injoignable — lance l’application Ollama (ou « ollama serve »)'
          } else {
            const wanted = explicit?.model ?? DEFAULT_LOCAL_EXTRACTION_MODEL
            reason = options.ollama.models.some(m => modelMatches(m, wanted))
              ? `modèle « ${wanted} » présent mais provider indisponible — vérifie les logs du service`
              : `modèle « ${wanted} » non téléchargé — « ollama pull ${wanted} »`
          }
          break
        }
        case 'lmstudio':
          reason = !options.lmstudio.available
            ? 'LM Studio injoignable — démarre son serveur local (onglet Developer)'
            : options.lmstudio.models.length === 0
              ? 'aucun modèle chargé dans LM Studio'
              : `modèle « ${explicit?.model ?? ''} » non chargé dans LM Studio`
          break
        case 'anthropic':
        case 'openai':
        case 'openrouter':
          reason = `clé API absente — place-la dans ~/.${provider}/api_key (chmod 600)`
          break
        default:
          reason = `provider inconnu : ${provider}`
      }
      extraction = { provider, model, available: false, reason }
    }

    // ---- embeddings : Ollama nomic-embed-text UNIQUEMENT en V1 — on le DIT
    let embeddings: LlmEngineHealth
    if (profile.embeddings) {
      embeddings = { provider: profile.embeddings.name, model: profile.embeddings.model, available: true }
    } else {
      embeddings = {
        provider: 'ollama',
        model: DEFAULT_OLLAMA_EMBEDDING_MODEL,
        available: false,
        reason: options.ollama.serverUp
          ? `Recherche sémantique : nécessite Ollama (${DEFAULT_OLLAMA_EMBEDDING_MODEL}) — « ollama pull ${DEFAULT_OLLAMA_EMBEDDING_MODEL} »`
          : `Recherche sémantique : nécessite Ollama (${DEFAULT_OLLAMA_EMBEDDING_MODEL}) — serveur Ollama injoignable`,
      }
    }

    return { extraction, embeddings, wal_pending: this.walPendingTotal(), options }
  }

  /** Profil LLM courant (config) + choix explicite d'extraction s'il existe. */
  getLlmProfile(): { profile: string; extraction?: { provider?: string; model?: string; base_url?: string } } {
    this.assertOpen()
    return {
      profile: this.resolved.config.llm?.profile ?? '100-local',
      extraction: this.resolved.config.llm?.extraction,
    }
  }

  /** Change le profil LLM (raccourci) et le persiste. */
  setLlmProfile(profile: string): void {
    this.assertOpen()
    // Choisir un profil raccourci efface le choix explicite de provider.
    this.resolved.config.llm = { ...this.resolved.config.llm, profile, extraction: undefined }
    this.persistLlmConfig(`set_llm_profile:${profile}`)
  }

  /**
   * Choix EXPLICITE du provider/modèle d'extraction (« l'utilisateur décide »).
   * provider ∈ ollama|lmstudio|anthropic|openai|openrouter. baseUrl : serveurs
   * locaux OpenAI-compatibles (LM Studio) hors port par défaut.
   */
  setExtractionProvider(provider: string, model?: string, baseUrl?: string): void {
    this.assertOpen()
    this.resolved.config.llm = {
      ...this.resolved.config.llm,
      profile: 'custom',
      extraction: { provider, ...(model ? { model } : {}), ...(baseUrl ? { base_url: baseUrl } : {}) },
    }
    this.persistLlmConfig(`set_extraction:${provider}${model ? `:${model}` : ''}`)
  }

  private persistLlmConfig(action: string): void {
    saveConfigFile(this.resolved.config, this.resolved.configPath)
    // invalide la résolution mémoïsée → re-résolue au prochain usage
    this.profilePromise = null
    this.pipelinePromise = null
    this.registry.audit({ actor_type: 'user', actor_id: 'local', action, target_id_hash: null, scope_id: null, reason: null })
  }

  // ------------------------------------------------------------ options (bucket C/D)

  /**
   * Options activables (couches opt-in / sur validation). OFF par défaut : ces
   * couches ne tournent QUE sur demande. ON = elles tournent automatiquement
   * (au boot du daemon + après les captures). L'utilisateur garde le contrôle.
   */
  getOptions(): Record<string, boolean> {
    this.assertOpen()
    const keys = ['auto_themes_ai', 'auto_self_observation', 'auto_revision', 'auto_patterns', 'markdown_export']
    const out: Record<string, boolean> = {}
    for (const k of keys) out[k] = this.registry.getSetting(`option.${k}`) === 'on'
    return out
  }

  /** Active/désactive une option. L'activer la fait tourner UNE FOIS tout de suite. */
  async setOption(key: string, enabled: boolean): Promise<void> {
    this.assertOpen()
    this.registry.setSetting(`option.${key}`, enabled ? 'on' : 'off')
    this.registry.audit({ actor_type: 'user', actor_id: 'local', action: `option_${enabled ? 'on' : 'off'}:${key}`, target_id_hash: null, scope_id: null, reason: null })
    if (enabled) await this.runOption(key)
  }

  /** Exécute une option sur toutes les instances actives (boot daemon + activation). */
  async runOption(key: string): Promise<void> {
    this.assertOpen()
    for (const inst of this.registry.listInstances()) {
      if (inst.revoked_at) continue
      const db = this.registry.dbForInstance(inst.id)
      if (!db || !existsSync(db.path)) continue
      try {
        switch (key) {
          case 'auto_themes_ai':
            await this.refineTopicLabels(inst.id)
            break
          case 'auto_self_observation':
            this.deriveSelfObservations(inst.id)
            break
          case 'auto_revision':
            await this.proposeRevisions(inst.id)
            break
          case 'auto_patterns':
            this.detectPatterns(inst.id)
            break
          case 'markdown_export':
            this.exportMarkdown(inst.id, join(this.paths.root, 'exports', inst.id), true)
            break
        }
      } catch (err) {
        console.warn(`[memoria] option ${key} sur ${inst.id} en échec :`, (err as Error).message)
      }
    }
  }

  /** Lance toutes les options ACTIVÉES (appelé au boot du daemon). */
  async runEnabledOptions(): Promise<{ ran: string[] }> {
    this.assertOpen()
    const ran: string[] = []
    for (const [key, on] of Object.entries(this.getOptions())) {
      if (on) {
        await this.runOption(key)
        ran.push(key)
      }
    }
    return { ran }
  }

  /** Mode de capture global : auto-private (défaut) | review-first | incognito (pause). */
  getCaptureMode(): CaptureMode {
    this.assertOpen()
    const raw = this.registry.getSetting('capture_mode')
    return raw === 'review-first' || raw === 'incognito' ? raw : 'auto-private'
  }

  setCaptureMode(mode: CaptureMode): void {
    this.assertOpen()
    this.registry.setSetting('capture_mode', mode)
    this.registry.audit({
      actor_type: 'user',
      actor_id: 'local',
      action: `set_capture_mode:${mode}`,
      target_id_hash: null,
      scope_id: null,
      reason: null,
    })
  }

  listAgents(): Array<{ instance: AssistantInstance; assistant_type: string; db_path: string | null }> {
    this.assertOpen()
    return this.registry.listInstances().map(instance => {
      const assistant = this.registry.getAssistant(instance.assistant_id)
      const db = this.registry.dbForInstance(instance.id)
      return { instance, assistant_type: assistant?.type ?? 'generic', db_path: db?.path ?? null }
    })
  }

  /** Synthèse par agent : ce que chacun sait (souvenirs, thèmes, procédures, maîtrise). */
  agentOverview(): Array<{
    instance: string
    type: string
    facts: number
    themes: number
    procedures: number
    expertise: string[]
  }> {
    this.assertOpen()
    const out: ReturnType<Memoria['agentOverview']> = []
    for (const inst of this.registry.listInstances()) {
      if (inst.revoked_at) continue
      const assistant = this.registry.getAssistant(inst.assistant_id)
      if (assistant?.type === 'generic') continue
      const db = this.registry.dbForInstance(inst.id)
      if (!db || !existsSync(db.path)) continue
      const store = this.openContent(db.path)
      out.push({
        instance: inst.id,
        type: assistant?.type ?? 'generic',
        facts: store.countFacts(),
        themes: this.topicFor(store, null).listTopics({ minFacts: 2 }).length,
        procedures: this.proceduralFor(store).listProcedures().length,
        expertise: this.feedbackFor(store).topDomains(4).map(d => d.domain),
      })
    }
    return out
  }

  /**
   * Stats vivantes des couches cognitives (écran « Système ») : compte réel par
   * table, agrégé sur toutes les DB de contenu. Sert à RENDRE VISIBLES les 24
   * couches et prouver qu'elles tournent.
   */
  cognitiveStats(): Record<string, number> {
    this.assertOpen()
    const tables = [
      'facts', 'entities', 'relations', 'fact_entities', 'observations', 'topics', 'fact_topics',
      'embeddings', 'procedures', 'patterns', 'fact_clusters', 'self_observations',
      'revision_proposals', 'wal_buffer',
    ]
    const totals: Record<string, number> = {}
    for (const t of tables) totals[t] = 0
    for (const entry of this.registry.listDbs()) {
      if (entry.kind === 'registry' || !existsSync(entry.path)) continue
      const store = this.openContent(entry.path)
      for (const t of tables) {
        try {
          const r = store.db.prepare(`SELECT COUNT(*) AS c FROM ${t}`).get() as { c: number }
          totals[t]! += r.c
        } catch {
          /* table absente sur cette DB — ignore */
        }
      }
    }
    totals['secret_refs'] = this.registry.listSecretRefs().length
    return totals
  }

  /** Coffre : références de secrets stockées (JAMAIS la valeur). */
  listSecrets(): Array<{ name: string; service: string | null; location: string; created_at: string }> {
    this.assertOpen()
    return this.registry.listSecretRefs()
  }

  /**
   * Mémoires PARTAGÉES (user/org/client/projet) + leur contenu explorable :
   * c'est là que vivent « les infos sur moi », « l'entreprise », « ce qui est
   * partagé ». Privé exclu (cf. écran Mémoire par agent).
   */
  listSharedScopes(): Array<{ id: string; type: string; name: string; label: string; facts: number }> {
    this.assertOpen()
    const LABELS: Record<string, string> = {
      user: 'Sur vous',
      org: 'Entreprise',
      client: 'Client',
      project: 'Projet',
      shared_topic: 'Sujet partagé',
    }
    const out: ReturnType<Memoria['listSharedScopes']> = []
    for (const scope of this.registry.listScopes()) {
      if (scope.type === 'private' || scope.type === 'legacy_to_review') continue
      const dbEntry = this.registry.dbForScope(scope.id)
      let facts = 0
      if (dbEntry && existsSync(dbEntry.path)) {
        facts = (this.openContent(dbEntry.path).db.prepare('SELECT COUNT(*) AS c FROM facts WHERE scope_id = ?').get(scope.id) as { c: number }).c
      }
      out.push({ id: scope.id, type: scope.type, name: scope.name, label: LABELS[scope.type] ?? scope.name, facts })
    }
    return out
  }

  /** Souvenirs d'un scope partagé (contenu de « Sur vous », « Entreprise », un client…). */
  scopeFacts(scopeId: string, limit = 100): Array<{ id: string; fact: string; category: string; created_at: string }> {
    this.assertOpen()
    const scope = this.registry.getScope(scopeId)
    if (!scope) return []
    const dbEntry = this.registry.dbForScope(scope.id)
    if (!dbEntry || !existsSync(dbEntry.path)) return []
    const rows = this.openContent(dbEntry.path).db
      .prepare('SELECT id, fact, category, created_at FROM facts WHERE scope_id = ? ORDER BY created_at DESC LIMIT ?')
      .all(scope.id, Math.min(limit, 300)) as Array<{ id: string; fact: string; category: string; created_at: string }>
    return rows
  }

  /**
   * Affine les libellés de thèmes d'une instance avec le LLM configuré (à la
   * demande, couche 14). Gratuit par défaut (heuristique) ; ce bouton paie un
   * petit appel par thème pour des noms propres. Retourne le nombre renommé.
   */
  async refineTopicLabels(instanceId: string, limit = 40): Promise<{ refined: number }> {
    this.assertOpen()
    const { extraction } = await this.ensureProfile()
    if (!extraction || !(await extraction.isAvailable())) return { refined: 0 }
    const db = this.registry.dbForInstance(instanceId)
    if (!db || !existsSync(db.path)) return { refined: 0 }
    const store = this.openContent(db.path)
    const topicEngine = this.topicFor(store, null)
    const topics = topicEngine.listTopics({ minFacts: 2 }).slice(0, limit)
    let refined = 0
    for (const t of topics) {
      const sample = topicEngine.factsForTopic(t.id, { limit: 5 }).map(f => f.fact)
      if (sample.length === 0) continue
      try {
        const raw = await extraction.complete({
          system: 'Donne un titre de THÈME court et clair (2-5 mots, en français, Title Case) qui résume ces souvenirs. Réponds UNIQUEMENT le titre, rien d’autre.',
          prompt: sample.map(s => `- ${s}`).join('\n'),
          maxTokens: 20,
          temperature: 0.2,
        })
        const label = raw.trim().replace(/^["'#*\s]+|["'.*\s]+$/g, '').slice(0, 60)
        if (label.length >= 3 && label.toLowerCase() !== t.name.toLowerCase()) {
          store.db.prepare('UPDATE topics SET name = ?, updated_at = ? WHERE id = ?').run(label, nowISO(), t.id)
          refined++
        }
      } catch (err) {
        console.warn(`[memoria:topics] affinage LLM échoué (${t.id}) :`, (err as Error).message)
      }
    }
    return { refined }
  }

  stats(): { facts: number; databases: number; instances: number } {
    this.assertOpen()
    let facts = 0
    let databases = 0
    for (const entry of this.registry.listDbs()) {
      if (entry.kind === 'registry') continue
      databases++
      if (existsSync(entry.path)) facts += this.openContent(entry.path).countFacts()
    }
    return { facts, databases, instances: this.registry.listInstances().length }
  }

  doctor(): DoctorReport {
    this.assertOpen()
    const warnings: string[] = []
    const databases: DoctorReport['databases'] = []
    let onNetwork = false
    let journalMode = 'wal'
    for (const entry of this.registry.listDbs()) {
      const exists = existsSync(entry.path)
      let size = 0
      let walPending: number | undefined
      if (exists) {
        size = statSync(entry.path).size
        if (entry.kind !== 'registry') {
          const store = this.openContent(entry.path)
          walPending = store.walPendingCount()
          onNetwork ||= store.onNetworkVolume
          journalMode = store.journalMode
          if (store.onNetworkVolume) {
            warnings.push(`DB sur volume réseau/synchronisé : ${entry.path} (journal_mode=${store.journalMode})`)
          }
        }
      } else if (entry.kind !== 'registry') {
        warnings.push(`DB enregistrée mais absente du disque : ${entry.path}`)
      }
      databases.push({ kind: entry.kind, path: entry.path, exists, size_bytes: size, wal_pending: walPending })
    }
    return {
      ok: warnings.length === 0,
      storage_root: this.paths.root,
      config_path: this.resolved.configPath,
      registry_path: this.paths.registry,
      databases,
      network_guard: { on_network_volume: onNetwork, journal_mode: journalMode },
      warnings,
    }
  }

  close(): void {
    if (this.closed) return
    this.closed = true
    for (const store of this.pool.values()) store.close()
    this.pool.clear()
    this.registry.close()
  }

  // ------------------------------------------------------------------ interne

  private assertOpen(): void {
    if (this.closed) throw new Error('Memoria est fermé (close() déjà appelé)')
  }

  /** Redaction des secrets avant tout stockage de fait → valeur au coffre, jamais en clair. */
  private redactBeforeStore(text: string): string {
    const result = this.redactor.redact(text)
    for (const secret of result.found) {
      try {
        this.secretProvider.set(secret.name, secret.value)
        this.registry.upsertSecretRef(secret.name, this.secretProvider.locationFor(secret.name), secret.kind)
      } catch (err) {
        console.warn(`[memoria] mise au coffre du secret « ${secret.name} » en échec :`, (err as Error).message)
      }
    }
    return result.text
  }

  private mustInstance(instanceId: string): AssistantInstance {
    const instance = this.registry.getInstance(instanceId)
    if (!instance) throw new Error(`instance inconnue : ${instanceId}`)
    if (instance.revoked_at) throw new Error(`instance révoquée : ${instanceId}`)
    return instance
  }

  private openContent(path: string): ContentStore {
    let store = this.pool.get(path)
    if (!store) {
      store = new ContentStore(path)
      this.pool.set(path, store)
    }
    return store
  }

  /** Scope cible d'une écriture : id, nom, ou défaut = privé de l'instance. */
  private resolveTargetScope(instance: AssistantInstance, scopeRef?: string): MemoryScope {
    if (!scopeRef) {
      const scope = this.registry.getScopeByName(`private:${instance.id}`)
      if (!scope) throw new Error(`scope privé introuvable pour l'instance ${instance.id}`)
      return scope
    }
    const scope = this.registry.getScope(scopeRef) ?? this.registry.getScopeByName(scopeRef)
    if (!scope) throw new Error(`scope inconnu : ${scopeRef}`)
    return scope
  }

  /** DB qui héberge un scope (privé → DB d'instance ; partagé → shared/…). */
  private storeForScope(scope: MemoryScope, instance: AssistantInstance): ContentStore {
    if (scope.type === 'private') {
      return this.openContent(this.paths.assistantDb(instance.id))
    }
    const dbPath = this.sharedDbPath(scope)
    const store = this.openContent(dbPath)
    this.registry.registerDb({ kind: 'shared', path: dbPath, assistant_instance_id: null, scope_id: scope.id })
    return store
  }

  private sharedDbPath(scope: MemoryScope): string {
    switch (scope.type) {
      case 'user':
        return this.paths.sharedDb('user')
      case 'org':
        return this.paths.sharedDb(`companies/${scope.org_id ?? scope.id}`)
      case 'client':
        return this.paths.sharedDb(`clients/${scope.client_org_id ?? scope.id}`)
      case 'project':
        return this.paths.sharedDb(`projects/${scope.project_id ?? scope.id}`)
      case 'shared_topic':
        return this.paths.sharedDb(`topics/${scope.id}`)
      case 'legacy_to_review':
        return this.paths.sharedDb('legacy_to_review')
      default:
        throw new Error(`type de scope sans DB partagée : ${scope.type}`)
    }
  }

  /**
   * Cibles de lecture du fan-out : la DB privée de CETTE instance + chaque DB
   * partagée dont le scope est lisible (policy can_read). Les scopes privés
   * des AUTRES instances sont exclus structurellement.
   */
  private resolveReadTargets(instance: AssistantInstance): Array<{ dbPath: string; scopeIds: string[]; scopeNames: string[] }> {
    const targets = new Map<string, { scopeIds: string[]; scopeNames: string[] }>()

    const push = (dbPath: string, scope: MemoryScope) => {
      const entry = targets.get(dbPath) ?? { scopeIds: [], scopeNames: [] }
      entry.scopeIds.push(scope.id)
      entry.scopeNames.push(scope.name)
      targets.set(dbPath, entry)
    }

    for (const scope of this.registry.readableScopes(instance.assistant_id)) {
      if (scope.type === 'private') {
        if (scope.name !== `private:${instance.id}`) continue
        push(this.paths.assistantDb(instance.id), scope)
      } else if (scope.type === 'legacy_to_review') {
        // La quarantaine n'entre JAMAIS dans le recall (revue via UI uniquement)
        continue
      } else {
        const dbPath = this.sharedDbPath(scope)
        if (existsSync(dbPath)) push(dbPath, scope)
      }
    }

    return [...targets.entries()].map(([dbPath, v]) => ({ dbPath, ...v }))
  }
}
