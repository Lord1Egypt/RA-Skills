/**
 * Intégration capture bout-en-bout dans le MOTEUR (P2 câblé) :
 * captureTurn → redaction (gate dur) → WAL → extraction (fake LLM) → dédup →
 * storeFact → recall. + capture_mode incognito + secret jamais persisté.
 */
import { mkdtempSync, readdirSync, readFileSync, rmSync, statSync } from 'node:fs'
import { join } from 'node:path'
import { tmpdir } from 'node:os'
import { afterEach, beforeEach, describe, expect, it } from 'vitest'
import { Memoria, type CompleteOptions, type LlmProvider } from '../src/index.js'

const FAKE_KEY = 'REDACTED-SECRET'

/** LLM d'extraction déterministe : 1 fait durable par tour. */
class FakeExtraction implements LlmProvider {
  readonly name = 'fake'
  readonly model = 'fake-extractor'
  calls = 0
  isAvailable(): Promise<boolean> {
    return Promise.resolve(true)
  }
  complete(opts: CompleteOptions): Promise<string> {
    this.calls++
    // restitue une portion du prompt pour vérifier que la redaction a eu lieu AVANT le LLM
    const leaked = opts.prompt.includes(FAKE_KEY)
    return Promise.resolve(
      JSON.stringify([
        {
          fact: leaked
            ? 'FUITE: la clé est passée au LLM en clair'
            : 'Néto déploie le site Primo sur Vercel avec un compte dédié',
          category: 'config',
          confidence: 0.9,
        },
      ]),
    )
  }
}

let root: string
let m: Memoria
let fake: FakeExtraction

beforeEach(() => {
  root = mkdtempSync(join(tmpdir(), 'memoria-capint-'))
  fake = new FakeExtraction()
  m = Memoria.init({
    storageRoot: root,
    configPath: join(root, 'config.toml'),
    llm: { extraction: fake },
    secretsVault: 'aes-vault',
  })
})

afterEach(() => {
  m.close()
  rmSync(root, { recursive: true, force: true })
})

describe('captureTurn intégré', () => {
  it('capture → extraction → fait retrouvable au recall', async () => {
    const a = m.pairAssistant({ type: 'claude-code' })
    const result = await m.captureTurn({
      instance: a.assistant_instance_id,
      messages: [
        { role: 'user', content: 'On déploie le site sur quoi déjà ?' },
        { role: 'assistant', content: 'Sur Vercel, avec le compte dédié Primo.' },
      ],
    })
    expect(result.mode).toBe('auto-private')
    expect(result.appended).toBe(2)
    expect(result.facts_created).toBeGreaterThan(0)

    const recall = m.recall({ instance: a.assistant_instance_id, query: 'déploiement site Primo Vercel' })
    expect(recall.items.some(i => i.content.includes('Vercel'))).toBe(true)
  })

  it('GATE DUR : un secret capturé ne touche NI le LLM, NI la DB, NI le WAL — et finit au coffre', async () => {
    const a = m.pairAssistant({ type: 'claude-code' })
    await m.captureTurn({
      instance: a.assistant_instance_id,
      messages: [{ role: 'user', content: `Ma clé API est ${FAKE_KEY}, note la config Vercel.` }],
    })

    // le fake LLM signale s'il a vu la clé en clair
    const recall = m.recall({ instance: a.assistant_instance_id, query: 'FUITE clé clair Vercel config' })
    expect(recall.items.every(i => !i.content.includes('FUITE'))).toBe(true)

    // la valeur n'apparaît dans AUCUN fichier du stockage (DB, WAL, vault en clair)
    const offenders: string[] = []
    const walk = (dir: string): void => {
      for (const name of readdirSync(dir)) {
        const p = join(dir, name)
        if (statSync(p).isDirectory()) walk(p)
        else if (readFileSync(p).includes(FAKE_KEY)) offenders.push(p)
      }
    }
    walk(root)
    expect(offenders).toEqual([])

    // référence enregistrée + valeur récupérable depuis le coffre chiffré
    const refs = m.registry.listSecretRefs()
    expect(refs.length).toBe(1)
    expect(refs[0]!.location).toContain('vault:')
    expect(m['secretProvider'].get(refs[0]!.name)).toBe(FAKE_KEY)
  })

  it('incognito : AUCUNE écriture (ni WAL ni fait)', async () => {
    const a = m.pairAssistant({ type: 'claude-code' })
    m.setCaptureMode('incognito')
    const result = await m.captureTurn({
      instance: a.assistant_instance_id,
      messages: [{ role: 'user', content: 'ceci ne doit laisser aucune trace' }],
    })
    expect(result).toMatchObject({ appended: 0, facts_created: 0, mode: 'incognito' })

    const store = m['openContent'](m.paths.assistantDb(a.assistant_instance_id))
    expect(store.walPendingCount()).toBe(0)
    expect(store.countFacts()).toBe(0)

    // retour en auto-private → la capture reprend
    m.setCaptureMode('auto-private')
    const back = await m.captureTurn({
      instance: a.assistant_instance_id,
      messages: [{ role: 'assistant', content: 'On choisit Postgres pour la prod, décision actée.' }],
    })
    expect(back.appended).toBe(1)
  })

  it('dédup : capturer deux fois le même tour ne crée qu’un fait', async () => {
    const a = m.pairAssistant({ type: 'claude-code' })
    const messages = [{ role: 'assistant' as const, content: 'Le déploiement se fait sur Vercel compte Primo.' }]
    const r1 = await m.captureTurn({ instance: a.assistant_instance_id, messages })
    const r2 = await m.captureTurn({ instance: a.assistant_instance_id, messages })
    expect(r1.facts_created).toBe(1)
    expect(r2.facts_created).toBe(0)
  })
})
