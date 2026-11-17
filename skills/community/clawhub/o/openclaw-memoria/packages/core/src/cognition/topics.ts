/**
 * Couche TOPICS (thèmes, couche 14, bucket B async) — ENTITÉ-first.
 *
 * Produit : chaque fait est rangé dans un ou plusieurs SUJETS lisibles
 * (« Déploiement Vercel », « Client Transport Rino ») → l'utilisateur voit OÙ
 * un souvenir va, et filtre par thème. 0 LLM par défaut : le label dérive des
 * ENTITÉS déjà extraites par la couche graph (`fact_entities`/`entities`) et,
 * à défaut, des mots-clés saillants du fait.
 *
 * Réutilise les tables `topics` + `fact_topics` (content-schema). Une migration
 * additive (versions 20-29, sans collision avec cognition ≥10) ajoute les
 * colonnes de gestion (slug, fact_count, updated_at) + une jointure
 * topic_entities pour un matching robuste.
 */
import type { Database } from 'better-sqlite3'
import type { ContentStore, FactRow } from '../storage/content.js'
import { runMigrations, type Migration } from '../storage/migrations.js'
import { fromJsonArray, newId, nowISO, toJson } from '../util.js'
import { normalizeText, isContentWord } from '../storage/content.js'
import type { LlmProvider } from '../llm/provider.js'

export interface TopicSummary {
  id: string
  name: string
  fact_count: number
  importance_score: number
  keywords: string[]
}

export interface AssignResult {
  topic_ids: string[]
  topic_names: string[]
  created: boolean
}

/** Une arête du graphe des thèmes : deux thèmes liés + ce qui les relie. */
export interface TopicRelation {
  a: string
  b: string
  /** Poids = 2×faits partagés + entités partagées (fortes comptées double). */
  weight: number
  shared_facts: number
  shared_entities: number
  /** Quelques entités communes lisibles (« liés par : Néto, AutoCare »). */
  via: string[]
}

export interface TopicGraph {
  nodes: TopicSummary[]
  edges: TopicRelation[]
}

export const topicMigrations: Migration[] = [
  {
    version: 20,
    name: 'topics-management-columns',
    up(db) {
      // Colonnes ajoutées de façon défensive (la table topics vient du tronc).
      const cols = (db.pragma('table_info(topics)') as Array<{ name: string }>).map(c => c.name)
      if (!cols.includes('slug')) db.exec("ALTER TABLE topics ADD COLUMN slug TEXT DEFAULT ''")
      if (!cols.includes('fact_count')) db.exec('ALTER TABLE topics ADD COLUMN fact_count INTEGER NOT NULL DEFAULT 0')
      if (!cols.includes('updated_at')) db.exec("ALTER TABLE topics ADD COLUMN updated_at TEXT DEFAULT ''")
      db.exec(`
        CREATE TABLE IF NOT EXISTS topic_entities (
          topic_id TEXT NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
          entity_id TEXT NOT NULL,
          PRIMARY KEY (topic_id, entity_id)
        );
        CREATE INDEX IF NOT EXISTS idx_topic_entities_entity ON topic_entities(entity_id);
      `)
    },
  },
]

/** Mots vides FR/EN à exclure des keywords de thème. */
const STOPWORDS = new Set([
  'avec', 'pour', 'dans', 'sur', 'les', 'des', 'une', 'que', 'qui', 'est', 'son', 'sa', 'ses', 'par',
  'plus', 'fait', 'avoir', 'etre', 'cette', 'cet', 'aux', 'leur', 'the', 'and', 'for', 'with', 'that',
  'this', 'from', 'are', 'was', 'has', 'have', 'not', 'utilisateur', 'preference', 'doit', 'peut',
])

/** Priorité de typage pour choisir l'entité « dominante » d'un fait. */
const TYPE_RANK: Record<string, number> = { person: 5, company: 4, project: 4, client: 4, place: 3, tool: 2, concept: 1 }

export function ensureTopicSchema(db: Database): void {
  runMigrations(db, topicMigrations)
}

export function topicKeywords(text: string): string[] {
  return normalizeText(text)
    .split(/[^\p{L}\p{N}_-]+/u)
    .filter(w => w.length > 3 && !STOPWORDS.has(w) && isContentWord(w))
}

function titleCase(s: string): string {
  return s.replace(/\b\p{L}/gu, c => c.toUpperCase())
}

interface EntityInfo {
  id: string
  name: string
  type: string
}

export interface TopicEngineOptions {
  store: ContentStore
  llm?: LlmProvider | null
}

export class TopicEngine {
  private readonly store: ContentStore
  private readonly llm: LlmProvider | null

  constructor(opts: TopicEngineOptions) {
    this.store = opts.store
    this.llm = opts.llm ?? null
    ensureTopicSchema(this.store.db)
  }

  private get db(): Database {
    return this.store.db
  }

  /** Entités d'un fait (via la jointure du graphe), bruit « fichier/chemin » exclu. */
  private entitiesOf(factId: string): EntityInfo[] {
    const rows = this.db
      .prepare(
        `SELECT e.id, e.name, e.type FROM fact_entities fe
         JOIN entities e ON e.id = fe.entity_id WHERE fe.fact_id = ?`,
      )
      .all(factId) as EntityInfo[]
    return rows.filter(e => !isFileLike(e.name))
  }

  /** Rang de typage d'une entité (pour préférer person/company/project au matching). */
  private highRank(e: EntityInfo): boolean {
    return (TYPE_RANK[e.type] ?? 0) >= 4
  }

  /**
   * Range UN fait dans un (ou plusieurs) topic(s). Idempotent, 0 LLM par défaut.
   * Match si ≥2 entités partagées avec un topic, OU Jaccard de keywords > 0.5.
   */
  async assignFact(factId: string): Promise<AssignResult> {
    const fact = this.store.getFact(factId)
    if (!fact || fact.superseded) return { topic_ids: [], topic_names: [], created: false }

    const entities = this.entitiesOf(factId)
    const keywords = topicKeywords(fact.fact).slice(0, 12)

    // 1) Candidat par entités partagées : ≥2 entités OU ≥1 entité forte
    //    (person/company/project) → bonne consolidation.
    let topicId: string | null = null
    if (entities.length > 0) {
      const placeholders = entities.map(() => '?').join(',')
      const rows = this.db
        .prepare(
          `SELECT te.topic_id, COUNT(*) AS shared, MAX(CASE WHEN e.type IN ('person','company','project','client') THEN 1 ELSE 0 END) AS strong
           FROM topic_entities te JOIN entities e ON e.id = te.entity_id
           WHERE te.entity_id IN (${placeholders})
           GROUP BY te.topic_id ORDER BY shared DESC`,
        )
        .all(...entities.map(e => e.id)) as Array<{ topic_id: string; shared: number; strong: number }>
      const hit = rows.find(r => r.shared >= 2 || r.strong === 1)
      if (hit) topicId = hit.topic_id
    }

    // 2) Sinon, candidat par recouvrement de keywords (Jaccard > 0.4).
    if (!topicId && keywords.length > 0) {
      const all = this.db.prepare('SELECT id, keywords FROM topics').all() as Array<{ id: string; keywords: string }>
      const set = new Set(keywords)
      let best: { id: string; score: number } | null = null
      for (const t of all) {
        const tk = new Set(fromJsonArray(t.keywords))
        if (tk.size === 0) continue
        const inter = [...set].filter(k => tk.has(k)).length
        const union = new Set([...set, ...tk]).size
        const score = union > 0 ? inter / union : 0
        if (score > 0.4 && (!best || score > best.score)) best = { id: t.id, score }
      }
      if (best) topicId = best.id
    }

    let created = false
    if (!topicId) {
      topicId = await this.createTopic(fact, entities, keywords)
      created = true
    }

    // Lien fact↔topic + entités du topic + recompte.
    this.db.prepare('INSERT OR IGNORE INTO fact_topics (fact_id, topic_id) VALUES (?, ?)').run(factId, topicId)
    const linkEnt = this.db.prepare('INSERT OR IGNORE INTO topic_entities (topic_id, entity_id) VALUES (?, ?)')
    for (const e of entities) linkEnt.run(topicId, e.id)
    this.recompute(topicId, keywords)

    const name = (this.db.prepare('SELECT name FROM topics WHERE id = ?').get(topicId) as { name: string }).name
    return { topic_ids: [topicId], topic_names: [name], created }
  }

  private async createTopic(fact: { id: string; fact: string; scope_id: string }, entities: EntityInfo[], keywords: string[]): Promise<string> {
    let label = this.heuristicLabel(entities, keywords)
    // LLM SEULEMENT si le label heuristique est faible (1 mot générique) et provider fourni.
    if (this.llm && label.split(' ').length < 2) {
      try {
        if (await this.llm.isAvailable()) {
          const raw = await this.llm.complete({
            system: 'Donne un titre de THÈME court (2-4 mots, Title Case) pour ce souvenir. Réponds UNIQUEMENT le titre.',
            prompt: fact.fact,
            maxTokens: 16,
            temperature: 0.2,
          })
          const cleaned = raw.trim().replace(/^["'#\s]+|["'.\s]+$/g, '').slice(0, 60)
          if (cleaned.length >= 3) label = titleCase(cleaned)
        }
      } catch (err) {
        console.warn(`[memoria:topics] libellé LLM en échec (fait ${fact.id}) — heuristique :`, (err as Error).message)
      }
    }
    const id = newId()
    const ts = nowISO()
    this.db
      .prepare(
        `INSERT INTO topics (id, name, scope_id, sensitivity, importance_score, keywords, slug, fact_count, created_at, updated_at)
         VALUES (?, ?, ?, 'normal', 0, ?, ?, 0, ?, ?)`,
      )
      .run(id, label, fact.scope_id, toJson(keywords.slice(0, 8)), slugify(label), ts, ts)
    return id
  }

  /** Label lisible sans LLM : entité dominante + qualificatif, ou keywords saillants. */
  private heuristicLabel(entities: EntityInfo[], keywords: string[]): string {
    if (entities.length > 0) {
      const dominant = [...entities].sort((a, b) => (TYPE_RANK[b.type] ?? 0) - (TYPE_RANK[a.type] ?? 0))[0]!
      const second = entities.find(e => e.id !== dominant.id)
      return titleCase(second ? `${dominant.name} ${second.name}` : dominant.name)
    }
    if (keywords.length > 0) return titleCase(keywords.slice(0, 3).join(' '))
    return 'Divers'
  }

  /** Recompte fact_count + importance + fusionne les keywords. */
  private recompute(topicId: string, extraKeywords: string[]): void {
    const count = (this.db.prepare('SELECT COUNT(*) AS c FROM fact_topics WHERE topic_id = ?').get(topicId) as { c: number }).c
    if (count === 0) {
      this.db.prepare('DELETE FROM topics WHERE id = ?').run(topicId)
      return
    }
    // récence : dernier fait du topic
    const last = this.db
      .prepare(
        `SELECT MAX(f.created_at) AS m FROM fact_topics ft JOIN facts f ON f.id = ft.fact_id WHERE ft.topic_id = ?`,
      )
      .get(topicId) as { m: string | null }
    const ageDays = last.m ? Math.max(0, (Date.now() - Date.parse(last.m)) / 86_400_000) : 999
    const recency = Math.exp((-Math.LN2 * ageDays) / 120)
    const importance = count * (0.5 + 0.5 * recency)

    const existing = new Set(fromJsonArray((this.db.prepare('SELECT keywords FROM topics WHERE id = ?').get(topicId) as { keywords: string }).keywords))
    for (const k of extraKeywords) existing.add(k)
    this.db
      .prepare('UPDATE topics SET fact_count = ?, importance_score = ?, keywords = ?, updated_at = ? WHERE id = ?')
      .run(count, importance, toJson([...existing].slice(0, 12)), nowISO(), topicId)
  }

  /** Range tous les faits actifs sans topic (post-capture async + rattrapage boot). */
  async assignPending(limit = 200): Promise<number> {
    const pending = this.db
      .prepare(
        `SELECT f.id FROM facts f
         WHERE f.superseded = 0
           AND NOT EXISTS (SELECT 1 FROM fact_topics ft WHERE ft.fact_id = f.id)
         ORDER BY f.created_at DESC LIMIT ?`,
      )
      .all(limit) as Array<{ id: string }>
    let done = 0
    for (const row of pending) {
      const r = await this.assignFact(row.id)
      if (r.topic_ids.length > 0) done++
    }
    return done
  }

  listTopics(opts: { minFacts?: number } = {}): TopicSummary[] {
    const min = opts.minFacts ?? 1
    const rows = this.db
      .prepare('SELECT id, name, fact_count, importance_score, keywords FROM topics WHERE fact_count >= ? ORDER BY importance_score DESC')
      .all(min) as Array<{ id: string; name: string; fact_count: number; importance_score: number; keywords: string }>
    return rows.map(r => ({ ...r, keywords: fromJsonArray(r.keywords) }))
  }

  /**
   * Graphe des thèmes : deux thèmes sont LIÉS s'ils partagent des faits (signal
   * fort : un même souvenir range dans deux thèmes) ou des entités (Néto, un
   * client, un projet apparaissent dans les deux). C'est le « où voir les
   * relations entre thèmes » du panneau Réglages/Thèmes — purement lecture, 0 LLM.
   */
  relations(opts: { minFacts?: number; minWeight?: number; topNodes?: number; maxEdges?: number } = {}): TopicGraph {
    // On borne le graphe pour qu'il reste LISIBLE : seuls les thèmes les plus
    // importants (déjà triés par importance) entrent dans la carte, et on plafonne
    // le nombre d'arêtes (les plus fortes d'abord). Sans ça, une grosse mémoire
    // produit des centaines d'arêtes illisibles.
    const topNodes = opts.topNodes ?? 28
    const maxEdges = opts.maxEdges ?? 70
    const nodes = this.listTopics({ minFacts: opts.minFacts ?? 2 }).slice(0, topNodes)
    const keep = new Set(nodes.map(n => n.id))
    const minWeight = opts.minWeight ?? 1

    // 1) faits partagés (a < b pour ne compter chaque paire qu'une fois)
    const sharedFacts = this.db
      .prepare(
        `SELECT ft1.topic_id AS a, ft2.topic_id AS b, COUNT(*) AS n
         FROM fact_topics ft1 JOIN fact_topics ft2
           ON ft1.fact_id = ft2.fact_id AND ft1.topic_id < ft2.topic_id
         GROUP BY ft1.topic_id, ft2.topic_id`,
      )
      .all() as Array<{ a: string; b: string; n: number }>

    // 2) entités partagées (+ noms lisibles, fortes comptées double, fortes d'abord
    //    pour que « via » montre Néto/un client/un projet avant les entités faibles)
    const sharedEnt = this.db
      .prepare(
        `SELECT te1.topic_id AS a, te2.topic_id AS b, e.name AS name,
                CASE WHEN e.type IN ('person','company','project','client') THEN 2 ELSE 1 END AS strength
         FROM topic_entities te1
         JOIN topic_entities te2 ON te1.entity_id = te2.entity_id AND te1.topic_id < te2.topic_id
         JOIN entities e ON e.id = te1.entity_id
         ORDER BY strength DESC`,
      )
      .all() as Array<{ a: string; b: string; name: string; strength: number }>

    const edges = new Map<string, TopicRelation>()
    const key = (a: string, b: string): string => `${a}|${b}`
    const ensure = (a: string, b: string): TopicRelation | null => {
      if (!keep.has(a) || !keep.has(b)) return null
      const k = key(a, b)
      let e = edges.get(k)
      if (!e) {
        e = { a, b, weight: 0, shared_facts: 0, shared_entities: 0, via: [] }
        edges.set(k, e)
      }
      return e
    }

    for (const r of sharedFacts) {
      const e = ensure(r.a, r.b)
      if (e) { e.shared_facts = r.n; e.weight += 2 * r.n }
    }
    const viaNoise = (name: string): boolean => name.length <= 2 || STOPWORDS.has(name.toLowerCase())
    for (const r of sharedEnt) {
      const e = ensure(r.a, r.b)
      if (!e) continue
      e.shared_entities += 1
      e.weight += r.strength
      if (e.via.length < 5 && !viaNoise(r.name) && !e.via.includes(r.name)) e.via.push(r.name)
    }

    const out = [...edges.values()]
      .filter(e => e.weight >= minWeight)
      .sort((x, y) => y.weight - x.weight)
      .slice(0, maxEdges)
    // ne garder que les nœuds réellement reliés (sinon des points isolés flottent)
    const linked = new Set<string>()
    for (const e of out) { linked.add(e.a); linked.add(e.b) }
    return { nodes: nodes.filter(n => linked.has(n.id)), edges: out }
  }

  topicsForFact(factId: string): TopicSummary[] {
    const rows = this.db
      .prepare(
        `SELECT t.id, t.name, t.fact_count, t.importance_score, t.keywords
         FROM fact_topics ft JOIN topics t ON t.id = ft.topic_id WHERE ft.fact_id = ?`,
      )
      .all(factId) as Array<{ id: string; name: string; fact_count: number; importance_score: number; keywords: string }>
    return rows.map(r => ({ ...r, keywords: fromJsonArray(r.keywords) }))
  }

  factsForTopic(topicId: string, opts: { limit?: number } = {}): FactRow[] {
    return this.db
      .prepare(
        `SELECT f.* FROM fact_topics ft JOIN facts f ON f.id = ft.fact_id
         WHERE ft.topic_id = ? AND f.superseded = 0 ORDER BY f.created_at DESC LIMIT ?`,
      )
      .all(topicId, opts.limit ?? 50) as FactRow[]
  }

  /** Oubli : retire les faits des topics, recompte, supprime les topics vides. Retourne nb topics supprimés. */
  onForget(factIds: string[]): number {
    if (factIds.length === 0) return 0
    const placeholders = factIds.map(() => '?').join(',')
    const affected = this.db
      .prepare(`SELECT DISTINCT topic_id FROM fact_topics WHERE fact_id IN (${placeholders})`)
      .all(...factIds) as Array<{ topic_id: string }>
    this.db.prepare(`DELETE FROM fact_topics WHERE fact_id IN (${placeholders})`).run(...factIds)
    let removed = 0
    for (const a of affected) {
      const before = this.db.prepare('SELECT id FROM topics WHERE id = ?').get(a.topic_id)
      this.recompute(a.topic_id, [])
      const after = this.db.prepare('SELECT id FROM topics WHERE id = ?').get(a.topic_id)
      if (before && !after) removed++
    }
    return removed
  }
}

function slugify(s: string): string {
  return normalizeText(s).replace(/[^\p{L}\p{N}]+/gu, '-').replace(/^-+|-+$/g, '').slice(0, 60)
}

/** Une entité « fichier/chemin » (AppsPage.tsx, config.env, /Users/…) pollue les thèmes. */
function isFileLike(name: string): boolean {
  return /\.[a-z0-9]{1,5}\b/i.test(name) || name.includes('/') || name.includes('\\')
}
