const fs = require("fs");
const path = require("path");

const SKILL_ROOT = path.resolve(__dirname, "..");
const PREVIEW_WIDTH = 1280;
const PREVIEW_HEIGHT = 720;
const DEFAULT_TEMPLATE = "signal-stage";
const VALID_SCENE_TYPES = new Set(["hero", "problem", "steps", "comparison", "stat", "quote", "closing"]);
const VALID_ELEMENT_TYPES = new Set(["title", "subtitle", "text", "bullet-list", "chip", "stat", "quote", "shape"]);
const VALID_EFFECTS = new Set([
  "fade",
  "fade-up",
  "slide-left",
  "slide-right",
  "pop",
  "clip-up",
  "zoom-in",
  "blur-in",
  "glow-pop",
  "swing-up",
  "reveal-right",
  "reveal-down"
]);
const VALID_SCENE_TRANSITIONS = new Set([
  "fade",
  "slide-left",
  "slide-right",
  "lift-up",
  "zoom-in",
  "zoom-out",
  "blur-in",
  "wipe-left",
  "wipe-up",
  "iris-in"
]);
const VALID_SUBTITLE_PRESETS = new Set(["bottom-band", "short-video-pop", "minimal-center"]);

function ensureDir(dirPath) {
  fs.mkdirSync(dirPath, { recursive: true });
}

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(path.resolve(filePath), "utf8"));
}

function writeText(filePath, content) {
  ensureDir(path.dirname(path.resolve(filePath)));
  fs.writeFileSync(path.resolve(filePath), content, "utf8");
}

function slugify(value) {
  return String(value)
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9\u4e00-\u9fa5]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .replace(/-+/g, "-");
}

function loadBaseCss() {
  return fs.readFileSync(path.join(SKILL_ROOT, "assets", "preview", "base.css"), "utf8");
}

function resolveTheme(themeName = "signal-ink") {
  const themePath = path.join(SKILL_ROOT, "assets", "themes", `${themeName}.json`);
  if (!fs.existsSync(themePath)) {
    throw new Error(`Theme not found: ${themeName}`);
  }
  return readJson(themePath);
}

function resolveTemplate(templateName = DEFAULT_TEMPLATE) {
  const templatePath = path.join(SKILL_ROOT, "assets", "templates", `${templateName}.json`);
  if (!fs.existsSync(templatePath)) {
    throw new Error(`Template not found: ${templateName}`);
  }
  return readJson(templatePath);
}

function listCatalogEntries(dirName) {
  const targetDir = path.join(SKILL_ROOT, "assets", dirName);
  if (!fs.existsSync(targetDir)) {
    return [];
  }

  return fs
    .readdirSync(targetDir)
    .filter((name) => name.endsWith(".json"))
    .map((name) => readJson(path.join(targetDir, name)));
}

function resolveCatalogEntry(dirName, entryId) {
  const entryPath = path.join(SKILL_ROOT, "assets", dirName, `${entryId}.json`);
  if (!fs.existsSync(entryPath)) {
    throw new Error(`${dirName} entry not found: ${entryId}`);
  }
  return readJson(entryPath);
}

function clamp(value, min, max) {
  return Math.max(min, Math.min(max, value));
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function normalizeNumber(value, fallback) {
  return Number.isFinite(value) ? value : fallback;
}

function computeTimeline(movie) {
  let cursor = 0;
  const scenes = (movie.scenes || []).map((scene) => {
    const durationMs = normalizeNumber(scene.durationMs, 0);
    const record = {
      ...scene,
      startMs: cursor,
      endMs: cursor + durationMs
    };
    cursor += durationMs;
    return record;
  });

  return {
    scenes,
    totalDurationMs: cursor
  };
}

function getMoviePath(inputPath) {
  const absolute = path.resolve(inputPath);
  if (path.extname(absolute).toLowerCase() === ".json") {
    return absolute;
  }
  return path.join(absolute, "movie.json");
}

function getProjectDir(inputPath) {
  const absolute = path.resolve(inputPath);
  if (path.extname(absolute).toLowerCase() === ".json") {
    return path.dirname(absolute);
  }
  return absolute;
}

function parseFlag(args, flagName, fallback = null) {
  const index = args.indexOf(flagName);
  if (index === -1) {
    return fallback;
  }
  return args[index + 1] && !args[index + 1].startsWith("--") ? args[index + 1] : true;
}

function formatDuration(ms) {
  const totalSeconds = Math.max(0, Math.round(ms / 1000));
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  return `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
}

module.exports = {
  DEFAULT_TEMPLATE,
  PREVIEW_HEIGHT,
  PREVIEW_WIDTH,
  SKILL_ROOT,
  VALID_EFFECTS,
  VALID_ELEMENT_TYPES,
  VALID_SCENE_TYPES,
  VALID_SCENE_TRANSITIONS,
  VALID_SUBTITLE_PRESETS,
  clamp,
  computeTimeline,
  ensureDir,
  escapeHtml,
  formatDuration,
  getMoviePath,
  getProjectDir,
  listCatalogEntries,
  loadBaseCss,
  parseFlag,
  readJson,
  resolveCatalogEntry,
  resolveTemplate,
  resolveTheme,
  slugify,
  writeText
};
