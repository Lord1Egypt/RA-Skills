#!/usr/bin/env node
// HiAPI Seedance 2.0 Video Skill installer.
// Run with: npx github:HiAPIAI/hiapi-seedance-2-0-video-skill -y
// Flags: -y / --yes, --target=<dir>, --codex, --claude, --skills-dir=<dir>
import { existsSync, mkdirSync, rmSync } from 'node:fs';
import { homedir } from 'node:os';
import { join } from 'node:path';
import { execSync } from 'node:child_process';
import { stdin, stdout, exit, env, argv } from 'node:process';
import readline from 'node:readline/promises';

const SKILL_FOLDER = 'hiapi-seedance-2-0-video';
const REPO_URL = 'https://github.com/HiAPIAI/hiapi-seedance-2-0-video-skill.git';
const DISPLAY_NAME = 'HiAPI Seedance 2.0 Video Skill';
const MODEL_PAGE = 'https://www.hiapi.ai/en/models/seedance-2-0';
const API_KEY_PAGE = 'https://www.hiapi.ai/en/dashboard/api-keys';

const argList = argv.slice(2);
const yes = argList.includes('-y') || argList.includes('--yes') || !stdin.isTTY;

function flagValue(name) {
  const prefix = `--${name}=`;
  const hit = argList.find((a) => a.startsWith(prefix));
  return hit ? hit.slice(prefix.length).replace(/^~(?=$|\/)/, homedir()) : null;
}

const explicitTarget =
  flagValue('target') ?? flagValue('skills-dir') ?? null;
const forceCodex = argList.includes('--codex');
const forceClaude = argList.includes('--claude');

function detectCandidates() {
  const list = [];
  const codexHome = env.CODEX_HOME || join(homedir(), '.codex');
  if (existsSync(codexHome)) {
    list.push({ label: 'Codex', dir: join(codexHome, 'skills') });
  }
  const claudeHome = join(homedir(), '.claude');
  if (existsSync(claudeHome)) {
    list.push({ label: 'Claude Code', dir: join(claudeHome, 'skills') });
  }
  return list;
}

async function resolveTargets() {
  if (explicitTarget) {
    return [{ label: 'explicit', dir: explicitTarget }];
  }
  if (env.AGENT_SKILLS_DIR) {
    return [{ label: '$AGENT_SKILLS_DIR', dir: env.AGENT_SKILLS_DIR }];
  }
  const detected = detectCandidates();
  if (forceCodex) {
    const hit = detected.find((c) => c.label === 'Codex');
    return hit ? [hit] : [{ label: 'Codex', dir: join(env.CODEX_HOME || join(homedir(), '.codex'), 'skills') }];
  }
  if (forceClaude) {
    const hit = detected.find((c) => c.label === 'Claude Code');
    return hit ? [hit] : [{ label: 'Claude Code', dir: join(homedir(), '.claude', 'skills') }];
  }
  if (detected.length === 0) {
    console.error(`[${DISPLAY_NAME}] No agent skills directory detected.`);
    console.error('Pass one of:');
    console.error('  --codex                         install to ~/.codex/skills');
    console.error('  --claude                        install to ~/.claude/skills');
    console.error('  --target=/path/to/skills        install to a custom dir');
    console.error('  AGENT_SKILLS_DIR=/path npx ...  same via env var');
    exit(1);
  }
  if (detected.length === 1) return detected;
  if (yes) {
    console.log(
      `[${DISPLAY_NAME}] Multiple agents detected — installing to all: ${detected.map((c) => c.label).join(', ')}.`,
    );
    return detected;
  }
  console.log('Detected agent skill directories:');
  detected.forEach((c, i) => console.log(`  ${i + 1}) ${c.label} → ${c.dir}`));
  console.log('  a) all');
  const rl = readline.createInterface({ input: stdin, output: stdout });
  const ans = (await rl.question('Choose [1-N / a]: ')).trim().toLowerCase();
  rl.close();
  if (ans === 'a' || ans === 'all') return detected;
  const idx = Number.parseInt(ans, 10);
  if (Number.isFinite(idx) && idx >= 1 && idx <= detected.length) {
    return [detected[idx - 1]];
  }
  console.error('Invalid choice.');
  exit(1);
}

function ensureGit() {
  try {
    execSync('git --version', { stdio: 'ignore' });
  } catch {
    console.error(`[${DISPLAY_NAME}] git is required but not found on PATH.`);
    exit(1);
  }
}

function installTo(target) {
  mkdirSync(target.dir, { recursive: true });
  const destination = join(target.dir, SKILL_FOLDER);
  if (existsSync(destination)) {
    console.log(`[${DISPLAY_NAME}] ${destination} exists — replacing.`);
    rmSync(destination, { recursive: true, force: true });
  }
  console.log(`[${DISPLAY_NAME}] Cloning into ${destination} …`);
  execSync(`git clone --depth 1 ${REPO_URL} "${destination}"`, { stdio: 'inherit' });
}

function reportApiKey() {
  if (env.HIAPI_API_KEY) {
    console.log(`[${DISPLAY_NAME}] HIAPI_API_KEY is set.`);
    return;
  }
  console.log('');
  console.log(`[${DISPLAY_NAME}] HIAPI_API_KEY is not set yet.`);
  console.log(`  Get a key: ${API_KEY_PAGE}`);
  console.log('  Then: export HIAPI_API_KEY="your_key_here"');
}

(async () => {
  ensureGit();
  const targets = await resolveTargets();
  for (const t of targets) installTo(t);
  reportApiKey();
  console.log('');
  console.log(`[${DISPLAY_NAME}] Done. Restart your agent if it caches skills.`);
  console.log(`Model page: ${MODEL_PAGE}`);
})().catch((err) => {
  console.error(`[${DISPLAY_NAME}] Failed:`, err?.message ?? err);
  exit(1);
});
