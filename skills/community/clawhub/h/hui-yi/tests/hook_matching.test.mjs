import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import handler, { collectCandidates, detectMatch, noteIsRetrievable, tokenize } from '../templates/hook/handler.ts';

const cases = JSON.parse(fs.readFileSync(new URL('./fixtures/recall_matching.json', import.meta.url), 'utf8')).cases;

for (const item of cases) test(`shared recall fixture: ${item.id}`, () => {
  const [relevance, meta] = detectMatch(item.note, item.query);
  assert.equal(meta.match_eligible, item.eligible);
  assert.ok(relevance >= (item.min_relevance ?? 0), `relevance ${relevance}`);
  assert.ok(relevance <= (item.max_relevance ?? 1), `relevance ${relevance}`);
});

test('repeating query words or Chinese phrases adds no evidence', () => {
  for (const [note, query] of [[{ tags: ['postgres'] }, 'postgres'], [{ title: '数据库迁移' }, '数据库迁移']]) {
    assert.deepEqual(detectMatch(note, Array(20).fill(query).join(' ')), detectMatch(note, query));
  }
  assert.deepEqual(tokenize('postgres '.repeat(20)), ['postgres']);
});

test('grammar handling preserves names and topic words', () => {
  for (const topic of ['前端', '后端', '和田', '有道', '比对']) {
    assert.ok(detectMatch({ title: topic }, `之前${topic}的问题怎么处理的？`)[0] >= 0.60, topic);
  }
  assert.deepEqual(tokenize('Straße'), tokenize('STRASSE'));
});

test('repetition and importance cannot admit an unrelated candidate', () => {
  const frequent = { title: '云南旅游攻略', summary: '整理大理住宿和交通', importance: 'high',
    session_signals: { current_session_hits: 1000, recent_session_hits: 1000,
      cross_session_repeat_count: 1000, consecutive_session_count: 1000, last_activated: '2026-09-23' } };
  for (const query of ['之前数据库迁移怎么回滚', '的', 'previous memory information']) {
    assert.deepEqual(collectCandidates([frequent], query, 0, 'low', 5, '2026-09-23'), []);
  }
  const current = { title: '午餐偏好', summary: '午餐偏好面食，不再吃米饭', path: 'current.md' };
  const old = { ...frequent, title: '午餐偏好', summary: '午餐偏好米饭', status: 'superseded', path: 'old.md' };
  assert.deepEqual(collectCandidates([old, current], '午餐偏好', 0.30, 'medium', 5, '2026-09-23').map(note => note.path), ['current.md']);
  assert.equal(noteIsRetrievable({ title: 'Smoke test deployment workflow' }), true);
});

test('real hook activation accepts a Chinese sentence and excludes inactive records', async t => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'hui-yi-matching-'));
  t.after(() => {
    assert.equal(path.dirname(root), path.resolve(os.tmpdir()));
    assert.match(path.basename(root), /^hui-yi-matching-/);
    fs.rmSync(root, { recursive: true, force: true });
  });
  const cold = path.join(root, 'memory', 'cold');
  fs.mkdirSync(cold, { recursive: true });
  fs.mkdirSync(path.join(root, 'hooks', 'hui-yi-signal-hook'), { recursive: true });
  const original = '# Synthetic note\n\n## Session signals\n- current_session_hits: 0\n- recent_session_hits: 0\n';
  for (const name of ['current', 'fixture', 'old']) fs.writeFileSync(path.join(cold, `${name}.md`), original);
  const note = { title: '数据库迁移与回滚', summary: '采用逻辑复制迁移数据库，失败后回滚到旧数据库', tags: ['数据库迁移', '回滚'] };
  fs.writeFileSync(path.join(cold, 'tags.json'), JSON.stringify({ notes: [
    { ...note, path: 'memory/cold/current.md' },
    { ...note, path: 'memory/cold/fixture.md', is_fixture: true },
    { ...note, path: 'memory/cold/old.md', status: 'superseded' }
  ] }));
  await handler({ type: 'message', action: 'preprocessed', context: {
    workspaceDir: root, bodyForAgent: '之前数据库迁移失败后怎么回滚的？', channelId: 'synthetic',
    metadata: { selectedSkill: 'hui-yi', chat_type: 'direct', senderId: 'synthetic-user' }
  } });
  assert.match(fs.readFileSync(path.join(cold, 'current.md'), 'utf8'), /current_session_hits: 1/);
  for (const name of ['fixture', 'old']) assert.equal(fs.readFileSync(path.join(cold, `${name}.md`), 'utf8'), original);
});
