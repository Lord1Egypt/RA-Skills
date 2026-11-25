import { test } from "node:test";
import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { build, extractVariables } from "../scripts/generate.js";

const DIR = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(DIR, "..");

const DESC = "Write a weekly summary of the sales report for managers, output as markdown. Include a section about the pipeline status.";

test("extracts variables and format", () => {
  const r = build(DESC);
  assert.equal(r.format, "Markdown");
  assert.ok(r.variables.length >= 1, "expected at least one variable");
  assert.ok(r.template.includes("# ROLE"));
  assert.ok(r.template.includes("{{"));
});

test("short input warns", () => {
  const r = build("summarize stuff");
  assert.ok(r.warnings.length >= 1);
});

test("quoted phrases become variables", () => {
  const vars = extractVariables(`Convert "invoice date" into ISO format`);
  assert.ok(vars.some((v) => v.name === "invoice_date"));
});

test("cli stdin mode works, exit 0 or 1 with json", () => {
  try {
    const out = execFileSync("node", ["scripts/generate.js", "-"], { cwd: ROOT, input: DESC, encoding: "utf8" });
    const j = JSON.parse(out);
    assert.ok(j.template);
  } catch (e) {
    assert.equal(e.status, 1);
    assert.ok(JSON.parse(e.stdout).template);
  }
});
