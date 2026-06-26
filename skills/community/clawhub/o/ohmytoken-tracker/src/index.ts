interface OhmyTokenConfig {
  api_key: string
  endpoint?: string
}

interface TokenUsage {
  model: string
  prompt_tokens: number
  completion_tokens: number
  reasoning_tokens?: number
  cached_tokens?: number
}

const DEFAULT_ENDPOINT = 'https://api.ohmytoken.dev/api/v1/ingest'

export default function ohmytokenTracker(config: OhmyTokenConfig) {
  const apiKey = config.api_key || process.env.OHMYTOKEN_API_KEY
  const endpoint = config.endpoint || DEFAULT_ENDPOINT

  if (!apiKey) {
    console.warn('[ohmytoken] No API key configured. Set OHMYTOKEN_API_KEY or config.api_key')
    return {}
  }

  return {
    name: 'ohmytoken-tracker',

    async onLLMResponse(usage: TokenUsage) {
      try {
        await fetch(endpoint, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-API-Key': apiKey,
          },
          body: JSON.stringify({
            model: usage.model || 'unknown',
            prompt_tokens: usage.prompt_tokens || 0,
            completion_tokens: usage.completion_tokens || 0,
            reasoning_tokens: usage.reasoning_tokens || 0,
            cached_tokens: usage.cached_tokens || 0,
          }),
        })
      } catch {
        // silent fail — don't break the user's workflow
      }
    },
  }
}
