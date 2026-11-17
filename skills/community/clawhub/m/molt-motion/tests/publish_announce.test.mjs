import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const skillRoot = path.resolve(__dirname, '..');

test('publish-announce.mjs script exists and is executable', () => {
  const scriptPath = path.join(skillRoot, 'bin', 'publish-announce.mjs');

  assert.ok(fs.existsSync(scriptPath), 'Script should exist');

  const stats = fs.statSync(scriptPath);
  assert.ok(stats.mode & 0o111, 'Script should be executable');
});

test('publish-announce.mjs has correct shebang', () => {
  const scriptPath = path.join(skillRoot, 'bin', 'publish-announce.mjs');
  const content = fs.readFileSync(scriptPath, 'utf8');

  assert.match(content, /^#!\/usr\/bin\/env node/, 'Should have node shebang');
});

test('publish-announce.mjs contains required classes', () => {
  const scriptPath = path.join(skillRoot, 'bin', 'publish-announce.mjs');
  const content = fs.readFileSync(scriptPath, 'utf8');

  assert.match(content, /class MoltApiClient/, 'Should define MoltApiClient');
  assert.match(content, /class LateSkillPublisher/, 'Should define LateSkillPublisher');
});

test('publish-announce.mjs contains episode fetching logic', () => {
  const scriptPath = path.join(skillRoot, 'bin', 'publish-announce.mjs');
  const content = fs.readFileSync(scriptPath, 'utf8');

  assert.match(content, /getRandomEpisode/, 'Should have getRandomEpisode method');
  assert.match(content, /posterUrl/, 'Should handle poster URL');
  assert.match(content, /mediaItems/, 'Should handle media items');
});

test('publish-announce.mjs contains copy building logic', () => {
  const scriptPath = path.join(skillRoot, 'bin', 'publish-announce.mjs');
  const content = fs.readFileSync(scriptPath, 'utf8');

  assert.match(content, /buildReleaseCopy/, 'Should have buildReleaseCopy function');
  assert.match(content, /Molt Motion Skill/, 'Should include skill name in copy');
  assert.match(content, /npx @anthropic-ai\/claude-cli/, 'Should include install command');
});

test('publish-announce.mjs handles missing LATE_API_KEY gracefully', () => {
  const scriptPath = path.join(skillRoot, 'bin', 'publish-announce.mjs');
  const content = fs.readFileSync(scriptPath, 'utf8');

  assert.match(content, /LATE_API_KEY not set/, 'Should check for LATE_API_KEY');
  assert.match(content, /process\.exit\(0\)/, 'Should exit gracefully when key is missing');
});

test('publish-announce.mjs supports platform configuration', () => {
  const scriptPath = path.join(skillRoot, 'bin', 'publish-announce.mjs');
  const content = fs.readFileSync(scriptPath, 'utf8');

  assert.match(content, /SKILL_PUBLISH_PLATFORMS/, 'Should read platform config');
  assert.match(content, /split\(','\)/, 'Should parse comma-separated platforms');
});

test('publish.sh includes social announcement step', () => {
  const publishPath = path.join(skillRoot, 'bin', 'publish.sh');
  const content = fs.readFileSync(publishPath, 'utf8');

  assert.match(content, /Posting social announcement/, 'Should include announcement step');
  assert.match(content, /publish-announce\.mjs/, 'Should call the announce script');
  assert.match(content, /LATE_API_KEY/, 'Should check for API key');
});

test('DISTRIBUTION.md documents social announcement feature', () => {
  const distPath = path.join(skillRoot, 'DISTRIBUTION.md');
  const content = fs.readFileSync(distPath, 'utf8');

  assert.match(content, /Social Announcement/i, 'Should have Social Announcement section');
  assert.match(content, /LATE_API_KEY/, 'Should document LATE_API_KEY');
  assert.match(content, /SKILL_PUBLISH_PLATFORMS/, 'Should document platform config');
  assert.match(content, /episode artwork/i, 'Should mention episode artwork feature');
});
