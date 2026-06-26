#!/usr/bin/env node

import { promises as fs } from "node:fs";
import path from "node:path";
import os from "node:os";

const TARGET_FULL = "openai/gpt-5.3";
const NEXT_FULL = "openai/gpt-5.2";
const TARGET_BARE = "gpt-5.3";
const NEXT_BARE = "gpt-5.2";
const BARE_MODEL_KEYS = new Set([
  "model",
  "primary",
  "defaultModel",
  "activeModel",
  "selectedModel",
  "modelId",
]);

function parseArgs(argv) {
  let apply = false;
  let root = path.join(os.homedir(), ".openclaw");
  for (let i = 2; i < argv.length; i += 1) {
    const token = argv[i];
    if (token === "--apply") {
      apply = true;
      continue;
    }
    if (token === "--root") {
      const next = argv[i + 1];
      if (!next) {
        throw new Error("Missing value for --root");
      }
      root = path.resolve(next);
      i += 1;
      continue;
    }
    if (token === "--help" || token === "-h") {
      printHelp();
      process.exit(0);
    }
    throw new Error(`Unknown argument: ${token}`);
  }
  return { apply, root };
}

function printHelp() {
  console.log(
    [
      "Usage:",
      "  node switch-model-to-gpt-5.2.js [--apply] [--root <openclaw-home>]",
      "",
      "Defaults:",
      "  --root $HOME/.openclaw",
      "  no --apply => dry-run only",
    ].join("\n"),
  );
}

function isProviderCatalogIdOrName(pathParts) {
  const key = pathParts[pathParts.length - 1];
  if (key !== "id" && key !== "name") return false;
  for (let i = 0; i < pathParts.length - 3; i += 1) {
    if (
      pathParts[i] === "providers" &&
      typeof pathParts[i + 1] === "string" &&
      pathParts[i + 2] === "models" &&
      typeof pathParts[i + 3] === "number"
    ) {
      return true;
    }
  }
  return false;
}

function shouldRewriteBareValue(pathParts) {
  const key = pathParts[pathParts.length - 1];
  return typeof key === "string" && BARE_MODEL_KEYS.has(key);
}

function rewriteTree(node, pathParts, stats) {
  if (typeof node === "string") {
    if (node === TARGET_FULL) {
      stats.full += 1;
      return NEXT_FULL;
    }
    if (node === TARGET_BARE && shouldRewriteBareValue(pathParts) && !isProviderCatalogIdOrName(pathParts)) {
      stats.bare += 1;
      return NEXT_BARE;
    }
    return node;
  }
  if (Array.isArray(node)) {
    return node.map((item, index) => rewriteTree(item, pathParts.concat(index), stats));
  }
  if (node && typeof node === "object") {
    const out = {};
    for (const [k, v] of Object.entries(node)) {
      out[k] = rewriteTree(v, pathParts.concat(k), stats);
    }
    return out;
  }
  return node;
}

async function pathExists(filePath) {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

async function collectTargets(root) {
  const files = [path.join(root, "openclaw.json")];
  const agentsDir = path.join(root, "agents");
  if (!(await pathExists(agentsDir))) return files;
  const dirents = await fs.readdir(agentsDir, { withFileTypes: true });
  for (const entry of dirents) {
    if (!entry.isDirectory()) continue;
    const agentRoot = path.join(agentsDir, entry.name);
    files.push(path.join(agentRoot, "agent", "models.json"));
    files.push(path.join(agentRoot, "sessions", "sessions.json"));
  }
  return files;
}

async function rewriteFile(filePath, apply) {
  const stats = { full: 0, bare: 0 };
  if (!(await pathExists(filePath))) {
    return { filePath, exists: false, changed: false, stats };
  }
  const raw = await fs.readFile(filePath, "utf8");
  const json = JSON.parse(raw);
  const next = rewriteTree(json, [], stats);
  const changed = stats.full + stats.bare > 0;
  if (changed && apply) {
    const stamp = new Date().toISOString().replace(/[:.]/g, "-");
    const backupPath = `${filePath}.bak.${stamp}`;
    await fs.copyFile(filePath, backupPath);
    await fs.writeFile(filePath, `${JSON.stringify(next, null, 2)}\n`, "utf8");
    return { filePath, exists: true, changed, stats, backupPath };
  }
  return { filePath, exists: true, changed, stats };
}

function formatResult(result) {
  if (!result.exists) return `SKIP  ${result.filePath} (not found)`;
  const count = result.stats.full + result.stats.bare;
  if (!result.changed) return `OK    ${result.filePath} (no changes)`;
  if (result.backupPath) {
    return `WRITE ${result.filePath} (${count} updates, backup: ${result.backupPath})`;
  }
  return `PLAN  ${result.filePath} (${count} updates)`;
}

async function main() {
  const { apply, root } = parseArgs(process.argv);
  const files = await collectTargets(root);
  const results = [];
  for (const file of files) {
    results.push(await rewriteFile(file, apply));
  }
  for (const result of results) {
    console.log(formatResult(result));
  }
  const total = results.reduce((sum, r) => sum + r.stats.full + r.stats.bare, 0);
  console.log(`Total updates: ${total}`);
  console.log(apply ? "Mode: apply" : "Mode: dry-run");
}

main().catch((error) => {
  console.error(`Failed: ${error instanceof Error ? error.message : String(error)}`);
  process.exit(1);
});
