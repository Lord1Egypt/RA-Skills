#!/usr/bin/env node
/**
 * Liu Yao six casts (bottom → top).
 * Coin model: 3 coins; heads=3 tails=2 (product-style simplified):
 *   sum 9 → old yang (moving), 8 → young yang, 7 → young yin, 6 → old yin (moving)
 * Usage:
 *   node cast.mjs [--seed N]
 *   node cast.mjs --throws "9,8,7,6,8,9"
 */
import { randomInt } from "node:crypto";

function mulberry32(a) {
  return function () {
    let t = (a += 0x6d2b79f5);
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function lineFromSum(sum) {
  if (sum === 9) return { yin_yang: "yang", moving: true, label: "old_yang", sum };
  if (sum === 8) return { yin_yang: "yang", moving: false, label: "young_yang", sum };
  if (sum === 7) return { yin_yang: "yin", moving: false, label: "young_yin", sum };
  if (sum === 6) return { yin_yang: "yin", moving: true, label: "old_yin", sum };
  throw new Error(`invalid coin sum ${sum}`);
}

function randomThrow(rand) {
  // three coins: each H=3 T=2
  let sum = 0;
  for (let i = 0; i < 3; i++) sum += rand() < 0.5 ? 3 : 2;
  return sum;
}

function parseArgs(argv) {
  const out = { seed: undefined, throws: undefined };
  for (let i = 2; i < argv.length; i++) {
    if (argv[i] === "--seed") out.seed = Number(argv[++i]);
    else if (argv[i] === "--throws") out.throws = argv[++i];
  }
  return out;
}

const NAMES = ["chu", "er", "san", "si", "wu", "shang"];
const cli = parseArgs(process.argv);
const seed = cli.seed ?? randomInt(1, 2 ** 31 - 1);
const rand = mulberry32(seed >>> 0);

let sums;
if (cli.throws) {
  sums = cli.throws.split(/[,:\s]+/).map((s) => Number(s.trim()));
  if (sums.length !== 6 || sums.some((n) => ![6, 7, 8, 9].includes(n))) {
    process.stderr.write("throws must be six values in {6,7,8,9}\n");
    process.exit(1);
  }
} else {
  sums = Array.from({ length: 6 }, () => randomThrow(rand));
}

const lines = sums.map((sum, i) => {
  const L = lineFromSum(sum);
  return {
    index: i + 1,
    name: NAMES[i],
    ...L,
    binary: L.yin_yang === "yang" ? 1 : 0
  };
});

const changed = lines.map((L) => ({
  ...L,
  yin_yang: L.moving ? (L.yin_yang === "yang" ? "yin" : "yang") : L.yin_yang,
  moving: false,
  binary: L.moving ? (L.binary ^ 1) : L.binary
}));

const hasMoving = lines.some((L) => L.moving);

process.stdout.write(
  JSON.stringify(
    {
      ok: true,
      seed: cli.throws ? null : seed,
      order: "bottom_to_top",
      lines,
      original_bits: lines.map((L) => L.binary).join(""),
      resulting_bits: hasMoving ? changed.map((L) => L.binary).join("") : null,
      has_moving: hasMoving,
      wiki_hint: {
        method: "liuyao.method.six-casts",
        rule: "liuyao.rule.ben-zhi-bian",
        index: "liuyao.table.64-gua",
        classics: "shared.work.yijing"
      }
    },
    null,
    2
  ) + "\n"
);
