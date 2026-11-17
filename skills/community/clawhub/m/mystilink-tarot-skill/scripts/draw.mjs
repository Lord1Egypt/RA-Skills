#!/usr/bin/env node
/**
 * Tarot draw — RWS 78 deck, upright/reversed.
 * Usage:
 *   node draw.mjs --spread three-card [--seed N]
 *   echo '{"spread":"three-card","count":3}' | node draw.mjs
 */
import { createHash, randomInt } from "node:crypto";

const MAJORS = [
  ["tarot.card.major.00-fool", "The Fool"],
  ["tarot.card.major.01-magician", "The Magician"],
  ["tarot.card.major.02-high-priestess", "The High Priestess"],
  ["tarot.card.major.03-empress", "The Empress"],
  ["tarot.card.major.04-emperor", "The Emperor"],
  ["tarot.card.major.05-hierophant", "The Hierophant"],
  ["tarot.card.major.06-lovers", "The Lovers"],
  ["tarot.card.major.07-chariot", "The Chariot"],
  ["tarot.card.major.08-strength", "Strength"],
  ["tarot.card.major.09-hermit", "The Hermit"],
  ["tarot.card.major.10-wheel-of-fortune", "Wheel of Fortune"],
  ["tarot.card.major.11-justice", "Justice"],
  ["tarot.card.major.12-hanged-man", "The Hanged Man"],
  ["tarot.card.major.13-death", "Death"],
  ["tarot.card.major.14-temperance", "Temperance"],
  ["tarot.card.major.15-devil", "The Devil"],
  ["tarot.card.major.16-tower", "The Tower"],
  ["tarot.card.major.17-star", "The Star"],
  ["tarot.card.major.18-moon", "The Moon"],
  ["tarot.card.major.19-sun", "The Sun"],
  ["tarot.card.major.20-judgement", "Judgement"],
  ["tarot.card.major.21-world", "The World"]
];

const SUITS = [
  ["wands", "Wands"],
  ["cups", "Cups"],
  ["swords", "Swords"],
  ["pentacles", "Pentacles"]
];
const RANKS = [
  ["ace", "Ace"],
  ["2", "Two"],
  ["3", "Three"],
  ["4", "Four"],
  ["5", "Five"],
  ["6", "Six"],
  ["7", "Seven"],
  ["8", "Eight"],
  ["9", "Nine"],
  ["10", "Ten"],
  ["page", "Page"],
  ["knight", "Knight"],
  ["queen", "Queen"],
  ["king", "King"]
];

function buildDeck() {
  const deck = MAJORS.map(([id, name]) => ({ id, name, arcana: "major" }));
  for (const [suitSlug, suitName] of SUITS) {
    for (const [rankSlug, rankName] of RANKS) {
      deck.push({
        id: `tarot.card.${suitSlug}.${rankSlug}`,
        name: `${rankName} of ${suitName}`,
        arcana: "minor",
        suit: suitSlug
      });
    }
  }
  return deck;
}

function mulberry32(a) {
  return function () {
    let t = (a += 0x6d2b79f5);
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function parseArgs(argv) {
  const out = { spread: "three-card", count: undefined, seed: undefined };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--spread") out.spread = argv[++i];
    else if (a === "--count") out.count = Number(argv[++i]);
    else if (a === "--seed") out.seed = Number(argv[++i]);
  }
  return out;
}

const SPREAD_COUNTS = {
  "three-card": 3,
  "one-card": 1,
  "celtic-cross": 10
};

async function readStdinJson() {
  if (process.stdin.isTTY) return null;
  const chunks = [];
  for await (const c of process.stdin) chunks.push(c);
  const raw = Buffer.concat(chunks).toString("utf8").trim();
  if (!raw) return null;
  return JSON.parse(raw);
}

function shuffle(deck, rand) {
  const a = [...deck];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(rand() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

const cli = parseArgs(process.argv);
const stdin = await readStdinJson().catch(() => null);
const spread = stdin?.spread ?? cli.spread;
const count = stdin?.count ?? cli.count ?? SPREAD_COUNTS[spread] ?? 3;
const seed =
  stdin?.seed ??
  cli.seed ??
  randomInt(1, 2 ** 31 - 1);

const rand = mulberry32(seed >>> 0);
const deck = shuffle(buildDeck(), rand);
const positions =
  spread === "three-card"
    ? ["past", "present", "advice"]
    : Array.from({ length: count }, (_, i) => `position_${i + 1}`);

const cards = [];
for (let i = 0; i < count; i++) {
  const base = deck[i];
  const orientation = rand() < 0.5 ? "upright" : "reversed";
  cards.push({
    position: positions[i] ?? `position_${i + 1}`,
    id: base.id,
    name: base.name,
    arcana: base.arcana,
    suit: base.suit,
    orientation
  });
}

process.stdout.write(
  JSON.stringify(
    {
      ok: true,
      spread,
      seed,
      drawn_at: new Date().toISOString(),
      cards,
      wiki_hint: "GET /api/v1/pages/{id}?locale=en"
    },
    null,
    2
  ) + "\n"
);
