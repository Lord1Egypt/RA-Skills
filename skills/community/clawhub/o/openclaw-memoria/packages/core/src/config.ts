/**
 * Configuration & résolution du stockage (spec §8, décision D1).
 *
 * - Fichier de découverte FIXE : `~/.memoria/config.toml` (pointe vers le storage_root).
 * - `resolveStorageRoot()` UNIQUE : param explicite > config.toml > $MEMORIA_HOME > ~/.memoria/data.
 *   (Corrige le legacy : 8 chemins divergents, `cfg.workspacePath` ignoré par la DB.)
 */
import { cpSync, existsSync, mkdirSync, readdirSync, readFileSync, renameSync, rmSync, writeFileSync } from 'node:fs'
import { homedir } from 'node:os'
import { dirname, join, resolve } from 'node:path'
import { parse as parseToml, stringify as stringifyToml } from 'smol-toml'

export interface MemoriaConfig {
  /** Racine du stockage (registry + DB + secrets + backups). */
  storage_path?: string
  /**
   * Kill-switch global (défaut true). À false : le daemon reste joignable pour
   * l'admin/UI mais REFUSE capture et recall (les agents n'écrivent ni ne
   * lisent de mémoire). Permet de « mettre Memoria en pause » sans tout fermer.
   */
  enabled?: boolean
  daemon?: {
    /** 0 = port auto (choisi au premier démarrage puis persisté). */
    port?: number
  }
  /**
   * Synchro inter-machines (SYNC-INTER-MACHINES.md). hub = détenteur canonique
   * des scopes partagés ; spoke = réplique locale qui tire/pousse vers le hub.
   * GVK/CPK/peer_token NE SONT JAMAIS ici (fichier clair) → Keychain.
   */
  sync?: {
    enabled?: boolean
    role?: 'hub' | 'spoke'
    machine_id?: string
    /** (spoke) adresse du hub « ip:port ». */
    hub?: string
    /** (hub) listener LAN dédié /v1/sync/* « ip:port » (≠ port loopback admin/memory). */
    listen_lan?: string
    interval_sec?: number
    tls?: boolean
    /** Types de scopes synchronisés (private exclu par construction). */
    scopes?: string[]
    relay_path?: string
    discovery_file?: string
  }
  llm?: {
    /** Profil raccourci : '100-local' | 'local-plus-cloud' | 'cloud' | 'custom'. */
    profile?: string
    /**
     * Choix EXPLICITE du provider/modèle d'extraction (prioritaire sur le
     * profil si présent). provider ∈ ollama|lmstudio|anthropic|openai|openrouter.
     * base_url : serveurs locaux OpenAI-compatibles (LM Studio — défaut
     * http://127.0.0.1:1234/v1) ou Ollama hors port standard.
     */
    extraction?: { provider?: string; model?: string; base_url?: string }
    /** Choix explicite des embeddings (provider ollama uniquement en V1). */
    embeddings?: { provider?: string; model?: string }
  }
}

export interface ResolvedConfig {
  configPath: string
  storageRoot: string
  config: MemoriaConfig
}

export const DEFAULT_CONFIG_PATH: string = join(homedir(), '.memoria', 'config.toml')

export function defaultStorageRoot(): string {
  return join(homedir(), '.memoria', 'data')
}

export function loadConfigFile(configPath: string = DEFAULT_CONFIG_PATH): MemoriaConfig {
  if (!existsSync(configPath)) return {}
  const raw = readFileSync(configPath, 'utf8')
  try {
    return parseToml(raw) as MemoriaConfig
  } catch (err) {
    throw new Error(`config.toml illisible (${configPath}) : ${(err as Error).message}`)
  }
}

export function saveConfigFile(config: MemoriaConfig, configPath: string = DEFAULT_CONFIG_PATH): void {
  mkdirSync(dirname(configPath), { recursive: true })
  writeFileSync(configPath, stringifyToml(config as Record<string, unknown>), 'utf8')
}

/** Memoria actif ? (kill-switch). Absent = true par défaut. */
export function isEnabled(configPath: string = DEFAULT_CONFIG_PATH): boolean {
  return loadConfigFile(configPath).enabled !== false
}

/** Bascule le kill-switch et persiste. Retourne l'état effectif. */
export function setEnabled(enabled: boolean, configPath: string = DEFAULT_CONFIG_PATH): boolean {
  const config = loadConfigFile(configPath)
  config.enabled = enabled
  saveConfigFile(config, configPath)
  return enabled
}

export interface ResolveOptions {
  /** Priorité 1 : chemin explicite (tests, daemon piloté). */
  storageRoot?: string
  /** Chemin du fichier de découverte (défaut ~/.memoria/config.toml). */
  configPath?: string
  /** Environnement injectable pour les tests. */
  env?: NodeJS.ProcessEnv
}

/** LE résolveur unique d'emplacement. Toute ouverture de DB passe par ici. */
export function resolveStorageRoot(opts: ResolveOptions = {}): ResolvedConfig {
  const configPath = opts.configPath ?? DEFAULT_CONFIG_PATH
  const env = opts.env ?? process.env
  const config = loadConfigFile(configPath)

  const root = opts.storageRoot ?? config.storage_path ?? env['MEMORIA_HOME'] ?? defaultStorageRoot()

  const storageRoot = resolve(root)
  return { configPath, storageRoot, config }
}

/** Arborescence canonique sous storage_root (spec §8). */
export function storagePaths(storageRoot: string) {
  return {
    root: storageRoot,
    registry: join(storageRoot, 'registry.sqlite'),
    assistantsDir: join(storageRoot, 'assistants'),
    assistantDb: (instanceId: string) => join(storageRoot, 'assistants', instanceId, 'memory.sqlite'),
    sharedDir: join(storageRoot, 'shared'),
    sharedDb: (scopeFile: string) => join(storageRoot, 'shared', `${scopeFile}.sqlite`),
    secretsDir: join(storageRoot, 'secrets'),
    backupsDir: join(storageRoot, 'backups'),
    cacheDir: join(storageRoot, 'cache'),
    daemonState: join(storageRoot, 'daemon.json'),
    daemonLock: join(storageRoot, 'daemon.lock'),
  } as const
}

/**
 * Déplace TOUTE la mémoire vers un nouvel emplacement (ex. clé USB) et met à
 * jour `config.toml` pour qu'il pointe dessus. Le daemon DOIT être arrêté.
 * Idempotent-safe : refuse si la destination existe déjà non vide.
 * Les chemins de DB en base sont relatifs au root via storagePaths → rien à
 * réécrire dans registry (db_registry stocke des chemins absolus : on les
 * recalcule au prochain boot via re-registerDb ; ici on déplace les fichiers).
 */
export function moveStorage(opts: {
  from?: string
  to: string
  configPath?: string
}): { from: string; to: string } {
  const configPath = opts.configPath ?? DEFAULT_CONFIG_PATH
  const resolved = resolveStorageRoot({ configPath })
  const from = resolveAbs(opts.from ?? resolved.storageRoot)
  const to = resolveAbs(opts.to)
  if (from === to) return { from, to }
  if (!existsSync(from)) throw new Error(`emplacement source introuvable : ${from}`)
  if (existsSync(to) && readdirSync(to).length > 0) {
    throw new Error(`destination déjà occupée : ${to} (choisis un dossier vide)`)
  }
  mkdirSync(dirname(to), { recursive: true })
  // déplacement (rename si même volume, sinon copie récursive + suppression)
  try {
    renameSync(from, to)
  } catch {
    cpSync(from, to, { recursive: true })
    rmSync(from, { recursive: true, force: true })
  }
  // mettre à jour le fichier de découverte
  const config = loadConfigFile(configPath)
  config.storage_path = to
  saveConfigFile(config, configPath)
  return { from, to }
}

function resolveAbs(p: string): string {
  return resolve(p.replace(/^~(?=$|\/)/, homedir()))
}

export function ensureStorageTree(storageRoot: string): void {
  const p = storagePaths(storageRoot)
  for (const dir of [p.root, p.assistantsDir, p.sharedDir, p.secretsDir, p.backupsDir, p.cacheDir]) {
    mkdirSync(dir, { recursive: true })
  }
}
