/**
 * Mise à jour de l'installation Memoria depuis l'UI (« bouton Mise à jour »).
 * Tire la dernière version (git), réinstalle + reconstruit, puis redémarre le
 * daemon. Pensé pour un non-dev (Badette sur l'iMac) : un clic, pas de terminal.
 *
 * Best-effort et HONNÊTE : renvoie le log réel ; si ce n'est pas un dépôt git
 * (paquet npm publié plus tard), le dit clairement au lieu d'échouer en silence.
 */
import { execFile } from 'node:child_process'
import { spawn } from 'node:child_process'
import { existsSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'
import { promisify } from 'node:util'

const run = promisify(execFile)

/** Racine du monorepo (server.js vit dans packages/daemon/dist/). */
export function repoRoot(): string {
  return fileURLToPath(new URL('../../../', import.meta.url))
}

export interface UpdateResult {
  ok: boolean
  is_git: boolean
  before: string | null
  after: string | null
  changed: boolean
  log: string
  message: string
}

async function gitSha(dir: string): Promise<string | null> {
  try {
    const { stdout } = await run('git', ['-C', dir, 'rev-parse', '--short', 'HEAD'])
    return stdout.trim()
  } catch {
    return null
  }
}

export async function currentVersion(): Promise<{ version: string; sha: string | null; is_git: boolean }> {
  const dir = repoRoot()
  const sha = await gitSha(dir)
  let version = '0.1.0'
  try {
    const pkg = JSON.parse((await run('cat', [join(dir, 'package.json')])).stdout) as { version?: string }
    if (pkg.version) version = pkg.version
  } catch {
    /* garde le défaut */
  }
  return { version, sha, is_git: sha !== null }
}

/**
 * Tire + reconstruit. Ne redémarre PAS lui-même (l'appelant décide) : on renvoie
 * le résultat d'abord pour que l'UI l'affiche, puis le daemon planifie son redémarrage.
 */
export async function pullAndBuild(): Promise<UpdateResult> {
  const dir = repoRoot()
  if (!existsSync(join(dir, '.git'))) {
    return { ok: false, is_git: false, before: null, after: null, changed: false, log: '', message: 'Installation non-git (paquet figé) — mets à jour via ton gestionnaire de paquets.' }
  }
  const before = await gitSha(dir)
  const log: string[] = []
  try {
    const pull = await run('git', ['-C', dir, 'pull', '--ff-only'], { timeout: 120_000 })
    log.push(pull.stdout.trim())
    const after = await gitSha(dir)
    const changed = before !== after
    if (changed) {
      const install = await run('npm', ['install', '--prefix', dir, '--no-audit', '--no-fund'], { timeout: 600_000 })
      log.push(install.stdout.trim().split('\n').slice(-3).join('\n'))
      const build = await run('npm', ['run', 'build', '--prefix', dir], { timeout: 600_000 })
      log.push(build.stdout.trim().split('\n').slice(-3).join('\n'))
    }
    return {
      ok: true,
      is_git: true,
      before,
      after,
      changed,
      log: log.join('\n'),
      message: changed ? `Mis à jour ${before} → ${after}. Redémarrage du service…` : 'Déjà à jour.',
    }
  } catch (err) {
    return { ok: false, is_git: true, before, after: before, changed: false, log: log.join('\n'), message: `Échec de la mise à jour : ${(err as Error).message}` }
  }
}

/**
 * Planifie un redémarrage du daemon APRÈS la réponse HTTP : un process détaché
 * attend ~1,5 s (le temps que la réponse parte + ce daemon s'arrête) puis relance
 * `memoria start`. Survit à la mort du parent (detached + unref).
 */
export function scheduleRestart(storageRoot: string): void {
  const cliBin = fileURLToPath(new URL('../../cli/dist/bin.js', import.meta.url))
  if (!existsSync(cliBin)) return
  const node = process.execPath
  // STOP (libère le lock + vide daemon.json) puis START : le nouveau process
  // charge le BUILD fraîchement reconstruit. Détaché → survit à notre arrêt.
  const script =
    `sleep 1; "${node}" "${cliBin}" stop --storage-root "${storageRoot}" >/dev/null 2>&1; ` +
    `sleep 1; "${node}" "${cliBin}" start --storage-root "${storageRoot}" >/dev/null 2>&1`
  const child = spawn('/bin/sh', ['-c', script], { detached: true, stdio: 'ignore', cwd: dirname(cliBin) })
  child.unref()
}
