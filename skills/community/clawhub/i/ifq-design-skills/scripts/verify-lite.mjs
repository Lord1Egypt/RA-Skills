#!/usr/bin/env node
// Zero-dependency static sanity check for shipped HTML.
// It does not launch a browser; use host browser tools for rendered checks.

import { readFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { resolve, basename } from 'node:path';

const files = process.argv.slice(2).filter((arg) => !arg.startsWith('--'));
if (!files.length) {
  console.error('Usage: node scripts/verify-lite.mjs <file.html> [more.html ...]');
  process.exit(1);
}

const PATTERNS = [
  ['brace-placeholder', /\{[^{}\n<>]{1,120}\}/g],
  ['year-token', /(^|[^A-Za-z0-9_])(YYYY|<year>)(?=$|[^A-Za-z0-9_])/g],
  ['month-day-token', /(^|[^A-Za-z0-9_])(MM|DD)(?=$|[^A-Za-z0-9_])/g],
  ['lorem-ipsum', /\blorem\s+ipsum\b/gi],
  ['template-stub', /\b(your\s+(headline|title|name|cta)\s+here|replace\s+me|TODO:)/gi],
  ['ifq-taxonomy-leak', /(^|[^A-Za-z0-9_])(FIELD\s+NOTE|SIGNAL\s+SPARK|RUST\s+LEDGER|MONO\s+FIELD\s+NOTE|QUIET\s+URL|EDITORIAL\s+CONTRAST)(?=$|[^A-Za-z0-9_])/g],
];
const EMPTY_DATE_ATTR = /<[^>]+\sdata-ifq-(year|month|day)[^>]*>\s*<\/[^>]+>/gi;

function stripScriptsAndStyles(html) {
  return html
    .replace(/<script\b[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style\b[\s\S]*?<\/style>/gi, ' ')
    .replace(/<!--[\s\S]*?-->/g, ' ');
}

function stripTags(html) {
  return html.replace(/<[^>]+>/g, ' ');
}

function clip(text, start, end, radius = 36) {
  return text
    .slice(Math.max(0, start - radius), Math.min(text.length, end + radius))
    .replace(/\s+/g, ' ')
    .trim();
}

let totalFindings = 0;

for (const rel of files) {
  const abs = resolve(process.cwd(), rel);
  if (!existsSync(abs)) {
    console.error(`ERROR: file not found: ${abs}`);
    totalFindings += 1;
    continue;
  }

  const raw = await readFile(abs, 'utf8');
  const bodyText = stripTags(stripScriptsAndStyles(raw));
  const findings = [];

  for (const [name, pattern] of PATTERNS) {
    pattern.lastIndex = 0;
    for (const match of bodyText.matchAll(pattern)) {
      const token = match[2] || match[0];
      const offset = match.index + (match[1] ? match[1].length : 0);
      findings.push({ kind: name, token, context: clip(bodyText, offset, offset + token.length) });
    }
  }

  for (const match of raw.matchAll(EMPTY_DATE_ATTR)) {
    findings.push({
      kind: 'empty-ifq-date-attr',
      token: match[0].slice(0, 60),
      context: 'date attribute rendered empty',
    });
  }

  console.log(`\n- ${basename(abs)}`);
  if (!findings.length) {
    console.log('  ok: no placeholder leaks');
    continue;
  }

  totalFindings += findings.length;
  for (const finding of findings.slice(0, 30)) {
    console.log(`  [${finding.kind}] ${finding.token} <- ${finding.context}`);
  }
  if (findings.length > 30) {
    console.log(`  ... and ${findings.length - 30} more`);
  }
}

if (totalFindings === 0) {
  console.log('\nverify-lite: all clean');
  process.exit(0);
}

console.log(`\nverify-lite: ${totalFindings} finding(s); fix before shipping`);
process.exit(1);
