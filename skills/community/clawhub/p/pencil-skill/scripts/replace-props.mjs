#!/usr/bin/env node
import {
  loadPen,
  savePen,
  backupPen,
  parseArgs,
  printHelpAndExit,
  fail,
  parseJsonOrFail,
  walkNodes,
  deepMerge,
  findNodeById,
} from './_utils.mjs';

const HELP = `Usage: node scripts/replace-props.mjs <file.pen> --match '<JSON>' --replace '<JSON>' [--parent-ids <id1,id2>] [--dry-run]`;
const args = parseArgs(process.argv.slice(2));
if (args.help) printHelpAndExit(HELP);
const file = args._[0];
if (!file) printHelpAndExit(HELP, 1);
if (!args.match || !args.replace) fail('Both --match and --replace are required');

const matchObj = parseJsonOrFail(args.match, '--match JSON');
const replaceObj = parseJsonOrFail(args.replace, '--replace JSON');
const pen = loadPen(file);

function normalizeAliasesInNode(value) {
  if (!value || typeof value !== 'object') return value;

  if (!Array.isArray(value)) {
    const aliases = [
      ['fills', 'fill'],
      ['strokes', 'stroke'],
      ['effects', 'effect'],
    ];
    for (const [plural, singular] of aliases) {
      if (plural in value) {
        if (!(singular in value)) value[singular] = value[plural];
        delete value[plural];
      }
    }
  }

  if (Array.isArray(value)) {
    for (const item of value) normalizeAliasesInNode(item);
    return value;
  }

  for (const child of Object.values(value)) normalizeAliasesInNode(child);
  return value;
}

const parentIds = args['parent-ids'] ? String(args['parent-ids']).split(',').map((s) => s.trim()).filter(Boolean) : null;

function matches(node, pattern) {
  for (const [k, v] of Object.entries(pattern)) {
    if (!(k in node)) return false;
    const nodeVal = node[k];
    if (v && typeof v === 'object') {
      if (!nodeVal || typeof nodeVal !== 'object') return false;
      if (!matches(nodeVal, v)) return false;
    } else if (nodeVal !== v) {
      return false;
    }
  }
  return true;
}

const targets = [];
if (parentIds && parentIds.length > 0) {
  for (const pid of parentIds) {
    const found = findNodeById(pen, pid);
    if (!found) fail(`Parent id not found: ${pid}`);
    const root = found.node;
    walkNodes({ children: [root] }, (node, ctx) => {
      if (matches(node, matchObj)) targets.push({ node, path: [pid, ...ctx.pathIds].filter(Boolean).join('/') });
    });
  }
} else {
  walkNodes(pen, (node, ctx) => {
    if (matches(node, matchObj)) targets.push({ node, path: ctx.pathIds.join('/') });
  });
}

if (args['dry-run']) {
  process.stdout.write(`${JSON.stringify({ matched: targets.length, paths: targets.map((t) => t.path) }, null, 2)}\n`);
  process.exit(0);
}

backupPen(file);
for (const t of targets) {
  Object.assign(t.node, normalizeAliasesInNode(deepMerge(t.node, replaceObj)));
}
savePen(file, pen);
process.stdout.write(`OK: replaced ${targets.length} node(s)\n`);
