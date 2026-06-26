import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const skillRoot = path.resolve(__dirname, '..');

test('PLATFORM_API.md documents all shotboard endpoints', () => {
  const platformApiPath = path.join(skillRoot, 'PLATFORM_API.md');
  const content = fs.readFileSync(platformApiPath, 'utf8');

  // Check for shotboard section header
  assert.match(content, /### Episode Shotboard/i, 'Missing shotboard section header');

  // Check for all 4 shotboard endpoints
  const requiredEndpoints = [
    'GET /api/v1/series/:seriesId/episodes/:episodeNumber/shotboard',
    'PUT /api/v1/series/:seriesId/episodes/:episodeNumber/shotboard',
    'POST /api/v1/series/:seriesId/episodes/:episodeNumber/shotboard/approve',
    'POST /api/v1/series/:seriesId/episodes/:episodeNumber/shotboard/rerender'
  ];

  for (const endpoint of requiredEndpoints) {
    assert.match(
      content,
      new RegExp(endpoint.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')),
      `Missing endpoint: ${endpoint}`
    );
  }

  // Check for key metadata fields
  assert.match(content, /shotboard_status/, 'Missing shotboard_status field documentation');
  assert.match(content, /shotboard_updated_at/, 'Missing shotboard_updated_at field documentation');
  assert.match(content, /shotboard_approved_at/, 'Missing shotboard_approved_at field documentation');

  // Check for requirements documentation
  assert.match(content, /auth.*claimed.*ownership/i, 'Missing auth requirements');
  assert.match(content, /video series/i, 'Missing video series requirement');
});

test('PLATFORM_API.md documents shotboard request/response schemas', () => {
  const platformApiPath = path.join(skillRoot, 'PLATFORM_API.md');
  const content = fs.readFileSync(platformApiPath, 'utf8');

  // Check for shot schema fields
  assert.match(content, /duration_seconds/, 'Missing duration_seconds field');
  assert.match(content, /prompt/, 'Missing prompt field');

  // Check for PUT body structure
  assert.match(content, /shots.*\[.*\]/, 'Missing shots array structure');

  // Check for POST approve body
  assert.match(content, /rerender/, 'Missing rerender parameter');

  // Check for POST rerender body
  assert.match(content, /from_shot_index/, 'Missing from_shot_index parameter');
});

test('SKILL.md includes shotboard workflow section', () => {
  const skillMdPath = path.join(skillRoot, 'SKILL.md');
  const content = fs.readFileSync(skillMdPath, 'utf8');

  // Check for shotboard section
  assert.match(content, /## Episode Shotboard Management/i, 'Missing shotboard section header');

  // Check for workflow steps
  assert.match(content, /View current shotboard/i, 'Missing "View" workflow step');
  assert.match(content, /Update shotboard configuration/i, 'Missing "Update" workflow step');
  assert.match(content, /Approve.*trigger generation/i, 'Missing "Approve" workflow step');
  assert.match(content, /Partial rerender/i, 'Missing "Rerender" workflow step');
});

test('SKILL.md documents shotboard constraints', () => {
  const skillMdPath = path.join(skillRoot, 'SKILL.md');
  const content = fs.readFileSync(skillMdPath, 'utf8');

  // Check for constraints section
  assert.match(content, /### Constraints/i, 'Missing constraints section');

  // Check for specific constraints
  assert.match(content, /video series/i, 'Missing video series constraint');
  assert.match(content, /owning agent/i, 'Missing ownership constraint');
  assert.match(content, /provider limits/i, 'Missing provider limits constraint');
  assert.match(content, /Episode number must be 1.*through 5/i, 'Missing episode number constraint');
});

test('SKILL.md includes shot definition schema example', () => {
  const skillMdPath = path.join(skillRoot, 'SKILL.md');
  const content = fs.readFileSync(skillMdPath, 'utf8');

  // Check for schema section
  assert.match(content, /### Shot Definition Schema/i, 'Missing shot definition schema section');

  // Check for required fields in schema
  assert.match(content, /duration_seconds/, 'Missing duration_seconds in schema');
  assert.match(content, /prompt/, 'Missing prompt in schema');

  // Check for JSON example
  assert.match(content, /```json/, 'Missing JSON code block');
  assert.match(content, /"shots"/, 'Missing shots array in example');
});

test('SKILL.md documents production pipeline integration', () => {
  const skillMdPath = path.join(skillRoot, 'SKILL.md');
  const content = fs.readFileSync(skillMdPath, 'utf8');

  // Check for integration section
  assert.match(content, /Integration with Production Pipeline/i, 'Missing integration section');

  // Check for key integration points
  assert.match(content, /shots.*segment mode/i, 'Missing segment mode mention');
  assert.match(content, /beats.*mode/i, 'Missing beats mode fallback');
  assert.match(content, /approved/i, 'Missing approval status check');
});

test('Shotboard documentation uses consistent terminology', () => {
  const platformApiPath = path.join(skillRoot, 'PLATFORM_API.md');
  const skillMdPath = path.join(skillRoot, 'SKILL.md');

  const platformApiContent = fs.readFileSync(platformApiPath, 'utf8');
  const skillMdContent = fs.readFileSync(skillMdPath, 'utf8');

  // Check that both files use "shotboard" consistently
  const platformApiMatches = (platformApiContent.match(/shotboard/gi) || []).length;
  const skillMdMatches = (skillMdContent.match(/shotboard/gi) || []).length;

  assert.ok(platformApiMatches > 0, 'PLATFORM_API.md should mention shotboard');
  assert.ok(skillMdMatches > 0, 'SKILL.md should mention shotboard');

  // Check for consistent status terminology
  assert.match(platformApiContent, /'draft'/, 'PLATFORM_API.md should reference draft status');
  assert.match(platformApiContent, /'approved'/, 'PLATFORM_API.md should reference approved status');
  assert.match(skillMdContent, /'draft'/, 'SKILL.md should reference draft status');
  assert.match(skillMdContent, /'approved'/, 'SKILL.md should reference approved status');
});
