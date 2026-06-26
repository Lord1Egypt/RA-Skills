#!/usr/bin/env node
import fs from 'fs';
import path from 'path';

const workspace = process.env.WORKSPACE || path.join(process.env.HOME, '.openclaw/workspace');
const file = path.join(workspace, '.learnings', 'EXPERIMENTS.md');
if (!fs.existsSync(file)) {
  console.error(`Missing experiments file: ${file}`);
  process.exit(1);
}

const text = fs.readFileSync(file, 'utf8');
const chunks = text.split(/^## \[(EXP-[^\]]+)\] experiment$/m);
const entries = [];
for (let i = 1; i < chunks.length; i += 2) {
  const id = chunks[i].trim();
  const body = chunks[i + 1] || '';
  const pick = (label) => {
    const re = new RegExp(`^### ${label}\\n([\\s\\S]*?)(?=\\n### |\\n---|$)`, 'm');
    const m = body.match(re);
    return m ? m[1].trim() : '';
  };
  const statusMatch = body.match(/\*\*Status\*\*: (.+)/);
  const loggedMatch = body.match(/\*\*Logged\*\*: (.+)/);
  const decision = pick('Keep or Discard') || (statusMatch ? statusMatch[1].trim() : 'unknown');
  entries.push({
    id,
    logged: loggedMatch ? loggedMatch[1].trim() : '',
    status: statusMatch ? statusMatch[1].trim() : 'unknown',
    target: pick('Target'),
    baseline: pick('Baseline'),
    mutation: pick('Mutation'),
    result: pick('Result'),
    decision
  });
}

const counts = { keep: 0, partial_keep: 0, discard: 0, baseline: 0, testing: 0, unknown: 0 };
for (const e of entries) counts[e.decision] = (counts[e.decision] || 0) + 1;
const partials = entries.filter(e => e.decision === 'partial_keep');

const out = {
  total: entries.length,
  counts,
  partialKeepNeedsFollowup: partials.map(e => ({
    id: e.id,
    logged: e.logged,
    target: e.target,
    result: e.result
  })),
  latest: entries.slice(-10)
};

console.log(JSON.stringify(out, null, 2));
