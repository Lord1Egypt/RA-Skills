#!/usr/bin/env node

import path from "node:path";
import {fileURLToPath} from "node:url";

import {
  RuleRegistryError,
  auditRuleRegistry,
} from "../src/rules/rule-registry.mjs";

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
    "Usage: node scripts/validate-rule-registry.mjs "
      + "[--root <repository-root>] [--registry <relative-json>] "
      + "[--overrides <relative-json>] [--format text|json]",
  );
  if (message) console.error(message);
  process.exit(EXIT.USAGE_OR_OPERATIONAL);
}

function parseArguments(argv) {
  const options = {
    root: DEFAULT_ROOT,
    registryPath: "rules/registry.json",
    overridesPath: undefined,
    format: "text",
  };
  const seen = new Set();
  for (let index = 0; index < argv.length; index += 1) {
    const option = argv[index];
    if (!["--root", "--registry", "--overrides", "--format"].includes(option)) {
      usage("unknown or unsupported option");
    }
    if (seen.has(option)) usage(`duplicate option: ${option}`);
    seen.add(option);
    const value = argv[index + 1];
    if (!value || value.startsWith("--")) usage(`${option} requires a value`);
    if (option === "--root") options.root = path.resolve(value);
    if (option === "--registry") options.registryPath = value;
    if (option === "--overrides") options.overridesPath = value;
    if (option === "--format") {
      if (!["text", "json"].includes(value)) usage("unsupported format");
      options.format = value;
    }
    index += 1;
  }
  return options;
}

function printText(report) {
  if (report.findings.length > 0) {
    for (const item of report.findings) {
      const suffix = item.ruleId ? ` rule=${item.ruleId}` : "";
      console.error(
        `FAIL ${item.code} ${item.pointer}${suffix}: ${item.message}`,
      );
    }
    console.error(
      `rule registry audit failed: ${report.summary.errors} finding(s)`,
    );
    return;
  }
  console.log(
    `rule registry audit passed: ${report.summary.rules} rule(s), `
      + `${report.summary.domains} domain(s), `
      + `${report.summary.runtimeRules} runtime / `
      + `${report.summary.contractRules} contract`,
  );
}

let options;
try {
  options = parseArguments(process.argv.slice(2));
  const report = auditRuleRegistry(options);
  if (options.format === "json") {
    process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
  } else {
    printText(report);
  }
  process.exitCode =
    report.findings.length === 0 ? EXIT.OK : EXIT.FINDINGS;
} catch (error) {
  const code = error instanceof RuleRegistryError
    ? error.code
    : "RULE_REGISTRY_OPERATIONAL_ERROR";
  console.error(`rule registry audit unavailable: ${code}`);
  process.exitCode = EXIT.USAGE_OR_OPERATIONAL;
}
