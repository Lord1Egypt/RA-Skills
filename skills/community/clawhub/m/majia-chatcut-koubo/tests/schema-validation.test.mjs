import assert from "node:assert/strict";
import {
  mkdir,
  mkdtemp,
  readdir,
  readFile,
  rm,
  symlink,
  writeFile,
} from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import test from "node:test";
import { fileURLToPath } from "node:url";

import {
  EXIT_CODES,
} from "../scripts/validate-all-json.mjs";

const TEST_DIRECTORY = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(TEST_DIRECTORY, "..");
const CLI = path.join(ROOT, "scripts", "validate-all-json.mjs");
const SKIPPED_DIRECTORIES = new Set([
  ".git",
  "coverage",
  "dist",
  "node_modules",
]);

function runCli(...arguments_) {
  return spawnSync(process.execPath, [CLI, ...arguments_], {
    cwd: ROOT,
    encoding: "utf8",
  });
}

async function repositoryJsonPaths() {
  const paths = [];

  async function visit(directory) {
    const entries = await readdir(directory, { withFileTypes: true });
    for (const entry of entries) {
      const absolutePath = path.join(directory, entry.name);
      if (entry.isDirectory() && !SKIPPED_DIRECTORIES.has(entry.name)) {
        await visit(absolutePath);
      } else if (entry.isFile() && entry.name.endsWith(".json")) {
        paths.push(path.relative(ROOT, absolutePath).split(path.sep).join("/"));
      }
    }
  }

  await visit(ROOT);
  return paths.sort();
}

test("baseline scan classifies every repository JSON offline", async () => {
  const result = runCli("--mode", "baseline", "--format", "json");
  assert.equal(
    result.status,
    EXIT_CODES.OK,
    `stderr:\n${result.stderr}\nstdout:\n${result.stdout}`,
  );

  const report = JSON.parse(result.stdout);
  assert.equal(report.offline, true);
  assert.equal(report.summary.errors, 0);
  assert.equal(report.summary.baseline, 0);

  const expectedPaths = await repositoryJsonPaths();
  const reportedPaths = [...new Set(report.files.map((file) => file.path))].sort();
  assert.deepEqual(reportedPaths, expectedPaths);

  const byPath = new Map(report.files.map((file) => [file.path, file]));
  assert.equal(
    byPath.get("assets/compositions.json").schema,
    "https://github.com/maojiebc/majia-chatcut-koubo/schemas/compositions.schema.json",
  );
  assert.equal(
    byPath.get("assets/theme-kit/tokens/layouts.json").schema,
    "https://github.com/maojiebc/majia-chatcut-koubo/schemas/theme-layouts.schema.json",
  );
  assert.equal(
    byPath.get("fixtures/contract/negative/captions.multiline.invalid.json")
      .status,
    "expected-invalid",
  );
});

test("canonical remote $schema identifiers resolve to local files", () => {
  const result = runCli(
    "--input",
    "fixtures/profiles/base/profile.source.json",
    "--format",
    "json",
  );
  assert.equal(
    result.status,
    EXIT_CODES.OK,
    `stderr:\n${result.stderr}\nstdout:\n${result.stdout}`,
  );

  const report = JSON.parse(result.stdout);
  const fixture = report.files.find(
    (file) => file.path === "fixtures/profiles/base/profile.source.json",
  );
  assert.equal(fixture.status, "valid");
  assert.equal(
    fixture.schema,
    "https://github.com/maojiebc/majia-chatcut-koubo/schemas/profile.source.schema.json",
  );
});

test("negative fixture must fail for its declared signature", () => {
  const result = runCli(
    "--input",
    "fixtures/contract/negative/captions.multiline.invalid.json",
    "--format",
    "json",
  );
  assert.equal(
    result.status,
    EXIT_CODES.OK,
    `stderr:\n${result.stderr}\nstdout:\n${result.stdout}`,
  );

  const report = JSON.parse(result.stdout);
  const fixture = report.files.find(
    (file) =>
      file.path ===
      "fixtures/contract/negative/captions.multiline.invalid.json",
  );
  assert.equal(fixture.status, "expected-invalid");
  assert.deepEqual(
    fixture.errors.map((error) => error.signature),
    ["maximum@/pages/0/lines"],
  );
});

test("line-break fixture fails only for the page text pattern", () => {
  const fixturePath =
    "fixtures/contract/negative/captions.linebreak.invalid.json";
  const result = runCli(
    "--input",
    fixturePath,
    "--format",
    "json",
  );
  assert.equal(
    result.status,
    EXIT_CODES.OK,
    `stderr:\n${result.stderr}\nstdout:\n${result.stdout}`,
  );

  const report = JSON.parse(result.stdout);
  const fixture = report.files.find((file) => file.path === fixturePath);
  assert.equal(fixture.status, "expected-invalid");
  assert.deepEqual(
    fixture.errors.map((error) => error.signature),
    ["pattern@/pages/0/text"],
  );
});

test("unexpected invalid data uses stable validation exit code", () => {
  const result = runCli(
    "--input",
    "fixtures/contract/negative/captions.multiline.invalid.json",
    "--expect",
    "valid",
    "--format",
    "json",
  );
  assert.equal(result.status, EXIT_CODES.VALIDATION_FAILED);

  const report = JSON.parse(result.stdout);
  const fixture = report.files.find(
    (file) =>
      file.path ===
      "fixtures/contract/negative/captions.multiline.invalid.json",
  );
  assert.equal(fixture.code, "CONTRACT.INVALID");
  assert.equal(fixture.errors[0].signature, "maximum@/pages/0/lines");
});

test("release mode upgrades explicit baseline debt to a failure", async () => {
  const temporaryRoot = await mkdtemp(
    path.join(os.tmpdir(), "koubo-baseline-test-"),
  );
  const contractDirectory = path.join(
    temporaryRoot,
    "fixtures",
    "contract",
  );
  await mkdir(contractDirectory, { recursive: true });
  await writeFile(
    path.join(contractDirectory, "schema-baseline.json"),
    `${JSON.stringify(
      {
        version: 1,
        entries: [
          {
            path: "known-debt.json",
            kind: "unmapped",
            issue: "TEST-001",
            reason: "exercise release fail-closed behavior",
          },
        ],
      },
      null,
      2,
    )}\n`,
  );
  await writeFile(
    path.join(contractDirectory, "cases.json"),
    `${JSON.stringify({ version: 1, cases: [] }, null, 2)}\n`,
  );
  await writeFile(path.join(temporaryRoot, "known-debt.json"), "{}\n");

  try {
    const baselineResult = runCli(
      "--root",
      temporaryRoot,
      "--mode",
      "baseline",
      "--format",
      "json",
    );
    assert.equal(baselineResult.status, EXIT_CODES.OK);
    assert.equal(JSON.parse(baselineResult.stdout).summary.baseline, 1);

    const releaseResult = runCli(
      "--root",
      temporaryRoot,
      "--mode",
      "release",
      "--format",
      "json",
    );
    assert.equal(releaseResult.status, EXIT_CODES.VALIDATION_FAILED);
    assert.equal(JSON.parse(releaseResult.stdout).summary.baseline, 1);
  } finally {
    await rm(temporaryRoot, { force: true, recursive: true });
  }
});

test("invalid CLI usage has stable exit code 2", () => {
  const result = runCli("--not-a-real-option");
  assert.equal(result.status, EXIT_CODES.USAGE_OR_INTERNAL_ERROR);
  assert.match(result.stderr, /unknown argument/u);
});

test("single-value CLI options cannot be repeated", () => {
  const result = runCli("--mode", "release", "--mode", "baseline");
  assert.equal(result.status, EXIT_CODES.USAGE_OR_INTERNAL_ERROR);
  assert.match(result.stderr, /duplicate option: --mode/u);
});

test("internal path errors expose only a stable code", () => {
  const missingRoot = path.join(
    os.tmpdir(),
    `koubo-missing-private-root-${process.pid}`,
  );
  const result = runCli("--root", missingRoot);
  assert.equal(result.status, EXIT_CODES.USAGE_OR_INTERNAL_ERROR);
  assert.match(result.stderr, /internal schema validator error: ENOENT/u);
  assert.doesNotMatch(result.stderr, new RegExp(missingRoot));
});

test("unresolved schema references do not disclose absolute paths", async () => {
  const temporaryRoot = await mkdtemp(
    path.join(os.tmpdir(), "koubo-schema-redaction-"),
  );
  const contractDirectory = path.join(temporaryRoot, "fixtures", "contract");
  await mkdir(contractDirectory, {recursive: true});
  await writeFile(
    path.join(contractDirectory, "schema-baseline.json"),
    `${JSON.stringify({version: 1, entries: []}, null, 2)}\n`,
  );
  await writeFile(
    path.join(contractDirectory, "cases.json"),
    `${JSON.stringify({version: 1, cases: []}, null, 2)}\n`,
  );
  await writeFile(
    path.join(temporaryRoot, "data.json"),
    `${JSON.stringify({
      $schema: "file:///Users/example/private.schema.json",
      value: true,
    })}\n`,
  );

  try {
    const result = runCli(
      "--root",
      temporaryRoot,
      "--format",
      "json",
    );
    assert.equal(result.status, EXIT_CODES.VALIDATION_FAILED);
    assert.doesNotMatch(result.stdout, /\/Users\/example/u);
    const report = JSON.parse(result.stdout);
    const data = report.files.find((file) => file.path === "data.json");
    assert.equal(data.schema, "<unresolved-schema-reference>");
  } finally {
    await rm(temporaryRoot, {force: true, recursive: true});
  }
});

test("invalid JSON reports do not echo private input fragments", async () => {
  const temporaryRoot = await mkdtemp(
    path.join(os.tmpdir(), "koubo-invalid-json-redaction-"),
  );
  const contractDirectory = path.join(temporaryRoot, "fixtures", "contract");
  await mkdir(contractDirectory, {recursive: true});
  await writeFile(
    path.join(contractDirectory, "schema-baseline.json"),
    `${JSON.stringify({version: 1, entries: []}, null, 2)}\n`,
  );
  await writeFile(
    path.join(contractDirectory, "cases.json"),
    `${JSON.stringify({version: 1, cases: []}, null, 2)}\n`,
  );
  await writeFile(
    path.join(temporaryRoot, "data.json"),
    '{"secret":"PRIVATE_JSON_SENTINEL",',
  );

  try {
    const result = runCli("--root", temporaryRoot, "--format", "json");
    assert.equal(result.status, EXIT_CODES.VALIDATION_FAILED);
    assert.doesNotMatch(result.stdout, /PRIVATE_JSON_SENTINEL/u);
    const report = JSON.parse(result.stdout);
    const data = report.files.find((file) => file.path === "data.json");
    assert.equal(data.code, "CONTRACT.INVALID_JSON");
    assert.equal(data.message, "invalid JSON: INVALID_JSON");
  } finally {
    await rm(temporaryRoot, {force: true, recursive: true});
  }
});

test("schema compile failures do not disclose absolute references", async () => {
  const temporaryRoot = await mkdtemp(
    path.join(os.tmpdir(), "koubo-schema-compile-redaction-"),
  );
  const contractDirectory = path.join(temporaryRoot, "fixtures", "contract");
  const schemaDirectory = path.join(temporaryRoot, "schemas");
  await mkdir(contractDirectory, {recursive: true});
  await mkdir(schemaDirectory, {recursive: true});
  await writeFile(
    path.join(contractDirectory, "schema-baseline.json"),
    `${JSON.stringify({version: 1, entries: []}, null, 2)}\n`,
  );
  await writeFile(
    path.join(contractDirectory, "cases.json"),
    `${JSON.stringify({version: 1, cases: []}, null, 2)}\n`,
  );
  await writeFile(
    path.join(schemaDirectory, "leaky.schema.json"),
    `${JSON.stringify({
      $schema: "https://json-schema.org/draft/2020-12/schema",
      $id: "https://github.com/maojiebc/majia-chatcut-koubo/schemas/leaky.schema.json",
      $ref: "file:///Users/example/private.schema.json",
    }, null, 2)}\n`,
  );

  try {
    const result = runCli("--root", temporaryRoot, "--format", "json");
    assert.equal(result.status, EXIT_CODES.VALIDATION_FAILED);
    assert.doesNotMatch(result.stdout, /\/Users\/example/u);
    const report = JSON.parse(result.stdout);
    const schema = report.files.find(
      (file) => file.path === "schemas/leaky.schema.json",
    );
    assert.equal(schema.code, "SCHEMA.COMPILE_FAILED");
    assert.equal(
      schema.message,
      "schema could not be compiled in the offline registry",
    );
  } finally {
    await rm(temporaryRoot, {force: true, recursive: true});
  }
});

test("explicit input rejects symlinks that could escape the root", async () => {
  const temporaryDirectory = await mkdtemp(
    path.join(os.tmpdir(), "koubo-schema-test-"),
  );
  const outsideFile = path.join(temporaryDirectory, "outside.json");
  const linkPath = path.join(
    ROOT,
    "fixtures",
    "contract",
    `.outside-link-${process.pid}.json`,
  );
  await writeFile(outsideFile, "{}\n");
  await symlink(outsideFile, linkPath);

  try {
    const result = runCli(
      "--input",
      path.relative(ROOT, linkPath),
      "--format",
      "json",
    );
    assert.equal(result.status, EXIT_CODES.USAGE_OR_INTERNAL_ERROR);
    assert.match(result.stderr, /symbolic-link inputs are not allowed/u);
  } finally {
    await rm(linkPath, { force: true });
    await rm(temporaryDirectory, { force: true, recursive: true });
  }
});

test("full repository scans report symlinks instead of silently skipping them", async () => {
  const temporaryRoot = await mkdtemp(
    path.join(os.tmpdir(), "koubo-full-scan-symlink-"),
  );
  const outsideDirectory = await mkdtemp(
    path.join(os.tmpdir(), "koubo-full-scan-target-"),
  );
  const contractDirectory = path.join(temporaryRoot, "fixtures", "contract");
  await mkdir(contractDirectory, {recursive: true});
  await writeFile(
    path.join(contractDirectory, "schema-baseline.json"),
    `${JSON.stringify({version: 1, entries: []}, null, 2)}\n`,
  );
  await writeFile(
    path.join(contractDirectory, "cases.json"),
    `${JSON.stringify({version: 1, cases: []}, null, 2)}\n`,
  );
  const outsideFile = path.join(outsideDirectory, "outside.json");
  await writeFile(outsideFile, "{}\n");
  await symlink(outsideFile, path.join(temporaryRoot, "linked.json"));

  try {
    const result = runCli(
      "--root",
      temporaryRoot,
      "--mode",
      "release",
      "--format",
      "json",
    );
    assert.equal(result.status, EXIT_CODES.VALIDATION_FAILED);
    const report = JSON.parse(result.stdout);
    const link = report.files.find((file) => file.path === "linked.json");
    assert.equal(link.code, "CONTRACT.SYMLINK_NOT_ALLOWED");
  } finally {
    await rm(temporaryRoot, {force: true, recursive: true});
    await rm(outsideDirectory, {force: true, recursive: true});
  }
});

test("baseline control file remains explicit and machine-readable", async () => {
  const baseline = JSON.parse(
    await readFile(path.join(ROOT, "fixtures/contract/schema-baseline.json")),
  );
  assert.equal(baseline.version, 1);
  assert.ok(Array.isArray(baseline.entries));
});
