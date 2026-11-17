import crypto from "node:crypto";

import {normalizeRate, validateTimeRange} from "../time/rational-time.mjs";

const HIDE_SENTINEL = "[[HIDE]]";

export class SrtBridgeError extends Error {
  constructor(code, message) {
    super(message);
    this.name = "SrtBridgeError";
    this.code = code;
  }
}

function sha256(value) {
  return `sha256:${crypto
    .createHash("sha256")
    .update(value)
    .digest("hex")}`;
}

function stableDecisionId(type, refs) {
  return `decision_${sha256(`${type}\u0000${refs.join("\u0000")}`)
    .slice(7, 23)}`;
}

function divFloor(numerator, denominator) {
  return numerator / denominator;
}

function divCeil(numerator, denominator) {
  return (numerator + denominator - 1n) / denominator;
}

function timeToMilliseconds(value, rate, rounding) {
  const normalized = normalizeRate(rate);
  const numerator = BigInt(value)
    * BigInt(normalized.denominator)
    * 1000n;
  const denominator = BigInt(normalized.numerator);
  const emitted = rounding === "floor"
    ? divFloor(numerator, denominator)
    : divCeil(numerator, denominator);
  const residual = numerator - emitted * denominator;
  if (
    emitted < 0n
    || emitted > BigInt(Number.MAX_SAFE_INTEGER)
    || residual < BigInt(Number.MIN_SAFE_INTEGER)
    || residual > BigInt(Number.MAX_SAFE_INTEGER)
  ) {
    throw new SrtBridgeError(
      "SRT_TIME_UNREPRESENTABLE",
      "cue time cannot be represented safely in SRT milliseconds",
    );
  }
  return {
    milliseconds: Number(emitted),
    residual: Number(residual),
    denominator: normalized.numerator,
  };
}

function pad(value, width) {
  return String(value).padStart(width, "0");
}

export function formatSrtTimestamp(milliseconds) {
  if (!Number.isSafeInteger(milliseconds) || milliseconds < 0) {
    throw new SrtBridgeError(
      "SRT_TIMESTAMP_INVALID",
      "SRT timestamp must be a non-negative safe integer",
    );
  }
  const hours = Math.floor(milliseconds / 3_600_000);
  const minutes = Math.floor((milliseconds % 3_600_000) / 60_000);
  const seconds = Math.floor((milliseconds % 60_000) / 1000);
  const remainder = milliseconds % 1000;
  return `${pad(hours, 2)}:${pad(minutes, 2)}:${pad(seconds, 2)},${pad(remainder, 3)}`;
}

function parseTimestamp(value) {
  const match = /^(?<hours>\d{2,}):(?<minutes>[0-5]\d):(?<seconds>[0-5]\d),(?<milliseconds>\d{3})$/u
    .exec(value);
  if (!match) {
    throw new SrtBridgeError(
      "SRT_TIMESTAMP_INVALID",
      "SRT timestamp has invalid syntax",
    );
  }
  const groups = match.groups;
  const result =
    Number(groups.hours) * 3_600_000
    + Number(groups.minutes) * 60_000
    + Number(groups.seconds) * 1000
    + Number(groups.milliseconds);
  if (!Number.isSafeInteger(result)) {
    throw new SrtBridgeError(
      "SRT_TIMESTAMP_INVALID",
      "SRT timestamp is outside the safe integer range",
    );
  }
  return result;
}

export function parseSrt(source) {
  if (typeof source !== "string") {
    throw new SrtBridgeError("SRT_INPUT_INVALID", "SRT input must be text");
  }
  const normalized = source
    .replace(/^\uFEFF/u, "")
    .replace(/\r\n?/gu, "\n")
    .trim();
  if (normalized.length === 0) return [];
  const blocks = normalized.split(/\n{2,}/u);
  const seenIndexes = new Set();
  return blocks.map((block, position) => {
    const lines = block.split("\n");
    if (lines.length < 2 || !/^\d+$/u.test(lines[0])) {
      throw new SrtBridgeError(
        "SRT_CUE_INVALID",
        "SRT cue must begin with a numeric index",
      );
    }
    const index = Number(lines[0]);
    if (!Number.isSafeInteger(index) || index < 1 || seenIndexes.has(index)) {
      throw new SrtBridgeError(
        "SRT_INDEX_INVALID",
        "SRT cue indexes must be unique positive safe integers",
      );
    }
    seenIndexes.add(index);
    const timing = /^(?<start>\S+)\s+-->\s+(?<end>\S+)$/u.exec(lines[1]);
    if (!timing) {
      throw new SrtBridgeError(
        "SRT_CUE_INVALID",
        "SRT cue timing line is invalid",
      );
    }
    const startMs = parseTimestamp(timing.groups.start);
    const endMs = parseTimestamp(timing.groups.end);
    if (endMs <= startMs) {
      throw new SrtBridgeError(
        "SRT_RANGE_INVALID",
        "SRT cue ranges must be non-empty half-open intervals",
      );
    }
    return {
      index,
      position,
      startMs,
      endMs,
      text: lines.slice(2).join("\n").trim(),
    };
  });
}

export function exportSrtBridge(captionPlan) {
  if (!captionPlan || !Array.isArray(captionPlan.pages)) {
    throw new SrtBridgeError(
      "SRT_CAPTION_PLAN_INVALID",
      "caption plan is missing pages",
    );
  }
  const rate = captionPlan.pages[0]?.range?.rate;
  const cues = captionPlan.pages.map((page, position) => {
    validateTimeRange(page.range, "timeline");
    const start = timeToMilliseconds(page.range.start, page.range.rate, "floor");
    const end = timeToMilliseconds(page.range.end, page.range.rate, "ceil");
    return {
      cueId: `cue_${page.pageId.replace(/^caption_/u, "")}`,
      pageId: page.pageId,
      ordinal: position + 1,
      range: structuredClone(page.range),
      emitted: {
        startMs: start.milliseconds,
        endMs: end.milliseconds,
      },
      quantization: {
        startResidual: start.residual,
        endResidual: end.residual,
        denominator: start.denominator,
      },
      sourceWordIds: [...page.sourceWordIds],
      sourceText: page.sourceText,
      displayText: page.displayText,
      evidenceRefs: [...page.evidenceRefs],
    };
  });
  const srt = `${cues.map((cue) => [
    cue.ordinal,
    `${formatSrtTimestamp(cue.emitted.startMs)} --> ${formatSrtTimestamp(cue.emitted.endMs)}`,
    cue.displayText,
  ].join("\n")).join("\n\n")}\n`;
  return {
    srt,
    sidecar: {
      $schema: "https://github.com/maojiebc/majia-chatcut-koubo/schemas/srt-sidecar.schema.json",
      schemaVersion: "1.0.0",
      bridgeId: `bridge_${sha256(JSON.stringify(captionPlan)).slice(7, 19)}`,
      projectId: captionPlan.projectId,
      timelineId: captionPlan.timelineId,
      timelineRevision: captionPlan.timelineRevision,
      transcriptId: captionPlan.transcriptId,
      transcriptRevision: captionPlan.transcriptRevision,
      captionPlanHash: sha256(JSON.stringify(captionPlan)),
      rate: structuredClone(rate),
      cues,
    },
  };
}

function sameTiming(imported, original) {
  return imported.startMs === original.emitted.startMs
    && imported.endMs === original.emitted.endMs;
}

function overlaps(imported, original) {
  return imported.startMs < original.emitted.endMs
    && imported.endMs > original.emitted.startMs;
}

export function validateSrtSidecar(sidecar) {
  if (!sidecar || !Array.isArray(sidecar.cues) || sidecar.cues.length === 0) {
    throw new SrtBridgeError(
      "SRT_SIDECAR_INVALID",
      "SRT sidecar is missing cues",
    );
  }
  const cueIds = new Set();
  const pageIds = new Set();
  sidecar.cues.forEach((cue, index) => {
    if (
      cue.ordinal !== index + 1
      || cueIds.has(cue.cueId)
      || pageIds.has(cue.pageId)
    ) {
      throw new SrtBridgeError(
        "SRT_SIDECAR_IDENTITY_INVALID",
        "SRT sidecar cue identities or ordinals are invalid",
      );
    }
    cueIds.add(cue.cueId);
    pageIds.add(cue.pageId);
    try {
      validateTimeRange(cue.range, "timeline");
    } catch {
      throw new SrtBridgeError(
        "SRT_SIDECAR_RANGE_INVALID",
        "SRT sidecar contains an invalid exact range",
      );
    }
    const start = timeToMilliseconds(cue.range.start, cue.range.rate, "floor");
    const end = timeToMilliseconds(cue.range.end, cue.range.rate, "ceil");
    if (
      cue.emitted.startMs !== start.milliseconds
      || cue.emitted.endMs !== end.milliseconds
      || cue.quantization.startResidual !== start.residual
      || cue.quantization.endResidual !== end.residual
      || cue.quantization.denominator !== start.denominator
    ) {
      throw new SrtBridgeError(
        "SRT_SIDECAR_QUANTIZATION_DRIFT",
        "SRT sidecar quantization no longer matches its exact range",
      );
    }
  });
  return true;
}

function chooseUnique(candidates) {
  if (candidates.length > 1) {
    throw new SrtBridgeError(
      "SRT_MATCH_AMBIGUOUS",
      "edited cue cannot be matched to one stable sidecar identity",
    );
  }
  return candidates[0] ?? null;
}

function decision(type, refs, changes = {}) {
  const highRisk = new Set(["delete", "merge", "split", "reorder"]);
  return {
    decisionId: stableDecisionId(type, refs),
    type,
    subjectRefs: refs,
    risk: highRisk.has(type) ? "high" : "medium",
    requiresApproval: highRisk.has(type),
    status: "candidate",
    ...changes,
  };
}

export function diffSrtBridge({srt, sidecar}) {
  validateSrtSidecar(sidecar);
  const imported = parseSrt(srt);
  const unmatchedOriginals = new Set(sidecar.cues);
  const unmatchedImported = new Set(imported);
  const matches = [];

  for (const mode of ["exact", "timing", "text"]) {
    for (const cue of [...unmatchedImported]) {
      const candidates = [...unmatchedOriginals].filter((original) => {
        if (mode === "exact") {
          return sameTiming(cue, original) && cue.text === original.displayText;
        }
        if (mode === "timing") return sameTiming(cue, original);
        if (cue.text !== original.displayText) return false;
        const overlappingImports = [...unmatchedImported].filter(
          (candidate) => overlaps(candidate, original),
        );
        return overlappingImports.length <= 1;
      });
      const original = chooseUnique(candidates);
      if (original) {
        matches.push({cue, original});
        unmatchedImported.delete(cue);
        unmatchedOriginals.delete(original);
      }
    }
  }
  for (const cue of [...unmatchedImported]) {
    const originals = [...unmatchedOriginals].filter(
      (original) => overlaps(cue, original),
    );
    if (originals.length !== 1) continue;
    const [original] = originals;
    const importedForOriginal = [...unmatchedImported].filter(
      (candidate) => overlaps(candidate, original),
    );
    if (importedForOriginal.length === 1) {
      matches.push({cue, original});
      unmatchedImported.delete(cue);
      unmatchedOriginals.delete(original);
    }
  }

  const decisions = [];
  const consumedOriginals = new Set();
  const consumedImported = new Set();
  for (const original of unmatchedOriginals) {
    const overlapping = [...unmatchedImported].filter(
      (cue) => overlaps(cue, original),
    );
    if (overlapping.length > 1) {
      decisions.push(decision(
        "split",
        [original.cueId, ...overlapping.map((cue) => `srt_${cue.index}`)],
      ));
      consumedOriginals.add(original);
      overlapping.forEach((cue) => consumedImported.add(cue));
    }
  }
  for (const cue of unmatchedImported) {
    if (consumedImported.has(cue)) continue;
    const overlapping = [...unmatchedOriginals].filter(
      (original) =>
        !consumedOriginals.has(original)
        && overlaps(cue, original),
    );
    if (overlapping.length > 1) {
      decisions.push(decision(
        "merge",
        [...overlapping.map((original) => original.cueId), `srt_${cue.index}`],
      ));
      overlapping.forEach((original) => consumedOriginals.add(original));
      consumedImported.add(cue);
    }
  }
  for (const original of unmatchedOriginals) {
    if (!consumedOriginals.has(original)) {
      decisions.push(decision("delete", [original.cueId]));
    }
  }
  for (const cue of unmatchedImported) {
    if (!consumedImported.has(cue)) {
      decisions.push(decision("split", [`srt_${cue.index}`]));
    }
  }

  for (const {cue, original} of matches) {
    if (cue.text === HIDE_SENTINEL || cue.text.length === 0) {
      decisions.push(decision("hide-caption", [original.cueId]));
    } else if (cue.text !== original.displayText) {
      decisions.push(decision("correction", [original.cueId], {
        before: original.displayText,
        after: cue.text,
      }));
    }
    if (!sameTiming(cue, original)) {
      decisions.push(decision("retime", [original.cueId], {
        before: structuredClone(original.emitted),
        after: {startMs: cue.startMs, endMs: cue.endMs},
      }));
    }
  }

  const matchedByImportedPosition = [...matches]
    .sort((left, right) => left.cue.position - right.cue.position)
    .map(({original}) => original.cueId);
  const expectedOrder = sidecar.cues
    .filter((original) => matches.some((match) => match.original === original))
    .map((original) => original.cueId);
  if (
    matchedByImportedPosition.length > 1
    && matchedByImportedPosition.some(
      (cueId, index) => cueId !== expectedOrder[index],
    )
  ) {
    decisions.push(decision("reorder", matchedByImportedPosition));
  }

  return {
    status: decisions.length === 0 ? "unchanged" : "candidates",
    bridgeId: sidecar.bridgeId,
    summary: {
      importedCues: imported.length,
      matchedCues: matches.length,
      candidates: decisions.length,
    },
    decisions,
  };
}

export const SRT_HIDE_SENTINEL = HIDE_SENTINEL;
