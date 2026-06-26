#!/usr/bin/env node
import { loadPen, parseArgs, printHelpAndExit, fail, findNodeById } from './_utils.mjs';

const HELP = `Usage: node scripts/read-tree.mjs <file.pen> [--id <nodeId>] [--depth <n>] [--types-only]\n\nPrint node tree in indented format.`;

const args = parseArgs(process.argv.slice(2));
if (args.help) printHelpAndExit(HELP);

const file = args._[0];
if (!file) printHelpAndExit(HELP, 1);

const pen = loadPen(file);
const maxDepth = args.depth !== undefined ? Number(args.depth) : Infinity;
if ((maxDepth !== Infinity && !Number.isFinite(maxDepth)) || maxDepth < 0) fail(`Invalid --depth: ${args.depth}`);
const typesOnly = Boolean(args['types-only']);

let roots = pen.children || [];
if (args.id) {
  const found = findNodeById(pen, args.id);
  if (!found) fail(`Node not found: ${args.id}`);
  roots = [found.node];
}

function nodeLabel(node) {
  const type = node.type || 'unknown';
  const namePart = node.name ? ` \"${node.name}\"` : '';
  const idPart = node.id ? ` (id: ${node.id})` : '';

  if (typesOnly) return `${type}${namePart}${idPart}`;

  const sizeBits = [];
  if (node.width !== undefined && node.height !== undefined) {
    sizeBits.push(`${node.width}x${node.height}`);
  } else if (node.width !== undefined) {
    sizeBits.push(`w:${node.width}`);
  } else if (node.height !== undefined) {
    sizeBits.push(`h:${node.height}`);
  }
  if (node.layout) sizeBits.push(`layout: ${node.layout}`);
  if (node.gap !== undefined) sizeBits.push(`gap: ${node.gap}`);

  const tail = sizeBits.length > 0 ? ` [${sizeBits.join(', ')}]` : '';
  return `${type}${namePart}${idPart}${tail}`;
}

function printNode(node, depth) {
  if (depth > maxDepth) return;
  process.stdout.write(`${'  '.repeat(depth)}${nodeLabel(node)}\n`);
  if (depth >= maxDepth) return;
  for (const child of node.children || []) {
    printNode(child, depth + 1);
  }
}

for (const root of roots) {
  printNode(root, 0);
}
