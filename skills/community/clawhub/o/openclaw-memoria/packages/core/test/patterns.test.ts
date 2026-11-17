/**
 * Couche PATTERNS (récurrences, couche 22, bucket D « sur validation », spec §12).
 *
 * Garanties PROUVÉES ici (pas juste « ça compile ») :
 *  - detect() regroupe les faits récurrents et PROPOSE 1 pattern (occurrences=5) ;
 *  - sous le seuil (2 faits) → AUCUN pattern proposé ;
 *  - idempotence : re-detect ne duplique pas ;
 *  - dismiss → plus jamais reproposé ; accept → status accepted ;
 *  - onForget retire un membre et DISSOUT le pattern sous le seuil ;
 *  - RÈGLE D'OR : detect() ne SUPERSEDE/ne SUPPRIME aucun fait (compteurs
 *    avant/après identiques) ; la consolidation est explicite et réversible.
 *
 * Tout est sans réseau (aucun LLM), DB en tmpdir.
 */
import { mkdtempSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { afterEach, beforeEach, describe, expect, it } from 'vitest'
import { ContentStore } from '../src/storage/content.js'
import {
  PatternEngine,
  patternMigrations,
  significantTokens,
  jaccardSets,
  confidenceFor,
} from '../src/cognition/patterns.js'

let dir: string
let store: ContentStore

beforeEach(() => {
  dir = mkdtempSync(join(tmpdir(), 'memoria-patterns-'))
  store = new ContentStore(join(dir, 'content.sqlite'))
})

afterEach(() => {
  store.close()
  rmSync(dir, { recursive: true, force: true })
})

/** Insère un fait actif et retourne son id. */
function fact(text: string, opts: { category?: string; topic_id?: string } = {}): string {
  return store.insertFact({
    fact: text,
    category: opts.category ?? 'preference',
    topic_id: opts.topic_id ?? null,
    scope_id: 's1',
  }).id
}

function activeFactCount(): number {
  return (store.db.prepare('SELECT COUNT(*) AS c FROM facts WHERE superseded = 0').get() as { c: number }).c
}
function supersededCount(): number {
  return (store.db.prepare('SELECT COUNT(*) AS c FROM facts WHERE superseded = 1').get() as { c: number }).c
}

describe('patternMigrations (schéma)', () => {
  it('crée la table patterns aux versions réservées 30-39', () => {
    expect(patternMigrations.every(m => m.version >= 30 && m.version <= 39)).toBe(true)
    // La table est appliquée par le constructeur de l'engine (paresseux).
    new PatternEngine({ store })
    const cols = store.db.prepare('PRAGMA table_info(patterns)').all() as Array<{ name: string }>
    const names = cols.map(c => c.name).sort()
    expect(names).toEqual(
      [
        'id', 'label', 'canonical_fact', 'member_fact_ids', 'occurrences', 'confidence',
        'status', 'kind', 'created_at', 'updated_at', 'reviewed_at',
      ].sort(),
    )
  })
})

describe('heuristiques pures', () => {
  it('significantTokens normalise (minuscules, sans diacritiques, mots > 3 car.)', () => {
    const t = significantTokens('Néto PRÉFÈRE les commits signés en français')
    expect(t.has('neto')).toBe(true)
    expect(t.has('prefere')).toBe(true)
    expect(t.has('commits')).toBe(true)
    expect(t.has('signes')).toBe(true)
    expect(t.has('francais')).toBe(true)
    expect(t.has('les')).toBe(false) // stopword/court
  })

  it('jaccardSets borné [0,1], symétrique', () => {
    const a = new Set(['alpha', 'beta', 'gamma'])
    const b = new Set(['beta', 'gamma', 'delta'])
    expect(jaccardSets(a, b)).toBeCloseTo(2 / 4, 5)
    expect(jaccardSets(a, b)).toBe(jaccardSets(b, a))
    expect(jaccardSets(a, new Set())).toBe(0)
  })

  it('confidenceFor croît avec les occurrences, reste bornée [0,1]', () => {
    const c3 = confidenceFor(3, 1)
    const c5 = confidenceFor(5, 1)
    const c10 = confidenceFor(10, 1)
    expect(c5).toBeGreaterThan(c3)
    expect(c10).toBeGreaterThan(c5)
    expect(c10).toBeLessThanOrEqual(1)
    expect(confidenceFor(3, 0)).toBeGreaterThanOrEqual(0)
  })
})

describe('PatternEngine.detect (proposition, bucket D)', () => {
  it('5 faits qui disent la MÊME préférence formulée différemment → 1 pattern occurrences=5', () => {
    fact('Néto préfère les commits signés en français')
    fact('Néto préfère des commits français bien signés')
    fact('Préférence de Néto : commits signés français toujours')
    fact('Néto veut ses commits signés et en français de préférence')
    fact('Pour Néto, préférence claire : commits français signés')

    const engine = new PatternEngine({ store })
    const res = engine.detect({ minOccurrences: 3 })

    expect(res.created).toBe(1)
    expect(res.proposed).toHaveLength(1)
    const p = res.proposed[0]!
    expect(p.occurrences).toBe(5)
    expect(p.member_fact_ids).toHaveLength(5)
    expect(p.status).toBe('proposed')
    expect(p.kind).toBe('preference')
    expect(p.confidence).toBeGreaterThan(0)
    // label = thème commun (mots récurrents) — contient le cœur du sujet.
    expect(p.label.length).toBeGreaterThan(0)
    expect(p.label).toMatch(/commits|francais|neto|signes|preference/)
  })

  it('2 faits similaires seulement → SOUS le seuil → AUCUN pattern', () => {
    fact('Néto préfère les commits signés en français')
    fact('Néto préfère des commits français bien signés')

    const engine = new PatternEngine({ store })
    const res = engine.detect({ minOccurrences: 3 })
    expect(res.created).toBe(0)
    expect(res.proposed).toHaveLength(0)
  })

  it('ne regroupe PAS des faits sans rapport (pas de faux pattern)', () => {
    fact('Néto préfère les commits signés en français')
    fact('Néto préfère des commits français bien signés')
    fact('Néto préfère ses commits signés français toujours')
    // 3 faits hors-sujet, deux à deux dissemblables :
    fact('Le NAS QNAP héberge les sauvegardes vidéo')
    fact('AutoCare cible le marché brésilien mobile')
    fact('Réunion lundi prochain salle bleue matin')

    const engine = new PatternEngine({ store })
    const res = engine.detect({ minOccurrences: 3 })
    expect(res.proposed).toHaveLength(1) // uniquement la préférence récurrente
    expect(res.proposed[0]!.occurrences).toBe(3)
  })

  it('regroupe par topic partagé + même sujet/prédicat même si Jaccard faible', () => {
    const topic = 'topic_deploy'
    store.db
      .prepare('INSERT INTO topics (id, name, sensitivity, importance_score, keywords, created_at) VALUES (?,?,?,?,?,?)')
      .run(topic, 'Déploiement', 'normal', 0, '[]', new Date().toISOString())
    // Même sujet/prédicat « deploiement vercel » répété, formulations courtes.
    fact('Deploiement Vercel branche principale', { category: 'convention', topic_id: topic })
    fact('Deploiement Vercel auteur autorise', { category: 'convention', topic_id: topic })
    fact('Deploiement Vercel squash interdit', { category: 'convention', topic_id: topic })

    const engine = new PatternEngine({ store })
    const res = engine.detect({ minOccurrences: 3 })
    expect(res.proposed).toHaveLength(1)
    expect(res.proposed[0]!.occurrences).toBe(3)
    expect(res.proposed[0]!.kind).toBe('convention')
  })

  it('RÈGLE D’OR : detect() ne superseder/supprime AUCUN fait (compteurs avant/après)', () => {
    fact('Néto préfère les commits signés en français')
    fact('Néto préfère des commits français bien signés')
    fact('Préférence de Néto : commits signés français toujours')
    fact('Néto veut ses commits signés et en français de préférence')
    fact('Pour Néto, préférence claire : commits français signés')
    const activeBefore = activeFactCount()
    const supersededBefore = supersededCount()
    const totalBefore = store.countFacts()

    const engine = new PatternEngine({ store })
    const res = engine.detect({ minOccurrences: 3 })
    expect(res.created).toBe(1)

    // AUCUN fait touché par la détection (bucket D : on PROPOSE, on n'applique pas).
    expect(activeFactCount()).toBe(activeBefore)
    expect(supersededCount()).toBe(supersededBefore)
    expect(supersededCount()).toBe(0)
    expect(store.countFacts()).toBe(totalBefore)
  })
})

describe('PatternEngine.detect (idempotence)', () => {
  it('re-détecter ne DUPLIQUE pas le pattern (mise à jour, pas insert)', () => {
    fact('Néto préfère les commits signés en français')
    fact('Néto préfère des commits français bien signés')
    fact('Préférence de Néto : commits signés français toujours')
    fact('Néto veut ses commits signés et en français de préférence')

    const engine = new PatternEngine({ store })
    const first = engine.detect({ minOccurrences: 3 })
    expect(first.created).toBe(1)
    const idFirst = first.proposed[0]!.id

    const second = engine.detect({ minOccurrences: 3 })
    expect(second.created).toBe(0) // pas de nouveau
    expect(second.updated).toBe(1) // réconcilié
    expect(second.proposed).toHaveLength(1)
    expect(second.proposed[0]!.id).toBe(idFirst) // même pattern
    expect((store.db.prepare('SELECT COUNT(*) AS c FROM patterns').get() as { c: number }).c).toBe(1)
  })

  it('un nouveau fait récurrent fait grossir le MÊME pattern (pas de doublon)', () => {
    fact('Néto préfère les commits signés en français')
    fact('Néto préfère des commits français bien signés')
    fact('Préférence de Néto : commits signés français toujours')

    const engine = new PatternEngine({ store })
    const first = engine.detect({ minOccurrences: 3 })
    expect(first.proposed[0]!.occurrences).toBe(3)
    const id = first.proposed[0]!.id

    fact('Néto veut ses commits signés et en français de préférence')
    fact('Pour Néto, préférence claire : commits français signés')
    const second = engine.detect({ minOccurrences: 3 })

    expect((store.db.prepare('SELECT COUNT(*) AS c FROM patterns').get() as { c: number }).c).toBe(1)
    expect(second.proposed).toHaveLength(1)
    expect(second.proposed[0]!.id).toBe(id)
    expect(second.proposed[0]!.occurrences).toBe(5)
  })
})

describe('PatternEngine.dismiss / accept', () => {
  it('dismiss → plus jamais reproposé par detect()', () => {
    fact('Néto préfère les commits signés en français')
    fact('Néto préfère des commits français bien signés')
    fact('Préférence de Néto : commits signés français toujours')

    const engine = new PatternEngine({ store })
    const first = engine.detect({ minOccurrences: 3 })
    const id = first.proposed[0]!.id

    const dismissed = engine.dismiss(id)
    expect(dismissed!.status).toBe('dismissed')
    expect(dismissed!.reviewed_at).not.toBeNull()
    expect(engine.listProposed()).toHaveLength(0)

    // Re-détection : le même groupe ne réapparaît PAS en proposition.
    const again = engine.detect({ minOccurrences: 3 })
    expect(again.created).toBe(0)
    expect(again.skippedDismissed).toBe(1)
    expect(engine.listProposed()).toHaveLength(0)
    // Et toujours un seul pattern en base (dismissed), pas de doublon.
    expect((store.db.prepare('SELECT COUNT(*) AS c FROM patterns').get() as { c: number }).c).toBe(1)
  })

  it('accept → status accepted + reviewed_at, NE consolide RIEN', () => {
    fact('Néto préfère les commits signés en français')
    fact('Néto préfère des commits français bien signés')
    fact('Préférence de Néto : commits signés français toujours')

    const engine = new PatternEngine({ store })
    const id = engine.detect({ minOccurrences: 3 }).proposed[0]!.id

    const accepted = engine.accept(id)
    expect(accepted!.status).toBe('accepted')
    expect(accepted!.reviewed_at).not.toBeNull()
    // accept seul = aucun fait superseded (la consolidation est une autre action).
    expect(supersededCount()).toBe(0)
    expect(engine.listProposed()).toHaveLength(0) // sorti des propositions
  })

  it('accept/dismiss sur un id inexistant → null (no-op annoncé, pas de throw)', () => {
    const engine = new PatternEngine({ store })
    expect(engine.accept('inexistant')).toBeNull()
    expect(engine.dismiss('inexistant')).toBeNull()
  })
})

describe('PatternEngine.consolidate (explicite, réversible)', () => {
  it('consolide UNIQUEMENT un pattern accepté → superseded les membres actifs', () => {
    const ids = [
      fact('Néto préfère les commits signés en français'),
      fact('Néto préfère des commits français bien signés'),
      fact('Préférence de Néto : commits signés français toujours'),
    ]
    const engine = new PatternEngine({ store })
    const pid = engine.detect({ minOccurrences: 3 }).proposed[0]!.id

    // Sans accept : consolidate est un no-op (applied=false, rien superseded).
    const noop = engine.consolidate(pid)
    expect(noop.applied).toBe(false)
    expect(noop.superseded).toHaveLength(0)
    expect(supersededCount()).toBe(0)

    // Après accept : la consolidation marque les membres superseded.
    engine.accept(pid)
    const done = engine.consolidate(pid)
    expect(done.applied).toBe(true)
    expect(done.superseded.sort()).toEqual([...ids].sort())
    expect(supersededCount()).toBe(3)
  })
})

describe('PatternEngine.onForget', () => {
  it('retire un membre et RECOMPTE quand le pattern reste au-dessus du seuil', () => {
    const ids = [
      fact('Néto préfère les commits signés en français'),
      fact('Néto préfère des commits français bien signés'),
      fact('Préférence de Néto : commits signés français toujours'),
      fact('Néto veut ses commits signés et en français de préférence'),
    ]
    const engine = new PatternEngine({ store })
    const pid = engine.detect({ minOccurrences: 3 }).proposed[0]!.id
    expect(engine.getPattern(pid)!.occurrences).toBe(4)

    const r = engine.onForget([ids[0]!], { minOccurrences: 3 })
    expect(r.updated).toBe(1)
    expect(r.removed).toBe(0)
    const after = engine.getPattern(pid)!
    expect(after.occurrences).toBe(3)
    expect(after.member_fact_ids).not.toContain(ids[0]!)
    expect(after.member_fact_ids).toHaveLength(3)
  })

  it('DISSOUT le pattern quand il retombe SOUS le seuil', () => {
    const ids = [
      fact('Néto préfère les commits signés en français'),
      fact('Néto préfère des commits français bien signés'),
      fact('Préférence de Néto : commits signés français toujours'),
    ]
    const engine = new PatternEngine({ store })
    const pid = engine.detect({ minOccurrences: 3 }).proposed[0]!.id

    // On oublie 1 membre → 2 restants < seuil 3 → pattern supprimé.
    const r = engine.onForget([ids[0]!], { minOccurrences: 3 })
    expect(r.removed).toBe(1)
    expect(engine.getPattern(pid)).toBeNull()
    expect((store.db.prepare('SELECT COUNT(*) AS c FROM patterns').get() as { c: number }).c).toBe(0)
  })

  it('no-op si aucun fait concerné', () => {
    fact('Néto préfère les commits signés en français')
    fact('Néto préfère des commits français bien signés')
    fact('Préférence de Néto : commits signés français toujours')
    const engine = new PatternEngine({ store })
    engine.detect({ minOccurrences: 3 })
    const r = engine.onForget(['fait-inconnu'], { minOccurrences: 3 })
    expect(r).toEqual({ updated: 0, removed: 0 })
  })
})
