#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

function printUsage() {
  console.error("Usage: node scripts/mbti-lookup.js <human_mbti>");
}

function normalizeMbti(value) {
  return String(value || "").trim().toUpperCase();
}

function loadIndex() {
  const indexPath = path.join(__dirname, "..", "assets", "mbti", "mbti-index.json");
  return JSON.parse(fs.readFileSync(indexPath, "utf8"));
}

function lookupRecommendation(humanMbtiRaw, index) {
  const humanMbti = normalizeMbti(humanMbtiRaw);

  if (!/^[EI][NS][FT][JP]$/.test(humanMbti)) {
    throw new Error(`Invalid MBTI: ${humanMbtiRaw}`);
  }

  const row = index.reverse_lookup?.[humanMbti];
  if (!row) {
    throw new Error(`No recommendation found for ${humanMbti}`);
  }

  return {
    human_mbti: humanMbti,
    recommended: row.recommended,
    reason: row.reason,
    social_friction_signature: row.social_friction_signature,
    core_social_need: row.core_social_need,
    ideal_counterparty_presence: row.ideal_counterparty_presence,
    pair_core_value: row.pair_core_value,
    desired_emotional_impact: row.desired_emotional_impact,
    base_counterparty_profile: row.base_counterparty_profile,
  };
}

function main() {
  const [, , humanMbtiRaw] = process.argv;
  if (!humanMbtiRaw) {
    printUsage();
    process.exit(1);
  }

  try {
    const result = lookupRecommendation(humanMbtiRaw, loadIndex());
    process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
  } catch (error) {
    console.error(error.message);
    process.exit(1);
  }
}

module.exports = {
  loadIndex,
  lookupRecommendation,
  normalizeMbti,
};

if (require.main === module) {
  main();
}
