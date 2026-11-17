/**
 * Client des routes « agents sur cette machine » (B1/B2/B3) — fetch stubé,
 * AUCUN réseau : chemins, méthodes, corps et auth vérifiés.
 */
import { afterEach, describe, expect, it, vi } from 'vitest'
import { connectAgent, detectMachineAgents, getImportStatus, startImport, type ImportJobStatus } from '../src/api'

const TOKEN_KEY = 'memoria.admin_token'

function stubBrowser(token = 'tok-admin'): void {
  const store = new Map<string, string>([[TOKEN_KEY, token]])
  vi.stubGlobal('sessionStorage', {
    getItem: (k: string) => store.get(k) ?? null,
    setItem: (k: string, v: string) => void store.set(k, v),
    removeItem: (k: string) => void store.delete(k),
  })
}

function jsonResponse(payload: unknown, status = 200): Response {
  return new Response(JSON.stringify(payload), { status, headers: { 'content-type': 'application/json' } })
}

afterEach(() => {
  vi.unstubAllGlobals()
})

describe('detectMachineAgents', () => {
  it('GET /v1/admin/agents_detect avec le token admin', async () => {
    stubBrowser()
    const agents = [
      { kind: 'claude-code', name: 'Claude Code', installed: true, data_found: { transcript_files: 12 }, already_connected: null },
    ]
    const fetchMock = vi.fn(async (url: string | URL | Request, init?: RequestInit) => {
      expect(String(url)).toBe('/v1/admin/agents_detect')
      const headers = (init?.headers ?? {}) as Record<string, string>
      expect(headers['authorization']).toBe('Bearer tok-admin')
      return jsonResponse({ agents })
    })
    vi.stubGlobal('fetch', fetchMock)
    await expect(detectMachineAgents()).resolves.toEqual(agents)
  })
})

describe('connectAgent', () => {
  it('POST /v1/admin/agents_connect { kind, name? }', async () => {
    stubBrowser()
    const result = {
      instance_id: 'inst-1',
      credentials_path: '/tmp/creds/inst-1.json',
      registered: { host: 'claude-code', registered: true, detail: 'ok' },
      restart_hint: 'Redémarre ton agent pour activer Memoria.',
    }
    const fetchMock = vi.fn(async (url: string | URL | Request, init?: RequestInit) => {
      expect(String(url)).toBe('/v1/admin/agents_connect')
      expect(init?.method).toBe('POST')
      expect(JSON.parse(String(init?.body))).toEqual({ kind: 'claude-code' })
      return jsonResponse(result)
    })
    vi.stubGlobal('fetch', fetchMock)
    await expect(connectAgent('claude-code')).resolves.toEqual(result)
  })
})

describe('startImport / getImportStatus', () => {
  const status: ImportJobStatus = {
    state: 'running',
    kind: 'legacy',
    instance_id: 'inst-1',
    progress: { files_done: 0, files_total: 1, facts_imported: 0 },
    error: null,
    errors: [],
    started_at: '2026-06-11T10:00:00.000Z',
    finished_at: null,
  }

  it('POST /v1/admin/import_start avec le corps complet', async () => {
    stubBrowser()
    const fetchMock = vi.fn(async (url: string | URL | Request, init?: RequestInit) => {
      expect(String(url)).toBe('/v1/admin/import_start')
      expect(JSON.parse(String(init?.body))).toEqual({
        instance_id: 'inst-1',
        kind: 'legacy',
        legacy_path: '/home/x/.openclaw/workspace/memory/memoria.db',
      })
      return jsonResponse(status)
    })
    vi.stubGlobal('fetch', fetchMock)
    await expect(
      startImport({ instance_id: 'inst-1', kind: 'legacy', legacy_path: '/home/x/.openclaw/workspace/memory/memoria.db' }),
    ).resolves.toEqual(status)
  })

  it('GET /v1/admin/import_status, et une erreur HTTP remonte en ApiError', async () => {
    stubBrowser()
    const fetchMock = vi.fn(async (url: string | URL | Request) => {
      expect(String(url)).toBe('/v1/admin/import_status')
      return jsonResponse(status)
    })
    vi.stubGlobal('fetch', fetchMock)
    await expect(getImportStatus()).resolves.toEqual(status)

    vi.stubGlobal('fetch', vi.fn(async () => jsonResponse({ error: 'un import est déjà en cours' }, 409)))
    await expect(startImport({ instance_id: 'inst-1', kind: 'transcripts' })).rejects.toThrow('un import est déjà en cours')
  })
})
