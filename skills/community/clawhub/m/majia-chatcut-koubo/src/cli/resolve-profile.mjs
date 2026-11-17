#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import {
  ProfileResolutionError,
  resolveProfile,
  toSerializableProfileResolution,
} from "../config/profile-resolver.mjs";

const USAGE = [
  "Usage: node src/cli/resolve-profile.mjs --profile <source.json>",
  "       [--out <resolved.json>] [--trace <merge-trace.json>]",
  "       [--root <profile-root>] [--strict] [--format json|text]",
].join("\n");

function parseArguments(argv) {
  const parsed = {format: "json", strict: false};
  const valueOptions = new Map([
    ["--profile", "profile"],
    ["--out", "out"],
    ["--trace", "trace"],
    ["--root", "root"],
    ["--format", "format"],
  ]);
  const seen = new Set();
  for (let index = 0; index < argv.length; index += 1) {
    const argument = argv[index];
    if (argument === "--help" || argument === "-h") {
      if (seen.has("help")) {
        throw new ProfileResolutionError(
          "PROFILE_CLI_DUPLICATE_ARGUMENT",
          "help option was provided more than once",
        );
      }
      seen.add("help");
      parsed.help = true;
      continue;
    }
    if (argument === "--strict") {
      if (seen.has("strict")) {
        throw new ProfileResolutionError(
          "PROFILE_CLI_DUPLICATE_ARGUMENT",
          "--strict was provided more than once",
        );
      }
      seen.add("strict");
      parsed.strict = true;
      continue;
    }
    const property = valueOptions.get(argument);
    if (!property) {
      throw new ProfileResolutionError(
        "PROFILE_CLI_UNKNOWN_ARGUMENT",
        "unknown or unsupported argument",
      );
    }
    if (seen.has(property)) {
      throw new ProfileResolutionError(
        "PROFILE_CLI_DUPLICATE_ARGUMENT",
        `${argument} was provided more than once`,
      );
    }
    const value = argv[index + 1];
    if (!value || value.startsWith("--")) {
      throw new ProfileResolutionError(
        "PROFILE_CLI_MISSING_VALUE",
        `${argument} requires a value`,
      );
    }
    seen.add(property);
    parsed[property] = value;
    index += 1;
  }
  return parsed;
}

function canonicalizePotentialPath(candidate) {
  const absolute = path.resolve(candidate);
  const missing = [];
  let existing = absolute;
  while (!fs.existsSync(existing)) {
    const parent = path.dirname(existing);
    if (parent === existing) return absolute;
    missing.unshift(path.basename(existing));
    existing = parent;
  }
  return path.join(fs.realpathSync(existing), ...missing);
}

function pathIsInside(root, candidate) {
  const relative = path.relative(root, candidate);
  return relative === ""
    || (!relative.startsWith(`..${path.sep}`)
      && relative !== ".."
      && !path.isAbsolute(relative));
}

function validateOutputTarget({
  target,
  configRoot,
  sourceFiles,
  referencedFiles,
}) {
  const canonical = canonicalizePotentialPath(target);
  if (!pathIsInside(configRoot, canonical) || canonical === configRoot) {
    throw new ProfileResolutionError(
      "PROFILE_CLI_OUTPUT_OUTSIDE_ROOT",
      "output files must stay inside the configured profile root",
    );
  }
  if (sourceFiles.has(canonical)) {
    throw new ProfileResolutionError(
      "PROFILE_CLI_SOURCE_COLLISION",
      "output file would overwrite a profile source",
    );
  }
  if (referencedFiles.has(canonical)) {
    throw new ProfileResolutionError(
      "PROFILE_CLI_REFERENCE_COLLISION",
      "output file would overwrite a referenced profile asset",
    );
  }
  return canonical;
}

function writeJson(file, value) {
  const absolute = path.resolve(file);
  const directory = path.dirname(absolute);
  fs.mkdirSync(directory, {recursive: true});
  const temporary = path.join(
    directory,
    `.${path.basename(absolute)}.${process.pid}.tmp`,
  );
  try {
    fs.writeFileSync(temporary, `${JSON.stringify(value, null, 2)}\n`, {
      encoding: "utf8",
      mode: 0o600,
    });
    fs.renameSync(temporary, absolute);
  } finally {
    try {
      fs.unlinkSync(temporary);
    } catch (error) {
      if (error?.code !== "ENOENT") throw error;
    }
  }
  return absolute;
}

function safeDestinationLabel(file) {
  const absolute = path.resolve(file);
  const relative = path.relative(process.cwd(), absolute);
  if (
    relative === ""
    || (!relative.startsWith(`..${path.sep}`)
      && relative !== ".."
      && !path.isAbsolute(relative))
  ) {
    return relative || path.basename(absolute);
  }
  return "<external-output>";
}

function publicError(error) {
  if (!(error instanceof ProfileResolutionError)) {
    return {
      code: "PROFILE_CLI_IO_ERROR",
      message: "profile resolver could not complete an I/O operation",
    };
  }
  return {
    code: error.code,
    message: error.message,
    ...(typeof error?.details?.pointer === "string"
      ? {pointer: error.details.pointer}
      : {}),
  };
}

function main() {
  let args;
  try {
    args = parseArguments(process.argv.slice(2));
  } catch (error) {
    console.error(JSON.stringify({ok: false, error: publicError(error)}));
    console.error(USAGE);
    return 2;
  }
  if (args.help) {
    console.log(USAGE);
    return 0;
  }
  if (!args.profile) {
    console.error(JSON.stringify({
      ok: false,
      error: {
        code: "PROFILE_CLI_PROFILE_REQUIRED",
        message: "--profile is required",
      },
    }));
    console.error(USAGE);
    return 2;
  }
  if (!["json", "text"].includes(args.format)) {
    console.error(JSON.stringify({
      ok: false,
      error: {
        code: "PROFILE_CLI_INVALID_FORMAT",
        message: "--format must be json or text",
      },
    }));
    return 2;
  }
  if (
    args.out
    && args.trace
    && path.resolve(args.out) === path.resolve(args.trace)
  ) {
    console.error(JSON.stringify({
      ok: false,
      error: {
        code: "PROFILE_CLI_OUTPUT_COLLISION",
        message: "--out and --trace must use different files",
      },
    }));
    return 2;
  }

  try {
    const profileAbsolute = path.resolve(args.profile);
    const requestedRoot = args.root ? path.resolve(args.root) : undefined;
    const resolution = resolveProfile(profileAbsolute, {
      allowedRoot: requestedRoot,
      tracePathMode: "absolute",
      trustMode: args.strict ? "strict" : "migration",
    });
    const profileRoot = resolution.configRoot;
    const sourceFiles = new Set(
      resolution.files.map((file) => canonicalizePotentialPath(file.file)),
    );
    const referencedFiles = new Set();
    if (
      typeof resolution.resolved.terminologyFile === "string"
      && path.isAbsolute(resolution.resolved.terminologyFile)
    ) {
      referencedFiles.add(
        canonicalizePotentialPath(resolution.resolved.terminologyFile),
      );
    }
    let resolvedOutput;
    let traceOutput;
    const outputAbsolute = args.out
      ? validateOutputTarget({
        target: args.out,
        configRoot: profileRoot,
        sourceFiles,
        referencedFiles,
      })
      : undefined;
    const traceAbsolute = args.trace
      ? validateOutputTarget({
        target: args.trace,
        configRoot: profileRoot,
        sourceFiles,
        referencedFiles,
      })
      : undefined;

    if (
      outputAbsolute
      && traceAbsolute
      && outputAbsolute === traceAbsolute
    ) {
      throw new ProfileResolutionError(
        "PROFILE_CLI_OUTPUT_COLLISION",
        "--out and --trace must use different files",
      );
    }

    if (outputAbsolute && resolution.contractStatus !== "valid") {
      throw new ProfileResolutionError(
        "PROFILE_CLI_MIGRATION_OUTPUT_BLOCKED",
        "migration-incomplete profiles cannot be written as resolved output",
      );
    }
    if (outputAbsolute) {
      const portable = toSerializableProfileResolution(resolution, {
        baseDirectory: path.dirname(outputAbsolute),
        externalPathMode: "relative",
        portableRoot: profileRoot,
      });
      resolvedOutput = writeJson(outputAbsolute, portable.resolved);
    }
    if (traceAbsolute) {
      const safe = toSerializableProfileResolution(resolution, {
        baseDirectory: profileRoot,
        externalPathMode: "redact",
      });
      traceOutput = writeJson(traceAbsolute, {
        entryFile: safe.entryFile,
        files: safe.files,
        sources: safe.sources,
        mergeTrace: safe.mergeTrace,
      });
    }

    if (args.format === "text") {
      console.log(
        `OK resolved profile (${resolution.files.length} layer${
          resolution.files.length === 1 ? "" : "s"
        })`,
      );
      if (resolvedOutput) {
        console.log(`resolved: ${safeDestinationLabel(resolvedOutput)}`);
      }
      if (traceOutput) {
        console.log(`trace: ${safeDestinationLabel(traceOutput)}`);
      }
    } else if (resolvedOutput || traceOutput) {
      console.log(JSON.stringify({
        ok: true,
        layers: resolution.files.length,
        trustMode: resolution.trustMode,
        contractStatus: resolution.contractStatus,
        warnings: resolution.warnings.map((warning) => warning.code),
        ...(resolvedOutput
          ? {resolved: safeDestinationLabel(resolvedOutput)}
          : {}),
        ...(traceOutput ? {trace: safeDestinationLabel(traceOutput)} : {}),
      }));
    } else {
      console.log(JSON.stringify({
        ok: true,
        layers: resolution.files.length,
        trustMode: resolution.trustMode,
        contractStatus: resolution.contractStatus,
        warnings: resolution.warnings.map((warning) => warning.code),
      }, null, 2));
    }
    return 0;
  } catch (error) {
    const failure = {ok: false, error: publicError(error)};
    if (args.format === "text") {
      console.error(`FAIL ${failure.error.code}: ${failure.error.message}`);
    } else {
      console.error(JSON.stringify(failure));
    }
    return error instanceof ProfileResolutionError ? 1 : 2;
  }
}

process.exitCode = main();
