#!/usr/bin/env node
import { mkdirSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import process from 'node:process';

import { defaultFailureSources, scanFailureSources } from './harness-improvement-lib.mjs';

const workspace = process.env.WORKSPACE || resolve(process.env.HOME || '/Users/m1', '.openclaw/workspace');
const openclawHome = process.env.OPENCLAW_HOME || resolve(process.env.HOME || '/Users/m1', '.openclaw');

function argValue(name, fallback = null) {
  const index = process.argv.indexOf(name);
  return index === -1 ? fallback : process.argv[index + 1] || fallback;
}

function hasFlag(name) {
  return process.argv.includes(name);
}

function shanghaiDate() {
  return new Date().toLocaleDateString('sv-SE', { timeZone: 'Asia/Shanghai' });
}

function markdownBacklog(scan) {
  const lines = [
    `# Harness Backlog — ${shanghaiDate()}`,
    '',
    `Generated: ${scan.generatedAt}`,
    `Sources scanned: ${scan.sources.length}`,
    `Failure events: ${scan.summary.total}`,
    '',
    '## Top Failure Classes',
    '',
  ];
  if (!scan.summary.topClasses.length) lines.push('- No classified failures found in scanned sources.');
  for (const item of scan.summary.topClasses) {
    lines.push(`- ${item.failureClass}: ${item.count} event(s), severity=${item.severity}`);
    lines.push(`  Next action: ${item.nextAction}`);
    for (const example of item.examples.slice(0, 3)) lines.push(`  Evidence: ${example.source}: ${example.evidence}`);
  }
  lines.push('', '## Operating Rule', '');
  lines.push('- Repeated classified failures should become a guardrail, test, or repair task; do not rely on operator memory.');
  lines.push('- Unclassified failures should be reduced over time by adding explicit rules after inspection.');
  return `${lines.join('\n')}\n`;
}

const outputPath = argValue('--output', null);
const explicitSources = process.argv.filter((arg, index) => index > 1 && !arg.startsWith('--') && process.argv[index - 1] !== '--output');
const sources = explicitSources.length ? explicitSources.map((path) => resolve(path)) : defaultFailureSources(openclawHome, workspace);
const scan = scanFailureSources(sources);

if (outputPath) {
  const path = resolve(outputPath);
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, hasFlag('--json') ? `${JSON.stringify(scan, null, 2)}\n` : markdownBacklog(scan));
  console.log(path);
} else if (hasFlag('--json')) {
  console.log(JSON.stringify(scan, null, 2));
} else {
  process.stdout.write(markdownBacklog(scan));
}
