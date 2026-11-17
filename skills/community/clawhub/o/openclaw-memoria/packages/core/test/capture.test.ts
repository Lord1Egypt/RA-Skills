/**
 * Tests CapturePipeline (spec §6.2) + selective :
 *  - WAL append AVANT extraction (extraction qui throw → messages en WAL) ;
 *  - redaction gate dur (le secret n'apparaît NULLE PART dans la DB) ;
 *  - sans LLM → 0 fait, entrées pending, pas d'exception ;
 *  - dédup : même tour capturé 2× → 1 seul fait (dormants inclus) ;
 *  - anti-coût : 1 SEUL appel LLM par tour.
 * Extraction = FAKE provider injecté, déterministe. Aucun réseau, aucun HOME réel.
 */
import { mkdtempSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { ContentStore } from '../src/storage/content.js'
import { CapturePipeline, parseFactArray, type CapturePipelineDeps } from '../src/engine/capture.js'
import { findDuplicate, normalizeFact } from '../src/engine/selective.js'
import type { CompleteOptions, LlmProvider } from '../src/llm/provider.js'
import type { DetectedSecret, RedactionResult, Redactor } from '../src/secrets/types.js'
import type { AuditEntry } from '../src/types.js'

const SCOPE = 'scope-private-test'
const INSTANCE = 'inst-capture-1'

/** Redactor déterministe : motif clé Anthropic → [secret:<name>]. */
class FakeRedactor implements Redactor {
  redact(text: string): RedactionResult {
    const found: DetectedSecret[] = []
    const out = text.replace(/sk-ant-[A-Za-z0-9_-]+/g, value => {
      const name = `anthropic-api-key-${found.length + 1}`
      found.push({ name, kind: 'anthropic', value })
      return `[secret:${name}]`
    })
    return { text: out, found }
  }
}

/** LLM fake : ré-émet chaque ligne de message du prompt comme un fait. */
class FakeLlm implements LlmProvider {
  readonly name = 'fake'
  readonly model = 'fake-extractor'
  available = true
  calls = 0
  completeImpl: (opts: CompleteOptions) => string = opts => {
    const facts = [...opts.prompt.matchAll(/^- \[(?:user|assistant|tool)\] (.+)$/gm)].map(m => ({
      fact: m[1] ?? '',
      category: 'general',
      confidence: 0.9,
    }))
    return JSON.stringify(facts)
  }

  isAvailable(): Promise<boolean> {
    return Promise.resolve(this.available)
  }

  complete(opts: CompleteOptions): Promise<string> {
    this.calls++
    return Promise.resolve(this.completeImpl(opts))
  }
}

let dir: string
let store: ContentStore
let auditLog: Array<Omit<AuditEntry, 'id' | 'ts'>>
let secrets: DetectedSecret[]

function makePipeline(extraction: LlmProvider | null, overrides: Partial<CapturePipelineDeps> = {}): CapturePipeline {
  return new CapturePipeline({
    openStore: () => store,
    defaultScope: () => SCOPE,
    storeFact: input =>
      store.insertFact({
        fact: input.content,
        category: input.category,
        confidence: input.confidence,
        source: input.source,
        assistant_instance_id: input.instance,
        org_id: input.org_id,
        client_org_id: input.client_org_id,
        project_id: input.project_id,
        scope_id: input.scope ?? SCOPE,
      }),
    audit: entry => {
      auditLog.push(entry)
    },
    redactor: new FakeRedactor(),
    secretSink: s => {
      secrets.push(s)
    },
    extraction,
    ...overrides,
  })
}

beforeEach(() => {
  dir = mkdtempSync(join(tmpdir(), 'memoria-capture-'))
  store = new ContentStore(join(dir, 'memory.sqlite'))
  auditLog = []
  secrets = []
  // Aucun test ne touche le réseau — fetch interdit par construction.
  vi.stubGlobal('fetch', () => {
    throw new Error('réseau interdit dans les tests')
  })
})

afterEach(() => {
  store.close()
  rmSync(dir, { recursive: true, force: true })
  vi.unstubAllGlobals()
  vi.restoreAllMocks()
})

describe('captureTurn — WAL d’abord', () => {
  it('append AVANT extraction : extraction qui throw → les messages sont quand même en WAL', async () => {
    vi.spyOn(console, 'warn').mockImplementation(() => {})
    const llm = new FakeLlm()
    let pendingAtCallTime = -1
    llm.completeImpl = () => {
      pendingAtCallTime = store.walPendingCount() // preuve d'ordre : déjà appendé
      throw new Error('extraction en panne')
    }
    const pipeline = makePipeline(llm)

    const result = await pipeline.captureTurn({
      instance: INSTANCE,
      messages: [
        { role: 'user', content: 'On passe le déploiement memoria sur la branche memoria-v1' },
        { role: 'assistant', content: 'Noté, je mets à jour la configuration de build' },
      ],
    })

    expect(result.appended).toBe(2)
    expect(result.facts_created).toBe(0)
    expect(pendingAtCallTime).toBe(2) // les 2 messages étaient en WAL AVANT le 1er appel LLM
    const rows = store.db.prepare('SELECT content FROM wal_buffer ORDER BY id').all() as Array<{ content: string }>
    expect(rows.map(r => r.content)).toEqual([
      'On passe le déploiement memoria sur la branche memoria-v1',
      'Noté, je mets à jour la configuration de build',
    ])
    expect(store.walPendingCount()).toBe(2) // rien de perdu, retry possible
    expect(store.countFacts()).toBe(0)
  })

  it('anti-coût : 1 SEUL appel LLM pour un tour de 3 messages', async () => {
    const llm = new FakeLlm()
    const pipeline = makePipeline(llm)
    const result = await pipeline.captureTurn({
      instance: INSTANCE,
      messages: [
        { role: 'user', content: 'Le projet primask utilise stripe en mode live' },
        { role: 'assistant', content: 'La signature windows reste le point manquant du produit' },
        { role: 'user', content: 'Le panneau admin sert de readiness pour le paiement' },
      ],
    })
    expect(llm.calls).toBe(1)
    expect(result.processed).toBe(3) // les 3 entrées WAL consommées
    expect(result.facts_created).toBe(3)
    expect(store.walPendingCount()).toBe(0)
  })

  it('abandon après maxAttempts → audit wal_entry_abandoned neutre, contenu encore en table', async () => {
    vi.spyOn(console, 'warn').mockImplementation(() => {})
    const llm = new FakeLlm()
    llm.completeImpl = () => {
      throw new Error('panne définitive')
    }
    const pipeline = makePipeline(llm, { maxAttempts: 1 })

    const result = await pipeline.captureTurn({
      instance: INSTANCE,
      messages: [{ role: 'user', content: 'contenu sensible qui ne doit pas fuiter en audit' }],
    })

    expect(result.abandoned).toBe(1)
    const abandonEntries = auditLog.filter(e => e.action === 'wal_entry_abandoned')
    expect(abandonEntries).toHaveLength(1)
    expect(abandonEntries[0]!.target_id_hash).toMatch(/^[0-9a-f]{64}$/)
    expect(abandonEntries[0]!.reason ?? '').not.toContain('sensible') // audit neutre : jamais le contenu
    const row = store.db.prepare('SELECT processed, content FROM wal_buffer').get() as { processed: number; content: string }
    expect(row.processed).toBe(1) // sorti de la file…
    expect(row.content).toContain('contenu sensible') // …mais pas perdu
  })
})

describe('redaction — gate dur secrets', () => {
  it('un sk-ant-xxx dans le message → fait stocké avec [secret:…], valeur NULLE PART dans la DB', async () => {
    const llm = new FakeLlm()
    const pipeline = makePipeline(llm)
    const result = await pipeline.captureTurn({
      instance: INSTANCE,
      messages: [{ role: 'user', content: 'La clé API du projet est sk-ant-abc123XYZ pour le provider cloud' }],
    })

    expect(result.facts_created).toBe(1)
    expect(secrets).toHaveLength(1)
    expect(secrets[0]!.value).toBe('sk-ant-abc123XYZ') // la valeur part au coffre…

    // …le fait stocké ne contient que la référence
    const fact = store.db.prepare('SELECT fact FROM facts').get() as { fact: string }
    expect(fact.fact).toContain('[secret:anthropic-api-key-1]')

    // …et la valeur n'apparaît NULLE PART : scan SQL de toutes les tables à contenu
    for (const table of ['facts', 'wal_buffer', 'procedures', 'topics']) {
      const cols = (store.db.prepare(`PRAGMA table_info(${table})`).all() as Array<{ name: string }>).map(c => c.name)
      for (const col of cols) {
        const hit = store.db
          .prepare(`SELECT COUNT(*) AS c FROM ${table} WHERE CAST(${col} AS TEXT) LIKE ?`)
          .get('%sk-ant-abc123XYZ%') as { c: number }
        expect(hit.c, `${table}.${col} contient le secret`).toBe(0)
      }
    }
    // l'index FTS non plus (alimenté par triggers depuis facts)
    const fts = store.db.prepare("SELECT COUNT(*) AS c FROM facts_fts WHERE facts_fts MATCH '\"abc123XYZ\"'").get() as { c: number }
    expect(fts.c).toBe(0)
  })
})

describe('sans LLM — pas d’invention, pas de perte', () => {
  it('extraction null → 0 fait, entrées pending, pas d’exception', async () => {
    const pipeline = makePipeline(null)
    const result = await pipeline.captureTurn({
      instance: INSTANCE,
      messages: [{ role: 'user', content: 'Message à garder pour plus tard quand un LLM sera dispo' }],
    })
    expect(result.facts_created).toBe(0)
    expect(result.deferred).toBe(1)
    expect(store.countFacts()).toBe(0)
    expect(store.walPendingCount()).toBe(1)
    expect(store.walPending(10)[0]!.attempts).toBe(0) // un défaut d'infra ne brûle pas le retry
  })

  it('provider indisponible (isAvailable=false) → même comportement', async () => {
    const llm = new FakeLlm()
    llm.available = false
    const pipeline = makePipeline(llm)
    const result = await pipeline.captureTurn({
      instance: INSTANCE,
      messages: [{ role: 'user', content: 'Encore un message en attente de traitement' }],
    })
    expect(llm.calls).toBe(0)
    expect(result.facts_created).toBe(0)
    expect(store.walPendingCount()).toBe(1)

    // le LLM revient → le pending est consommé au tour suivant (replay)
    llm.available = true
    const replay = await pipeline.replayAtBoot(INSTANCE)
    expect(replay.processed).toBe(1)
    expect(replay.facts_created).toBe(1)
    expect(store.walPendingCount()).toBe(0)
  })
})

describe('dédup selective', () => {
  it('même tour capturé 2× → 1 seul fait', async () => {
    const llm = new FakeLlm()
    const pipeline = makePipeline(llm)
    const messages = [{ role: 'user' as const, content: 'Néto préfère les tests déterministes pour la CI memoria' }]

    const first = await pipeline.captureTurn({ instance: INSTANCE, messages })
    expect(first.facts_created).toBe(1)

    const second = await pipeline.captureTurn({ instance: INSTANCE, messages })
    expect(second.facts_created).toBe(0)
    expect(second.processed).toBe(1) // l'entrée WAL est bien consommée (dup ≠ échec)
    expect(store.countFacts()).toBe(1)
  })

  it('normalizeFact : lowercase + ponctuation/espaces compactés', () => {
    expect(normalizeFact('  Néto PRÉFÈRE,   le café !!  ')).toBe('néto préfère le café')
  })

  it('exact-dup détecté MÊME sur un fait dormant (bug legacy SEL-2 corrigé)', () => {
    const fact = store.insertFact({ fact: 'Le build memoria passe par npm run build', scope_id: SCOPE })
    store.db.prepare("UPDATE facts SET lifecycle_state = 'dormant' WHERE id = ?").run(fact.id)

    const match = findDuplicate(store, SCOPE, 'le build MEMORIA passe par npm run build !')
    expect(match?.kind).toBe('exact')
    expect(match?.existing.id).toBe(fact.id)
  })

  it('near-dup : top-3 FTS + Jaccard > 0.85', () => {
    const base = 'le déploiement vercel du site primo utilise la branche main avec un build vite en production'
    const fact = store.insertFact({ fact: base, scope_id: SCOPE })

    const near = findDuplicate(store, SCOPE, `${base} ok`)
    expect(near?.kind).toBe('near')
    expect(near?.existing.id).toBe(fact.id)

    // un texte réellement différent ne matche pas
    expect(findDuplicate(store, SCOPE, 'la facturation qonto est rapprochée chaque vendredi matin')).toBeNull()
  })

  it('le dedup est borné au scope : même texte dans un autre scope → pas un doublon', () => {
    store.insertFact({ fact: 'Le tarif standard est de 900 euros par jour', scope_id: 'scope-autre' })
    expect(findDuplicate(store, SCOPE, 'Le tarif standard est de 900 euros par jour')).toBeNull()
  })
})

describe('parseFactArray — parse robuste des sorties LLM', () => {
  it('extrait le premier [...] même entouré de texte/fences', () => {
    const raw = 'Voici les faits :\n```json\n[{"fact": "Néto utilise vitest", "category": "Config", "confidence": 1.4}]\n```'
    const facts = parseFactArray(raw)
    expect(facts).toHaveLength(1)
    expect(facts[0]!.category).toBe('config')
    expect(facts[0]!.confidence).toBe(1) // clampé
  })

  it('items invalides filtrés, JSON illisible → throw avec extrait', () => {
    expect(parseFactArray('[{"fact": "ok"}, {"pas": "un fait"}, "texte"]')).toHaveLength(0) // fact < 5 chars + items invalides
    expect(() => parseFactArray('pas de tableau ici')).toThrow(/sans JSON/)
    expect(() => parseFactArray('[{cassé]')).toThrow(/JSON invalide/)
  })
})
