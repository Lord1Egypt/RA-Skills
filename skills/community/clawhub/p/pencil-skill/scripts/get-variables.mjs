#!/usr/bin/env node
import { loadPen, parseArgs, printHelpAndExit } from './_utils.mjs';

const HELP = `Usage: node scripts/get-variables.mjs <file.pen> [--format table|json]`;
const args = parseArgs(process.argv.slice(2));
if (args.help) printHelpAndExit(HELP);
const file = args._[0];
if (!file) printHelpAndExit(HELP, 1);

const pen = loadPen(file);
const format = args.format || 'table';

if (format === 'json') {
  process.stdout.write(`${JSON.stringify({ themes: pen.themes || {}, variables: pen.variables || {} }, null, 2)}\n`);
  process.exit(0);
}

const themes = pen.themes || {};
const variables = pen.variables || {};

let out = '=== Themes ===\n';
for (const [axis, values] of Object.entries(themes)) {
  out += `  ${axis}: ${(values || []).join(', ')}\n`;
}
if (Object.keys(themes).length === 0) out += '  (none)\n';

out += '\n=== Variables ===\n';
for (const [name, entry] of Object.entries(variables)) {
  const type = entry?.type || 'unknown';
  const value = entry?.value;
  let rendered;
  if (Array.isArray(value)) {
    rendered = value
      .map((v) => {
        const tv = v?.theme ? ` (${Object.entries(v.theme).map(([k, val]) => `${k}:${val}`).join(', ')})` : '';
        return `${JSON.stringify(v?.value)}${tv}`;
      })
      .join(' / ');
  } else {
    rendered = JSON.stringify(value);
  }
  out += `  $${name}  ${type}  ${rendered}\n`;
}
if (Object.keys(variables).length === 0) out += '  (none)\n';

process.stdout.write(out);
