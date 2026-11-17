/**
 * Providers Ollama (spec §14) — voie 100 % locale par défaut.
 * Chat via POST /api/chat (stream:false), embeddings via POST /api/embed.
 * isAvailable() vérifie que le serveur répond ET que le modèle est tiré
 * (GET /api/tags) — un échec réseau retourne false mais N'EST JAMAIS muet.
 */
import type { CompleteOptions, EmbeddingProvider, LlmProvider } from './provider.js'
import { assertVectorDimensions } from './embeddings-guard.js'

export const DEFAULT_OLLAMA_BASE_URL = 'http://127.0.0.1:11434'
export const DEFAULT_OLLAMA_EMBEDDING_MODEL = 'nomic-embed-text'
export const DEFAULT_OLLAMA_EMBEDDING_DIMENSIONS = 768
/** Modèle d'extraction local par défaut (spec §14). */
export const DEFAULT_LOCAL_EXTRACTION_MODEL = 'qwen2.5:3b'

const TAGS_TIMEOUT_MS = 1500

interface OllamaTagsResponse {
  models?: Array<{ name?: string; model?: string }>
}

/** « nomic-embed-text » matche « nomic-embed-text:latest » (exporté pour detect.ts). */
export function modelMatches(installed: string, wanted: string): boolean {
  if (installed === wanted) return true
  // /api/tags liste « name:tag » — accepter « nomic-embed-text » pour « nomic-embed-text:latest »
  return !wanted.includes(':') && installed === `${wanted}:latest`
}

/** true ssi le serveur Ollama répond ET liste le modèle. Échec réseau → warn + false. */
async function ollamaHasModel(baseUrl: string, model: string): Promise<boolean> {
  try {
    const res = await fetch(`${baseUrl}/api/tags`, { signal: AbortSignal.timeout(TAGS_TIMEOUT_MS) })
    if (!res.ok) {
      console.warn(`[memoria:llm] ollama ${baseUrl}/api/tags → HTTP ${res.status} : provider indisponible`)
      return false
    }
    const data = (await res.json()) as OllamaTagsResponse
    return (data.models ?? []).some(m => modelMatches(m.name ?? m.model ?? '', model))
  } catch (err) {
    // Réseau KO / timeout : indisponible — visible dans les logs, jamais avalé en silence.
    console.warn(`[memoria:llm] ollama injoignable (${baseUrl}) : ${(err as Error).message}`)
    return false
  }
}

export interface OllamaProviderOptions {
  model: string
  baseUrl?: string
  timeoutMs?: number
}

export class OllamaProvider implements LlmProvider {
  readonly name = 'ollama'
  readonly model: string
  private readonly baseUrl: string
  private readonly timeoutMs: number

  constructor(opts: OllamaProviderOptions) {
    this.model = opts.model
    this.baseUrl = (opts.baseUrl ?? DEFAULT_OLLAMA_BASE_URL).replace(/\/$/, '')
    this.timeoutMs = opts.timeoutMs ?? 30_000
  }

  isAvailable(): Promise<boolean> {
    return ollamaHasModel(this.baseUrl, this.model)
  }

  async complete(opts: CompleteOptions): Promise<string> {
    const messages: Array<{ role: string; content: string }> = []
    if (opts.system) messages.push({ role: 'system', content: opts.system })
    messages.push({ role: 'user', content: opts.prompt })

    const res = await fetch(`${this.baseUrl}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: this.model,
        messages,
        stream: false,
        options: {
          num_predict: opts.maxTokens ?? 1024,
          temperature: opts.temperature ?? 0.1,
        },
        format: opts.json ? 'json' : undefined,
      }),
      signal: AbortSignal.timeout(this.timeoutMs),
    })
    if (!res.ok) {
      const detail = await res.text().catch(() => '')
      throw new Error(`ollama /api/chat HTTP ${res.status} (modèle ${this.model}) : ${detail.slice(0, 200)}`)
    }
    const data = (await res.json()) as { message?: { content?: string } }
    const content = data.message?.content
    if (typeof content !== 'string') {
      throw new Error(`réponse ollama invalide : message.content absent (modèle ${this.model})`)
    }
    return content
  }
}

export interface OllamaEmbeddingProviderOptions {
  model?: string
  dimensions?: number
  baseUrl?: string
  timeoutMs?: number
}

export class OllamaEmbeddingProvider implements EmbeddingProvider {
  readonly name = 'ollama'
  readonly model: string
  readonly dimensions: number
  private readonly baseUrl: string
  private readonly timeoutMs: number

  constructor(opts: OllamaEmbeddingProviderOptions = {}) {
    this.model = opts.model ?? DEFAULT_OLLAMA_EMBEDDING_MODEL
    this.dimensions = opts.dimensions ?? DEFAULT_OLLAMA_EMBEDDING_DIMENSIONS
    this.baseUrl = (opts.baseUrl ?? DEFAULT_OLLAMA_BASE_URL).replace(/\/$/, '')
    this.timeoutMs = opts.timeoutMs ?? 60_000
  }

  isAvailable(): Promise<boolean> {
    return ollamaHasModel(this.baseUrl, this.model)
  }

  async embed(texts: string[]): Promise<Float32Array[]> {
    if (texts.length === 0) return []
    const res = await fetch(`${this.baseUrl}/api/embed`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ model: this.model, input: texts }),
      signal: AbortSignal.timeout(this.timeoutMs),
    })
    if (!res.ok) {
      const detail = await res.text().catch(() => '')
      throw new Error(`ollama /api/embed HTTP ${res.status} (modèle ${this.model}) : ${detail.slice(0, 200)}`)
    }
    const data = (await res.json()) as { embeddings?: number[][] }
    const embeddings = data.embeddings
    if (!Array.isArray(embeddings) || embeddings.length !== texts.length) {
      throw new Error(
        `réponse ollama /api/embed invalide : ${Array.isArray(embeddings) ? embeddings.length : 0} ` +
          `vecteurs pour ${texts.length} textes (modèle ${this.model})`,
      )
    }
    return embeddings.map(vec => {
      const f32 = Float32Array.from(vec)
      // LA garde anti-768/1536 : aucun vecteur cross-dimension ne sort d'ici.
      assertVectorDimensions(f32, this.dimensions, this.model)
      return f32
    })
  }
}
