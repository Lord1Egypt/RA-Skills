#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

import Ajv2020 from "ajv/dist/2020.js";
import addFormats from "ajv-formats";

import {
  auditCapabilityProfile,
} from "../src/execution/capability-profile.mjs";

const DEFAULT_ROOT = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
);

class CapabilityError extends Error {
  constructor(code, message) {
    super(message);
    this.code = code;
  }
}

function usage() {
  return "usage: validate-capability-profile --profile <path> --as-of <ISO-date-time> [--root <path>] [--format text|json]";
}

function parseArguments(argv) {
  const values = new Map();
  const allowed = new Set(["--as-of", "--format", "--profile", "--root"]);
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
      throw new CapabilityError("CAPABILITY_USAGE", usage());
    }
    values.set(option, value);
  }
  if (!values.has("--profile") || !values.has("--as-of")) {
    throw new CapabilityError("CAPABILITY_USAGE", usage());
  }
  const format = values.get("--format") ?? "text";
  if (
    !["text", "json"].includes(format)
    || !Number.isFinite(Date.parse(values.get("--as-of")))
  ) {
    throw new CapabilityError("CAPABILITY_USAGE", usage());
  }
  return {
    root: values.get("--root") ?? DEFAULT_ROOT,
    profile: values.get("--profile"),
    asOf: values.get("--as-of"),
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
    throw new CapabilityError(
      "CAPABILITY_PATH_UNSAFE",
      "capability profile path is unsafe",
    );
  }
  const candidate = path.resolve(root, relativeValue);
  if (!inside(root, candidate)) {
    throw new CapabilityError(
      "CAPABILITY_PATH_UNSAFE",
      "capability profile path is unsafe",
    );
  }
  let stat;
  try {
    stat = fs.lstatSync(candidate);
  } catch {
    throw new CapabilityError(
      "CAPABILITY_PROFILE_MISSING",
      "capability profile is missing",
    );
  }
  if (stat.isSymbolicLink() || !stat.isFile()) {
    throw new CapabilityError(
      "CAPABILITY_PROFILE_UNSAFE",
      "capability profile must be a regular non-symlink file",
    );
  }
  const canonical = fs.realpathSync(candidate);
  if (!inside(root, canonical)) {
    throw new CapabilityError(
      "CAPABILITY_PATH_UNSAFE",
      "capability profile path is unsafe",
    );
  }
  return canonical;
}

function readJson(absolutePath, label) {
  try {
    return JSON.parse(fs.readFileSync(absolutePath, "utf8"));
  } catch {
    throw new CapabilityError(
      "CAPABILITY_JSON_INVALID",
      `${label} is invalid JSON`,
    );
  }
}

function validateSchema(root, profile) {
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
    "capability-profile.schema.json",
  ]) {
    ajv.addSchema(readJson(path.join(root, "schemas", name), name));
  }
  const validate = ajv.getSchema(
    "https://github.com/maojiebc/majia-chatcut-koubo/schemas/capability-profile.schema.json",
  );
  if (!validate(profile)) {
    throw new CapabilityError(
      "CAPABILITY_SCHEMA_INVALID",
      "capability profile violates its schema",
    );
  }
}

try {
  const options = parseArguments(process.argv.slice(2));
  let root;
  try {
    root = fs.realpathSync(path.resolve(options.root));
  } catch {
    throw new CapabilityError(
      "CAPABILITY_ROOT_UNREADABLE",
      "capability root is unreadable",
    );
  }
  const profile = readJson(resolveInput(root, options.profile), "profile");
  validateSchema(root, profile);
  const report = auditCapabilityProfile(
    profile,
    {asOf: options.asOf},
  );
  if (options.format === "json") {
    process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
  } else {
    process.stdout.write(
      `capability profile ${report.status}: ${report.effectiveStatus}, live=${report.liveAllowed}, ${report.summary.errors} error(s)\n`,
    );
  }
  process.exitCode = report.status === "passed" ? 0 : 1;
} catch (error) {
  const code = error instanceof CapabilityError
    ? error.code
    : "CAPABILITY_AUDIT_FAILED";
  const message = error instanceof CapabilityError
    ? error.message
    : "capability profile audit failed";
  process.stderr.write(`${code}: ${message}\n`);
  process.exitCode = code === "CAPABILITY_USAGE" ? 2 : 1;
}
