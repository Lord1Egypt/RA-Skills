#!/usr/bin/env npx tsx
/**
 * utter-transcript.ts — Get the current transcript from a running OpenUtter bot
 *
 * Usage:
 *   npx tsx skills/openutter/scripts/utter-transcript.ts
 *   npx tsx skills/openutter/scripts/utter-transcript.ts --last 20
 *
 * Finds the most recent transcript file and prints its contents.
 * Use this when the user asks "what are they saying?" or "what's happening in the meeting?"
 *
 * IMPORTANT: This is the correct way to get meeting content.
 * Do NOT use utter-screenshot.ts for this — screenshots are only for visual context.
 */

import { existsSync, readdirSync, readFileSync, statSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";

const TRANSCRIPTS_DIR = join(homedir(), ".openclaw", "workspace", "openutter", "transcripts");

function main() {
  const args = process.argv.slice(2);
  const lastIdx = args.indexOf("--last");
  const lastN = lastIdx >= 0 ? Number.parseInt(args[lastIdx + 1] ?? "0", 10) : 0;

  if (!existsSync(TRANSCRIPTS_DIR)) {
    console.error("No transcripts directory found. Is the bot running in a meeting?");
    process.exit(1);
  }

  // Find the most recent transcript file
  const files = readdirSync(TRANSCRIPTS_DIR)
    .filter((f) => f.endsWith(".txt"))
    .map((f) => ({
      name: f,
      path: join(TRANSCRIPTS_DIR, f),
      mtime: statSync(join(TRANSCRIPTS_DIR, f)).mtimeMs,
    }))
    .sort((a, b) => b.mtime - a.mtime);

  if (files.length === 0) {
    console.error("No transcript files found. Captions may not have been captured yet.");
    console.error("Make sure the bot is in a meeting and captions are enabled.");
    process.exit(1);
  }

  const latest = files[0]!;
  const content = readFileSync(latest.path, "utf-8").trim();

  if (!content) {
    console.log(`[OPENUTTER_TRANSCRIPT] ${latest.path}`);
    console.log("\n(No captions captured yet — is someone speaking?)");
    return;
  }

  const lines = content.split("\n");

  console.log(`[OPENUTTER_TRANSCRIPT] ${latest.path}`);
  console.log(`Transcript: ${latest.name} (${lines.length} lines)\n`);

  if (lastN > 0 && lines.length > lastN) {
    console.log(`(showing last ${lastN} of ${lines.length} lines)\n`);
    console.log(lines.slice(-lastN).join("\n"));
  } else {
    console.log(content);
  }
}

main();
