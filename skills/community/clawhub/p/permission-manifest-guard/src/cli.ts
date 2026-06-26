#!/usr/bin/env node

// CLI entrypoint: takes a skill directory path, prints markdown manifest to
// stdout, writes JSON manifest to <skillDir>/permission-manifest.json.

import { writeFile, stat } from 'node:fs/promises';
import { resolve, join } from 'node:path';
import { analyzeSkill } from './index.js';

const USAGE = 'Usage: permission-manifest-guard <skill-directory>';
const JSON_FILENAME = 'permission-manifest.json';

async function main(): Promise<void> {
  const arg = process.argv[2];
  if (!arg) {
    process.stderr.write(`${USAGE}\n`);
    process.exitCode = 1;
    return;
  }

  const skillDir = resolve(arg);

  // Fail early if the path does not exist or is not a directory.
  let stats;
  try {
    stats = await stat(skillDir);
  } catch {
    process.stderr.write(`Error: path does not exist: ${skillDir}\n`);
    process.exitCode = 1;
    return;
  }
  if (!stats.isDirectory()) {
    process.stderr.write(`Error: not a directory: ${skillDir}\n`);
    process.exitCode = 1;
    return;
  }

  let result;
  try {
    result = await analyzeSkill(skillDir);
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    process.stderr.write(`Error: analyzeSkill failed: ${msg}\n`);
    process.exitCode = 1;
    return;
  }

  // Print diagnostics to stderr so they don't pollute piped markdown output.
  for (const d of result.diagnostics) {
    process.stderr.write(`[${d.stage}] ${d.file}: ${d.message}\n`);
  }

  process.stdout.write(result.markdownManifest);

  const jsonPath = join(skillDir, JSON_FILENAME);
  await writeFile(jsonPath, JSON.stringify(result.jsonManifest, null, 2) + '\n', 'utf-8');
  process.stderr.write(`Wrote ${jsonPath}\n`);
}

main();
