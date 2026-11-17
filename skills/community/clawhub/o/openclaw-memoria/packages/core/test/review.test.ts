/**
 * Mode review-first (spec §13 « Import & revue », décision v2.1 #8) :
 * les faits capturés naissent DORMANTS + en file de revue ; approuver = activer,
 * rejeter = hard-delete. Rien ne sort au recall avant approbation.
 */
import { mkdtempSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { afterEach, beforeEach, describe, expect, it } from 'vitest'
import { Memoria, type CompleteOptions, type LlmProvider } from '../src/index.js'

class FakeExtraction implements LlmProvider {
  readonly name = 'fake'
  readonly model = 'fake'
  isAvailable(): Promise<boolean> {
    return Promise.resolve(true)
  }
  complete(_opts: CompleteOptions): Promise<string> {
    return Promise.resolve(JSON.stringify({ facts: [{ fact: 'Le serveur de staging tourne sur scaleway', category: 'config', confidence: 0.85 }] }))
  }
}

let root: string
let m: Memoria
let instance: string

beforeEach(() => {
  root = mkdtempSync(join(tmpdir(), 'memoria-review-'))
  m = Memoria.init({
    storageRoot: root,
    configPath: join(root, 'config.toml'),
    llm: { extraction: new FakeExtraction() },
    secretsVault: 'aes-vault',
  })
  instance = m.pairAssistant({ type: 'claude-code' }).assistant_instance_id
  m.setCaptureMode('review-first')
})

afterEach(() => {
  m.close()
  rmSync(root, { recursive: true, force: true })
})

describe('review-first', () => {
  it('capture → fait dormant + pending ; invisible au recall ; approbation → visible', async () => {
    const cap = await m.captureTurn({
      instance,
      messages: [{ role: 'assistant', content: 'Le staging est chez Scaleway.' }],
    })
    expect(cap.mode).toBe('review-first')
    expect(cap.facts_created).toBe(1)

    // invisible tant que non approuvé
    expect(m.recall({ instance, query: 'serveur staging scaleway' }).items).toHaveLength(0)

    const pending = m.listReview()
    expect(pending).toHaveLength(1)
    expect(pending[0]!.content).toContain('scaleway')
    expect(pending[0]!.source_type).toBe('capture-review')

    const { updated } = m.reviewDecision([pending[0]!.id], 'accepted')
    expect(updated).toBe(1)

    expect(m.recall({ instance, query: 'serveur staging scaleway' }).items).toHaveLength(1)
    expect(m.listReview()).toHaveLength(0)
  })

  it('rejet → hard-delete (aucune trace, même en dormant)', async () => {
    await m.captureTurn({ instance, messages: [{ role: 'assistant', content: 'Le staging est chez Scaleway.' }] })
    const pending = m.listReview()
    expect(pending).toHaveLength(1)

    m.reviewDecision([pending[0]!.id], 'rejected')

    expect(m.recall({ instance, query: 'staging scaleway', include_dormant: true }).items).toHaveLength(0)
    const store = m['openContent'](m.paths.assistantDb(instance))
    expect(store.countFacts()).toBe(0)
    expect(m.listReview()).toHaveLength(0)
  })

  it('en auto-private, pas de file de revue (capture directe active)', async () => {
    m.setCaptureMode('auto-private')
    await m.captureTurn({ instance, messages: [{ role: 'assistant', content: 'Le staging est chez Scaleway.' }] })
    expect(m.listReview()).toHaveLength(0)
    expect(m.recall({ instance, query: 'staging scaleway' }).items).toHaveLength(1)
  })
})
