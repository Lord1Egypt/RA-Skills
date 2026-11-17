/**
 * Tests du client daemon — environnement node, AUCUN réseau :
 * fetch / sessionStorage / location / history sont stubés.
 */
import { afterEach, describe, expect, it, vi } from 'vitest'
import {
  ApiError,
  adoptTokenFromHash,
  copyOpenClawKey,
  extractTokenFromHash,
  forgetFacts,
  getAgents,
  getLlmHealth,
  getOllamaPullStatus,
  getStats,
  pairAgent,
  searchFacts,
  startOllamaPull,
} from '../src/api'

const TOKEN_KEY = 'memoria.admin_token'

function stubBrowser(opts: { hash?: string; token?: string } = {}): {
  store: Map<string, string>
  replaceState: ReturnType<typeof vi.fn>
} {
  const store = new Map<string, string>()
  if (opts.token) store.set(TOKEN_KEY, opts.token)
  vi.stubGlobal('sessionStorage', {
    getItem: (k: string) => store.get(k) ?? null,
    setItem: (k: string, v: string) => void store.set(k, v),
    removeItem: (k: string) => void store.delete(k),
  })
  const replaceState = vi.fn()
  vi.stubGlobal('location', { hash: opts.hash ?? '', pathname: '/ui/', search: '' })
  vi.stubGlobal('history', { replaceState })
  return { store, replaceState }
}

function jsonResponse(payload: unknown, status = 200): Response {
  return new Response(JSON.stringify(payload), {
    status,
    headers: { 'content-type': 'application/json' },
  })
}

afterEach(() => {
  vi.unstubAllGlobals()
})

describe('extractTokenFromHash', () => {
  it('extrait et décode le token du fragment', () => {
    expect(extractTokenFromHash('#token=abc123')).toBe('abc123')
    expect(extractTokenFromHash('#token=a%20b&x=1')).toBe('a b')
  })

  it('retourne null sans token', () => {
    expect(extractTokenFromHash('')).toBeNull()
    expect(extractTokenFromHash('#foo=bar')).toBeNull()
    expect(extractTokenFromHash('#token=')).toBeNull()
  })
})

describe('adoptTokenFromHash', () => {
  it('range le token en sessionStorage et nettoie l’URL', () => {
    const { store, replaceState } = stubBrowser({ hash: '#token=secret-admin' })
    adoptTokenFromHash()
    expect(store.get(TOKEN_KEY)).toBe('secret-admin')
    expect(replaceState).toHaveBeenCalledWith(null, '', '/ui/')
  })

  it('ne touche à rien sans token dans le hash', () => {
    const { store, replaceState } = stubBrowser({ hash: '#autre=chose' })
    adoptTokenFromHash()
    expect(store.has(TOKEN_KEY)).toBe(false)
    expect(replaceState).not.toHaveBeenCalled()
  })
})

describe('requêtes authentifiées', () => {
  it('envoie le header Bearer et déballe la réponse (GET /v1/admin/agents)', async () => {
    stubBrowser({ token: 'tok-admin' })
    const agents = [{ instance: { id: 'i1' }, assistant_type: 'codex', db_path: null }]
    const fetchMock = vi.fn(async () => jsonResponse({ agents }))
    vi.stubGlobal('fetch', fetchMock)

    const result = await getAgents()

    expect(result).toEqual(agents)
    expect(fetchMock).toHaveBeenCalledTimes(1)
    const [url, init] = fetchMock.mock.calls[0] as unknown as [string, RequestInit]
    expect(url).toBe('/v1/admin/agents')
    expect((init.headers as Record<string, string>)['authorization']).toBe('Bearer tok-admin')
  })

  it('refuse AVANT tout appel réseau quand il n’y a pas de token', async () => {
    stubBrowser() // pas de token
    const fetchMock = vi.fn()
    vi.stubGlobal('fetch', fetchMock)

    await expect(getStats()).rejects.toMatchObject({ status: 401 })
    expect(fetchMock).not.toHaveBeenCalled()
  })

  it('propage les erreurs du daemon en ApiError (status + message)', async () => {
    stubBrowser({ token: 'tok-admin' })
    vi.stubGlobal('fetch', vi.fn(async () => jsonResponse({ error: 'token admin requis' }, 401)))

    const err = await getStats().then(
      () => null,
      (e: unknown) => e,
    )
    expect(err).toBeInstanceOf(ApiError)
    expect((err as ApiError).status).toBe(401)
    expect((err as ApiError).message).toBe('token admin requis')
  })

  it('survit à une réponse d’erreur non-JSON (message HTTP par défaut)', async () => {
    stubBrowser({ token: 'tok-admin' })
    const warn = vi.spyOn(console, 'warn').mockImplementation(() => undefined)
    vi.stubGlobal('fetch', vi.fn(async () => new Response('boom', { status: 500 })))

    await expect(getStats()).rejects.toMatchObject({ status: 500, message: 'Le service a répondu HTTP 500.' })
    expect(warn).toHaveBeenCalled() // l'avalement du JSON cassé est loggé, pas muet
    warn.mockRestore()
  })

  it('pairAgent poste le type et retourne code + commande', async () => {
    stubBrowser({ token: 'tok-admin' })
    const result = {
      assistant_id: 'a1',
      assistant_instance_id: 'i1',
      pairing_code: 'ABC123',
      command: 'npx -y @memoria/mcp connect --code ABC123',
    }
    const fetchMock = vi.fn(async () => jsonResponse(result))
    vi.stubGlobal('fetch', fetchMock)

    await expect(pairAgent('claude-code')).resolves.toEqual(result)
    const [url, init] = fetchMock.mock.calls[0] as unknown as [string, RequestInit]
    expect(url).toBe('/v1/admin/pair')
    expect(init.method).toBe('POST')
    expect(JSON.parse(init.body as string)).toEqual({ type: 'claude-code' })
  })

  it('searchFacts encode instance et requête dans l’URL', async () => {
    stubBrowser({ token: 'tok-admin' })
    const fetchMock = vi.fn(async () => jsonResponse({ facts: [] }))
    vi.stubGlobal('fetch', fetchMock)

    await expect(searchFacts('inst-1', 'café & code')).resolves.toEqual([])
    const [url] = fetchMock.mock.calls[0] as unknown as [string]
    expect(url).toBe('/v1/admin/facts?instance=inst-1&q=caf%C3%A9+%26+code')
  })

  it('forgetFacts poste les ids et retourne le compte supprimé', async () => {
    stubBrowser({ token: 'tok-admin' })
    const fetchMock = vi.fn(async () => jsonResponse({ deleted: 2 }))
    vi.stubGlobal('fetch', fetchMock)

    await expect(forgetFacts(['f1', 'f2'])).resolves.toBe(2)
    const [url, init] = fetchMock.mock.calls[0] as unknown as [string, RequestInit]
    expect(url).toBe('/v1/admin/forget')
    expect(JSON.parse(init.body as string)).toEqual({ ids: ['f1', 'f2'] })
  })

  it('forgetFacts sans ids ne fait AUCUN appel (garde anti-suppression massive)', async () => {
    stubBrowser({ token: 'tok-admin' })
    const fetchMock = vi.fn()
    vi.stubGlobal('fetch', fetchMock)

    await expect(forgetFacts([])).resolves.toBe(0)
    expect(fetchMock).not.toHaveBeenCalled()
  })
})

describe('santé LLM (anti-mort-silencieuse)', () => {
  it('getLlmHealth lit GET /v1/admin/llm_health tel quel', async () => {
    stubBrowser({ token: 'tok-admin' })
    const health = {
      extraction: { provider: 'ollama', model: 'qwen2.5:3b', available: false, reason: 'serveur Ollama injoignable' },
      embeddings: { provider: 'ollama', model: 'nomic-embed-text', available: false, reason: 'nécessite Ollama' },
      wal_pending: 7,
      options: { ollama: { kind: 'ollama', available: false } },
    }
    const fetchMock = vi.fn(async () => jsonResponse(health))
    vi.stubGlobal('fetch', fetchMock)

    await expect(getLlmHealth()).resolves.toEqual(health)
    const [url] = fetchMock.mock.calls[0] as unknown as [string]
    expect(url).toBe('/v1/admin/llm_health')
  })

  it('startOllamaPull poste le modèle ; getOllamaPullStatus lit la progression', async () => {
    stubBrowser({ token: 'tok-admin' })
    const fetchMock = vi.fn(async () => jsonResponse({ ok: true, model: 'nomic-embed-text' }))
    vi.stubGlobal('fetch', fetchMock)

    await startOllamaPull('nomic-embed-text')
    const [url, init] = fetchMock.mock.calls[0] as unknown as [string, RequestInit]
    expect(url).toBe('/v1/admin/ollama_pull')
    expect(JSON.parse(init.body as string)).toEqual({ model: 'nomic-embed-text' })

    const status = { running: true, model: 'nomic-embed-text', percent: 42, status: 'pulling abc', error: null }
    vi.stubGlobal('fetch', vi.fn(async () => jsonResponse(status)))
    await expect(getOllamaPullStatus()).resolves.toEqual(status)
  })

  it('startOllamaPull propage le 409 « déjà en cours » en ApiError', async () => {
    stubBrowser({ token: 'tok-admin' })
    vi.stubGlobal('fetch', vi.fn(async () => jsonResponse({ error: 'un téléchargement est déjà en cours (qwen2.5:3b)' }, 409)))
    await expect(startOllamaPull('autre')).rejects.toMatchObject({ status: 409 })
  })

  it('copyOpenClawKey poste le provider et retourne le fichier écrit', async () => {
    stubBrowser({ token: 'tok-admin' })
    const fetchMock = vi.fn(async () => jsonResponse({ ok: true, provider: 'openrouter', key_file: '/home/x/.openrouter/api_key' }))
    vi.stubGlobal('fetch', fetchMock)

    const r = await copyOpenClawKey('openrouter')
    expect(r.key_file).toBe('/home/x/.openrouter/api_key')
    const [url, init] = fetchMock.mock.calls[0] as unknown as [string, RequestInit]
    expect(url).toBe('/v1/admin/openclaw_copy_key')
    expect(JSON.parse(init.body as string)).toEqual({ provider: 'openrouter' })
  })
})
