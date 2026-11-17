#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

import Ajv2020 from "ajv/dist/2020.js";
import addFormats from "ajv-formats";

import {assertEvidenceClaims} from "../src/orchestration/handoff-reporter.mjs";
import {runFakeOneClickSession} from "../src/orchestration/orchestrator.mjs";
import {assertSourceInventoryBindings} from "../src/orchestration/source-inventory.mjs";

const DEFAULT_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const RUNTIME_SCHEMA_PREFIX = "https://github.com/maojiebc/majia-chatcut-koubo/schemas/runtime/";
const REQUIRED_SCENARIOS = new Set([
  "scenario-happy-path",
  "scenario-timeout-before",
  "scenario-timeout-after",
  "scenario-partial-write",
  "scenario-manual-edit",
]);

function usage(message) {
  process.stderr.write("Usage: node scripts/validate-runtime-fixtures.mjs [--root <repository-root>] [--json]\n");
  if (message) process.stderr.write(`${message}\n`);
  process.exit(2);
}

function parseArguments(argv) {
  let root = DEFAULT_ROOT;
  let json = false;
  let rootSeen = false;
  for (let index = 0; index < argv.length; index += 1) {
    const option = argv[index];
    if (option === "--json") {
      if (json) usage("duplicate option: --json");
      json = true;
      continue;
    }
    if (option === "--root") {
      if (rootSeen) usage("duplicate option: --root");
      const value = argv[index + 1];
      if (!value || value.startsWith("--")) usage("--root requires a value");
      root = path.resolve(value);
      rootSeen = true;
      index += 1;
      continue;
    }
    usage("unknown option");
  }
  return {root, json};
}

function relative(root, file) {
  const value = path.relative(root, file).split(path.sep).join("/");
  return value && !value.startsWith("../") && !path.isAbsolute(value)
    ? value
    : "<outside-root>";
}

function readJson(root, relativePath) {
  const absolute = path.resolve(root, relativePath);
  if (relative(root, absolute) === "<outside-root>") throw new Error("RUNTIME_PATH_OUTSIDE_ROOT");
  let stat;
  try {
    stat = fs.lstatSync(absolute);
  } catch {
    throw new Error(`RUNTIME_FILE_MISSING:${relativePath}`);
  }
  if (!stat.isFile() || stat.isSymbolicLink()) throw new Error(`RUNTIME_FILE_UNSAFE:${relativePath}`);
  try {
    return JSON.parse(fs.readFileSync(absolute, "utf8"));
  } catch {
    throw new Error(`RUNTIME_JSON_INVALID:${relativePath}`);
  }
}

function listJson(root, directory) {
  const absolute = path.resolve(root, directory);
  let entries;
  try {
    entries = fs.readdirSync(absolute, {withFileTypes: true});
  } catch {
    throw new Error(`RUNTIME_DIRECTORY_MISSING:${directory}`);
  }
  return entries
    .filter((entry) => entry.isFile() && entry.name.endsWith(".json"))
    .map((entry) => `${directory}/${entry.name}`)
    .sort();
}

function errorSummary(validate) {
  return (validate.errors ?? [])
    .slice(0, 3)
    .map((error) => `${error.keyword}@${error.instancePath || "/"}`)
    .join(",");
}

function createRegistry(root) {
  const ajv = new Ajv2020({
    allErrors: true,
    logger: false,
    strict: true,
    strictRequired: false,
  });
  addFormats(ajv);
  const schemaFiles = [...listJson(root, "schemas/runtime"), "schemas/official-source.schema.json"];
  for (const file of schemaFiles) {
    const schema = readJson(root, file);
    if (!schema.$id?.startsWith(RUNTIME_SCHEMA_PREFIX) && !(file === "schemas/official-source.schema.json" && schema.$id === "https://github.com/maojiebc/majia-chatcut-koubo/schemas/official-source.schema.json")) {
      throw new Error(`RUNTIME_SCHEMA_ID_INVALID:${file}`);
    }
    if (!ajv.validateSchema(schema)) {
      throw new Error(`RUNTIME_SCHEMA_META_INVALID:${file}`);
    }
    ajv.addSchema(schema);
  }
  return {ajv, schemaFiles};
}

function validateDocument(ajv, root, file, {expectValid = true} = {}) {
  const document = readJson(root, file);
  const validate = typeof document.$schema === "string"
    ? ajv.getSchema(document.$schema)
    : null;
  if (!validate) throw new Error(`RUNTIME_SCHEMA_NOT_REGISTERED:${file}`);
  const valid = validate(document);
  if (valid !== expectValid) {
    const expectation = expectValid ? "VALID" : "INVALID";
    throw new Error(`RUNTIME_EXPECTED_${expectation}:${file}:${errorSummary(validate)}`);
  }
  if (expectValid && document.$schema?.endsWith("/source-inventory.schema.json")) {
    assertSourceInventoryBindings(document);
  }
  return document;
}

function validateGenerated(ajv, label, value) {
  if (!value) return 0;
  const validate = ajv.getSchema(value.$schema);
  if (!validate || !validate(value)) {
    throw new Error(`RUNTIME_GENERATED_INVALID:${label}:${validate ? errorSummary(validate) : "schema-missing"}`);
  }
  if (value.$schema?.endsWith("/source-inventory.schema.json")) {
    assertSourceInventoryBindings(value);
  }
  return 1;
}

function requireCondition(condition, code) {
  if (!condition) throw new Error(code);
}

function runAudit(root) {
  const {ajv, schemaFiles} = createRegistry(root);
  const templateFiles = listJson(root, "templates/runtime");
  const profileFiles = listJson(root, "profiles");
  const reportFiles = fs.existsSync(path.join(root, "reports"))
    ? listJson(root, "reports")
    : [];

  let documents = 0;
  for (const file of [...templateFiles, ...profileFiles, ...reportFiles]) {
    validateDocument(ajv, root, file);
    documents += 1;
  }
  validateDocument(ajv, root, "fixtures/runtime/negative/high-risk-auto.invalid.json", {
    expectValid: false,
  });
  documents += 1;

  const profileIds = profileFiles.map((file) => readJson(root, file).id);
  requireCondition(new Set(profileIds).size === 4, "RUNTIME_PROFILE_IDS_NOT_UNIQUE");
  requireCondition(
    ["balanced-stable", "tight-short", "trust-longform", "screen-demo"]
      .every((id) => profileIds.includes(id)),
    "RUNTIME_PROFILE_SET_INCOMPLETE",
  );
  for (const file of profileFiles) {
    const profile = readJson(root, file);
    for (const treatment of ["restructure", "broll", "motionGraphics", "music", "generatedMedia", "export"]) {
      requireCondition(profile.defaults?.treatments?.[treatment] === false, `RUNTIME_PROFILE_DEFAULT_UNSAFE:${file}`);
    }
  }

  const suite = validateDocument(ajv, root, "fixtures/runtime/scenarios.json");
  documents += 1;
  const scenarioIds = suite.scenarios.map((scenario) => scenario.scenarioId);
  requireCondition(
    scenarioIds.length === new Set(scenarioIds).size,
    "RUNTIME_SCENARIO_IDS_NOT_UNIQUE",
  );
  requireCondition(
    [...REQUIRED_SCENARIOS].every((id) => scenarioIds.includes(id)),
    "RUNTIME_REQUIRED_SCENARIOS_MISSING",
  );

  let generatedDocuments = 0;
  for (const scenario of suite.scenarios) {
    const result = runFakeOneClickSession(scenario);
    requireCondition(
      result.manifest.stage === scenario.expectedStage,
      `RUNTIME_SCENARIO_STAGE_MISMATCH:${scenario.scenarioId}`,
    );
    generatedDocuments += validateGenerated(ajv, `${scenario.scenarioId}:brief`, result.brief);
    generatedDocuments += validateGenerated(ajv, `${scenario.scenarioId}:manifest`, result.manifest);
    generatedDocuments += validateGenerated(ajv, `${scenario.scenarioId}:decisions`, result.decisionLog);
    generatedDocuments += validateGenerated(ajv, `${scenario.scenarioId}:handoff`, result.handoff);
    for (const checkpoint of result.checkpoints) {
      generatedDocuments += validateGenerated(ajv, `${scenario.scenarioId}:checkpoint`, checkpoint);
    }
    assertEvidenceClaims(result.handoff);
  }

  return {
    ok: true,
    schemas: schemaFiles.length,
    documents,
    scenarios: suite.scenarios.length,
    generatedDocuments,
    evidenceBoundary: "offline-contracts-only",
    liveChatCutVerified: false,
  };
}

const options = parseArguments(process.argv.slice(2));
try {
  const result = runAudit(options.root);
  if (options.json) {
    process.stdout.write(`${JSON.stringify(result)}\n`);
  } else {
    process.stdout.write(
      `runtime fixture audit passed: ${result.schemas} schema(s), ${result.documents} fixture/template/profile document(s), ${result.scenarios} scenario(s), ${result.generatedDocuments} generated document(s); evidence=${result.evidenceBoundary}\n`,
    );
  }
} catch (error) {
  const message = typeof error?.message === "string" ? error.message : "RUNTIME_FIXTURE_AUDIT_FAILED";
  const safe = /^RUNTIME_[A-Z0-9_]+(?::[A-Za-z0-9._/<>,-]+)*$/u.test(message)
    ? message
    : "RUNTIME_FIXTURE_AUDIT_FAILED";
  process.stderr.write(`${safe}: runtime fixture audit failed\n`);
  if (process.env.MAJIA_RUNTIME_DEBUG === "1") {
    const detail = message.replaceAll(options.root, "<root>").replace(/[\r\n]+/gu, " ").slice(0, 400);
    process.stderr.write(`debug: ${detail}\n`);
  }
  process.exitCode = 1;
}
