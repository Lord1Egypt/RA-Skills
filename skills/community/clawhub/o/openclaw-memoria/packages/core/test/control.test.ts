/**
 * Contrôle & config (Réglages) : kill-switch, déplacement du stockage,
 * suppression définitive d'agent, lancement auto.
 */
import { existsSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { afterEach, beforeEach, describe, expect, it } from 'vitest'
import {
  autostartStatus,
  isEnabled,
  Memoria,
  moveStorage,
  setEnabled,
} from '../src/index.js'

describe('kill-switch (config.enabled)', () => {
  let dir: string
  let configPath: string
  beforeEach(() => {
    dir = mkdtempSync(join(tmpdir(), 'memoria-killswitch-'))
    configPath = join(dir, 'config.toml')
  })
  afterEach(() => rmSync(dir, { recursive: true, force: true }))

  it('actif par défaut (absent = true)', () => {
    expect(isEnabled(configPath)).toBe(true)
  })

  it('setEnabled(false) persiste et isEnabled le relit', () => {
    setEnabled(false, configPath)
    expect(isEnabled(configPath)).toBe(false)
    expect(readFileSync(configPath, 'utf8')).toContain('enabled')
    setEnabled(true, configPath)
    expect(isEnabled(configPath)).toBe(true)
  })

  it('l’engine expose isEnabled/setEnabled cohérents avec la config', () => {
    const root = join(dir, 'data')
    const m = Memoria.init({ storageRoot: root, configPath, llm: { extraction: null } })
    try {
      expect(m.isEnabled()).toBe(true)
      m.setEnabled(false)
      expect(m.isEnabled()).toBe(false)
      // persisté sur disque → relisible hors-process
      expect(isEnabled(configPath)).toBe(false)
    } finally {
      m.close()
    }
  })
})

describe('storageInfo + moveStorage', () => {
  let dir: string
  beforeEach(() => {
    dir = mkdtempSync(join(tmpdir(), 'memoria-move-'))
  })
  afterEach(() => rmSync(dir, { recursive: true, force: true }))

  it('storageInfo renvoie la racine courante', () => {
    const root = join(dir, 'data')
    const configPath = join(dir, 'config.toml')
    const m = Memoria.init({ storageRoot: root, configPath, llm: { extraction: null } })
    try {
      const info = m.storageInfo()
      expect(info.root).toBe(root)
      expect(info.config_path).toBe(configPath)
      expect(typeof info.on_network_volume).toBe('boolean')
    } finally {
      m.close()
    }
  })

  it('déplace les fichiers et réécrit config.toml', () => {
    const from = join(dir, 'data')
    const to = join(dir, 'usb', 'memoria')
    const configPath = join(dir, 'config.toml')
    // poser un fait puis fermer (DB non ouverte pendant le move)
    const m = Memoria.init({ storageRoot: from, configPath, llm: { extraction: null } })
    const a = m.pairAssistant({ type: 'claude-code' })
    m.storeFact({ instance: a.assistant_instance_id, content: 'Néto utilise une clé USB pour la mémoire portable' })
    m.close()

    const res = moveStorage({ from, to, configPath })
    expect(res.to).toBe(to)
    expect(existsSync(from)).toBe(false)
    expect(existsSync(join(to, 'registry.sqlite'))).toBe(true)
    // config pointe désormais sur la destination
    expect(readFileSync(configPath, 'utf8')).toContain(to)

    // ré-ouverture au nouvel emplacement → le fait survit
    const m2 = Memoria.init({ configPath, llm: { extraction: null } })
    try {
      expect(m2.paths.root).toBe(to)
      const agents = m2.listAgents()
      expect(agents.length).toBeGreaterThan(0)
    } finally {
      m2.close()
    }
  })

  it('refuse une destination déjà occupée', () => {
    const from = join(dir, 'data')
    const to = join(dir, 'occupe')
    const configPath = join(dir, 'config.toml')
    Memoria.init({ storageRoot: from, configPath, llm: { extraction: null } }).close()
    // destination NON vide
    writeFileSync(join(dir, 'placeholder.txt'), 'x') // garde-fou : le parent existe déjà (mkdtemp)
    Memoria.init({ storageRoot: to, configPath: join(dir, 'other.toml'), llm: { extraction: null } }).close()
    expect(() => moveStorage({ from, to, configPath })).toThrow(/déjà occupée/)
  })
})

describe('deleteInstance (suppression définitive)', () => {
  let dir: string
  let m: Memoria
  beforeEach(() => {
    dir = mkdtempSync(join(tmpdir(), 'memoria-delagent-'))
    m = Memoria.init({ storageRoot: join(dir, 'data'), configPath: join(dir, 'config.toml'), llm: { extraction: null } })
  })
  afterEach(() => {
    m.close()
    rmSync(dir, { recursive: true, force: true })
  })

  it('efface l’agent, sa DB privée et le retire de la liste', () => {
    const a = m.pairAssistant({ type: 'codex' })
    m.storeFact({ instance: a.assistant_instance_id, content: 'fait privé à effacer' })
    const dbPath = m.paths.assistantDb(a.assistant_instance_id)
    expect(existsSync(dbPath)).toBe(true)
    expect(m.listAgents().some(x => x.instance.id === a.assistant_instance_id)).toBe(true)

    const res = m.deleteInstance(a.assistant_instance_id)
    expect(res.deleted).toBe(true)
    expect(existsSync(dbPath)).toBe(false)
    expect(m.listAgents().some(x => x.instance.id === a.assistant_instance_id)).toBe(false)
  })

  it('renvoie deleted:false pour une instance inconnue', () => {
    expect(m.deleteInstance('inconnu').deleted).toBe(false)
  })
})

describe('autostartStatus', () => {
  it('renvoie un plistPath et un drapeau supported', () => {
    const s = autostartStatus()
    expect(typeof s.supported).toBe('boolean')
    expect(s.plistPath).toContain('fr.primo-studio.memoria.plist')
    // sur cette machine (darwin) c'est pris en charge, mais on n'installe rien ici
    expect(typeof s.installed).toBe('boolean')
  })
})
