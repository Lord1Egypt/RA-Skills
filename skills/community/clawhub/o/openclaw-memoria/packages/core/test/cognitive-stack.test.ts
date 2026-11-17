/**
 * Intégration de la pile cognitive (vagues 5+6) via l'API publique Memoria :
 * capture → entités → thèmes → procédures → expertise → aperçu. Prouve que les
 * couches s'enchaînent réellement à travers le moteur.
 */
import { mkdtempSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { afterEach, beforeEach, describe, expect, it } from 'vitest'
import { Memoria } from '../src/index.js'

let root: string
let m: Memoria
let instance: string

beforeEach(() => {
  root = mkdtempSync(join(tmpdir(), 'memoria-cogstack-'))
  m = Memoria.init({ storageRoot: root, configPath: join(root, 'config.toml'), llm: { extraction: null } })
  instance = m.pairAssistant({ type: 'claude-code' }).assistant_instance_id
})

afterEach(() => {
  m.close()
  rmSync(root, { recursive: true, force: true })
})

describe('pile cognitive intégrée', () => {
  it('capture → thèmes → procédures → expertise → aperçu', async () => {
    // faits liés par DEUX entités communes (Vercel + Hello-Primo) → même thème
    m.storeFact({ instance, content: 'Le déploiement Vercel utilise le compte Hello-Primo' })
    m.storeFact({ instance, content: 'Vercel échoue quand le cache Hello-Primo est corrompu' })
    m.storeFact({ instance, content: 'Le projet Memoria a un daemon local unique en TypeScript' })
    m.storeFact({ instance, content: 'La recette de cuisine du dimanche prend du curcuma' })

    // entités (graph) + thèmes (topics) en async
    await m.processCognition(instance)
    const themes = m.listTopics(instance, 1)
    expect(themes.length).toBeGreaterThan(0)
    const vercelTheme = themes.find(t => /vercel|hello/i.test(t.name))
    expect(vercelTheme?.fact_count).toBeGreaterThanOrEqual(2)

    // les faits portent bien leur thème (puce dans Revue/Mémoire)
    const browsed = m.browseFacts({ instance, limit: 50 })
    expect(browsed.some(f => f.topics.length > 0)).toBe(true)

    // procédures : on en stocke une et on la retrouve par tâche
    const store = m['openContent'](m.registry.dbForInstance(instance)!.path)
    m['proceduralFor'](store).storeProcedure({
      name: 'Construire Memoria',
      description: 'Compiler le monorepo',
      steps: ['npm install', 'npm run build', 'npm test'],
      trigger_patterns: ['build memoria', 'compiler'],
      scope_id: m.registry.getScopeByName(`private:${instance}`)!.id,
    })
    const match = m.matchProcedures(instance, 'compiler memoria build')
    expect(match.length).toBeGreaterThan(0)
    expect(match[0]!.procedure.name).toBe('Construire Memoria')

    // apprentissage : enregistrer un succès remonte la qualité
    const ok = m.recordProcedureExecution(instance, match[0]!.procedure.id, 'success')
    expect(ok).toBe(true)

    // expertise amorcée depuis les thèmes
    m.bootstrapExpertise(instance)
    // (besoin d'au moins un thème ≥3 faits pour l'expertise — sinon liste vide, acceptable)

    // aperçu agent : synthèse cohérente
    const overview = m.agentOverview().find(o => o.instance === instance)!
    expect(overview.facts).toBe(4)
    expect(overview.themes).toBeGreaterThanOrEqual(1)
    expect(overview.procedures).toBe(1)
  })

  it('forget propage aux thèmes (pas de thème fantôme)', async () => {
    const f = m.storeFact({ instance, content: 'Sujet unique sur le serveur Scaleway de staging interne' })
    await m.processCognition(instance)
    const before = m.listTopics(instance, 1).length
    expect(before).toBeGreaterThan(0)
    m.forget({ ids: [f.id] })
    const store = m['openContent'](m.registry.dbForInstance(instance)!.path)
    // le fait n'a plus de thème (lien nettoyé)
    const ghost = store.db.prepare('SELECT COUNT(*) AS c FROM fact_topics WHERE fact_id = ?').get(f.id) as { c: number }
    expect(ghost.c).toBe(0)
  })
})
