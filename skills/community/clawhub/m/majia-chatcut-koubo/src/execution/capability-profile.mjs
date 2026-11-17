const REQUIRED_CAPABILITIES = [
  "timeline-read",
  "timeline-write",
  "media-import",
  "preview-render",
  "media-export",
];

function finding(code, pointer, severity = "error") {
  return {code, pointer, severity};
}

function dateValue(value) {
  const parsed = Date.parse(value ?? "");
  return Number.isFinite(parsed) ? parsed : null;
}

export function auditCapabilityProfile(profile, {asOf}) {
  const findings = [];
  const asOfTime = dateValue(asOf);
  if (asOfTime === null) {
    throw new TypeError("asOf must be an ISO date-time");
  }
  const seen = new Set();
  profile.capabilities.forEach((capability, index) => {
    if (seen.has(capability.capabilityId)) {
      findings.push(finding(
        "CAPABILITY_ID_DUPLICATE",
        `/capabilities/${index}/capabilityId`,
      ));
    }
    seen.add(capability.capabilityId);
  });
  for (const capabilityId of REQUIRED_CAPABILITIES) {
    if (!seen.has(capabilityId)) {
      findings.push(finding(
        "CAPABILITY_MANDATORY_MISSING",
        "/capabilities",
      ));
    }
  }

  const observed = dateValue(profile.observedAt);
  const expires = dateValue(profile.expiresAt);
  const expired = expires !== null && expires < asOfTime;
  if (
    observed !== null
    && expires !== null
    && expires < observed
  ) {
    findings.push(finding(
      "CAPABILITY_TTL_INVALID",
      "/expiresAt",
    ));
  }
  if (expired) {
    findings.push(finding(
      "CAPABILITY_PROFILE_STALE",
      "/expiresAt",
      "warning",
    ));
  }

  const mandatory = profile.capabilities.filter(
    (capability) => capability.mandatory,
  );
  const validatedEvidence = mandatory.every(
    (capability) =>
      capability.status === "validated"
      && capability.probeRefs.length > 0,
  );
  const currentEvidence = (
    profile.status === "validated"
    && typeof profile.hostBuild === "string"
    && typeof profile.toolSchemaHash === "string"
    && observed !== null
    && expires !== null
    && !expired
    && profile.canary.status === "passed"
    && profile.canary.evidenceRefs.length > 0
    && validatedEvidence
  );
  if (profile.status === "validated" && !currentEvidence) {
    findings.push(finding(
      "CAPABILITY_VALIDATION_EVIDENCE_INCOMPLETE",
      "/",
    ));
  }
  if (profile.canary.status === "failed") {
    findings.push(finding(
      "CAPABILITY_CANARY_FAILED",
      "/canary/status",
    ));
  }

  const liveAllowed = currentEvidence && findings.every(
    (item) => item.severity !== "error",
  );
  if (profile.liveRouteRequested && !liveAllowed) {
    findings.push(finding(
      "CAPABILITY_LIVE_ROUTE_BLOCKED",
      "/liveRouteRequested",
    ));
  }
  const routes = profile.capabilities.map((capability) => ({
    capabilityId: capability.capabilityId,
    route: liveAllowed && capability.status === "validated"
      ? "live"
      : capability.fallback,
  }));
  const errors = findings.filter(
    (item) => item.severity === "error",
  ).length;
  return {
    status: errors === 0 ? "passed" : "failed",
    profileId: profile.profileId,
    effectiveStatus: liveAllowed ? "validated" : (
      expired ? "stale" : "unverified"
    ),
    liveAllowed,
    routes,
    summary: {
      capabilities: profile.capabilities.length,
      errors,
      warnings: findings.length - errors,
    },
    findings,
  };
}
