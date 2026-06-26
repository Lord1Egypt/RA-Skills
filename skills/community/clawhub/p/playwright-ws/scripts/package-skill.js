#!/usr/bin/env node
/**
 * Package the skill into a .skill file (zip with .skill extension)
 * Usage: node scripts/package-skill.js [skill-path] [output-dir]
 */

const fs = require('fs');
const path = require('path');

const skillPath = path.resolve(process.argv[2] || '.');
const outputDir = path.resolve(process.argv[3] || '.');
const skillName = path.basename(skillPath);
const outputFile = path.join(outputDir, `${skillName}.skill`);

console.log(`Packaging skill: ${skillName}`);
console.log(`Output: ${outputFile}`);

// Validate
const skillMd = path.join(skillPath, 'SKILL.md');
if (!fs.existsSync(skillMd)) {
  console.error('❌ SKILL.md not found');
  process.exit(1);
}

const content = fs.readFileSync(skillMd, 'utf8');
if (!content.startsWith('---')) {
  console.error('❌ SKILL.md missing YAML frontmatter');
  process.exit(1);
}

// Create zip
const tempDir = fs.mkdtempSync(path.join(require('os').tmpdir(), 'skill-'));

// Copy files (excluding node_modules, .git, etc.)
const exclude = ['node_modules', '.git', 'coverage', '.DS_Store', '*.log', '*.skill'];

function shouldExclude(file) {
  return exclude.some(pattern => {
    if (pattern.includes('*')) {
      const regex = new RegExp(pattern.replace('*', '.*'));
      return regex.test(file);
    }
    return file === pattern || file.startsWith(pattern + '/');
  });
}

function copyDir(src, dest) {
  fs.mkdirSync(dest, { recursive: true });
  const entries = fs.readdirSync(src, { withFileTypes: true });
  
  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    const relPath = path.relative(skillPath, srcPath);
    
    if (shouldExclude(relPath)) continue;
    
    if (entry.isDirectory()) {
      copyDir(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

copyDir(skillPath, path.join(tempDir, skillName));

// Create zip — use array args to avoid shell injection
const { spawnSync } = require('child_process');
process.chdir(tempDir);
try {
  const result = spawnSync('zip', ['-r', outputFile, skillName], { stdio: 'inherit' });
  if (result.status !== 0) throw new Error(`zip exited with code ${result.status}`);
  console.log(`\n✅ Skill packaged: ${outputFile}`);
} catch (err) {
  console.error('❌ Failed to create zip:', err.message);
  process.exit(1);
} finally {
  // Cleanup
  fs.rmSync(tempDir, { recursive: true, force: true });
}