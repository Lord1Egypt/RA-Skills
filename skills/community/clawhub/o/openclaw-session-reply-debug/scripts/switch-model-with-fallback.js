#!/usr/bin/env node

import { promises as fs } from "node:fs";
import path from "node:path";
import os from "node:os";
import { fileURLToPath } from "node:url";

const BARE_MODEL_KEYS = new Set([
  "model",
  "primary",
  "defaultModel",
  "activeModel",
  "selectedModel",
  "modelId",
]);

export function printHelp() {
  console.log(
    [
      "Usage:",
      "  node switch-model-with-fallback.js --primary <model> [--fallback <model> ...] [options]",
      "",
      "Required:",
      "  --primary <model>          Target primary model. Accepts gpt-5.4 or openai/gpt-5.4",
      "",
      "Optional:",
      "  --fallback <model>         Fallback model, repeatable",
      "  --provider <name>          Provider name for bare model refs (default: openai)",
      "  --root <path>              OpenClaw home (default: $HOME/.openclaw)",
      "  --no-probe                 Skip provider probes and force primary",
      "  --probe-timeout-ms <ms>    Probe timeout in ms (default: 20000)",
      "  --apply                    Apply changes (default: dry-run)",
      "  -h, --help                 Show this help",
      "",
      "Examples:",
      "  node switch-model-with-fallback.js --primary gpt-5.4 --fallback gpt-5.3 --fallback gpt-5.2",
      "  node switch-model-with-fallback.js --primary openai/gpt-5.4 --fallback openai/gpt-5.2 --apply",
    ].join("\n"),
  );
}

export function parseArgs(argv) {
  const options = {
    apply: false,
    root: path.join(os.homedir(), ".openclaw"),
    provider: "openai",
    primary: "",
    fallbacks: [],
    probe: true,
    probeTimeoutMs: 20_000,
  };

  for (let i = 2; i < argv.length; i += 1) {
    const token = argv[i];

    if (token === "--apply") {
      options.apply = true;
      continue;
    }
    if (token === "--no-probe") {
      options.probe = false;
      continue;
    }
    if (token === "--primary") {
      const next = argv[i + 1];
      if (!next) throw new Error("Missing value for --primary");
      options.primary = next;
      i += 1;
      continue;
    }
    if (token === "--fallback") {
      const next = argv[i + 1];
      if (!next) throw new Error("Missing value for --fallback");
      options.fallbacks.push(next);
      i += 1;
      continue;
    }
    if (token === "--provider") {
      const next = argv[i + 1];
      if (!next) throw new Error("Missing value for --provider");
      options.provider = next;
      i += 1;
      continue;
    }
    if (token === "--root") {
      const next = argv[i + 1];
      if (!next) throw new Error("Missing value for --root");
      options.root = path.resolve(next);
      i += 1;
      continue;
    }
    if (token === "--probe-timeout-ms") {
      const next = argv[i + 1];
      if (!next) throw new Error("Missing value for --probe-timeout-ms");
      const parsed = Number(next);
      if (!Number.isFinite(parsed) || parsed <= 0) {
        throw new Error("--probe-timeout-ms must be a positive number");
      }
      options.probeTimeoutMs = parsed;
      i += 1;
      continue;
    }
    if (token === "--help" || token === "-h") {
      printHelp();
      process.exit(0);
    }

    throw new Error(`Unknown argument: ${token}`);
  }

  if (!options.primary) {
    throw new Error("--primary is required");
  }

  return options;
}

export function normalizeModelRef(modelRef, provider) {
  const trimmed = modelRef.trim();
  if (!trimmed) {
    throw new Error("Model id cannot be empty");
  }

  if (trimmed.includes("/")) {
    const [p, ...rest] = trimmed.split("/");
    const bare = rest.join("/");
    if (!p || !bare) {
      throw new Error(`Invalid model reference: ${modelRef}`);
    }
    return {
      original: modelRef,
      provider: p,
      bare,
      full: `${p}/${bare}`,
    };
  }

  return {
    original: modelRef,
    provider,
    bare: trimmed,
    full: `${provider}/${trimmed}`,
  };
}

export function dedupeCandidates(candidates) {
  const seen = new Set();
  const out = [];
  for (const item of candidates) {
    if (seen.has(item.full)) continue;
    seen.add(item.full);
    out.push(item);
  }
  return out;
}

export function shouldRewriteBareValue(pathParts) {
  const key = pathParts[pathParts.length - 1];
  return typeof key === "string" && BARE_MODEL_KEYS.has(key);
}

export function isProviderCatalogIdOrName(pathParts) {
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

export function rewriteTree(node, pathParts, selected, replacements, stats) {
  if (typeof node === "string") {
    if (isProviderCatalogIdOrName(pathParts)) {
      return node;
    }
    if (replacements.full.has(node)) {
      stats.full += 1;
      return selected.full;
    }
    if (
      replacements.bare.has(node) &&
      shouldRewriteBareValue(pathParts)
    ) {
      stats.bare += 1;
      return selected.bare;
    }
    return node;
  }

  if (Array.isArray(node)) {
    return node.map((item, index) => rewriteTree(item, pathParts.concat(index), selected, replacements, stats));
  }

  if (node && typeof node === "object") {
    const out = {};
    for (const [k, v] of Object.entries(node)) {
      out[k] = rewriteTree(v, pathParts.concat(k), selected, replacements, stats);
    }
    return out;
  }

  return node;
}

export async function pathExists(filePath) {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

export async function collectTargets(root) {
  const files = [path.join(root, "openclaw.json")];
  const agentsDir = path.join(root, "agents");

  if (!(await pathExists(agentsDir))) {
    return files;
  }

  const dirents = await fs.readdir(agentsDir, { withFileTypes: true });
  for (const entry of dirents) {
    if (!entry.isDirectory()) continue;
    const agentRoot = path.join(agentsDir, entry.name);
    files.push(path.join(agentRoot, "agent", "models.json"));
    files.push(path.join(agentRoot, "sessions", "sessions.json"));
  }

  return files;
}

export async function loadOpenClawConfig(root) {
  const configPath = path.join(root, "openclaw.json");
  const raw = await fs.readFile(configPath, "utf8");
  return JSON.parse(raw);
}

export async function probeModel(providerConfig, model, timeoutMs) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch(`${providerConfig.baseUrl}/chat/completions`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${providerConfig.apiKey}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        model,
        messages: [{ role: "user", content: "reply with OK" }],
        max_tokens: 8,
      }),
      signal: controller.signal,
    });

    const body = await response.text();
    let parsed;
    try {
      parsed = JSON.parse(body);
    } catch {
      return {
        ok: false,
        status: response.status,
        detail: `NON_JSON ${body.slice(0, 200)}`,
      };
    }

    if (parsed.error) {
      return {
        ok: false,
        status: response.status,
        detail: parsed.error.message || JSON.stringify(parsed.error),
      };
    }

    const content = parsed.choices?.[0]?.message?.content;
    const text = typeof content === "string" ? content.trim().replace(/\s+/g, " ") : "";
    return {
      ok: response.ok,
      status: response.status,
      detail: text || "NO_CONTENT",
    };
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    return { ok: false, status: 0, detail: message };
  } finally {
    clearTimeout(timer);
  }
}

export function formatProbeLine(candidate, result) {
  if (result.ok) {
    return `OK    ${candidate.full} (HTTP ${result.status}, ${result.detail})`;
  }
  const status = result.status || "-";
  return `FAIL  ${candidate.full} (HTTP ${status}, ${result.detail})`;
}

export async function resolveSelectedModel(options, candidates, dependencies = {}) {
  const loadConfig = dependencies.loadConfig ?? loadOpenClawConfig;
  const probe = dependencies.probe ?? probeModel;

  if (!options.probe) {
    return {
      selected: candidates[0],
      results: [],
      mode: "force-primary",
    };
  }

  const config = await loadConfig(options.root);
  const providerConfig = config.models?.providers?.[options.provider];
  if (!providerConfig) {
    throw new Error(`Provider not configured in openclaw.json: ${options.provider}`);
  }
  if (!providerConfig.baseUrl) {
    throw new Error(`Missing baseUrl for provider: ${options.provider}`);
  }
  if (!providerConfig.apiKey) {
    throw new Error(`Missing apiKey for provider: ${options.provider}`);
  }

  const results = [];
  for (const candidate of candidates) {
    if (candidate.provider !== options.provider) {
      results.push({
        candidate,
        result: {
          ok: false,
          status: 0,
          detail: `Provider mismatch: expected ${options.provider}, got ${candidate.provider}`,
        },
      });
      continue;
    }

    const result = await probe(providerConfig, candidate.bare, options.probeTimeoutMs);
    results.push({ candidate, result });

    if (result.ok) {
      return {
        selected: candidate,
        results,
        mode: "probe",
      };
    }
  }

  return {
    selected: null,
    results,
    mode: "probe",
  };
}

export async function rewriteFile(filePath, apply, selected, replacements) {
  const stats = { full: 0, bare: 0 };

  if (!(await pathExists(filePath))) {
    return { filePath, exists: false, changed: false, stats };
  }

  const raw = await fs.readFile(filePath, "utf8");
  const json = JSON.parse(raw);
  const next = rewriteTree(json, [], selected, replacements, stats);
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

export function formatRewriteResult(result) {
  if (!result.exists) return `SKIP  ${result.filePath} (not found)`;

  const count = result.stats.full + result.stats.bare;
  if (!result.changed) return `OK    ${result.filePath} (no changes)`;

  if (result.backupPath) {
    return `WRITE ${result.filePath} (${count} updates, backup: ${result.backupPath})`;
  }

  return `PLAN  ${result.filePath} (${count} updates)`;
}

export function buildReplacements(candidates, selected) {
  const full = new Set();
  const bare = new Set();

  for (const model of candidates) {
    if (model.full === selected.full) continue;
    full.add(model.full);
    bare.add(model.bare);
  }

  return { full, bare };
}

function summarizeRewriteResults(results) {
  const changedFiles = results.filter((result) => result.changed).length;
  const missingFiles = results.filter((result) => !result.exists).length;
  const totalUpdates = results.reduce((sum, result) => sum + result.stats.full + result.stats.bare, 0);
  return {
    changedFiles,
    missingFiles,
    totalUpdates,
  };
}

export async function run(options, dependencies = {}) {
  const collectFiles = dependencies.collectTargets ?? collectTargets;
  const rewrite = dependencies.rewriteFile ?? rewriteFile;

  const candidates = dedupeCandidates(
    [options.primary, ...options.fallbacks].map((item) => normalizeModelRef(item, options.provider)),
  );
  for (const candidate of candidates) {
    if (candidate.provider !== options.provider) {
      throw new Error(
        `Candidate provider mismatch: ${candidate.full}. Use --provider ${candidate.provider} or keep all candidates under ${options.provider}.`,
      );
    }
  }

  const resolution = await resolveSelectedModel(options, candidates, dependencies);

  console.log(`Mode: ${options.apply ? "apply" : "dry-run"}`);
  console.log(`Selection: ${resolution.mode}`);
  console.log(`Provider: ${options.provider}`);
  console.log(`Candidates: ${candidates.map((x) => x.full).join(", ")}`);

  if (resolution.results.length > 0) {
    console.log("Probe results:");
    for (const line of resolution.results) {
      console.log(`  ${formatProbeLine(line.candidate, line.result)}`);
    }
  }

  if (!resolution.selected) {
    throw new Error("No available model found in primary/fallback candidates");
  }

  const selected = resolution.selected;
  console.log(`Selected model: ${selected.full} (bare: ${selected.bare})`);

  const replacements = buildReplacements(candidates, selected);
  const files = await collectFiles(options.root);
  const results = [];

  for (const file of files) {
    results.push(await rewrite(file, options.apply, selected, replacements));
  }

  for (const result of results) {
    console.log(formatRewriteResult(result));
  }

  const summary = summarizeRewriteResults(results);
  console.log(`Changed files: ${summary.changedFiles}`);
  console.log(`Missing files: ${summary.missingFiles}`);
  console.log(`Total updates: ${summary.totalUpdates}`);

  if (replacements.full.size + replacements.bare.size === 0) {
    console.log("Nothing to rewrite: only one candidate model was provided.");
  }

  return {
    candidates,
    resolution,
    replacements,
    results,
    summary,
  };
}

async function main(argv = process.argv) {
  const options = parseArgs(argv);
  await run(options);
}

const entryPath = process.argv[1] ? path.resolve(process.argv[1]) : "";
const scriptPath = fileURLToPath(import.meta.url);

if (entryPath === scriptPath) {
  main().catch((error) => {
    console.error(`Failed: ${error instanceof Error ? error.message : String(error)}`);
    process.exit(1);
  });
}
