/**
 * Coffre natif macOS via `/usr/bin/security` (spec §9, D2).
 * ⚠ TOUJOURS execFileSync avec arguments séparés — jamais d'interpolation
 * shell : un nom ou une valeur de secret ne doit pas pouvoir injecter une
 * commande.
 */
import { execFileSync } from 'node:child_process'
import { existsSync } from 'node:fs'
import type { SecretProvider } from './types.js'

const SECURITY_BIN = '/usr/bin/security'

/** Erreur levée par execFileSync (status + stderr du process fils). */
interface ExecError {
  status?: number | null
  stderr?: string | Buffer
  message?: string
}

function stderrOf(err: unknown): string {
  const e = err as ExecError
  if (typeof e.stderr === 'string') return e.stderr
  if (Buffer.isBuffer(e.stderr)) return e.stderr.toString('utf8')
  return e.message ?? String(err)
}

/** `security` signale l'absence d'un item par ce libellé (errSecItemNotFound). */
function isNotFound(err: unknown): boolean {
  return stderrOf(err).includes('could not be found')
}

export interface KeychainMacOptions {
  /** Service keychain (défaut `memoria`) — surchargé uniquement par les tests. */
  service?: string
}

export class KeychainMacProvider implements SecretProvider {
  readonly kind = 'keychain-macos'
  private readonly service: string

  constructor(opts: KeychainMacOptions = {}) {
    this.service = opts.service ?? 'memoria'
  }

  isAvailable(): boolean {
    return process.platform === 'darwin' && existsSync(SECURITY_BIN)
  }

  set(name: string, value: string): void {
    // -U = update si l'item existe déjà (sinon `security` refuse le doublon).
    execFileSync(
      SECURITY_BIN,
      ['add-generic-password', '-U', '-s', this.service, '-a', name, '-w', value],
      { stdio: ['ignore', 'pipe', 'pipe'] },
    )
  }

  get(name: string): string | null {
    try {
      const out = execFileSync(
        SECURITY_BIN,
        ['find-generic-password', '-s', this.service, '-a', name, '-w'],
        { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] },
      )
      // `security -w` ajoute un \n final — on ne retire QUE celui-là.
      return out.replace(/\n$/, '')
    } catch (err) {
      if (isNotFound(err)) return null // contrat : null si absent
      console.warn(`[memoria] keychain get('${name}') a échoué : ${stderrOf(err).trim()}`)
      return null
    }
  }

  delete(name: string): void {
    try {
      execFileSync(
        SECURITY_BIN,
        ['delete-generic-password', '-s', this.service, '-a', name],
        { stdio: ['ignore', 'pipe', 'pipe'] },
      )
    } catch (err) {
      if (isNotFound(err)) return // delete idempotent : absent = déjà supprimé
      console.warn(`[memoria] keychain delete('${name}') a échoué : ${stderrOf(err).trim()}`)
    }
  }

  locationFor(name: string): string {
    return `keychain:${this.service}/${name}`
  }
}
