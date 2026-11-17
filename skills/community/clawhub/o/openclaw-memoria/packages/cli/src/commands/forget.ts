/**
 * `memoria forget` — hard-delete gouverné (spec §11).
 *   --id … (répétable) | --query … [--scope …] [--confirm-bulk]
 * Confirmation interactive si > 5 suppressions, sauf --yes.
 * La suppression par requête (volume inconnu d'avance) exige --confirm-bulk.
 */
import { createInterface } from 'node:readline/promises'
import type { Readable, Writable } from 'node:stream'
import { Command, Option } from 'clipanion/lib/advanced/index.js'
import type { ForgetFilter } from '@memoria/core'
import type { DaemonState } from '@memoria/daemon'
import { fail, findAliveDaemon, withLocalMemoria } from '../index.js'

const CONFIRM_THRESHOLD = 5

export class ForgetCommand extends Command {
  static override paths = [['forget']]
  static override usage = Command.Usage({
    description: 'Supprime définitivement des souvenirs (hard-delete, partout).',
    examples: [
      ['Par identifiants', 'memoria forget --id abc123 --id def456'],
      ['Par requête (suppression en masse)', 'memoria forget --query "ancien client" --confirm-bulk'],
    ],
  })

  ids = Option.Array('--id', { description: 'Identifiant de souvenir à supprimer (répétable)' })
  query = Option.String('--query', { description: 'Requête plein-texte — supprime tous les souvenirs correspondants' })
  scope = Option.String('--scope', { description: 'Restreint la requête à un scope_id' })
  confirmBulk = Option.Boolean('--confirm-bulk', false, {
    description: 'Confirme une suppression en masse (obligatoire avec --query)',
  })
  yes = Option.Boolean('--yes', false, { description: 'Saute la confirmation interactive' })
  storageRoot = Option.String('--storage-root', { description: 'Racine du stockage (défaut : résolution standard)' })
  config = Option.String('--config', { description: 'Fichier de découverte (défaut : ~/.memoria/config.toml)' })

  override async execute(): Promise<number> {
    const out = this.context.stdout
    const errOut = this.context.stderr
    const ids = this.ids ?? []

    if (ids.length === 0 && !this.query) {
      return fail(errOut, 'forget : filtre vide refusé — précise --id … (répétable) ou --query …')
    }
    if (ids.length === 0 && this.query && !this.confirmBulk) {
      return fail(errOut, 'forget : suppression par requête (volume inconnu) — ajoute --confirm-bulk pour confirmer')
    }

    if (ids.length > CONFIRM_THRESHOLD && !this.yes) {
      const stdin = this.context.stdin as Readable & { isTTY?: boolean }
      if (stdin.isTTY !== true) {
        return fail(errOut, `forget : ${ids.length} suppressions demandées — relance avec --yes (entrée non interactive)`)
      }
      const ok = await askConfirmation(stdin, out, `Supprimer ${ids.length} souvenirs ? Cette action est définitive. (o/N) `)
      if (!ok) {
        out.write('Abandon — rien n’a été supprimé.\n')
        return 1
      }
    }

    const filter: ForgetFilter = {
      ...(ids.length > 0 ? { ids } : {}),
      ...(this.query ? { query: this.query } : {}),
      ...(this.scope ? { scope_id: this.scope } : {}),
      ...(this.confirmBulk ? { confirm_bulk: true } : {}),
    }

    const opts = { storageRoot: this.storageRoot, configPath: this.config }
    try {
      const daemon = await findAliveDaemon(opts)
      let deleted: number
      if (daemon) {
        deleted = (await daemonForget(daemon.state, filter)).deleted
      } else {
        out.write('⚠ note : daemon arrêté — suppression locale directe\n')
        deleted = withLocalMemoria(opts, memoria => memoria.forget(filter)).deleted
      }
      out.write(`✓ ${deleted} souvenir(s) supprimé(s) définitivement.\n`)
      return 0
    } catch (err) {
      return fail(errOut, `forget : ${(err as Error).message}`)
    }
  }
}

/**
 * DaemonClient n'expose pas (encore) forget — appel direct de la route admin
 * POST /v1/admin/forget avec le token de daemon.json.
 */
async function daemonForget(state: DaemonState, filter: ForgetFilter): Promise<{ deleted: number }> {
  const res = await fetch(`http://127.0.0.1:${state.port}/v1/admin/forget`, {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
      authorization: `Bearer ${state.admin_token}`,
    },
    body: JSON.stringify(filter),
  })
  const payload = (await res.json().catch(() => ({}))) as Record<string, unknown>
  if (!res.ok) {
    throw new Error(`daemon /v1/admin/forget → ${res.status} : ${String(payload['error'] ?? 'erreur')}`)
  }
  return payload as { deleted: number }
}

async function askConfirmation(input: Readable, output: Writable, question: string): Promise<boolean> {
  const rl = createInterface({ input, output })
  try {
    const answer = await rl.question(question)
    return /^o(ui)?$/i.test(answer.trim())
  } finally {
    rl.close()
  }
}
