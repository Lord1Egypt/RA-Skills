import type Database from "better-sqlite3";

export interface CircuitBreakerState {
  scope: string;
  failure_count: number;
  last_failure_at?: string | null;
  open_until?: string | null;
  last_error?: string | null;
  updated_at?: string | null;
}

function nowIso(): string {
  return new Date().toISOString();
}

function toIso(ms: number): string {
  return new Date(ms).toISOString();
}

export function getCircuitBreaker(db: Database.Database, scope: string): CircuitBreakerState | null {
  return (db.prepare(`SELECT * FROM circuit_breakers WHERE scope = ?`).get(scope) as CircuitBreakerState | undefined) ?? null;
}

export function isCircuitOpen(db: Database.Database, scope: string): { open: boolean; state: CircuitBreakerState | null } {
  const state = getCircuitBreaker(db, scope);
  if (!state?.open_until) return { open: false, state };
  const openUntil = new Date(state.open_until).getTime();
  if (Number.isNaN(openUntil)) return { open: false, state };
  return { open: openUntil > Date.now(), state };
}

export function recordCircuitSuccess(db: Database.Database, scope: string): void {
  db.prepare(`
    INSERT INTO circuit_breakers (scope, failure_count, last_failure_at, open_until, last_error, updated_at)
    VALUES (?, 0, NULL, NULL, NULL, CURRENT_TIMESTAMP)
    ON CONFLICT(scope) DO UPDATE SET
      failure_count = 0,
      last_failure_at = NULL,
      open_until = NULL,
      last_error = NULL,
      updated_at = CURRENT_TIMESTAMP
  `).run(scope);
}

export function recordCircuitFailure(
  db: Database.Database,
  scope: string,
  error: string,
  failureThreshold: number,
  cooldownMs: number
): CircuitBreakerState {
  const current = getCircuitBreaker(db, scope);
  const failureCount = (current?.failure_count ?? 0) + 1;
  const shouldOpen = failureCount >= Math.max(1, failureThreshold);
  const openUntil = shouldOpen ? toIso(Date.now() + Math.max(1000, cooldownMs)) : null;
  const ts = nowIso();

  db.prepare(`
    INSERT INTO circuit_breakers (scope, failure_count, last_failure_at, open_until, last_error, updated_at)
    VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    ON CONFLICT(scope) DO UPDATE SET
      failure_count = excluded.failure_count,
      last_failure_at = excluded.last_failure_at,
      open_until = excluded.open_until,
      last_error = excluded.last_error,
      updated_at = CURRENT_TIMESTAMP
  `).run(scope, failureCount, ts, openUntil, error);

  return getCircuitBreaker(db, scope)!;
}
