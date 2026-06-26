// HTTP client con rate limiting y retry para la API de Mercado Libre

import { getAccessToken } from './auth.js'
import type { MLError } from './types.js'

const ML_API_BASE = 'https://api.mercadolibre.com'
const MAX_RETRIES = 2
const RETRY_DELAY_MS = 1000

interface RequestOptions {
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE'
  body?: Record<string, unknown>
  params?: Record<string, string | number | undefined>
}

export async function mlFetch<T>(
  path: string,
  options: RequestOptions = {}
): Promise<T> {
  const { method = 'GET', body, params } = options

  // Construir URL con query params
  let url = `${ML_API_BASE}${path}`
  if (params) {
    const searchParams = new URLSearchParams()
    for (const [key, value] of Object.entries(params)) {
      if (value !== undefined) {
        searchParams.set(key, String(value))
      }
    }
    const qs = searchParams.toString()
    if (qs) url += `?${qs}`
  }

  let lastError: Error | null = null

  for (let attempt = 0; attempt <= MAX_RETRIES; attempt++) {
    try {
      const token = await getAccessToken()

      const response = await fetch(url, {
        method,
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        ...(body ? { body: JSON.stringify(body) } : {}),
      })

      // Rate limit: esperar y reintentar
      if (response.status === 429) {
        const retryAfter = response.headers.get('retry-after')
        const waitMs = retryAfter ? parseInt(retryAfter) * 1000 : RETRY_DELAY_MS * (attempt + 1)
        console.error(`[ml-mcp] Rate limited. Esperando ${waitMs}ms...`)
        await sleep(waitMs)
        continue
      }

      if (!response.ok) {
        const errorData = await response.json().catch(() => null) as MLError | null
        const errorMsg = errorData?.message || errorData?.error || `HTTP ${response.status}`
        const cause = errorData?.cause?.join(', ') || ''

        // Token expirado: limpiar cache y reintentar
        if (response.status === 401 && attempt < MAX_RETRIES) {
          const { clearTokenCache } = await import('./auth.js')
          clearTokenCache()
          continue
        }

        throw new Error(
          `Error API ML: ${errorMsg}${cause ? ` (${cause})` : ''} [${method} ${path}]`
        )
      }

      return await response.json() as T
    } catch (error) {
      lastError = error as Error
      if (attempt < MAX_RETRIES && isRetryable(error as Error)) {
        await sleep(RETRY_DELAY_MS * (attempt + 1))
        continue
      }
      throw error
    }
  }

  throw lastError || new Error('Error inesperado en mlFetch')
}

// Fetch múltiple con batching (ML soporta multi-get en /items)
export async function mlMultiGet<T>(ids: string[], path: string): Promise<T[]> {
  if (ids.length === 0) return []

  // ML permite hasta 20 items por multi-get
  const BATCH_SIZE = 20
  const results: T[] = []

  for (let i = 0; i < ids.length; i += BATCH_SIZE) {
    const batch = ids.slice(i, i + BATCH_SIZE)
    const data = await mlFetch<T[]>(path, {
      params: { ids: batch.join(',') },
    })
    results.push(...data)
  }

  return results
}

function isRetryable(error: Error): boolean {
  const msg = error.message.toLowerCase()
  return (
    msg.includes('fetch failed') ||
    msg.includes('network') ||
    msg.includes('econnreset') ||
    msg.includes('timeout')
  )
}

function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms))
}
