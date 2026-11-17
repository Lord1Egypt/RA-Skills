/**
 * Couches SELF-OBSERVATION (19) + DIALECTIC (21) — bucket C « Opt-in », spec §12.
 *
 * Garanties PROUVÉES (pas juste « ça compile ») :
 *  SELF-OBSERVATION
 *   - record insère, puis UPSERT idempotent par observation normalisée
 *     (evidence_count++ , pas de doublon, casse/accents/espaces indifférents) ;
 *   - kind invalide / observation vide → throw (pas de mort silencieuse) ;
 *   - deriveFromHistory PROPOSE une « weakness » sur une procédure échouée et une
 *     « strength » sur une procédure réussie ; re-dériver ne duplique pas ;
 *   - list filtre par kind, forget retire ;
 *   - RÈGLE D'OR bucket C : aucun fait inséré/modifié/supprimé par cette couche.
 *  DIALECTIC
 *   - « le port est 8080 » vs « le port est 9090 » → pour/contre répartis,
 *     synthèse NON vide ;
 *   - négation isolée → contre ; marqueur « mais/cependant » → nuance ;
 *   - RÈGLE D'OR : AUCUN fait modifié (compteurs + contenu avant/après) ;
 *   - respecte les scopes (un fait hors scope autorisé n'apparaît pas) ;
 *   - LLM optionnel produit une synthèse ; son indispo retombe sur l'heuristique.
 *
 * Tout est en tmpdir, fake LLM, 0 réseau.
 */
import { mkdtempSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { afterEach, beforeEach, describe, expect, it } from 'vitest'
import { ContentStore } from '../src/storage/content.js'
import type { LlmProvider } from '../src/llm/provider.js'
import {
  SelfObservationEngine,
  selfObservationMigrations,
  ensureSelfObservationSchema,
  SELF_OBSERVATION_KINDS,
  normalizeObservation,
} from '../src/cognition/self-observation.js'
import { dialectic, hasContrast, heuristicSynthesis } from '../src/cognition/dialectic.js'

let dir: string
let store: ContentStore

beforeEach(() => {
  dir = mkdtempSync(join(tmpdir(), 'memoria-self-dialectic-'))
  store = new ContentStore(join(dir, 'c.sqlite'))
})

afterEach(() => {
  store.close()
  rmSync(dir, { recursive: true, force: true })
})

function fact(text: string, scope = 's1'): string {
  return store.insertFact({ fact: text, category: 'general', scope_id: scope }).id
}
function activeFactCount(): number {
  return (store.db.prepare('SELECT COUNT(*) AS c FROM facts WHERE superseded = 0').get() as { c: number }).c
}
function textOf(id: string): string {
  return (store.db.prepare('SELECT fact FROM facts WHERE id = ?').get(id) as { fact: string }).fact
}
function supersededCount(): number {
  return (store.db.prepare('SELECT COUNT(*) AS c FROM facts WHERE superseded = 1').get() as { c: number }).c
}

/** Fake LLM déterministe : répond une chaîne fixe (ou échoue). */
class FakeLlm implements LlmProvider {
  readonly name = 'fake'
  readonly model = 'fake-1'
  completeCalls = 0
  constructor(
    private readonly answer: string,
    private readonly available = true,
    private readonly throwOnAvailable = false,
  ) {}
  isAvailable(): Promise<boolean> {
    if (this.throwOnAvailable) return Promise.reject(new Error('réseau down'))
    return Promise.resolve(this.available)
  }
  complete(): Promise<string> {
    this.completeCalls++
    return Promise.resolve(this.answer)
  }
}

// ===========================================================================
// SELF-OBSERVATION
// ===========================================================================

describe('self-observation — schéma & migrations', () => {
  it('migrations réservées au créneau 70-79', () => {
    for (const m of selfObservationMigrations) {
      expect(m.version).toBeGreaterThanOrEqual(70)
      expect(m.version).toBeLessThanOrEqual(79)
    }
  })

  it('ensureSelfObservationSchema est idempotent (no-op si déjà appliqué)', () => {
    // La migration est désormais câblée au tronc (ContentStore l'applique au
    // constructeur) → ensure est toujours un no-op ici, et reste idempotent.
    expect(ensureSelfObservationSchema(store.db)).toBe(0)
    expect(ensureSelfObservationSchema(store.db)).toBe(0)
  })

  it('CHECK SQL rejette un kind hors liste', () => {
    new SelfObservationEngine({ store })
    expect(() =>
      store.db
        .prepare(
          `INSERT INTO self_observations (id, instance_id, observation, kind, evidence_count, confidence, created_at, updated_at)
           VALUES ('x','', 'truc', 'inconnu', 1, 0.5, '2026-01-01', '2026-01-01')`,
        )
        .run(),
    ).toThrow()
  })
})

describe('self-observation — record & upsert', () => {
  it('record insère une auto-observation (evidence_count = 1)', () => {
    const engine = new SelfObservationEngine({ store })
    const obs = engine.record({ observation: 'Je gère bien les déploiements Vercel', kind: 'strength' })
    expect(obs.evidence_count).toBe(1)
    expect(obs.kind).toBe('strength')
    expect(obs.confidence).toBeGreaterThan(0)
    expect(engine.list()).toHaveLength(1)
  })

  it('ré-enregistrer la MÊME observation = UPSERT idempotent (pas de doublon)', () => {
    const engine = new SelfObservationEngine({ store })
    const a = engine.record({ observation: 'Je me trompe sur les chemins ESM', kind: 'weakness', confidence: 0.5 })
    const b = engine.record({ observation: 'Je me trompe sur les chemins ESM', kind: 'weakness', confidence: 0.9 })
    expect(b.id).toBe(a.id) // même ligne
    expect(b.evidence_count).toBe(2) // renforcée
    expect(engine.list()).toHaveLength(1) // toujours UNE seule ligne
    // Confiance lissée entre 0.5 et 0.9, pas un simple écrasement.
    expect(b.confidence).toBeGreaterThan(0.5)
    expect(b.confidence).toBeLessThan(0.9)
  })

  it('upsert insensible casse/accents/espaces (clé normalisée)', () => {
    const engine = new SelfObservationEngine({ store })
    engine.record({ observation: 'Je préfère les commits signés', kind: 'habit' })
    engine.record({ observation: '  je PRÉFÈRE les commits signés  ', kind: 'habit' })
    const all = engine.list()
    expect(all).toHaveLength(1)
    expect(all[0]!.evidence_count).toBe(2)
    // Le helper de normalisation confirme l'équivalence.
    expect(normalizeObservation('  je PRÉFÈRE les commits signés  ')).toBe(
      normalizeObservation('Je préfère les commits signés'),
    )
  })

  it('observations distinctes par instance_id (clé composite)', () => {
    const engine = new SelfObservationEngine({ store })
    engine.record({ observation: 'Je suis lent', kind: 'weakness', instanceId: 'koda' })
    engine.record({ observation: 'Je suis lent', kind: 'weakness', instanceId: 'luna' })
    expect(engine.list()).toHaveLength(2)
    expect(engine.list({ instanceId: 'koda' })).toHaveLength(1)
  })

  it('observation vide ou kind invalide → throw (jamais avalé)', () => {
    const engine = new SelfObservationEngine({ store })
    expect(() => engine.record({ observation: '', kind: 'strength' })).toThrow()
    expect(() => engine.record({ observation: ' ', kind: 'weakness' })).toThrow()
    // @ts-expect-error kind volontairement invalide pour prouver la garde runtime
    expect(() => engine.record({ observation: 'ok', kind: 'inconnu' })).toThrow()
  })
})

describe('self-observation — list & forget', () => {
  it('list filtre par kind et trie par preuve décroissante', () => {
    const engine = new SelfObservationEngine({ store })
    engine.record({ observation: 'Force A', kind: 'strength' })
    engine.record({ observation: 'Faiblesse B', kind: 'weakness' })
    engine.record({ observation: 'Faiblesse B', kind: 'weakness' }) // evidence ++
    expect(engine.list({ kind: 'strength' })).toHaveLength(1)
    expect(engine.list({ kind: 'weakness' })).toHaveLength(1)
    const all = engine.list()
    expect(all[0]!.observation).toBe('Faiblesse B') // plus de preuves → en tête
  })

  it('forget retire une auto-observation par id', () => {
    const engine = new SelfObservationEngine({ store })
    const obs = engine.record({ observation: 'À oublier', kind: 'habit' })
    expect(engine.forget(obs.id)).toBe(true)
    expect(engine.list()).toHaveLength(0)
    expect(engine.forget(obs.id)).toBe(false) // déjà parti
  })

  it('SELF_OBSERVATION_KINDS = les 4 valeurs du schéma', () => {
    expect([...SELF_OBSERVATION_KINDS].sort()).toEqual(['blindspot', 'habit', 'strength', 'weakness'])
  })
})

describe('self-observation — deriveFromHistory (heuristique, 0 LLM)', () => {
  it('procédure à fort taux d’échec → PROPOSE une weakness', () => {
    const engine = new SelfObservationEngine({ store })
    const { proposed } = engine.deriveFromHistory({
      procedures: [{ name: 'déployer le daemon', success_count: 1, failure_count: 5 }],
    })
    expect(proposed).toHaveLength(1)
    expect(proposed[0]!.kind).toBe('weakness')
    expect(proposed[0]!.observation).toContain('déployer le daemon')
    // La proposition est bien PERSISTÉE (record), pas seulement retournée.
    expect(engine.list({ kind: 'weakness' })).toHaveLength(1)
  })

  it('procédure à fort taux de succès → PROPOSE une strength', () => {
    const engine = new SelfObservationEngine({ store })
    const { proposed } = engine.deriveFromHistory({
      procedures: [{ name: 'publier un article Directus', success_count: 9, failure_count: 1 }],
    })
    expect(proposed).toHaveLength(1)
    expect(proposed[0]!.kind).toBe('strength')
  })

  it('procédure sans assez d’historique → ignorée (anti-bruit)', () => {
    const engine = new SelfObservationEngine({ store })
    const { proposed } = engine.deriveFromHistory({
      procedures: [{ name: 'truc rare', success_count: 0, failure_count: 1 }],
    })
    expect(proposed).toHaveLength(0)
  })

  it('pattern récurrent → PROPOSE une habit', () => {
    const engine = new SelfObservationEngine({ store })
    const { proposed } = engine.deriveFromHistory({
      patterns: [{ description: 'tu commits toujours en fin de session', occurrences: 6 }],
    })
    expect(proposed).toHaveLength(1)
    expect(proposed[0]!.kind).toBe('habit')
  })

  it('re-dériver le même historique ne DUPLIQUE pas (upsert)', () => {
    const engine = new SelfObservationEngine({ store })
    const hist = { procedures: [{ name: 'déployer le daemon', success_count: 1, failure_count: 5 }] }
    engine.deriveFromHistory(hist)
    engine.deriveFromHistory(hist)
    expect(engine.list({ kind: 'weakness' })).toHaveLength(1)
    expect(engine.list({ kind: 'weakness' })[0]!.evidence_count).toBe(2)
  })

  it('RÈGLE D’OR bucket C : aucun fait inséré/modifié/supprimé', () => {
    const engine = new SelfObservationEngine({ store })
    const f1 = fact('Le client Rino fait du BTP')
    const before = textOf(f1)
    const countBefore = activeFactCount()
    engine.record({ observation: 'Je suis fort en transport', kind: 'strength' })
    engine.deriveFromHistory({
      procedures: [{ name: 'devis BDL', success_count: 0, failure_count: 4 }],
    })
    expect(activeFactCount()).toBe(countBefore)
    expect(supersededCount()).toBe(0)
    expect(textOf(f1)).toBe(before)
  })
})

// ===========================================================================
// DIALECTIC
// ===========================================================================

describe('dialectic — heuristiques pures', () => {
  it('hasContrast détecte « mais / cependant / par contre / however »', () => {
    expect(hasContrast('Vercel est rapide mais cher')).toBe(true)
    expect(hasContrast('C’est solide ; cependant fragile au boot')).toBe(true)
    expect(hasContrast('Fast however expensive')).toBe(true)
    expect(hasContrast('Le port est 8080')).toBe(false)
  })

  it('heuristicSynthesis non vide dès qu’il y a un camp', () => {
    const s = heuristicSynthesis('le port ?', { pour: [], contre: [], nuance: [] })
    expect(s).toContain('Aucun souvenir')
  })
})

describe('dialectic — répartition POUR/CONTRE/NUANCE', () => {
  it('« port 8080 » vs « port 9090 » → pour & contre, synthèse non vide', async () => {
    fact('Le port du daemon est 8080')
    fact('Le port du daemon est 9090')
    const res = await dialectic(store, 'quel est le port du daemon')
    // Les deux faits sont remontés et répartis (un camp pour, l'autre contre).
    expect(res.pour.length).toBeGreaterThanOrEqual(1)
    expect(res.contre.length).toBeGreaterThanOrEqual(1)
    expect(res.pour.length + res.contre.length + res.nuance.length).toBe(2)
    expect(res.synthese.trim().length).toBeGreaterThan(0)
    expect(res.synthese).toContain('contre')
  })

  it('négation isolée → CONTRE', async () => {
    fact('On utilise Vercel pour le déploiement')
    fact('On n’utilise plus Vercel pour le déploiement')
    const res = await dialectic(store, 'on utilise Vercel pour le déploiement')
    expect(res.contre.length).toBeGreaterThanOrEqual(1)
    expect(res.contre.some(f => f.fact.includes('plus'))).toBe(true)
  })

  it('marqueur d’opposition → NUANCE', async () => {
    fact('Vercel est pratique mais bloque les commits hello@')
    const res = await dialectic(store, 'Vercel est pratique')
    expect(res.nuance.length).toBe(1)
    expect(res.pour.length).toBe(0)
    expect(res.contre.length).toBe(0)
  })

  it('aucun souvenir pertinent → synthèse explicite, listes vides', async () => {
    fact('Le client Rino fait du BTP')
    const res = await dialectic(store, 'préférences couleur du logo JamBoard')
    expect(res.pour).toHaveLength(0)
    expect(res.contre).toHaveLength(0)
    expect(res.nuance).toHaveLength(0)
    expect(res.synthese).toContain('Aucun souvenir pertinent')
  })
})

describe('dialectic — RÈGLE D’OR & isolation', () => {
  it('NE MODIFIE AUCUN fait (compteurs + contenu avant/après)', async () => {
    const a = fact('Le port du daemon est 8080')
    const b = fact('Le port du daemon est 9090')
    const beforeA = textOf(a)
    const beforeB = textOf(b)
    const countBefore = activeFactCount()
    await dialectic(store, 'quel est le port du daemon')
    expect(activeFactCount()).toBe(countBefore)
    expect(supersededCount()).toBe(0)
    expect(textOf(a)).toBe(beforeA)
    expect(textOf(b)).toBe(beforeB)
  })

  it('respecte les scopes : un fait hors scope autorisé n’apparaît pas', async () => {
    fact('Le port du daemon est 8080', 'clientA')
    fact('Le port du daemon est 9090', 'clientB')
    const res = await dialectic(store, 'quel est le port du daemon', { scopeIds: ['clientA'] })
    const all = [...res.pour, ...res.contre, ...res.nuance]
    expect(all).toHaveLength(1)
    expect(all[0]!.scope_id).toBe('clientA')
    expect(all.some(f => f.fact.includes('9090'))).toBe(false)
  })
})

describe('dialectic — LLM optionnel', () => {
  it('LLM disponible → synthèse fournie par le modèle', async () => {
    fact('Le port du daemon est 8080')
    fact('Le port du daemon est 9090')
    const llm = new FakeLlm('Synthèse modèle : les souvenirs divergent sur le port.')
    const res = await dialectic(store, 'quel est le port du daemon', { llm })
    expect(res.synthese).toBe('Synthèse modèle : les souvenirs divergent sur le port.')
    expect(llm.completeCalls).toBe(1)
  })

  it('LLM indisponible (isAvailable rejette) → repli heuristique, jamais silencieux', async () => {
    fact('Le port du daemon est 8080')
    fact('Le port du daemon est 9090')
    const llm = new FakeLlm('ne devrait pas servir', true, /* throwOnAvailable */ true)
    const res = await dialectic(store, 'quel est le port du daemon', { llm })
    // Pas de complete() appelé ; synthèse heuristique non vide.
    expect(llm.completeCalls).toBe(0)
    expect(res.synthese.trim().length).toBeGreaterThan(0)
    expect(res.synthese).not.toContain('ne devrait pas servir')
  })
})
