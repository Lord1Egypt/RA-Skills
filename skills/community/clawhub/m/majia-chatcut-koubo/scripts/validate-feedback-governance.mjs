#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

import Ajv2020 from "ajv/dist/2020.js";
import addFormats from "ajv-formats";

import {
  auditFeedbackEvent,
  auditSuggestedUpdateQueue,
} from "../src/governance/feedback-governance.mjs";

const DEFAULT_ROOT = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
);

class FeedbackError extends Error {
  constructor(code, message) {
    super(message);
    this.code = code;
  }
}

function usage() {
  return "usage: validate-feedback-governance --event <path> --queue <path> [--root <path>] [--format text|json]";
}

function parseArguments(argv) {
  const values = new Map();
  const allowed = new Set(["--event", "--format", "--queue", "--root"]);
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
      throw new FeedbackError("FEEDBACK_USAGE", usage());
    }
    values.set(option, value);
  }
  if (!values.has("--event") || !values.has("--queue")) {
    throw new FeedbackError("FEEDBACK_USAGE", usage());
  }
  const format = values.get("--format") ?? "text";
  if (!["text", "json"].includes(format)) {
    throw new FeedbackError("FEEDBACK_USAGE", usage());
  }
  return {
    root: values.get("--root") ?? DEFAULT_ROOT,
    event: values.get("--event"),
    queue: values.get("--queue"),
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
    throw new FeedbackError(
      "FEEDBACK_PATH_UNSAFE",
      `${label} path is unsafe`,
    );
  }
  const candidate = path.resolve(root, relativeValue);
  if (!inside(root, candidate)) {
    throw new FeedbackError(
      "FEEDBACK_PATH_UNSAFE",
      `${label} path is unsafe`,
    );
  }
  let stat;
  try {
    stat = fs.lstatSync(candidate);
  } catch {
    throw new FeedbackError(
      "FEEDBACK_INPUT_MISSING",
      `${label} is missing`,
    );
  }
  if (stat.isSymbolicLink() || !stat.isFile()) {
    throw new FeedbackError(
      "FEEDBACK_INPUT_UNSAFE",
      `${label} must be a regular non-symlink file`,
    );
  }
  const canonical = fs.realpathSync(candidate);
  if (!inside(root, canonical)) {
    throw new FeedbackError(
      "FEEDBACK_PATH_UNSAFE",
      `${label} path is unsafe`,
    );
  }
  return canonical;
}

function readJson(absolutePath, label) {
  try {
    return JSON.parse(fs.readFileSync(absolutePath, "utf8"));
  } catch {
    throw new FeedbackError(
      "FEEDBACK_JSON_INVALID",
      `${label} is invalid JSON`,
    );
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
    "feedback-event.schema.json",
    "suggested-update-queue.schema.json",
  ]) {
    ajv.addSchema(readJson(path.join(root, "schemas", name), name));
  }
  return {
    event: ajv.getSchema(
      "https://github.com/maojiebc/majia-chatcut-koubo/schemas/feedback-event.schema.json",
    ),
    queue: ajv.getSchema(
      "https://github.com/maojiebc/majia-chatcut-koubo/schemas/suggested-update-queue.schema.json",
    ),
  };
}

try {
  const options = parseArguments(process.argv.slice(2));
  let root;
  try {
    root = fs.realpathSync(path.resolve(options.root));
  } catch {
    throw new FeedbackError(
      "FEEDBACK_ROOT_UNREADABLE",
      "feedback root is unreadable",
    );
  }
  const event = readJson(
    resolveInput(root, options.event, "feedback event"),
    "feedback event",
  );
  const queue = readJson(
    resolveInput(root, options.queue, "suggestion queue"),
    "suggestion queue",
  );
  const registry = readJson(
    path.join(root, "rules/registry.json"),
    "rule registry",
  );
  const validators = loadValidators(root);
  if (!validators.event(event) || !validators.queue(queue)) {
    throw new FeedbackError(
      "FEEDBACK_SCHEMA_INVALID",
      "feedback documents violate their schema",
    );
  }
  const eventReport = auditFeedbackEvent(event, registry);
  const queueReport = auditSuggestedUpdateQueue(queue, registry);
  const errors = eventReport.findings.length + queueReport.findings.length;
  const report = {
    status: errors === 0 ? "passed" : "failed",
    summary: {
      events: 1,
      suggestions: queueReport.summary.suggestions,
      released: queueReport.summary.released,
      errors,
    },
    findings: [...eventReport.findings, ...queueReport.findings],
  };
  if (options.format === "json") {
    process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
  } else {
    process.stdout.write(
      `feedback governance ${report.status}: ${report.summary.events} event(s), ${report.summary.suggestions} suggestion(s), ${errors} error(s)\n`,
    );
  }
  process.exitCode = report.status === "passed" ? 0 : 1;
} catch (error) {
  const code = error instanceof FeedbackError
    ? error.code
    : "FEEDBACK_GOVERNANCE_FAILED";
  const message = error instanceof FeedbackError
    ? error.message
    : "feedback governance failed";
  process.stderr.write(`${code}: ${message}\n`);
  process.exitCode = code === "FEEDBACK_USAGE" ? 2 : 1;
}
