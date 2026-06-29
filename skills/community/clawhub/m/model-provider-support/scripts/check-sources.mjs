#!/usr/bin/env node
import { readFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const skillDir = resolve(__dirname, '..');
const registryPath = resolve(skillDir, 'references/source-registry.json');
const skillPath = resolve(skillDir, 'SKILL.md');

function fail(message) {
  console.error(`check-sources: ${message}`);
  process.exitCode = 1;
}

function parseFrontmatter(text) {
  if (!text.startsWith('---\n')) throw new Error('missing opening frontmatter marker');
  const end = text.indexOf('\n---\n', 4);
  if (end === -1) throw new Error('missing closing frontmatter marker');
  const raw = text.slice(4, end).trim();
  const data = {};
  for (const line of raw.split('\n')) {
    const match = line.match(/^([A-Za-z0-9_-]+):\s*(.*)$/);
    if (!match) throw new Error(`unsupported frontmatter line: ${line}`);
    let value = match[2].trim();
    if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
      value = value.slice(1, -1);
    }
    data[match[1]] = value;
  }
  return data;
}

const skillText = await readFile(skillPath, 'utf8');
let frontmatter;
try {
  frontmatter = parseFrontmatter(skillText);
} catch (error) {
  fail(`invalid SKILL.md frontmatter: ${error.message}`);
}

if (frontmatter) {
  if (frontmatter.name !== 'model-provider-support') fail('frontmatter name must be model-provider-support');
  if (!frontmatter.description || frontmatter.description.length < 40) fail('frontmatter description is missing or too short');
}

let registry;
try {
  registry = JSON.parse(await readFile(registryPath, 'utf8'));
} catch (error) {
  fail(`invalid source registry JSON: ${error.message}`);
}

if (registry) {
  if (!Number.isInteger(registry.schemaVersion)) fail('schemaVersion must be an integer');
  if (!/^\d{4}-\d{2}-\d{2}$/.test(registry.lastReviewed || '')) fail('lastReviewed must be YYYY-MM-DD');
  if (!Array.isArray(registry.sources) || registry.sources.length === 0) fail('sources must be a non-empty array');

  const ids = new Set();
  const requiredNeedles = [
    'platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock',
    'platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai',
    'docs.aws.amazon.com/bedrock',
    'cloud.google.com/vertex-ai/generative-ai/docs/partner-models',
    'learn.microsoft.com/en-us/azure/ai-services/openai',
    'platform.openai.com/docs',
    'cloud.google.com/vertex-ai/generative-ai/docs/learn/models',
    'ai.google.dev/gemini-api/docs'
  ];

  const urls = [];
  for (const [index, source] of registry.sources.entries()) {
    const prefix = `sources[${index}]`;
    for (const field of ['id', 'provider', 'surface', 'officialUrl', 'sourceType', 'useFor', 'verificationRules']) {
      if (!(field in source)) fail(`${prefix} missing ${field}`);
    }
    if (ids.has(source.id)) fail(`duplicate source id: ${source.id}`);
    ids.add(source.id);
    try {
      const url = new URL(source.officialUrl);
      if (url.protocol !== 'https:') fail(`${source.id} officialUrl must use https`);
      urls.push(source.officialUrl);
    } catch {
      fail(`${source.id} officialUrl is not a valid URL`);
    }
    if (!Array.isArray(source.useFor) || source.useFor.length === 0) fail(`${source.id} useFor must be non-empty`);
    if (!Array.isArray(source.verificationRules) || source.verificationRules.length === 0) fail(`${source.id} verificationRules must be non-empty`);
  }

  for (const needle of requiredNeedles) {
    if (!urls.some((url) => url.includes(needle))) fail(`missing required official source matching ${needle}`);
  }
}

if (process.exitCode) process.exit(process.exitCode);
console.log(`ok: validated ${registry.sources.length} official source entries`);
