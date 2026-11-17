/**
 * Couche MARKDOWN SYNC (bucket C opt-in) : miroir lisible des faits en `.md`.
 * Vérifie : MEMORY.md contient les faits ; byTopic → un fichier par thème ;
 * ré-export idempotent (même contenu) ; un `[secret:…]` reste masqué tel quel ;
 * aucune écriture DB par défaut (compte de faits inchangé) ; garde-fous chemin.
 */
import { mkdtempSync, readFileSync, readdirSync, rmSync, existsSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { afterEach, beforeEach, describe, expect, it } from 'vitest'
import { ContentStore } from '../src/storage/content.js'
import { CognitionEngine } from '../src/cognition/index.js'
import { TopicEngine } from '../src/cognition/topics.js'
import { MarkdownSync, slugifyFile, orderedCategories, sanitizeBullet } from '../src/cognition/markdown-sync.js'

let dir: string
let outDir: string
let store: ContentStore
let cognition: CognitionEngine
let topics: TopicEngine

beforeEach(() => {
  dir = mkdtempSync(join(tmpdir(), 'memoria-mdsync-'))
  outDir = join(dir, 'md')
  store = new ContentStore(join(dir, 'c.sqlite'))
  cognition = new CognitionEngine({ store })
  topics = new TopicEngine({ store })
})

afterEach(() => {
  store.close()
  rmSync(dir, { recursive: true, force: true })
})

/** Insère un fait actif (catégorie optionnelle) dans un scope. */
function addFact(text: string, opts: { category?: string; scope?: string } = {}): string {
  const f = store.insertFact({ fact: text, category: opts.category, scope_id: opts.scope ?? 's1' })
  return f.id
}

/** Insère + extrait entités + range dans un topic (comme le pipeline réel). */
async function addWithTopic(text: string, scope = 's1'): Promise<string> {
  const id = addFact(text, { scope })
  await cognition.processFact(id)
  await topics.assignFact(id)
  return id
}

describe('MarkdownSync — export global', () => {
  it('crée un MEMORY.md contenant les faits actifs', () => {
    addFact('Le client Transport Rino utilise des bons de livraison numériques', { category: 'client' })
    addFact('Je préfère le café sans sucre', { category: 'preference' })
    const sync = new MarkdownSync({ store, outDir })

    const res = sync.export()
    expect(res.facts).toBe(2)
    expect(res.files).toHaveLength(1)
    expect(res.files[0]).toBe(join(outDir, 'MEMORY.md'))

    const md = readFileSync(res.files[0]!, 'utf8')
    expect(md).toContain('# MEMORY')
    expect(md).toContain('Transport Rino')
    expect(md).toContain('café sans sucre')
    // groupé par catégorie : titres lisibles présents
    expect(md).toContain('Clients')
    expect(md).toContain('Préférences')
    // chaque fait est une puce
    expect(md).toContain('- Le client Transport Rino utilise des bons de livraison numériques')
  })

  it('exclut les faits supersédés et dormants du miroir', () => {
    const active = addFact('Fait actif et visible', { category: 'savoir' })
    const dormant = store.insertFact({ fact: 'Fait dormant en attente de revue', scope_id: 's1', lifecycle_state: 'dormant' })
    // marque un fait comme supersédé directement
    store.db.prepare('UPDATE facts SET superseded = 1 WHERE id = ?').run(active)

    const sync = new MarkdownSync({ store, outDir })
    const res = sync.export()
    const md = readFileSync(res.files[0]!, 'utf8')
    expect(res.facts).toBe(0)
    expect(md).not.toContain('Fait actif et visible')
    expect(md).not.toContain('Fait dormant')
    void dormant
  })

  it('respecte scopeFilter', () => {
    addFact('Fait du scope A', { scope: 'A' })
    addFact('Fait du scope B', { scope: 'B' })
    const sync = new MarkdownSync({ store, outDir })

    const res = sync.export({ scopeFilter: ['A'] })
    const md = readFileSync(res.files[0]!, 'utf8')
    expect(res.facts).toBe(1)
    expect(md).toContain('Fait du scope A')
    expect(md).not.toContain('Fait du scope B')
  })
})

describe('MarkdownSync — export par thème', () => {
  it('crée un fichier .md par thème', async () => {
    await addWithTopic('Le déploiement du projet Vercel utilise le compte Hello-Primo')
    await addWithTopic('Le projet Vercel échoue parfois quand le cache Hello-Primo est corrompu')
    await addWithTopic('La recette de cuisine du dimanche utilise du curcuma frais')

    const sync = new MarkdownSync({ store, outDir })
    const res = sync.export({ byTopic: true })

    // au moins 2 thèmes distincts → au moins 2 fichiers
    expect(res.files.length).toBeGreaterThanOrEqual(2)
    // tous les fichiers sont sous outDir et finissent en .md
    for (const f of res.files) {
      expect(f.startsWith(outDir)).toBe(true)
      expect(f.endsWith('.md')).toBe(true)
    }
    // tous les faits actifs sont couverts
    expect(res.facts).toBe(3)

    // le contenu des fichiers couvre l'ensemble des faits
    const allContent = res.files.map(f => readFileSync(f, 'utf8')).join('\n')
    expect(allContent).toContain('Vercel')
    expect(allContent).toContain('curcuma')
  })

  it('range les faits sans thème dans _sans-theme.md', () => {
    // fait inséré SANS passer par la couche topics → aucun thème
    addFact('Fait orphelin sans aucun thème assigné', { category: 'savoir' })
    const sync = new MarkdownSync({ store, outDir })
    const res = sync.export({ byTopic: true })

    const orphanFile = res.files.find(f => f.endsWith('_sans-theme.md'))
    expect(orphanFile).toBeTruthy()
    expect(readFileSync(orphanFile!, 'utf8')).toContain('Fait orphelin sans aucun thème')
  })
})

describe('MarkdownSync — idempotence & secrets', () => {
  it('ré-export idempotent : même contenu pour le même état', () => {
    addFact('Fait stable un', { category: 'savoir' })
    addFact('Fait stable deux', { category: 'savoir' })
    const sync = new MarkdownSync({ store, outDir })

    sync.export()
    const first = readFileSync(join(outDir, 'MEMORY.md'), 'utf8')
    sync.export()
    const second = readFileSync(join(outDir, 'MEMORY.md'), 'utf8')

    // on ignore la ligne d'en-tête horodatée (la liste des faits doit être identique)
    const stripHeader = (s: string) => s.replace(/^> .*$/m, '> [header]')
    expect(stripHeader(first)).toBe(stripHeader(second))
    // la liste des puces est strictement identique
    const bullets = (s: string) => s.split('\n').filter(l => l.startsWith('- ')).join('\n')
    expect(bullets(first)).toBe(bullets(second))
  })

  it('un fait [secret:…] reste masqué tel quel (jamais résolu)', () => {
    addFact('La clé API est [secret:anthropic_key]', { category: 'outil' })
    const sync = new MarkdownSync({ store, outDir })
    sync.export()
    const md = readFileSync(join(outDir, 'MEMORY.md'), 'utf8')

    // le marqueur reste littéralement présent, aucun déchiffrement
    expect(md).toContain('[secret:anthropic_key]')
    expect(md).toContain('- La clé API est [secret:anthropic_key]')
  })
})

describe('MarkdownSync — aucune écriture DB par défaut', () => {
  it('export() ne modifie pas le compte de faits ni meta par défaut', () => {
    addFact('Fait un', { category: 'savoir' })
    addFact('Fait deux', { category: 'savoir' })
    const before = store.countFacts()

    const sync = new MarkdownSync({ store, outDir })
    sync.export()
    sync.export({ byTopic: true })

    expect(store.countFacts()).toBe(before)
    // aucune clé markdown_last_sync écrite sans writeMeta
    const meta = store.db.prepare("SELECT value FROM meta WHERE key = 'markdown_last_sync'").get()
    expect(meta).toBeUndefined()
  })

  it('writeMeta: true écrit le hash de sync SANS toucher aux faits', () => {
    addFact('Fait un', { category: 'savoir' })
    const before = store.countFacts()
    const sync = new MarkdownSync({ store, outDir })

    sync.export({ writeMeta: true })
    expect(store.countFacts()).toBe(before)
    const meta = store.db.prepare("SELECT value FROM meta WHERE key = 'markdown_last_sync'").get() as { value: string } | undefined
    expect(meta).toBeTruthy()
    const parsed = JSON.parse(meta!.value)
    expect(parsed.facts).toBe(1)
    expect(typeof parsed.hash).toBe('string')
  })
})

describe('MarkdownSync — garde-fous chemin', () => {
  it('refuse un outDir relatif', () => {
    expect(() => new MarkdownSync({ store, outDir: 'relatif/md' })).toThrow(/absolu/)
  })

  it('écrit uniquement dans outDir (fichiers présents)', () => {
    addFact('Fait présent', { category: 'savoir' })
    const sync = new MarkdownSync({ store, outDir })
    sync.export()
    expect(existsSync(join(outDir, 'MEMORY.md'))).toBe(true)
    const entries = readdirSync(outDir)
    expect(entries).toContain('MEMORY.md')
  })
})

describe('MarkdownSync — helpers purs', () => {
  it('slugifyFile élimine tout caractère de traversée/extension', () => {
    expect(slugifyFile('../../etc/passwd')).toBe('etc-passwd')
    expect(slugifyFile('Déploiement Vercel')).toBe('deploiement-vercel')
    expect(slugifyFile('a/b\\c.d')).toBe('a-b-c-d')
    expect(slugifyFile('')).toBe('')
  })

  it('orderedCategories met les catégories connues en tête, inconnues triées en fin', () => {
    expect(orderedCategories(['zzz', 'preference', 'aaa', 'savoir'])).toEqual(['preference', 'savoir', 'aaa', 'zzz'])
  })

  it('sanitizeBullet aplatit les sauts de ligne mais garde le secret', () => {
    expect(sanitizeBullet('ligne un\nligne deux')).toBe('ligne un ligne deux')
    expect(sanitizeBullet('mot   espacé')).toBe('mot espacé')
    expect(sanitizeBullet('clé [secret:x]')).toBe('clé [secret:x]')
  })
})
