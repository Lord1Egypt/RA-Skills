/**
 * Horloge & identité de NŒUD pour la synchro inter-machines (SYNC §3.0/§3.9).
 *
 * - `machine_id` : identité STABLE de la machine (≠ `daemonId` éphémère du boot).
 *   Persistée dans `settings['sync.machine_id']` du registry. Sert de provenance
 *   et de tie-break déterministe du LWW.
 * - `origin_rev` : compteur logique monotone PAR machine (settings['sync.rev']).
 *   C'est le critère PRIMAIRE du LWW — robuste aux horloges Mac désynchronisées.
 */
import { hostname } from 'node:os'
import type { RegistryStore } from '../storage/registry.js'

const MACHINE_ID_KEY = 'sync.machine_id'
const REV_KEY = 'sync.rev'

/** Suffixe aléatoire court, stable une fois généré (pas de Math.random global interdit côté workflow). */
function randomSuffix(): string {
  // 6 hexs depuis crypto (disponible partout), sans dépendre de Math.random.
  const bytes = globalThis.crypto.getRandomValues(new Uint8Array(3))
  return Array.from(bytes, b => b.toString(16).padStart(2, '0')).join('')
}

/** Lit (ou crée au premier appel) l'identité stable de cette machine. */
export function localMachineId(registry: RegistryStore): string {
  const existing = registry.getSetting(MACHINE_ID_KEY)
  if (existing) return existing
  const id = `${sanitizeHost(hostname())}-${randomSuffix()}`
  registry.setSetting(MACHINE_ID_KEY, id)
  return id
}

function sanitizeHost(h: string): string {
  return (h.split('.')[0] ?? 'machine').toLowerCase().replace(/[^a-z0-9-]/g, '').slice(0, 24) || 'machine'
}

/** Incrémente et renvoie la révision logique suivante de cette machine (monotone). */
export function nextRev(registry: RegistryStore): number {
  const cur = Number.parseInt(registry.getSetting(REV_KEY) ?? '0', 10)
  const next = (Number.isFinite(cur) ? cur : 0) + 1
  registry.setSetting(REV_KEY, String(next))
  return next
}

/** Révision courante sans incrémenter (diagnostic). */
export function currentRev(registry: RegistryStore): number {
  const cur = Number.parseInt(registry.getSetting(REV_KEY) ?? '0', 10)
  return Number.isFinite(cur) ? cur : 0
}
