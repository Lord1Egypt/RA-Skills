/**
 * Couche FACT-CLUSTERS (couche 16, bucket B async — spec §12).
 *
 * Différence avec TOPICS : un topic est un LIBELLÉ lisible qu'on attribue à un
 * fait (« Déploiement Vercel »). Un CLUSTER est STRUCTUREL : un « paquet » de
 * faits qui vont ensemble parce qu'ils partagent beaucoup d'entités/keywords,
 * indépendamment d'un libellé. Le cluster est plus large/transversal (un fait
 * peut relier deux topics) et sert à la consolidation/observation par lots et à
 * la carte 3D. Le label n'est qu'un repère humain, pas l'identité du cluster.
 *
 * 0 LLM : le clustering est purement structurel (entités partagées via
 * `fact_entities`, complétées par les keywords du fait). C'est un job ASYNC
 * (rebuild batch), jamais dans le chemin de réponse du recall.
 *
 * Idempotence : `rebuild()` est un recalcul COMPLET déterministe — il efface les
 * clusters précédents et reconstruit. Deux rebuilds consécutifs sur le même état
 * produisent les mêmes paquets (mêmes membres) ; seuls les ids changent, jamais
 * la partition. `onForget` retire des faits et dissout les clusters qui passent
 * sous `minSize`.
 *
 * Migrations 60-69 (créneau réservé à cette couche, partage `schema_migrations`).
 */
import type { Database } from 'better-sqlite3'
import type { ContentStore } from '../storage/content.js'
import { runMigrations, type Migration } from '../storage/migrations.js'
import { fromJsonArray, newId, nowISO, toJson } from '../util.js'
import { normalizeText, isContentWord } from '../storage/content.js'

export const clusterMigrations: Migration[] = [
  {
    version: 60,
    name: 'fact-clusters-initial',
    up(db) {
      db.exec(`
        -- FACT-CLUSTERS : paquets STRUCTURELS de faits liés (entités/keywords).
        --  member_fact_ids   = JSON array des faits du cluster (source de vérité
        --                      des membres ; cluster_members = jointure indexable) ;
        --  centroid_keywords = JSON array des keywords les + représentatifs ;
        --  size              = nb de membres (= longueur de member_fact_ids).
        -- AUCUNE colonne ne touche aux faits : un cluster est descriptif.
        CREATE TABLE fact_clusters (
          id TEXT PRIMARY KEY,
          label TEXT NOT NULL DEFAULT '',
          member_fact_ids TEXT NOT NULL DEFAULT '[]',
          centroid_keywords TEXT NOT NULL DEFAULT '[]',
          size INTEGER NOT NULL DEFAULT 0,
          created_at TEXT NOT NULL,
          updated_at TEXT NOT NULL
        );
        -- Jointure fait↔cluster (JOIN exact et indexable dans les deux sens),
        -- doublée du JSON member_fact_ids pour la lecture directe.
        CREATE TABLE cluster_members (
          cluster_id TEXT NOT NULL REFERENCES fact_clusters(id) ON DELETE CASCADE,
          fact_id TEXT NOT NULL,
          PRIMARY KEY (cluster_id, fact_id)
        );
        CREATE INDEX idx_cluster_members_fact ON cluster_members(fact_id);
      `)
    },
  },
]

/** Applique le schéma clusters à une DB de contenu (idempotent — re-run sans effet). */
export function ensureClusterSchema(db: Database): number {
  return runMigrations(db, clusterMigrations)
}

export interface ClusterRow {
  id: string
  label: string
  member_fact_ids: string
  centroid_keywords: string
  size: number
  created_at: string
  updated_at: string
}

/** Cluster hydraté (JSON parsé) — forme exposée à l'UI/daemon/tests. */
export interface Cluster {
  id: string
  label: string
  member_fact_ids: string[]
  centroid_keywords: string[]
  size: number
  created_at: string
  updated_at: string
}

export interface RebuildOptions {
  /** Taille minimale d'un paquet pour devenir un cluster (défaut 3). */
  minSize?: number
  /** Force de lien minimale (entités/keywords partagés) pour relier 2 faits. Défaut 0.34. */
  linkThreshold?: number
}

export interface RebuildResult {
  /** Nombre de clusters retenus (taille ≥ minSize). */
  clusters: number
  /** Faits couverts par un cluster. */
  factsClustered: number
}

const DEFAULT_MIN_SIZE = 3
const DEFAULT_LINK_THRESHOLD = 0.34
const MAX_CENTROID_KEYWORDS = 8

/** Mots-outils FR/EN ignorés pour les keywords structurels. */
const STOPWORDS = new Set([
  'pour', 'avec', 'dans', 'plus', 'mais', 'que', 'qui', 'les', 'des', 'une', 'mon', 'mes',
  'son', 'ses', 'est', 'sont', 'sur', 'par', 'pas', 'tout', 'tous', 'toujours', 'jamais',
  'cette', 'cet', 'aux', 'leur', 'the', 'and', 'for', 'with', 'this', 'that', 'have', 'has',
  'are', 'was', 'were', 'you', 'your', 'always', 'never', 'all', 'any', 'not', 'utilise',
])

/** Keywords significatifs d'un fait (normalisés, > 3 car., hors stopwords). */
export function clusterKeywords(text: string): string[] {
  return normalizeText(text)
    .split(/[^\p{L}\p{N}_-]+/u)
    .map(t => t.trim())
    .filter(t => t.length > 3 && !STOPWORDS.has(t) && isContentWord(t))
}

/** Forme interne d'un fait pendant le clustering. */
interface Node {
  id: string
  /** Signature = ids d'entités (préfixés) ∪ keywords. Base du lien structurel. */
  signature: Set<string>
  keywords: string[]
}

export interface ClusterEngineOptions {
  store: ContentStore
}

export class ClusterEngine {
  private readonly store: ContentStore

  constructor(opts: ClusterEngineOptions) {
    this.store = opts.store
    // Schéma appliqué paresseusement (idempotent) : la couche est utilisable seule.
    ensureClusterSchema(this.store.db)
  }

  get db(): Database {
    return this.store.db
  }

  /**
   * Recalcul COMPLET des clusters (job async batch). Déterministe et idempotent :
   * efface les clusters existants, repartitionne les faits actifs en composantes
   * connexes du graphe de proximité structurelle, ne garde que les paquets de
   * taille ≥ minSize. Ne touche AUCUN fait.
   */
  rebuild(opts: RebuildOptions = {}): RebuildResult {
    const minSize = Math.max(2, opts.minSize ?? DEFAULT_MIN_SIZE)
    const threshold = opts.linkThreshold ?? DEFAULT_LINK_THRESHOLD

    const nodes = this.loadNodes()
    const groups = connectedComponents(nodes, threshold).filter(g => g.length >= minSize)

    let clustered = 0
    const tx = this.db.transaction(() => {
      // Recalcul complet : on repart d'une table propre (déterminisme de partition).
      this.db.prepare('DELETE FROM cluster_members').run()
      this.db.prepare('DELETE FROM fact_clusters').run()

      const insCluster = this.db.prepare(
        `INSERT INTO fact_clusters (id, label, member_fact_ids, centroid_keywords, size, created_at, updated_at)
         VALUES (?, ?, ?, ?, ?, ?, ?)`,
      )
      const insMember = this.db.prepare('INSERT OR IGNORE INTO cluster_members (cluster_id, fact_id) VALUES (?, ?)')
      const ts = nowISO()

      for (const group of groups) {
        const memberIds = group.map(n => n.id).sort()
        const centroid = centroidKeywords(group)
        const label = labelFor(centroid, memberIds.length)
        const id = newId()
        insCluster.run(id, label, toJson(memberIds), toJson(centroid), memberIds.length, ts, ts)
        for (const fid of memberIds) insMember.run(id, fid)
        clustered += memberIds.length
      }
    })
    tx()

    return { clusters: groups.length, factsClustered: clustered }
  }

  /** Tous les clusters, triés par taille décroissante. */
  listClusters(opts: { minSize?: number } = {}): Cluster[] {
    const min = opts.minSize ?? 1
    const rows = this.db
      .prepare('SELECT * FROM fact_clusters WHERE size >= ? ORDER BY size DESC, created_at ASC')
      .all(min) as ClusterRow[]
    return rows.map(hydrate)
  }

  /** Cluster(s) contenant un fait donné (via la jointure). */
  clustersForFact(factId: string): Cluster[] {
    const rows = this.db
      .prepare(
        `SELECT fc.* FROM cluster_members cm JOIN fact_clusters fc ON fc.id = cm.cluster_id
         WHERE cm.fact_id = ? ORDER BY fc.size DESC`,
      )
      .all(factId) as ClusterRow[]
    return rows.map(hydrate)
  }

  /** Lecture d'un cluster par id (hydraté), ou null. */
  getCluster(clusterId: string): Cluster | null {
    const row = this.db.prepare('SELECT * FROM fact_clusters WHERE id = ?').get(clusterId) as ClusterRow | undefined
    return row ? hydrate(row) : null
  }

  /**
   * Réaction à l'oubli/suppression de faits (hard-delete §11 — `cluster_members`
   * est cité dans la liste d'effacement). Retire les faits des clusters, recompte
   * la taille, et SUPPRIME un cluster qui retombe sous minSize. Retourne
   * {updated, removed}.
   */
  onForget(factIds: string[], opts: { minSize?: number } = {}): { updated: number; removed: number } {
    if (factIds.length === 0) return { updated: 0, removed: 0 }
    const minSize = Math.max(2, opts.minSize ?? DEFAULT_MIN_SIZE)
    const forget = new Set(factIds)
    let updated = 0
    let removed = 0

    const tx = this.db.transaction(() => {
      const rows = this.db.prepare('SELECT * FROM fact_clusters').all() as ClusterRow[]
      for (const row of rows) {
        const members = fromJsonArray(row.member_fact_ids)
        const kept = members.filter(id => !forget.has(id))
        if (kept.length === members.length) continue // aucun membre concerné
        // Retire les liens de jointure des faits oubliés.
        const placeholders = factIds.map(() => '?').join(',')
        this.db
          .prepare(`DELETE FROM cluster_members WHERE cluster_id = ? AND fact_id IN (${placeholders})`)
          .run(row.id, ...factIds)
        if (kept.length < minSize) {
          this.db.prepare('DELETE FROM fact_clusters WHERE id = ?').run(row.id)
          removed++
          continue
        }
        this.db
          .prepare('UPDATE fact_clusters SET member_fact_ids = ?, size = ?, updated_at = ? WHERE id = ?')
          .run(toJson(kept), kept.length, nowISO(), row.id)
        updated++
      }
    })
    tx()
    return { updated, removed }
  }

  /** Statistiques diagnostic (nb clusters, taille moyenne, faits couverts). */
  stats(): { clusters: number; facts: number; avgSize: number } {
    const r = this.db
      .prepare('SELECT COUNT(*) AS c, COALESCE(SUM(size),0) AS s, COALESCE(AVG(size),0) AS a FROM fact_clusters')
      .get() as { c: number; s: number; a: number }
    return { clusters: r.c, facts: r.s, avgSize: r.a }
  }

  // --- interne -------------------------------------------------------------

  /**
   * Charge les faits ACTIFS en nœuds : signature = entités du graphe (préfixées
   * `e:` pour ne pas collisionner avec les keywords) ∪ keywords du texte. Si la
   * couche graph n'a pas tourné, on retombe sur les keywords seuls (le cluster
   * se forme quand même).
   */
  private loadNodes(): Node[] {
    const facts = this.db
      .prepare(`SELECT id, fact FROM facts WHERE superseded = 0 AND lifecycle_state = 'active'`)
      .all() as Array<{ id: string; fact: string }>
    const entStmt = this.db.prepare('SELECT entity_id FROM fact_entities WHERE fact_id = ?')

    const out: Node[] = []
    for (const f of facts) {
      const keywords = clusterKeywords(f.fact)
      const sig = new Set<string>(keywords)
      const ents = entStmt.all(f.id) as Array<{ entity_id: string }>
      for (const e of ents) sig.add(`e:${e.entity_id}`)
      if (sig.size === 0) continue // fait sans contenu structurel exploitable
      out.push({ id: f.id, signature: sig, keywords })
    }
    return out
  }
}

// ---------------------------------------------------------------------------
// Heuristiques pures (testables isolément, 0 LLM, 0 réseau)
// ---------------------------------------------------------------------------

/**
 * Force de lien structurel entre 2 nœuds : Jaccard pondéré de leurs signatures.
 * Les entités partagées (tokens préfixés `e:`) PÈSENT PLUS que les keywords —
 * c'est le principe « entité-first » du fact-cluster : partager une entité forte
 * (un client, un projet) rapproche bien plus que partager un mot courant. Chaque
 * élément partagé compte ENTITY_WEIGHT s'il est une entité, 1 sinon.
 */
const ENTITY_WEIGHT = 3
function tokenWeight(t: string): number {
  return t.startsWith('e:') ? ENTITY_WEIGHT : 1
}

export function linkStrength(a: Set<string>, b: Set<string>): number {
  if (a.size === 0 || b.size === 0) return 0
  const [small, large] = a.size <= b.size ? [a, b] : [b, a]
  let interW = 0
  for (const t of small) if (large.has(t)) interW += tokenWeight(t)
  // Union pondérée = somme des poids de A + B - intersection pondérée.
  let weightA = 0
  for (const t of a) weightA += tokenWeight(t)
  let weightB = 0
  for (const t of b) weightB += tokenWeight(t)
  const unionW = weightA + weightB - interW
  return unionW === 0 ? 0 : interW / unionW
}

/**
 * Composantes connexes du graphe de proximité : deux faits sont reliés si leur
 * force de lien dépasse le seuil. Déterministe (ordre d'insertion préservé) :
 * chaque nœud non assigné démarre un paquet et absorbe transitivement ses
 * voisins.
 */
function connectedComponents(nodes: Node[], threshold: number): Node[][] {
  const assigned = new Set<string>()
  const groups: Node[][] = []
  for (const seed of nodes) {
    if (assigned.has(seed.id)) continue
    const group: Node[] = [seed]
    assigned.add(seed.id)
    let grew = true
    while (grew) {
      grew = false
      for (const cand of nodes) {
        if (assigned.has(cand.id)) continue
        if (group.some(m => linkStrength(m.signature, cand.signature) >= threshold)) {
          group.push(cand)
          assigned.add(cand.id)
          grew = true
        }
      }
    }
    groups.push(group)
  }
  return groups
}

/** Keywords du centroïde : les plus fréquents parmi les membres du paquet. */
function centroidKeywords(group: Node[]): string[] {
  const freq = new Map<string, number>()
  for (const n of group) for (const k of n.keywords) freq.set(k, (freq.get(k) ?? 0) + 1)
  return [...freq.entries()]
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .slice(0, MAX_CENTROID_KEYWORDS)
    .map(([k]) => k)
}

/** Label heuristique : 2-3 keywords dominants du centroïde, sinon repli sur la taille. */
function labelFor(centroid: string[], size: number): string {
  if (centroid.length > 0) return centroid.slice(0, 3).join(' ')
  return `cluster (${size} faits)`
}

function hydrate(row: ClusterRow): Cluster {
  return {
    ...row,
    member_fact_ids: fromJsonArray(row.member_fact_ids),
    centroid_keywords: fromJsonArray(row.centroid_keywords),
  }
}
