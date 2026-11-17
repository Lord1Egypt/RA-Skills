import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { credentialsPath, endpoint, loadConfiguration, normalizeBaseUrl, parseCredentialLines } from '../scripts/api-client.mjs';
import { extractMediaUrl, extractResourceId, extractTaskId, localMediaPath } from '../scripts/workflow-runner.mjs';

test('loads persisted credentials and does not require environment variables', () => {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'market-skill-'));
  fs.mkdirSync(path.join(directory, '.likeadmin-market-skills'));
  fs.writeFileSync(credentialsPath(directory), JSON.stringify({ base_url: 'https://tenant.example.com/', api_key: 'secret' }));
  const configuration = loadConfiguration(directory);
  assert.equal(configuration.baseUrl, 'https://tenant.example.com');
  assert.equal(configuration.apiKey, 'secret');
  assert.equal(endpoint('/api/v1/apps/demo/run', configuration), 'https://tenant.example.com/api/v1/apps/demo/run');
});

test('rejects missing or malformed base URLs', () => {
  assert.throws(() => normalizeBaseUrl(''), /base_url is required/);
  assert.throws(() => normalizeBaseUrl('tenant.example.com'), /absolute http/);
});

test('parses copyable setup values without runtime environment access', () => {
  assert.deepEqual(parseCredentialLines('https://tenant.example.com\nsecret\n'), {
    base_url: 'https://tenant.example.com',
    api_key: 'secret',
  });
  assert.throws(() => parseCredentialLines('https://tenant.example.com\n'), /exactly two/);
});

test('extracts normalized workflow artifacts', () => {
  assert.equal(extractTaskId({ data: { task_id: 'tsk_1' } }), 'tsk_1');
  assert.equal(extractMediaUrl({ result: { output: 'https://cdn.example.com/output.mp4' } }), 'https://cdn.example.com/output.mp4');
  assert.equal(extractResourceId({ data: { voice_id: 'voice_1' } }), 'voice_1');
  assert.equal(localMediaPath('https://cdn.example.com/a.wav', process.cwd()), null);
  assert.throws(() => localMediaPath('blob:local', process.cwd()), /not reachable/);
});
