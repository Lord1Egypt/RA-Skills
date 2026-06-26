import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { ASSET_ENTRIES } from '../lib/constants.js';
import { copyDirectoryFiltered } from '../lib/copy.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const packageRoot = path.resolve(__dirname, '..');
const repoRoot = path.resolve(packageRoot, '../..');
const assetsDir = path.join(packageRoot, 'assets');

const SOURCE_FILES = [
  { from: path.join(repoRoot, 'SKILL.md'), to: path.join(assetsDir, 'SKILL.md') },
  { from: path.join(repoRoot, 'skill.json'), to: path.join(assetsDir, 'skill.json') },
];

const SOURCE_DIRS = ['docs', 'reference', 'examples', 'scripts'].map((name) => ({
  from: path.join(repoRoot, name),
  to: path.join(assetsDir, name),
}));

async function syncManifestVersion() {
  const manifestPath = path.join(assetsDir, 'skill.json');
  const pkg = JSON.parse(await fs.readFile(path.join(packageRoot, 'package.json'), 'utf8'));
  const manifest = JSON.parse(await fs.readFile(manifestPath, 'utf8'));
  manifest.version = pkg.version;
  await fs.writeFile(manifestPath, `${JSON.stringify(manifest, null, 2)}\n`, 'utf8');
}

async function ensureParentDir(filePath) {
  await fs.mkdir(path.dirname(filePath), { recursive: true });
}

async function copyFile(from, to) {
  await ensureParentDir(to);
  await fs.copyFile(from, to);
  console.log(`  copied ${path.relative(repoRoot, from)}`);
}

async function copyDir(from, to) {
  await fs.rm(to, { recursive: true, force: true });
  await copyDirectoryFiltered(from, to);
  console.log(`  copied ${path.relative(repoRoot, from)}/`);
}

async function main() {
  console.log('Syncing skill assets into packages/insentek-skill-cli/assets ...\n');
  await fs.mkdir(assetsDir, { recursive: true });

  for (const item of SOURCE_FILES) {
    await copyFile(item.from, item.to);
  }

  for (const item of SOURCE_DIRS) {
    await copyDir(item.from, item.to);
  }

  await syncManifestVersion();

  console.log('\nAsset sync complete:');
  for (const entry of ASSET_ENTRIES) {
    console.log(`  • assets/${entry}`);
  }
}

main().catch((error) => {
  console.error(`Asset sync failed: ${error.message}`);
  process.exit(1);
});
