#!/usr/bin/env node
import { readFileSync } from 'fs';
import {
  assertDomainFrontDoor,
  assertTaskFrontDoor,
  buildSubagentSpawnPlan,
  getCanonicalDomainFrontDoor,
  getCanonicalTaskRunner,
} from '../../../lib/intent-router/policy.mjs';

function readJsonArg() {
  if (process.argv[2]) return JSON.parse(process.argv[2]);
  const stdin = readFileSync(0, 'utf8').trim();
  if (!stdin) throw new Error('expected JSON argument or stdin');
  return JSON.parse(stdin);
}

const input = readJsonArg();
const strict =
  Boolean(input.criticalWrite) ||
  input.taskClass === 'C' ||
  input.taskClass === 'D';

const canonicalTaskRunner = getCanonicalTaskRunner(input.taskName);
const canonicalDomainFrontDoor = getCanonicalDomainFrontDoor(input.domain);
const requestedFrontDoor = input.frontDoor || input.runner || null;

const taskFrontDoor = assertTaskFrontDoor({
  taskName: input.taskName,
  requestedRunner: requestedFrontDoor,
  failClosed: strict,
});
const domainFrontDoor = assertDomainFrontDoor({
  domain: input.domain || null,
  requestedFrontDoor,
  failClosed: strict,
});

const plan = buildSubagentSpawnPlan({
  taskName: input.taskName,
  taskClass: input.taskClass,
  requiresDeepReasoning: input.requiresDeepReasoning,
  deterministic: input.deterministic,
  criticalWrite: input.criticalWrite,
  domain: input.domain || null,
  prompt: input.prompt || '',
  label: input.label || null,
  notes: input.notes || '',
});

const out = {
  kind: 'governed-delegation-decision',
  input: {
    taskName: input.taskName || null,
    taskClass: input.taskClass || 'B',
    requiresDeepReasoning: Boolean(input.requiresDeepReasoning),
    deterministic: Boolean(input.deterministic),
    criticalWrite: Boolean(input.criticalWrite),
    domain: input.domain || null,
    label: input.label || null,
    frontDoor: requestedFrontDoor,
  },
  decision: {
    model: plan.model,
    failClosed: plan.failClosed,
    runtime: plan.runtime,
    policySource: plan.policy.source,
    preferredModel: plan.policy.preferredModel,
    runner: plan.policy.runner,
    notes: plan.notes || '',
    frontDoor: {
      task: {
        requested: taskFrontDoor.requestedRunner,
        canonical: canonicalTaskRunner,
        status: taskFrontDoor.reason,
      },
      domain: {
        requested: domainFrontDoor.requestedFrontDoor,
        canonical: canonicalDomainFrontDoor,
        status: domainFrontDoor.reason,
      },
    },
  },
  spawnRequest: {
    runtime: plan.runtime,
    model: plan.model,
    label: plan.label,
    task: plan.prompt,
    frontDoor: canonicalTaskRunner || canonicalDomainFrontDoor || null,
  },
};

console.log(JSON.stringify(out, null, 2));
