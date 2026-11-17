/**
 * BENCHMARK QUALITÉ DE RECALL (spec §16) — le juge du produit.
 * Jeu synthétique : user / own_company / clientA / clientB / projectX(clientA)
 * / projectY(interne) / privés d'agents + distracteurs.
 * Cibles NON NÉGOCIABLES : fuite inter-clients = 0, dormant explicite,
 * bruit sous cap, partage correct. Si ce fichier n'est pas vert, la feature
 * n'est pas finie.
 */
import { mkdtempSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { afterAll, beforeAll, describe, expect, it } from 'vitest'
import { Memoria, type Organization, type PairAssistantResult, type Project } from '../src/index.js'

let root: string
let m: Memoria
let claude: PairAssistantResult
let codex: PairAssistantResult
let orgA: Organization
let orgB: Organization
let projX: Project
let projY: Project

beforeAll(() => {
  root = mkdtempSync(join(tmpdir(), 'memoria-bench-'))
  m = Memoria.init({ storageRoot: root, configPath: join(root, 'config.toml') })

  claude = m.pairAssistant({ type: 'claude-code' })
  codex = m.pairAssistant({ type: 'codex' })

  orgA = m.registry.createOrganization('Client Alpha', 'client')
  orgB = m.registry.createOrganization('Client Beta', 'client')
  const own = m.registry.ownCompany()!
  projX = m.registry.createProject('Projet X', own.id, orgA.id)
  projY = m.registry.createProject('Projet Y', own.id)

  const scopeUser = m.registry.getScopeByName('user')!
  const scopeClientA = m.registry.ensureScope('client', 'client:alpha', { client_org_id: orgA.id })
  const scopeProjX = m.registry.ensureScope('project', 'project:x', { client_org_id: orgA.id, project_id: projX.id })
  const scopeProjY = m.registry.ensureScope('project', 'project:y', { project_id: projY.id })

  // Claude lit/écrit partout (pour le seed) ; Codex ne lit que user (défaut pairing)
  for (const scope of [scopeUser, scopeClientA, scopeProjX, scopeProjY]) {
    m.registry.setPolicy({
      assistant_id: claude.assistant_id,
      scope_id: scope.id,
      can_read: true,
      can_write: true,
      can_share: false,
      secret_access: 'none',
    })
  }

  const inst = claude.assistant_instance_id
  // — faits significatifs par scope —
  m.storeFact({ instance: inst, scope: scopeProjX.id, client_org_id: orgA.id, project_id: projX.id, category: 'procedure', content: 'La commande de build du projet X est `make release-x` depuis la racine du monorepo' })
  m.storeFact({ instance: inst, scope: scopeProjX.id, client_org_id: orgA.id, project_id: projX.id, content: 'Le projet X déploie sur le cluster kubernetes alpha-prod en région eu-west' })
  m.storeFact({ instance: inst, scope: scopeClientA.id, client_org_id: orgA.id, content: 'Le tarif négocié avec le client Alpha est de 950 euros par jour' })
  m.storeFact({ instance: inst, scope: scopeProjY.id, project_id: projY.id, category: 'procedure', content: 'La commande de build du projet Y interne est `npm run build:y`' })
  m.storeFact({ instance: inst, scope: scopeUser.id, content: 'Néto préfère les réponses courtes et le tutoiement en français' })
  m.storeFact({ instance: inst, content: 'Note privée Claude : brouillon de refacto du module scheduler' })

  // — fait dormant —
  const dormant = m.storeFact({ instance: inst, scope: scopeUser.id, content: 'Ancienne préférence : Néto utilisait Sublime Text avant 2020' })
  const userDbPath = m.registry.dbForScope(scopeUser.id)!.path
  m['openContent'](userDbPath).db.prepare("UPDATE facts SET lifecycle_state = 'dormant' WHERE id = ?").run(dormant.id)

  // — distracteurs (bruit réaliste) —
  const topics = ['café', 'réunion lundi', 'facture vercel', 'logo svg', 'serveur de staging', 'librairie react', 'apple store', 'tests vitest', 'docker compose', 'sauvegarde nas']
  for (let i = 0; i < 40; i++) {
    m.storeFact({ instance: inst, content: `Note diverse ${i} à propos de ${topics[i % topics.length]} sans rapport particulier avec les projets` })
  }
})

afterAll(() => {
  m.close()
  rmSync(root, { recursive: true, force: true })
})

describe('benchmark recall — pertinence', () => {
  it('« commande de build du projet X » en contexte X → la procédure projet X est top-1', () => {
    const r = m.recall({
      instance: claude.assistant_instance_id,
      query: 'commande de build du projet X',
      active_context: { project_id: projX.id, client_org_id: orgA.id },
    })
    expect(r.items.length).toBeGreaterThan(0)
    expect(r.items[0]!.content).toContain('make release-x')
  })

  it('même question en contexte projet Y → c’est la procédure du projet Y qui sort devant', () => {
    const r = m.recall({
      instance: claude.assistant_instance_id,
      query: 'commande de build du projet',
      active_context: { project_id: projY.id },
    })
    expect(r.items.length).toBeGreaterThan(0)
    expect(r.items[0]!.content).toContain('build:y')
  })
})

describe('benchmark recall — ANTI-FUITE (cible : 0)', () => {
  const leakQueries = [
    'commande de build du projet X',
    'tarif négocié client Alpha',
    'cluster kubernetes production',
    'déploiement projet',
    'combien coûte la prestation par jour',
  ]

  it('taux de fuite client A en contexte client B = 0 sur toute la batterie', () => {
    let leaks = 0
    for (const q of leakQueries) {
      const r = m.recall({
        instance: claude.assistant_instance_id,
        query: q,
        active_context: { client_org_id: orgB.id },
        limit: 20,
      })
      for (const item of r.items) {
        if (item.content.includes('make release-x') || item.content.includes('950 euros') || item.content.includes('alpha-prod')) {
          leaks++
        }
      }
    }
    expect(leaks).toBe(0)
  })

  it('sans contexte déclaré : les données client restent masquées (défaut sûr)', () => {
    const r = m.recall({ instance: claude.assistant_instance_id, query: 'tarif négocié euros par jour', limit: 20 })
    expect(r.items.every(i => !i.content.includes('950 euros'))).toBe(true)
  })

  it('les scopes globaux restent accessibles en contexte client (pas de sur-masquage)', () => {
    const r = m.recall({
      instance: claude.assistant_instance_id,
      query: 'préférences de Néto réponses courtes',
      active_context: { client_org_id: orgB.id },
    })
    expect(r.items.some(i => i.content.includes('tutoiement'))).toBe(true)
  })
})

describe('benchmark recall — dormant, bruit, partage', () => {
  it('dormant : exclu par défaut, retrouvé avec include_dormant', () => {
    const sans = m.recall({ instance: claude.assistant_instance_id, query: 'Sublime Text préférence ancienne' })
    expect(sans.items.every(i => !i.content.includes('Sublime'))).toBe(true)
    const avec = m.recall({ instance: claude.assistant_instance_id, query: 'Sublime Text préférence ancienne', include_dormant: true })
    expect(avec.items.some(i => i.content.includes('Sublime'))).toBe(true)
  })

  it('bruit : 40 distracteurs, le budget tient et le top reste pertinent', () => {
    const r = m.recall({
      instance: claude.assistant_instance_id,
      query: 'commande de build du projet X',
      active_context: { project_id: projX.id, client_org_id: orgA.id },
      token_budget: 400,
    })
    expect(r.tokens).toBeLessThanOrEqual(400)
    expect(r.items[0]!.content).toContain('make release-x')
  })

  it('partage : le scope user est visible par le 2e agent, le privé non', () => {
    const r = m.recall({ instance: codex.assistant_instance_id, query: 'préférences réponses courtes tutoiement' })
    expect(r.items.some(i => i.content.includes('tutoiement'))).toBe(true)
    const priv = m.recall({ instance: codex.assistant_instance_id, query: 'brouillon refacto scheduler' })
    expect(priv.items).toHaveLength(0)
  })
})
