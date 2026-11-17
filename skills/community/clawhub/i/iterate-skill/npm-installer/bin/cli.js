#!/usr/bin/env node

/**
 * iterate-skill-installer CLI
 *
 * One-command installer for iterate-skill across AI coding assistants.
 *
 * Usage:
 *   npx iterate-skill-installer
 *   npx iterate-skill-installer --ai trae
 *   npx iterate-skill-installer --target /path/to/project
 *   npx iterate-skill-installer --global
 *   npx iterate-skill-installer --no-cli
 *
 * The installer downloads the latest GitHub release, verifies its SHA256
 * checksum, then delegates file copying and assistant selection to the
 * Python install script bundled in the release.
 */

const { main, parseArgs, VERSION } = require('../lib/installer');

function printHelp() {
  console.log(`
Usage: npx iterate-skill-installer [options]

Options:
  --ai <assistant>    Install only to the specified assistant (e.g. trae, claude, cursor).
  --target <path>     Install into a project directory instead of the global home dir.
  --global            Install into the user's home directory (default).
  --force             Overwrite existing skill files.
  --no-cli            Skip installing the iterate CLI (skill-only install).
  --token <token>     GitHub token for higher API rate limits.
  -h, --help          Show this help message.
  -v, --version       Show version.

Examples:
  npx iterate-skill-installer
  npx iterate-skill-installer --ai trae
  npx iterate-skill-installer --target ./my-project
  npx iterate-skill-installer --no-cli
`);
}

async function run() {
  let options;
  try {
    options = parseArgs(process.argv.slice(2));
  } catch (err) {
    // Hard argument errors are THROWN by parseArgs (library code never calls
    // process.exit); report them cleanly at this boundary.
    console.error(`Error: ${err.message}`);
    return 1;
  }

  if (options.mode === 'help') {
    printHelp();
    return 0;
  }

  if (options.mode === 'version') {
    console.log(`iterate-skill-installer ${VERSION}`);
    return 0;
  }

  try {
    const code = await main(options);
    // Normalize: a null/non-numeric code (main should never produce one, but a
    // signal-killed child upstream does) must surface as a failure, never as
    // the success exit 0 that a null exit code would yield.
    return typeof code === 'number' ? code : 1;
  } catch (err) {
    console.error(`\nUnexpected error: ${err.message}`);
    return 1;
  }
}

// CLI boundary: set process.exitCode rather than calling process.exit(), so
// buffered stdout/stderr still flush and no caller cleanup is skipped. The
// trailing catch is the top-level net: an unexpected rejection (e.g. a throw
// before run()'s inner try) becomes a clean message + non-zero code, never an
// unhandled-rejection stack trace.
run()
  .then((code) => {
    process.exitCode = typeof code === 'number' ? code : 1;
  })
  .catch((err) => {
    console.error(`\nUnexpected error: ${err && err.message ? err.message : err}`);
    process.exitCode = 1;
  });
