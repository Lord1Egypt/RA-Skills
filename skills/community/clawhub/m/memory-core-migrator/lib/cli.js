import { resolve } from "node:path";
import { ADAPTERS, loadRecordsDetailed } from "./adapters.js";
import { auditRecords, atomicWrite, renderMemoryCore, writeJsonl, writeMemoryCore } from "./operations.js";
import { portabilityErrors, preflightPaths } from "./safety.js";
import { RunState } from "./state.js";
import { formatMigratorError, migratorError } from "./errors.js";

const COMMANDS = new Set(["preflight", "normalize", "audit", "render", "run-init", "approve"]);
const VERSION = "0.1.0-rc.4";

function usage() {
  return [
    "Usage: openclaw-memory-migrator <command> [options]",
    "Commands: preflight, normalize, audit, render, run-init, approve",
    "Every command is dry-run unless --apply is set, including run-init and approve.",
    "normalize, audit, and render writes also require --state and --approval.",
    "run-init --apply creates only a local run-state file. approve --apply issues one local token.",
    "Neither command writes memory, exports, or OpenClaw databases.",
    "",
    "Common options:",
    "  --dry-run                         Explicit no-write mode (default)",
    "  --apply                           Perform the write after approval",
    "  --state <run-state.json>          State file required with --apply",
    "  --approval <token>                Exact one-use approval required with --apply",
    "",
    "Audit and accounting options:",
    "  --max-comparisons <integer>       Comparison budget (default: 10000)",
    "  --approximate-threshold <0..1>    Similarity threshold (default: 0.9)",
    "  --require-complete-approximate    Exit 2 when approximate audit is truncated",
    "  --expected-total <integer>        Require an exact accepted-record count",
    "  --json-errors                     Emit structured errors to stderr as JSON",
  ].join("\n");
}

function parseArgs(argv) {
  const [command, ...rest] = argv;
  if (!COMMANDS.has(command)) throw new Error(`${usage()}\nUnknown or missing command: ${command || "(none)"}`);
  const options = { input: [], apply: false, dry_run: false };
  const booleans = new Set(["apply", "dry_run", "require_complete_approximate", "json_errors"]);
  for (let index = 0; index < rest.length; index += 1) {
    const argument = rest[index];
    if (!argument.startsWith("--")) throw new Error(`unexpected argument: ${argument}`);
    const key = argument.slice(2).replaceAll("-", "_");
    if (booleans.has(key)) {
      options[key] = true;
      continue;
    }
    const value = rest[index + 1];
    if (value === undefined || value.startsWith("--")) throw new Error(`${argument} requires a value`);
    index += 1;
    if (key === "input") options.input.push(value);
    else options[key] = value;
  }
  if (options.apply && options.dry_run) {
    throw migratorError("USAGE_ERROR", "--dry-run conflicts with --apply");
  }
  return { command, options };
}

function requireOption(options, name) {
  if (options[name] === undefined || options[name] === null || options[name] === "") {
    throw migratorError("USAGE_ERROR", `--${name.replaceAll("_", "-")} is required`);
  }
}

function nonNegativeInteger(value, name) {
  const parsed = Number(value);
  if (!Number.isSafeInteger(parsed) || parsed < 0) {
    throw migratorError("USAGE_ERROR", `invalid --${name}: expected a non-negative integer`);
  }
  return parsed;
}

function approvalAction(command, output) {
  return `${command}:${resolve(output)}`;
}

async function requireApproval(options, action) {
  requireOption(options, "state");
  requireOption(options, "approval");
  const state = await RunState.load(resolve(options.state));
  await state.consumeApproval(action, options.approval);
  return state;
}

function printJson(value, stdout) {
  stdout.write(`${JSON.stringify(value, null, 2)}\n`);
}

function preflightError(errors) {
  const code = errors.some((error) => error.includes("symbolic link"))
    ? "SYMBOLIC_LINK"
    : errors.some((error) => error.includes("overwrite") || error.includes("already exist"))
      ? "OUTPUT_CONFLICT"
      : "PREFLIGHT_FAILED";
  return migratorError(code, errors.join("; "), { details: { errors } });
}

export async function main(argv = process.argv.slice(2), {
  stdout = process.stdout,
  stderr = process.stderr,
} = {}) {
  const jsonErrors = argv.includes("--json-errors");
  try {
    if (argv.length === 0 || argv[0] === "--help" || argv[0] === "-h") {
      stdout.write(`${usage()}\n`);
      return 0;
    }
    if (argv[0] === "--version" || argv[0] === "-V") {
      stdout.write(`${VERSION}\n`);
      return 0;
    }
    const { command, options } = parseArgs(argv);
    if (command === "run-init") {
      requireOption(options, "state");
      const statePath = resolve(options.state);
      if (!options.apply) {
        printJson({
          dry_run: true,
          command,
          state: statePath,
          would_create_run_state: true,
          writes: "none",
        }, stdout);
        return 0;
      }
      const state = await RunState.create(statePath, options.run_id);
      printJson({ run_id: state.runId, state: statePath }, stdout);
      return 0;
    }
    if (command === "approve") {
      requireOption(options, "state");
      requireOption(options, "action");
      const statePath = resolve(options.state);
      if (!options.apply) {
        printJson({
          dry_run: true,
          command,
          state: statePath,
          action: options.action,
          would_issue_one_use_approval: true,
          writes: "none",
        }, stdout);
        return 0;
      }
      const state = await RunState.load(statePath);
      stdout.write(`${await state.issueApproval(options.action)}\n`);
      return 0;
    }
    if (!options.input.length) throw migratorError("USAGE_ERROR", "--input is required and repeatable");
    const inputs = options.input.map((path) => resolve(path));
    if (command === "preflight") {
      const output = options.output ? resolve(options.output) : null;
      const errors = [...new Set([
        ...options.input.flatMap((path) => portabilityErrors(path, "input")),
        ...(options.output ? portabilityErrors(options.output, "output") : []),
        ...await preflightPaths(inputs, output, { outputKind: options.output_kind || "file" }),
      ])];
      printJson({ ok: errors.length === 0, errors }, stdout);
      return errors.length ? 2 : 0;
    }
    requireOption(options, "adapter");
    if (!ADAPTERS.has(options.adapter)) {
      throw migratorError("USAGE_ERROR", `unknown adapter: ${options.adapter}`);
    }
    if ((command === "normalize" || command === "render") && !options.output) {
      throw migratorError("USAGE_ERROR", "--output is required");
    }
    const output = options.output ? resolve(options.output) : null;
    const errors = [...new Set([
      ...options.input.flatMap((path) => portabilityErrors(path, "input")),
      ...(options.output ? portabilityErrors(options.output, "output") : []),
      ...await preflightPaths(inputs, output, {
        outputKind: command === "render" ? "directory" : "file",
      }),
    ])];
    if (errors.length) throw preflightError(errors);
    const { records, summary: inputSummary } = await loadRecordsDetailed(options.adapter, inputs);

    if (options.expected_total !== undefined) {
      const expectedTotal = nonNegativeInteger(options.expected_total, "expected-total");
      if (records.length !== expectedTotal) {
        throw migratorError(
          "COUNT_MISMATCH",
          `expected total ${expectedTotal}, but accepted ${records.length} records`,
          { details: { expected_total: expectedTotal, accepted: records.length } },
        );
      }
    }

    if (command === "audit") {
      const approximateThreshold = options.approximate_threshold === undefined
        ? 0.9
        : Number(options.approximate_threshold);
      if (!Number.isFinite(approximateThreshold)
        || approximateThreshold < 0
        || approximateThreshold > 1) {
        throw migratorError(
          "USAGE_ERROR",
          "invalid --approximate-threshold: expected a number from 0 to 1",
        );
      }
      const maxComparisons = options.max_comparisons === undefined
        ? 10_000
        : nonNegativeInteger(options.max_comparisons, "max-comparisons");
      const report = auditRecords(records, { approximateThreshold, maxComparisons });
      report.input_summary = inputSummary;
      if (report.approximate_comparisons.truncated) {
        const comparisonMessage = `approximate audit truncated; compared `
          + `${report.approximate_comparisons.performed}/`
          + `${report.approximate_comparisons.total_candidates} candidate pairs `
          + `(coverage ${report.approximate_comparisons.coverage})`;
        if (jsonErrors) {
          stderr.write(`${JSON.stringify({
            code: "AUDIT_TRUNCATED_WARNING",
            message: comparisonMessage,
            next_action: "Increase --max-comparisons or require completeness to fail closed.",
            details: report.approximate_comparisons,
          })}\n`);
        } else {
          stderr.write(`warning: ${comparisonMessage}\n`);
        }
      }
      if (options.require_complete_approximate && report.approximate_comparisons.truncated) {
        printJson(report, stdout);
        stderr.write(formatMigratorError(migratorError(
          "AUDIT_INCOMPLETE",
          "approximate duplicate audit was truncated",
          { details: report.approximate_comparisons },
        ), { json: jsonErrors }));
        return 2;
      }
      if (output && options.apply) {
        const action = approvalAction("audit", output);
        const state = await requireApproval(options, action);
        await atomicWrite(output, `${JSON.stringify(report, null, 2)}\n`);
        await state.completeStep("audit", {
          output, records: records.length, input_summary: inputSummary,
        });
        printJson({
          written: output,
          records: records.length,
          input_summary: inputSummary,
          run_id: state.runId,
        }, stdout);
      } else {
        printJson(report, stdout);
        if (output) stderr.write(`DRY RUN: would write audit report to ${output}\n`);
      }
      return 0;
    }

    const action = approvalAction(command, output);
    if (!options.apply) {
      if (command === "normalize") {
        printJson({
          dry_run: true,
          records: records.length,
          input_summary: inputSummary,
          output,
          approval_action: action,
        }, stdout);
      } else {
        const rendered = renderMemoryCore(records);
        printJson({
          dry_run: true,
          records: records.length,
          input_summary: inputSummary,
          output,
          files: Object.keys(rendered).sort(),
          approval_action: action,
        }, stdout);
      }
      return 0;
    }
    const state = await requireApproval(options, action);
    let files;
    if (command === "normalize") await writeJsonl(records, output);
    else files = await writeMemoryCore(records, output);
    await state.completeStep(command, {
      output,
      records: records.length,
      input_summary: inputSummary,
      ...(files ? { files } : {}),
    });
    printJson({
      written: output,
      records: records.length,
      input_summary: inputSummary,
      run_id: state.runId,
      ...(files ? { files } : {}),
    }, stdout);
    return 0;
  } catch (error) {
    stderr.write(formatMigratorError(error, { json: jsonErrors }));
    return 2;
  }
}
