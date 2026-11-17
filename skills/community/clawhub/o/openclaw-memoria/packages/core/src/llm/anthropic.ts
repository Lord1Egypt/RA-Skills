/**
 * Provider Anthropic (spec §14) — cloud opt-in, défaut Haiku 4.5.
 * Clé : param explicite > $ANTHROPIC_API_KEY > fichier ~/.anthropic/api_key
 * (chemin injectable pour les tests). isAvailable() = clé présente, AUCUN
 * appel réseau.
 */
import { existsSync, readFileSync } from 'node:fs'
import { homedir } from 'node:os'
import { join } from 'node:path'
import type { CompleteOptions, LlmProvider } from './provider.js'

export const DEFAULT_ANTHROPIC_MODEL = 'claude-haiku-4-5-20251001'
export const DEFAULT_ANTHROPIC_BASE_URL = 'https://api.anthropic.com'
export const ANTHROPIC_API_VERSION = '2023-06-01'

export function defaultAnthropicKeyFile(): string {
  return join(homedir(), '.anthropic', 'api_key')
}

export interface AnthropicKeyOptions {
  /** Priorité 1 : clé passée en paramètre. */
  apiKey?: string
  /** Environnement injectable pour les tests (défaut process.env). */
  env?: NodeJS.ProcessEnv
  /** Chemin du fichier de clé, injectable pour les tests (défaut ~/.anthropic/api_key). */
  keyFilePath?: string
}

/** Résout la clé API : param > env ANTHROPIC_API_KEY > fichier. null si rien. */
export function resolveAnthropicApiKey(opts: AnthropicKeyOptions = {}): string | null {
  if (opts.apiKey && opts.apiKey.trim() !== '') return opts.apiKey.trim()

  const env = opts.env ?? process.env
  const fromEnv = env['ANTHROPIC_API_KEY']
  if (fromEnv && fromEnv.trim() !== '') return fromEnv.trim()

  const keyFile = opts.keyFilePath ?? defaultAnthropicKeyFile()
  try {
    if (!existsSync(keyFile)) return null
    const raw = readFileSync(keyFile, 'utf8').trim()
    return raw === '' ? null : raw
  } catch (err) {
    // Fichier présent mais illisible (droits ?) : on le signale, on ne plante pas.
    console.warn(`[memoria:llm] clé Anthropic illisible (${keyFile}) : ${(err as Error).message}`)
    return null
  }
}

export interface AnthropicProviderOptions extends AnthropicKeyOptions {
  model?: string
  baseUrl?: string
  timeoutMs?: number
}

interface AnthropicMessageResponse {
  content?: Array<{ type?: string; text?: string }>
}

export class AnthropicProvider implements LlmProvider {
  readonly name = 'anthropic'
  readonly model: string
  private readonly apiKey: string | null
  private readonly baseUrl: string
  private readonly timeoutMs: number

  constructor(opts: AnthropicProviderOptions = {}) {
    this.model = opts.model ?? DEFAULT_ANTHROPIC_MODEL
    this.apiKey = resolveAnthropicApiKey(opts)
    this.baseUrl = (opts.baseUrl ?? DEFAULT_ANTHROPIC_BASE_URL).replace(/\/$/, '')
    this.timeoutMs = opts.timeoutMs ?? 30_000
  }

  isAvailable(): Promise<boolean> {
    return Promise.resolve(this.apiKey !== null)
  }

  async complete(opts: CompleteOptions): Promise<string> {
    if (this.apiKey === null) {
      throw new Error('AnthropicProvider : aucune clé API (param, $ANTHROPIC_API_KEY ou ~/.anthropic/api_key)')
    }

    // Pas de mode JSON natif côté API : on contraint via le system prompt (best effort).
    let system = opts.system
    if (opts.json) {
      const directive = 'Réponds uniquement avec un objet JSON valide, sans aucun texte autour.'
      system = system ? `${system}\n${directive}` : directive
    }

    const res = await fetch(`${this.baseUrl}/v1/messages`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': this.apiKey,
        'anthropic-version': ANTHROPIC_API_VERSION,
      },
      body: JSON.stringify({
        model: this.model,
        max_tokens: opts.maxTokens ?? 1024,
        temperature: opts.temperature,
        system,
        messages: [{ role: 'user', content: opts.prompt }],
      }),
      signal: AbortSignal.timeout(this.timeoutMs),
    })
    if (!res.ok) {
      const detail = await res.text().catch(() => '')
      throw new Error(`anthropic /v1/messages HTTP ${res.status} (modèle ${this.model}) : ${detail.slice(0, 200)}`)
    }
    const data = (await res.json()) as AnthropicMessageResponse
    const first = data.content?.[0]
    if (!first || typeof first.text !== 'string') {
      throw new Error(`réponse anthropic invalide : content[0].text absent (modèle ${this.model})`)
    }
    return first.text
  }
}
