/**
 * recallSemantic intégré au moteur : capture → indexation auto → la requête
 * par synonyme retrouve le fait que le FTS seul rate. Anti-fuite et permissions
 * restent vérifiées sur le chemin hybride.
 */
import { mkdtempSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { afterEach, beforeEach, describe, expect, it } from 'vitest'
import { Memoria, type CompleteOptions, type EmbeddingProvider, type LlmProvider } from '../src/index.js'

class FakeExtraction implements LlmProvider {
  readonly name = 'fake'
  readonly model = 'fake'
  isAvailable(): Promise<boolean> {
    return Promise.resolve(true)
  }
  complete(_opts: CompleteOptions): Promise<string> {
    return Promise.resolve(
      JSON.stringify({ facts: [{ fact: "L'automobile de fonction est garée au parking souterrain", category: 'general', confidence: 0.9 }] }),
    )
  }
}

class FakeEmbedding implements EmbeddingProvider {
  readonly name = 'fake'
  readonly model = 'fake-8d'
  readonly dimensions = 8
  isAvailable(): Promise<boolean> {
    return Promise.resolve(true)
  }
  embed(texts: string[]): Promise<Float32Array[]> {
    return Promise.resolve(
      texts.map(t => {
        const v = new Float32Array(8)
        if (/voiture|automobile|véhicule/i.test(t)) v[0] = 1
        else v[6] = 1
        return v
      }),
    )
  }
}

let root: string
let m: Memoria
let instance: string

beforeEach(() => {
  root = mkdtempSync(join(tmpdir(), 'memoria-sem-'))
  m = Memoria.init({
    storageRoot: root,
    configPath: join(root, 'config.toml'),
    llm: { extraction: new FakeExtraction(), embeddings: new FakeEmbedding() },
    secretsVault: 'aes-vault',
  })
  instance = m.pairAssistant({ type: 'claude-code' }).assistant_instance_id
})

afterEach(() => {
  m.close()
  rmSync(root, { recursive: true, force: true })
})

describe('recallSemantic', () => {
  it('capture → indexation → le synonyme retrouve le fait (FTS seul = 0)', async () => {
    await m.captureTurn({ instance, messages: [{ role: 'assistant', content: 'La voiture est au parking.' }] })
    await m.indexEmbeddings(instance) // déterministe pour le test (sinon fire-and-forget)

    // FTS seul : « véhicule » n'apparaît pas dans le texte stocké
    const fts = m.recall({ instance, query: 'véhicule' })
    expect(fts.items).toHaveLength(0)

    const hybrid = await m.recallSemantic({ instance, query: 'véhicule' })
    expect(hybrid.items.length).toBeGreaterThan(0)
    expect(hybrid.items[0]!.content).toContain('automobile')
  })

  it('un fait SPÉCIFIQUE (couvre bcp de termes) bat un fait générique (1 mot commun)', async () => {
    // Régression : le RRF pur classait par rang et enterrait les faits très
    // couvrants derrière des faits génériques fréquents. La couverture lexicale
    // ré-injectée dans hybrid.ts doit remonter le fait spécifique.
    const generic = m.storeFact({ instance, content: 'Quand Neto demande une facture Indy, la télécharger depuis Indy', category: 'general', confidence: 0.7 })
    const specific = m.storeFact({ instance, content: 'Sur Indy, fermer la modale pop-up promo avec la croix avant toute action', category: 'procedure', confidence: 0.9 })
    // Le générique est « chaud » et souvent rappelé (avantage d'ancienneté) :
    // malgré ça, le spécifique doit gagner sur la pertinence lexicale.
    m.recall({ instance, query: 'facture Indy' }) // touchFacts → chauffe le générique
    await m.indexEmbeddings(instance)

    const r = await m.recallSemantic({ instance, query: 'modale pop-up Indy fermer croix' })
    const ids = r.items.map(i => i.id)
    expect(ids).toContain(specific.id)
    expect(ids.indexOf(specific.id)).toBeLessThan(ids.indexOf(generic.id))
  })

  it('requête impérative : une procédure prime sur un fait général équivalent', async () => {
    // Deux faits au TEXTE identique (même couverture, même vecteur) : seul le
    // type diffère. Sur une requête impérative, la procédure doit passer devant.
    const text = 'Sur Indy, fermer la modale avant toute action'
    const general = m.storeFact({ instance, content: text, category: 'general', confidence: 0.8 })
    const procedure = m.storeFact({ instance, content: text, category: 'procedure', confidence: 0.8 })
    await m.indexEmbeddings(instance)

    const r = await m.recallSemantic({ instance, query: 'comment fermer la modale sur Indy' })
    const ids = r.items.map(i => i.id)
    expect(ids).toContain(procedure.id)
    expect(ids.indexOf(procedure.id)).toBeLessThan(ids.indexOf(general.id))
  })

  it('forget nettoie aussi l’index vectoriel (pas de fantôme sémantique)', async () => {
    await m.captureTurn({ instance, messages: [{ role: 'assistant', content: 'La voiture est au parking.' }] })
    await m.indexEmbeddings(instance)
    const before = await m.recallSemantic({ instance, query: 'véhicule' })
    expect(before.items.length).toBeGreaterThan(0)

    m.forget({ ids: [before.items[0]!.id] })

    const after = await m.recallSemantic({ instance, query: 'véhicule' })
    expect(after.items).toHaveLength(0)
  })

  it('sans provider d’embeddings : recallSemantic ≡ recall (dégradation propre)', async () => {
    const m2 = Memoria.init({
      storageRoot: mkdtempSync(join(tmpdir(), 'memoria-sem2-')),
      configPath: join(root, 'config2.toml'),
      llm: { extraction: new FakeExtraction() },
      secretsVault: 'aes-vault',
    })
    const inst2 = m2.pairAssistant({ type: 'codex' }).assistant_instance_id
    await m2.captureTurn({ instance: inst2, messages: [{ role: 'assistant', content: 'La voiture est au parking.' }] })
    const semantic = await m2.recallSemantic({ instance: inst2, query: 'automobile parking' })
    const plain = m2.recall({ instance: inst2, query: 'automobile parking' })
    expect(semantic.items.map(i => i.id)).toEqual(plain.items.map(i => i.id))
    const r2 = m2.paths.root
    m2.close()
    rmSync(r2, { recursive: true, force: true })
  })
})
