#!/usr/bin/env node

/**
 * IFQ Design Skills · Anti-Slop Preflight Scanner
 * Zero-dependency Node script that scans HTML for 7 AI-slop violations.
 * See references/anti-ai-slop.md for the full checklist.
 *
 * Usage: node scripts/anti-slop-preflight.mjs <file.html> [file2.html ...]
 * Exit 0 = clean, Exit 1 = violations found.
 */

import fs from 'node:fs';
import path from 'node:path';

const violations = [];

function fail(file, rule, detail) {
  violations.push({ file, rule, detail });
}

function scanFile(filePath) {
  const html = fs.readFileSync(filePath, 'utf8');
  const rel = path.relative(process.cwd(), filePath);
  const lines = html.split(/\r?\n/);

  // Strip <script> and <style> blocks for content analysis
  const stripped = html
    .replace(/<script[\s\S]*?<\/script>/gi, '')
    .replace(/<style[\s\S]*?<\/style>/gi, '');

  // Rule 1: Side border-left > 1px on cards/alerts
  // Look for border-left with width > 1px in <style> blocks
  // Allow: blockquote/annotation uses (border-left on elements with quote/annotation/think in the selector)
  const styleBlocks = [...html.matchAll(/<style[^>]*>([\s\S]*?)<\/style>/gi)].map(m => m[1]);
  for (const style of styleBlocks) {
    // Split into rule blocks to check context
    const ruleBlocks = style.split(/(?=\})|(?<=\{)/);
    const borderLeftMatches = style.match(/border-left\s*:\s*(\d+(?:\.\d+)?)(px|rem|em)/gi) || [];
    for (const match of borderLeftMatches) {
      const numMatch = match.match(/(\d+(?:\.\d+)?)(px|rem|em)/i);
      if (numMatch) {
        const val = parseFloat(numMatch[1]);
        const unit = numMatch[2].toLowerCase();
        let isViolation = false;
        if (unit === 'px' && val > 1) { isViolation = true; }
        if ((unit === 'rem' || unit === 'em') && val > 0.0625) { isViolation = true; }
        if (isViolation) {
          // Find the selector context for this match
          const matchIndex = style.indexOf(match);
          const preceding = style.substring(Math.max(0, matchIndex - 300), matchIndex);
          // Match the last complete selector before the opening brace
          const selectorMatch = preceding.match(/([^{}]+)\s*\{[^}]*$/);
          const selector = selectorMatch ? selectorMatch[1].trim() : '';
          // Allow blockquote/annotation/quote contexts, nav items, timelines, verdicts, and active states
          if (/quote|annotation|think|pull|cite|aside|nav|timeline|verdict|ledger|rail|spine|active|indicator|progress/i.test(selector)) {
            continue;
          }
          fail(rel, 'border-left-width', `border-left > 1px found in "${selector || 'unknown'}": ${match.trim()} — use full border, background block, or icon lead instead`);
        }
      }
    }
  }

  // Rule 2: Gradient text (background-clip: text)
  for (const style of styleBlocks) {
    if (/background-clip\s*:\s*text/i.test(style) || /-webkit-background-clip\s*:\s*text/i.test(style)) {
      fail(rel, 'gradient-text', 'background-clip: text detected — use solid color + weight/size for hierarchy');
    }
  }

  // Rule 3: Default glassmorphism (backdrop-filter: blur as card default)
  for (const style of styleBlocks) {
    if (/backdrop-filter\s*:\s*blur/i.test(style)) {
      fail(rel, 'glassmorphism', 'backdrop-filter: blur detected — use only when real spatial depth exists');
    }
  }

  // Rule 4: Hero-metric template pattern (big number + small label + gradient)
  // Heuristic: look for font-size > 36px near "metric" or "kpi" or "stat" class names
  for (const style of styleBlocks) {
    const heroMetricRe = /\.(?:metric|kpi|stat|hero[_-]?num|big[_-]?num)[^{]*\{[^}]*font-size\s*:\s*(\d+)/gi;
    let match;
    while ((match = heroMetricRe.exec(style)) !== null) {
      const size = parseInt(match[1], 10);
      if (size >= 40) {
        // Check if there's also a gradient nearby
        const context = style.substring(Math.max(0, match.index - 200), match.index + 300);
        if (/gradient/i.test(context)) {
          fail(rel, 'hero-metric', `Large metric number (${size}px) with gradient nearby — SaaS cliché since 2018`);
        }
      }
    }
  }

  // Rule 5: Same-size icon card grid (heuristic: repeated grid children with identical dimensions)
  // This is hard to detect statically — skip for now (better caught by manual review)

  // Rule 6: Purple gradient on white
  for (const style of styleBlocks) {
    if (/purple/i.test(style) || /#[6-9a-f][0-9a-f]{2,3}.*gradient/i.test(style)) {
      const hasWhite = /background\s*:\s*(?:#fff(?:fff)?|white)/i.test(style);
      if (hasWhite && /gradient/i.test(style)) {
        fail(rel, 'purple-gradient', 'Possible purple gradient on white background — AI "premium" cliché');
      }
    }
    // Also check for typical purple hex values with gradients
    const purpleGradRe = /background\s*:[^;]*(?:#[89a-f][0-9a-f]{5}|rgb\s*\(\s*(?:1[0-9]{2}|2[0-3][0-9])\s*,\s*\d+\s*,\s*(?:1[5-9][0-9]|2[0-5][0-9])\s*\))[^;]*gradient/i;
    if (purpleGradRe.test(style)) {
      fail(rel, 'purple-gradient', 'Purple gradient detected — use a different color strategy');
    }
  }

  // Rule 7: Display font = Inter/Roboto/Arial/system default
  for (const style of styleBlocks) {
    const displayFontRe = /(?:--ifq-display|--ifq-font-display|font-family)\s*:[^;]*'(Inter|Roboto|Arial)'/gi;
    let match;
    while ((match = displayFontRe.exec(style)) !== null) {
      fail(rel, 'display-font', `Display font set to ${match[1]} — use Newsreader, Noto Serif SC, or user's brand font`);
    }
  }

  // Additional: Check for Lorem ipsum
  if (/lorem\s+ipsum/i.test(stripped)) {
    fail(rel, 'lorem-ipsum', 'Lorem ipsum placeholder found — use real content or labeled placeholder');
  }

  // Additional: Check for generic AI copy
  const genericPhrases = [
    /welcome\s+to\s+your\s+dashboard/i,
    /get\s+started\s+in\s+seconds/i,
    /unlock\s+your\s+potential/i,
    /take\s+your\s+\w+\s+to\s+the\s+next\s+level/i,
  ];
  for (const phrase of genericPhrases) {
    if (phrase.test(stripped)) {
      fail(rel, 'generic-copy', `Generic AI copy detected: "${phrase.source}" — use specific, concrete language`);
    }
  }
}

// Main
const args = process.argv.slice(2);
if (args.length === 0) {
  console.error('Usage: node scripts/anti-slop-preflight.mjs <file.html> [file2.html ...]');
  process.exit(1);
}

for (const arg of args) {
  const filePath = path.resolve(arg);
  if (!fs.existsSync(filePath)) {
    console.error(`File not found: ${arg}`);
    process.exit(1);
  }
  scanFile(filePath);
}

if (violations.length === 0) {
  console.log(`✓ anti-slop preflight passed (${args.length} file${args.length > 1 ? 's' : ''} scanned)`);
  process.exit(0);
} else {
  console.error(`\nanti-slop violations found (${violations.length}):\n`);
  for (const v of violations) {
    console.error(`  ✗ [${v.rule}] ${v.file}: ${v.detail}`);
  }
  console.error(`\nSee references/anti-ai-slop.md for the full checklist and fixes.`);
  process.exit(1);
}
