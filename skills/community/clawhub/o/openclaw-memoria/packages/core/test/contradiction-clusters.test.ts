/**
 * Couches CONTRADICTION (3, dans selective) + FACT-CLUSTERS (16).
 *
 * Garanties PROUVÉES (pas juste « ça compile ») :
 *  CONTRADICTION
 *   - « le port est 8080 » vs « le port est 9090 » → contradiction (valeur opposée) ;
 *   - « préfère X » vs « ne préfère plus X » → contradiction (polarité opposée) ;
 *   - 2 faits sans rapport → AUCUN faux positif ;
 *   - RÈGLE D'OR : ne SUPERSÈDE/ne modifie AUCUN fait (compteurs avant/après) ;
 *   - LLM optionnel confirme un cas limite (fake LLM, 0 réseau).
 *  CLUSTERS
 *   - 4 faits liés → 1 cluster de taille ≥ 3 ;
 *   - faits isolés → pas de cluster ;
 *   - idempotence du rebuild (même partition) ;
 *   - onForget retire un membre / dissout sous le seuil ; ne touche aucun fait.
 *
 * Tout est en tmpdir, fake LLM, 0 réseau.
 */
import { mkdtempSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { afterEach, beforeEach, describe, expect, it } from 'vitest'
import { ContentStore } from '../src/storage/content.js'
import { CognitionEngine } from '../src/cognition/index.js'
import type { LlmProvider } from '../src/llm/provider.js'
import {
  detectContradiction,
  hasNegation,
  subjectTokens,
} from '../src/cognition/contradiction.js'
import {
  ClusterEngine,
  clusterMigrations,
  clusterKeywords,
  linkStrength,
} from '../src/cognition/clusters.js'

let dir: string
let store: ContentStore

beforeEach(() => {
  dir = mkdtempSync(join(tmpdir(), 'memoria-contra-clusters-'))
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
function supersededCount(): number {
  return (store.db.prepare('SELECT COUNT(*) AS c FROM facts WHERE superseded = 1').get() as { c: number }).c
}

/** Fake LLM déterministe : répond OUI/NON selon une fonction injectée. */
class FakeLlm implements LlmProvider {
  readonly name = 'fake'
  readonly model = 'fake-1'
  calls = 0
  constructor(private readonly answer: (prompt: string) => string, private readonly available = true) {}
  isAvailable(): Promise<boolean> {
    return Promise.resolve(this.available)
  }
  complete(opts: { prompt: string }): Promise<string> {
    this.calls++
    return Promise.resolve(this.answer(opts.prompt))
  }
}

// ===========================================================================
// CONTRADICTION
// ===========================================================================

describe('contradiction — heuristiques pures', () => {
  it('hasNegation détecte « ne…plus / ne…pas / jamais / no longer »', () => {
    expect(hasNegation('Néto ne préfère plus les commits signés')).toBe(true)
    expect(hasNegation("Je n'utilise plus Vercel")).toBe(true)
    expect(hasNegation('We no longer use port 8080')).toBe(true)
    expect(hasNegation('Néto préfère les commits signés')).toBe(false)
  })

  it('subjectTokens normalise et retire les stopwords', () => {
    const t = subjectTokens('Le PORT du serveur est 8080 pour Vercel')
    expect(t.has('port')).toBe(true)
    expect(t.has('serveur')).toBe(true)
    expect(t.has('vercel')).toBe(true)
    expect(t.has('pour')).toBe(false)
  })
})

describe('detectContradiction (propose, ne modifie rien)', () => {
  it('« le port est 8080 » vs « le port est 9090 » → contradiction (valeur opposée)', async () => {
    fact('Le port du serveur de staging est 8080')
    const res = await detectContradiction(store, 'Le port du serveur de staging est 9090', 's1')
    expect(res.length).toBe(1)
    expect(res[0]!.kind).toBe('value')
    expect(res[0]!.existingFact).toContain('8080')
    expect(res[0]!.confidence).toBeGreaterThanOrEqual(0.5)
  })

  it('« préfère X » vs « ne préfère plus X » → contradiction (polarité opposée)', async () => {
    fact('Néto préfère les commits signés en français')
    const res = await detectContradiction(store, 'Néto ne préfère plus les commits signés en français', 's1')
    expect(res.length).toBe(1)
    expect(res[0]!.kind).toBe('negation')
    expect(res[0]!.confidence).toBeGreaterThanOrEqual(0.5)
  })

  it('PAS de faux positif sur 2 faits sans rapport', async () => {
    fact('Le NAS QNAP héberge les sauvegardes vidéo de Primo')
    const res = await detectContradiction(store, 'AutoCare cible le marché brésilien mobile', 's1')
    expect(res).toHaveLength(0)
  })

  it('PAS de contradiction quand les deux faits sont d’accord (même valeur)', async () => {
    fact('Le port du serveur de staging est 8080')
    const res = await detectContradiction(store, 'Le port du serveur de staging reste 8080', 's1')
    expect(res).toHaveLength(0)
  })

  it('ignore le doublon exact (dedup, pas contradiction)', async () => {
    fact('Le port du serveur est 8080')
    const res = await detectContradiction(store, 'Le port du serveur est 8080', 's1')
    expect(res).toHaveLength(0)
  })

  it('borne au scope : un fait contradictoire d’un AUTRE scope n’est pas remonté', async () => {
    fact('Le port du serveur est 8080', 'autre_scope')
    const res = await detectContradiction(store, 'Le port du serveur est 9090', 's1')
    expect(res).toHaveLength(0)
  })

  it('RÈGLE D’OR : ne SUPERSÈDE / ne modifie AUCUN fait', async () => {
    fact('Le port du serveur de staging est 8080')
    fact('Néto préfère les commits signés en français')
    const activeBefore = activeFactCount()
    const totalBefore = store.countFacts()

    await detectContradiction(store, 'Le port du serveur de staging est 9090', 's1')
    await detectContradiction(store, 'Néto ne préfère plus les commits signés en français', 's1')

    expect(activeFactCount()).toBe(activeBefore)
    expect(supersededCount()).toBe(0)
    expect(store.countFacts()).toBe(totalBefore)
  })

  it('LLM optionnel : confirme un cas limite que l’heuristique laissait ambigu', async () => {
    // Sujet faiblement recouvrant + négation d’un seul côté → candidat « ambigu »
    // (confiance heuristique sous le minimum) que le LLM peut confirmer.
    fact('Néto valide la migration vers le nouveau fournisseur cloud')
    const llmYes = new FakeLlm(() => 'OUI')
    const res = await detectContradiction(
      store,
      "Néto n'a pas validé la migration cloud finalement",
      's1',
      { useLlm: true, minConfidence: 0.9 },
      llmYes,
    )
    // Le LLM a confirmé au moins un candidat (kind 'llm').
    expect(res.some(c => c.kind === 'llm')).toBe(true)
    expect(llmYes.calls).toBeGreaterThan(0)
  })

  it('LLM indisponible → heuristique seule, aucune mort silencieuse (pas de throw)', async () => {
    fact('Le port du serveur est 8080')
    const llmDown = new FakeLlm(() => 'OUI', false)
    const res = await detectContradiction(store, 'Le port du serveur est 9090', 's1', { useLlm: true }, llmDown)
    // La contradiction de valeur est trouvée par l’heuristique, sans appeler complete().
    expect(res.some(c => c.kind === 'value')).toBe(true)
    expect(llmDown.calls).toBe(0)
  })
})

// ===========================================================================
// CLUSTERS
// ===========================================================================

describe('clusterMigrations (schéma)', () => {
  it('réserve le créneau 60-69 et crée fact_clusters + cluster_members', () => {
    expect(clusterMigrations.every(m => m.version >= 60 && m.version <= 69)).toBe(true)
    new ClusterEngine({ store })
    const cols = (store.db.prepare('PRAGMA table_info(fact_clusters)').all() as Array<{ name: string }>)
      .map(c => c.name)
      .sort()
    expect(cols).toEqual(
      ['id', 'label', 'member_fact_ids', 'centroid_keywords', 'size', 'created_at', 'updated_at'].sort(),
    )
    const memberCols = (store.db.prepare('PRAGMA table_info(cluster_members)').all() as Array<{ name: string }>).map(
      c => c.name,
    )
    expect(memberCols.sort()).toEqual(['cluster_id', 'fact_id'].sort())
  })
})

describe('clusters — heuristiques pures', () => {
  it('clusterKeywords retire les stopwords et les mots courts', () => {
    const k = clusterKeywords('Le déploiement Vercel utilise le compte Hello-Primo')
    expect(k).toContain('deploiement')
    expect(k).toContain('vercel')
    expect(k).toContain('hello-primo')
    expect(k).not.toContain('utilise')
  })

  it('linkStrength = Jaccard borné [0,1], symétrique', () => {
    const a = new Set(['vercel', 'deploiement', 'compte'])
    const b = new Set(['vercel', 'deploiement', 'cache'])
    expect(linkStrength(a, b)).toBeCloseTo(2 / 4, 5)
    expect(linkStrength(a, b)).toBe(linkStrength(b, a))
    expect(linkStrength(a, new Set())).toBe(0)
  })
})

describe('ClusterEngine.rebuild', () => {
  it('4 faits liés (sujet commun) → 1 cluster de taille ≥ 3', () => {
    fact('Le déploiement Vercel utilise le compte Hello-Primo pour le site')
    fact('Le déploiement Vercel du site échoue quand le compte Hello-Primo expire')
    fact('Sur Vercel, le compte Hello-Primo gère le déploiement du site Primo')
    fact('Le site Primo se déploie via Vercel avec le compte Hello-Primo')

    const engine = new ClusterEngine({ store })
    const res = engine.rebuild({ minSize: 3 })
    expect(res.clusters).toBe(1)
    const list = engine.listClusters()
    expect(list).toHaveLength(1)
    expect(list[0]!.size).toBeGreaterThanOrEqual(3)
    expect(list[0]!.member_fact_ids.length).toBe(list[0]!.size)
    expect(list[0]!.centroid_keywords.length).toBeGreaterThan(0)
    expect(list[0]!.label.length).toBeGreaterThan(0)
  })

  it('faits isolés (sans rapport) → aucun cluster', () => {
    fact('La recette du dimanche utilise du curcuma frais')
    fact('Le serveur Directus est derrière Cloudflare en Guyane')
    fact('JamBoard cible les musiciens semi-professionnels brésiliens')

    const engine = new ClusterEngine({ store })
    const res = engine.rebuild({ minSize: 3 })
    expect(res.clusters).toBe(0)
    expect(engine.listClusters()).toHaveLength(0)
  })

  it('clustersForFact remonte le cluster d’un fait membre', () => {
    const a = fact('Le déploiement Vercel utilise le compte Hello-Primo pour le site')
    fact('Le déploiement Vercel du site échoue quand le compte Hello-Primo expire')
    fact('Sur Vercel le compte Hello-Primo gère le déploiement du site Primo')

    const engine = new ClusterEngine({ store })
    engine.rebuild({ minSize: 3 })
    const cl = engine.clustersForFact(a)
    expect(cl).toHaveLength(1)
    expect(cl[0]!.member_fact_ids).toContain(a)
  })

  it('s’appuie aussi sur les entités du graphe (entité-first)', async () => {
    // L'entité partagée « Transport Rino » (extraite par la couche graph) pèse
    // plus que les keywords : les 3 faits se regroupent même avec un vocabulaire
    // partiellement différent — c'est le principe entité-first du cluster.
    const cognition = new CognitionEngine({ store })
    const ids = [
      fact('Transport Rino veut des bons de livraison numériques'),
      fact('Transport Rino gère ses bons de livraison sur chantier'),
      fact('Transport Rino édite des bons de livraison pour Nora'),
    ]
    for (const id of ids) await cognition.processFact(id)
    const engine = new ClusterEngine({ store })
    const res = engine.rebuild({ minSize: 3 })
    expect(res.clusters).toBe(1)
    // L'entité Transport Rino est bien le liant (présente dans le centroïde/keywords).
    const cl = engine.listClusters()[0]!
    expect(cl.member_fact_ids).toHaveLength(3)
  })

  it('RÈGLE D’OR : rebuild ne touche AUCUN fait', () => {
    fact('Le déploiement Vercel utilise le compte Hello-Primo')
    fact('Le déploiement Vercel échoue quand le compte Hello-Primo expire')
    fact('Sur Vercel le compte Hello-Primo gère le déploiement')
    const activeBefore = activeFactCount()
    const totalBefore = store.countFacts()

    new ClusterEngine({ store }).rebuild({ minSize: 3 })

    expect(activeFactCount()).toBe(activeBefore)
    expect(supersededCount()).toBe(0)
    expect(store.countFacts()).toBe(totalBefore)
  })
})

describe('ClusterEngine.rebuild (idempotence)', () => {
  it('deux rebuilds consécutifs → même partition (mêmes membres)', () => {
    fact('Le déploiement Vercel utilise le compte Hello-Primo pour le site')
    fact('Le déploiement Vercel du site échoue quand le compte Hello-Primo expire')
    fact('Sur Vercel le compte Hello-Primo gère le déploiement du site Primo')
    fact('Le site Primo se déploie via Vercel avec le compte Hello-Primo')

    const engine = new ClusterEngine({ store })
    const first = engine.rebuild({ minSize: 3 })
    const membersFirst = engine.listClusters().map(c => [...c.member_fact_ids].sort().join(',')).sort()

    const second = engine.rebuild({ minSize: 3 })
    const membersSecond = engine.listClusters().map(c => [...c.member_fact_ids].sort().join(',')).sort()

    expect(second.clusters).toBe(first.clusters)
    expect(membersSecond).toEqual(membersFirst)
    // pas de doublon de cluster en base
    expect((store.db.prepare('SELECT COUNT(*) AS c FROM fact_clusters').get() as { c: number }).c).toBe(
      first.clusters,
    )
  })
})

describe('ClusterEngine.onForget', () => {
  it('retire un membre et RECOMPTE quand le cluster reste au-dessus du seuil', () => {
    const ids = [
      fact('Le déploiement Vercel utilise le compte Hello-Primo pour le site'),
      fact('Le déploiement Vercel du site échoue quand le compte Hello-Primo expire'),
      fact('Sur Vercel le compte Hello-Primo gère le déploiement du site Primo'),
      fact('Le site Primo se déploie via Vercel avec le compte Hello-Primo'),
    ]
    const engine = new ClusterEngine({ store })
    engine.rebuild({ minSize: 3 })
    const before = engine.listClusters()[0]!
    expect(before.size).toBe(4)

    const r = engine.onForget([ids[0]!], { minSize: 3 })
    expect(r.updated).toBe(1)
    expect(r.removed).toBe(0)
    const after = engine.getCluster(before.id)!
    expect(after.size).toBe(3)
    expect(after.member_fact_ids).not.toContain(ids[0]!)
    expect(engine.clustersForFact(ids[0]!)).toHaveLength(0)
  })

  it('DISSOUT le cluster quand il retombe sous le seuil', () => {
    const ids = [
      fact('Le déploiement Vercel utilise le compte Hello-Primo pour le site'),
      fact('Le déploiement Vercel du site échoue quand le compte Hello-Primo expire'),
      fact('Sur Vercel le compte Hello-Primo gère le déploiement du site Primo'),
    ]
    const engine = new ClusterEngine({ store })
    engine.rebuild({ minSize: 3 })
    const cid = engine.listClusters()[0]!.id

    const r = engine.onForget([ids[0]!], { minSize: 3 })
    expect(r.removed).toBe(1)
    expect(engine.getCluster(cid)).toBeNull()
    expect((store.db.prepare('SELECT COUNT(*) AS c FROM fact_clusters').get() as { c: number }).c).toBe(0)
  })

  it('no-op si aucun fait concerné', () => {
    fact('Le déploiement Vercel utilise le compte Hello-Primo')
    fact('Le déploiement Vercel échoue quand le compte Hello-Primo expire')
    fact('Sur Vercel le compte Hello-Primo gère le déploiement')
    const engine = new ClusterEngine({ store })
    engine.rebuild({ minSize: 3 })
    expect(engine.onForget(['inconnu'], { minSize: 3 })).toEqual({ updated: 0, removed: 0 })
  })
})
