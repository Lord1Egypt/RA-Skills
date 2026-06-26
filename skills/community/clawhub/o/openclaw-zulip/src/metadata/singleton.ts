/**
 * Module-level MetadataStore singleton.
 *
 * Initialised once when the Zulip gateway starts; torn down on stop.
 */

import { mkdirSync } from "node:fs";
import { dirname } from "node:path";
import { initDatabase } from "./schema.ts";
import { MetadataStore } from "./store.ts";

let _store: MetadataStore | null = null;
let _dbClose: (() => void) | null = null;

/**
 * Create the SQLite DB (and parent dirs) and stash the MetadataStore singleton.
 * Calling twice without destroy in between replaces the previous store.
 */
export function initMetadataStore(dbPath: string): MetadataStore {
  if (_store) {
    destroyMetadataStore();
  }
  mkdirSync(dirname(dbPath), { recursive: true });
  const db = initDatabase(dbPath);
  _store = new MetadataStore(db);
  _dbClose = () => db.close();
  return _store;
}

/** Return the current singleton, or null if not yet initialised. */
export function getMetadataStore(): MetadataStore | null {
  return _store;
}

/** Close the underlying DB and clear the singleton. Safe to call when already destroyed. */
export function destroyMetadataStore(): void {
  if (_dbClose) {
    try {
      _dbClose();
    } catch {
      // best-effort
    }
    _dbClose = null;
  }
  _store = null;
}
