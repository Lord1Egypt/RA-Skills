#!/usr/bin/env node
// Update check for hiapi-video-prompt-generator.
// Mirrors the checkSkillUpdate logic used by the HiAPI API skills:
// below minimumVersion -> exit 1 with the update command; below latestVersion -> stderr notice.

export const SKILL_ID = "hiapi-video-prompt-generator";
export const SKILL_VERSION = "0.1.3";
export const DEFAULT_SKILLS_MANIFEST_URL = "https://raw.githubusercontent.com/HiAPIAI/hiapi-skills/main/skills.json";
const DEFAULT_UPDATE_COMMAND = "npx -y github:HiAPIAI/hiapi-video-prompt-generator-skill -y";

export function compareVersions(left, right) {
  const parse = (value) => String(value || "0.0.0")
    .split(/[+-]/, 1)[0]
    .split(".")
    .map((part) => Number.parseInt(part, 10) || 0);
  const a = parse(left);
  const b = parse(right);
  for (let index = 0; index < Math.max(a.length, b.length, 3); index += 1) {
    const delta = (a[index] || 0) - (b[index] || 0);
    if (delta !== 0) return delta > 0 ? 1 : -1;
  }
  return 0;
}

export async function checkSkillUpdate({
  currentVersion = SKILL_VERSION,
  skillId = SKILL_ID,
  manifestUrl = process.env.HIAPI_SKILLS_MANIFEST_URL || DEFAULT_SKILLS_MANIFEST_URL,
  fetchImpl = fetch,
  timeoutMs = 1200,
  env = process.env,
} = {}) {
  if (env.HIAPI_SKIP_UPDATE_CHECK === "1" || env.HIAPI_SKIP_UPDATE_CHECK === "true") {
    return { status: "skipped" };
  }

  let response;
  const controller = typeof AbortController === "function" ? new AbortController() : null;
  const timer = controller ? setTimeout(() => controller.abort(), timeoutMs) : null;
  try {
    response = await fetchImpl(manifestUrl, {
      headers: { Accept: "application/json" },
      signal: controller?.signal,
    });
  } catch {
    return { status: "skipped" };
  } finally {
    if (timer) clearTimeout(timer);
  }

  if (!response?.ok) return { status: "skipped" };

  let manifest;
  try {
    manifest = await response.json();
  } catch {
    return { status: "skipped" };
  }

  const skill = Array.isArray(manifest.skills)
    ? manifest.skills.find((entry) => entry?.id === skillId)
    : null;
  const policy = skill?.updatePolicy;
  if (!policy) return { status: "current" };

  const minimumVersion = policy.minimumVersion || skill.version || currentVersion;
  const latestVersion = policy.latestVersion || skill.version || minimumVersion;
  const updateCommand = policy.updateCommand || DEFAULT_UPDATE_COMMAND;

  if (compareVersions(currentVersion, minimumVersion) < 0) {
    return {
      status: "required",
      message: [
        policy.requiredNotice || "This HiAPI skill version is outdated and must be updated.",
        `Installed version: ${currentVersion}; required version: ${minimumVersion}.`,
        `Update now: ${updateCommand}`,
      ].join("\n"),
      latestVersion,
      minimumVersion,
      updateCommand,
    };
  }

  if (compareVersions(currentVersion, latestVersion) < 0) {
    return {
      status: "available",
      message: [
        policy.notice || "A newer HiAPI skill is available.",
        `Installed version: ${currentVersion}; latest version: ${latestVersion}.`,
        `Update: ${updateCommand}`,
      ].join("\n"),
      latestVersion,
      minimumVersion,
      updateCommand,
    };
  }

  return { status: "current", latestVersion, minimumVersion, updateCommand };
}

const isMain = process.argv[1] && import.meta.url.endsWith(process.argv[1].split("/").pop());
if (isMain) {
  const result = await checkSkillUpdate();
  if (result.status === "required") {
    console.error(result.message);
    process.exit(1);
  }
  if (result.status === "available" && result.message) {
    console.error(result.message);
  }
  console.log(JSON.stringify({ skill: SKILL_ID, version: SKILL_VERSION, updateStatus: result.status }));
}
