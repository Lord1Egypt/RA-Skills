/**
 * Interlocuteurs (personnes) : reconnaître QUI parle à l'agent, via un
 * identifiant (Telegram/WhatsApp/mail/handle) ou un nom. Normalisation +
 * unicité + identifyInterlocutor + cascade de suppression.
 */
import { mkdtempSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { afterEach, beforeEach, describe, expect, it } from 'vitest'
import { Memoria } from '../src/index.js'

let dir: string
let m: Memoria

beforeEach(() => {
  dir = mkdtempSync(join(tmpdir(), 'memoria-persons-'))
  m = Memoria.init({ storageRoot: join(dir, 'data'), configPath: join(dir, 'config.toml'), llm: { extraction: null } })
})
afterEach(() => {
  m.close()
  rmSync(dir, { recursive: true, force: true })
})

describe('personnes & identifiants', () => {
  it('crée une personne et la liste', () => {
    const p = m.createPerson({ display_name: 'Badette', relation: 'collaboratrice', notes: 'Gère les builds iOS' })
    expect(p.id).toBeTruthy()
    const list = m.listPersons()
    expect(list).toHaveLength(1)
    expect(list[0]!.display_name).toBe('Badette')
    expect(list[0]!.relation).toBe('collaboratrice')
    expect(list[0]!.identifiers).toEqual([])
  })

  it('normalise les identifiants (téléphone, telegram, email)', () => {
    const p = m.createPerson({ display_name: 'Badette' })
    m.addPersonIdentifier(p.id, 'phone', '+594 6 94 12 34 56')
    m.addPersonIdentifier(p.id, 'telegram', '@Badette_Primo')
    m.addPersonIdentifier(p.id, 'email', 'Badette@Primo-Studio.FR')

    // matching insensible à la mise en forme (même numéro, ponctuation différente)
    expect(m.identifyInterlocutor({ phone: '+594-6-94.12.34.56' })?.person.display_name).toBe('Badette')
    expect(m.identifyInterlocutor({ telegram: 'badette_primo' })?.person.display_name).toBe('Badette')
    expect(m.identifyInterlocutor({ email: 'badette@primo-studio.fr' })?.person.display_name).toBe('Badette')
  })

  it('identifyInterlocutor : telegram > nom en repli ; inconnu = null', () => {
    const p = m.createPerson({ display_name: 'Néto Pompeu', relation: 'owner' })
    m.addPersonIdentifier(p.id, 'telegram', '123456789')

    expect(m.identifyInterlocutor({ telegram: '123456789' })?.person.display_name).toBe('Néto Pompeu')
    // repli par nom exact
    expect(m.identifyInterlocutor({ name: 'néto pompeu' })?.person.id).toBe(p.id)
    // inconnu → null (l'agent supposera l'owner)
    expect(m.identifyInterlocutor({ telegram: '000', name: 'Inconnu' })).toBeNull()
  })

  it('un identifiant ne pointe que vers UNE personne (réattribution propre)', () => {
    const a = m.createPerson({ display_name: 'Alice' })
    const b = m.createPerson({ display_name: 'Bob' })
    m.addPersonIdentifier(a.id, 'telegram', 'shared_handle')
    m.addPersonIdentifier(b.id, 'telegram', 'shared_handle') // réattribue à Bob
    expect(m.identifyInterlocutor({ telegram: 'shared_handle' })?.person.display_name).toBe('Bob')
    // Alice n'a plus cet identifiant
    expect(m.getPerson(a.id)!.identifiers).toHaveLength(0)
  })

  it('supprimer une personne efface ses identifiants (cascade)', () => {
    const p = m.createPerson({ display_name: 'Stagiaire' })
    m.addPersonIdentifier(p.id, 'email', 'stage@primo-studio.fr')
    expect(m.deletePerson(p.id)).toBe(true)
    expect(m.listPersons()).toHaveLength(0)
    // l'identifiant ne matche plus rien
    expect(m.identifyInterlocutor({ email: 'stage@primo-studio.fr' })).toBeNull()
  })

  it('identifyInterlocutor renvoie les faits connus sur la personne', () => {
    const a = m.pairAssistant({ type: 'claude-code' })
    const p = m.createPerson({ display_name: 'Badette', relation: 'collaboratrice' })
    m.addPersonIdentifier(p.id, 'telegram', 'badette')
    m.storeFact({ instance: a.assistant_instance_id, content: 'Badette gère les builds iOS et les soumissions TestFlight' })

    const match = m.identifyInterlocutor({ telegram: 'badette' })
    expect(match).not.toBeNull()
    expect(match!.known.some(f => /Badette/.test(f))).toBe(true)
  })

  it('describeInterlocutor produit une ligne lisible', () => {
    const p = m.createPerson({ display_name: 'Badette', relation: 'collaboratrice', notes: 'Accès builds iOS.' })
    const line = m.describeInterlocutor(p.id)
    expect(line).toContain('Badette')
    expect(line).toContain('collaboratrice')
    expect(line).toContain('Accès builds iOS.')
  })

  it('identifyOrCreateInterlocutor crée la personne au 1er contact puis la retrouve', () => {
    // 1er contact d'un numéro WhatsApp inconnu → création automatique
    const first = m.identifyOrCreateInterlocutor({ whatsapp: '+594694003393', name: 'Patron SOC' })
    expect(first).not.toBeNull()
    expect(first!.created).toBe(true)
    expect(first!.person.display_name).toBe('Patron SOC')
    expect(first!.person.identifiers.some(i => i.kind === 'whatsapp')).toBe(true)

    // 2e contact du même numéro → retrouvée, PAS recréée
    const second = m.identifyOrCreateInterlocutor({ whatsapp: '+594694003393' })
    expect(second!.created).toBe(false)
    expect(second!.person.id).toBe(first!.person.id)
    expect(m.listPersons()).toHaveLength(1)
  })

  it('identifyOrCreateInterlocutor sans identifiant ne crée rien (owner par défaut)', () => {
    const r = m.identifyOrCreateInterlocutor({ name: 'Inconnu sans identifiant' })
    expect(r).toBeNull()
    expect(m.listPersons()).toHaveLength(0)
  })
})
