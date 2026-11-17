/**
 * Observations (couche 9 legacy, portée en version simple, bucket B async).
 *
 * Une observation = synthèse vivante AGRÉGÉE par sujet. Contrairement au legacy
 * (re-synthèse LLM coûteuse à chaque fait), le modèle V1 de cette couche est un
 * UPSERT par sujet normalisé : ré-observer un sujet incrémente `obs_count` et
 * remet à jour le contenu/confiance, ne duplique JAMAIS (index unique sur
 * subject). Le legacy self_observations/observations suivait la même logique
 * d'accumulation par clé.
 *
 * Pas de LLM requis : le contenu fourni peut venir d'un extracteur (LLM ou
 * heuristique). La synthèse LLM avancée (re-résumé multi-faits) est un sur-coût
 * Phase 6, branché ailleurs — ici on garantit l'agrégation idempotente.
 */
import type { Database } from 'better-sqlite3'
import { newId, nowISO } from '../util.js'

export interface ObservationRow {
  id: string
  subject: string
  content: string
  confidence: number
  obs_count: number
  created_at: string
  updated_at: string
}

export interface UpsertObservationInput {
  subject: string
  content: string
  confidence?: number
}

/**
 * Upsert d'une observation par sujet (dédup NOCASE). Nouveau sujet → insert
 * (obs_count = 1) ; sujet connu → obs_count + 1, content/confiance rafraîchis,
 * confiance lissée vers la valeur observée (moyenne mobile bornée [0,1]).
 * Retourne {id, created} — `created` distingue insert vs renforcement.
 */
export function upsertObservation(db: Database, input: UpsertObservationInput): { id: string; created: boolean } {
  const subject = input.subject.trim()
  const content = input.content.trim()
  if (subject.length < 2 || content.length < 2) {
    throw new Error('observation invalide : subject et content non vides requis')
  }
  const confidence = clamp01(input.confidence ?? 0.8)
  const existing = db
    .prepare('SELECT id, confidence, obs_count FROM observations WHERE subject = ? COLLATE NOCASE')
    .get(subject) as { id: string; confidence: number; obs_count: number } | undefined

  const ts = nowISO()
  if (existing) {
    // Confiance = moyenne mobile (poids égal au nombre d'observations) → stable.
    const n = existing.obs_count
    const blended = clamp01((existing.confidence * n + confidence) / (n + 1))
    db.prepare(
      'UPDATE observations SET content = ?, confidence = ?, obs_count = obs_count + 1, updated_at = ? WHERE id = ?',
    ).run(content, blended, ts, existing.id)
    return { id: existing.id, created: false }
  }
  const id = newId()
  db.prepare(
    `INSERT INTO observations (id, subject, content, confidence, obs_count, created_at, updated_at)
     VALUES (?, ?, ?, ?, 1, ?, ?)`,
  ).run(id, subject, content, confidence, ts, ts)
  return { id, created: true }
}

export function getObservation(db: Database, subject: string): ObservationRow | null {
  const row = db
    .prepare('SELECT * FROM observations WHERE subject = ? COLLATE NOCASE')
    .get(subject.trim()) as ObservationRow | undefined
  return row ?? null
}

export interface ObservationStats {
  total: number
  avg_obs_count: number
}

export function observationStats(db: Database): ObservationStats {
  const total = (db.prepare('SELECT COUNT(*) AS c FROM observations').get() as { c: number }).c
  if (total === 0) return { total: 0, avg_obs_count: 0 }
  const avg = (db.prepare('SELECT AVG(obs_count) AS a FROM observations').get() as { a: number | null }).a ?? 0
  return { total, avg_obs_count: Math.round(avg * 10) / 10 }
}

function clamp01(n: number): number {
  if (!Number.isFinite(n)) return 0
  return Math.min(1, Math.max(0, n))
}
