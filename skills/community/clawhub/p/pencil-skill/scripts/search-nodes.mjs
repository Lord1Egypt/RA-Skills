#!/usr/bin/env node
import { loadPen, parseArgs, printHelpAndExit, fail, walkNodes } from './_utils.mjs';

const HELP = `Usage: node scripts/search-nodes.mjs <file.pen> [--type <type>] [--name <regex>] [--prop <key=value>] [--reusable] [--depth <n>]`;
const args = parseArgs(process.argv.slice(2));
if (args.help) printHelpAndExit(HELP);
const file = args._[0];
if (!file) printHelpAndExit(HELP, 1);

const pen = loadPen(file);
const maxDepth = args.depth !== undefined ? Number(args.depth) : Infinity;
if ((maxDepth !== Infinity && !Number.isFinite(maxDepth)) || maxDepth < 0) fail(`Invalid --depth: ${args.depth}`);

let nameRegex = null;
if (args.name) {
  try {
    nameRegex = new RegExp(args.name);
  } catch (error) {
    fail(`Invalid --name regex: ${error.message}`);
  }
}

const propFilters = [];
const propsRaw = args.prop === undefined ? [] : (Array.isArray(args.prop) ? args.prop : [args.prop]);
for (const token of propsRaw) {
  const idx = token.indexOf('=');
  if (idx <= 0) fail(`Invalid --prop format: ${token}. Expected key=value`);
  const key = token.slice(0, idx);
  const value = token.slice(idx + 1);
  propFilters.push({ key, value });
}

const results = [];
walkNodes(pen, (node, ctx) => {
  if (ctx.depth > maxDepth) return;
  if (args.type && node.type !== args.type) return;
  if (args.reusable && node.reusable !== true) return;
  if (nameRegex && !nameRegex.test(String(node.name || ''))) return;

  for (const { key, value } of propFilters) {
    if (!(key in node)) return;
    const nodeVal = node[key];
    const normalized = typeof nodeVal === 'string' ? nodeVal : JSON.stringify(nodeVal);
    if (normalized !== value) return;
  }

  results.push({
    id: node.id,
    type: node.type,
    name: node.name ?? null,
    path: ctx.pathIds.join('/'),
  });
}, { maxDepth });

process.stdout.write(`${JSON.stringify(results, null, 2)}\n`);
