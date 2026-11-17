#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

const args = process.argv.slice(2);
let requestedRoot = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
);
let rootSeen = false;
for (let index = 0; index < args.length; index += 1) {
  const option = args[index];
  if (option !== "--root") {
    console.error("Usage: node scripts/check-assets.mjs [--root <repository-root>]");
    console.error("unknown or unsupported option");
    process.exit(2);
  }
  if (rootSeen) {
    console.error("Usage: node scripts/check-assets.mjs [--root <repository-root>]");
    console.error("duplicate option: --root");
    process.exit(2);
  }
  const value = args[index + 1];
  if (!value || value.startsWith("--")) {
    console.error("Usage: node scripts/check-assets.mjs [--root <repository-root>]");
    console.error("--root requires a value");
    process.exit(2);
  }
  requestedRoot = path.resolve(value);
  rootSeen = true;
  index += 1;
}
let root;
try {
  root = fs.realpathSync(requestedRoot);
} catch (error) {
  console.error(`repository root is not readable: ${error.code ?? "READ_FAILED"}`);
  process.exit(2);
}
const errors = [];

function readJson(relativePath) {
  const absolutePath = path.join(root, relativePath);
  try {
    return JSON.parse(fs.readFileSync(absolutePath, "utf8"));
  } catch (error) {
    const code = error instanceof SyntaxError
      ? "INVALID_JSON"
      : error?.code ?? "READ_FAILED";
    errors.push(`${relativePath}: cannot read JSON (${code})`);
    return null;
  }
}

function requireUnique(values, label) {
  const seen = new Set();
  for (const value of values) {
    if (seen.has(value)) errors.push(`${label}: duplicate id "${value}"`);
    seen.add(value);
  }
}

function pathInsideRoot(absolutePath) {
  const relative = path.relative(root, absolutePath);
  return relative === ""
    || (relative !== ".."
      && !relative.startsWith(`..${path.sep}`)
      && !path.isAbsolute(relative));
}

function resolveReference(relativePath, label) {
  if (typeof relativePath !== "string" || relativePath.length === 0) {
    errors.push(`${label}: expected a non-empty relative path`);
    return null;
  }
  const absolutePath = path.resolve(root, relativePath);
  if (!pathInsideRoot(absolutePath)) {
    errors.push(`${label}: path escapes repository root (${relativePath})`);
    return null;
  }
  return absolutePath;
}

function validateOptionalReference(relativePath, label) {
  resolveReference(relativePath, label);
}

function requirePath(relativePath, label, expectedKind = "file") {
  const absolutePath = resolveReference(relativePath, label);
  if (!absolutePath) return;
  let stat;
  try {
    stat = fs.lstatSync(absolutePath);
  } catch (error) {
    if (error?.code === "ENOENT") {
      errors.push(`${label}: missing ${relativePath}`);
    } else {
      errors.push(`${label}: cannot inspect ${relativePath} (${error?.code ?? "READ_FAILED"})`);
    }
    return;
  }
  if (stat.isSymbolicLink()) {
    errors.push(`${label}: symbolic links are not allowed (${relativePath})`);
    return;
  }
  let canonicalPath;
  try {
    canonicalPath = fs.realpathSync(absolutePath);
  } catch (error) {
    errors.push(`${label}: cannot resolve ${relativePath} (${error?.code ?? "READ_FAILED"})`);
    return;
  }
  if (!pathInsideRoot(canonicalPath)) {
    errors.push(`${label}: resolved path escapes repository root (${relativePath})`);
    return;
  }
  if (expectedKind === "directory" && !stat.isDirectory()) {
    errors.push(`${label}: expected directory ${relativePath}`);
  } else if (expectedKind === "file" && !stat.isFile()) {
    errors.push(`${label}: expected file ${relativePath}`);
  }
}

function checkRect(rect, canvas, label) {
  if (!rect || typeof rect !== "object") {
    errors.push(`${label}: missing rectangle`);
    return;
  }
  for (const key of ["x", "y", "w", "h"]) {
    if (!Number.isFinite(rect[key])) errors.push(`${label}.${key}: expected finite number`);
  }
  if (![rect.x, rect.y, rect.w, rect.h].every(Number.isFinite)) return;
  if (rect.w <= 0 || rect.h <= 0) errors.push(`${label}: width and height must be positive`);
  if (rect.x < 0 || rect.y < 0) errors.push(`${label}: rectangle starts outside canvas`);
  if (rect.x + rect.w > canvas.width || rect.y + rect.h > canvas.height) {
    errors.push(`${label}: rectangle exceeds ${canvas.width}x${canvas.height} canvas`);
  }
}

function checkSafeArea(canvas, safeArea, label) {
  if (!safeArea || typeof safeArea !== "object") {
    errors.push(`${label}: missing safe area`);
    return false;
  }
  const values = ["left", "right", "top", "bottom"]
    .map((key) => safeArea[key]);
  if (!values.every((value) => Number.isFinite(value) && value >= 0)) {
    errors.push(`${label}: insets must be finite non-negative numbers`);
    return false;
  }
  if (safeArea.left + safeArea.right >= canvas.width) {
    errors.push(`${label}: horizontal insets consume the canvas`);
    return false;
  }
  if (safeArea.top + safeArea.bottom >= canvas.height) {
    errors.push(`${label}: vertical insets consume the canvas`);
    return false;
  }
  return true;
}

function checkRectInsideSafeArea(rect, canvas, safeArea, label) {
  if (
    !rect
    || !["x", "y", "w", "h"].every((key) => Number.isFinite(rect[key]))
  ) {
    return;
  }
  const right = canvas.width - safeArea.right;
  const bottom = canvas.height - safeArea.bottom;
  if (
    rect.x < safeArea.left
    || rect.y < safeArea.top
    || rect.x + rect.w > right
    || rect.y + rect.h > bottom
  ) {
    errors.push(`${label}: rectangle leaves the declared safe area`);
  }
}

function checkCompositions() {
  const document = readJson("assets/compositions.json");
  if (!document) return;

  const sourceSlots = document.sourceSlots || [];
  requireUnique(sourceSlots.map((slot) => slot.id), "compositions.sourceSlots");
  requireUnique((document.formats || []).map((format) => format.id), "compositions.formats");
  for (const slot of sourceSlots) {
    const visible = new Set(slot.mustRemainVisible || []);
    for (const marker of slot.mustBeRedacted || []) {
      if (visible.has(marker)) {
        errors.push(
          `source slot ${slot.id}: "${marker}" cannot be both visible and redacted`,
        );
      }
    }
  }

  const layoutIds = [];
  for (const format of document.formats || []) {
    const canvas = format.canvas || {};
    if (!Number.isInteger(canvas.width) || !Number.isInteger(canvas.height)) {
      errors.push(`format ${format.id}: canvas width/height must be integers`);
      continue;
    }
    const safeAreaValid = checkSafeArea(
      canvas,
      format.safeArea,
      `format ${format.id}.safeArea`,
    );
    checkRect(format.subtitleBaseline, canvas, `format ${format.id}.subtitleBaseline`);
    if (safeAreaValid) {
      checkRectInsideSafeArea(
        format.subtitleBaseline,
        canvas,
        format.safeArea,
        `format ${format.id}.subtitleBaseline`,
      );
    }
    if (format.subtitleBaseline?.maxLines !== 1) {
      errors.push(`format ${format.id}.subtitleBaseline.maxLines: expected 1`);
    }
    for (const layout of format.layouts || []) {
      layoutIds.push(layout.id);
      for (const role of ["screen", "speaker", "title", "point", "subtitle"]) {
        checkRect(layout[role], canvas, `layout ${layout.id}.${role}`);
      }
      if (layout.subtitle?.maxLines !== 1) {
        errors.push(`layout ${layout.id}.subtitle.maxLines: expected 1`);
      }
      if (layout.speakerShape === "circle") {
        if (layout.speaker?.w !== layout.speaker?.h) {
          errors.push(`layout ${layout.id}.speaker: circle must use equal width and height`);
        }
        if (layout.speaker?.radius !== layout.speaker?.w / 2) {
          errors.push(`layout ${layout.id}.speaker.radius: expected half of visible width`);
        }
      }
    }
  }
  requireUnique(layoutIds, "compositions.layouts");
}

function checkThemeKit() {
  const manifest = readJson("assets/theme-kit/manifest.json");
  const themes = readJson("assets/theme-kit/tokens/themes.json");
  const layouts = readJson("assets/theme-kit/tokens/layouts.json");
  const demo = readJson("assets/theme-kit/examples/demo-data.json");
  if (!manifest || !themes || !layouts || !demo) return;

  const themeEntries = themes.themes || [];
  const layoutEntries = layouts.layouts || [];
  requireUnique(themeEntries.map((theme) => theme.id), "theme-kit.themes");
  requireUnique(themeEntries.map((theme) => theme.index), "theme-kit.theme indexes");
  requireUnique(layoutEntries.map((layout) => layout.id), "theme-kit.layouts");
  const themeById = new Map(themeEntries.map((theme) => [theme.id, theme]));
  const layoutIds = new Set(layoutEntries.map((layout) => layout.id));
  requireUnique((manifest.themes || []).map((theme) => theme.id), "theme-kit.manifest.themes");

  for (const [name, relativePath] of Object.entries(manifest.entrypoints || {})) {
    requirePath(path.posix.join("assets/theme-kit", relativePath), `theme-kit.entrypoints.${name}`);
  }
  for (const [name, relativePath] of Object.entries(manifest.assets || {})) {
    requirePath(
      path.posix.join("assets/theme-kit", relativePath),
      `theme-kit.assets.${name}`,
      name.endsWith("Directory") ? "directory" : "file",
    );
  }
  for (const [name, relativePath] of Object.entries(manifest.generatedAssets || {})) {
    validateOptionalReference(
      path.posix.join("assets/theme-kit", relativePath),
      `theme-kit.generatedAssets.${name}`,
    );
  }

  const generatedPngDirectory = manifest.generatedAssets?.backgroundPngDirectory;
  const generatedPngAbsolute = generatedPngDirectory
    ? resolveReference(
      path.posix.join("assets/theme-kit", generatedPngDirectory),
      "theme-kit.generatedAssets.backgroundPngDirectory",
    )
    : null;
  const generatedPngDirectoryExists = generatedPngAbsolute
    ? fs.existsSync(generatedPngAbsolute)
    : false;

  for (const theme of themeEntries) {
    requireUnique(
      (theme.sourcePalette || []).map((entry) => entry.role),
      `theme-kit theme ${theme.id}.sourcePalette`,
    );
    const expectedSvg = `assets/backgrounds/${theme.index}-${theme.id}.svg`;
    const expectedPng = `assets/backgrounds-png/${theme.index}-${theme.id}.png`;
    if (theme.backgroundAsset !== expectedSvg) {
      errors.push(`theme-kit ${theme.id}: expected backgroundAsset ${expectedSvg}`);
    }
    if (theme.backgroundPng !== expectedPng) {
      errors.push(`theme-kit ${theme.id}: expected backgroundPng ${expectedPng}`);
    }
    validateOptionalReference(
      path.posix.join("assets/theme-kit", theme.backgroundPng),
      `theme-kit theme ${theme.id}.backgroundPng`,
    );
    if (generatedPngDirectoryExists) {
      requirePath(
        path.posix.join("assets/theme-kit", theme.backgroundPng),
        `theme-kit theme ${theme.id}.backgroundPng`,
      );
    }
  }

  const recommendedTheme = themeById.get(demo.recommendedTheme);
  if (!recommendedTheme) {
    errors.push(`theme-kit demo: unknown recommendedTheme "${demo.recommendedTheme}"`);
  }
  if (!layoutIds.has(demo.recommendedLayout)) {
    errors.push(`theme-kit demo: unknown recommendedLayout "${demo.recommendedLayout}"`);
  }
  if (
    recommendedTheme
    && recommendedTheme.layout !== demo.recommendedLayout
  ) {
    errors.push(
      `theme-kit demo: recommended theme/layout mismatch (${demo.recommendedTheme} uses ${recommendedTheme.layout})`,
    );
  }

  const manifestIds = new Set();
  for (const entry of manifest.themes || []) {
    manifestIds.add(entry.id);
    const theme = themeById.get(entry.id);
    if (!theme) {
      errors.push(`theme-kit.manifest: unknown theme "${entry.id}"`);
      continue;
    }
    if (!layoutIds.has(entry.layout)) {
      errors.push(`theme-kit.manifest ${entry.id}: unknown layout "${entry.layout}"`);
    }
    if (theme.layout !== entry.layout) {
      errors.push(`theme-kit ${entry.id}: manifest/theme layout mismatch`);
    }
    if (theme.backgroundAsset !== entry.backgroundAsset) {
      errors.push(`theme-kit ${entry.id}: manifest/theme background mismatch`);
    }
    requirePath(
      path.posix.join("assets/theme-kit", entry.backgroundAsset),
      `theme-kit.manifest ${entry.id}.backgroundAsset`,
    );
  }

  for (const themeId of themeById.keys()) {
    if (!manifestIds.has(themeId)) errors.push(`theme-kit.manifest: missing theme "${themeId}"`);
  }

  const canvas = layouts.canvas || {};
  const safeAreaValid = checkSafeArea(
    canvas,
    canvas.safeArea,
    "theme layout canvas.safeArea",
  );
  checkRect(canvas.subtitleZone, canvas, "theme layout canvas.subtitleZone");
  if (safeAreaValid) {
    checkRectInsideSafeArea(
      canvas.subtitleZone,
      canvas,
      canvas.safeArea,
      "theme layout canvas.subtitleZone",
    );
  }
  for (const layout of layouts.layouts || []) {
    for (const [zoneName, rect] of Object.entries(layout.zones || {})) {
      checkRect(rect, canvas, `theme layout ${layout.id}.${zoneName}`);
    }
    if (safeAreaValid && layout.zones?.subtitle) {
      checkRectInsideSafeArea(
        layout.zones.subtitle,
        canvas,
        canvas.safeArea,
        `theme layout ${layout.id}.subtitle`,
      );
    }
  }
}

checkCompositions();
checkThemeKit();

if (errors.length > 0) {
  for (const error of errors) console.error(`FAIL ${error}`);
  console.error(`asset audit failed: ${errors.length} error(s)`);
  process.exitCode = 1;
} else {
  console.log("asset audit passed: compositions, theme references, and geometry are consistent");
}
