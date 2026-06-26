#!/usr/bin/env node
/**
 * linear-agent — OpenClaw skill for Linear project management
 *
 * Dual-mode entrypoint:
 *
 *   1. OpenClaw skill mode (default when OPENCLAW=1 or piped stdin)
 *      Reads a JSON payload from stdin:
 *        { "command": "<command>", "params": { ... } }
 *      Writes a JSON result to stdout.
 *
 *   2. CLI mode
 *      node index.js <command> --param value --flag
 *      node index.js <command> --json '{"param":"value"}'
 *
 * Auth: set LINEAR_API_KEY in your environment.
 */

'use strict';

const { LinearClient } = require('./src/client');
const issues   = require('./src/issues');
const teams    = require('./src/teams');
const cycles   = require('./src/cycles');
const projects = require('./src/projects');
const comments = require('./src/comments');
const workflow = require('./src/workflow');
const search   = require('./src/search');
const git      = require('./src/git');

// ---------------------------------------------------------------------------
// Command router
// ---------------------------------------------------------------------------

/**
 * Dispatch a command to the appropriate handler.
 *
 * @param {LinearClient} client
 * @param {string} command
 * @param {object} params
 * @returns {Promise<object>} Always returns a structured result object
 */
async function dispatch(client, command, params) {
  switch (command) {
    // ── Issues ──────────────────────────────────────────────────────────────
    case 'create-issue':
      return issues.createIssue(client, params);

    case 'update-issue':
      return issues.updateIssue(client, params);

    case 'get-issue':
      return issues.getIssue(client, params);

    case 'list-issues':
      return issues.listIssues(client, params);

    // ── Search ───────────────────────────────────────────────────────────────
    case 'search-issues':
      return search.searchIssues(client, params);

    // ── Workflow / states ────────────────────────────────────────────────────
    case 'move-issue':
      return workflow.moveIssue(client, params);

    case 'list-states':
      return workflow.listWorkflowStates(client, params);

    // ── Teams ────────────────────────────────────────────────────────────────
    case 'list-teams':
      return teams.listTeams(client);

    case 'backlog-summary':
      return teams.backlogSummary(client, params);

    // ── Cycles ───────────────────────────────────────────────────────────────
    case 'get-cycle':
      return cycles.getCycle(client, params);

    case 'list-cycles':
      return cycles.listCycles(client, params);

    case 'cycle-progress':
      return cycles.cycleProgress(client, params);

    // ── Projects ─────────────────────────────────────────────────────────────
    case 'create-project':
      return projects.createProject(client, params);

    case 'update-project':
      return projects.updateProject(client, params);

    case 'list-projects':
      return projects.listProjects(client, params);

    // ── Comments ─────────────────────────────────────────────────────────────
    case 'post-comment':
      return comments.postComment(client, params);

    // ── Git sync ─────────────────────────────────────────────────────────────
    case 'sync-commit':
      return git.syncFromCommit(client, params);

    // ── Meta ─────────────────────────────────────────────────────────────────
    case 'help':
    case '--help':
    case '-h':
      return { success: true, data: buildHelp() };

    default:
      throw new Error(
        `Unknown command: "${command}". Run with "help" to see available commands.`
      );
  }
}

// ---------------------------------------------------------------------------
// Mode detection + entry
// ---------------------------------------------------------------------------

async function main() {
  const apiKey = process.env.LINEAR_API_KEY;

  // ── Detect invocation mode ───────────────────────────────────────────────
  const isOpenClaw = process.env.OPENCLAW === '1' || !process.stdout.isTTY || isStdinPiped();
  const hasCLIArgs = process.argv.length > 2;

  if (!hasCLIArgs && isOpenClaw) {
    await runSkillMode(apiKey);
  } else if (hasCLIArgs) {
    await runCLIMode(apiKey);
  } else {
    // Interactive: print help
    console.log(formatHelp());
    process.exit(0);
  }
}

// ---------------------------------------------------------------------------
// OpenClaw skill mode — reads JSON from stdin, writes JSON to stdout
// ---------------------------------------------------------------------------

async function runSkillMode(apiKey) {
  let payload;

  try {
    const raw = await readStdin();
    if (!raw.trim()) {
      outputJSON({ success: false, error: 'No input received on stdin.' });
      process.exit(1);
    }
    payload = JSON.parse(raw);
  } catch (err) {
    outputJSON({ success: false, error: `Failed to parse stdin JSON: ${err.message}` });
    process.exit(1);
  }

  const { command, params = {} } = payload;

  if (!command) {
    outputJSON({ success: false, error: 'Input JSON must have a "command" field.' });
    process.exit(1);
  }

  // Help doesn't need an API key
  if (command === 'help') {
    outputJSON({ success: true, data: buildHelp() });
    return;
  }

  try {
    const client = new LinearClient(apiKey);
    const result = await dispatch(client, command, params);
    outputJSON(result);
  } catch (err) {
    outputJSON({ success: false, error: err.message });
    process.exit(1);
  }
}

// ---------------------------------------------------------------------------
// CLI mode — parses argv, runs command, prints JSON
// ---------------------------------------------------------------------------

async function runCLIMode(apiKey) {
  const args = process.argv.slice(2);
  const command = args[0];

  // Support --json '{ ... }' for passing params as a JSON blob
  const jsonFlagIdx = args.indexOf('--json');
  let params = {};

  if (jsonFlagIdx !== -1 && args[jsonFlagIdx + 1]) {
    try {
      params = JSON.parse(args[jsonFlagIdx + 1]);
    } catch (err) {
      fatal(`Invalid JSON passed to --json: ${err.message}`);
    }
  } else {
    // Parse --key value pairs from the remaining args
    params = parseArgv(args.slice(1));
  }

  // Special case: don't need API key for help
  if (command === 'help' || command === '--help' || command === '-h') {
    console.log(formatHelp());
    process.exit(0);
  }

  try {
    const client = new LinearClient(apiKey);
    const result = await dispatch(client, command, params);

    // Pretty-print to stdout
    if (result.summary) {
      // For summary commands, print the human-readable text first
      console.error('\n' + result.summary + '\n');
    }
    outputJSON(result);
  } catch (err) {
    outputJSON({ success: false, error: err.message });
    process.exit(1);
  }
}

// ---------------------------------------------------------------------------
// Argv parser
// ---------------------------------------------------------------------------

/**
 * Parse a flat argv array into a params object.
 *
 * Handles:
 *   --key value          → { key: "value" }
 *   --key=value          → { key: "value" }
 *   --flag               → { flag: true }
 *   --key a,b,c          → { key: ["a","b","c"] } (comma-separated arrays)
 *   --key '["a","b"]'    → { key: ["a","b"] } (JSON arrays)
 *
 * @param {string[]} args
 * @returns {object}
 */
function parseArgv(args) {
  const params = {};

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];

    if (!arg.startsWith('--')) continue;

    let key, rawValue;

    if (arg.includes('=')) {
      [key, rawValue] = arg.slice(2).split('=');
    } else {
      key = arg.slice(2);
      const next = args[i + 1];
      if (next && !next.startsWith('--')) {
        rawValue = next;
        i++;
      } else {
        rawValue = 'true';
      }
    }

    // Coerce types
    params[key] = coerce(rawValue);
  }

  return params;
}

/**
 * Attempt to coerce a raw string value to a more useful JS type.
 */
function coerce(raw) {
  if (raw === 'true')  return true;
  if (raw === 'false') return false;

  // JSON array or object
  if ((raw.startsWith('[') && raw.endsWith(']')) ||
      (raw.startsWith('{') && raw.endsWith('}'))) {
    try { return JSON.parse(raw); } catch (_) { /* fall through */ }
  }

  // Comma-separated list → array (only if no spaces around commas)
  if (/^[^,\s]+(,[^,\s]+)+$/.test(raw)) {
    return raw.split(',').map(coerce);
  }

  // Number
  const num = Number(raw);
  if (!isNaN(num) && raw !== '') return num;

  return raw;
}

// ---------------------------------------------------------------------------
// Output helpers
// ---------------------------------------------------------------------------

function outputJSON(obj) {
  process.stdout.write(JSON.stringify(obj, null, 2) + '\n');
}

function fatal(msg) {
  outputJSON({ success: false, error: msg });
  process.exit(1);
}

// ---------------------------------------------------------------------------
// Stdin reader
// ---------------------------------------------------------------------------

function readStdin() {
  return new Promise((resolve, reject) => {
    let data = '';
    process.stdin.setEncoding('utf8');
    process.stdin.on('data', (chunk) => { data += chunk; });
    process.stdin.on('end', () => resolve(data));
    process.stdin.on('error', reject);
  });
}

function isStdinPiped() {
  try {
    return !process.stdin.isTTY;
  } catch (_) {
    return false;
  }
}

// ---------------------------------------------------------------------------
// Help text
// ---------------------------------------------------------------------------

function buildHelp() {
  return {
    commands: [
      { name: 'create-issue',    description: 'Create a new issue',                   required: ['title', 'teamId'] },
      { name: 'update-issue',    description: 'Update an existing issue',             required: ['id'] },
      { name: 'get-issue',       description: 'Get a single issue by ID/identifier',  required: ['id'] },
      { name: 'list-issues',     description: 'List/filter issues',                   required: [] },
      { name: 'search-issues',   description: 'Full-text search issues',              required: ['query'] },
      { name: 'move-issue',      description: 'Move issue to a workflow state',       required: ['id', 'stateId|stateName'] },
      { name: 'list-states',     description: 'List workflow states for a team',      required: ['teamId'] },
      { name: 'list-teams',      description: 'List all teams',                       required: [] },
      { name: 'backlog-summary', description: 'Plain-English team backlog summary',   required: ['teamId'] },
      { name: 'get-cycle',       description: 'Get a cycle and its issues',           required: ['id'] },
      { name: 'list-cycles',     description: 'List cycles for a team',               required: ['teamId'] },
      { name: 'cycle-progress',  description: 'Get cycle completion progress',        required: ['id|teamId'] },
      { name: 'create-project',  description: 'Create a new project',                required: ['name', 'teamIds'] },
      { name: 'update-project',  description: 'Update an existing project',           required: ['id'] },
      { name: 'list-projects',   description: 'List projects',                        required: [] },
      { name: 'post-comment',    description: 'Post a comment on an issue',           required: ['issueId', 'body'] },
      { name: 'sync-commit',     description: 'Sync issues from git commit message',  required: ['message'] },
    ],
    usage: [
      'CLI:         node index.js <command> --param value',
      'CLI (JSON):  node index.js <command> --json \'{"param":"value"}\'',
      'Skill mode:  echo \'{"command":"list-teams"}\' | node index.js',
      'Auth:        export LINEAR_API_KEY=lin_api_...',
    ],
  };
}

function formatHelp() {
  const help = buildHelp();
  const lines = [
    '',
    '  linear-agent — OpenClaw skill for Linear project management',
    '',
    '  Usage:',
    ...help.usage.map((u) => `    ${u}`),
    '',
    '  Commands:',
    ...help.commands.map((c) => {
      const req = c.required.length ? `  (requires: ${c.required.join(', ')})` : '';
      return `    ${c.name.padEnd(20)} ${c.description}${req}`;
    }),
    '',
    '  Environment:',
    '    LINEAR_API_KEY    Your Linear personal API key (required)',
    '',
  ];
  return lines.join('\n');
}

// ---------------------------------------------------------------------------
// Run
// ---------------------------------------------------------------------------

main().catch((err) => {
  outputJSON({ success: false, error: err.message });
  process.exit(1);
});
