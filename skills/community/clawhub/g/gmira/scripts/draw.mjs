#!/usr/bin/env node
// Draw material worlds by external index, and print what was drawn.
//
//   node draw.mjs <slug> [salt] [--count N]
//
// A model's ranking of design options is a deterministic function of its priors, so "rank harder"
// cannot beat the prior. Only an outside assignment can. This script is that outside source.
// Same inputs, same worlds, so a direction can be reproduced and audited.

import { readFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const CATALOG = join(here, "..", "references", "playbooks", "worlds.md");

const argv = process.argv.slice(2);
const slug = argv.find((a) => !a.startsWith("--"));
const salt = argv.filter((a) => !a.startsWith("--"))[1] ?? new Date().toISOString().slice(0, 10);
const ci = argv.indexOf("--count");
const count = ci !== -1 ? Math.max(1, Math.min(20, Number(argv[ci + 1]) || 7)) : 7;

if (!slug) {
  console.error("usage: node draw.mjs <slug> [salt] [--count N]");
  console.error("  slug  the project or surface identifier, e.g. car-shop");
  console.error("  salt  defaults to today, so the same project can be re-rolled by date");
  process.exit(2);
}

const md = await readFile(CATALOG, "utf8").catch(() => {
  console.error(`cannot read ${CATALOG}`);
  process.exit(2);
});

// Parse "### NN. Name" through to the next "###" or "##".
const entries = new Map();
const re = /^### (\d{2})\. (.+)$/gm;
const heads = [...md.matchAll(re)];
for (let i = 0; i < heads.length; i++) {
  const n = Number(heads[i][1]);
  const start = heads[i].index + heads[i][0].length;
  const end = i + 1 < heads.length ? heads[i + 1].index : md.length;
  entries.set(n, { n, name: heads[i][2].trim(), body: md.slice(start, end).trim() });
}

const N = entries.size;
if (N === 0) {
  console.error("no worlds parsed from the catalog");
  process.exit(2);
}

// FNV-1a over "slug:salt", then a decorrelated second stream for successive draws.
let h = 2166136261;
for (const ch of `${slug}:${salt}`) {
  h ^= ch.charCodeAt(0);
  h = Math.imul(h, 16777619);
}
let state = h >>> 0;
const next = () => {
  state = Math.imul(state ^ 0x9e3779b9, 2654435761) >>> 0;
  return state;
};

// Draw `count` distinct indices.
const drawn = [];
const seen = new Set();
let guard = 0;
while (drawn.length < Math.min(count, N) && guard++ < 500) {
  const idx = (next() % N) + 1;
  if (seen.has(idx)) continue;
  seen.add(idx);
  drawn.push(idx);
}

const family = (body) => {
  const m = body.match(/^SOURCE\s+(.+)$/m);
  return m ? m[1].slice(0, 72) : "";
};

console.log(`\nseed        ${slug}:${salt}`);
console.log(`catalog     ${N} worlds`);
console.log(`drawn       ${drawn.join(", ")}\n`);
console.log("Candidates. Discard any that collide with the category rut or its obvious opposite,");
console.log("then fuse the two strongest and judge the fusion on exactly two axes.\n");

for (const i of drawn) {
  const e = entries.get(i);
  console.log(`  ${String(e.n).padStart(2, "0")}  ${e.name}`);
  console.log(`      ${family(e.body)}`);
}

const [a, b] = drawn;
console.log(`\nFull entries for the first two:\n`);
for (const i of [a, b]) {
  const e = entries.get(i);
  console.log(`### ${String(e.n).padStart(2, "0")}. ${e.name}`);
  console.log(e.body);
  console.log("");
}

console.log(`Record the seed "${slug}:${salt}" in the direction contract's FORM block.`);
console.log("A direction whose seed is not written down cannot be reproduced or audited.\n");
