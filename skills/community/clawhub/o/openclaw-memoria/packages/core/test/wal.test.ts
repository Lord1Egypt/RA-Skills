/**
 * Tests WalProcessor (spec §6.2 étapes 1 et 7) — la pièce « rien ne se perd » :
 * retry borné, abandon audité via onPermanentFailure, replay crash/restart
 * exactement-une-fois, cleanup borné. Corrige WAL-1/WAL-2 du legacy.
 */
import { mkdtempSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { ContentStore } from '../src/storage/content.js'
import { WalProcessor, type ProcessOutcome } from '../src/engine/wal.js'
import type { WalEntry } from '../src/types.js'

let dir: string
let store: ContentStore

const done = (facts = 0): ProcessOutcome => ({ status: 'done', facts_created: facts })

beforeEach(() => {
  dir = mkdtempSync(join(tmpdir(), 'memoria-wal-'))
  store = new ContentStore(join(dir, 'memory.sqlite'))
  // Aucun test ne touche le réseau — fetch interdit par construction.
  vi.stubGlobal('fetch', () => {
    throw new Error('réseau interdit dans les tests')
  })
})

afterEach(() => {
  store.close()
  rmSync(dir, { recursive: true, force: true })
  vi.unstubAllGlobals()
  vi.restoreAllMocks()
})

describe('échecs : retry borné, jamais muet', () => {
  it('échec transitoire → reste pending avec attempts++ et un warn AVEC l’id', async () => {
    const warn = vi.spyOn(console, 'warn').mockImplementation(() => {})
    const id = store.walAppend('inst-1', 'user', 'message à traiter')

    let fail = true
    const processor = new WalProcessor({
      store,
      processEntry: () => (fail ? Promise.reject(new Error('LLM timeout')) : Promise.resolve(done(1))),
    })

    const run1 = await processor.processPending()
    expect(run1.failed).toBe(1)
    expect(run1.processed).toBe(0)
    const pending = store.walPending(10)
    expect(pending).toHaveLength(1)
    expect(pending[0]!.attempts).toBe(1)
    expect(warn).toHaveBeenCalledWith(expect.stringContaining(`WAL #${id}`))

    // le retry suivant réussit → consommée, plus pending
    fail = false
    const run2 = await processor.processPending()
    expect(run2.processed).toBe(1)
    expect(run2.facts_created).toBe(1)
    expect(store.walPendingCount()).toBe(0)
  })

  it('échec permanent (maxAttempts) → markProcessed + onPermanentFailure, contenu conservé en table', async () => {
    vi.spyOn(console, 'warn').mockImplementation(() => {})
    store.walAppend('inst-1', 'user', 'message condamné')

    const abandoned: WalEntry[] = []
    const processor = new WalProcessor({
      store,
      maxAttempts: 2,
      processEntry: () => Promise.reject(new Error('échec définitif')),
      onPermanentFailure: entry => {
        abandoned.push(entry)
      },
    })

    const run1 = await processor.processPending()
    expect(run1.failed).toBe(1)
    expect(run1.abandoned).toBe(0)

    const run2 = await processor.processPending()
    expect(run2.abandoned).toBe(1)
    expect(abandoned).toHaveLength(1)
    expect(abandoned[0]!.attempts).toBe(2)

    // sortie de la file (anti-boucle) MAIS ligne conservée : zéro perte silencieuse
    expect(store.walPendingCount()).toBe(0)
    const row = store.db
      .prepare('SELECT processed, content FROM wal_buffer WHERE id = ?')
      .get(abandoned[0]!.id) as { processed: number; content: string }
    expect(row.processed).toBe(1)
    expect(row.content).toBe('message condamné')

    // run suivant : plus jamais re-tenté (pas de boucle infinie)
    const run3 = await processor.processPending()
    expect(run3.failed + run3.abandoned + run3.processed).toBe(0)
  })

  it('outcome defer (no-llm) → reste pending SANS tentative comptée', async () => {
    store.walAppend('inst-1', 'user', 'en attente de LLM')
    const processor = new WalProcessor({
      store,
      processEntry: () => Promise.resolve({ status: 'defer', reason: 'no-llm' }),
    })
    const run = await processor.processPending()
    expect(run.deferred).toBe(1)
    const pending = store.walPending(10)
    expect(pending).toHaveLength(1)
    expect(pending[0]!.attempts).toBe(0) // un défaut d'infra ne brûle pas le budget de retry
  })
})

describe('crash/restart : replay exactement-une-fois', () => {
  it('nouveau WalProcessor sur la même DB → 0 perte, 0 doublon', async () => {
    // 3 messages appendés puis « crash » avant tout traitement
    store.walAppend('inst-1', 'user', 'tour 1 — message utilisateur')
    store.walAppend('inst-1', 'assistant', 'tour 1 — réponse assistant')
    store.walAppend('inst-1', 'user', 'tour 2 — message utilisateur')
    store.close()

    // redémarrage : nouvelle connexion, nouveau processor
    store = new ContentStore(join(dir, 'memory.sqlite'))
    const processedIds = new Map<number, number>()
    const processor = new WalProcessor({
      store,
      processEntry: entry => {
        processedIds.set(entry.id, (processedIds.get(entry.id) ?? 0) + 1)
        return Promise.resolve(done(1))
      },
    })

    const replay = await processor.replayAtBoot()
    expect(replay.processed).toBe(3)
    expect(replay.facts_created).toBe(3)
    expect(store.walPendingCount()).toBe(0)
    expect([...processedIds.values()]).toEqual([1, 1, 1]) // chacune exactement une fois

    // 2e boot : rien à rejouer, aucun doublon
    const replay2 = await processor.replayAtBoot()
    expect(replay2.processed).toBe(0)
    expect([...processedIds.values()]).toEqual([1, 1, 1])
  })

  it('cleanup borné après replay (anti table illimitée du legacy)', async () => {
    for (let i = 0; i < 5; i++) store.walAppend('inst-1', 'user', `message ${i}`)
    const processor = new WalProcessor({
      store,
      processEntry: () => Promise.resolve(done(0)),
      cleanupMaxRows: 2,
      cleanupMaxAgeDays: 30,
    })

    const replay = await processor.replayAtBoot()
    expect(replay.processed).toBe(5)
    expect(replay.cleaned).toBe(3) // 5 traitées, on n'en garde que les 2 plus récentes

    const rows = store.db.prepare('SELECT COUNT(*) AS c FROM wal_buffer').get() as { c: number }
    expect(rows.c).toBe(2)
  })
})
