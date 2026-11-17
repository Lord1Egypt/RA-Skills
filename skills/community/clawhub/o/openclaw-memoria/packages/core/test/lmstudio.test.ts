/**
 * Provider LM Studio (mocké, zéro réseau réel).
 * Vérifie : détection /models (up, modèles, erreurs BRUYANTES), résolution du
 * modèle « auto » (premier chargé, mémorisé), complete (corps, en-tête de
 * convention, directive JSON), erreurs HTTP claires.
 */
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import {
  DEFAULT_LMSTUDIO_BASE_URL,
  LMSTUDIO_AUTO_MODEL,
  LmStudioProvider,
  lmstudioListModels,
} from '../src/index.js'

type FetchFn = (input: string | URL | Request, init?: RequestInit) => Promise<Response>

let fetchMock: ReturnType<typeof vi.fn<FetchFn>>
let warnSpy: ReturnType<typeof vi.spyOn>

function jsonResponse(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json' } })
}

/** Réponse /models au format OpenAI { data: [{id}] } — fraîche à chaque appel. */
function modelsResponse(ids: string[]): () => Promise<Response> {
  return async () => jsonResponse({ data: ids.map(id => ({ id })) })
}

beforeEach(() => {
  fetchMock = vi.fn<FetchFn>()
  vi.stubGlobal('fetch', fetchMock)
  warnSpy = vi.spyOn(console, 'warn').mockImplementation(() => {})
})

afterEach(() => {
  vi.unstubAllGlobals()
  vi.restoreAllMocks()
})

describe('lmstudioListModels', () => {
  it('GET {base}/models → up + liste des id', async () => {
    fetchMock.mockImplementation(modelsResponse(['qwen2.5-7b-instruct', 'llama-3.2-3b']))
    const r = await lmstudioListModels()
    expect(String(fetchMock.mock.calls[0]?.[0])).toBe(`${DEFAULT_LMSTUDIO_BASE_URL}/models`)
    expect(r).toEqual({ up: true, models: ['qwen2.5-7b-instruct', 'llama-3.2-3b'] })
  })

  it('réseau KO → up:false + warn (jamais muet)', async () => {
    fetchMock.mockRejectedValueOnce(new TypeError('fetch failed'))
    const r = await lmstudioListModels('http://127.0.0.1:9999/v1')
    expect(r.up).toBe(false)
    expect(warnSpy).toHaveBeenCalledWith(expect.stringContaining('lmstudio injoignable'))
  })

  it('HTTP 500 → up:false + warn', async () => {
    fetchMock.mockResolvedValueOnce(new Response('ko', { status: 500 }))
    const r = await lmstudioListModels()
    expect(r.up).toBe(false)
    expect(warnSpy).toHaveBeenCalledWith(expect.stringContaining('HTTP 500'))
  })
})

describe('LmStudioProvider', () => {
  it('mode auto : isAvailable true si ≥ 1 modèle chargé, false (warn) sinon', async () => {
    fetchMock.mockImplementation(modelsResponse(['qwen2.5-7b-instruct']))
    const p = new LmStudioProvider()
    expect(p.name).toBe('lmstudio')
    expect(p.model).toBe(LMSTUDIO_AUTO_MODEL)
    await expect(p.isAvailable()).resolves.toBe(true)

    fetchMock.mockImplementation(modelsResponse([]))
    await expect(new LmStudioProvider().isAvailable()).resolves.toBe(false)
    expect(warnSpy).toHaveBeenCalledWith(expect.stringContaining('aucun modèle chargé'))
  })

  it('modèle explicite : présent → true ; absent → false + warn nommant le modèle', async () => {
    fetchMock.mockImplementation(modelsResponse(['llama-3.2-3b']))
    await expect(new LmStudioProvider({ model: 'llama-3.2-3b' }).isAvailable()).resolves.toBe(true)
    await expect(new LmStudioProvider({ model: 'mistral-7b' }).isAvailable()).resolves.toBe(false)
    expect(warnSpy).toHaveBeenCalledWith(expect.stringContaining('mistral-7b'))
  })

  it('complete auto : résout le PREMIER modèle chargé puis le mémorise (1 seul /models)', async () => {
    const bodies: Array<Record<string, unknown>> = []
    fetchMock.mockImplementation(async (url: unknown, init?: RequestInit) => {
      if (String(url).endsWith('/models')) return jsonResponse({ data: [{ id: 'qwen2.5-7b-instruct' }] })
      bodies.push(JSON.parse(String(init?.body)) as Record<string, unknown>)
      return jsonResponse({ choices: [{ message: { content: '{"facts":[]}' } }] })
    })
    const p = new LmStudioProvider({ baseUrl: 'http://127.0.0.1:1234/v1/' })
    await p.complete({ prompt: 'extrais', maxTokens: 256, temperature: 0.1 })
    await p.complete({ prompt: 'encore' })

    const modelCalls = fetchMock.mock.calls.filter(c => String(c[0]).endsWith('/models'))
    expect(modelCalls).toHaveLength(1) // mémorisé après le 1er appel
    expect(bodies[0]?.['model']).toBe('qwen2.5-7b-instruct')
    expect(bodies[0]?.['max_tokens']).toBe(256)
    expect(bodies[0]?.['temperature']).toBe(0.1)
  })

  it('complete : en-tête Authorization de convention + directive JSON dans le system', async () => {
    let headers: Record<string, string> = {}
    let body: Record<string, unknown> = {}
    fetchMock.mockImplementation(async (url: unknown, init?: RequestInit) => {
      if (String(url).endsWith('/models')) return jsonResponse({ data: [{ id: 'm1' }] })
      headers = (init?.headers ?? {}) as Record<string, string>
      body = JSON.parse(String(init?.body)) as Record<string, unknown>
      return jsonResponse({ choices: [{ message: { content: 'ok' } }] })
    })
    await new LmStudioProvider().complete({ prompt: 'extrais les faits durables', json: true })
    expect(headers['Authorization']).toBe('Bearer lm-studio')
    // pas de response_format (rejeté par certaines versions) — directive system
    expect(body['response_format']).toBeUndefined()
    const messages = body['messages'] as Array<{ role: string; content: string }>
    expect(messages.some(m => m.role === 'system' && m.content.toLowerCase().includes('objet json'))).toBe(true)
  })

  it('complete modèle explicite : AUCUN appel /models', async () => {
    fetchMock.mockImplementation(async () => jsonResponse({ choices: [{ message: { content: 'ok' } }] }))
    await new LmStudioProvider({ model: 'mistral-7b' }).complete({ prompt: 'x' })
    expect(fetchMock.mock.calls.every(c => !String(c[0]).endsWith('/models'))).toBe(true)
  })

  it('complete : HTTP 400 → erreur claire avec le modèle ; serveur down en auto → erreur explicite', async () => {
    fetchMock.mockImplementation(async (url: unknown) => {
      if (String(url).endsWith('/models')) return jsonResponse({ data: [{ id: 'm1' }] })
      return new Response('bad request', { status: 400 })
    })
    await expect(new LmStudioProvider().complete({ prompt: 'x' })).rejects.toThrow(/HTTP 400.*m1/)

    fetchMock.mockRejectedValue(new TypeError('fetch failed'))
    await expect(new LmStudioProvider().complete({ prompt: 'x' })).rejects.toThrow(/lmstudio injoignable/)
  })

  it('complete : réponse sans choices[0].message.content → erreur explicite', async () => {
    fetchMock.mockImplementation(async (url: unknown) => {
      if (String(url).endsWith('/models')) return jsonResponse({ data: [{ id: 'm1' }] })
      return jsonResponse({ choices: [] })
    })
    await expect(new LmStudioProvider().complete({ prompt: 'x' })).rejects.toThrow(/content absent/)
  })
})
