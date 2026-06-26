#!/usr/bin/env node
// Validates evals/evals.json without network, dependencies, or process control.

import { promises as fs } from 'node:fs';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const EVALS_PATH = path.join(ROOT, 'evals', 'evals.json');
const EVALS_SCHEMA_PATH = path.join(ROOT, 'evals', 'evals.schema.json');
const TEMPLATE_INDEX_PATH = path.join(ROOT, 'assets', 'templates', 'INDEX.json');
const REQUIRED_MODES = Array.from({ length: 12 }, (_, idx) => `M-${String(idx + 1).padStart(2, '0')}`);
const SAFE_COMMAND_PREFIXES = [
  'npm run verify:lite -- ',
  'npm run preview -- ',
  'manual ',
];

let failures = 0;

function fail(message) {
  failures += 1;
  console.log(`FAIL ${message}`);
}

function ok(message) {
  console.log(`OK ${message}`);
}

async function readJson(filePath) {
  return JSON.parse(await fs.readFile(filePath, 'utf8'));
}

function isPlainObject(value) {
  return value !== null && typeof value === 'object' && !Array.isArray(value);
}

function validId(value) {
  return typeof value === 'string' && /^[a-z0-9][a-z0-9-]{2,80}$/.test(value);
}

function safeRelativePath(value) {
  return typeof value === 'string' && value.length > 0 && !value.startsWith('/') && !value.includes('..');
}

function normalizeLocalSchemaPath(value) {
  if (typeof value !== 'string' || !value.trim()) return null;
  return value.replace(/^\.\//, '');
}

function validateStringArray(value, label, scenarioId, minimum = 1) {
  if (!Array.isArray(value) || value.length < minimum) {
    fail(`${scenarioId}: ${label} must contain at least ${minimum} item(s)`);
    return [];
  }
  for (const item of value) {
    if (typeof item !== 'string' || item.trim().length === 0) {
      fail(`${scenarioId}: ${label} contains an empty or non-string item`);
    }
  }
  return value;
}

function validateCommand(command, scenarioId) {
  if (typeof command !== 'string' || command.length === 0) {
    fail(`${scenarioId}: verification command must be a non-empty string`);
    return;
  }
  if (!SAFE_COMMAND_PREFIXES.some((prefix) => command.startsWith(prefix))) {
    fail(`${scenarioId}: unsupported verification command ${JSON.stringify(command)}`);
  }
}

async function main() {
  if (!existsSync(EVALS_PATH)) {
    fail('missing evals/evals.json');
    process.exit(1);
  }

  const evals = await readJson(EVALS_PATH);
  const templateIndex = await readJson(TEMPLATE_INDEX_PATH);
  const templateIds = new Set((templateIndex.templates || []).map((template) => template.id));
  const routeModes = new Set(Object.keys(templateIndex.modeRoutes || {}));
  const routeByMode = templateIndex.modeRoutes || {};

  const schemaPath = normalizeLocalSchemaPath(evals.$schema);
  if (schemaPath !== 'evals.schema.json') {
    fail(`evals.$schema must be "./evals.schema.json", found ${JSON.stringify(evals.$schema)}`);
  }
  if (!existsSync(EVALS_SCHEMA_PATH)) {
    fail('missing evals/evals.schema.json');
  }

  if (evals.version !== '1.0') fail(`evals.version must be "1.0", found ${JSON.stringify(evals.version)}`);
  validateStringArray(evals.quality_principles, 'quality_principles', 'evals', 3);
  if (!Array.isArray(evals.scenarios) || evals.scenarios.length < REQUIRED_MODES.length) {
    fail(`evals.scenarios must cover at least ${REQUIRED_MODES.length} scenarios`);
  }

  const ids = new Set();
  const coveredModes = new Set();
  let firstRunCoverage = false;

  for (const scenario of evals.scenarios || []) {
    if (!isPlainObject(scenario)) {
      fail('scenario entry must be an object');
      continue;
    }

    const id = scenario.id || '(missing-id)';
    if (!validId(scenario.id)) fail(`${id}: id must be kebab-case and stable`);
    if (ids.has(scenario.id)) fail(`${id}: duplicate id`);
    ids.add(scenario.id);

    const route = routeByMode[scenario.mode];
    if (!routeModes.has(scenario.mode)) fail(`${id}: unknown mode ${JSON.stringify(scenario.mode)}`);
    else coveredModes.add(scenario.mode);

    for (const key of ['prompt_zh', 'prompt_en', 'user_value', 'agent_value']) {
      if (typeof scenario[key] !== 'string' || scenario[key].trim().length < 12) {
        fail(`${id}: ${key} must be descriptive`);
      }
    }

    const contract = scenario.agent_contract;
    if (!isPlainObject(contract)) {
      fail(`${id}: agent_contract is required`);
      continue;
    }

    if (typeof contract.route !== 'string' || !contract.route.includes(scenario.mode)) {
      fail(`${id}: agent_contract.route must include ${scenario.mode}`);
    }

    const contractTemplateIds = validateStringArray(contract.template_ids, 'agent_contract.template_ids', id);
    for (const templateId of contractTemplateIds) {
      if (!templateIds.has(templateId)) fail(`${id}: unknown template id ${templateId}`);
    }
    if (route?.primaryTemplate && !contractTemplateIds.includes(route.primaryTemplate)) {
      fail(`${id}: agent_contract.template_ids must include route primary template ${route.primaryTemplate}`);
    }

    const mustRead = validateStringArray(contract.must_read, 'agent_contract.must_read', id, 2);
    for (const relPath of mustRead) {
      if (!safeRelativePath(relPath)) {
        fail(`${id}: unsafe must_read path ${JSON.stringify(relPath)}`);
      } else if (!existsSync(path.join(ROOT, relPath))) {
        fail(`${id}: must_read path missing ${relPath}`);
      }
    }
    for (const relPath of route?.requiredReferences || []) {
      if (!mustRead.includes(relPath)) {
        fail(`${id}: agent_contract.must_read must include route reference ${relPath}`);
      }
    }

    if (typeof contract.tier !== 'string' || !contract.tier.includes('Tier')) {
      fail(`${id}: agent_contract.tier must name the tier policy`);
    }

    const verification = validateStringArray(contract.verification, 'agent_contract.verification', id, 2);
    for (const command of verification) {
      validateCommand(command, id);
    }
    if (!verification.some((command) => command.startsWith('npm run verify:lite -- '))) {
      fail(`${id}: verification must include npm run verify:lite`);
    }
    if (!verification.some((command) => command.startsWith('npm run preview -- '))) {
      fail(`${id}: verification must include npm run preview`);
    }

    if (typeof contract.fact_check_required !== 'boolean') {
      fail(`${id}: agent_contract.fact_check_required must be boolean`);
    }

    if (String(scenario.id).includes('first-run') || /ClawHub/i.test(`${scenario.prompt_en} ${scenario.prompt_zh}`)) {
      firstRunCoverage = true;
      const firstRunText = [
        ...(contract.verification || []),
        ...(scenario.quality_bar?.must_include || []),
        ...(scenario.quality_bar?.must_not || []),
      ].join(' | ');
      for (const token of ['file', 'route', 'template', 'assumptions', 'verification', 'caveats']) {
        if (!firstRunText.toLowerCase().includes(token)) {
          fail(`${id}: first-run coverage must mention ${token} in evidence expectations`);
        }
      }
    }

    if (!isPlainObject(scenario.quality_bar)) {
      fail(`${id}: quality_bar is required`);
      continue;
    }
    validateStringArray(scenario.quality_bar.must_include, 'quality_bar.must_include', id, 3);
    validateStringArray(scenario.quality_bar.must_not, 'quality_bar.must_not', id, 2);
  }

  for (const mode of REQUIRED_MODES) {
    if (!coveredModes.has(mode)) fail(`missing eval coverage for ${mode}`);
  }
  if (!firstRunCoverage) {
    fail('eval suite must include a ClawHub first-run activation scenario');
  }

  if (failures === 0) {
    ok(`${(evals.scenarios || []).length} scenarios validated; all 12 modes covered`);
    process.exit(0);
  }
  process.exit(1);
}

main().catch((error) => {
  fail(`eval validator crashed: ${error.message}`);
  process.exit(2);
});
