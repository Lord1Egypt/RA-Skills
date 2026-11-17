/**
 * Provider LM Studio (spec §14) — serveur LOCAL OpenAI-compatible.
 * Base par défaut http://127.0.0.1:1234/v1 (configurable : config.toml
 * [llm.extraction] base_url). Aucune clé requise : LM Studio ignore
 * l'en-tête Authorization (on envoie « lm-studio » par convention).
 *
 * Modèle : explicite si configuré, sinon le PREMIER modèle chargé retourné
 * par GET /models — résolu au premier appel puis mémorisé.
 *
 * Mode JSON : on n'envoie PAS response_format (certaines versions de
 * LM Studio le rejettent sans json_schema) — on injecte une directive
 * « objet JSON » dans le system, comme le provider OpenAI.
 */
import type { CompleteOptions, LlmProvider } from './provider.js'

export const DEFAULT_LMSTUDIO_BASE_URL = 'http://127.0.0.1:1234/v1'
/** Sentinelle « premier modèle chargé » (résolu via /models au 1er appel). */
export const LMSTUDIO_AUTO_MODEL = 'auto'

const MODELS_TIMEOUT_MS = 1500

export interface LmStudioModelsResult {
  /** Le serveur répond sur GET /models. */
  up: boolean
  /** Identifiants des modèles chargés (format OpenAI : data[].id). */
  models: string[]
}

/**
 * Liste les modèles chargés dans LM Studio (GET {base}/models, timeout court).
 * Échec réseau/HTTP → up:false, ET c'est dit dans les logs — jamais muet.
 */
export async function lmstudioListModels(
  baseUrl: string = DEFAULT_LMSTUDIO_BASE_URL,
  timeoutMs: number = MODELS_TIMEOUT_MS,
): Promise<LmStudioModelsResult> {
  const base = baseUrl.replace(/\/$/, '')
  try {
    const res = await fetch(`${base}/models`, { signal: AbortSignal.timeout(timeoutMs) })
    if (!res.ok) {
      console.warn(`[memoria:llm] lmstudio ${base}/models → HTTP ${res.status} : provider indisponible`)
      return { up: false, models: [] }
    }
    const data = (await res.json()) as { data?: Array<{ id?: string }> }
    const models = (data.data ?? []).map(m => m.id ?? '').filter(id => id !== '')
    return { up: true, models }
  } catch (err) {
    console.warn(`[memoria:llm] lmstudio injoignable (${base}) : ${(err as Error).message}`)
    return { up: false, models: [] }
  }
}

export interface LmStudioProviderOptions {
  /** Modèle explicite ; absent → premier modèle chargé (LMSTUDIO_AUTO_MODEL). */
  model?: string
  baseUrl?: string
  timeoutMs?: number
}

interface ChatCompletionResponse {
  choices?: Array<{ message?: { content?: string } }>
}

export class LmStudioProvider implements LlmProvider {
  readonly name = 'lmstudio'
  /** Modèle configuré, ou 'auto' (= premier modèle chargé, résolu au 1er appel). */
  readonly model: string
  private resolvedModel: string | null = null
  private readonly baseUrl: string
  private readonly timeoutMs: number

  constructor(opts: LmStudioProviderOptions = {}) {
    this.model = opts.model ?? LMSTUDIO_AUTO_MODEL
    this.baseUrl = (opts.baseUrl ?? DEFAULT_LMSTUDIO_BASE_URL).replace(/\/$/, '')
    this.timeoutMs = opts.timeoutMs ?? 60_000
  }

  /**
   * true ssi le serveur répond ET (mode auto : ≥ 1 modèle chargé ; modèle
   * explicite : présent dans la liste). Faux → warn, jamais silencieux.
   */
  async isAvailable(): Promise<boolean> {
    const { up, models } = await lmstudioListModels(this.baseUrl)
    if (!up) return false
    if (this.model === LMSTUDIO_AUTO_MODEL) {
      if (models.length === 0) {
        console.warn(`[memoria:llm] lmstudio : aucun modèle chargé (${this.baseUrl}) — charge un modèle dans LM Studio`)
        return false
      }
      return true
    }
    const present = models.includes(this.model)
    if (!present) {
      console.warn(`[memoria:llm] lmstudio : modèle « ${this.model} » non chargé (chargés : ${models.join(', ') || 'aucun'})`)
    }
    return present
  }

  /** Modèle effectif : explicite, ou premier modèle chargé (mémorisé). */
  private async effectiveModel(): Promise<string> {
    if (this.model !== LMSTUDIO_AUTO_MODEL) return this.model
    if (this.resolvedModel) return this.resolvedModel
    const { up, models } = await lmstudioListModels(this.baseUrl)
    if (!up) throw new Error(`lmstudio injoignable (${this.baseUrl}) — démarre le serveur local de LM Studio`)
    const first = models[0]
    if (!first) throw new Error(`lmstudio : aucun modèle chargé (${this.baseUrl}) — charge un modèle dans LM Studio`)
    this.resolvedModel = first
    return first
  }

  async complete(opts: CompleteOptions): Promise<string> {
    const model = await this.effectiveModel()

    // Mode JSON : directive explicite dans le system (pas de response_format —
    // voir l'en-tête du fichier). On demande un OBJET, jamais un tableau nu.
    let system = opts.system
    if (opts.json) {
      const hasJson = `${system ?? ''} ${opts.prompt}`.toLowerCase().includes('json')
      if (!hasJson) {
        const directive = 'Réponds uniquement avec un objet JSON valide.'
        system = system ? `${system}\n${directive}` : directive
      }
    }

    const messages: Array<{ role: string; content: string }> = []
    if (system) messages.push({ role: 'system', content: system })
    messages.push({ role: 'user', content: opts.prompt })

    const res = await fetch(`${this.baseUrl}/chat/completions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // Pas de clé requise — en-tête de convention, ignoré par LM Studio.
        Authorization: 'Bearer lm-studio',
      },
      body: JSON.stringify({
        model,
        messages,
        max_tokens: opts.maxTokens ?? 1024,
        ...(opts.temperature !== undefined ? { temperature: opts.temperature } : {}),
      }),
      signal: AbortSignal.timeout(this.timeoutMs),
    })
    if (!res.ok) {
      const detail = await res.text().catch(() => '')
      throw new Error(`lmstudio /chat/completions HTTP ${res.status} (modèle ${model}) : ${detail.slice(0, 200)}`)
    }
    const data = (await res.json()) as ChatCompletionResponse
    const content = data.choices?.[0]?.message?.content
    if (typeof content !== 'string') {
      throw new Error(`réponse lmstudio invalide : choices[0].message.content absent (modèle ${model})`)
    }
    return content
  }
}
