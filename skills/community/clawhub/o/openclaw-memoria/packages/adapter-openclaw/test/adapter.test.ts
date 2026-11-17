/**
 * Contrat de l'adaptateur OpenClaw : on mocke l'API de hooks et `fetch`, et on
 * vérifie le mapping hooks → daemon SANS vrai OpenClaw ni vrai daemon.
 */
import { afterEach, describe, expect, it, vi } from 'vitest'
import {
  formatRecall,
  partsToText,
  queryFromEvent,
  register,
  resolveBaseUrl,
  toMemoriaMessages,
  type OpenClawPluginApi,
} from '../src/index.js'

/** Faux api.on : mémorise les handlers par nom de hook. */
function fakeApi(config: Record<string, unknown>): {
  api: OpenClawPluginApi
  handlers: Map<string, (event: unknown, ctx?: unknown) => unknown>
  warnings: string[]
} {
  const handlers = new Map<string, (event: unknown, ctx?: unknown) => unknown>()
  const warnings: string[] = []
  const api: OpenClawPluginApi = {
    pluginConfig: config,
    logger: { warn: m => warnings.push(m), info: () => {}, debug: () => {} },
    on: (hook, handler) => handlers.set(hook, handler as (event: unknown, ctx?: unknown) => unknown),
  }
  return { api, handlers, warnings }
}

afterEach(() => vi.unstubAllGlobals())

describe('helpers purs', () => {
  it('partsToText gère string, tableau de parts, objet {text}', () => {
    expect(partsToText('bonjour')).toBe('bonjour')
    expect(partsToText([{ text: 'a' }, { text: 'b' }])).toBe('ab')
    expect(partsToText([{ type: 'text', text: 'x' }, 'y'])).toBe('xy')
    expect(partsToText({ text: 'z' })).toBe('z')
    expect(partsToText(null)).toBe('')
  })

  it('toMemoriaMessages filtre le vide et normalise le rôle', () => {
    const out = toMemoriaMessages([
      { role: 'user', content: 'salut' },
      { role: 'assistant', content: [{ text: 'oui ' }, { text: 'voilà' }] },
      { role: 'user', content: '   ' }, // ignoré (vide)
      { content: 'sans rôle' }, // rôle par défaut
      'pas un objet',
    ])
    expect(out).toEqual([
      { role: 'user', content: 'salut' },
      { role: 'assistant', content: 'oui voilà' },
      { role: 'assistant', content: 'sans rôle' },
    ])
  })

  it('queryFromEvent : prompt texte > dernier message user', () => {
    expect(queryFromEvent({ prompt: 'ma question' })).toBe('ma question')
    expect(
      queryFromEvent({
        messages: [
          { role: 'user', content: 'première' },
          { role: 'assistant', content: 'réponse' },
          { role: 'user', content: 'dernière question' },
        ],
      }),
    ).toBe('dernière question')
    expect(queryFromEvent({})).toBe('')
  })

  it('formatRecall produit un bloc Markdown, vide si aucun item', () => {
    expect(formatRecall([])).toBe('')
    const block = formatRecall([
      { kind: 'fact', content: 'Néto préfère le local-first', category: 'preference', score: 1 },
      { kind: 'procedure', content: 'Déployer via Hello-Primo', category: 'howto', score: 0.8 },
    ])
    expect(block).toContain('🧠 Mémoire pertinente (Memoria)')
    expect(block).toContain('Néto préfère le local-first')
    expect(block).toContain('⚙️ Déployer via Hello-Primo')
  })

  it('resolveBaseUrl : daemonUrl explicite gagne et est nettoyé', () => {
    expect(resolveBaseUrl({ daemonUrl: 'http://127.0.0.1:7077/' })).toBe('http://127.0.0.1:7077')
    expect(resolveBaseUrl({ daemonUrl: undefined, storageRoot: '/tmp/inexistant-memoria-xyz' })).toBeNull()
  })
})

describe('register → hooks → daemon', () => {
  const baseConfig = { daemonUrl: 'http://127.0.0.1:9999', token: 'tok-instance', instance: 'koda' }

  it('refuse de s’enregistrer sans token (mémoire désactivée, pas de hooks)', () => {
    const { api, handlers, warnings } = fakeApi({ daemonUrl: 'http://x', instance: 'koda' })
    register(api)
    expect(handlers.size).toBe(0)
    expect(warnings.join(' ')).toMatch(/token/i)
  })

  it('before_prompt_build appelle /recall et renvoie prependContext', async () => {
    const fetchMock = vi.fn(async () =>
      new Response(JSON.stringify({ items: [{ kind: 'fact', content: 'Koda bosse pour Néto', category: 'identity', score: 1 }] }), {
        status: 200,
        headers: { 'content-type': 'application/json' },
      }),
    )
    vi.stubGlobal('fetch', fetchMock)
    const { api, handlers } = fakeApi(baseConfig)
    register(api)

    const recall = handlers.get('before_prompt_build')!
    const result = (await recall({ prompt: 'qui est Néto ?' })) as { prependContext?: string } | undefined

    expect(fetchMock).toHaveBeenCalledTimes(1)
    const [url, init] = fetchMock.mock.calls[0]!
    expect(url).toBe('http://127.0.0.1:9999/v1/memory/recall')
    expect((init as RequestInit).method).toBe('POST')
    expect((init as RequestInit).headers).toMatchObject({ authorization: 'Bearer tok-instance' })
    expect(JSON.parse((init as RequestInit).body as string)).toMatchObject({ query: 'qui est Néto ?', limit: 12 })
    expect(result?.prependContext).toContain('Koda bosse pour Néto')
  })

  it('recall : Memoria en pause (disabled) → aucune injection', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => new Response(JSON.stringify({ items: [], disabled: true }), { status: 200 })))
    const { api, handlers } = fakeApi(baseConfig)
    register(api)
    const result = await handlers.get('before_prompt_build')!({ prompt: 'x' })
    expect(result).toBeUndefined()
  })

  it('recall : daemon injoignable (pas de daemonUrl, pas de daemon.json) → pas de throw, pas d’injection', async () => {
    const { api, handlers } = fakeApi({ token: 'tok', instance: 'koda', storageRoot: '/tmp/inexistant-memoria-xyz' })
    register(api)
    const result = await handlers.get('before_prompt_build')!({ prompt: 'x' })
    expect(result).toBeUndefined()
  })

  it('agent_end poste les messages vers /capture_turn', async () => {
    const fetchMock = vi.fn(async () => new Response(JSON.stringify({ appended: 2 }), { status: 200 }))
    vi.stubGlobal('fetch', fetchMock)
    const { api, handlers } = fakeApi(baseConfig)
    register(api)

    await handlers.get('agent_end')!({
      success: true,
      messages: [
        { role: 'user', content: 'salut' },
        { role: 'assistant', content: 'bonjour Néto' },
      ],
    })
    expect(fetchMock).toHaveBeenCalledTimes(1)
    const [url, init] = fetchMock.mock.calls[0]!
    expect(url).toBe('http://127.0.0.1:9999/v1/memory/capture_turn')
    expect(JSON.parse((init as RequestInit).body as string).messages).toEqual([
      { role: 'user', content: 'salut' },
      { role: 'assistant', content: 'bonjour Néto' },
    ])
  })

  it('agent_end sans message ne fait aucun appel', async () => {
    const fetchMock = vi.fn(async () => new Response('{}', { status: 200 }))
    vi.stubGlobal('fetch', fetchMock)
    const { api, handlers } = fakeApi(baseConfig)
    register(api)
    await handlers.get('agent_end')!({ success: true, messages: [] })
    expect(fetchMock).not.toHaveBeenCalled()
  })

  it('autoCapture:false → pas de hook agent_end ; autoRecall:false → pas de before_prompt_build', () => {
    const { api, handlers } = fakeApi({ ...baseConfig, autoCapture: false, autoRecall: false })
    register(api)
    expect(handlers.has('agent_end')).toBe(false)
    expect(handlers.has('before_prompt_build')).toBe(false)
  })
})
