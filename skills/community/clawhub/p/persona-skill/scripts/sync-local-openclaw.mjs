import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const ROOT_DIR = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const SKILL_DIR_NAME = "persona-skill";

function run(cmd, args, options = {}) {
  const result = spawnSync(cmd, args, { stdio: "inherit", ...options });
  if (result.error) throw result.error;
  if (typeof result.status === "number" && result.status !== 0) process.exit(result.status);
}

function hasCmd(cmd) {
  const isWin = process.platform === "win32";
  const result = isWin
    ? spawnSync(`${cmd} --version`, { stdio: "ignore", shell: true })
    : spawnSync(cmd, ["--version"], { stdio: "ignore", shell: false });
  return !result.error && result.status === 0;
}

function ensureSkillRootLooksValid(rootDir) {
  const skillMdPath = path.join(rootDir, "SKILL.md");
  if (!fs.existsSync(skillMdPath)) {
    throw new Error(`Expected SKILL.md at repo root but not found: ${skillMdPath}`);
  }
}

function syncWithRsync(sourceDir, destDir) {
  // Trailing slash copies *contents* into destDir.
  const src = `${sourceDir}${path.sep}`;
  const dst = `${destDir}${path.sep}`;

  run("mkdir", ["-p", destDir]);
  run("rsync", [
    "-av",
    "--delete",
    "--exclude",
    ".git",
    "--exclude",
    "node_modules",
    "--exclude",
    "coverage",
    "--exclude",
    ".clawhub",
    "--exclude",
    ".DS_Store",
    src,
    dst,
  ]);
}

function syncWithNodeCopy(sourceDir, destDir) {
  fs.mkdirSync(destDir, { recursive: true });

  // Node fallback does not do perfect rsync semantics; this is "good enough" for local testing.
  // It aggressively deletes the destination first to avoid stale files.
  fs.rmSync(destDir, { recursive: true, force: true });
  fs.mkdirSync(destDir, { recursive: true });

  fs.cpSync(sourceDir, destDir, {
    recursive: true,
    dereference: true,
    filter(src) {
      const rel = path.relative(sourceDir, src);
      if (!rel) return true;
      const parts = rel.split(path.sep);
      const top = parts[0];
      if (top === ".git" || top === "node_modules" || top === "coverage" || top === ".clawhub") return false;
      if (parts[parts.length - 1] === ".DS_Store") return false;
      return true;
    },
  });
}

function main() {
  ensureSkillRootLooksValid(ROOT_DIR);

  const destRoot = path.join(os.homedir(), ".openclaw", "workspace", "skills");
  const destDir = path.join(destRoot, SKILL_DIR_NAME);

  console.log(`Syncing ${SKILL_DIR_NAME} -> ${destDir}`);
  if (hasCmd("rsync") && hasCmd("mkdir")) {
    syncWithRsync(ROOT_DIR, destDir);
  } else {
    syncWithNodeCopy(ROOT_DIR, destDir);
  }
  console.log("Done. Start a new OpenClaw session to pick up the updated skill.");
}

main();

