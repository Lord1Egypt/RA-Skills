/**
 * Importeur de transcripts d'agents (spec §7.2) :
 *   fichiers Claude Code / Codex → tours → fenêtres → extraction LLM (1 appel /
 *   fenêtre) → dédup → faits en QUARANTAINE (dormant + memory_import_items
 *   'pending') dans la mémoire PRIVÉE de l'instance → écran Revue.
 *
 * Garanties (alignées sur import-legacy.ts et le mode review-first de memoria.ts) :
 *  - IDEMPOTENCE par sha256 du contenu du fichier (memory_sources.source_hash,
 *    source_type='transcript') : ré-importer le même fichier = 0 nouveau ;
 *  - PROVENANCE : chaque fait retenu pointe vers sa memory_sources (chemin + hash)
 *    via memory_import_items ;
 *  - QUARANTAINE : le fait naît `dormant` (invisible au recall) + 'pending' —
 *    seule l'approbation par lot (Memoria.reviewDecision) l'active ;
 *  - DÉDUP : hash de contenu normalisé EN MÉMOIRE (dans le run) ET contre la DB
 *    privée (findDuplicate) — pas de doublon inter-fenêtres ni avec l'existant ;
 *  - SANS LLM (extraction null / indisponible) : 0 fait, note 'no-llm', AUCUNE
 *    invention, AUCUNE écriture de fait ;
 *  - une fenêtre dont l'extraction échoue ne bloque pas le fichier : l'erreur va
 *    dans report.errors + console.warn, on continue (jamais de mort silencieuse) ;
 *  - dryRun : parse + compte, AUCUNE écriture.
 *
 * NB : ce module n'écrit JAMAIS un fait actif. La promotion vers `active` passe
 * exclusivement par la revue gouvernée (Memoria.reviewDecision).
 */
import { readFileSync } from 'node:fs'
import { basename } from 'node:path'
import { ContentStore } from '../storage/content.js'
import { findDuplicate } from '../engine/selective.js'
import { parseFactArray } from '../engine/capture.js'
import { newId, nowISO, sha256Hex } from '../util.js'
import {
  detectTranscriptFormat,
  parseTranscript,
  type TranscriptFormat,
  type Turn,
} from './transcript-parsers.js'
import type { LlmProvider } from '../llm/provider.js'
import type { Fact, StoreFactInput } from '../types.js'

/**
 * Surface minimale du moteur dont l'importeur a besoin (Memoria la satisfait).
 * Découplage volontaire : l'import ne dépend pas de la classe concrète, et on
 * n'a pas à modifier engine/memoria.ts pour le câbler (helper externe).
 */
export interface ImportTranscriptsMemoria {
  /** storeFact gouverné (audite 'store_fact'). On le rend ensuite dormant + pending. */
  storeFact(input: StoreFactInput): Fact
  paths: { assistantDb(instanceId: string): string }
  registry: { getScopeByName(name: string): { id: string } | null }
}

export interface ImportTranscriptsInput {
  /** Chemins absolus des fichiers de transcript à importer. */
  files: string[]
  memoria: ImportTranscriptsMemoria
  /** assistant_instance_id cible (scope privé). */
  instanceId: string
  /** LLM d'extraction. null/indisponible → 0 fait + note 'no-llm' (pas d'invention). */
  extraction: LlmProvider | null
  /** Ne garder que les tours à/après cette date ISO (filtre les vieilles convs). */
  sinceDate?: string
  /** Garde-fou anti-explosion : nb max de fenêtres traitées par fichier (défaut 20). */
  maxWindowsPerFile?: number
  /** Parse + compte sans AUCUNE écriture. */
  dryRun?: boolean
  /**
   * Progression (job d'import du daemon, CLI) : appelé après CHAQUE fichier,
   * y compris ceux ignorés/en échec. Une exception du callback est loggée,
   * jamais avalée, et n'interrompt pas l'import.
   */
  onProgress?: (progress: ImportTranscriptsProgress) => void
}

export interface ImportTranscriptsProgress {
  filesDone: number
  filesTotal: number
  factsImported: number
}

export interface ImportTranscriptsReport {
  files_read: number
  files_skipped_already_imported: number
  windows: number
  facts_extracted: number
  facts_quarantined: number
  facts_skipped_duplicates: number
  errors: string[]
  notes: string[]
  dry_run: boolean
}

/** Prompt système dédié transcripts (dérivé de EXTRACTION_SYSTEM, spec §7.2). */
const TRANSCRIPT_EXTRACTION_SYSTEM = `Tu extrais des faits DURABLES depuis un extrait de conversation entre un utilisateur et un assistant de code, pour une mémoire long-terme.
Ne retiens QUE le durable et réutilisable : préférences de l'utilisateur, décisions et leurs raisons, configurations exactes, conventions de projet, leçons d'erreurs, processus appris.
N'extrais RIEN d'éphémère : état passager d'une tâche ponctuelle, politesse, question sans réponse, narration ("je lis le fichier"), détail valable une seule fois.
Chaque fait doit être AUTONOME (compréhensible seul) et contenir un élément concret (nom, version, commande, chemin, décision).
Réponds UNIQUEMENT avec un objet JSON, sans texte autour :
{"facts": [{"fact": "énoncé autonome et précis", "category": "preference|decision|config|erreur|process|general", "confidence": 0.0-1.0}]}
{"facts": []} si rien de durable.`

const DEFAULT_MAX_WINDOWS = 20
/** Cible de regroupement d'une fenêtre : ~6 tours OU ~2000 chars (borne le coût). */
const MAX_TURNS_PER_WINDOW = 6
const MAX_CHARS_PER_WINDOW = 2000

interface ConversationWindow {
  turns: Turn[]
}

function emptyReport(dryRun: boolean): ImportTranscriptsReport {
  return {
    files_read: 0,
    files_skipped_already_imported: 0,
    windows: 0,
    facts_extracted: 0,
    facts_quarantined: 0,
    facts_skipped_duplicates: 0,
    errors: [],
    notes: [],
    dry_run: dryRun,
  }
}

/** Hash de contenu normalisé (dédup faits) : casse + espaces neutralisés. Aligné sur import-legacy. */
function contentHash(text: string): string {
  return sha256Hex(text.trim().replaceAll(/\s+/gu, ' ').toLowerCase())
}

/** Regroupe les tours en fenêtres (~6 tours / ~2000 chars). Une fenêtre = 1 appel LLM. */
function buildWindows(turns: Turn[]): ConversationWindow[] {
  const windows: ConversationWindow[] = []
  let current: Turn[] = []
  let chars = 0
  for (const turn of turns) {
    current.push(turn)
    chars += turn.text.length
    if (current.length >= MAX_TURNS_PER_WINDOW || chars >= MAX_CHARS_PER_WINDOW) {
      windows.push({ turns: current })
      current = []
      chars = 0
    }
  }
  if (current.length > 0) windows.push({ turns: current })
  return windows
}

/** Prompt utilisateur d'une fenêtre (rôles préservés pour le contexte). */
function windowPrompt(window: ConversationWindow): string {
  const lines = window.turns.map(t => `- [${t.role}] ${t.text}`)
  return `Extrait de conversation :\n${lines.join('\n')}\n\nObjet JSON {"facts": [...]} des faits durables :`
}

/**
 * Filtre les tours par sinceDate. Un tour SANS ts est conservé (on ne jette pas
 * faute de métadonnée — décision conservatrice, signalée en note plus haut).
 */
function filterSince(turns: Turn[], sinceDate: string | undefined): Turn[] {
  if (!sinceDate) return turns
  const cutoff = Date.parse(sinceDate)
  if (Number.isNaN(cutoff)) return turns
  return turns.filter(t => {
    if (!t.ts) return true
    const ts = Date.parse(t.ts)
    return Number.isNaN(ts) || ts >= cutoff
  })
}

/**
 * Importe un lot de transcripts en quarantaine de revue. Ne throw jamais : toute
 * erreur d'un fichier/fenêtre est consignée dans report.errors + console.warn,
 * et l'import continue sur les autres.
 */
export async function importTranscripts(input: ImportTranscriptsInput): Promise<ImportTranscriptsReport> {
  const report = emptyReport(input.dryRun ?? false)
  const maxWindows = input.maxWindowsPerFile ?? DEFAULT_MAX_WINDOWS

  const privateScope = input.memoria.registry.getScopeByName(`private:${input.instanceId}`)
  if (!privateScope) {
    const msg = `scope privé introuvable pour l'instance ${input.instanceId} (pairing non fait ?)`
    console.warn(`[memoria] import transcripts : ${msg}`)
    report.errors.push(msg)
    return report
  }
  const scopeId = privateScope.id

  // Sans LLM : on le dit franchement et on s'arrête (aucune invention de faits).
  const llmReady = input.extraction !== null && (await safeIsAvailable(input.extraction, report))
  if (!llmReady) {
    report.notes.push('no-llm : aucun LLM d’extraction disponible — 0 fait extrait (aucune invention)')
  }

  // Une seule connexion à la DB privée pour tout le run (better-sqlite3 WAL).
  const dbPath = input.memoria.paths.assistantDb(input.instanceId)
  const store = new ContentStore(dbPath)

  try {
    // Dédup persistante : hash des faits déjà présents dans le scope privé.
    const existingHashes = new Set<string>(
      (store.db.prepare('SELECT fact FROM facts WHERE scope_id = ?').all(scopeId) as Array<{ fact: string }>).map(r =>
        contentHash(r.fact),
      ),
    )
    const seenInRun = new Set<string>()

    let filesDone = 0
    for (const file of input.files) {
      try {
        await importOneFile(file, {
          input,
          report,
          store,
          scopeId,
          maxWindows,
          llmReady,
          existingHashes,
          seenInRun,
        })
      } catch (err) {
        // Erreur INATTENDUE sur un fichier : visible, jamais avalée, on continue.
        const msg = `fichier « ${file} » : ${(err as Error).message}`
        console.warn(`[memoria] import transcripts : ${msg}`)
        report.errors.push(msg)
      }
      filesDone++
      notifyProgress(input.onProgress, {
        filesDone,
        filesTotal: input.files.length,
        factsImported: report.facts_quarantined,
      })
    }
  } finally {
    store.close()
  }

  return report
}

interface FileContext {
  input: ImportTranscriptsInput
  report: ImportTranscriptsReport
  store: ContentStore
  scopeId: string
  maxWindows: number
  llmReady: boolean
  existingHashes: Set<string>
  seenInRun: Set<string>
}

async function importOneFile(file: string, ctx: FileContext): Promise<void> {
  const { input, report, store, scopeId, maxWindows, llmReady, existingHashes, seenInRun } = ctx

  let content: string
  try {
    content = readFileSync(file, 'utf8')
  } catch (err) {
    report.errors.push(`lecture impossible « ${file} » : ${(err as Error).message}`)
    console.warn(`[memoria] import transcripts : lecture impossible « ${file} » : ${(err as Error).message}`)
    return
  }

  const sourceHash = sha256Hex(content)

  // IDEMPOTENCE : ce contenu exact déjà importé → SKIP (0 nouveau).
  const already = store.db
    .prepare("SELECT id FROM memory_sources WHERE source_hash = ? AND source_type = 'transcript'")
    .get(sourceHash) as { id: string } | undefined
  if (already) {
    report.files_skipped_already_imported++
    report.notes.push(`déjà importé (hash) : ${basename(file)} — re-import = 0 nouveau`)
    return
  }

  const firstLines = content.split(/\r?\n/).slice(0, 12).join('\n')
  const format: TranscriptFormat = detectTranscriptFormat(file, firstLines)
  if (format === 'unknown') {
    report.notes.push(`format non reconnu, ignoré : ${basename(file)}`)
    return
  }

  report.files_read++

  const allTurns = parseTranscript(format, content)
  const turns = filterSince(allTurns, input.sinceDate)
  if (turns.length === 0) {
    report.notes.push(`aucun tour exploitable (${format}) : ${basename(file)}`)
    return
  }

  let windows = buildWindows(turns)

  // GARDE-FOU : trop de fenêtres → on garde les PLUS RÉCENTES + on LOG le nombre
  // ignoré (jamais de troncature silencieuse — règle du projet).
  if (windows.length > maxWindows) {
    const ignored = windows.length - maxWindows
    windows = windows.slice(-maxWindows)
    const note = `${basename(file)} : ${ignored} fenêtre(s) ancienne(s) ignorée(s) (cap ${maxWindows}) — gardé les plus récentes`
    report.notes.push(note)
    console.warn(`[memoria] import transcripts : ${note}`)
  }

  // dryRun : on compte les fenêtres mais on n'écrit / n'extrait rien.
  if (report.dry_run) {
    report.windows += windows.length
    report.notes.push(`dry-run ${basename(file)} (${format}) : ${windows.length} fenêtre(s) — AUCUNE écriture`)
    return
  }

  // Sans LLM : aucune extraction possible — fenêtres comptées, 0 fait.
  if (!llmReady) {
    report.windows += windows.length
    return
  }

  // Provenance : 1 memory_sources par fichier (créée à la 1re écriture utile).
  let sourceId: string | null = null
  const ensureSource = (): string => {
    if (sourceId) return sourceId
    sourceId = newId()
    store.db
      .prepare(
        `INSERT INTO memory_sources (id, source_type, source_path, source_hash, imported_at, metadata)
         VALUES (?, 'transcript', ?, ?, ?, ?)`,
      )
      .run(
        sourceId,
        file,
        sourceHash,
        nowISO(),
        JSON.stringify({ format, turns: turns.length, windows: windows.length }),
      )
    return sourceId
  }

  for (const window of windows) {
    report.windows++
    const facts = await extractWindow(input.extraction!, window, report, file)
    for (const item of facts) {
      report.facts_extracted++
      const hash = contentHash(item.fact)
      // Dédup intra-run + persistante (existant) + near-dup (findDuplicate).
      if (seenInRun.has(hash) || existingHashes.has(hash)) {
        report.facts_skipped_duplicates++
        continue
      }
      if (findDuplicate(store, scopeId, item.fact)) {
        report.facts_skipped_duplicates++
        continue
      }
      seenInRun.add(hash)
      existingHashes.add(hash)
      quarantineFact(ctx, ensureSource(), item)
      report.facts_quarantined++
    }
  }

  // Aucun fait retenu mais fichier traité : on garde quand même la provenance
  // pour l'idempotence (re-import inutile). Si rien n'a été extrait du tout,
  // on crée tout de même la source pour ne pas re-scanner.
  if (!sourceId) ensureSource()
}

interface ExtractedFact {
  fact: string
  category: string
  confidence: number
}

/** 1 SEUL appel LLM par fenêtre. Échec → erreur consignée, fenêtre ignorée, on continue. */
async function extractWindow(
  extraction: LlmProvider,
  window: ConversationWindow,
  report: ImportTranscriptsReport,
  file: string,
): Promise<ExtractedFact[]> {
  try {
    const raw = await extraction.complete({
      system: TRANSCRIPT_EXTRACTION_SYSTEM,
      prompt: windowPrompt(window),
      json: true,
      maxTokens: 1024,
      temperature: 0.1,
    })
    return parseFactArray(raw)
  } catch (err) {
    const msg = `extraction de fenêtre en échec (${basename(file)}) : ${(err as Error).message}`
    console.warn(`[memoria] import transcripts : ${msg}`)
    report.errors.push(msg)
    return []
  }
}

/**
 * Écrit un fait extrait en QUARANTAINE : storeFact privé → dormant → ligne
 * memory_import_items 'pending'. Reproduit le mécanisme review-first de
 * memoria.storeCaptured (mais source 'transcript' + provenance fichier).
 */
function quarantineFact(ctx: FileContext, sourceId: string, item: ExtractedFact): void {
  const { input, store, scopeId } = ctx
  const fact = input.memoria.storeFact({
    instance: input.instanceId,
    content: item.fact,
    category: item.category,
    confidence: item.confidence,
    source: 'transcript-import',
  })
  // Invisible au recall jusqu'à approbation.
  store.db.prepare("UPDATE facts SET lifecycle_state = 'dormant' WHERE id = ?").run(fact.id)
  store.db
    .prepare(
      `INSERT INTO memory_import_items (id, source_id, target_memory_id, target_type, proposed_scope_id, status, confidence)
       VALUES (?, ?, ?, 'fact', ?, 'pending', ?)`,
    )
    .run(newId(), sourceId, fact.id, scopeId, item.confidence)
}

/** Progression tolérante : un callback qui jette est loggé, l'import continue. */
function notifyProgress(
  cb: ImportTranscriptsInput['onProgress'],
  progress: ImportTranscriptsProgress,
): void {
  if (!cb) return
  try {
    cb(progress)
  } catch (err) {
    console.warn(`[memoria] import transcripts : callback de progression en échec : ${(err as Error).message}`)
  }
}

/** isAvailable tolérant : une exception du provider = indisponible (consigné), pas un crash. */
async function safeIsAvailable(provider: LlmProvider, report: ImportTranscriptsReport): Promise<boolean> {
  try {
    return await provider.isAvailable()
  } catch (err) {
    const msg = `provider.isAvailable() a échoué : ${(err as Error).message}`
    console.warn(`[memoria] import transcripts : ${msg}`)
    report.errors.push(msg)
    return false
  }
}
