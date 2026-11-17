/**
 * Tests stockage : resolveStorageRoot (résolveur UNIQUE), migrations,
 * triggers FTS (anti-bug rebuildFts), WAL borné, garde réseau.
 */
import { mkdtempSync, rmSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { afterEach, beforeEach, describe, expect, it } from 'vitest'
import { ContentStore, isOnNetworkVolume, resolveStorageRoot } from '../src/index.js'

let dir: string

beforeEach(() => {
  dir = mkdtempSync(join(tmpdir(), 'memoria-storage-'))
})

afterEach(() => {
  rmSync(dir, { recursive: true, force: true })
})

describe('resolveStorageRoot — précédence', () => {
  it('param explicite > config.toml > env > défaut', () => {
    const cfgPath = join(dir, 'config.toml')

    // défaut (pas de config, pas d'env)
    const byDefault = resolveStorageRoot({ configPath: cfgPath, env: {} })
    expect(byDefault.storageRoot).toContain('.memoria')

    // env
    const byEnv = resolveStorageRoot({ configPath: cfgPath, env: { MEMORIA_HOME: join(dir, 'from-env') } })
    expect(byEnv.storageRoot).toBe(join(dir, 'from-env'))

    // config.toml bat l'env
    writeFileSync(cfgPath, `storage_path = "${join(dir, 'from-config')}"\n`)
    const byConfig = resolveStorageRoot({ configPath: cfgPath, env: { MEMORIA_HOME: join(dir, 'from-env') } })
    expect(byConfig.storageRoot).toBe(join(dir, 'from-config'))

    // param explicite bat tout
    const byParam = resolveStorageRoot({
      configPath: cfgPath,
      env: { MEMORIA_HOME: join(dir, 'from-env') },
      storageRoot: join(dir, 'explicit'),
    })
    expect(byParam.storageRoot).toBe(join(dir, 'explicit'))
  })
})

describe('FTS — synchronisation par triggers (anti rebuildFts désaligné)', () => {
  it('insert / update / delete restent alignés sans rebuild manuel', () => {
    const store = new ContentStore(join(dir, 'content.sqlite'))
    const f = store.insertFact({ fact: 'le serveur tourne sur le port 8080', scope_id: 's1' })

    expect(store.searchFacts('serveur port', { scopeIds: ['s1'] })).toHaveLength(1)

    // update → l'index suit
    store.db.prepare('UPDATE facts SET fact = ? WHERE id = ?').run('le daemon écoute sur le port 9090', f.id)
    expect(store.searchFacts('serveur', { scopeIds: ['s1'] })).toHaveLength(0)
    expect(store.searchFacts('daemon 9090', { scopeIds: ['s1'] })).toHaveLength(1)

    // delete → plus de fantôme
    store.hardDeleteFacts([f.id])
    expect(store.searchFacts('daemon', { scopeIds: ['s1'] })).toHaveLength(0)
    const ghost = store.db.prepare("SELECT COUNT(*) AS c FROM facts_fts WHERE facts_fts MATCH 'daemon'").get() as { c: number }
    expect(ghost.c).toBe(0)
    store.close()
  })

  it('le pré-filtre exclut superseded / archived / sensibilité', () => {
    const store = new ContentStore(join(dir, 'content2.sqlite'))
    const a = store.insertFact({ fact: 'config nginx ancienne', scope_id: 's1' })
    store.insertFact({ fact: 'config nginx récente', scope_id: 's1' })
    store.insertFact({ fact: 'config nginx ultra-secrète', scope_id: 's1', sensitivity: 'critical' })
    store.db.prepare('UPDATE facts SET superseded = 1 WHERE id = ?').run(a.id)

    const hits = store.searchFacts('config nginx', { scopeIds: ['s1'], maxSensitivity: 'sensitive' })
    expect(hits).toHaveLength(1)
    expect(hits[0]!.row.fact).toBe('config nginx récente')
    store.close()
  })
})

describe('WAL buffer — borné (anti table illimitée du legacy)', () => {
  it('append → pending → markProcessed → cleanup', () => {
    const store = new ContentStore(join(dir, 'wal.sqlite'))
    for (let i = 0; i < 20; i++) store.walAppend('inst-1', 'user', `message ${i}`)
    expect(store.walPendingCount()).toBe(20)

    const pending = store.walPending(50)
    store.walMarkProcessed(pending.map(p => p.id))
    expect(store.walPendingCount()).toBe(0)

    // cleanup borné : on garde au plus maxRows traités
    const purged = store.walCleanup(5, 14)
    expect(purged).toBe(15)
    const left = store.db.prepare('SELECT COUNT(*) AS c FROM wal_buffer').get() as { c: number }
    expect(left.c).toBe(5)
    store.close()
  })
})

describe('garde réseau', () => {
  it('détecte les chemins réseau/synchronisés notoires (selon la plateforme)', () => {
    if (process.platform === 'darwin') {
      // /Volumes/* n'a de sens que sur macOS — la garde est gated par plateforme
      expect(isOnNetworkVolume('/Volumes/NAS-QNAP/memoria/data')).toBe(true)
    }
    expect(isOnNetworkVolume(`${process.env['HOME']}/Library/Mobile Documents/com~apple~CloudDocs/memoria`)).toBe(true)
    expect(isOnNetworkVolume(`${process.env['HOME']}/Dropbox/memoria`)).toBe(true)
    expect(isOnNetworkVolume(dir)).toBe(false)
  })
})
