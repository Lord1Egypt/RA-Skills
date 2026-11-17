#!/usr/bin/env node

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const skillRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const projectRoot = path.resolve(skillRoot, '..', '..');
const sourceRoot = path.resolve(process.argv[2] || path.join(projectRoot, 'api-doc', 'online-developer-docs'));
const outputFile = path.resolve(process.argv[3] || path.join(skillRoot, 'references', 'contracts.bundle.json'));
const manifestFile = path.join(sourceRoot, 'manifest.json');

if (!fs.existsSync(manifestFile)) throw new Error(`Missing documentation manifest: ${manifestFile}`);
const manifest = JSON.parse(fs.readFileSync(manifestFile, 'utf8'));
function safetyPrefix(document) {
  if (document.app_code !== 'watermark_removal') return '';
  return '## Authorized Use\n\nOnly process content the user owns or is authorized to process. Do not bulk collect social-media content, evade platform restrictions, or remove attribution from third-party media.\n\n';
}

const documents = manifest.documents.map((document) => ({
  ...document,
  contract_id: document.slug,
  content: `${safetyPrefix(document)}${fs.readFileSync(path.join(sourceRoot, document.file), 'utf8')}`,
}));

fs.mkdirSync(path.dirname(outputFile), { recursive: true });
fs.writeFileSync(outputFile, `${JSON.stringify({ schema_version: 1, source: manifest.source, exported_at: manifest.exported_at, documents }, null, 2)}\n`);
process.stdout.write(`${JSON.stringify({ output: outputFile, documents: documents.length }, null, 2)}\n`);
