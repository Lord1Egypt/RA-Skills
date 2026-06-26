#!/usr/bin/env node
import { readFileSync } from 'fs';
import { dirname, resolve } from 'path';
import { fileURLToPath } from 'url';
import { spawnSync } from 'child_process';

const __dirname = dirname(fileURLToPath(import.meta.url));
const workspaceRoot = resolve(__dirname, '../../..');
const fitbitTools = resolve(workspaceRoot, 'fitbit-connector/scripts/fitbit_tools.py');

function readJsonInput() {
  if (process.argv[2]) return JSON.parse(process.argv[2]);
  const stdin = readFileSync(0, 'utf8').trim();
  if (!stdin) throw new Error('expected JSON input argument or stdin');
  return JSON.parse(stdin);
}

function toInt(value, fallback) {
  if (value === undefined || value === null || value === '') return fallback;
  const n = Number(value);
  if (!Number.isFinite(n) || n <= 0) throw new Error(`invalid positive integer: ${value}`);
  return Math.floor(n);
}

function buildArgs(input) {
  const action = String(input.action || '').trim();
  if (!action) throw new Error('missing required field: action');

  const ensureFresh = input.ensureFresh !== undefined ? Boolean(input.ensureFresh) : true;

  switch (action) {
    case 'auth_status':
      return ['auth-status'];

    case 'latest_recovery': {
      const days = toInt(input.days, 3);
      const metrics = input.metrics || 'hrv_rmssd,resting_hr,sleep_minutes,sleep_score,data_quality';
      const args = ['fetch-latest', '--days', String(days), '--metrics', metrics];
      if (ensureFresh) args.push('--ensure-fresh');
      return args;
    }

    case 'quality_flags': {
      const days = toInt(input.days, 7);
      return ['quality-flags', '--days', String(days)];
    }

    case 'training_status': {
      const days = toInt(input.days, 14);
      const args = ['training-health-status', '--days', String(days)];
      if (ensureFresh) args.push('--ensure-fresh');
      return args;
    }

    case 'training_window': {
      const days = toInt(input.days, 14);
      const args = ['training-health-window', '--days', String(days)];
      if (ensureFresh) args.push('--ensure-fresh');
      return args;
    }

    case 'unified_latest': {
      const days = toInt(input.days, 14);
      const source = String(input.source || 'best').trim();
      return ['unified-fetch-latest', '--days', String(days), '--source', source];
    }

    default:
      throw new Error(`unsupported action: ${action}`);
  }
}

function runFitbitTools(args) {
  const proc = spawnSync('python3', [fitbitTools, ...args], {
    cwd: workspaceRoot,
    encoding: 'utf8',
    env: process.env,
    maxBuffer: 5 * 1024 * 1024,
  });

  if (proc.error) throw proc.error;

  const stdout = (proc.stdout || '').trim();
  const stderr = (proc.stderr || '').trim();

  if (proc.status !== 0) {
    throw new Error(`fitbit_tools failed (${proc.status}): ${stderr || stdout || 'no output'}`);
  }

  try {
    return stdout ? JSON.parse(stdout) : { ok: true };
  } catch {
    return { ok: true, raw: stdout };
  }
}

try {
  const input = readJsonInput();
  const args = buildArgs(input);
  const result = runFitbitTools(args);

  const out = {
    kind: 'health-training-frontdoor-result',
    input: {
      action: input.action,
      days: input.days ?? null,
      ensureFresh: input.ensureFresh ?? null,
      source: input.source ?? null,
    },
    backend: {
      tool: 'fitbit_tools.py',
      command: ['python3', 'fitbit-connector/scripts/fitbit_tools.py', ...args],
    },
    result,
  };

  console.log(JSON.stringify(out, null, 2));
} catch (error) {
  console.error(error?.stack || String(error));
  process.exit(1);
}
