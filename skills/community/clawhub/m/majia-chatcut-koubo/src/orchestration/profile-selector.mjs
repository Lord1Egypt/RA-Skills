import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

import {contentHash} from "../planning/preview-approval.mjs";

const MODULE_DIRECTORY = path.dirname(fileURLToPath(import.meta.url));
const DEFAULT_PROFILE_DIRECTORY = path.resolve(MODULE_DIRECTORY, "../../profiles");
const PROFILE_FILES = Object.freeze([
  "balanced-stable.json",
  "tight-short.json",
  "trust-longform.json",
  "screen-demo.json",
]);

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8"));
}

export function loadOrchestrationProfiles(directory = DEFAULT_PROFILE_DIRECTORY) {
  return PROFILE_FILES.map((name) => readJson(path.join(directory, name)));
}

export function selectProfile({
  mode = "stable",
  goal = "daily-publish",
  durationSec = null,
  hasScreenCapture = false,
} = {}, profiles = loadOrchestrationProfiles()) {
  if (!["stable", "fast", "pro"].includes(mode)) throw new Error("PROFILE_MODE_INVALID");
  if (durationSec !== null && (!Number.isFinite(durationSec) || durationSec <= 0)) {
    throw new Error("PROFILE_DURATION_INVALID");
  }
  const screenRequired = hasScreenCapture || goal === "screen-demo";
  const candidates = profiles.filter((candidate) => {
    if (!candidate.supportedModes.includes(mode)) return false;
    if (screenRequired && candidate.selection.requiresScreenCapture !== true) return false;
    if (!screenRequired && candidate.selection.requiresScreenCapture === true) return false;
    if (durationSec !== null && candidate.selection.minimumDurationSec !== null && durationSec < candidate.selection.minimumDurationSec) return false;
    if (durationSec !== null && candidate.selection.maximumDurationSec !== null && durationSec > candidate.selection.maximumDurationSec) return false;
    return true;
  });
  if (candidates.length === 0) throw new Error("PROFILE_COMBINATION_UNSUPPORTED");
  const scored = candidates.map((candidate) => ({
    candidate,
    score: candidate.selection.priority
      + (candidate.selection.goals.includes(goal) ? 1000 : 0)
      + (durationSec !== null && candidate.selection.minimumDurationSec !== null ? 1500 : 0)
      + (durationSec !== null && candidate.selection.maximumDurationSec !== null ? 100 : 0)
      - (durationSec === null && (candidate.selection.minimumDurationSec !== null || candidate.selection.maximumDurationSec !== null) ? 500 : 0),
  }));
  scored.sort((left, right) => right.score - left.score || left.candidate.id.localeCompare(right.candidate.id));
  return structuredClone(scored[0].candidate);
}

export function profileFingerprint(profile) {
  return contentHash(profile);
}

export function createProjectBrief({
  route,
  profile,
  goal = "daily-publish",
  platform = "unspecified",
  targetDurationSec = null,
  createdAt = new Date().toISOString(),
  missingFields = [],
} = {}) {
  if (!route || !profile) throw new Error("PROJECT_BRIEF_INPUT_REQUIRED");
  if (typeof platform !== "string" || platform.length < 1 || platform.length > 64) throw new Error("PROJECT_BRIEF_PLATFORM_INVALID");
  if (!/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$/u.test(createdAt) || !Number.isFinite(Date.parse(createdAt))) {
    throw new Error("PROJECT_BRIEF_DATE_INVALID");
  }
  const normalizedMissingFields = [...new Set(missingFields)].slice(0, 5);
  const treatments = structuredClone(profile.defaults.treatments);
  for (const [name, enabled] of Object.entries(route.requestedTreatments ?? {})) {
    if (name in treatments) treatments[name] = Boolean(enabled);
  }
  if (route.textEdit && route.textEdit.target !== "speech-cut") {
    treatments.arollCleanup = false;
    treatments.smoothAudio = false;
    if (route.textEdit.target !== "caption-display") treatments.captions = false;
  }
  return {
    $schema: "https://github.com/maojiebc/majia-chatcut-koubo/schemas/runtime/project-brief.schema.json",
    schemaVersion: "majia.koubo.brief.v1",
    mode: route.mode,
    goal,
    platform,
    targetDurationSec,
    pacing: profile.defaults.pacing,
    automationLevel: route.automationLevel,
    treatments,
    ...(route.textEdit ? {textEdit: route.textEdit} : {}),
    contentProtections: [...profile.contentProtections],
    intake: {
      asked: normalizedMissingFields.length >= 2,
      missingFields: normalizedMissingFields,
    },
    createdAt,
  };
}

export const DEFAULT_ORCHESTRATION_PROFILE_DIRECTORY = DEFAULT_PROFILE_DIRECTORY;
