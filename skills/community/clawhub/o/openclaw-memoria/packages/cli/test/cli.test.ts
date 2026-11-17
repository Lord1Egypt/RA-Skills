/**
 * Tests CLI : enregistrement des commandes, doctor local sans daemon,
 * chemin HTTP admin avec fetch mocké, gardes de forget.
 * Aucun réseau réel (fetch stubé), aucun vrai HOME (tmpdir + --config).
 */
import { mkdirSync, mkdtempSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { PassThrough } from 'node:stream'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { Memoria } from '@memoria/core'
import { writeDaemonState } from '@memoria/daemon'
import {
  AgentsCommand,
  AuditCommand,
  buildCli,
  DaemonCommand,
  DoctorCommand,
  ForgetCommand,
  InitCommand,
  PairCommand,
  RevokeCommand,
  StartCommand,
  StatsCommand,
  StopCommand,
} from '../src/index.js'

let root: string
let cfg: string

function makeIo() {
  const outChunks: Buffer[] = []
  const errChunks: Buffer[] = []
  const stdout = new PassThrough()
  stdout.on('data', (c: Buffer) => outChunks.push(c))
  const stderr = new PassThrough()
  stderr.on('data', (c: Buffer) => errChunks.push(c))
  return {
    context: { stdin: new PassThrough(), stdout, stderr },
    out: () => Buffer.concat(outChunks).toString('utf8'),
    err: () => Buffer.concat(errChunks).toString('utf8'),
  }
}

function jsonResponse(payload: unknown): Response {
  return new Response(JSON.stringify(payload), {
    status: 200,
    headers: { 'content-type': 'application/json' },
  })
}

beforeEach(() => {
  root = mkdtempSync(join(tmpdir(), 'memoria-cli-'))
  cfg = join(root, 'config.toml')
  // Réseau interdit par défaut : tout fetch imprévu fait échouer le chemin daemon.
  vi.stubGlobal('fetch', vi.fn(async () => {
    throw new Error('réseau interdit dans les tests')
  }))
})

afterEach(() => {
  vi.unstubAllGlobals()
  rmSync(root, { recursive: true, force: true })
})

const args = (...rest: string[]): string[] => [...rest, '--storage-root', root, '--config', cfg]

describe('helpers', () => {
  it('formatBytes : unités correctes', async () => {
    const { formatBytes } = await import('../src/index.js')
    expect(formatBytes(512)).toBe('512 o')
    expect(formatBytes(4096)).toBe('4 Ko')
    expect(formatBytes(163_840)).toBe('160 Ko')
    expect(formatBytes(5 * 1024 * 1024)).toBe('5 Mo')
  })
})

describe('enregistrement des commandes', () => {
  it('cli.process trouve chaque commande', () => {
    const cli = buildCli()
    const cases: Array<[string[], unknown]> = [
      [['init'], InitCommand],
      [['daemon'], DaemonCommand],
      [['start'], StartCommand],
      [['stop'], StopCommand],
      [['doctor'], DoctorCommand],
      [['pair', 'claude-code'], PairCommand],
      [['agents'], AgentsCommand],
      [['revoke', 'instance-1'], RevokeCommand],
      [['stats'], StatsCommand],
      [['forget', '--id', 'abc'], ForgetCommand],
      [['audit'], AuditCommand],
    ]
    for (const [argv, klass] of cases) {
      expect(cli.process(argv), argv.join(' ')).toBeInstanceOf(klass)
    }
  })
})

describe('doctor', () => {
  it('sans daemon : rapport local, note « daemon arrêté », code 0', async () => {
    const io = makeIo()
    const code = await buildCli().run(args('doctor'), io.context)
    expect(code).toBe(0)
    const out = io.out()
    expect(out).toContain('daemon arrêté')
    expect(out).toContain('registry.sqlite')
    expect(out).toContain('garde réseau')
    expect(out).toContain('État')
    expect(io.err()).toBe('')
  })

  it('avec daemon vivant : passe par HTTP admin (fetch mocké), sans note locale', async () => {
    mkdirSync(root, { recursive: true })
    writeDaemonState(root, {
      daemon_id: 'd-test',
      port: 4242,
      admin_token: 'token-admin-test',
      pid: process.pid, // PID vivant garanti
      started_at: new Date().toISOString(),
    })
    const report = {
      ok: true,
      storage_root: root,
      config_path: cfg,
      registry_path: join(root, 'registry.sqlite'),
      databases: [{ kind: 'registry', path: join(root, 'registry.sqlite'), exists: true, size_bytes: 4096 }],
      network_guard: { on_network_volume: false, journal_mode: 'wal' },
      warnings: [],
    }
    const fetchMock = vi.fn(async (url: string | URL | Request, init?: RequestInit) => {
      const u = String(url)
      if (u.endsWith('/v1/health')) return jsonResponse({ ok: true, version: 'test', daemon_id: 'd-test' })
      if (u.endsWith('/v1/admin/doctor')) {
        const headers = (init?.headers ?? {}) as Record<string, string>
        expect(headers['authorization']).toBe('Bearer token-admin-test')
        return jsonResponse(report)
      }
      throw new Error(`URL inattendue : ${u}`)
    })
    vi.stubGlobal('fetch', fetchMock)

    const io = makeIo()
    const code = await buildCli().run(args('doctor'), io.context)
    expect(code).toBe(0)
    expect(io.out()).not.toContain('daemon arrêté')
    expect(io.out()).toContain('État : ✓ OK')
    expect(fetchMock).toHaveBeenCalledWith(expect.stringContaining('/v1/admin/doctor'), expect.anything())
  })
})

describe('forget — gardes', () => {
  it('sans --id ni --query : erreur propre, code 1, pas de stack', async () => {
    const io = makeIo()
    const code = await buildCli().run(args('forget'), io.context)
    expect(code).toBe(1)
    expect(io.err()).toContain('filtre vide')
    expect(io.err()).not.toContain('    at ') // pas de stack brute
    expect(io.out()).toBe('')
  })

  it('--query sans --confirm-bulk : erreur propre, code 1', async () => {
    const io = makeIo()
    const code = await buildCli().run(args('forget', '--query', 'vieux client'), io.context)
    expect(code).toBe(1)
    expect(io.err()).toContain('--confirm-bulk')
  })

  it('> 5 ids sans --yes en non-TTY : erreur propre, code 1', async () => {
    const io = makeIo()
    const ids = ['a', 'b', 'c', 'd', 'e', 'f'].flatMap(id => ['--id', id])
    const code = await buildCli().run(args('forget', ...ids), io.context)
    expect(code).toBe(1)
    expect(io.err()).toContain('--yes')
  })

  it('par --id en local (daemon arrêté) : supprime vraiment, code 0', async () => {
    const memoria = Memoria.init({ storageRoot: root, configPath: cfg })
    const paired = memoria.pairAssistant({ type: 'claude-code' })
    const fact = memoria.storeFact({ instance: paired.assistant_instance_id, content: 'souvenir à oublier' })
    memoria.close()

    const io = makeIo()
    const code = await buildCli().run(args('forget', '--id', fact.id), io.context)
    expect(code).toBe(0)
    expect(io.out()).toContain('1 souvenir(s) supprimé(s)')

    const reopened = Memoria.init({ storageRoot: root, configPath: cfg })
    expect(reopened.stats().facts).toBe(0)
    reopened.close()
  })
})

describe('commandes locales (daemon arrêté)', () => {
  it('stats : compteurs à zéro sur une racine neuve, code 0', async () => {
    const io = makeIo()
    const code = await buildCli().run(args('stats'), io.context)
    expect(code).toBe(0)
    expect(io.out()).toContain('daemon arrêté')
    expect(io.out()).toContain('Souvenirs : 0')
    expect(io.out()).toContain('Instances : 0')
  })

  it('agents : liste vide annoncée, code 0', async () => {
    const io = makeIo()
    const code = await buildCli().run(args('agents'), io.context)
    expect(code).toBe(0)
    expect(io.out()).toContain('Aucune instance')
  })

  it('audit : trace les actions (pairing visible), code 0', async () => {
    const memoria = Memoria.init({ storageRoot: root, configPath: cfg })
    memoria.pairAssistant({ type: 'codex' })
    memoria.close()

    const io = makeIo()
    const code = await buildCli().run(args('audit'), io.context)
    expect(code).toBe(0)
    expect(io.out()).toContain('pair_assistant')
    expect(io.out()).toContain('jamais de contenu')
  })

  it('stop sans daemon.json : message clair, code 0', async () => {
    const io = makeIo()
    const code = await buildCli().run(args('stop'), io.context)
    expect(code).toBe(0)
    expect(io.out()).toContain('rien à arrêter')
  })

  it('pair avec un type inconnu : erreur propre AVANT tout démarrage de daemon, code 1', async () => {
    const io = makeIo()
    const code = await buildCli().run(args('pair', 'skynet'), io.context)
    expect(code).toBe(1)
    expect(io.err()).toContain('type inconnu')
    expect(io.err()).toContain('claude-code')
    // la validation précède ensureDaemon : aucun fetch, aucun spawn
    expect(vi.mocked(fetch)).not.toHaveBeenCalled()
  })

  it('revoke sur une instance inconnue : erreur propre, code 1', async () => {
    const io = makeIo()
    const code = await buildCli().run(args('revoke', 'instance-fantome'), io.context)
    expect(code).toBe(1)
    expect(io.err()).toContain('instance inconnue')
  })
})
