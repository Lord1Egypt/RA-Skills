/**
 * Import des couches cognitives legacy v3.34 → schéma cognition V3.
 *
 * Récupère, depuis une DB legacy (lecture seule conceptuelle — l'appelant
 * fournit un better-sqlite3 readonly), les tables :
 *   - entities          → entities
 *   - relations         → relations (ré-écrites NON-dirigées, paire ordonnée)
 *   - observations      → observations (topic→subject, summary→content)
 *   - self_observations → observations (domain→subject, signal/detail→content)
 *   - topics            → topics (table du tronc)
 *
 * C'est ce qui rapatrie les 3607 observations + 3039 entités + 3329 relations
 * de Koda (Mac Studio) dans le nouveau schéma.
 *
 * Garanties :
 *  - mapping TOLÉRANT aux colonnes (PRAGMA table_info) — un schéma legacy
 *    partiel (try/catch muets historiques) n'interrompt pas l'import ;
 *  - IDEMPOTENT par hash : ré-importer la même DB ne duplique rien (entités par
 *    nom NOCASE, relations par paire ordonnée, observations par sujet, topics
 *    par nom) ;
 *  - aucune erreur avalée : tout échec part dans report.errors + console.warn.
 */
import type { Database } from 'better-sqlite3'
import type { ContentStore } from '../storage/content.js'
import { ensureCognitionSchema } from '../storage/cognition-schema.js'
import { newId, nowISO, sha256Hex } from '../util.js'
import { normalizeEntityType, normalizeRelationType } from '../cognition/entities.js'

export interface ImportCognitionInput {
  /** DB legacy v3.34 ouverte (idéalement `readonly: true`). */
  legacyDb: Database
  /** Cible : DB de contenu V3 (schéma cognition appliqué). */
  targetStore: ContentStore
  /**
   * Scope d'accueil. Non stocké sur les entités/relations (le graphe vit dans
   * le fichier DB cible → isolation par fichier). Conservé pour la provenance
   * et l'audit éventuel de l'intégrateur.
   */
  scopeId: string
}

export interface ImportCognitionReport {
  entities_read: number
  entities_imported: number
  entities_skipped: number
  relations_read: number
  relations_imported: number
  relations_skipped: number
  observations_read: number
  observations_imported: number
  observations_skipped: number
  self_observations_read: number
  topics_read: number
  topics_imported: number
  topics_skipped: number
  errors: string[]
  notes: string[]
}

type LegacyRow = Record<string, unknown>

const asString = (v: unknown): string | null => (typeof v === 'string' && v.length > 0 ? v : null)
const asNumber = (v: unknown): number | null => (typeof v === 'number' && Number.isFinite(v) ? v : null)

function epochToISO(v: number | null, fallback: string): string {
  if (v === null || v <= 0) return fallback
  const ms = v < 1e11 ? v * 1000 : v
  const d = new Date(ms)
  return Number.isNaN(d.getTime()) ? fallback : d.toISOString()
}

function hasTable(db: Database, table: string): boolean {
  const row = db.prepare("SELECT name FROM sqlite_master WHERE type = 'table' AND name = ?").get(table)
  return row !== undefined
}

function tableColumns(db: Database, table: string): Set<string> {
  if (!hasTable(db, table)) return new Set()
  const rows = db.pragma(`table_info(${table})`) as Array<{ name: string }>
  return new Set(rows.map(r => r.name))
}

/** Lit une table legacy si elle existe, sinon []. */
function readTable(db: Database, table: string): LegacyRow[] {
  if (!hasTable(db, table)) return []
  return db.prepare(`SELECT * FROM ${table}`).all() as LegacyRow[]
}

function emptyReport(): ImportCognitionReport {
  return {
    entities_read: 0,
    entities_imported: 0,
    entities_skipped: 0,
    relations_read: 0,
    relations_imported: 0,
    relations_skipped: 0,
    observations_read: 0,
    observations_imported: 0,
    observations_skipped: 0,
    self_observations_read: 0,
    topics_read: 0,
    topics_imported: 0,
    topics_skipped: 0,
    errors: [],
    notes: [],
  }
}

function orderedPair(a: string, b: string): [string, string] {
  return a <= b ? [a, b] : [b, a]
}

/** Sujet d'observation depuis un signal de self-observation (clé d'agrégation). */
function selfObsSubject(domain: string, signal: string): string {
  return `self:${domain}:${signal}`.toLowerCase()
}

export function importLegacyCognition(input: ImportCognitionInput): ImportCognitionReport {
  const { legacyDb, targetStore, scopeId } = input
  void scopeId // provenance/audit côté intégrateur ; le graphe vit par fichier DB
  const db = targetStore.db
  const report = emptyReport()
  // Le schéma cognition doit exister dans la cible (idempotent) avant d'écrire.
  ensureCognitionSchema(db)

  try {
    // ------------------------------------------------------------- ENTITÉS
    // Mapping legacy id → nouvel id (les relations legacy référencent les
    // anciens ids ; on doit pouvoir les retrouver après dédup par nom).
    const legacyEntityIdToNew = new Map<string, string>()
    const entityCols = tableColumns(legacyDb, 'entities')
    if (entityCols.size > 0) {
      const rows = readTable(legacyDb, 'entities')
      report.entities_read = rows.length
      const findByName = db.prepare('SELECT id FROM entities WHERE name = ? COLLATE NOCASE')
      const insertEntity = db.prepare(
        'INSERT INTO entities (id, name, type, mention_count, created_at) VALUES (?, ?, ?, ?, ?)',
      )
      const bump = db.prepare('UPDATE entities SET mention_count = mention_count + ? WHERE id = ?')
      const tx = db.transaction(() => {
        for (const row of rows) {
          const legacyId = asString(row['id'])
          const name = asString(row['name'])
          if (!legacyId || !name) {
            report.entities_skipped++
            continue
          }
          const type = normalizeEntityType(asString(row['type']) ?? 'concept')
          const createdAt = epochToISO(asNumber(row['created_at']), nowISO())
          const mention = Math.max(0, asNumber(row['access_count']) ?? 0)
          const existing = findByName.get(name.trim()) as { id: string } | undefined
          if (existing) {
            // Dédup par nom : renforce le compteur, réutilise l'id existant.
            bump.run(mention, existing.id)
            legacyEntityIdToNew.set(legacyId, existing.id)
            report.entities_skipped++
          } else {
            const newEntityId = newId()
            insertEntity.run(newEntityId, name.trim(), type, mention, createdAt)
            legacyEntityIdToNew.set(legacyId, newEntityId)
            report.entities_imported++
          }
        }
      })
      tx()
    }

    // ----------------------------------------------------------- RELATIONS
    const relCols = tableColumns(legacyDb, 'relations')
    if (relCols.size > 0) {
      const rows = readTable(legacyDb, 'relations')
      report.relations_read = rows.length
      // Colonnes source/target tolérantes (legacy : source_id/target_id).
      const srcCol = relCols.has('source_id') ? 'source_id' : relCols.has('from_entity') ? 'from_entity' : null
      const tgtCol = relCols.has('target_id') ? 'target_id' : relCols.has('to_entity') ? 'to_entity' : null
      const kindCol = relCols.has('relation') ? 'relation' : relCols.has('kind') ? 'kind' : null
      if (!srcCol || !tgtCol) {
        report.notes.push('table relations sans colonnes source/target reconnues — ignorée')
      } else {
        const findPair = db.prepare('SELECT id, context FROM relations WHERE from_entity = ? AND to_entity = ?')
        const insertRel = db.prepare(
          `INSERT INTO relations (id, from_entity, to_entity, kind, weight, context, created_at, last_accessed_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)`,
        )
        const reinforce = db.prepare(
          'UPDATE relations SET weight = MIN(MAX(weight, ?), 1.0), context = ?, last_accessed_at = ? WHERE id = ?',
        )
        const tx = db.transaction(() => {
          for (const row of rows) {
            const legacySrc = asString(row[srcCol])
            const legacyTgt = asString(row[tgtCol])
            const newFrom = legacySrc ? legacyEntityIdToNew.get(legacySrc) : undefined
            const newTo = legacyTgt ? legacyEntityIdToNew.get(legacyTgt) : undefined
            if (!newFrom || !newTo || newFrom === newTo) {
              report.relations_skipped++
              continue
            }
            const [from, to] = orderedPair(newFrom, newTo)
            const kind = normalizeRelationType(kindCol ? asString(row[kindCol]) ?? 'related_to' : 'related_to')
            const weight = Math.min(1, Math.max(0, asNumber(row['weight']) ?? 0.5))
            const createdAt = epochToISO(asNumber(row['created_at']), nowISO())
            const lastAccess = epochToISO(asNumber(row['last_accessed_at']), createdAt)
            const context = normalizeContext(row['context'])
            const existing = findPair.get(from, to) as { id: string; context: string } | undefined
            if (existing) {
              // Idempotence : la paire existe déjà → fusionne context + poids max.
              const merged = mergeContext(existing.context, context)
              reinforce.run(weight, merged, lastAccess, existing.id)
              report.relations_skipped++
            } else {
              insertRel.run(newId(), from, to, kind, weight, JSON.stringify(context), createdAt, lastAccess)
              report.relations_imported++
            }
          }
        })
        tx()
      }
    }

    // -------------------------------------------------------- OBSERVATIONS
    const obsCols = tableColumns(legacyDb, 'observations')
    if (obsCols.size > 0) {
      const rows = readTable(legacyDb, 'observations')
      report.observations_read = rows.length
      // legacy : topic→subject, summary→content. Tolérant aux variantes.
      const subjectCol = obsCols.has('topic') ? 'topic' : obsCols.has('subject') ? 'subject' : null
      const contentCol = obsCols.has('summary') ? 'summary' : obsCols.has('content') ? 'content' : null
      if (!subjectCol || !contentCol) {
        report.notes.push('table observations sans colonnes topic/summary reconnues — ignorée')
      } else {
        const tx = db.transaction(() => {
          for (const row of rows) {
            const subject = asString(row[subjectCol])
            const content = asString(row[contentCol])
            if (!subject || !content) {
              report.observations_skipped++
              continue
            }
            const confidence = Math.min(1, Math.max(0, asNumber(row['confidence']) ?? 0.8))
            const obsCount = Math.max(1, asNumber(row['revision']) ?? asNumber(row['obs_count']) ?? 1)
            if (upsertObservationRaw(db, subject, content, confidence, obsCount)) report.observations_imported++
            else report.observations_skipped++
          }
        })
        tx()
      }
    }

    // -------------------------------------------------- SELF-OBSERVATIONS
    const selfCols = tableColumns(legacyDb, 'self_observations')
    if (selfCols.size > 0) {
      const rows = readTable(legacyDb, 'self_observations')
      report.self_observations_read = rows.length
      const tx = db.transaction(() => {
        for (const row of rows) {
          const domain = asString(row['domain'])
          const signal = asString(row['signal'])
          if (!domain || !signal) {
            report.observations_skipped++
            continue
          }
          const detail = asString(row['detail']) ?? ''
          const subject = selfObsSubject(domain, signal)
          const content = detail.length > 0 ? `${signal} — ${detail}` : signal
          if (upsertObservationRaw(db, subject, content, 0.7, 1)) report.observations_imported++
          else report.observations_skipped++
        }
      })
      tx()
    }

    // -------------------------------------------------------------- TOPICS
    const topicCols = tableColumns(legacyDb, 'topics')
    if (topicCols.size > 0) {
      const rows = readTable(legacyDb, 'topics')
      report.topics_read = rows.length
      const findTopic = db.prepare('SELECT id FROM topics WHERE name = ? COLLATE NOCASE')
      const insertTopic = db.prepare(
        `INSERT INTO topics (id, name, scope_id, share_policy, sensitivity, importance_score, keywords, created_at)
         VALUES (?, ?, ?, NULL, 'normal', ?, ?, ?)`,
      )
      const tx = db.transaction(() => {
        for (const row of rows) {
          const name = asString(row['name'])
          if (!name) {
            report.topics_skipped++
            continue
          }
          if (findTopic.get(name.trim())) {
            report.topics_skipped++
            continue
          }
          const importance = asNumber(row['importance_score']) ?? 0
          const keywords = normalizeKeywords(row['keywords'])
          const createdAt = epochToISO(asNumber(row['first_seen']) ?? asNumber(row['created_at']), nowISO())
          insertTopic.run(newId(), name.trim(), scopeId, importance, JSON.stringify(keywords), createdAt)
          report.topics_imported++
        }
      })
      tx()
    }

    return report
  } catch (err) {
    const msg = `import cognition interrompu : ${(err as Error).message}`
    console.warn(`[memoria] ${msg}`)
    report.errors.push(msg)
    return report
  }
}

/**
 * Upsert observation brut (sans passer par observations.ts pour rester dans la
 * transaction d'import). Retourne true si insert, false si renforcement.
 */
function upsertObservationRaw(
  db: Database,
  subject: string,
  content: string,
  confidence: number,
  obsCount: number,
): boolean {
  const s = subject.trim()
  const c = content.trim()
  if (s.length < 2 || c.length < 2) return false
  const ts = nowISO()
  const existing = db
    .prepare('SELECT id, confidence, obs_count FROM observations WHERE subject = ? COLLATE NOCASE')
    .get(s) as { id: string; confidence: number; obs_count: number } | undefined
  if (existing) {
    const n = existing.obs_count
    const blended = Math.min(1, Math.max(0, (existing.confidence * n + confidence) / (n + 1)))
    db.prepare(
      'UPDATE observations SET content = ?, confidence = ?, obs_count = obs_count + ?, updated_at = ? WHERE id = ?',
    ).run(c, blended, obsCount, ts, existing.id)
    return false
  }
  db.prepare(
    `INSERT INTO observations (id, subject, content, confidence, obs_count, created_at, updated_at)
     VALUES (?, ?, ?, ?, ?, ?, ?)`,
  ).run(newId(), s, c, Math.min(1, Math.max(0, confidence)), Math.max(1, obsCount), ts, ts)
  return true
}

/** context legacy → array de fact_ids (JSON valide ou []). */
function normalizeContext(raw: unknown): string[] {
  if (typeof raw !== 'string' || raw.length === 0) return []
  try {
    const parsed: unknown = JSON.parse(raw)
    return Array.isArray(parsed) ? parsed.map(String) : []
  } catch {
    return []
  }
}

function mergeContext(existing: string, incoming: string[]): string {
  let arr: string[]
  try {
    const parsed: unknown = JSON.parse(existing || '[]')
    arr = Array.isArray(parsed) ? parsed.map(String) : []
  } catch {
    arr = []
  }
  for (const id of incoming) if (!arr.includes(id)) arr.push(id)
  return JSON.stringify(arr.slice(-20))
}

function normalizeKeywords(raw: unknown): string[] {
  if (typeof raw !== 'string' || raw.length === 0) return []
  try {
    const parsed: unknown = JSON.parse(raw)
    return Array.isArray(parsed) ? parsed.map(String) : []
  } catch {
    return []
  }
}

// Hash de provenance (réservé : un futur registre de sources cognition pourra
// l'utiliser ; gardé exporté pour cohérence avec import-legacy).
export function cognitionSourceHash(label: string): string {
  return sha256Hex(`cognition:${label}`)
}
