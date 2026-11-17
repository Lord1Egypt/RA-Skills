/**
 * Runner de migrations additives — table `schema_migrations(version, applied_at)`.
 * Chaque DB (registry, contenu) a sa propre série. Les migrations sont
 * transactionnelles et idempotentes (re-run sans effet).
 */
import type { Database } from 'better-sqlite3'
import { nowISO } from '../util.js'

export interface Migration {
  version: number
  name: string
  up: (db: Database) => void
}

export function runMigrations(db: Database, migrations: Migration[]): number {
  db.exec(
    'CREATE TABLE IF NOT EXISTS schema_migrations (version INTEGER PRIMARY KEY, name TEXT NOT NULL, applied_at TEXT NOT NULL)',
  )
  const appliedRows = db.prepare('SELECT version FROM schema_migrations').all() as Array<{ version: number }>
  const applied = new Set(appliedRows.map(r => r.version))

  const sorted = [...migrations].sort((a, b) => a.version - b.version)
  let count = 0
  for (const m of sorted) {
    if (applied.has(m.version)) continue
    const run = db.transaction(() => {
      m.up(db)
      db.prepare('INSERT INTO schema_migrations (version, name, applied_at) VALUES (?, ?, ?)').run(
        m.version,
        m.name,
        nowISO(),
      )
    })
    run()
    count++
  }
  return count
}

export function schemaVersion(db: Database): number {
  try {
    const row = db.prepare('SELECT MAX(version) AS v FROM schema_migrations').get() as { v: number | null }
    return row.v ?? 0
  } catch {
    return 0
  }
}
