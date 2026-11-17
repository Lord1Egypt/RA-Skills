import {
  ratesEqual,
  validateTimeRange,
} from "../time/rational-time.mjs";

function finding(code, pointer) {
  return {code, pointer};
}

function addSample(samples, position, reason, duration) {
  if (position < duration.start || position >= duration.end) return;
  const existing = samples.get(position) ?? new Set();
  existing.add(reason);
  samples.set(position, existing);
}

export function buildInspectionSchedule({
  duration,
  boundaries = [],
  privacyRisks = [],
}) {
  validateTimeRange(duration, "export");
  const samples = new Map();
  addSample(samples, duration.start, "start", duration);
  addSample(samples, duration.end - 1, "end", duration);
  for (const boundary of boundaries) {
    addSample(samples, boundary - 1, "boundary-before", duration);
    addSample(samples, boundary, "boundary", duration);
    addSample(samples, boundary + 1, "boundary-after", duration);
  }
  for (const risk of privacyRisks) {
    validateTimeRange(risk.range, "export");
    addSample(samples, risk.range.start, "privacy-start", duration);
    addSample(
      samples,
      Math.floor((risk.range.start + risk.range.end - 1) / 2),
      "privacy-mid",
      duration,
    );
    addSample(samples, risk.range.end - 1, "privacy-end", duration);
  }
  return [...samples.entries()]
    .sort(([left], [right]) => left - right)
    .map(([position, reasons], index) => ({
      sampleId: `sample_${String(index + 1).padStart(3, "0")}`,
      position,
      reasons: [...reasons].sort(),
      evidenceRef: `evidence_frame_${String(index + 1).padStart(3, "0")}`,
    }));
}

function rangesCover(ranges, target) {
  const clipped = ranges
    .map((range) => ({
      start: Math.max(range.start, target.start),
      end: Math.min(range.end, target.end),
    }))
    .filter((range) => range.end > range.start)
    .sort((left, right) => left.start - right.start);
  let cursor = target.start;
  for (const range of clipped) {
    if (range.start > cursor) return false;
    cursor = Math.max(cursor, range.end);
    if (cursor >= target.end) return true;
  }
  return cursor >= target.end;
}

function durationUnits(range) {
  return range.end - range.start;
}

function auditRangeCollection(findings, ranges, duration, pointer) {
  ranges.forEach((range, index) => {
    try {
      validateTimeRange(range, "export");
      if (
        !ratesEqual(range.rate, duration.rate)
        || range.start < duration.start
        || range.end > duration.end
      ) {
        findings.push(finding(
          "MEDIA_RANGE_OUTSIDE_ARTIFACT",
          `${pointer}/${index}`,
        ));
      }
    } catch {
      findings.push(finding("MEDIA_RANGE_INVALID", `${pointer}/${index}`));
    }
  });
}

function compareProbe(findings, expected, actual) {
  for (const key of [
    "videoCodec",
    "width",
    "height",
    "pixelFormat",
    "colorSpace",
    "audioCodec",
    "audioChannels",
    "audioSampleRate",
  ]) {
    if (expected[key] !== actual[key]) {
      findings.push(finding(
        "MEDIA_PROBE_MISMATCH",
        `/actualProbe/${key}`,
      ));
    }
  }
  for (const key of ["frameRate", "timeBase"]) {
    if (!ratesEqual(expected[key], actual[key])) {
      findings.push(finding(
        "MEDIA_PROBE_MISMATCH",
        `/actualProbe/${key}`,
      ));
    }
  }
  if (
    expected.duration.start !== actual.duration.start
    || expected.duration.end !== actual.duration.end
    || !ratesEqual(expected.duration.rate, actual.duration.rate)
  ) {
    findings.push(finding(
      "MEDIA_PROBE_MISMATCH",
      "/actualProbe/duration",
    ));
  }
}

export function auditMediaRelease(report) {
  const findings = [];
  const duration = report.actualProbe.duration;
  try {
    validateTimeRange(duration, "export");
  } catch {
    findings.push(finding("MEDIA_DURATION_INVALID", "/actualProbe/duration"));
    return {status: "failed", findings};
  }
  compareProbe(findings, report.expectedProbe, report.actualProbe);
  const policy = report.qaPolicy;
  if (
    policy.loudnessMinLufs > policy.loudnessMaxLufs
    || report.audioAnalysis.integratedLufs < policy.loudnessMinLufs
    || report.audioAnalysis.integratedLufs > policy.loudnessMaxLufs
  ) {
    findings.push(finding("MEDIA_LOUDNESS_OUT_OF_RANGE", "/audioAnalysis/integratedLufs"));
  }
  if (report.audioAnalysis.truePeakDbtp > policy.truePeakMaxDbtp) {
    findings.push(finding("MEDIA_TRUE_PEAK_EXCEEDED", "/audioAnalysis/truePeakDbtp"));
  }
  auditRangeCollection(
    findings,
    report.audioAnalysis.silenceSegments,
    duration,
    "/audioAnalysis/silenceSegments",
  );
  report.audioAnalysis.silenceSegments.forEach((range, index) => {
    if (durationUnits(range) > policy.maxSilenceUnits) {
      findings.push(finding(
        "MEDIA_SILENCE_TOO_LONG",
        `/audioAnalysis/silenceSegments/${index}`,
      ));
    }
  });
  for (const [collection, maximum, code] of [
    [report.visualAnalysis.blackSegments, policy.maxBlackUnits, "MEDIA_BLACK_TOO_LONG"],
    [report.visualAnalysis.freezeSegments, policy.maxFreezeUnits, "MEDIA_FREEZE_TOO_LONG"],
  ]) {
    auditRangeCollection(findings, collection, duration, "/visualAnalysis");
    collection.forEach((range, index) => {
      if (durationUnits(range) > maximum) {
        findings.push(finding(code, `/visualAnalysis/${index}`));
      }
    });
  }

  auditRangeCollection(
    findings,
    report.privacy.risks.map((item) => item.range),
    duration,
    "/privacy/risks",
  );
  auditRangeCollection(
    findings,
    report.privacy.treatments.map((item) => item.range),
    duration,
    "/privacy/treatments",
  );
  report.privacy.risks
    .filter((risk) => risk.severity === "critical")
    .forEach((risk, index) => {
      const treatments = report.privacy.treatments
        .filter((item) => item.riskId === risk.riskId)
        .map((item) => item.range);
      if (!rangesCover(treatments, risk.range)) {
        findings.push(finding(
          "MEDIA_PRIVACY_COVERAGE_MISSING",
          `/privacy/risks/${index}`,
        ));
      }
    });

  const expectedSamples = buildInspectionSchedule({
    duration,
    boundaries: report.inspection.boundaries,
    privacyRisks: report.privacy.risks,
  });
  if (JSON.stringify(expectedSamples) !== JSON.stringify(report.inspection.samples)) {
    findings.push(finding("MEDIA_INSPECTION_SCHEDULE_DRIFT", "/inspection/samples"));
  }
  const authorization = report.exportAuthorization;
  if (
    authorization.decision !== "approved"
    || authorization.artifactHash !== report.artifact.sha256
    || authorization.planHash !== report.planHash
  ) {
    findings.push(finding(
      "MEDIA_EXPORT_AUTHORIZATION_MISMATCH",
      "/exportAuthorization",
    ));
  }
  const computedStatus = findings.length === 0 ? "passed" : "failed";
  if (report.status !== computedStatus) {
    findings.push(finding("MEDIA_STATUS_CLAIM_MISMATCH", "/status"));
  }
  return {
    status: findings.length === 0 ? "passed" : "failed",
    artifactId: report.artifact.artifactId,
    summary: {
      samples: report.inspection.samples.length,
      privacyRisks: report.privacy.risks.length,
      errors: findings.length,
    },
    findings,
  };
}
