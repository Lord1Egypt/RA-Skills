import { existsSync, mkdirSync, writeFileSync } from "node:fs";
import { basename, dirname, join, resolve } from "node:path";
import { spawnSync } from "node:child_process";

function parseArgs(argv) {
  const values = new Map();
  for (let index = 0; index < argv.length; index += 2) {
    const key = argv[index];
    const value = argv[index + 1];
    if (!key?.startsWith("--") || !value || value.startsWith("--")) {
      throw new Error(`Invalid argument near ${key ?? "end of command"}`);
    }
    values.set(key.slice(2), value);
  }
  return values;
}

function required(args, name) {
  const value = args.get(name);
  if (!value) throw new Error(`Missing --${name}`);
  return resolve(value);
}

function resolveCli(override) {
  if (override) {
    const candidate = resolve(override);
    if (existsSync(candidate)) return { command: process.execPath, prefix: [candidate] };
    return { command: override, prefix: [] };
  }
  const local = resolve(import.meta.dirname, "../../..", "packages/pixel-asset-cli/dist/pixel-asset.cjs");
  if (existsSync(local)) return { command: process.execPath, prefix: [local] };
  return { command: "pixel-asset", prefix: [] };
}

function parseJson(text) {
  if (!text.trim()) return null;
  try {
    return JSON.parse(text);
  } catch {
    return { raw: text.trim() };
  }
}

function run(cli, command, args) {
  const result = spawnSync(cli.command, [...cli.prefix, command, ...args], { encoding: "utf8" });
  if (result.error?.code === "ENOENT") {
    throw new Error("pixel-asset CLI was not found. Install pixel-asset-compiler or pass --cli <path>.");
  }
  return {
    exitCode: result.status ?? 1,
    output: parseJson(result.stdout),
    error: parseJson(result.stderr),
  };
}

const args = parseArgs(process.argv.slice(2));
const input = required(args, "input");
const output = required(args, "output");
const target = args.get("target") ?? "godot";
if (target !== "godot" && target !== "generic") throw new Error("--target must be godot or generic");
const targetOutput = resolve(args.get("target-output") ?? `${output}-godot`);
const reportPath = resolve(args.get("report") ?? join(dirname(output), `${basename(output)}.workflow.json`));
const cli = resolveCli(args.get("cli"));
const report = {
  schemaVersion: "1.0",
  status: "running",
  input,
  output,
  target,
  targetOutput: target === "godot" ? targetOutput : null,
  failedActions: [],
  phases: {},
};

function finish(status, exitCode) {
  report.status = status;
  mkdirSync(dirname(reportPath), { recursive: true });
  writeFileSync(reportPath, `${JSON.stringify(report, null, 2)}\n`);
  process.stdout.write(`${JSON.stringify({ ...report, report: reportPath }, null, 2)}\n`);
  process.exitCode = exitCode;
}

const inspection = run(cli, "inspect", ["--input", input]);
report.phases.inspect = inspection;
if (inspection.exitCode !== 0) {
  finish("input-required", 2);
} else {
  const compilation = run(cli, "compile", ["--input", input, "--output", output]);
  report.phases.compile = compilation;
  if (compilation.exitCode !== 0) {
    finish("compile-failed", 1);
  } else {
    const audit = run(cli, "audit", ["--input", output]);
    report.phases.audit = audit;
    report.failedActions = audit.output?.failedActions ?? [];
    if (audit.exitCode !== 0 || report.failedActions.length > 0) {
      finish("regeneration-required", 2);
    } else {
      const validation = run(cli, "validate", ["--input", output]);
      report.phases.validate = validation;
      if (validation.exitCode !== 0) {
        finish("validation-failed", 1);
      } else if (target === "generic") {
        finish("ready", 0);
      } else {
        const exported = run(cli, "export", [
          "--target", "godot",
          "--input", output,
          "--output", targetOutput,
        ]);
        report.phases.export = exported;
        finish(exported.exitCode === 0 ? "ready" : "export-failed", exported.exitCode === 0 ? 0 : 1);
      }
    }
  }
}
