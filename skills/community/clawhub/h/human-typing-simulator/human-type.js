#!/usr/bin/env node
/**
 * human-type CLI
 * Usage: human-type <command> [options]
 */

const fs   = require('fs');
const path = require('path');
const { generateScript, inspectScript } = require('./engine');

const VERSION = '2.0.1';

// ─── Minimal arg parser ──────────────────────────────────────────────────────

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith('--')) {
      const key = a.slice(2);
      const next = argv[i + 1];
      if (next && !next.startsWith('--')) {
        args[key] = next;
        i++;
      } else {
        args[key] = true;
      }
    } else {
      args._.push(a);
    }
  }
  return args;
}

// ─── Helpers ─────────────────────────────────────────────────────────────────

function die(msg) {
  process.stderr.write(`\x1b[31merror:\x1b[0m ${msg}\n`);
  process.exit(1);
}

function info(msg) {
  process.stdout.write(msg + '\n');
}

function pct(n) {
  return Math.round(n * 100);
}

// ─── Commands ─────────────────────────────────────────────────────────────────

async function cmdRun(args) {
  const text = args['text'];
  if (!text) die('--text is required');

  const duration      = parseFloat(args['duration']     ?? '10');
  const mistakeRate   = parseInt(args['mistakes']       ?? '20') / 100;
  const pauseRate     = parseInt(args['pauses']         ?? '15') / 100;
  const deferRate     = parseInt(args['defer']          ?? '35') / 100;
  const accentOmitRate= parseInt(args['accent-omit']   ?? '60') / 100;
  const french        = !!args['french'];
  const seed          = args['seed'] ? parseInt(args['seed']) : undefined;
  const selector      = args['selector'];
  const delayStart    = parseInt(args['delay-start']    ?? '500');
  const dryRun        = !!args['dry-run'];
  const cdpUrl        = args['cdp-url'] ?? process.env.OPENCLAW_CDP_URL;

  if (duration < 2) die('--duration must be at least 2 seconds');

  const modeStr = french ? ', french accent mode' : '';
  info(`\x1b[2mGenerating script for ${text.length} chars over ${duration}s ` +
       `(mistakes ${pct(mistakeRate)}%, pauses ${pct(pauseRate)}%, defer ${pct(deferRate)}%${modeStr})…\x1b[0m`);

  const { events, seed: usedSeed } = generateScript(text, duration, {
    mistakeRate, pauseRate, deferRate, accentOmitRate, french, seed,
  });

  const stats = inspectScript(events, text);
  info(`\x1b[2mScript: ${stats.events} events, ${stats.immediateFixes} immediate fixes, ` +
       `${stats.deferredFixes} deferred fixes, ${stats.pauses} pauses, ~${stats.avgWpm} WPM  [seed: ${usedSeed}]\x1b[0m`);

  if (dryRun) {
    info('\nDry run — script (first 30 events):');
    info(JSON.stringify(events.slice(0, 30), null, 2));
    if (events.length > 30) info(`  … and ${events.length - 30} more events`);
    return;
  }

  const { playScript } = require('./player');
  info(`\x1b[32mTyping…\x1b[0m`);
  await playScript(events, { selector, delayStart, cdpUrl });
  info(`\x1b[32mDone.\x1b[0m`);
}

async function cmdGenerate(args) {
  const text = args['text'];
  if (!text) die('--text is required');

  const duration      = parseFloat(args['duration']     ?? '10');
  const mistakeRate   = parseInt(args['mistakes']       ?? '20') / 100;
  const pauseRate     = parseInt(args['pauses']         ?? '15') / 100;
  const deferRate     = parseInt(args['defer']          ?? '35') / 100;
  const accentOmitRate= parseInt(args['accent-omit']   ?? '60') / 100;
  const french        = !!args['french'];
  const seed          = args['seed'] ? parseInt(args['seed']) : undefined;
  const output        = args['output'] ?? './human-type-script.json';

  const { events, seed: usedSeed } = generateScript(text, duration, {
    mistakeRate, pauseRate, deferRate, accentOmitRate, french, seed,
  });

  const payload = {
    meta: {
      targetText: text,
      duration,
      mistakeRate: pct(mistakeRate),
      pauseRate:   pct(pauseRate),
      deferRate:   pct(deferRate),
      accentOmitRate: pct(accentOmitRate),
      french,
      seed:        usedSeed,
      generatedAt: new Date().toISOString(),
      ...inspectScript(events, text),
    },
    events,
  };

  fs.writeFileSync(path.resolve(output), JSON.stringify(payload, null, 2));
  info(`\x1b[32mScript saved to ${output}  (${events.length} events, seed: ${usedSeed})\x1b[0m`);
}

async function cmdPlay(args) {
  const file = args._[0] ?? args['file'];
  if (!file) die('Usage: human-type play <script.json> [--selector <css>]');

  const raw = fs.readFileSync(path.resolve(file), 'utf8');
  const data = JSON.parse(raw);

  // Support both { events: [...] } and bare array
  const events   = Array.isArray(data) ? data : data.events;
  const selector = args['selector'];
  const cdpUrl   = args['cdp-url'] ?? process.env.OPENCLAW_CDP_URL;

  if (!events?.length) die('Script file contains no events');

  const stats = inspectScript(events, data?.meta?.targetText ?? '');
  info(`\x1b[2mReplaying ${stats.events} events over ~${stats.totalSec}s…\x1b[0m`);

  const { playScript } = require('./player');
  await playScript(events, { selector, cdpUrl });
  info(`\x1b[32mDone.\x1b[0m`);
}

function cmdInspect(args) {
  const file = args._[0] ?? args['file'];
  if (!file) die('Usage: human-type inspect <script.json>');

  const raw  = fs.readFileSync(path.resolve(file), 'utf8');
  const data = JSON.parse(raw);
  const events = Array.isArray(data) ? data : data.events;
  const meta   = data?.meta ?? {};

  if (!events?.length) die('Script file contains no events');

  const stats = inspectScript(events, meta.targetText ?? '');

  info('');
  if (meta.targetText) info(`  Target text    "${meta.targetText}"`);
  info(`  Events         ${stats.events}`);
  info(`  Keystrokes     ${stats.keystrokes}`);
  info(`  Immediate fixes ${stats.immediateFixes}`);
  info(`  Deferred fixes  ${stats.deferredFixes}`);
  info(`  Arrow moves     ${stats.arrowMoves}`);
  info(`  Pauses         ${stats.pauses}`);
  info(`  Total time     ${stats.totalSec}s`);
  info(`  Avg WPM        ${stats.avgWpm}`);
  if (meta.seed) info(`  Seed           ${meta.seed}`);
  if (meta.french) info(`  French mode    yes (accent-omit ${meta.accentOmitRate ?? 60}%)`);
  info('');
}

// ─── Main ─────────────────────────────────────────────────────────────────────

async function main() {
  const argv = process.argv.slice(2);
  const args = parseArgs(argv);
  const cmd  = args._[0];

  if (!cmd || cmd === '--help' || cmd === '-h' || cmd === 'help') {
    info(`human-type v${VERSION}

Usage:
  human-type run      --text <string> [options]
  human-type generate --text <string> [options] [--output <file>]
  human-type play     <script.json>  [--selector <css>] [--cdp-url <url>]
  human-type inspect  <script.json>

Options:
  --text          Final desired text (required for run/generate)
  --duration      Total typing time in seconds (default: 10)
  --mistakes      Immediate typo rate 0-100% (default: 20)
  --pauses        Pause frequency 0-100% (default: 15)
  --defer         Fraction of typos deferred for later correction 0-100% (default: 35)
  --french        Enable French accent omission mode (flag, no value needed)
  --accent-omit   Fraction of accented chars omitted and fixed later 0-100% (default: 60)
  --selector      CSS selector to click/focus before typing
  --delay-start   Ms to wait before first keystroke (default: 500)
  --seed          Fix RNG seed for reproducible output
  --dry-run       Print script without typing
  --output        Output file path for generate command (default: ./human-type-script.json)
  --cdp-url       Chrome DevTools Protocol URL (default: http://127.0.0.1:18800)

Examples:
  human-type run --text "Hello world" --duration 8 --mistakes 25 --defer 40
  human-type run --text "Bonjour, ça va?" --duration 10 --french
  human-type run --text "Fix this later" --duration 8 --defer 100 --dry-run

Notes:
  Defaults to OPENCLAW_CDP_URL when set, otherwise http://127.0.0.1:18800
`);
    return;
  }

  if (cmd === '--version' || cmd === '-v' || cmd === 'version') {
    info(`human-type v${VERSION}`);
    return;
  }

  const subArgs = { ...args, _: args._.slice(1) };

  switch (cmd) {
    case 'run':      await cmdRun(subArgs);     break;
    case 'generate': await cmdGenerate(subArgs); break;
    case 'play':     await cmdPlay(subArgs);     break;
    case 'inspect':  cmdInspect(subArgs);        break;
    default:         die(`Unknown command: ${cmd}. Run human-type --help`);
  }
}

main().catch(err => {
  process.stderr.write(`\x1b[31mFatal: ${err.message}\x1b[0m\n`);
  process.exit(1);
});
