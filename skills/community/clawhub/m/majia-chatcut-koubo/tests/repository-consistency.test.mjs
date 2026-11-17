import assert from "node:assert/strict";
import {LIVE_CANARY_REPORT} from "../src/config/release-files.mjs";
import {spawnSync} from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import {fileURLToPath} from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const HUMAN_MAINTENANCE_FILES = [
  "01-从这里开始/README.md",
  "02-剪辑方法手册/README.md",
  "03-实操迭代与踩坑/README.md",
  "03-实操迭代与踩坑/迭代记录.md",
  "04-项目设计与路线图/README.md",
];
const VERSION_SURFACE_FILES = [
  "package.json",
  "package-lock.json",
  ".node-version",
  ".github/workflows/ci.yml",
  "SKILL.md",
  "README.md",
  "README.en.md",
  "CHANGELOG.md",
  "04-项目设计与路线图/系统架构.svg",
  "04-项目设计与路线图/V1.3.1迁移指南.md",
  "04-项目设计与路线图/公开路线图.md",
  "02-剪辑方法手册/07-字幕与术语.md",
  "agents/openai.yaml",
  LIVE_CANARY_REPORT,
  "profiles/balanced-stable.json",
  "profiles/tight-short.json",
  "profiles/trust-longform.json",
  "profiles/screen-demo.json",
  "workflows/one-click-stable.md",
  "workflows/fast-cut.md",
  "workflows/pro-enhance.md",
  "workflows/resume.md",
  "workflows/official-skill-map.md",
  "rules/policy.json",
  "rules/registry.json",
  "fixtures/profiles/local/profile.source.json",
  "templates/operating-profile.template.json",
  "templates/local-config-example/profile/landscape.example.json",
  "assets/theme-kit/package.json",
  "assets/theme-kit/manifest.json",
  "assets/theme-kit/tokens/themes.json",
];

test("human maintenance navigation remains complete", () => {
  const readme = fs.readFileSync(path.join(root, "README.md"), "utf8");
  for (const file of HUMAN_MAINTENANCE_FILES) {
    assert.equal(fs.existsSync(path.join(root, file)), true, `missing ${file}`);
  }
  for (const directory of [
    "01-从这里开始",
    "02-剪辑方法手册",
    "03-实操迭代与踩坑",
    "04-项目设计与路线图",
  ]) {
    assert.match(readme, new RegExp(`${directory}/README\\.md`, "u"));
  }
});

function copyVersionSurface(t) {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), "version-drift-"));
  t.after(() => fs.rmSync(directory, {recursive: true, force: true}));
  for (const file of VERSION_SURFACE_FILES) {
    const destination = path.join(directory, file);
    fs.mkdirSync(path.dirname(destination), {recursive: true});
    fs.copyFileSync(path.join(root, file), destination);
  }
  return directory;
}

test("version and state-count documentation cannot drift silently", () => {
  const result = spawnSync(process.execPath, ["scripts/check-version-drift.mjs"], {
    cwd: process.cwd(),
    encoding: "utf8",
  });
  assert.equal(result.status, 0, result.stderr || result.stdout);
  assert.match(result.stdout, /version drift audit passed/);
});

test("profile resolver outputs are excluded from public commits", () => {
  const ignoreRules = fs.readFileSync(path.join(root, ".gitignore"), "utf8");
  assert.match(ignoreRules, /^\*\.resolved\.json$/mu);
  assert.match(ignoreRules, /^\*\.merge-trace\.json$/mu);
});

test("runtime validators keep Ajv packages in production dependencies", () => {
  const manifest = JSON.parse(
    fs.readFileSync(path.join(root, "package.json"), "utf8"),
  );
  const lock = JSON.parse(
    fs.readFileSync(path.join(root, "package-lock.json"), "utf8"),
  );
  for (const dependency of ["ajv", "ajv-formats"]) {
    assert.equal(typeof manifest.dependencies?.[dependency], "string");
    assert.equal(manifest.devDependencies?.[dependency], undefined);
    assert.equal(
      lock.packages?.[""]?.dependencies?.[dependency],
      manifest.dependencies[dependency],
    );
  }
});

test("version drift gate fails closed when the lockfile root version drifts", (t) => {
  const directory = copyVersionSurface(t);
  const lockFile = path.join(directory, "package-lock.json");
  const lock = JSON.parse(fs.readFileSync(lockFile, "utf8"));
  lock.packages[""].version = "0.0.0";
  fs.writeFileSync(lockFile, `${JSON.stringify(lock, null, 2)}\n`);

  const result = spawnSync(
    process.execPath,
    ["scripts/check-version-drift.mjs", "--root", directory],
    {cwd: root, encoding: "utf8"},
  );
  assert.equal(result.status, 1);
  assert.match(result.stderr, /package-lock root version 0\.0\.0/);
});

test("version drift gate binds Node pin, engines and CI setup", (t) => {
  const directory = copyVersionSurface(t);
  fs.writeFileSync(path.join(directory, ".node-version"), "24.17.0\n");

  const result = spawnSync(
    process.execPath,
    ["scripts/check-version-drift.mjs", "--root", directory],
    {cwd: root, encoding: "utf8"},
  );
  assert.equal(result.status, 1);
  assert.match(result.stderr, /package engines\.node .* != >=24\.17\.0 <25/);
});

test("version drift gate rejects an incomplete Node version pin", (t) => {
  const directory = copyVersionSurface(t);
  fs.writeFileSync(path.join(directory, ".node-version"), "24\n");

  const result = spawnSync(
    process.execPath,
    ["scripts/check-version-drift.mjs", "--root", directory],
    {cwd: root, encoding: "utf8"},
  );
  assert.equal(result.status, 1);
  assert.match(result.stderr, /\.node-version: invalid semantic version 24/);
});

test("version drift gate keeps caption root and provenance guidance in sync", (t) => {
  const directory = copyVersionSurface(t);
  const migrationPath = path.join(directory, "04-项目设计与路线图/V1.3.1迁移指南.md");
  const migration = fs.readFileSync(migrationPath, "utf8")
    .replaceAll("--root <profile-config-root>", "--config-boundary omitted");
  fs.writeFileSync(migrationPath, migration);

  const result = spawnSync(
    process.execPath,
    ["scripts/check-version-drift.mjs", "--root", directory],
    {cwd: root, encoding: "utf8"},
  );
  assert.equal(result.status, 1);
  assert.match(
    result.stderr,
    /V1\.3\.1迁移指南\.md: caption validation example must declare its profile root/,
  );
});

test("version drift gate keeps the public roadmap linked and governed", (t) => {
  const directory = copyVersionSurface(t);
  const roadmapPath = path.join(directory, "04-项目设计与路线图/公开路线图.md");
  const roadmap = fs.readFileSync(roadmapPath, "utf8")
    .replaceAll("不是发布时间或版本承诺", "时间承诺省略");
  fs.writeFileSync(roadmapPath, roadmap);

  const result = spawnSync(
    process.execPath,
    ["scripts/check-version-drift.mjs", "--root", directory],
    {cwd: root, encoding: "utf8"},
  );
  assert.equal(result.status, 1);
  assert.match(
    result.stderr,
    /公开路线图\.md: missing governance marker/,
  );
});

test("version drift gate binds Rule Registry to hard policy and release verify", (t) => {
  const directory = copyVersionSurface(t);
  const registryPath = path.join(directory, "rules/registry.json");
  const registry = JSON.parse(fs.readFileSync(registryPath, "utf8"));
  registry.policyVersion = "0.0.0";
  fs.writeFileSync(registryPath, `${JSON.stringify(registry, null, 2)}\n`);

  const result = spawnSync(
    process.execPath,
    ["scripts/check-version-drift.mjs", "--root", directory],
    {cwd: root, encoding: "utf8"},
  );
  assert.equal(result.status, 1);
  assert.match(
    result.stderr,
    /rules\/registry\.json: policyVersion 0\.0\.0/,
  );
});

test("version drift input failures use a stable code without absolute paths", (t) => {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), "version-private-"));
  t.after(() => fs.rmSync(directory, {recursive: true, force: true}));

  const result = spawnSync(
    process.execPath,
    ["scripts/check-version-drift.mjs", "--root", directory],
    {cwd: root, encoding: "utf8"},
  );
  assert.equal(result.status, 2);
  assert.match(result.stderr, /version drift audit unavailable: ENOENT/);
  assert.doesNotMatch(
    result.stderr,
    new RegExp(directory.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")),
  );
});
