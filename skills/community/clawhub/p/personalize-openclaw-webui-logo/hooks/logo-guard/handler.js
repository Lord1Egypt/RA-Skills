// logo-guard handler — gateway:startup hook for personalize-openclaw-webui-logo.
//
// On every gateway start, spawn check-and-restore.sh detached. The checker is
// cheap (one sha256 of favicon-32.png) and only re-applies the logo if the
// dist was overwritten (e.g. by an openclaw upgrade).
//
// We never await the child — gateway startup must not be blocked.
//
// Locating check-and-restore.sh:
//   1. If $LOGO_GUARD_SKILL_DIR is set (install-hook.sh writes it as env file
//      or it can be exported), use it.
//   2. Otherwise read <hookDir>/.skill-dir (written by install-hook.sh).
//   3. Otherwise fall back to walking up from __filename (works only if this
//      file is symlinked back into the skill).
import { spawn } from "node:child_process";
import { existsSync, readFileSync, realpathSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";

const __filename = fileURLToPath(import.meta.url);
const HOOK_DIR = path.dirname(__filename);

function resolveSkillDir() {
  if (process.env.LOGO_GUARD_SKILL_DIR) return process.env.LOGO_GUARD_SKILL_DIR;
  const pointer = path.join(HOOK_DIR, ".skill-dir");
  if (existsSync(pointer)) {
    try {
      const v = readFileSync(pointer, "utf8").trim();
      if (v) return v;
    } catch {}
  }
  // Fallback: maybe this file is a symlink back into the skill
  try {
    const real = realpathSync(__filename);
    return path.resolve(path.dirname(real), "..", "..");
  } catch {
    return path.resolve(HOOK_DIR, "..", "..");
  }
}

const SKILL_DIR = resolveSkillDir();
const CHECKER = path.join(SKILL_DIR, "check-and-restore.sh");

async function handler(event) {
  if (event.type !== "gateway" || event.action !== "startup") return;
  if (!existsSync(CHECKER)) return; // skill not where we expected — stay silent

  try {
    const child = spawn("bash", [CHECKER], {
      detached: true,
      stdio: "ignore",
      cwd: SKILL_DIR,
    });
    child.on("error", () => {}); // swallow — don't crash gateway
    child.unref();
  } catch {
    // best-effort hook; never throw out of startup
  }
}

export default handler;
