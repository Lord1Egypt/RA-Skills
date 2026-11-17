/**
 * `memoria-mcp disconnect [--instance <id>]` — déconnexion SIMPLE et complète :
 *  1. retire le serveur MCP de la config de l'hôte (Claude Code / Codex…) ;
 *  2. révoque l'instance côté daemon (le token ne vaut plus rien) ;
 *  3. supprime les credentials locaux.
 * Sans --instance : déconnecte la seule instance connue, ou demande de préciser.
 */
import { resolveStorageRoot } from '@memoria/core'
import { DaemonClient, readDaemonState, type DaemonState } from '@memoria/daemon'
import { deleteCredentials, defaultCredentialsDir, listCredentials, loadCredentials } from './credentials.js'
import { autoUnregister, type RegisterResult } from './register.js'

export interface DisconnectOptions {
  instanceId?: string
  storageRoot?: string
  credentialsDir?: string
  /** Injectables pour les tests. */
  stateFor?: (storageRoot: string) => DaemonState | null
  revoker?: (state: DaemonState, instanceId: string) => Promise<void>
  unregistrar?: (host: string) => RegisterResult
}

export interface DisconnectResult {
  instanceId: string
  unregistration: RegisterResult
  revoked: boolean
  credentialsDeleted: boolean
  message: string
}

export async function disconnect(opts: DisconnectOptions = {}): Promise<DisconnectResult> {
  const dir = opts.credentialsDir ?? defaultCredentialsDir()

  const requested = opts.instanceId?.trim()
  let instanceId: string
  if (requested) {
    instanceId = requested
  } else {
    const known = listCredentials(dir)
    if (known.length === 0) throw new Error('aucun agent connecté (aucun credential local).')
    if (known.length > 1) {
      throw new Error(`plusieurs agents connectés — précise --instance <id> parmi : ${known.join(', ')}`)
    }
    instanceId = known[0]!
  }

  const creds = loadCredentials(instanceId, dir)
  const host = creds?.assistant_type ?? 'generic'

  // 1. retirer l'enregistrement MCP de l'hôte
  const unregistrar = opts.unregistrar ?? autoUnregister
  const unregistration = unregistrar(host)

  // 2. révoquer l'instance côté daemon (best-effort : si le daemon est éteint,
  //    on continue le nettoyage local — l'instance sera de toute façon inutile).
  const { storageRoot } = resolveStorageRoot(opts.storageRoot !== undefined ? { storageRoot: opts.storageRoot } : {})
  const state = opts.stateFor ? opts.stateFor(storageRoot) : readDaemonState(storageRoot)
  let revoked = false
  if (state) {
    try {
      if (opts.revoker) {
        await opts.revoker(state, instanceId)
      } else {
        await new DaemonClient(state, state.admin_token).revoke(instanceId)
      }
      revoked = true
    } catch (err) {
      console.warn(`[memoria-mcp] révocation côté daemon échouée (${(err as Error).message}) — nettoyage local poursuivi`)
    }
  }

  // 3. supprimer les credentials locaux
  const credentialsDeleted = deleteCredentials(instanceId, dir)

  const message = [
    `✓ Agent déconnecté — ${host} (instance ${instanceId})`,
    `  ${unregistration.detail}`,
    revoked ? '  Instance révoquée côté Memoria.' : '  (daemon arrêté ou instance déjà révoquée)',
    credentialsDeleted ? '  Credentials locaux supprimés.' : '  (pas de credentials locaux à supprimer)',
  ].join('\n')

  return { instanceId, unregistration, revoked, credentialsDeleted, message }
}
