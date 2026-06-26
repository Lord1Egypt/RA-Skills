#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const workspaceRoot = process.argv[2] || '/Users/m1/.openclaw/workspace';
const evalsPath = path.join(workspaceRoot, 'skills', 'openclaw-self-improvement', 'routing-evals.json');
const reportPath = path.join(workspaceRoot, '.learnings', 'skill-health-report.json');

const evals = JSON.parse(fs.readFileSync(evalsPath, 'utf8'));

function extractTriggerPhrases(description) {
  const phrases = [];
  const lower = description.toLowerCase();
  const patterns = [
    /"([^"]+)"/g,
    /'([^']+)'/g,
    /use when[^.]+/g,
    /should be used when[^.]+/g,
    /triggers?[^:]*:\s*([^\n]+)/g,
  ];
  for (const pattern of patterns) {
    let m;
    while ((m = pattern.exec(lower))) {
      const text = m[1] || m[0];
      if (text.length > 3) phrases.push(text.replace(/\.$/, '').trim());
    }
  }
  return phrases;
}

function scoreSkill(input, skill) {
  const inputLower = input.toLowerCase();
  const desc = `${skill.name || ''} ${skill.description || ''}`.toLowerCase();
  let score = 0;
  const inputWords = new Set(inputLower.split(/[^a-z0-9]+/).filter(Boolean));

  // Name match
  const nameWords = (skill.name || '').toLowerCase().split(/[^a-z0-9]+/).filter(Boolean);
  for (const word of nameWords) {
    if (inputLower.includes(word)) score += 3;
  }

  // Trigger phrase match
  const phrases = extractTriggerPhrases(skill.description || '');
  for (const phrase of phrases) {
    const phraseWords = phrase.split(/[^a-z0-9]+/).filter(Boolean);
    let hits = 0;
    for (const word of phraseWords) {
      if (inputLower.includes(word)) hits += 1;
    }
    const ratio = hits / phraseWords.length;
    if (ratio >= 0.5) {
      score += ratio * 5;
    }
  }

  // Description keyword overlap
  const descWords = desc.split(/[^a-z0-9]+/).filter(Boolean);
  const descSet = new Set(descWords);
  let overlap = 0;
  for (const word of inputWords) {
    if (descSet.has(word)) overlap += 1;
  }
  if (inputWords.size > 0) {
    score += (overlap / inputWords.size) * 2;
  }

  // Special bonus for exact action words
  const actionBonuses = {
    'debug': ['investigate', 'openclaw-investigate'],
    'brainstorm': ['office-hours', 'openclaw-office-hours'],
    'startup idea': ['office-hours', 'openclaw-office-hours'],
    'create skill': ['skill-creator'],
    'update the docs': ['document-release'],
    'post-ship': ['document-release'],
    'sync documentation': ['document-release'],
    'audit content': ['content-quality-auditor'],
    'write blog': ['content-writer'],
    'blog post': ['content-writer'],
    'ClawLite': ['content-writer'],
    'daily marketing': ['daily-marketing-operating-system'],
    'retro': ['retro'],
  };
  for (const [keyword, bonusIds] of Object.entries(actionBonuses)) {
    if (inputLower.includes(keyword) && bonusIds.includes(skill.id)) {
      score += 8;
    }
  }

  return score;
}

function routeInput(input, skills) {
  let best = null;
  let bestScore = 0;
  for (const skill of skills) {
    const score = scoreSkill(input, skill);
    if (score > bestScore) {
      bestScore = score;
      best = skill;
    }
  }
  return best ? best.id : null;
}

const report = JSON.parse(fs.readFileSync(reportPath, 'utf8'));
const skills = report.skills || [];

const results = [];
let pass = 0;
let fail = 0;

for (const evalCase of evals) {
  const routed = routeInput(evalCase.input, skills);
  const shouldHit = evalCase.shouldTrigger.includes(routed);
  const shouldNotHit = evalCase.shouldNotTrigger.includes(routed);
  const status = shouldHit && !shouldNotHit ? 'PASS' : 'FAIL';
  if (status === 'PASS') pass += 1;
  else fail += 1;
  results.push({
    id: evalCase.id,
    input: evalCase.input,
    routed,
    expected: evalCase.shouldTrigger,
    forbidden: evalCase.shouldNotTrigger,
    status,
    note: evalCase.note,
  });
}

const summary = {
  generatedAt: new Date().toISOString(),
  total: evals.length,
  pass,
  fail,
  passRate: evals.length ? Number(((pass / evals.length) * 100).toFixed(1)) : 0,
  results,
};

const outPath = path.join(workspaceRoot, '.learnings', 'routing-eval-report.json');
fs.mkdirSync(path.dirname(outPath), { recursive: true });
fs.writeFileSync(outPath, JSON.stringify(summary, null, 2));
console.log(JSON.stringify(summary, null, 2));
