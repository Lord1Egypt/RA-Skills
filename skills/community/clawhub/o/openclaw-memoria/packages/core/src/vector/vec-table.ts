/**
 * Table vectorielle sqlite-vec (spec §10) — index ANN dans le MÊME fichier
 * SQLite que la vérité (la table embeddings reste la source).
 *
 * Une table virtuelle PAR dimensionnalité (`vec_index_768`, `vec_index_8`…) :
 * le mélange de dimensions est structurellement impossible (anti-bug 768/1536).
 * Machine sans binaire sqlite-vec → dégradation PROPRE vers FTS seul,
 * annoncée une fois (console.warn), jamais silencieuse.
 */
import { createRequire } from 'node:module'
import type { Database } from 'better-sqlite3'
import { vectorToBuffer } from '../util.js'

let warnedUnavailable = false
const loadedDbs = new WeakSet<Database>()
const knownTables = new WeakMap<Database, Set<number>>()

/** Charge l'extension sqlite-vec dans cette connexion. False si indisponible. */
export function loadVecExtension(db: Database): boolean {
  if (loadedDbs.has(db)) return true
  try {
    requireSqliteVec().load(db)
    loadedDbs.add(db)
    return true
  } catch (err) {
    if (!warnedUnavailable) {
      warnedUnavailable = true
      console.warn(
        `[memoria] extension sqlite-vec indisponible (${(err as Error).message}) — recall en FTS seul`,
      )
    }
    return false
  }
}

interface SqliteVecModule {
  load: (db: Database) => void
}

// sqlite-vec est CJS, le core est en ESM strict → createRequire
const requireCjs = createRequire(import.meta.url)
let cachedModule: SqliteVecModule | null | undefined
function requireSqliteVec(): SqliteVecModule {
  if (cachedModule === undefined) {
    try {
      cachedModule = requireCjs('sqlite-vec') as SqliteVecModule
    } catch {
      cachedModule = null
    }
  }
  if (!cachedModule) throw new Error('module sqlite-vec introuvable')
  return cachedModule
}

export function isVecAvailable(db: Database): boolean {
  return loadVecExtension(db)
}

/** Crée (si besoin) la table vectorielle de cette dimensionnalité. */
export function ensureVecTable(db: Database, dimensions: number): boolean {
  if (!loadVecExtension(db)) return false
  let tables = knownTables.get(db)
  if (!tables) {
    tables = new Set()
    knownTables.set(db, tables)
  }
  if (tables.has(dimensions)) return true
  db.exec(
    `CREATE VIRTUAL TABLE IF NOT EXISTS vec_index_${dimensions} USING vec0(
       embedding float[${dimensions}],
       fact_id TEXT
     )`,
  )
  tables.add(dimensions)
  return true
}

export function vecTableName(dimensions: number): string {
  return `vec_index_${dimensions}`
}

/** Insère/remplace le vecteur d'un fait dans l'index. */
export function upsertVector(db: Database, dimensions: number, factId: string, vector: Float32Array): void {
  if (vector.length !== dimensions) {
    throw new Error(`dimension du vecteur (${vector.length}) ≠ table vec_index_${dimensions} — interdit`)
  }
  if (!ensureVecTable(db, dimensions)) return
  const table = vecTableName(dimensions)
  db.prepare(`DELETE FROM ${table} WHERE fact_id = ?`).run(factId)
  db.prepare(`INSERT INTO ${table} (embedding, fact_id) VALUES (?, ?)`).run(vectorToBuffer(vector), factId)
}

/** Retire des faits de l'index (hard-delete / réindexation). */
export function removeVectors(db: Database, dimensions: number, factIds: string[]): void {
  if (factIds.length === 0 || !ensureVecTable(db, dimensions)) return
  const table = vecTableName(dimensions)
  const stmt = db.prepare(`DELETE FROM ${table} WHERE fact_id = ?`)
  for (const id of factIds) stmt.run(id)
}

export interface KnnHit {
  fact_id: string
  distance: number
}

/** KNN brut sur l'index — le filtrage permissions se fait PAR-DESSUS (jointure facts). */
export function knn(db: Database, dimensions: number, query: Float32Array, k: number): KnnHit[] {
  if (query.length !== dimensions) {
    throw new Error(`dimension de la requête (${query.length}) ≠ table vec_index_${dimensions} — interdit`)
  }
  if (!ensureVecTable(db, dimensions)) return []
  const table = vecTableName(dimensions)
  return db
    .prepare(`SELECT fact_id, distance FROM ${table} WHERE embedding MATCH ? AND k = ? ORDER BY distance`)
    .all(vectorToBuffer(query), k) as KnnHit[]
}
