#!/usr/bin/env node
/**
 * gray-matter CLI wrapper — parse/stringify front-matter from files or stdin.
 *
 * Usage:
 *   node parse.js <file>                    Parse front-matter from a file
 *   node parse.js --stdin < string          Parse front-matter from stdin
 *   node parse.js <file> --data-only        Output only the data (YAML)
 *   node parse.js <file> --content-only     Output only the content
 *   node parse.js <file> --excerpt          Include excerpt in output
 *   node parse.js <file> --lang toml        Force TOML parsing
 *   node parse.js <file> --delims ~~~       Custom delimiters
 *   node parse.js <file> --stringify        Stringify back to front-matter
 *   node parse.js <file> --test             Test if string has front-matter
 *
 * Output: JSON to stdout (except --data-only, --content-only, --test, --stringify)
 */

const fs = require('fs');
const path = require('path');

// Resolve gray-matter: prefer local install, fall back to global
let matter;
try {
  matter = require('gray-matter');
} catch {
  // Try installing locally in the scripts directory
  const { execSync } = require('child_process');
  const scriptsDir = __dirname;
  try {
    execSync('npm install gray-matter', { cwd: scriptsDir, stdio: 'ignore' });
    matter = require(path.join(scriptsDir, 'node_modules', 'gray-matter'));
  } catch (e) {
    console.error('Error: gray-matter is not installed. Run: npm install gray-matter');
    process.exit(1);
  }
}

function parseArgs(argv) {
  const args = { _: [], options: {} };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--stdin') {
      args.stdin = true;
    } else if (a === '--data-only') {
      args.dataOnly = true;
    } else if (a === '--content-only') {
      args.contentOnly = true;
    } else if (a === '--excerpt') {
      args.options.excerpt = true;
    } else if (a === '--test') {
      args.testOnly = true;
    } else if (a === '--stringify') {
      args.stringify = true;
    } else if (a === '--lang' && argv[i + 1]) {
      args.options.language = argv[++i];
    } else if (a === '--delims' && argv[i + 1]) {
      args.options.delimiters = argv[++i];
    } else if (a === '--excerpt-sep' && argv[i + 1]) {
      args.options.excerpt_separator = argv[++i];
    } else if (!a.startsWith('--')) {
      args._.push(a);
    }
  }
  return args;
}

function getInput(args) {
  if (args.stdin) {
    const chunks = [];
    process.stdin.setEncoding('utf8');
    return new Promise((resolve) => {
      process.stdin.on('data', (d) => chunks.push(d));
      process.stdin.on('end', () => resolve(chunks.join('')));
      process.stdin.resume();
    });
  }
  if (args._.length > 0) {
    const filepath = args._[0];
    if (!fs.existsSync(filepath)) {
      console.error(`Error: file not found: ${filepath}`);
      process.exit(1);
    }
    return Promise.resolve(fs.readFileSync(filepath, 'utf8'));
  }
  console.error('Error: no input. Provide a file path or use --stdin');
  process.exit(1);
}

async function main() {
  const args = parseArgs(process.argv);
  const input = await getInput(args);

  if (args.testOnly) {
    console.log(matter.test(input, args.options) ? 'true' : 'false');
    return;
  }

  if (args.stringify) {
    // For stringify, input is content, --data comes via stdin as JSON
    let data = {};
    try {
      data = JSON.parse(input);
    } catch {
      console.error('Error: --stringify requires JSON data as input');
      process.exit(1);
    }
    console.log(matter.stringify('', data, args.options));
    return;
  }

  const result = matter(input, args.options);

  if (args.dataOnly) {
    if (result.data && Object.keys(result.data).length > 0) {
      const yaml = require('js-yaml');
      console.log(yaml.dump(result.data));
    }
    return;
  }

  if (args.contentOnly) {
    process.stdout.write(result.content);
    return;
  }

  const output = {
    data: result.data || {},
    content: result.content || '',
    language: result.language || 'yaml',
    isEmpty: result.isEmpty || false,
  };

  if (result.excerpt) output.excerpt = result.excerpt;
  if (result.empty) output.empty = result.empty;
  if (result.matter) output.matter = result.matter;

  console.log(JSON.stringify(output, null, 2));
}

main().catch((err) => {
  console.error('Error:', err.message);
  process.exit(1);
});