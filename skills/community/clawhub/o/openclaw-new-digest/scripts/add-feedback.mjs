#!/usr/bin/env node

import {
  readJSON,
  writeJSON,
  todayStr,
  nowISO,
  feedbackPath,
  generateId,
} from "./lib/storage.mjs";

function usage() {
  console.error(
    `Usage: add-feedback.mjs [--date YYYY-MM-DD] --slot morning|noon|evening [--item-id <id>] "feedback text"

Options:
  --date <date>     Target push date (default: today)
  --slot <slot>     Push slot: morning, noon, or evening (required)
  --item-id <id>    Optional: ID of a specific item to attach feedback to

Example:
  node add-feedback.mjs --slot morning "希望多一些DeFi相关的新闻"
  node add-feedback.mjs --date 2026-03-06 --slot noon --item-id item-002 "这条总结太简略了"`
  );
  process.exit(2);
}

const args = process.argv.slice(2);
if (args.length === 0 || args[0] === "-h" || args[0] === "--help") usage();

let date = todayStr();
let slot = null;
let itemId = null;
let feedbackText = null;

for (let i = 0; i < args.length; i++) {
  const a = args[i];
  if (a === "--date") {
    date = args[++i];
    continue;
  }
  if (a === "--slot") {
    slot = args[++i];
    continue;
  }
  if (a === "--item-id") {
    itemId = args[++i];
    continue;
  }
  if (a.startsWith("-")) {
    console.error(`Unknown arg: ${a}`);
    usage();
  }
  feedbackText = a;
}

if (!slot || !["morning", "noon", "evening"].includes(slot)) {
  console.error(
    `Error: --slot is required and must be one of: morning, noon, evening. Got: "${slot}"`
  );
  process.exit(1);
}

if (!feedbackText) {
  console.error("Error: feedback text is required as the last argument.");
  process.exit(1);
}

const filePath = feedbackPath(date, slot);
const dateCompact = date.replace(/-/g, "");
const pushId = `push-${dateCompact}-${slot}`;

let record = readJSON(filePath);
if (!record) {
  record = {
    push_id: pushId,
    feedbacks: [],
  };
}

const fb = {
  id: generateId("fb"),
  item_id: itemId || null,
  text: feedbackText,
  created_at: nowISO(),
};

record.feedbacks.push(fb);
writeJSON(filePath, record);

console.log(`## Feedback Recorded\n`);
console.log(`- **ID**: ${fb.id}`);
console.log(`- **Push**: ${pushId}`);
if (itemId) {
  console.log(`- **Item**: ${itemId}`);
}
console.log(`- **Text**: ${feedbackText}`);
console.log(`- **Path**: ${filePath}`);
