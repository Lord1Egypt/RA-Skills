import { fileURLToPath } from 'node:url';
import { dirname } from 'node:path';
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
// @ts-nocheck
import fs from 'node:fs';
import path from 'node:path';

const ROOT = path.join(__dirname, '..');
const pkg = JSON.parse(fs.readFileSync(path.join(ROOT, 'package.json'), 'utf8'));
const lock = JSON.parse(fs.readFileSync(path.join(ROOT, 'package-lock.json'), 'utf8'));
const outPath = path.join(ROOT, 'docs', 'spec', 'sbom.json');

const components = Object.entries(lock.packages || {})
  .filter(([name]) => name)
  .map(([name, meta]) => ({
    name: name.replace(/^node_modules\//, ''),
    version: meta.version || 'unknown',
    license: meta.license || 'UNKNOWN',
  }));

const sbom = {
  bomFormat: 'CycloneDX-like',
  specVersion: '0.1',
  metadata: {
    component: {
      name: pkg.name,
      version: pkg.version,
    },
    generatedAt: new Date().toISOString(),
  },
  components,
};

fs.writeFileSync(outPath, JSON.stringify(sbom, null, 2) + '\n');
console.log(`✅ SBOM written to ${outPath}`);
