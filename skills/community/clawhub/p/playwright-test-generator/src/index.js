#!/usr/bin/env node
/**
 * playwright-test-generator — CLI entry point
 *
 * Usage:
 *   node src/index.js generate --input "Click login" --framework pytest-playwright --type pom
 *   node src/index.js analyze --url https://example.com
 *   node src/index.js extract-locators --html "$(cat form.html)"
 */

import { PlaywrightTestGenerator } from './generator.js';
import { LocatorExtractor } from './locator.js';
import { parse } from './parser.js';

// ─── Arg Parser ─────────────────────────────────────────────────────────────

function parseArgs(args) {
  const opts = {};
  const positional = [];

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg.startsWith('--')) {
      const key = arg.slice(2).replace(/-([a-z])/g, (_, c) => c.toUpperCase());
      const next = args[i + 1];
      if (next && !next.startsWith('--')) {
        opts[key] = next;
        i++;
      } else {
        opts[key] = true;
      }
    } else if (arg.startsWith('-') && arg.length === 2) {
      opts[arg[1]] = args[i + 1];
      i++;
    } else {
      positional.push(arg);
    }
  }

  return { opts, positional };
}

// ─── Commands ────────────────────────────────────────────────────────────────

async function cmdGenerate(opts) {
  const gen = new PlaywrightTestGenerator();

  const input = opts.input || opts.i;
  const framework = opts.framework || opts.f || 'pytest-playwright';
  const codeType = opts.type || opts.t || opts.codeType || 'standard';
  const pageName = opts.pageName || opts.page || 'Page';
  const testName = opts.testName || opts.test || 'test_playwright';
  const output = opts.output || opts.o;
  const testDataFile = opts.testData || opts.data;

  let testData = [];
  if (testDataFile) {
    try {
      const content = await import('fs').then(fs => fs.readFileSync(testDataFile, 'utf8'));
      testData = JSON.parse(content);
    } catch (err) {
      console.error(`⚠  Could not read test data file: ${err.message}`);
    }
  }

  const result = await gen.generate({
    input,
    framework,
    codeType,
    pageName,
    testName,
    testData
  });

  console.log(`\n✅ Generated ${result.codeType} test for ${result.framework}`);
  console.log(`📄 Language: ${result.language}`);
  console.log(`📋 Steps parsed: ${result.steps.length}\n`);

  if (output) {
    await import('fs').then(fs => fs.writeFileSync(output, result.code, 'utf8'));
    console.log(`💾 Written to: ${output}`);
  } else {
    console.log('--- Generated Code ---\n');
    console.log(result.code);
  }

  return result;
}

async function cmdAnalyze(opts) {
  const gen = new PlaywrightTestGenerator();

  const url = opts.url || opts.u;
  if (!url) {
    throw new Error('--url is required for analyze command');
  }

  const mock = opts.mock === 'true' || opts.mock === '1';
  const result = await gen.analyzeUrl(url, { mock });

  console.log(`\n🔍 Page Analysis: ${result.url}`);
  console.log(`   Title: ${result.title}`);
  console.log(`   Locators found: ${Object.keys(result.locators).length}\n`);

  for (const [name, selector] of Object.entries(result.locators)) {
    console.log(`   ${name.padEnd(30)} → ${selector}`);
  }

  return result;
}

async function cmdExtractLocators(opts) {
  const html = opts.html || opts.h;
  if (!html) {
    throw new Error('--html is required for extract-locators command');
  }

  const result = LocatorExtractor.extract(html);
  const output = opts.output || opts.o;

  console.log(`\n🔎 Extracted ${Object.keys(result.locators).length} locators\n`);

  const json = JSON.stringify(result, null, 2);
  if (output) {
    await import('fs').then(fs => fs.writeFileSync(output, json, 'utf8'));
    console.log(`💾 Written to: ${output}`);
  } else {
    console.log(json);
  }

  return result;
}

async function cmdInteractive() {
  const readline = await import('readline');
  const gen = new PlaywrightTestGenerator();

  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  const question = (q) => new Promise(resolve => rl.question(q, resolve));

  console.log('\n🎭 Playwright Test Generator — Interactive Mode\n');

  const framework = await question('Framework [pytest-playwright]: ') || 'pytest-playwright';
  const codeType = await question('Code type [standard] (pom/standard/data-driven): ') || 'standard';
  const pageName = await question('Page name [MyPage]: ') || 'MyPage';
  console.log('\nEnter your test steps (one per line, empty line to finish):\n');

  const steps = [];
  let line;
  while ((line = await question('  > ')) !== '') {
    steps.push(line);
  }

  const input = steps.join(', ');
  const result = await gen.generate({ input, framework, codeType, pageName });

  console.log('\n--- Generated Code ---\n');
  console.log(result.code);

  rl.close();
  return result;
}

// ─── Main ────────────────────────────────────────────────────────────────────

async function main() {
  const [, , command, ...args] = process.argv;

  if (!command || command === '--help' || command === '-h') {
    console.log(`playwright-test-generator <command>

Commands:
  generate         Generate test code from natural language
  analyze          Analyze URL and extract page structure + locators
  extract-locators Extract locators from HTML snippet
  interactive      Guided interactive test generation

Options for generate:
  --input, -i          Natural language test description
  --framework, -f       pytest-playwright | jest-playwright | native-playwright
  --type, -t           pom | standard | data-driven
  --page               Page name for POM (default: Page)
  --test               Test function name (default: test_playwright)
  --output, -o         Write output to file
  --test-data          JSON file with test data for data-driven tests
  --mock               Use mock data for analyze (for testing)

Examples:
  node src/index.js generate -i "Click login, enter email and password" -f pytest-playwright -t pom
  node src/index.js analyze --url https://example.com --mock
  node src/index.js extract-locators --html '<input id="email" />'
  node src/index.js interactive
`);
    process.exit(0);
  }

  try {
    const { opts, positional } = parseArgs(args);

    switch (command) {
      case 'generate':
        await cmdGenerate(opts);
        break;
      case 'analyze':
        await cmdAnalyze(opts);
        break;
      case 'extract-locators':
      case 'extract':
        await cmdExtractLocators(opts);
        break;
      case 'interactive':
      case 'i':
        await cmdInteractive();
        break;
      default:
        console.error(`Unknown command: ${command}`);
        console.error('Run with --help to see available commands.');
        process.exit(1);
    }
  } catch (err) {
    console.error(`\n❌ Error: ${err.message}\n`);
    process.exit(1);
  }
}

main();
