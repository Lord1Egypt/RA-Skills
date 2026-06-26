#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const manifestPath = process.argv[2];
if (!manifestPath) {
  console.error('Usage: node validate-screenshots.mjs <manifest.json>');
  process.exit(1);
}

const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
const minBytes = Number(process.env.MIN_SCREENSHOT_BYTES || 28000);
let ok = true;

function check(label, filePath, extra = '') {
  if (!filePath) return;
  const stat = fs.statSync(filePath);
  if (stat.size < minBytes) {
    console.error(`FAIL ${label}: ${stat.size} bytes (< ${minBytes})`);
    ok = false;
  } else {
    console.log(`OK ${label}: ${stat.size} bytes${extra}`);
  }
}

for (const section of manifest.sections || []) {
  if (!section.file) continue;
  check(section.heading, section.file, section.barCount != null ? `, bars=${section.barCount}` : '');
}

for (const cat of manifest.categoryScenarios || []) {
  if (!cat.file) continue;
  const top = cat.rankings?.[0]?.model ? `, top=${cat.rankings[0].model}` : '';
  check(`Categories/${cat.scenario}`, cat.file, top);
  if (!cat.rankings?.length) {
    console.error(`FAIL Categories/${cat.scenario}: no rankings parsed`);
    ok = false;
  }
}

if (manifest.fullPage?.file) {
  check('full page', manifest.fullPage.file);
}

const summaryPath = path.join(path.dirname(manifestPath), 'summary.md');
if (!fs.existsSync(summaryPath)) {
  console.error('FAIL summary.md missing — run capture-rankings.mjs');
  ok = false;
} else {
  console.log('OK summary.md present');
}

process.exit(ok ? 0 : 1);
