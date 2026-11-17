/**
 * Adaptateur OpenClaw ⇄ Memoria — plugin de hooks MINCE, ZÉRO dépendance native.
 *
 * OpenClaw parle MCP nativement (pull), mais l'auto-recall (injecter la mémoire
 * AVANT chaque tour) et l'auto-capture (mémoriser APRÈS chaque tour) exigent les
 * HOOKS. Ce plugin ne contient aucune logique mémoire : il traduit deux hooks en
 * appels HTTP au daemon Memoria local (127.0.0.1 + token d'instance).
 *
 *   before_prompt_build  → POST /v1/memory/recall        → { prependContext }
 *   agent_end            → POST /v1/memory/capture_turn  (fire-and-forget)
 *
 * ⚠️ `agent_end` est un « conversation hook » : depuis OpenClaw 2026.5, il est
 * BLOQUÉ par défaut pour les plugins non bundlés tant que la config ne pose pas
 * `plugins.entries.memoria.hooks.allowConversationAccess=true`. C'est ce qui a
 * silencieusement tué la capture en v3.34 (voir docs/v3/DIAG-OPENCLAW-2026.6.5.md).
 * L'install (registerOpenClaw côté @memoria/mcp) pose ce flag automatiquement.
 *
 * Tout échec (daemon arrêté, timeout, Memoria en pause) est AVALÉ proprement :
 * un agent ne doit jamais casser parce que sa mémoire est indisponible.
 */
import { existsSync, readFileSync } from 'node:fs'
import { homedir } from 'node:os'
import { join } from 'node:path'

// ------------------------------------------------------------ types OpenClaw (type-only, effacés au runtime)

/** Sous-ensemble de `OpenClawPluginApi` réellement utilisé (cf. DIAG §3). */
export interface OpenClawPluginApi {
  pluginConfig?: Record<string, unknown>
  logger?: { warn?: (m: string) => void; info?: (m: string) => void; debug?: (m: string) => void }
  on: <E = unknown, R = unknown>(
    hook: string,
    handler: (event: E, ctx?: HookContext) => R | Promise<R>,
    opts?: { priority?: number; timeoutMs?: number },
  ) => void
}

export interface HookContext {
  sessionId?: string
  agentId?: string
}

/** Événement before_prompt_build (DIAG §2). */
export interface BeforePromptBuildEvent {
  prompt?: unknown
  messages?: unknown
}

/** Résultat before_prompt_build : on n'utilise que prependContext (DIAG §2.3). */
export interface BeforePromptBuildResult {
  prependContext?: string
}

/** Événement agent_end (DIAG §2). `toolCallCount` est ABSENT du type — ne pas le lire. */
export interface AgentEndEvent {
  runId?: string
  messages?: unknown
  success?: boolean
  error?: string
  durationMs?: number
}

// ------------------------------------------------------------ config & découverte du daemon

interface AdapterConfig {
  daemonUrl?: string
  token?: string
  instance: string
  storageRoot?: string
  autoRecall: boolean
  autoCapture: boolean
  recallLimit: number
  recallTimeoutMs: number
}

function readConfig(raw: Record<string, unknown> | undefined): AdapterConfig {
  const c = raw ?? {}
  return {
    daemonUrl: typeof c['daemonUrl'] === 'string' && c['daemonUrl'] ? String(c['daemonUrl']) : undefined,
    token: typeof c['token'] === 'string' && c['token'] ? String(c['token']) : undefined,
    instance: typeof c['instance'] === 'string' && c['instance'] ? String(c['instance']) : 'koda',
    storageRoot: typeof c['storageRoot'] === 'string' && c['storageRoot'] ? String(c['storageRoot']) : undefined,
    autoRecall: c['autoRecall'] !== false,
    autoCapture: c['autoCapture'] !== false,
    recallLimit: clampInt(c['recallLimit'], 12, 1, 20),
    recallTimeoutMs: clampInt(c['recallTimeoutMs'], 400, 100, 5000),
  }
}

function clampInt(v: unknown, def: number, min: number, max: number): number {
  const n = typeof v === 'number' ? v : Number(v)
  if (!Number.isFinite(n)) return def
  return Math.min(max, Math.max(min, Math.round(n)))
}

/**
 * URL de base du daemon : `daemonUrl` explicite, sinon découverte du PORT via le
 * fichier d'état `<storageRoot>/daemon.json` (le port est éphémère côté Memoria).
 * Le token d'instance, lui, vient TOUJOURS de la config (jamais de daemon.json,
 * qui ne contient que le token admin — inutilisable sur /v1/memory/*).
 */
export function resolveBaseUrl(cfg: Pick<AdapterConfig, 'daemonUrl' | 'storageRoot'>): string | null {
  if (cfg.daemonUrl) return cfg.daemonUrl.replace(/\/+$/, '')
  const root = cfg.storageRoot ?? join(homedir(), '.memoria', 'data')
  const statePath = join(root, 'daemon.json')
  if (!existsSync(statePath)) return null
  try {
    const state = JSON.parse(readFileSync(statePath, 'utf8')) as { port?: number }
    if (typeof state.port === 'number' && state.port > 0) return `http://127.0.0.1:${state.port}`
  } catch {
    /* fichier illisible : daemon probablement arrêté */
  }
  return null
}

// ------------------------------------------------------------ extraction défensive des payloads

/** Extrait le texte d'un message OpenClaw (string OU tableau de parts {text}). */
export function partsToText(content: unknown): string {
  if (typeof content === 'string') return content
  if (Array.isArray(content)) {
    return content
      .map(p => {
        if (typeof p === 'string') return p
        if (p && typeof p === 'object') {
          const o = p as Record<string, unknown>
          if (typeof o['text'] === 'string') return o['text']
          if (typeof o['content'] === 'string') return o['content']
        }
        return ''
      })
      .join('')
  }
  if (content && typeof content === 'object') {
    const o = content as Record<string, unknown>
    if (typeof o['text'] === 'string') return o['text']
  }
  return ''
}

/** Normalise des messages hétérogènes vers le format Memoria {role, content}. */
export function toMemoriaMessages(messages: unknown): Array<{ role: string; content: string }> {
  if (!Array.isArray(messages)) return []
  const out: Array<{ role: string; content: string }> = []
  for (const m of messages) {
    if (!m || typeof m !== 'object') continue
    const o = m as Record<string, unknown>
    const role = typeof o['role'] === 'string' ? o['role'] : 'assistant'
    const content = partsToText(o['content'] ?? o['text']).trim()
    if (content) out.push({ role, content })
  }
  return out
}

/** Requête de recall : le prompt s'il est texte, sinon le dernier message user. */
export function queryFromEvent(event: BeforePromptBuildEvent): string {
  if (typeof event.prompt === 'string' && event.prompt.trim()) return event.prompt.trim()
  const msgs = toMemoriaMessages(event.messages)
  for (let i = msgs.length - 1; i >= 0; i--) {
    const m = msgs[i]
    if (m && m.role === 'user') return m.content
  }
  return msgs.length > 0 ? msgs[msgs.length - 1]!.content : ''
}

/** Item de recall renvoyé par le daemon (cf. RecallItem du core). */
export interface RecallItem {
  kind: 'fact' | 'procedure' | 'observation'
  content: string
  category: string
  score: number
}

/** Formate les souvenirs en bloc Markdown injectable. Vide → chaîne vide. */
export function formatRecall(items: RecallItem[]): string {
  if (!items || items.length === 0) return ''
  const icon = (k: string): string => (k === 'procedure' ? '⚙️' : k === 'observation' ? '👁️' : '•')
  const lines = items.map(i => `${icon(i.kind)} ${i.content.trim()}`)
  return ['## 🧠 Mémoire pertinente (Memoria)', '', ...lines, ''].join('\n')
}

// ------------------------------------------------------------ register

export function register(api: OpenClawPluginApi): void {
  const cfg = readConfig(api.pluginConfig)
  const warn = (m: string): void => api.logger?.warn?.(`[memoria] ${m}`)

  if (!cfg.token) {
    warn('aucun token d’instance configuré (plugins.entries.memoria.config.token) — mémoire désactivée jusqu’au pairing.')
    return
  }

  const post = async (path: string, body: unknown, timeoutMs: number): Promise<Response | null> => {
    const base = resolveBaseUrl(cfg)
    if (!base) return null // daemon arrêté : on n'injecte/capture pas, sans bruit
    try {
      return await fetch(base + path, {
        method: 'POST',
        headers: { 'content-type': 'application/json', authorization: `Bearer ${cfg.token!}` },
        body: JSON.stringify(body),
        signal: AbortSignal.timeout(timeoutMs),
      })
    } catch (err) {
      warn(`appel ${path} ignoré : ${(err as Error).message}`)
      return null
    }
  }

  // (1) AUTO-RECALL — before_prompt_build est un prompt-injection hook, autorisé
  //     par défaut (allowPromptInjection ≠ false). Timeout DUR : la mémoire ne
  //     doit jamais retarder un tour.
  if (cfg.autoRecall) {
    api.on<BeforePromptBuildEvent, BeforePromptBuildResult | undefined>(
      'before_prompt_build',
      async event => {
        const query = queryFromEvent(event)
        if (!query) return undefined
        const res = await post('/v1/memory/recall', { query, limit: cfg.recallLimit }, cfg.recallTimeoutMs)
        if (!res || !res.ok) return undefined
        try {
          const data = (await res.json()) as { items?: RecallItem[]; disabled?: boolean }
          if (data.disabled || !data.items || data.items.length === 0) return undefined
          const prependContext = formatRecall(data.items)
          return prependContext ? { prependContext } : undefined
        } catch {
          return undefined
        }
      },
      { timeoutMs: cfg.recallTimeoutMs + 200 },
    )
  }

  // (2) AUTO-CAPTURE — agent_end est un CONVERSATION hook : exige
  //     allowConversationAccess=true (posé à l'install).
  //     VRAI fire-and-forget : on ne bloque PAS la fin de tour de l'agent. Le
  //     daemon journalise (WAL) AVANT d'extraire → même si le timeout coupe
  //     l'extraction, les messages sont rejoués au prochain boot (jamais perdus).
  if (cfg.autoCapture) {
    api.on<AgentEndEvent, void>('agent_end', event => {
      const messages = toMemoriaMessages(event.messages)
      if (messages.length === 0) return
      // pas d'await : la requête vit en tâche de fond pendant que l'agent rend la main
      void post('/v1/memory/capture_turn', { messages }, 15_000)
    })
  }

  api.logger?.info?.(
    `[memoria] connecté (instance ${cfg.instance}) — recall:${cfg.autoRecall ? 'on' : 'off'} capture:${cfg.autoCapture ? 'on' : 'off'}`,
  )
}

export default { register }
