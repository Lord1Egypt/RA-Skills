import assert from "node:assert/strict";
import {spawnSync} from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import {fileURLToPath} from "node:url";

import Ajv2020 from "ajv/dist/2020.js";
import addFormats from "ajv-formats";

import {
  REQUIRED_RULE_DOMAINS,
  auditRuleRegistry,
  auditRuleRegistryDocument,
  evaluateRuleOverrides,
} from "../src/rules/rule-registry.mjs";

const ROOT = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
);
const CLI = path.join(ROOT, "scripts", "validate-rule-registry.mjs");

function readJson(relativePath) {
  return JSON.parse(fs.readFileSync(path.join(ROOT, relativePath), "utf8"));
}

function runCli(...arguments_) {
  return spawnSync(process.execPath, [CLI, ...arguments_], {
    cwd: ROOT,
    encoding: "utf8",
  });
}

test("canonical Rule Registry passes all six governed domains", () => {
  const report = auditRuleRegistry({root: ROOT});
  assert.equal(report.status, "passed", JSON.stringify(report.findings));
  assert.deepEqual(report.summary, {
    rules: 18,
    domains: 6,
    runtimeRules: 18,
    contractRules: 0,
    errors: 0,
  });

  const registry = readJson("rules/registry.json");
  assert.deepEqual(
    [...new Set(registry.rules.map((rule) => rule.domain))].sort(),
    [...REQUIRED_RULE_DOMAINS].sort(),
  );
});

test("Rule Registry schema blocks hard-rule weakening semantics", () => {
  const schema = readJson("schemas/rule-registry.schema.json");
  const registry = readJson("rules/registry.json");
  const ajv = new Ajv2020({
    allErrors: true,
    strict: true,
    strictRequired: false,
  });
  addFormats(ajv);
  const validate = ajv.compile(schema);
  assert.equal(validate(registry), true, JSON.stringify(validate.errors));

  const invalid = structuredClone(registry);
  invalid.rules[0].overridePolicy = "local";
  invalid.rules[0].waiverPolicy = "allowed";
  invalid.rules[0].fallback = "report-only";
  assert.equal(validate(invalid), false);
  assert.ok(validate.errors.some(
    (error) =>
      error.instancePath === "/rules/0/overridePolicy"
      && error.keyword === "enum",
  ));
  assert.ok(validate.errors.some(
    (error) =>
      error.instancePath === "/rules/0/waiverPolicy"
      && error.keyword === "const",
  ));
});

test("valid overrides may preserve or tighten hard rules", () => {
  const result = runCli(
    "--overrides",
    "fixtures/rules/overrides.valid.json",
    "--format",
    "json",
  );
  assert.equal(result.status, 0, result.stderr || result.stdout);
  const report = JSON.parse(result.stdout);
  assert.equal(report.status, "passed");
  assert.equal(report.summary.errors, 0);
});

test("weakened overrides fail every registered rule without echoing values", () => {
  const result = runCli(
    "--overrides",
    "fixtures/rules/overrides.weakened.invalid.json",
    "--format",
    "json",
  );
  assert.equal(result.status, 1, result.stderr || result.stdout);
  const report = JSON.parse(result.stdout);
  assert.equal(report.findings.length, 18);
  assert.ok(report.findings.every(
    (item) => item.code === "RULE_OVERRIDE_WEAKENED",
  ));
  assert.equal(
    new Set(report.findings.map((item) => item.ruleId)).size,
    18,
  );
  assert.doesNotMatch(result.stdout, /translation|blind-retry/u);
});

test("override evaluator rejects stale, duplicate, and unknown rule identities", () => {
  const registry = readJson("rules/registry.json");
  const findings = evaluateRuleOverrides({
    registry,
    overrides: {
      version: 1,
      registryVersion: "0.0.0",
      overrides: [
        {
          ruleId: "CAPTION-MAX-LINES",
          value: 1,
        },
        {
          ruleId: "CAPTION-MAX-LINES",
          value: 1,
        },
        {
          ruleId: "UNKNOWN-RULE-ID",
          value: true,
        },
      ],
    },
  });
  assert.deepEqual(
    findings.map((item) => item.code),
    [
      "RULE_OVERRIDE_REGISTRY_VERSION",
      "RULE_OVERRIDE_DUPLICATE",
      "RULE_OVERRIDE_UNKNOWN",
    ],
  );
});

test("override evaluator fails closed on a malformed direct-call document", () => {
  const registry = readJson("rules/registry.json");
  assert.deepEqual(
    evaluateRuleOverrides({registry, overrides: {overrides: null}}),
    [
      {
        code: "RULE_OVERRIDES_SCHEMA_TYPE",
        pointer: "/overrides",
        message: "override document does not contain an override array",
      },
    ],
  );
});

test("registry audit detects policy-version and canonical-value drift", () => {
  const registry = readJson("rules/registry.json");
  registry.policyVersion = "0.0.0";
  registry.rules.find(
    (rule) => rule.ruleId === "CAPTION-REPLACEMENT-MAX",
  ).canonical.value = 5;
  const report = auditRuleRegistryDocument({root: ROOT, registry});
  const codes = new Set(report.findings.map((item) => item.code));
  assert.ok(codes.has("RULE_REGISTRY_POLICY_VERSION"));
  assert.ok(codes.has("RULE_REGISTRY_CANONICAL_DRIFT"));
  assert.ok(codes.has("RULE_REGISTRY_FIXTURE_EXPECTATION"));
});

test("registry audit requires stable ordering, unique checks, and all domains", () => {
  const registry = readJson("rules/registry.json");
  registry.rules.reverse();
  registry.rules = registry.rules.filter(
    (rule) => rule.domain !== "privacy",
  );
  registry.rules.find(
    (rule) => rule.ruleId === "CAPTION-MAX-LINES",
  ).enforcement.checkId = "caption.automatic-wrap";
  const report = auditRuleRegistryDocument({root: ROOT, registry});
  const codes = new Set(report.findings.map((item) => item.code));
  assert.ok(codes.has("RULE_REGISTRY_ORDER"));
  assert.ok(codes.has("RULE_REGISTRY_DUPLICATE_CHECK"));
  assert.ok(codes.has("RULE_REGISTRY_MISSING_DOMAIN"));
});

test("registry audit rejects unsafe and missing repository references", () => {
  const registry = readJson("rules/registry.json");
  registry.rules[0].source.reference = "../outside.md";
  registry.rules[1].enforcement.implementedBy[0] = "scripts/missing.mjs";
  const report = auditRuleRegistryDocument({root: ROOT, registry});
  const codes = new Set(report.findings.map((item) => item.code));
  assert.ok(codes.has("RULE_REGISTRY_UNSAFE_REFERENCE"));
  assert.ok(codes.has("RULE_REGISTRY_REFERENCE_MISSING"));
});

test("registry fixture coverage proves a pass and fail case per rule", () => {
  const registry = readJson("rules/registry.json");
  registry.rules[0].fixtureRefs.fail = [
    "fixtures/rules/overrides.valid.json",
  ];
  const report = auditRuleRegistryDocument({root: ROOT, registry});
  assert.ok(report.findings.some(
    (item) =>
      item.ruleId === "CAPTION-AUTOMATIC-WRAP"
      && item.code === "RULE_REGISTRY_FIXTURE_EXPECTATION",
  ));
});

test("Rule Registry CLI rejects ambiguous options with exit 2", () => {
  const unknown = runCli("--rules", "rules/registry.json");
  assert.equal(unknown.status, 2);
  assert.match(unknown.stderr, /unknown or unsupported option/u);

  const duplicate = runCli(
    "--format",
    "json",
    "--format",
    "text",
  );
  assert.equal(duplicate.status, 2);
  assert.match(duplicate.stderr, /duplicate option: --format/u);

  const valueless = runCli("--overrides");
  assert.equal(valueless.status, 2);
  assert.match(valueless.stderr, /--overrides requires a value/u);
});

test("Rule Registry operational failures use stable codes without paths", (t) => {
  const temporaryRoot = fs.mkdtempSync(
    path.join(os.tmpdir(), "koubo-rule-private-"),
  );
  t.after(() => fs.rmSync(temporaryRoot, {recursive: true, force: true}));
  const result = runCli("--root", temporaryRoot);
  assert.equal(result.status, 2);
  assert.match(
    result.stderr,
    /rule registry audit unavailable: RULE_REGISTRY_INPUT_UNREADABLE/u,
  );
  assert.doesNotMatch(
    result.stderr,
    new RegExp(temporaryRoot.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")),
  );
});
