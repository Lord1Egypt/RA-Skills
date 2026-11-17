/**
 * Credentials d'instance (issus du pairing) — `~/.memoria/credentials/<instance_id>.json`.
 * Le token d'instance est un secret local : fichier chmod 600, dossier chmod 700.
 * Le répertoire est injectable pour les tests (jamais le vrai HOME en test).
 *
 * DÉPLACÉ depuis @memoria/mcp vers @memoria/core (mission B2) : le daemon écrit
 * lui-même les credentials lors de la connexion 1 clic (POST /v1/admin/agents_connect).
 * @memoria/mcp ré-exporte ce module (API publique inchangée).
 */
import { chmodSync, existsSync, mkdirSync, readdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs'
import { homedir } from 'node:os'
import { join } from 'node:path'

export interface InstanceCredentials {
  instance_token: string
  storage_root: string
  created_at: string
  /** Type d'hôte (claude-code/codex/openclaw) — pour le désenregistrement. */
  assistant_type?: string
}

/** Liste les instances ayant des credentials locaux. */
export function listCredentials(dir: string = defaultCredentialsDir()): string[] {
  if (!existsSync(dir)) return []
  try {
    return readdirSync(dir)
      .filter(f => f.endsWith('.json'))
      .map(f => f.slice(0, -'.json'.length))
  } catch {
    return []
  }
}

export function deleteCredentials(instanceId: string, dir: string = defaultCredentialsDir()): boolean {
  const p = credentialsPath(instanceId, dir)
  if (!existsSync(p)) return false
  rmSync(p, { force: true })
  return true
}

export function defaultCredentialsDir(): string {
  return join(homedir(), '.memoria', 'credentials')
}

export function credentialsPath(instanceId: string, dir: string = defaultCredentialsDir()): string {
  return join(dir, `${instanceId}.json`)
}

export function saveCredentials(
  instanceId: string,
  creds: InstanceCredentials,
  dir: string = defaultCredentialsDir(),
): string {
  // l'id sert de nom de fichier : refuser tout séparateur de chemin
  if (!/^[A-Za-z0-9_.@-]+$/.test(instanceId)) {
    throw new Error(`identifiant d'instance invalide : ${instanceId}`)
  }
  mkdirSync(dir, { recursive: true, mode: 0o700 })
  const p = credentialsPath(instanceId, dir)
  writeFileSync(p, JSON.stringify(creds, null, 2), 'utf8')
  chmodSync(p, 0o600)
  return p
}

export function loadCredentials(
  instanceId: string,
  dir: string = defaultCredentialsDir(),
): InstanceCredentials | null {
  const p = credentialsPath(instanceId, dir)
  if (!existsSync(p)) return null
  try {
    const parsed = JSON.parse(readFileSync(p, 'utf8')) as Partial<InstanceCredentials>
    if (typeof parsed.instance_token !== 'string' || typeof parsed.storage_root !== 'string') {
      console.warn(`[memoria] credentials incomplets, fichier ignoré : ${p}`)
      return null
    }
    return {
      instance_token: parsed.instance_token,
      storage_root: parsed.storage_root,
      created_at: typeof parsed.created_at === 'string' ? parsed.created_at : '',
      assistant_type: typeof parsed.assistant_type === 'string' ? parsed.assistant_type : undefined,
    }
  } catch (err) {
    // anti « mort silencieuse » : un fichier corrompu doit se voir
    console.warn(`[memoria] credentials illisibles (${p}) : ${(err as Error).message}`)
    return null
  }
}
