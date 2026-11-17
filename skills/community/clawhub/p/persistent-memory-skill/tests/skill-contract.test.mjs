import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';

const read = (file) => readFile(new URL(`../${file}`, import.meta.url), 'utf8');

test('documents an explicit upgrade path for existing memory', async () => {
  const [en, zh] = await Promise.all([read('SKILL.md'), read('SKILL_zh.md')]);

  assert.match(en, /## Upgrade Existing Memory/);
  assert.match(zh, /## 升级已有记忆/);
  assert.match(en, /memory upgrade/);
  assert.match(zh, /升级记忆/);
});

test('limits lifecycle paths and protects core memory', async () => {
  const [en, zh] = await Promise.all([read('SKILL.md'), read('SKILL_zh.md')]);

  assert.match(en, /relative path/i);
  assert.match(zh, /相对路径/);

  for (const text of [en, zh]) {
    assert.match(text, /_core/);
    assert.match(text, /_archive\/_index\.md/);
    assert.match(text, /\.{2}/);
  }
});

test('requires explicit confirmation before lifecycle migration or mutation', async () => {
  const [en, zh] = await Promise.all([read('SKILL.md'), read('SKILL_zh.md')]);

  assert.match(en, /explicit user confirmation/i);
  assert.match(zh, /用户明确确认/);
});

test('states the cross-agent sharing conditions without claiming full-context loading', async () => {
  const [en, zh] = await Promise.all([read('README.md'), read('README_zh.md')]);

  assert.match(en, /same local filesystem/i);
  assert.match(en, /compatible agent/i);
  assert.match(en, /baseline context/i);
  assert.doesNotMatch(en, /Loads your full context/);
  assert.match(zh, /同一.*本地文件系统/);
  assert.match(zh, /基础上下文/);
});

test('keeps raw repositories and media outside managed memory', async () => {
  const [en, zh] = await Promise.all([read('README.md'), read('README_zh.md')]);

  assert.match(en, /raw repositories, downloads, media files, and datasets/i);
  assert.match(zh, /原始仓库、下载文件、媒体文件和数据集/);
});

test('documents optional summary-first loading with a safe legacy fallback', async () => {
  const [en, zh, readmeEn, readmeZh] = await Promise.all([
    read('SKILL.md'),
    read('SKILL_zh.md'),
    read('README.md'),
    read('README_zh.md'),
  ]);

  assert.match(en, /Summary-first on-demand loading/i);
  assert.match(en, /## Summary/);
  assert.match(en, /summary is insufficient/i);
  assert.match(en, /no valid summary.*read the full file/is);
  assert.match(zh, /摘要优先的按需加载/);
  assert.match(zh, /## 摘要/);
  assert.match(zh, /摘要不足/);
  assert.match(zh, /没有有效摘要.*读取全文/is);
  assert.match(readmeEn, /optional.*Summary-first/i);
  assert.match(readmeZh, /可选.*摘要优先/);
});

test('requires reviewed summary maintenance without automatic migration', async () => {
  const [en, zh] = await Promise.all([read('SKILL.md'), read('SKILL_zh.md')]);

  assert.match(en, /same preview.*explicit user confirmation/is);
  assert.match(en, /do not automatically create.*Summary/is);
  assert.match(en, /Do not bulk-migrate/i);
  assert.match(zh, /同一次预览.*用户明确确认/is);
  assert.match(zh, /不得自动创建.*摘要/is);
  assert.match(zh, /不得批量迁移/);
});

test('preserves an index entry before archiving so recovery never guesses', async () => {
  const [en, zh] = await Promise.all([read('SKILL.md'), read('SKILL_zh.md')]);

  assert.match(en, /exact active index line/i);
  assert.match(zh, /原始活跃索引行/);
  assert.match(en, /must not guess/i);
  assert.match(zh, /不得猜测/);
});

test('refuses lifecycle destination collisions before moving files', async () => {
  const [en, zh, readmeEn, readmeZh] = await Promise.all([
    read('SKILL.md'),
    read('SKILL_zh.md'),
    read('README.md'),
    read('README_zh.md'),
  ]);

  assert.match(en, /destination does not already exist/i);
  assert.match(zh, /目标路径不存在/);
  assert.match(en, /stop without moving files/i);
  assert.match(zh, /不移动任何文件/);
  assert.match(readmeEn, /path collision/i);
  assert.match(readmeZh, /路径冲突/);
});
