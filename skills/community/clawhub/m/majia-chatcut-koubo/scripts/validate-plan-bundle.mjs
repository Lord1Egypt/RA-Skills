#!/usr/bin/env node

import path from "node:path";
import {fileURLToPath} from "node:url";

import {
  PlanBundleError,
  validatePlanBundle,
} from "../src/planning/plan-bundle-validator.mjs";

const EXIT = Object.freeze({
  OK: 0,
  FINDINGS: 1,
  USAGE_OR_OPERATIONAL: 2,
});
const DEFAULT_ROOT = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
);

function usage(message) {
  console.error(
    "Usage: node scripts/validate-plan-bundle.mjs "
      + "--bundle <relative-json> [--root <repository-root>] "
      + "[--format text|json]",
  );
  if (message) console.error(message);
  process.exit(EXIT.USAGE_OR_OPERATIONAL);
}

function parseArguments(argv) {
  const options = {root: DEFAULT_ROOT, bundlePath: null, format: "text"};
  const seen = new Set();
  for (let index = 0; index < argv.length; index += 1) {
    const option = argv[index];
    if (!["--root", "--bundle", "--format"].includes(option)) {
      usage("unknown or unsupported option");
    }
    if (seen.has(option)) usage(`duplicate option: ${option}`);
    seen.add(option);
    const value = argv[index + 1];
    if (!value || value.startsWith("--")) usage(`${option} requires a value`);
    if (option === "--root") options.root = path.resolve(value);
    if (option === "--bundle") options.bundlePath = value;
    if (option === "--format") {
      if (!["text", "json"].includes(value)) usage("unsupported format");
      options.format = value;
    }
    index += 1;
  }
  if (!options.bundlePath) usage("--bundle is required");
  return options;
}

function printText(report) {
  if (report.findings.length > 0) {
    for (const item of report.findings) {
      console.error(`FAIL ${item.code} ${item.pointer}: ${item.message}`);
    }
    console.error(
      `plan bundle validation failed: ${report.summary.errors} finding(s)`,
    );
  } else {
    console.log(
      `plan bundle validation passed: ${report.summary.documents} document(s)`,
    );
  }
}

try {
  const options = parseArguments(process.argv.slice(2));
  const report = validatePlanBundle(options);
  if (options.format === "json") {
    process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
  } else {
    printText(report);
  }
  process.exitCode = report.findings.length === 0 ? EXIT.OK : EXIT.FINDINGS;
} catch (error) {
  const code = error instanceof PlanBundleError
    ? error.code
    : "PLAN_OPERATIONAL_ERROR";
  console.error(`plan bundle validation unavailable: ${code}`);
  process.exitCode = EXIT.USAGE_OR_OPERATIONAL;
}
