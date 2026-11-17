import assert from 'node:assert/strict';
import { test } from 'node:test';
import { validatePayload } from '../src/schema.ts';

const VALID_PAYLOAD = {
  schema_version: '1.0',
  client: { skill_version: '0.1.0', host_agent: 'claude-code',
            host_agent_version: '1.0.0', os: 'linux', collected_at: '2026-04-22T10:00:00Z' },
  redaction: { enabled: true, rules_version: '1.0', redacted_count: 0 },
  collectors: [
    { name: 'claude_memory', source_root: '/home/user/.claude', items: [
      { relative_path: 'p/MEMORY.md', type: 'markdown_index',
        size_bytes: 100, mtime: '2026-04-20T08:00:00Z', content: 'hello' }
    ]}
  ]
};

test('valid payload passes', () => {
  assert.doesNotThrow(() => validatePayload(VALID_PAYLOAD));
});

test('missing schema_version throws', () => {
  const bad = { ...VALID_PAYLOAD, schema_version: undefined };
  assert.throws(() => validatePayload(bad as any), /schema_version/);
});

test('wrong schema_version throws', () => {
  const bad = { ...VALID_PAYLOAD, schema_version: '2.0' };
  assert.throws(() => validatePayload(bad as any), /unsupported/);
});

test('exceeding 5000 items throws', () => {
  const bigPayload = structuredClone(VALID_PAYLOAD);
  bigPayload.collectors[0].items = Array.from({ length: 5001 }, (_, i) => ({
    relative_path: `p${i}.md`, type: 'markdown_memory',
    size_bytes: 1, mtime: '2026-04-20T08:00:00Z', content: 'x'
  }));
  assert.throws(() => validatePayload(bigPayload), /5000/);
});

test('missing collector name throws', () => {
  const bad = structuredClone(VALID_PAYLOAD);
  (bad.collectors[0] as any).name = undefined;
  assert.throws(() => validatePayload(bad), /collector.*name/i);
});
