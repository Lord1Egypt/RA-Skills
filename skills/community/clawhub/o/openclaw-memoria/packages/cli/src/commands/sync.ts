/**
 * `memoria sync …` — synchro inter-machines (SYNC-INTER-MACHINES.md).
 *
 *   memoria sync init-hub [--listen 0.0.0.0:47600]   désigne CETTE machine comme hub
 *   memoria sync invite [--name "Luna (iMac)"]        code one-shot à donner au spoke
 *   memoria sync join --hub <ip:port> --code XXXX      relie CETTE machine au hub (+ bootstrap)
 *   memoria sync now | status | peers | revoke <id> | leave
 *
 * Toutes passent par le daemon (il détient les DB). Le join/bootstrap réel
 * tourne DANS le daemon (accès réseau + écriture registry/scopes).
 */
import { Command, Option } from 'clipanion/lib/advanced/index.js'
import { fail, findAliveDaemon } from '../index.js'

abstract class SyncBase extends Command {
  storageRoot = Option.String('--storage-root', { description: 'Racine du stockage' })
  config = Option.String('--config', { description: 'Fichier de découverte' })

  protected async daemon() {
    const d = await findAliveDaemon({ storageRoot: this.storageRoot, configPath: this.config })
    if (!d) throw new Error('daemon arrêté — lance « memoria start » d’abord (la synchro vit dans le daemon).')
    return d
  }
}

export class SyncStatusCommand extends SyncBase {
  static override paths = [['sync', 'status'], ['sync']]
  static override usage = Command.Usage({ description: 'État de la synchro inter-machines (rôle, hub, pairs).' })
  override async execute(): Promise<number> {
    try {
      const { client } = await this.daemon()
      const s = (await client.syncStatus()) as { enabled: boolean; role: string; machine_id: string; hub: string | null; listen_lan: string | null; peers: Array<{ display_name: string; role: string; machine_id: string; last_seen_at: string | null; revoked_at: string | null }> }
      const out = this.context.stdout
      out.write(`Synchro : ${s.enabled ? 'activée' : 'désactivée'} · rôle ${s.role} · machine ${s.machine_id}\n`)
      if (s.role === 'hub') out.write(`  écoute LAN : ${s.listen_lan ?? '(non configuré)'}\n`)
      if (s.role === 'spoke') out.write(`  hub : ${s.hub ?? '(aucun)'}\n`)
      if (s.peers.length === 0) out.write('  aucun pair.\n')
      for (const p of s.peers) out.write(`  • ${p.display_name} [${p.role}] ${p.revoked_at ? '(révoqué)' : ''} — ${p.machine_id}\n`)
      return 0
    } catch (err) {
      return fail(this.context.stderr, `sync status : ${(err as Error).message}`)
    }
  }
}

export class SyncInitHubCommand extends SyncBase {
  static override paths = [['sync', 'init-hub']]
  static override usage = Command.Usage({ description: 'Désigne cette machine comme HUB de synchro (redémarrage requis).' })
  listen = Option.String('--listen', { description: 'Adresse d’écoute LAN (défaut 0.0.0.0:47600)' })
  override async execute(): Promise<number> {
    try {
      const { client } = await this.daemon()
      const r = (await client.syncInitHub(this.listen ?? '0.0.0.0:47600')) as { listen_lan: string; machine_id: string }
      this.context.stdout.write(`✓ Hub configuré (écoute ${r.listen_lan}, machine ${r.machine_id}).\n  Redémarre : memoria stop && memoria start — puis « memoria sync invite ».\n`)
      return 0
    } catch (err) {
      return fail(this.context.stderr, `sync init-hub : ${(err as Error).message}`)
    }
  }
}

export class SyncInviteCommand extends SyncBase {
  static override paths = [['sync', 'invite']]
  static override usage = Command.Usage({ description: 'Génère un code one-shot pour relier une nouvelle machine (spoke).' })
  name = Option.String('--name', { description: 'Nom de la machine invitée (ex. « Luna (iMac) »)' })
  override async execute(): Promise<number> {
    try {
      const { client } = await this.daemon()
      const r = await client.syncInvite(this.name)
      this.context.stdout.write(
        `Code de synchro : ${r.code}  (valable 10 min)\n` +
          `Sur l’autre machine :\n    memoria sync join --hub ${r.hub_lan ?? '<ip-de-ce-mac>:47600'} --code ${r.code}\n`,
      )
      return 0
    } catch (err) {
      return fail(this.context.stderr, `sync invite : ${(err as Error).message}`)
    }
  }
}

export class SyncJoinCommand extends SyncBase {
  static override paths = [['sync', 'join']]
  static override usage = Command.Usage({ description: 'Relie cette machine à un hub et récupère la mémoire partagée + le coffre.' })
  hub = Option.String('--hub', { required: true, description: 'Adresse du hub « ip:port »' })
  code = Option.String('--code', { required: true, description: 'Code one-shot affiché par « memoria sync invite »' })
  override async execute(): Promise<number> {
    try {
      const { client } = await this.daemon()
      const r = await client.syncJoin(this.hub, this.code)
      this.context.stdout.write(`✓ Relié au hub. Reçu : ${r.facts} souvenirs partagés, ${r.secrets} secrets, sur ${r.scopes} espaces.\n`)
      return 0
    } catch (err) {
      return fail(this.context.stderr, `sync join : ${(err as Error).message}`)
    }
  }
}

export class SyncNowCommand extends SyncBase {
  static override paths = [['sync', 'now']]
  static override usage = Command.Usage({ description: 'Force une passe de synchro maintenant.' })
  override async execute(): Promise<number> {
    try {
      const { client } = await this.daemon()
      const r = await client.syncNow()
      this.context.stdout.write(`✓ Synchro : ${r.pulled} reçus, ${r.pushed} poussés.\n`)
      return 0
    } catch (err) {
      return fail(this.context.stderr, `sync now : ${(err as Error).message}`)
    }
  }
}

export class SyncRevokeCommand extends SyncBase {
  static override paths = [['sync', 'revoke']]
  static override usage = Command.Usage({ description: 'Révoque un pair (par machine_id).' })
  machineId = Option.String({ required: true })
  override async execute(): Promise<number> {
    try {
      const { client } = await this.daemon()
      const r = await client.syncRevoke(this.machineId)
      this.context.stdout.write(r.revoked ? `✓ Pair révoqué : ${this.machineId}\n` : `Aucun pair actif « ${this.machineId} ».\n`)
      return 0
    } catch (err) {
      return fail(this.context.stderr, `sync revoke : ${(err as Error).message}`)
    }
  }
}

export class SyncLeaveCommand extends SyncBase {
  static override paths = [['sync', 'leave']]
  static override usage = Command.Usage({ description: 'Se déconnecte du hub (garde les souvenirs déjà reçus).' })
  override async execute(): Promise<number> {
    try {
      const { client } = await this.daemon()
      await client.syncLeave()
      this.context.stdout.write('✓ Déconnecté du hub. Les souvenirs et secrets déjà reçus restent disponibles.\n')
      return 0
    } catch (err) {
      return fail(this.context.stderr, `sync leave : ${(err as Error).message}`)
    }
  }
}
