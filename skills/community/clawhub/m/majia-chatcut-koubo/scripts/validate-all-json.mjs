#!/usr/bin/env node

import { promises as fs } from "node:fs";
import path from "node:path";
import process from "node:process";
import { fileURLToPath, pathToFileURL } from "node:url";

import Ajv2020 from "ajv/dist/2020.js";
import addFormats from "ajv-formats";

export const EXIT_CODES = Object.freeze({
  OK: 0,
  VALIDATION_FAILED: 1,
  USAGE_OR_INTERNAL_ERROR: 2,
});

const SCRIPT_DIRECTORY = path.dirname(fileURLToPath(import.meta.url));
const DEFAULT_ROOT = path.resolve(SCRIPT_DIRECTORY, "..");
const DRAFT_2020_12 = "https://json-schema.org/draft/2020-12/schema";
const REPOSITORY_SCHEMA_ID_PREFIX =
  "https://github.com/maojiebc/majia-chatcut-koubo/";
const BASELINE_PATH = "fixtures/contract/schema-baseline.json";
const CASES_PATH = "fixtures/contract/cases.json";
const IGNORED_DIRECTORIES = new Set([
  ".git",
  "coverage",
  "dist",
  "node_modules",
]);

// These assets predate embedded $schema declarations. Keeping the mapping here
// makes their contract visible without modifying public asset payloads.
export const PATH_SCHEMA_MAP = Object.freeze({
  "assets/compositions.json": "schemas/compositions.schema.json",
  "assets/theme-kit/examples/demo-data.json":
    "schemas/theme-demo-data.schema.json",
  "assets/theme-kit/manifest.json": "schemas/theme-manifest.schema.json",
  "assets/theme-kit/package.json": "schemas/theme-package.schema.json",
  "assets/theme-kit/tokens/layouts.json":
    "schemas/theme-layouts.schema.json",
  "extensions/registry.json": "schemas/extension-registry.schema.json",
  "extensions/cuttips-kb/manifest.json":
    "schemas/extension-manifest.schema.json",
  "extensions/cuttips-kb/data/categories.json":
    "schemas/extension-array.schema.json",
  "extensions/cuttips-kb/data/knowledge-items.json":
    "schemas/extension-array.schema.json",
  "extensions/cuttips-kb/data/rules.json":
    "schemas/extension-array.schema.json",
  "extensions/cuttips-kb/data/sources.json":
    "schemas/extension-array.schema.json",
  "extensions/cuttips-kb/data/stats.json":
    "schemas/cuttips-stats.schema.json",
  "extensions/video-shotcraft/manifest.json":
    "schemas/extension-manifest.schema.json",
  "extensions/video-shotcraft/allowlist.json":
    "schemas/extension-array.schema.json",
});

const BASELINE_DOCUMENT_SCHEMA = {
  type: "object",
  additionalProperties: false,
  required: ["version", "entries"],
  properties: {
    $comment: { type: "string" },
    version: { const: 1 },
    entries: {
      type: "array",
      items: {
        type: "object",
        additionalProperties: false,
        required: ["path", "kind", "issue", "reason"],
        properties: {
          path: { type: "string", minLength: 1 },
          kind: { enum: ["unmapped", "validation-error"] },
          issue: { type: "string", minLength: 1 },
          reason: { type: "string", minLength: 1 },
          allowedErrorSignatures: {
            type: "array",
            minItems: 1,
            uniqueItems: true,
            items: { type: "string", minLength: 1 },
          },
        },
      },
    },
  },
};

const CASES_DOCUMENT_SCHEMA = {
  type: "object",
  additionalProperties: false,
  required: ["version", "cases"],
  properties: {
    $comment: { type: "string" },
    version: { const: 1 },
    cases: {
      type: "array",
      items: {
        type: "object",
        additionalProperties: false,
        required: ["path", "schema", "expect"],
        properties: {
          path: { type: "string", minLength: 1 },
          schema: { type: "string", minLength: 1 },
          expect: { enum: ["valid", "invalid"] },
          expectedErrorSignatures: {
            type: "array",
            minItems: 1,
            uniqueItems: true,
            items: { type: "string", minLength: 1 },
          },
        },
      },
    },
  },
};

const PACKAGE_JSON_SCHEMA = {
  type: "object",
  required: ["name", "version"],
  properties: {
    name: { type: "string", minLength: 1 },
    version: {
      type: "string",
      pattern: "^\\d+\\.\\d+\\.\\d+(?:-[0-9A-Za-z.-]+)?$",
    },
    private: { type: "boolean" },
    type: { enum: ["commonjs", "module"] },
    scripts: { type: "object" },
    engines: { type: "object" },
    dependencies: { type: "object" },
    devDependencies: { type: "object" },
  },
};

const PACKAGE_LOCK_SCHEMA = {
  type: "object",
  required: ["name", "version", "lockfileVersion", "packages"],
  properties: {
    name: { type: "string", minLength: 1 },
    version: { type: "string", minLength: 1 },
    lockfileVersion: { type: "integer", minimum: 1 },
    packages: { type: "object" },
  },
};

class UsageError extends Error {}

function createAjv() {
  const ajv = new Ajv2020({
    allErrors: true,
    allowUnionTypes: true,
    logger: false,
    strict: true,
    // Existing pre-v1.4 schemas contain required properties that are
    // intentionally open-ended. They remain meta-schema-valid and are tracked
    // separately from runtime data failures.
    strictRequired: false,
    validateFormats: true,
  });
  addFormats(ajv);
  return ajv;
}

function toPosixPath(value) {
  return value.split(path.sep).join("/");
}

function relativePath(root, absolutePath) {
  return toPosixPath(path.relative(root, absolutePath));
}

function isInsideRoot(root, absolutePath) {
  const relative = path.relative(root, absolutePath);
  return (
    relative !== "" &&
    relative !== ".." &&
    !relative.startsWith(`..${path.sep}`) &&
    !path.isAbsolute(relative)
  );
}

function normalizeConfiguredPath(value) {
  if (
    typeof value !== "string" ||
    value.length === 0 ||
    value.includes("\\") ||
    path.posix.isAbsolute(value)
  ) {
    return null;
  }

  const normalized = path.posix.normalize(value);
  if (
    normalized === "." ||
    normalized === ".." ||
    normalized.startsWith("../") ||
    !normalized.endsWith(".json")
  ) {
    return null;
  }
  return normalized;
}

function presentUnresolvedSchemaReference(reference) {
  if (
    typeof reference !== "string"
    || /^[A-Za-z][A-Za-z\d+.-]*:/u.test(reference)
  ) {
    return "<unresolved-schema-reference>";
  }
  const normalized = normalizeConfiguredPath(reference);
  return normalized ?? "<unresolved-schema-reference>";
}

async function collectJsonFiles(root) {
  const files = [];
  const symbolicLinks = [];

  async function visit(directory) {
    const entries = await fs.readdir(directory, { withFileTypes: true });
    entries.sort((left, right) => left.name.localeCompare(right.name));

    for (const entry of entries) {
      const absolutePath = path.join(directory, entry.name);
      if (entry.isSymbolicLink()) {
        symbolicLinks.push(absolutePath);
      } else if (entry.isDirectory()) {
        if (!IGNORED_DIRECTORIES.has(entry.name)) {
          await visit(absolutePath);
        }
      } else if (entry.isFile() && entry.name.endsWith(".json")) {
        files.push(absolutePath);
      }
    }
  }

  await visit(root);
  return {files, symbolicLinks};
}

async function readJsonFile(absolutePath) {
  try {
    const source = await fs.readFile(absolutePath, "utf8");
    return {
      data: JSON.parse(source.replace(/^\uFEFF/u, "")),
      error: null,
    };
  } catch (error) {
    return {
      data: null,
      error:
        error instanceof SyntaxError
          ? "invalid JSON: INVALID_JSON"
          : `cannot read file: ${error.code ?? "unknown error"}`,
    };
  }
}

function errorSignature(error) {
  let detail = "";
  if (error.keyword === "additionalProperties") {
    detail = `:${error.params.additionalProperty}`;
  } else if (error.keyword === "required") {
    detail = `:${error.params.missingProperty}`;
  } else if (error.keyword === "format") {
    detail = `:${error.params.format}`;
  }
  return `${error.keyword}@${error.instancePath || "/"}${detail}`;
}

function normalizeAjvErrors(errors, namespace = "SCHEMA") {
  return (errors ?? []).map((error) => ({
    code: `${namespace}.${error.keyword
      .replace(/([a-z])([A-Z])/gu, "$1_$2")
      .replaceAll("-", "_")
      .toUpperCase()}`,
    pointer: error.instancePath || "/",
    keyword: error.keyword,
    schemaPath: error.schemaPath,
    signature: errorSignature(error),
    message: error.message ?? "schema validation failed",
    params: error.params,
  }));
}

function invalidFile(relative, code, message, extra = {}) {
  return {
    path: relative,
    status: "invalid",
    code,
    message,
    errors: [],
    ...extra,
  };
}

function addCustomError(record, code, message) {
  record.status = "invalid";
  record.code = code;
  record.message = message;
  record.errors ??= [];
  record.errors.push({
    code,
    pointer: "/",
    keyword: "contract",
    schemaPath: "",
    signature: `${code}@/`,
    message,
    params: {},
  });
}

async function loadControlDocument({
  root,
  relative,
  validator,
  codePrefix,
}) {
  const absolutePath = path.join(root, relative);
  const parsed = await readJsonFile(absolutePath);
  if (parsed.error) {
    return {
      data: null,
      record: invalidFile(
        relative,
        `${codePrefix}.INVALID_JSON`,
        parsed.error,
      ),
    };
  }

  if (!validator(parsed.data)) {
    return {
      data: parsed.data,
      record: {
        path: relative,
        status: "invalid",
        code: `${codePrefix}.INVALID`,
        message: "control document does not match its internal contract",
        schema: `internal:${codePrefix.toLowerCase()}`,
        errors: normalizeAjvErrors(validator.errors, codePrefix),
      },
    };
  }

  return {
    data: parsed.data,
    record: {
      path: relative,
      status: "valid",
      code: `${codePrefix}.VALID`,
      message: "control document is valid",
      schema: `internal:${codePrefix.toLowerCase()}`,
      errors: [],
    },
  };
}

function indexControlEntries(control, collectionKey, controlRecord, codePrefix) {
  const index = new Map();
  for (const entry of control?.[collectionKey] ?? []) {
    const normalized = normalizeConfiguredPath(entry.path);
    if (!normalized) {
      addCustomError(
        controlRecord,
        `${codePrefix}.INVALID_PATH`,
        `entry path must be a normalized repository-relative JSON path: ${entry.path}`,
      );
      continue;
    }
    if (index.has(normalized)) {
      addCustomError(
        controlRecord,
        `${codePrefix}.DUPLICATE_PATH`,
        `duplicate entry path: ${normalized}`,
      );
      continue;
    }
    if (
      entry.kind === "validation-error" &&
      !entry.allowedErrorSignatures?.length
    ) {
      addCustomError(
        controlRecord,
        `${codePrefix}.MISSING_SIGNATURES`,
        `validation-error entry requires allowedErrorSignatures: ${normalized}`,
      );
      continue;
    }
    if (entry.expect === "invalid" && !entry.expectedErrorSignatures?.length) {
      addCustomError(
        controlRecord,
        `${codePrefix}.MISSING_SIGNATURES`,
        `invalid fixture requires expectedErrorSignatures: ${normalized}`,
      );
      continue;
    }
    index.set(normalized, entry);
  }
  return index;
}

async function buildSchemaRegistry({ ajv, root, jsonFiles }) {
  const schemaFiles = jsonFiles.filter((file) =>
    file.endsWith(".schema.json"),
  );
  const descriptors = [];
  const byFile = new Map();
  const byId = new Map();
  const byRepoPath = new Map();
  const records = [];

  for (const absolutePath of schemaFiles) {
    const relative = relativePath(root, absolutePath);
    const parsed = await readJsonFile(absolutePath);
    const descriptor = {
      absolutePath,
      relative,
      document: parsed.data,
      id: parsed.data?.$id,
      validate: null,
      available: false,
      record: null,
    };
    descriptors.push(descriptor);
    byFile.set(path.resolve(absolutePath), descriptor);
    byRepoPath.set(relative, descriptor);

    if (parsed.error) {
      descriptor.record = invalidFile(
        relative,
        "SCHEMA.INVALID_JSON",
        parsed.error,
      );
      records.push(descriptor.record);
      continue;
    }
    if (
      !parsed.data ||
      typeof parsed.data !== "object" ||
      Array.isArray(parsed.data)
    ) {
      descriptor.record = invalidFile(
        relative,
        "SCHEMA.NOT_OBJECT",
        "schema document must be a JSON object",
      );
      records.push(descriptor.record);
      continue;
    }
    if (parsed.data.$schema !== DRAFT_2020_12) {
      descriptor.record = invalidFile(
        relative,
        "SCHEMA.UNSUPPORTED_DRAFT",
        `schema must declare ${DRAFT_2020_12}`,
      );
      records.push(descriptor.record);
      continue;
    }
    if (typeof parsed.data.$id !== "string" || parsed.data.$id.length === 0) {
      descriptor.record = invalidFile(
        relative,
        "SCHEMA.MISSING_ID",
        "schema must declare a non-empty $id",
      );
      records.push(descriptor.record);
      continue;
    }
    if (
      !parsed.data.$id.startsWith(REPOSITORY_SCHEMA_ID_PREFIX)
      || parsed.data.$id.includes("?")
      || parsed.data.$id.includes("#")
    ) {
      descriptor.record = invalidFile(
        relative,
        "SCHEMA.INVALID_ID",
        "schema $id must use the canonical repository HTTPS prefix",
      );
      records.push(descriptor.record);
      continue;
    }
    if (!ajv.validateSchema(parsed.data)) {
      descriptor.record = {
        path: relative,
        status: "invalid",
        code: "SCHEMA.META_INVALID",
        message: "schema does not pass the draft 2020-12 meta-schema",
        schema: DRAFT_2020_12,
        errors: normalizeAjvErrors(ajv.errors, "SCHEMA_META"),
      };
      records.push(descriptor.record);
      continue;
    }
    if (byId.has(parsed.data.$id)) {
      descriptor.record = invalidFile(
        relative,
        "SCHEMA.DUPLICATE_ID",
        `duplicate schema $id: ${parsed.data.$id}`,
      );
      records.push(descriptor.record);
      continue;
    }

    descriptor.record = {
      path: relative,
      status: "schema-valid",
      code: "SCHEMA.VALID",
      message: "schema is meta-schema-valid and compiled",
      schema: DRAFT_2020_12,
      schemaId: parsed.data.$id,
      errors: [],
    };
    byId.set(parsed.data.$id, descriptor);
    records.push(descriptor.record);
  }

  // Register all schemas before compiling any one of them, so relative and
  // cross-schema $refs resolve without network access.
  for (const descriptor of descriptors) {
    if (descriptor.record?.status !== "schema-valid") {
      continue;
    }
    try {
      ajv.addSchema(descriptor.document);
      descriptor.available = true;
    } catch (error) {
      addCustomError(
        descriptor.record,
        "SCHEMA.REGISTRATION_FAILED",
        "schema could not be registered in the offline registry",
      );
      descriptor.available = false;
    }
  }

  for (const descriptor of descriptors) {
    if (!descriptor.available) {
      continue;
    }
    try {
      descriptor.validate = ajv.getSchema(descriptor.id);
      if (typeof descriptor.validate !== "function") {
        throw new Error("Ajv did not return a compiled validator");
      }
    } catch (error) {
      addCustomError(
        descriptor.record,
        "SCHEMA.COMPILE_FAILED",
        "schema could not be compiled in the offline registry",
      );
      descriptor.available = false;
      descriptor.validate = null;
    }
  }

  return {
    byFile,
    byId,
    byRepoPath,
    records,
    schemaFiles: new Set(schemaFiles.map((file) => path.resolve(file))),
  };
}

function resolveSchemaDescriptor({
  reference,
  dataFile,
  registry,
  root,
  rootRelative = false,
}) {
  if (typeof reference !== "string" || reference.length === 0) {
    return null;
  }

  const withoutEmptyFragment = reference.endsWith("#")
    ? reference.slice(0, -1)
    : reference;
  if (registry.byId.has(reference)) {
    return registry.byId.get(reference);
  }
  if (registry.byId.has(withoutEmptyFragment)) {
    return registry.byId.get(withoutEmptyFragment);
  }

  if (rootRelative) {
    const normalized = normalizeConfiguredPath(reference);
    return normalized ? registry.byRepoPath.get(normalized) ?? null : null;
  }

  if (/^[a-z][a-z0-9+.-]*:/iu.test(reference)) {
    if (reference.startsWith("file:")) {
      try {
        return (
          registry.byFile.get(path.resolve(fileURLToPath(reference))) ?? null
        );
      } catch {
        return null;
      }
    }
    // Remote identifiers are resolved only from already-loaded local $ids.
    // There is deliberately no fetch fallback.
    return null;
  }

  const absolutePath = path.resolve(path.dirname(dataFile), reference);
  if (!isInsideRoot(root, absolutePath)) {
    return null;
  }
  return registry.byFile.get(absolutePath) ?? null;
}

function compareSignatures(actualErrors, expectedSignatures) {
  const actual = new Set(actualErrors.map((error) => error.signature));
  const expected = new Set(expectedSignatures ?? []);
  return {
    unexpected: [...actual].filter((signature) => !expected.has(signature)),
    missing: [...expected].filter((signature) => !actual.has(signature)),
  };
}

function validateWithCompiledSchema({
  data,
  descriptor,
  relative,
  expected,
  expectedSignatures,
  baselineEntry,
  mode,
}) {
  if (!descriptor?.available || typeof descriptor.validate !== "function") {
    return invalidFile(
      relative,
      "CONTRACT.SCHEMA_UNAVAILABLE",
      "mapped schema did not compile successfully",
      { schema: descriptor?.id },
    );
  }

  const valid = descriptor.validate(data);
  const errors = normalizeAjvErrors(descriptor.validate.errors, "SCHEMA");

  if (expected === "invalid") {
    if (valid) {
      return invalidFile(
        relative,
        "FIXTURE.UNEXPECTED_VALID",
        "negative fixture unexpectedly passed its schema",
        { schema: descriptor.id },
      );
    }
    const comparison = compareSignatures(errors, expectedSignatures);
    if (comparison.unexpected.length > 0 || comparison.missing.length > 0) {
      return {
        path: relative,
        status: "invalid",
        code: "FIXTURE.WRONG_FAILURE",
        message: "negative fixture failed with a different error signature",
        schema: descriptor.id,
        expectedErrorSignatures: expectedSignatures,
        unexpectedErrorSignatures: comparison.unexpected,
        missingErrorSignatures: comparison.missing,
        errors,
      };
    }
    return {
      path: relative,
      status: "expected-invalid",
      code: "FIXTURE.EXPECTED_INVALID",
      message: "negative fixture failed for its declared reason",
      schema: descriptor.id,
      errors,
    };
  }

  if (valid) {
    if (baselineEntry) {
      return invalidFile(
        relative,
        "BASELINE.STALE",
        "file now passes its schema; remove the obsolete baseline entry",
        {
          issue: baselineEntry.issue,
          schema: descriptor.id,
        },
      );
    }
    return {
      path: relative,
      status: "valid",
      code: "CONTRACT.VALID",
      message: "JSON document matches its schema",
      schema: descriptor.id,
      errors: [],
    };
  }

  if (baselineEntry?.kind === "validation-error") {
    const comparison = compareSignatures(
      errors,
      baselineEntry.allowedErrorSignatures,
    );
    if (comparison.unexpected.length === 0 && comparison.missing.length === 0) {
      return {
        path: relative,
        status: "baseline",
        code: "BASELINE.KNOWN_VALIDATION_ERROR",
        message:
          mode === "release"
            ? "known schema error is release-blocking"
            : "known schema error is explicitly baselined",
        issue: baselineEntry.issue,
        reason: baselineEntry.reason,
        schema: descriptor.id,
        releaseBlocking: true,
        errors,
      };
    }
    return {
      path: relative,
      status: "invalid",
      code: "BASELINE.DRIFT",
      message: "actual schema errors differ from the explicit baseline",
      issue: baselineEntry.issue,
      schema: descriptor.id,
      unexpectedErrorSignatures: comparison.unexpected,
      missingErrorSignatures: comparison.missing,
      errors,
    };
  }

  return {
    path: relative,
    status: "invalid",
    code: "CONTRACT.INVALID",
    message: "JSON document does not match its schema",
    schema: descriptor.id,
    errors,
  };
}

async function validateDataFile({
  absolutePath,
  root,
  registry,
  fixtureCase,
  baselineEntry,
  expectationOverride,
  mode,
  packageValidator,
  packageLockValidator,
}) {
  const relative = relativePath(root, absolutePath);
  const parsed = await readJsonFile(absolutePath);
  if (parsed.error) {
    return invalidFile(relative, "CONTRACT.INVALID_JSON", parsed.error);
  }

  if (relative === "package.json") {
    if (!packageValidator(parsed.data)) {
      return {
        path: relative,
        status: "invalid",
        code: "PACKAGE_JSON.INVALID",
        message: "package manifest does not match the offline minimum contract",
        schema: "internal:package-json",
        errors: normalizeAjvErrors(packageValidator.errors, "PACKAGE_JSON"),
      };
    }
    return {
      path: relative,
      status: "valid",
      code: "PACKAGE_JSON.VALID",
      message: "package manifest matches the offline minimum contract",
      schema: "internal:package-json",
      errors: [],
    };
  }

  if (relative === "package-lock.json") {
    if (!packageLockValidator(parsed.data)) {
      return {
        path: relative,
        status: "invalid",
        code: "PACKAGE_LOCK.INVALID",
        message: "package lock does not match the offline minimum contract",
        schema: "internal:package-lock",
        errors: normalizeAjvErrors(packageLockValidator.errors, "PACKAGE_LOCK"),
      };
    }
    return {
      path: relative,
      status: "valid",
      code: "PACKAGE_LOCK.VALID",
      message: "package lock matches the offline minimum contract",
      schema: "internal:package-lock",
      errors: [],
    };
  }

  let schemaReference = fixtureCase?.schema;
  let rootRelativeReference = Boolean(fixtureCase);

  if (!schemaReference && Object.hasOwn(parsed.data ?? {}, "$schema")) {
    if (typeof parsed.data.$schema !== "string") {
      return invalidFile(
        relative,
        "CONTRACT.INVALID_SCHEMA_REFERENCE",
        "$schema must be a string",
      );
    }
    schemaReference = parsed.data.$schema;
    rootRelativeReference = false;
  }

  if (!schemaReference && PATH_SCHEMA_MAP[relative]) {
    schemaReference = PATH_SCHEMA_MAP[relative];
    rootRelativeReference = true;
  }

  if (!schemaReference) {
    if (baselineEntry?.kind === "unmapped") {
      return {
        path: relative,
        status: "baseline",
        code: "BASELINE.UNMAPPED_JSON",
        message:
          mode === "release"
            ? "unmapped JSON is release-blocking"
            : "unmapped JSON is explicitly baselined",
        issue: baselineEntry.issue,
        reason: baselineEntry.reason,
        releaseBlocking: true,
        errors: [],
      };
    }
    return invalidFile(
      relative,
      "CONTRACT.UNMAPPED_JSON",
      "JSON file has no $schema, path mapping, fixture case, or baseline entry",
    );
  }

  if (baselineEntry?.kind === "unmapped") {
    return invalidFile(
      relative,
      "BASELINE.STALE",
      "file now has a schema mapping; remove the obsolete unmapped baseline",
      { issue: baselineEntry.issue },
    );
  }

  const descriptor = resolveSchemaDescriptor({
    reference: schemaReference,
    dataFile: absolutePath,
    registry,
    root,
    rootRelative: rootRelativeReference,
  });
  if (!descriptor) {
    const presentedReference =
      presentUnresolvedSchemaReference(schemaReference);
    return invalidFile(
      relative,
      "CONTRACT.SCHEMA_UNRESOLVED",
      `schema reference is not available in the offline registry: ${presentedReference}`,
      { schema: presentedReference },
    );
  }

  return validateWithCompiledSchema({
    data: parsed.data,
    descriptor,
    relative,
    expected: expectationOverride ?? fixtureCase?.expect ?? "valid",
    expectedSignatures:
      expectationOverride === undefined
        ? fixtureCase?.expectedErrorSignatures
        : expectationOverride === "invalid"
          ? fixtureCase?.expectedErrorSignatures
          : undefined,
    baselineEntry,
    mode,
  });
}

function summarize(files) {
  const summary = {
    files: files.length,
    valid: 0,
    schemaDocuments: 0,
    expectedInvalid: 0,
    baseline: 0,
    errors: 0,
  };
  for (const file of files) {
    if (file.status === "schema-valid") {
      summary.schemaDocuments += 1;
      summary.valid += 1;
    } else if (file.status === "valid") {
      summary.valid += 1;
    } else if (file.status === "expected-invalid") {
      summary.expectedInvalid += 1;
    } else if (file.status === "baseline") {
      summary.baseline += 1;
    } else if (file.status === "invalid") {
      summary.errors += 1;
    }
  }
  return summary;
}

export function exitCodeForReport(report, mode = report.mode) {
  if (report.summary.errors > 0) {
    return EXIT_CODES.VALIDATION_FAILED;
  }
  if (mode === "release" && report.summary.baseline > 0) {
    return EXIT_CODES.VALIDATION_FAILED;
  }
  return EXIT_CODES.OK;
}

export async function validateRepository({
  root = DEFAULT_ROOT,
  mode = "baseline",
  inputs = [],
  expectationOverride,
} = {}) {
  const absoluteRoot = await fs.realpath(path.resolve(root));
  if (!["baseline", "release"].includes(mode)) {
    throw new UsageError(`unsupported mode: ${mode}`);
  }
  if (
    expectationOverride !== undefined &&
    !["valid", "invalid"].includes(expectationOverride)
  ) {
    throw new UsageError(
      `unsupported expectation override: ${expectationOverride}`,
    );
  }
  if (expectationOverride !== undefined && inputs.length !== 1) {
    throw new UsageError("--expect requires exactly one --input");
  }

  const collected = await collectJsonFiles(absoluteRoot);
  const jsonFiles = collected.files;
  const allRelativePaths = new Set(
    jsonFiles.map((file) => relativePath(absoluteRoot, file)),
  );
  const ajv = createAjv();
  const baselineValidator = ajv.compile(BASELINE_DOCUMENT_SCHEMA);
  const casesValidator = ajv.compile(CASES_DOCUMENT_SCHEMA);
  const packageValidator = ajv.compile(PACKAGE_JSON_SCHEMA);
  const packageLockValidator = ajv.compile(PACKAGE_LOCK_SCHEMA);

  const baselineControl = await loadControlDocument({
    root: absoluteRoot,
    relative: BASELINE_PATH,
    validator: baselineValidator,
    codePrefix: "BASELINE",
  });
  const casesControl = await loadControlDocument({
    root: absoluteRoot,
    relative: CASES_PATH,
    validator: casesValidator,
    codePrefix: "FIXTURE_MANIFEST",
  });
  const baselineIndex = indexControlEntries(
    baselineControl.data,
    "entries",
    baselineControl.record,
    "BASELINE",
  );
  const casesIndex = indexControlEntries(
    casesControl.data,
    "cases",
    casesControl.record,
    "FIXTURE_MANIFEST",
  );

  const registry = await buildSchemaRegistry({
    ajv,
    root: absoluteRoot,
    jsonFiles,
  });
  const files = [
    baselineControl.record,
    casesControl.record,
    ...registry.records,
    ...collected.symbolicLinks.map((absolutePath) =>
      invalidFile(
        relativePath(absoluteRoot, absolutePath),
        "CONTRACT.SYMLINK_NOT_ALLOWED",
        "symbolic links are not allowed in the governed repository tree",
      )),
  ];

  let selectedFiles;
  if (inputs.length === 0) {
    selectedFiles = jsonFiles;
  } else {
    selectedFiles = [];
    for (const input of inputs) {
      const lexicalPath = path.resolve(absoluteRoot, input);
      if (!isInsideRoot(absoluteRoot, lexicalPath)) {
        throw new UsageError(`input must be inside repository root: ${input}`);
      }
      let stat;
      try {
        stat = await fs.lstat(lexicalPath);
      } catch {
        throw new UsageError(`input does not exist: ${input}`);
      }
      if (stat.isSymbolicLink()) {
        throw new UsageError(`symbolic-link inputs are not allowed: ${input}`);
      }
      const absolutePath = await fs.realpath(lexicalPath);
      if (!isInsideRoot(absoluteRoot, absolutePath)) {
        throw new UsageError(
          `resolved input must be inside repository root: ${input}`,
        );
      }
      if (!stat.isFile() || !absolutePath.endsWith(".json")) {
        throw new UsageError(`input must be a JSON file: ${input}`);
      }
      selectedFiles.push(absolutePath);
    }
  }

  const controlFiles = new Set([
    path.resolve(absoluteRoot, BASELINE_PATH),
    path.resolve(absoluteRoot, CASES_PATH),
  ]);
  const usedBaselinePaths = new Set();
  const usedCasePaths = new Set();

  for (const absolutePath of selectedFiles) {
    const resolved = path.resolve(absolutePath);
    if (controlFiles.has(resolved) || registry.schemaFiles.has(resolved)) {
      continue;
    }
    const relative = relativePath(absoluteRoot, resolved);
    const fixtureCase = casesIndex.get(relative);
    const baselineEntry = baselineIndex.get(relative);
    if (fixtureCase) {
      usedCasePaths.add(relative);
    }
    if (baselineEntry) {
      usedBaselinePaths.add(relative);
    }
    files.push(
      await validateDataFile({
        absolutePath: resolved,
        root: absoluteRoot,
        registry,
        fixtureCase,
        baselineEntry,
        expectationOverride,
        mode,
        packageValidator,
        packageLockValidator,
      }),
    );
  }

  if (inputs.length === 0) {
    for (const fixturePath of casesIndex.keys()) {
      if (!allRelativePaths.has(fixturePath)) {
        files.push(
          invalidFile(
            fixturePath,
            "FIXTURE_MANIFEST.MISSING_FILE",
            "fixture manifest references a missing file",
          ),
        );
      } else if (!usedCasePaths.has(fixturePath)) {
        files.push(
          invalidFile(
            fixturePath,
            "FIXTURE_MANIFEST.UNUSED_CASE",
            "fixture case was not evaluated",
          ),
        );
      }
    }
    for (const [baselinePath, entry] of baselineIndex) {
      if (!allRelativePaths.has(baselinePath)) {
        files.push(
          invalidFile(
            baselinePath,
            "BASELINE.MISSING_FILE",
            "baseline references a missing file",
            { issue: entry.issue },
          ),
        );
      } else if (!usedBaselinePaths.has(baselinePath)) {
        files.push(
          invalidFile(
            baselinePath,
            "BASELINE.STALE",
            "baseline entry was not used; remove it",
            { issue: entry.issue },
          ),
        );
      }
    }
  }

  files.sort((left, right) => {
    const pathOrder = left.path.localeCompare(right.path);
    return pathOrder === 0
      ? left.code.localeCompare(right.code)
      : pathOrder;
  });
  const report = {
    reportVersion: 1,
    mode,
    offline: true,
    summary: summarize(files),
    files,
  };
  report.exitCode = exitCodeForReport(report, mode);
  return report;
}

export function renderTextReport(report) {
  const lines = [
    `JSON contract validation (${report.mode}, offline schema registry)`,
  ];
  for (const file of report.files) {
    const marker =
      file.status === "invalid"
        ? "✗"
        : file.status === "baseline"
          ? report.mode === "release"
            ? "✗"
            : "~"
          : "✓";
    lines.push(`${marker} ${file.path} [${file.code}] ${file.message}`);
    if (file.issue) {
      lines.push(`  issue: ${file.issue}`);
    }
    if (file.reason) {
      lines.push(`  reason: ${file.reason}`);
    }
    for (const error of file.errors ?? []) {
      lines.push(
        `  ${error.code} ${error.pointer} (${error.signature}): ${error.message}`,
      );
    }
    for (const signature of file.unexpectedErrorSignatures ?? []) {
      lines.push(`  unexpected signature: ${signature}`);
    }
    for (const signature of file.missingErrorSignatures ?? []) {
      lines.push(`  missing signature: ${signature}`);
    }
  }
  lines.push(
    `Summary: ${report.summary.files} files, ${report.summary.valid} valid, ` +
      `${report.summary.expectedInvalid} expected-invalid, ` +
      `${report.summary.baseline} baseline, ${report.summary.errors} errors`,
  );
  if (report.mode === "release" && report.summary.baseline > 0) {
    lines.push("Release blocked: baseline debt is not allowed in release mode.");
  }
  return `${lines.join("\n")}\n`;
}

function usage() {
  return `Usage: node scripts/validate-all-json.mjs [options]

Options:
  --root <directory>       Repository root (default: script parent)
  --input <json>           Validate one repository-relative JSON (repeatable)
  --mode baseline|release  Baseline reports debt; release blocks it
  --expect valid|invalid   Override one --input fixture expectation
  --format text|json       Report format (default: text)
  --help                   Show this help

Exit codes:
  0  all contracts passed (baseline debt is allowed only in baseline mode)
  1  JSON/schema/fixture validation failed, or release debt remains
  2  invalid CLI usage or an internal execution error
`;
}

function parseArguments(argv) {
  const options = {
    root: DEFAULT_ROOT,
    inputs: [],
    mode: "baseline",
    format: "text",
    expectationOverride: undefined,
    help: false,
  };
  const seen = new Set();

  for (let index = 0; index < argv.length; index += 1) {
    const argument = argv[index];
    if (argument === "--help" || argument === "-h") {
      if (seen.has("help")) throw new UsageError("duplicate option: --help");
      seen.add("help");
      options.help = true;
    } else if (
      argument === "--root" ||
      argument === "--input" ||
      argument === "--mode" ||
      argument === "--format" ||
      argument === "--expect"
    ) {
      if (argument !== "--input" && seen.has(argument)) {
        throw new UsageError(`duplicate option: ${argument}`);
      }
      seen.add(argument);
      const value = argv[index + 1];
      if (!value || value.startsWith("--")) {
        throw new UsageError(`${argument} requires a value`);
      }
      index += 1;
      if (argument === "--root") {
        options.root = path.resolve(value);
      } else if (argument === "--input") {
        options.inputs.push(value);
      } else if (argument === "--mode") {
        if (!["baseline", "release"].includes(value)) {
          throw new UsageError(`unsupported mode: ${value}`);
        }
        options.mode = value;
      } else if (argument === "--format") {
        if (!["text", "json"].includes(value)) {
          throw new UsageError(`unsupported format: ${value}`);
        }
        options.format = value;
      } else if (argument === "--expect") {
        if (!["valid", "invalid"].includes(value)) {
          throw new UsageError(`unsupported expectation: ${value}`);
        }
        options.expectationOverride = value;
      }
    } else {
      throw new UsageError(`unknown argument: ${argument}`);
    }
  }
  return options;
}

async function main() {
  let options;
  try {
    options = parseArguments(process.argv.slice(2));
    if (options.help) {
      process.stdout.write(usage());
      return EXIT_CODES.OK;
    }
    const report = await validateRepository(options);
    if (options.format === "json") {
      process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
    } else {
      process.stdout.write(renderTextReport(report));
    }
    return report.exitCode;
  } catch (error) {
    if (error instanceof UsageError) {
      process.stderr.write(`${error.message}\n\n${usage()}`);
    } else {
      const code =
        typeof error?.code === "string" && error.code.length > 0
          ? error.code
          : "INTERNAL_ERROR";
      process.stderr.write(`internal schema validator error: ${code}\n`);
    }
    return EXIT_CODES.USAGE_OR_INTERNAL_ERROR;
  }
}

const invokedAsScript =
  process.argv[1] &&
  path.resolve(process.argv[1]) === path.resolve(fileURLToPath(import.meta.url));
if (invokedAsScript) {
  process.exitCode = await main();
}
