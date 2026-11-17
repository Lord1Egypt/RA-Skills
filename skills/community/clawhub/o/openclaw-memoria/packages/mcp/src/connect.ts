/**
 * `memoria-mcp connect --code XXXX-XXXX` — échange le code de pairing (affiché
 * par l'UI/CLI admin) contre un token d'instance, sauvegarde les credentials,
 * puis ENREGISTRE AUTOMATIQUEMENT le serveur MCP auprès de l'hôte détecté
 * (Claude Code / Codex / OpenClaw). Une seule commande à coller, rien d'autre.
 */
import { nowISO, resolveStorageRoot } from '@memoria/core'
import { DaemonClient, ensureDaemon, type DaemonState } from '@memoria/daemon'
import { defaultCredentialsDir, saveCredentials } from './credentials.js'
import { autoRegister, serveInvocation, type RegisterResult } from './register.js'

export interface PairingCompleter {
  completePairing(code: string): Promise<{ assistant_instance_id: string; instance_token: string; assistant_type?: string }>
}

export interface ConnectOptions {
  code: string
  storageRoot?: string
  credentialsDir?: string
  /** Enregistrer automatiquement le serveur MCP auprès de l'hôte (défaut: true). */
  register?: boolean
  /** Injectables pour les tests (pas de vrai daemon, pas de réseau). */
  ensure?: (opts: { storageRoot?: string }) => Promise<Pick<DaemonState, 'port'>>
  clientFor?: (state: Pick<DaemonState, 'port'>) => PairingCompleter
  /** Injectable pour les tests : enregistrement MCP + hooks. */
  registrar?: (host: string, instanceId: string, opts: { token?: string; storageRoot?: string }) => RegisterResult
}

export interface ConnectResult {
  instanceId: string
  assistantType: string
  credentialsPath: string
  storageRoot: string
  registration: RegisterResult | null
  /** Message complet en français, prêt à imprimer (bin.ts). */
  message: string
}

export async function connect(opts: ConnectOptions): Promise<ConnectResult> {
  const code = opts.code.trim()
  if (!code) throw new Error('code de pairing manquant (--code XXXX-XXXX)')

  const { storageRoot } = resolveStorageRoot(
    opts.storageRoot !== undefined ? { storageRoot: opts.storageRoot } : {},
  )

  const ensure = opts.ensure ?? ensureDaemon
  const state = await ensure(opts.storageRoot !== undefined ? { storageRoot: opts.storageRoot } : {})

  const client = opts.clientFor ? opts.clientFor(state) : new DaemonClient(state)
  const done = await client.completePairing(code)
  const assistantType = done.assistant_type ?? 'generic'

  const credentialsPath = saveCredentials(
    done.assistant_instance_id,
    {
      instance_token: done.instance_token,
      storage_root: storageRoot,
      created_at: nowISO(),
      assistant_type: assistantType,
    },
    opts.credentialsDir ?? defaultCredentialsDir(),
  )

  // Enregistrement AUTOMATIQUE du serveur MCP (sauf --no-register).
  let registration: RegisterResult | null = null
  if (opts.register !== false) {
    const registrar = opts.registrar ?? autoRegister
    registration = registrar(assistantType, done.assistant_instance_id, { token: done.instance_token, storageRoot })
  }

  const lines = [
    `✓ Agent connecté à Memoria — ${assistantType} (instance ${done.assistant_instance_id})`,
    `  Token : ${credentialsPath} (chmod 600)`,
    `  Stockage : ${storageRoot}`,
  ]
  if (registration) {
    lines.push(
      '',
      registration.registered
        ? `✓ ${registration.detail}`
        : `⚠ Enregistrement automatique non effectué : ${registration.detail}`,
    )
    if (registration.registered) {
      lines.push('  Redémarre ton agent (Claude Code / Codex) pour activer la mémoire.')
    }
  } else {
    const inv = serveInvocation(done.assistant_instance_id)
    lines.push('', 'Enregistrement manuel (—-no-register) :', `    ${inv.command} ${inv.args.join(' ')}`)
  }

  return {
    instanceId: done.assistant_instance_id,
    assistantType,
    credentialsPath,
    storageRoot,
    registration,
    message: lines.join('\n'),
  }
}
