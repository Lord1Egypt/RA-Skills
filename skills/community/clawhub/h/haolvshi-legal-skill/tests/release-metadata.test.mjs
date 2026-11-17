import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import test from 'node:test';

const skillDir = path.resolve(new URL('..', import.meta.url).pathname);
const repoDir = path.resolve(skillDir, '..');

test('技能包发布元数据版本保持一致', async () => {
  const packageJson = JSON.parse(await fs.readFile(path.join(skillDir, 'package.json'), 'utf8'));
  const skillHubMeta = JSON.parse(await fs.readFile(path.join(skillDir, '_skillhub_meta.json'), 'utf8'));
  const skillMarkdown = await fs.readFile(path.join(skillDir, 'SKILL.md'), 'utf8');
  const escapedVersion = packageJson.version.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

  assert.match(packageJson.version, /^\d+\.\d+$/);
  assert.equal(skillHubMeta.version, packageJson.version);
  assert.match(skillMarkdown, new RegExp(`version: "${escapedVersion}"`));

  // 仓库根 README 的版本一致性只有在仓库里才校验得了。测试文件会随技能包
  // 一起分发，用户把 zip 解压到任意目录后同样会跑到这里，找不到根 README
  // 属于正常情况，不应判为失败。
  const readIfPresent = async filePath => fs.readFile(filePath, 'utf8').catch(() => null);
  const rootReadme = await readIfPresent(path.join(repoDir, 'README.md'))
    ?? await readIfPresent(path.resolve(repoDir, '..', 'README.md'));
  if (rootReadme !== null) {
    assert.match(rootReadme, new RegExp('当前技能包版本为 `' + escapedVersion + '`'));
  }
  assert.match(skillMarkdown, /养老保险待遇/);
  assert.match(skillMarkdown, /社会保险待遇/);
});
