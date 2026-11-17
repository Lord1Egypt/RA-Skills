#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const errors = [];
const readJson = (relative) => JSON.parse(fs.readFileSync(path.join(root, relative), "utf8"));
const exists = (relative) => fs.statSync(path.join(root, relative), {throwIfNoEntry: false})?.isFile();

function fail(message) {
  errors.push(message);
}

function unique(values, label) {
  const seen = new Set();
  for (const value of values) {
    if (seen.has(value)) fail(`${label}: duplicate ${value}`);
    seen.add(value);
  }
}

function sha256(relative) {
  return `sha256:${crypto.createHash("sha256").update(fs.readFileSync(path.join(root, relative))).digest("hex")}`;
}

const registry = readJson("extensions/registry.json");
unique(registry.packs.map((pack) => pack.id), "registry");
for (const pack of registry.packs) {
  if (pack.required !== false) fail(`${pack.id}: extension must remain optional`);
  if (!exists(pack.manifest)) {
    fail(`${pack.id}: missing manifest ${pack.manifest}`);
    continue;
  }
  const manifest = readJson(pack.manifest);
  if (manifest.id !== pack.id) fail(`${pack.id}: manifest id mismatch`);
  if (manifest.mode !== pack.mode) fail(`${pack.id}: manifest mode mismatch`);
}

const cuttipsManifest = readJson("extensions/cuttips-kb/manifest.json");
const categories = readJson("extensions/cuttips-kb/data/categories.json");
const knowledge = readJson("extensions/cuttips-kb/data/knowledge-items.json");
const rules = readJson("extensions/cuttips-kb/data/rules.json");
const sources = readJson("extensions/cuttips-kb/data/sources.json");
const stats = readJson("extensions/cuttips-kb/data/stats.json");

const expectedCounts = {
  categories: categories.length,
  knowledgeItems: knowledge.length,
  rules: rules.length,
  sources: sources.length,
  reviewedSources: sources.filter((source) => source.evidenceTier === "A").length,
  secondaryReviewPending: sources.filter((source) => source.evidenceTier === "B").length,
};
for (const [key, actual] of Object.entries(expectedCounts)) {
  if (cuttipsManifest.content[key] !== actual) {
    fail(`cuttips manifest ${key}=${cuttipsManifest.content[key]} but data=${actual}`);
  }
}
if (stats.sourceCount !== sources.length
  || stats.knowledgeItemCount !== knowledge.length
  || stats.machineRuleCount !== rules.length) {
  fail("cuttips stats counts do not match data");
}
if (stats.reviewedCount + stats.getnoteOnlyCount !== stats.sourceCount) {
  fail("cuttips review counts do not sum to source count");
}

const categoryIds = new Set(categories.map((category) => category.id));
const knowledgeIds = new Set(knowledge.map((item) => item.id));
const sourceIds = new Set(sources.map((source) => source.id));
unique([...categoryIds], "cuttips categories");
unique([...knowledgeIds], "cuttips knowledge");
unique([...sourceIds], "cuttips sources");

for (const item of knowledge) {
  if (!categoryIds.has(item.category)) fail(`${item.id}: unknown category ${item.category}`);
  for (const sourceRef of item.sourceRefs) {
    if (!sourceIds.has(sourceRef)) fail(`${item.id}: unknown sourceRef ${sourceRef}`);
  }
}
for (const rule of rules) {
  if (!knowledgeIds.has(rule.knowledgeRef)) fail(`${rule.id}: unknown knowledgeRef ${rule.knowledgeRef}`);
  for (const sourceRef of rule.evidence ?? []) {
    if (!sourceIds.has(sourceRef)) fail(`${rule.id}: unknown evidence ${sourceRef}`);
  }
}

for (const [name, expected] of Object.entries(cuttipsManifest.files)) {
  const relative = `extensions/cuttips-kb/data/${name}`;
  if (!exists(relative)) fail(`cuttips missing file ${name}`);
  else if (sha256(relative) !== expected) fail(`cuttips checksum mismatch ${name}`);
}

const publicSnapshot = JSON.stringify({categories, knowledge, rules, sources, stats});
for (const forbidden of [
  "/Users/",
  "xfyun",
  "order_id",
  "backup_path",
  "signed_url",
]) {
  if (publicSnapshot.toLocaleLowerCase("en-US").includes(forbidden.toLocaleLowerCase("en-US"))) {
    fail(`cuttips public snapshot contains forbidden marker ${forbidden}`);
  }
}

const shotcraftManifest = readJson("extensions/video-shotcraft/manifest.json");
const allowlist = readJson("extensions/video-shotcraft/allowlist.json");
if (!/^[0-9a-f]{40}$/u.test(shotcraftManifest.revision)) fail("video-shotcraft revision must be a full commit SHA");
if (shotcraftManifest.mode !== "external") fail("video-shotcraft must remain external");
if (shotcraftManifest.license !== "Apache-2.0") fail("video-shotcraft license declaration drifted");
unique(allowlist.map((adapter) => adapter.card), "video-shotcraft allowlist");
const blockedCards = new Set(["strobe-black-frames", "anime-impact", "bubble-swarm"]);
for (const adapter of allowlist) {
  if (blockedCards.has(adapter.card)) fail(`${adapter.card}: unsafe or unsuitable card must not be enabled`);
  for (const key of [
    "styles",
    "semanticSignals",
    "allowedStates",
    "blockedConditions",
    "fallback",
    "compositionOwner",
    "renderMode",
  ]) {
    if (!(key in adapter) || (Array.isArray(adapter[key]) && adapter[key].length === 0)) {
      fail(`${adapter.card}: missing ${key}`);
    }
  }
  if (adapter.compositionOwner !== "external-mg") fail(`${adapter.card}: invalid composition owner`);
  if (!Number.isInteger(adapter.maxUsesPerMinute) || adapter.maxUsesPerMinute < 1) {
    fail(`${adapter.card}: invalid maxUsesPerMinute`);
  }
}

if (errors.length) {
  for (const error of errors) console.error(`FAIL ${error}`);
  console.error(`extension validation failed: ${errors.length} error(s)`);
  process.exit(1);
}
console.log(`extension validation passed: packs=${registry.packs.length}, cuttips=${sources.length} sources/${knowledge.length} cards/${rules.length} rules, shotcraft=${allowlist.length} adapters`);
