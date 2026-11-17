import fs from "node:fs";
import path from "node:path";

import Ajv2020 from "ajv/dist/2020.js";
import addFormats from "ajv-formats";

import {
  auditContiguousCoverage,
  rangesEqual,
  ratesEqual,
  validateTimeRange,
} from "../time/rational-time.mjs";

const SCHEMA_FILES = Object.freeze({
  project: "schemas/project-manifest.schema.json",
  transcript: "schemas/transcript.schema.json",
  editPlan: "schemas/edit-plan.schema.json",
  statePlan: "schemas/state-plan.schema.json",
  ownerLedger: "schemas/owner-ledger.schema.json",
  captionPlan: "schemas/caption-plan.schema.json",
  evidenceManifest: "schemas/evidence-manifest.schema.json",
  bundle: "schemas/plan-bundle.schema.json",
});
const COMMON_SCHEMA = "schemas/creator-os-common.schema.json";

export class PlanBundleError extends Error {
  constructor(code, message, options = {}) {
    super(message, options);
    this.name = "PlanBundleError";
    this.code = code;
  }
}

function finding(code, pointer, message, details = {}) {
  return {code, pointer, message, ...details};
}

function isInsideRoot(root, candidate) {
  const relative = path.relative(root, candidate);
  return relative === ""
    || (
      relative !== ".."
      && !relative.startsWith(`..${path.sep}`)
      && !path.isAbsolute(relative)
    );
}

function normalizeRelativePath(value) {
  if (
    typeof value !== "string"
    || value.length === 0
    || value.includes("\\")
    || path.posix.isAbsolute(value)
  ) {
    return null;
  }
  const normalized = path.posix.normalize(value);
  if (
    normalized === "."
    || normalized === ".."
    || normalized.startsWith("../")
    || normalized !== value
  ) {
    return null;
  }
  return normalized;
}

function inspectFile(root, base, relativePath) {
  const normalized = normalizeRelativePath(relativePath);
  if (!normalized) return {ok: false, code: "PLAN_UNSAFE_PATH"};
  const absolutePath = path.resolve(base, normalized);
  if (!isInsideRoot(root, absolutePath)) {
    return {ok: false, code: "PLAN_UNSAFE_PATH"};
  }
  let stat;
  try {
    stat = fs.lstatSync(absolutePath);
  } catch {
    return {ok: false, code: "PLAN_FILE_MISSING"};
  }
  if (stat.isSymbolicLink()) {
    return {ok: false, code: "PLAN_SYMLINK_NOT_ALLOWED"};
  }
  if (!stat.isFile()) {
    return {ok: false, code: "PLAN_FILE_NOT_REGULAR"};
  }
  let canonical;
  try {
    canonical = fs.realpathSync(absolutePath);
  } catch {
    return {ok: false, code: "PLAN_FILE_UNREADABLE"};
  }
  if (!isInsideRoot(root, canonical)) {
    return {ok: false, code: "PLAN_UNSAFE_PATH"};
  }
  return {ok: true, absolutePath: canonical, relativePath: normalized};
}

function readJson(absolutePath, code) {
  let source;
  try {
    source = fs.readFileSync(absolutePath, "utf8");
  } catch (cause) {
    throw new PlanBundleError(code, "plan input is not readable", {cause});
  }
  try {
    return JSON.parse(source);
  } catch (cause) {
    throw new PlanBundleError(code, "plan input is invalid JSON", {cause});
  }
}

function createValidators(root) {
  const ajv = new Ajv2020({
    allErrors: true,
    allowUnionTypes: true,
    logger: false,
    strict: true,
    strictRequired: false,
    validateFormats: true,
  });
  addFormats(ajv);
  const documents = [
    COMMON_SCHEMA,
    ...Object.values(SCHEMA_FILES),
  ].map((relativePath) => readJson(
    path.join(root, relativePath),
    "PLAN_SCHEMA_READ_FAILED",
  ));
  for (const document of documents) ajv.addSchema(document);
  const validators = {};
  for (const [name, relativePath] of Object.entries(SCHEMA_FILES)) {
    const schemaId = readJson(
      path.join(root, relativePath),
      "PLAN_SCHEMA_READ_FAILED",
    ).$id;
    validators[name] = ajv.getSchema(schemaId);
    if (typeof validators[name] !== "function") {
      throw new PlanBundleError(
        "PLAN_SCHEMA_COMPILE_FAILED",
        "plan schema could not be compiled",
      );
    }
  }
  return validators;
}

function schemaFindings(validate, document, documentName) {
  if (validate(document)) return [];
  return (validate.errors ?? []).map((error) =>
    finding(
      `PLAN_SCHEMA_${error.keyword
        .replace(/([a-z])([A-Z])/gu, "$1_$2")
        .replaceAll("-", "_")
        .toUpperCase()}`,
      `/documents/${documentName}${error.instancePath || ""}`,
      "plan document does not match its schema",
      {document: documentName},
    ));
}

function requireEqual(findings, left, right, code, pointer, message) {
  if (left !== right) findings.push(finding(code, pointer, message));
}

function requireUnique(findings, items, key, pointer, code) {
  const seen = new Set();
  items.forEach((item, index) => {
    const value = item[key];
    if (seen.has(value)) {
      findings.push(
        finding(
          code,
          `${pointer}/${index}/${key}`,
          `${key} must be document-global unique`,
        ),
      );
    }
    seen.add(value);
  });
}

function auditRange(findings, range, expectedDomain, expectedRate, pointer) {
  try {
    validateTimeRange(range, expectedDomain);
  } catch (error) {
    findings.push(
      finding(
        error.code ?? "PLAN_TIME_INVALID",
        pointer,
        "time range is invalid",
      ),
    );
    return false;
  }
  if (expectedRate && !ratesEqual(range.rate, expectedRate)) {
    findings.push(
      finding(
        "PLAN_TIME_RATE_MISMATCH",
        `${pointer}/rate`,
        "time range rate differs from its owning timeline or source",
      ),
    );
    return false;
  }
  return true;
}

function safeRangesEqual(left, right) {
  try {
    return rangesEqual(left, right);
  } catch {
    return false;
  }
}

function auditProject(findings, project) {
  auditRange(
    findings,
    project.timeline.duration,
    "timeline",
    project.timeline.duration.rate,
    "/documents/project/timeline/duration",
  );
  if (project.timeline.duration.start !== 0) {
    findings.push(
      finding(
        "PLAN_TIMELINE_START",
        "/documents/project/timeline/duration/start",
        "timeline duration must start at zero",
      ),
    );
  }
  requireUnique(
    findings,
    project.sources,
    "assetId",
    "/documents/project/sources",
    "PLAN_SOURCE_DUPLICATE",
  );
  project.sources.forEach((source, index) => {
    auditRange(
      findings,
      source.duration,
      "source",
      source.duration.rate,
      `/documents/project/sources/${index}/duration`,
    );
    if (source.duration.start !== 0) {
      findings.push(
        finding(
          "PLAN_SOURCE_START",
          `/documents/project/sources/${index}/duration/start`,
          "source duration must start at zero",
        ),
      );
    }
  });
}

function auditTranscript(findings, project, transcript, evidenceById) {
  const source = project.sources.find(
    (candidate) => candidate.assetId === transcript.sourceAssetId,
  );
  if (!source) {
    findings.push(
      finding(
        "PLAN_TRANSCRIPT_SOURCE_UNKNOWN",
        "/documents/transcript/sourceAssetId",
        "transcript source is not declared by the project",
      ),
    );
    return;
  }
  requireEqual(
    findings,
    transcript.sourceRevision,
    source.revision,
    "PLAN_TRANSCRIPT_SOURCE_REVISION",
    "/documents/transcript/sourceRevision",
    "transcript source revision differs from the project source",
  );
  requireUnique(
    findings,
    transcript.words,
    "wordId",
    "/documents/transcript/words",
    "PLAN_WORD_DUPLICATE",
  );
  let previousEnd = null;
  transcript.words.forEach((word, index) => {
    const pointer = `/documents/transcript/words/${index}`;
    const validRange = auditRange(
      findings,
      word.range,
      "source",
      source.duration.rate,
      `${pointer}/range`,
    );
    if (validRange) {
      if (
        word.range.start < source.duration.start
        || word.range.end > source.duration.end
      ) {
        findings.push(
          finding(
            "PLAN_WORD_OUTSIDE_SOURCE",
            `${pointer}/range`,
            "word range leaves the declared source duration",
          ),
        );
      }
      if (previousEnd !== null && word.range.start < previousEnd) {
        findings.push(
          finding(
            "PLAN_WORD_OVERLAP",
            `${pointer}/range/start`,
            "word ranges must be monotonic and non-overlapping",
          ),
        );
      }
      previousEnd = Math.max(previousEnd ?? 0, word.range.end);
    }
    for (const evidenceRef of word.evidenceRefs) {
      const evidence = evidenceById.get(evidenceRef);
      if (!evidence) {
        findings.push(
          finding(
            "PLAN_EVIDENCE_UNKNOWN",
            `${pointer}/evidenceRefs`,
            "word references unknown evidence",
          ),
        );
      } else if (evidence.result !== "passed") {
        findings.push(
          finding(
            "PLAN_CONTENT_EVIDENCE_UNVERIFIED",
            `${pointer}/evidenceRefs`,
            "validated transcript words require passed evidence",
          ),
        );
      }
    }
  });
}

function auditEditPlan(findings, transcript, editPlan, bundleStatus) {
  requireEqual(
    findings,
    editPlan.transcriptId,
    transcript.transcriptId,
    "PLAN_EDIT_TRANSCRIPT_ID",
    "/documents/editPlan/transcriptId",
    "edit plan targets a different transcript",
  );
  requireEqual(
    findings,
    editPlan.transcriptRevision,
    transcript.revision,
    "PLAN_EDIT_TRANSCRIPT_REVISION",
    "/documents/editPlan/transcriptRevision",
    "edit plan targets a different transcript revision",
  );
  const wordIds = new Set(transcript.words.map((word) => word.wordId));
  requireUnique(
    findings,
    editPlan.segments,
    "segmentId",
    "/documents/editPlan/segments",
    "PLAN_SEGMENT_DUPLICATE",
  );
  requireUnique(
    findings,
    editPlan.segments,
    "order",
    "/documents/editPlan/segments",
    "PLAN_SEGMENT_ORDER_DUPLICATE",
  );
  editPlan.segments.forEach((segment, index) => {
    const pointer = `/documents/editPlan/segments/${index}`;
    if (segment.sourceAssetId !== transcript.sourceAssetId) {
      findings.push(
        finding(
          "PLAN_EDIT_SOURCE_MISMATCH",
          `${pointer}/sourceAssetId`,
          "edit segment source differs from the transcript source",
        ),
      );
    }
    for (const wordId of segment.sourceWordIds) {
      if (!wordIds.has(wordId)) {
        findings.push(
          finding(
            "PLAN_EDIT_WORD_UNKNOWN",
            `${pointer}/sourceWordIds`,
            "edit segment references an unknown word",
          ),
        );
      }
    }
    const highRisk =
      segment.risk === "high"
      || segment.action === "reorder";
    if (highRisk && !segment.approval.required) {
      findings.push(
        finding(
          "PLAN_EDIT_APPROVAL_REQUIRED",
          `${pointer}/approval/required`,
          "high-risk edit decisions must require approval",
        ),
      );
    }
    if (
      bundleStatus === "validated"
      && highRisk
      && (
        segment.approval.status !== "approved"
        || !segment.approval.approvalId
      )
    ) {
      findings.push(
        finding(
          "PLAN_EDIT_APPROVAL_PENDING",
          `${pointer}/approval`,
          "validated bundles cannot contain unapproved high-risk edits",
        ),
      );
    }
  });
}

function auditStateAndOwners(
  findings,
  project,
  statePlan,
  ownerLedger,
  bundleStatus,
) {
  const timeline = project.timeline;
  const stateRanges = statePlan.compositionStates.map((state) => state.range);
  for (const coverage of auditContiguousCoverage(
    stateRanges,
    timeline.duration,
  )) {
    findings.push(
      finding(
        coverage.code.replace("TIME_", "PLAN_"),
        `/documents/statePlan/compositionStates/${coverage.index}`,
        "composition states must cover the timeline exactly once",
      ),
    );
  }
  statePlan.compositionStates.forEach((state, index) => {
    auditRange(
      findings,
      state.range,
      "timeline",
      timeline.duration.rate,
      `/documents/statePlan/compositionStates/${index}/range`,
    );
  });
  statePlan.privacyOverlays.forEach((overlay, index) => {
    const pointer = `/documents/statePlan/privacyOverlays/${index}`;
    auditRange(
      findings,
      overlay.range,
      "timeline",
      timeline.duration.rate,
      `${pointer}/range`,
    );
    const source = project.sources.find(
      (candidate) => candidate.assetId === overlay.sourceAssetId,
    );
    if (!source) {
      findings.push(
        finding(
          "PLAN_PRIVACY_SOURCE_UNKNOWN",
          `${pointer}/sourceAssetId`,
          "privacy overlay source is not declared by the project",
        ),
      );
      return;
    }
    if (auditRange(
      findings,
      overlay.sourceRange,
      "source",
      source.duration.rate,
      `${pointer}/sourceRange`,
    ) && (
      overlay.sourceRange.start < source.duration.start
      || overlay.sourceRange.end > source.duration.end
    )) {
      findings.push(
        finding(
          "PLAN_PRIVACY_SOURCE_OUTSIDE_ASSET",
          `${pointer}/sourceRange`,
          "privacy source range leaves the declared source duration",
        ),
      );
    }
  });
  if (
    bundleStatus === "validated"
    && (
      !statePlan.approval.required
      || statePlan.approval.status !== "approved"
      || !statePlan.approval.approvalId
    )
  ) {
    findings.push(
      finding(
        "PLAN_STATE_APPROVAL_PENDING",
        "/documents/statePlan/approval",
        "validated bundles require an approved state plan",
      ),
    );
  }

  requireUnique(
    findings,
    ownerLedger.owners,
    "ownerId",
    "/documents/ownerLedger/owners",
    "PLAN_OWNER_DUPLICATE",
  );
  const visualOwners = ownerLedger.owners.filter(
    (owner) => owner.domain === "visual-composition",
  );
  for (const state of statePlan.compositionStates) {
    const matches = visualOwners.filter(
      (owner) => owner.subjectRef === state.stateInstanceId
        && safeRangesEqual(owner.range, state.range),
    );
    if (matches.length !== 1) {
      findings.push(
        finding(
          "PLAN_VISUAL_OWNER_MISMATCH",
          "/documents/ownerLedger/owners",
          "every composition state requires one exact visual owner",
          {subjectRef: state.stateInstanceId},
        ),
      );
    }
  }
  for (const owner of visualOwners) {
    if (!statePlan.compositionStates.some(
      (state) => state.stateInstanceId === owner.subjectRef,
    )) {
      findings.push(
        finding(
          "PLAN_VISUAL_OWNER_ORPHAN",
          "/documents/ownerLedger/owners",
          "visual owner does not reference a composition state",
          {subjectRef: owner.subjectRef},
        ),
      );
    }
  }

  const privacyOwners = ownerLedger.owners.filter(
    (owner) => owner.domain === "privacy",
  );
  for (const overlay of statePlan.privacyOverlays) {
    const matches = privacyOwners.filter(
      (owner) => owner.subjectRef === overlay.privacyInstanceId
        && safeRangesEqual(owner.range, overlay.range),
    );
    if (matches.length !== 1) {
      findings.push(
        finding(
          "PLAN_PRIVACY_OWNER_MISMATCH",
          "/documents/ownerLedger/owners",
          "every privacy overlay requires one exact privacy owner",
          {subjectRef: overlay.privacyInstanceId},
        ),
      );
    }
  }
  for (const owner of privacyOwners) {
    if (!statePlan.privacyOverlays.some(
      (overlay) => overlay.privacyInstanceId === owner.subjectRef,
    )) {
      findings.push(
        finding(
          "PLAN_PRIVACY_OWNER_ORPHAN",
          "/documents/ownerLedger/owners",
          "privacy owner does not reference a privacy overlay",
          {subjectRef: owner.subjectRef},
        ),
      );
    }
  }
}

function auditCaptions(
  findings,
  transcript,
  captionPlan,
  evidenceById,
  timelineRate,
) {
  const wordIds = new Set(transcript.words.map((word) => word.wordId));
  requireUnique(
    findings,
    captionPlan.pages,
    "pageId",
    "/documents/captionPlan/pages",
    "PLAN_CAPTION_DUPLICATE",
  );
  let previousEnd = null;
  captionPlan.pages.forEach((page, index) => {
    const pointer = `/documents/captionPlan/pages/${index}`;
    if (auditRange(
      findings,
      page.range,
      "timeline",
      timelineRate,
      `${pointer}/range`,
    )) {
      if (previousEnd !== null && page.range.start < previousEnd) {
        findings.push(
          finding(
            "PLAN_CAPTION_OVERLAP",
            `${pointer}/range/start`,
            "caption pages cannot overlap",
          ),
        );
      }
      previousEnd = Math.max(previousEnd ?? 0, page.range.end);
    }
    for (const wordId of page.sourceWordIds) {
      if (!wordIds.has(wordId)) {
        findings.push(
          finding(
            "PLAN_CAPTION_WORD_UNKNOWN",
            `${pointer}/sourceWordIds`,
            "caption page references an unknown word",
          ),
        );
      }
    }
    if (page.sourceText !== page.displayText) {
      findings.push(
        finding(
          "PLAN_CAPTION_CORRECTION_UNMODELED",
          `${pointer}/displayText`,
          "caption corrections require a future explicit correction record",
        ),
      );
    }
    for (const evidenceRef of page.evidenceRefs) {
      if (!evidenceById.has(evidenceRef)) {
        findings.push(
          finding(
            "PLAN_EVIDENCE_UNKNOWN",
            `${pointer}/evidenceRefs`,
            "caption page references unknown evidence",
          ),
        );
      }
    }
  });
}

function auditCrossDocument(findings, bundle, documents, root) {
  const {
    project,
    transcript,
    editPlan,
    statePlan,
    ownerLedger,
    captionPlan,
    evidenceManifest,
  } = documents;
  for (const [name, document] of Object.entries(documents)) {
    requireEqual(
      findings,
      document.projectId,
      bundle.projectId,
      "PLAN_PROJECT_ID_MISMATCH",
      `/documents/${name}/projectId`,
      "plan document belongs to a different project",
    );
  }
  requireEqual(
    findings,
    project.runId,
    bundle.runId,
    "PLAN_RUN_ID_MISMATCH",
    "/documents/project/runId",
    "project run differs from the bundle",
  );
  requireEqual(
    findings,
    evidenceManifest.runId,
    bundle.runId,
    "PLAN_RUN_ID_MISMATCH",
    "/documents/evidenceManifest/runId",
    "evidence run differs from the bundle",
  );
  for (const [name, document] of Object.entries({
    statePlan,
    ownerLedger,
    captionPlan,
  })) {
    requireEqual(
      findings,
      document.timelineId,
      project.timeline.timelineId,
      "PLAN_TIMELINE_ID_MISMATCH",
      `/documents/${name}/timelineId`,
      "plan document targets a different timeline",
    );
    requireEqual(
      findings,
      document.timelineRevision,
      project.timeline.revision,
      "PLAN_TIMELINE_REVISION_MISMATCH",
      `/documents/${name}/timelineRevision`,
      "plan document targets a different timeline revision",
    );
  }
  requireEqual(
    findings,
    evidenceManifest.timelineRevision,
    project.timeline.revision,
    "PLAN_TIMELINE_REVISION_MISMATCH",
    "/documents/evidenceManifest/timelineRevision",
    "evidence manifest targets a different timeline revision",
  );
  requireEqual(
    findings,
    captionPlan.transcriptId,
    transcript.transcriptId,
    "PLAN_CAPTION_TRANSCRIPT_ID",
    "/documents/captionPlan/transcriptId",
    "caption plan targets a different transcript",
  );
  requireEqual(
    findings,
    captionPlan.transcriptRevision,
    transcript.revision,
    "PLAN_CAPTION_TRANSCRIPT_REVISION",
    "/documents/captionPlan/transcriptRevision",
    "caption plan targets a different transcript revision",
  );

  const policy = readJson(
    path.join(root, "rules/policy.json"),
    "PLAN_POLICY_READ_FAILED",
  );
  const registry = readJson(
    path.join(root, "rules/registry.json"),
    "PLAN_REGISTRY_READ_FAILED",
  );
  requireEqual(
    findings,
    project.contracts.policyVersion,
    policy.version,
    "PLAN_POLICY_VERSION_MISMATCH",
    "/documents/project/contracts/policyVersion",
    "project policy version differs from the repository",
  );
  requireEqual(
    findings,
    project.contracts.registryVersion,
    registry.registryVersion,
    "PLAN_REGISTRY_VERSION_MISMATCH",
    "/documents/project/contracts/registryVersion",
    "project registry version differs from the repository",
  );

  requireUnique(
    findings,
    evidenceManifest.artifacts,
    "evidenceId",
    "/documents/evidenceManifest/artifacts",
    "PLAN_EVIDENCE_DUPLICATE",
  );
  const evidenceById = new Map(
    evidenceManifest.artifacts.map(
      (artifact) => [artifact.evidenceId, artifact],
    ),
  );
  auditProject(findings, project);
  auditTranscript(findings, project, transcript, evidenceById);
  auditEditPlan(findings, transcript, editPlan, bundle.status);
  auditStateAndOwners(
    findings,
    project,
    statePlan,
    ownerLedger,
    bundle.status,
  );
  auditCaptions(
    findings,
    transcript,
    captionPlan,
    evidenceById,
    project.timeline.duration.rate,
  );
}

export function validatePlanBundle({
  root,
  bundlePath = "bundle.json",
} = {}) {
  let canonicalRoot;
  try {
    canonicalRoot = fs.realpathSync(path.resolve(root));
  } catch (cause) {
    throw new PlanBundleError(
      "PLAN_ROOT_UNREADABLE",
      "repository root is not readable",
      {cause},
    );
  }
  const bundleInput = inspectFile(canonicalRoot, canonicalRoot, bundlePath);
  if (!bundleInput.ok) {
    throw new PlanBundleError(
      "PLAN_BUNDLE_UNREADABLE",
      "plan bundle is missing, unsafe, or unreadable",
    );
  }
  const validators = createValidators(canonicalRoot);
  const bundle = readJson(
    bundleInput.absolutePath,
    "PLAN_BUNDLE_INVALID_JSON",
  );
  const findings = schemaFindings(validators.bundle, bundle, "bundle");
  if (findings.length > 0) {
    return {
      status: "failed",
      summary: {documents: 0, errors: findings.length},
      findings,
    };
  }

  const bundleDirectory = path.dirname(bundleInput.absolutePath);
  const documents = {};
  const seenPaths = new Set();
  for (const [name, relativePath] of Object.entries(bundle.documents)) {
    if (seenPaths.has(relativePath)) {
      findings.push(
        finding(
          "PLAN_DOCUMENT_PATH_DUPLICATE",
          `/documents/${name}`,
          "bundle documents must use distinct files",
        ),
      );
      continue;
    }
    seenPaths.add(relativePath);
    const input = inspectFile(canonicalRoot, bundleDirectory, relativePath);
    if (!input.ok) {
      findings.push(
        finding(
          input.code,
          `/documents/${name}`,
          "plan document is missing, unsafe, or unreadable",
          {document: name},
        ),
      );
      continue;
    }
    try {
      documents[name] = readJson(
        input.absolutePath,
        "PLAN_DOCUMENT_INVALID_JSON",
      );
      findings.push(
        ...schemaFindings(validators[name], documents[name], name),
      );
    } catch {
      findings.push(
        finding(
          "PLAN_DOCUMENT_INVALID_JSON",
          `/documents/${name}`,
          "plan document is invalid JSON",
          {document: name},
        ),
      );
    }
  }
  if (
    Object.keys(documents).length === Object.keys(bundle.documents).length
    && findings.length === 0
  ) {
    auditCrossDocument(findings, bundle, documents, canonicalRoot);
  }
  return {
    status: findings.length === 0 ? "passed" : "failed",
    bundleId: bundle.bundleId,
    projectId: bundle.projectId,
    runId: bundle.runId,
    summary: {
      documents: Object.keys(documents).length,
      errors: findings.length,
    },
    findings,
  };
}
