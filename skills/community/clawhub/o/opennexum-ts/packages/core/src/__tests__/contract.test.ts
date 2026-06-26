import assert from "node:assert/strict";
import { mkdtemp, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import test from "node:test";

import { parseContract, validateContract } from "../contract";

const FIXTURE_CONTRACT_PATH = path.resolve(
  path.dirname(new URL(import.meta.url).pathname),
  "../../../../docs/nexum/contracts/NX-001.yaml"
);

test("parseContract parses an existing contract file", async () => {
  const contract = await parseContract(FIXTURE_CONTRACT_PATH);

  assert.equal(contract.id, "NX-001");
  assert.equal(contract.type, "coding");
  assert.equal(contract.scope.files[0], "pnpm-workspace.yaml");
  assert.equal(contract.eval_strategy.criteria[0].id, "C1");
  assert.equal(validateContract(contract).length, 0);
});

test("validateContract reports missing required fields", async () => {
  const directory = await mkdtemp(path.join(tmpdir(), "nexum-contract-"));
  const contractPath = path.join(directory, "missing-fields.yaml");

  await writeFile(
    contractPath,
    [
      "id: NX-MISSING",
      "type: coding",
      "created_at: \"2026-03-29T04:00:00Z\"",
      "scope:",
      "  files: []",
      "  boundaries: []",
      "  conflicts_with: []",
      "deliverables: []",
      "eval_strategy:",
      "  type: unit",
      "  criteria: []",
      "generator: codex-1",
      "evaluator: eval",
      "max_iterations: 3",
      "depends_on: []",
      ""
    ].join("\n"),
    "utf8"
  );

  const contract = await parseContract(contractPath);
  const errors = validateContract(contract);

  assert.ok(errors.includes("Missing or invalid field: name"));
});

test("validateContract rejects unknown eval_strategy.type", async () => {
  const directory = await mkdtemp(path.join(tmpdir(), "nexum-contract-"));
  const contractPath = path.join(directory, "invalid-eval.yaml");

  await writeFile(
    contractPath,
    [
      "id: NX-BAD-EVAL",
      "name: \"Bad Eval Strategy\"",
      "type: coding",
      "created_at: \"2026-03-29T04:00:00Z\"",
      "scope:",
      "  files: []",
      "  boundaries: []",
      "  conflicts_with: []",
      "deliverables: []",
      "eval_strategy:",
      "  type: smoke",
      "  criteria:",
      "    - id: C1",
      "      desc: \"desc\"",
      "      method: \"method\"",
      "      threshold: pass",
      "generator: codex-1",
      "evaluator: eval",
      "max_iterations: 3",
      "depends_on: []",
      ""
    ].join("\n"),
    "utf8"
  );

  const contract = await parseContract(contractPath);
  const errors = validateContract(contract);

  assert.ok(errors.includes("Missing or invalid field: eval_strategy.type"));
});
