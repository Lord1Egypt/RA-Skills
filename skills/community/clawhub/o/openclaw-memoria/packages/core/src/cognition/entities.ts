/**
 * Extraction d'entités d'un fait (couche graphe, bucket B async).
 *
 * Deux voies, par ordre de préférence :
 *  1. LLM injecté (optionnel) — qualité maximale, JSON {entities, relations} ;
 *  2. heuristique pure (défaut, ZÉRO réseau) — noms propres capitalisés FR/EN
 *     + termes techniques (CamelCase, identifiants à point/tiret, ALLCAPS).
 *
 * Le portage conserve la sémantique legacy (graph.ts) : types stricts
 * normalisés, dédup par nom NOCASE, cap d'entités par fait. La nouveauté V3 :
 * l'heuristique permet de peupler le graphe SANS LLM (le LLM n'est plus
 * obligatoire), et l'upsert d'entité passe par la table dédiée + index unique.
 */
import type { Database } from 'better-sqlite3'
import type { LlmProvider } from '../llm/provider.js'
import { newId, nowISO } from '../util.js'

/** Types d'entités valides (inchangés depuis le legacy graph.ts). */
export const ENTITY_TYPES = ['person', 'project', 'tool', 'concept', 'place', 'company'] as const
export type EntityType = (typeof ENTITY_TYPES)[number]

/** Types de relations valides (inchangés depuis le legacy graph.ts). */
export const RELATION_TYPES = [
  'uses',
  'part_of',
  'works_on',
  'manages',
  'created_by',
  'depends_on',
  'deployed_on',
  'related_to',
] as const
export type RelationType = (typeof RELATION_TYPES)[number]

export interface ExtractedEntity {
  name: string
  type: EntityType
}

export interface ExtractedRelation {
  from: string
  to: string
  type: RelationType
}

export interface Extraction {
  entities: ExtractedEntity[]
  relations: ExtractedRelation[]
}

export interface EntityRow {
  id: string
  name: string
  type: string
  mention_count: number
  created_at: string
}

const MAX_ENTITIES_PER_FACT = 5
const MAX_RELATIONS_PER_FACT = 3

export function normalizeEntityType(type: string): EntityType {
  const lower = (type || '').toLowerCase().trim()
  return (ENTITY_TYPES as readonly string[]).includes(lower) ? (lower as EntityType) : 'concept'
}

export function normalizeRelationType(type: string): RelationType {
  const lower = (type || '').toLowerCase().trim()
  return (RELATION_TYPES as readonly string[]).includes(lower) ? (lower as RelationType) : 'related_to'
}

// Mots-outils FR/EN en tête de phrase : capitalisés par la ponctuation, PAS des
// entités. Filtre pour éviter « Le », « The », « La »… comme noms propres.
const STOPWORDS_LEADING = new Set([
  'le',
  'la',
  'les',
  'un',
  'une',
  'des',
  'de',
  'du',
  'ce',
  'cette',
  'ces',
  'mon',
  'ma',
  'mes',
  'son',
  'sa',
  'ses',
  'il',
  'elle',
  'on',
  'nous',
  'vous',
  'ils',
  'elles',
  'the',
  'a',
  'an',
  'this',
  'that',
  'these',
  'those',
  'it',
  'he',
  'she',
  'they',
  'we',
  'you',
  'my',
  'his',
  'her',
  'their',
  'our',
  'your',
])

/**
 * Heuristique d'extraction — PAS de LLM. Détecte :
 *  - les noms propres capitalisés (y compris séquences « Mac Studio ») ;
 *  - les termes techniques : CamelCase (PixConsent), identifiants à point/tiret
 *    (fr.primo-studio.igara, qwen2.5:3b), ALLCAPS (NAS, QNAP).
 * Aucune relation typée inférée (sans LLM, on ne devine pas la sémantique) —
 * les relations naissent de la CO-OCCURRENCE dans le graphe (graph.ts).
 */
export function heuristicEntities(text: string): ExtractedEntity[] {
  const found = new Map<string, ExtractedEntity>()
  const push = (name: string, type: EntityType) => {
    const trimmed = name.trim()
    if (trimmed.length < 2) return
    const key = trimmed.toLowerCase()
    if (!found.has(key)) found.set(key, { name: trimmed, type })
  }

  // 1. Termes techniques : identifiants à point/tiret/deux-points, CamelCase, ALLCAPS.
  const technical = text.match(/\b[A-Za-z][\w-]*(?:[.:][\w-]+)+\b/g) ?? []
  for (const t of technical) push(t, 'tool')

  const camel = text.match(/\b[A-Z][a-z]+[A-Z][A-Za-z]*\b/g) ?? []
  for (const c of camel) push(c, 'tool')

  const allcaps = text.match(/\b[A-Z]{2,}\b/g) ?? []
  for (const a of allcaps) push(a, 'concept')

  // 2. Noms propres capitalisés (et séquences capitalisées « Mac Studio »).
  //    \p{Lu}\p{Ll}+ = une Majuscule suivie de minuscules (Unicode → accents FR).
  const proper = text.match(/\b\p{Lu}\p{Ll}+(?:\s+\p{Lu}\p{Ll}+)*\b/gu) ?? []
  for (const p of proper) {
    // Rejette les mots-outils capitalisés par la ponctuation de début de phrase.
    const firstWord = p.split(/\s+/)[0]!.toLowerCase()
    if (STOPWORDS_LEADING.has(firstWord) && !p.includes(' ')) continue
    // Si séquence multi-mots dont le 1er est un stopword, on retire le stopword.
    let name = p
    if (STOPWORDS_LEADING.has(firstWord) && p.includes(' ')) {
      name = p.slice(p.indexOf(' ') + 1)
    }
    push(name, 'concept')
  }

  return [...found.values()].slice(0, MAX_ENTITIES_PER_FACT)
}

/**
 * Extraction par LLM (optionnelle). Prompt aligné sur le legacy (graph.ts) :
 * entités typées + relations typées. Échec / indisponible → null (l'appelant
 * retombe sur l'heuristique). Aucune erreur avalée en silence : le throw est
 * relancé à l'appelant qui décide (retry / fallback).
 */
const LLM_EXTRACT_SYSTEM = `Tu extrais les entités et relations d'un fait, pour un graphe de connaissances.
Réponds UNIQUEMENT en JSON, sans texte autour :
{"entities":[{"name":"NomExact","type":"person|project|tool|concept|place|company"}],
 "relations":[{"from":"NomExact1","to":"NomExact2","type":"uses|part_of|works_on|manages|created_by|depends_on|deployed_on|related_to"}]}
Règles : noms propres exacts ; types stricts ; relations les plus importantes (max 3) ;
rien d'intéressant → {"entities":[],"relations":[]}.`

export async function llmExtract(llm: LlmProvider, factText: string): Promise<Extraction | null> {
  if (!(await llm.isAvailable())) return null
  const raw = await llm.complete({
    system: LLM_EXTRACT_SYSTEM,
    prompt: `Fait : "${factText}"\n\nJSON {"entities":[...],"relations":[...]} :`,
    json: true,
    maxTokens: 512,
    temperature: 0.1,
  })
  return parseExtraction(raw)
}

/** Parse robuste de la sortie LLM (objet ou bloc JSON noyé dans du texte). */
export function parseExtraction(raw: string): Extraction {
  let parsed: unknown
  try {
    parsed = JSON.parse(raw)
  } catch {
    const start = raw.indexOf('{')
    const end = raw.lastIndexOf('}')
    if (start === -1 || end <= start) {
      throw new Error(`extraction graphe LLM sans JSON : « ${excerpt(raw)} »`)
    }
    try {
      parsed = JSON.parse(raw.slice(start, end + 1))
    } catch {
      throw new Error(`extraction graphe LLM illisible : « ${excerpt(raw.slice(start, end + 1))} »`)
    }
  }
  if (parsed === null || typeof parsed !== 'object' || Array.isArray(parsed)) {
    throw new Error(`extraction graphe LLM : objet attendu, reçu ${Array.isArray(parsed) ? 'array' : typeof parsed}`)
  }
  const record = parsed as Record<string, unknown>
  const entities: ExtractedEntity[] = []
  for (const e of Array.isArray(record.entities) ? record.entities : []) {
    if (typeof e !== 'object' || e === null) continue
    const name = typeof (e as Record<string, unknown>).name === 'string' ? ((e as Record<string, unknown>).name as string).trim() : ''
    if (name.length < 2) continue
    entities.push({ name, type: normalizeEntityType(String((e as Record<string, unknown>).type ?? '')) })
  }
  const relations: ExtractedRelation[] = []
  for (const r of Array.isArray(record.relations) ? record.relations : []) {
    if (typeof r !== 'object' || r === null) continue
    const rec = r as Record<string, unknown>
    const from = typeof rec.from === 'string' ? rec.from.trim() : ''
    const to = typeof rec.to === 'string' ? rec.to.trim() : ''
    if (from.length < 2 || to.length < 2) continue
    relations.push({ from, to, type: normalizeRelationType(String(rec.type ?? '')) })
  }
  return {
    entities: entities.slice(0, MAX_ENTITIES_PER_FACT),
    relations: relations.slice(0, MAX_RELATIONS_PER_FACT),
  }
}

/**
 * Upsert d'une entité par nom (dédup NOCASE via l'index unique). Retourne son
 * id ; incrémente mention_count à chaque (ré)apparition. Idempotent sur l'id :
 * deux extractions du même nom → 1 seule ligne.
 */
export function upsertEntity(db: Database, name: string, type: EntityType): string {
  const normalized = name.trim()
  const existing = db.prepare('SELECT id FROM entities WHERE name = ? COLLATE NOCASE').get(normalized) as
    | { id: string }
    | undefined
  if (existing) {
    db.prepare('UPDATE entities SET mention_count = mention_count + 1 WHERE id = ?').run(existing.id)
    return existing.id
  }
  const id = newId()
  db.prepare(
    'INSERT INTO entities (id, name, type, mention_count, created_at) VALUES (?, ?, ?, 1, ?)',
  ).run(id, normalized, type, nowISO())
  return id
}

function excerpt(text: string, max = 120): string {
  const flat = text.replaceAll('\n', ' ')
  return flat.length > max ? `${flat.slice(0, max)}…` : flat
}
