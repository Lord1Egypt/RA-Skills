/**
 * Couches FEEDBACK (7) + EXPERTISE (8) — bucket A « Actif », spec §12.
 *
 * Garanties PROUVÉES ici (pas juste « ça compile ») :
 *  - reinforce(used=true) MONTE relevance_weight + usefulness + used_count, et
 *    crédite l'expertise du domaine (catégorie) ;
 *  - reinforce(used=false) BAISSE relevance_weight, JAMAIS sous le plancher 0.3 ;
 *  - le CAP 2.0 est respecté même après de nombreux signaux positifs ;
 *  - decayUnused n'affecte QUE les vieux faits non utilisés (récents et utilisés
 *    intacts), et ne descend jamais sous le plancher ;
 *  - l'expertise monte avec les signaux et topDomains trie par niveau ;
 *  - RÈGLE D'OR : le CONTENU des faits n'est JAMAIS touché, aucun fait supprimé
 *    ni superseded.
 *
 * Tout est sans réseau (aucun LLM), DB en tmpdir.
 */
import { mkdtempSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { afterEach, beforeEach, describe, expect, it } from 'vitest'
import { ContentStore } from '../src/storage/content.js'
import {
  FeedbackEngine,
  feedbackMigrations,
  ensureFeedbackSchema,
  RELEVANCE_FLOOR,
  RELEVANCE_CAP,
} from '../src/cognition/feedback.js'

let dir: string
let store: ContentStore
let engine: FeedbackEngine

beforeEach(() => {
  dir = mkdtempSync(join(tmpdir(), 'memoria-feedback-'))
  store = new ContentStore(join(dir, 'content.sqlite'))
  engine = new FeedbackEngine({ store })
})

afterEach(() => {
  store.close()
  rmSync(dir, { recursive: true, force: true })
})

/** Insère un fait actif et retourne son id. */
function fact(text: string, opts: { category?: string } = {}): string {
  return store.insertFact({ fact: text, category: opts.category ?? 'general', scope_id: 's1' }).id
}

function weightOf(id: string): number {
  return (store.db.prepare('SELECT relevance_weight FROM facts WHERE id = ?').get(id) as { relevance_weight: number }).relevance_weight
}
function usefulnessOf(id: string): number {
  return (store.db.prepare('SELECT usefulness FROM facts WHERE id = ?').get(id) as { usefulness: number }).usefulness
}
function usedCountOf(id: string): number {
  return (store.db.prepare('SELECT used_count FROM facts WHERE id = ?').get(id) as { used_count: number }).used_count
}
function textOf(id: string): string {
  return (store.db.prepare('SELECT fact FROM facts WHERE id = ?').get(id) as { fact: string }).fact
}
function totalFacts(): number {
  return (store.db.prepare('SELECT COUNT(*) AS c FROM facts').get() as { c: number }).c
}
function supersededCount(): number {
  return (store.db.prepare('SELECT COUNT(*) AS c FROM facts WHERE superseded = 1').get() as { c: number }).c
}

/** Force la « dernière activité » d'un fait dans le passé (test decay). */
function backdate(id: string, days: number): void {
  const ts = new Date(Date.now() - days * 86_400_000).toISOString()
  store.db.prepare('UPDATE facts SET created_at = ?, last_accessed_at = NULL WHERE id = ?').run(ts, id)
}

describe('feedbackMigrations (schéma)', () => {
  it('réserve les versions 50-59 et crée la table expertise', () => {
    expect(feedbackMigrations.every(m => m.version >= 50 && m.version <= 59)).toBe(true)
    const cols = store.db.prepare('PRAGMA table_info(expertise)').all() as Array<{ name: string }>
    const names = cols.map(c => c.name).sort()
    expect(names).toEqual(['id', 'domain', 'level', 'evidence_count', 'updated_at'].sort())
  })

  it('ensureFeedbackSchema est idempotent (re-run sans effet)', () => {
    const second = ensureFeedbackSchema(store.db)
    expect(second).toBe(0)
  })

  it('domain est UNIQUE', () => {
    // Deux signaux sur le même domaine ne créent qu'UNE ligne.
    engine.updateExpertise('vercel', 0.5)
    engine.updateExpertise('vercel', 0.5)
    const c = (store.db.prepare("SELECT COUNT(*) AS c FROM expertise WHERE domain = 'vercel'").get() as { c: number }).c
    expect(c).toBe(1)
  })
})

describe('reinforce(used=true) — signal positif', () => {
  it('monte relevance_weight, usefulness et used_count', () => {
    const id = fact('Néto préfère Vercel pour le déploiement')
    expect(weightOf(id)).toBe(1.0) // défaut tronc
    expect(usefulnessOf(id)).toBe(0)
    expect(usedCountOf(id)).toBe(0)

    const res = engine.reinforce([id], { used: true })
    expect(res.updated).toEqual([id])

    expect(weightOf(id)).toBeGreaterThan(1.0)
    expect(usefulnessOf(id)).toBeGreaterThan(0)
    expect(usedCountOf(id)).toBe(1)
  })

  it('plusieurs usages cumulent used_count et usefulness', () => {
    const id = fact('fait utile répété')
    engine.reinforce([id], { used: true })
    engine.reinforce([id], { used: true })
    engine.reinforce([id], { used: true })
    expect(usedCountOf(id)).toBe(3)
    expect(usefulnessOf(id)).toBeGreaterThanOrEqual(3)
  })

  it('respecte le CAP 2.0 même après de nombreux signaux positifs', () => {
    const id = fact('fait massivement utile')
    for (let i = 0; i < 50; i++) engine.reinforce([id], { used: true })
    expect(weightOf(id)).toBeLessThanOrEqual(RELEVANCE_CAP)
    expect(weightOf(id)).toBe(RELEVANCE_CAP) // saturé au cap
  })

  it('ignore les ids inconnus et les faits superseded', () => {
    const id = fact('actif')
    store.db.prepare("UPDATE facts SET superseded = 1 WHERE id = ?").run(id)
    const res = engine.reinforce([id, 'inexistant'], { used: true })
    expect(res.updated).toEqual([]) // superseded exclu, inconnu exclu
    expect(usedCountOf(id)).toBe(0)
  })
})

describe('reinforce(used=false) — remonté mais inutile', () => {
  it('baisse relevance_weight', () => {
    const id = fact('remonté à tort')
    const before = weightOf(id)
    engine.reinforce([id], { used: false })
    expect(weightOf(id)).toBeLessThan(before)
  })

  it("ne descend JAMAIS sous le plancher 0.3, même après beaucoup de signaux", () => {
    const id = fact('jamais utile')
    for (let i = 0; i < 100; i++) engine.reinforce([id], { used: false })
    expect(weightOf(id)).toBeGreaterThanOrEqual(RELEVANCE_FLOOR)
    expect(weightOf(id)).toBeCloseTo(RELEVANCE_FLOOR, 6)
  })

  it("n'incrémente pas used_count (ce n'était pas un usage réel)", () => {
    const id = fact('remonté inutilement')
    engine.reinforce([id], { used: false })
    expect(usedCountOf(id)).toBe(0)
  })
})

describe('decayUnused — vieux faits non utilisés', () => {
  it('atténue un vieux fait jamais utilisé', () => {
    const old = fact('vieux souvenir oublié')
    backdate(old, 90)
    const before = weightOf(old)
    const n = engine.decayUnused({ olderThanDays: 30, factor: 0.9 })
    expect(n).toBe(1)
    expect(weightOf(old)).toBeLessThan(before)
  })

  it("n'affecte PAS un fait récent", () => {
    const recent = fact('souvenir récent') // created_at = maintenant
    const before = weightOf(recent)
    engine.decayUnused({ olderThanDays: 30, factor: 0.9 })
    expect(weightOf(recent)).toBe(before)
  })

  it("n'affecte PAS un vieux fait DÉJÀ utilisé (used_count > 0)", () => {
    const used = fact('vieux mais utile')
    engine.reinforce([used], { used: true }) // used_count = 1, last_accessed_at = maintenant
    // On vieillit created_at mais reinforce a posé last_accessed_at récent +
    // used_count>0 → exclu du decay quoi qu'il arrive.
    store.db.prepare('UPDATE facts SET created_at = ? WHERE id = ?')
      .run(new Date(Date.now() - 90 * 86_400_000).toISOString(), used)
    const before = weightOf(used)
    engine.decayUnused({ olderThanDays: 30, factor: 0.9 })
    expect(weightOf(used)).toBe(before)
  })

  it('ne descend jamais sous le plancher 0.3', () => {
    const old = fact('très vieux')
    backdate(old, 365)
    for (let i = 0; i < 100; i++) engine.decayUnused({ olderThanDays: 30, factor: 0.5 })
    expect(weightOf(old)).toBeGreaterThanOrEqual(RELEVANCE_FLOOR)
  })
})

describe('EXPERTISE', () => {
  it('monte avec les signaux et sature sous le plafond 1.0', () => {
    expect(engine.getExpertise('deploiement')).toBeNull()
    const l1 = engine.updateExpertise('deploiement', 0.3)
    const l2 = engine.updateExpertise('deploiement', 0.3)
    expect(l2).toBeGreaterThan(l1)
    for (let i = 0; i < 50; i++) engine.updateExpertise('deploiement', 0.3)
    expect(engine.getExpertise('deploiement')!.level).toBeLessThanOrEqual(1.0)
  })

  it('evidence_count compte chaque signal', () => {
    engine.updateExpertise('seo', 0.2)
    engine.updateExpertise('seo', 0.2)
    engine.updateExpertise('seo', 0.2)
    expect(engine.getExpertise('seo')!.evidence_count).toBe(3)
  })

  it('reinforce(used=true) crédite l\'expertise du domaine (catégorie du fait)', () => {
    const id = fact('config Vercel projet', { category: 'devops' })
    const res = engine.reinforce([id], { used: true })
    expect(res.domains).toContain('devops')
    expect(engine.getExpertise('devops')!.level).toBeGreaterThan(0)
  })

  it('reinforce(used=false) NE crédite PAS l\'expertise', () => {
    const id = fact('fait', { category: 'devops' })
    engine.reinforce([id], { used: false })
    expect(engine.getExpertise('devops')).toBeNull()
  })

  it('topDomains trie par niveau décroissant', () => {
    engine.updateExpertise('faible', 0.1)
    engine.updateExpertise('moyen', 0.4)
    engine.updateExpertise('fort', 0.8)
    const top = engine.topDomains(10)
    expect(top.map(d => d.domain)).toEqual(['fort', 'moyen', 'faible'])
    expect(top[0]!.level).toBeGreaterThan(top[1]!.level)
  })

  it('topDomains respecte la limite', () => {
    for (let i = 0; i < 5; i++) engine.updateExpertise(`d${i}`, 0.5)
    expect(engine.topDomains(3)).toHaveLength(3)
  })

  it('updateExpertise ignore un domaine vide', () => {
    engine.updateExpertise('   ', 0.5)
    expect((store.db.prepare('SELECT COUNT(*) AS c FROM expertise').get() as { c: number }).c).toBe(0)
  })
})

describe("RÈGLE D'OR — ne touche jamais le contenu, aucune suppression", () => {
  it('le texte des faits est inchangé après reinforce/decay', () => {
    const id = fact('Texte original à préserver')
    engine.reinforce([id], { used: true })
    engine.reinforce([id], { used: false })
    engine.decayUnused({ olderThanDays: 0, factor: 0.5 })
    expect(textOf(id)).toBe('Texte original à préserver')
  })

  it('aucun fait supprimé ni superseded', () => {
    const ids = [fact('a'), fact('b'), fact('c')]
    for (const id of ids) backdate(id, 90)
    engine.reinforce(ids, { used: true })
    engine.reinforce(ids, { used: false })
    engine.decayUnused({ olderThanDays: 30, factor: 0.5 })
    expect(totalFacts()).toBe(3)
    expect(supersededCount()).toBe(0)
  })
})

describe('stats()', () => {
  it('reflète reinforced / attenuated / neverUsed / expertise', () => {
    const boosted = fact('utile')
    const damped = fact('inutile')
    fact('jamais touché')
    engine.reinforce([boosted], { used: true })
    engine.reinforce([damped], { used: false })

    const s = engine.stats()
    expect(s.reinforced).toBe(1)
    expect(s.attenuated).toBe(1)
    expect(s.neverUsed).toBe(2) // damped jamais "used", + jamais touché
    expect(s.totalUses).toBe(1)
    expect(s.domains).toBeGreaterThanOrEqual(1)
  })
})
