/**
 * Tests @memoria/mcp : credentials (round-trip + chmod 600), auto-détection
 * repo, handlers MCP (relai daemon + active_context, erreur propre sans throw),
 * connect (pairing → credentials + snippets), gateway HTTP capture_turn.
 * Jamais de vrai daemon, de réseau, ni de vrai HOME : tmpdir + fakes.
 */
import { mkdirSync, mkdtempSync, readFileSync, rmSync, statSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import type { RecallResult } from '@memoria/core'
import {
  ActiveContextTracker,
  buildServer,
  connect,
  credentialsPath,
  HttpDaemonGateway,
  loadCredentials,
  saveCredentials,
  type DaemonGateway,
  type InstanceCredentials,
} from '../src/index.js'

let root: string

beforeEach(() => {
  root = mkdtempSync(join(tmpdir(), 'memoria-mcp-'))
})

afterEach(() => {
  rmSync(root, { recursive: true, force: true })
  vi.restoreAllMocks()
  vi.unstubAllGlobals()
})

const RECALL_EMPTY: RecallResult = { items: [], totalFound: 0, tokens: 0, scopes_searched: [] }

/** Gateway factice qui enregistre les appels. */
function fakeGateway(): DaemonGateway & { calls: Array<{ method: string; input: Record<string, unknown> }> } {
  const calls: Array<{ method: string; input: Record<string, unknown> }> = []
  return {
    calls,
    recall: async input => {
      calls.push({ method: 'recall', input })
      return RECALL_EMPTY
    },
    storeFact: async input => {
      calls.push({ method: 'storeFact', input })
      return { fact: { id: 'f1' } }
    },
    captureTurn: async input => {
      calls.push({ method: 'captureTurn', input })
      return { queued: true }
    },
    identifyInterlocutor: async input => {
      calls.push({ method: 'identifyInterlocutor', input })
      return { match: null }
    },
  }
}

describe('credentials', () => {
  it('round-trip + chmod 600', () => {
    const creds: InstanceCredentials = {
      instance_token: 'tok-secret',
      storage_root: '/tmp/memoria-data',
      created_at: '2026-06-10T00:00:00.000Z',
    }
    const p = saveCredentials('inst-1', creds, root)
    expect(p).toBe(credentialsPath('inst-1', root))
    expect(statSync(p).mode & 0o777).toBe(0o600)
    expect(loadCredentials('inst-1', root)).toEqual(creds)
  })

  it('instance inconnue → null ; fichier corrompu → warn + null (pas de throw)', () => {
    expect(loadCredentials('absent', root)).toBeNull()

    const warn = vi.spyOn(console, 'warn').mockImplementation(() => {})
    writeFileSync(credentialsPath('corrompu', root), '{pas du json', 'utf8')
    expect(loadCredentials('corrompu', root)).toBeNull()
    expect(warn).toHaveBeenCalledOnce()
  })

  it('refuse un instance_id avec séparateur de chemin', () => {
    const creds: InstanceCredentials = { instance_token: 't', storage_root: '/x', created_at: '' }
    expect(() => saveCredentials('../evil', creds, root)).toThrow(/invalide/)
  })
})

describe('ActiveContextTracker', () => {
  it('autoDetect remonte jusqu’à la racine .git (repo_path + topic)', () => {
    const repo = join(root, 'mon-projet')
    mkdirSync(join(repo, 'src', 'deep'), { recursive: true })
    mkdirSync(join(repo, '.git'))

    const tracker = new ActiveContextTracker()
    const found = tracker.autoDetect(join(repo, 'src', 'deep'))
    expect(found).toEqual({ repo_path: repo, topic: 'mon-projet' })
    expect(tracker.current()).toMatchObject({ repo_path: repo, topic: 'mon-projet' })
  })

  it('hors repo → null ; set() explicite prime sur la détection', () => {
    const tracker = new ActiveContextTracker()
    expect(tracker.autoDetect(root)).toBeNull()

    const repo = join(root, 'repo-b')
    mkdirSync(join(repo, '.git'), { recursive: true })
    tracker.autoDetect(repo)
    const effective = tracker.set({ project: 'primask', client: 'acme', repo_path: '/ailleurs' })
    expect(effective).toMatchObject({
      project_id: 'primask',
      client_org_id: 'acme',
      repo_path: '/ailleurs', // explicite > détecté
      topic: 'repo-b',
    })
  })
})

describe('buildServer handlers', () => {
  it('memoria_recall transmet query + limit + active_context au daemon', async () => {
    const gateway = fakeGateway()
    const tracker = new ActiveContextTracker()
    tracker.set({ project: 'memoria-v3', client: 'interne' })

    const { handlers } = buildServer({
      instanceId: 'inst-1',
      tracker,
      connect: async () => gateway,
    })

    const result = await handlers.recall({ query: 'règles de déploiement', limit: 7 })
    expect(result.isError).toBeUndefined()
    expect(gateway.calls).toHaveLength(1)
    expect(gateway.calls[0]?.input).toEqual({
      query: 'règles de déploiement',
      limit: 7,
      active_context: { project_id: 'memoria-v3', client_org_id: 'interne' },
    })
    const text = (result.content[0] as { type: 'text'; text: string }).text
    expect(JSON.parse(text)).toEqual(RECALL_EMPTY)
  })

  it('memoria_store_fact et memoria_capture_turn relaient au daemon', async () => {
    const gateway = fakeGateway()
    const tracker = new ActiveContextTracker()
    const { handlers } = buildServer({ instanceId: 'i', tracker, connect: async () => gateway })

    await handlers.storeFact({ content: 'Néto préfère le français', category: 'preference', tags: ['langue'] })
    await handlers.captureTurn({ messages: [{ role: 'user', content: 'salut' }] })

    expect(gateway.calls.map(c => c.method)).toEqual(['storeFact', 'captureTurn'])
    expect(gateway.calls[0]?.input).toEqual({
      content: 'Néto préfère le français',
      category: 'preference',
      tags: ['langue'],
    })
    expect(gateway.calls[1]?.input).toMatchObject({ messages: [{ role: 'user', content: 'salut' }] })
  })

  it('daemon mort → UNE re-connexion puis erreur MCP propre (jamais de throw)', async () => {
    const warn = vi.spyOn(console, 'warn').mockImplementation(() => {})
    let attempts = 0
    const broken: DaemonGateway = {
      recall: async () => {
        throw new Error('ECONNREFUSED 127.0.0.1:9999')
      },
      storeFact: async () => ({}),
      captureTurn: async () => ({}),
      identifyInterlocutor: async () => ({ match: null }),
    }
    const { handlers } = buildServer({
      instanceId: 'i',
      tracker: new ActiveContextTracker(),
      connect: async () => {
        attempts += 1
        return broken
      },
    })

    const result = await handlers.recall({ query: 'x' })
    expect(result.isError).toBe(true)
    const text = (result.content[0] as { type: 'text'; text: string }).text
    expect(text).toContain('ECONNREFUSED')
    expect(attempts).toBe(2) // connexion initiale + UNE relance
    expect(warn).toHaveBeenCalled()
  })

  it('memoria_set_context / memoria_get_context retournent le contexte effectif', async () => {
    const tracker = new ActiveContextTracker()
    const { handlers } = buildServer({ instanceId: 'i', tracker, connect: async () => fakeGateway() })

    const set = await handlers.setContext({ project: 'jamboard' })
    const setPayload = JSON.parse((set.content[0] as { type: 'text'; text: string }).text) as {
      active_context: { project_id: string }
    }
    expect(setPayload.active_context.project_id).toBe('jamboard')

    const get = await handlers.getContext()
    const getPayload = JSON.parse((get.content[0] as { type: 'text'; text: string }).text) as {
      active_context: { project_id: string }
    }
    expect(getPayload.active_context.project_id).toBe('jamboard')
  })

  it('le serveur MCP expose bien les 7 outils', () => {
    const { server } = buildServer({
      instanceId: 'i',
      tracker: new ActiveContextTracker(),
      connect: async () => fakeGateway(),
    })
    // registre privé du SDK — vérification structurelle volontairement minimale
    const tools = (server as unknown as { _registeredTools: Record<string, unknown> })._registeredTools
    expect(Object.keys(tools).sort()).toEqual([
      'memoria_capture_turn',
      'memoria_get_context',
      'memoria_identify_interlocutor',
      'memoria_identify_or_create_interlocutor',
      'memoria_recall',
      'memoria_set_context',
      'memoria_store_fact',
    ])
  })
})

describe('connect (pairing)', () => {
  it('ensureDaemon → completePairing → credentials 600 + auto-register', async () => {
    const completePairing = vi.fn(async (code: string) => {
      expect(code).toBe('ABCD-2345')
      return { assistant_instance_id: 'claude-code-abc123', instance_token: 'tok-xyz', assistant_type: 'claude-code' }
    })
    const registrar = vi.fn(() => ({ host: 'claude-code' as const, registered: true, detail: 'enregistré' }))

    const result = await connect({
      code: ' ABCD-2345 ', // trim vérifié
      storageRoot: join(root, 'data'),
      credentialsDir: join(root, 'credentials'),
      ensure: async () => ({ port: 4242 }),
      clientFor: () => ({ completePairing }),
      registrar,
    })

    expect(completePairing).toHaveBeenCalledOnce()
    expect(result.instanceId).toBe('claude-code-abc123')
    expect(result.assistantType).toBe('claude-code')
    expect(statSync(result.credentialsPath).mode & 0o777).toBe(0o600)

    const saved = JSON.parse(readFileSync(result.credentialsPath, 'utf8')) as InstanceCredentials
    expect(saved.instance_token).toBe('tok-xyz')
    expect(saved.storage_root).toBe(join(root, 'data'))
    expect(saved.assistant_type).toBe('claude-code')

    expect(registrar).toHaveBeenCalledWith('claude-code', 'claude-code-abc123', { token: 'tok-xyz', storageRoot: join(root, 'data') })
    expect(result.registration?.registered).toBe(true)
    expect(result.message).toContain('Agent connecté à Memoria')
  })

  it('code vide → erreur explicite', async () => {
    await expect(connect({ code: '   ', credentialsDir: root })).rejects.toThrow(/pairing manquant/)
  })
})

describe('HttpDaemonGateway.captureTurn', () => {
  it('POST /v1/memory/capture_turn avec Bearer token (fetch mocké)', async () => {
    const fetchMock = vi.fn(async (url: unknown, init?: { headers?: Record<string, string>; body?: string }) => {
      expect(String(url)).toBe('http://127.0.0.1:5151/v1/memory/capture_turn')
      expect(init?.headers?.['authorization']).toBe('Bearer tok-abc')
      expect(JSON.parse(init?.body ?? '{}')).toMatchObject({ messages: [{ role: 'user', content: 'hello' }] })
      return new Response(JSON.stringify({ queued: true }), { status: 200 })
    })
    vi.stubGlobal('fetch', fetchMock)

    const gateway = new HttpDaemonGateway({ port: 5151 }, 'tok-abc')
    const out = await gateway.captureTurn({ messages: [{ role: 'user', content: 'hello' }] })
    expect(out).toEqual({ queued: true })
    expect(fetchMock).toHaveBeenCalledOnce()
  })

  it('réponse non-OK → erreur avec status + message daemon', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn(async () => new Response(JSON.stringify({ error: 'route inconnue' }), { status: 404 })),
    )
    const gateway = new HttpDaemonGateway({ port: 5151 }, 'tok-abc')
    await expect(gateway.captureTurn({ messages: [] })).rejects.toThrow(/404.*route inconnue/)
  })
})
