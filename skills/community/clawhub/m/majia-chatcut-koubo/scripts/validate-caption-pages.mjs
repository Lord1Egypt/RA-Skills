#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { createHash } from "node:crypto";
import { fileURLToPath } from "node:url";
import Ajv2020 from "ajv/dist/2020.js";
import addFormats from "ajv-formats";
import {
  getProfileDiagnostics,
  loadProfile,
} from "../src/config/index.mjs";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const args = process.argv.slice(2);

function printUsage() {
  console.error("Usage: node scripts/validate-caption-pages.mjs --profile <profile.json> --input <captions.json|read_captions.txt> [--root <profile-root>] [--terms <terminology.json>] [--strict]");
  console.error("  --root explicitly authorizes profile inheritance and profile-owned paths within one local root");
  console.error("  --terms overrides the profile's terminologyFile (e.g. your personal terminology in ~/.config/majia-chatcut-koubo/)");
  console.error("  --strict treats every warning as a blocking validation failure");
}

function failArguments(message) {
  console.error(`FAIL invalid arguments: ${message}`);
  printUsage();
  process.exit(2);
}

function parseArguments(argv) {
  const valueOptions = new Map([
    ["--profile", "profilePath"],
    ["--input", "inputPath"],
    ["--root", "profileRoot"],
    ["--terms", "termsPath"],
  ]);
  const parsed = {strictWarnings: false};
  const seen = new Set();

  for (let index = 0; index < argv.length; index += 1) {
    const option = argv[index];
    if (option === "--strict" || option === "--strict-warnings") {
      if (seen.has("strictWarnings")) failArguments("strict warning option was provided more than once");
      seen.add("strictWarnings");
      parsed.strictWarnings = true;
      continue;
    }
    const destination = valueOptions.get(option);
    if (!destination) failArguments("unknown or unsupported option");
    if (seen.has(destination)) failArguments(`${option} was provided more than once`);
    const value = argv[index + 1];
    if (typeof value !== "string" || value.length === 0 || value.startsWith("--")) {
      failArguments(`${option} requires a value`);
    }
    seen.add(destination);
    parsed[destination] = value;
    index += 1;
  }
  return parsed;
}

const {
  profilePath,
  inputPath,
  profileRoot,
  termsPath,
  strictWarnings,
} = parseArguments(args);
if (!profilePath || !inputPath) {
  failArguments("--profile and --input are required");
}

const readJson = (file) => JSON.parse(fs.readFileSync(file, "utf8"));
const profileAbsolute = path.resolve(profilePath);

let profile;
let profileDiagnostics;
try {
  profile = loadProfile(profileAbsolute, {
    ...(profileRoot ? {allowedRoot: path.resolve(profileRoot)} : {}),
  });
  profileDiagnostics = getProfileDiagnostics(profile);
} catch (error) {
  const code = typeof error?.code === "string" ? error.code : "PROFILE_LOAD_FAILED";
  console.error(`FAIL invalid profile: ${code}`);
  process.exit(code === "PROFILE_READ_ERROR" || code === "PROFILE_LOAD_FAILED" ? 2 : 1);
}
let policy;
try {
  policy = readJson(path.join(root, "rules/policy.json"));
} catch {
  console.error("FAIL hard policy is unavailable: POLICY_READ_FAILED");
  process.exit(2);
}
let validateStructuredCaptions;
let validateTerminologyContract;
try {
  const ajv = new Ajv2020({
    allErrors: true,
    allowUnionTypes: true,
    logger: false,
    strict: true,
    strictRequired: false,
    validateFormats: true,
  });
  addFormats(ajv);
  validateStructuredCaptions = ajv.compile(readJson(path.join(root, "schemas/captions.schema.json")));
  validateTerminologyContract = ajv.compile(readJson(path.join(root, "schemas/terminology.schema.json")));
} catch {
  console.error("FAIL caption schema is unavailable: SCHEMA_COMPILE_FAILED");
  process.exit(2);
}
let input;
try {
  input = fs.readFileSync(path.resolve(inputPath), "utf8");
} catch {
  console.error("FAIL caption input is unavailable: INPUT_READ_FAILED");
  process.exit(2);
}
const errors = [];
const warnings = (profileDiagnostics?.warnings ?? []).map(
  (warning) => `${warning.code} ${warning.message}`,
);

function decodeQuoted(value) {
  try {
    return JSON.parse(`"${value}"`);
  } catch {
    return value;
  }
}

function parseLegacy(text) {
  const pagination = text.match(/pagination density:\s*maxLines=(\d+)\s+maxCharactersPerLine=(\d+)/i);
  const sourceVariant = text.match(/source variant:\s*([^\s]+)/i);
  const timelineFps = text.match(/timeline fps:\s*([\d.]+)/i);
  const automaticWrap = text.match(/automatic wrap allowed:\s*(true|false)/i);
  const pages = [];
  const pageRe = /^\[P(\d+)\].*?frame=(\d+)-(\d+)\s+text="((?:\\.|[^"\\])*)"\s+lines=(\d+)\s+words=(\d+)/gm;
  let match;
  while ((match = pageRe.exec(text))) {
    pages.push({
      index: Number(match[1]),
      startFrame: Number(match[2]),
      endFrame: Number(match[3]),
      text: decodeQuoted(match[4]),
      lines: Number(match[5]),
      declaredWordCount: Number(match[6]),
      words: [],
    });
  }

  const wordRe = /^\s+-\s+key=(\S+)\s+text="((?:\\.|[^"\\])*)"\s+frame=(\d+)-(\d+)(.*)$/gm;
  while ((match = wordRe.exec(text))) {
    const startFrame = Number(match[3]);
    const page = pages.find((candidate) => startFrame >= candidate.startFrame && startFrame < candidate.endFrame);
    if (!page) continue;
    page.words.push({
      key: match[1],
      text: decodeQuoted(match[2]),
      startFrame,
      endFrame: Number(match[4]),
      edited: /\bedited\b/.test(match[5]),
    });
  }

  return {
    schemaVersion: "legacy-read-captions",
    metadata: {
      sourceVariant: sourceVariant?.[1],
      timelineFps: timelineFps ? Number(timelineFps[1]) : undefined,
      automaticWrapAllowed: automaticWrap ? automaticWrap[1].toLowerCase() === "true" : undefined,
      pagination: pagination ? {
        maxLines: Number(pagination[1]),
        maxCharactersPerLine: Number(pagination[2]),
      } : undefined,
    },
    pages,
  };
}

let usedLegacyParser = false;
function parseInput(text) {
  try {
    const value = JSON.parse(text);
    if (!value || typeof value !== "object" || !Array.isArray(value.pages)) {
      throw new Error("captions JSON must contain a pages array");
    }
    return value;
  } catch (error) {
    if (/^\s*[\[{]/.test(text)) throw error;
    usedLegacyParser = true;
    warnings.push("legacy text input is deprecated; prefer structured captions JSON");
    return parseLegacy(text);
  }
}

let document;
try {
  document = parseInput(input);
} catch (error) {
  const code = error instanceof SyntaxError ? "INVALID_JSON" : "INVALID_STRUCTURE";
  console.error(`FAIL invalid caption input: ${code}`);
  process.exit(1);
}

if (!usedLegacyParser && !validateStructuredCaptions(document)) {
  for (const error of validateStructuredCaptions.errors || []) {
    errors.push(`caption schema ${error.keyword}@${error.instancePath || "/"}`);
  }
  for (const line of [...new Set(errors)]) console.error(`FAIL ${line}`);
  console.error(`caption schema audit failed: ${new Set(errors).size} error(s)`);
  process.exit(1);
}

const captionPolicy = policy.caption;
const captions = profile.captions || {};
const metadata = document.metadata || {};
const pagination = metadata.pagination || {};
const timelineFps = Number(metadata.timelineFps ?? profile.timeline?.fps);
const captionProvenanceFields = ["projectId", "timelineId", "timelineRevision", "sourceAssetId", "sourceRevision"];
const isLegacyCaptionInput = usedLegacyParser;
const hasOwn = (value, key) => Object.prototype.hasOwnProperty.call(value, key);
const profileHasMigrationTrustGap = (
  profileDiagnostics?.contractStatus === "migration-incomplete"
);

if (profile.policyVersion !== policy.version) {
  warnings.push(`profile policyVersion=${profile.policyVersion ?? "missing"}; expected ${policy.version}; migrate the leaf profile before strict release`);
}
if (profile.status !== "validated" && !profileHasMigrationTrustGap) {
  errors.push(`profile status=${profile.status ?? "missing"}; release requires validated`);
}
if (!Array.isArray(profile.provenance?.validatedTimelineIds) || profile.provenance.validatedTimelineIds.length === 0) {
  if (!profileHasMigrationTrustGap) {
    errors.push("profile has no validatedTimelineIds");
  }
}
if (
  (!profile.provenance?.projectId || /REPLACE|your-/i.test(profile.provenance.projectId))
  && !profileHasMigrationTrustGap
) {
  errors.push("profile projectId is missing or still a placeholder");
}
if (!isLegacyCaptionInput) {
  const providedCaptionProvenance = captionProvenanceFields.filter((field) => metadata[field] !== undefined);
  if (providedCaptionProvenance.length === 0) {
    warnings.push(`caption provenance metadata is missing; provide ${captionProvenanceFields.join(", ")}`);
  } else {
    if (providedCaptionProvenance.length !== captionProvenanceFields.length) {
      errors.push(`caption provenance metadata must provide all of: ${captionProvenanceFields.join(", ")}`);
    }
    let validCaptionProvenance = true;
    for (const field of captionProvenanceFields) {
      if (metadata[field] === undefined) {
        validCaptionProvenance = false;
      } else if (typeof metadata[field] !== "string" || metadata[field].trim().length === 0) {
        errors.push(`caption ${field} must be a non-empty string`);
        validCaptionProvenance = false;
      }
    }
    if (validCaptionProvenance) {
      if (metadata.projectId !== profile.provenance?.projectId) {
        errors.push("PROVENANCE_PROJECT_MISMATCH caption projectId does not match the resolved profile");
      }
      const timelineIsValidated = profile.provenance?.validatedTimelineIds?.includes(metadata.timelineId);
      if (!timelineIsValidated) {
        errors.push("PROVENANCE_TIMELINE_UNVALIDATED caption timelineId is not validated by the resolved profile");
      }
      const timelineRevisions = profile.provenance?.validatedTimelineRevisions;
      if (timelineRevisions === undefined) {
        warnings.push("PROVENANCE_TIMELINE_REVISION_MISSING add provenance.validatedTimelineRevisions before strict release");
      } else if (
        timelineRevisions === null
        || typeof timelineRevisions !== "object"
        || Array.isArray(timelineRevisions)
      ) {
        errors.push("profile provenance.validatedTimelineRevisions must be an object");
      } else if (!hasOwn(timelineRevisions, metadata.timelineId)) {
        errors.push("PROVENANCE_TIMELINE_REVISION_UNVALIDATED selected timeline has no validated revision evidence");
      } else if (
        typeof timelineRevisions[metadata.timelineId] !== "string"
        || timelineRevisions[metadata.timelineId].trim().length === 0
      ) {
        errors.push("PROVENANCE_TIMELINE_REVISION_INVALID profile timeline revision evidence must be a non-empty string");
      } else if (metadata.timelineRevision !== timelineRevisions[metadata.timelineId]) {
        errors.push("PROVENANCE_TIMELINE_REVISION_MISMATCH caption timelineRevision does not match profile evidence");
      }
      const sourceRevisions = profile.provenance?.validatedSourceRevisions;
      if (sourceRevisions === undefined) {
        warnings.push("PROVENANCE_SOURCE_REVISION_MISSING add provenance.validatedSourceRevisions before strict release");
      } else if (
        sourceRevisions === null
        || typeof sourceRevisions !== "object"
        || Array.isArray(sourceRevisions)
      ) {
        errors.push("profile provenance.validatedSourceRevisions must be an object");
      } else if (!hasOwn(sourceRevisions, metadata.sourceAssetId)) {
        errors.push("PROVENANCE_SOURCE_UNVALIDATED caption sourceAssetId is not validated by the resolved profile");
      } else if (
        typeof sourceRevisions[metadata.sourceAssetId] !== "string"
        || sourceRevisions[metadata.sourceAssetId].trim().length === 0
      ) {
        errors.push("PROVENANCE_SOURCE_REVISION_INVALID profile source revision evidence must be a non-empty string");
      } else if (metadata.sourceRevision !== sourceRevisions[metadata.sourceAssetId]) {
        errors.push("PROVENANCE_SOURCE_REVISION_MISMATCH caption sourceRevision does not match profile evidence");
      }
    }
  }
}
if (!Number.isFinite(timelineFps) || timelineFps <= 0) errors.push("timeline fps is missing or invalid");
if (Number.isFinite(Number(metadata.timelineFps)) && Number.isFinite(Number(profile.timeline?.fps)) && Number(metadata.timelineFps) !== Number(profile.timeline.fps)) {
  errors.push(`caption timelineFps=${metadata.timelineFps}; profile timeline fps=${profile.timeline.fps}`);
}
if (metadata.sourceVariant !== captions.sourceVariant || !captionPolicy.allowedSourceVariants.includes(metadata.sourceVariant)) {
  errors.push(`source variant=${metadata.sourceVariant ?? "missing"}; expected ${captions.sourceVariant ?? captionPolicy.allowedSourceVariants[0]}`);
}
if (metadata.automaticWrapAllowed !== captionPolicy.automaticWrapAllowed) {
  errors.push(`automaticWrapAllowed=${metadata.automaticWrapAllowed ?? "missing"}; policy requires ${captionPolicy.automaticWrapAllowed}`);
}
if (pagination.maxLines !== captionPolicy.maxLines) errors.push(`config maxLines=${pagination.maxLines ?? "missing"}; policy requires ${captionPolicy.maxLines}`);
if (pagination.maxCharactersPerLine !== captions.maxCharactersPerLine) {
  errors.push(`config maxCharactersPerLine=${pagination.maxCharactersPerLine ?? "missing"}; profile requires ${captions.maxCharactersPerLine ?? "missing"}`);
}

function loadTerminology() {
  if (termsPath) {
    const file = path.resolve(termsPath);
    try {
      return readJson(file);
    } catch (error) {
      if (error instanceof SyntaxError) {
        errors.push("terminology JSON is invalid: TERMINOLOGY_INVALID_JSON");
        return {};
      }
      console.error("FAIL terminology is unavailable: TERMINOLOGY_READ_FAILED");
      process.exit(2);
      return {};
    }
  }
  if (profile.terminology && typeof profile.terminology === "object") return { terminology: profile.terminology };
  if (!profile.terminologyFile) {
    errors.push("terminologyFile is required");
    return {};
  }
  const file = path.resolve(path.dirname(profileAbsolute), profile.terminologyFile);
  try {
    return readJson(file);
  } catch (error) {
    if (error instanceof SyntaxError) {
      errors.push("terminology JSON is invalid: TERMINOLOGY_INVALID_JSON");
      return {};
    }
    console.error("FAIL terminology is unavailable: TERMINOLOGY_READ_FAILED");
    process.exit(2);
    return {};
  }
}

const normalize = (value) => String(value ?? "").normalize("NFKC").trim();
const charCount = (value) => Array.from(normalize(value).replace(/\s+/g, "")).length;
const lexicalText = (value) => normalize(value).replace(/[^\p{L}\p{N}]/gu, "").toLocaleLowerCase("zh-CN");
const isSafeFrame = (value) => typeof value === "number" && Number.isSafeInteger(value) && value >= 0;
const hasLineBreak = (value) => typeof value === "string" && /[\r\n]/u.test(value);
const termIdPattern = /^[A-Za-z0-9][A-Za-z0-9._-]*$/u;
const opaqueRef = (kind, value) => {
  const digest = createHash("sha256").update(String(value ?? "")).digest("hex").slice(0, 10);
  return `${kind}#${digest}`;
};

const loadedTerminologyData = loadTerminology();
const terminologyData = loadedTerminologyData !== null
  && typeof loadedTerminologyData === "object"
  && !Array.isArray(loadedTerminologyData)
  ? loadedTerminologyData
  : {};
if (terminologyData !== loadedTerminologyData) {
  errors.push("terminology root must be an object");
}

if (hasOwn(terminologyData, "terminology") && !hasOwn(terminologyData, "entries")) {
  warnings.push("legacy terminology map is migration-only; use the terminology schema before strict release");
} else {
  const terminologyForSchema = JSON.parse(JSON.stringify(terminologyData));
  if (!hasOwn(terminologyForSchema, "maintainer")) {
    terminologyForSchema.maintainer = "legacy-migration";
    warnings.push("terminology maintainer is missing; migrate the terminology file before strict release");
  }
  if (Array.isArray(terminologyForSchema.entries)) {
    terminologyForSchema.entries = terminologyForSchema.entries.map((entry, index) => (
      entry !== null
      && typeof entry === "object"
      && !Array.isArray(entry)
      && !hasOwn(entry, "termId")
        ? {...entry, termId: `legacy-term-${index + 1}`}
        : entry
    ));
  }
  if (!validateTerminologyContract(terminologyForSchema)) {
    for (const error of validateTerminologyContract.errors || []) {
      errors.push(`terminology schema ${error.keyword}@${error.instancePath || "/"}`);
    }
    for (const line of [...new Set(errors)]) console.error(`FAIL ${line}`);
    console.error(`terminology schema audit failed: ${new Set(errors).size} error(s)`);
    process.exit(1);
  }
}

function rawTerminologyEntries(data) {
  if (hasOwn(data, "entries")) {
    if (!Array.isArray(data.entries)) {
      errors.push("terminology entries must be an array");
      return [];
    }
    return data.entries;
  }
  if (!hasOwn(data, "terminology")) return [];
  if (
    data.terminology === null
    || typeof data.terminology !== "object"
    || Array.isArray(data.terminology)
  ) {
    errors.push("legacy terminology map must be an object");
    return [];
  }
  return Object.entries(data.terminology).map(([correct, wrong]) => ({
    correct,
    wrong,
    matchMode: "substring",
  }));
}

function prepareTerminologyEntries(data) {
  const prepared = [];
  const termIds = new Set();
  let missingTermIdCount = 0;

  for (const [entryIndex, entry] of rawTerminologyEntries(data).entries()) {
    if (entry === null || typeof entry !== "object" || Array.isArray(entry)) {
      errors.push(`terminology entry ${entryIndex} must be an object`);
      continue;
    }
    if (typeof entry.correct !== "string" || normalize(entry.correct).length === 0) {
      errors.push(`terminology entry ${entryIndex} correct must be a non-empty string`);
      continue;
    }
    const wrongs = hasOwn(entry, "wrong") ? entry.wrong : entry.wrongs;
    if (!Array.isArray(wrongs) || wrongs.length === 0) {
      errors.push(`terminology entry ${entryIndex} wrong must be a non-empty array`);
      continue;
    }
    if (wrongs.some((wrong) => typeof wrong !== "string" || normalize(wrong).length === 0)) {
      errors.push(`terminology entry ${entryIndex} wrong must contain only non-empty strings`);
      continue;
    }
    if (entry.matchMode !== "substring" && entry.matchMode !== "exact") {
      errors.push(`terminology entry ${entryIndex} matchMode must be substring or exact`);
      continue;
    }
    if (hasOwn(entry, "caseSensitive") && typeof entry.caseSensitive !== "boolean") {
      errors.push(`terminology entry ${entryIndex} caseSensitive must be a boolean`);
      continue;
    }
    if (hasOwn(entry, "requiresAudioEvidence") && typeof entry.requiresAudioEvidence !== "boolean") {
      errors.push(`terminology entry ${entryIndex} requiresAudioEvidence must be a boolean`);
      continue;
    }

    let termId;
    if (!hasOwn(entry, "termId")) {
      missingTermIdCount += 1;
    } else if (typeof entry.termId !== "string" || !termIdPattern.test(entry.termId)) {
      errors.push(`terminology entry ${entryIndex} termId is invalid`);
    } else if (termIds.has(entry.termId)) {
      errors.push(`terminology ${opaqueRef("termId", entry.termId)} is duplicated`);
    } else {
      termId = entry.termId;
      termIds.add(termId);
    }

    prepared.push({
      entryIndex,
      termId,
      correct: normalize(entry.correct),
      wrongs: wrongs.map((wrong) => normalize(wrong)),
      matchMode: entry.matchMode,
      caseSensitive: entry.caseSensitive === true,
      requiresAudioEvidence: entry.requiresAudioEvidence === true,
      risk: entry.risk,
    });
  }

  if (missingTermIdCount > 0) {
    warnings.push(`terminology is missing stable termId on ${missingTermIdCount} entry(s); migrate the terminology file before strict release`);
  }
  return prepared;
}

function optionalStringArray(value, label) {
  if (value === undefined) return [];
  if (
    !Array.isArray(value)
    || value.some((item) => typeof item !== "string" || normalize(item).length === 0)
  ) {
    errors.push(`${label} must be an array of non-empty strings`);
    return [];
  }
  return value;
}

const preparedTerminologyEntries = prepareTerminologyEntries(terminologyData);

function semanticText(value) {
  const compact = normalize(value)
    .replace(/\s+/gu, "")
    .replace(/[−﹣–—]/gu, "-")
    .replace(/／/gu, "/")
    .replace(/：/gu, ":")
    .replace(/％/gu, "%")
    .replace(/＋/gu, "+")
    .replace(/￥/gu, "¥");
  const characters = Array.from(compact);
  const isLetterOrNumber = (character) => character !== undefined && /[\p{L}\p{N}]/u.test(character);
  const isNumber = (character) => character !== undefined && /\p{N}/u.test(character);

  return characters.filter((character, index) => {
    if (isLetterOrNumber(character)) return true;
    const previous = characters[index - 1];
    const next = characters[index + 1];
    if ("$¥€£%‰°℃℉".includes(character)) return isLetterOrNumber(previous) || isLetterOrNumber(next);
    if (character === "." || character === "," || character === ":") return isNumber(previous) && isNumber(next);
    if (character === "+" || character === "-") return isNumber(previous) || isNumber(next);
    if (character === "/" || character === "×") return isLetterOrNumber(previous) && isLetterOrNumber(next);
    return false;
  }).join("");
}

function viewerTextMatchesEvidence(viewer, evidence) {
  return semanticText(viewer) === semanticText(evidence);
}

function configuredTermMatch(value, target, matchMode, caseSensitive) {
  let candidate = normalize(value);
  let expected = normalize(target);
  if (!caseSensitive) {
    candidate = candidate.toLocaleLowerCase("zh-CN");
    expected = expected.toLocaleLowerCase("zh-CN");
  }
  return matchMode === "exact"
    ? candidate === expected
    : candidate.includes(expected);
}

function matchingCorrectionTerms(sourceText, displayText) {
  return preparedTerminologyEntries.filter((entry) => (
    configuredTermMatch(
      displayText,
      entry.correct,
      entry.matchMode,
      entry.caseSensitive,
    )
    && entry.wrongs.some((wrong) => configuredTermMatch(
      sourceText,
      wrong,
      entry.matchMode,
      entry.caseSensitive,
    ))
  ));
}

function hasAudioEvidence(evidenceRefs) {
  return Array.isArray(evidenceRefs)
    && evidenceRefs.some((reference) => (
      typeof reference === "string"
      && /^audio:\S+/iu.test(reference)
    ));
}

function hasPixelEvidence(evidenceRefs) {
  return Array.isArray(evidenceRefs)
    && evidenceRefs.some((reference) => (
      typeof reference === "string"
      && /^(?:frame|pixel|image):\S+/iu.test(reference)
    ));
}

function negationFingerprint(value) {
  const normalized = normalize(value).toLocaleLowerCase("zh-CN");
  const matches = normalized.match(/没有|不能|不会|不是|并非|未曾|不|没|无|非|未|否|never|without|cannot|can't|not|no/gu);
  return (matches || []).join("|");
}

function isHighRiskSemanticChange(sourceText, displayText) {
  if (semanticText(sourceText) === semanticText(displayText)) return false;
  const combined = `${normalize(sourceText)} ${normalize(displayText)}`;
  if (/[\p{N}$¥€£%‰]/u.test(combined)) return true;
  if (/[零〇一二两三四五六七八九十百千万亿兆]/u.test(combined)) return true;
  if (/(?:人民币|美元|欧元|日元|港元|元|块钱)/u.test(combined)) return true;
  const unitToken = /^(?:[kmgt]?b|[kmgt]?bps|[kmg]?hz|ms|s|min|h|kg|g|mg|km|m|cm|mm|l|ml|°c|℃|°f|℉)$/iu;
  if (
    unitToken.test(normalize(sourceText).replace(/\s+/gu, ""))
    || unitToken.test(normalize(displayText).replace(/\s+/gu, ""))
  ) {
    return true;
  }
  const directionalFingerprint = (value) => (
    normalize(value)
      .match(/上升|下降|增加|减少|盈利|亏损|负|正|增|减|涨|跌/gu)
      ?.join("|") ?? ""
  );
  if (directionalFingerprint(sourceText) !== directionalFingerprint(displayText)) {
    return true;
  }
  return negationFingerprint(sourceText) !== negationFingerprint(displayText);
}

const approvedTerms = new Set([
  ...optionalStringArray(
    captions.shortCardPolicy?.approvedTerms,
    "profile shortCardPolicy.approvedTerms",
  ),
  ...optionalStringArray(
    terminologyData.shortCardWhitelist?.approved,
    "terminology shortCardWhitelist.approved",
  ),
].map((value) => normalize(value).toLocaleLowerCase("zh-CN")));
const shortCardPattern = new RegExp(captionPolicy.shortCardAllowedPattern, "u");
const hardReplacementLimit = captionPolicy.maxReplacementCharacters;
const profileReplacementLimit = captions.displayOverridePolicy?.maxReplacementCharacters;
const replacementLimit = Number.isSafeInteger(profileReplacementLimit) && profileReplacementLimit >= 0
  ? Math.min(hardReplacementLimit, profileReplacementLimit)
  : hardReplacementLimit;

const pages = document.pages || [];
if (pages.length === 0) errors.push("no viewer-facing pages parsed");
const indexes = new Set();
const wordKeys = new Set();
const sourceWordKeys = new Set();
let previous;
let wordCount = 0;
let missingSourceTextCount = 0;
let missingWordSourceBindingCount = 0;

for (const page of pages) {
  const index = page.index;
  const start = Number(page.startFrame);
  const end = Number(page.endFrame);
  const pageTextIsString = typeof page.text === "string";
  const text = pageTextIsString ? normalize(page.text) : "";
  const lines = page.lines;
  const words = Array.isArray(page.words) ? page.words : [];
  const label = `P${String(index)} frames=${start}-${end}`;

  if (!Number.isSafeInteger(index) || index < 1) errors.push(`${label}: page index must be a positive safe integer`);
  if (indexes.has(index)) errors.push(`${label}: duplicate page index`);
  indexes.add(index);
  if (!isSafeFrame(page.startFrame) || !isSafeFrame(page.endFrame)) {
    errors.push(`${label}: page frame interval must use non-negative safe integers`);
  }
  if (!Number.isFinite(start) || !Number.isFinite(end) || end <= start) errors.push(`${label}: invalid frame interval`);
  if (previous && start < previous.startFrame) errors.push(`${label}: pages are not sorted by start frame`);
  if (previous && start < previous.endFrame) errors.push(`${label}: overlaps P${previous.index}`);
  previous = page;
  if (!pageTextIsString) {
    errors.push(`${label}: page text must be a string`);
  } else {
    if (!text) errors.push(`${label}: empty page`);
    if (hasLineBreak(page.text)) errors.push(`${label}: page text contains a CR or LF line break`);
  }
  if (!Number.isSafeInteger(lines)) {
    errors.push(`${label}: lines must be an integer`);
  } else if (lines < 1 || lines > captionPolicy.maxLines) {
    errors.push(`${label}: ${lines} lines exceeds policy range 1-${captionPolicy.maxLines}`);
  }
  const chars = charCount(text);
  const effectiveLines = Number.isSafeInteger(lines) && lines > 0 ? lines : 1;
  const characterBudget = captions.maxCharactersPerLine * Math.min(effectiveLines, captionPolicy.maxLines);
  if (chars > characterBudget) {
    errors.push(`${label}: ${chars} chars > ${characterBudget} (${effectiveLines} line(s) × ${captions.maxCharactersPerLine})`);
  }
  if (chars === 1) errors.push(`${label}: single-character page`);

  if (Number.isFinite(timelineFps) && end > start) {
    const durationMs = ((end - start) / timelineFps) * 1000;
    if (durationMs < captionPolicy.hardMinDurationMs) {
      errors.push(`${label}: ${durationMs.toFixed(1)}ms < hard minimum ${captionPolicy.hardMinDurationMs}ms`);
    } else if (durationMs < captionPolicy.normalMinDurationMs) {
      const approved = approvedTerms.has(text.toLocaleLowerCase("zh-CN"));
      const policyEligible = chars >= captionPolicy.shortCardMinCharacters
        && chars <= captionPolicy.shortCardMaxCharacters
        && shortCardPattern.test(text);
      if (approved && !policyEligible) {
        errors.push(`${label}: ${durationMs.toFixed(1)}ms short page is not policy-eligible; only approved English/numeric brand abbreviations are allowed`);
      } else if (!approved) {
        errors.push(`${label}: ${durationMs.toFixed(1)}ms short page is not terminology-approved`);
      } else {
        const evidence = page.shortCardEvidence;
        const hasReviewerEvidence = evidence
          && typeof evidence.reviewedBy === "string"
          && evidence.reviewedBy.trim().length > 0
          && Array.isArray(evidence.evidenceRefs)
          && hasPixelEvidence(evidence.evidenceRefs);
        if (!hasReviewerEvidence) {
          warnings.push(`${label}: approved short terminology card is missing reviewer/pixel evidence`);
        }
      }
    }
  }

  if (page.declaredWordCount !== undefined && Number(page.declaredWordCount) !== words.length) {
    errors.push(`${label}: declares ${page.declaredWordCount} words but parsed ${words.length}`);
  }
  if (captionPolicy.requireWordLevelAudit && words.length === 0) errors.push(`${label}: word-level audit missing`);
  if (words.length > 0) {
    const evidenceText = words.map((word) => typeof word.text === "string" ? word.text : "").join("");
    if (!viewerTextMatchesEvidence(text, evidenceText)) {
      if (lexicalText(evidenceText) === lexicalText(text) && /\p{N}/u.test(`${text}${evidenceText}`)) {
        errors.push(`${label}: viewer text numeric semantics differ from its word evidence`);
      } else {
        errors.push(`${label}: viewer text does not match its word evidence`);
      }
    }
  }
  wordCount += words.length;

  let previousWord;
  for (const [wordIndex, word] of words.entries()) {
    const wordLabel = `W${wordIndex + 1}`;
    const wordKey = typeof word.key === "string" ? word.key.trim() : "";
    const wordTextIsString = typeof word.text === "string";
    const wordText = wordTextIsString ? normalize(word.text) : "";
    const sourceTextProvided = hasOwn(word, "sourceText");
    const sourceTextIsString = sourceTextProvided && typeof word.sourceText === "string";
    const sourceText = sourceTextIsString ? normalize(word.sourceText) : "";
    const editedProvided = hasOwn(word, "edited");
    const editedIsBoolean = editedProvided && typeof word.edited === "boolean";
    const wordStart = Number(word.startFrame);
    const wordEnd = Number(word.endFrame);
    if (!isLegacyCaptionInput) {
      const wordSourceBindingFields = ["sourceAssetId", "sourceRevision", "sourceWordKey"];
      const providedWordSourceBinding = wordSourceBindingFields.filter((field) => word[field] !== undefined);
      if (providedWordSourceBinding.length === 0) {
        missingWordSourceBindingCount += 1;
      } else if (providedWordSourceBinding.length !== wordSourceBindingFields.length) {
        errors.push(`${label} ${wordLabel}: source binding must provide all of: ${wordSourceBindingFields.join(", ")}`);
      } else {
        let validWordSourceBinding = true;
        for (const field of wordSourceBindingFields) {
          if (typeof word[field] !== "string" || word[field].trim().length === 0) {
            errors.push(`${label} ${wordLabel}: ${field} must be a non-empty string`);
            validWordSourceBinding = false;
          }
        }
        if (validWordSourceBinding) {
          if (word.sourceAssetId !== metadata.sourceAssetId) {
            errors.push(`${label} ${wordLabel}: WORD_SOURCE_ASSET_MISMATCH`);
          }
          if (word.sourceRevision !== metadata.sourceRevision) {
            errors.push(`${label} ${wordLabel}: WORD_SOURCE_REVISION_MISMATCH`);
          }
          if (sourceWordKeys.has(word.sourceWordKey)) {
            errors.push(`${label} ${wordLabel}: duplicate ${opaqueRef("sourceWordKey", word.sourceWordKey)}`);
          } else {
            sourceWordKeys.add(word.sourceWordKey);
          }
        }
      }
    }
    if (!wordKey) {
      errors.push(`${label}: word key missing`);
    } else if (wordKeys.has(wordKey)) {
      errors.push(`${label} ${wordLabel}: duplicate ${opaqueRef("wordKey", wordKey)}`);
    } else {
      wordKeys.add(wordKey);
    }
    if (!wordTextIsString) {
      errors.push(`${label} ${wordLabel}: text must be a string`);
    } else {
      if (!wordText) errors.push(`${label}: empty word text`);
      if (hasLineBreak(word.text)) errors.push(`${label} ${wordLabel}: text contains a CR or LF line break`);
    }
    if (!sourceTextProvided) {
      missingSourceTextCount += 1;
    } else if (!sourceTextIsString) {
      errors.push(`${label} ${wordLabel}: sourceText must be a string`);
    } else {
      if (!sourceText) errors.push(`${label} ${wordLabel}: sourceText is empty`);
      if (hasLineBreak(word.sourceText)) errors.push(`${label} ${wordLabel}: sourceText contains a CR or LF line break`);
    }
    if (editedProvided && !editedIsBoolean) {
      errors.push(`${label} ${wordLabel}: edited must be a boolean`);
    }
    const safeWordInterval = isSafeFrame(word.startFrame) && isSafeFrame(word.endFrame);
    if (!safeWordInterval) {
      errors.push(`${label} ${wordLabel}: frame interval must use non-negative safe integers`);
    }
    if (!Number.isFinite(wordStart) || !Number.isFinite(wordEnd) || wordEnd <= wordStart || wordStart < start || wordEnd > end) {
      errors.push(`${label} ${wordLabel}: interval is outside its page`);
    }
    if (safeWordInterval && wordEnd > wordStart && previousWord) {
      if (wordStart < previousWord.startFrame) {
        errors.push(`${label} ${wordLabel}: words are not sorted by start frame (precedes ${previousWord.label})`);
      }
      if (wordStart < previousWord.endFrame) {
        errors.push(`${label} ${wordLabel}: overlaps ${previousWord.label}`);
      }
    }
    if (safeWordInterval && wordEnd > wordStart) {
      previousWord = {label: wordLabel, startFrame: wordStart, endFrame: wordEnd};
    }
    let derivedEdited;
    if (wordTextIsString && sourceTextIsString) {
      derivedEdited = wordText !== sourceText;
      if (editedIsBoolean && word.edited !== derivedEdited) {
        errors.push(`${label} ${wordLabel}: edited assertion disagrees with derived edit state`);
      }
      const correction = word.correction;
      if (derivedEdited) {
        if (correction === null || typeof correction !== "object" || Array.isArray(correction)) {
          errors.push(`${label} ${wordLabel}: CORRECTION_RECORD_REQUIRED`);
        } else {
          const matchingTerms = matchingCorrectionTerms(sourceText, wordText);
          const matchingTermIds = matchingTerms
            .map((entry) => entry.termId)
            .filter((termId) => termId !== undefined);
          if (matchingTermIds.length > 0) {
            if (typeof correction.termId !== "string") {
              errors.push(`${label} ${wordLabel}: CORRECTION_TERM_ID_REQUIRED`);
            } else if (!matchingTermIds.includes(correction.termId)) {
              errors.push(`${label} ${wordLabel}: CORRECTION_TERM_ID_MISMATCH`);
            }
          } else if (typeof correction.termId === "string") {
            const declaredTerm = preparedTerminologyEntries.find((entry) => entry.termId === correction.termId);
            if (!declaredTerm) {
              errors.push(`${label} ${wordLabel}: CORRECTION_TERM_ID_UNKNOWN`);
            } else {
              errors.push(`${label} ${wordLabel}: CORRECTION_TERM_ID_MISMATCH`);
            }
          }
          const termRequiresAudio = matchingTerms.some((entry) => (
            entry.requiresAudioEvidence
            || entry.risk !== undefined
          ));
          if (
            (termRequiresAudio || isHighRiskSemanticChange(sourceText, wordText))
            && !hasAudioEvidence(correction.evidenceRefs)
          ) {
            errors.push(`${label} ${wordLabel}: CORRECTION_AUDIO_EVIDENCE_REQUIRED`);
          }
        }
      } else if (word.correction !== undefined) {
        errors.push(`${label} ${wordLabel}: STALE_CORRECTION_RECORD`);
      }
    }
    const requiresOverrideCheck = derivedEdited === true
      || (!sourceTextProvided && word.edited === true);
    if (requiresOverrideCheck && charCount(wordText) > replacementLimit) {
      errors.push(`${label} ${wordLabel}: word override exceeds ${replacementLimit} characters`);
    }
  }
}

if (captionPolicy.requireWordLevelAudit && wordCount === 0 && pages.length > 0) errors.push("word-level audit missing; request words=true");
if (missingSourceTextCount > 0) {
  warnings.push(`caption word evidence is missing sourceText on ${missingSourceTextCount} word(s); add sourceText before release`);
}
if (missingWordSourceBindingCount > 0) {
  warnings.push(`caption word evidence is missing source binding on ${missingWordSourceBindingCount} word(s); add sourceAssetId, sourceRevision, and sourceWordKey before release`);
}

const viewerText = pages.map((page) => normalize(page.text)).join("\n");
const traditionalCharacters = new RegExp(`[${policy.caption.traditionalCharacters}]`, "gu");
const traditionalHits = viewerText.match(traditionalCharacters) || [];
if (traditionalHits.length > captionPolicy.maxTraditionalChineseHits) {
  errors.push(`traditional Chinese: found ${traditionalHits.length} hit(s)`);
}

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function containsForbiddenTerminology({
  viewer,
  correct,
  wrong,
  matchMode,
  caseSensitive,
}) {
  const flags = caseSensitive ? "gu" : "giu";
  if (matchMode === "exact") {
    const pattern = `(?:^|\\n)\\s*${escapeRegExp(wrong)}\\s*(?:$|\\n)`;
    return new RegExp(pattern, flags).test(viewer);
  }

  const wrongMatches = viewer.matchAll(
    new RegExp(escapeRegExp(wrong), flags),
  );
  if (!correct) return !wrongMatches.next().done;

  const correctRanges = Array.from(
    viewer.matchAll(new RegExp(escapeRegExp(correct), flags)),
    (match) => [match.index, match.index + match[0].length],
  );
  for (const match of wrongMatches) {
    const start = match.index;
    const end = start + match[0].length;
    const isInsideCorrectTerm = correctRanges.some(
      ([correctStart, correctEnd]) => (
        correctStart <= start && end <= correctEnd
      ),
    );
    if (!isInsideCorrectTerm) return true;
  }
  return false;
}

for (const entry of preparedTerminologyEntries) {
  const correct = entry.correct;
  const wrongs = entry.wrongs;
  const caseSensitive = entry.caseSensitive;
  for (const rawWrong of wrongs) {
    const wrong = normalize(rawWrong);
    if (!wrong || wrong === correct) continue;
    if (containsForbiddenTerminology({
      viewer: viewerText,
      correct,
      wrong,
      matchMode: entry.matchMode,
      caseSensitive,
    })) {
      errors.push(`terminology entry ${entry.entryIndex}: forbidden form detected`);
    }
  }
}

for (const line of warnings) console.warn(`WARN ${line}`);
if (strictWarnings && warnings.length) {
  errors.push(`strict warning mode: ${warnings.length} warning(s) must be resolved`);
}
if (errors.length) {
  for (const line of [...new Set(errors)]) console.error(`FAIL ${line}`);
  console.error(`caption audit failed: ${new Set(errors).size} error(s), ${warnings.length} warning(s), ${pages.length} page(s)`);
  process.exit(1);
}
console.log(`caption audit passed: ${pages.length} page(s), ${wordCount} word(s), ${warnings.length} approved warning(s)`);
