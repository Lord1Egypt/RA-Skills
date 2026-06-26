import { fileURLToPath } from 'node:url';
import { dirname } from 'node:path';
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
// @ts-nocheck
import fs from 'node:fs';
import path from 'node:path';

const specPath = path.join(__dirname, '..', 'docs', 'spec', 'capabilities.json');
const readmePath = path.join(__dirname, '..', 'README.md');
const packagePath = path.join(__dirname, '..', 'package.json');
const skillPath = path.join(__dirname, '..', 'SKILL.md');
const pluginPath = path.join(__dirname, '..', 'openclaw.plugin.json');
const changelogPath = path.join(__dirname, '..', 'CHANGELOG.md');

let hasErrors = false;

function error(msg) {
  console.error(`❌ ERROR: ${msg}`);
  hasErrors = true;
}

function check() {
  console.log('🛡️  Validating Guard-Scanner SSoT (Single Source of Truth)...\n');
  
  if (!fs.existsSync(specPath)) {
    error('docs/spec/capabilities.json not found!');
    process.exit(1);
  }

  const spec = JSON.parse(fs.readFileSync(specPath, 'utf8'));
  const readme = fs.existsSync(readmePath) ? fs.readFileSync(readmePath, 'utf8') : '';
  const pkg = JSON.parse(fs.readFileSync(packagePath, 'utf8'));
  const skill = fs.existsSync(skillPath) ? fs.readFileSync(skillPath, 'utf8') : '';
  const plugin = fs.existsSync(pluginPath) ? JSON.parse(fs.readFileSync(pluginPath, 'utf8')) : null;
  const changelog = fs.existsSync(changelogPath) ? fs.readFileSync(changelogPath, 'utf8') : '';

  // 1. Dependency Validation
  const actualDeps = Object.keys(pkg.dependencies || {});
  if (actualDeps.length > 0) {
    if (readme.includes('zero dependencies')) {
      error('README claims "zero dependencies" but package.json has: ' + actualDeps.join(', '));
    }
    if (skill.includes('zero dependencies')) {
      error('SKILL.md claims "zero dependencies" but package.json has dependencies.');
    }
  }

  // 2. Marketing Claim Validation (Humble & Accurate)
  const falseClaims = [/the first open-source/i, /purpose-built/i];
  falseClaims.forEach(regex => {
    if (regex.test(readme)) error(`README contains unprovable marketing claim matching: ${regex}`);
    if (regex.test(skill)) error(`SKILL.md contains unprovable marketing claim matching: ${regex}`);
  });

  // 3. Static Pattern Count Validation
  const patternRegex = new RegExp(`${spec.static_pattern_count}\\s*static patterns`, 'i');
  if (readme && !patternRegex.test(readme)) error(`README does not reflect static pattern count: ${spec.static_pattern_count}`);
  if (skill && !patternRegex.test(skill)) error(`SKILL.md does not reflect static pattern count: ${spec.static_pattern_count}`);
  
  // 4. Threat Category Validation
  const catRegex = new RegExp(`${spec.threat_category_count}\\s*threat categories`, 'i');
  if (readme && !catRegex.test(readme)) error(`README does not reflect category count: ${spec.threat_category_count}`);
  if (skill && !catRegex.test(skill)) error(`SKILL.md does not reflect category count: ${spec.threat_category_count}`);

  if (hasErrors) {
    console.log('\n💥 SSoT Validation FAILED. Please sync documentation with docs/spec/capabilities.json');
    process.exit(1);
  } else {
    console.log('✅ SSoT Validation PASSED. Documentation is synchronized with capabilities.json.');
  }
}

check();
