/**
 * Provider OpenAI + OpenRouter (mocké, zéro réseau réel).
 * Vérifie : résolution de clé (param/env/fichier), max_tokens vs
 * max_completion_tokens (modèles gpt-5 et o-series), directive json, base URL
 * et en-têtes OpenRouter, erreurs claires.
 */
import { mkdtempSync, rmSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { OpenAiProvider, resolveOpenAiApiKey } from '../src/index.js'

let dir: string

beforeEach(() => {
  dir = mkdtempSync(join(tmpdir(), 'memoria-openai-'))
})
afterEach(() => {
  vi.unstubAllGlobals()
  rmSync(dir, { recursive: true, force: true })
})

function mockChat(capture: (body: Record<string, unknown>, url: string, headers: Record<string, string>) => void) {
  vi.stubGlobal('fetch', vi.fn(async (url: unknown, init?: { body?: string; headers?: Record<string, string> }) => {
    capture(JSON.parse(init?.body ?? '{}'), String(url), init?.headers ?? {})
    return new Response(JSON.stringify({ choices: [{ message: { content: '{"facts":[]}' } }] }), { status: 200 })
  }))
}

describe('resolveOpenAiApiKey', () => {
  it('param > env > fichier, par flavor', () => {
    expect(resolveOpenAiApiKey({ apiKey: 'sk-param' })).toBe('sk-param')
    expect(resolveOpenAiApiKey({ env: { OPENAI_API_KEY: 'sk-env' } as never, flavor: 'openai' })).toBe('sk-env')
    expect(resolveOpenAiApiKey({ env: { OPENROUTER_API_KEY: 'or-env' } as never, flavor: 'openrouter' })).toBe('or-env')

    const f = join(dir, 'key')
    writeFileSync(f, 'sk-file\n')
    expect(resolveOpenAiApiKey({ keyFilePath: f, env: {} as never })).toBe('sk-file')
    expect(resolveOpenAiApiKey({ keyFilePath: join(dir, 'absent'), env: {} as never })).toBeNull()
  })
})

describe('OpenAiProvider', () => {
  it('gpt-4o-mini → max_tokens + temperature', async () => {
    let body: Record<string, unknown> = {}
    mockChat(b => { body = b })
    const p = new OpenAiProvider({ apiKey: 'sk-x', model: 'gpt-4o-mini' })
    await p.complete({ prompt: 'extrais du json', maxTokens: 256, temperature: 0.1, json: true })
    expect(body['max_tokens']).toBe(256)
    expect(body['temperature']).toBe(0.1)
    expect(body['response_format']).toEqual({ type: 'json_object' })
  })

  it('gpt-5-mini → max_completion_tokens, pas de temperature', async () => {
    let body: Record<string, unknown> = {}
    mockChat(b => { body = b })
    const p = new OpenAiProvider({ apiKey: 'sk-x', model: 'gpt-5-mini' })
    await p.complete({ prompt: 'json please', maxTokens: 256, temperature: 0.1, json: true })
    expect(body['max_completion_tokens']).toBe(256)
    expect(body['max_tokens']).toBeUndefined()
    expect(body['temperature']).toBeUndefined()
  })

  it('mode json sans « json » dans le prompt → directive ajoutée au system', async () => {
    let body: Record<string, unknown> = {}
    mockChat(b => { body = b })
    const p = new OpenAiProvider({ apiKey: 'sk-x', model: 'gpt-4o-mini' })
    await p.complete({ prompt: 'extrais les faits durables', json: true })
    const messages = body['messages'] as Array<{ role: string; content: string }>
    expect(messages.some(m => m.role === 'system' && m.content.toLowerCase().includes('json'))).toBe(true)
  })

  it('OpenRouter : base URL + en-têtes d’attribution', async () => {
    let url = ''
    let headers: Record<string, string> = {}
    mockChat((_b, u, h) => { url = u; headers = h })
    const p = new OpenAiProvider({ apiKey: 'or-x', flavor: 'openrouter', model: 'openai/gpt-4o-mini' })
    expect(p.name).toBe('openrouter')
    await p.complete({ prompt: 'hi' })
    expect(url).toBe('https://openrouter.ai/api/v1/chat/completions')
    expect(headers['X-Title']).toBe('Memoria')
    expect(headers['Authorization']).toBe('Bearer or-x')
  })

  it('sans clé → isAvailable false + complete throw clair', async () => {
    const p = new OpenAiProvider({ env: {} as never, keyFilePath: join(dir, 'none') })
    expect(await p.isAvailable()).toBe(false)
    await expect(p.complete({ prompt: 'x' })).rejects.toThrow(/aucune clé/)
  })

  it('HTTP 400 → erreur explicite avec modèle', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => new Response('{"error":{"message":"bad"}}', { status: 400 })))
    const p = new OpenAiProvider({ apiKey: 'sk-x', model: 'gpt-4o-mini' })
    await expect(p.complete({ prompt: 'x' })).rejects.toThrow(/HTTP 400.*gpt-4o-mini/)
  })
})
