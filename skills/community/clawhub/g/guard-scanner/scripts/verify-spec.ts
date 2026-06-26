import { fileURLToPath } from 'node:url';
import { dirname } from 'node:path';
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
// @ts-nocheck
import fs from 'node:fs';
import path from 'node:path';

const specPath = path.join(__dirname, '../docs/spec/capabilities.json');
const spec = JSON.parse(fs.readFileSync(specPath, 'utf8'));

let errors = [];

function checkFile(filePath, regex, expectedValue, errorMessage) {
  const content = fs.readFileSync(path.join(__dirname, '..', filePath), 'utf8');
  if (!regex.test(content)) {
    errors.push(`${filePath}: ${errorMessage}. Expected ${expectedValue}`);
  }
}

// Check README.md
checkFile('README.md', new RegExp(`${spec.threat_category_count} threat categories`), spec.threat_category_count, 'Threat categories mismatch');
checkFile('README.md', new RegExp(`${spec.static_pattern_count} static patterns`), spec.static_pattern_count, 'Static patterns mismatch');
checkFile('README.md', new RegExp(`${spec.runtime_check_count} runtime checks`), spec.runtime_check_count, 'Runtime checks mismatch');

// Check README_ja.md
checkFile('README_ja.md', new RegExp(`${spec.threat_category_count}の脅威カテゴリ`), spec.threat_category_count, 'Threat categories mismatch (JA)');
checkFile('README_ja.md', new RegExp(`${spec.static_pattern_count}の静的パターン`), spec.static_pattern_count, 'Static patterns mismatch (JA)');

// Check SKILL.md
checkFile('SKILL.md', new RegExp(`${spec.static_pattern_count} static patterns`), spec.static_pattern_count, 'Static patterns mismatch (SKILL)');
checkFile('SKILL.md', new RegExp(`${spec.threat_category_count} categories`), spec.threat_category_count, 'Categories mismatch (SKILL)');

// Ensure no "zero dependencies" false claims
const readmeContent = fs.readFileSync(path.join(__dirname, '../README.md'), 'utf8');
if (readmeContent.toLowerCase().includes('zero dependencies')) {
  errors.push('README.md contains false "zero dependencies" claim');
}

if (errors.length > 0) {
  console.error('❌ Spec verification failed:');
  errors.forEach(e => console.error('  - ' + e));
  process.exit(1);
} else {
  console.log('✅ Spec verification passed: All claims match capabilities.json');
}
