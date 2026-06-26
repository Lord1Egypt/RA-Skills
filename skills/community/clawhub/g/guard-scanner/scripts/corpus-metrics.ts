import { fileURLToPath } from 'node:url';
import { dirname } from 'node:path';
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
// @ts-nocheck
import fs from 'node:fs';
import path from 'node:path';

import { GuardScanner }  from '../src/scanner';

const ROOT = path.join(__dirname, '..');
const corpusPath = path.join(ROOT, 'tests', 'fixtures', 'corpus', 'security-corpus.json');
const outputPath = path.join(ROOT, 'docs', 'data', 'corpus-metrics.json');
const corpus = JSON.parse(fs.readFileSync(corpusPath, 'utf8'));
const scanner = new GuardScanner({ quiet: true, summaryOnly: true });

let truePositives = 0;
let falsePositives = 0;
let falseNegatives = 0;
let trueNegatives = 0;

for (const sample of corpus.malicious) {
  const result = scanner.scanText(sample.content);
  if (result.detections.length > 0) truePositives++;
  else falseNegatives++;
}

for (const sample of corpus.benign) {
  const result = scanner.scanText(sample.content);
  if (result.detections.length > 0) falsePositives++;
  else trueNegatives++;
}

const metrics = {
  generatedAt: new Date().toISOString(),
  corpus: {
    benign: corpus.benign.length,
    malicious: corpus.malicious.length,
  },
  precision: truePositives / Math.max(1, (truePositives + falsePositives)),
  recall: truePositives / Math.max(1, (truePositives + falseNegatives)),
  false_positive_rate: falsePositives / Math.max(1, corpus.benign.length),
  false_negative_rate: falseNegatives / Math.max(1, corpus.malicious.length),
};

if (process.argv.includes('--check')) {
  const existing = JSON.parse(fs.readFileSync(outputPath, 'utf8'));
  const current = JSON.stringify({ ...metrics, generatedAt: 'ignored' });
  const baseline = JSON.stringify({ ...existing, generatedAt: 'ignored' });
  if (current !== baseline) {
    console.error('❌ corpus metrics drift detected. Run node scripts/corpus-metrics.js to refresh baseline.');
    process.exit(1);
  }
  console.log('✅ Corpus metrics match baseline');
} else {
  fs.writeFileSync(outputPath, JSON.stringify(metrics, null, 2) + '\n');
  console.log(`✅ Corpus metrics written to ${outputPath}`);
}
