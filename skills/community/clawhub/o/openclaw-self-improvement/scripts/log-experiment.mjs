#!/usr/bin/env node
import fs from 'fs';
import path from 'path';

const [,, target, baseline = '', mutation = '', evalsRaw = '', result = '', decision = 'testing'] = process.argv;
if (!target) {
  console.error('Usage: node log-experiment.mjs <target> [baseline] [mutation] [eval1|eval2|eval3] [result] [decision]');
  process.exit(2);
}

const workspace = process.env.WORKSPACE || path.join(process.env.HOME, '.openclaw/workspace');
const dir = path.join(workspace, '.learnings');
fs.mkdirSync(dir, { recursive: true });
const file = path.join(dir, 'EXPERIMENTS.md');
const now = new Date();
const iso = now.toISOString();
const ymd = iso.slice(0,10).replace(/-/g,'');
const id = `EXP-${ymd}-${Math.random().toString(36).slice(2,5).toUpperCase()}`;
const evals = evalsRaw ? evalsRaw.split('|').map(s => s.trim()).filter(Boolean) : [];
const evalBlock = evals.length
  ? evals.map(e => `- [ ] ${e}`).join('\n')
  : '- [ ] Define binary evals';
const normalizedDecision = ['baseline','testing','keep','discard','partial_keep'].includes(decision) ? decision : 'testing';

const block = [
  `## [${id}] experiment`,
  '',
  `**Logged**: ${iso}`,
  `**Priority**: medium`,
  `**Status**: ${normalizedDecision}`,
  `**Area**: ops`,
  '',
  '### Target',
  target,
  '',
  '### Baseline',
  baseline || '(none recorded)',
  '',
  '### Mutation',
  mutation || '(none recorded)',
  '',
  '### Binary Evals',
  evalBlock,
  '',
  '### Result',
  result || '(pending)',
  '',
  '### Keep or Discard',
  normalizedDecision,
  '',
  '### Metadata',
  '- Source: manual',
  '- Related Files:',
  '- Tags:',
  '',
  '---',
  ''
].join('\n');

fs.appendFileSync(file, block);
console.log(file);
console.log(id);
