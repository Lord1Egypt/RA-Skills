#!/usr/bin/env node

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const bundle = JSON.parse(fs.readFileSync(path.join(root, 'references', 'contracts.bundle.json'), 'utf8'));
const catalog = JSON.parse(fs.readFileSync(path.join(root, 'references', 'capability-catalog.json'), 'utf8'));
const errors = [];
const bundledContracts = new Set(bundle.documents.map((document) => document.contract_id));

if (catalog.capabilities.length !== bundle.documents.length) {
  errors.push(`Catalog has ${catalog.capabilities.length} entries; bundle has ${bundle.documents.length}.`);
}

for (const capability of catalog.capabilities) {
  if (!bundledContracts.has(capability.contract_id)) errors.push(`Missing bundled contract: ${capability.contract_id}`);
  if (capability.contract_file !== `contracts.bundle.json#${capability.contract_id}`) errors.push(`Invalid contract reference: ${capability.contract_id}`);
  if (capability.kind === 'app_api' && capability.semantic?.operation === 'direct_app_call') {
    errors.push(`Unclassified application capability: ${capability.resource_key}`);
  }
}

const appApis = catalog.capabilities.filter((item) => item.kind === 'app_api');
const models = catalog.capabilities.filter((item) => item.kind === 'model');
const summary = {
  contracts: bundle.documents.length,
  model_contracts: models.length,
  app_api_contracts: appApis.length,
  active_models_on_snapshot: models.filter((item) => item.active_on_snapshot).length,
  active_app_apis_on_snapshot: appApis.filter((item) => item.active_on_snapshot).length,
  errors,
};

process.stdout.write(`${JSON.stringify(summary, null, 2)}\n`);
process.exit(errors.length ? 1 : 0);
