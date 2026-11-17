#!/usr/bin/env node

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const skillRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const query = String(process.argv[2] || '').trim();
if (!query) throw new Error('Usage: read-contract.mjs <contract-id|model-code|app-code/api-code>');
const bundle = JSON.parse(fs.readFileSync(path.join(skillRoot, 'references', 'contracts.bundle.json'), 'utf8'));
const document = bundle.documents.find((item) => (
  item.contract_id === query || item.model_code === query || `${item.app_code}/${item.api_code}` === query
));
if (!document) throw new Error(`No bundled contract matches: ${query}`);
process.stdout.write(`${document.content}\n`);
