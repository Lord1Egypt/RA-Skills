#!/usr/bin/env node
import fs from 'fs';
import path from 'path';

const [,, kind, summary, details = '', suggested = ''] = process.argv;
if (!kind || !summary) {
  console.error('Usage: node log-learning.mjs <learning|error|feature> <summary> [details] [suggested_action]');
  process.exit(2);
}
const workspace = process.env.WORKSPACE || path.join(process.env.HOME, '.openclaw/workspace');
const dir = path.join(workspace, '.learnings');
fs.mkdirSync(dir, { recursive: true });
const map = {
  learning: { file: 'LEARNINGS.md', prefix: 'LRN', header: 'learning', area: 'workflow' },
  error: { file: 'ERRORS.md', prefix: 'ERR', header: 'error', area: 'ops' },
  feature: { file: 'FEATURE_REQUESTS.md', prefix: 'FEAT', header: 'feature', area: 'product' },
  experiment: { file: 'EXPERIMENTS.md', prefix: 'EXP', header: 'experiment', area: 'ops' }
};
const cfg = map[kind];
if (!cfg) {
  console.error('kind must be one of: learning, error, feature');
  process.exit(2);
}
const now = new Date();
const d = now.toISOString();
const ymd = d.slice(0,10).replace(/-/g,'');
const id = `${cfg.prefix}-${ymd}-${Math.random().toString(36).slice(2,5).toUpperCase()}`;
const file = path.join(dir, cfg.file);
const block = [`## [${id}] ${cfg.header}`,'',`**Logged**: ${d}`,`**Priority**: medium`,`**Status**: pending`,`**Area**: ${cfg.area}`,'',`### Summary`,summary,'',cfg.prefix==='ERR' ? '### Error' : cfg.prefix==='FEAT' ? '### User Context' : '### Details',details || '(none)','',`### Suggested Action`,suggested || '(none)','',`### Metadata`,`- Source: manual`,`- Related Files:`,`- Tags:`, '', '---', ''].join('\n');
fs.appendFileSync(file, block);
console.log(file);
console.log(id);
