import { execSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(__dirname, "..");
const source = path.join(repoRoot, "SKILL.md");

function resolveOpenClawSkillsDir() {
  const fromEnv = process.env.OPENCLAW_SKILLS_DIR?.trim();
  if (fromEnv) return fromEnv;

  try {
    const npmRoot = execSync("npm root -g", { encoding: "utf8" }).trim();
    if (npmRoot) {
      return path.join(npmRoot, "openclaw", "skills");
    }
  } catch {
    // ignore and fallback
  }

  return path.join(os.homedir(), ".openclaw", "skills");
}

const skillsDir = resolveOpenClawSkillsDir();
const targetDir = path.join(skillsDir, "grinders-farm");
const targetFile = path.join(targetDir, "SKILL.md");

fs.mkdirSync(targetDir, { recursive: true });
fs.copyFileSync(source, targetFile);

console.log(`✓ SKILL.md 已同步到: ${targetFile}`);
