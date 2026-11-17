/**
 * detectLlmOptions + scan/copie des clés OpenClaw + santé LLM (llmHealth).
 * Tout est injecté : fetch mocké, fichiers de clés tmp, faux ~/.openclaw
 * (JSON legacy + store SQLite), vérificateur de binaire. AUCUNE valeur de clé
 * ne doit sortir de detectLlmOptions.
 */
import { mkdirSync, mkdtempSync, rmSync, statSync, readFileSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import DatabaseCtor from 'better-sqlite3'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import {
  Memoria,
  copyOpenClawKey,
  detectLlmOptions,
  scanOpenClawCredentials,
} from '../src/index.js'

type FetchFn = (input: string | URL | Request, init?: RequestInit) => Promise<Response>

let fetchMock: ReturnType<typeof vi.fn<FetchFn>>
let warnSpy: ReturnType<typeof vi.spyOn>
let tmp: string

function jsonResponse(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json' } })
}

/** fetch simulant Ollama (tags) + LM Studio (models) selon l'URL. */
function stubServers(opts: { ollamaModels?: string[] | null; lmModels?: string[] | null }): void {
  fetchMock.mockImplementation(async (url: unknown) => {
    const u = String(url)
    if (u.includes('/api/tags')) {
      if (opts.ollamaModels === null || opts.ollamaModels === undefined) throw new TypeError('fetch failed')
      return jsonResponse({ models: opts.ollamaModels.map(name => ({ name })) })
    }
    if (u.endsWith('/models')) {
      if (opts.lmModels === null || opts.lmModels === undefined) throw new TypeError('fetch failed')
      return jsonResponse({ data: opts.lmModels.map(id => ({ id })) })
    }
    throw new Error(`URL inattendue dans le test : ${u}`)
  })
}

/** Faux ~/.openclaw : agents/main/agent/auth-profiles.json + state sqlite. */
function makeOpenClawDir(opts: {
  profiles?: Record<string, unknown>
  flatAuth?: Record<string, unknown>
  sqliteStore?: Record<string, unknown>
} = {}): string {
  const dir = join(tmp, '.openclaw')
  const agentDir = join(dir, 'agents', 'main', 'agent')
  mkdirSync(agentDir, { recursive: true })
  if (opts.profiles) {
    writeFileSync(join(agentDir, 'auth-profiles.json'), JSON.stringify({ version: 1, profiles: opts.profiles }), 'utf8')
  }
  if (opts.flatAuth) {
    writeFileSync(join(agentDir, 'auth.json'), JSON.stringify(opts.flatAuth), 'utf8')
  }
  if (opts.sqliteStore) {
    const stateDir = join(dir, 'state')
    mkdirSync(stateDir, { recursive: true })
    const db = new DatabaseCtor(join(stateDir, 'openclaw.sqlite'))
    db.exec('CREATE TABLE auth_profile_stores (store_key TEXT PRIMARY KEY, store_json TEXT NOT NULL, updated_at INTEGER NOT NULL)')
    db.prepare('INSERT INTO auth_profile_stores VALUES (?, ?, ?)').run('main', JSON.stringify(opts.sqliteStore), Date.now())
    db.close()
  }
  return dir
}

beforeEach(() => {
  tmp = mkdtempSync(join(tmpdir(), 'memoria-detect-'))
  fetchMock = vi.fn<FetchFn>()
  vi.stubGlobal('fetch', fetchMock)
  warnSpy = vi.spyOn(console, 'warn').mockImplementation(() => {})
})

afterEach(() => {
  vi.unstubAllGlobals()
  vi.restoreAllMocks()
  rmSync(tmp, { recursive: true, force: true })
})

describe('detectLlmOptions', () => {
  const baseInput = () => ({
    env: {} as NodeJS.ProcessEnv,
    keyFiles: {
      openai: join(tmp, 'openai_key'),
      anthropic: join(tmp, 'anthropic_key'),
      openrouter: join(tmp, 'openrouter_key'),
    },
    openclawDir: join(tmp, 'absent-openclaw'),
    hasCommand: () => false,
  })

  it('ollama : serveur up + les deux modèles → available, champs séparés corrects', async () => {
    stubServers({ ollamaModels: ['qwen2.5:3b', 'nomic-embed-text:latest'], lmModels: null })
    const o = await detectLlmOptions({ ...baseInput(), hasCommand: cmd => cmd === 'ollama' })
    expect(o.ollama).toMatchObject({
      available: true,
      serverUp: true,
      hasEmbedModel: true,
      hasExtractModel: true,
      binaryInPath: true,
    })
    expect(o.lmstudio.available).toBe(false)
  })

  it('ollama : serveur up, modèle d’extraction manquant → available:false + detail nommant le modèle', async () => {
    stubServers({ ollamaModels: ['nomic-embed-text:latest'], lmModels: null })
    const o = await detectLlmOptions(baseInput())
    expect(o.ollama.available).toBe(false)
    expect(o.ollama.serverUp).toBe(true)
    expect(o.ollama.hasEmbedModel).toBe(true)
    expect(o.ollama.hasExtractModel).toBe(false)
    expect(o.ollama.detail).toContain('qwen2.5:3b')
  })

  it('ollama : serveur down → serverUp:false (warn, pas silencieux)', async () => {
    stubServers({ ollamaModels: null, lmModels: null })
    const o = await detectLlmOptions(baseInput())
    expect(o.ollama.serverUp).toBe(false)
    expect(o.ollama.available).toBe(false)
    expect(warnSpy).toHaveBeenCalledWith(expect.stringContaining('ollama injoignable'))
  })

  it('lmstudio : serveur up → available + liste des modèles chargés', async () => {
    stubServers({ ollamaModels: null, lmModels: ['qwen2.5-7b-instruct'] })
    const o = await detectLlmOptions(baseInput())
    expect(o.lmstudio.available).toBe(true)
    expect(o.lmstudio.models).toEqual(['qwen2.5-7b-instruct'])
  })

  it('clés API : fichier > rien ; env reconnu ; la VALEUR ne sort jamais', async () => {
    stubServers({ ollamaModels: null, lmModels: null })
    writeFileSync(join(tmp, 'openai_key'), 'sk-secret-test-123\n', 'utf8')
    const o = await detectLlmOptions({ ...baseInput(), env: { OPENROUTER_API_KEY: 'or-secret-456' } })
    expect(o.openai).toMatchObject({ available: true, source: 'fichier' })
    expect(o.openrouter).toMatchObject({ available: true, source: 'env' })
    expect(o.anthropic).toMatchObject({ available: false, source: null })
    // la clé ne fuit nulle part dans le rapport
    expect(JSON.stringify(o)).not.toContain('sk-secret-test-123')
    expect(JSON.stringify(o)).not.toContain('or-secret-456')
  })

  it('openclaw absent → available:false ; présent avec clé api_key → reusable + provider + configPath', async () => {
    stubServers({ ollamaModels: null, lmModels: null })
    const absent = await detectLlmOptions(baseInput())
    expect(absent.openclaw).toMatchObject({ available: false, reusable: false })

    const dir = makeOpenClawDir({
      profiles: { 'openrouter:default': { type: 'api_key', provider: 'openrouter', key: 'or-openclaw-789' } },
    })
    const o = await detectLlmOptions({ ...baseInput(), openclawDir: dir })
    expect(o.openclaw).toMatchObject({ available: true, reusable: true, provider: 'openrouter' })
    expect(o.openclaw.configPath).toContain('auth-profiles.json')
    expect(JSON.stringify(o)).not.toContain('or-openclaw-789') // jamais la valeur
  })

  it('openclaw OAuth uniquement → reusable:false avec raison honnête', async () => {
    stubServers({ ollamaModels: null, lmModels: null })
    const dir = makeOpenClawDir({
      profiles: { 'anthropic:user@mail.com': { type: 'oauth', provider: 'anthropic', access: 'a', refresh: 'r', expires: 9999999999999 } },
    })
    const o = await detectLlmOptions({ ...baseInput(), openclawDir: dir })
    expect(o.openclaw.available).toBe(true)
    expect(o.openclaw.reusable).toBe(false)
    expect(o.openclaw.reason).toContain('OAuth')
  })
})

describe('scanOpenClawCredentials', () => {
  it('lit la forme canonique, la forme plate ET le store SQLite', () => {
    const dir = makeOpenClawDir({
      profiles: { 'openai:default': { type: 'api_key', provider: 'openai', key: 'sk-json' } },
      flatAuth: { openrouter: { apiKey: 'or-flat' } },
      sqliteStore: { profiles: { 'anthropic:default': { type: 'api_key', provider: 'anthropic', key: 'sk-ant-sqlite' } } },
    })
    const scan = scanOpenClawCredentials(dir)
    const byProvider = Object.fromEntries(scan.candidates.map(c => [c.provider, c]))
    expect(byProvider['openai']?.key).toBe('sk-json')
    expect(byProvider['openrouter']?.key).toBe('or-flat')
    expect(byProvider['anthropic']?.key).toBe('sk-ant-sqlite')
    expect(byProvider['anthropic']?.configPath).toContain('openclaw.sqlite')
  })

  it('fichier JSON corrompu → note explicite, jamais avalé', () => {
    const dir = makeOpenClawDir({})
    writeFileSync(join(dir, 'agents', 'main', 'agent', 'auth-profiles.json'), '{pas du json', 'utf8')
    const scan = scanOpenClawCredentials(dir)
    expect(scan.candidates).toHaveLength(0)
    expect(scan.notes.some(n => n.includes('illisible'))).toBe(true)
  })
})

describe('copyOpenClawKey', () => {
  it('copie la clé vers le fichier cible en chmod 600 (sans la logger)', () => {
    const dir = makeOpenClawDir({
      profiles: { 'openai:default': { type: 'api_key', provider: 'openai', key: 'sk-copie-me' } },
    })
    const keyFile = join(tmp, 'dest', 'api_key')
    const r = copyOpenClawKey('openai', { openclawDir: dir, keyFile })
    expect(r.keyFile).toBe(keyFile)
    expect(readFileSync(keyFile, 'utf8')).toBe('sk-copie-me\n')
    expect(statSync(keyFile).mode & 0o777).toBe(0o600)
    // rien de loggé pendant la copie (la clé ne doit jamais finir en console)
    expect(warnSpy.mock.calls.flat().join(' ')).not.toContain('sk-copie-me')
  })

  it('OAuth seulement → erreur explicite ; rien trouvé → erreur explicite', () => {
    const oauthDir = makeOpenClawDir({
      profiles: { 'openai:me': { type: 'oauth', provider: 'openai', access: 'a', refresh: 'r' } },
    })
    expect(() => copyOpenClawKey('openai', { openclawDir: oauthDir, keyFile: join(tmp, 'x') })).toThrow(/OAuth/)
    expect(() => copyOpenClawKey('anthropic', { openclawDir: join(tmp, 'vide'), keyFile: join(tmp, 'y') })).toThrow(/aucune clé/)
  })
})

describe('Memoria.llmHealth', () => {
  it('aucun moteur joignable → extraction/embeddings indisponibles AVEC raisons + wal_pending', async () => {
    stubServers({ ollamaModels: null, lmModels: null })
    const root = join(tmp, 'data')
    const m = Memoria.init({ storageRoot: root, configPath: join(tmp, 'config.toml'), secretsVault: 'aes-vault' })
    try {
      const h = await m.llmHealth()
      expect(h.extraction.available).toBe(false)
      expect(h.extraction.provider).toBe('ollama') // défaut 100-local
      expect(h.extraction.reason).toContain('Ollama injoignable')
      expect(h.embeddings.available).toBe(false)
      expect(h.embeddings.reason).toContain('nécessite Ollama')
      expect(h.wal_pending).toBe(0)
      expect(h.options.ollama.kind).toBe('ollama')
      expect(h.options.lmstudio.kind).toBe('lmstudio')
      expect(h.options.openclaw.kind).toBe('openclaw')
    } finally {
      m.close()
    }
  })

  it('Ollama complet → extraction et embeddings disponibles ; modèle manquant → raison « pull »', async () => {
    stubServers({ ollamaModels: ['qwen2.5:3b', 'nomic-embed-text:latest'], lmModels: null })
    const root = join(tmp, 'data2')
    const m = Memoria.init({ storageRoot: root, configPath: join(tmp, 'config2.toml'), secretsVault: 'aes-vault' })
    try {
      const ok = await m.llmHealth()
      expect(ok.extraction).toMatchObject({ provider: 'ollama', model: 'qwen2.5:3b', available: true })
      expect(ok.embeddings).toMatchObject({ provider: 'ollama', model: 'nomic-embed-text', available: true })

      stubServers({ ollamaModels: ['nomic-embed-text:latest'], lmModels: null })
      const manque = await m.llmHealth()
      expect(manque.extraction.available).toBe(false)
      expect(manque.extraction.reason).toContain('ollama pull qwen2.5:3b')
      expect(manque.embeddings.available).toBe(true)
    } finally {
      m.close()
    }
  })

  it('provider explicite lmstudio configuré → santé reflète LM Studio', async () => {
    stubServers({ ollamaModels: null, lmModels: ['qwen2.5-7b-instruct'] })
    const root = join(tmp, 'data3')
    const m = Memoria.init({ storageRoot: root, configPath: join(tmp, 'config3.toml'), secretsVault: 'aes-vault' })
    try {
      m.setExtractionProvider('lmstudio', 'qwen2.5-7b-instruct')
      const h = await m.llmHealth()
      expect(h.extraction).toMatchObject({ provider: 'lmstudio', model: 'qwen2.5-7b-instruct', available: true })
      // embeddings restent Ollama-only en V1 : indisponible ET DIT explicitement
      expect(h.embeddings.available).toBe(false)
      expect(h.embeddings.reason).toContain('nécessite Ollama (nomic-embed-text)')
    } finally {
      m.close()
    }
  })
})
