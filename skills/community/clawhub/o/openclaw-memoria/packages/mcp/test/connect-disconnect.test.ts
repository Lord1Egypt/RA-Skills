/**
 * connect/disconnect SIMPLES : une commande connecte + enregistre auto le MCP,
 * une commande déconnecte + désenregistre + révoque + nettoie. Tout injecté
 * (pas de vrai daemon, pas de vrai agent, credentials en tmpdir).
 */
import { mkdtempSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { connect } from '../src/connect.js'
import { disconnect } from '../src/disconnect.js'
import { listCredentials, loadCredentials } from '../src/credentials.js'
import type { RegisterResult } from '../src/register.js'

let dir: string

beforeEach(() => {
  dir = mkdtempSync(join(tmpdir(), 'memoria-creds-'))
})
afterEach(() => {
  rmSync(dir, { recursive: true, force: true })
})

const fakeEnsure = async () => ({ port: 0 })
const fakeClient = (type: string) => () => ({
  completePairing: async (code: string) => ({
    assistant_instance_id: `inst-${code}`,
    instance_token: 'tok-123',
    assistant_type: type,
  }),
})

describe('connect', () => {
  it('connecte ET enregistre automatiquement le serveur MCP (1 seule commande)', async () => {
    const registrar = vi.fn((host: string, id: string): RegisterResult => ({
      host: host as never,
      registered: true,
      detail: `enregistré pour ${host}/${id}`,
    }))
    const res = await connect({
      code: 'AAAA-BBBB',
      storageRoot: dir,
      credentialsDir: dir,
      ensure: fakeEnsure,
      clientFor: fakeClient('codex'),
      registrar,
    })
    expect(res.assistantType).toBe('codex')
    expect(registrar).toHaveBeenCalledWith('codex', 'inst-AAAA-BBBB', { token: 'tok-123', storageRoot: dir })
    expect(res.registration?.registered).toBe(true)
    expect(res.message).toContain('connecté')

    // credentials sauvegardés avec le type d'hôte (pour la déconnexion)
    const creds = loadCredentials('inst-AAAA-BBBB', dir)
    expect(creds?.instance_token).toBe('tok-123')
    expect(creds?.assistant_type).toBe('codex')
  })

  it('--no-register : pas d’enregistrement auto, instructions manuelles', async () => {
    const registrar = vi.fn()
    const res = await connect({
      code: 'CCCC-DDDD',
      storageRoot: dir,
      credentialsDir: dir,
      register: false,
      ensure: fakeEnsure,
      clientFor: fakeClient('claude-code'),
      registrar: registrar as never,
    })
    expect(registrar).not.toHaveBeenCalled()
    expect(res.registration).toBeNull()
    expect(res.message).toContain('manuel')
  })
})

describe('disconnect', () => {
  it('désenregistre + révoque + supprime les credentials', async () => {
    // d'abord connecter
    await connect({
      code: 'EEEE-FFFF',
      storageRoot: dir,
      credentialsDir: dir,
      ensure: fakeEnsure,
      clientFor: fakeClient('claude-code'),
      registrar: () => ({ host: 'claude-code', registered: true, detail: 'ok' }),
    })
    expect(listCredentials(dir)).toHaveLength(1)

    const unregistrar = vi.fn((host: string): RegisterResult => ({ host: host as never, registered: false, detail: `retiré ${host}` }))
    const revoker = vi.fn(async () => {})
    const res = await disconnect({
      storageRoot: dir,
      credentialsDir: dir,
      stateFor: () => ({ daemon_id: 'd', port: 0, admin_token: 'a', pid: 1, started_at: '' }),
      revoker,
      unregistrar,
    })

    expect(unregistrar).toHaveBeenCalledWith('claude-code')
    expect(revoker).toHaveBeenCalledWith(expect.anything(), 'inst-EEEE-FFFF')
    expect(res.revoked).toBe(true)
    expect(res.credentialsDeleted).toBe(true)
    expect(listCredentials(dir)).toHaveLength(0)
  })

  it('sans --instance et plusieurs agents → demande de préciser', async () => {
    for (const code of ['A-A', 'B-B']) {
      await connect({
        code, storageRoot: dir, credentialsDir: dir, ensure: fakeEnsure,
        clientFor: fakeClient('codex'), registrar: () => ({ host: 'codex', registered: true, detail: 'ok' }),
      })
    }
    await expect(
      disconnect({ storageRoot: dir, credentialsDir: dir, stateFor: () => null, unregistrar: () => ({ host: 'codex', registered: false, detail: '' }) }),
    ).rejects.toThrow(/précise --instance/)
  })

  it('daemon éteint : nettoyage local quand même (best-effort)', async () => {
    await connect({
      code: 'G-G', storageRoot: dir, credentialsDir: dir, ensure: fakeEnsure,
      clientFor: fakeClient('openclaw'), registrar: () => ({ host: 'openclaw', registered: true, detail: 'ok' }),
    })
    const res = await disconnect({
      storageRoot: dir, credentialsDir: dir,
      stateFor: () => null, // daemon absent
      unregistrar: () => ({ host: 'openclaw', registered: false, detail: 'retiré' }),
    })
    expect(res.revoked).toBe(false)
    expect(res.credentialsDeleted).toBe(true)
  })
})
