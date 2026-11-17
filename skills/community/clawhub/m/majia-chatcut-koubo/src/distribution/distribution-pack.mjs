function finding(code, pointer, severity = "error") {
  return {code, pointer, severity};
}

function requireUnique(findings, items, key, pointer) {
  const seen = new Set();
  items.forEach((item, index) => {
    if (seen.has(item[key])) {
      findings.push(finding(
        "DISTRIBUTION_ID_DUPLICATE",
        `${pointer}/${index}/${key}`,
      ));
    }
    seen.add(item[key]);
  });
}

function parseDate(value) {
  const parsed = Date.parse(`${value}T00:00:00Z`);
  return Number.isFinite(parsed) ? parsed : null;
}

export function auditDistributionPack(pack, {asOf}) {
  const findings = [];
  const effectiveProfiles = [];
  const asOfTime = parseDate(asOf);
  if (asOfTime === null) {
    throw new TypeError("asOf must be an ISO calendar date");
  }
  requireUnique(findings, pack.platformProfiles, "profileId", "/platformProfiles");
  requireUnique(findings, pack.platformProfiles, "platformId", "/platformProfiles");
  requireUnique(findings, pack.deliverables, "deliverableId", "/deliverables");
  requireUnique(findings, pack.deliverables, "path", "/deliverables");

  for (const [index, profile] of pack.platformProfiles.entries()) {
    const observed = parseDate(profile.observedAt);
    const expires = parseDate(profile.expiresAt);
    if (observed === null || expires === null || expires < observed) {
      findings.push(finding(
        "DISTRIBUTION_PROFILE_DATE_INVALID",
        `/platformProfiles/${index}`,
      ));
      continue;
    }
    const stale = expires < asOfTime;
    if (stale) {
      findings.push(finding(
        "DISTRIBUTION_PROFILE_STALE",
        `/platformProfiles/${index}/expiresAt`,
        "warning",
      ));
    }
    effectiveProfiles.push({
      profileId: profile.profileId,
      platformId: profile.platformId,
      stale,
      rules: profile.rules.map((rule) => ({
        ruleId: rule.ruleId,
        effectiveLevel: stale ? "advisory" : rule.intendedLevel,
      })),
    });
  }

  const profilePlatforms = new Set(
    pack.platformProfiles.map((item) => item.platformId),
  );
  for (const [index, deliverable] of pack.deliverables.entries()) {
    const pointer = `/deliverables/${index}`;
    if (!profilePlatforms.has(deliverable.platformId)) {
      findings.push(finding(
        "DISTRIBUTION_PROFILE_MISSING",
        `${pointer}/platformId`,
      ));
    }
    if (deliverable.parentArtifactHash !== pack.master.artifactHash) {
      findings.push(finding(
        "DISTRIBUTION_MASTER_HASH_MISMATCH",
        `${pointer}/parentArtifactHash`,
      ));
    }
    if (deliverable.masterTimelineRevision !== pack.master.timelineRevision) {
      findings.push(finding(
        "DISTRIBUTION_MASTER_REVISION_MISMATCH",
        `${pointer}/masterTimelineRevision`,
      ));
    }
    if (deliverable.contentTruthHash !== pack.master.contentTruthHash) {
      findings.push(finding(
        "DISTRIBUTION_CONTENT_TRUTH_MISMATCH",
        `${pointer}/contentTruthHash`,
      ));
    }
  }
  if (pack.publishAction !== "none") {
    findings.push(finding(
      "DISTRIBUTION_PUBLISH_FORBIDDEN",
      "/publishAction",
    ));
  }
  const errors = findings.filter((item) => item.severity === "error").length;
  const warnings = findings.length - errors;
  return {
    status: errors === 0 ? "passed" : "failed",
    packId: pack.packId,
    summary: {
      deliverables: pack.deliverables.length,
      profiles: pack.platformProfiles.length,
      errors,
      warnings,
    },
    effectiveProfiles,
    findings,
  };
}
