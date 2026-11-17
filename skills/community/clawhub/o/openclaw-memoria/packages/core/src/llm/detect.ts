/**
 * Inventaire des moteurs d'intelligence DISPONIBLES sur la machine (onboarding
 * + santé LLM — chantier anti-mort-silencieuse). Tout est injectable pour les
 * tests : URLs, fichiers de clés, dossier OpenClaw, vérificateur de binaire.
 *
 * ⚠ Aucune valeur de clé API ne sort de detectLlmOptions() — uniquement
 * « présente ou non » et sa source (fichier|env). La copie effective d'une clé
 * OpenClaw passe par copyOpenClawKey(), qui écrit le fichier ~/.<p>/api_key
 * (chmod 600) sans jamais logger la valeur.
 *
 * Format OpenClaw investigué (version 2026.6.5 installée sur cette machine) :
 *  - `~/.openclaw/openclaw.json` ne contient JAMAIS de credentials (métadonnées
 *    de routing seulement — doc officielle « auth-credential-semantics »).
 *  - Clés/API : store par agent. Legacy JSON en clair :
 *    `agents/<id>/agent/auth-profiles.json` de forme canonique
 *    { version, profiles: { "openai:default": { type:"api_key", provider, key } } }
 *    (+ forme plate historique { "<provider>": { "apiKey": "..." } }).
 *  - Moderne : SQLite `agents/<id>/agent/openclaw-agent.sqlite` et
 *    `state/openclaw.sqlite`, table auth_profile_stores(store_key, store_json) —
 *    store_json reprend la même forme canonique { profiles: {...} }.
 *  - `type:"oauth"` = compte OAuth (access/refresh) : NON réutilisable pour des
 *    appels API directs → reusable:false, on le dit honnêtement.
 */
import { execFileSync } from 'node:child_process'
import { chmodSync, existsSync, mkdirSync, readFileSync, readdirSync, writeFileSync } from 'node:fs'
import { homedir } from 'node:os'
import { dirname, join } from 'node:path'
import DatabaseCtor from 'better-sqlite3'
import {
  DEFAULT_LOCAL_EXTRACTION_MODEL,
  DEFAULT_OLLAMA_BASE_URL,
  DEFAULT_OLLAMA_EMBEDDING_MODEL,
  modelMatches,
} from './ollama.js'
import { DEFAULT_LMSTUDIO_BASE_URL, lmstudioListModels } from './lmstudio.js'

// ------------------------------------------------------------------- types

export type ReusableProvider = 'openai' | 'anthropic' | 'openrouter'

export interface OllamaOption {
  kind: 'ollama'
  /** Prêt pour Memoria : serveur up + les DEUX modèles requis présents. */
  available: boolean
  serverUp: boolean
  hasEmbedModel: boolean
  hasExtractModel: boolean
  binaryInPath: boolean
  models: string[]
  baseUrl: string
  detail: string
}

export interface LmStudioOption {
  kind: 'lmstudio'
  /** Le serveur local répond (un modèle chargé n'est pas garanti — voir models). */
  available: boolean
  models: string[]
  baseUrl: string
  detail: string
}

export interface ApiKeyOption {
  kind: ReusableProvider
  /** Clé présente (fichier non vide OU variable d'env) — la VALEUR ne sort jamais. */
  available: boolean
  source: 'fichier' | 'env' | null
  keyFile: string
  detail: string
}

export interface OpenClawOption {
  kind: 'openclaw'
  /** OpenClaw détecté (binaire dans le PATH ou ~/.openclaw existant). */
  available: boolean
  /** Une clé API en CLAIR réutilisable a été trouvée dans ses stores. */
  reusable: boolean
  provider?: ReusableProvider
  configPath?: string
  reason?: string
  detail: string
}

export interface LlmOptions {
  ollama: OllamaOption
  lmstudio: LmStudioOption
  openai: ApiKeyOption
  anthropic: ApiKeyOption
  openrouter: ApiKeyOption
  openclaw: OpenClawOption
}

export interface DetectLlmOptionsInput {
  ollamaBaseUrl?: string
  lmstudioBaseUrl?: string
  /** Environnement injectable (tests). */
  env?: NodeJS.ProcessEnv
  /** Overrides des fichiers de clés par provider (tests). */
  keyFiles?: Partial<Record<ReusableProvider, string>>
  /** Dossier ~/.openclaw injectable (tests). */
  openclawDir?: string
  /** Vérificateur « binaire présent dans le PATH » injectable (tests). */
  hasCommand?: (cmd: string) => boolean
  timeoutMs?: number
}

// ------------------------------------------------------------------ helpers

/** `cmd --version` en silence : présent → true. */
export function defaultHasCommand(cmd: string): boolean {
  try {
    execFileSync(cmd, ['--version'], { stdio: 'ignore' })
    return true
  } catch {
    return false
  }
}

const KEY_ENV_VARS: Record<ReusableProvider, string> = {
  openai: 'OPENAI_API_KEY',
  anthropic: 'ANTHROPIC_API_KEY',
  openrouter: 'OPENROUTER_API_KEY',
}

function defaultKeyFile(provider: ReusableProvider): string {
  return join(homedir(), `.${provider}`, 'api_key')
}

/** Présence d'une clé SANS jamais retourner sa valeur. */
function keyPresence(provider: ReusableProvider, env: NodeJS.ProcessEnv, keyFile: string): ApiKeyOption {
  const fromEnv = env[KEY_ENV_VARS[provider]]
  if (fromEnv && fromEnv.trim() !== '') {
    return { kind: provider, available: true, source: 'env', keyFile, detail: `clé présente (variable ${KEY_ENV_VARS[provider]})` }
  }
  try {
    if (existsSync(keyFile) && readFileSync(keyFile, 'utf8').trim() !== '') {
      return { kind: provider, available: true, source: 'fichier', keyFile, detail: `clé présente (${keyFile})` }
    }
  } catch (err) {
    return { kind: provider, available: false, source: null, keyFile, detail: `fichier de clé illisible (${keyFile}) : ${(err as Error).message}` }
  }
  return { kind: provider, available: false, source: null, keyFile, detail: `aucune clé (ni ${KEY_ENV_VARS[provider]}, ni ${keyFile})` }
}

// ------------------------------------------------------ scan OpenClaw

const REUSABLE_PROVIDERS: ReadonlySet<string> = new Set(['openai', 'anthropic', 'openrouter'])

export interface OpenClawKeyCandidate {
  provider: ReusableProvider
  /** Fichier (JSON ou SQLite) où la clé a été trouvée. */
  configPath: string
  /** Valeur en clair — consommée par copyOpenClawKey, JAMAIS loggée/exposée. */
  key: string
}

export interface OpenClawScan {
  candidates: OpenClawKeyCandidate[]
  /** Providers vus en OAuth uniquement (non réutilisables hors OpenClaw). */
  oauthProviders: string[]
  /** Anomalies de lecture — toujours remontées, jamais avalées. */
  notes: string[]
}

/** Interprète un objet « profil » OpenClaw (canonique ou plat). */
function harvestProfile(value: unknown, providerHint: string | null, source: string, scan: OpenClawScan): void {
  if (!value || typeof value !== 'object') return
  const o = value as Record<string, unknown>
  const provider = typeof o['provider'] === 'string' ? o['provider'] : providerHint
  if (o['type'] === 'oauth') {
    if (provider) scan.oauthProviders.push(provider)
    return
  }
  // canonique { type:"api_key", provider, key } — ou plat { apiKey: "..." }
  const key = typeof o['key'] === 'string' ? o['key'] : typeof o['apiKey'] === 'string' ? o['apiKey'] : null
  if (key && key.trim() !== '' && provider && REUSABLE_PROVIDERS.has(provider)) {
    scan.candidates.push({ provider: provider as ReusableProvider, configPath: source, key: key.trim() })
  }
}

/** Parse un document auth (store complet { profiles } / plat / profil seul). */
function harvestAuthDocument(doc: unknown, source: string, scan: OpenClawScan): void {
  if (!doc || typeof doc !== 'object') return
  const root = doc as Record<string, unknown>
  const profiles = root['profiles']
  if (profiles && typeof profiles === 'object') {
    for (const [id, value] of Object.entries(profiles as Record<string, unknown>)) {
      // id de profil « provider:label » → indice de provider si absent du corps
      harvestProfile(value, id.split(':')[0] ?? null, source, scan)
    }
    return
  }
  if (typeof root['type'] === 'string') {
    harvestProfile(root, null, source, scan)
    return
  }
  // forme plate historique { "<provider>": { "apiKey": "..." } }
  for (const [id, value] of Object.entries(root)) {
    if (REUSABLE_PROVIDERS.has(id) || (value && typeof value === 'object' && 'apiKey' in (value as object))) {
      harvestProfile(value, id, source, scan)
    }
  }
}

/** Lit la table auth_profile_stores d'un SQLite OpenClaw (lecture seule). */
function harvestSqliteStore(dbPath: string, scan: OpenClawScan): void {
  let db: InstanceType<typeof DatabaseCtor> | null = null
  try {
    db = new DatabaseCtor(dbPath, { readonly: true, fileMustExist: true })
    const table = db
      .prepare(`SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'auth_profile_stores'`)
      .get() as { name: string } | undefined
    if (!table) return
    const rows = db.prepare('SELECT store_json FROM auth_profile_stores').all() as Array<{ store_json: string }>
    for (const row of rows) {
      try {
        harvestAuthDocument(JSON.parse(row.store_json), dbPath, scan)
      } catch (err) {
        scan.notes.push(`store_json illisible dans ${dbPath} : ${(err as Error).message}`)
      }
    }
  } catch (err) {
    scan.notes.push(`SQLite OpenClaw illisible (${dbPath}) : ${(err as Error).message}`)
  } finally {
    db?.close()
  }
}

/** Lit un fichier auth JSON OpenClaw (legacy en clair). */
function harvestJsonFile(filePath: string, scan: OpenClawScan): void {
  if (!existsSync(filePath)) return
  try {
    harvestAuthDocument(JSON.parse(readFileSync(filePath, 'utf8')), filePath, scan)
  } catch (err) {
    scan.notes.push(`fichier auth OpenClaw illisible (${filePath}) : ${(err as Error).message}`)
  }
}

/**
 * Cherche des credentials OpenClaw réutilisables dans TOUS les emplacements
 * connus (legacy JSON + stores SQLite). Lecture seule, jamais de log de clé.
 */
export function scanOpenClawCredentials(openclawDir: string = join(homedir(), '.openclaw')): OpenClawScan {
  const scan: OpenClawScan = { candidates: [], oauthProviders: [], notes: [] }
  if (!existsSync(openclawDir)) return scan

  const agentsDir = join(openclawDir, 'agents')
  if (existsSync(agentsDir)) {
    let agentIds: string[] = []
    try {
      agentIds = readdirSync(agentsDir)
    } catch (err) {
      scan.notes.push(`dossier agents OpenClaw illisible (${agentsDir}) : ${(err as Error).message}`)
    }
    for (const id of agentIds) {
      const agentDir = join(agentsDir, id, 'agent')
      harvestJsonFile(join(agentDir, 'auth-profiles.json'), scan)
      harvestJsonFile(join(agentDir, 'auth.json'), scan)
      const agentDb = join(agentDir, 'openclaw-agent.sqlite')
      if (existsSync(agentDb)) harvestSqliteStore(agentDb, scan)
    }
  }
  // fichier d'import legacy (OAuth uniquement, mais on le lit pour être complet)
  harvestJsonFile(join(openclawDir, 'credentials', 'oauth.json'), scan)
  const stateDb = join(openclawDir, 'state', 'openclaw.sqlite')
  if (existsSync(stateDb)) harvestSqliteStore(stateDb, scan)
  return scan
}

export interface CopyOpenClawKeyResult {
  provider: ReusableProvider
  /** Fichier écrit (chmod 600). */
  keyFile: string
  /** Store OpenClaw d'origine. */
  from: string
}

/**
 * Copie une clé API en clair trouvée chez OpenClaw vers ~/.<provider>/api_key
 * (chmod 600) — l'action « Réutiliser ma config OpenClaw » de l'onboarding.
 * Échec = erreur EXPLICITE (pas de clé trouvée, OAuth seulement, écriture KO).
 */
export function copyOpenClawKey(
  provider: ReusableProvider,
  opts: { openclawDir?: string; keyFile?: string } = {},
): CopyOpenClawKeyResult {
  const scan = scanOpenClawCredentials(opts.openclawDir)
  const candidate = scan.candidates.find(c => c.provider === provider)
  if (!candidate) {
    const oauth = scan.oauthProviders.includes(provider)
    throw new Error(
      oauth
        ? `OpenClaw n'a qu'un compte OAuth pour ${provider} — non réutilisable hors OpenClaw`
        : `aucune clé API ${provider} en clair trouvée dans la config OpenClaw${scan.notes.length > 0 ? ` (${scan.notes.join(' ; ')})` : ''}`,
    )
  }
  const keyFile = opts.keyFile ?? defaultKeyFile(provider)
  mkdirSync(dirname(keyFile), { recursive: true, mode: 0o700 })
  writeFileSync(keyFile, `${candidate.key}\n`, { encoding: 'utf8', mode: 0o600 })
  chmodSync(keyFile, 0o600) // mode de writeFileSync ignoré si le fichier existait
  return { provider, keyFile, from: candidate.configPath }
}

/**
 * Écrit une clé API SAISIE PAR L'UTILISATEUR vers ~/.<provider>/api_key
 * (chmod 600). Permet de coller sa clé depuis l'UI sans toucher au terminal.
 * La valeur n'est jamais loggée. Échec si la clé est vide.
 */
export function writeProviderKey(
  provider: ReusableProvider,
  key: string,
  opts: { keyFile?: string } = {},
): { provider: ReusableProvider; keyFile: string } {
  const trimmed = key.trim()
  if (trimmed === '') throw new Error('clé vide')
  const keyFile = opts.keyFile ?? defaultKeyFile(provider)
  mkdirSync(dirname(keyFile), { recursive: true, mode: 0o700 })
  writeFileSync(keyFile, `${trimmed}\n`, { encoding: 'utf8', mode: 0o600 })
  chmodSync(keyFile, 0o600) // mode de writeFileSync ignoré si le fichier existait
  return { provider, keyFile }
}

// ------------------------------------------------------ détection globale

/**
 * Inventaire des moteurs d'intelligence disponibles — LA source de l'étape
 * « Moteur d'intelligence » de l'onboarding et de GET /v1/admin/llm_health.
 */
export async function detectLlmOptions(opts: DetectLlmOptionsInput = {}): Promise<LlmOptions> {
  const env = opts.env ?? process.env
  const hasCommand = opts.hasCommand ?? defaultHasCommand
  const timeoutMs = opts.timeoutMs ?? 1500

  // --- Ollama : serveur + modèles requis + binaire
  const ollamaBase = (opts.ollamaBaseUrl ?? DEFAULT_OLLAMA_BASE_URL).replace(/\/$/, '')
  let serverUp = false
  let ollamaModels: string[] = []
  try {
    const res = await fetch(`${ollamaBase}/api/tags`, { signal: AbortSignal.timeout(timeoutMs) })
    if (res.ok) {
      serverUp = true
      const data = (await res.json()) as { models?: Array<{ name?: string; model?: string }> }
      ollamaModels = (data.models ?? []).map(m => m.name ?? m.model ?? '').filter(n => n !== '')
    } else {
      console.warn(`[memoria:llm] ollama ${ollamaBase}/api/tags → HTTP ${res.status}`)
    }
  } catch (err) {
    // serveur arrêté/injoignable : état normal en onboarding — visible quand même
    console.warn(`[memoria:llm] ollama injoignable (${ollamaBase}) : ${(err as Error).message}`)
  }
  const hasEmbedModel = ollamaModels.some(m => modelMatches(m, DEFAULT_OLLAMA_EMBEDDING_MODEL))
  const hasExtractModel = ollamaModels.some(m => modelMatches(m, DEFAULT_LOCAL_EXTRACTION_MODEL))
  const binaryInPath = hasCommand('ollama')
  const ollama: OllamaOption = {
    kind: 'ollama',
    available: serverUp && hasEmbedModel && hasExtractModel,
    serverUp,
    hasEmbedModel,
    hasExtractModel,
    binaryInPath,
    models: ollamaModels,
    baseUrl: ollamaBase,
    detail: !serverUp
      ? binaryInPath
        ? 'binaire ollama présent mais serveur injoignable — lance l’application Ollama (ou « ollama serve »)'
        : 'non détecté — installe-le depuis https://ollama.com/download'
      : !hasEmbedModel || !hasExtractModel
        ? `serveur actif, modèle(s) manquant(s) : ${[
            ...(hasExtractModel ? [] : [DEFAULT_LOCAL_EXTRACTION_MODEL]),
            ...(hasEmbedModel ? [] : [DEFAULT_OLLAMA_EMBEDDING_MODEL]),
          ].join(', ')}`
        : `prêt (${ollamaModels.length} modèle·s)`,
  }

  // --- LM Studio
  const lmBase = (opts.lmstudioBaseUrl ?? DEFAULT_LMSTUDIO_BASE_URL).replace(/\/$/, '')
  const lm = await lmstudioListModels(lmBase, timeoutMs)
  const lmstudio: LmStudioOption = {
    kind: 'lmstudio',
    available: lm.up,
    models: lm.models,
    baseUrl: lmBase,
    detail: !lm.up
      ? 'non détecté — installe LM Studio puis démarre son serveur local (onglet Developer)'
      : lm.models.length === 0
        ? 'serveur actif mais aucun modèle chargé — charge un modèle dans LM Studio'
        : `prêt (${lm.models.length} modèle·s chargé·s)`,
  }

  // --- Clés API (présence seulement, jamais la valeur)
  const openai = keyPresence('openai', env, opts.keyFiles?.openai ?? defaultKeyFile('openai'))
  const anthropic = keyPresence('anthropic', env, opts.keyFiles?.anthropic ?? defaultKeyFile('anthropic'))
  const openrouter = keyPresence('openrouter', env, opts.keyFiles?.openrouter ?? defaultKeyFile('openrouter'))

  // --- OpenClaw
  const openclawDir = opts.openclawDir ?? join(homedir(), '.openclaw')
  const openclawPresent = hasCommand('openclaw') || existsSync(openclawDir)
  let openclaw: OpenClawOption
  if (!openclawPresent) {
    openclaw = { kind: 'openclaw', available: false, reusable: false, detail: 'OpenClaw non détecté sur cette machine' }
  } else {
    const scan = scanOpenClawCredentials(openclawDir)
    const first = scan.candidates[0]
    const notes = scan.notes.length > 0 ? ` (${scan.notes.join(' ; ')})` : ''
    if (first) {
      openclaw = {
        kind: 'openclaw',
        available: true,
        reusable: true,
        provider: first.provider,
        configPath: first.configPath,
        detail: `clé API ${first.provider} réutilisable trouvée dans ${first.configPath}${notes}`,
      }
    } else if (scan.oauthProviders.length > 0) {
      openclaw = {
        kind: 'openclaw',
        available: true,
        reusable: false,
        reason: 'compte OAuth — non réutilisable hors OpenClaw',
        detail: `OpenClaw détecté, mais seulement des comptes OAuth (${[...new Set(scan.oauthProviders)].join(', ')})${notes}`,
      }
    } else {
      openclaw = {
        kind: 'openclaw',
        available: true,
        reusable: false,
        reason: 'aucune clé API en clair trouvée dans ses stores',
        detail: `OpenClaw détecté (${openclawDir}), aucune clé API en clair dans ses stores${notes}`,
      }
    }
  }

  return { ollama, lmstudio, openai, anthropic, openrouter, openclaw }
}
