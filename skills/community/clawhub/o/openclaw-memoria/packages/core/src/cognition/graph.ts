/**
 * Graphe entité→relations (couche 5 legacy, portée propre, bucket B async).
 *
 * Modèle (décision GE-5) : UNE seule implémentation, arête NON-dirigée, 1 ligne
 * par paire (invariant `from_entity < to_entity`), poids ∈ [0,1] cap 1.0,
 * renforcement +0.1 par co-occurrence. La double implémentation Hebbian
 * (dirigée, cap 2.0, doublons) est JETÉE.
 *
 * Anti-fuite (le risque #1 du portage) : l'expansion au recall RESPECTE
 * toujours un ensemble de fact_ids autorisés fourni par le pré-filtre
 * permissions (§6.1). Le graphe ne contourne JAMAIS les permissions — un fait
 * hors scope autorisé n'est jamais remonté (benchmark §16 : fuite = 0).
 *
 * Liens fait↔entité via la table de jointure `fact_entities` (remplace le
 * `entity_ids LIKE` fragile, GE-3). Pas de colonne `status` : l'état actif d'un
 * fait = `superseded = 0` ; une arête vit par son poids (decay/prune).
 */
import type { Database } from 'better-sqlite3'
import { newId, nowISO } from '../util.js'
import type { RelationType } from './entities.js'

export interface RelationRow {
  id: string
  from_entity: string
  to_entity: string
  kind: string
  weight: number
  context: string
  created_at: string
  last_accessed_at: string
}

export interface DecayConfig {
  /** Facteur de decay par jour (défaut 0.995 ≈ -0.5 %/jour). */
  decayPerDay: number
  /** Poids minimal sous lequel l'arête est élaguée (défaut 0.05). */
  pruneThreshold: number
}

export const DEFAULT_DECAY: DecayConfig = { decayPerDay: 0.995, pruneThreshold: 0.05 }

const WEIGHT_INCREMENT = 0.1
const WEIGHT_CAP = 1.0
const INITIAL_WEIGHT = 0.5
const CONTEXT_CAP = 20

/** Ordonne la paire (invariant non-dirigé) : la plus petite id en premier. */
function orderedPair(a: string, b: string): [string, string] {
  return a <= b ? [a, b] : [b, a]
}

/**
 * Upsert d'une relation entre deux entités (par fait justificatif). Non-dirigée :
 * la paire est ordonnée → 1 SEULE ligne quel que soit l'ordre d'extraction.
 * Renforce le poids (cap 1.0) et accumule le fait dans le context (cappé 20).
 * Self-loop (a === b) ignoré.
 */
export function upsertRelation(
  db: Database,
  entityA: string,
  entityB: string,
  kind: RelationType,
  factId: string,
): void {
  if (entityA === entityB) return
  const [from, to] = orderedPair(entityA, entityB)
  const ts = nowISO()
  const existing = db
    .prepare('SELECT id, context FROM relations WHERE from_entity = ? AND to_entity = ?')
    .get(from, to) as { id: string; context: string } | undefined

  if (existing) {
    const context = appendContext(existing.context, factId)
    db.prepare(
      'UPDATE relations SET weight = MIN(weight + ?, ?), last_accessed_at = ?, context = ? WHERE id = ?',
    ).run(WEIGHT_INCREMENT, WEIGHT_CAP, ts, context, existing.id)
  } else {
    db.prepare(
      `INSERT INTO relations (id, from_entity, to_entity, kind, weight, context, created_at, last_accessed_at)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?)`,
    ).run(newId(), from, to, kind, INITIAL_WEIGHT, JSON.stringify([factId]), ts, ts)
  }
}

/** Lie un fait à une entité (idempotent via PK composite). */
export function linkFactEntity(db: Database, factId: string, entityId: string): void {
  db.prepare('INSERT OR IGNORE INTO fact_entities (fact_id, entity_id) VALUES (?, ?)').run(factId, entityId)
}

/**
 * Renforce TOUTES les paires d'un ensemble d'entités co-occurrentes dans un
 * même fait (Hebbian « fire together, wire together »). Corrige GE-1 : on
 * utilise les ids FRAÎCHEMENT extraits, le chemin s'exécute réellement.
 */
export function reinforceCooccurrence(db: Database, entityIds: string[], factId: string): void {
  for (let i = 0; i < entityIds.length; i++) {
    for (let j = i + 1; j < entityIds.length; j++) {
      upsertRelation(db, entityIds[i]!, entityIds[j]!, 'related_to', factId)
    }
  }
}

/**
 * EXPANSION au recall (étape 4 du pipeline §6.1) : à partir d'un ensemble de
 * faits germes, suit le graphe (BFS, `maxHops`) pour proposer des fact_ids
 * connexes — STRICTEMENT bornés par `allowedFactIds` (anti-fuite = 0).
 *
 * Retourne des fact_ids (PAS le contenu) : l'appelant les re-résout dans la DB
 * autorisée, jamais en contournant le pré-filtre. Un fait hors `allowedFactIds`
 * n'est jamais ni traversé ni remonté.
 */
export function expandByEntities(
  db: Database,
  seedFactIds: string[],
  allowedFactIds: ReadonlySet<string>,
  opts: { maxHops?: number; maxFacts?: number } = {},
): Array<{ fact_id: string; score: number; hops: number }> {
  const maxHops = opts.maxHops ?? 2
  const maxFacts = opts.maxFacts ?? 5
  // Germes filtrés : on ne part QUE de faits autorisés.
  const seeds = seedFactIds.filter(id => allowedFactIds.has(id))
  if (seeds.length === 0) return []

  // Entités des faits germes.
  const seedEntities = entitiesOfFacts(db, seeds)
  if (seedEntities.size === 0) return []

  const visited = new Set<string>(seedEntities)
  const queue: Array<{ entityId: string; hop: number }> = [...seedEntities].map(e => ({ entityId: e, hop: 0 }))
  // Meilleur score par fact_id découvert (hors germes).
  const scores = new Map<string, { score: number; hops: number }>()
  const getRelations = db.prepare(
    'SELECT from_entity, to_entity, weight FROM relations WHERE from_entity = ? OR to_entity = ?',
  )
  const factsOfEntity = db.prepare('SELECT fact_id FROM fact_entities WHERE entity_id = ?')

  while (queue.length > 0) {
    const { entityId, hop } = queue.shift()!
    if (hop >= maxHops) continue
    const rels = getRelations.all(entityId, entityId) as Array<{
      from_entity: string
      to_entity: string
      weight: number
    }>
    for (const rel of rels) {
      const neighbor = rel.from_entity === entityId ? rel.to_entity : rel.from_entity
      const hopPenalty = 1 / (hop + 1)
      const score = rel.weight * hopPenalty
      const neighborFacts = factsOfEntity.all(neighbor) as Array<{ fact_id: string }>
      for (const { fact_id } of neighborFacts) {
        // FILTRE DUR anti-fuite : jamais un fait hors de l'ensemble autorisé,
        // jamais un germe (déjà connu de l'appelant).
        if (!allowedFactIds.has(fact_id) || seeds.includes(fact_id)) continue
        const prev = scores.get(fact_id)
        if (!prev || prev.score < score) scores.set(fact_id, { score, hops: hop + 1 })
      }
      if (!visited.has(neighbor)) {
        visited.add(neighbor)
        queue.push({ entityId: neighbor, hop: hop + 1 })
      }
    }
  }

  return [...scores.entries()]
    .map(([fact_id, v]) => ({ fact_id, score: v.score, hops: v.hops }))
    .sort((a, b) => b.score - a.score)
    .slice(0, maxFacts)
}

/** Entités liées à un ensemble de faits (via la table de jointure). */
function entitiesOfFacts(db: Database, factIds: string[]): Set<string> {
  if (factIds.length === 0) return new Set()
  const placeholders = factIds.map(() => '?').join(',')
  const rows = db
    .prepare(`SELECT DISTINCT entity_id FROM fact_entities WHERE fact_id IN (${placeholders})`)
    .all(...factIds) as Array<{ entity_id: string }>
  return new Set(rows.map(r => r.entity_id))
}

/**
 * DECAY (corrige GE-2 : jamais branché dans le legacy). À déclencher en job
 * quotidien daemon. Affaiblit les arêtes selon le temps depuis le dernier
 * accès ; élague celles sous le seuil. Retourne {decayed, pruned}.
 */
export function applyDecay(db: Database, config: DecayConfig = DEFAULT_DECAY, now = Date.now()): {
  decayed: number
  pruned: number
} {
  const rows = db.prepare('SELECT id, weight, last_accessed_at, created_at FROM relations').all() as Array<{
    id: string
    weight: number
    last_accessed_at: string
    created_at: string
  }>
  const update = db.prepare('UPDATE relations SET weight = ? WHERE id = ?')
  const remove = db.prepare('DELETE FROM relations WHERE id = ?')
  let decayed = 0
  let pruned = 0
  const tx = db.transaction(() => {
    for (const rel of rows) {
      const ref = Date.parse(rel.last_accessed_at || rel.created_at)
      const days = Number.isNaN(ref) ? 0 : Math.max(0, (now - ref) / 86_400_000)
      const decayedWeight = rel.weight * Math.pow(config.decayPerDay, days)
      if (decayedWeight < config.pruneThreshold) {
        remove.run(rel.id)
        pruned++
      } else if (decayedWeight < rel.weight) {
        update.run(decayedWeight, rel.id)
        decayed++
      }
    }
  })
  tx()
  return { decayed, pruned }
}

/**
 * Sur supersession d'un fait : le retire du context des relations qu'il
 * justifiait ; relation au context vidé → supprimée, sinon affaiblie
 * (-0.15, plancher 0.1). Retire aussi ses liens fact_entities. Idempotent.
 */
export function onFactSuperseded(db: Database, factId: string): number {
  let affected = 0
  const tx = db.transaction(() => {
    const rels = db
      .prepare('SELECT id, context FROM relations WHERE context LIKE ?')
      .all(`%${factId}%`) as Array<{ id: string; context: string }>
    for (const rel of rels) {
      let ctx: string[]
      try {
        const parsed: unknown = JSON.parse(rel.context || '[]')
        ctx = Array.isArray(parsed) ? parsed.map(String) : []
      } catch {
        ctx = []
      }
      if (!ctx.includes(factId)) continue
      const updated = ctx.filter(id => id !== factId)
      if (updated.length === 0) {
        db.prepare('DELETE FROM relations WHERE id = ?').run(rel.id)
      } else {
        db.prepare('UPDATE relations SET context = ?, weight = MAX(weight - 0.15, 0.1) WHERE id = ?').run(
          JSON.stringify(updated),
          rel.id,
        )
      }
      affected++
    }
    db.prepare('DELETE FROM fact_entities WHERE fact_id = ?').run(factId)
  })
  tx()
  return affected
}

export interface GraphStats {
  entities: number
  relations: number
  avg_weight: number
}

export function graphStats(db: Database): GraphStats {
  const e = (db.prepare('SELECT COUNT(*) AS c FROM entities').get() as { c: number }).c
  const r = db.prepare('SELECT COUNT(*) AS c, AVG(weight) AS avg FROM relations').get() as {
    c: number
    avg: number | null
  }
  return { entities: e, relations: r.c, avg_weight: r.avg ?? 0 }
}

function appendContext(existing: string, factId: string): string {
  let arr: string[]
  try {
    const parsed: unknown = JSON.parse(existing || '[]')
    arr = Array.isArray(parsed) ? parsed.map(String) : []
  } catch {
    arr = []
  }
  if (!arr.includes(factId)) arr.push(factId)
  return JSON.stringify(arr.slice(-CONTEXT_CAP))
}
