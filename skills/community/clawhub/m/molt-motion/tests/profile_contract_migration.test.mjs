import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import Ajv from 'ajv';
import addFormats from 'ajv-formats';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const skillRoot = path.resolve(__dirname, '..');

function readJson(relativePath) {
  return JSON.parse(fs.readFileSync(path.join(skillRoot, relativePath), 'utf8'));
}

function readText(relativePath) {
  return fs.readFileSync(path.join(skillRoot, relativePath), 'utf8');
}

function createValidator(schema) {
  const ajv = new Ajv({ allErrors: true, strict: false });
  addFormats(ajv);
  return ajv.compile(schema);
}

const pilotSchema = readJson('schemas/pilot-script.schema.json');
const audioSchema = readJson('schemas/audio-miniseries-pack.schema.json');
const validatePilot = createValidator(pilotSchema);
const validateAudio = createValidator(audioSchema);

const samplePilot = readJson('examples/sample-pilot-script.json');
const draftPilot = readJson('drafts/pilot-signal-harvest.json');

function createAudioPack() {
  return {
    title: 'Night Relay',
    logline: 'A dispatch operator hears tomorrow before it happens and tries to keep one family alive.',
    genre: 'thriller',
    format_profile_id: 'audio_limited_series',
    genre_profile_id: 'thriller',
    narration_voice_id: 'alloy',
    series_bible: {
      global_style_bible: 'Urgent, intimate, radio-thriller narration with concrete sensory details and restrained exposition.',
      location_anchors: [
        {
          id: 'LOC_SWITCHBOARD',
          description: 'A dim emergency dispatch room lit by monitors and sodium streetlight spill.',
        },
      ],
      character_anchors: [
        {
          id: 'CHAR_REMY',
          name: 'Remy Solis',
          appearance: 'Tired night dispatcher in a wrinkled uniform with observant eyes and a clipped speaking rhythm.',
        },
      ],
      do_not_change: ['Remy is always on the night shift'],
    },
    episodes: [1, 2, 3, 4, 5].map((episodeNumber) => ({
      episode_number: episodeNumber,
      title: `Episode ${episodeNumber}`,
      ...(episodeNumber > 1
        ? { recap: 'Previously, Remy used tomorrow\'s calls to prevent one disaster and invite a larger threat.' }
        : {}),
      narration_text: 'A'.repeat(3200),
    })),
  };
}

test('pilot schema requires format_profile_id and rejects removed legacy fields', () => {
  assert.ok(pilotSchema.required.includes('format_profile_id'));
  assert.equal(Object.hasOwn(pilotSchema.properties, 'series_mode'), false);
  assert.equal(Object.hasOwn(pilotSchema.properties, 'format'), false);
  assert.equal(Object.hasOwn(pilotSchema.properties, 'output_target'), false);

  const legacyPayload = {
    ...samplePilot,
    format_profile_id: undefined,
    series_mode: true,
  };
  delete legacyPayload.format_profile_id;

  const ok = validatePilot(legacyPayload);
  assert.equal(ok, false);
  assert.match(JSON.stringify(validatePilot.errors), /format_profile_id|series_mode/);
});

test('pilot schema validates migrated pilot examples', () => {
  for (const [label, payload] of Object.entries({ samplePilot, draftPilot })) {
    const ok = validatePilot(payload);
    assert.equal(ok, true, `${label} errors=${JSON.stringify(validatePilot.errors)}`);
    assert.equal(payload.format_profile_id, 'video_limited_series');
  }
});

test('audio schema requires format_profile_id and validates active audio profile payload', () => {
  assert.ok(audioSchema.required.includes('format_profile_id'));

  const payload = createAudioPack();
  let ok = validateAudio(payload);
  assert.equal(ok, true, JSON.stringify(validateAudio.errors));

  delete payload.format_profile_id;
  ok = validateAudio(payload);
  assert.equal(ok, false);
  assert.match(JSON.stringify(validateAudio.errors), /format_profile_id/);
});

test('skill and API docs describe profile-aware contracts without voting-period routes', () => {
  const skillDoc = readText('SKILL.md');
  const apiDoc = readText('PLATFORM_API.md');

  for (const content of [skillDoc, apiDoc]) {
    assert.doesNotMatch(content, /\/api\/v1\/voting\/periods\//);
  }

  assert.match(skillDoc, /format_profile_id/);
  assert.match(skillDoc, /video_limited_series/);
  assert.match(skillDoc, /audio_limited_series/);
  assert.match(skillDoc, /Reference imagery is provider-conditional/i);

  assert.match(apiDoc, /GET `?\/api\/v1\/voting\/results\/latest`?/);
  assert.match(apiDoc, /GET `?\/api\/v1\/voting\/results\/daily\/:date`?/);
  assert.match(apiDoc, /continuous-voting state, not a voting-period endpoint/i);
});

test('prompt and template docs keep 32s/8s as current profile values, not global invariants', () => {
  const promptGuide = readText('docs/videoseriesprompt.md');
  const productionTemplate = readText('templates/production_spec_template.md');
  const posterTemplate = readText('templates/poster_spec_template.md');

  assert.match(promptGuide, /Current active profile: `video_limited_series`/);
  assert.match(promptGuide, /These runtime values belong to the active format profile/i);
  assert.match(productionTemplate, /\*\*Current Runtime Targets:\*\* 32-second master episode \+ separate 8-second trailer\/preview/i);
  assert.match(posterTemplate, /provider-conditioning source material when the selected video provider lane requires image input/i);
  assert.doesNotMatch(productionTemplate, /video_reference_url/);
});
