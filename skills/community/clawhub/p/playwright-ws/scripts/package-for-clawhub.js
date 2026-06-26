#!/usr/bin/env node
/**
 * Package skill for ClawHub publication
 * Creates clean .skill file without CI/dev files
 */

const fs = require('fs');
const path = require('path');

const skillPath = process.argv[2] || '.';
const outputFile = process.argv[3] || 'playwright.skill';

const fullPath = path.resolve(skillPath);
const tempDir = fs.mkdtempSync(path.join(require('os').tmpdir(), 'skill-'));
const skillName = path.basename(fullPath);

console.log(`Packaging: ${skillName} -> ${outputFile}`);

// Files to include (whitelist)
const include = [
  'SKILL.md',
  'README.md',
  'package.json',
  'package-lock.json',
  'CHANGELOG.md',
  'LICENSE',
  'CONTRIBUTING.md',
  'INSTALL.md',
  'test.sh',
  '_meta.json'
];

// Directories to include recursively
const includeDirs = [
  'scripts',
  'references',
  'examples'
];

// Create skill directory
const destPath = path.join(tempDir, skillName);
fs.mkdirSync(destPath, { recursive: true });

// Copy included files
for (const file of include) {
  const src = path.join(fullPath, file);
  const dst = path.join(destPath, file);
  if (fs.existsSync(src)) {
    fs.copyFileSync(src, dst);
    console.log(`  + ${file}`);
  }
}

// Copy included directories
for (const dir of includeDirs) {
  const srcDir = path.join(fullPath, dir);
  const dstDir = path.join(destPath, dir);
  if (fs.existsSync(srcDir)) {
    fs.mkdirSync(dstDir, { recursive: true });
    copyRecursive(srcDir, dstDir);
    console.log(`  + ${dir}/`);
  }
}

function copyRecursive(src, dest) {
  const entries = fs.readdirSync(src, { withFileTypes: true });
  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    if (entry.isDirectory()) {
      fs.mkdirSync(destPath, { recursive: true });
      copyRecursive(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

// Create zip — use array args to avoid shell injection
const { spawnSync } = require('child_process');
process.chdir(tempDir);
try {
  const result = spawnSync('zip', ['-r', path.resolve(outputFile), skillName], { stdio: 'inherit' });
  if (result.status !== 0) throw new Error(`zip exited with code ${result.status}`);
  console.log(`\n✅ Created: ${outputFile}`);
} catch (err) {
  console.error('❌ Failed:', err.message);
  process.exit(1);
} finally {
  fs.rmSync(tempDir, { recursive: true, force: true });
}