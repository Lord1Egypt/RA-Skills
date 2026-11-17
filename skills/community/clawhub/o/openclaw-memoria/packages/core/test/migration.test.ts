/**
 * Tests migration legacy v3.34 → V3 (spec §7.1) :
 * import nominal (counts + quarantaine + FTS + mapping), idempotence,
 * dry-run, rollback, corruption (abort avant écriture), DB legacy jamais
 * modifiée. Tout sur DB synthétique au schéma v3.34 exact — jamais le réseau,
 * jamais le vrai HOME.
 */
import { existsSync, mkdtempSync, readFileSync, readdirSync, rmSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { Memoria } from '../src/engine/memoria.js'
import { ContentStore } from '../src/storage/content.js'
import { sha256Hex } from '../src/util.js'
import { createSyntheticLegacyDb, importLegacyDb } from '../src/migration/index.js'

let dir: string
let m: Memoria

beforeEach(() => {
  dir = mkdtempSync(join(tmpdir(), 'memoria-migration-'))
  m = Memoria.init({ storageRoot: join(dir, 'data'), configPath: join(dir, 'config.toml') })
  // Garde anti-réseau : tout appel fetch dans ce module est un bug.
  vi.stubGlobal('fetch', () => {
    throw new Error('réseau interdit dans les tests de migration')
  })
})

afterEach(() => {
  m.close()
  vi.unstubAllGlobals()
  vi.restoreAllMocks()
  rmSync(dir, { recursive: true, force: true })
})

const targetDbPath = () => join(dir, 'data', 'shared', 'legacy_to_review.sqlite')

function openTarget(): ContentStore {
  return new ContentStore(targetDbPath())
}

describe('import nominal', () => {
  it('importe ~50 faits FR en quarantaine : counts exacts, FTS, mapping, provenance', () => {
    const legacyPath = join(dir, 'memoria.db')
    const summary = createSyntheticLegacyDb(legacyPath)
    const hashBefore = sha256Hex(readFileSync(legacyPath))

    const report = importLegacyDb({ legacyPath, memoria: m })

    // Rapport
    expect(report.errors).toEqual([])
    expect(report.rolled_back).toBe(false)
    expect(report.facts_read).toBe(summary.facts)
    expect(report.facts_skipped_duplicates).toBe(summary.duplicateFacts)
    expect(report.facts_imported).toBe(summary.facts - summary.duplicateFacts)
    expect(report.procedures_read).toBe(summary.procedures)
    expect(report.procedures_imported).toBe(summary.procedures)
    expect(report.source_hash).toBe(hashBefore)

    // Embeddings legacy NON copiés, note explicite
    expect(summary.embeddings768).toBeGreaterThan(0)
    expect(summary.embeddings1536).toBeGreaterThan(0)
    expect(report.embeddings_skipped).toBe(summary.embeddings768 + summary.embeddings1536)
    expect(report.notes.some(n => n.includes('réindexation'))).toBe(true)

    // Backup créé sous backups/
    expect(report.backup_path).not.toBeNull()
    expect(existsSync(report.backup_path!)).toBe(true)
    expect(report.backup_path).toContain(join('data', 'backups'))

    const target = openTarget()
    try {
      // Counts cible
      expect(target.countFacts()).toBe(report.facts_imported)
      const sources = target.db.prepare('SELECT * FROM memory_sources').all() as Array<{ source_hash: string }>
      expect(sources).toHaveLength(1)
      expect(sources[0]!.source_hash).toBe(report.source_hash)
      const items = target.db
        .prepare("SELECT COUNT(*) AS c FROM memory_import_items WHERE status = 'pending'")
        .get() as { c: number }
      expect(items.c).toBe(report.facts_imported + report.procedures_imported)

      // Mapping : scope quarantaine + instance null partout
      const scope = m.registry.getScopeByName('legacy_to_review')!
      const offScope = target.db
        .prepare('SELECT COUNT(*) AS c FROM facts WHERE scope_id != ? OR assistant_instance_id IS NOT NULL')
        .get(scope.id) as { c: number }
      expect(offScope.c).toBe(0)

      // lifecycle mappé : fresh/settled → active, dormant conservé
      const f1 = target.getFact('fact_0001')! // fresh legacy
      expect(f1.lifecycle_state).toBe('active')
      const f2 = target.getFact('fact_0002')! // settled legacy
      expect(f2.lifecycle_state).toBe('active')
      const f3 = target.getFact('fact_0003')! // dormant legacy
      expect(f3.lifecycle_state).toBe('dormant')

      // superseded + created_at conservés (epoch ms → ISO)
      const f0 = target.getFact('fact_0000')!
      expect(f0.superseded).toBe(true)
      expect(f0.superseded_by).toBe('fact_0001')
      const base = Date.parse('2026-01-15T10:00:00.000Z')
      expect(f1.created_at).toBe(new Date(base + 60_000).toISOString())

      // tags JSON invalide → normalisé '[]' ; tags valides conservés
      const f6 = target.getFact('fact_0006')!
      expect(f6.tags).toEqual([])
      expect(f1.tags.length).toBeGreaterThan(0)

      // Aucun embedding copié dans la cible
      const emb = target.db.prepare('SELECT COUNT(*) AS c FROM embeddings').get() as { c: number }
      expect(emb.c).toBe(0)

      // FTS retrouve les sentinelles dans le scope quarantaine
      for (const id of summary.sentinelFactIds.slice(0, 5)) {
        const text = (target.getFact(id)!).fact
        const word = text
          .split(/[^\p{L}\p{N}_-]+/u)
          .filter(w => w.length >= 5)
          .sort((a, b) => b.length - a.length)[0]!
        const hits = target.searchFacts(word, { scopeIds: [scope.id], limit: 50 })
        expect(hits.some(h => h.row.id === id)).toBe(true)
      }

      // Procédures : failure_reasons absent du legacy → '[]'
      const proc = target.db.prepare("SELECT * FROM procedures WHERE id = 'proc_000'").get() as {
        failure_reasons: string
        scope_id: string
      }
      expect(proc.failure_reasons).toBe('[]')
      expect(proc.scope_id).toBe(scope.id)
    } finally {
      target.close()
    }

    // La DB legacy n'est JAMAIS modifiée (ouverture readonly)
    expect(sha256Hex(readFileSync(legacyPath))).toBe(hashBefore)
  })

  it('tolère les variantes de schéma (sans synced_to_md, sans extensions procedures)', () => {
    const legacyPath = join(dir, 'memoria-partial.db')
    const summary = createSyntheticLegacyDb(legacyPath, {
      factCount: 12,
      procedureCount: 2,
      withSyncedToMd: false,
      withProcedureExtensions: false,
    })

    const report = importLegacyDb({ legacyPath, memoria: m })
    expect(report.errors).toEqual([])
    expect(report.facts_imported).toBe(summary.facts - summary.duplicateFacts)
    expect(report.procedures_imported).toBe(summary.procedures)
  })
})

describe('idempotence', () => {
  it('re-import du même fichier = 0 nouveau (source_hash connu)', () => {
    const legacyPath = join(dir, 'memoria.db')
    const summary = createSyntheticLegacyDb(legacyPath)

    const first = importLegacyDb({ legacyPath, memoria: m })
    expect(first.facts_imported).toBe(summary.facts - summary.duplicateFacts)

    const second = importLegacyDb({ legacyPath, memoria: m })
    expect(second.errors).toEqual([])
    expect(second.facts_imported).toBe(0)
    expect(second.procedures_imported).toBe(0)
    expect(second.notes.some(n => n.includes('déjà importée'))).toBe(true)

    const target = openTarget()
    try {
      expect(target.countFacts()).toBe(first.facts_imported)
      const sources = target.db.prepare('SELECT COUNT(*) AS c FROM memory_sources').get() as { c: number }
      expect(sources.c).toBe(1)
    } finally {
      target.close()
    }
  })
})

describe('dry-run', () => {
  it('analyse sans AUCUNE écriture dans la cible', () => {
    const legacyPath = join(dir, 'memoria.db')
    const summary = createSyntheticLegacyDb(legacyPath)

    const report = importLegacyDb({ legacyPath, memoria: m, dryRun: true })
    expect(report.errors).toEqual([])
    expect(report.dry_run).toBe(true)
    expect(report.facts_read).toBe(summary.facts)
    expect(report.facts_imported).toBe(0)
    expect(report.notes.some(n => n.includes('dry-run'))).toBe(true)

    const target = openTarget()
    try {
      expect(target.countFacts()).toBe(0)
      const sources = target.db.prepare('SELECT COUNT(*) AS c FROM memory_sources').get() as { c: number }
      expect(sources.c).toBe(0)
      const items = target.db.prepare('SELECT COUNT(*) AS c FROM memory_import_items').get() as { c: number }
      expect(items.c).toBe(0)
    } finally {
      target.close()
    }
  })
})

describe('rollback', () => {
  it('échec de vérification injecté → cible entièrement nettoyée + rolled_back', () => {
    const warn = vi.spyOn(console, 'warn').mockImplementation(() => {})
    const legacyPath = join(dir, 'memoria.db')
    createSyntheticLegacyDb(legacyPath)
    const hashBefore = sha256Hex(readFileSync(legacyPath))

    const report = importLegacyDb({ legacyPath, memoria: m, forceVerifyFailureForTests: true })
    expect(report.rolled_back).toBe(true)
    expect(report.errors.some(e => e.includes('injecté'))).toBe(true)
    expect(report.facts_imported).toBe(0)
    expect(report.procedures_imported).toBe(0)
    // Le rollback n'est jamais silencieux
    expect(warn).toHaveBeenCalled()

    const target = openTarget()
    try {
      expect(target.countFacts()).toBe(0)
      for (const table of ['procedures', 'memory_sources', 'memory_import_items']) {
        const r = target.db.prepare(`SELECT COUNT(*) AS c FROM ${table}`).get() as { c: number }
        expect(r.c).toBe(0)
      }
      // FTS nettoyé avec (pas de fantômes)
      const fts = target.db.prepare('SELECT COUNT(*) AS c FROM facts_fts').get() as { c: number }
      expect(fts.c).toBe(0)
    } finally {
      target.close()
    }

    // Source intacte malgré le rollback
    expect(sha256Hex(readFileSync(legacyPath))).toBe(hashBefore)
  })
})

describe('corruption & pré-vol', () => {
  it('fichier non-SQLite → abort propre AVANT toute écriture', () => {
    const warn = vi.spyOn(console, 'warn').mockImplementation(() => {})
    const legacyPath = join(dir, 'garbage.db')
    writeFileSync(legacyPath, 'ceci n’est pas une base sqlite, juste du texte assez long pour dépasser le header')

    const report = importLegacyDb({ legacyPath, memoria: m })
    expect(report.errors.length).toBeGreaterThan(0)
    expect(report.rolled_back).toBe(false)
    expect(report.backup_path).toBeNull()
    expect(warn).toHaveBeenCalled()

    // Aucune écriture : pas de DB cible, pas de backup
    expect(existsSync(targetDbPath())).toBe(false)
    expect(readdirSync(join(dir, 'data', 'backups'))).toEqual([])
  })

  it('fichier tronqué → abort propre, source non touchée', () => {
    vi.spyOn(console, 'warn').mockImplementation(() => {})
    const fullPath = join(dir, 'memoria-full.db')
    createSyntheticLegacyDb(fullPath)
    const bytes = readFileSync(fullPath)
    const truncatedPath = join(dir, 'memoria-truncated.db')
    writeFileSync(truncatedPath, bytes.subarray(0, Math.floor(bytes.length / 2)))
    const hashBefore = sha256Hex(readFileSync(truncatedPath))

    const report = importLegacyDb({ legacyPath: truncatedPath, memoria: m })
    expect(report.errors.length).toBeGreaterThan(0)
    expect(report.rolled_back).toBe(false)
    expect(report.facts_imported).toBe(0)
    expect(existsSync(targetDbPath())).toBe(false)
    expect(sha256Hex(readFileSync(truncatedPath))).toBe(hashBefore)
  })

  it('fichier inexistant → abort propre', () => {
    vi.spyOn(console, 'warn').mockImplementation(() => {})
    const report = importLegacyDb({ legacyPath: join(dir, 'nexiste-pas.db'), memoria: m })
    expect(report.errors[0]).toContain('introuvable')
    expect(report.backup_path).toBeNull()
  })
})
