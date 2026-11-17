/**
 * Sous-système LLM (spec §14) — factory de profils + exports.
 * resolveLlmProfile() ne retourne QUE des providers vérifiés disponibles :
 * jamais un nom de modèle inexistant (anti-exemple legacy : `gpt-5.4-nano`).
 * Ce qui n'est pas disponible vaut null — les couches LLM se désactivent
 * PROPREMENT, l'appelant teste isAvailable().
 */
import type { MemoriaConfig } from '../config.js'
import type { EmbeddingProvider, LlmProfile, LlmProvider } from './provider.js'
import { AnthropicProvider } from './anthropic.js'
import { DEFAULT_LOCAL_EXTRACTION_MODEL, OllamaEmbeddingProvider, OllamaProvider } from './ollama.js'
import { LmStudioProvider } from './lmstudio.js'
import {
  DEFAULT_OPENAI_MODEL,
  DEFAULT_OPENROUTER_MODEL,
  OpenAiProvider,
  resolveOpenAiApiKey,
} from './openai.js'

export type {
  CompleteOptions,
  EmbeddingProvider,
  LlmProfile,
  LlmProvider,
} from './provider.js'
export { NullLlmProvider } from './provider.js'
export {
  DEFAULT_LOCAL_EXTRACTION_MODEL,
  DEFAULT_OLLAMA_BASE_URL,
  DEFAULT_OLLAMA_EMBEDDING_DIMENSIONS,
  DEFAULT_OLLAMA_EMBEDDING_MODEL,
  OllamaEmbeddingProvider,
  OllamaProvider,
  modelMatches,
} from './ollama.js'
export type { OllamaEmbeddingProviderOptions, OllamaProviderOptions } from './ollama.js'
export {
  DEFAULT_LMSTUDIO_BASE_URL,
  LMSTUDIO_AUTO_MODEL,
  LmStudioProvider,
  lmstudioListModels,
} from './lmstudio.js'
export type { LmStudioModelsResult, LmStudioProviderOptions } from './lmstudio.js'
export {
  copyOpenClawKey,
  writeProviderKey,
  defaultHasCommand,
  detectLlmOptions,
  scanOpenClawCredentials,
} from './detect.js'
export type {
  ApiKeyOption,
  CopyOpenClawKeyResult,
  DetectLlmOptionsInput,
  LlmOptions,
  LmStudioOption,
  OllamaOption,
  OpenClawKeyCandidate,
  OpenClawOption,
  OpenClawScan,
  ReusableProvider,
} from './detect.js'
export {
  ANTHROPIC_API_VERSION,
  AnthropicProvider,
  DEFAULT_ANTHROPIC_BASE_URL,
  DEFAULT_ANTHROPIC_MODEL,
  defaultAnthropicKeyFile,
  resolveAnthropicApiKey,
} from './anthropic.js'
export type { AnthropicKeyOptions, AnthropicProviderOptions } from './anthropic.js'
export {
  DEFAULT_OPENAI_MODEL,
  DEFAULT_OPENAI_BASE_URL,
  DEFAULT_OPENROUTER_MODEL,
  DEFAULT_OPENROUTER_BASE_URL,
  OpenAiProvider,
  resolveOpenAiApiKey,
  defaultOpenAiKeyFile,
  defaultOpenRouterKeyFile,
} from './openai.js'
export type { OpenAiKeyOptions, OpenAiProviderOptions, OpenAiFlavor } from './openai.js'
export { assertVectorDimensions, cosineSimilarity } from './embeddings-guard.js'

export type LlmProfileName = '100-local' | 'local-plus-cloud' | 'cloud'

export interface ResolveLlmProfileOptions {
  /** URL du serveur Ollama (défaut http://127.0.0.1:11434). */
  ollamaBaseUrl?: string
  /** URL du serveur LM Studio (défaut http://127.0.0.1:1234/v1). */
  lmstudioBaseUrl?: string
  /** Environnement injectable pour les tests. */
  env?: NodeJS.ProcessEnv
  /** Chemin du fichier de clé Anthropic, injectable pour les tests. */
  anthropicKeyFile?: string
}

function normalizeProfileName(raw: string | undefined): LlmProfileName {
  if (raw === undefined || raw === '100-local' || raw === 'custom') return raw === 'custom' ? '100-local' : '100-local'
  if (raw === 'local-plus-cloud' || raw === 'cloud') return raw
  console.warn(`[memoria:llm] profil LLM inconnu « ${raw} » — repli sur 100-local`)
  return '100-local'
}

/** Construit un provider d'extraction nommé explicitement, ou null si indispo. */
async function buildExplicitProvider(
  provider: string,
  model: string | undefined,
  opts: ResolveLlmProfileOptions,
  baseUrl?: string,
): Promise<LlmProvider | null> {
  let p: LlmProvider | null = null
  switch (provider) {
    case 'ollama':
      p = new OllamaProvider({ model: model ?? DEFAULT_LOCAL_EXTRACTION_MODEL, baseUrl: baseUrl ?? opts.ollamaBaseUrl })
      break
    case 'lmstudio':
      p = new LmStudioProvider({ ...(model ? { model } : {}), baseUrl: baseUrl ?? opts.lmstudioBaseUrl })
      break
    case 'anthropic':
      p = new AnthropicProvider({ env: opts.env, keyFilePath: opts.anthropicKeyFile, ...(model ? { model } : {}) })
      break
    case 'openai':
      p = new OpenAiProvider({ flavor: 'openai', env: opts.env, model: model ?? DEFAULT_OPENAI_MODEL })
      break
    case 'openrouter':
      p = new OpenAiProvider({ flavor: 'openrouter', env: opts.env, model: model ?? DEFAULT_OPENROUTER_MODEL })
      break
    default:
      console.warn(`[memoria:llm] provider inconnu « ${provider} »`)
      return null
  }
  return (await p.isAvailable()) ? p : null
}

/**
 * Résout le profil LLM depuis la config :
 * - '100-local'       : extraction Ollama qwen2.5:3b · embeddings Ollama nomic-embed-text.
 * - 'local-plus-cloud': extraction Anthropic Haiku si clé, sinon Ollama · embeddings Ollama.
 * - 'cloud'           : extraction Anthropic si clé · embeddings Ollama (pas d'embeddings cloud en V1).
 * Chaque slot indisponible vaut null (et c'est dit dans les logs).
 */
export async function resolveLlmProfile(
  config: MemoriaConfig,
  opts: ResolveLlmProfileOptions = {},
): Promise<LlmProfile> {
  const ollamaExtraction = new OllamaProvider({
    model: DEFAULT_LOCAL_EXTRACTION_MODEL,
    baseUrl: opts.ollamaBaseUrl,
  })
  const ollamaEmbeddings = new OllamaEmbeddingProvider({ baseUrl: opts.ollamaBaseUrl })
  const anthropic = new AnthropicProvider({ env: opts.env, keyFilePath: opts.anthropicKeyFile })

  let extraction: LlmProvider | null = null

  // 1) Choix EXPLICITE du provider/modèle (prioritaire) — le « l'utilisateur décide ».
  const explicit = config.llm?.extraction
  if (explicit?.provider) {
    extraction = await buildExplicitProvider(explicit.provider, explicit.model, opts, explicit.base_url)
    if (extraction === null) {
      console.warn(`[memoria:llm] provider d'extraction « ${explicit.provider} » indisponible (clé/modèle ?) — repli profil`)
    }
  }

  // 2) Sinon, profil raccourci.
  if (extraction === null) {
    const profile = normalizeProfileName(config.llm?.profile)
    switch (profile) {
      case '100-local':
        extraction = (await ollamaExtraction.isAvailable()) ? ollamaExtraction : null
        break
      case 'local-plus-cloud':
        if (await anthropic.isAvailable()) extraction = anthropic
        else extraction = (await ollamaExtraction.isAvailable()) ? ollamaExtraction : null
        break
      case 'cloud':
        extraction = (await anthropic.isAvailable()) ? anthropic : null
        break
    }
  }

  // Embeddings : Ollama seul en V1 (Anthropic n'expose pas d'embeddings) — quel que soit le profil.
  const embeddings: EmbeddingProvider | null = (await ollamaEmbeddings.isAvailable())
    ? ollamaEmbeddings
    : null

  if (extraction === null) {
    console.warn(`[memoria:llm] aucun provider d'extraction disponible — couches LLM d'extraction désactivées`)
  }
  if (embeddings === null) {
    console.warn(`[memoria:llm] embeddings indisponibles — recherche sémantique désactivée (FTS seul)`)
  }

  return { extraction, embeddings }
}
