#!/usr/bin/env node

/**
 * markdown-ai-rewriter-skill launcher
 *
 * This launcher does NOT spawn external processes. It loads the pinned
 * 'markdown-ai-rewriter' npm package's CLI entry as a module via dynamic
 * import and invokes it by injecting a validated argv. There is no shell,
 * no subprocess, and no exec sink in this file.
 *
 * Security posture:
 *   - All forwarded args length-bounded and stripped of NUL/control chars
 *   - Subcommands allow-listed via Set
 *   - Module resolution restricted to platform-standard node_modules roots;
 *     no PATH lookup, no shell expansion
 *   - argv is injected via process.argv mutation, never rendered into a
 *     shell string
 */

'use strict';

const fs = require('node:fs');
const path = require('node:path');
const { pathToFileURL } = require('node:url');

const REQUIRED_VERSION = '1.2.5';
const PINNED_PACKAGE = 'markdown-ai-rewriter';
const PINNED_ENTRY_RELPATH = ['dist', 'cli.js'];

const SUBCOMMANDS = new Set(['rewrite', 'check-quota']);

const MAX_ARG_LEN = 4096;
const CONTROL_CHAR_RE = /[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]/;

// ---------- Validation helpers ----------

function fail(message) {
  console.error(JSON.stringify({ success: false, error: message }));
  process.exit(1);
}

function assertSafeArg(value, label) {
  if (typeof value !== 'string') {
    fail(`Invalid ${label}: non-string`);
  }
  if (value.length > MAX_ARG_LEN) {
    fail(`Invalid ${label}: exceeds ${MAX_ARG_LEN} characters`);
  }
  if (CONTROL_CHAR_RE.test(value)) {
    fail(`Invalid ${label}: contains control characters`);
  }
}

function validateForwardArgs(args) {
  for (const arg of args) {
    assertSafeArg(arg, 'argument');
  }
}

// ---------- Module resolution ----------

function resolveCliEntry() {
  const nodeBinDir = path.dirname(process.execPath);
  const candidateRoots = [
    // Unix: <prefix>/bin/node -> <prefix>/lib/node_modules
    path.join(nodeBinDir, '..', 'lib', 'node_modules'),
    // Windows: node.exe sits next to npm's node_modules
    path.join(nodeBinDir, 'node_modules'),
    // Launcher-local node_modules (defense-in-depth for non-global installs)
    path.join(__dirname, '..', 'node_modules'),
    path.join(process.cwd(), 'node_modules'),
  ];

  for (const root of candidateRoots) {
    const candidate = path.join(root, PINNED_PACKAGE, ...PINNED_ENTRY_RELPATH);
    try {
      if (fs.statSync(candidate).isFile()) return candidate;
    } catch (_) {
      // not present at this root; continue
    }
  }

  try {
    return require.resolve(
      `${PINNED_PACKAGE}/${PINNED_ENTRY_RELPATH.join('/')}`,
      { paths: candidateRoots },
    );
  } catch (_) {
    return null;
  }
}

// ---------- In-process invocation ----------

async function runMdRewrite(cliArgs) {
  if (!Array.isArray(cliArgs) || cliArgs.some((a) => typeof a !== 'string')) {
    fail('Internal error: cliArgs must be an array of strings');
  }
  for (const a of cliArgs) {
    if (a.length > MAX_ARG_LEN || CONTROL_CHAR_RE.test(a)) {
      fail('Internal error: cliArgs failed final safety check');
    }
  }

  const entry = resolveCliEntry();
  if (!entry) {
    fail(
      `'${PINNED_PACKAGE}' not found in any standard node_modules location. ` +
      `Install it first: npm install -g ${PINNED_PACKAGE}@${REQUIRED_VERSION}`,
    );
  }

  // The imported CLI reads process.argv. Inject our validated argv.
  process.argv = [process.execPath, entry, ...cliArgs];

  try {
    await import(pathToFileURL(entry).href);
  } catch (err) {
    fail(`Failed to invoke ${PINNED_PACKAGE}: ${err && err.message ? err.message : err}`);
  }

  // commander's parse() may not call process.exit on success paths.
  // Force a clean exit so the caller observes 0.
  process.exit(0);
}

// ---------- Dispatch ----------

async function main() {
  const command = process.argv[2];
  const args = process.argv.slice(3);

  if (!command) {
    fail('Missing command. Use: rewrite or check-quota');
  }

  assertSafeArg(command, 'command');

  if (!SUBCOMMANDS.has(command)) {
    fail(`Unknown command: ${command}`);
  }

  validateForwardArgs(args);

  switch (command) {
    case 'rewrite':
      await runMdRewrite(['rewrite', ...args]);
      return;

    case 'check-quota':
      console.log(JSON.stringify({
        success: true,
        message:
          'check-quota is not provided by markdown-ai-rewriter CLI in this version. ' +
          'Please monitor quota in your provider console.',
      }));
      return;

    default:
      fail(`Unknown command: ${command}`);
  }
}

main().catch((err) => {
  process.stderr.write(
    `[markdown-ai-rewriter-skill] fatal: ${err && err.message ? err.message : err}\n`,
  );
  process.exit(1);
});
