/**
 * Daemon local unique (spec §2.2) — UN processus détient les DB ;
 * MCP/CLI/UI sont des clients HTTP sur 127.0.0.1.
 *
 * Auth à trois niveaux :
 *  - aucun : /v1/health, /v1/pairing/complete (le code one-shot TTL EST le secret) ;
 *  - Bearer <admin_token> (daemon.json chmod 600) : /v1/admin/* — réservé à
 *    l'utilisateur local (CLI, UI web) ;
 *  - Bearer <instance_token> (issu du pairing) : /v1/memory/* — les agents.
 *
 * Écritures sérialisées de fait : better-sqlite3 est synchrone sur l'unique
 * thread Node → zéro contention inter-process par construction.
 */
import { createServer, type IncomingMessage, type Server, type ServerResponse } from 'node:http'
import { existsSync } from 'node:fs'
import { timingSafeEqual } from 'node:crypto'
import { fileURLToPath } from 'node:url'
import {
  Memoria,
  autoRegister,
  autostartStatus,
  collectTranscriptFiles,
  copyOpenClawKey,
  writeProviderKey,
  detectAgents,
  disableAutostart,
  enableAutostart,
  newToken,
  nowISO,
  saveCredentials,
  serveInvocation,
  type AssistantType,
  type CaptureMode,
  type CaptureTurnInput,
  type ForgetFilter,
  type MemoriaInitOptions,
  type RecallInput,
  type RegisterOptions,
  type RegisterResult,
  type ReusableProvider,
  type StoreFactInput,
} from '@memoria/core'
import { OllamaPullJob } from './ollama-pull.js'
import { ImportJobRunner } from './import-job.js'
import { daemonBinPath } from './client.js'
import { currentVersion, pullAndBuild, scheduleRestart } from './update.js'
import { findUiDist, serveUi } from './static.js'
import { acquireLock, clearDaemonState, writeDaemonState, type DaemonState } from './state.js'

export const DAEMON_VERSION = '0.1.0'

export interface DaemonOptions {
  storageRoot?: string
  configPath?: string
  /** Port d'écoute ; 0 = éphémère (persisté dans daemon.json). */
  port?: number
  /** Dossier dist de l'UI web (défaut : auto-détection @memoria/web/dist). */
  uiDist?: string
  /** URL du serveur Ollama (santé LLM + téléchargements) — injectable pour les tests. */
  ollamaBaseUrl?: string
  /** HOME inspecté par la détection d'agents et la collecte de transcripts (tests : tmpdir). */
  agentsHome?: string
  /** Sonde de présence d'un CLI (tests : jamais les vrais binaires). */
  checkCli?: (bin: string) => boolean
  /** Enregistrement MCP auprès de l'hôte (tests : stub — jamais le vrai ~/.claude.json). */
  registrar?: (host: string, instanceId: string, opts: RegisterOptions) => RegisterResult
  /** Dossier des credentials d'instance (tests : tmpdir, jamais ~/.memoria). */
  credentialsDir?: string
  /** Override LLM transmis au moteur (tests : extraction mockée, zéro réseau). */
  llm?: MemoriaInitOptions['llm']
}

export interface RunningDaemon {
  state: DaemonState
  memoria: Memoria
  close: () => Promise<void>
}

class HttpError extends Error {
  constructor(
    readonly status: number,
    message: string,
  ) {
    super(message)
  }
}

export async function startDaemon(opts: DaemonOptions = {}): Promise<RunningDaemon> {
  const memoria = Memoria.init({ storageRoot: opts.storageRoot, configPath: opts.configPath, llm: opts.llm })
  const storageRoot = memoria.paths.root
  const importJobs = new ImportJobRunner(memoria)

  const release = acquireLock(storageRoot)
  if (!release) {
    memoria.close()
    throw new Error(`un daemon Memoria tourne déjà pour ${storageRoot} (daemon.lock)`)
  }

  const adminToken = newToken()
  const daemonId = newToken().slice(0, 16)
  // Un seul téléchargement de modèle Ollama à la fois (progression en mémoire).
  const ollamaPull = new OllamaPullJob(opts.ollamaBaseUrl)

  const server = createServer((req, res) => {
    void handle(req, res).catch((err: unknown) => {
      const status = err instanceof HttpError ? err.status : 500
      sendJson(res, status, { error: (err as Error).message ?? 'erreur interne' })
    })
  })

  const uiDist = findUiDist(opts.uiDist)

  async function handle(req: IncomingMessage, res: ServerResponse): Promise<void> {
    const url = new URL(req.url ?? '/', 'http://127.0.0.1')
    const route = `${req.method} ${url.pathname}`

    // Anti-DNS-rebinding : un site web malveillant peut résoudre un domaine vers
    // 127.0.0.1 et taper notre daemon. On n'accepte que les hôtes loopback.
    if (!isLoopbackHost(req.headers.host) || !isAllowedOrigin(req.headers.origin)) {
      res.writeHead(403).end()
      return
    }

    if (route === 'GET /v1/health') {
      sendJson(res, 200, { ok: true, version: DAEMON_VERSION, daemon_id: daemonId, ui: Boolean(uiDist) })
      return
    }

    if (req.method === 'GET' && uiDist && serveUi(url.pathname, uiDist, res)) return

    if (route === 'POST /v1/pairing/complete') {
      const body = await readJson(req)
      const code = String(body['code'] ?? '')
      const done = memoria.completePairing(code)
      if (!done) throw new HttpError(401, 'code de pairing invalide ou expiré')
      sendJson(res, 200, done)
      return
    }

    const token = bearerToken(req)

    if (url.pathname.startsWith('/v1/admin/')) {
      if (!token || !timingSafeEqualStr(token, adminToken)) throw new HttpError(401, 'token admin requis')
      await handleAdmin(route, url, req, res)
      return
    }

    if (url.pathname.startsWith('/v1/memory/')) {
      if (!token) throw new HttpError(401, 'token d’instance requis')
      const instance = memoria.authenticate(token)
      if (!instance) throw new HttpError(401, 'token d’instance invalide ou révoqué')
      await handleMemory(route, req, res, instance.id)
      return
    }

    throw new HttpError(404, `route inconnue : ${route}`)
  }

  async function handleAdmin(route: string, url: URL, req: IncomingMessage, res: ServerResponse): Promise<void> {
    switch (route) {
      case 'GET /v1/admin/facts': {
        const facts = memoria.browseFacts({
          instance: url.searchParams.get('instance') ?? undefined,
          q: url.searchParams.get('q') ?? undefined,
          limit: url.searchParams.has('limit') ? Number(url.searchParams.get('limit')) : undefined,
        })
        sendJson(res, 200, { facts })
        return
      }
      case 'GET /v1/admin/search': {
        const q = url.searchParams.get('q') ?? ''
        const limit = url.searchParams.has('limit') ? Number(url.searchParams.get('limit')) : 80
        sendJson(res, 200, { facts: memoria.globalSearch(q, limit) })
        return
      }
      case 'GET /v1/admin/review': {
        sendJson(res, 200, { items: memoria.listReview() })
        return
      }
      case 'POST /v1/admin/adopt_legacy': {
        const body = await readJson(req)
        const instanceId = String(body['instance'] ?? '')
        if (!instanceId) throw new HttpError(400, 'instance requise')
        sendJson(res, 200, memoria.adoptLegacyInto(instanceId, { reindex: body['reindex'] !== false }))
        return
      }
      case 'GET /v1/admin/scopes': {
        sendJson(res, 200, { scopes: memoria.listScopesWithAccess(), assistants: memoria.registry.listAssistants() })
        return
      }
      case 'POST /v1/admin/share': {
        const body = await readJson(req)
        const factIds = (body['fact_ids'] as string[]) ?? []
        const targetScope = String(body['target_scope'] ?? '')
        if (!targetScope) throw new HttpError(400, 'target_scope requis')
        sendJson(res, 200, memoria.shareFacts(factIds, targetScope))
        return
      }
      case 'POST /v1/admin/policy': {
        const body = await readJson(req)
        const assistantId = String(body['assistant_id'] ?? '')
        const scopeId = String(body['scope_id'] ?? '')
        if (!assistantId || !scopeId) throw new HttpError(400, 'assistant_id et scope_id requis')
        memoria.setScopeAccess(assistantId, scopeId, body as Record<string, never>)
        sendJson(res, 200, { ok: true })
        return
      }
      case 'GET /v1/admin/identity_candidates': {
        const instance = url.searchParams.get('instance')
        if (!instance) throw new HttpError(400, 'instance requise')
        sendJson(res, 200, { candidates: memoria.suggestIdentityFacts(instance) })
        return
      }
      case 'GET /v1/admin/topics': {
        const instance = url.searchParams.get('instance')
        if (!instance) throw new HttpError(400, 'instance requise')
        const minFacts = url.searchParams.has('min_facts') ? Number(url.searchParams.get('min_facts')) : 1
        sendJson(res, 200, { topics: memoria.listTopics(instance, minFacts) })
        return
      }
      case 'GET /v1/admin/topic_facts': {
        const instance = url.searchParams.get('instance')
        const topic = url.searchParams.get('topic')
        if (!instance || !topic) throw new HttpError(400, 'instance et topic requis')
        sendJson(res, 200, { facts: memoria.topicFacts(instance, topic) })
        return
      }
      case 'GET /v1/admin/topic_relations': {
        const instance = url.searchParams.get('instance')
        if (!instance) throw new HttpError(400, 'instance requise')
        const minFacts = url.searchParams.has('min_facts') ? Number(url.searchParams.get('min_facts')) : 2
        sendJson(res, 200, memoria.topicRelations(instance, minFacts))
        return
      }
      case 'GET /v1/admin/patterns': {
        const instance = url.searchParams.get('instance')
        if (!instance) throw new HttpError(400, 'instance requise')
        // détection à la demande (puis liste des propositions)
        memoria.detectPatterns(instance)
        sendJson(res, 200, { patterns: memoria.listPatterns(instance) })
        return
      }
      case 'POST /v1/admin/pattern_decision': {
        const body = await readJson(req)
        const instance = String(body['instance'] ?? '')
        const id = String(body['id'] ?? '')
        const decision = body['decision'] === 'accept' ? 'accept' : 'dismiss'
        if (!instance || !id) throw new HttpError(400, 'instance et id requis')
        sendJson(res, 200, memoria.decidePattern(instance, id, decision))
        return
      }
      case 'GET /v1/admin/procedures': {
        const instance = url.searchParams.get('instance')
        if (!instance) throw new HttpError(400, 'instance requise')
        sendJson(res, 200, { procedures: memoria.listProcedures(instance) })
        return
      }
      case 'GET /v1/admin/expertise': {
        const instance = url.searchParams.get('instance')
        if (!instance) throw new HttpError(400, 'instance requise')
        sendJson(res, 200, { domains: memoria.topExpertise(instance) })
        return
      }
      case 'GET /v1/admin/clusters': {
        const instance = url.searchParams.get('instance')
        if (!instance) throw new HttpError(400, 'instance requise')
        sendJson(res, 200, { clusters: memoria.listClusters(instance) })
        return
      }
      case 'GET /v1/admin/self_observations': {
        const instance = url.searchParams.get('instance')
        if (!instance) throw new HttpError(400, 'instance requise')
        sendJson(res, 200, { observations: memoria.selfObservations(instance) })
        return
      }
      case 'POST /v1/admin/derive_self': {
        const body = await readJson(req)
        sendJson(res, 200, memoria.deriveSelfObservations(String(body['instance'] ?? '')))
        return
      }
      case 'POST /v1/admin/dialectic': {
        const body = await readJson(req)
        const instance = String(body['instance'] ?? '')
        const question = String(body['question'] ?? '')
        if (!instance || !question) throw new HttpError(400, 'instance et question requis')
        sendJson(res, 200, await memoria.dialectic(instance, question))
        return
      }
      case 'GET /v1/admin/revisions': {
        const instance = url.searchParams.get('instance')
        if (!instance) throw new HttpError(400, 'instance requise')
        sendJson(res, 200, { proposals: memoria.listRevisions(instance) })
        return
      }
      case 'POST /v1/admin/propose_revisions': {
        const body = await readJson(req)
        sendJson(res, 200, await memoria.proposeRevisions(String(body['instance'] ?? '')))
        return
      }
      case 'POST /v1/admin/revision_decision': {
        const body = await readJson(req)
        const instance = String(body['instance'] ?? '')
        const id = String(body['id'] ?? '')
        const decision = body['decision'] === 'accept' ? 'accept' : 'dismiss'
        if (!instance || !id) throw new HttpError(400, 'instance et id requis')
        sendJson(res, 200, memoria.decideRevision(instance, id, decision))
        return
      }
      case 'GET /v1/admin/skill_proposals': {
        const instance = url.searchParams.get('instance')
        if (!instance) throw new HttpError(400, 'instance requise')
        sendJson(res, 200, { skills: memoria.proposeSkills(instance) })
        return
      }
      case 'POST /v1/admin/review/approve': {
        const body = await readJson(req)
        sendJson(res, 200, memoria.reviewDecision((body['ids'] as string[]) ?? [], 'accepted'))
        return
      }
      case 'POST /v1/admin/review/reject': {
        const body = await readJson(req)
        sendJson(res, 200, memoria.reviewDecision((body['ids'] as string[]) ?? [], 'rejected'))
        return
      }
      case 'GET /v1/admin/providers': {
        sendJson(res, 200, await memoria.detectProviders())
        return
      }
      case 'GET /v1/admin/llm_profile': {
        sendJson(res, 200, memoria.getLlmProfile())
        return
      }
      case 'POST /v1/admin/llm_profile': {
        const body = await readJson(req)
        const profile = String(body['profile'] ?? '')
        if (!['100-local', 'local-plus-cloud', 'cloud'].includes(profile)) {
          throw new HttpError(400, `profil inconnu : ${profile}`)
        }
        memoria.setLlmProfile(profile)
        sendJson(res, 200, { profile })
        return
      }
      case 'POST /v1/admin/llm_extraction': {
        const body = await readJson(req)
        const provider = String(body['provider'] ?? '')
        if (!['ollama', 'lmstudio', 'anthropic', 'openai', 'openrouter'].includes(provider)) {
          throw new HttpError(400, `provider inconnu : ${provider}`)
        }
        memoria.setExtractionProvider(provider, body['model'] as string | undefined, body['base_url'] as string | undefined)
        sendJson(res, 200, { provider, model: body['model'] ?? null })
        return
      }
      case 'GET /v1/admin/llm_health': {
        // LA source de vérité anti-mort-silencieuse : moteurs effectifs +
        // raisons d'indisponibilité + WAL en attente + options détectées.
        sendJson(res, 200, await memoria.llmHealth({ ollamaBaseUrl: opts.ollamaBaseUrl }))
        return
      }
      case 'POST /v1/admin/ollama_pull': {
        const body = await readJson(req)
        const model = String(body['model'] ?? '').trim()
        if (!model) throw new HttpError(400, 'model requis')
        if (ollamaPull.status().running) {
          throw new HttpError(409, `un téléchargement est déjà en cours (${ollamaPull.status().model ?? '?'})`)
        }
        ollamaPull.start(model)
        sendJson(res, 200, { ok: true, model })
        return
      }
      case 'GET /v1/admin/ollama_pull_status': {
        sendJson(res, 200, ollamaPull.status())
        return
      }
      case 'POST /v1/admin/openclaw_copy_key': {
        // « Réutiliser ma config OpenClaw » : copie une clé API en clair vers
        // ~/.<provider>/api_key (chmod 600). La valeur n'apparaît JAMAIS ici.
        const body = await readJson(req)
        const provider = String(body['provider'] ?? '')
        if (!['openai', 'anthropic', 'openrouter'].includes(provider)) {
          throw new HttpError(400, `provider invalide : ${provider}`)
        }
        const copied = copyOpenClawKey(provider as ReusableProvider)
        memoria.registry.audit({
          actor_type: 'user',
          actor_id: 'local',
          action: `openclaw_copy_key:${provider}`,
          target_id_hash: null,
          scope_id: null,
          reason: `depuis ${copied.from}`,
        })
        sendJson(res, 200, { ok: true, provider, key_file: copied.keyFile })
        return
      }
      case 'POST /v1/admin/provider_key': {
        // L'utilisateur colle sa clé API → écrite dans ~/.<provider>/api_key
        // (chmod 600). La valeur n'est JAMAIS loggée ni renvoyée.
        const body = await readJson(req)
        const provider = String(body['provider'] ?? '')
        const key = String(body['key'] ?? '')
        if (!['openai', 'anthropic', 'openrouter'].includes(provider)) {
          throw new HttpError(400, `provider invalide : ${provider}`)
        }
        if (key.trim() === '') throw new HttpError(400, 'clé vide')
        const written = writeProviderKey(provider as ReusableProvider, key)
        memoria.registry.audit({
          actor_type: 'user',
          actor_id: 'local',
          action: `provider_key:${provider}`,
          target_id_hash: null,
          scope_id: null,
          reason: 'clé saisie par l’utilisateur',
        })
        sendJson(res, 200, { ok: true, provider, key_file: written.keyFile })
        return
      }
      case 'GET /v1/admin/options': {
        sendJson(res, 200, { options: memoria.getOptions() })
        return
      }
      case 'POST /v1/admin/options': {
        const body = await readJson(req)
        const key = String(body['key'] ?? '')
        const enabled = body['enabled'] === true
        if (!key) throw new HttpError(400, 'key requise')
        await memoria.setOption(key, enabled)
        sendJson(res, 200, { options: memoria.getOptions() })
        return
      }
      case 'GET /v1/admin/capture_mode': {
        sendJson(res, 200, { mode: memoria.getCaptureMode() })
        return
      }
      case 'POST /v1/admin/capture_mode': {
        const body = await readJson(req)
        const mode = String(body['mode'] ?? '') as CaptureMode
        if (!['auto-private', 'review-first', 'incognito'].includes(mode)) {
          throw new HttpError(400, `mode de capture inconnu : ${mode}`)
        }
        memoria.setCaptureMode(mode)
        sendJson(res, 200, { mode })
        return
      }
      case 'POST /v1/admin/pair': {
        const body = await readJson(req)
        const result = memoria.pairAssistant({
          type: (body['type'] as never) ?? 'generic',
          display_name: body['display_name'] as string | undefined,
          machine: body['machine'] as string | undefined,
          profile: (body['profile'] as string | undefined) ?? null,
        })
        // Tant que @memoria/mcp n'est pas publié sur npm, la commande npx ne
        // marche pas : on la remplace par le binaire LOCAL s'il existe.
        sendJson(res, 200, { ...result, command: localConnectCommand(result.pairing_code) ?? result.command })
        return
      }
      case 'POST /v1/admin/revoke': {
        const body = await readJson(req)
        memoria.revokeInstance(String(body['assistant_instance_id'] ?? ''))
        sendJson(res, 200, { ok: true })
        return
      }
      case 'GET /v1/admin/agents': {
        sendJson(res, 200, { agents: memoria.listAgents() })
        return
      }
      case 'GET /v1/admin/persons': {
        sendJson(res, 200, { persons: memoria.listPersons() })
        return
      }
      case 'POST /v1/admin/person': {
        const body = await readJson(req)
        const displayName = String(body['display_name'] ?? '').trim()
        if (!displayName) throw new HttpError(400, 'display_name requis')
        sendJson(res, 200, {
          person: memoria.createPerson({
            display_name: displayName,
            relation: (body['relation'] as string | null) ?? null,
            notes: (body['notes'] as string | null) ?? null,
            org_id: (body['org_id'] as string | null) ?? null,
          }),
        })
        return
      }
      case 'POST /v1/admin/person_update': {
        const body = await readJson(req)
        const id = String(body['id'] ?? '')
        if (!id) throw new HttpError(400, 'id requis')
        const person = memoria.updatePerson(id, body as Record<string, never>)
        if (!person) throw new HttpError(404, 'personne inconnue')
        sendJson(res, 200, { person })
        return
      }
      case 'POST /v1/admin/person_delete': {
        const body = await readJson(req)
        sendJson(res, 200, { deleted: memoria.deletePerson(String(body['id'] ?? '')) })
        return
      }
      case 'POST /v1/admin/person_identifier': {
        const body = await readJson(req)
        const personId = String(body['person_id'] ?? '')
        const kind = String(body['kind'] ?? '') as 'phone' | 'email' | 'telegram' | 'whatsapp' | 'handle' | 'other'
        const value = String(body['value'] ?? '')
        if (!personId || !kind || !value) throw new HttpError(400, 'person_id, kind et value requis')
        if (!['phone', 'email', 'telegram', 'whatsapp', 'handle', 'other'].includes(kind)) throw new HttpError(400, `kind inconnu : ${kind}`)
        sendJson(res, 200, { identifier: memoria.addPersonIdentifier(personId, kind, value, (body['label'] as string | null) ?? null) })
        return
      }
      case 'POST /v1/admin/person_identifier_delete': {
        const body = await readJson(req)
        sendJson(res, 200, { deleted: memoria.removePersonIdentifier(String(body['id'] ?? '')) })
        return
      }
      case 'POST /v1/admin/identify_interlocutor': {
        const body = await readJson(req)
        sendJson(res, 200, { match: memoria.identifyInterlocutor(body as Record<string, never>) })
        return
      }
      case 'GET /v1/admin/stats': {
        sendJson(res, 200, memoria.stats())
        return
      }
      case 'GET /v1/admin/overview': {
        sendJson(res, 200, { agents: memoria.agentOverview() })
        return
      }
      case 'GET /v1/admin/cognitive_stats': {
        sendJson(res, 200, { stats: memoria.cognitiveStats() })
        return
      }
      case 'GET /v1/admin/secrets': {
        sendJson(res, 200, { secrets: memoria.listSecrets() })
        return
      }
      case 'GET /v1/admin/shared_scopes': {
        sendJson(res, 200, { scopes: memoria.listSharedScopes() })
        return
      }
      case 'GET /v1/admin/scope_facts': {
        const scope = url.searchParams.get('scope')
        if (!scope) throw new HttpError(400, 'scope requis')
        sendJson(res, 200, { facts: memoria.scopeFacts(scope) })
        return
      }
      case 'POST /v1/admin/refine_topics': {
        const body = await readJson(req)
        const instance = String(body['instance'] ?? '')
        if (!instance) throw new HttpError(400, 'instance requise')
        sendJson(res, 200, await memoria.refineTopicLabels(instance))
        return
      }
      case 'GET /v1/admin/doctor': {
        sendJson(res, 200, memoria.doctor())
        return
      }
      case 'POST /v1/admin/forget': {
        const body = await readJson(req)
        sendJson(res, 200, memoria.forget(body as ForgetFilter))
        return
      }
      case 'GET /v1/admin/audit': {
        sendJson(res, 200, { entries: memoria.registry.auditTail(200) })
        return
      }
      case 'GET /v1/admin/control': {
        sendJson(res, 200, {
          enabled: memoria.isEnabled(),
          autostart: autostartStatus(),
          storage: memoria.storageInfo(),
        })
        return
      }
      case 'POST /v1/admin/enabled': {
        const body = await readJson(req)
        const enabled = memoria.setEnabled(body['enabled'] === true)
        sendJson(res, 200, { enabled })
        return
      }
      case 'POST /v1/admin/autostart': {
        const body = await readJson(req)
        if (body['enabled'] === true) {
          const args = [process.execPath, daemonBinPath(), '--storage-root', storageRoot]
          sendJson(res, 200, { autostart: enableAutostart({ programArguments: args, workingDirectory: storageRoot }) })
        } else {
          sendJson(res, 200, { autostart: disableAutostart() })
        }
        return
      }
      case 'POST /v1/admin/delete_agent': {
        const body = await readJson(req)
        const instanceId = String(body['assistant_instance_id'] ?? '')
        if (!instanceId) throw new HttpError(400, 'assistant_instance_id requis')
        sendJson(res, 200, memoria.deleteInstance(instanceId))
        return
      }
      // ------------------------------------- agents sur cette machine (B1/B2/B3)
      case 'GET /v1/admin/agents_detect': {
        sendJson(res, 200, {
          agents: detectAgents({
            home: opts.agentsHome,
            checkCli: opts.checkCli,
            agents: memoria.listAgents(),
          }),
        })
        return
      }
      case 'POST /v1/admin/agents_connect': {
        // Connexion 1 CLIC : pairing complet EN PROCESSUS (pairAssistant +
        // completePairing), credentials chmod 600, puis enregistrement MCP
        // automatique selon le type — l'équivalent serveur de mcp/connect.ts.
        const body = await readJson(req)
        const kind = String(body['kind'] ?? '')
        const allowedKinds = ['claude-code', 'codex', 'openclaw', 'cursor', 'generic']
        if (!allowedKinds.includes(kind)) {
          throw new HttpError(400, `type d'agent inconnu : « ${kind} » (attendu : ${allowedKinds.join(', ')})`)
        }
        const displayName = typeof body['name'] === 'string' && body['name'].trim().length > 0 ? body['name'].trim() : undefined
        const paired = memoria.pairAssistant({ type: kind as AssistantType, display_name: displayName })
        const done = memoria.completePairing(paired.pairing_code)
        if (!done) throw new HttpError(500, 'échange de pairing impossible — code interne rejeté (voir le journal du daemon)')

        const credentialsPath = saveCredentials(
          done.assistant_instance_id,
          {
            instance_token: done.instance_token,
            storage_root: storageRoot,
            created_at: nowISO(),
            assistant_type: kind,
          },
          opts.credentialsDir,
        )

        const registrar = opts.registrar ?? autoRegister
        let registration: RegisterResult
        try {
          registration = registrar(kind, done.assistant_instance_id, { token: done.instance_token, storageRoot })
        } catch (err) {
          // VISIBLE, jamais avalé : échec précis + repli manuel (commande serve).
          const inv = serveInvocation(done.assistant_instance_id)
          registration = {
            host: 'generic',
            registered: false,
            detail: `enregistrement automatique en échec : ${(err as Error).message}. Manuel : ${inv.command} ${inv.args.join(' ')}`,
          }
        }
        if (!registration.registered) {
          console.warn(`[memoria-daemon] agents_connect ${kind} : ${registration.detail}`)
        }
        sendJson(res, 200, {
          instance_id: done.assistant_instance_id,
          credentials_path: credentialsPath,
          registered: registration,
          restart_hint: registration.registered ? 'Redémarre ton agent pour activer Memoria.' : null,
        })
        return
      }
      case 'POST /v1/admin/import_start': {
        const body = await readJson(req)
        const instanceId = String(body['instance_id'] ?? '')
        const kind = String(body['kind'] ?? '')
        if (!instanceId) throw new HttpError(400, 'instance_id requis')
        if (kind !== 'transcripts' && kind !== 'legacy') {
          throw new HttpError(400, `kind inconnu : « ${kind} » (attendu : transcripts | legacy)`)
        }
        if (importJobs.running) {
          throw new HttpError(409, 'un import est déjà en cours — attends sa fin (GET /v1/admin/import_status)')
        }
        const agent = memoria.listAgents().find(a => a.instance.id === instanceId)
        if (!agent) throw new HttpError(404, `instance inconnue : ${instanceId}`)
        if (agent.instance.revoked_at !== null) {
          throw new HttpError(400, 'instance révoquée — reconnecte l’agent avant d’importer')
        }

        if (kind === 'legacy') {
          // Pas de LLM requis : l'import legacy copie des faits déjà extraits.
          const legacyPath = String(body['legacy_path'] ?? '')
          if (!legacyPath) {
            throw new HttpError(400, 'legacy_path requis pour un import legacy (chemin de la base memoria.db OpenClaw)')
          }
          if (!existsSync(legacyPath)) throw new HttpError(404, `base legacy introuvable : ${legacyPath}`)
          // GARDE-FOU : scope legacy_to_review UNIQUE — jamais 2 bases en même temps.
          const pending = memoria.legacyQuarantineCount()
          if (pending > 0) {
            throw new HttpError(
              409,
              `la quarantaine legacy contient déjà ${pending} souvenir(s) non adoptés — termine cette adoption d'abord (une seule base legacy à la fois)`,
            )
          }
          sendJson(res, 200, importJobs.startLegacy({ instanceId, legacyPath }))
          return
        }

        // kind === 'transcripts'
        if (agent.assistant_type === 'openclaw') {
          throw new HttpError(400, 'OpenClaw n’a pas de transcripts importables — utilise l’import de mémoire legacy (kind=legacy + legacy_path)')
        }
        if (agent.assistant_type !== 'claude-code' && agent.assistant_type !== 'codex') {
          throw new HttpError(400, `pas de transcripts connus pour le type « ${agent.assistant_type} » (supportés : claude-code, codex)`)
        }
        // L'extraction a besoin d'un LLM : pas de job qui tourne pour rien.
        if (!(await memoria.hasExtraction())) {
          throw new HttpError(422, 'Configure d’abord un moteur d’intelligence (Réglages) — l’import de conversations a besoin d’un LLM d’extraction.')
        }
        const files = collectTranscriptFiles(agent.assistant_type, opts.agentsHome)
        if (files.length === 0) {
          throw new HttpError(404, `aucune conversation trouvée pour ${agent.assistant_type} sur cette machine`)
        }
        const rawMax = body['max_windows_per_file']
        let maxWindowsPerFile: number | undefined
        if (rawMax !== undefined && rawMax !== null) {
          const n = Number(rawMax)
          if (!Number.isFinite(n) || n < 1) throw new HttpError(400, 'max_windows_per_file doit être un entier ≥ 1')
          maxWindowsPerFile = Math.floor(n)
        }
        sendJson(res, 200, importJobs.startTranscripts({ instanceId, files, maxWindowsPerFile }))
        return
      }
      case 'GET /v1/admin/import_status': {
        sendJson(res, 200, importJobs.current)
        return
      }
      // ----------------------------------------------------------- synchro inter-machines (admin)
      case 'GET /v1/admin/sync/status': {
        const cfg = memoria.resolved.config.sync ?? {}
        sendJson(res, 200, {
          enabled: cfg.enabled === true,
          role: memoria.sync.role,
          machine_id: memoria.sync.machineId,
          hub: cfg.hub ?? null,
          listen_lan: cfg.listen_lan ?? null,
          scopes: memoria.sync.syncScopes().map(s => ({ id: s.id, type: s.type, name: s.name })),
          peers: memoria.sync.peers(),
        })
        return
      }
      case 'POST /v1/admin/sync/init_hub': {
        const body = await readJson(req)
        const listenLan = String(body['listen_lan'] ?? '0.0.0.0:47600')
        memoria.configureSyncHub(listenLan, (body['scopes'] as string[] | undefined) ?? undefined)
        sendJson(res, 200, { role: 'hub', listen_lan: listenLan, machine_id: memoria.sync.machineId, restart_required: true })
        return
      }
      case 'POST /v1/admin/sync/invite': {
        const body = await readJson(req)
        sendJson(res, 200, memoria.sync.invite((body['display_name'] as string | undefined) ?? undefined))
        return
      }
      case 'POST /v1/admin/sync/join': {
        const body = await readJson(req)
        const hub = String(body['hub'] ?? '')
        const code = String(body['code'] ?? '')
        if (!hub || !code) throw new HttpError(400, 'hub et code requis')
        sendJson(res, 200, await memoria.sync.join({ hub, code }))
        return
      }
      case 'POST /v1/admin/sync/now': {
        const r = await memoria.sync.syncAll()
        sendJson(res, 200, r)
        return
      }
      case 'GET /v1/admin/sync/peers': {
        sendJson(res, 200, { peers: memoria.sync.peers() })
        return
      }
      case 'POST /v1/admin/sync/revoke': {
        const body = await readJson(req)
        sendJson(res, 200, { revoked: memoria.registry.revokePeer(String(body['machine_id'] ?? '')) })
        return
      }
      case 'POST /v1/admin/sync/leave': {
        memoria.sync.leave()
        sendJson(res, 200, { ok: true })
        return
      }
      // ----------------------------------------------------------- mise à jour
      case 'GET /v1/admin/version': {
        sendJson(res, 200, { ...(await currentVersion()), daemon: DAEMON_VERSION })
        return
      }
      case 'POST /v1/admin/update': {
        const result = await pullAndBuild()
        sendJson(res, 200, result)
        // si du neuf a été buildé, on planifie un redémarrage APRÈS l'envoi de la réponse
        if (result.ok && result.changed) scheduleRestart(storageRoot)
        return
      }
      default:
        throw new HttpError(404, `route admin inconnue : ${route}`)
    }
  }

  async function handleMemory(route: string, req: IncomingMessage, res: ServerResponse, instanceId: string): Promise<void> {
    // KILL-SWITCH (config.enabled = false) : Memoria est « en pause ». On reste
    // joignable (l'agent ne casse pas) mais on ne lit ni n'écrit AUCUNE mémoire.
    // Réponse no-op ANNONCÉE (disabled: true) — jamais un échec silencieux.
    if (!memoria.isEnabled()) {
      if (route === 'POST /v1/memory/recall') sendJson(res, 200, { items: [], disabled: true })
      else if (route === 'POST /v1/memory/store_fact') sendJson(res, 200, { fact: null, disabled: true })
      else if (route === 'POST /v1/memory/capture_turn') sendJson(res, 200, { captured: 0, facts: [], disabled: true })
      else throw new HttpError(404, `route mémoire inconnue : ${route}`)
      return
    }
    switch (route) {
      case 'POST /v1/memory/store_fact': {
        const body = await readJson(req)
        const fact = memoria.storeFact({ ...(body as Omit<StoreFactInput, 'instance'>), instance: instanceId })
        sendJson(res, 200, { fact })
        return
      }
      case 'POST /v1/memory/recall': {
        const body = await readJson(req)
        // Hybride FTS+vectoriel quand un provider d'embeddings est disponible —
        // sinon strictement équivalent au recall FTS.
        const result = await memoria.recallSemantic({ ...(body as Omit<RecallInput, 'instance'>), instance: instanceId })
        sendJson(res, 200, result)
        return
      }
      case 'POST /v1/memory/capture_turn': {
        const body = await readJson(req)
        const messages = body['messages']
        if (!Array.isArray(messages) || messages.length === 0) {
          throw new HttpError(400, 'messages requis (tableau {role, content})')
        }
        const result = await memoria.captureTurn({
          instance: instanceId,
          messages: messages as CaptureTurnInput['messages'],
          active_context: body['active_context'] as CaptureTurnInput['active_context'],
        })
        sendJson(res, 200, result)
        return
      }
      case 'POST /v1/memory/identify_interlocutor': {
        // L'agent demande « à qui je parle ? » via un identifiant (Telegram/mail/tel…).
        const body = await readJson(req)
        sendJson(res, 200, { match: memoria.identifyInterlocutor(body as Record<string, never>) })
        return
      }
      case 'POST /v1/memory/identify_or_create_interlocutor': {
        // Comme identify_interlocutor mais CRÉE la personne au 1er contact d'un
        // identifiant inconnu (auto-enregistrement WhatsApp/Telegram/…).
        const body = await readJson(req)
        sendJson(res, 200, { match: memoria.identifyOrCreateInterlocutor(body as Record<string, never>) })
        return
      }
      default:
        throw new HttpError(404, `route mémoire inconnue : ${route}`)
    }
  }

  /**
   * Routes de SYNCHRO sur le LAN (SYNC §3.10). Seules ces routes sortent du
   * loopback, derrière peer_token + HMAC (sauf /pairing/complete : code TTL).
   * /v1/admin/* et /v1/memory/* ne sont JAMAIS servis ici.
   */
  async function handleSync(req: IncomingMessage, res: ServerResponse): Promise<void> {
    const url = new URL(req.url ?? '/', 'http://lan')
    if (!url.pathname.startsWith('/v1/sync/')) {
      res.writeHead(403).end()
      return
    }
    const method = req.method ?? 'GET'
    const pathWithQuery = url.pathname + url.search
    const body = await readRawBody(req)

    // Pairing : pas de Bearer (le code one-shot TTL EST le secret).
    if (method === 'POST' && url.pathname === '/v1/sync/pairing/complete') {
      const parsed = body ? (JSON.parse(body) as Record<string, unknown>) : {}
      const host = (req.socket.remoteAddress ?? '').replace(/^::ffff:/, '')
      sendJson(res, 200, memoria.sync.completePairing({
        code: String(parsed['code'] ?? ''),
        machine_id: String(parsed['machine_id'] ?? ''),
        display_name: parsed['display_name'] as string | undefined,
        host: host || undefined,
      }))
      return
    }

    // Toutes les autres routes : authenticité HMAC + token de pair.
    try {
      memoria.sync.authenticate(
        bearerToken(req) ?? undefined,
        headerStr(req, 'x-memoria-sig'),
        { method, path: pathWithQuery, body, ts: headerStr(req, 'x-memoria-ts') ?? '', nonce: headerStr(req, 'x-memoria-nonce') ?? '' },
      )
    } catch (err) {
      sendJson(res, 401, { error: (err as Error).message })
      return
    }

    if (method === 'GET' && url.pathname === '/v1/sync/snapshot') {
      sendJson(res, 200, memoria.sync.snapshot(url.searchParams.get('scope') ?? '', url.searchParams.get('since') ?? undefined))
      return
    }
    if (method === 'GET' && url.pathname === '/v1/sync/pull') {
      sendJson(res, 200, memoria.sync.collectDelta(url.searchParams.get('scope') ?? '', url.searchParams.get('since') ?? '1970-01-01T00:00:00.000Z'))
      return
    }
    if (method === 'POST' && url.pathname === '/v1/sync/push') {
      const b = JSON.parse(body) as { scope_id: string; facts: never[]; tombstones: never[] }
      sendJson(res, 200, memoria.sync.applyIncoming(b.scope_id, b.facts ?? [], b.tombstones ?? []))
      return
    }
    if (method === 'GET' && url.pathname === '/v1/sync/secrets') {
      const secrets = memoria.sync.serveSecrets(url.searchParams.get('scope') ?? '').map(s => ({ name: s.name, env: s.env }))
      sendJson(res, 200, { secrets })
      return
    }
    throw new HttpError(404, `route sync inconnue : ${method} ${url.pathname}`)
  }

  let port: number
  try {
    port = await new Promise<number>((resolvePort, reject) => {
      server.once('error', reject)
      server.listen(opts.port ?? 0, '127.0.0.1', () => {
        const addr = server.address()
        if (addr && typeof addr === 'object') resolvePort(addr.port)
        else reject(new Error('adresse d’écoute illisible'))
      })
    })
  } catch (err) {
    release()
    memoria.close()
    throw err
  }

  const state: DaemonState = {
    daemon_id: daemonId,
    port,
    admin_token: adminToken,
    pid: process.pid,
    started_at: nowISO(),
  }
  writeDaemonState(storageRoot, state)

  // ---- SYNCHRO INTER-MACHINES (SYNC §3.10) -------------------------------
  // (a) HUB : second listener sur le LAN, routes /v1/sync/* uniquement.
  const syncCfg = memoria.resolved.config.sync
  let lanServer: Server | null = null
  let syncTimer: ReturnType<typeof setInterval> | null = null
  if (syncCfg?.enabled && syncCfg.role === 'hub' && syncCfg.listen_lan) {
    const [lanHost, lanPortStr] = parseHostPort(syncCfg.listen_lan)
    lanServer = createServer((req, res) => {
      void handleSync(req, res).catch((err: unknown) => {
        const status = err instanceof HttpError ? err.status : 500
        sendJson(res, status, { error: (err as Error).message ?? 'erreur interne' })
      })
    })
    lanServer.on('error', e => console.warn('[memoria-daemon] listener LAN sync en échec :', (e as Error).message))
    lanServer.listen(lanPortStr, lanHost, () => console.log(`[memoria-daemon] synchro HUB à l'écoute sur ${lanHost}:${lanPortStr} (/v1/sync/*)`))
  }
  // (b) SPOKE : passe de synchro best-effort, au boot puis périodiquement.
  if (syncCfg?.enabled && syncCfg.role === 'spoke') {
    const intervalMs = Math.max(30, syncCfg.interval_sec ?? 120) * 1000
    const runTick = (): void => {
      void memoria.sync.tick().then(r => {
        if (r && (r.pulled > 0 || r.pushed > 0)) console.log(`[memoria-daemon] synchro : ${r.pulled} reçus, ${r.pushed} poussés`)
      }).catch(() => {})
    }
    syncTimer = setInterval(runTick, intervalMs)
    setTimeout(runTick, 2000) // 1re passe peu après le boot (laisse replayWal démarrer)
  }

  // Rejeu du WAL au boot (spec §6.2) : best-effort, jamais bloquant pour le
  // démarrage — sans LLM dispo les entrées restent pending (visibles au doctor).
  void memoria
    .replayWal()
    .then(replayed => {
      const totals = replayed.reduce(
        (acc, r) => ({ processed: acc.processed + r.summary.processed, facts: acc.facts + r.summary.facts_created }),
        { processed: 0, facts: 0 },
      )
      if (totals.processed > 0) {
        console.log(`[memoria-daemon] WAL rejoué : ${totals.processed} entrées → ${totals.facts} faits`)
      }
      // rattrapage d'indexation vectorielle (faits jamais embedés)
      return memoria.indexEmbeddings()
    })
    .then(r => {
      if (r.indexed > 0) console.log(`[memoria-daemon] embeddings indexés : ${r.indexed}`)
      // options activées (couches opt-in qui tournent en auto)
      return memoria.runEnabledOptions()
    })
    .then(o => {
      if (o.ran.length > 0) console.log(`[memoria-daemon] options auto exécutées : ${o.ran.join(', ')}`)
    })
    .catch((err: unknown) => console.warn('[memoria-daemon] rejeu/indexation au boot en échec :', (err as Error).message))

  const close = async (): Promise<void> => {
    if (syncTimer) clearInterval(syncTimer)
    if (lanServer) await new Promise<void>(r => lanServer!.close(() => r()))
    await new Promise<void>((resolveClose) => server.close(() => resolveClose()))
    clearDaemonState(storageRoot)
    release()
    memoria.close()
  }

  return { state, memoria, close }
}

// ----------------------------------------------------------------- helpers

/** Valeur d'en-tête HTTP en string (jamais un tableau). */
function headerStr(req: IncomingMessage, name: string): string | undefined {
  const v = req.headers[name]
  return Array.isArray(v) ? v[0] : v
}

/** « host:port » → [host, port]. host vide → 0.0.0.0. */
function parseHostPort(addr: string): [string, number] {
  const i = addr.lastIndexOf(':')
  if (i < 0) return ['0.0.0.0', Number.parseInt(addr, 10) || 47600]
  const host = addr.slice(0, i) || '0.0.0.0'
  const port = Number.parseInt(addr.slice(i + 1), 10) || 47600
  return [host, port]
}

/**
 * Commande de connexion LOCALE : `node <repo>/packages/mcp/dist/bin.js connect
 * --code XXXX`. Le bin MCP est voisin du daemon dans le monorepo. Retourne null
 * si introuvable (paquet publié npm → on garde la forme npx).
 */
function localConnectCommand(code: string): string | null {
  try {
    const binPath = fileURLToPath(new URL('../../mcp/dist/bin.js', import.meta.url))
    if (existsSync(binPath)) return `${process.execPath} ${binPath} connect --code ${code}`
  } catch {
    /* ignore */
  }
  return null
}

/** Hôte loopback uniquement (anti-DNS-rebinding). Absent = client non-HTTP/1.0 toléré. */
function isLoopbackHost(host: string | undefined): boolean {
  if (!host) return true
  const name = host.replace(/:\d+$/, '').toLowerCase()
  return name === '127.0.0.1' || name === 'localhost' || name === '[::1]' || name === '::1'
}

/** Origin (si présent) doit être loopback — un site web tiers ne doit pas nous appeler. */
function isAllowedOrigin(origin: string | undefined): boolean {
  if (!origin) return true // appels non-navigateur (CLI/MCP/agents) n'envoient pas d'Origin
  try {
    const h = new URL(origin).hostname.toLowerCase()
    return h === '127.0.0.1' || h === 'localhost' || h === '::1'
  } catch {
    return false
  }
}

/** Comparaison de tokens à temps constant (anti-timing-attack). */
function timingSafeEqualStr(a: string, b: string): boolean {
  const ab = Buffer.from(a)
  const bb = Buffer.from(b)
  if (ab.length !== bb.length) return false
  return timingSafeEqual(ab, bb)
}

function bearerToken(req: IncomingMessage): string | null {
  const header = req.headers.authorization
  if (!header?.startsWith('Bearer ')) return null
  return header.slice('Bearer '.length).trim()
}

async function readJson(req: IncomingMessage): Promise<Record<string, unknown>> {
  const raw = await readRawBody(req)
  if (raw.length === 0) return {}
  try {
    return JSON.parse(raw) as Record<string, unknown>
  } catch {
    throw new HttpError(400, 'JSON invalide')
  }
}

/** Corps BRUT (string) — nécessaire au HMAC de synchro (sha256 du corps exact). */
async function readRawBody(req: IncomingMessage): Promise<string> {
  const chunks: Buffer[] = []
  let size = 0
  for await (const chunk of req) {
    size += (chunk as Buffer).length
    if (size > 8_000_000) throw new HttpError(413, 'corps de requête trop grand')
    chunks.push(chunk as Buffer)
  }
  return chunks.length === 0 ? '' : Buffer.concat(chunks).toString('utf8')
}

function sendJson(res: ServerResponse, status: number, payload: unknown): void {
  const body = JSON.stringify(payload)
  res.writeHead(status, { 'content-type': 'application/json', 'content-length': Buffer.byteLength(body) })
  res.end(body)
}

export type { Server }
