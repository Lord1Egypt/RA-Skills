/**
 * Détection des assistants IA installés sur CETTE machine (mission B1) :
 *  - CLI présente ? (`claude` / `codex` / `openclaw` / `cursor` --version)
 *  - données importables ? (transcripts .jsonl, base legacy OpenClaw)
 *  - déjà connecté à Memoria ? (croisement avec le registry)
 *
 * Tout est injectable pour les tests : `home` (jamais le vrai HOME en test),
 * `checkCli` (jamais les vrais binaires), `agents` (registre) et `machine`.
 * Les erreurs de parcours/lecture sont LOGGÉES, jamais avalées.
 */
import DatabaseCtor from 'better-sqlite3'
import { existsSync, readdirSync } from 'node:fs'
import { homedir, hostname } from 'node:os'
import { basename, join } from 'node:path'
import { cliInstalled } from './register.js'

export type DetectableAgentKind = 'claude-code' | 'codex' | 'openclaw' | 'cursor'

export interface DetectedLegacyDb {
  path: string
  fact_count: number
}

export interface DetectedAgentData {
  /** Nombre de fichiers de conversation importables (.jsonl). */
  transcript_files?: number
  /** Base mémoire legacy OpenClaw trouvée (lecture seule). */
  legacy_db?: DetectedLegacyDb
}

export interface DetectedAgent {
  kind: DetectableAgentKind
  /** Nom suggéré, affichable tel quel. */
  name: string
  /** CLI présente sur la machine. */
  installed: boolean
  data_found: DetectedAgentData
  /** instance_id si une instance non révoquée de ce type existe déjà pour cette machine. */
  already_connected: string | null
}

/** Vue minimale d'un agent du registry (forme de Memoria.listAgents()). */
export interface RegisteredAgentLike {
  instance: { id: string; machine_id: string; revoked_at: string | null }
  assistant_type: string
}

export interface DetectAgentsOptions {
  /** Racine HOME à inspecter (défaut : homedir()). */
  home?: string
  /** Sonde de présence d'un binaire (défaut : `<bin> --version`). */
  checkCli?: (bin: string) => boolean
  /** Agents du registry pour croiser `already_connected`. */
  agents?: RegisteredAgentLike[]
  /** Identifiant machine du registry (défaut : hostname()). */
  machine?: string
}

const AGENT_NAMES: Record<DetectableAgentKind, string> = {
  'claude-code': 'Claude Code',
  codex: 'Codex',
  openclaw: 'OpenClaw',
  cursor: 'Cursor',
}

const AGENT_CLIS: Record<DetectableAgentKind, string> = {
  'claude-code': 'claude',
  codex: 'codex',
  openclaw: 'openclaw',
  cursor: 'cursor',
}

/** Bornes du parcours disque (anti-explosion sur un HOME pathologique). */
const MAX_WALK_DEPTH = 6
const MAX_WALK_FILES = 20_000

/**
 * Parcours borné (profondeur + nombre) ; un dossier illisible est loggé et
 * ignoré (le reste de la détection continue).
 */
function walkFiles(dir: string, keep: (path: string) => boolean, out: string[], depth = 0): void {
  if (depth > MAX_WALK_DEPTH || out.length >= MAX_WALK_FILES) return
  let entries
  try {
    entries = readdirSync(dir, { withFileTypes: true })
  } catch (err) {
    console.warn(`[memoria] détection : lecture impossible de ${dir} : ${(err as Error).message}`)
    return
  }
  for (const entry of entries) {
    if (out.length >= MAX_WALK_FILES) return
    const p = join(dir, entry.name)
    if (entry.isDirectory()) walkFiles(p, keep, out, depth + 1)
    else if (entry.isFile() && keep(p)) out.push(p)
  }
}

/**
 * Fichiers de transcript importables pour un type d'agent :
 *  - claude-code → ~/.claude/projects/**\/*.jsonl
 *  - codex       → ~/.codex/sessions/**\/rollout-*.jsonl + ~/.codex/history.jsonl
 * Réutilisé par la détection (count) ET par le job d'import du daemon (liste).
 */
export function collectTranscriptFiles(kind: 'claude-code' | 'codex', home: string = homedir()): string[] {
  const out: string[] = []
  if (kind === 'claude-code') {
    const root = join(home, '.claude', 'projects')
    if (existsSync(root)) walkFiles(root, p => p.endsWith('.jsonl'), out)
  } else {
    const sessions = join(home, '.codex', 'sessions')
    if (existsSync(sessions)) walkFiles(sessions, p => basename(p).startsWith('rollout-') && p.endsWith('.jsonl'), out)
    const history = join(home, '.codex', 'history.jsonl')
    if (existsSync(history)) out.push(history)
  }
  return out.sort()
}

/** Compte les faits d'une base legacy en LECTURE SEULE. null = illisible (loggé). */
export function countLegacyFacts(path: string): number | null {
  try {
    const db = new DatabaseCtor(path, { readonly: true, fileMustExist: true })
    try {
      const r = db.prepare('SELECT COUNT(*) AS c FROM facts').get() as { c: number }
      return r.c
    } finally {
      db.close()
    }
  } catch (err) {
    console.warn(`[memoria] détection : base legacy illisible (${path}) : ${(err as Error).message}`)
    return null
  }
}

/**
 * Base legacy OpenClaw candidate : ~/.openclaw/workspace/memory/memoria.db en
 * premier, sinon recherche BORNÉE sous ~/.openclaw. Ignore les *-backup-* et
 * cortex.db (piège documenté AGENTS-RESEAU.md §39-41).
 */
export function findOpenClawLegacyDb(home: string = homedir()): DetectedLegacyDb | null {
  const ocDir = join(home, '.openclaw')
  const candidates: string[] = []
  const preferred = join(ocDir, 'workspace', 'memory', 'memoria.db')
  if (existsSync(preferred)) {
    candidates.push(preferred)
  } else if (existsSync(ocDir)) {
    walkFiles(ocDir, p => basename(p) === 'memoria.db' && !p.includes('-backup-'), candidates)
  }
  for (const path of candidates) {
    const count = countLegacyFacts(path)
    if (count !== null) return { path, fact_count: count }
  }
  return null
}

/**
 * Détecte les assistants présents sur la machine. Ne retourne QUE les agents
 * « intéressants » : CLI installée, OU données importables trouvées, OU déjà
 * connectés à Memoria. Tableau vide = machine vraiment vierge.
 */
export function detectAgents(opts: DetectAgentsOptions = {}): DetectedAgent[] {
  const home = opts.home ?? homedir()
  const checkCli = opts.checkCli ?? cliInstalled
  const machine = opts.machine ?? hostname()
  const registered = opts.agents ?? []

  const out: DetectedAgent[] = []
  for (const kind of ['claude-code', 'codex', 'openclaw', 'cursor'] as const) {
    const installed = checkCli(AGENT_CLIS[kind])

    const data: DetectedAgentData = {}
    if (kind === 'claude-code' || kind === 'codex') {
      const files = collectTranscriptFiles(kind, home)
      if (files.length > 0) data.transcript_files = files.length
    }
    if (kind === 'openclaw') {
      const legacy = findOpenClawLegacyDb(home)
      if (legacy) data.legacy_db = legacy
    }

    const connected = registered.find(
      a => a.assistant_type === kind && a.instance.revoked_at === null && a.instance.machine_id === machine,
    )

    const hasData = data.transcript_files !== undefined || data.legacy_db !== undefined
    if (!installed && !hasData && !connected) continue

    out.push({
      kind,
      name: AGENT_NAMES[kind],
      installed,
      data_found: data,
      already_connected: connected?.instance.id ?? null,
    })
  }
  return out
}
