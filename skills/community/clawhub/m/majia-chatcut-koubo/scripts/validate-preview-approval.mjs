#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

import Ajv2020 from "ajv/dist/2020.js";
import addFormats from "ajv-formats";

import {
  PreviewApprovalError,
  evaluatePreviewApproval,
} from "../src/planning/preview-approval.mjs";

const DEFAULT_ROOT = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
);

function usage() {
  return [
    "usage: validate-preview-approval",
    "  --preview <path> --approval-log <path>",
    "  --plan-hash <sha256:...> --style-fingerprint <sha256:...>",
    "  --timeline-revision <revision> [--root <path>] [--format text|json]",
  ].join("\n");
}

function parseArguments(argv) {
  const values = new Map();
  const allowed = new Set([
    "--approval-log",
    "--format",
    "--plan-hash",
    "--preview",
    "--root",
    "--style-fingerprint",
    "--timeline-revision",
  ]);
  for (let index = 0; index < argv.length; index += 2) {
    const option = argv[index];
    const value = argv[index + 1];
    if (
      !allowed.has(option)
      || option.includes("=")
      || value === undefined
      || value.startsWith("--")
      || values.has(option)
    ) {
      throw new PreviewApprovalError("PREVIEW_USAGE", usage());
    }
    values.set(option, value);
  }
  for (const option of [
    "--approval-log",
    "--plan-hash",
    "--preview",
    "--style-fingerprint",
    "--timeline-revision",
  ]) {
    if (!values.has(option)) {
      throw new PreviewApprovalError("PREVIEW_USAGE", usage());
    }
  }
  const format = values.get("--format") ?? "text";
  if (!["json", "text"].includes(format)) {
    throw new PreviewApprovalError("PREVIEW_USAGE", usage());
  }
  return {
    root: values.get("--root") ?? DEFAULT_ROOT,
    preview: values.get("--preview"),
    approvalLog: values.get("--approval-log"),
    currentPlanHash: values.get("--plan-hash"),
    currentStyleFingerprint: values.get("--style-fingerprint"),
    currentTimelineRevision: values.get("--timeline-revision"),
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

function canonicalRoot(value) {
  try {
    return fs.realpathSync(path.resolve(value));
  } catch {
    throw new PreviewApprovalError(
      "PREVIEW_ROOT_UNREADABLE",
      "preview root is unreadable",
    );
  }
}

function inputPath(root, value) {
  if (
    typeof value !== "string"
    || value.length === 0
    || value.includes("\\")
    || path.posix.isAbsolute(value)
  ) {
    throw new PreviewApprovalError(
      "PREVIEW_PATH_UNSAFE",
      "preview input path is unsafe",
    );
  }
  const normalized = path.posix.normalize(value);
  if (
    normalized !== value
    || normalized === ".."
    || normalized.startsWith("../")
  ) {
    throw new PreviewApprovalError(
      "PREVIEW_PATH_UNSAFE",
      "preview input path is unsafe",
    );
  }
  const candidate = path.resolve(root, normalized);
  if (!inside(root, candidate)) {
    throw new PreviewApprovalError(
      "PREVIEW_PATH_UNSAFE",
      "preview input path is unsafe",
    );
  }
  let stat;
  try {
    stat = fs.lstatSync(candidate);
  } catch {
    throw new PreviewApprovalError(
      "PREVIEW_INPUT_MISSING",
      "preview input is missing",
    );
  }
  if (stat.isSymbolicLink() || !stat.isFile()) {
    throw new PreviewApprovalError(
      "PREVIEW_INPUT_UNSAFE",
      "preview input must be a regular non-symlink file",
    );
  }
  const canonical = fs.realpathSync(candidate);
  if (!inside(root, canonical)) {
    throw new PreviewApprovalError(
      "PREVIEW_PATH_UNSAFE",
      "preview input path is unsafe",
    );
  }
  return canonical;
}

function readJson(absolutePath) {
  try {
    return JSON.parse(fs.readFileSync(absolutePath, "utf8"));
  } catch {
    throw new PreviewApprovalError(
      "PREVIEW_JSON_INVALID",
      "preview input is invalid JSON",
    );
  }
}

function validators(root) {
  const ajv = new Ajv2020({
    allErrors: true,
    logger: false,
    strict: true,
    strictRequired: false,
  });
  addFormats(ajv);
  for (const name of [
    "creator-os-common.schema.json",
    "preview-bundle.schema.json",
    "approval-log.schema.json",
  ]) {
    ajv.addSchema(readJson(path.join(root, "schemas", name)));
  }
  return {
    preview: ajv.getSchema(
      "https://github.com/maojiebc/majia-chatcut-koubo/schemas/preview-bundle.schema.json",
    ),
    approval: ajv.getSchema(
      "https://github.com/maojiebc/majia-chatcut-koubo/schemas/approval-log.schema.json",
    ),
  };
}

function requireValid(validate, document) {
  if (!validate(document)) {
    throw new PreviewApprovalError(
      "PREVIEW_SCHEMA_INVALID",
      "preview input violates its schema",
    );
  }
}

try {
  const options = parseArguments(process.argv.slice(2));
  const root = canonicalRoot(options.root);
  const validate = validators(root);
  const previewBundle = readJson(inputPath(root, options.preview));
  const approvalLog = readJson(inputPath(root, options.approvalLog));
  requireValid(validate.preview, previewBundle);
  requireValid(validate.approval, approvalLog);
  const report = evaluatePreviewApproval({
    previewBundle,
    approvalLog,
    currentPlanHash: options.currentPlanHash,
    currentStyleFingerprint: options.currentStyleFingerprint,
    currentTimelineRevision: options.currentTimelineRevision,
  });
  if (options.format === "json") {
    process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
  } else {
    process.stdout.write(
      `preview approval gate ${report.status}: ${report.reasons.length} reason(s)\n`,
    );
  }
  process.exitCode = report.canExecute ? 0 : 1;
} catch (error) {
  const code = error instanceof PreviewApprovalError
    ? error.code
    : "PREVIEW_OPERATION_FAILED";
  const message = error instanceof PreviewApprovalError
    ? error.message
    : "preview approval validation failed";
  process.stderr.write(`${code}: ${message}\n`);
  process.exitCode = code === "PREVIEW_USAGE" ? 2 : 1;
}
