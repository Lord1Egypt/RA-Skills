import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import {
  PROFILE_RESOLVED_SCHEMA_ID,
  PROFILE_SOURCE_SCHEMA_ID,
} from "./profile-resolver-ids.mjs";
import {
  validateProfileResolved,
  validateProfileSource,
} from "./profile-schema-validator.mjs";

export {
  PROFILE_RESOLVED_SCHEMA_ID,
  PROFILE_SOURCE_SCHEMA_ID,
} from "./profile-resolver-ids.mjs";

export const DEFAULT_PROFILE_PATH_POINTERS = Object.freeze([
  "/terminologyFile",
]);
export const PROFILE_RESOLUTION_DIAGNOSTICS = Symbol.for(
  "majia-chatcut-koubo.profile-resolution-diagnostics",
);

const UNSAFE_KEYS = new Set(["__proto__", "constructor", "prototype"]);
const CANONICAL_STATUSES = new Set([
  "untested-template",
  "validated",
  "deprecated",
]);
const NON_INHERITABLE_FIELDS = new Set(["status", "provenance"]);
const DELETION_TOMBSTONES = new Set(["/terminology"]);
const TRUST_MODES = new Set(["strict", "migration"]);

export class ProfileResolutionError extends Error {
  constructor(code, message, details = {}, options = {}) {
    super(message, options);
    this.name = "ProfileResolutionError";
    this.code = code;
    this.details = details;
  }
}

function resolutionError(code, message, details, cause) {
  return new ProfileResolutionError(
    code,
    message,
    details,
    cause ? {cause} : undefined,
  );
}

function hasOwn(value, key) {
  return Object.prototype.hasOwnProperty.call(value, key);
}

function isPlainObject(value) {
  if (value === null || typeof value !== "object" || Array.isArray(value)) {
    return false;
  }
  const prototype = Object.getPrototypeOf(value);
  return prototype === Object.prototype || prototype === null;
}

function escapePointerSegment(segment) {
  return String(segment).replaceAll("~", "~0").replaceAll("/", "~1");
}

function joinPointer(parent, segment) {
  return `${parent}/${escapePointerSegment(segment)}`;
}

function assertSafeValue(value, pointer = "") {
  if (Array.isArray(value)) {
    value.forEach((item, index) => assertSafeValue(item, joinPointer(pointer, index)));
    return;
  }
  if (value === null || typeof value !== "object") return;
  if (!isPlainObject(value)) {
    throw resolutionError(
      "PROFILE_NON_PLAIN_OBJECT",
      `profile value at ${pointer || "/"} must be a plain JSON object`,
      {pointer: pointer || "/"},
    );
  }
  for (const key of Object.keys(value)) {
    const childPointer = joinPointer(pointer, key);
    if (UNSAFE_KEYS.has(key)) {
      throw resolutionError(
        "PROFILE_UNSAFE_KEY",
        `unsafe profile key rejected at ${childPointer}`,
        {pointer: childPointer, key},
      );
    }
    assertSafeValue(value[key], childPointer);
  }
}

function cloneJsonValue(value) {
  if (Array.isArray(value)) return value.map(cloneJsonValue);
  if (!isPlainObject(value)) return value;
  const clone = {};
  for (const [key, child] of Object.entries(value)) {
    clone[key] = cloneJsonValue(child);
  }
  return clone;
}

function resolveFileReference(reference, declaringDirectory, pointer) {
  if (typeof reference !== "string" || reference.length === 0) {
    throw resolutionError(
      "PROFILE_INVALID_PATH_REFERENCE",
      `profile path at ${pointer} must be a non-empty string`,
      {pointer},
    );
  }
  if (path.isAbsolute(reference)) return path.normalize(reference);
  if (reference.startsWith("file:")) {
    try {
      return path.normalize(fileURLToPath(reference));
    } catch (cause) {
      throw resolutionError(
        "PROFILE_INVALID_PATH_REFERENCE",
        `profile path at ${pointer} is not a valid file URL`,
        {pointer},
        cause,
      );
    }
  }
  if (/^[A-Za-z][A-Za-z\d+.-]*:/.test(reference)) {
    throw resolutionError(
      "PROFILE_UNSUPPORTED_PATH_URI",
      `profile path at ${pointer} must be a local file reference`,
      {pointer},
    );
  }
  return path.resolve(declaringDirectory, reference);
}

function normalizeLayerValue(
  value,
  pointer,
  declaringDirectory,
  pathPointers,
  normalizedPointers,
  allowedRoot,
) {
  if (pathPointers.has(pointer)) {
    const normalized = canonicalizePotentialPath(
      resolveFileReference(value, declaringDirectory, pointer),
    );
    if (!pathIsInside(allowedRoot, normalized)) {
      throw resolutionError(
        "PROFILE_REFERENCE_OUTSIDE_ROOT",
        `profile file reference at ${pointer} leaves the configured root`,
        {pointer},
      );
    }
    if (normalized !== value) normalizedPointers.add(pointer);
    return normalized;
  }
  if (Array.isArray(value)) {
    return value.map((child, index) =>
      normalizeLayerValue(
        child,
        joinPointer(pointer, index),
        declaringDirectory,
        pathPointers,
        normalizedPointers,
        allowedRoot,
      ));
  }
  if (!isPlainObject(value)) return value;
  const normalized = {};
  for (const [key, child] of Object.entries(value)) {
    normalized[key] = normalizeLayerValue(
      child,
      joinPointer(pointer, key),
      declaringDirectory,
      pathPointers,
      normalizedPointers,
      allowedRoot,
    );
  }
  return normalized;
}

function readProfileJson(profileFile) {
  let text;
  try {
    text = fs.readFileSync(profileFile, "utf8");
  } catch (cause) {
    throw resolutionError(
      "PROFILE_READ_ERROR",
      "cannot read profile source",
      {file: profileFile},
      cause,
    );
  }
  let value;
  try {
    value = JSON.parse(text);
  } catch (cause) {
    throw resolutionError(
      "PROFILE_PARSE_ERROR",
      "profile source is not valid JSON",
      {file: profileFile},
      cause,
    );
  }
  if (!isPlainObject(value)) {
    throw resolutionError(
      "PROFILE_ROOT_TYPE",
      "profile source root must be a JSON object",
      {file: profileFile},
    );
  }
  assertSafeValue(value);
  return value;
}

function canonicalProfileFile(profileFile) {
  const absolute = path.resolve(profileFile);
  try {
    return fs.realpathSync(absolute);
  } catch (cause) {
    throw resolutionError(
      "PROFILE_READ_ERROR",
      "cannot resolve profile source",
      {file: absolute},
      cause,
    );
  }
}

function canonicalizePotentialPath(candidate) {
  const absolute = path.resolve(candidate);
  const missingSegments = [];
  let existing = absolute;
  while (!fs.existsSync(existing)) {
    const parent = path.dirname(existing);
    if (parent === existing) return absolute;
    missingSegments.unshift(path.basename(existing));
    existing = parent;
  }
  try {
    return path.join(fs.realpathSync(existing), ...missingSegments);
  } catch {
    return absolute;
  }
}

function resolveExtendsReference(reference, declaringDirectory) {
  if (typeof reference !== "string" || reference.trim().length === 0) {
    throw resolutionError(
      "PROFILE_INVALID_EXTENDS",
      "profile extends must be a non-empty local file reference",
      {},
    );
  }
  return resolveFileReference(reference, declaringDirectory, "/extends");
}

function loadProfileLayers(entryFile, maxDepth, allowedRoot) {
  const layers = [];
  const active = [];

  function visit(candidate) {
    if (active.length >= maxDepth) {
      throw resolutionError(
        "PROFILE_MAX_DEPTH",
        `profile inheritance exceeds the maximum depth of ${maxDepth}`,
        {maxDepth},
      );
    }
    const file = canonicalProfileFile(candidate);
    if (!pathIsInside(allowedRoot, file)) {
      throw resolutionError(
        "PROFILE_EXTENDS_OUTSIDE_ROOT",
        "profile inheritance leaves the configured profile root",
        {},
      );
    }
    const cycleIndex = active.indexOf(file);
    if (cycleIndex >= 0) {
      throw resolutionError(
        "PROFILE_INHERITANCE_CYCLE",
        "profile inheritance cycle detected",
        {files: [...active.slice(cycleIndex), file]},
      );
    }
    active.push(file);
    const value = readProfileJson(file);
    const sourceContract = validateProfileSource(value);
    if (!sourceContract.valid) {
      throw resolutionError(
        "PROFILE_SOURCE_SCHEMA_INVALID",
        "profile source does not satisfy the source contract",
        {errors: sourceContract.errors},
      );
    }
    if (hasOwn(value, "extends")) {
      const parent = resolveExtendsReference(value.extends, path.dirname(file));
      visit(parent);
    }
    layers.push({file, value});
    active.pop();
  }

  visit(entryFile);
  return layers;
}

function isNonBlankString(value) {
  return typeof value === "string" && value.trim().length > 0;
}

function revisionMapIsComplete(value) {
  return isPlainObject(value)
    && Object.keys(value).length > 0
    && Object.entries(value).every(
      ([key, revision]) => isNonBlankString(key) && isNonBlankString(revision),
    );
}

function assertValidatedProvenance(provenance) {
  if (provenance.validatedTimelineIds.length === 0) {
    throw resolutionError(
      "PROFILE_VALIDATED_TIMELINE_REQUIRED",
      "validated leaf provenance requires at least one timeline",
      {pointer: "/provenance/validatedTimelineIds"},
    );
  }
  const trustIdentifiers = [
    provenance.projectId,
    ...provenance.validatedTimelineIds,
    ...Object.entries(provenance.validatedTimelineRevisions ?? {}).flat(),
    ...Object.entries(provenance.validatedSourceRevisions ?? {}).flat(),
  ];
  if (trustIdentifiers.some((value) => /REPLACE|your-/iu.test(String(value)))) {
    throw resolutionError(
      "PROFILE_PLACEHOLDER_PROVENANCE",
      "validated leaf provenance cannot contain placeholder identifiers",
      {pointer: "/provenance"},
    );
  }
  if (!revisionMapIsComplete(provenance.validatedTimelineRevisions)) {
    throw resolutionError(
      "PROFILE_TIMELINE_REVISIONS_REQUIRED",
      "validated leaf provenance requires timeline revision evidence",
      {pointer: "/provenance/validatedTimelineRevisions"},
    );
  }
  for (const timelineId of provenance.validatedTimelineIds) {
    if (!hasOwn(provenance.validatedTimelineRevisions, timelineId)) {
      throw resolutionError(
        "PROFILE_TIMELINE_REVISION_COVERAGE",
        "validated timeline revision evidence is incomplete",
        {pointer: "/provenance/validatedTimelineRevisions"},
      );
    }
  }
  if (!revisionMapIsComplete(provenance.validatedSourceRevisions)) {
    throw resolutionError(
      "PROFILE_SOURCE_REVISIONS_REQUIRED",
      "validated leaf provenance requires source revision evidence",
      {pointer: "/provenance/validatedSourceRevisions"},
    );
  }
}

function evaluateLeafTrust(leaf, trustMode, warnings) {
  const status = leaf.value.status;
  if (!hasOwn(leaf.value, "status") || !CANONICAL_STATUSES.has(status)) {
    if (trustMode === "strict") {
      const missing = !hasOwn(leaf.value, "status");
      throw resolutionError(
        missing
          ? "PROFILE_NON_INHERITABLE_REQUIRED"
          : "PROFILE_INVALID_LEAF_STATUS",
        missing
          ? "leaf profile must declare its own status"
          : "leaf profile status must use a canonical resolved status",
        {pointer: "/status"},
      );
    }
    warnings.push({
      code: "PROFILE_MIGRATION_STATUS_DOWNGRADED",
      pointer: "/status",
      message: "legacy leaf status was downgraded to untested-template",
    });
  }

  const provenance = leaf.value.provenance;
  if (!hasOwn(leaf.value, "provenance") || provenance === null) {
    if (trustMode === "strict") {
      throw resolutionError(
        "PROFILE_NON_INHERITABLE_REQUIRED",
        "leaf profile must declare its own provenance",
        {pointer: "/provenance"},
      );
    }
    warnings.push({
      code: "PROFILE_MIGRATION_LEAF_PROVENANCE_MISSING",
      pointer: "/provenance",
      message: "legacy leaf has no own provenance; parent trust was discarded",
    });
    warnings.push({
      code: "PROFILE_MIGRATION_STATUS_DOWNGRADED",
      pointer: "/status",
      message: "profile trust was downgraded to untested-template",
    });
    return {trusted: false, effectiveStatus: "untested-template"};
  }

  if (
    !isPlainObject(provenance)
    || !isNonBlankString(provenance.projectId)
    || !Array.isArray(provenance.validatedTimelineIds)
    || provenance.validatedTimelineIds.some(
      (timelineId) => !isNonBlankString(timelineId),
    )
  ) {
    throw resolutionError(
      "PROFILE_INCOMPLETE_LEAF_PROVENANCE",
      "leaf profile provenance must contain projectId and validatedTimelineIds",
      {pointer: "/provenance"},
    );
  }

  if (status === "validated") {
    if (trustMode === "strict") {
      assertValidatedProvenance(provenance);
    } else {
      try {
        assertValidatedProvenance(provenance);
      } catch (error) {
        warnings.push({
          code: "PROFILE_MIGRATION_REVISION_EVIDENCE_INCOMPLETE",
          pointer: error.details?.pointer ?? "/provenance",
          message: "profile revision evidence must be completed before strict release",
        });
      }
    }
  }
  return {
    trusted: CANONICAL_STATUSES.has(status),
    effectiveStatus: CANONICAL_STATUSES.has(status)
      ? status
      : "untested-template",
  };
}

function pathIsInside(root, candidate) {
  const relative = path.relative(root, candidate);
  return relative === ""
    || (!relative.startsWith(`..${path.sep}`)
      && relative !== ".."
      && !path.isAbsolute(relative));
}

function portablePath(value) {
  return value.split(path.sep).join("/");
}

function createFilePresenter({entryFile, traceRoot, tracePathMode}) {
  const root = canonicalizePotentialPath(
    traceRoot || path.dirname(entryFile),
  );
  const aliases = new Map();
  let nextAlias = 1;

  return (file) => {
    if (file === "<resolver>") return file;
    if (tracePathMode === "absolute") return file;
    if (pathIsInside(root, file)) {
      const relative = path.relative(root, file);
      return portablePath(relative || path.basename(file));
    }
    if (!aliases.has(file)) {
      aliases.set(file, `<external:${nextAlias}>`);
      nextAlias += 1;
    }
    return aliases.get(file);
  };
}

function deleteSourceSubtree(sources, pointer) {
  for (const sourcePointer of Object.keys(sources)) {
    if (
      sourcePointer === pointer
      || sourcePointer.startsWith(`${pointer}/`)
    ) {
      delete sources[sourcePointer];
    }
  }
}

function recordSourceTree(sources, value, pointer, source) {
  sources[pointer] = source;
  if (Array.isArray(value)) {
    value.forEach((child, index) =>
      recordSourceTree(sources, child, joinPointer(pointer, index), source));
    return;
  }
  if (!isPlainObject(value)) return;
  for (const [key, child] of Object.entries(value)) {
    recordSourceTree(sources, child, joinPointer(pointer, key), source);
  }
}

function makeTraceRecorder(mergeTrace) {
  return (event) => {
    mergeTrace.push({
      sequence: mergeTrace.length + 1,
      ...event,
    });
  };
}

function applyLayer({
  target,
  overlay,
  layer,
  layerIndex,
  sourceFile,
  sources,
  trace,
  normalizedPointers,
}) {
  function sourceFor(pointer) {
    return {
      file: sourceFile,
      layer: layerIndex,
      normalizedPath: normalizedPointers.has(pointer),
    };
  }

  function applyObject(targetObject, overlayObject, parentPointer) {
    for (const [key, value] of Object.entries(overlayObject)) {
      if (key === "extends" || key === "$schema") continue;
      const pointer = joinPointer(parentPointer, key);
      applyValue(targetObject, key, value, pointer);
    }
  }

  function applyValue(targetObject, key, value, pointer) {
    const existed = hasOwn(targetObject, key);
    const previousSource = sources[pointer]?.file;
    const source = sourceFor(pointer);

    if (value === null && DELETION_TOMBSTONES.has(pointer)) {
      deleteSourceSubtree(sources, pointer);
      delete targetObject[key];
      trace({
        operation: "delete",
        path: pointer,
        sourceFile,
        layer: layerIndex,
        ...(previousSource ? {previousSourceFile: previousSource} : {}),
      });
      return;
    }

    if (isPlainObject(value)) {
      if (!existed || !isPlainObject(targetObject[key])) {
        deleteSourceSubtree(sources, pointer);
        targetObject[key] = {};
        trace({
          operation: existed ? "replace-with-object" : "set-object",
          path: pointer,
          sourceFile,
          layer: layerIndex,
          ...(previousSource ? {previousSourceFile: previousSource} : {}),
        });
      } else {
        trace({
          operation: "merge-object",
          path: pointer,
          sourceFile,
          layer: layerIndex,
          ...(previousSource ? {previousSourceFile: previousSource} : {}),
        });
      }
      sources[pointer] = source;
      applyObject(targetObject[key], value, pointer);
      return;
    }

    deleteSourceSubtree(sources, pointer);
    targetObject[key] = cloneJsonValue(value);
    recordSourceTree(sources, targetObject[key], pointer, source);
    trace({
      operation: Array.isArray(value)
        ? (existed ? "replace-array" : "set-array")
        : (existed ? "override" : "set"),
      path: pointer,
      sourceFile,
      layer: layerIndex,
      ...(previousSource ? {previousSourceFile: previousSource} : {}),
      ...(normalizedPointers.has(pointer) ? {normalizedPath: true} : {}),
    });
  }

  applyObject(target, overlay, "");
}

/**
 * Resolve a source profile synchronously.
 *
 * Arrays use replace semantics. Plain objects are merged recursively and
 * scalars are overridden by the child layer. `status` and `provenance` are
 * never inherited: the leaf must declare both itself.
 */
export function resolveProfile(profileFile, options = {}) {
  const entryFile = canonicalProfileFile(profileFile);
  const trustMode = options.trustMode ?? "strict";
  if (!TRUST_MODES.has(trustMode)) {
    throw new TypeError("trustMode must be strict or migration");
  }
  const maxDepth = options.maxDepth ?? 64;
  if (!Number.isInteger(maxDepth) || maxDepth < 1) {
    throw new TypeError("maxDepth must be a positive integer");
  }
  const pathPointers = new Set(
    options.pathPointers ?? DEFAULT_PROFILE_PATH_POINTERS,
  );
  const tracePathMode = options.tracePathMode ?? "relative";
  if (!["relative", "absolute"].includes(tracePathMode)) {
    throw new TypeError("tracePathMode must be relative or absolute");
  }

  const entryDirectory = path.dirname(entryFile);
  const inferredRoot = ["profile", "profiles"].includes(
    path.basename(entryDirectory),
  )
    ? path.dirname(entryDirectory)
    : entryDirectory;
  const allowedRoot = canonicalizePotentialPath(
    options.allowedRoot ?? inferredRoot,
  );
  if (!pathIsInside(allowedRoot, entryFile)) {
    throw resolutionError(
      "PROFILE_ENTRY_OUTSIDE_ROOT",
      "profile entry is outside the configured profile root",
      {},
    );
  }

  const layers = loadProfileLayers(entryFile, maxDepth, allowedRoot);
  const leaf = layers.at(-1);
  const warnings = [];
  const leafTrust = evaluateLeafTrust(leaf, trustMode, warnings);
  const presentFile = createFilePresenter({
    entryFile,
    traceRoot: options.traceRoot,
    tracePathMode,
  });
  const resolved = {};
  const sources = {};
  const mergeTrace = [];
  const trace = makeTraceRecorder(mergeTrace);

  layers.forEach((layer, layerIndex) => {
    const isLeaf = layerIndex === layers.length - 1;
    const sourceFile = presentFile(layer.file);
    const normalizedPointers = new Set();
    const normalized = normalizeLayerValue(
      layer.value,
      "",
      path.dirname(layer.file),
      pathPointers,
      normalizedPointers,
      allowedRoot,
    );

    for (const field of NON_INHERITABLE_FIELDS) {
      if (!isLeaf && hasOwn(normalized, field)) {
        trace({
          operation: "discard-non-inheritable",
          path: `/${field}`,
          sourceFile,
          layer: layerIndex,
        });
        delete normalized[field];
      }
    }
    if (
      isLeaf
      && hasOwn(normalized, "provenance")
      && normalized.provenance === null
    ) {
      trace({
        operation: "discard-non-inheritable",
        path: "/provenance",
        sourceFile,
        layer: layerIndex,
      });
      delete normalized.provenance;
    }

    applyLayer({
      target: resolved,
      overlay: normalized,
      layer,
      layerIndex,
      sourceFile,
      sources,
      trace,
      normalizedPointers,
    });
  });

  if (resolved.status !== leafTrust.effectiveStatus) {
    const previousSourceFile = sources["/status"]?.file;
    resolved.status = leafTrust.effectiveStatus;
    sources["/status"] = {
      file: "<resolver>",
      layer: layers.length,
      normalizedPath: false,
    };
    trace({
      operation: "downgrade-trust",
      path: "/status",
      sourceFile: "<resolver>",
      layer: layers.length,
      ...(previousSourceFile ? {previousSourceFile} : {}),
    });
  }
  if (!leafTrust.trusted) {
    delete resolved.provenance;
    deleteSourceSubtree(sources, "/provenance");
  }

  resolved.$schema = PROFILE_RESOLVED_SCHEMA_ID;
  sources["/$schema"] = {
    file: "<resolver>",
    layer: layers.length,
    normalizedPath: false,
  };
  trace({
    operation: "set-resolved-schema",
    path: "/$schema",
    sourceFile: "<resolver>",
    layer: layers.length,
  });

  const resolvedContract = validateProfileResolved(resolved);
  let contractStatus = "valid";
  if (!resolvedContract.valid) {
    const migrationCompatible = trustMode === "migration"
      && resolvedContract.errors.every((error) => (
        (error.keyword === "required"
          && (
            error.missingProperty === "provenance"
            || error.missingProperty === "validatedTimelineRevisions"
            || error.missingProperty === "validatedSourceRevisions"
          ))
        || error.pointer.startsWith("/provenance")
        || (error.keyword === "if" && error.pointer === "/")
      ));
    if (!migrationCompatible) {
      throw resolutionError(
        "PROFILE_RESOLVED_SCHEMA_INVALID",
        "merged profile does not satisfy the resolved contract",
        {errors: resolvedContract.errors},
      );
    }
    contractStatus = "migration-incomplete";
    warnings.push({
      code: "PROFILE_MIGRATION_RESOLVED_CONTRACT_INCOMPLETE",
      pointer: "/provenance",
      message: "legacy profile is usable for migration audit but is not a release-ready resolved contract",
    });
  }

  return {
    resolved,
    sources,
    mergeTrace,
    trustMode,
    contractStatus,
    warnings,
    entryFile: presentFile(entryFile),
    configRoot: presentFile(allowedRoot),
    files: layers.map((layer, index) => ({
      file: presentFile(layer.file),
      layer: index,
      role: index === layers.length - 1 ? "leaf" : "parent",
    })),
  };
}

/**
 * Compatibility value-only API for the existing caption CLI.
 */
export function loadProfile(profileFile, options = {}) {
  const resolution = resolveProfile(profileFile, {
    ...options,
    trustMode: options.trustMode ?? "migration",
  });
  Object.defineProperty(
    resolution.resolved,
    PROFILE_RESOLUTION_DIAGNOSTICS,
    {
      configurable: false,
      enumerable: false,
      writable: false,
      value: {
        trustMode: resolution.trustMode,
        contractStatus: resolution.contractStatus,
        warnings: cloneJsonValue(resolution.warnings),
      },
    },
  );
  return resolution.resolved;
}

export function getProfileDiagnostics(profile) {
  return profile?.[PROFILE_RESOLUTION_DIAGNOSTICS] ?? {
    trustMode: "unknown",
    contractStatus: "unknown",
    warnings: [],
  };
}

function sanitizeAbsolutePath(
  value,
  baseDirectory,
  externalPathMode,
  aliases,
  portableRoot,
) {
  if (!path.isAbsolute(value)) return value;
  const relative = path.relative(baseDirectory, value);
  if (externalPathMode === "relative") {
    if (!portableRoot || !pathIsInside(portableRoot, value)) {
      throw resolutionError(
        "PROFILE_EXTERNAL_PATH_NOT_PORTABLE",
        "resolved profile contains a path outside its portable root",
        {},
      );
    }
    return portablePath(relative || path.basename(value));
  }
  if (pathIsInside(baseDirectory, value)) {
    return portablePath(relative || path.basename(value));
  }
  if (externalPathMode === "absolute") return value;
  if (!aliases.has(value)) {
    aliases.set(value, `<external-path:${aliases.size + 1}>`);
  }
  return aliases.get(value);
}

function transformPointers(value, pointer, pathPointers, transform) {
  if (pathPointers.has(pointer)) return transform(value);
  if (Array.isArray(value)) {
    return value.map((child, index) =>
      transformPointers(
        child,
        joinPointer(pointer, index),
        pathPointers,
        transform,
      ));
  }
  if (!isPlainObject(value)) return value;
  const transformed = {};
  for (const [key, child] of Object.entries(value)) {
    transformed[key] = transformPointers(
      child,
      joinPointer(pointer, key),
      pathPointers,
      transform,
    );
  }
  return transformed;
}

/**
 * Produce a report-safe copy. By default, absolute references outside
 * `baseDirectory` are replaced with stable anonymous labels.
 *
 * Use `externalPathMode: "relative"` with `portableRoot` when writing a
 * portable resolved profile. Only declared path fields are rebased; semantic
 * strings such as route patterns remain untouched.
 */
export function toSerializableProfileResolution(resolution, options = {}) {
  const baseDirectory = canonicalizePotentialPath(
    options.baseDirectory ?? process.cwd(),
  );
  const externalPathMode = options.externalPathMode ?? "redact";
  if (!["redact", "relative", "absolute"].includes(externalPathMode)) {
    throw new TypeError(
      "externalPathMode must be redact, relative, or absolute",
    );
  }
  const portableRoot = options.portableRoot
    ? canonicalizePotentialPath(options.portableRoot)
    : undefined;
  const pathPointers = new Set(
    options.pathPointers ?? DEFAULT_PROFILE_PATH_POINTERS,
  );
  const aliases = new Map();
  const sanitize = (value) =>
    typeof value === "string"
      ? sanitizeAbsolutePath(
        value,
        baseDirectory,
        externalPathMode,
        aliases,
        portableRoot,
      )
      : value;
  const serialized = cloneJsonValue(resolution);
  serialized.resolved = transformPointers(
    resolution.resolved,
    "",
    pathPointers,
    sanitize,
  );

  for (const source of Object.values(serialized.sources ?? {})) {
    if (typeof source.file === "string") source.file = sanitize(source.file);
  }
  for (const event of serialized.mergeTrace ?? []) {
    if (typeof event.sourceFile === "string") {
      event.sourceFile = sanitize(event.sourceFile);
    }
    if (typeof event.previousSourceFile === "string") {
      event.previousSourceFile = sanitize(event.previousSourceFile);
    }
  }
  if (typeof serialized.entryFile === "string") {
    serialized.entryFile = sanitize(serialized.entryFile);
  }
  if (typeof serialized.configRoot === "string") {
    serialized.configRoot = sanitize(serialized.configRoot);
  }
  for (const file of serialized.files ?? []) {
    if (typeof file.file === "string") file.file = sanitize(file.file);
  }
  return serialized;
}
