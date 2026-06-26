#!/usr/bin/env node
import { formatText, formatJson } from './lib/format.mjs';
import { makeEnvelope } from './lib/helpers.mjs';
import search from './lib/commands/search.mjs';
import departures from './lib/commands/departures.mjs';
import parse from './lib/commands/parse.mjs';
import journey from './lib/commands/journey.mjs';
import live from './lib/commands/live.mjs';
import track from './lib/commands/track.mjs';

// START Argument parsing
const argv = process.argv.slice(2);
const flags = {};
const positional = [];

// Flags that never take a value argument
const BOOL_FLAGS = new Set(['json', 'predict', 'stats', 'help']);

for (let i = 0; i < argv.length; i++) {
  if (argv[i].startsWith('--')) {
    const key = argv[i].slice(2);
    const next = argv[i + 1];
    if (!BOOL_FLAGS.has(key) && next && !next.startsWith('--')) {
      flags[key] = next;
      i++;
    } else {
      flags[key] = true;
    }
  } else {
    positional.push(argv[i]);
  }
}

// END Argument parsing

// ── dispatch ────────────────────────────────────────
const commands = { search, departures, parse, journey, live, track };
const MODES = Object.keys(commands);
const mode = MODES.find(m => flags[m] !== undefined);
const isJson = flags.json === true;

function output(envelope) {
  console.log(isJson ? formatJson(envelope) : formatText(envelope));
}

// ── help ────────────────────────────────────────────
function showHelp() {
  console.log(`Usage: node bahn.mjs --<mode> [flags]

Modes:
  --search <query>                          Station lookup
  --departures <station> [--results N]      Live departure board
  --parse [file] [--predict] [--stats]      Parse connection (stdin or file)
  --journey <from> <to> [--date] [--time]   Route search [--results N] [--days N] [--predict]
  --live <file> --current-leg N [--delay M]  Real-time transfer check [--predict]
  --track --train NUM --category CAT        Train tracking [--date]

Flags:
  --json       Output as JSON
  --predict    Exponential delay model (transferProb, zugbindungProb)
  --stats      Historical aggregate data (via bahn.expert)
  --help       Show this help`);
}

try {
  if (flags.help) {
    showHelp();
    process.exit(0);
  }

  if (!mode) {
    const errEnvelope = makeEnvelope('error');
    errEnvelope.errors.push('No mode specified. Usage: node bahn.mjs --help');
    output(errEnvelope);
    process.exit(1);
  }

  const envelope = await commands[mode]({ flags, positional });
  output(envelope);
} catch (err) {
  const envelope = makeEnvelope(mode || 'error');
  envelope.errors.push(err.message || String(err));
  if (isJson) {
    console.log(formatJson(envelope));
  } else {
    console.log(`Error: ${err.message || err}`);
    if (envelope.warnings.length) {
      for (const w of envelope.warnings) console.log(`Warning: ${w}`);
    }
  }
  process.exit(1);
}
