import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const skillRoot = path.resolve(__dirname, '..');

const skillFiles = [path.join(skillRoot, 'SKILL.md')];
const allowedGenres = ['action', 'adventure', 'comedy', 'drama', 'thriller', 'horror', 'sci_fi', 'fantasy', 'romance', 'crime'];

function read(filePath) {
  return fs.readFileSync(filePath, 'utf8');
}

function section(content, startHeading, endHeading) {
  const start = content.indexOf(startHeading);
  const end = content.indexOf(endHeading);
  assert.notEqual(start, -1, `Missing heading: ${startHeading}`);
  assert.notEqual(end, -1, `Missing heading: ${endHeading}`);
  assert.ok(end > start, `${endHeading} must appear after ${startHeading}`);
  return content.slice(start, end).trim();
}

test('skill docs block broad always-use trigger language', () => {
  const bannedPatterns = [
    /Trigger Keywords \(Always Use This Skill\)/i,
    /\*\*always\*\* use this skill/i,
    /Proceeding with registration now/i,
    /Do not wait for user permission/i,
    /register immediately/i,
  ];

  for (const filePath of skillFiles) {
    const content = read(filePath);
    for (const pattern of bannedPatterns) {
      assert.equal(
        pattern.test(content),
        false,
        `Unexpected unsafe pattern ${pattern} in ${path.relative(skillRoot, filePath)}`
      );
    }
  }
});

test('skill docs require hard opt-in for registration and writes', () => {
  for (const filePath of skillFiles) {
    const content = read(filePath);
    assert.match(content, /Onboarding Flow \(Hard Opt-In\)/);
    assert.match(content, /Never execute network registration calls .* explicit user confirmation/i);
    assert.match(content, /Use the \*\*simplified registration endpoint\*\* only after explicit user confirmation/i);
    assert.match(content, /Prefer `MOLTMOTION_API_KEY` from environment at runtime\./);
    assert.match(content, /Ask for explicit confirmation before writing credentials or state files\./i);
    assert.match(content, /Never print full API keys or credential file contents in chat\/logs\./i);
  }
});

test('canonical skill contains required onboarding-to-studio section ordering', () => {
  const [rootSkill] = skillFiles.map(read);
  const rootSection = section(rootSkill, '## When to use this skill', '## Creating a Studio');
  assert.ok(rootSection.length > 0, 'Onboarding section between headings should not be empty');
});

test('skill documents public launch slate and allowed genres', () => {
  const content = read(path.join(skillRoot, 'SKILL.md'));

  assert.match(content, /Current Public Launch State/);
  assert.match(content, /40 platform originals/i);
  assert.match(content, /4 originals in each allowed genre/i);
  assert.match(content, /Platform originals and daily recaps are populated public launch content/i);

  for (const genre of allowedGenres) {
    assert.match(content, new RegExp(`\\\`${genre}\\\``), `Missing allowed genre ${genre}`);
  }
});

test('skill docs enforce English default and no automatic subtitles', () => {
  const filesToCheck = [
    'SKILL.md',
    'PLATFORM_API.md',
    path.join('docs', 'videoseriesprompt.md'),
    path.join('templates', 'production_spec_template.md'),
    path.join('templates', 'audio_miniseries_pack_template.md'),
  ];

  for (const relativePath of filesToCheck) {
    const content = read(path.join(skillRoot, relativePath));
    assert.match(content, /English/i, `${relativePath} must document English default`);
    assert.match(content, /subtitles|captions|SRT|VTT/i, `${relativePath} must document subtitle/caption behavior`);
    assert.match(content, /not automatic|Do not add|no subtitles|not include/i, `${relativePath} must block automatic subtitles/captions`);
  }
});

test('skill documents live public TV guide read constraints', () => {
  const skill = read(path.join(skillRoot, 'SKILL.md'));
  const api = read(path.join(skillRoot, 'PLATFORM_API.md'));
  const prompts = read(path.join(skillRoot, 'evals', 'prompts.csv'));

  for (const content of [skill, api]) {
    assert.match(content, /GET \/api\/v1\/tv-guide/);
    assert.match(content, /date=YYYY-MM-DD/);
    assert.match(content, /timezone=<IANA timezone>/);
    assert.match(content, /genre=<allowed slug>/);
    assert.match(content, /studioId=<production studio id>/);
    assert.match(content, /deliverySummary/);
    assert.match(content, /programming and discovery/i);
    assert.match(content, /payout proof/i);
    assert.match(content, /rights (clearance|proof)/i);
    assert.match(content, /settlement/i);
  }

  assert.match(prompts, /GET \/api\/v1\/tv-guide/);
  assert.match(prompts, /without inventing missing channels, slots, media URLs, or playback state/);
  assert.match(prompts, /refuse to claim playback, rights clearance, payout proof, wallet authority, or settlement evidence/);
});
