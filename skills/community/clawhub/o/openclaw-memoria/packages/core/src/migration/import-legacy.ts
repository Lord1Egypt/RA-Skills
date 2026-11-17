/**
 * Import memoria.db v3.34 → V3 (spec §7.1, P1 DoD) :
 * PRÉ-VOL (readonly + integrity_check + détection de schéma tolérante)
 * → BACKUP (VACUUM INTO, refus de continuer si échec)
 * → IMPORT en quarantaine `legacy_to_review` avec provenance
 *   (memory_sources + memory_import_items 'pending')
 * → VÉRIF (counts relus + échantillon FTS) sinon ROLLBACK complet.
 *
 * Garanties :
 *  - la DB legacy est ouverte `readonly: true` — JAMAIS modifiée ;
 *  - idempotence par sha256 du fichier source + dédup par hash de contenu
 *    normalisé ;
 *  - embeddings legacy NON copiés (768d/1536d mélangés sans colonne
 *    dimensions = invalides) — réindexation propre plus tard ;
 *  - aucune erreur avalée : tout échec finit dans report.errors + console.warn.
 */
import Database from 'better-sqlite3'
import { existsSync, readFileSync } from 'node:fs'
import { join } from 'node:path'
import { ContentStore } from '../storage/content.js'
import { newId, nowISO, sha256Hex, toJson } from '../util.js'
import type { Memoria } from '../engine/memoria.js'
import type { MemoryScope } from '../types.js'

export interface ImportLegacyInput {
  legacyPath: string
  memoria: Memoria
  /** Pré-vol + backup + analyse, mais AUCUNE écriture dans la cible. */
  dryRun?: boolean
  /** Réservé aux tests : force l'échec de la vérification → chemin rollback. */
  forceVerifyFailureForTests?: boolean
}

export interface ImportLegacyReport {
  source_hash: string
  backup_path: string | null
  facts_read: number
  facts_imported: number
  facts_skipped_duplicates: number
  procedures_read: number
  procedures_imported: number
  procedures_skipped_duplicates: number
  /** Embeddings legacy ignorés (réindexation propre requise). */
  embeddings_skipped: number
  errors: string[]
  notes: string[]
  rolled_back: boolean
  dry_run: boolean
}

/** Fait legacy mappé, prêt à insérer dans le schéma V3. */
interface MappedFact {
  id: string
  fact: string
  category: string
  fact_type: string
  confidence: number
  source: string
  scope_id: string
  tags: string
  entity_ids: string
  lifecycle_state: 'active' | 'dormant'
  superseded: number
  superseded_by: string | null
  usefulness: number
  recall_count: number
  used_count: number
  relevance_weight: number
  created_at: string
  updated_at: string
  last_accessed_at: string | null
}

interface MappedProcedure {
  id: string
  name: string
  description: string
  steps: string
  success_count: number
  failure_count: number
  scope_id: string
  created_at: string
  updated_at: string
}

/** Erreur de pré-vol/backup → abort propre (convertie en report.errors). */
class ImportAbort extends Error {}

type LegacyRow = Record<string, unknown>

const asString = (v: unknown): string | null => (typeof v === 'string' ? v : null)
const asNumber = (v: unknown): number | null => (typeof v === 'number' && Number.isFinite(v) ? v : null)

/** Epoch legacy (ms, parfois secondes) → ISO ; valeur invalide → fallback. */
function epochToISO(v: number | null, fallback: string): string {
  if (v === null || v <= 0) return fallback
  const ms = v < 1e11 ? v * 1000 : v
  const d = new Date(ms)
  return Number.isNaN(d.getTime()) ? fallback : d.toISOString()
}

/** fresh|settled → active ; dormant → dormant ; inconnu → active. */
function mapLifecycle(v: unknown): 'active' | 'dormant' {
  return v === 'dormant' ? 'dormant' : 'active'
}

/** Garde un JSON array valide tel quel, sinon '[]' (tags/entity_ids/steps legacy parfois invalides). */
function keepJsonArray(raw: unknown): string {
  if (typeof raw !== 'string' || raw.length === 0) return '[]'
  try {
    const parsed: unknown = JSON.parse(raw)
    return Array.isArray(parsed) ? raw : '[]'
  } catch {
    return '[]'
  }
}

/** Hash de contenu normalisé (dédup) : casse + espaces neutralisés. */
function contentHash(text: string): string {
  return sha256Hex(text.trim().replaceAll(/\s+/gu, ' ').toLowerCase())
}

function tableColumns(db: Database.Database, table: string): Set<string> {
  const rows = db.pragma(`table_info(${table})`) as Array<{ name: string }>
  return new Set(rows.map(r => r.name))
}

function emptyReport(): ImportLegacyReport {
  return {
    source_hash: '',
    backup_path: null,
    facts_read: 0,
    facts_imported: 0,
    facts_skipped_duplicates: 0,
    procedures_read: 0,
    procedures_imported: 0,
    procedures_skipped_duplicates: 0,
    embeddings_skipped: 0,
    errors: [],
    notes: [],
    rolled_back: false,
    dry_run: false,
  }
}

export function importLegacyDb(input: ImportLegacyInput): ImportLegacyReport {
  const { legacyPath, memoria } = input
  const report = emptyReport()
  report.dry_run = input.dryRun ?? false

  let legacy: Database.Database | null = null
  let target: ContentStore | null = null
  try {
    // ----------------------------------------------------------- 1. PRÉ-VOL
    if (!existsSync(legacyPath)) {
      throw new ImportAbort(`fichier legacy introuvable : ${legacyPath}`)
    }
    try {
      legacy = new Database(legacyPath, { readonly: true })
    } catch (err) {
      throw new ImportAbort(`ouverture lecture seule impossible : ${(err as Error).message}`)
    }
    let integrity: Array<{ integrity_check: string }>
    try {
      integrity = legacy.pragma('integrity_check') as Array<{ integrity_check: string }>
    } catch (err) {
      throw new ImportAbort(`integrity_check impossible (fichier corrompu ?) : ${(err as Error).message}`)
    }
    if (integrity.length !== 1 || integrity[0]?.integrity_check !== 'ok') {
      throw new ImportAbort(`integrity_check non-ok : ${integrity.map(r => r.integrity_check).join(' | ')}`)
    }

    // Détection de schéma TOLÉRANTE : les try/catch muets du legacy ont pu
    // laisser des schémas partiels (synced_to_md ou quality_* absents).
    const factCols = tableColumns(legacy, 'facts')
    if (!factCols.has('id') || !factCols.has('fact') || !factCols.has('created_at')) {
      throw new ImportAbort(`schéma non reconnu : table facts absente ou colonnes minimales manquantes (${legacyPath})`)
    }
    const procCols = tableColumns(legacy, 'procedures')
    const hasEmbeddings = tableColumns(legacy, 'embeddings').size > 0

    report.source_hash = sha256Hex(readFileSync(legacyPath))

    // ------------------------------------------------------------ 2. BACKUP
    // REFUS de continuer si le backup échoue — c'est le filet de sécurité.
    const stamp = nowISO().replaceAll(/[:.]/gu, '-')
    const backupPath = join(memoria.paths.backupsDir, `legacy-${stamp}-${newId().slice(0, 8)}.sqlite`)
    try {
      legacy.prepare('VACUUM INTO ?').run(backupPath)
    } catch (err) {
      throw new ImportAbort(`backup VACUUM INTO échoué (${backupPath}) : ${(err as Error).message}`)
    }
    report.backup_path = backupPath

    // ------------------------------------------------- lecture de la source
    const legacyFacts = legacy.prepare('SELECT * FROM facts').all() as LegacyRow[]
    report.facts_read = legacyFacts.length
    const legacyProcs = procCols.size > 0 ? (legacy.prepare('SELECT * FROM procedures').all() as LegacyRow[]) : []
    report.procedures_read = legacyProcs.length
    if (hasEmbeddings) {
      const r = legacy.prepare('SELECT COUNT(*) AS c FROM embeddings').get() as { c: number }
      report.embeddings_skipped = r.c
      if (r.c > 0) {
        report.notes.push(
          `${r.c} embeddings legacy NON copiés (dimensions 768/1536 mélangées sans colonne dimensions) — réindexation propre requise`,
        )
      }
    }

    // ------------------------------------------------------ cible & dédup
    const scope = memoria.registry.getScopeByName('legacy_to_review')
    if (!scope) {
      throw new ImportAbort('scope legacy_to_review introuvable dans le registry (bootstrap non exécuté ?)')
    }
    // Même mapping de DB que le moteur : shared/legacy_to_review.sqlite
    const targetPath = memoria.paths.sharedDb('legacy_to_review')
    target = new ContentStore(targetPath)
    memoria.registry.registerDb({ kind: 'shared', path: targetPath, assistant_instance_id: null, scope_id: scope.id })

    // 4. IDEMPOTENCE — même fichier déjà importé → 0 nouveau.
    const already = target.db
      .prepare('SELECT id FROM memory_sources WHERE source_hash = ?')
      .get(report.source_hash) as { id: string } | undefined
    if (already) {
      report.notes.push(`source déjà importée (memory_sources.id=${already.id}) — re-import = 0 nouveau`)
      return report
    }

    const plan = buildPlan(legacyFacts, legacyProcs, scope, target, report)

    if (report.dry_run) {
      report.notes.push(
        `dry-run : ${plan.facts.length} faits et ${plan.procedures.length} procédures seraient importés ` +
          `(${report.facts_skipped_duplicates} doublons de faits ignorés) — AUCUNE écriture effectuée`,
      )
      return report
    }

    // ------------------------------------------------- 3. IMPORT (transaction)
    const sourceId = newId()
    runImport(target, sourceId, legacyPath, plan, report, scope)
    report.facts_imported = plan.facts.length
    report.procedures_imported = plan.procedures.length

    // ------------------------------------------------------------- 5. VÉRIF
    const verifyErrors = verifyImport(target, scope.id, sourceId, plan)
    if (input.forceVerifyFailureForTests) {
      verifyErrors.push('échec de vérification injecté (option de test)')
    }
    if (verifyErrors.length > 0) {
      console.warn(`[memoria] import legacy : vérification échouée → rollback (${verifyErrors.join(' ; ')})`)
      try {
        rollbackImport(target, sourceId)
        report.rolled_back = true
      } catch (rollbackErr) {
        // Rollback lui-même en échec : on le dit haut et fort, jamais en silence.
        const msg = `ROLLBACK ÉCHOUÉ — cible possiblement incohérente : ${(rollbackErr as Error).message}`
        console.warn(`[memoria] import legacy : ${msg}`)
        report.errors.push(msg)
      }
      report.errors.push(...verifyErrors)
      report.facts_imported = 0
      report.procedures_imported = 0
      memoria.registry.audit({
        actor_type: 'system',
        actor_id: 'import-legacy',
        action: 'import_legacy_rollback',
        target_id_hash: sha256Hex(report.source_hash),
        scope_id: scope.id,
        reason: verifyErrors[0] ?? null,
      })
      return report
    }

    memoria.registry.audit({
      actor_type: 'system',
      actor_id: 'import-legacy',
      action: 'import_legacy',
      target_id_hash: sha256Hex(report.source_hash),
      scope_id: scope.id,
      reason: `facts=${report.facts_imported}/${report.facts_read} procedures=${report.procedures_imported}/${report.procedures_read}`,
    })
    return report
  } catch (err) {
    // Abort propre : pré-vol/backup/import en échec → rapport, pas d'exception.
    const msg = err instanceof ImportAbort ? err.message : `erreur inattendue : ${(err as Error).message}`
    console.warn(`[memoria] import legacy interrompu : ${msg}`)
    report.errors.push(msg)
    return report
  } finally {
    try {
      legacy?.close()
    } catch (err) {
      console.warn(`[memoria] fermeture DB legacy : ${(err as Error).message}`)
    }
    try {
      target?.close()
    } catch (err) {
      console.warn(`[memoria] fermeture DB cible : ${(err as Error).message}`)
    }
  }
}

interface ImportPlan {
  facts: MappedFact[]
  procedures: MappedProcedure[]
}

/**
 * Mapping colonnes ancien → nouveau + dédup (hash de contenu normalisé,
 * intra-lot ET contre la cible) + collisions d'id.
 */
function buildPlan(
  legacyFacts: LegacyRow[],
  legacyProcs: LegacyRow[],
  scope: MemoryScope,
  target: ContentStore,
  report: ImportLegacyReport,
): ImportPlan {
  const fallbackTs = nowISO()

  const existingFactHashes = new Set<string>(
    (target.db.prepare('SELECT fact FROM facts WHERE scope_id = ?').all(scope.id) as Array<{ fact: string }>).map(r =>
      contentHash(r.fact),
    ),
  )
  const factIdExists = target.db.prepare('SELECT 1 AS one FROM facts WHERE id = ?')
  const seenHashes = new Set<string>()

  const facts: MappedFact[] = []
  for (const row of legacyFacts) {
    const text = asString(row['fact'])
    const legacyId = asString(row['id'])
    if (!text || !legacyId) {
      report.facts_skipped_duplicates++
      report.notes.push(`fait legacy sans id/texte ignoré (id=${String(row['id'])})`)
      continue
    }
    const hash = contentHash(text)
    if (seenHashes.has(hash) || existingFactHashes.has(hash) || factIdExists.get(legacyId) !== undefined) {
      report.facts_skipped_duplicates++
      continue
    }
    seenHashes.add(hash)

    const createdAt = epochToISO(asNumber(row['created_at']), fallbackTs)
    // access_count legacy fusionné dans recall_count via MAX (décision §18)
    const recallCount = Math.max(asNumber(row['recall_count']) ?? 0, asNumber(row['access_count']) ?? 0)
    facts.push({
      id: legacyId,
      fact: text,
      category: asString(row['category']) ?? 'savoir',
      fact_type: asString(row['fact_type']) ?? 'semantic',
      confidence: Math.min(1, Math.max(0, asNumber(row['confidence']) ?? 0.8)),
      source: asString(row['source']) ?? 'auto-capture',
      scope_id: scope.id,
      tags: keepJsonArray(row['tags']),
      entity_ids: keepJsonArray(row['entity_ids']),
      lifecycle_state: mapLifecycle(row['lifecycle_state']),
      superseded: row['superseded'] === 1 ? 1 : 0,
      superseded_by: asString(row['superseded_by']),
      usefulness: asNumber(row['usefulness']) ?? 0,
      recall_count: recallCount,
      used_count: asNumber(row['used_count']) ?? 0,
      relevance_weight: asNumber(row['relevance_weight']) ?? 1.0,
      created_at: createdAt,
      updated_at: epochToISO(asNumber(row['updated_at']), createdAt),
      last_accessed_at: asNumber(row['last_accessed_at']) !== null ? epochToISO(asNumber(row['last_accessed_at']), createdAt) : null,
    })
  }

  const existingProcHashes = new Set<string>(
    (target.db.prepare('SELECT name, steps FROM procedures WHERE scope_id = ?').all(scope.id) as Array<{
      name: string
      steps: string
    }>).map(r => contentHash(`${r.name}\n${r.steps}`)),
  )
  const procIdExists = target.db.prepare('SELECT 1 AS one FROM procedures WHERE id = ?')
  const seenProcHashes = new Set<string>()

  const procedures: MappedProcedure[] = []
  for (const row of legacyProcs) {
    const legacyId = asString(row['id'])
    const name = asString(row['name'])
    if (!legacyId || !name) {
      report.procedures_skipped_duplicates++
      report.notes.push(`procédure legacy sans id/nom ignorée (id=${String(row['id'])})`)
      continue
    }
    const steps = keepJsonArray(row['steps'])
    const hash = contentHash(`${name}\n${steps}`)
    if (seenProcHashes.has(hash) || existingProcHashes.has(hash) || procIdExists.get(legacyId) !== undefined) {
      report.procedures_skipped_duplicates++
      continue
    }
    seenProcHashes.add(hash)

    const updatedAt = epochToISO(asNumber(row['last_updated_at']), fallbackTs)
    procedures.push({
      id: legacyId,
      name,
      description: asString(row['goal']) ?? '',
      steps,
      success_count: asNumber(row['success_count']) ?? 0,
      failure_count: asNumber(row['failure_count']) ?? 0,
      scope_id: scope.id,
      // pas de created_at legacy → last_updated_at fait foi
      created_at: updatedAt,
      updated_at: updatedAt,
    })
  }

  return { facts, procedures }
}

/** Insertion transactionnelle : provenance + faits + procédures + quarantaine. */
function runImport(
  target: ContentStore,
  sourceId: string,
  legacyPath: string,
  plan: ImportPlan,
  report: ImportLegacyReport,
  scope: MemoryScope,
): void {
  const insertFact = target.db.prepare(`
    INSERT INTO facts (
      id, fact, category, fact_type, confidence, source,
      assistant_instance_id, user_id, org_id, client_org_id, project_id, topic_id, scope_id,
      sensitivity, visibility, tags, entity_ids,
      lifecycle_state, superseded, superseded_by,
      usefulness, recall_count, used_count, relevance_weight,
      created_at, updated_at, last_accessed_at
    ) VALUES (
      @id, @fact, @category, @fact_type, @confidence, @source,
      NULL, NULL, NULL, NULL, NULL, NULL, @scope_id,
      'normal', 'private', @tags, @entity_ids,
      @lifecycle_state, @superseded, @superseded_by,
      @usefulness, @recall_count, @used_count, @relevance_weight,
      @created_at, @updated_at, @last_accessed_at
    )
  `)
  const insertProc = target.db.prepare(`
    INSERT INTO procedures (
      id, name, description, steps, trigger_patterns,
      success_count, failure_count, failure_reasons,
      scope_id, assistant_instance_id, project_id, lifecycle_state,
      created_at, updated_at
    ) VALUES (
      @id, @name, @description, @steps, '[]',
      @success_count, @failure_count, '[]',
      @scope_id, NULL, NULL, 'active',
      @created_at, @updated_at
    )
  `)
  const insertItem = target.db.prepare(`
    INSERT INTO memory_import_items (
      id, source_id, target_memory_id, target_type,
      proposed_scope_id, proposed_entity_ids, status, confidence
    ) VALUES (?, ?, ?, ?, ?, ?, 'pending', ?)
  `)

  const tx = target.db.transaction(() => {
    target.db
      .prepare(
        'INSERT INTO memory_sources (id, source_type, source_path, source_hash, imported_at, metadata) VALUES (?, ?, ?, ?, ?, ?)',
      )
      .run(
        sourceId,
        'openclaw-memoria-v3.34',
        legacyPath,
        report.source_hash,
        nowISO(),
        toJson({
          facts_read: report.facts_read,
          procedures_read: report.procedures_read,
          embeddings_skipped: report.embeddings_skipped,
        }),
      )
    for (const f of plan.facts) {
      insertFact.run(f)
      insertItem.run(newId(), sourceId, f.id, 'fact', scope.id, f.entity_ids, f.confidence)
    }
    for (const p of plan.procedures) {
      insertProc.run(p)
      insertItem.run(newId(), sourceId, p.id, 'procedure', scope.id, '[]', 0.5)
    }
  })
  tx()
}

/** Counts relus depuis la cible + échantillon de 5 faits retrouvables par FTS. */
function verifyImport(target: ContentStore, scopeId: string, sourceId: string, plan: ImportPlan): string[] {
  const errors: string[] = []

  const factItemCount = (
    target.db
      .prepare("SELECT COUNT(*) AS c FROM memory_import_items WHERE source_id = ? AND target_type = 'fact'")
      .get(sourceId) as { c: number }
  ).c
  const factRowCount = (
    target.db
      .prepare(
        `SELECT COUNT(*) AS c FROM facts WHERE id IN (
           SELECT target_memory_id FROM memory_import_items WHERE source_id = ? AND target_type = 'fact'
         )`,
      )
      .get(sourceId) as { c: number }
  ).c
  if (factItemCount !== plan.facts.length || factRowCount !== plan.facts.length) {
    errors.push(`counts faits incohérents : attendu=${plan.facts.length} items=${factItemCount} rows=${factRowCount}`)
  }

  const procRowCount = (
    target.db
      .prepare(
        `SELECT COUNT(*) AS c FROM procedures WHERE id IN (
           SELECT target_memory_id FROM memory_import_items WHERE source_id = ? AND target_type = 'procedure'
         )`,
      )
      .get(sourceId) as { c: number }
  ).c
  if (procRowCount !== plan.procedures.length) {
    errors.push(`counts procédures incohérents : attendu=${plan.procedures.length} rows=${procRowCount}`)
  }

  // Échantillon : 5 faits actifs non-superseded doivent ressortir en FTS.
  const sample = plan.facts.filter(f => f.superseded === 0 && f.lifecycle_state === 'active').slice(0, 5)
  for (const f of sample) {
    const word = f.fact
      .split(/[^\p{L}\p{N}_-]+/u)
      .filter(w => w.length >= 4)
      .sort((a, b) => b.length - a.length)[0]
    if (!word) continue
    const hits = target.searchFacts(word, { scopeIds: [scopeId], limit: 50 })
    if (!hits.some(h => h.row.id === f.id)) {
      errors.push(`recall de contrôle FTS échoué : fait ${f.id} introuvable via « ${word} »`)
    }
  }
  return errors
}

/**
 * ROLLBACK : supprime TOUT ce qui porte source_id — faits (hard-delete,
 * FTS/embeddings/fact_topics inclus), procédures, import_items (CASCADE)
 * et la ligne memory_sources elle-même.
 */
function rollbackImport(target: ContentStore, sourceId: string): void {
  const tx = target.db.transaction(() => {
    const items = target.db
      .prepare('SELECT target_memory_id, target_type FROM memory_import_items WHERE source_id = ?')
      .all(sourceId) as Array<{ target_memory_id: string | null; target_type: string | null }>
    const factIds = items.filter(i => i.target_type === 'fact' && i.target_memory_id).map(i => i.target_memory_id as string)
    const procIds = items
      .filter(i => i.target_type === 'procedure' && i.target_memory_id)
      .map(i => i.target_memory_id as string)
    if (factIds.length > 0) target.hardDeleteFacts(factIds)
    if (procIds.length > 0) {
      const placeholders = procIds.map(() => '?').join(',')
      target.db.prepare(`DELETE FROM procedures WHERE id IN (${placeholders})`).run(...procIds)
    }
    // FK ON DELETE CASCADE → memory_import_items purgés avec la source
    target.db.prepare('DELETE FROM memory_sources WHERE id = ?').run(sourceId)
  })
  tx()
}
