/**
 * Tests `memoria ui` : enregistrement (chemin 'ui' + commande PAR DÉFAUT),
 * construction de l'URL avec le token admin, ouverture injectée, démarrage
 * du daemon quand il est arrêté (ensureDaemon injecté), échec d'ouverture
 * annoncé (jamais silencieux), et helper openInBrowser réel (spawn).
 * Aucun réseau réel (fetch stubé), aucun vrai HOME (tmpdir + --config).
 */
import { mkdirSync, mkdtempSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { PassThrough } from 'node:stream'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { Builtins } from 'clipanion/lib/advanced/index.js'
import { writeDaemonState, type DaemonState } from '@memoria/daemon'
import { buildCli, UiCommand } from '../src/index.js'
import { openerFor, openInBrowser } from '../src/commands/ui.js'

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
  root = mkdtempSync(join(tmpdir(), 'memoria-cli-ui-'))
  cfg = join(root, 'config.toml')
  // Réseau interdit par défaut : tout fetch imprévu fait échouer le test.
  vi.stubGlobal('fetch', vi.fn(async () => {
    throw new Error('réseau interdit dans les tests')
  }))
})

afterEach(() => {
  vi.unstubAllGlobals()
  rmSync(root, { recursive: true, force: true })
})

const args = (...rest: string[]): string[] => [...rest, '--storage-root', root, '--config', cfg]

/** daemon.json « vivant » (PID du process de test) + fetch health OK. */
function fakeAliveDaemon(port: number, token: string): void {
  mkdirSync(root, { recursive: true })
  writeDaemonState(root, {
    daemon_id: 'd-ui-test',
    port,
    admin_token: token,
    pid: process.pid,
    started_at: new Date().toISOString(),
  })
  vi.stubGlobal('fetch', vi.fn(async (url: string | URL | Request) => {
    const u = String(url)
    if (u.endsWith('/v1/health')) return jsonResponse({ ok: true, version: 'test', daemon_id: 'd-ui-test' })
    throw new Error(`URL inattendue : ${u}`)
  }))
}

describe('enregistrement', () => {
  it("'ui' ET la commande par défaut (`memoria` seul) résolvent UiCommand", () => {
    const cli = buildCli()
    expect(cli.process(['ui'])).toBeInstanceOf(UiCommand)
    expect(cli.process([])).toBeInstanceOf(UiCommand)
  })

  it("l'aide reste accessible : --help et -h résolvent HelpCommand, pas UiCommand", () => {
    const cli = buildCli()
    expect(cli.process(['--help'])).toBeInstanceOf(Builtins.HelpCommand)
    expect(cli.process(['-h'])).toBeInstanceOf(Builtins.HelpCommand)
  })
})

describe('memoria ui — daemon vivant', () => {
  it("affiche l'URL avec le token admin et l'ouvre via openUrl injecté, code 0", async () => {
    fakeAliveDaemon(4242, 'token-admin-test')
    const opened: string[] = []
    const cli = buildCli()
    const cmd = cli.process(args('ui')) as UiCommand
    cmd.openUrl = async url => {
      opened.push(url)
    }
    const io = makeIo()
    const code = await cli.run(cmd, io.context)
    expect(code).toBe(0)
    expect(opened).toEqual(['http://127.0.0.1:4242/ui/#token=token-admin-test'])
    expect(io.out()).toContain('Interface : http://127.0.0.1:4242/ui/#token=token-admin-test')
    expect(io.out()).toContain('✓ Interface ouverte dans le navigateur.')
    expect(io.out()).not.toContain('démarrage') // daemon déjà vivant : pas de start
    expect(io.err()).toBe('')
  })

  it("échec d'ouverture : annoncé en clair, l'URL reste affichée, code 0", async () => {
    fakeAliveDaemon(4242, 'token-admin-test')
    const cli = buildCli()
    const cmd = cli.process(args('ui')) as UiCommand
    cmd.openUrl = async () => {
      throw new Error('navigateur introuvable')
    }
    const io = makeIo()
    const code = await cli.run(cmd, io.context)
    expect(code).toBe(0)
    expect(io.out()).toContain('Interface : http://127.0.0.1:4242/ui/#token=token-admin-test')
    expect(io.out()).toContain('Ouverture automatique impossible (navigateur introuvable)')
  })
})

describe('memoria ui — daemon arrêté', () => {
  it('le démarre (ensureDaemon injecté), attend son état, puis ouvre', async () => {
    const state: DaemonState = {
      daemon_id: 'd-started',
      port: 5151,
      admin_token: 'tok-started',
      pid: process.pid,
      started_at: new Date().toISOString(),
    }
    const ensureDaemonMock = vi.fn(async () => state)
    const opened: string[] = []
    const cli = buildCli()
    const cmd = cli.process(args('ui')) as UiCommand
    cmd.ensureDaemonFn = ensureDaemonMock
    cmd.openUrl = async url => {
      opened.push(url)
    }
    const io = makeIo()
    const code = await cli.run(cmd, io.context)
    expect(code).toBe(0)
    expect(ensureDaemonMock).toHaveBeenCalledWith({ storageRoot: root, configPath: cfg })
    expect(io.out()).toContain('Le service Memoria est arrêté — démarrage…')
    expect(io.out()).toContain('Daemon démarré sur 127.0.0.1:5151')
    expect(opened).toEqual(['http://127.0.0.1:5151/ui/#token=tok-started'])
  })

  it("échec du démarrage : erreur propre sur stderr, code 1, pas d'ouverture", async () => {
    const cli = buildCli()
    const cmd = cli.process(args('ui')) as UiCommand
    cmd.ensureDaemonFn = vi.fn(async () => {
      throw new Error('le daemon n’a pas démarré dans les 15 s (voir memoria doctor)')
    })
    const openUrl = vi.fn(async () => {})
    cmd.openUrl = openUrl
    const io = makeIo()
    const code = await cli.run(cmd, io.context)
    expect(code).toBe(1)
    expect(io.err()).toContain('ui : le daemon n’a pas démarré')
    expect(io.err()).not.toContain('    at ') // pas de stack brute
    expect(openUrl).not.toHaveBeenCalled()
  })
})

describe('openInBrowser (spawn réel, opener injecté)', () => {
  it('openerFor : open sur macOS, xdg-open ailleurs', () => {
    expect(openerFor('darwin')).toBe('open')
    expect(openerFor('linux')).toBe('xdg-open')
  })

  it('résout quand la commande réussit (true)', async () => {
    await expect(openInBrowser('http://127.0.0.1:1/ui/', 'true')).resolves.toBeUndefined()
  })

  it('rejette avec le code de sortie quand la commande échoue (false)', async () => {
    await expect(openInBrowser('http://127.0.0.1:1/ui/', 'false')).rejects.toThrow('a échoué (code 1)')
  })

  it('rejette quand la commande est introuvable', async () => {
    await expect(openInBrowser('http://127.0.0.1:1/ui/', 'memoria-opener-inexistant-xyz')).rejects.toThrow('indisponible')
  })
})
