#!/usr/bin/env node
/**
 * Copy reference docs from idclawserver-idc into skill/references/ before ClawHub publish.
 *
 * Env:
 *   IDENTYCLAW_REFERENCES — source directory (default: ../idclawserver-idc/references)
 */
import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const skillRoot = join(dirname(fileURLToPath(import.meta.url)), "..");
const repoRoot = join(skillRoot, "..");

const REFERENCE_FILES = [
  "api-reference.md",
  "did-rodit-method.md",
  "finding-agents.md",
  "hola-agent-authentication.md",
  "hola-howto.md",
  "holanonce-api.md",
  "login-authentication.md",
  "token-metadata.md",
  "mcp-auth-tools.md",
  "hola-subagent-authentication.md",
  "inter-agent-communication.md",
  "collaboration-envelope.md",
  "openclaw-integration-guide.md",
  "mcp-discovery-index.md",
  "identyclaw-skill.md",
  "enrollment.md"
];

function resolveReferencesDir() {
  if (process.env.IDENTYCLAW_REFERENCES) {
    return resolve(process.env.IDENTYCLAW_REFERENCES);
  }
  const candidates = [join(repoRoot, "..", "idclawserver-idc", "references")];
  for (const dir of candidates) {
    if (existsSync(dir)) {
      return dir;
    }
  }
  return candidates[0];
}

const referencesDir = resolveReferencesDir();
const outDir = join(skillRoot, "references");

if (!existsSync(referencesDir)) {
  console.error(
    `Missing references source: ${referencesDir}\n` +
      "Clone idclawserver-idc alongside this repo or set IDENTYCLAW_REFERENCES=/path/to/references"
  );
  process.exit(1);
}

mkdirSync(outDir, { recursive: true });

for (const file of REFERENCE_FILES) {
  const src = join(referencesDir, file);
  const dest = join(outDir, file);
  if (!existsSync(src)) {
    console.error(`Missing reference file: ${src}`);
    process.exit(1);
  }
  copyFileSync(src, dest);
  console.log(`synced ${file}`);
}

console.log(`references copied from ${referencesDir} → ${outDir}`);
