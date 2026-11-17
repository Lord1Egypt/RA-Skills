import fs from "node:fs";
import path from "node:path";

import Ajv2020 from "ajv/dist/2020.js";
import addFormats from "ajv-formats";

export const REQUIRED_RULE_DOMAINS = Object.freeze([
  "content-truth",
  "captions",
  "privacy",
  "timeline-integrity",
  "execution-safety",
  "export-authorization",
]);

export class RuleRegistryError extends Error {
  constructor(code, message, options = {}) {
    super(message, options);
    this.name = "RuleRegistryError";
    this.code = code;
  }
}

function finding(code, pointer, message, ruleId) {
  return {
    code,
    pointer,
    message,
    ...(ruleId ? {ruleId} : {}),
  };
}

function readJsonFile(absolutePath, code) {
  let source;
  try {
    source = fs.readFileSync(absolutePath, "utf8");
  } catch (cause) {
    throw new RuleRegistryError(code, "required JSON input is not readable", {
      cause,
    });
  }
  try {
    return JSON.parse(source);
  } catch (cause) {
    throw new RuleRegistryError(code, "required JSON input is invalid", {
      cause,
    });
  }
}

function isInsideRoot(root, absolutePath) {
  const relative = path.relative(root, absolutePath);
  return relative === ""
    || (
      relative !== ".."
      && !relative.startsWith(`..${path.sep}`)
      && !path.isAbsolute(relative)
    );
}

function splitReference(reference) {
  const marker = reference.indexOf("#");
  return marker === -1
    ? {file: reference, fragment: ""}
    : {
        file: reference.slice(0, marker),
        fragment: reference.slice(marker + 1),
      };
}

function normalizeRepositoryReference(reference) {
  if (
    typeof reference !== "string"
    || reference.length === 0
    || reference.includes("\\")
    || path.posix.isAbsolute(reference)
  ) {
    return null;
  }
  const {file, fragment} = splitReference(reference);
  const normalized = path.posix.normalize(file);
  if (
    normalized === "."
    || normalized === ".."
    || normalized.startsWith("../")
    || normalized !== file
  ) {
    return null;
  }
  return {file: normalized, fragment};
}

function inspectRepositoryFile(root, reference) {
  const normalized = normalizeRepositoryReference(reference);
  if (!normalized) {
    return {ok: false, code: "RULE_REGISTRY_UNSAFE_REFERENCE"};
  }
  const absolutePath = path.resolve(root, normalized.file);
  if (!isInsideRoot(root, absolutePath)) {
    return {ok: false, code: "RULE_REGISTRY_UNSAFE_REFERENCE"};
  }
  let stat;
  try {
    stat = fs.lstatSync(absolutePath);
  } catch {
    return {ok: false, code: "RULE_REGISTRY_REFERENCE_MISSING"};
  }
  if (stat.isSymbolicLink()) {
    return {ok: false, code: "RULE_REGISTRY_SYMLINK_REFERENCE"};
  }
  if (!stat.isFile()) {
    return {ok: false, code: "RULE_REGISTRY_REFERENCE_NOT_FILE"};
  }
  let canonical;
  try {
    canonical = fs.realpathSync(absolutePath);
  } catch {
    return {ok: false, code: "RULE_REGISTRY_REFERENCE_UNREADABLE"};
  }
  if (!isInsideRoot(root, canonical)) {
    return {ok: false, code: "RULE_REGISTRY_UNSAFE_REFERENCE"};
  }
  return {
    ok: true,
    absolutePath: canonical,
    relativePath: normalized.file,
    fragment: normalized.fragment,
  };
}

function createSchemaValidators(root) {
  const registrySchema = readJsonFile(
    path.join(root, "schemas/rule-registry.schema.json"),
    "RULE_REGISTRY_SCHEMA_READ_FAILED",
  );
  const overridesSchema = readJsonFile(
    path.join(root, "schemas/rule-overrides.schema.json"),
    "RULE_REGISTRY_SCHEMA_READ_FAILED",
  );
  const ajv = new Ajv2020({
    allErrors: true,
    allowUnionTypes: true,
    logger: false,
    strict: true,
    strictRequired: false,
    validateFormats: true,
  });
  addFormats(ajv);
  return {
    validateRegistry: ajv.compile(registrySchema),
    validateOverrides: ajv.compile(overridesSchema),
  };
}

function schemaFindings(validate, document, prefix) {
  if (validate(document)) return [];
  return (validate.errors ?? []).map((error) =>
    finding(
      `${prefix}_${error.keyword
        .replace(/([a-z])([A-Z])/gu, "$1_$2")
        .replaceAll("-", "_")
        .toUpperCase()}`,
      error.instancePath || "/",
      "document does not match its schema",
    ));
}

function valuesEqual(left, right) {
  if (Array.isArray(left) || Array.isArray(right)) {
    return Array.isArray(left)
      && Array.isArray(right)
      && left.length === right.length
      && left.every((value, index) => value === right[index]);
  }
  return Object.is(left, right);
}

function overridePreservesRule(rule, candidate) {
  const {comparison, value: canonical} = rule.canonical;
  if (comparison === "equal") return valuesEqual(candidate, canonical);
  if (comparison === "maximum") {
    return Number.isFinite(candidate)
      && Number.isFinite(canonical)
      && candidate <= canonical;
  }
  if (comparison === "minimum") {
    return Number.isFinite(candidate)
      && Number.isFinite(canonical)
      && candidate >= canonical;
  }
  if (comparison === "subset") {
    if (!Array.isArray(candidate) || !Array.isArray(canonical)) return false;
    const allowed = new Set(canonical);
    return candidate.length > 0 && candidate.every((value) => allowed.has(value));
  }
  return false;
}

export function evaluateRuleOverrides({
  registry,
  overrides,
  validateOverrides,
} = {}) {
  const findings = [];
  if (validateOverrides) {
    findings.push(
      ...schemaFindings(
        validateOverrides,
        overrides,
        "RULE_OVERRIDES_SCHEMA",
      ),
    );
    if (findings.length > 0) return findings;
  }
  if (!overrides || !Array.isArray(overrides.overrides)) {
    return [
      finding(
        "RULE_OVERRIDES_SCHEMA_TYPE",
        "/overrides",
        "override document does not contain an override array",
      ),
    ];
  }
  if (!registry || !Array.isArray(registry.rules)) {
    return [
      finding(
        "RULE_REGISTRY_UNAVAILABLE",
        "/",
        "rule registry is unavailable",
      ),
    ];
  }
  if (overrides.registryVersion !== registry.registryVersion) {
    findings.push(
      finding(
        "RULE_OVERRIDE_REGISTRY_VERSION",
        "/registryVersion",
        "override document targets a different registry version",
      ),
    );
  }
  const byId = new Map(registry.rules.map((rule) => [rule.ruleId, rule]));
  const seen = new Set();
  for (let index = 0; index < overrides.overrides.length; index += 1) {
    const override = overrides.overrides[index];
    const pointer = `/overrides/${index}`;
    if (seen.has(override.ruleId)) {
      findings.push(
        finding(
          "RULE_OVERRIDE_DUPLICATE",
          `${pointer}/ruleId`,
          "override document repeats a rule",
          override.ruleId,
        ),
      );
      continue;
    }
    seen.add(override.ruleId);
    const rule = byId.get(override.ruleId);
    if (!rule) {
      findings.push(
        finding(
          "RULE_OVERRIDE_UNKNOWN",
          `${pointer}/ruleId`,
          "override refers to an unknown rule",
          override.ruleId,
        ),
      );
      continue;
    }
    if (!overridePreservesRule(rule, override.value)) {
      findings.push(
        finding(
          "RULE_OVERRIDE_WEAKENED",
          `${pointer}/value`,
          "override would weaken or change a protected rule",
          override.ruleId,
        ),
      );
    }
  }
  return findings;
}

function decodePointerSegment(segment) {
  return segment.replaceAll("~1", "/").replaceAll("~0", "~");
}

function resolveJsonPointer(document, fragment) {
  if (!fragment.startsWith("/")) return {found: false};
  let current = document;
  for (const rawSegment of fragment.slice(1).split("/")) {
    const segment = decodePointerSegment(rawSegment);
    if (
      current === null
      || typeof current !== "object"
      || !Object.prototype.hasOwnProperty.call(current, segment)
    ) {
      return {found: false};
    }
    current = current[segment];
  }
  return {found: true, value: current};
}

function auditReference(root, reference, pointer, ruleId, findings) {
  const result = inspectRepositoryFile(root, reference);
  if (!result.ok) {
    findings.push(
      finding(
        result.code,
        pointer,
        "repository reference is missing, unsafe, or unsupported",
        ruleId,
      ),
    );
  }
  return result;
}

function readFixture(root, reference, pointer, ruleId, findings) {
  const inspected = auditReference(
    root,
    reference,
    pointer,
    ruleId,
    findings,
  );
  if (!inspected.ok) return null;
  try {
    return readJsonFile(
      inspected.absolutePath,
      "RULE_REGISTRY_FIXTURE_READ_FAILED",
    );
  } catch {
    findings.push(
      finding(
        "RULE_REGISTRY_FIXTURE_READ_FAILED",
        pointer,
        "rule fixture is not readable JSON",
        ruleId,
      ),
    );
    return null;
  }
}

function findRuleOverride(document, ruleId) {
  if (!document || !Array.isArray(document.overrides)) return null;
  const matches = document.overrides.filter(
    (override) => override.ruleId === ruleId,
  );
  return matches.length === 1 ? matches[0] : null;
}

function auditFixtureCoverage({
  root,
  registry,
  rule,
  ruleIndex,
  validateOverrides,
  findings,
}) {
  for (const expectation of ["pass", "fail"]) {
    const references = rule.fixtureRefs[expectation];
    for (let index = 0; index < references.length; index += 1) {
      const pointer =
        `/rules/${ruleIndex}/fixtureRefs/${expectation}/${index}`;
      const document = readFixture(
        root,
        references[index],
        pointer,
        rule.ruleId,
        findings,
      );
      if (!document) continue;
      const schemaErrors = schemaFindings(
        validateOverrides,
        document,
        "RULE_OVERRIDES_SCHEMA",
      );
      if (schemaErrors.length > 0) {
        findings.push(
          finding(
            "RULE_REGISTRY_FIXTURE_SCHEMA",
            pointer,
            "rule fixture does not match the override contract",
            rule.ruleId,
          ),
        );
        continue;
      }
      const candidate = findRuleOverride(document, rule.ruleId);
      if (!candidate) {
        findings.push(
          finding(
            "RULE_REGISTRY_FIXTURE_COVERAGE",
            pointer,
            "rule fixture must contain the rule exactly once",
            rule.ruleId,
          ),
        );
        continue;
      }
      const actualPass = overridePreservesRule(rule, candidate.value);
      if (
        (expectation === "pass" && !actualPass)
        || (expectation === "fail" && actualPass)
      ) {
        findings.push(
          finding(
            "RULE_REGISTRY_FIXTURE_EXPECTATION",
            pointer,
            "rule fixture does not produce its declared outcome",
            rule.ruleId,
          ),
        );
      }
    }
  }
}

export function auditRuleRegistryDocument({root, registry}) {
  const canonicalRoot = fs.realpathSync(path.resolve(root));
  const {validateRegistry, validateOverrides} =
    createSchemaValidators(canonicalRoot);
  const findings = schemaFindings(
    validateRegistry,
    registry,
    "RULE_REGISTRY_SCHEMA",
  );
  if (findings.length > 0) {
    return {
      registry,
      validateOverrides,
      findings,
    };
  }

  const policy = readJsonFile(
    path.join(canonicalRoot, "rules/policy.json"),
    "RULE_REGISTRY_POLICY_READ_FAILED",
  );
  if (registry.policyVersion !== policy.version) {
    findings.push(
      finding(
        "RULE_REGISTRY_POLICY_VERSION",
        "/policyVersion",
        "registry policy version differs from the hard policy",
      ),
    );
  }

  const ids = registry.rules.map((rule) => rule.ruleId);
  const sortedIds = [...ids].sort((left, right) => left.localeCompare(right));
  if (!ids.every((id, index) => id === sortedIds[index])) {
    findings.push(
      finding(
        "RULE_REGISTRY_ORDER",
        "/rules",
        "rules must be sorted by ruleId",
      ),
    );
  }
  const seenIds = new Set();
  const seenChecks = new Set();
  const presentDomains = new Set();

  registry.rules.forEach((rule, ruleIndex) => {
    const basePointer = `/rules/${ruleIndex}`;
    presentDomains.add(rule.domain);
    if (seenIds.has(rule.ruleId)) {
      findings.push(
        finding(
          "RULE_REGISTRY_DUPLICATE_ID",
          `${basePointer}/ruleId`,
          "ruleId must be document-global unique",
          rule.ruleId,
        ),
      );
    }
    seenIds.add(rule.ruleId);

    if (rule.enforcement.checkId) {
      if (seenChecks.has(rule.enforcement.checkId)) {
        findings.push(
          finding(
            "RULE_REGISTRY_DUPLICATE_CHECK",
            `${basePointer}/enforcement/checkId`,
            "runtime checkId must be unique",
            rule.ruleId,
          ),
        );
      }
      seenChecks.add(rule.enforcement.checkId);
    }

    const source = auditReference(
      canonicalRoot,
      rule.source.reference,
      `${basePointer}/source/reference`,
      rule.ruleId,
      findings,
    );
    if (
      source.ok
      && rule.source.type === "repository-policy"
    ) {
      let sourceDocument;
      try {
        sourceDocument = readJsonFile(
          source.absolutePath,
          "RULE_REGISTRY_POLICY_SOURCE_READ_FAILED",
        );
      } catch {
        findings.push(
          finding(
            "RULE_REGISTRY_POLICY_SOURCE_READ_FAILED",
            `${basePointer}/source/reference`,
            "policy source is not readable JSON",
            rule.ruleId,
          ),
        );
      }
      if (sourceDocument) {
        const resolved = resolveJsonPointer(sourceDocument, source.fragment);
        if (!resolved.found) {
          findings.push(
            finding(
              "RULE_REGISTRY_POLICY_POINTER",
              `${basePointer}/source/reference`,
              "policy source JSON pointer does not resolve",
              rule.ruleId,
            ),
          );
        } else if (!valuesEqual(resolved.value, rule.canonical.value)) {
          findings.push(
            finding(
              "RULE_REGISTRY_CANONICAL_DRIFT",
              `${basePointer}/canonical/value`,
              "canonical value differs from its policy source",
              rule.ruleId,
            ),
          );
        }
      }
    }

    rule.enforcement.implementedBy.forEach((reference, index) => {
      auditReference(
        canonicalRoot,
        reference,
        `${basePointer}/enforcement/implementedBy/${index}`,
        rule.ruleId,
        findings,
      );
    });

    auditFixtureCoverage({
      root: canonicalRoot,
      registry,
      rule,
      ruleIndex,
      validateOverrides,
      findings,
    });
  });

  for (const domain of REQUIRED_RULE_DOMAINS) {
    if (!presentDomains.has(domain)) {
      findings.push(
        finding(
          "RULE_REGISTRY_MISSING_DOMAIN",
          "/rules",
          `required rule domain is missing: ${domain}`,
        ),
      );
    }
  }

  return {
    registry,
    validateOverrides,
    findings,
  };
}

export function auditRuleRegistry({
  root,
  registryPath = "rules/registry.json",
  overridesPath,
}) {
  let canonicalRoot;
  try {
    canonicalRoot = fs.realpathSync(path.resolve(root));
  } catch (cause) {
    throw new RuleRegistryError(
      "RULE_REGISTRY_ROOT_UNREADABLE",
      "repository root is not readable",
      {cause},
    );
  }
  const registryReference = inspectRepositoryFile(
    canonicalRoot,
    registryPath,
  );
  if (!registryReference.ok) {
    throw new RuleRegistryError(
      "RULE_REGISTRY_INPUT_UNREADABLE",
      "registry input is missing, unsafe, or unreadable",
    );
  }
  const registry = readJsonFile(
    registryReference.absolutePath,
    "RULE_REGISTRY_INPUT_INVALID",
  );
  const audit = auditRuleRegistryDocument({
    root: canonicalRoot,
    registry,
  });
  const findings = [...audit.findings];

  if (overridesPath) {
    const overridesReference = inspectRepositoryFile(
      canonicalRoot,
      overridesPath,
    );
    if (!overridesReference.ok) {
      throw new RuleRegistryError(
        "RULE_OVERRIDES_INPUT_UNREADABLE",
        "override input is missing, unsafe, or unreadable",
      );
    }
    const overrides = readJsonFile(
      overridesReference.absolutePath,
      "RULE_OVERRIDES_INPUT_INVALID",
    );
    findings.push(
      ...evaluateRuleOverrides({
        registry,
        overrides,
        validateOverrides: audit.validateOverrides,
      }),
    );
  }

  const rules = Array.isArray(registry.rules) ? registry.rules : [];
  const domains = new Set(rules.map((rule) => rule.domain));
  const runtimeRules =
    rules.filter((rule) => rule.enforcement?.level === "runtime").length;
  const contractRules =
    rules.filter(
      (rule) => rule.enforcement?.level === "registry-contract",
    ).length;
  return {
    status: findings.length === 0 ? "passed" : "failed",
    registryVersion: registry?.registryVersion ?? null,
    policyVersion: registry?.policyVersion ?? null,
    summary: {
      rules: rules.length,
      domains: domains.size,
      runtimeRules,
      contractRules,
      errors: findings.length,
    },
    findings,
  };
}
