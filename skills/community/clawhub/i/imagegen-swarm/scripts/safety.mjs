import { writeFile } from "node:fs/promises";
import path from "node:path";

// Written inside a work directory this run created. Cleanup deletes a matching
// directory only when the marker equals this run's id.
export const RUN_MARKER_FILE = ".imagegen-swarm-run";

export { STDIO_DISCARD as STDIO_QUIET } from "./stdio-modes.mjs";

export const WORK_NAME = /^\.(attempt-|codex-img-|gemini-image-|grok-image-|jimeng-image-|muse-image-|lovart-|api-image-)/;

export async function markRunDir(dir) {
  const id = process.env.IMAGE_GEN_RUN_ID;
  if (!id) return;
  const file = path.join(dir, RUN_MARKER_FILE);
  await writeFile(file, (id) + "\n", { flag: "wx" }).catch((error) => {
    if (error.code !== "EEXIST") throw error;
  });
}

// Files: only paths this run recorded. Directories: only a matching run marker.
export function removableWorkPath({ name, isFile, marker, runId, ownedNames }) {
  if (!WORK_NAME.test(name)) return false;
  if (isFile) return ownedNames.has(name);
  return Boolean(runId) && marker === runId;
}

// A retry may leave workspace-write only when the user set the approval
// variable. --escalate-sandbox alone does not widen the sandbox.
export function sandboxMayWiden({ escalateSandbox, approved, blocked, sandbox }) {
  return Boolean(escalateSandbox && approved && blocked && sandbox !== "danger-full-access");
}

export function userApprovedSandboxWiden(env = process.env) {
  return env.IMAGE_GEN_SANDBOX_ESCALATE === "yes";
}
