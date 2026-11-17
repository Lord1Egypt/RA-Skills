/**
 * CapturePipeline — capture WAL-first (spec §6.2, phase P2) : « rien ne se perd ».
 *
 * Ordre STRICT par tour :
 *   0. redaction secrets (gate dur §9) — la valeur d'un secret ne touche
 *      JAMAIS la DB, wal_buffer inclus ;
 *   1. WAL append de CHAQUE message AVANT tout LLM (source de vérité) ;
 *   2. consommation du WAL : extraction LLM (1 SEUL appel par tour — les
 *      messages d'un même tour sont batchés dans un seul prompt, leçon du
 *      legacy à ~3-15 appels bloquants par fait) → dedup selective PAR SCOPE
 *      → storeFact(source='capture') → markProcessed.
 * Sans LLM disponible : les entrées RESTENT pending (doctor les affiche) —
 * aucun fait inventé, aucune perte.
 *
 * Injection de dépendances : aucun import des implémentations secrets/llm,
 * uniquement leurs interfaces.
 */
import { sha256Hex } from '../util.js'
import { findDuplicate } from './selective.js'
import { WalProcessor, type ProcessOutcome, type WalReplaySummary } from './wal.js'
import type { ContentStore } from '../storage/content.js'
import type { DetectedSecret, Redactor } from '../secrets/types.js'
import type { LlmProvider } from '../llm/provider.js'
import type { ActiveContext, AuditEntry, Fact, StoreFactInput, WalEntry } from '../types.js'

export interface CaptureMessage {
  role: WalEntry['role']
  content: string
}

export interface CaptureTurnInput {
  /** assistant_instance_id */
  instance: string
  messages: CaptureMessage[]
  active_context?: ActiveContext
}

export interface CaptureTurnResult {
  /** Messages écrits au WAL (étape 1 — garantis même si tout le reste échoue). */
  appended: number
  /** Entrées WAL consommées avec succès pendant ce tour. */
  processed: number
  facts_created: number
  /** Entrées restées pending (ex. aucun LLM disponible). */
  deferred: number
  failed: number
  abandoned: number
}

export interface CapturePipelineDeps {
  /** DB de contenu (privée) de l'instance — héberge son wal_buffer. */
  openStore: (instanceId: string) => ContentStore
  /** Scope cible des écritures de capture (privé de l'instance en P2). */
  defaultScope: (instanceId: string) => string
  /** storeFact gouverné (Memoria.storeFact) — audite déjà 'store_fact'. */
  storeFact: (input: StoreFactInput) => Fact
  /** Audit neutre (jamais de contenu) — utilisé pour 'wal_entry_abandoned'. */
  audit: (entry: Omit<AuditEntry, 'id' | 'ts'>) => void
  /** Gate dur secrets — null = pas de redaction (assumé par l'intégrateur). */
  redactor: Redactor | null
  /** Réceptacle des secrets détectés (coffre). null = valeur abandonnée (sûre). */
  secretSink: ((s: DetectedSecret) => void) | null
  /** LLM d'extraction — null/indisponible = les entrées WAL restent pending. */
  extraction: LlmProvider | null
  maxAttempts?: number
  /** Plafond de faits retenus par entrée WAL (anti-spam LLM, défaut 8). */
  maxFactsPerEntry?: number
}

interface TurnGroup {
  /** Messages (déjà rédactés) du tour — extraits en UN SEUL appel LLM. */
  messages: CaptureMessage[]
  context: ActiveContext | undefined
  extracted: boolean
}

interface ExtractedFact {
  fact: string
  category: string
  confidence: number
}

// Objet racine (pas un tableau nu) : le mode JSON d'Ollama pousse les petits
// modèles à émettre un objet — un tableau demandé donnait « {} » (vu en E2E).
const EXTRACTION_SYSTEM = `Tu extrais des faits DURABLES depuis une conversation, pour une mémoire long-terme d'assistant.
Ne retiens QUE le durable : préférences, décisions et leurs raisons, configurations exactes, leçons d'erreurs, processus appris.
N'extrais RIEN d'éphémère (état passager, politesse, question sans réponse).
Réponds UNIQUEMENT avec un objet JSON, sans texte autour :
{"facts": [{"fact": "énoncé autonome et précis", "category": "preference|decision|config|erreur|process|general", "confidence": 0.0-1.0}]}
{"facts": []} si rien ne mérite d'être retenu.`

export class CapturePipeline {
  private readonly deps: CapturePipelineDeps
  private readonly processors = new Map<string, WalProcessor>()
  /** id d'entrée WAL → groupe du tour (mémoire de process uniquement). */
  private readonly groups = new Map<number, TurnGroup>()
  private readonly maxFactsPerEntry: number

  constructor(deps: CapturePipelineDeps) {
    this.deps = deps
    this.maxFactsPerEntry = deps.maxFactsPerEntry ?? 8
  }

  /**
   * ÉTAPE 1 : redaction (gate dur) puis walAppend de CHAQUE message — AVANT
   * tout traitement. ÉTAPE 2 : consommation du pending. Une extraction qui
   * échoue ne fait JAMAIS échouer captureTurn : les messages sont en WAL.
   */
  async captureTurn(input: CaptureTurnInput): Promise<CaptureTurnResult> {
    const store = this.deps.openStore(input.instance)

    const redacted: CaptureMessage[] = []
    for (const message of input.messages) {
      const content = message.content.trim()
      if (!content) continue
      redacted.push({ role: message.role, content: this.redact(content) })
    }

    const ids: number[] = []
    for (const message of redacted) {
      ids.push(store.walAppend(input.instance, message.role, message.content))
    }
    if (ids.length > 0) {
      const group: TurnGroup = { messages: redacted, context: input.active_context, extracted: false }
      for (const id of ids) this.groups.set(id, group)
    }

    const run = await this.processorFor(input.instance, store).processPending()
    return {
      appended: ids.length,
      processed: run.processed,
      facts_created: run.facts_created,
      deferred: run.deferred,
      failed: run.failed,
      abandoned: run.abandoned,
    }
  }

  /** Rejeu au boot (daemon) pour une instance : pending → extraction, puis cleanup borné. */
  replayAtBoot(instanceId: string): Promise<WalReplaySummary> {
    const store = this.deps.openStore(instanceId)
    return this.processorFor(instanceId, store).replayAtBoot()
  }

  // ------------------------------------------------------------------ interne

  private processorFor(instanceId: string, store: ContentStore): WalProcessor {
    let processor = this.processors.get(instanceId)
    if (!processor) {
      processor = new WalProcessor({
        store,
        processEntry: entry => this.processEntry(instanceId, store, entry),
        maxAttempts: this.deps.maxAttempts,
        onPermanentFailure: (entry, error) => {
          this.groups.delete(entry.id)
          // Audit NEUTRE : id hashé + nb de tentatives — jamais le contenu.
          this.deps.audit({
            actor_type: 'system',
            actor_id: 'capture-pipeline',
            action: 'wal_entry_abandoned',
            target_id_hash: sha256Hex(`wal:${store.path}:${entry.id}`),
            scope_id: null,
            reason: `attempts=${entry.attempts}; error=${error instanceof Error ? error.constructor.name : typeof error}`,
          })
        },
      })
      this.processors.set(instanceId, processor)
    }
    return processor
  }

  private async processEntry(instanceId: string, store: ContentStore, entry: WalEntry): Promise<ProcessOutcome> {
    const group = this.groups.get(entry.id)
    if (group) {
      if (group.extracted) {
        // Tour déjà extrait via une autre entrée du même groupe (1 LLM/tour).
        this.groups.delete(entry.id)
        return { status: 'done', facts_created: 0 }
      }
      const outcome = await this.extractAndStore(instanceId, store, group.messages, group.context)
      if (outcome.status === 'done') {
        group.extracted = true
        this.groups.delete(entry.id)
      }
      return outcome
    }
    // Entrée orpheline (rejeu post-crash : le groupage mémoire est perdu) :
    // extraction individuelle, re-redaction par défense (entrées legacy importées).
    const message: CaptureMessage = { role: entry.role, content: this.redact(entry.content) }
    return this.extractAndStore(instanceId, store, [message], undefined)
  }

  /** Gate dur : secrets détectés → secretSink (coffre), texte remplacé par [secret:…]. */
  private redact(text: string): string {
    if (!this.deps.redactor) return text
    const result = this.deps.redactor.redact(text)
    for (const secret of result.found) {
      if (this.deps.secretSink) {
        this.deps.secretSink(secret)
      } else {
        // Valeur abandonnée (jamais stockée) — visible, pas muet.
        console.warn(`[memoria] secret « ${secret.name} » (${secret.kind}) détecté sans coffre configuré : valeur non conservée`)
      }
    }
    return result.text
  }

  /** 1 SEUL appel LLM pour tout le lot de messages, puis dedup + store par fait. */
  private async extractAndStore(
    instanceId: string,
    store: ContentStore,
    messages: CaptureMessage[],
    context: ActiveContext | undefined,
  ): Promise<ProcessOutcome> {
    const { extraction } = this.deps
    if (!extraction || !(await extraction.isAvailable())) {
      // Pas d'invention de faits : l'entrée RESTE pending (doctor l'affichera).
      return { status: 'defer', reason: 'no-llm' }
    }

    const prompt = buildExtractionPrompt(messages)
    const raw = await extraction.complete({
      system: EXTRACTION_SYSTEM,
      prompt,
      json: true,
      maxTokens: 1024,
      temperature: 0.1,
    })
    const extracted = parseFactArray(raw).slice(0, this.maxFactsPerEntry)

    const scopeId = this.deps.defaultScope(instanceId)
    let created = 0
    for (const item of extracted) {
      if (findDuplicate(store, scopeId, item.fact)) continue
      this.deps.storeFact({
        instance: instanceId,
        scope: scopeId,
        content: item.fact,
        category: item.category,
        confidence: item.confidence,
        source: 'capture',
        org_id: context?.org_id ?? null,
        client_org_id: context?.client_org_id ?? null,
        project_id: context?.project_id ?? null,
      })
      created++
    }
    return { status: 'done', facts_created: created }
  }
}

function buildExtractionPrompt(messages: CaptureMessage[]): string {
  const lines = messages.map(m => `- [${m.role}] ${m.content}`)
  return `Messages du tour :\n${lines.join('\n')}\n\nObjet JSON {"facts": [...]} des faits durables :`
}

/**
 * Parse robuste de la sortie LLM : accepte `{"facts": [...]}` (forme demandée)
 * ou un tableau nu `[...]`, extrait du texte environnant si besoin, valide
 * chaque item. Échec → throw avec extrait (retry WAL).
 */
export function parseFactArray(raw: string): ExtractedFact[] {
  let parsed: unknown
  try {
    parsed = JSON.parse(raw)
  } catch {
    // sortie verbeuse : extraire le premier bloc JSON plausible
    const objStart = raw.indexOf('{')
    const objEnd = raw.lastIndexOf('}')
    const arrStart = raw.indexOf('[')
    const arrEnd = raw.lastIndexOf(']')
    const candidate =
      objStart !== -1 && objEnd > objStart && (arrStart === -1 || objStart < arrStart)
        ? raw.slice(objStart, objEnd + 1)
        : arrStart !== -1 && arrEnd > arrStart
          ? raw.slice(arrStart, arrEnd + 1)
          : null
    if (candidate === null) {
      throw new Error(`extraction LLM sans JSON : « ${excerpt(raw)} »`)
    }
    try {
      parsed = JSON.parse(candidate)
    } catch {
      throw new Error(`extraction LLM illisible (JSON invalide) : « ${excerpt(candidate)} »`)
    }
  }
  if (parsed !== null && typeof parsed === 'object' && !Array.isArray(parsed)) {
    const inner = (parsed as Record<string, unknown>)['facts']
    if (inner === undefined || inner === null) return [] // {"facts" absent} / {} = rien à retenir
    parsed = inner
  }
  if (!Array.isArray(parsed)) {
    throw new Error(`extraction LLM : tableau attendu, reçu ${typeof parsed}`)
  }
  const facts: ExtractedFact[] = []
  for (const item of parsed) {
    if (typeof item !== 'object' || item === null) continue
    const record = item as Record<string, unknown>
    const fact = typeof record.fact === 'string' ? record.fact.trim() : ''
    if (fact.length < 5) continue
    const category = typeof record.category === 'string' && record.category.trim() ? record.category.trim().toLowerCase() : 'general'
    const confidence = typeof record.confidence === 'number' ? Math.min(1, Math.max(0, record.confidence)) : 0.7
    facts.push({ fact, category, confidence })
  }
  return facts
}

function excerpt(text: string, max = 120): string {
  const flat = text.replaceAll('\n', ' ')
  return flat.length > max ? `${flat.slice(0, max)}…` : flat
}
