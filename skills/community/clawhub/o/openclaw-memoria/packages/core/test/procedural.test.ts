/**
 * Couche PROCEDURAL (« comment faire les choses », couche 6, bucket A, spec §12).
 *
 * Garanties PROUVÉES ici (pas juste « ça compile ») :
 *  - store + match : la procédure la PLUS PERTINENTE remonte ; à pertinence
 *    proche, celle au PLUS HAUT TAUX DE SUCCÈS passe en tête de sa requête ;
 *  - recordExecution success/failure : compteurs + quality_score mis à jour ;
 *  - failure_reasons en FENÊTRE GLISSANTE de 10 (11e échec → 10 entrées) ;
 *  - RÉPARATION procedural.ts:1053 : la colonne EXISTE et est écrite, AUCUNE
 *    exception avalée (on espionne console pour le prouver) ;
 *  - RÉPARATION procedural.ts:296 : la FTS reste ALIGNÉE après update (pas de
 *    fantôme, pas de mauvais id retourné, même après UPSERT qui change le nom).
 *
 * Tout est sans réseau (aucun LLM), DB en tmpdir.
 */
import { mkdtempSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { ContentStore } from '../src/storage/content.js'
import {
  ProceduralEngine,
  proceduralMigrations,
  successRateOf,
  recencyScore,
  formatFailureReason,
  FAILURE_REASONS_WINDOW,
} from '../src/cognition/procedural.js'

let dir: string
let store: ContentStore
let engine: ProceduralEngine

beforeEach(() => {
  dir = mkdtempSync(join(tmpdir(), 'memoria-procedural-'))
  store = new ContentStore(join(dir, 'content.sqlite'))
  engine = new ProceduralEngine({ store })
})

afterEach(() => {
  store.close()
  rmSync(dir, { recursive: true, force: true })
})

function countFtsRows(): number {
  return (store.db.prepare('SELECT COUNT(*) AS c FROM procedures_fts').get() as { c: number }).c
}

describe('proceduralMigrations (schéma)', () => {
  it('réserve les versions 40-49 et ajoute quality_score + last_used_at', () => {
    expect(proceduralMigrations.every(m => m.version >= 40 && m.version <= 49)).toBe(true)
    const cols = (store.db.prepare('PRAGMA table_info(procedures)').all() as Array<{ name: string }>).map(c => c.name)
    expect(cols).toContain('quality_score')
    expect(cols).toContain('last_used_at')
    // failure_reasons vient déjà du tronc (content-schema, bug procedural.ts:1053 gravé corrigé).
    expect(cols).toContain('failure_reasons')
  })

  it('le constructeur est idempotent (ré-instancier ne casse rien)', () => {
    expect(() => new ProceduralEngine({ store })).not.toThrow()
    expect(() => new ProceduralEngine({ store })).not.toThrow()
  })
})

describe('helpers purs', () => {
  it('successRateOf : lissé Laplace, neutre à vide, monotone', () => {
    expect(successRateOf(0, 0)).toBeCloseTo(0.5, 5)
    expect(successRateOf(5, 0)).toBeGreaterThan(successRateOf(1, 0))
    expect(successRateOf(0, 5)).toBeLessThan(0.5)
    expect(successRateOf(5, 0)).toBeLessThan(1) // jamais 1.0 (lissage)
    expect(successRateOf(9, 1)).toBeGreaterThan(successRateOf(4, 1))
  })

  it('recencyScore : récent ≈ 1, ancien → 0, jamais utilisé = neutre 0.5', () => {
    const now = Date.parse('2026-06-10T12:00:00.000Z')
    expect(recencyScore(null, now)).toBeCloseTo(0.5, 5)
    expect(recencyScore('2026-06-10T12:00:00.000Z', now)).toBeCloseTo(1, 2)
    const old = recencyScore('2026-01-01T00:00:00.000Z', now)
    expect(old).toBeLessThan(0.2)
    expect(old).toBeGreaterThan(0)
  })

  it('formatFailureReason : horodaté, compacté, tronqué, repli sans détail', () => {
    const r = formatFailureReason('2026-06-10T09:30:00.000Z', '  timeout   réseau\nVercel ')
    expect(r).toBe('[2026-06-10] timeout réseau Vercel')
    expect(formatFailureReason('2026-06-10T09:30:00.000Z')).toBe('[2026-06-10] échec sans détail')
  })
})

describe('ProceduralEngine.storeProcedure', () => {
  it('crée une procédure hydratée + alimente la FTS', () => {
    const p = engine.storeProcedure({
      name: 'Déployer le site Primo sur Vercel',
      description: 'Commit en Nieto42 puis push pour relancer le déploiement',
      steps: ['git config user', 'git commit', 'git push'],
      trigger_patterns: ['deploiement vercel', 'publier site primo'],
      scope_id: 's1',
    })
    expect(p.id).toBeTruthy()
    expect(p.steps).toEqual(['git config user', 'git commit', 'git push'])
    expect(p.trigger_patterns).toEqual(['deploiement vercel', 'publier site primo'])
    expect(p.success_count).toBe(0)
    expect(p.failure_count).toBe(0)
    expect(p.failure_reasons).toEqual([])
    expect(p.quality_score).toBeCloseTo(0.5, 5)
    expect(p.lifecycle_state).toBe('active')
    expect(countFtsRows()).toBe(1)
    // relecture cohérente
    expect(engine.getProcedure(p.id)).toEqual(p)
  })

  it('UPSERT par id : re-store met à jour SANS dupliquer ni casser la FTS', () => {
    const p = engine.storeProcedure({ name: 'Cataphote obsolete', scope_id: 's1' })
    engine.storeProcedure({ id: p.id, name: 'Pangolin Vercel', scope_id: 's1' })

    const all = store.db.prepare('SELECT COUNT(*) AS c FROM procedures').get() as { c: number }
    expect(all.c).toBe(1)
    expect(countFtsRows()).toBe(1) // pas de fantôme

    expect(engine.getProcedure(p.id)!.name).toBe('Pangolin Vercel')

    // La recherche sur l'ANCIEN terme (mots uniques, non partagés) ne trouve plus
    // rien — la FTS est resynchronisée par le trigger procedures_au (réparation du
    // bug rebuildFts procedural.ts:296 : pas d'entrée fantôme sur l'ancien texte).
    expect(engine.matchProcedures('cataphote obsolete')).toHaveLength(0)
    const hit = engine.matchProcedures('Pangolin Vercel')
    expect(hit).toHaveLength(1)
    expect(hit[0]!.procedure.id).toBe(p.id)
  })
})

describe('ProceduralEngine.matchProcedures', () => {
  it('retrouve la procédure pertinente pour une requête de tâche', () => {
    engine.storeProcedure({
      name: 'Publier un article de blog Directus',
      description: 'POST draft puis PATCH published via curl avec le token',
      trigger_patterns: ['article blog directus', 'publier blog'],
      scope_id: 's1',
    })
    engine.storeProcedure({
      name: 'Notariser un DMG macOS',
      description: 'Signer et soumettre à Apple notarytool',
      trigger_patterns: ['notariser dmg', 'signature code'],
      scope_id: 's1',
    })

    const res = engine.matchProcedures('comment publier un article de blog')
    expect(res.length).toBeGreaterThanOrEqual(1)
    expect(res[0]!.procedure.name).toContain('Directus')
    expect(res[0]!.relevance).toBeGreaterThan(0)
    expect(res[0]!.score).toBeGreaterThan(0)
  })

  it('requête sans token significatif → aucun résultat (pas de throw)', () => {
    engine.storeProcedure({ name: 'Procédure X', description: 'desc', scope_id: 's1' })
    expect(engine.matchProcedures('a la')).toEqual([])
  })

  it('à pertinence égale, la procédure au PLUS HAUT TAUX DE SUCCÈS remonte en tête', () => {
    // Deux procédures au texte indexé IDENTIQUE (même name/desc/triggers) → même
    // pertinence FTS. Seul le vécu (succès/échec) doit les départager.
    const winner = engine.storeProcedure({
      name: 'Déployer sur Vercel',
      description: 'commit push relancer vercel',
      trigger_patterns: ['deploiement vercel'],
      scope_id: 's1',
    })
    const loser = engine.storeProcedure({
      name: 'Déployer sur Vercel',
      description: 'commit push relancer vercel',
      trigger_patterns: ['deploiement vercel'],
      scope_id: 's1',
    })
    // winner : 9 succès / 1 échec ; loser : 1 succès / 9 échecs.
    for (let i = 0; i < 9; i++) engine.recordExecution({ procedureId: winner.id, outcome: 'success' })
    engine.recordExecution({ procedureId: winner.id, outcome: 'failure', errorOutput: 'flaky' })
    engine.recordExecution({ procedureId: loser.id, outcome: 'success' })
    for (let i = 0; i < 9; i++) engine.recordExecution({ procedureId: loser.id, outcome: 'failure', errorOutput: 'KO' })

    const res = engine.matchProcedures('déployer sur vercel')
    expect(res.length).toBeGreaterThanOrEqual(2)
    expect(res[0]!.procedure.id).toBe(winner.id) // le plus fiable en tête
    expect(res[0]!.score).toBeGreaterThan(res[1]!.score)
  })

  it('borne aux scopes autorisés (anti-fuite)', () => {
    engine.storeProcedure({ name: 'Déployer Vercel privé', scope_id: 'secret' })
    engine.storeProcedure({ name: 'Déployer Vercel partagé', scope_id: 'public' })

    const res = engine.matchProcedures('déployer vercel', { scopeIds: ['public'] })
    expect(res).toHaveLength(1)
    expect(res[0]!.procedure.scope_id).toBe('public')
  })

  it('exclut les procédures non actives par défaut, sauf includeInactive', () => {
    engine.storeProcedure({ name: 'Déployer Vercel obsolète', scope_id: 's1', lifecycle_state: 'archived' })
    expect(engine.matchProcedures('déployer vercel')).toHaveLength(0)
    expect(engine.matchProcedures('déployer vercel', { includeInactive: true })).toHaveLength(1)
  })
})

describe('ProceduralEngine.recordExecution', () => {
  it('success incrémente success_count + quality_score + last_used_at', () => {
    const p = engine.storeProcedure({ name: 'Tester avec vitest', scope_id: 's1' })
    const r = engine.recordExecution({ procedureId: p.id, outcome: 'success' })
    expect(r.applied).toBe(true)
    const after = r.procedure!
    expect(after.success_count).toBe(1)
    expect(after.failure_count).toBe(0)
    expect(after.failure_reasons).toEqual([])
    expect(after.quality_score).toBeCloseTo(successRateOf(1, 0), 5)
    expect(after.quality_score).toBeGreaterThan(0.5)
    expect(after.last_used_at).not.toBeNull()
  })

  it('failure incrémente failure_count + append un motif horodaté', () => {
    const p = engine.storeProcedure({ name: 'Notariser DMG', scope_id: 's1' })
    const r = engine.recordExecution({
      procedureId: p.id,
      outcome: 'failure',
      errorOutput: 'notarytool timeout après 30 min',
    })
    const after = r.procedure!
    expect(after.failure_count).toBe(1)
    expect(after.success_count).toBe(0)
    expect(after.quality_score).toBeLessThan(0.5)
    expect(after.failure_reasons).toHaveLength(1)
    expect(after.failure_reasons[0]).toMatch(/^\[\d{4}-\d{2}-\d{2}\] notarytool timeout/)
  })

  it('FENÊTRE GLISSANTE 10 : le 11e échec évince le plus ancien (bug procedural.ts:1053)', () => {
    const p = engine.storeProcedure({ name: 'Build flaky', scope_id: 's1' })
    for (let i = 1; i <= FAILURE_REASONS_WINDOW + 1; i++) {
      engine.recordExecution({ procedureId: p.id, outcome: 'failure', errorOutput: `erreur n°${i}` })
    }
    const after = engine.getProcedure(p.id)!
    expect(after.failure_count).toBe(FAILURE_REASONS_WINDOW + 1) // compteur NON borné
    expect(after.failure_reasons).toHaveLength(FAILURE_REASONS_WINDOW) // motifs bornés à 10
    // Le plus ancien (n°1) est évincé ; les n°2..11 restent, dans l'ordre.
    expect(after.failure_reasons.some(r => r.includes('erreur n°1)'))).toBe(false)
    expect(after.failure_reasons[0]).toContain('erreur n°2')
    expect(after.failure_reasons.at(-1)).toContain(`erreur n°${FAILURE_REASONS_WINDOW + 1}`)
  })

  it('AUCUNE exception avalée : écrire failure_reasons NE log AUCUN debug/error', () => {
    // Réparation procedural.ts:1053 : en legacy, l'écriture levait 'no such column'
    // avalée par un catch console.debug. Ici la colonne existe : 0 log d'erreur.
    const errSpy = vi.spyOn(console, 'error').mockImplementation(() => {})
    const debugSpy = vi.spyOn(console, 'debug').mockImplementation(() => {})
    const warnSpy = vi.spyOn(console, 'warn').mockImplementation(() => {})

    const p = engine.storeProcedure({ name: 'Procédure surveillée', scope_id: 's1' })
    expect(() =>
      engine.recordExecution({ procedureId: p.id, outcome: 'failure', errorOutput: 'boom' }),
    ).not.toThrow()
    expect(engine.getProcedure(p.id)!.failure_reasons).toHaveLength(1)

    expect(errSpy).not.toHaveBeenCalled()
    expect(debugSpy).not.toHaveBeenCalled()
    expect(warnSpy).not.toHaveBeenCalled()
    errSpy.mockRestore()
    debugSpy.mockRestore()
    warnSpy.mockRestore()
  })

  it('procédure inconnue → applied=false, no-op (pas de throw)', () => {
    const r = engine.recordExecution({ procedureId: 'inconnu', outcome: 'success' })
    expect(r).toEqual({ applied: false, procedure: null })
  })

  it('FTS reste ALIGNÉE après update (pas de fantôme, bon id retourné)', () => {
    // 3 procédures distinctes → enregistrer des exécutions (UPDATE des compteurs,
    // PAS des colonnes FTS) ne doit JAMAIS désaligner procedures_fts.
    const a = engine.storeProcedure({ name: 'Alpha déploiement', scope_id: 's1' })
    const b = engine.storeProcedure({ name: 'Beta migration', scope_id: 's1' })
    const c = engine.storeProcedure({ name: 'Gamma notarisation', scope_id: 's1' })

    engine.recordExecution({ procedureId: a.id, outcome: 'success' })
    engine.recordExecution({ procedureId: b.id, outcome: 'failure', errorOutput: 'x' })
    engine.recordExecution({ procedureId: c.id, outcome: 'success' })

    expect(countFtsRows()).toBe(3) // 1 ligne FTS par procédure, aucune en trop

    // Chaque nom renvoie EXACTEMENT sa propre procédure (le bug rebuildFts
    // procedural.ts:296 renvoyait la mauvaise via un rowid désaligné).
    expect(engine.matchProcedures('Gamma notarisation')[0]!.procedure.id).toBe(c.id)
    expect(engine.matchProcedures('Beta migration')[0]!.procedure.id).toBe(b.id)
    expect(engine.matchProcedures('Alpha déploiement')[0]!.procedure.id).toBe(a.id)
  })
})

describe('ProceduralEngine.listProcedures / getProcedure', () => {
  it('liste les actives par défaut, triées par fiabilité', () => {
    const good = engine.storeProcedure({ name: 'Fiable', scope_id: 's1' })
    const bad = engine.storeProcedure({ name: 'Casse souvent', scope_id: 's1' })
    engine.storeProcedure({ name: 'Archivée', scope_id: 's1', lifecycle_state: 'archived' })
    for (let i = 0; i < 5; i++) engine.recordExecution({ procedureId: good.id, outcome: 'success' })
    for (let i = 0; i < 5; i++) engine.recordExecution({ procedureId: bad.id, outcome: 'failure', errorOutput: 'x' })

    const list = engine.listProcedures()
    expect(list.map(p => p.name)).toEqual(['Fiable', 'Casse souvent']) // archivée exclue, fiable en tête
    expect(engine.listProcedures({ includeInactive: true })).toHaveLength(3)
  })

  it('filtre par scope', () => {
    engine.storeProcedure({ name: 'P public', scope_id: 'public' })
    engine.storeProcedure({ name: 'P secret', scope_id: 'secret' })
    const list = engine.listProcedures({ scopeIds: ['public'] })
    expect(list).toHaveLength(1)
    expect(list[0]!.scope_id).toBe('public')
  })

  it('getProcedure inconnu → null', () => {
    expect(engine.getProcedure('nope')).toBeNull()
  })
})
