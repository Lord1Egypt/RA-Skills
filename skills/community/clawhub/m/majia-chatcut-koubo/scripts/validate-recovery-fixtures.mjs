#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

import Ajv2020 from "ajv/dist/2020.js";
import addFormats from "ajv-formats";

import {
  FakeTimelineAdapter,
  RecoverableExecutor,
} from "../src/execution/recoverable-executor.mjs";

const ROOT = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
);

function readJson(relativePath) {
  try {
    return JSON.parse(fs.readFileSync(path.join(ROOT, relativePath), "utf8"));
  } catch {
    throw new Error("EXEC_FIXTURE_READ_FAILED");
  }
}

function createValidators() {
  const ajv = new Ajv2020({
    allErrors: true,
    logger: false,
    strict: true,
    strictRequired: false,
  });
  addFormats(ajv);
  for (const name of [
    "creator-os-common.schema.json",
    "execution-plan.schema.json",
    "operation-journal.schema.json",
    "evidence-manifest.schema.json",
  ]) {
    ajv.addSchema(readJson(`schemas/${name}`));
  }
  return {
    plan: ajv.getSchema(
      "https://github.com/maojiebc/majia-chatcut-koubo/schemas/execution-plan.schema.json",
    ),
    journal: ajv.getSchema(
      "https://github.com/maojiebc/majia-chatcut-koubo/schemas/operation-journal.schema.json",
    ),
    evidence: ajv.getSchema(
      "https://github.com/maojiebc/majia-chatcut-koubo/schemas/evidence-manifest.schema.json",
    ),
  };
}

function requireCondition(condition, code) {
  if (!condition) throw new Error(code);
}

function runScenario(plan, validate, configuration) {
  const adapter = new FakeTimelineAdapter();
  for (const [operationId, type] of configuration.failures ?? []) {
    adapter.injectFailure(operationId, type);
  }
  const executor = new RecoverableExecutor(adapter);
  const result = executor.execute({
    executionPlan: plan,
    approvalReport: {canExecute: true},
  });
  requireCondition(
    result.status === configuration.expectedStatus,
    "EXEC_FIXTURE_STATUS_MISMATCH",
  );
  requireCondition(
    validate.journal(result.journal),
    "EXEC_FIXTURE_JOURNAL_INVALID",
  );
  requireCondition(
    validate.evidence(result.evidenceManifest),
    "EXEC_FIXTURE_EVIDENCE_INVALID",
  );
  configuration.inspect?.(result, adapter, executor);
  return result;
}

try {
  const plan = readJson("fixtures/execution/valid/execution-plan.json");
  const validate = createValidators();
  requireCondition(validate.plan(plan), "EXEC_FIXTURE_PLAN_INVALID");
  let checks = 0;
  const complete = (configuration = {}) => {
    checks += 1;
    return runScenario(plan, validate, {
      expectedStatus: "completed",
      ...configuration,
    });
  };
  const fail = (configuration) => {
    checks += 1;
    return runScenario(plan, validate, {
      expectedStatus: "failed",
      ...configuration,
    });
  };

  complete();
  complete({
    failures: [["operation_001", "timeout-before-commit"]],
    inspect: (result) => requireCondition(
      result.journal.entries[0].reconciliation === "retry",
      "EXEC_FIXTURE_RETRY_MISSING",
    ),
  });
  complete({
    failures: [["operation_001", "timeout-after-commit"]],
    inspect: (result) => requireCondition(
      result.journal.entries[0].reconciliation === "readback",
      "EXEC_FIXTURE_READBACK_MISSING",
    ),
  });
  complete({
    failures: [["operation_001", "id-change"]],
  });
  fail({
    failures: [["operation_001", "partial-write"]],
    inspect: (result, adapter) => {
      requireCondition(
        result.errorCode === "EXEC_POSTCONDITION_FAILED",
        "EXEC_FIXTURE_PARTIAL_NOT_DETECTED",
      );
      requireCondition(
        adapter.objectCount() === 0,
        "EXEC_FIXTURE_SCENE_NOT_COMPENSATED",
      );
    },
  });
  fail({
    failures: [["operation_001", "revision-drift"]],
    inspect: (result) => requireCondition(
      result.errorCode === "EXEC_REVISION_DRIFT",
      "EXEC_FIXTURE_REVISION_NOT_DETECTED",
    ),
  });

  checks += 1;
  const resumeAdapter = new FakeTimelineAdapter();
  const resumeExecutor = new RecoverableExecutor(resumeAdapter);
  resumeAdapter.injectFailure("operation_002", "partial-write");
  const interrupted = resumeExecutor.execute({
    executionPlan: plan,
    approvalReport: {canExecute: true},
  });
  const resumed = resumeExecutor.execute({
    executionPlan: plan,
    approvalReport: {canExecute: true},
    journal: interrupted.journal,
    evidenceManifest: interrupted.evidenceManifest,
  });
  requireCondition(resumed.status === "completed", "EXEC_FIXTURE_RESUME_FAILED");
  requireCondition(validate.journal(resumed.journal), "EXEC_FIXTURE_JOURNAL_INVALID");
  requireCondition(
    validate.evidence(resumed.evidenceManifest),
    "EXEC_FIXTURE_EVIDENCE_INVALID",
  );

  process.stdout.write(
    `recovery fixture audit passed: ${checks} scenario(s)\n`,
  );
} catch (error) {
  const code = typeof error?.message === "string"
    && /^EXEC_[A-Z0-9_]+$/u.test(error.message)
    ? error.message
    : "EXEC_FIXTURE_AUDIT_FAILED";
  process.stderr.write(`${code}: recovery fixture audit failed\n`);
  process.exitCode = 1;
}
