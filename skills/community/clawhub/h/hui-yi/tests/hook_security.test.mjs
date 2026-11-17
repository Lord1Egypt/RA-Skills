import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import test from 'node:test';
import { SafeFiles, relativeParts } from '../templates/hook/safe-fs.ts';

process.env.HUI_YI_HOOK_DEBUG = '1';
const hookUrl = process.env.HUI_YI_TEST_HOOK ? pathToFileURL(process.env.HUI_YI_TEST_HOOK).href : new URL('../templates/hook/handler.ts', import.meta.url).href;
const { default: handler } = await import(hookUrl);

function fixture(t) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'hui-yi-security-'));
  const cold = path.join(root, 'memory', 'cold');
  const hook = path.join(root, 'hooks', 'hui-yi-signal-hook');
  const outside = path.join(root, 'outside');
  for (const p of [cold, hook, outside]) fs.mkdirSync(p, { recursive: true });
  t.after(() => {
    assert.equal(path.dirname(root), path.resolve(os.tmpdir()));
    assert.match(path.basename(root), /^hui-yi-security-/);
    fs.rmSync(root, { recursive: true, force: true });
  });
  const text = '# Private Fixture\n\n## Session signals\n- current_session_hits: 0\n- recent_session_hits: 0\n- cross_session_repeat_count: 0\n- consecutive_session_count: 0\n- last_activated: -\n';
  fs.writeFileSync(path.join(cold, 'note.md'), text);
  const payload = { _meta: { version: 5 }, notes: [{ title: 'secretfixture', summary: 'secretfixture', path: 'memory/cold/note.md', tags: ['secretfixture'] }] };
  const saveTags = () => fs.writeFileSync(path.join(cold, 'tags.json'), JSON.stringify(payload));
  saveTags();
  const event = { type: 'message', action: 'preprocessed', context: { workspaceDir: root, bodyForAgent: 'secretfixture do you remember secretfixture', channelId: 'user:private-user-id', metadata: { selectedSkill: 'hui-yi', chat_type: 'direct', senderId: 'private-user-id', threadId: 'private-thread-id' } } };
  return { root, cold, hook, outside, text, payload, saveTags, event };
}

test('normal nested Unicode note is updated once and logs contain no private text', async t => {
  const f = fixture(t);
  fs.mkdirSync(path.join(f.cold, '分类'));
  fs.renameSync(path.join(f.cold, 'note.md'), path.join(f.cold, '分类', '旧经验.md'));
  f.payload.notes[0].path = 'memory/cold/分类/旧经验.md'; f.saveTags();
  await handler(f.event);
  const first = fs.readFileSync(path.join(f.cold, '分类', '旧经验.md'), 'utf8');
  assert.match(first, /current_session_hits: 1/);
  await handler(f.event);
  assert.equal(fs.readFileSync(path.join(f.cold, '分类', '旧经验.md'), 'utf8'), first);
  const tags = JSON.parse(fs.readFileSync(path.join(f.cold, 'tags.json'), 'utf8'));
  assert.match(tags.notes[0].last_session_key, /^sha256:[0-9a-f]{16}$/);
  const log = fs.readFileSync(path.join(f.hook, 'hook.log'), 'utf8');
  for (const secret of ['secretfixture', 'private-user-id', 'private-thread-id', '旧经验', 'bodyPreview', 'overlap_terms']) assert.ok(!log.includes(secret), secret);
});

test('ordinary recall phrases do not mutate memory without host skill selection', async t => {
  const f = fixture(t);
  delete f.event.context.metadata.selectedSkill;
  const tags = fs.readFileSync(path.join(f.cold, 'tags.json'), 'utf8');
  await handler(f.event);
  assert.equal(fs.readFileSync(path.join(f.cold, 'note.md'), 'utf8'), f.text);
  assert.equal(fs.readFileSync(path.join(f.cold, 'tags.json'), 'utf8'), tags);
});

for (const command of ['/hui-yi', '/hui_yi']) test(`plain native event accepts only explicit ${command} query`, async t => {
  const f = fixture(t);
  // Matches the installed mapper's plain-body projection, with no skill fields.
  const event = { type: 'message', action: 'preprocessed', context: {
    body: `${command} secretfixture`, bodyForAgent: 'unrelated processed content',
    from: 'telegram:private-user-id', channelId: 'telegram',
    conversationId: 'private-conversation', isGroup: false,
    cfg: { agents: { defaults: { workspace: f.root } } }
  } };
  await handler(event);
  const note = fs.readFileSync(path.join(f.cold, 'note.md'), 'utf8');
  assert.match(note, /current_session_hits: 1/);
  await handler(event);
  assert.equal(fs.readFileSync(path.join(f.cold, 'note.md'), 'utf8'), note);
  const log = fs.readFileSync(path.join(f.hook, 'hook.log'), 'utf8');
  assert.ok(log.includes('explicit_command'));
  for (const secret of ['secretfixture', 'private-user-id', 'private-conversation', 'unrelated']) assert.ok(!log.includes(secret), secret);
});

test('embedded quoted empty or processed commands cannot authorize activation', async t => {
  const f = fixture(t);
  delete f.event.context.metadata.selectedSkill;
  const tags = fs.readFileSync(path.join(f.cold, 'tags.json'), 'utf8');
  for (const body of [undefined, '', '/hui-yi', '/hui-yi   ', '/hui-yiextra secretfixture',
      ' /hui-yi secretfixture', '> /hui-yi secretfixture', 'example\n/hui-yi secretfixture',
      '/hui-yi\nsecretfixture', 'ordinary secretfixture', '[envelope] /hui-yi secretfixture']) {
    f.event.context.body = body;
    f.event.context.bodyForAgent = '/hui-yi secretfixture';
    await handler(f.event);
    assert.equal(fs.readFileSync(path.join(f.cold, 'note.md'), 'utf8'), f.text);
    assert.equal(fs.readFileSync(path.join(f.cold, 'tags.json'), 'utf8'), tags);
  }
});

test('preflight and apply select the same exact path despite title aliases', async t => {
  const f = fixture(t);
  fs.writeFileSync(path.join(f.cold, 'a.md'), f.text);
  fs.writeFileSync(path.join(f.cold, 'b.md'), f.text);
  f.payload.notes = [
    { title: 'alpha', path: 'memory/cold/a.md', summary: 'alpha', tags: ['alpha'] },
    { title: 'memory/cold/b.md', path: '../outside.md' },
    { title: 'beta', path: 'memory/cold/b.md', summary: 'beta', tags: ['beta'] }
  ];
  f.saveTags(); f.event.context.bodyForAgent = 'alpha beta';
  await handler(f.event);
  const payload = JSON.parse(fs.readFileSync(path.join(f.cold, 'tags.json'), 'utf8'));
  for (const index of [0, 2]) {
    assert.equal(payload.notes[index].session_signals.current_session_hits, 1);
    assert.match(fs.readFileSync(path.join(f.cold, index === 0 ? 'a.md' : 'b.md'), 'utf8'), /current_session_hits: 1/);
  }
  assert.equal(payload.notes[1].session_signals, undefined);
});

test('directory junction cannot redirect hook note writes', async t => {
  const f = fixture(t);
  const external = path.join(f.outside, 'note.md'); fs.writeFileSync(external, f.text);
  fs.symlinkSync(f.outside, path.join(f.cold, 'linked'), process.platform === 'win32' ? 'junction' : 'dir');
  f.payload.notes[0].path = 'memory/cold/linked/note.md'; f.saveTags();
  const tags = fs.readFileSync(path.join(f.cold, 'tags.json'), 'utf8');
  await handler(f.event);
  assert.equal(fs.readFileSync(external, 'utf8'), f.text);
  assert.equal(fs.readFileSync(path.join(f.cold, 'tags.json'), 'utf8'), tags);
});

for (const targetName of ['note.md', 'tags.json']) test(`reject linked ${targetName} without external writes`, async t => {
  const f = fixture(t);
  const local = path.join(f.cold, targetName), external = path.join(f.outside, targetName);
  const original = fs.readFileSync(local, 'utf8'); fs.renameSync(local, external);
  fs.symlinkSync(external, local, 'file');
  await handler(f.event);
  assert.equal(fs.readFileSync(external, 'utf8'), original);
  if (targetName === 'tags.json') assert.equal(fs.readFileSync(path.join(f.cold, 'note.md'), 'utf8'), f.text);
});

test('linked hook log is never read truncated or appended', async t => {
  const f = fixture(t), external = path.join(f.outside, 'private.log');
  const sentinel = 'private-external'.repeat(30000); fs.writeFileSync(external, sentinel);
  fs.symlinkSync(external, path.join(f.hook, 'hook.log'), 'file');
  await handler(f.event);
  assert.equal(fs.readFileSync(external, 'utf8'), sentinel);
});

test('dangling symlinks remain links and do not create outside files', t => {
  const f = fixture(t), external = path.join(f.outside, 'missing.md');
  fs.symlinkSync(external, path.join(f.cold, 'missing.md'), 'file');
  assert.throws(() => new SafeFiles(f.cold).write('missing.md', 'bad'));
  assert.equal(fs.existsSync(external), false);
});

test('linked cold root and linked ancestor are rejected', t => {
  const f = fixture(t);
  fs.symlinkSync(f.cold, path.join(f.root, 'alias'), process.platform === 'win32' ? 'junction' : 'dir');
  assert.throws(() => new SafeFiles(path.join(f.root, 'alias')));
  fs.mkdirSync(path.join(f.cold, 'child'));
  assert.throws(() => new SafeFiles(path.join(f.root, 'alias', 'child')));
});

test('hardlink targets cannot alias protected files', t => {
  const f = fixture(t), external = path.join(f.outside, 'hard.md');
  fs.writeFileSync(external, 'sentinel'); fs.linkSync(external, path.join(f.cold, 'hard.md'));
  const files = new SafeFiles(f.cold);
  assert.throws(() => files.read('hard.md'));
  assert.throws(() => files.write('hard.md', 'bad'));
  assert.equal(fs.readFileSync(external, 'utf8'), 'sentinel');
});

test('path grammar rejects traversal ADS device and drive variants', () => {
  for (const raw of ['../note.md', 'x/../note.md', 'x/./note.md', '/a.md', 'C:note.md', 'C:/note.md', '//server/share.md', 'a.md:stream', 'NUL.md', 'COM1.md', 'x.', 'x ', 'a//b.md', ' x.md']) assert.throws(() => relativeParts(raw), raw);
  assert.deepEqual(relativeParts('..note.md'), ['..note.md']);
  assert.deepEqual(relativeParts('分类\\旧经验.md'), ['分类', '旧经验.md']);
});

test('a leaf swapped during file I/O is rejected without external writes', t => {
  const f = fixture(t), external = path.join(f.outside, 'sentinel.md');
  fs.writeFileSync(external, 'sentinel');
  const originalFsync = fs.fsyncSync;
  fs.fsyncSync = fd => { originalFsync(fd); fs.unlinkSync(path.join(f.cold, 'note.md')); fs.symlinkSync(external, path.join(f.cold, 'note.md'), 'file'); };
  try { assert.throws(() => new SafeFiles(f.cold).write('note.md', 'bad')); }
  finally { fs.fsyncSync = originalFsync; }
  assert.equal(fs.readFileSync(external, 'utf8'), 'sentinel');
});

test('an ancestor swapped during file I/O is rejected without external writes', t => {
  const f = fixture(t); fs.mkdirSync(path.join(f.cold, 'nested')); fs.writeFileSync(path.join(f.cold, 'nested', 'note.md'), 'original');
  fs.writeFileSync(path.join(f.outside, 'note.md'), 'sentinel');
  const originalFsync = fs.fsyncSync;
  fs.fsyncSync = fd => { originalFsync(fd); fs.renameSync(path.join(f.cold, 'nested'), path.join(f.cold, 'moved')); fs.symlinkSync(f.outside, path.join(f.cold, 'nested'), process.platform === 'win32' ? 'junction' : 'dir'); };
  try { assert.throws(() => new SafeFiles(f.cold).write('nested/note.md', 'bad')); }
  finally { fs.fsyncSync = originalFsync; }
  assert.equal(fs.readFileSync(path.join(f.outside, 'note.md'), 'utf8'), 'sentinel');
});

test('Windows descriptor updates retain identity and recover an ordinary write failure', { skip: process.platform !== 'win32' }, t => {
  const f = fixture(t), target = path.join(f.cold, 'note.md');
  const identity = fs.statSync(target).ino;
  const files = new SafeFiles(f.cold);
  files.write('note.md', 'initial');
  assert.equal(fs.statSync(target).ino, identity);
  const originalWrite = fs.writeSync;
  let count = 0;
  fs.writeSync = (fd, bytes, offset, length, position) => {
    count++;
    if (count === 1) return originalWrite(fd, bytes, offset, 1, position);
    if (count === 2) throw new Error('simulated write failure');
    return originalWrite(fd, bytes, offset, length, position);
  };
  try { assert.throws(() => files.write('note.md', 'replacement content')); }
  finally { fs.writeSync = originalWrite; }
  assert.equal(fs.readFileSync(target, 'utf8'), 'initial');
  assert.equal(fs.statSync(target).ino, identity);
});
