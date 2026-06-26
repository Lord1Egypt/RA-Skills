#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const workspaceRoot = process.argv[2] || '/Users/m1/.openclaw/workspace';
const learningDir = path.join(workspaceRoot, '.learnings');
const reportPath = path.join(learningDir, 'skill-health-report.json');
const evalPath = path.join(learningDir, 'routing-eval-report.json');
const historyPath = path.join(learningDir, 'skill-health-history.json');
const summaryPath = path.join(learningDir, 'daily-skill-health-summary.txt');

async function main() {
  const { execSync } = await import('node:child_process');

  // Run health check
  execSync(`node ${path.join(workspaceRoot, 'skills/openclaw-self-improvement/scripts/skill-health-check.mjs')} ${workspaceRoot}`, { encoding: 'utf8' });

  // Run eval
  execSync(`node ${path.join(workspaceRoot, 'skills/openclaw-self-improvement/scripts/routing-eval-runner.mjs')} ${workspaceRoot}`, { encoding: 'utf8' });

  const report = JSON.parse(fs.readFileSync(reportPath, 'utf8'));
  const evalReport = JSON.parse(fs.readFileSync(evalPath, 'utf8'));

  let previous = null;
  if (fs.existsSync(historyPath)) {
    previous = JSON.parse(fs.readFileSync(historyPath, 'utf8'));
  }

  const deltas = [];
  if (previous) {
    if (report.duplicatePairs !== previous.duplicatePairs) {
      deltas.push(`Duplicate pairs: ${previous.duplicatePairs} → ${report.duplicatePairs}`);
    }
    if (report.darkSkills !== previous.darkSkills) {
      deltas.push(`Dark skills: ${previous.darkSkills} → ${report.darkSkills}`);
    }
    if (report.totalSkills !== previous.totalSkills) {
      deltas.push(`Total skills: ${previous.totalSkills} → ${report.totalSkills}`);
    }
    if (evalReport.passRate !== previous.passRate) {
      deltas.push(`Eval pass rate: ${previous.passRate}% → ${evalReport.passRate}%`);
    }
  }

  const summary = `OpenClaw Skill Self Improvement — Daily Health Summary
Generated: ${new Date().toISOString()}

Health Check
- Total skills: ${report.totalSkills}
- Duplicate pairs: ${report.duplicatePairs}
- Dark skills: ${report.darkSkills}
- Stale skills: ${report.staleSkills || 0}

Routing Eval
- Cases: ${evalReport.total}
- Pass: ${evalReport.pass}/${evalReport.total} (${evalReport.passRate}%)

${deltas.length ? 'Changes since last run:\n' + deltas.map((d) => '- ' + d).join('\n') : 'No significant changes since last run.'}

${report.recommendedActions?.length ? 'Recommended actions:\n' + report.recommendedActions.map((a) => '- ' + a).join('\n') : ''}
`;

  fs.writeFileSync(summaryPath, summary);
  fs.writeFileSync(historyPath, JSON.stringify({
    date: new Date().toISOString(),
    totalSkills: report.totalSkills,
    duplicatePairs: report.duplicatePairs,
    darkSkills: report.darkSkills,
    passRate: evalReport.passRate,
  }, null, 2));

  console.log(summary);
}

main().catch((err) => {
  console.error('Daily heartbeat failed:', err.message);
  process.exit(1);
});
