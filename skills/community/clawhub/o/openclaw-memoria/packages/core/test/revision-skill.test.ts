/**
 * Couches REVISION (18+24) + AUTO-SKILL (23), bucket D « sur validation » (spec §12).
 *
 * Garanties PROUVÉES ici (pas juste « ça compile ») :
 *  REVISION
 *   - propose() détecte un fait CONTREDIT par un plus récent → 1 proposal
 *     'contradicted' (le plus ancien proposé, le plus récent = replacement) ;
 *   - propose() détecte un DOUBLON quasi-exact → 1 proposal 'duplicate' ;
 *   - RÈGLE D'OR : propose() ne modifie AUCUN fait (compteurs avant/après) ;
 *   - accept() supersède l'ANCIEN (superseded=1, superseded_by=remplaçant RÉEL) et
 *     PAS le nouveau ; c'est la SEULE méthode qui touche un fait ;
 *   - dismiss() ne modifie RIEN et empêche la re-proposition ;
 *   - idempotence : re-propose() ne re-propose pas un fait déjà proposé/dismissed.
 *  AUTO-SKILL
 *   - propose() depuis un pattern ACCEPTÉ → proposition {label, steps, source} ;
 *   - propose() ne crée RIEN en base (0 procédure tant qu'on n'a pas accept) ;
 *   - accept() crée une procédure RETROUVABLE par matchProcedures (FTS câblée).
 *
 * Tout est sans réseau (aucun LLM), DB en tmpdir.
 */
import { mkdtempSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { afterEach, beforeEach, describe, expect, it } from 'vitest'
import { ContentStore } from '../src/storage/content.js'
import { RevisionEngine, revisionMigrations } from '../src/cognition/revision.js'
import { AutoSkillEngine } from '../src/cognition/auto-skill.js'
import { PatternEngine } from '../src/cognition/patterns.js'
import { ProceduralEngine } from '../src/cognition/procedural.js'

let dir: string
let store: ContentStore

beforeEach(() => {
  dir = mkdtempSync(join(tmpdir(), 'memoria-revskill-'))
  store = new ContentStore(join(dir, 'content.sqlite'))
})

afterEach(() => {
  store.close()
  rmSync(dir, { recursive: true, force: true })
})

/**
 * Insère un fait actif avec un `created_at` EXPLICITE (ordre déterministe) et
 * retourne son id. On force created_at après l'insert : insertFact ne l'expose pas,
 * et deux inserts dans la même ms casseraient l'ordre récent→ancien.
 */
function factAt(text: string, createdAt: string, opts: { scope?: string; category?: string } = {}): string {
  const f = store.insertFact({
    fact: text,
    scope_id: opts.scope ?? 's1',
    category: opts.category ?? 'savoir',
  })
  store.db.prepare('UPDATE facts SET created_at = ? WHERE id = ?').run(createdAt, f.id)
  return f.id
}

function activeFactCount(): number {
  return (store.db.prepare('SELECT COUNT(*) AS c FROM facts WHERE superseded = 0').get() as { c: number }).c
}
function supersededCount(): number {
  return (store.db.prepare('SELECT COUNT(*) AS c FROM facts WHERE superseded = 1').get() as { c: number }).c
}

describe('revisionMigrations (schéma)', () => {
  it('crée la table revision_proposals aux versions réservées 90-99', () => {
    expect(revisionMigrations.every(m => m.version >= 90 && m.version <= 99)).toBe(true)
    new RevisionEngine({ store }) // applique le schéma (paresseux)
    const cols = (store.db.prepare('PRAGMA table_info(revision_proposals)').all() as Array<{ name: string }>).map(
      c => c.name,
    )
    expect(cols.sort()).toEqual(
      ['id', 'fact_id', 'kind', 'reason', 'replacement_fact_id', 'status', 'created_at'].sort(),
    )
  })
})

describe('RevisionEngine.propose (contradiction, bucket D)', () => {
  it('détecte un fait CONTREDIT par un plus récent → 1 proposal "contradicted"', async () => {
    const oldId = factAt('Le port du serveur de production est 8080', '2026-01-01T00:00:00.000Z')
    const newId = factAt('Le port du serveur de production est 9090', '2026-02-01T00:00:00.000Z')

    const engine = new RevisionEngine({ store })
    const res = await engine.propose({ limit: 50 })

    expect(res.created).toBe(1)
    const contradicted = res.proposals.filter(p => p.kind === 'contradicted')
    expect(contradicted).toHaveLength(1)
    const p = contradicted[0]!
    // Le plus ANCIEN est proposé ; le plus RÉCENT en est le remplaçant.
    expect(p.fact_id).toBe(oldId)
    expect(p.replacement_fact_id).toBe(newId)
    expect(p.status).toBe('proposed')
    expect(p.reason.length).toBeGreaterThan(0)
  })

  it('RÈGLE D’OR : propose() ne supersède/supprime AUCUN fait (compteurs avant/après)', async () => {
    factAt('Le port du serveur de production est 8080', '2026-01-01T00:00:00.000Z')
    factAt('Le port du serveur de production est 9090', '2026-02-01T00:00:00.000Z')
    const activeBefore = activeFactCount()
    const supersededBefore = supersededCount()
    const totalBefore = store.countFacts()

    const engine = new RevisionEngine({ store })
    const res = await engine.propose({ limit: 50 })
    expect(res.created).toBeGreaterThanOrEqual(1)

    // AUCUN fait touché par la proposition (bucket D : on PROPOSE, on n'applique pas).
    expect(activeFactCount()).toBe(activeBefore)
    expect(supersededCount()).toBe(supersededBefore)
    expect(supersededCount()).toBe(0)
    expect(store.countFacts()).toBe(totalBefore)
  })

  it('détecte un DOUBLON quasi-exact → 1 proposal "duplicate" (ancien proposé, récent = remplaçant)', async () => {
    const oldId = factAt('Le NAS QNAP héberge les sauvegardes vidéo', '2026-01-01T00:00:00.000Z', { scope: 'sd' })
    const newId = factAt('Le NAS QNAP héberge les sauvegardes vidéo', '2026-02-01T00:00:00.000Z', { scope: 'sd' })

    const engine = new RevisionEngine({ store })
    const res = await engine.propose({ limit: 50 })

    const dup = res.proposals.filter(p => p.kind === 'duplicate')
    expect(dup).toHaveLength(1)
    expect(dup[0]!.fact_id).toBe(oldId)
    expect(dup[0]!.replacement_fact_id).toBe(newId)
  })
})

describe('RevisionEngine.accept (application explicite — SEULE à modifier un fait)', () => {
  it('supersède l’ANCIEN (superseded=1, superseded_by=remplaçant réel) et PAS le nouveau', async () => {
    const oldId = factAt('Le port du serveur de production est 8080', '2026-01-01T00:00:00.000Z')
    const newId = factAt('Le port du serveur de production est 9090', '2026-02-01T00:00:00.000Z')

    const engine = new RevisionEngine({ store })
    const proposalId = (await engine.propose({ limit: 50 })).proposals[0]!.id

    const acc = engine.accept(proposalId)
    expect(acc.applied).toBe(true)
    expect(acc.supersededFactId).toBe(oldId)

    const oldFact = store.getFact(oldId)!
    const newFact = store.getFact(newId)!
    // L'ancien est superseded, chaîné vers un fact.id RÉEL (pas une chaîne fabriquée).
    expect(oldFact.superseded).toBe(true)
    expect(oldFact.superseded_by).toBe(newId)
    expect(store.getFact(oldFact.superseded_by!)).not.toBeNull()
    // Le remplaçant (le plus récent) n'est JAMAIS touché.
    expect(newFact.superseded).toBe(false)
    expect(newFact.superseded_by).toBeNull()

    // La proposition passe en 'accepted', sort des propositions.
    expect(engine.getProposal(proposalId)!.status).toBe('accepted')
    expect(engine.listProposals()).toHaveLength(0)
  })

  it('accept sur un id inexistant / déjà traité → no-op annoncé (applied=false)', async () => {
    factAt('Le port du serveur de production est 8080', '2026-01-01T00:00:00.000Z')
    factAt('Le port du serveur de production est 9090', '2026-02-01T00:00:00.000Z')
    const engine = new RevisionEngine({ store })
    const id = (await engine.propose({ limit: 50 })).proposals[0]!.id

    expect(engine.accept('inexistant').applied).toBe(false)
    expect(engine.accept(id).applied).toBe(true)
    // Deuxième accept du même → no-op (n'est plus 'proposed').
    const second = engine.accept(id)
    expect(second.applied).toBe(false)
    expect(second.supersededFactId).toBeNull()
  })
})

describe('RevisionEngine.dismiss (ne modifie rien)', () => {
  it('dismiss ne touche AUCUN fait et empêche la re-proposition', async () => {
    const oldId = factAt('Le port du serveur de production est 8080', '2026-01-01T00:00:00.000Z')
    factAt('Le port du serveur de production est 9090', '2026-02-01T00:00:00.000Z')

    const engine = new RevisionEngine({ store })
    const id = (await engine.propose({ limit: 50 })).proposals[0]!.id

    const supersededBefore = supersededCount()
    const dismissed = engine.dismiss(id)
    expect(dismissed).toBe(true)
    // Aucun fait touché.
    expect(supersededCount()).toBe(supersededBefore)
    expect(store.getFact(oldId)!.superseded).toBe(false)
    expect(engine.getProposal(id)!.status).toBe('dismissed')
    expect(engine.listProposals()).toHaveLength(0)

    // Re-propose : le fait écarté n'est PAS re-proposé (respect de la décision).
    const again = await engine.propose({ limit: 50 })
    expect(again.created).toBe(0)
    expect(again.skippedExisting).toBeGreaterThanOrEqual(1)
    expect(engine.listProposals()).toHaveLength(0)

    // dismiss d'un id inexistant / déjà traité → false (no-op).
    expect(engine.dismiss('inexistant')).toBe(false)
    expect(engine.dismiss(id)).toBe(false)
  })
})

describe('RevisionEngine.propose (idempotence)', () => {
  it('re-propose ne re-propose pas un fait DÉJÀ proposé', async () => {
    factAt('Le port du serveur de production est 8080', '2026-01-01T00:00:00.000Z')
    factAt('Le port du serveur de production est 9090', '2026-02-01T00:00:00.000Z')

    const engine = new RevisionEngine({ store })
    const first = await engine.propose({ limit: 50 })
    expect(first.created).toBe(1)
    const idFirst = first.proposals[0]!.id

    // Deuxième passe SANS rien accepter : la même contradiction ne re-crée rien.
    const second = await engine.propose({ limit: 50 })
    expect(second.created).toBe(0)
    expect(second.skippedExisting).toBeGreaterThanOrEqual(1)
    // Toujours une seule proposition en base, le même id.
    expect(second.proposals).toHaveLength(1)
    expect(second.proposals[0]!.id).toBe(idFirst)
    expect(
      (store.db.prepare('SELECT COUNT(*) AS c FROM revision_proposals').get() as { c: number }).c,
    ).toBe(1)
  })
})

describe('AutoSkillEngine.propose / accept (bucket D)', () => {
  /** Crée 3 faits récurrents, détecte + accepte le pattern, retourne son id. */
  function seedAcceptedPattern(): string {
    factAt('Néto consolide en Hello-Primo avant de pousser', '2026-03-01T00:00:00.000Z', {
      scope: 's2',
      category: 'convention',
    })
    factAt('Néto consolide toujours en Hello-Primo avant de pousser', '2026-03-02T00:00:00.000Z', {
      scope: 's2',
      category: 'convention',
    })
    factAt('Pour Néto, consolide en Hello-Primo avant de pousser les commits', '2026-03-03T00:00:00.000Z', {
      scope: 's2',
      category: 'convention',
    })
    const pe = new PatternEngine({ store })
    const det = pe.detect({ minOccurrences: 3 })
    expect(det.proposed).toHaveLength(1)
    const pid = det.proposed[0]!.id
    pe.accept(pid)
    return pid
  }

  it('propose() depuis un PATTERN ACCEPTÉ → 1 proposition {label, steps, source}', () => {
    seedAcceptedPattern()
    const ae = new AutoSkillEngine({ store })
    const props = ae.propose({ defaultScopeId: 's2' })

    const fromPattern = props.filter(p => p.source === 'pattern')
    expect(fromPattern).toHaveLength(1)
    const sk = fromPattern[0]!
    expect(sk.label.length).toBeGreaterThan(0)
    expect(sk.steps.length).toBeGreaterThanOrEqual(1)
    expect(sk.scope_id).toBe('s2')
  })

  it('propose() ne crée RIEN en base (0 procédure tant qu’on n’a pas accept)', () => {
    seedAcceptedPattern()
    const proceduresBefore = (store.db.prepare('SELECT COUNT(*) AS c FROM procedures').get() as { c: number }).c
    const ae = new AutoSkillEngine({ store })
    ae.propose({ defaultScopeId: 's2' })
    const proceduresAfter = (store.db.prepare('SELECT COUNT(*) AS c FROM procedures').get() as { c: number }).c
    expect(proceduresAfter).toBe(proceduresBefore)
  })

  it('accept() crée une procédure RETROUVABLE par matchProcedures', () => {
    seedAcceptedPattern()
    const ae = new AutoSkillEngine({ store })
    const props = ae.propose({ defaultScopeId: 's2' })
    const proposal = props.find(p => p.source === 'pattern')!

    const before = (store.db.prepare('SELECT COUNT(*) AS c FROM procedures').get() as { c: number }).c
    const acc = ae.accept(proposal)
    expect(acc.applied).toBe(true)
    expect(acc.procedure).not.toBeNull()
    const after = (store.db.prepare('SELECT COUNT(*) AS c FROM procedures').get() as { c: number }).c
    expect(after).toBe(before + 1)

    // La skill est immédiatement retrouvable (triggers FTS câblés à l'INSERT).
    const proc = new ProceduralEngine({ store })
    const matches = proc.matchProcedures(proposal.label, { scopeIds: ['s2'] })
    expect(matches.length).toBeGreaterThanOrEqual(1)
    expect(matches.some(m => m.procedure.id === acc.procedure!.id)).toBe(true)
    // Étapes consolidées préservées.
    expect(acc.procedure!.steps.length).toBeGreaterThanOrEqual(1)
  })

  it('accept() d’une proposition vide → no-op annoncé (aucune procédure dégénérée)', () => {
    const ae = new AutoSkillEngine({ store })
    const before = (store.db.prepare('SELECT COUNT(*) AS c FROM procedures').get() as { c: number }).c
    const acc = ae.accept({ label: '', steps: [], source: 'pattern', source_id: 'x', scope_id: 's2' })
    expect(acc.applied).toBe(false)
    expect(acc.procedure).toBeNull()
    const after = (store.db.prepare('SELECT COUNT(*) AS c FROM procedures').get() as { c: number }).c
    expect(after).toBe(before)
  })

  it('propose() ne re-propose pas une skill déjà matérialisée (idempotence pratique)', () => {
    seedAcceptedPattern()
    const ae = new AutoSkillEngine({ store })
    const proposal = ae.propose({ defaultScopeId: 's2' }).find(p => p.source === 'pattern')!
    ae.accept(proposal)
    // Une 2e proposition ne re-propose pas la skill homonyme déjà créée.
    const again = ae.propose({ defaultScopeId: 's2' })
    expect(again.some(p => p.label.toLowerCase() === proposal.label.toLowerCase())).toBe(false)
  })
})
