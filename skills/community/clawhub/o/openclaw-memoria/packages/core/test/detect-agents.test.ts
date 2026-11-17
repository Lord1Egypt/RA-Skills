/**
 * detectAgents (mission B1) : CLI présente, données importables (transcripts /
 * base legacy OpenClaw), croisement registry (already_connected). Tout injecté :
 * faux HOME en tmpdir, sonde CLI stubée, jamais les vrais binaires.
 */
import Database from 'better-sqlite3'
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { afterEach, beforeEach, describe, expect, it } from 'vitest'
import {
  collectTranscriptFiles,
  countLegacyFacts,
  detectAgents,
  findOpenClawLegacyDb,
} from '../src/agents/detect.js'

let home: string

beforeEach(() => {
  home = mkdtempSync(join(tmpdir(), 'memoria-detect-'))
})

afterEach(() => {
  rmSync(home, { recursive: true, force: true })
})

/** Faux fichier .jsonl (le contenu n'importe pas pour la détection). */
function touch(path: string, content = '{}'): void {
  mkdirSync(join(path, '..'), { recursive: true })
  writeFileSync(path, content)
}

/** Base legacy minimale : table facts + n lignes. */
function makeLegacyDb(path: string, facts: number): void {
  mkdirSync(join(path, '..'), { recursive: true })
  const db = new Database(path)
  db.exec('CREATE TABLE facts (id TEXT PRIMARY KEY, fact TEXT NOT NULL)')
  const insert = db.prepare('INSERT INTO facts (id, fact) VALUES (?, ?)')
  for (let i = 0; i < facts; i++) insert.run(`f${i}`, `souvenir numéro ${i}`)
  db.close()
}

describe('collectTranscriptFiles', () => {
  it('claude-code : tous les .jsonl sous ~/.claude/projects/**', () => {
    touch(join(home, '.claude', 'projects', 'proj-a', 'conv1.jsonl'))
    touch(join(home, '.claude', 'projects', 'proj-a', 'conv2.jsonl'))
    touch(join(home, '.claude', 'projects', 'proj-b', 'sub', 'conv3.jsonl'))
    touch(join(home, '.claude', 'projects', 'proj-b', 'notes.txt')) // ignoré
    const files = collectTranscriptFiles('claude-code', home)
    expect(files).toHaveLength(3)
    expect(files.every(f => f.endsWith('.jsonl'))).toBe(true)
  })

  it('codex : rollout-*.jsonl sous sessions/** + history.jsonl', () => {
    touch(join(home, '.codex', 'sessions', '2026', '06', '01', 'rollout-abc.jsonl'))
    touch(join(home, '.codex', 'sessions', '2026', '06', '02', 'rollout-def.jsonl'))
    touch(join(home, '.codex', 'sessions', '2026', '06', '02', 'autre.jsonl')) // pas rollout-* : ignoré
    touch(join(home, '.codex', 'history.jsonl'))
    const files = collectTranscriptFiles('codex', home)
    expect(files).toHaveLength(3)
    expect(files.filter(f => f.endsWith('history.jsonl'))).toHaveLength(1)
  })

  it('HOME vide : aucun fichier, aucun crash', () => {
    expect(collectTranscriptFiles('claude-code', home)).toHaveLength(0)
    expect(collectTranscriptFiles('codex', home)).toHaveLength(0)
  })
})

describe('findOpenClawLegacyDb', () => {
  it('priorité au chemin canonique workspace/memory/memoria.db', () => {
    makeLegacyDb(join(home, '.openclaw', 'workspace', 'memory', 'memoria.db'), 5)
    const found = findOpenClawLegacyDb(home)
    expect(found?.fact_count).toBe(5)
    expect(found?.path.endsWith(join('workspace', 'memory', 'memoria.db'))).toBe(true)
  })

  it('repli : recherche bornée sous ~/.openclaw, ignore *-backup-* et cortex.db', () => {
    makeLegacyDb(join(home, '.openclaw', 'autre-dossier', 'memoria.db'), 7)
    makeLegacyDb(join(home, '.openclaw', 'memoria-backup-2026', 'memoria.db'), 99) // ignoré (-backup-)
    makeLegacyDb(join(home, '.openclaw', 'autre-dossier', 'cortex.db'), 50) // ignoré (pas memoria.db)
    const found = findOpenClawLegacyDb(home)
    expect(found?.fact_count).toBe(7)
    expect(found?.path).toContain('autre-dossier')
  })

  it('aucune base : null, et un fichier corrompu est ignoré (loggé)', () => {
    expect(findOpenClawLegacyDb(home)).toBeNull()
    // fichier qui n'est pas une DB SQLite → countLegacyFacts retourne null
    const bogus = join(home, '.openclaw', 'workspace', 'memory', 'memoria.db')
    touch(bogus, 'pas une base sqlite')
    expect(countLegacyFacts(bogus)).toBeNull()
    expect(findOpenClawLegacyDb(home)).toBeNull()
  })
})

describe('detectAgents', () => {
  it('croise CLI + données + registry pour already_connected', () => {
    // données : 2 conv Claude, 1 rollout + history Codex, 3 souvenirs OpenClaw
    touch(join(home, '.claude', 'projects', 'p', 'a.jsonl'))
    touch(join(home, '.claude', 'projects', 'p', 'b.jsonl'))
    touch(join(home, '.codex', 'sessions', '2026', 'rollout-x.jsonl'))
    touch(join(home, '.codex', 'history.jsonl'))
    makeLegacyDb(join(home, '.openclaw', 'workspace', 'memory', 'memoria.db'), 3)

    const checkCli = (bin: string) => bin === 'claude' || bin === 'openclaw'
    const agents = detectAgents({
      home,
      checkCli,
      machine: 'imac-test',
      agents: [
        // claude-code connecté sur CETTE machine → already_connected
        { instance: { id: 'inst-claude', machine_id: 'imac-test', revoked_at: null }, assistant_type: 'claude-code' },
        // codex connecté mais RÉVOQUÉ → pas connecté
        { instance: { id: 'inst-codex', machine_id: 'imac-test', revoked_at: '2026-06-01T00:00:00.000Z' }, assistant_type: 'codex' },
        // openclaw connecté sur une AUTRE machine → pas connecté ici
        { instance: { id: 'inst-oc', machine_id: 'autre-machine', revoked_at: null }, assistant_type: 'openclaw' },
      ],
    })

    const byKind = new Map(agents.map(a => [a.kind, a]))

    const claude = byKind.get('claude-code')
    expect(claude).toMatchObject({ installed: true, already_connected: 'inst-claude', name: 'Claude Code' })
    expect(claude?.data_found.transcript_files).toBe(2)

    const codex = byKind.get('codex')
    expect(codex).toMatchObject({ installed: false, already_connected: null })
    expect(codex?.data_found.transcript_files).toBe(2) // rollout + history

    const openclaw = byKind.get('openclaw')
    expect(openclaw).toMatchObject({ installed: true, already_connected: null })
    expect(openclaw?.data_found.legacy_db?.fact_count).toBe(3)

    // cursor : ni CLI, ni données, ni connexion → absent du résultat
    expect(byKind.has('cursor')).toBe(false)
  })

  it('machine vierge : tableau vide', () => {
    expect(detectAgents({ home, checkCli: () => false, machine: 'vierge', agents: [] })).toHaveLength(0)
  })

  it('cursor : retourné si la CLI est présente (sans données)', () => {
    const agents = detectAgents({ home, checkCli: bin => bin === 'cursor', machine: 'm', agents: [] })
    expect(agents).toHaveLength(1)
    expect(agents[0]).toMatchObject({ kind: 'cursor', installed: true, already_connected: null })
    expect(agents[0]?.data_found).toEqual({})
  })
})
