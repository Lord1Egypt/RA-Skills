/**
 * Routes santé LLM + téléchargement Ollama du daemon, de bout en bout par
 * HTTP : un FAUX serveur Ollama local (node:http) rend les tests
 * déterministes quel que soit l'environnement (vrai Ollama installé ou non).
 */
import { createServer, type Server } from 'node:http'
import { mkdtempSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { afterEach, beforeEach, describe, expect, it } from 'vitest'
import { startDaemon, type RunningDaemon } from '../src/index.js'

let root: string
let daemon: RunningDaemon
let fakeOllama: Server
let fakeOllamaUrl: string

/** Faux Ollama : /api/tags (modèles complets) + /api/pull (NDJSON court). */
function startFakeOllama(): Promise<{ server: Server; url: string }> {
  const server = createServer((req, res) => {
    if (req.method === 'GET' && req.url === '/api/tags') {
      res.writeHead(200, { 'content-type': 'application/json' })
      res.end(JSON.stringify({ models: [{ name: 'qwen2.5:3b' }, { name: 'nomic-embed-text:latest' }] }))
      return
    }
    if (req.method === 'POST' && req.url === '/api/pull') {
      res.writeHead(200, { 'content-type': 'application/x-ndjson' })
      res.write(`${JSON.stringify({ status: 'pulling manifest' })}\n`)
      res.write(`${JSON.stringify({ status: 'pulling abc', total: 100, completed: 50 })}\n`)
      res.write(`${JSON.stringify({ status: 'success' })}\n`)
      res.end()
      return
    }
    res.writeHead(404).end()
  })
  return new Promise(resolve => {
    server.listen(0, '127.0.0.1', () => {
      const addr = server.address()
      const port = addr && typeof addr === 'object' ? addr.port : 0
      resolve({ server, url: `http://127.0.0.1:${port}` })
    })
  })
}

async function admin(method: 'GET' | 'POST', path: string, body?: unknown): Promise<Response> {
  return fetch(`http://127.0.0.1:${daemon.state.port}${path}`, {
    method,
    headers: {
      authorization: `Bearer ${daemon.state.admin_token}`,
      ...(body !== undefined ? { 'content-type': 'application/json' } : {}),
    },
    ...(body !== undefined ? { body: JSON.stringify(body) } : {}),
  })
}

beforeEach(async () => {
  root = mkdtempSync(join(tmpdir(), 'memoria-llmhealth-'))
  const fake = await startFakeOllama()
  fakeOllama = fake.server
  fakeOllamaUrl = fake.url
  daemon = await startDaemon({ storageRoot: root, configPath: join(root, 'config.toml'), ollamaBaseUrl: fakeOllamaUrl })
})

afterEach(async () => {
  await daemon.close()
  await new Promise<void>(r => fakeOllama.close(() => r()))
  rmSync(root, { recursive: true, force: true })
})

describe('GET /v1/admin/llm_health', () => {
  it('sans token → 401 ; avec token → bilan complet (extraction, embeddings, wal_pending, options)', async () => {
    const anonymous = await fetch(`http://127.0.0.1:${daemon.state.port}/v1/admin/llm_health`)
    expect(anonymous.status).toBe(401)

    const res = await admin('GET', '/v1/admin/llm_health')
    expect(res.status).toBe(200)
    const health = (await res.json()) as {
      extraction: { provider: string; model: string; available: boolean }
      embeddings: { provider: string; model: string; available: boolean }
      wal_pending: number
      options: Record<string, { kind: string }>
    }
    // le faux Ollama liste les deux modèles requis → moteur prêt
    expect(health.extraction).toMatchObject({ provider: 'ollama', model: 'qwen2.5:3b', available: true })
    expect(health.embeddings).toMatchObject({ provider: 'ollama', model: 'nomic-embed-text', available: true })
    expect(health.wal_pending).toBe(0)
    for (const kind of ['ollama', 'lmstudio', 'openai', 'anthropic', 'openrouter', 'openclaw']) {
      expect(health.options[kind]?.kind).toBe(kind)
    }
  })
})

describe('POST /v1/admin/ollama_pull + status', () => {
  it('flux complet : démarrage → progression → terminé (polling status)', async () => {
    const started = await admin('POST', '/v1/admin/ollama_pull', { model: 'nomic-embed-text' })
    expect(started.status).toBe(200)
    expect(await started.json()).toEqual({ ok: true, model: 'nomic-embed-text' })

    // polling jusqu'à la fin du job (le faux pull est instantané)
    const deadline = Date.now() + 3000
    let status: { running: boolean; percent: number | null; status: string | null; error: string | null } | null = null
    for (;;) {
      const res = await admin('GET', '/v1/admin/ollama_pull_status')
      expect(res.status).toBe(200)
      status = (await res.json()) as typeof status
      if (status && !status.running) break
      if (Date.now() > deadline) throw new Error('le job ollama_pull ne se termine pas')
      await new Promise(r => setTimeout(r, 20))
    }
    expect(status).toMatchObject({ running: false, percent: 100, status: 'terminé', error: null })
  })

  it('model manquant → 400 explicite', async () => {
    const res = await admin('POST', '/v1/admin/ollama_pull', {})
    expect(res.status).toBe(400)
    expect(((await res.json()) as { error: string }).error).toContain('model requis')
  })
})

describe('POST /v1/admin/llm_extraction (lmstudio accepté)', () => {
  it('provider lmstudio + modèle persistés, relus par llm_profile', async () => {
    const res = await admin('POST', '/v1/admin/llm_extraction', { provider: 'lmstudio', model: 'qwen2.5-7b-instruct' })
    expect(res.status).toBe(200)

    const profile = await admin('GET', '/v1/admin/llm_profile')
    const config = (await profile.json()) as { extraction?: { provider?: string; model?: string } }
    expect(config.extraction).toMatchObject({ provider: 'lmstudio', model: 'qwen2.5-7b-instruct' })
  })

  it('provider farfelu → 400', async () => {
    const res = await admin('POST', '/v1/admin/llm_extraction', { provider: 'gpt-5.4-nano' })
    expect(res.status).toBe(400)
  })
})

describe('POST /v1/admin/openclaw_copy_key', () => {
  it('provider invalide → 400 (la copie réelle est testée côté core)', async () => {
    const res = await admin('POST', '/v1/admin/openclaw_copy_key', { provider: 'pas-un-provider' })
    expect(res.status).toBe(400)
  })
})
