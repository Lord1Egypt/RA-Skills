#!/usr/bin/env node

import { existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { getDataDir, loadConfig, configPath } from "./lib/storage.mjs";

const __dirname = dirname(fileURLToPath(import.meta.url));
const SKILL_ROOT = join(__dirname, "..");

const ENV_CANDIDATES = [
  join(process.env.HOME ?? "~", ".openclaw", "workspace", ".env"),
  join(SKILL_ROOT, ".env"),
  join(process.env.HOME ?? "~", ".env"),
];

function checkEnvVar(name, required) {
  const val = (process.env[name] ?? "").trim();
  if (val) return `OK (set, ${val.slice(0, 4)}...)`;
  return required ? "MISSING" : "not set (optional)";
}

console.log("## Environment Check\n");

console.log(`- **TAVILY_API_KEY**: ${checkEnvVar("TAVILY_API_KEY", true)}`);
console.log(`- **XPOZ_API_KEY**: ${checkEnvVar("XPOZ_API_KEY", false)}`);
console.log(`- **NEWS_DIGEST_DATA_DIR**: ${(process.env.NEWS_DIGEST_DATA_DIR ?? "").trim() || "(default)"}`);

console.log();
console.log(`- **Node.js**: ${process.version}`);
console.log(`- **Skill root**: ${SKILL_ROOT}`);
console.log(`- **Data dir**: ${getDataDir()} (${existsSync(getDataDir()) ? "exists" : "will be created on first use"})`);

const envFile = ENV_CANDIDATES.find((p) => existsSync(p));
console.log(`- **.env file**: ${envFile ? `found at ${envFile}` : "not found"}`);

const config = loadConfig();
if (config && config.slots) {
  const slotSummary = config.slots.map((s) => `${s.name} (${s.time})`).join(", ");
  console.log(`- **Config**: ${configPath()} — ${config.slots.length} slot(s): ${slotSummary}`);
} else {
  console.log(`- **Config**: not found — run \`manage-config.mjs init\` or ask the agent to set up`);
}

let issues = 0;
if (!(process.env.TAVILY_API_KEY ?? "").trim()) {
  console.log("\n**Warning**: TAVILY_API_KEY is not set. Tavily search/extract will fail.");
  issues++;
}
if (!(process.env.XPOZ_API_KEY ?? "").trim()) {
  console.log("\n**Note**: XPOZ_API_KEY is not set. Twitter source will be skipped (graceful degradation).");
}
if (!config) {
  console.log("\n**Warning**: No schedule config found. The agent needs to set up push schedule with the user.");
  issues++;
}

if (issues === 0) {
  console.log("\nAll checks passed.");
} else {
  console.log(`\n${issues} issue(s) found. See above.`);
}
