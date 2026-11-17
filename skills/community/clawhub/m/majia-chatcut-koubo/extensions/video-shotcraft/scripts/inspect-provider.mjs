#!/usr/bin/env node

import {execFileSync} from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

const extensionRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const repositoryRoot = path.resolve(extensionRoot, "../..");
const manifest = JSON.parse(fs.readFileSync(path.join(extensionRoot, "manifest.json"), "utf8"));
const allowlist = JSON.parse(fs.readFileSync(path.join(extensionRoot, "allowlist.json"), "utf8"));

function usage(message) {
  if (message) console.error(message);
  console.error("Usage: node extensions/video-shotcraft/scripts/inspect-provider.mjs --checkout <video-shotcraft checkout>");
  process.exit(2);
}

const args = process.argv.slice(2);
if (args.length !== 2 || args[0] !== "--checkout" || !args[1]) usage();

const checkout = path.resolve(args[1]);
if (!fs.statSync(checkout, {throwIfNoEntry: false})?.isDirectory()) {
  usage("checkout must be an existing directory");
}

let revision;
try {
  revision = execFileSync("git", ["-C", checkout, "rev-parse", "HEAD"], {encoding: "utf8"}).trim();
} catch {
  console.error("FAIL provider checkout is not a readable git worktree");
  process.exit(1);
}
if (revision !== manifest.revision) {
  console.error(`FAIL provider revision ${revision} does not match pinned ${manifest.revision}`);
  process.exit(1);
}

const libraryFile = path.join(checkout, manifest.libraryPath);
if (!fs.statSync(libraryFile, {throwIfNoEntry: false})?.isFile()) {
  console.error(`FAIL missing provider library: ${manifest.libraryPath}`);
  process.exit(1);
}
const library = JSON.parse(fs.readFileSync(libraryFile, "utf8"));
const cards = new Map((library.cards ?? []).map((card) => [card.name, card]));
const errors = [];

for (const adapter of allowlist) {
  const card = cards.get(adapter.card);
  if (!card) {
    errors.push(`missing card: ${adapter.card}`);
    continue;
  }
  const styles = new Set((card.styles ?? []).map((style) => style.key));
  for (const style of adapter.styles) {
    if (!styles.has(style)) errors.push(`${adapter.card}: missing style ${style}`);
  }
  if (!fs.statSync(path.join(checkout, card.source), {throwIfNoEntry: false})?.isFile()) {
    errors.push(`${adapter.card}: missing source document ${card.source}`);
  }
}

if (errors.length) {
  for (const error of errors) console.error(`FAIL ${error}`);
  process.exit(1);
}

console.log(`video-shotcraft provider passed: revision=${revision}, cards=${allowlist.length}, repository=${path.relative(repositoryRoot, extensionRoot)}`);
