/**
 * @memoria/cli — `memoria`, le CLI humain (spec §2.1). Client du daemon :
 * chaque commande passe par HTTP admin quand le daemon vit, sinon bascule en
 * lecture locale directe ANNONCÉE (note « daemon arrêté ») — jamais en silence.
 *
 * Les helpers partagés vivent ici en déclarations `function` : les modules de
 * commandes les importent depuis '../index.js' (cycle ESM bénin — accès
 * uniquement à l'exécution, jamais pendant l'initialisation des modules).
 */
import type { Writable } from 'node:stream'
import { Builtins, Cli } from 'clipanion/lib/advanced/index.js'
import { Memoria, resolveStorageRoot } from '@memoria/core'
import { DaemonClient, readDaemonState, type DaemonState } from '@memoria/daemon'
import { AgentsCommand, DeleteAgentCommand, RevokeCommand } from './commands/agents.js'
import { AuditCommand } from './commands/audit.js'
import { AutostartCommand, DisableCommand, EnableCommand, MoveCommand, UpdateCommand } from './commands/control.js'
import { DaemonCommand, StartCommand, StopCommand } from './commands/daemon.js'
import {
  SyncInitHubCommand,
  SyncInviteCommand,
  SyncJoinCommand,
  SyncLeaveCommand,
  SyncNowCommand,
  SyncRevokeCommand,
  SyncStatusCommand,
} from './commands/sync.js'
import { DoctorCommand } from './commands/doctor.js'
import { ExportCommand } from './commands/export.js'
import { ForgetCommand } from './commands/forget.js'
import { ImportCommand } from './commands/import.js'
import { InitCommand } from './commands/init.js'
import { PairCommand } from './commands/pair.js'
import { StatsCommand } from './commands/stats.js'
import { UiCommand } from './commands/ui.js'

export const CLI_VERSION = '0.1.0'

export {
  AgentsCommand,
  AuditCommand,
  AutostartCommand,
  DaemonCommand,
  DeleteAgentCommand,
  DisableCommand,
  DoctorCommand,
  EnableCommand,
  ExportCommand,
  ForgetCommand,
  InitCommand,
  MoveCommand,
  PairCommand,
  RevokeCommand,
  StartCommand,
  StatsCommand,
  StopCommand,
  UiCommand,
}

/** Options communes à toutes les commandes (`--storage-root`, `--config`). */
export interface CommonOptions {
  storageRoot?: string | undefined
  configPath?: string | undefined
}

/** Racine + config résolues par LE résolveur unique du core. */
export function resolveCommon(opts: CommonOptions): { storageRoot: string; configPath: string } {
  const resolved = resolveStorageRoot({ storageRoot: opts.storageRoot, configPath: opts.configPath })
  return { storageRoot: resolved.storageRoot, configPath: resolved.configPath }
}

/**
 * Daemon vivant pour cette racine ? `{ state, client admin }` si oui, sinon
 * null. `health()` encaisse l'absence de réponse : daemon arrêté = cas attendu
 * (les commandes l'affichent, elles ne le masquent pas).
 */
export async function findAliveDaemon(
  opts: CommonOptions,
): Promise<{ state: DaemonState; client: DaemonClient } | null> {
  const { storageRoot } = resolveCommon(opts)
  const state = readDaemonState(storageRoot)
  if (!state) return null
  const client = new DaemonClient(state, state.admin_token)
  if (!(await client.health())) return null
  return { state, client }
}

/**
 * Ouvre le moteur en local et garantit `close()`. À n'utiliser que quand le
 * daemon est arrêté (sinon deux processus écriraient les mêmes DB).
 */
export function withLocalMemoria<T>(opts: CommonOptions, fn: (memoria: Memoria) => T): T {
  const memoria = Memoria.init({ storageRoot: opts.storageRoot, configPath: opts.configPath })
  try {
    return fn(memoria)
  } finally {
    memoria.close()
  }
}

/** Erreur ATTENDUE : message propre sur stderr + code 1 — jamais de stack brute. */
export function fail(stderr: Writable, message: string): number {
  stderr.write(`✗ ${message}\n`)
  return 1
}

export function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} o`
  const units = ['Ko', 'Mo', 'Go', 'To'] as const
  let value = bytes / 1024 // première division = Ko (index 0)
  let unit = 0
  while (value >= 1024 && unit < units.length - 1) {
    value /= 1024
    unit++
  }
  const rounded = value >= 100 ? Math.round(value) : Math.round(value * 10) / 10
  return `${rounded} ${units[unit] as string}`
}

/** « il y a 3 min » / « jamais » — pour la colonne "vu" de `memoria agents`. */
export function humanizeSince(iso: string | null): string {
  if (!iso) return 'jamais'
  const ts = new Date(iso).getTime()
  if (!Number.isFinite(ts)) return iso
  const deltaMs = Date.now() - ts
  if (deltaMs < 60_000) return 'à l’instant'
  const minutes = Math.floor(deltaMs / 60_000)
  if (minutes < 60) return `il y a ${minutes} min`
  const hours = Math.floor(minutes / 60)
  if (hours < 48) return `il y a ${hours} h`
  const days = Math.floor(hours / 24)
  if (days < 60) return `il y a ${days} j`
  return iso.slice(0, 10)
}

/** CLI complet (utilisé par bin.ts et les tests). */
export function buildCli(): Cli {
  const cli = new Cli({
    binaryLabel: 'Memoria',
    binaryName: 'memoria',
    binaryVersion: CLI_VERSION,
  })
  cli.register(Builtins.HelpCommand)
  cli.register(Builtins.VersionCommand)
  cli.register(InitCommand)
  cli.register(UiCommand) // aussi commande par défaut (`memoria` seul = `memoria ui`)
  cli.register(DaemonCommand)
  cli.register(StartCommand)
  cli.register(StopCommand)
  cli.register(DoctorCommand)
  cli.register(ExportCommand)
  cli.register(PairCommand)
  cli.register(AgentsCommand)
  cli.register(RevokeCommand)
  cli.register(DeleteAgentCommand)
  cli.register(StatsCommand)
  cli.register(ForgetCommand)
  cli.register(ImportCommand)
  cli.register(AuditCommand)
  cli.register(EnableCommand)
  cli.register(DisableCommand)
  cli.register(AutostartCommand)
  cli.register(MoveCommand)
  cli.register(UpdateCommand)
  cli.register(SyncStatusCommand)
  cli.register(SyncInitHubCommand)
  cli.register(SyncInviteCommand)
  cli.register(SyncJoinCommand)
  cli.register(SyncNowCommand)
  cli.register(SyncRevokeCommand)
  cli.register(SyncLeaveCommand)
  return cli
}
