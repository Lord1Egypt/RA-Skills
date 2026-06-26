#!/usr/bin/env node
/**
 * build-publish.js — Generate publish/SKILL.md from root SKILL.md
 *
 * Reads the full (root) SKILL.md and produces a compressed version
 * suitable for ClawHub publishing. Compression rules:
 *
 * 1. ❌ Remove all "原文扩展示例 (Extended Original Text)" blocks & [NEEDS_HUMAN_INPUT] blocks
 * 2. ✂️  Compress long paragraph blocks (>3 lines after "Meaning:") to 2-3 core lines
 * 3. ✂️  Compress historical cases (Case 1-11) to 2-3 sentences each
 * 4. ✂️  Compress Part 4 dialogue guide items to 1 sentence each
 * 5. ✂️  Compress framework examples to title + 1 sentence description
 * 6. ✂️  Compress reverse examples to failure reason + core lesson
 * 7. ✂️  Compress Part 6 boundary items to 1 sentence each
 * 8. 🌐  Keep ALL bilingual (EN/CN) labels and section headers
 */

const fs = require('fs');
const path = require('path');

const ROOT_SKILL = path.join(__dirname, '..', 'SKILL.md');
const PUBLISH_SKILL = path.join(__dirname, '..', 'publish', 'SKILL.md');

function buildPublish() {
  let content = fs.readFileSync(ROOT_SKILL, 'utf-8');
  const originalLen = content.length;
  const originalLines = content.split('\n').length;

  // Rule 1: Remove Extended Original Text blocks
  // Match from "> **原文扩展示例" to the next standalone "---" line
  content = content.replace(
    />\s*\*\*原文扩展示例\s*\(Extended Original Text\)\*\*[\s\S]*?(?=\n---\n)/g,
    ''
  );

  // Rule 1b: Remove any standalone [NEEDS_HUMAN_INPUT] lines
  content = content.replace(/\[NEEDS_HUMAN_INPUT[^\]]*\]/g, '');
  // Clean up empty lines created by removal (no more than 2 consecutive blank lines)
  content = content.replace(/\n{3,}/g, '\n\n');

  // Rule 3: Compress historical cases (Case 1-14) — keep title, first key sentence, and when-to-use
  // Each case block starts with "### Case N:" and ends before the next "### Case" or "### A Note on..."
  const caseRegex = /(### Case \d+:.*?\n\n)([\s\S]*?)(?=\n### Case |\n### A Note on My Blind)/g;
  content = content.replace(caseRegex, (match, header, body) => {
    // Take the first 2 non-empty, non-header lines as summary
    const meaningfulLines = body.split('\n')
      .map(l => l.trim())
      .filter(l => l && !l.startsWith('/') && !l.startsWith('**When') && !l.startsWith('**适用场景'))
      .slice(0, 2);
    // Extract the "When to use" line (bilingual)
    const whenLine = body.match(/\*\*When to use[^*]*\*\*.*/);
    const whenLineCN = body.match(/\*\*适用场景[^*]*\*\*.*/);
    const when = whenLine ? whenLine[0] : (whenLineCN ? whenLineCN[0] : '');
    return header + meaningfulLines.join('\n') + '\n\n' + when + '\n\n';
  });

  // Rule 4: Compress Part 4 dialogue guide — each item to 1 sentence
  // Strategy: keep the bold headers and the first sentence after each "**item**"
  const compressPart4 = (text) => {
    // Mode Behavior section — keep as-is (it's already short)
    // Tone items (1-6) — keep bold header + first sentence
    // Tone items (1-6) — keep bold header + first sentence
    const toneRegex = /(\*\*I should speak like this[\s\S]*?)(?=\*\*I must not speak like this)/;
    text = text.replace(toneRegex, (match) => {
      // Compress each numbered item to just the bold header
      return match.replace(/^(\d+\.\s+\*\*.*?\*\*).*$/gm, '$1');
    });
    return text;
  };
  content = compressPart4(content);

  // Rule 6: Compress reverse examples to failure reason + core lesson
  content = content.replace(
    /### Reverse \d+: (.*?)\n\n([\s\S]*?)(?=### Reverse|\n---\n\n> The common thread|\n---\n\n## Part 6)/g,
    (match, title, body) => {
      // Extract just the key lesson lines
      const keyLines = body.match(/^(>.*?)$/gm) || [];
      const firstSentence = body.split('\n').filter(l => l.trim() && !l.startsWith('>')).slice(0, 2).join(' ');
      return `### Reverse: ${title}\n\n${firstSentence.substring(0, 200)}...\n\n`;
    }
  );

  // Rule 7: Compress Part 6 boundary items
  content = content.replace(
    /### Do NOT use me for.*?\n\n([\s\S]*?)(?=### My Historical Limitations)/,
    (match) => {
      return match
        .replace(/\*\*(.*?)\*\*[\s\S]*?(?=\n\*\*|$)/g, '**$1** — excluded. / 排除。')
        .replace(/\n{3,}/g, '\n\n');
    }
  );

  const compressedLen = content.length;
  const compressedLines = content.split('\n').length;
  
  // Write output
  const publishDir = path.dirname(PUBLISH_SKILL);
  if (!fs.existsSync(publishDir)) fs.mkdirSync(publishDir, { recursive: true });
  
  fs.writeFileSync(PUBLISH_SKILL, content);

  console.log(`\n📦 build-publish.js — Compression Report`);
  console.log(`────────────────────────────────────`);
  console.log(`  Root SKILL.md:    ${originalLen} bytes, ${originalLines} lines`);
  console.log(`  Publish SKILL.md: ${compressedLen} bytes, ${compressedLines} lines`);
  console.log(`  Compression:      ${((1 - compressedLines / originalLines) * 100).toFixed(1)}%`);
  console.log(`────────────────────────────────────`);
  console.log(`✅ publish/SKILL.md generated\n`);
}

try {
  buildPublish();
} catch (err) {
  console.error('❌ build-publish.js failed:', err.message);
  process.exit(1);
}