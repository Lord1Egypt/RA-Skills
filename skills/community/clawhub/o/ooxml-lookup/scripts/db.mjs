/**
 * The only module in this repo that imports `node:sqlite`.
 *
 * That confinement is deliberate and cheap insurance: the API is flagged
 * experimental and documented as free to change, so a break costs one file
 * rather than a rewrite. Everything above this module deals in plain objects.
 *
 * The database sits next to this file (`./data/ooxml.db`), resolved through
 * `import.meta.url` rather than `process.cwd()`. That is what makes the
 * vendoring scheme work unchanged in three places: `core/`, `skill/scripts/`
 * and `mcp/src/` each carry their own copy beside their own copy of this
 * module, and none of them cares where the process was started from.
 */
import {DatabaseSync} from 'node:sqlite';
import {silenceSqliteExperimentalWarning} from './warnings.mjs';

/**
 * Bumped whenever `build/schema.sql` changes. `build/build-db.mjs` writes these
 * same values, so they are stated once, here.
 */
export const EXPECTED_USER_VERSION = 2;
/** 'OOX1' as a big-endian int32 — `file`-style magic for a SQLite payload. */
export const EXPECTED_APPLICATION_ID = 0x4f4f5831;

export const DEFAULT_DB_PATH = new URL('./data/ooxml.db', import.meta.url);

/**
 * Open the graph, refusing anything that is not the database this code knows.
 *
 * The check is not paranoia. Both surfaces ship a *vendored copy* of the
 * database beside a *vendored copy* of this module, and if a release ever lands
 * one without the other the result is not a crash — it is a tool that answers
 * confidently from a schema whose columns have moved. `user_version` turns that
 * into a startup error naming the fix.
 */
/** @param {string | URL} path */
export function openGraph(path = DEFAULT_DB_PATH) {
  silenceSqliteExperimentalWarning();

  let db;
  try {
    db = new DatabaseSync(path, {readOnly: true});
  } catch (cause) {
    throw new Error(
      `cannot open the OOXML schema database at ${path}. ` +
        'In a checkout, build it with `make db`; in an installed package this is a packaging bug.',
      {cause},
    );
  }

  const applicationId = db.prepare('PRAGMA application_id').get().application_id;
  if (applicationId !== EXPECTED_APPLICATION_ID) {
    db.close();
    throw new Error(
      `${path} is not an OOXML schema database ` +
        `(application_id ${applicationId}, expected ${EXPECTED_APPLICATION_ID}).`,
    );
  }

  const userVersion = db.prepare('PRAGMA user_version').get().user_version;
  if (userVersion !== EXPECTED_USER_VERSION) {
    db.close();
    throw new Error(
      `schema version mismatch: the database at ${path} is version ${userVersion}, ` +
        `this code expects ${EXPECTED_USER_VERSION}. The vendored database and the ` +
        'vendored core have drifted — run `make sync-core`.',
    );
  }

  const statements = new Map();
  /** Prepared statements are cached: the CLI is one process per call, the MCP server is not. */
  const prepare = (sql) => {
    let statement = statements.get(sql);
    if (statement === undefined) {
      statement = db.prepare(sql);
      statements.set(sql, statement);
    }
    return statement;
  };

  return {
    /** @returns {any[]} */
    all: (sql, ...params) => prepare(sql).all(...params),
    /** @returns {any} */
    get: (sql, ...params) => prepare(sql).get(...params),
    close: () => db.close(),
    path: String(path),
  };
}
