#!/usr/bin/env node
'use strict';

/**
 * paperclip-resilience setup wizard
 *
 * Interactively generates config.json from user input.
 * Outputs the final config and optionally writes it to disk.
 *
 * Usage:
 *   node scripts/setup.js
 *   node scripts/setup.js --output ./my-config.json
 *   node scripts/setup.js --no-input  (emit defaults, no prompts)
 */

const path = require('path');
const fs = require('fs');
const readline = require('readline');

const DEFAULTS_PATH = path.join(__dirname, '..', 'config.defaults.json');
const EXAMPLE_PATH  = path.join(__dirname, '..', 'config.example.json');
const DEFAULT_OUT   = path.join(__dirname, '..', 'config.json');

const args = process.argv.slice(2);
const noInput  = args.includes('--no-input');
const outFlag  = args.indexOf('--output');
const outPath  = outFlag !== -1 ? path.resolve(args[outFlag + 1]) : DEFAULT_OUT;
const dryRun   = args.includes('--dry-run');
const helpFlag = args.includes('--help') || args.includes('-h');

if (helpFlag) {
  console.log(`
paperclip-resilience setup wizard

  node scripts/setup.js [options]

Options:
  --output <path>   Path to write config.json (default: ./config.json)
  --no-input        Skip prompts and emit defaults only
  --dry-run         Print the generated config but do not write it
  -h, --help        Show this help
  `);
  process.exit(0);
}

// ── helpers ────────────────────────────────────────────────────────────────

function loadDefaults() {
  if (!fs.existsSync(DEFAULTS_PATH)) return {};
  try { return JSON.parse(fs.readFileSync(DEFAULTS_PATH, 'utf8')); }
  catch { return {}; }
}

function ask(rl, question) {
  return new Promise(resolve => rl.question(question, resolve));
}

function printSep(label) {
  const line = '─'.repeat(60);
  if (label) console.log(`\n${line}\n  ${label}\n${line}`);
  else console.log(line);
}

// ── main ───────────────────────────────────────────────────────────────────

async function main() {
  const defaults = loadDefaults();

  if (noInput) {
    // Just write/show defaults
    output(defaults);
    return;
  }

  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });

  printSep('paperclip-resilience — setup wizard');
  console.log('This wizard generates your config.json.');
  console.log('Press ENTER to accept defaults shown in [brackets].\n');

  // ── 1. Primary model alias ────────────────────────────────────────────────
  printSep('Primary model');
  console.log('Which model alias should be your PRIMARY agent?');
  console.log('Common options: sonnet, opus, haiku, flash, flash-lite, codex');
  const primaryAlias = (await ask(rl, `  Primary model [sonnet]: `)).trim() || 'sonnet';

  // ── 2. Fallback model ─────────────────────────────────────────────────────
  printSep('Fallback model');
  console.log('Which model alias should be the FALLBACK when the primary hits rate limits?');
  const fallbackSuggest = primaryAlias === 'sonnet' ? 'codex' : 'sonnet';
  const fallbackAlias = (await ask(rl, `  Fallback model [${fallbackSuggest}]: `)).trim() || fallbackSuggest;

  // ── 3. Custom aliases ─────────────────────────────────────────────────────
  printSep('Custom model aliases (optional)');
  console.log('Add any extra alias=provider/model pairs (comma-separated).');
  console.log('Example: mymodel=anthropic/claude-haiku-4-5,gpt4=openai/gpt-4o');
  const customAliasStr = (await ask(rl, '  Extra aliases [none]: ')).trim();

  // ── 4. Cron setup intent ──────────────────────────────────────────────────
  printSep('Run Recovery cron');
  console.log('Do you want run-recovery cron instructions included in the output? [y/N]');
  const wantCron = (await ask(rl, '  Enable cron hints? [y/N]: ')).trim().toLowerCase();
  const includeCron = wantCron === 'y' || wantCron === 'yes';

  rl.close();

  // ── Build config ──────────────────────────────────────────────────────────

  const builtConfig = JSON.parse(JSON.stringify(defaults)); // deep clone

  // Ensure aliases and fallbacks objects exist
  if (!builtConfig.aliases) builtConfig.aliases = {};
  if (!builtConfig.fallbacks) builtConfig.fallbacks = {};

  // Expand the user-chosen aliases to full model strings (look up from defaults or keep as-is)
  const defaultAliases = defaults.aliases || {};
  const primaryFull  = defaultAliases[primaryAlias]  || primaryAlias;
  const fallbackFull = defaultAliases[fallbackAlias] || fallbackAlias;

  // Ensure chosen aliases are present
  builtConfig.aliases[primaryAlias]  = primaryFull;
  builtConfig.aliases[fallbackAlias] = fallbackFull;

  // Wire fallbacks bidirectionally
  builtConfig.fallbacks[primaryFull]  = fallbackFull;
  builtConfig.fallbacks[fallbackFull] = primaryFull;

  // Parse custom aliases
  if (customAliasStr) {
    for (const pair of customAliasStr.split(',')) {
      const [alias, model] = pair.split('=').map(s => s.trim());
      if (alias && model) {
        builtConfig.aliases[alias] = model;
      }
    }
  }

  // Cron hint
  if (includeCron) {
    builtConfig['$doc'] = [
      'Generated by scripts/setup.js.',
      '',
      'Run recovery cron (add to your system crontab):',
      '  */15 * * * *  node skills/paperclip-resilience/src/run-recovery.js',
      '',
      'Or add via OpenClaw cron:',
      '  openclaw cron add --schedule "*/15 * * * *" --command "node skills/paperclip-resilience/src/run-recovery.js"',
    ].join('\n');
  } else {
    builtConfig['$doc'] = 'Generated by scripts/setup.js. See SKILL.md for full configuration options.';
  }

  output(builtConfig);
}

function output(config) {
  const json = JSON.stringify(config, null, 2);

  if (dryRun) {
    console.log('\n── Generated config (dry-run, not written) ──');
    console.log(json);
    return;
  }

  const dir = path.dirname(outPath);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });

  // Safety check: don't overwrite without warning if file exists
  if (fs.existsSync(outPath)) {
    console.log(`\n⚠  ${outPath} already exists — overwriting.`);
  }

  fs.writeFileSync(outPath, json + '\n', 'utf8');
  console.log(`\n✅  Config written to: ${outPath}`);
  console.log('\nNext steps:');
  console.log('  1. Review the generated config.json');
  console.log('  2. Adjust aliases and fallbacks to match your API keys');
  console.log('  3. Run: node src/spawn-with-fallback.js --dry-run --model sonnet --task "Test"');
  if (config['$doc'] && config['$doc'].includes('cron')) {
    console.log('  4. Wire the run-recovery cron per the $doc field in your config.json');
  }
}

main().catch(err => {
  console.error('Setup failed:', err.message);
  process.exit(1);
});
