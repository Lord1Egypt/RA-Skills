#!/usr/bin/env node
/** Start pinned agent-guard watcher (heartbeat + enforce). */
import { createRequire } from 'node:module';
import { dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const require = createRequire(import.meta.url);

try {
  const pkgJson = require.resolve('@hypelens/hypelens-agent-guard/package.json');
  const pkg = require(pkgJson);
  const binRel = (pkg.bin && pkg.bin['agent-guard-watcher']) || 'bin/agent-guard-watcher.js';
  const entry = join(dirname(pkgJson), binRel);
  await import(pathToFileURL(entry).href);
} catch (e) {
  try {
    const localEntry = join(
      dirname(fileURLToPath(import.meta.url)),
      '..',
      '..',
      'bin',
      'agent-guard-watcher.js',
    );
    await import(pathToFileURL(localEntry).href);
  } catch {
    console.error('Missing dependency. Run: npm install (in this scripts/ folder)');
    console.error(String(e && e.message ? e.message : e));
    process.exit(1);
  }
}
