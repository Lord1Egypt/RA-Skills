/**
 * Silence exactly one warning: `node:sqlite`'s experimental notice.
 *
 * Node 24 prints
 *
 *     ExperimentalWarning: SQLite is an experimental feature and might change
 *     at any time
 *
 * on stderr the first time `node:sqlite` is imported. For a CLI whose contract
 * is "everything it prints is JSON" that is noise, and on an MCP stdio
 * transport it is at best confusing to whoever is reading the log.
 *
 * Filtered at the `warning` **event** rather than by overriding
 * `process.emitWarning`, because the warning is emitted while `node:sqlite` is
 * being imported — earlier than any code in this module could run, since ESM
 * evaluates a module's dependencies before its body. Printing, though, is
 * deferred to a later tick, so intercepting the event still catches it however
 * the imports end up ordered. That immunity to import order matters: an
 * import-sorting formatter must not be able to silently un-fix this.
 *
 * Deliberately **not** `--no-warnings`, and deliberately not
 * `removeAllListeners('warning')`: every other warning still reaches whatever
 * was listening, including Node's own printer. We are hiding one known-benign
 * message, not going quiet.
 */
let installed = false;

/**
 * Installs the filter once per process. Every `openGraph()` calls this, and
 * installing again would wrap the previous filter in a new one each time.
 */
export function silenceSqliteExperimentalWarning() {
  if (installed) return;
  installed = true;
  const existing = process.listeners('warning');
  process.removeAllListeners('warning');
  process.on('warning', (warning) => {
    if (
      warning.name === 'ExperimentalWarning' &&
      warning.message.includes('SQLite is an experimental feature')
    ) {
      return;
    }
    for (const listener of existing) listener(warning);
  });
}
