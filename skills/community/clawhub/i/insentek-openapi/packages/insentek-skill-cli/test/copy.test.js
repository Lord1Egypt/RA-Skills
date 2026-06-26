import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { describe, it } from 'node:test';
import { replaceDirectoryAtomic } from '../lib/copy.js';
import { pathExists, removeDir } from '../lib/utils.js';

async function writeFixture(root) {
  for (const dir of ['docs', 'reference', 'examples', 'scripts']) {
    await fs.mkdir(path.join(root, dir), { recursive: true });
  }
  await fs.writeFile(path.join(root, 'skill.json'), '{"id":"insentek-openapi","version":"2.0.0"}\n');
  await fs.writeFile(path.join(root, 'SKILL.md'), 'name: insentek-openapi\n');
  await fs.writeFile(path.join(root, 'docs', 'guide.md'), '# guide\n');
  await fs.writeFile(path.join(root, 'reference', '.keep'), '');
  await fs.writeFile(path.join(root, 'examples', '.keep'), '');
  await fs.writeFile(path.join(root, 'scripts', 'insentek_cli.py'), 'print("ok")\n');
}

async function readVersion(installDir) {
  const content = await fs.readFile(path.join(installDir, 'skill.json'), 'utf8');
  return JSON.parse(content).version;
}

describe('replaceDirectoryAtomic', () => {
  it('replaces existing install without leaving backup artifacts', async () => {
    const root = await fs.mkdtemp(path.join(os.tmpdir(), 'insentek-copy-'));
    const sourceDir = path.join(root, 'source');
    const installDir = path.join(root, 'install', 'insentek-openapi');

    try {
      await writeFixture(sourceDir);
      await fs.mkdir(path.dirname(installDir), { recursive: true });
      await fs.mkdir(installDir, { recursive: true });
      await fs.writeFile(path.join(installDir, 'skill.json'), '{"id":"insentek-openapi","version":"1.0.0"}\n');
      await fs.writeFile(path.join(installDir, 'SKILL.md'), 'name: old\n');

      await replaceDirectoryAtomic(sourceDir, installDir);

      assert.equal(await readVersion(installDir), '2.0.0');
      const parentEntries = await fs.readdir(path.dirname(installDir));
      assert.equal(parentEntries.some((name) => name.includes('.backup-')), false);
      assert.equal(parentEntries.some((name) => name.includes('.staging-')), false);
    } finally {
      await removeDir(root);
    }
  });

  it('keeps original install when staging copy fails', async () => {
    const root = await fs.mkdtemp(path.join(os.tmpdir(), 'insentek-copy-'));
    const sourceDir = path.join(root, 'source');
    const installDir = path.join(root, 'install', 'insentek-openapi');

    try {
      await writeFixture(sourceDir);
      await fs.rm(path.join(sourceDir, 'SKILL.md'));

      await fs.mkdir(installDir, { recursive: true });
      await fs.writeFile(path.join(installDir, 'skill.json'), '{"id":"insentek-openapi","version":"1.0.0"}\n');
      await fs.writeFile(path.join(installDir, 'SKILL.md'), 'name: old\n');

      await assert.rejects(
        () => replaceDirectoryAtomic(sourceDir, installDir),
        /Missing bundled asset: SKILL.md/,
      );

      assert.equal(await pathExists(installDir), true);
      assert.equal(await readVersion(installDir), '1.0.0');
      const parentEntries = await fs.readdir(path.dirname(installDir));
      assert.equal(parentEntries.some((name) => name.includes('.backup-')), false);
      assert.equal(parentEntries.some((name) => name.includes('.staging-')), false);
    } finally {
      await removeDir(root);
    }
  });
});
