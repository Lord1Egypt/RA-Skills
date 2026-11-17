/**
 * `memoria doctor` — santé du stockage. Via HTTP admin si le daemon vit,
 * sinon lecture locale directe avec la note « daemon arrêté ».
 */
import { relative } from 'node:path'
import type { Writable } from 'node:stream'
import { Command, Option } from 'clipanion/lib/advanced/index.js'
import type { DoctorReport } from '@memoria/core'
import { fail, findAliveDaemon, formatBytes, withLocalMemoria } from '../index.js'

export class DoctorCommand extends Command {
  static override paths = [['doctor']]
  static override usage = Command.Usage({
    description: 'Vérifie la santé du stockage Memoria (DB, garde réseau, WAL).',
  })

  storageRoot = Option.String('--storage-root', { description: 'Racine du stockage (défaut : résolution standard)' })
  config = Option.String('--config', { description: 'Fichier de découverte (défaut : ~/.memoria/config.toml)' })

  override async execute(): Promise<number> {
    const opts = { storageRoot: this.storageRoot, configPath: this.config }
    try {
      const daemon = await findAliveDaemon(opts)
      let report: DoctorReport
      let note: string | null = null
      if (daemon) {
        report = (await daemon.client.doctor()) as DoctorReport
      } else {
        note = 'daemon arrêté — lecture locale directe'
        report = withLocalMemoria(opts, memoria => memoria.doctor())
      }
      renderDoctor(this.context.stdout, report, note)
      // Le rapport EST le livrable : avertissements ≠ échec de la commande.
      return 0
    } catch (err) {
      return fail(this.context.stderr, `doctor : ${(err as Error).message}`)
    }
  }
}

function renderDoctor(out: Writable, report: DoctorReport, note: string | null): void {
  out.write(`Memoria doctor — ${report.storage_root}\n`)
  if (note) out.write(`⚠ note : ${note}\n`)
  out.write('\n')
  out.write(`✓ config : ${report.config_path}\n`)

  for (const db of report.databases) {
    const label = db.kind === 'registry' ? 'registre' : `db ${db.kind}`
    const path = relativeOrAbsolute(report.storage_root, db.path)
    if (!db.exists) {
      out.write(`⚠ ${label} : ${path} — enregistrée mais absente du disque\n`)
      continue
    }
    const wal = db.wal_pending !== undefined ? `, wal_pending=${db.wal_pending}` : ''
    out.write(`✓ ${label} : ${path} (${formatBytes(db.size_bytes)}${wal})\n`)
  }

  const guard = report.network_guard
  if (guard.on_network_volume) {
    out.write(`⚠ garde réseau : volume réseau/synchronisé détecté (journal_mode=${guard.journal_mode})\n`)
  } else {
    out.write(`✓ garde réseau : volume local (journal_mode=${guard.journal_mode})\n`)
  }

  if (report.warnings.length > 0) {
    out.write('\nAvertissements :\n')
    for (const warning of report.warnings) out.write(`  ⚠ ${warning}\n`)
  }
  out.write('\n')
  out.write(report.ok ? 'État : ✓ OK\n' : `État : ⚠ ${report.warnings.length} avertissement(s)\n`)
}

function relativeOrAbsolute(root: string, path: string): string {
  const rel = relative(root, path)
  return rel === '' || rel.startsWith('..') ? path : rel
}
