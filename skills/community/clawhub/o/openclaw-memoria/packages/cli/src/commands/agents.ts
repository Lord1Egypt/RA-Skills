/**
 * `memoria agents` — liste les instances connectées (type, machine, vu pour la
 * dernière fois, état). `memoria revoke <instance_id>` — coupe une instance.
 */
import type { Writable } from 'node:stream'
import { Command, Option } from 'clipanion/lib/advanced/index.js'
import type { AssistantInstance } from '@memoria/core'
import { fail, findAliveDaemon, humanizeSince, withLocalMemoria } from '../index.js'

/** Forme renvoyée par GET /v1/admin/agents (= Memoria.listAgents()). */
interface AgentEntry {
  instance: AssistantInstance
  assistant_type: string
  db_path: string | null
}

export class AgentsCommand extends Command {
  static override paths = [['agents']]
  static override usage = Command.Usage({
    description: 'Liste les instances d’assistants connues (type, machine, dernière activité, état).',
  })

  storageRoot = Option.String('--storage-root', { description: 'Racine du stockage (défaut : résolution standard)' })
  config = Option.String('--config', { description: 'Fichier de découverte (défaut : ~/.memoria/config.toml)' })

  override async execute(): Promise<number> {
    const opts = { storageRoot: this.storageRoot, configPath: this.config }
    const out = this.context.stdout
    try {
      const daemon = await findAliveDaemon(opts)
      let entries: AgentEntry[]
      if (daemon) {
        entries = ((await daemon.client.agents()) as { agents: AgentEntry[] }).agents
      } else {
        out.write('⚠ note : daemon arrêté — lecture locale directe\n')
        entries = withLocalMemoria(opts, memoria => memoria.listAgents())
      }
      renderAgents(out, entries)
      return 0
    } catch (err) {
      return fail(this.context.stderr, `agents : ${(err as Error).message}`)
    }
  }
}

function renderAgents(out: Writable, entries: AgentEntry[]): void {
  if (entries.length === 0) {
    out.write('Aucune instance connectée — « memoria pair <type> » pour connecter un agent.\n')
    return
  }
  const rows = entries.map(e => [
    e.assistant_type,
    e.instance.machine_id,
    humanizeSince(e.instance.last_seen_at),
    e.instance.revoked_at ? 'révoqué' : 'actif',
    e.instance.id,
  ])
  const header = ['TYPE', 'MACHINE', 'VU', 'ÉTAT', 'INSTANCE']
  const widths = header.map((h, i) => Math.max(h.length, ...rows.map(r => (r[i] ?? '').length)))
  const line = (cols: string[]): string =>
    cols.map((c, i) => c.padEnd(widths[i] ?? c.length)).join('  ').trimEnd() + '\n'
  out.write(line(header))
  for (const row of rows) out.write(line(row))
  out.write(`\n${entries.length} instance(s) — « memoria revoke <instance_id> » pour en couper une.\n`)
}

export class RevokeCommand extends Command {
  static override paths = [['revoke']]
  static override usage = Command.Usage({
    description: 'Révoque une instance d’assistant : son token n’est plus accepté.',
  })

  instanceId = Option.String({ required: true })
  storageRoot = Option.String('--storage-root', { description: 'Racine du stockage (défaut : résolution standard)' })
  config = Option.String('--config', { description: 'Fichier de découverte (défaut : ~/.memoria/config.toml)' })

  override async execute(): Promise<number> {
    const opts = { storageRoot: this.storageRoot, configPath: this.config }
    const out = this.context.stdout
    try {
      const daemon = await findAliveDaemon(opts)
      if (daemon) {
        // Vérifie l'existence avant : la route revoke ne se plaint pas d'un id inconnu.
        const { agents } = (await daemon.client.agents()) as { agents: AgentEntry[] }
        if (!agents.some(a => a.instance.id === this.instanceId)) {
          return fail(this.context.stderr, `revoke : instance inconnue « ${this.instanceId} » (voir memoria agents)`)
        }
        await daemon.client.revoke(this.instanceId)
      } else {
        out.write('⚠ note : daemon arrêté — révocation locale directe\n')
        const known = withLocalMemoria(opts, memoria => {
          if (!memoria.registry.getInstance(this.instanceId)) return false
          memoria.revokeInstance(this.instanceId)
          return true
        })
        if (!known) {
          return fail(this.context.stderr, `revoke : instance inconnue « ${this.instanceId} » (voir memoria agents)`)
        }
      }
      out.write(`✓ Instance révoquée : ${this.instanceId} — son token n’est plus accepté.\n`)
      return 0
    } catch (err) {
      return fail(this.context.stderr, `revoke : ${(err as Error).message}`)
    }
  }
}

export class DeleteAgentCommand extends Command {
  static override paths = [['delete-agent']]
  static override usage = Command.Usage({
    description: 'Supprime DÉFINITIVEMENT un agent : révoque + efface sa mémoire privée (irréversible, ≠ revoke).',
  })

  instanceId = Option.String({ required: true })
  yes = Option.Boolean('--yes', false, { description: 'Confirme la suppression sans question.' })
  storageRoot = Option.String('--storage-root', { description: 'Racine du stockage (défaut : résolution standard)' })
  config = Option.String('--config', { description: 'Fichier de découverte (défaut : ~/.memoria/config.toml)' })

  override async execute(): Promise<number> {
    const opts = { storageRoot: this.storageRoot, configPath: this.config }
    const out = this.context.stdout
    if (!this.yes) {
      return fail(
        this.context.stderr,
        `delete-agent : action IRRÉVERSIBLE (efface la mémoire privée de l’agent). Relance avec --yes pour confirmer.`,
      )
    }
    try {
      const daemon = await findAliveDaemon(opts)
      let deleted: boolean
      if (daemon) {
        deleted = ((await daemon.client.deleteAgent(this.instanceId)) as { deleted: boolean }).deleted
      } else {
        out.write('⚠ note : daemon arrêté — suppression locale directe\n')
        deleted = withLocalMemoria(opts, memoria => memoria.deleteInstance(this.instanceId).deleted)
      }
      if (!deleted) return fail(this.context.stderr, `delete-agent : instance inconnue « ${this.instanceId} » (voir memoria agents)`)
      out.write(`✓ Agent supprimé définitivement : ${this.instanceId} (mémoire privée effacée).\n`)
      return 0
    } catch (err) {
      return fail(this.context.stderr, `delete-agent : ${(err as Error).message}`)
    }
  }
}
