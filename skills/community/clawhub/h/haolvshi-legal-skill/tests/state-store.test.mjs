import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { StateStore } from '../scripts/state-store.mjs';

test('任务状态和报告文件使用私有权限并可以恢复', async t => {
  const stateDir = await fs.mkdtemp(path.join(os.tmpdir(), 'lvpin-skill-test-'));
  t.after(() => fs.rm(stateDir, { recursive: true, force: true }));
  const store = new StateStore({ stateDir, stateTtlMs: 60_000 });
  const state = await store.create({ capability: 'consultation', stage: 'collecting' });
  const artifactPath = await store.writeArtifact(state.sessionId, 'report.html', '<h1>报告</h1>');
  const loaded = await store.load(state.sessionId);

  assert.equal(loaded.capability, 'consultation');
  assert.equal((await fs.stat(stateDir)).mode & 0o777, 0o700);
  assert.equal((await fs.stat(store.sessionPath(state.sessionId))).mode & 0o777, 0o600);
  assert.equal((await fs.stat(artifactPath)).mode & 0o777, 0o600);
});
