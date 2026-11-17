/**
 * Enregistrement/désenregistrement AUTOMATIQUE du serveur MCP Memoria auprès de
 * l'agent hôte (Claude Code / Codex / OpenClaw). Objectif : une seule commande
 * pour connecter, une seule pour déconnecter — zéro édition manuelle.
 *
 * DÉPLACÉ depuis @memoria/mcp vers @memoria/core (mission B2) : le daemon doit
 * pouvoir enregistrer un agent EN PROCESSUS (connexion 1 clic depuis l'UI) et
 * @memoria/mcp dépend déjà de @memoria/daemon — une dépendance daemon→mcp
 * créerait un cycle de project references. @memoria/mcp ré-exporte ce module
 * (API publique inchangée).
 *
 * La commande `serve` pointe sur le bin de @memoria/mcp de CETTE installation
 * (chemin absolu) tant que le paquet n'est pas publié sur npm ; après
 * publication → `npx -y @memoria/mcp`.
 */
import { execFileSync } from 'node:child_process'
import { cpSync, existsSync, lstatSync, mkdirSync, readFileSync, rmSync, symlinkSync, writeFileSync } from 'node:fs'
import { homedir } from 'node:os'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

export type HostKind = 'claude-code' | 'codex' | 'openclaw' | 'generic'

/** Options d'enregistrement (le token d'instance permet l'install des hooks OpenClaw). */
export interface RegisterOptions {
  /** Token d'instance (pairing) — requis pour l'auto-capture OpenClaw via hooks. */
  token?: string
  /** Racine du stockage (pour que l'adaptateur découvre le port du daemon). */
  storageRoot?: string
}

export interface RegisterResult {
  host: HostKind
  registered: boolean
  /** Décrit ce qui a été fait, ou l'instruction manuelle si l'auto a échoué. */
  detail: string
}

/**
 * Invocation `serve` du bin @memoria/mcp de cette installation.
 * Ce fichier compile dans packages/core/dist/agents/ → le bin MCP voisin est
 * dans packages/mcp/dist/bin.js (monorepo).
 */
export function serveInvocation(instanceId: string): { command: string; args: string[] } {
  const binPath = fileURLToPath(new URL('../../../mcp/dist/bin.js', import.meta.url))
  return { command: process.execPath, args: [binPath, 'serve', '--instance', instanceId] }
}

/** Sonde `<bin> --version` : CLI présente ? Échec = absente (jamais un crash). */
export function cliInstalled(bin: string): boolean {
  try {
    execFileSync(bin, ['--version'], { stdio: 'ignore', timeout: 5_000 })
    return true
  } catch {
    return false
  }
}

function hasClaudeCli(): boolean {
  return cliInstalled('claude')
}

function hasOpenClawCli(): boolean {
  return cliInstalled('openclaw')
}

// --------------------------------------------------------------- Claude Code

export function registerClaudeCode(instanceId: string): RegisterResult {
  const { command, args } = serveInvocation(instanceId)
  if (hasClaudeCli()) {
    try {
      // -- sépare les flags claude de la commande du serveur
      execFileSync('claude', ['mcp', 'remove', '--scope', 'user', 'memoria'], { stdio: 'ignore' })
    } catch {
      /* pas encore enregistré — normal */
    }
    execFileSync('claude', ['mcp', 'add', '--scope', 'user', 'memoria', '--', command, ...args], { stdio: 'ignore' })
    return { host: 'claude-code', registered: true, detail: 'serveur MCP « memoria » ajouté à Claude Code (scope user).' }
  }
  // Repli : éditer ~/.claude.json (mcpServers global)
  const cfgPath = join(homedir(), '.claude.json')
  try {
    const cfg = existsSync(cfgPath) ? (JSON.parse(readFileSync(cfgPath, 'utf8')) as Record<string, unknown>) : {}
    const servers = (cfg['mcpServers'] as Record<string, unknown> | undefined) ?? {}
    servers['memoria'] = { command, args }
    cfg['mcpServers'] = servers
    writeFileSync(cfgPath, JSON.stringify(cfg, null, 2), 'utf8')
    return { host: 'claude-code', registered: true, detail: `serveur MCP « memoria » écrit dans ${cfgPath}.` }
  } catch (err) {
    return { host: 'claude-code', registered: false, detail: `échec auto (${(err as Error).message}). Manuel : claude mcp add memoria -- ${command} ${args.join(' ')}` }
  }
}

export function unregisterClaudeCode(): RegisterResult {
  if (hasClaudeCli()) {
    try {
      execFileSync('claude', ['mcp', 'remove', '--scope', 'user', 'memoria'], { stdio: 'ignore' })
      return { host: 'claude-code', registered: false, detail: 'serveur MCP « memoria » retiré de Claude Code.' }
    } catch (err) {
      return { host: 'claude-code', registered: false, detail: `retrait CLI échoué (${(err as Error).message}).` }
    }
  }
  const cfgPath = join(homedir(), '.claude.json')
  try {
    if (!existsSync(cfgPath)) return { host: 'claude-code', registered: false, detail: 'aucune config Claude Code à nettoyer.' }
    const cfg = JSON.parse(readFileSync(cfgPath, 'utf8')) as Record<string, unknown>
    const servers = cfg['mcpServers'] as Record<string, unknown> | undefined
    if (servers && 'memoria' in servers) {
      delete servers['memoria']
      writeFileSync(cfgPath, JSON.stringify(cfg, null, 2), 'utf8')
    }
    return { host: 'claude-code', registered: false, detail: `serveur MCP « memoria » retiré de ${cfgPath}.` }
  } catch (err) {
    return { host: 'claude-code', registered: false, detail: `nettoyage échoué (${(err as Error).message}).` }
  }
}

// --------------------------------------------------------------------- Codex

const CODEX_CONFIG = join(homedir(), '.codex', 'config.toml')

/** Retire un bloc `[mcp_servers.memoria]` existant (jusqu'au prochain `[` ou EOF). */
function stripCodexBlock(toml: string): string {
  const lines = toml.split('\n')
  const out: string[] = []
  let skipping = false
  for (const line of lines) {
    if (/^\s*\[mcp_servers\.memoria(\.|])/.test(line)) {
      skipping = true
      continue
    }
    if (skipping && /^\s*\[/.test(line)) skipping = false
    if (!skipping) out.push(line)
  }
  return out.join('\n').replace(/\n{3,}/g, '\n\n')
}

export function registerCodex(instanceId: string): RegisterResult {
  const { command, args } = serveInvocation(instanceId)
  try {
    const existing = existsSync(CODEX_CONFIG) ? readFileSync(CODEX_CONFIG, 'utf8') : ''
    const cleaned = stripCodexBlock(existing).replace(/\s*$/, '')
    const block = [
      '',
      '[mcp_servers.memoria]',
      `command = ${JSON.stringify(command)}`,
      `args = [${args.map(a => JSON.stringify(a)).join(', ')}]`,
      'startup_timeout_sec = 30',
      '',
    ].join('\n')
    mkdirSync(dirname(CODEX_CONFIG), { recursive: true })
    writeFileSync(CODEX_CONFIG, `${cleaned}\n${block}`, 'utf8')
    return { host: 'codex', registered: true, detail: `serveur MCP « memoria » écrit dans ${CODEX_CONFIG}.` }
  } catch (err) {
    return { host: 'codex', registered: false, detail: `échec auto (${(err as Error).message}). Ajoute [mcp_servers.memoria] manuellement dans ${CODEX_CONFIG}.` }
  }
}

export function unregisterCodex(): RegisterResult {
  try {
    if (!existsSync(CODEX_CONFIG)) return { host: 'codex', registered: false, detail: 'aucune config Codex à nettoyer.' }
    const cleaned = stripCodexBlock(readFileSync(CODEX_CONFIG, 'utf8'))
    writeFileSync(CODEX_CONFIG, cleaned, 'utf8')
    return { host: 'codex', registered: false, detail: `serveur MCP « memoria » retiré de ${CODEX_CONFIG}.` }
  } catch (err) {
    return { host: 'codex', registered: false, detail: `nettoyage échoué (${(err as Error).message}).` }
  }
}

// ------------------------------------------------------------------ OpenClaw

const OPENCLAW_DIR = join(homedir(), '.openclaw')

/** Répertoire du package adaptateur DANS cette installation (non publié sur npm). */
function adapterDir(): string | null {
  // register.js compile dans packages/core/dist/agents/ → adaptateur dans packages/adapter-openclaw
  const dir = fileURLToPath(new URL('../../../adapter-openclaw', import.meta.url))
  return existsSync(join(dir, 'dist', 'index.js')) && existsSync(join(dir, 'openclaw.plugin.json')) ? dir : null
}

/**
 * Installe l'adaptateur de HOOKS OpenClaw (auto-recall + auto-capture) :
 *  1. lie le plugin dans ~/.openclaw/extensions/memoria (symlink, copie en repli) ;
 *  2. écrit ~/.openclaw/openclaw.json avec `allowConversationAccess=true` — SANS quoi
 *     `agent_end`/`llm_output` sont bloqués silencieusement (DIAG-OPENCLAW-2026.6.5 §2.1).
 * Le token d'instance est REQUIS (le plugin lit/écrit la mémoire via /v1/memory/*).
 */
export function installOpenClawHooks(opts: {
  instanceId: string
  token?: string
  storageRoot?: string
  /** Override de ~/.openclaw (tests). */
  openclawDir?: string
  /** Override du dossier source de l'adaptateur (tests). */
  srcDir?: string
}): { ok: boolean; detail: string } {
  if (!opts.token) return { ok: false, detail: 'hooks non installés : pas de token d’instance (MCP seul, pull manuel).' }
  const src = opts.srcDir ?? adapterDir()
  if (!src) return { ok: false, detail: 'hooks non installés : adaptateur introuvable (lance « npm run build »).' }

  const ocDir = opts.openclawDir ?? OPENCLAW_DIR
  const ocConfig = join(ocDir, 'openclaw.json')
  const ocExtDir = join(ocDir, 'extensions', 'memoria')

  try {
    // 1) lien du plugin (symlink → mises à jour live au rebuild ; copie si symlink refusé)
    mkdirSync(dirname(ocExtDir), { recursive: true })
    if (existsSync(ocExtDir) || isSymlink(ocExtDir)) rmSync(ocExtDir, { recursive: true, force: true })
    try {
      symlinkSync(src, ocExtDir, 'dir')
    } catch {
      cpSync(src, ocExtDir, { recursive: true })
    }

    // 2) merge openclaw.json (jamais d'écrasement du reste de la config)
    const cfg = existsSync(ocConfig) ? (JSON.parse(readFileSync(ocConfig, 'utf8')) as Record<string, unknown>) : {}
    const plugins = (cfg['plugins'] as Record<string, unknown> | undefined) ?? {}
    const allow = new Set([...(Array.isArray(plugins['allow']) ? (plugins['allow'] as string[]) : []), 'memoria'])
    const entries = (plugins['entries'] as Record<string, unknown> | undefined) ?? {}
    const prev = (entries['memoria'] as Record<string, unknown> | undefined) ?? {}
    const prevConfig = (prev['config'] as Record<string, unknown> | undefined) ?? {}
    entries['memoria'] = {
      ...prev,
      enabled: true,
      hooks: { allowConversationAccess: true, allowPromptInjection: true },
      config: {
        ...prevConfig,
        token: opts.token,
        instance: opts.instanceId,
        ...(opts.storageRoot ? { storageRoot: opts.storageRoot } : {}),
      },
    }
    plugins['allow'] = [...allow]
    plugins['entries'] = entries
    cfg['plugins'] = plugins
    mkdirSync(ocDir, { recursive: true })
    writeFileSync(ocConfig, JSON.stringify(cfg, null, 2), 'utf8')
    return { ok: true, detail: `hooks installés (${ocExtDir}) + allowConversationAccess=true dans ${ocConfig}.` }
  } catch (err) {
    return { ok: false, detail: `install hooks échouée (${(err as Error).message}).` }
  }
}

function isSymlink(p: string): boolean {
  try {
    return lstatSync(p).isSymbolicLink()
  } catch {
    return false
  }
}

export function registerOpenClaw(instanceId: string, opts: RegisterOptions = {}): RegisterResult {
  const { command, args } = serveInvocation(instanceId)
  const details: string[] = []
  let mcpOk = false

  // (a) serveur MCP (pull + tools manuels)
  if (hasOpenClawCli()) {
    try {
      execFileSync('openclaw', ['mcp', 'set', 'memoria', JSON.stringify({ command, args })], { stdio: 'ignore' })
      mcpOk = true
      details.push('serveur MCP « memoria » enregistré dans OpenClaw.')
    } catch (err) {
      details.push(`openclaw mcp set échoué (${(err as Error).message}).`)
    }
  } else {
    details.push(`CLI openclaw absente — MCP manuel : openclaw mcp set memoria '${JSON.stringify({ command, args })}'`)
  }

  // (b) hooks (auto-recall + auto-capture) — le vrai cœur, indépendant du CLI
  const hooks = installOpenClawHooks({ instanceId, token: opts.token, storageRoot: opts.storageRoot })
  details.push(hooks.ok ? hooks.detail : `⚠ ${hooks.detail}`)

  return { host: 'openclaw', registered: mcpOk || hooks.ok, detail: details.join(' ') }
}

export function unregisterOpenClaw(opts: { openclawDir?: string } = {}): RegisterResult {
  const ocDir = opts.openclawDir ?? OPENCLAW_DIR
  const ocConfig = join(ocDir, 'openclaw.json')
  const ocExtDir = join(ocDir, 'extensions', 'memoria')
  const details: string[] = []
  if (hasOpenClawCli()) {
    try {
      execFileSync('openclaw', ['mcp', 'unset', 'memoria'], { stdio: 'ignore' })
      details.push('serveur MCP « memoria » retiré d’OpenClaw.')
    } catch (err) {
      details.push(`openclaw mcp unset échoué (${(err as Error).message}).`)
    }
  }
  // retire le plugin de hooks + son entrée de config (laisse le reste intact)
  try {
    if (existsSync(ocExtDir) || isSymlink(ocExtDir)) rmSync(ocExtDir, { recursive: true, force: true })
    if (existsSync(ocConfig)) {
      const cfg = JSON.parse(readFileSync(ocConfig, 'utf8')) as Record<string, unknown>
      const plugins = cfg['plugins'] as Record<string, unknown> | undefined
      if (plugins) {
        const entries = plugins['entries'] as Record<string, unknown> | undefined
        if (entries && 'memoria' in entries) delete entries['memoria']
        if (Array.isArray(plugins['allow'])) plugins['allow'] = (plugins['allow'] as string[]).filter(x => x !== 'memoria')
        writeFileSync(ocConfig, JSON.stringify(cfg, null, 2), 'utf8')
      }
    }
    details.push('hooks « memoria » retirés d’OpenClaw.')
  } catch (err) {
    details.push(`nettoyage hooks échoué (${(err as Error).message}).`)
  }
  return { host: 'openclaw', registered: false, detail: details.join(' ') }
}

// ---------------------------------------------------------------- dispatch

export function autoRegister(host: string, instanceId: string, opts: RegisterOptions = {}): RegisterResult {
  switch (host) {
    case 'claude-code':
      return registerClaudeCode(instanceId)
    case 'codex':
      return registerCodex(instanceId)
    case 'openclaw':
      return registerOpenClaw(instanceId, opts)
    default:
      return { host: 'generic', registered: false, detail: `Type « ${host} » : enregistre le serveur MCP manuellement (memoria-mcp serve --instance ${instanceId}).` }
  }
}

export function autoUnregister(host: string): RegisterResult {
  switch (host) {
    case 'claude-code':
      return unregisterClaudeCode()
    case 'codex':
      return unregisterCodex()
    case 'openclaw':
      return unregisterOpenClaw()
    default:
      return { host: 'generic', registered: false, detail: 'Rien à nettoyer automatiquement pour ce type.' }
  }
}
