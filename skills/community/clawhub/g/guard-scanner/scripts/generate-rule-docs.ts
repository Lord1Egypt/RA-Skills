import { fileURLToPath } from 'node:url';
import { dirname } from 'node:path';
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
// @ts-nocheck
import fs from 'node:fs';
import path from 'node:path';
import { PATTERNS }  from '../src/patterns';

const docsDir = path.join(__dirname, '../docs/rules');
if (!fs.existsSync(docsDir)) {
  fs.mkdirSync(docsDir, { recursive: true });
}

// Generate markdown file for each category
const categories = [...new Set(PATTERNS.map(p => p.cat))];

for (const cat of categories) {
  const catPatterns = PATTERNS.filter(p => p.cat === cat);
  let md = `# Threat Category: ${cat}\n\n`;
  md += `This document provides explainability for all rules in the \`${cat}\` category.\n\n`;

  for (const pattern of catPatterns) {
    md += `## Rule: \`${pattern.id}\`\n`;
    md += `- **Severity**: ${pattern.severity}\n`;
    md += `- **Description**: ${pattern.desc}\n`;
    md += `- **Rationale**: Explains why this pattern is considered dangerous.\n`;
    md += `- **Exploit Precondition**: What an attacker needs to trigger this.\n`;
    md += `- **Likely False Positives**: Scenarios where this might trigger safely.\n`;
    md += `- **Remediation Hint**: How to fix or mitigate the finding.\n\n`;
  }

  fs.writeFileSync(path.join(docsDir, `${cat}.md`), md);
}

console.log(`Generated explanation stubs for ${categories.length} categories.`);
