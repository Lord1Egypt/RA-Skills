#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

import Ajv2020 from "ajv/dist/2020.js";
import addFormats from "ajv-formats";

import {auditDistributionPack} from "../src/distribution/distribution-pack.mjs";

const DEFAULT_ROOT = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
);

class DistributionError extends Error {
  constructor(code, message) {
    super(message);
    this.code = code;
  }
}

function usage() {
  return "usage: validate-distribution-pack --pack <path> --as-of <YYYY-MM-DD> [--root <path>] [--format text|json]";
}

function parseArguments(argv) {
  const values = new Map();
  const allowed = new Set(["--as-of", "--format", "--pack", "--root"]);
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
      throw new DistributionError("DISTRIBUTION_USAGE", usage());
    }
    values.set(option, value);
  }
  if (!values.has("--pack") || !values.has("--as-of")) {
    throw new DistributionError("DISTRIBUTION_USAGE", usage());
  }
  const format = values.get("--format") ?? "text";
  if (
    !["text", "json"].includes(format)
    || !/^\d{4}-\d{2}-\d{2}$/u.test(values.get("--as-of"))
  ) {
    throw new DistributionError("DISTRIBUTION_USAGE", usage());
  }
  return {
    root: values.get("--root") ?? DEFAULT_ROOT,
    pack: values.get("--pack"),
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

function resolveInput(rootValue, relativeValue) {
  let root;
  try {
    root = fs.realpathSync(path.resolve(rootValue));
  } catch {
    throw new DistributionError(
      "DISTRIBUTION_ROOT_UNREADABLE",
      "distribution root is unreadable",
    );
  }
  if (
    typeof relativeValue !== "string"
    || relativeValue.includes("\\")
    || path.posix.isAbsolute(relativeValue)
    || path.posix.normalize(relativeValue) !== relativeValue
    || relativeValue.startsWith("../")
  ) {
    throw new DistributionError(
      "DISTRIBUTION_PATH_UNSAFE",
      "distribution pack path is unsafe",
    );
  }
  const candidate = path.resolve(root, relativeValue);
  if (!inside(root, candidate)) {
    throw new DistributionError(
      "DISTRIBUTION_PATH_UNSAFE",
      "distribution pack path is unsafe",
    );
  }
  let stat;
  try {
    stat = fs.lstatSync(candidate);
  } catch {
    throw new DistributionError(
      "DISTRIBUTION_PACK_MISSING",
      "distribution pack is missing",
    );
  }
  if (stat.isSymbolicLink() || !stat.isFile()) {
    throw new DistributionError(
      "DISTRIBUTION_PACK_UNSAFE",
      "distribution pack must be a regular non-symlink file",
    );
  }
  const canonical = fs.realpathSync(candidate);
  if (!inside(root, canonical)) {
    throw new DistributionError(
      "DISTRIBUTION_PATH_UNSAFE",
      "distribution pack path is unsafe",
    );
  }
  return {root, absolutePath: canonical};
}

function readJson(absolutePath) {
  try {
    return JSON.parse(fs.readFileSync(absolutePath, "utf8"));
  } catch {
    throw new DistributionError(
      "DISTRIBUTION_JSON_INVALID",
      "distribution pack is invalid JSON",
    );
  }
}

function requireSchema(root, pack) {
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
    "distribution-pack.schema.json",
  ]) {
    ajv.addSchema(readJson(path.join(root, "schemas", name)));
  }
  const validate = ajv.getSchema(
    "https://github.com/maojiebc/majia-chatcut-koubo/schemas/distribution-pack.schema.json",
  );
  if (!validate(pack)) {
    throw new DistributionError(
      "DISTRIBUTION_SCHEMA_INVALID",
      "distribution pack violates its schema",
    );
  }
}

try {
  const options = parseArguments(process.argv.slice(2));
  const input = resolveInput(options.root, options.pack);
  const pack = readJson(input.absolutePath);
  requireSchema(input.root, pack);
  const report = auditDistributionPack(pack, {asOf: options.asOf});
  if (options.format === "json") {
    process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
  } else {
    process.stdout.write(
      `distribution pack audit ${report.status}: ${report.summary.errors} error(s), ${report.summary.warnings} warning(s)\n`,
    );
  }
  process.exitCode = report.status === "passed" ? 0 : 1;
} catch (error) {
  const code = error instanceof DistributionError
    ? error.code
    : "DISTRIBUTION_AUDIT_FAILED";
  const message = error instanceof DistributionError
    ? error.message
    : "distribution pack audit failed";
  process.stderr.write(`${code}: ${message}\n`);
  process.exitCode = code === "DISTRIBUTION_USAGE" ? 2 : 1;
}
