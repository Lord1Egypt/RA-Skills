#!/usr/bin/env node
import { loadPen, parseArgs, printHelpAndExit, fail } from './_utils.mjs';

const HELP = `Usage: node scripts/validate-pen.mjs <file.pen>\n\nValidates a .pen file for structural correctness, value-type checks, ID uniqueness,\nvariable references, node types, and design best practices.`;
const args = parseArgs(process.argv.slice(2));
if (args.help) printHelpAndExit(HELP);
const file = args._[0];
if (!file) printHelpAndExit(HELP, 1);

const ALLOWED = new Set([
  'rectangle','ellipse','line','polygon','path','text','frame','group','note','prompt','context','icon_font','ref'
]);

// _PRIVATE schema node types intentionally excluded from public authoring/type unions.
const PRIVATE_TYPES = new Set(['connection']);

function warn(msg){ console.log(`⚠️ ${msg}`); }

function describeType(value) {
  if (Array.isArray(value)) return 'array';
  if (value === null) return 'null';
  return typeof value;
}

function isObject(value) {
  return value && typeof value === 'object' && !Array.isArray(value);
}

function isObjectOrObjectArray(value) {
  if (isObject(value)) return true;
  return Array.isArray(value) && value.every(isObject);
}

function isVariableBindingString(value) {
  return typeof value === 'string' && value.startsWith('$');
}

function isObjectOrObjectArrayOrVariable(value) {
  return isObjectOrObjectArray(value) || isVariableBindingString(value);
}

function nodeLabel(node) {
  return typeof node?.id === 'string' && node.id.trim() ? node.id : '(unknown)';
}

const data = loadPen(file);

if (!data.version) fail('missing top-level key: version');
if (data.version !== '2.8') fail(`version must be "2.8", got "${data.version}"`);
if (!Array.isArray(data.children)) fail('top-level children must be array');

const idMap = new Map();
const reusableIds = new Set();
const variableKeys = new Set(Object.keys(data.variables || {}));

function collectVariablesFromValue(value, path) {
  if (typeof value === 'string') {
    if (value.startsWith('$')) {
      if (!variableKeys.has(value.slice(1))) {
        warn(`${path} references undefined variable: ${value}`);
      }
    }
    return;
  }
  if (Array.isArray(value)) {
    value.forEach((v, i) => collectVariablesFromValue(v, `${path}[${i}]`));
    return;
  }
  if (value && typeof value === 'object') {
    for (const [k, v] of Object.entries(value)) {
      collectVariablesFromValue(v, `${path}.${k}`);
    }
  }
}

function walk(node, p='root', parent=null) {
  if (typeof node !== 'object' || node === null) fail(`${p} must be object`);

  if (node.type && !ALLOWED.has(node.type) && !PRIVATE_TYPES.has(node.type)) {
    warn(`${p} unknown type: ${node.type}`);
  }

  for (const [plural, singular] of [['fills', 'fill'], ['strokes', 'stroke'], ['effects', 'effect']]) {
    if (plural in node) {
      warn(`${p} uses plural alias "${plural}" (scripts auto-normalize to "${singular}")`);
    }
  }

  if (typeof node.id !== 'string' || !node.id.trim()) {
    fail(`${p}.id must be non-empty string`);
  }

  if (node.id.includes('/')) {
    fail(`${p}.id must not contain '/': ${node.id}`);
  }

  if (idMap.has(node.id)) {
    const prev = idMap.get(node.id);
    fail(`${p}.id duplicated: '${node.id}' already used at ${prev}`);
  }
  idMap.set(node.id, p);

  if (node.reusable === true) {
    reusableIds.add(node.id);
  }

  if (node.type === 'text') {
    const hasTextGrowth = typeof node.textGrowth === 'string';
    if (!hasTextGrowth && ('width' in node || 'height' in node)) {
      warn(`${p} text uses width/height without textGrowth (may be ignored)`);
    }
  }

  for (const prop of ['fill', 'stroke', 'effect']) {
    if (prop in node && !isObjectOrObjectArrayOrVariable(node[prop])) {
      warn(`node "${nodeLabel(node)}" has invalid ${prop} value (expected object or array, got ${describeType(node[prop])})`);
    }
  }

  for (const prop of ['width', 'height']) {
    if (prop in node) {
      const value = node[prop];
      if (!(typeof value === 'number' || typeof value === 'string')) {
        warn(`node "${nodeLabel(node)}" has invalid ${prop} value (expected number or string, got ${describeType(value)})`);
      }
    }
  }

  if ('opacity' in node) {
    const value = node.opacity;
    const validOpacity = (typeof value === 'number' && value >= 0 && value <= 1) || isVariableBindingString(value);
    if (!validOpacity) {
      warn(`node "${nodeLabel(node)}" has invalid opacity value (expected number 0..1 or variable binding string, got ${describeType(value)})`);
    }
  }

  if ('rotation' in node) {
    const value = node.rotation;
    const validRotation = typeof value === 'number' || isVariableBindingString(value);
    if (!validRotation) {
      warn(`node "${nodeLabel(node)}" has invalid rotation value (expected number or variable binding string, got ${describeType(value)})`);
    }
  }

  collectVariablesFromValue(node, p);

  if ('children' in node && !Array.isArray(node.children)) fail(`${p}.children must be array`);
  if (Array.isArray(node.children)) {
    node.children.forEach((c, i) => walk(c, `${p}.children[${i}]`, node));
  }
}

data.children.forEach((n, i) => walk(n, `children[${i}]`));

function validateRefs(node, p='root') {
  if (node && typeof node === 'object') {
    if (node.type === 'ref') {
      if (typeof node.ref !== 'string' || !node.ref.trim()) {
        fail(`${p}.ref must be non-empty string`);
      }
      if (!reusableIds.has(node.ref)) {
        fail(`${p} references missing reusable component: '${node.ref}'`);
      }
    }
    if (Array.isArray(node.children)) {
      node.children.forEach((c, i) => validateRefs(c, `${p}.children[${i}]`));
    }
  }
}

data.children.forEach((n, i) => validateRefs(n, `children[${i}]`));


// Theme consistency check
const themes = data.themes || {};
const variables = data.variables || {};
for (const [varName, varDef] of Object.entries(variables)) {
  if (Array.isArray(varDef.value)) {
    for (const entry of varDef.value) {
      if (entry.theme) {
        for (const [axis, val] of Object.entries(entry.theme)) {
          if (!themes[axis]) {
            warn(`Variable "${varName}" references undeclared theme axis "${axis}"`);
          } else if (!themes[axis].includes(val)) {
            warn(`Variable "${varName}" references undeclared theme value "${axis}:${val}"`);
          }
        }
      }
    }
  }
}


console.log(`✅ validate-pen pass: ${file}`);
