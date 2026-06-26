#!/usr/bin/env node
/**
 * OpenClaw Spirits — Deterministic spirit generation
 * 24 species, 5 rarities, 5 stats, eyes and accessories
 * Same math as Claude Code: mulberry32 PRNG + hashString
 */

const SALT = "openclaw-spirit-2026";

// === 24 Species ===
const SPECIES = [
  // Living (灵生) 1-12
  "mosscat", "inkoi", "embermoth", "frostpaw", "bellhop", "astortoise",
  "foldwing", "cogmouse", "umbracrow", "crackviper", "glowshroom", "bubbloom",
  // Elemental (元灵) 13-24
  "inkling", "rustbell", "mossrock", "frostfang", "loopwyrm", "bubbell",
  "cogbeast", "umbra", "stardust", "crackle", "wickling", "echochord"
];

// === Rarities (稀有度) ===
const RARITIES = ["mundane", "peculiar", "spirited", "phantom", "mythic"];
const RARITY_WEIGHTS = {
  mundane: 55,
  peculiar: 25,
  spirited: 12,
  phantom: 6,
  mythic: 2
};

// === Stats (属性) ===
const STAT_NAMES = ["intuition", "grit", "spark", "anchor", "edge"];

// === Eyes (眼睛) ===
const EYES = ["◦", "◈", "✧", "●", "◎", "⊙"];

// === Accessories (饰品) ===
const ACCESSORIES = ["none", "bell", "halo", "starmark", "thundermark", "scroll", "crownfire"];

// === PRNG: Mulberry32 ===
function mulberry32(seed) {
  let a = seed >>> 0;
  return function() {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

// === Hash function ===
function hashString(s) {
  let h = 2166136261;
  for (let i = 0; i < s.length; i++) {
    h ^= s.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return h >>> 0;
}

// === Helpers ===
function pick(rng, arr) {
  return arr[Math.floor(rng() * arr.length)];
}

function rollRarity(rng) {
  const total = Object.values(RARITY_WEIGHTS).reduce((a, b) => a + b, 0);
  let roll = rng() * total;
  for (const rarity of RARITIES) {
    roll -= RARITY_WEIGHTS[rarity];
    if (roll < 0) return rarity;
  }
  return "mundane";
}

const RARITY_FLOOR = {
  mundane: 5,
  peculiar: 15,
  spirited: 25,
  phantom: 35,
  mythic: 50
};

function rollStats(rng, rarity) {
  const floor = RARITY_FLOOR[rarity];
  // Peak stat and dump stat
  const peak = pick(rng, STAT_NAMES);
  let dump = pick(rng, STAT_NAMES);
  while (dump === peak) dump = pick(rng, STAT_NAMES);

  const stats = {};
  for (const name of STAT_NAMES) {
    if (name === peak) {
      stats[name] = Math.min(100, floor + 50 + Math.floor(rng() * 30));
    } else if (name === dump) {
      stats[name] = Math.max(1, floor - 10 + Math.floor(rng() * 15));
    } else {
      stats[name] = floor + Math.floor(rng() * 40);
    }
  }
  return stats;
}

function rollAccessory(rng, rarity) {
  if (rarity === "mundane") return "none";
  if (rarity === "peculiar") return rng() < 0.5 ? "none" : "bell";
  if (rarity === "spirited") return pick(rng, ["bell", "halo", "starmark"]);
  if (rarity === "phantom") return pick(rng, ["halo", "starmark", "thundermark", "scroll"]);
  if (rarity === "mythic") return "crownfire";
  return "none";
}

// === Main generation ===
function generate(userId) {
  const seed = hashString(userId + SALT);
  const rng = mulberry32(seed);

  const rarity = rollRarity(rng);
  const species = pick(rng, SPECIES);
  const eye = pick(rng, EYES);
  const accessory = rollAccessory(rng, rarity);
  const shiny = rng() < 0.01; // 1% shiny
  const stats = rollStats(rng, rarity);

  return {
    species,
    rarity,
    eye,
    accessory,
    shiny,
    stats
  };
}

// === CLI ===
if (require.main === module) {
  const userId = process.argv[2] || "test-user";
  const bones = generate(userId);
  console.log(JSON.stringify(bones, null, 2));
}

module.exports = { generate, SPECIES, RARITIES, STAT_NAMES };
