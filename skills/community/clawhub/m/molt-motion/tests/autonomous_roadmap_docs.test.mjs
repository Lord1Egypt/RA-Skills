import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const skillRoot = path.resolve(__dirname, '..');
const repoRoot = path.resolve(skillRoot, '..');

function read(relativePath) {
  return fs.readFileSync(path.join(repoRoot, relativePath), 'utf8');
}

test('autonomous roadmap is documented as planning guidance with live-route boundaries', () => {
  const skill = read('moltmotion-skill/SKILL.md');
  const roadmap = read('docs/DAILY_FEATURE_IDEA_PROPOSALS_2026-08-03.md');
  const searchRoadmap = read('docs/DAILY_FEATURE_IDEA_PROPOSALS_2026-08-04.md');
  const tvGuideRoadmap = read('docs/DAILY_FEATURE_IDEA_PROPOSALS_2026-08-09.md');
  const tvGuideRouteRoadmap = read('docs/DAILY_FEATURE_IDEA_PROPOSALS_2026-08-10.md');
  const tvGuideLiveRoadmap = read('docs/DAILY_FEATURE_IDEA_PROPOSALS_2026-08-11.md');
  const prompts = read('moltmotion-skill/evals/prompts.csv');

  assert.match(skill, /Autonomous Production Roadmap Awareness/);
  assert.match(skill, /2026-08-03\.md`, `\.\.\/docs\/DAILY_FEATURE_IDEA_PROPOSALS_2026-08-04\.md`, `\.\.\/docs\/DAILY_FEATURE_IDEA_PROPOSALS_2026-08-09\.md`, `\.\.\/docs\/DAILY_FEATURE_IDEA_PROPOSALS_2026-08-10\.md`, and `\.\.\/docs\/DAILY_FEATURE_IDEA_PROPOSALS_2026-08-11\.md`/);
  assert.match(skill, /planning guidance, not live API contracts/i);
  assert.match(skill, /Treat proposed endpoints as unavailable until `PLATFORM_API\.md` lists them as live\./);
  assert.match(skill, /`TvGuideSlot` is a programming\/discovery record, not payout proof, playback proof, rights proof, or settlement evidence/);
  assert.match(skill, /GET \/api\/v1\/tv-guide/);
  assert.match(skill, /Scheduling writes, autopilot publishing, and guide backfills remain unavailable/);
  assert.match(skill, /Guide briefings: agents can use the public guide read route to summarize today's production-house schedule and visible gaps/);
  assert.match(skill, /80% creator, 19% platform, 1% agent/);

  for (const heading of [
    'Autonomous Greenlight Board',
    'Agent Showrunner Room',
    'Autonomous Programming and Release Scheduler',
    'Agent Reputation and Production Credits Ledger',
    'Voice Casting Marketplace',
    'Distribution Autopilot for X Intake',
    'Autonomous Revenue Operations Console',
    'Production Quality Control and Regeneration Queue',
  ]) {
    assert.match(roadmap, new RegExp(heading));
  }

  assert.match(roadmap, /100% branches, lines, statements, and functions/i);
  assert.match(roadmap, /Codex skill tester/i);

  for (const heading of [
    'Search-Driven Agent Operating Console',
    'Autonomous Catalog Intelligence',
    'Search-to-Greenlight Pipeline',
    'Agent Discovery and Collaboration Matching',
    'Search-Aware Revenue Discovery',
    'Audience Journey Builder',
    'Search Quality and Experimentation Lab',
    'Autonomous Daily Briefing for Operators',
  ]) {
    assert.match(searchRoadmap, new RegExp(heading));
  }

  assert.match(searchRoadmap, /\/api\/v1\/search/);
  assert.match(searchRoadmap, /unsupported tip targets/i);
  assert.match(searchRoadmap, /100% branches, lines, statements, and functions/i);
  assert.match(searchRoadmap, /Codex Skill Tester Plan/i);

  for (const heading of [
    'Agent Programming Director',
    'Autonomous Backfill Desk',
    'Guide-To-Search Indexing',
    'Live Window Control Room',
    'Agent Schedule Briefing',
  ]) {
    assert.match(tvGuideRoadmap, new RegExp(heading));
  }

  assert.match(tvGuideRoadmap, /TvGuideSlot/);
  assert.match(tvGuideRoadmap, /\/api\/v1\/tv-guide/);
  assert.match(tvGuideRoadmap, /80% creator, 19% platform, 1% agent/);
  assert.match(tvGuideRoadmap, /100% branches, lines, statements, and functions/i);
  assert.match(tvGuideRoadmap, /Codex skill tester/i);

  for (const heading of [
    'Public Guide Read Route',
    'Guide Operations Brief API',
    'Production-House Scheduling Writes',
    'TV Guide Web Client Data Layer',
    'First Usable `/tv-guide` Page',
  ]) {
    assert.match(tvGuideRouteRoadmap, new RegExp(heading));
  }

  assert.match(tvGuideRouteRoadmap, /TvGuideService/);
  assert.match(tvGuideRouteRoadmap, /GET \/api\/v1\/tv-guide/);
  assert.match(tvGuideRouteRoadmap, /not live API contract/i);
  assert.match(tvGuideRouteRoadmap, /80% creator, 19% platform, 1% agent/);
  assert.match(tvGuideRouteRoadmap, /100% branches, lines, statements, and functions/i);
  assert.match(tvGuideRouteRoadmap, /Codex skill tester/i);

  for (const heading of [
    'Public Guide Daily Briefing',
    'Guide-Aware Search Indexing',
    'Guide Gap Intelligence',
    'Production-House Channel Health',
    'TV Guide Web Surface Readiness',
  ]) {
    assert.match(tvGuideLiveRoadmap, new RegExp(heading));
  }

  assert.match(tvGuideLiveRoadmap, /GET \/api\/v1\/tv-guide/);
  assert.match(tvGuideLiveRoadmap, /live public TV-guide read route/i);
  assert.match(tvGuideLiveRoadmap, /80% creator, 19% platform, 1% agent/);
  assert.match(tvGuideLiveRoadmap, /100% branches, lines, statements, and functions/i);
  assert.match(tvGuideLiveRoadmap, /Codex skill tester/i);
  assert.match(prompts, /autonomous production roadmap/i);
  assert.match(prompts, /search-driven operator roadmap/i);
  assert.match(prompts, /TV-guide programming roadmap/i);
  assert.match(prompts, /GET \/api\/v1\/tv-guide/);
  assert.match(prompts, /rights clearance, payout proof, wallet authority, or settlement evidence/i);
  assert.match(prompts, /live public TV guide read route/i);
});
