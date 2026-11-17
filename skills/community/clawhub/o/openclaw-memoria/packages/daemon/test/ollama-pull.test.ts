/**
 * Machine à états du job « ollama pull » (fetch 100 % mocké, zéro réseau) :
 * idle → running (progression NDJSON) → terminé | erreur. Un seul job à la
 * fois, échec TOUJOURS visible dans le statut (anti-mort-silencieuse).
 */
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { OllamaPullJob } from '../src/ollama-pull.js'

let warnSpy: ReturnType<typeof vi.spyOn>

/** Réponse streaming NDJSON contrôlée à la main (releaser par étapes). */
function ndjsonStream(): { response: Response; push: (line: object) => void; end: () => void } {
  let controller!: ReadableStreamDefaultController<Uint8Array>
  const stream = new ReadableStream<Uint8Array>({ start: c => void (controller = c) })
  const encoder = new TextEncoder()
  return {
    response: new Response(stream, { status: 200 }),
    push: line => controller.enqueue(encoder.encode(`${JSON.stringify(line)}\n`)),
    end: () => controller.close(),
  }
}

/** Attend que le prédicat passe (polling 5 ms, timeout 2 s). */
async function waitFor(predicate: () => boolean): Promise<void> {
  const deadline = Date.now() + 2000
  while (!predicate()) {
    if (Date.now() > deadline) throw new Error('waitFor : délai dépassé')
    await new Promise(r => setTimeout(r, 5))
  }
}

beforeEach(() => {
  warnSpy = vi.spyOn(console, 'warn').mockImplementation(() => {})
  vi.spyOn(console, 'log').mockImplementation(() => {})
})

afterEach(() => {
  vi.unstubAllGlobals()
  vi.restoreAllMocks()
})

describe('OllamaPullJob', () => {
  it('progression NDJSON → percent/status, puis succès (running:false, 100 %)', async () => {
    const { response, push, end } = ndjsonStream()
    vi.stubGlobal('fetch', vi.fn(async (url: unknown, init?: RequestInit) => {
      expect(String(url)).toBe('http://127.0.0.1:11434/api/pull')
      expect(JSON.parse(String(init?.body))).toEqual({ name: 'nomic-embed-text', stream: true })
      return response
    }))

    const job = new OllamaPullJob()
    expect(job.status()).toEqual({ running: false, model: null, percent: null, status: null, error: null })

    job.start('nomic-embed-text')
    expect(job.status().running).toBe(true)
    expect(job.status().model).toBe('nomic-embed-text')

    push({ status: 'pulling manifest' })
    await waitFor(() => job.status().status === 'pulling manifest')

    push({ status: 'pulling abc', total: 1000, completed: 250 })
    await waitFor(() => job.status().percent === 25)

    push({ status: 'success' })
    end()
    await waitFor(() => !job.status().running)
    expect(job.status()).toMatchObject({ running: false, percent: 100, status: 'terminé', error: null })
  })

  it('erreur DANS le stream ({"error":...}) → état erreur explicite + warn', async () => {
    const { response, push, end } = ndjsonStream()
    vi.stubGlobal('fetch', vi.fn(async () => response))
    const job = new OllamaPullJob()
    job.start('modele-inexistant')
    push({ error: 'pull model manifest: file does not exist' })
    end()
    await waitFor(() => !job.status().running)
    expect(job.status().status).toBe('erreur')
    expect(job.status().error).toContain('file does not exist')
    expect(warnSpy).toHaveBeenCalledWith(expect.stringContaining('en échec'))
  })

  it('HTTP 500 / réseau KO → état erreur, jamais une fin muette', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => new Response('boom', { status: 500 })))
    const job = new OllamaPullJob()
    job.start('m')
    await waitFor(() => !job.status().running)
    expect(job.status().error).toContain('HTTP 500')

    vi.stubGlobal('fetch', vi.fn(async () => { throw new TypeError('fetch failed') }))
    const job2 = new OllamaPullJob()
    job2.start('m')
    await waitFor(() => !job2.status().running)
    expect(job2.status().error).toContain('fetch failed')
  })

  it('un SEUL job à la fois : start pendant running → throw explicite', async () => {
    const { response, push, end } = ndjsonStream()
    vi.stubGlobal('fetch', vi.fn(async () => response))
    const job = new OllamaPullJob()
    job.start('qwen2.5:3b')
    expect(() => job.start('autre')).toThrow(/déjà en cours/)
    push({ status: 'success' })
    end()
    await waitFor(() => !job.status().running)
    // une fois fini, on peut relancer
    vi.stubGlobal('fetch', vi.fn(async () => new Response('ko', { status: 500 })))
    expect(() => job.start('autre')).not.toThrow()
    await waitFor(() => !job.status().running)
  })
})
