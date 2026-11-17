/**
 * Install/désinstall des HOOKS OpenClaw (auto-recall + auto-capture).
 * Le point critique : poser `allowConversationAccess=true`, sans quoi
 * `agent_end`/`llm_output` sont bloqués silencieusement (DIAG-OPENCLAW §2.1).
 * Chemins ~/.openclaw injectés en tmpdir : on ne touche jamais la vraie config.
 */
import { existsSync, mkdtempSync, readFileSync, rmSync, writeFileSync, mkdirSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { afterEach, beforeEach, describe, expect, it } from 'vitest'
import { installOpenClawHooks, unregisterOpenClaw } from '../src/register.js'

let oc: string // faux ~/.openclaw
let src: string // faux dossier adaptateur

beforeEach(() => {
  const base = mkdtempSync(join(tmpdir(), 'memoria-ochooks-'))
  oc = join(base, '.openclaw')
  src = join(base, 'adapter')
  mkdirSync(join(src, 'dist'), { recursive: true })
  writeFileSync(join(src, 'dist', 'index.js'), 'export function register(){}')
  writeFileSync(join(src, 'openclaw.plugin.json'), JSON.stringify({ id: 'memoria' }))
})
afterEach(() => rmSync(join(oc, '..'), { recursive: true, force: true }))

describe('installOpenClawHooks', () => {
  it('refuse sans token (MCP seul)', () => {
    const r = installOpenClawHooks({ instanceId: 'i1', openclawDir: oc, srcDir: src })
    expect(r.ok).toBe(false)
    expect(r.detail).toMatch(/token/i)
  })

  it('pose allowConversationAccess=true + lie le plugin + écrit la config', () => {
    const r = installOpenClawHooks({ instanceId: 'koda-1', token: 'tok-abc', storageRoot: '/data/memo', openclawDir: oc, srcDir: src })
    expect(r.ok).toBe(true)

    // plugin lié dans extensions/memoria
    expect(existsSync(join(oc, 'extensions', 'memoria', 'dist', 'index.js'))).toBe(true)

    // openclaw.json correct
    const cfg = JSON.parse(readFileSync(join(oc, 'openclaw.json'), 'utf8'))
    expect(cfg.plugins.allow).toContain('memoria')
    expect(cfg.plugins.entries.memoria.enabled).toBe(true)
    expect(cfg.plugins.entries.memoria.hooks.allowConversationAccess).toBe(true) // ← LE point critique
    expect(cfg.plugins.entries.memoria.hooks.allowPromptInjection).toBe(true)
    expect(cfg.plugins.entries.memoria.config).toMatchObject({ token: 'tok-abc', instance: 'koda-1', storageRoot: '/data/memo' })
  })

  it('préserve le reste de la config existante (merge, pas écrasement)', () => {
    mkdirSync(oc, { recursive: true })
    writeFileSync(join(oc, 'openclaw.json'), JSON.stringify({ model: 'claude', mcp: { servers: { autre: {} } }, plugins: { allow: ['déjà'] } }))
    installOpenClawHooks({ instanceId: 'i', token: 't', openclawDir: oc, srcDir: src })
    const cfg = JSON.parse(readFileSync(join(oc, 'openclaw.json'), 'utf8'))
    expect(cfg.model).toBe('claude') // intact
    expect(cfg.mcp.servers.autre).toBeDefined() // intact
    expect(cfg.plugins.allow).toEqual(expect.arrayContaining(['déjà', 'memoria'])) // fusionné
  })

  it('round-trip : unregister retire le plugin et l’entrée, garde le reste', () => {
    mkdirSync(oc, { recursive: true })
    writeFileSync(join(oc, 'openclaw.json'), JSON.stringify({ model: 'x', plugins: { allow: ['memoria'], entries: { memoria: { enabled: true } } } }))
    installOpenClawHooks({ instanceId: 'i', token: 't', openclawDir: oc, srcDir: src })
    expect(existsSync(join(oc, 'extensions', 'memoria'))).toBe(true)

    const res = unregisterOpenClaw({ openclawDir: oc })
    expect(res.detail).toMatch(/retir/i)
    expect(existsSync(join(oc, 'extensions', 'memoria'))).toBe(false)
    const cfg = JSON.parse(readFileSync(join(oc, 'openclaw.json'), 'utf8'))
    expect(cfg.model).toBe('x') // intact
    expect(cfg.plugins.entries.memoria).toBeUndefined() // retiré
    expect(cfg.plugins.allow).not.toContain('memoria') // retiré
  })
})
