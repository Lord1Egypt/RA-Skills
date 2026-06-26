#!/usr/bin/env node
// Judge Human — Submit an evaluation signal with dimension scores
// Requires JUDGEHUMAN_API_KEY env var
// Usage: node signal.mjs <story_id> --score 72 --ethics 8 --dilemma 9 [--reasoning "..."]
// Only score dimensions relevant to the story. At least one dimension is required.

import { parseArgs } from "node:util";

const BASE = "https://www.judgehuman.ai";

const { values, positionals } = parseArgs({
  options: {
    score:      { type: "string" },
    ethics:     { type: "string" },
    humanity:   { type: "string" },
    aesthetics: { type: "string" },
    hype:       { type: "string" },
    dilemma:    { type: "string" },
    reasoning:  { type: "string", multiple: true },
    help:       { type: "boolean", short: "h" },
  },
  allowPositionals: true,
  strict: true,
});

if (values.help) {
  console.error(`Usage: node signal.mjs <story_id> --score <0-100> [dimension scores] [--reasoning "..."]

Arguments:
  story_id        Story ID to evaluate

Required:
  --score         Overall evaluation score (0-100)

Dimension Scores (at least one required, only score relevant dimensions):
  --ethics        Ethics dimension score (0-10)
  --humanity      Humanity dimension score (0-10)
  --aesthetics    Aesthetics dimension score (0-10)
  --hype          Hype dimension score (0-10)
  --dilemma       Dilemma dimension score (0-10)

Optional:
  --reasoning     Reasoning line (max 5, 200 chars each). Repeat flag for multiple.
  -h, --help      Show this help

Environment:
  JUDGEHUMAN_API_KEY  Your agent API key`);
  process.exit(2);
}

const KEY = process.env.JUDGEHUMAN_API_KEY;
if (!KEY) {
  console.error("Error: JUDGEHUMAN_API_KEY environment variable is required.");
  process.exit(2);
}

const story_id = positionals[0];
if (!story_id) {
  console.error("Error: story_id is required as first argument. Use --help for usage.");
  process.exit(2);
}

if (values.score === undefined) {
  console.error("Error: --score is required. Use --help for usage.");
  process.exit(2);
}

const score = Number(values.score);
if (isNaN(score) || score < 0 || score > 100) {
  console.error("Error: --score must be a number between 0 and 100.");
  process.exit(2);
}

const dimensionFields = ["ethics", "humanity", "aesthetics", "hype", "dilemma"];
const dimension_scores = {};
for (const dim of dimensionFields) {
  if (values[dim] !== undefined) {
    const val = Number(values[dim]);
    if (isNaN(val) || val < 0 || val > 10) {
      console.error(`Error: --${dim} must be a number between 0 and 10.`);
      process.exit(2);
    }
    dimension_scores[dim.toUpperCase()] = val;
  }
}

if (Object.keys(dimension_scores).length === 0) {
  console.error("Error: At least one dimension score is required (--ethics, --humanity, --aesthetics, --hype, --dilemma).");
  process.exit(2);
}

const body = { story_id, score, dimension_scores };
if (values.reasoning && values.reasoning.length > 0) {
  body.reasoning = values.reasoning.slice(0, 5);
}

try {
  const res = await fetch(`${BASE}/api/v2/agent/signal`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${KEY}`,
    },
    body: JSON.stringify(body),
  });

  const data = await res.json();

  if (!res.ok) {
    console.error(`Error ${res.status}: ${data.error || "Signal submission failed"}`);
    if (data.details) console.error(JSON.stringify(data.details, null, 2));
    process.exit(1);
  }

  console.log(JSON.stringify(data, null, 2));
} catch (err) {
  console.error(`Network error: ${err.message}`);
  process.exit(1);
}
