import assert from "node:assert/strict";
import {spawnSync} from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import Ajv2020 from "ajv/dist/2020.js";

test("composition and theme assets have valid references and geometry", () => {
  const result = spawnSync(process.execPath, ["scripts/check-assets.mjs"], {
    cwd: process.cwd(),
    encoding: "utf8",
  });
  assert.equal(result.status, 0, result.stderr || result.stdout);
  assert.match(result.stdout, /asset audit passed/);
});

test("theme roles meet the repository's documented contrast targets", () => {
  const result = spawnSync(process.execPath, ["assets/theme-kit/scripts/check-contrast.mjs"], {
    cwd: process.cwd(),
    encoding: "utf8",
  });
  assert.equal(result.status, 0, result.stderr || result.stdout);
  assert.doesNotMatch(result.stdout, /FAIL/);
});

test("theme schema rejects malformed colors and unknown fields", () => {
  const schema = JSON.parse(
    fs.readFileSync("assets/theme-kit/tokens/themes.schema.json", "utf8"),
  );
  const themes = JSON.parse(
    fs.readFileSync("assets/theme-kit/tokens/themes.json", "utf8"),
  );
  const validate = new Ajv2020({allErrors: true, strict: true}).compile(schema);
  assert.equal(validate(themes), true, JSON.stringify(validate.errors));

  const invalid = structuredClone(themes);
  invalid.themes[0].semantic.canvas = "not-a-color";
  invalid.themes[0].unexpected = true;
  assert.equal(validate(invalid), false);
  assert.ok(validate.errors.some(
    (error) =>
      error.instancePath === "/themes/0/semantic/canvas"
      && error.keyword === "pattern",
  ));
  assert.ok(validate.errors.some(
    (error) =>
      error.instancePath === "/themes/0"
      && error.keyword === "additionalProperties",
  ));

  const invalidRgba = structuredClone(themes);
  invalidRgba.themes[0].semantic.shadow = "rgba(999,0,0,0.5)";
  assert.equal(validate(invalidRgba), false);
  assert.ok(validate.errors.some(
    (error) =>
      error.instancePath === "/themes/0/semantic/shadow"
      && error.keyword === "pattern",
  ));
});

test("asset validation fails closed on a missing referenced background", () => {
  const fixtureRoot = fs.mkdtempSync(path.join(os.tmpdir(), "koubo-assets-"));
  try {
    fs.cpSync("assets", path.join(fixtureRoot, "assets"), {recursive: true});
    const manifestPath = path.join(fixtureRoot, "assets/theme-kit/manifest.json");
    const manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
    manifest.themes[0].backgroundAsset = "assets/backgrounds/missing.svg";
    fs.writeFileSync(manifestPath, `${JSON.stringify(manifest, null, 2)}\n`);

    const result = spawnSync(process.execPath, ["scripts/check-assets.mjs", "--root", fixtureRoot], {
      cwd: process.cwd(),
      encoding: "utf8",
    });
    assert.equal(result.status, 1, result.stderr || result.stdout);
    assert.match(result.stderr, /missing assets\/theme-kit\/assets\/backgrounds\/missing\.svg/);
  } finally {
    fs.rmSync(fixtureRoot, {recursive: true, force: true});
  }
});

test("asset validation fails closed on duplicate theme identifiers", () => {
  const fixtureRoot = fs.mkdtempSync(path.join(os.tmpdir(), "koubo-assets-"));
  try {
    fs.cpSync("assets", path.join(fixtureRoot, "assets"), {recursive: true});
    const themesPath = path.join(
      fixtureRoot,
      "assets/theme-kit/tokens/themes.json",
    );
    const themes = JSON.parse(fs.readFileSync(themesPath, "utf8"));
    themes.themes[1].id = themes.themes[0].id;
    fs.writeFileSync(themesPath, `${JSON.stringify(themes, null, 2)}\n`);

    const result = spawnSync(
      process.execPath,
      ["scripts/check-assets.mjs", "--root", fixtureRoot],
      {cwd: process.cwd(), encoding: "utf8"},
    );
    assert.equal(result.status, 1, result.stderr || result.stdout);
    assert.match(result.stderr, /theme-kit\.themes: duplicate id/);
  } finally {
    fs.rmSync(fixtureRoot, {recursive: true, force: true});
  }
});

test("asset validation requires every shipped manifest asset", () => {
  const fixtureRoot = fs.mkdtempSync(path.join(os.tmpdir(), "koubo-assets-"));
  try {
    fs.cpSync("assets", path.join(fixtureRoot, "assets"), {recursive: true});
    const manifestPath = path.join(fixtureRoot, "assets/theme-kit/manifest.json");
    const manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
    manifest.assets.safeAreaOverlay = "assets/overlays/missing.svg";
    fs.writeFileSync(manifestPath, `${JSON.stringify(manifest, null, 2)}\n`);

    const result = spawnSync(
      process.execPath,
      ["scripts/check-assets.mjs", "--root", fixtureRoot],
      {cwd: process.cwd(), encoding: "utf8"},
    );
    assert.equal(result.status, 1, result.stderr || result.stdout);
    assert.match(
      result.stderr,
      /theme-kit\.assets\.safeAreaOverlay: missing assets\/theme-kit\/assets\/overlays\/missing\.svg/,
    );
  } finally {
    fs.rmSync(fixtureRoot, {recursive: true, force: true});
  }
});

test("asset validator rejects unknown CLI options", () => {
  const result = spawnSync(
    process.execPath,
    ["scripts/check-assets.mjs", "--rot", "/tmp/not-used"],
    {cwd: process.cwd(), encoding: "utf8"},
  );
  assert.equal(result.status, 2);
  assert.match(result.stderr, /unknown or unsupported option/);
});

test("asset input failures do not disclose the absolute repository path", (t) => {
  const fixtureRoot = fs.mkdtempSync(
    path.join(os.tmpdir(), "koubo-private-assets-"),
  );
  t.after(() => fs.rmSync(fixtureRoot, {recursive: true, force: true}));

  const result = spawnSync(
    process.execPath,
    ["scripts/check-assets.mjs", "--root", fixtureRoot],
    {cwd: process.cwd(), encoding: "utf8"},
  );
  assert.equal(result.status, 1);
  assert.match(result.stderr, /assets\/compositions\.json: cannot read JSON \(ENOENT\)/);
  assert.doesNotMatch(result.stderr, new RegExp(
    fixtureRoot.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"),
  ));
});

test("asset validation rejects impossible safe-area insets", (t) => {
  const fixtureRoot = fs.mkdtempSync(path.join(os.tmpdir(), "koubo-assets-"));
  t.after(() => fs.rmSync(fixtureRoot, {recursive: true, force: true}));
  fs.cpSync("assets", path.join(fixtureRoot, "assets"), {recursive: true});
  const layoutsPath = path.join(
    fixtureRoot,
    "assets/theme-kit/tokens/layouts.json",
  );
  const layouts = JSON.parse(fs.readFileSync(layoutsPath, "utf8"));
  layouts.canvas.safeArea.left = 900;
  layouts.canvas.safeArea.right = 200;
  fs.writeFileSync(layoutsPath, `${JSON.stringify(layouts, null, 2)}\n`);

  const result = spawnSync(
    process.execPath,
    ["scripts/check-assets.mjs", "--root", fixtureRoot],
    {cwd: process.cwd(), encoding: "utf8"},
  );
  assert.equal(result.status, 1, result.stderr || result.stdout);
  assert.match(result.stderr, /horizontal insets consume the canvas/);
});

test("asset validation keeps subtitle baselines inside the safe area", (t) => {
  const fixtureRoot = fs.mkdtempSync(path.join(os.tmpdir(), "koubo-assets-"));
  t.after(() => fs.rmSync(fixtureRoot, {recursive: true, force: true}));
  fs.cpSync("assets", path.join(fixtureRoot, "assets"), {recursive: true});
  const compositionsPath = path.join(
    fixtureRoot,
    "assets/compositions.json",
  );
  const compositions = JSON.parse(fs.readFileSync(compositionsPath, "utf8"));
  compositions.formats[0].subtitleBaseline.x = 0;
  fs.writeFileSync(
    compositionsPath,
    `${JSON.stringify(compositions, null, 2)}\n`,
  );

  const result = spawnSync(
    process.execPath,
    ["scripts/check-assets.mjs", "--root", fixtureRoot],
    {cwd: process.cwd(), encoding: "utf8"},
  );
  assert.equal(result.status, 1, result.stderr || result.stdout);
  assert.match(result.stderr, /subtitleBaseline: rectangle leaves the declared safe area/);
});

test("asset validation cross-checks demo theme and layout references", (t) => {
  const fixtureRoot = fs.mkdtempSync(path.join(os.tmpdir(), "koubo-assets-"));
  t.after(() => fs.rmSync(fixtureRoot, {recursive: true, force: true}));
  fs.cpSync("assets", path.join(fixtureRoot, "assets"), {recursive: true});
  const demoPath = path.join(
    fixtureRoot,
    "assets/theme-kit/examples/demo-data.json",
  );
  const demo = JSON.parse(fs.readFileSync(demoPath, "utf8"));
  demo.recommendedLayout = "missing-layout";
  fs.writeFileSync(demoPath, `${JSON.stringify(demo, null, 2)}\n`);

  const result = spawnSync(
    process.execPath,
    ["scripts/check-assets.mjs", "--root", fixtureRoot],
    {cwd: process.cwd(), encoding: "utf8"},
  );
  assert.equal(result.status, 1, result.stderr || result.stdout);
  assert.match(result.stderr, /unknown recommendedLayout "missing-layout"/);
});

test("asset validation rejects contradictory visibility markers", (t) => {
  const fixtureRoot = fs.mkdtempSync(path.join(os.tmpdir(), "koubo-assets-"));
  t.after(() => fs.rmSync(fixtureRoot, {recursive: true, force: true}));
  fs.cpSync("assets", path.join(fixtureRoot, "assets"), {recursive: true});
  const compositionsPath = path.join(
    fixtureRoot,
    "assets/compositions.json",
  );
  const compositions = JSON.parse(fs.readFileSync(compositionsPath, "utf8"));
  compositions.sourceSlots[0].mustBeRedacted.push(
    compositions.sourceSlots[0].mustRemainVisible[0],
  );
  fs.writeFileSync(
    compositionsPath,
    `${JSON.stringify(compositions, null, 2)}\n`,
  );

  const result = spawnSync(
    process.execPath,
    ["scripts/check-assets.mjs", "--root", fixtureRoot],
    {cwd: process.cwd(), encoding: "utf8"},
  );
  assert.equal(result.status, 1, result.stderr || result.stdout);
  assert.match(result.stderr, /cannot be both visible and redacted/);
});
