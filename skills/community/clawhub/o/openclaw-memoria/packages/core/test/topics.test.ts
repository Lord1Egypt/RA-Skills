/**
 * Couche TOPICS : range les faits par thème (entité-first, 0 LLM par défaut).
 * Vérifie : faits d'un même sujet → même topic ; sans rapport → topics
 * distincts ; idempotence ; tri par importance ; onForget vide le topic.
 */
import { mkdtempSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { afterEach, beforeEach, describe, expect, it } from 'vitest'
import { ContentStore } from '../src/storage/content.js'
import { CognitionEngine } from '../src/cognition/index.js'
import { TopicEngine } from '../src/cognition/topics.js'

let dir: string
let store: ContentStore
let cognition: CognitionEngine
let topics: TopicEngine

beforeEach(() => {
  dir = mkdtempSync(join(tmpdir(), 'memoria-topics-'))
  store = new ContentStore(join(dir, 'c.sqlite'))
  cognition = new CognitionEngine({ store })
  topics = new TopicEngine({ store })
})

afterEach(() => {
  store.close()
  rmSync(dir, { recursive: true, force: true })
})

/** Insère un fait, peuple ses entités (graph), puis le range dans un topic. */
async function add(text: string, scope = 's1'): Promise<string> {
  const f = store.insertFact({ fact: text, scope_id: scope })
  await cognition.processFact(f.id) // peuple fact_entities
  await topics.assignFact(f.id)
  return f.id
}

describe('TopicEngine', () => {
  it('deux faits sur le même sujet (entités communes) → même topic', async () => {
    await add('Le déploiement du projet Vercel utilise le compte Hello-Primo')
    await add('Le projet Vercel échoue parfois quand le cache Hello-Primo est corrompu')
    const list = topics.listTopics()
    // au moins un topic regroupe les deux faits Vercel/Hello-Primo
    const vercel = list.find(t => /vercel|hello/i.test(t.name) && t.fact_count >= 2)
    expect(vercel).toBeTruthy()
  })

  it('faits sans rapport → topics distincts, label lisible', async () => {
    await add('La recette de cuisine du dimanche utilise du curcuma frais')
    await add('Le serveur Directus est derrière Cloudflare en Guyane')
    const list = topics.listTopics()
    expect(list.length).toBeGreaterThanOrEqual(2)
    // labels non vides et lisibles
    for (const t of list) expect(t.name.length).toBeGreaterThan(2)
  })

  it('idempotent : re-assigner ne duplique pas le lien', async () => {
    const id = await add('Le client Transport Rino veut des bons de livraison numériques')
    await topics.assignFact(id)
    await topics.assignFact(id)
    const tf = topics.topicsForFact(id)
    expect(tf.length).toBeGreaterThan(0)
    const links = store.db.prepare('SELECT COUNT(*) AS c FROM fact_topics WHERE fact_id = ?').get(id) as { c: number }
    expect(links.c).toBe(tf.length) // pas de doublon
  })

  it('listTopics trié par importance ; factsForTopic retourne les faits', async () => {
    await add('Le projet Memoria tourne en TypeScript sur Node')
    await add('Le projet Memoria utilise sqlite-vec pour le recall')
    await add('Le projet Memoria a un daemon local unique')
    const list = topics.listTopics()
    expect(list[0]!.importance_score).toBeGreaterThanOrEqual(list[list.length - 1]!.importance_score)
    const memoria = list.find(t => /memoria/i.test(t.name))
    if (memoria) {
      const facts = topics.factsForTopic(memoria.id)
      expect(facts.length).toBe(memoria.fact_count)
    }
  })

  it('onForget vide le topic et le supprime s’il devient vide', async () => {
    const id = await add('Sujet unique sur le serveur Scaleway de staging')
    const before = topics.topicsForFact(id)
    expect(before.length).toBeGreaterThan(0)
    const removed = topics.onForget([id])
    expect(removed).toBeGreaterThan(0)
    expect(topics.listTopics().find(t => t.id === before[0]!.id)).toBeUndefined()
  })

  it('assignPending range les faits non classés', async () => {
    const f1 = store.insertFact({ fact: 'Note sur le pipeline CI GitHub Actions', scope_id: 's1' })
    const f2 = store.insertFact({ fact: 'Le pipeline CI GitHub échoue sur Node 20', scope_id: 's1' })
    await cognition.processFact(f1.id)
    await cognition.processFact(f2.id)
    const done = await topics.assignPending()
    expect(done).toBe(2)
    expect(topics.topicsForFact(f1.id).length).toBeGreaterThan(0)
  })
})

/** Insère un topic « nu » (sans passer par assignFact) pour tester relations(). */
function seedTopic(store: ContentStore, id: string, name: string, factCount: number): void {
  const ts = new Date().toISOString()
  store.db
    .prepare(
      `INSERT INTO topics (id, name, scope_id, sensitivity, importance_score, keywords, slug, fact_count, created_at, updated_at)
       VALUES (?, ?, 's1', 'normal', ?, '[]', ?, ?, ?, ?)`,
    )
    .run(id, name, factCount, name.toLowerCase().replace(/\s+/g, '-'), factCount, ts, ts)
}
function seedEntity(store: ContentStore, id: string, name: string, type: string): void {
  store.db.prepare('INSERT INTO entities (id, name, type, mention_count, created_at) VALUES (?, ?, ?, 1, ?)').run(id, name, type, new Date().toISOString())
}
function link(store: ContentStore, topicId: string, entityId: string): void {
  store.db.prepare('INSERT OR IGNORE INTO topic_entities (topic_id, entity_id) VALUES (?, ?)').run(topicId, entityId)
}

describe('TopicEngine.relations (graphe des thèmes)', () => {
  it('deux thèmes partageant des entités sont reliés ; « via » liste les fortes d’abord', () => {
    seedTopic(store, 'A', 'Projet JamBoard', 3)
    seedTopic(store, 'B', 'Projet AutoCare', 3)
    seedTopic(store, 'C', 'Recette de cuisine', 2) // isolé, ne partage rien
    seedEntity(store, 'e-neto', 'Néto', 'person') // forte
    seedEntity(store, 'e-fb', 'Firebase', 'tool') // faible
    seedEntity(store, 'e-jb', 'JamBoard', 'project')
    seedEntity(store, 'e-ac', 'AutoCare', 'project')
    link(store, 'A', 'e-neto'); link(store, 'A', 'e-fb'); link(store, 'A', 'e-jb')
    link(store, 'B', 'e-neto'); link(store, 'B', 'e-fb'); link(store, 'B', 'e-ac')

    const g = topics.relations({ minFacts: 2 })
    const edge = g.edges.find(e => (e.a === 'A' && e.b === 'B') || (e.a === 'B' && e.b === 'A'))
    expect(edge).toBeTruthy()
    expect(edge!.shared_entities).toBe(2) // Néto + Firebase
    expect(edge!.weight).toBe(3) // person(2) + tool(1)
    expect(edge!.via[0]).toBe('Néto') // forte en tête
    expect(edge!.via).toContain('Firebase')
    // le thème isolé n'apparaît pas dans le graphe (aucune arête)
    expect(g.nodes.find(n => n.id === 'C')).toBeUndefined()
  })

  it('un souvenir rangé dans deux thèmes crée un lien fort (shared_facts)', () => {
    seedTopic(store, 'X', 'Migration Vercel', 2)
    seedTopic(store, 'Y', 'Déploiement Hello-Primo', 2)
    const f = store.insertFact({ fact: 'Le déploiement Vercel utilise le compte Hello-Primo', scope_id: 's1' })
    store.db.prepare('INSERT INTO fact_topics (fact_id, topic_id) VALUES (?, ?)').run(f.id, 'X')
    store.db.prepare('INSERT INTO fact_topics (fact_id, topic_id) VALUES (?, ?)').run(f.id, 'Y')

    const g = topics.relations({ minFacts: 2 })
    const edge = g.edges.find(e => (e.a === 'X' && e.b === 'Y') || (e.a === 'Y' && e.b === 'X'))
    expect(edge).toBeTruthy()
    expect(edge!.shared_facts).toBe(1)
    expect(edge!.weight).toBeGreaterThanOrEqual(2) // faits partagés comptent double
  })

  it('respecte le plafond d’arêtes (maxEdges)', () => {
    for (let i = 0; i < 6; i++) seedTopic(store, `T${i}`, `Thème ${i}`, 2)
    seedEntity(store, 'hub', 'PivotCommun', 'concept')
    for (let i = 0; i < 6; i++) link(store, `T${i}`, 'hub') // graphe complet → 15 arêtes
    const g = topics.relations({ minFacts: 2, maxEdges: 5 })
    expect(g.edges.length).toBe(5)
  })
})
