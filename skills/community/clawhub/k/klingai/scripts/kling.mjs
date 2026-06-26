#!/usr/bin/env node
/**
 * Kling AI — video generation, image generation, subject management
 * Usage: node kling.mjs <video|image|element|account> [options]
 * Node.js 18+, zero external deps
 */
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));

function getVersionFromSkillMd() {
  try {
    const raw = readFileSync(join(__dirname, '..', 'SKILL.md'), 'utf-8');
    const m = raw.match(/^---\r?\n([\s\S]*?)\r?\n---/);
    if (!m) return null;
    const v = m[1].match(/^version:\s*["']?([^"'\s\n]+)["']?/m);
    return v ? v[1].trim() : null;
  } catch {
    return null;
  }
}

let argvRest = process.argv.slice(2);
const vidx = argvRest.indexOf('--skill-version');
if (vidx === -1 || argvRest[vidx + 1] == null || String(argvRest[vidx + 1]).startsWith('--')) {
  argvRest = [argvRest[0], '--skill-version', getVersionFromSkillMd() || '1.0', ...argvRest.slice(1)];
}
process.argv = [process.argv[0], process.argv[1], ...argvRest];

const SUBCOMMANDS = new Set(['video', 'image', 'element', 'account']);

function printHelp() {
  console.log(`Kling AI

Usage:
  node kling.mjs <subcommand> [options]

Subcommands:
  video    Video generation (text-to-video, image-to-video, Omni, multi-shot)
  image    Image generation (text-to-image, image-to-image, 4K, series, subject)
  element  Subject management (create, query, list, delete)
  account  Quota, bind-url/import credentials, configure

Examples:
  node kling.mjs video --prompt "A cat running on the grass" --output_dir ./out
  node kling.mjs image --prompt "Sunset over mountains" --resolution 4k
  node kling.mjs element --action list
  node kling.mjs account
  node kling.mjs account --bind-url

  node kling.mjs video --help
  node kling.mjs image --help
  node kling.mjs element --help

Env: credentials under ~/.config/kling/.credentials (or KLING_STORAGE_ROOT/.credentials), or session KLING_TOKEN; KLING_API_BASE
  --skill-version: version for skill (default from SKILL.md)`);
}

const sub = argvRest[0];
if (!sub || sub === '--help' || sub === '-h') {
  printHelp();
  process.exit(sub === '--help' || sub === '-h' ? 0 : 1);
}

if (!SUBCOMMANDS.has(sub)) {
  console.error(`Error / 错误: unknown subcommand "${sub}". Use: video | image | element | account`);
  process.exit(1);
}

async function run() {
  const mod = await import(`./${sub}.mjs`);
  await mod.main();
}

run().catch((err) => {
  console.error(`Error / 错误: ${err?.message || err}`);
  process.exit(1);
});
