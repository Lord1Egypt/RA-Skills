#!/usr/bin/env node
// validate-templates - policy-check INDEX.json + verify every referenced template.

import { readFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { scanBundle } from './lib/bundle-scanner.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const TPL_DIR = path.join(ROOT, 'assets/templates');

const RED = '\x1b[31m', GREEN = '\x1b[32m', RESET = '\x1b[0m';
let failures = 0;
const fail = (msg) => { failures++; console.log(`${RED}x${RESET} ${msg}`); };
const ok = (msg) => console.log(`${GREEN}+${RESET} ${msg}`);

const EXPECTED = ['A-01', 'A-02', 'A-03', 'A-04', 'A-05', 'A-06', 'A-07', 'A-08', 'A-09', 'A-10', 'A-11', 'A-12'];
const TOP_LEVEL_KEYS = new Set(['version', 'author', 'description', 'modeRoutes']);
const ROUTE_KEYS = new Set(['mode', 'templateId', 'templateFile', 'triggers', 'stack', 'artifact', 'verify_command', 'fallback_note', 'example_prompt']);
const ROUTE_REQUIRED = ['mode', 'templateId', 'templateFile', 'triggers', 'stack', 'artifact', 'verify_command', 'example_prompt'];
const VERIFY_COMMAND = 'npm run verify:lite -- <bundle.prompt.md>';
const UNSAFE_TEXT_PATTERNS = [
  /\b(?:ignore|disregard)\s+(?:all\s+)?(?:previous|above|prior)\s+instructions\b/i,
  /\b(?:system|developer)\s+prompt\b/i,
  /\b(?:exfiltrate|credential\s+dump|private\s+key)\b/i,
  /\b(?:curl|wget|powershell|invoke-webrequest|start-process|bash\s+-c|sh\s+-c|rm\s+-rf)\b/i,
  /(?:&&|\|\||;;|>>|`|\$\()/,
];

function typeOf(value) {
  if (Array.isArray(value)) return 'array';
  if (value === null) return 'null';
  return typeof value;
}

function checkSafeText(value, pathStr, errs, { min = 1, max = 240 } = {}) {
  if (typeof value !== 'string') {
    errs.push(`${pathStr}: expected string, got ${typeOf(value)}`);
    return;
  }
  const trimmed = value.trim();
  if (trimmed.length < min) errs.push(`${pathStr}: too short (<${min})`);
  if (trimmed.length > max) errs.push(`${pathStr}: too long (>${max})`);
  for (const pattern of UNSAFE_TEXT_PATTERNS) {
    if (pattern.test(trimmed)) errs.push(`${pathStr}: contains unsafe instruction or shell-shaped text`);
  }
}

function validateIndex(index) {
  const errs = [];
  if (typeOf(index) !== 'object') return [`$: expected object, got ${typeOf(index)}`];

  for (const key of Object.keys(index)) {
    if (!TOP_LEVEL_KEYS.has(key)) errs.push(`$.${key}: unknown property`);
  }
  for (const key of TOP_LEVEL_KEYS) {
    if (!(key in index)) errs.push(`$.${key}: required`);
  }

  checkSafeText(index.version, '$.version', errs, { min: 3, max: 16 });
  if (typeof index.version === 'string' && !/^[0-9]+\.[0-9]+(?:\.[0-9]+)?$/.test(index.version)) {
    errs.push('$.version: must be semantic version like 1.0.0');
  }
  checkSafeText(index.author, '$.author', errs, { min: 1, max: 80 });
  checkSafeText(index.description, '$.description', errs, { min: 16, max: 640 });

  if (!Array.isArray(index.modeRoutes)) {
    errs.push(`$.modeRoutes: expected array, got ${typeOf(index.modeRoutes)}`);
    return errs;
  }
  if (index.modeRoutes.length !== EXPECTED.length) {
    errs.push(`$.modeRoutes: expected ${EXPECTED.length} routes, got ${index.modeRoutes.length}`);
  }

  for (const [i, route] of index.modeRoutes.entries()) {
    const routePath = `$.modeRoutes[${i}]`;
    if (typeOf(route) !== 'object') {
      errs.push(`${routePath}: expected object, got ${typeOf(route)}`);
      continue;
    }
    for (const key of Object.keys(route)) {
      if (!ROUTE_KEYS.has(key)) errs.push(`${routePath}.${key}: unknown property`);
    }
    for (const key of ROUTE_REQUIRED) {
      if (!(key in route)) errs.push(`${routePath}.${key}: required`);
    }

    checkSafeText(route.mode, `${routePath}.mode`, errs, { min: 4, max: 4 });
    if (typeof route.mode === 'string' && !/^A-(?:0[1-9]|1[0-2])$/.test(route.mode)) errs.push(`${routePath}.mode: invalid mode tag`);
    checkSafeText(route.templateId, `${routePath}.templateId`, errs, { min: 4, max: 80 });
    if (typeof route.templateId === 'string' && !/^T-[a-z0-9-]+$/.test(route.templateId)) errs.push(`${routePath}.templateId: invalid template id`);
    checkSafeText(route.templateFile, `${routePath}.templateFile`, errs, { min: 10, max: 120 });
    if (typeof route.templateFile === 'string' && !/^[a-z0-9-]+\.prompt\.md$/.test(route.templateFile)) errs.push(`${routePath}.templateFile: must be a local *.prompt.md file`);
    if (route.verify_command !== VERIFY_COMMAND) errs.push(`${routePath}.verify_command: must equal "${VERIFY_COMMAND}"`);

    if (!Array.isArray(route.triggers)) {
      errs.push(`${routePath}.triggers: expected array`);
    } else {
      if (route.triggers.length < 2 || route.triggers.length > 12) errs.push(`${routePath}.triggers: expected 2-12 entries`);
      for (const [j, trigger] of route.triggers.entries()) checkSafeText(trigger, `${routePath}.triggers[${j}]`, errs, { min: 2, max: 80 });
    }
    checkSafeText(route.stack, `${routePath}.stack`, errs, { min: 4, max: 160 });
    checkSafeText(route.artifact, `${routePath}.artifact`, errs, { min: 3, max: 160 });
    checkSafeText(route.example_prompt, `${routePath}.example_prompt`, errs, { min: 8, max: 220 });
    if ('fallback_note' in route) checkSafeText(route.fallback_note, `${routePath}.fallback_note`, errs, { min: 12, max: 220 });
  }

  return errs;
}

const indexPath = path.join(TPL_DIR, 'INDEX.json');

if (!existsSync(indexPath)) {
  fail('assets/templates/INDEX.json missing');
  process.exit(1);
}

const indexRaw = await readFile(indexPath, 'utf8');
let index;
try {
  index = JSON.parse(indexRaw);
} catch (error) {
  fail(`INDEX.json invalid JSON: ${error.message}`);
  process.exit(1);
}

const policyErrors = validateIndex(index);
if (policyErrors.length) {
  for (const error of policyErrors) fail(error);
} else {
  ok('INDEX.json conforms to the built-in template registry policy');
}

const seenModes = new Set();
const seenTemplateIds = new Set();
for (const route of index.modeRoutes || []) {
  if (seenModes.has(route.mode)) fail(`duplicate mode ${route.mode} in INDEX.json`);
  if (seenTemplateIds.has(route.templateId)) fail(`duplicate templateId ${route.templateId} in INDEX.json`);
  seenModes.add(route.mode);
  seenTemplateIds.add(route.templateId);

  const filePath = path.join(TPL_DIR, route.templateFile || '');
  if (!existsSync(filePath)) {
    fail(`${route.mode}: templateFile ${route.templateFile} not found`);
    continue;
  }
  if (path.dirname(path.relative(TPL_DIR, filePath)) !== '.') {
    fail(`${route.mode}: templateFile must stay directly inside assets/templates`);
    continue;
  }

  const raw = await readFile(filePath, 'utf8');
  const { findings } = scanBundle(raw, { templateMode: true });
  const errors = findings.filter(f => f.level === 'error');
  if (errors.length) {
    for (const error of errors) fail(`${route.templateFile} [${error.code}]: ${error.message}`);
  } else {
    ok(`${route.mode}  ${route.templateFile}`);
  }
  if (!raw.includes(route.mode)) fail(`${route.templateFile} does not mention mode ${route.mode}`);
  if (!raw.includes(route.templateId)) fail(`${route.templateFile} does not mention templateId ${route.templateId}`);
}

for (const mode of EXPECTED) {
  if (!seenModes.has(mode)) fail(`expected mode ${mode} not found in INDEX.json`);
}

console.log('');
if (failures) {
  console.log(`${RED}x validate-templates: ${failures} failure(s)${RESET}`);
  process.exit(1);
}
console.log(`${GREEN}+ validate-templates: ${index.modeRoutes.length} template(s) registered, all clean${RESET}`);
