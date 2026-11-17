#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

import Ajv2020 from "ajv/dist/2020.js";
import addFormats from "ajv-formats";

import {
  SrtBridgeError,
  diffSrtBridge,
  exportSrtBridge,
} from "../src/planning/srt-bridge.mjs";

const DEFAULT_ROOT = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
);

function usage() {
  return [
    "usage:",
    "  srt-bridge export --caption-plan <path> --srt-out <path> --sidecar-out <path> [--root <path>]",
    "  srt-bridge diff --srt <path> --sidecar <path> [--root <path>] [--format text|json]",
  ].join("\n");
}

function parseArguments(argv) {
  const [mode, ...rest] = argv;
  if (!["export", "diff"].includes(mode)) {
    throw new SrtBridgeError("SRT_USAGE", usage());
  }
  const values = new Map();
  for (let index = 0; index < rest.length; index += 2) {
    const option = rest[index];
    const value = rest[index + 1];
    if (
      !option?.startsWith("--")
      || option.includes("=")
      || value === undefined
      || value.startsWith("--")
      || values.has(option)
    ) {
      throw new SrtBridgeError("SRT_USAGE", usage());
    }
    values.set(option, value);
  }
  const allowed = mode === "export"
    ? new Set(["--root", "--caption-plan", "--srt-out", "--sidecar-out"])
    : new Set(["--root", "--srt", "--sidecar", "--format"]);
  for (const option of values.keys()) {
    if (!allowed.has(option)) {
      throw new SrtBridgeError("SRT_USAGE", usage());
    }
  }
  const required = mode === "export"
    ? ["--caption-plan", "--srt-out", "--sidecar-out"]
    : ["--srt", "--sidecar"];
  if (required.some((option) => !values.has(option))) {
    throw new SrtBridgeError("SRT_USAGE", usage());
  }
  const format = values.get("--format") ?? "text";
  if (!["text", "json"].includes(format)) {
    throw new SrtBridgeError("SRT_USAGE", usage());
  }
  return {
    mode,
    root: values.get("--root") ?? DEFAULT_ROOT,
    format,
    values,
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

function normalizeRelative(value) {
  if (
    typeof value !== "string"
    || value.length === 0
    || value.includes("\\")
    || path.posix.isAbsolute(value)
  ) {
    return null;
  }
  const normalized = path.posix.normalize(value);
  if (
    normalized === "."
    || normalized === ".."
    || normalized.startsWith("../")
    || normalized !== value
  ) {
    return null;
  }
  return normalized;
}

function canonicalRoot(value) {
  try {
    return fs.realpathSync(path.resolve(value));
  } catch {
    throw new SrtBridgeError(
      "SRT_ROOT_UNREADABLE",
      "SRT bridge root is unreadable",
    );
  }
}

function inputPath(root, value) {
  const relative = normalizeRelative(value);
  if (!relative) {
    throw new SrtBridgeError("SRT_PATH_UNSAFE", "SRT input path is unsafe");
  }
  const candidate = path.resolve(root, relative);
  if (!inside(root, candidate)) {
    throw new SrtBridgeError("SRT_PATH_UNSAFE", "SRT input path is unsafe");
  }
  let stat;
  try {
    stat = fs.lstatSync(candidate);
  } catch {
    throw new SrtBridgeError("SRT_INPUT_MISSING", "SRT input is missing");
  }
  if (stat.isSymbolicLink() || !stat.isFile()) {
    throw new SrtBridgeError(
      "SRT_INPUT_UNSAFE",
      "SRT input must be a regular non-symlink file",
    );
  }
  const canonical = fs.realpathSync(candidate);
  if (!inside(root, canonical)) {
    throw new SrtBridgeError("SRT_PATH_UNSAFE", "SRT input path is unsafe");
  }
  return canonical;
}

function outputPath(root, value) {
  const relative = normalizeRelative(value);
  if (!relative) {
    throw new SrtBridgeError("SRT_PATH_UNSAFE", "SRT output path is unsafe");
  }
  const candidate = path.resolve(root, relative);
  if (!inside(root, candidate)) {
    throw new SrtBridgeError("SRT_PATH_UNSAFE", "SRT output path is unsafe");
  }
  let parent;
  try {
    parent = fs.realpathSync(path.dirname(candidate));
  } catch {
    throw new SrtBridgeError(
      "SRT_OUTPUT_PARENT_MISSING",
      "SRT output parent must already exist",
    );
  }
  if (!inside(root, parent)) {
    throw new SrtBridgeError("SRT_PATH_UNSAFE", "SRT output path is unsafe");
  }
  try {
    const stat = fs.lstatSync(candidate);
    if (stat.isSymbolicLink() || !stat.isFile()) {
      throw new SrtBridgeError(
        "SRT_OUTPUT_UNSAFE",
        "SRT output target is not a regular file",
      );
    }
  } catch (error) {
    if (error instanceof SrtBridgeError) throw error;
    if (error?.code !== "ENOENT") {
      throw new SrtBridgeError(
        "SRT_OUTPUT_UNSAFE",
        "SRT output target cannot be inspected",
      );
    }
  }
  return candidate;
}

function readText(absolutePath) {
  try {
    return fs.readFileSync(absolutePath, "utf8");
  } catch {
    throw new SrtBridgeError("SRT_INPUT_UNREADABLE", "SRT input is unreadable");
  }
}

function readJson(absolutePath) {
  try {
    return JSON.parse(readText(absolutePath));
  } catch (error) {
    if (error instanceof SrtBridgeError) throw error;
    throw new SrtBridgeError(
      "SRT_JSON_INVALID",
      "SRT bridge JSON input is invalid",
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
    "caption-plan.schema.json",
    "srt-sidecar.schema.json",
  ]) {
    ajv.addSchema(readJson(path.join(root, "schemas", name)));
  }
  return {
    captionPlan: ajv.getSchema(
      "https://github.com/maojiebc/majia-chatcut-koubo/schemas/caption-plan.schema.json",
    ),
    sidecar: ajv.getSchema(
      "https://github.com/maojiebc/majia-chatcut-koubo/schemas/srt-sidecar.schema.json",
    ),
  };
}

function requireValid(validate, document, code) {
  if (!validate(document)) {
    throw new SrtBridgeError(code, "SRT bridge JSON input violates its schema");
  }
}

function run(options) {
  const root = canonicalRoot(options.root);
  const validate = validators(root);
  if (options.mode === "export") {
    const captionPlan = readJson(inputPath(
      root,
      options.values.get("--caption-plan"),
    ));
    requireValid(validate.captionPlan, captionPlan, "SRT_CAPTION_PLAN_INVALID");
    const exported = exportSrtBridge(captionPlan);
    requireValid(validate.sidecar, exported.sidecar, "SRT_SIDECAR_INVALID");
    const srtOutput = outputPath(root, options.values.get("--srt-out"));
    const sidecarOutput = outputPath(
      root,
      options.values.get("--sidecar-out"),
    );
    fs.writeFileSync(srtOutput, exported.srt, {encoding: "utf8", flag: "w"});
    fs.writeFileSync(
      sidecarOutput,
      `${JSON.stringify(exported.sidecar, null, 2)}\n`,
      {encoding: "utf8", flag: "w"},
    );
    return {
      status: "exported",
      bridgeId: exported.sidecar.bridgeId,
      cues: exported.sidecar.cues.length,
    };
  }
  const sidecar = readJson(inputPath(root, options.values.get("--sidecar")));
  requireValid(validate.sidecar, sidecar, "SRT_SIDECAR_INVALID");
  return diffSrtBridge({
    srt: readText(inputPath(root, options.values.get("--srt"))),
    sidecar,
  });
}

try {
  const options = parseArguments(process.argv.slice(2));
  const report = run(options);
  if (options.format === "json") {
    process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
  } else if (report.status === "exported") {
    process.stdout.write(`SRT bridge exported: ${report.cues} cue(s)\n`);
  } else {
    process.stdout.write(
      `SRT diff ${report.status}: ${report.summary.candidates} candidate(s)\n`,
    );
  }
} catch (error) {
  const code = error instanceof SrtBridgeError
    ? error.code
    : "SRT_OPERATION_FAILED";
  const message = error instanceof SrtBridgeError
    ? error.message
    : "SRT bridge operation failed";
  process.stderr.write(`${code}: ${message}\n`);
  process.exitCode = code === "SRT_USAGE" ? 2 : 1;
}
