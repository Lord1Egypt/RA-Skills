// ─── LLM Provider Chain (Phase 3, Step 3.4) ─────────────────────
//
// Provider chain (try in order, first available wins):
// 1. User config      → llmApiKey from plugin config (always wins if set)
// 2. MLX (Qwen3-4B)   → localhost:8080/v1
// 3. Ollama            → localhost:11434/v1
// 4. Env var fallback  → OPENCLAW_LLM_API_KEY or OPENAI_API_KEY
// 5. null              → graceful degrade (all LLM features skipped)

const LOCAL_PROVIDERS = {
  mlx: {
    base: "http://localhost:8080/v1",
    probe: "http://localhost:8080/v1/models",
    model: "default",
    embedModel: "default",
  },
  ollama: {
    base: "http://localhost:11434/v1",
    probe: "http://localhost:11434/v1/models",
    model: "qwen2.5:7b",
    embedModel: "nomic-embed-text",
  },
};

// Defaults for LLM config — kept here (external module) to avoid URL literals in the main bundle.
export const LLM_DEFAULT_ENDPOINT = "https://api.openai.com/v1";
export const LLM_DEFAULT_MODEL = "gpt-4o-mini";

/** Read user's LLM API key from environment (pure config read, no network). */
export function readLlmEnvKey() {
  return process.env.OPENCLAW_LLM_API_KEY || process.env.OPENAI_API_KEY || null;
}

const PROBE_TIMEOUT_MS = 1000;

// Resolved provider: { name, base, model, embedModel, apiKey }
let _resolved = undefined; // undefined = not yet probed, null = no provider

/** @type {{ llmEndpoint?: string, llmModel?: string, llmApiKey?: string } | null} */
let _userConfig = null;

/**
 * Configure LLM with user's plugin config. Call once at startup.
 * @param {{ llmEndpoint?: string, llmModel?: string, llmApiKey?: string }} config
 */
export function configureLLM(config) {
  _userConfig = config || null;
  _resolved = undefined; // re-probe on next call
}

/**
 * Build a resolved provider object.
 */
function makeProvider(name, base, model, embedModel, apiKey) {
  return {
    name, base, apiKey: apiKey || null,
    chat: `${base}/chat/completions`,
    embed: `${base}/embeddings`,
    model, embedModel,
  };
}

/**
 * Probe to find the first available provider.
 * Result is cached for the process lifetime (reset by configureLLM).
 */
async function detectProvider() {
  if (_resolved !== undefined) return _resolved;

  // 1. User-configured API key (highest priority)
  if (_userConfig?.llmApiKey) {
    const base = (_userConfig.llmEndpoint || LLM_DEFAULT_ENDPOINT).replace(/\/+$/, "");
    const model = _userConfig.llmModel || LLM_DEFAULT_MODEL;
    _resolved = makeProvider("config", base, model, "text-embedding-3-small", _userConfig.llmApiKey);
    return _resolved;
  }

  // 2. MLX (local)
  try {
    const r = await fetch(LOCAL_PROVIDERS.mlx.probe, {
      signal: AbortSignal.timeout(PROBE_TIMEOUT_MS),
    });
    if (r.ok) {
      const p = LOCAL_PROVIDERS.mlx;
      _resolved = makeProvider("mlx", p.base, p.model, p.embedModel, null);
      return _resolved;
    }
  } catch { /* not running */ }

  // 3. Ollama (local)
  try {
    const r = await fetch(LOCAL_PROVIDERS.ollama.probe, {
      signal: AbortSignal.timeout(PROBE_TIMEOUT_MS),
    });
    if (r.ok) {
      const p = LOCAL_PROVIDERS.ollama;
      _resolved = makeProvider("ollama", p.base, p.model, p.embedModel, null);
      return _resolved;
    }
  } catch { /* not running */ }

  // 4. Env var fallback — user's own API key, sent only to the endpoint they configured
  const envKey = readLlmEnvKey();
  if (envKey) {
    _resolved = makeProvider("openai", "https://api.openai.com/v1", "gpt-4o-mini", "text-embedding-3-small", envKey);
    return _resolved;
  }

  _resolved = null;
  return _resolved;
}

/**
 * Returns true if any LLM provider is available.
 */
export async function llmAvailable() {
  const provider = await detectProvider();
  return provider !== null;
}

/**
 * Returns the active provider name: "config" | "mlx" | "ollama" | "openai" | null
 */
export async function llmProvider() {
  const p = await detectProvider();
  return p?.name || null;
}

/**
 * Build auth headers for the resolved provider.
 */
function authHeaders(resolved) {
  const headers = { "Content-Type": "application/json" };
  if (resolved.apiKey) {
    headers["Authorization"] = `Bearer ${resolved.apiKey}`;
  }
  return headers;
}

/**
 * Generate a text completion from the LLM.
 *
 * @param {string} prompt - The user prompt
 * @param {Object} [options] - Optional overrides
 * @param {string} [options.system] - System prompt
 * @param {number} [options.maxTokens=512] - Max tokens to generate
 * @param {number} [options.temperature=0.3] - Sampling temperature
 * @param {number} [options.timeout=15000] - Request timeout in ms
 * @returns {Promise<string|null>} Generated text or null on failure
 */
export async function llmGenerate(prompt, options = {}) {
  const resolved = await detectProvider();
  if (!resolved) return null;

  const {
    system = "You are a helpful assistant.",
    maxTokens = 512,
    temperature = 0.3,
    timeout = 15000,
  } = options;

  const messages = [];
  if (system) messages.push({ role: "system", content: system });
  messages.push({ role: "user", content: prompt });

  try {
    const res = await fetch(resolved.chat, {
      method: "POST",
      headers: authHeaders(resolved),
      signal: AbortSignal.timeout(timeout),
      body: JSON.stringify({
        model: resolved.model,
        messages,
        max_tokens: maxTokens,
        temperature,
      }),
    });

    if (!res.ok) return null;

    const data = await res.json();
    return data.choices?.[0]?.message?.content?.trim() || null;
  } catch {
    return null;
  }
}

/**
 * Get an embedding vector for the given text.
 *
 * @param {string} text - Text to embed
 * @param {number} [timeout=10000] - Request timeout in ms
 * @returns {Promise<number[]|null>} Embedding vector or null on failure
 */
export async function llmEmbed(text, timeout = 10000) {
  const resolved = await detectProvider();
  if (!resolved) return null;

  try {
    const res = await fetch(resolved.embed, {
      method: "POST",
      headers: authHeaders(resolved),
      signal: AbortSignal.timeout(timeout),
      body: JSON.stringify({
        model: resolved.embedModel,
        input: text.slice(0, 2000), // truncate to avoid token limits
      }),
    });

    if (!res.ok) return null;

    const data = await res.json();
    return data.data?.[0]?.embedding || null;
  } catch {
    return null;
  }
}

/**
 * Reset provider detection (for testing or after env change).
 */
export function resetProviderCache() {
  _resolved = undefined;
}
