#!/usr/bin/env node
import fs from 'fs';
import os from 'os';
import path from 'path';

const args = process.argv.slice(2);
function getArg(name, fallback = undefined) {
  const idx = args.indexOf(name);
  if (idx === -1) return fallback;
  return args[idx + 1] ?? fallback;
}

const configPath = path.resolve(getArg('--config', path.join(os.homedir(), '.openclaw', 'openclaw.json')));
const findings = [];
const recommendations = [];
const evidence = { configPath };
let score = 100;

if (!fs.existsSync(configPath)) {
  findings.push({ level: 'HIGH', area: 'config', issue: 'OpenClaw config not found' });
  recommendations.push('Point the script at the real config path before trusting any cost assessment.');
  score -= 40;
  console.log(JSON.stringify({ score, verdict: 'FAIL', summary: 'Cost posture cannot be assessed without a config file.', findings, recommendations, guardrails: [], evidence }, null, 2));
  process.exit(1);
}

let cfg;
try {
  cfg = JSON.parse(fs.readFileSync(configPath, 'utf8'));
} catch (error) {
  findings.push({ level: 'HIGH', area: 'config', issue: 'OpenClaw config is not valid JSON' });
  recommendations.push('Repair the config file before performing budget governance.');
  score -= 35;
  console.log(JSON.stringify({ score, verdict: 'FAIL', summary: 'Cost posture cannot be assessed because the config is invalid.', findings, recommendations, guardrails: [], evidence: { ...evidence, parseError: String(error) } }, null, 2));
  process.exit(1);
}

const serialized = JSON.stringify(cfg, null, 2);
const budgetHints = [
  cfg?.ai?.monthlyBudget,
  cfg?.ai?.dailyLimit,
  cfg?.limits?.monthlyBudget,
  cfg?.limits?.dailyBudget,
  cfg?.budget?.monthly,
  cfg?.budget?.daily
].filter((v) => v != null);

evidence.budgetHints = budgetHints;
if (budgetHints.length === 0) {
  findings.push({ level: 'HIGH', area: 'budget', issue: 'no explicit budget fields detected' });
  recommendations.push('Set daily/monthly budget or usage caps before scaling agents or cron jobs.');
  score -= 20;
}

const expensivePatterns = [
  /opus/i,
  /gpt-5/i,
  /gpt-4\.1/i,
  /o1/i,
  /sonnet-4/i,
  /gemini-2\.5-pro/i,
  /claude-3-opus/i
];
const matchedExpensive = expensivePatterns.filter((re) => re.test(serialized)).map((re) => re.source);
evidence.expensiveModelSignals = matchedExpensive;
if (matchedExpensive.length > 0) {
  findings.push({ level: 'MEDIUM', area: 'model-defaults', issue: 'premium-model signals detected in config' });
  recommendations.push('Reserve premium models for explicit escalation paths instead of routine defaults.');
  score -= Math.min(18, 6 + matchedExpensive.length * 2);
}

const maxTokenMatches = [...serialized.matchAll(/"max(?:Output)?Tokens"\s*:\s*(\d+)/g)].map((m) => Number(m[1]));
const maxToken = maxTokenMatches.length ? Math.max(...maxTokenMatches) : null;
evidence.maxTokenSignals = maxTokenMatches;
if (maxToken != null && maxToken >= 16000) {
  findings.push({ level: 'MEDIUM', area: 'token-limits', issue: `very large token ceiling detected (${maxToken})` });
  recommendations.push('Reduce global token ceilings for routine jobs; large outputs quietly multiply cost.');
  score -= 10;
}

if (/chrome-relay|existing-session|browser|playwright/i.test(serialized)) {
  findings.push({ level: 'WARN', area: 'interactive-workflows', issue: 'browser or interactive workflow capability detected' });
  recommendations.push('Use browser-based flows only when API/script options are insufficient; interactive runs are cost-amplifying.');
  score -= 6;
}

if (/cron/i.test(serialized) && budgetHints.length === 0) {
  findings.push({ level: 'MEDIUM', area: 'recurring-work', issue: 'cron-like automation signal detected without obvious budget guardrails' });
  recommendations.push('Review recurring jobs and assign a budget owner before increasing schedule frequency.');
  score -= 8;
}

if (/reasoning|thinking|verbose/i.test(serialized)) {
  findings.push({ level: 'LOW', area: 'verbosity', issue: 'reasoning/thinking/verbose signals present' });
  recommendations.push('Keep higher-think or verbose settings off for routine background tasks unless they are earning their cost.');
  score -= 4;
}

const guardrails = [
  'Define a monthly ceiling and a daily kill-threshold.',
  'Downgrade the default model for routine jobs; escalate only on failure or high-value tasks.',
  'Audit recurring cron jobs separately because small per-run waste compounds fast.',
  'Prefer scripts and APIs over browser-based agent loops when possible.',
  'Track one human owner for every recurring automated spend source.'
];

let verdict = 'PASS';
if (score < 60 || findings.some((f) => f.level === 'HIGH')) verdict = 'FAIL';
else if (score < 85 || findings.some((f) => f.level === 'MEDIUM' || f.level === 'WARN')) verdict = 'WARN';

const summary = verdict === 'PASS'
  ? 'Config looks broadly cost-aware in this lightweight pass.'
  : verdict === 'WARN'
    ? 'Cost risk is present; tighten guardrails before scaling.'
    : 'Denial-of-wallet risk is materially elevated; add budget controls before wider rollout.';

console.log(JSON.stringify({ score, verdict, summary, findings, recommendations, guardrails, evidence }, null, 2));
process.exit(verdict === 'FAIL' ? 1 : 0);
