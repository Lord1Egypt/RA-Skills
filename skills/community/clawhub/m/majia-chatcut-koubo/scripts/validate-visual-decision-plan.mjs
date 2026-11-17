#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

import Ajv2020 from "ajv/dist/2020.js";
import addFormats from "ajv-formats";

import {
  auditVisualDecisionPlan,
} from "../src/planning/visual-decision-plan.mjs";

const DEFAULT_ROOT = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
);

class VisualDecisionError extends Error {
  constructor(code, message) {
    super(message);
    this.code = code;
  }
}

function usage() {
  return "usage: validate-visual-decision-plan --plan <path> [--root <path>] [--format text|json]";
}

function parseArguments(argv) {
  const values = new Map();
  const allowed = new Set(["--format", "--plan", "--root"]);
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
      throw new VisualDecisionError("VISUAL_DECISION_USAGE", usage());
    }
    values.set(option, value);
  }
  if (!values.has("--plan")) {
    throw new VisualDecisionError("VISUAL_DECISION_USAGE", usage());
  }
  const format = values.get("--format") ?? "text";
  if (!["text", "json"].includes(format)) {
    throw new VisualDecisionError("VISUAL_DECISION_USAGE", usage());
  }
  return {
    root: values.get("--root") ?? DEFAULT_ROOT,
    plan: values.get("--plan"),
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

function resolveInput(root, relativeValue) {
  if (
    typeof relativeValue !== "string"
    || relativeValue.includes("\\")
    || path.posix.isAbsolute(relativeValue)
    || path.posix.normalize(relativeValue) !== relativeValue
    || relativeValue.startsWith("../")
  ) {
    throw new VisualDecisionError(
      "VISUAL_DECISION_PATH_UNSAFE",
      "visual decision plan path is unsafe",
    );
  }
  const candidate = path.resolve(root, relativeValue);
  if (!inside(root, candidate)) {
    throw new VisualDecisionError(
      "VISUAL_DECISION_PATH_UNSAFE",
      "visual decision plan path is unsafe",
    );
  }
  let stat;
  try {
    stat = fs.lstatSync(candidate);
  } catch {
    throw new VisualDecisionError(
      "VISUAL_DECISION_INPUT_MISSING",
      "visual decision plan is missing",
    );
  }
  if (stat.isSymbolicLink() || !stat.isFile()) {
    throw new VisualDecisionError(
      "VISUAL_DECISION_INPUT_UNSAFE",
      "visual decision plan must be a regular non-symlink file",
    );
  }
  const canonical = fs.realpathSync(candidate);
  if (!inside(root, canonical)) {
    throw new VisualDecisionError(
      "VISUAL_DECISION_PATH_UNSAFE",
      "visual decision plan path is unsafe",
    );
  }
  return canonical;
}

function readJson(absolutePath, label) {
  try {
    return JSON.parse(fs.readFileSync(absolutePath, "utf8"));
  } catch {
    throw new VisualDecisionError(
      "VISUAL_DECISION_JSON_INVALID",
      `${label} is invalid JSON`,
    );
  }
}

function loadValidator(root) {
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
    "visual-decision-plan.schema.json",
  ]) {
    ajv.addSchema(readJson(path.join(root, "schemas", name), name));
  }
  return ajv.getSchema(
    "https://github.com/maojiebc/majia-chatcut-koubo/schemas/visual-decision-plan.schema.json",
  );
}

try {
  const options = parseArguments(process.argv.slice(2));
  let root;
  try {
    root = fs.realpathSync(path.resolve(options.root));
  } catch {
    throw new VisualDecisionError(
      "VISUAL_DECISION_ROOT_UNREADABLE",
      "visual decision root is unreadable",
    );
  }
  const plan = readJson(
    resolveInput(root, options.plan),
    "visual decision plan",
  );
  const validate = loadValidator(root);
  if (!validate(plan)) {
    throw new VisualDecisionError(
      "VISUAL_DECISION_SCHEMA_INVALID",
      "visual decision plan violates its schema",
    );
  }
  const report = auditVisualDecisionPlan(plan);
  if (options.format === "json") {
    process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
  } else {
    process.stdout.write(
      `visual decision ${report.status}: ${report.summary.segments} segment(s), ${report.summary.candidates} candidate(s), executionAllowed=${report.executionAllowed}, ${report.summary.errors} error(s)\n`,
    );
  }
  process.exitCode = report.status === "passed" ? 0 : 1;
} catch (error) {
  const code = error instanceof VisualDecisionError
    ? error.code
    : "VISUAL_DECISION_FAILED";
  const message = error instanceof VisualDecisionError
    ? error.message
    : "visual decision validation failed";
  process.stderr.write(`${code}: ${message}\n`);
  process.exitCode = code === "VISUAL_DECISION_USAGE" ? 2 : 1;
}
