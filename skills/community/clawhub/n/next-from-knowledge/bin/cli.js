#!/usr/bin/env node

const NextFromKnowledge = require('../src/index.js');
const pkg = require('../package.json');

function parseArgs(argv) {
  const options = { _: [] };

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];

    if (!arg.startsWith('-')) {
      options._.push(arg);
      continue;
    }

    const key = arg.replace(/^-+/, '');
    const next = argv[i + 1];
    const hasValue = typeof next !== 'undefined' && !next.startsWith('-');
    options[key] = hasValue ? next : true;
    if (hasValue) {
      i += 1;
    }
  }

  return options;
}

function printHelp() {
  console.log(`NextFromKnowledge ${pkg.version}

Usage:
  nfk next-step --file notes.md
  nfk next-step --text "..."
  nfk plan --file notes.md --horizon 7d
  nfk decide --file options.md --options "方案A,方案B"
  nfk experiment --file summary.md
  nfk gaps --file summary.md
  nfk analyze --file summary.md --json

Commands:
  next-step, next   Recommend the most useful next move
  plan              Build a short action plan
  decide            Choose between explicit options
  experiment        Propose the smallest useful experiment
  gaps              Surface the smallest missing facts that matter
  analyze           Return the distilled knowledge structure

Options:
  --file <path>     Read input from a file
  --text <text>     Read input from inline text
  --options <csv>   Comma-separated decision options
  --horizon <span>  Planning horizon, such as 7d or 30d
  --json            Print JSON output
  --help            Show this help
  --version         Show version
`);
}

function requireInput(options) {
  if (!options.file && !options.text) {
    throw new Error('Please provide --file or --text');
  }
}

function writeOutput(engine, result, asJson) {
  if (asJson) {
    console.log(JSON.stringify(result, null, 2));
    return;
  }
  console.log(engine.render(result));
}

async function main() {
  const argv = process.argv.slice(2);
  const command = argv[0];

  if (!command || command === '--help' || command === '-h') {
    printHelp();
    return;
  }

  if (command === '--version' || command === '-v') {
    console.log(pkg.version);
    return;
  }

  const options = parseArgs(argv.slice(1));
  const engine = new NextFromKnowledge();

  try {
    switch (command) {
      case 'next':
      case 'next-step':
        requireInput(options);
        writeOutput(engine, engine.nextStep(options), options.json);
        return;
      case 'plan':
        requireInput(options);
        writeOutput(engine, engine.plan(options, { horizon: options.horizon || '7d' }), options.json);
        return;
      case 'decide':
        requireInput(options);
        if (!options.options) {
          throw new Error('Please provide --options "Option A,Option B"');
        }
        writeOutput(
          engine,
          engine.decide(options, { options: String(options.options).split(',').map((item) => item.trim()).filter(Boolean) }),
          options.json
        );
        return;
      case 'experiment':
        requireInput(options);
        writeOutput(engine, engine.experiment(options), options.json);
        return;
      case 'gaps':
        requireInput(options);
        writeOutput(engine, engine.gaps(options), options.json);
        return;
      case 'analyze':
        requireInput(options);
        console.log(JSON.stringify(engine.analyze(options), null, 2));
        return;
      default:
        throw new Error(`Unknown command: ${command}`);
    }
  } catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }
}

main();
