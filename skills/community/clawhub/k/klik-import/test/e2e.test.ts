// Requires: KLIK_BASE_URL env var pointing to a running Klik instance
// Run: KLIK_BASE_URL=http://localhost:8413 KLIK_IMPORT_CODE=123456 \
//      node --test --experimental-strip-types test/e2e.test.ts

import assert from 'node:assert/strict';
import { test } from 'node:test';
import { verifyCode, uploadPayload } from '../src/uploader.ts';
import type { ImportPayload } from '../src/types.ts';

const SKIP = !process.env.KLIK_BASE_URL;

test('full code → token → upload flow', { skip: SKIP ? 'Set KLIK_BASE_URL to run' : false }, async () => {
  const code = process.env.KLIK_IMPORT_CODE!;
  const opts = { baseUrl: process.env.KLIK_BASE_URL };

  const { import_token, user_id } = await verifyCode(code, opts);
  assert.ok(import_token.startsWith('klik_imp_'));
  assert.ok(user_id.length > 0);

  const payload: ImportPayload = {
    schema_version: '1.0',
    client: { skill_version: '0.1.0', host_agent: 'test', host_agent_version: '0', os: 'linux', collected_at: new Date().toISOString() },
    redaction: { enabled: true, rules_version: '1.0', redacted_count: 0 },
    collectors: [
      { name: 'claude_memory', source_root: '/tmp', items: [
        { relative_path: 'test.md', type: 'markdown_memory', size_bytes: 5, mtime: new Date().toISOString(), content: 'hello' }
      ]}
    ]
  };

  const result = await uploadPayload(payload, import_token, opts);
  assert.ok(result.import_id.length > 0);
  console.log('import_id:', result.import_id);
});
