/**
 * Routes « agents sur cette machine » (missions B1/B2) :
 *  - GET  /v1/admin/agents_detect : détection injectée (faux HOME, sonde CLI stubée) ;
 *  - POST /v1/admin/agents_connect : pairing EN PROCESSUS + credentials chmod 600 +
 *    enregistrement MCP (stub) — succès, échec visible, kind invalide.
 * Aucun vrai HOME, aucun vrai binaire : tout passe par les injectables du daemon.
 */
import { hostname } from 'node:os'
import { mkdirSync, mkdtempSync, readFileSync, rmSync, statSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import type { RegisterResult } from '@memoria/core'
import { startDaemon, type RunningDaemon } from '../src/index.js'

let root: string
let home: string
let credsDir: string
let daemon: RunningDaemon

const registrar = vi.fn(
  (host: string, instanceId: string): RegisterResult => ({
    host: host as RegisterResult['host'],
    registered: true,
    detail: `stub : enregistré ${host}/${instanceId}`,
  }),
)

beforeEach(async () => {
  root = mkdtempSync(join(tmpdir(), 'memoria-agents-routes-'))
  home = join(root, 'home')
  credsDir = join(root, 'credentials')
  mkdirSync(home, { recursive: true })
  registrar.mockClear()
  daemon = await startDaemon({
    storageRoot: join(root, 'storage'),
    configPath: join(root, 'config.toml'),
    agentsHome: home,
    checkCli: bin => bin === 'claude',
    registrar,
    credentialsDir: credsDir,
    llm: { extraction: null },
  })
})

afterEach(async () => {
  await daemon.close()
  rmSync(root, { recursive: true, force: true })
})

function url(path: string): string {
  return `http://127.0.0.1:${daemon.state.port}${path}`
}

function adminHeaders(): Record<string, string> {
  return { authorization: `Bearer ${daemon.state.admin_token}`, 'content-type': 'application/json' }
}

async function post(path: string, body: unknown): Promise<{ status: number; json: Record<string, unknown> }> {
  const res = await fetch(url(path), { method: 'POST', headers: adminHeaders(), body: JSON.stringify(body) })
  return { status: res.status, json: (await res.json()) as Record<string, unknown> }
}

async function get(path: string): Promise<{ status: number; json: Record<string, unknown> }> {
  const res = await fetch(url(path), { headers: adminHeaders() })
  return { status: res.status, json: (await res.json()) as Record<string, unknown> }
}

describe('GET /v1/admin/agents_detect', () => {
  it('détecte CLI + données et croise le registry', async () => {
    // données Claude Code dans le faux HOME
    mkdirSync(join(home, '.claude', 'projects', 'p'), { recursive: true })
    writeFileSync(join(home, '.claude', 'projects', 'p', 'conv.jsonl'), '{}')

    const before = await get('/v1/admin/agents_detect')
    expect(before.status).toBe(200)
    const agentsBefore = before.json['agents'] as Array<Record<string, unknown>>
    const claudeBefore = agentsBefore.find(a => a['kind'] === 'claude-code')
    expect(claudeBefore).toMatchObject({ installed: true, already_connected: null })
    expect((claudeBefore?.['data_found'] as Record<string, unknown>)['transcript_files']).toBe(1)

    // après connexion → already_connected renseigné (instance non révoquée, même machine)
    const conn = await post('/v1/admin/agents_connect', { kind: 'claude-code' })
    expect(conn.status).toBe(200)
    const after = await get('/v1/admin/agents_detect')
    const claudeAfter = (after.json['agents'] as Array<Record<string, unknown>>).find(a => a['kind'] === 'claude-code')
    expect(claudeAfter?.['already_connected']).toBe(conn.json['instance_id'])
  })
})

describe('POST /v1/admin/agents_connect', () => {
  it('1 clic : pairing en processus + credentials chmod 600 + enregistrement MCP', async () => {
    const { status, json } = await post('/v1/admin/agents_connect', { kind: 'claude-code', name: 'Claude iMac' })
    expect(status).toBe(200)
    const instanceId = json['instance_id'] as string
    expect(instanceId).toBeTruthy()
    expect(json['restart_hint']).toContain('Redémarre ton agent')
    expect((json['registered'] as Record<string, unknown>)['registered']).toBe(true)

    // registrar appelé avec le token d'instance
    expect(registrar).toHaveBeenCalledTimes(1)
    expect(registrar.mock.calls[0]?.[0]).toBe('claude-code')
    expect(registrar.mock.calls[0]?.[1]).toBe(instanceId)

    // credentials écrits, chmod 600, token VALIDE (utilisable sur /v1/memory/*)
    const credsPath = json['credentials_path'] as string
    expect(credsPath).toContain(credsDir)
    const mode = statSync(credsPath).mode & 0o777
    expect(mode).toBe(0o600)
    const creds = JSON.parse(readFileSync(credsPath, 'utf8')) as { instance_token: string; assistant_type: string }
    expect(creds.assistant_type).toBe('claude-code')

    const memRes = await fetch(url('/v1/memory/store_fact'), {
      method: 'POST',
      headers: { authorization: `Bearer ${creds.instance_token}`, 'content-type': 'application/json' },
      body: JSON.stringify({ content: 'le projet de test utilise vitest', category: 'config' }),
    })
    expect(memRes.status).toBe(200)

    // l'instance est visible et NON en attente (last_seen_at renseigné par completePairing)
    const agents = daemon.memoria.listAgents()
    const inst = agents.find(a => a.instance.id === instanceId)
    expect(inst?.assistant_type).toBe('claude-code')
    expect(inst?.instance.last_seen_at).not.toBeNull()
    expect(inst?.instance.machine_id).toBe(hostname())
  })

  it('échec d’enregistrement : visible, avec instructions de repli (pas de 500)', async () => {
    registrar.mockImplementationOnce(() => {
      throw new Error('fichier verrouillé')
    })
    const { status, json } = await post('/v1/admin/agents_connect', { kind: 'codex' })
    expect(status).toBe(200)
    const reg = json['registered'] as Record<string, unknown>
    expect(reg['registered']).toBe(false)
    expect(String(reg['detail'])).toContain('fichier verrouillé')
    expect(String(reg['detail'])).toContain('Manuel')
    expect(json['restart_hint']).toBeNull()
    // l'instance existe quand même (l'utilisateur peut réessayer l'enregistrement)
    expect(json['instance_id']).toBeTruthy()
  })

  it('kind invalide → 400 explicite', async () => {
    const { status, json } = await post('/v1/admin/agents_connect', { kind: 'skynet' })
    expect(status).toBe(400)
    expect(String(json['error'])).toContain('skynet')
  })
})
