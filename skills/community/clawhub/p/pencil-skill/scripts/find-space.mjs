#!/usr/bin/env node
import { loadPen, parseArgs, printHelpAndExit, fail, findNodeById, toNumberOrFail } from './_utils.mjs';

const HELP = `Usage: node scripts/find-space.mjs <file.pen> --width <n> --height <n> [--direction right|below|left|above] [--near <nodeId>] [--padding <n>]`;
const args = parseArgs(process.argv.slice(2));
if (args.help) printHelpAndExit(HELP);
const file = args._[0];
if (!file) printHelpAndExit(HELP, 1);
if (args.width === undefined || args.height === undefined) printHelpAndExit(HELP, 1);

const width = toNumberOrFail(args.width, 'width');
const height = toNumberOrFail(args.height, 'height');
const padding = args.padding !== undefined ? toNumberOrFail(args.padding, 'padding') : 24;
const direction = args.direction || 'right';
if (!['right', 'below', 'left', 'above'].includes(direction)) fail(`Invalid --direction: ${direction}`);

const pen = loadPen(file);
const top = pen.children || [];

function rectOf(node) {
  const x = Number(node?.x ?? 0);
  const y = Number(node?.y ?? 0);
  const w = Number(node?.width ?? 0);
  const h = Number(node?.height ?? 0);
  return { x: isNaN(x) ? 0 : x, y: isNaN(y) ? 0 : y, w: isNaN(w) ? 0 : w, h: isNaN(h) ? 0 : h };
}

const obstacles = top.map(rectOf);

let anchor = { x: 0, y: 0, w: 0, h: 0 };
if (args.near) {
  const found = findNodeById(pen, args.near);
  if (!found) fail(`Node not found for --near: ${args.near}`);
  anchor = rectOf(found.node);
} else if (obstacles.length > 0) {
  const minX = Math.min(...obstacles.map((r) => r.x));
  const minY = Math.min(...obstacles.map((r) => r.y));
  const maxR = Math.max(...obstacles.map((r) => r.x + r.w));
  const maxB = Math.max(...obstacles.map((r) => r.y + r.h));
  anchor = { x: minX, y: minY, w: maxR - minX, h: maxB - minY };
}

function overlaps(a, b) {
  return !(a.x + a.w <= b.x || b.x + b.w <= a.x || a.y + a.h <= b.y || b.y + b.h <= a.y);
}

function findCandidate() {
  const step = Math.max(8, Math.min(width, height, 32));
  const starts = {
    right: { x: anchor.x + anchor.w + padding, y: anchor.y },
    below: { x: anchor.x, y: anchor.y + anchor.h + padding },
    left: { x: anchor.x - width - padding, y: anchor.y },
    above: { x: anchor.x, y: anchor.y - height - padding },
  };

  const s = starts[direction];
  for (let t = 0; t < 200; t += 1) {
    let cand = { x: s.x, y: s.y, w: width, h: height };
    if (direction === 'right' || direction === 'left') cand.y += t * step;
    else cand.x += t * step;

    if (!obstacles.some((o) => overlaps(cand, o))) return cand;
  }

  return { x: s.x, y: s.y, w: width, h: height };
}

const pos = findCandidate();
process.stdout.write(`${JSON.stringify({ x: pos.x, y: pos.y })}\n`);
