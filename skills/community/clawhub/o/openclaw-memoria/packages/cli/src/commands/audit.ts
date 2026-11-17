/**
 * `memoria audit` — journal d'audit neutre (jamais de contenu, hashes seulement).
 */
import type { Writable } from 'node:stream'
import { Command, Option } from 'clipanion/lib/advanced/index.js'
import type { AuditEntry } from '@memoria/core'
import { fail, findAliveDaemon, withLocalMemoria } from '../index.js'

export class AuditCommand extends Command {
  static override paths = [['audit']]
  static override usage = Command.Usage({
    description: 'Affiche le journal d’audit (actions, acteurs, hashes — jamais de contenu).',
  })

  limit = Option.String('--limit', '50', { description: 'Nombre d’entrées à afficher (défaut : 50, max 200)' })
  storageRoot = Option.String('--storage-root', { description: 'Racine du stockage (défaut : résolution standard)' })
  config = Option.String('--config', { description: 'Fichier de découverte (défaut : ~/.memoria/config.toml)' })

  override async execute(): Promise<number> {
    const opts = { storageRoot: this.storageRoot, configPath: this.config }
    const out = this.context.stdout
    const limit = Number.parseInt(this.limit, 10)
    if (!Number.isFinite(limit) || limit <= 0) {
      return fail(this.context.stderr, `audit : --limit invalide « ${this.limit} »`)
    }
    try {
      const daemon = await findAliveDaemon(opts)
      let entries: AuditEntry[]
      if (daemon) {
        // La route renvoie les 200 dernières entrées ; on tronque côté client.
        entries = ((await daemon.client.audit()) as { entries: AuditEntry[] }).entries
      } else {
        out.write('⚠ note : daemon arrêté — lecture locale directe\n')
        entries = withLocalMemoria(opts, memoria => memoria.registry.auditTail(Math.min(limit, 200)))
      }
      renderAudit(out, entries.slice(0, limit))
      return 0
    } catch (err) {
      return fail(this.context.stderr, `audit : ${(err as Error).message}`)
    }
  }
}

function renderAudit(out: Writable, entries: AuditEntry[]): void {
  if (entries.length === 0) {
    out.write('Journal d’audit vide.\n')
    return
  }
  for (const entry of entries) {
    const actor = `${entry.actor_type}:${entry.actor_id.slice(0, 8)}`
    const target = entry.target_id_hash ? ` cible=${entry.target_id_hash.slice(0, 12)}…` : ''
    const scope = entry.scope_id ? ` scope=${entry.scope_id.slice(0, 8)}` : ''
    const reason = entry.reason ? ` (${entry.reason})` : ''
    out.write(`${entry.ts}  ${entry.action.padEnd(18)} ${actor}${target}${scope}${reason}\n`)
  }
  out.write(`\n${entries.length} entrée(s) — audit neutre : actions et hashes, jamais de contenu.\n`)
}
