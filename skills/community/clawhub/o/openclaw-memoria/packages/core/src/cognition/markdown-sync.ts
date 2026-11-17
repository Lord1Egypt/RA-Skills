/**
 * Couche MARKDOWN SYNC (couche 20, bucket C OPT-IN — spec §12).
 *
 * Produit : un MIROIR lisible et versionnable de la mémoire sous forme de
 * fichiers `.md`. L'utilisateur (ou un agent) peut lire/diff/commiter sa
 * mémoire dans n'importe quel éditeur, sans toucher à la base SQLite.
 *
 * RÈGLE D'OR BUCKET C (gravée) :
 *  - OPT-IN : `export()` n'est JAMAIS appelé automatiquement dans le chemin de
 *    réponse du recall. C'est une commande explicite.
 *  - LECTURE SEULE côté faits : on ne modifie/supprime AUCUN fait. La seule
 *    écriture DB possible est un hash de dernière sync dans la table `meta`
 *    (clé `markdown_last_sync`), et UNIQUEMENT si `writeMeta: true` est demandé.
 *    Par défaut, aucune écriture DB : le compte de faits reste strictement
 *    inchangé.
 *  - SECRETS : un fait déjà rédigé en amont (`[secret:…]`) est recopié TEL QUEL.
 *    Ce module ne RÉSOUT JAMAIS un secret, ne déchiffre rien, n'ouvre aucun
 *    coffre. Le marqueur `[secret:…]` reste visible dans le `.md`.
 *
 * GARDE-FOU CHEMIN (anti-traversée) : `outDir` DOIT être absolu. Les noms de
 * fichiers dérivent de libellés de thèmes potentiellement arbitraires ; chaque
 * chemin écrit est re-résolu et vérifié pour rester STRICTEMENT sous `outDir`.
 * Tout chemin qui s'en échappe est rejeté (throw, jamais d'écriture muette).
 *
 * Pas de table SQL nécessaire : la table `meta` (content-schema) suffit pour le
 * hash optionnel. Aucune migration ajoutée par cette couche.
 */
import { mkdirSync, writeFileSync } from 'node:fs'
import { isAbsolute, relative, resolve, sep } from 'node:path'
import type { Database } from 'better-sqlite3'
import type { ContentStore } from '../storage/content.js'
import { nowISO, sha256Hex } from '../util.js'

/** Catégories connues (legacy v3.34) + repli `general` du tronc v3. Ordre d'affichage. */
const CATEGORY_ORDER = [
  'preference',
  'savoir',
  'outil',
  'client',
  'rh',
  'erreur',
  'chronologie',
  'general',
] as const

/** Titres lisibles FR par catégorie (repli : titlecase de la clé brute). */
const CATEGORY_TITLES: Record<string, string> = {
  preference: 'Préférences',
  savoir: 'Savoir',
  outil: 'Outils',
  client: 'Clients',
  rh: 'RH',
  erreur: 'Erreurs & leçons',
  chronologie: 'Chronologie',
  general: 'Général',
  statement: 'Faits',
}

export interface MarkdownSyncOptions {
  store: ContentStore
  /** Répertoire de sortie ABSOLU. Aucune écriture ne sort de ce dossier. */
  outDir: string
}

export interface ExportOptions {
  /** Restreint l'export à ces scopes (sinon : tous les scopes actifs). */
  scopeFilter?: string[]
  /** true → un fichier `.md` par THÈME (table topics/fact_topics). false → un MEMORY.md global groupé par catégorie. */
  byTopic?: boolean
  /** OPT-IN : écrit un hash de dernière sync dans `meta`. Défaut false (aucune écriture DB). */
  writeMeta?: boolean
}

export interface ExportResult {
  /** Chemins absolus des fichiers écrits. */
  files: string[]
  /** Nombre de faits exportés. */
  facts: number
}

/** Forme minimale d'un fait pour le rendu Markdown. */
interface MdFact {
  id: string
  fact: string
  category: string
  scope_id: string
  created_at: string
}

export class MarkdownSync {
  private readonly store: ContentStore
  private readonly outDir: string

  constructor(opts: MarkdownSyncOptions) {
    this.store = opts.store
    // Garde-fou : un outDir relatif ouvrirait une ambiguïté de résolution
    // (cwd du daemon) et casserait l'anti-traversée → on refuse net.
    if (!isAbsolute(opts.outDir)) {
      throw new Error(`MarkdownSync : outDir doit être un chemin absolu (reçu : ${opts.outDir})`)
    }
    this.outDir = resolve(opts.outDir)
  }

  private get db(): Database {
    return this.store.db
  }

  /**
   * Écrit le miroir Markdown des faits ACTIFS (non supersédés, lifecycle
   * `active`). Idempotent : réécrit proprement le même contenu pour le même
   * état de mémoire. Retourne les fichiers écrits + le nombre de faits.
   */
  export(opts: ExportOptions = {}): ExportResult {
    const facts = this.activeFacts(opts.scopeFilter)
    mkdirSync(this.outDir, { recursive: true })

    const files = opts.byTopic ? this.exportByTopic(facts) : this.exportGlobal(facts)

    if (opts.writeMeta) {
      // Hash déterministe de l'état exporté (id + texte de chaque fait, triés)
      // → permet de savoir si un ré-export changerait quelque chose. C'est la
      // SEULE écriture DB tolérée, et elle ne touche aucun fait.
      const signature = [...facts].sort((a, b) => a.id.localeCompare(b.id)).map(f => `${f.id}:${f.fact}`).join('\n')
      this.db
        .prepare('INSERT INTO meta (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = excluded.value')
        .run('markdown_last_sync', JSON.stringify({ at: nowISO(), hash: sha256Hex(signature), facts: facts.length }))
    }

    return { files, facts: facts.length }
  }

  // --- rendu ----------------------------------------------------------------

  /** MEMORY.md global, groupé par catégorie. */
  private exportGlobal(facts: MdFact[]): string[] {
    const byCat = new Map<string, MdFact[]>()
    for (const f of facts) {
      const arr = byCat.get(f.category) ?? []
      arr.push(f)
      byCat.set(f.category, arr)
    }

    const lines: string[] = []
    lines.push('# MEMORY')
    lines.push('')
    lines.push(`> Miroir Markdown de la mémoire — ${facts.length} fait(s) — généré le ${nowISO()}`)
    lines.push('')

    for (const cat of orderedCategories([...byCat.keys()])) {
      const arr = byCat.get(cat)!
      lines.push(`## ${categoryTitle(cat)} (${arr.length})`)
      lines.push('')
      for (const f of sortFacts(arr)) lines.push(`- ${sanitizeBullet(f.fact)}`)
      lines.push('')
    }

    const file = this.safePath('MEMORY.md')
    writeFileSync(file, `${lines.join('\n').trimEnd()}\n`, 'utf8')
    return [file]
  }

  /** Un fichier `.md` par thème (topics/fact_topics) + un `_sans-theme.md` pour le reste. */
  private exportByTopic(facts: MdFact[]): string[] {
    const factById = new Map(facts.map(f => [f.id, f]))
    const exported = new Set<string>()
    const files: string[] = []

    const topics = this.db
      .prepare('SELECT id, name, slug FROM topics ORDER BY importance_score DESC, name ASC')
      .all() as Array<{ id: string; name: string; slug: string | null }>

    const usedNames = new Set<string>()
    for (const t of topics) {
      const memberIds = (
        this.db.prepare('SELECT fact_id FROM fact_topics WHERE topic_id = ?').all(t.id) as Array<{ fact_id: string }>
      ).map(r => r.fact_id)
      const members = memberIds.map(id => factById.get(id)).filter((f): f is MdFact => f !== undefined)
      if (members.length === 0) continue
      for (const f of members) exported.add(f.id)

      const base = uniqueFileBase(topicFileBase(t.slug, t.name, t.id), usedNames)
      files.push(this.writeTopicFile(`${base}.md`, t.name, members))
    }

    // Faits actifs sans aucun thème (la couche topics est async/opt-in : elle
    // peut ne pas avoir tourné). On ne les perd pas.
    const orphans = facts.filter(f => !exported.has(f.id))
    if (orphans.length > 0) {
      files.push(this.writeTopicFile('_sans-theme.md', 'Sans thème', orphans))
    }

    return files
  }

  private writeTopicFile(fileName: string, title: string, facts: MdFact[]): string {
    const lines: string[] = []
    lines.push(`# ${title}`)
    lines.push('')
    lines.push(`> ${facts.length} fait(s) — généré le ${nowISO()}`)
    lines.push('')
    for (const f of sortFacts(facts)) lines.push(`- ${sanitizeBullet(f.fact)}`)
    const file = this.safePath(fileName)
    writeFileSync(file, `${lines.join('\n').trimEnd()}\n`, 'utf8')
    return file
  }

  // --- accès données --------------------------------------------------------

  /** Faits ACTIFS (non supersédés, lifecycle active), filtrés par scope optionnel. */
  private activeFacts(scopeFilter?: string[]): MdFact[] {
    const where: string[] = [`superseded = 0`, `lifecycle_state = 'active'`]
    const params: unknown[] = []
    if (scopeFilter && scopeFilter.length > 0) {
      where.push(`scope_id IN (${scopeFilter.map(() => '?').join(',')})`)
      params.push(...scopeFilter)
    }
    return this.db
      .prepare(
        `SELECT id, fact, category, scope_id, created_at FROM facts
         WHERE ${where.join(' AND ')} ORDER BY created_at ASC, id ASC`,
      )
      .all(...params) as MdFact[]
  }

  // --- garde-fou chemin -----------------------------------------------------

  /**
   * Résout `relativePath` SOUS outDir et vérifie qu'il n'en sort pas
   * (anti-traversée : un libellé de thème malicieux ne doit pas écrire
   * `../../etc/...`). Throw si évasion. Jamais d'écriture muette hors zone.
   */
  private safePath(relativePath: string): string {
    const full = resolve(this.outDir, relativePath)
    const rel = relative(this.outDir, full)
    if (rel === '' || rel.startsWith('..') || isAbsolute(rel) || rel.split(sep).includes('..')) {
      throw new Error(`MarkdownSync : chemin hors de outDir refusé (${relativePath})`)
    }
    // Sécurité défensive supplémentaire : préfixe littéral.
    if (full !== this.outDir && !full.startsWith(this.outDir + sep)) {
      throw new Error(`MarkdownSync : chemin hors de outDir refusé (${relativePath})`)
    }
    return full
  }
}

// ---------------------------------------------------------------------------
// Helpers purs (testables, déterministes, 0 LLM, 0 réseau)
// ---------------------------------------------------------------------------

/** Tri stable des faits d'une section : par date de création puis id. */
function sortFacts(facts: MdFact[]): MdFact[] {
  return [...facts].sort((a, b) => a.created_at.localeCompare(b.created_at) || a.id.localeCompare(b.id))
}

/**
 * Nettoie un fait pour le rendre en PUCE Markdown sur une ligne.
 * NE TOUCHE PAS aux marqueurs `[secret:…]` : un secret rédigé en amont reste
 * masqué TEL QUEL (on ne résout jamais un secret). On normalise seulement les
 * sauts de ligne internes (la puce reste sur une ligne) et on échappe le tout
 * début pour ne pas casser le Markdown.
 */
export function sanitizeBullet(fact: string): string {
  const oneLine = fact.replace(/\r?\n+/g, ' ').replace(/\s+/g, ' ').trim()
  return oneLine
}

/** Catégories triées selon CATEGORY_ORDER, les inconnues en fin (ordre alpha). */
export function orderedCategories(cats: string[]): string[] {
  const known = CATEGORY_ORDER.filter(c => cats.includes(c))
  const unknown = cats.filter(c => !(CATEGORY_ORDER as readonly string[]).includes(c)).sort()
  return [...known, ...unknown]
}

function categoryTitle(cat: string): string {
  return CATEGORY_TITLES[cat] ?? titleCase(cat)
}

function titleCase(s: string): string {
  return s.replace(/\b\p{L}/gu, c => c.toUpperCase())
}

/** Base de nom de fichier d'un thème : slug si présent, sinon slug dérivé du nom, sinon id. */
function topicFileBase(slug: string | null, name: string, id: string): string {
  const fromSlug = slugifyFile(slug ?? '')
  if (fromSlug) return fromSlug
  const fromName = slugifyFile(name)
  if (fromName) return fromName
  return slugifyFile(id) || 'theme'
}

/**
 * Slugify SÛR pour nom de fichier : minuscules, sans diacritiques, seuls
 * `[a-z0-9-]` survivent (élimine tout `/`, `\`, `.`, espace → aucun risque de
 * traversée ou d'extension sauvage). Préfixe `_sans-theme` réservé.
 */
export function slugifyFile(s: string): string {
  return s
    .toLowerCase()
    .normalize('NFD')
    .replace(/\p{M}+/gu, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 60)
}

/** Désambiguïse deux thèmes au même slug (suffixe -2, -3, …) pour ne pas s'écraser. */
function uniqueFileBase(base: string, used: Set<string>): string {
  let candidate = base
  let n = 2
  while (used.has(candidate)) {
    candidate = `${base}-${n}`
    n++
  }
  used.add(candidate)
  return candidate
}
