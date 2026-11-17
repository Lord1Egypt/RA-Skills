/**
 * Cœur de convergence de la synchro (SYNC §3.3). PUR et DÉTERMINISTE :
 * appliquer les mêmes deltas dans n'importe quel ordre converge vers le même
 * état sur les 3 machines. Pas de CRDT/Raft : LWW par fait suffit pour 3 nœuds.
 */
import { sha256Hex } from '../util.js'
import { normalizeText } from '../storage/content.js'

/** Sous-ensemble des champs d'un fait nécessaires au LWW. */
export interface MergeFields {
  origin_rev?: number
  updated_at: string
  origin_machine_id?: string | null
}

/** Empreinte de contenu : déduplique deux faits créés indépendamment sur 2 machines. */
export function contentHash(f: { fact: string; category: string; scope_id: string }): string {
  // normalizeText (lower + sans diacritiques) + espaces réduits → robuste à la mise en forme
  const norm = normalizeText(f.fact).replace(/\s+/g, ' ').trim()
  return sha256Hex(`${norm}|${f.category}|${f.scope_id}`)
}

/**
 * Décision LWW déterministe (spec §3.3) : l'entrant l'emporte si sa révision
 * logique est plus haute ; à révision égale, la date la plus récente ; à égalité
 * parfaite, l'id de machine le plus grand (tie-break stable → même issue partout).
 */
export function winner(local: MergeFields | undefined, incoming: MergeFields): 'apply' | 'skip' {
  if (!local) return 'apply'
  const lr = local.origin_rev ?? 0
  const ir = incoming.origin_rev ?? 0
  if (ir !== lr) return ir > lr ? 'apply' : 'skip'
  if (incoming.updated_at !== local.updated_at) return incoming.updated_at > local.updated_at ? 'apply' : 'skip'
  const lm = local.origin_machine_id ?? ''
  const im = incoming.origin_machine_id ?? ''
  if (im !== lm) return im > lm ? 'apply' : 'skip'
  return 'skip' // strictement identique → no-op (anti ping-pong)
}

/** Fait transporté sur le réseau (ligne `facts` complète, sans la télémétrie locale). */
export interface SyncFact {
  id: string
  fact: string
  category: string
  fact_type: string
  confidence: number
  source: string
  scope_id: string
  sensitivity: string
  visibility: string
  tags: string
  entity_ids: string
  lifecycle_state: string
  superseded: number
  superseded_by: string | null
  origin_machine_id: string | null
  origin_rev: number
  content_hash: string | null
  deleted_at: string | null
  created_at: string
  updated_at: string
}

export interface Tombstone {
  id: string
  deleted_at: string
  origin_machine_id: string | null
  origin_rev: number
  updated_at: string
}

/** Magasin minimal que `applyDelta` manipule (implémenté par ContentStore). */
export interface SyncStore {
  getMergeFields(id: string): (MergeFields & { id: string }) | undefined
  findIdByContentHash(hash: string): string | null
  upsertSyncedFact(f: SyncFact): void
  applyTombstone(t: Tombstone): boolean
}

export interface ApplyReport {
  applied: number
  skipped_lww: number
  deduped: number
  tombstoned: number
}

/**
 * Applique un delta entrant (faits + tombstones) de façon idempotente et
 * convergente. `myMachineId` sert à ignorer nos propres échos.
 */
export function applyDelta(store: SyncStore, facts: SyncFact[], tombstones: Tombstone[]): ApplyReport {
  const report: ApplyReport = { applied: 0, skipped_lww: 0, deduped: 0, tombstoned: 0 }

  for (const f of facts) {
    const local = store.getMergeFields(f.id)
    // dédup inter-machines : même contenu sous un autre UUID déjà présent
    if (!local && f.content_hash) {
      const dupId = store.findIdByContentHash(f.content_hash)
      if (dupId && dupId !== f.id) {
        report.deduped++
        continue
      }
    }
    if (winner(local, f) === 'apply') {
      store.upsertSyncedFact(f)
      report.applied++
    } else {
      report.skipped_lww++
    }
  }

  for (const t of tombstones) {
    const local = store.getMergeFields(t.id)
    if (winner(local, t) === 'apply') {
      if (store.applyTombstone(t)) report.tombstoned++
    } else {
      report.skipped_lww++
    }
  }

  return report
}
