/**
 * Importeur de transcripts (spec §7.2) :
 *  - parsers des 4 formats réels (Claude Code / Codex rollout / Codex history /
 *    Markdown) sur des mini-fichiers reproduisant les structures EXACTES, bruit
 *    filtré ;
 *  - importTranscripts → faits en QUARANTAINE (dormant + pending) : invisibles
 *    au recall, visibles via listReview, approuvables par lot ;
 *  - idempotence (ré-import = 0 nouveau), dédup (même fait sur 2 fenêtres = 1),
 *    dryRun (0 écriture), sinceDate (filtre les vieux tours), sans LLM (0 fait).
 */
import { mkdtempSync, rmSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { afterEach, beforeEach, describe, expect, it } from 'vitest'
import { Memoria } from '../src/engine/memoria.js'
import { ContentStore } from '../src/storage/content.js'
import {
  detectTranscriptFormat,
  parseClaudeCodeTranscript,
  parseCodexHistory,
  parseCodexRollout,
  parseMarkdown,
} from '../src/migration/transcript-parsers.js'
import { importTranscripts } from '../src/migration/import-transcripts.js'
import type { CompleteOptions, LlmProvider } from '../src/llm/provider.js'

// ───────────────────────────── Faux LLM déterministe ─────────────────────────

/** Émet 1 fait durable par fenêtre, dérivé du contenu (faits distincts). */
class FakeExtraction implements LlmProvider {
  readonly name = 'fake'
  readonly model = 'fake'
  calls = 0
  isAvailable(): Promise<boolean> {
    return Promise.resolve(true)
  }
  complete(opts: CompleteOptions): Promise<string> {
    this.calls++
    // Fait dérivé d'un mot saillant du prompt → un fait par fenêtre, distinct.
    const m = opts.prompt.match(/\b(scaleway|convex|vitest|postgres|stripe|vercel|ollama|qwen)\b/i)
    const topic = m ? m[1]!.toLowerCase() : `sujet${this.calls}`
    return Promise.resolve(
      JSON.stringify({
        facts: [{ fact: `Le projet utilise ${topic} comme brique technique de référence`, category: 'config', confidence: 0.9 }],
      }),
    )
  }
}

/** Émet TOUJOURS le même fait → teste la dédup inter-fenêtres. */
class ConstantExtraction implements LlmProvider {
  readonly name = 'const'
  readonly model = 'const'
  isAvailable(): Promise<boolean> {
    return Promise.resolve(true)
  }
  complete(): Promise<string> {
    return Promise.resolve(
      JSON.stringify({ facts: [{ fact: 'Le déploiement se fait sur Vercel en production', category: 'process', confidence: 0.9 }] }),
    )
  }
}

// ─────────────────────────────── Parsers ───────────────────────────────

describe('parsers', () => {
  it('Claude Code : type user/assistant, content string OU blocs text, bruit tool_use/thinking ignoré', () => {
    const lines = [
      // contenu = string
      JSON.stringify({ type: 'user', timestamp: '2026-06-01T10:00:00.000Z', message: { role: 'user', content: 'Configure le projet avec Convex.' } }),
      // contenu = tableau de blocs (text + thinking + tool_use à filtrer)
      JSON.stringify({
        type: 'assistant',
        timestamp: '2026-06-01T10:00:05.000Z',
        message: {
          role: 'assistant',
          content: [
            { type: 'thinking', thinking: 'réflexion interne à ignorer' },
            { type: 'text', text: 'Convex est configuré.' },
            { type: 'tool_use', name: 'Bash', input: { command: 'ls' } },
          ],
        },
      }),
      // événements à ignorer : summary + tool_result-only
      JSON.stringify({ type: 'summary', summary: 'résumé', leafUuid: 'x' }),
      JSON.stringify({ type: 'user', message: { role: 'user', content: [{ type: 'tool_result', content: 'sortie outil' }] } }),
      'ligne json invalide {{{', // ligne corrompue : ignorée, pas de throw
    ].join('\n')

    const turns = parseClaudeCodeTranscript(lines)
    expect(turns).toHaveLength(2)
    expect(turns[0]).toMatchObject({ role: 'user', text: 'Configure le projet avec Convex.' })
    expect(turns[0]!.ts).toBe('2026-06-01T10:00:00.000Z')
    expect(turns[1]).toMatchObject({ role: 'assistant', text: 'Convex est configuré.' })
  })

  it('Codex rollout : response_item/message, blocs input_text/output_text, environment_context ignoré', () => {
    const lines = [
      JSON.stringify({
        timestamp: '2026-06-02T08:00:00.000Z',
        type: 'response_item',
        payload: { type: 'message', role: 'user', content: [{ type: 'input_text', text: 'Ajoute des tests vitest.' }] },
      }),
      JSON.stringify({
        timestamp: '2026-06-02T08:00:10.000Z',
        type: 'response_item',
        payload: { type: 'message', role: 'assistant', content: [{ type: 'output_text', text: 'Tests vitest ajoutés.' }] },
      }),
      // bruit système : <environment_context> → filtré
      JSON.stringify({
        timestamp: '2026-06-02T07:59:00.000Z',
        type: 'response_item',
        payload: { type: 'message', role: 'user', content: [{ type: 'input_text', text: '<environment_context>cwd=/x</environment_context>' }] },
      }),
      // autres types à ignorer
      JSON.stringify({ timestamp: '2026-06-02T08:00:05.000Z', type: 'response_item', payload: { type: 'function_call', name: 'shell' } }),
      JSON.stringify({ timestamp: '2026-06-02T08:00:01.000Z', type: 'event_msg', payload: { type: 'token_count' } }),
    ].join('\n')

    const turns = parseCodexRollout(lines)
    expect(turns).toHaveLength(2)
    expect(turns[0]).toMatchObject({ role: 'user', text: 'Ajoute des tests vitest.' })
    expect(turns[1]).toMatchObject({ role: 'assistant', text: 'Tests vitest ajoutés.' })
  })

  it('Codex history : prompts user seuls, ts epoch s → ISO', () => {
    const lines = [
      JSON.stringify({ session_id: 's1', ts: 1_733_040_000, text: 'Migre vers Postgres.' }),
      JSON.stringify({ session_id: 's1', ts: 1_733_040_060, text: 'Utilise Stripe pour le paiement.' }),
      'corrompu', // ignorée
    ].join('\n')

    const turns = parseCodexHistory(lines)
    expect(turns).toHaveLength(2)
    expect(turns.every(t => t.role === 'user')).toBe(true)
    expect(turns[0]!.text).toBe('Migre vers Postgres.')
    expect(turns[0]!.ts).toBe(new Date(1_733_040_000_000).toISOString())
  })

  it('Markdown : découpe en sections de titre ##, role user', () => {
    const md = ['# Titre principal', 'intro', '', '## Section A', 'contenu A sur plusieurs', 'lignes', '', '## Section B', 'contenu B'].join('\n')
    const turns = parseMarkdown(md)
    expect(turns.length).toBeGreaterThanOrEqual(2)
    expect(turns.every(t => t.role === 'user')).toBe(true)
    expect(turns.some(t => t.text.includes('Section A') && t.text.includes('contenu A'))).toBe(true)
    expect(turns.some(t => t.text.includes('Section B'))).toBe(true)
  })

  it('detectTranscriptFormat : par chemin et par contenu', () => {
    expect(detectTranscriptFormat('/home/u/.codex/history.jsonl', '')).toBe('codex-history')
    expect(detectTranscriptFormat('/home/u/.codex/sessions/2026/06/01/rollout-abc.jsonl', '')).toBe('codex-rollout')
    expect(detectTranscriptFormat('/home/u/.claude/projects/slug/uuid.jsonl', '')).toBe('claude-code')
    expect(detectTranscriptFormat('/x/notes.md', '')).toBe('markdown')
    // par contenu (extension/chemin ambigus)
    expect(detectTranscriptFormat('/x/dump.jsonl', JSON.stringify({ session_id: 's', ts: 1, text: 'hi' }))).toBe('codex-history')
    expect(detectTranscriptFormat('/x/dump.jsonl', JSON.stringify({ timestamp: 't', type: 'response_item', payload: { type: 'message' } }))).toBe('codex-rollout')
    expect(detectTranscriptFormat('/x/dump.jsonl', JSON.stringify({ type: 'user', message: { role: 'user', content: 'hi' } }))).toBe('claude-code')
    expect(detectTranscriptFormat('/x/whatever.txt', 'juste du texte libre')).toBe('unknown')
  })
})

// ─────────────────────────── importTranscripts ───────────────────────────

let root: string
let m: Memoria | undefined
let instance: string

function newMemoria(extraction: LlmProvider | null): Memoria {
  m = Memoria.init({
    storageRoot: root,
    configPath: join(root, 'config.toml'),
    llm: { extraction },
    secretsVault: 'aes-vault',
  })
  return m
}

beforeEach(() => {
  root = mkdtempSync(join(tmpdir(), 'memoria-transcripts-'))
  m = undefined
})

afterEach(() => {
  // Les tests de parsers n'instancient pas Memoria ; ne fermer que si créé.
  m?.close()
  m = undefined
  rmSync(root, { recursive: true, force: true })
})

/** Écrit un transcript Claude Code multi-tours (génère ≥2 fenêtres). */
function writeClaudeFile(path: string, topics: string[], baseTs = '2026-06-05T10:00:00.000Z'): void {
  const lines: string[] = []
  let t = Date.parse(baseTs)
  for (const topic of topics) {
    lines.push(JSON.stringify({ type: 'user', timestamp: new Date(t).toISOString(), message: { role: 'user', content: `On parle de ${topic} maintenant.` } }))
    t += 60_000
    lines.push(JSON.stringify({ type: 'assistant', timestamp: new Date(t).toISOString(), message: { role: 'assistant', content: [{ type: 'text', text: `D'accord, ${topic} est en place et fonctionne bien.` }] } }))
    t += 60_000
  }
  writeFileSync(path, lines.join('\n'))
}

describe('importTranscripts — quarantaine de revue', () => {
  it('faits en quarantaine (dormant + pending) : invisibles au recall, visibles via listReview, approuvables', async () => {
    const fake = new FakeExtraction()
    const mem = newMemoria(fake)
    instance = mem.pairAssistant({ type: 'claude-code' }).assistant_instance_id

    const file = join(root, 'conv.jsonl')
    // 4 sujets × 2 tours = 8 tours → ≥2 fenêtres (6 tours/fenêtre)
    writeClaudeFile(file, ['scaleway', 'convex', 'vitest', 'postgres'])

    const report = await importTranscripts({ files: [file], memoria: mem, instanceId: instance, extraction: fake })

    expect(report.errors).toEqual([])
    expect(report.files_read).toBe(1)
    expect(report.windows).toBeGreaterThanOrEqual(2)
    expect(fake.calls).toBe(report.windows) // 1 appel LLM / fenêtre
    expect(report.facts_quarantined).toBeGreaterThanOrEqual(2)

    // INVISIBLE au recall normal (faits dormants)
    expect(mem.recall({ instance, query: 'scaleway brique technique' }).items).toHaveLength(0)
    expect(mem.recall({ instance, query: 'convex référence' }).items).toHaveLength(0)

    // VISIBLE dans la file de revue, provenance 'transcript'
    const pending = mem.listReview()
    expect(pending.length).toBe(report.facts_quarantined)
    expect(pending.every(p => p.source_type === 'transcript')).toBe(true)

    // Approbation par lot → recallable
    const { updated } = mem.reviewDecision(pending.map(p => p.id), 'accepted')
    expect(updated).toBe(pending.length)
    expect(mem.recall({ instance, query: 'scaleway brique technique' }).items.length).toBeGreaterThanOrEqual(1)
    expect(mem.listReview()).toHaveLength(0)
  })

  it('idempotence : ré-importer le même fichier → 0 nouveau', async () => {
    const fake = new FakeExtraction()
    const mem = newMemoria(fake)
    instance = mem.pairAssistant({ type: 'claude-code' }).assistant_instance_id
    const file = join(root, 'conv.jsonl')
    writeClaudeFile(file, ['scaleway', 'convex'])

    const first = await importTranscripts({ files: [file], memoria: mem, instanceId: instance, extraction: fake })
    expect(first.facts_quarantined).toBeGreaterThanOrEqual(1)

    const second = await importTranscripts({ files: [file], memoria: mem, instanceId: instance, extraction: fake })
    expect(second.files_skipped_already_imported).toBe(1)
    expect(second.files_read).toBe(0)
    expect(second.facts_quarantined).toBe(0)
    expect(second.windows).toBe(0)

    // toujours le même nombre d'items en revue
    expect(mem.listReview().length).toBe(first.facts_quarantined)
  })

  it('dédup : 2 fenêtres produisant le même fait → 1 seul quarantiné', async () => {
    const constant = new ConstantExtraction()
    const mem = newMemoria(constant)
    instance = mem.pairAssistant({ type: 'claude-code' }).assistant_instance_id
    const file = join(root, 'conv.jsonl')
    // 6 sujets × 2 = 12 tours → ≥2 fenêtres, toutes renvoient LE MÊME fait
    writeClaudeFile(file, ['a', 'b', 'c', 'd', 'e', 'f'])

    const report = await importTranscripts({ files: [file], memoria: mem, instanceId: instance, extraction: constant })
    expect(report.windows).toBeGreaterThanOrEqual(2)
    expect(report.facts_extracted).toBeGreaterThanOrEqual(2)
    expect(report.facts_quarantined).toBe(1)
    expect(report.facts_skipped_duplicates).toBeGreaterThanOrEqual(1)
    expect(mem.listReview()).toHaveLength(1)
  })

  it('dryRun : parse + compte, AUCUNE écriture', async () => {
    const fake = new FakeExtraction()
    const mem = newMemoria(fake)
    instance = mem.pairAssistant({ type: 'claude-code' }).assistant_instance_id
    const file = join(root, 'conv.jsonl')
    writeClaudeFile(file, ['scaleway', 'convex', 'vitest', 'postgres'])

    const report = await importTranscripts({ files: [file], memoria: mem, instanceId: instance, extraction: fake, dryRun: true })
    expect(report.dry_run).toBe(true)
    expect(report.windows).toBeGreaterThanOrEqual(2)
    expect(report.facts_quarantined).toBe(0)
    expect(fake.calls).toBe(0) // aucune extraction en dry-run

    const store = new ContentStore(mem.paths.assistantDb(instance))
    expect(store.countFacts()).toBe(0)
    const sources = store.db.prepare("SELECT COUNT(*) AS c FROM memory_sources WHERE source_type = 'transcript'").get() as { c: number }
    expect(sources.c).toBe(0)
    store.close()
    expect(mem.listReview()).toHaveLength(0)
  })

  it('sinceDate : filtre les vieux tours', async () => {
    const fake = new FakeExtraction()
    const mem = newMemoria(fake)
    instance = mem.pairAssistant({ type: 'claude-code' }).assistant_instance_id
    const file = join(root, 'conv.jsonl')

    // 2 tours anciens (2026-01) + 2 récents (2026-06)
    const lines = [
      JSON.stringify({ type: 'user', timestamp: '2026-01-01T10:00:00.000Z', message: { role: 'user', content: 'Vieux sujet ollama.' } }),
      JSON.stringify({ type: 'assistant', timestamp: '2026-01-01T10:01:00.000Z', message: { role: 'assistant', content: [{ type: 'text', text: 'Vieille réponse ollama.' }] } }),
      JSON.stringify({ type: 'user', timestamp: '2026-06-01T10:00:00.000Z', message: { role: 'user', content: 'Sujet récent stripe.' } }),
      JSON.stringify({ type: 'assistant', timestamp: '2026-06-01T10:01:00.000Z', message: { role: 'assistant', content: [{ type: 'text', text: 'Réponse récente stripe.' }] } }),
    ].join('\n')
    writeFileSync(file, lines)

    const report = await importTranscripts({
      files: [file],
      memoria: mem,
      instanceId: instance,
      extraction: fake,
      sinceDate: '2026-05-01T00:00:00.000Z',
    })

    // Seuls les tours récents survivent → 1 seule fenêtre (2 tours), 1 appel LLM.
    expect(report.windows).toBe(1)
    expect(fake.calls).toBe(1)
    expect(report.facts_quarantined).toBe(1)
  })

  it('sans LLM : 0 fait extrait, note no-llm, aucune invention', async () => {
    const mem = newMemoria(null)
    instance = mem.pairAssistant({ type: 'claude-code' }).assistant_instance_id
    const file = join(root, 'conv.jsonl')
    writeClaudeFile(file, ['scaleway', 'convex'])

    const report = await importTranscripts({ files: [file], memoria: mem, instanceId: instance, extraction: null })
    expect(report.facts_quarantined).toBe(0)
    expect(report.facts_extracted).toBe(0)
    expect(report.notes.some(n => n.startsWith('no-llm'))).toBe(true)
    expect(mem.listReview()).toHaveLength(0)
  })

  it('maxWindowsPerFile : garde les fenêtres récentes et signale les ignorées', async () => {
    const fake = new FakeExtraction()
    const mem = newMemoria(fake)
    instance = mem.pairAssistant({ type: 'claude-code' }).assistant_instance_id
    const file = join(root, 'big.jsonl')
    // 18 sujets × 2 = 36 tours → 6 fenêtres ; cap à 2 → 4 ignorées.
    writeClaudeFile(file, Array.from({ length: 18 }, (_, i) => `t${i}`))

    const report = await importTranscripts({ files: [file], memoria: mem, instanceId: instance, extraction: fake, maxWindowsPerFile: 2 })
    expect(report.windows).toBe(2)
    expect(report.notes.some(n => n.includes('fenêtre(s) ancienne(s) ignorée(s)'))).toBe(true)
  })

  it('onProgress : appelé après CHAQUE fichier avec compteurs exacts (et un callback qui jette ne casse rien)', async () => {
    const fake = new FakeExtraction()
    const mem = newMemoria(fake)
    instance = mem.pairAssistant({ type: 'claude-code' }).assistant_instance_id
    const fileA = join(root, 'a.jsonl')
    const fileB = join(root, 'b.jsonl')
    writeClaudeFile(fileA, ['scaleway'])
    writeClaudeFile(fileB, ['convex'])

    const ticks: Array<{ filesDone: number; filesTotal: number; factsImported: number }> = []
    const report = await mem.importTranscripts(instance, [fileA, fileB], {
      onProgress: p => ticks.push({ ...p }),
    })

    expect(ticks).toHaveLength(2) // 1 tick par fichier
    expect(ticks[0]).toMatchObject({ filesDone: 1, filesTotal: 2 })
    expect(ticks[1]).toMatchObject({ filesDone: 2, filesTotal: 2 })
    // compteur monotone, et le dernier tick reflète le total final
    expect(ticks[1]!.factsImported).toBeGreaterThanOrEqual(ticks[0]!.factsImported)
    expect(ticks[1]!.factsImported).toBe(report.facts_quarantined)

    // un callback qui jette est loggé mais n'interrompt pas l'import
    const fileC = join(root, 'c.jsonl')
    writeClaudeFile(fileC, ['stripe'])
    const report2 = await mem.importTranscripts(instance, [fileC], {
      onProgress: () => {
        throw new Error('boom UI')
      },
    })
    expect(report2.errors).toEqual([])
    expect(report2.files_read).toBe(1)
  })

  // Demandé par la revue adversariale : prouver que la quarantaine d'un agent
  // ne fuite JAMAIS vers un autre agent, avant ET après approbation.
  it('ANTI-FUITE : transcript importé pour A invisible au recall de B', async () => {
    const fake = new FakeExtraction()
    const mem = newMemoria(fake)
    const a = mem.pairAssistant({ type: 'claude-code', display_name: 'Agent A' }).assistant_instance_id
    const b = mem.pairAssistant({ type: 'codex', display_name: 'Agent B' }).assistant_instance_id
    const file = join(root, 'a.jsonl')
    writeClaudeFile(file, ['deploiement vercel', 'config firebase'])

    await mem.importTranscripts(a, [file])
    const query = 'deploiement vercel config firebase'

    // B ne voit rien, ni avant ni après l'approbation chez A
    expect(mem.recall({ instance: b, query }).items).toHaveLength(0)
    const items = mem.listReview().map(i => i.id)
    expect(items.length).toBeGreaterThan(0)
    mem.reviewDecision(items, 'accepted')
    expect(mem.recall({ instance: b, query }).items).toHaveLength(0)
    // …mais A, lui, retrouve sa mémoire approuvée
    expect(mem.recall({ instance: a, query }).items.length).toBeGreaterThan(0)
  })
})
