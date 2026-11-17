#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

import Ajv2020 from "ajv/dist/2020.js";
import addFormats from "ajv-formats";

import {auditMediaRelease} from "../src/qa/media-release-audit.mjs";

const DEFAULT_ROOT = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
);

class MediaQaError extends Error {
  constructor(code, message) {
    super(message);
    this.code = code;
  }
}

function usage() {
  return "usage: validate-media-release --report <path> [--root <path>] [--format text|json]";
}

function parseArguments(argv) {
  const values = new Map();
  const allowed = new Set(["--format", "--report", "--root"]);
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
      throw new MediaQaError("MEDIA_USAGE", usage());
    }
    values.set(option, value);
  }
  if (!values.has("--report")) {
    throw new MediaQaError("MEDIA_USAGE", usage());
  }
  const format = values.get("--format") ?? "text";
  if (!["text", "json"].includes(format)) {
    throw new MediaQaError("MEDIA_USAGE", usage());
  }
  return {
    root: values.get("--root") ?? DEFAULT_ROOT,
    report: values.get("--report"),
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
    throw new MediaQaError("MEDIA_ROOT_UNREADABLE", "media QA root is unreadable");
  }
}

function inputPath(root, value) {
  if (
    typeof value !== "string"
    || value.length === 0
    || value.includes("\\")
    || path.posix.isAbsolute(value)
  ) {
    throw new MediaQaError("MEDIA_PATH_UNSAFE", "media QA path is unsafe");
  }
  const normalized = path.posix.normalize(value);
  if (
    normalized !== value
    || normalized === ".."
    || normalized.startsWith("../")
  ) {
    throw new MediaQaError("MEDIA_PATH_UNSAFE", "media QA path is unsafe");
  }
  const candidate = path.resolve(root, normalized);
  if (!inside(root, candidate)) {
    throw new MediaQaError("MEDIA_PATH_UNSAFE", "media QA path is unsafe");
  }
  let stat;
  try {
    stat = fs.lstatSync(candidate);
  } catch {
    throw new MediaQaError("MEDIA_REPORT_MISSING", "media QA report is missing");
  }
  if (stat.isSymbolicLink() || !stat.isFile()) {
    throw new MediaQaError(
      "MEDIA_REPORT_UNSAFE",
      "media QA report must be a regular non-symlink file",
    );
  }
  const canonical = fs.realpathSync(candidate);
  if (!inside(root, canonical)) {
    throw new MediaQaError("MEDIA_PATH_UNSAFE", "media QA path is unsafe");
  }
  return canonical;
}

function readJson(absolutePath) {
  try {
    return JSON.parse(fs.readFileSync(absolutePath, "utf8"));
  } catch {
    throw new MediaQaError("MEDIA_JSON_INVALID", "media QA report is invalid JSON");
  }
}

function validateSchema(root, report) {
  const ajv = new Ajv2020({
    allErrors: true,
    logger: false,
    strict: true,
    strictRequired: false,
  });
  addFormats(ajv);
  for (const name of [
    "creator-os-common.schema.json",
    "media-release-report.schema.json",
  ]) {
    ajv.addSchema(readJson(path.join(root, "schemas", name)));
  }
  const validate = ajv.getSchema(
    "https://github.com/maojiebc/majia-chatcut-koubo/schemas/media-release-report.schema.json",
  );
  if (!validate(report)) {
    throw new MediaQaError(
      "MEDIA_SCHEMA_INVALID",
      "media QA report violates its schema",
    );
  }
}

try {
  const options = parseArguments(process.argv.slice(2));
  const root = canonicalRoot(options.root);
  const report = readJson(inputPath(root, options.report));
  validateSchema(root, report);
  const result = auditMediaRelease(report);
  if (options.format === "json") {
    process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
  } else {
    process.stdout.write(
      `media release audit ${result.status}: ${result.summary.errors} error(s)\n`,
    );
  }
  process.exitCode = result.status === "passed" ? 0 : 1;
} catch (error) {
  const code = error instanceof MediaQaError
    ? error.code
    : "MEDIA_AUDIT_FAILED";
  const message = error instanceof MediaQaError
    ? error.message
    : "media release audit failed";
  process.stderr.write(`${code}: ${message}\n`);
  process.exitCode = code === "MEDIA_USAGE" ? 2 : 1;
}
