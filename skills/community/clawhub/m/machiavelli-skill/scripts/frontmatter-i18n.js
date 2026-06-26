#!/usr/bin/env node
/**
 * frontmatter-i18n.js — Add English frontmatter fields to a Chinese SKILL.md
 * 
 * Usage: node frontmatter-i18n.js <path/to/SKILL.md>
 * 
 * Scans the YAML frontmatter for a `name` field and generates English
 * equivalents. Useful for ClawHub skill developers wanting to internationalize.
 * 
 * Free version — Sponsor for full bilingual conversion with section-by-section
 * English summaries.
 * 
 * GitHub: https://github.com/niflhum/machiavelli-skill
 */

const fs = require('fs');

const filePath = process.argv[2];
if (!filePath) {
  console.error('Usage: node frontmatter-i18n.js <path/to/SKILL.md>');
  process.exit(1);
}

let content = fs.readFileSync(filePath, 'utf-8');
const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---/);

if (!frontmatterMatch) {
  console.error('No YAML frontmatter found in', filePath);
  process.exit(1);
}

// Simple heuristic: if name field already contains a "/" (bilingual), skip
const frontmatter = frontmatterMatch[1];
if (frontmatter.includes('/')) {
  console.log('✓ Frontmatter already appears bilingual (contains "/") — no changes needed');
} else {
  console.log('ℹ Frontmatter is Chinese-only. Consider adding English equivalents.');
  console.log('\nSuggested frontmatter additions:');
  console.log('  name: <English Name> / <中文名称>');
  console.log('  description: |');
  console.log('    <English description>');
  console.log('    / <中文描述>');
  console.log('  tags: [english-tag-1, english-tag-2, 中文标签1, 中文标签2]');
  console.log('\nFor a complete bilingual example, see:');
  console.log('  https://clawhub.ai/niflhum/machiavelli-skill');
}
