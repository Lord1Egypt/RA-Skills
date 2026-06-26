#!/usr/bin/env node

import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';
import { fileURLToPath } from 'node:url';
import Ajv from 'ajv';
import addFormats from 'ajv-formats';

const ROOT_DIR = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const STATE_SCHEMA_PATH = path.join(ROOT_DIR, 'schemas', 'state_schema.json');
const DEFAULT_STATE_PATH = path.join(ROOT_DIR, 'state.json');
const EXAMPLE_STATE_PATH = path.join(ROOT_DIR, 'examples', 'state.example.json');

function printUsage() {
  console.log('Usage: moltmotion-skill <command> [options]');
  console.log('');
  console.log('Commands:');
  console.log('  validate-state [--file <path>]   Validate state JSON against schemas/state_schema.json');
}

function parseJson(filePath, label) {
  if (!fs.existsSync(filePath)) {
    throw new Error(`${label} not found: ${filePath}`);
  }

  try {
    return JSON.parse(fs.readFileSync(filePath, 'utf8'));
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Unknown JSON parse error';
    throw new Error(`${label} parse error (${filePath}): ${message}`);
  }
}

function runValidateState(args) {
  const fileFlagIndex = args.indexOf('--file');
  let statePath;

  if (fileFlagIndex !== -1) {
    statePath = args[fileFlagIndex + 1];
    if (!statePath) {
      throw new Error('Missing value for --file');
    }
    statePath = path.resolve(process.cwd(), statePath);
  } else {
    statePath = fs.existsSync(DEFAULT_STATE_PATH) ? DEFAULT_STATE_PATH : EXAMPLE_STATE_PATH;
  }

  const schema = parseJson(STATE_SCHEMA_PATH, 'Schema');
  const state = parseJson(statePath, 'State file');

  const ajv = new Ajv({ allErrors: true, strict: false });
  addFormats(ajv);
  const validate = ajv.compile(schema);

  const valid = validate(state);
  if (!valid) {
    console.error('❌ state validation failed');
    for (const err of validate.errors || []) {
      console.error(`- ${err.instancePath || '/'}: ${err.message}`);
    }
    return 1;
  }

  console.log(`✅ state validation passed (${path.relative(ROOT_DIR, statePath)})`);
  return 0;
}

function main() {
  const [command, ...args] = process.argv.slice(2);

  if (!command || command === '--help' || command === '-h') {
    printUsage();
    return 0;
  }

  if (command === 'validate-state') {
    return runValidateState(args);
  }

  console.error(`Unknown command: ${command}`);
  printUsage();
  return 1;
}

process.exit(main());
