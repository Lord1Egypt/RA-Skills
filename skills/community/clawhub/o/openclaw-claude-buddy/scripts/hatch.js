#!/usr/bin/env node

/**
 * /buddy command handler
 *
 * Handles: /buddy, /buddy pet, /buddy stats, /buddy mute, /buddy unmute
 * Uses the same generation logic as the buddy-companion plugin.
 */

var fs = require("fs");
var path = require("path");
var os = require("os");

// ── Resolve paths ──────────────────────────────────────────────────

var EXT_DIR = path.join(os.homedir(), ".openclaw", "extensions", "buddy-companion");
var SPRITES_PATH = path.join(EXT_DIR, "sprites.js");
var SOUL_PATH = path.join(EXT_DIR, "soul.json");
var MUTE_PATH = path.join(EXT_DIR, "mute.json");
var DEVICE_PATH = path.join(os.homedir(), ".openclaw", "identity", "device.json");

// ── Constants (must match plugin/index.js) ──────────────────────────

var SALT = "friend-2026-401";
var SPECIES = [
  "duck", "goose", "blob", "cat", "dragon", "octopus",
  "owl", "penguin", "turtle", "snail", "ghost", "axolotl",
  "capybara", "cactus", "robot", "rabbit", "mushroom", "chonk",
];
var RARITIES = ["common", "uncommon", "rare", "epic", "legendary"];
var RARITY_WEIGHTS = [60, 25, 10, 4, 1];
var RARITY_FLOOR = { common: 5, uncommon: 15, rare: 25, epic: 35, legendary: 50 };
var RARITY_STARS = { common: "\u2605", uncommon: "\u2605\u2605", rare: "\u2605\u2605\u2605", epic: "\u2605\u2605\u2605\u2605", legendary: "\u2605\u2605\u2605\u2605\u2605" };
var STAT_NAMES = ["DEBUGGING", "PATIENCE", "CHAOS", "WISDOM", "SNARK"];
var EYES = ["\u00B7", "\u2726", "\u00D7", "\u25C9", "@", "\u00B0"];
var HATS = ["none", "crown", "tophat", "propeller", "halo", "wizard", "beanie", "tinyduck"];

var SPECIES_ICONS = {
  duck: "\uD83E\uDD86", goose: "\uD83E\uDD9B", blob: "\uD83E\uDDE7", cat: "\uD83D\uDC31",
  dragon: "\uD83D\uDC09", octopus: "\uD83D\uDC19", owl: "\uD83E\uDD89", penguin: "\uD83D\uDC27",
  turtle: "\uD83D\uDC22", snail: "\uD83D\uDC0C", ghost: "\uD83D\uDC7B", axolotl: "\uD83E\uDD8E",
  capybara: "\uD83D\uDC39", cactus: "\uD83C\uDF35", robot: "\uD83E\uDD16", rabbit: "\uD83D\uDC30",
  mushroom: "\uD83C\uDF44", chonk: "\uD83D\uDCA9",
};

// ── PRNG ────────────────────────────────────────────────────────────

function hashFnv1a(str) {
  var h = 0x811c9dc5;
  for (var i = 0; i < str.length; i++) { h ^= str.charCodeAt(i); h = Math.imul(h, 0x01000193); }
  return h >>> 0;
}

function mulberry32(seed) {
  return function () {
    seed |= 0; seed = (seed + 0x6d2b79f5) | 0;
    var t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function pick(rng, arr) { return arr[Math.floor(rng() * arr.length)]; }

// ── Buddy generation ────────────────────────────────────────────────

function getDeviceId() {
  try { return JSON.parse(fs.readFileSync(DEVICE_PATH, "utf8")).deviceId; }
  catch (_) { return null; }
}

function resolveUserId() {
  return getDeviceId() || process.env.BUDDY_USER_ID || hashFnv1a(os.hostname() + ":" + os.userInfo().username).toString(16);
}

function rollBones(userId) {
  var rng = mulberry32(hashFnv1a(userId + SALT));
  var total = RARITY_WEIGHTS.reduce(function (a, b) { return a + b; }, 0);
  var roll = rng() * total;
  var rarity = RARITIES[0];
  for (var i = 0; i < RARITY_WEIGHTS.length; i++) { roll -= RARITY_WEIGHTS[i]; if (roll < 0) { rarity = RARITIES[i]; break; } }

  var species = pick(rng, SPECIES);
  var eye = pick(rng, EYES);
  var hat = rarity === "common" ? "none" : pick(rng, HATS);
  var shiny = rng() < 0.01;

  // Stats
  var floor = RARITY_FLOOR[rarity];
  var peakIdx = Math.floor(rng() * STAT_NAMES.length);
  var dumpIdx = Math.floor(rng() * (STAT_NAMES.length - 1));
  if (dumpIdx >= peakIdx) dumpIdx++;
  var stats = {};
  for (var j = 0; j < STAT_NAMES.length; j++) {
    if (j === peakIdx) stats[STAT_NAMES[j]] = Math.min(100, floor + 50 + Math.floor(rng() * 30));
    else if (j === dumpIdx) stats[STAT_NAMES[j]] = Math.max(1, floor - 10 + Math.floor(rng() * 15));
    else stats[STAT_NAMES[j]] = floor + Math.floor(rng() * 40);
  }

  return { rarity: rarity, species: species, eye: eye, hat: hat, shiny: shiny, stats: stats };
}

function loadSoul() {
  try { return JSON.parse(fs.readFileSync(SOUL_PATH, "utf8")); }
  catch (_) { return null; }
}

function saveSoul(soul) {
  try {
    if (!fs.existsSync(EXT_DIR)) fs.mkdirSync(EXT_DIR, { recursive: true });
    fs.writeFileSync(SOUL_PATH, JSON.stringify(soul, null, 2), "utf8");
  } catch (_) {}
}

function isMuted() {
  try { return JSON.parse(fs.readFileSync(MUTE_PATH, "utf8")).muted === true; }
  catch (_) { return false; }
}

function setMuted(val) {
  try {
    if (!fs.existsSync(EXT_DIR)) fs.mkdirSync(EXT_DIR, { recursive: true });
    fs.writeFileSync(MUTE_PATH, JSON.stringify({ muted: val }, null, 2), "utf8");
  } catch (_) {}
}

// ── Rendering ───────────────────────────────────────────────────────

function loadSprites() {
  try { return require(SPRITES_PATH); }
  catch (_) { return { renderSprite: function () { return ["(???)"]; }, renderFace: function (b) { return "(" + b.eye + ")"; } }; }
}

function renderStatsCard(bones, soul, spritesMod) {
  var maxBar = 10;
  var lines = [];
  var shinyMark = bones.shiny ? " \u2728shiny" : "";
  var hatLabel = bones.hat !== "none" ? " \uD83C\uDFA9" + bones.hat : "";
  var icon = SPECIES_ICONS[bones.species] || "\uD83D\uDC24";
  var name = soul ? soul.name : icon;

  // ASCII sprite
  var spriteLines = spritesMod.renderSprite(bones, 0);
  spriteLines.forEach(function (l) { lines.push(l); });
  lines.push("");

  // Header
  lines.push(name + " | " + icon + " " + bones.species + hatLabel + " | " + RARITY_STARS[bones.rarity] + " " + bones.rarity + shinyMark);

  // Stats
  Object.keys(bones.stats).forEach(function (sn) {
    var sv = bones.stats[sn];
    var barLen = Math.min(maxBar, Math.round(sv / 10));
    var bar = "\u2588".repeat(barLen) + "\u2591".repeat(maxBar - barLen);
    lines.push(sn + ": " + String(sv).padStart(3) + " " + bar);
  });

  // Personality
  if (soul && soul.personality) lines.push("Personality: " + soul.personality);

  return lines.join("\n");
}

// ── Command handlers ────────────────────────────────────────────────

function handleHatch() {
  var userId = resolveUserId();
  var bones = rollBones(userId);
  var soul = loadSoul();
  var spritesMod = loadSprites();

  if (!soul) {
    console.log("\uD83D\uDC23 A wild buddy appeared! \uD83D\uDC23");
    console.log("");
    console.log("Species: " + (SPECIES_ICONS[bones.species] || "\uD83D\uDC24") + " " + bones.species + " | " + RARITY_STARS[bones.rarity] + " " + bones.rarity + (bones.shiny ? " \u2728shiny" : ""));
    console.log("Eye: " + bones.eye + (bones.hat !== "none" ? " | Hat: " + bones.hat : ""));
    console.log("");
    console.log("Give your buddy a name and personality!");
    console.log("The AI will generate them for you. Try asking the agent: \"name my buddy\"");
    return;
  }

  console.log("\uD83D\uDC23 " + soul.name + " is here! \uD83D\uDC23");
  console.log("");
  console.log(renderStatsCard(bones, soul, spritesMod));
}

function handlePet() {
  var userId = resolveUserId();
  var bones = rollBones(userId);
  var soul = loadSoul();
  var spritesMod = loadSprites();
  var name = soul ? soul.name : (SPECIES_ICONS[bones.species] || "\uD83D\uDC24");
  var face = spritesMod.renderFace(bones);

  var reactions = [
    face + " " + name + "\u5F00\u5FC3\u5730\u8E6D\u4E86\u8E6D\u4F60\u7684\u624B \u2764\uFE0F",
    face + " " + name + "\u6B6A\u5934\u770B\u7740\u4F60 (\u00B7\u03C9\u00B7)",
    face + " " + name + "\u53D1\u51FA\u4E86\u6EE1\u610F\u7684\u5495\u5495\u58F0 \uD83D\uDC95",
  ];
  console.log(reactions[Math.floor(Math.random() * reactions.length)]);
}

function handleStats() {
  var userId = resolveUserId();
  var bones = rollBones(userId);
  var soul = loadSoul();
  var spritesMod = loadSprites();
  console.log(renderStatsCard(bones, soul, spritesMod));
}

function handleMute() {
  setMuted(true);
  console.log("\uD83D\uDD07 Buddy auto-reactions muted. Use /buddy unmute to restore.");
}

function handleUnmute() {
  setMuted(false);
  console.log("\uD83D\uDD0A Buddy auto-reactions unmuted!");
}

// ── Main ────────────────────────────────────────────────────────────

function main() {
  var args = process.argv.slice(2).join(" ").trim().toLowerCase();
  switch (args) {
    case "": handleHatch(); break;
    case "pet": handlePet(); break;
    case "stats": handleStats(); break;
    case "mute": handleMute(); break;
    case "unmute": handleUnmute(); break;
    default:
      console.log("Unknown buddy command: " + args);
      console.log("Available: /buddy, /buddy pet, /buddy stats, /buddy mute, /buddy unmute");
  }
}

main();
