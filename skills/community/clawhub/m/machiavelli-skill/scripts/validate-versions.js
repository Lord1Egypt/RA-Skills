#!/usr/bin/env node
/**
 * validate-versions.js — Validate version consistency across files
 *
 * Checks:
 *   1. Root SKILL.md version field
 *   2. publish/SKILL.md version field
 *   3. CHANGELOG.md latest entry version
 *   4. README.md version reference + trigger words
 *   5. package.json version (if exists)
 *
 * Usage: node scripts/validate-versions.js
 * Exit code: 0 = consistent, 1 = inconsistent
 */

const fs = require('fs');
const path = require('path');

const ROOT_SKILL  = path.join(__dirname, '..', 'SKILL.md');
const PUBLISH_SKILL = path.join(__dirname, '..', 'publish', 'SKILL.md');
const CHANGELOG = path.join(__dirname, '..', 'CHANGELOG.md');
const README     = path.join(__dirname, '..', 'README.md');
const PACKAGE_JSON = path.join(__dirname, '..', 'package.json');

function readFile(filePath) {
  if (!fs.existsSync(filePath)) return null;
  return fs.readFileSync(filePath, 'utf-8');
}

function extractVersion(content, pattern) {
  const match = content.match(pattern);
  return match ? match[1] : null;
}

function validate() {
  let errors = [];
  let warnings = [];

  // 1. Root SKILL.md
  const rootContent = readFile(ROOT_SKILL);
  const rootVersion = rootContent
    ? extractVersion(rootContent, /^\s*version:\s*(\d+\.\d+\.\d+)/m)
    : null;
  if (!rootVersion) {
    errors.push(`❌ Root SKILL.md: version field not found or malformed`);
  } else {
    console.log(`✅ Root SKILL.md: v${rootVersion}`);
  }

  // 2. publish/SKILL.md
  const pubContent = readFile(PUBLISH_SKILL);
  const publishVersion = pubContent
    ? extractVersion(pubContent, /^\s*version:\s*(\d+\.\d+\.\d+)/m)
    : null;
  if (!publishVersion) {
    errors.push(`❌ publish/SKILL.md: version field not found or malformed`);
  } else {
    console.log(`✅ publish/SKILL.md: v${publishVersion}`);
  }

  // 3. CHANGELOG.md latest entry
  const clContent = readFile(CHANGELOG);
  if (clContent) {
    const match = clContent.match(/^##\s*\[(\d+\.\d+\.\d+)\]/m);
    if (match) {
      const changelogVersion = match[1];
      console.log(`✅ CHANGELOG.md latest: v${changelogVersion}`);

      if (rootVersion && rootVersion !== changelogVersion) {
        errors.push(`❌ Version mismatch: Root SKILL.md (v${rootVersion}) vs CHANGELOG.md (v${changelogVersion})`);
      }
      if (publishVersion && publishVersion !== changelogVersion) {
        warnings.push(`⚠️  publish/SKILL.md (v${publishVersion}) ≠ CHANGELOG.md (v${changelogVersion})`);
      }
    } else {
      errors.push(`❌ CHANGELOG.md: latest version entry not found`);
    }

    // Check CHANGELOG ordering: entries should be in descending version order
    const versionHeaders = [...clContent.matchAll(/^##\s*\[(\d+\.\d+\.\d+)\]/gm)].map(m => m[1]);
    for (let i = 1; i < versionHeaders.length; i++) {
      if (compareVersions(versionHeaders[i - 1], versionHeaders[i]) < 0) {
        warnings.push(`⚠️  CHANGELOG.md ordering: [${versionHeaders[i - 1]}] should come after [${versionHeaders[i]}]`);
      }
    }
  } else {
    errors.push(`❌ CHANGELOG.md not found`);
  }

  // 4. README.md checks
  const readmeContent = readFile(README);
  if (readmeContent) {
    // Check: README should mention the current version
    if (rootVersion && !readmeContent.includes(rootVersion)) {
      warnings.push(`⚠️  README.md: does not mention current version v${rootVersion}`);
    } else if (rootVersion) {
      console.log(`✅ README.md: mentions v${rootVersion}`);
    }

    // Check: README should NOT contain old trigger words
    const oldTriggers = ['`/mach`', '`/mach-a`', '`/mach-w`', '"/mach"', '"/mach-a"', '"/mach-w"'];
    const foundOld = oldTriggers.filter(t => readmeContent.includes(t));
    if (foundOld.length > 0) {
      errors.push(`❌ README.md: contains old trigger words: ${foundOld.join(', ')} (should be /machia, /machia-a, /machia-w)`);
    } else {
      console.log(`✅ README.md: no stale trigger words`);
    }

    // Check: README should contain current trigger words
    const expectedTriggers = ['`/machia`', '`/machia-a`', '`/machia-w`'];
    const missingNew = expectedTriggers.filter(t => !readmeContent.includes(t));
    if (missingNew.length > 0) {
      warnings.push(`⚠️  README.md: missing current trigger words: ${missingNew.join(', ')}`);
    } else {
      console.log(`✅ README.md: current trigger words present`);
    }

    // Check: README file structure should mention sources/original/
    const structureSection = readmeContent.split('## 文件结构 / Project Structure')[1] || readmeContent;
    if (!structureSection.includes('original/')) {
      warnings.push(`⚠️  README.md: file structure may be outdated (missing original/ under sources/)`);
    } else {
      console.log(`✅ README.md: sources/original/ referenced in structure`);
    }
  } else {
    errors.push(`❌ README.md not found`);
  }

  // 5. package.json (optional)
  if (fs.existsSync(PACKAGE_JSON)) {
    try {
      const pkg = JSON.parse(readFile(PACKAGE_JSON));
      if (pkg.version) {
        console.log(`✅ package.json: v${pkg.version}`);
        if (rootVersion && rootVersion !== pkg.version) {
          warnings.push(`⚠️  Root SKILL.md (v${rootVersion}) vs package.json (v${pkg.version})`);
        }
      }
    } catch (e) {
      warnings.push(`⚠️  package.json: invalid JSON (${e.message})`);
    }
  } else {
    console.log(`ℹ️  package.json not found (optional)`);
  }

  // Summary
  console.log('\n' + '='.repeat(50));
  if (errors.length > 0) {
    console.error('\n❌ Validation FAILED:\n');
    errors.forEach(e => console.error(`  ${e}`));
    if (warnings.length > 0) {
      console.warn('\n⚠️  Warnings:\n');
      warnings.forEach(w => console.warn(`  ${w}`));
    }
    process.exit(1);
  } else {
    console.log('\n✅ Validation PASSED');
    if (warnings.length > 0) {
      console.log('\n⚠️  Warnings:\n');
      warnings.forEach(w => console.log(`  ${w}`));
    }
    process.exit(0);
  }
}

function compareVersions(a, b) {
  const pa = a.split('.').map(Number);
  const pb = b.split('.').map(Number);
  for (let i = 0; i < 3; i++) {
    if ((pa[i] || 0) !== (pb[i] || 0)) return (pa[i] || 0) - (pb[i] || 0);
  }
  return 0;
}

validate();
