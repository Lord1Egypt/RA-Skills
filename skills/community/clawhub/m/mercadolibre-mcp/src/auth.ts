// OAuth2 para Mercado Libre — soporta 2 modos:
// 1. Token directo (ML_ACCESS_TOKEN) — refresheado externamente por n8n/cron
// 2. Auto-refresh (ML_CLIENT_ID + ML_CLIENT_SECRET + ML_REFRESH_TOKEN) — refresh interno cada 6h

import type { MLConfig, TokenData } from './types.js'

const ML_AUTH_URL = 'https://api.mercadolibre.com/oauth/token'

let cachedToken: TokenData | null = null

export function getConfig(): MLConfig {
  const clientId = process.env.ML_CLIENT_ID || ''
  const clientSecret = process.env.ML_CLIENT_SECRET || ''
  const refreshToken = process.env.ML_REFRESH_TOKEN || ''
  const siteId = process.env.ML_SITE_ID || 'MLA'

  return { clientId, clientSecret, refreshToken, siteId }
}

export async function getAccessToken(): Promise<string> {
  // Modo 1: Token directo (gestionado externamente por n8n, cron, etc.)
  const directToken = process.env.ML_ACCESS_TOKEN
  if (directToken) {
    return directToken
  }

  // Modo 2: Auto-refresh con OAuth2
  // Si el token está cacheado y no expiró (con 5 min de margen), reusar
  if (cachedToken && cachedToken.expiresAt > Date.now() + 5 * 60 * 1000) {
    return cachedToken.accessToken
  }

  const config = getConfig()

  if (!config.clientId || !config.clientSecret || !config.refreshToken) {
    throw new Error(
      'Configurá ML_ACCESS_TOKEN (token directo) o ML_CLIENT_ID + ML_CLIENT_SECRET + ML_REFRESH_TOKEN (auto-refresh). ' +
      'Si usás n8n para renovar el token, configurá ML_ACCESS_TOKEN.'
    )
  }

  const response = await fetch(ML_AUTH_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      grant_type: 'refresh_token',
      client_id: config.clientId,
      client_secret: config.clientSecret,
      refresh_token: config.refreshToken,
    }),
  })

  if (!response.ok) {
    const errorText = await response.text()
    throw new Error(
      `Error renovando token ML (${response.status}): ${errorText}. ` +
      'Verificá que ML_CLIENT_ID, ML_CLIENT_SECRET y ML_REFRESH_TOKEN sean correctos.'
    )
  }

  const data = await response.json() as {
    access_token: string
    expires_in: number
    refresh_token: string
  }

  cachedToken = {
    accessToken: data.access_token,
    expiresAt: Date.now() + data.expires_in * 1000,
  }

  // Actualizar el refresh_token si ML devuelve uno nuevo
  if (data.refresh_token && data.refresh_token !== config.refreshToken) {
    process.env.ML_REFRESH_TOKEN = data.refresh_token
    console.error(
      `[ml-mcp] Refresh token actualizado. Nuevo: ${data.refresh_token.substring(0, 20)}...`
    )
  }

  return cachedToken.accessToken
}

// Para tests o reset manual
export function clearTokenCache(): void {
  cachedToken = null
}
