import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';

const fixtures = [
  'legacy-guide.md',
  'event-record.md',
  'course-brief.md',
  'completed-web-project.md',
];

const readFixture = (name) =>
  readFile(new URL(`./fixtures/v08-summary-first/${name}`, import.meta.url), 'utf8');

const summaryBullets = (text) => {
  const match = text.match(/^## Summary\r?\n([\s\S]*?)(?=^## (?!Summary)|\z)/m);
  assert.ok(match, 'fixture must include a Summary section');
  return match[1].match(/^- .+$/gm) ?? [];
};

for (const name of fixtures) {
  test(`${name} is a long, summary-first synthetic fixture`, async () => {
    const text = await readFixture(name);
    assert.match(text, /^# .+/m);
    assert.match(text, /^## Summary\r?\n/m);
    assert.equal(summaryBullets(text).length, 6);
    assert.match(text, /^## Full Details\r?\n/m);
    assert.ok(text.split(/\r?\n/).length >= 120, 'fixture must be at least 120 lines');
  });
}
