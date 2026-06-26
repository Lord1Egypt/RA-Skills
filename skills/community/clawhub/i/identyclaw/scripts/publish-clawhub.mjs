#!/usr/bin/env node
/**
 * Sync references, then publish (or dry-run) the skill to ClawHub.
 * Requires: clawhub login (clawhub whoami), @identyclaw publisher access.
 */
import { readFileSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const skillRoot = join(dirname(fileURLToPath(import.meta.url)), "..");
const repoRoot = join(skillRoot, "..");
const dryRun = process.argv.includes("--dry-run");

function run(command, args) {
  const result = spawnSync(command, args, {
    cwd: skillRoot,
    stdio: "inherit",
    encoding: "utf8"
  });
  if (result.status !== 0) {
    process.exit(result.status ?? 1);
  }
}

function readSkillVersion() {
  const skillMd = readFileSync(join(skillRoot, "SKILL.md"), "utf8");
  const match = skillMd.match(/^version:\s*([^\n]+)/m);
  if (!match) {
    console.error("skill/SKILL.md frontmatter missing version:");
    process.exit(1);
  }
  return match[1].trim();
}

function readChangelogSummary(version) {
  const changelogPath = join(repoRoot, "CHANGELOG.md");
  try {
    const changelog = readFileSync(changelogPath, "utf8");
    const section = changelog.match(
      new RegExp(`## ${version.replace(/\./g, "\\.")}[^\n]*\\n([\\s\\S]*?)(?=\\n## |$)`)
    );
    if (section) {
      const bullets = section[1]
        .split("\n")
        .filter((line) => line.startsWith("- "))
        .map((line) => line.slice(2).trim())
        .join("; ");
      if (bullets) {
        return `v${version}: ${bullets}`;
      }
    }
  } catch {
    // optional
  }
  return `IdentyClaw skill v${version}`;
}

run("node", [join(skillRoot, "scripts/sync-references.mjs")]);

const version = readSkillVersion();
const publishArgs = [
  "skill",
  "publish",
  ".",
  "--owner",
  "identyclaw",
  "--slug",
  "identyclaw",
  "--name",
  "IdentyClaw",
  "--version",
  version,
  "--changelog",
  readChangelogSummary(version)
];

if (dryRun) {
  publishArgs.push("--dry-run");
}

const clawhub = spawnSync("npx", ["--yes", "clawhub", ...publishArgs], {
  cwd: skillRoot,
  stdio: "inherit"
});
process.exit(clawhub.status ?? 1);
