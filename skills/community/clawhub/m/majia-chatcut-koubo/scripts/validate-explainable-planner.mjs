#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

import Ajv2020 from "ajv/dist/2020.js";
import addFormats from "ajv-formats";

import {
  auditExplainableScorecard,
  buildExplainableScorecard,
} from "../src/planning/explainable-planner.mjs";

const DEFAULT_ROOT = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
);

class PlannerError extends Error {
  constructor(code, message) {
    super(message);
    this.code = code;
  }
}

function usage() {
  return "usage: validate-explainable-planner --transcript <path> --edit-plan <path> --expected <path> [--root <path>] [--format text|json]";
}

function parseArguments(argv) {
  const values = new Map();
  const allowed = new Set([
    "--edit-plan",
    "--expected",
    "--format",
    "--root",
    "--transcript",
  ]);
  for (let index = 0; index < argv.length; index += 2) {
    const option = argv[index];
    const value = argv[index + 1];
    if (
      !allowed.has(option)
      || option.includes("=")
      || !value
      || value.startsWith("--")
      || values.has(option)
    ) {
      throw new PlannerError("PLANNER_USAGE", usage());
    }
    values.set(option, value);
  }
  for (const required of ["--transcript", "--edit-plan", "--expected"]) {
    if (!values.has(required)) {
      throw new PlannerError("PLANNER_USAGE", usage());
    }
  }
  const format = values.get("--format") ?? "text";
  if (!["text", "json"].includes(format)) {
    throw new PlannerError("PLANNER_USAGE", usage());
  }
  return {
    root: values.get("--root") ?? DEFAULT_ROOT,
    transcript: values.get("--transcript"),
    editPlan: values.get("--edit-plan"),
    expected: values.get("--expected"),
    format,
  };
}

function inside(root, candidate) {
  const relative = path.relative(root, candidate);
  return relative === ""
    || (
      relative !== ".."
      && !relative.startsWith(`..${path.sep}`)
      && !path.isAbsolute(relative)
    );
}

function resolveInput(root, relativeValue, label) {
  if (
    typeof relativeValue !== "string"
    || relativeValue.includes("\\")
    || path.posix.isAbsolute(relativeValue)
    || path.posix.normalize(relativeValue) !== relativeValue
    || relativeValue.startsWith("../")
  ) {
    throw new PlannerError("PLANNER_PATH_UNSAFE", `${label} path is unsafe`);
  }
  const candidate = path.resolve(root, relativeValue);
  if (!inside(root, candidate)) {
    throw new PlannerError("PLANNER_PATH_UNSAFE", `${label} path is unsafe`);
  }
  let stat;
  try {
    stat = fs.lstatSync(candidate);
  } catch {
    throw new PlannerError("PLANNER_INPUT_MISSING", `${label} is missing`);
  }
  if (stat.isSymbolicLink() || !stat.isFile()) {
    throw new PlannerError(
      "PLANNER_INPUT_UNSAFE",
      `${label} must be a regular non-symlink file`,
    );
  }
  const canonical = fs.realpathSync(candidate);
  if (!inside(root, canonical)) {
    throw new PlannerError("PLANNER_PATH_UNSAFE", `${label} path is unsafe`);
  }
  return canonical;
}

function readJson(absolutePath, label) {
  try {
    return JSON.parse(fs.readFileSync(absolutePath, "utf8"));
  } catch {
    throw new PlannerError("PLANNER_JSON_INVALID", `${label} is invalid JSON`);
  }
}

function loadValidators(root) {
  const ajv = new Ajv2020({
    allErrors: true,
    allowUnionTypes: true,
    logger: false,
    strict: true,
    strictRequired: false,
  });
  addFormats(ajv);
  for (const name of [
    "creator-os-common.schema.json",
    "transcript.schema.json",
    "edit-plan.schema.json",
    "content-scorecard.schema.json",
  ]) {
    ajv.addSchema(readJson(path.join(root, "schemas", name), name));
  }
  return {
    transcript: ajv.getSchema(
      "https://github.com/maojiebc/majia-chatcut-koubo/schemas/transcript.schema.json",
    ),
    editPlan: ajv.getSchema(
      "https://github.com/maojiebc/majia-chatcut-koubo/schemas/edit-plan.schema.json",
    ),
    scorecard: ajv.getSchema(
      "https://github.com/maojiebc/majia-chatcut-koubo/schemas/content-scorecard.schema.json",
    ),
  };
}

try {
  const options = parseArguments(process.argv.slice(2));
  let root;
  try {
    root = fs.realpathSync(path.resolve(options.root));
  } catch {
    throw new PlannerError(
      "PLANNER_ROOT_UNREADABLE",
      "planner root is unreadable",
    );
  }
  const transcript = readJson(
    resolveInput(root, options.transcript, "transcript"),
    "transcript",
  );
  const editPlan = readJson(
    resolveInput(root, options.editPlan, "edit plan"),
    "edit plan",
  );
  const expected = readJson(
    resolveInput(root, options.expected, "expected scorecard"),
    "expected scorecard",
  );
  const validators = loadValidators(root);
  if (
    !validators.transcript(transcript)
    || !validators.editPlan(editPlan)
    || !validators.scorecard(expected)
  ) {
    throw new PlannerError(
      "PLANNER_SCHEMA_INVALID",
      "planner documents violate their schema",
    );
  }
  const generated = buildExplainableScorecard(
    transcript,
    editPlan,
    {scorecardId: expected.scorecardId},
  );
  if (!validators.scorecard(generated)) {
    throw new PlannerError(
      "PLANNER_OUTPUT_SCHEMA_INVALID",
      "generated scorecard violates its schema",
    );
  }
  const report = auditExplainableScorecard(
    expected,
    transcript,
    editPlan,
  );
  if (options.format === "json") {
    process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
  } else {
    process.stdout.write(
      `explainable planner ${report.status}: ${report.findings.length} error(s)\n`,
    );
  }
  process.exitCode = report.status === "passed" ? 0 : 1;
} catch (error) {
  const code = error instanceof PlannerError
    ? error.code
    : "PLANNER_VALIDATION_FAILED";
  const message = error instanceof PlannerError
    ? error.message
    : "planner validation failed";
  process.stderr.write(`${code}: ${message}\n`);
  process.exitCode = code === "PLANNER_USAGE" ? 2 : 1;
}
