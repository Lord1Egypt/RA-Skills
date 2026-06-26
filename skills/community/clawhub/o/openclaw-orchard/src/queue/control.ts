import type Database from "better-sqlite3";
import { getSetting, setSetting } from "../db/settings.js";
import { recordCircuitFailure, recordCircuitSuccess } from "./circuit-breaker.js";

export function isQueuePaused(db: Database.Database): boolean {
  return getSetting(db, "queue.paused") === true;
}

export function setQueuePaused(db: Database.Database, paused: boolean): void {
  setSetting(db, "queue.paused", paused);
}

export function openCircuit(
  db: Database.Database,
  scope: string,
  reason: string,
  cooldownMs: number
): void {
  recordCircuitFailure(db, scope, reason, 1, cooldownMs);
}

export function closeCircuit(db: Database.Database, scope: string): void {
  recordCircuitSuccess(db, scope);
}
