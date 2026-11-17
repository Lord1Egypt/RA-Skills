#!/usr/bin/env node
// Validate generated scenarios through the application's importer and simulation engine.
import { readFile, stat } from 'node:fs/promises';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const usage = 'Usage: node validate-config.mjs --repo <repo-root> <config.json> [--simulate] [--strict]';
const placeholder = /^\{\{\s*[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*\s*\}\}$/;
let repo, file, simulate = false, strict = false;
try {
  const args = process.argv.slice(2);
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === '--repo' && !repo && args[i + 1] && !args[i + 1].startsWith('--')) repo = args[++i];
    else if (arg === '--simulate') simulate = true;
    else if (arg === '--strict') strict = true;
    else if (!arg.startsWith('--') && !file) file = arg;
    else throw new Error(usage);
  }
  if (!repo || !file) throw new Error(usage);
  repo = resolve(repo);
  file = resolve(file);
  if ((await stat(file)).size > 4_000_000) throw new Error('File exceeds the web app import limit (4 MB)');

  // Use the application's parser; do not maintain a competing config schema.
  const src = name => pathToFileURL(resolve(repo, 'src', name)).href;
  const { readComparisonConfig, validateComparison, resolvePlanDescription } = await import(src('comparison.js'));
  const { descriptionReferences } = await import(src('plan-description.js'));
  const raw = JSON.parse(await readFile(file, 'utf8'));
  const template = raw?.type === 'token-lab-template'
    ? (await import(src('templates.js'))).readTemplate(raw)
    : null;
  const config = template ? template.config : readComparisonConfig(raw);
  const errors = validateComparison(config);
  if (Object.keys(errors).length) throw new Error(JSON.stringify(errors));

  const output = { valid: true, file, plans: config.plans.length, simulated: false };
  if (template) output.template = {
    version: template.version, name: template.name, description: template.description,
  };
  output.planDescriptions = config.plans.map(plan => {
    const description = plan.description ?? '';
    const rendered = resolvePlanDescription(plan, config.globalSimulation);
    const unresolvedVariables = descriptionReferences(rendered);
    const blocks = [...description.matchAll(/\{\{[\s\S]*?\}\}/g)].map(match => match[0]);
    const invalidPlaceholders = [...new Set(blocks.filter(block => !placeholder.test(block)))];
    const outside = description.replace(/\{\{[\s\S]*?\}\}/g, '');
    const unmatchedBraces = outside.includes('{{') || outside.includes('}}');
    return { id: plan.id, rendered, unresolvedVariables, invalidPlaceholders, unmatchedBraces };
  });
  output.warnings = output.planDescriptions.flatMap(plan => [
    ...(plan.unresolvedVariables.length
      ? ['Plan ' + plan.id + ' description contains unresolved variables: ' + plan.unresolvedVariables.join(', ')] : []),
    ...(plan.invalidPlaceholders.length
      ? ['Plan ' + plan.id + ' description contains unsupported placeholders: ' + plan.invalidPlaceholders.join(', ')] : []),
    ...(plan.unmatchedBraces
      ? ['Plan ' + plan.id + ' description contains unmatched double braces'] : []),
  ]);
  if (strict && output.warnings.length) throw new Error(output.warnings.join('\n'));

  if (simulate) {
    const { simulate: run } = await import(src('session-report.js'));
    output.results = run(config).map(result => ({
      id: result.planId, name: result.planName,
      model: result.model.name, currency: result.model.currency,
      totalCost: result.cost.total,
      estimateDuration: result.estimateDuration,
      averageTurnDurationSeconds: result.averageTurnDurationSeconds,
    }));
    output.simulated = true;
  }
  console.log(JSON.stringify(output, null, 2));
} catch (error) {
  console.error(JSON.stringify({ valid: false, error: error.message }, null, 2));
  process.exitCode = 1;
}
