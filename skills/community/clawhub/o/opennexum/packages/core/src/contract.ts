import { readFile } from "node:fs/promises";
import { load as loadYaml } from "js-yaml";

import type {
  Contract,
  ContractDeliverable,
  ContractCriterion,
  ContractEvalStrategy,
  ContractScope,
  ContractType,
  EvalStrategyType
} from "./types";

export interface CriterionResult {
  id: string;
  passed: boolean;
  reason: string;
}

export interface EvalSummary {
  feedback: string;
  failedCriteria: string[];
  passCount: number;
  totalCount: number;
  criteriaResults: CriterionResult[];
}

const CONTRACT_TYPES = new Set<ContractType>(["coding", "task"]);
const EVAL_STRATEGY_TYPES = new Set<EvalStrategyType>([
  "unit",
  "integration",
  "review",
  "e2e",
  "composite"
]);

export async function parseContract(filePath: string): Promise<Contract> {
  const source = await readFile(filePath, "utf8");
  const parsed = loadYaml(source);

  const errors = validateContract(parsed);
  if (errors.length > 0) {
    throw new Error(`Invalid contract ${filePath}:\n- ${errors.join("\n- ")}`);
  }

  return normalizeContract(parsed as Record<string, unknown>);
}

export async function parseEvalResult(filePath: string): Promise<EvalSummary> {
  try {
    const content = await readFile(filePath, "utf8");
    const feedback = parseQuotedScalar(content.match(/^feedback:\s*(.+)$/m)?.[1]);
    const criteriaResults: CriterionResult[] = [];
    const failedCriteria: string[] = [];
    const criteriaBlocks = content.split(/\n\s*-\s*id:\s*/);

    for (const block of criteriaBlocks.slice(1)) {
      const idMatch = block.match(/^(\S+)/);
      const statusMatch = block.match(/^\s*(?:status|result):\s*(pass|fail)\s*$/m);
      const reason =
        parseQuotedScalar(block.match(/^\s*reason:\s*(.+)$/m)?.[1]) ||
        parseQuotedScalar(block.match(/^\s*evidence:\s*(.+)$/m)?.[1]) ||
        parseQuotedScalar(block.match(/^\s*detail:\s*(.+)$/m)?.[1]);

      if (!idMatch || !statusMatch) {
        continue;
      }

      const passed = statusMatch[1] === "pass";
      criteriaResults.push({ id: idMatch[1], passed, reason });

      if (!passed) {
        failedCriteria.push(idMatch[1]);
      }
    }

    const passCount =
      criteriaResults.length > 0
        ? criteriaResults.filter((result) => result.passed).length
        : [...content.matchAll(/(?:status|result):\s*pass/g)].length;
    const failCount =
      criteriaResults.length > 0
        ? criteriaResults.filter((result) => !result.passed).length
        : [...content.matchAll(/(?:status|result):\s*fail/g)].length;
    const totalCount = criteriaResults.length > 0 ? criteriaResults.length : passCount + failCount;

    return { feedback, failedCriteria, passCount, totalCount, criteriaResults };
  } catch {
    return { feedback: "", failedCriteria: [], passCount: 0, totalCount: 0, criteriaResults: [] };
  }
}

export function validateContract(contract: unknown): string[] {
  const errors: string[] = [];
  if (!isPlainObject(contract)) {
    return ["Contract root must be an object"];
  }

  const record = contract;

  requireString(record.id, "id", errors);
  requireString(record.name, "name", errors);

  if (record.type !== undefined) {
    requireEnum(record.type, "type", CONTRACT_TYPES, errors);
  }

  if (record.created_at !== undefined) {
    requireString(record.created_at, "created_at", errors);
  }

  if (record.batch !== undefined) {
    requireString(record.batch, "batch", errors);
  }

  if (record.description !== undefined) {
    requireString(record.description, "description", errors);
  }

  const agent = isPlainObject(record.agent) ? record.agent : undefined;
  const generator = firstNonEmptyString(record.generator, agent?.generator);
  const evaluator = firstNonEmptyString(record.evaluator, agent?.evaluator);

  if (!generator) {
    errors.push("Missing or invalid field: generator|agent.generator");
  }

  if (!evaluator) {
    errors.push("Missing or invalid field: evaluator|agent.evaluator");
  }

  if (typeof record.max_iterations !== "number") {
    errors.push("Missing or invalid field: max_iterations");
  }

  const scope = record.scope;
  if (!isPlainObject(scope)) {
    errors.push("Missing or invalid field: scope");
  } else {
    requireStringArray(scope.files, "scope.files", errors);
    if (scope.boundaries !== undefined) {
      requireStringArray(scope.boundaries, "scope.boundaries", errors);
    }
    if (scope.conflicts_with !== undefined) {
      requireStringArray(scope.conflicts_with, "scope.conflicts_with", errors);
    }
  }

  if (!Array.isArray(record.deliverables)) {
    errors.push("Missing or invalid field: deliverables");
  } else {
    record.deliverables.forEach((deliverable, index) => {
      if (typeof deliverable === "string") {
        if (deliverable.trim() === "") {
          errors.push(`Missing or invalid field: deliverables[${index}]`);
        }
        return;
      }

      if (!isPlainObject(deliverable)) {
        errors.push(`Invalid deliverable at deliverables[${index}]`);
        return;
      }

      const hasDescription =
        typeof deliverable.description === "string" && deliverable.description.trim() !== "";
      const hasPath = typeof deliverable.path === "string" && deliverable.path.trim() !== "";

      if (!hasDescription && !hasPath) {
        errors.push(
          `Missing or invalid field: deliverables[${index}].description|deliverables[${index}].path`
        );
      }

      if (deliverable.path !== undefined) {
        requireString(deliverable.path, `deliverables[${index}].path`, errors);
      }

      if (deliverable.description !== undefined) {
        requireString(deliverable.description, `deliverables[${index}].description`, errors);
      }
    });
  }

  if (record.depends_on !== undefined) {
    requireStringArray(record.depends_on, "depends_on", errors);
  }

  const evalStrategy = record.eval_strategy;
  if (!isPlainObject(evalStrategy)) {
    errors.push("Missing or invalid field: eval_strategy");
  } else {
    requireEnum(evalStrategy.type, "eval_strategy.type", EVAL_STRATEGY_TYPES, errors);

    if (!Array.isArray(evalStrategy.criteria)) {
      errors.push("Missing or invalid field: eval_strategy.criteria");
    } else {
      evalStrategy.criteria.forEach((criterion, index) => {
        if (!isPlainObject(criterion)) {
          errors.push(`Invalid criterion at eval_strategy.criteria[${index}]`);
          return;
        }

        requireString(criterion.id, `eval_strategy.criteria[${index}].id`, errors);
        requireString(criterion.desc, `eval_strategy.criteria[${index}].desc`, errors);
        if (criterion.method !== undefined) {
          requireString(criterion.method, `eval_strategy.criteria[${index}].method`, errors);
        }
        if (criterion.threshold !== undefined) {
          requireString(criterion.threshold, `eval_strategy.criteria[${index}].threshold`, errors);
        }
        if (criterion.weight !== undefined && typeof criterion.weight !== "number") {
          errors.push(`Missing or invalid field: eval_strategy.criteria[${index}].weight`);
        }
      });
    }
  }

  return errors;
}

function normalizeContract(record: Record<string, unknown>): Contract {
  const agent = normalizeAgent(record.agent);
  const generator = firstNonEmptyString(record.generator, agent?.generator) ?? "";
  const evaluator = firstNonEmptyString(record.evaluator, agent?.evaluator) ?? "";
  const scope = isPlainObject(record.scope) ? record.scope : {};
  const evalStrategy = isPlainObject(record.eval_strategy) ? record.eval_strategy : {};

  return {
    id: String(record.id).trim(),
    name: String(record.name).trim(),
    type: isContractType(record.type) ? record.type : "coding",
    created_at: optionalString(record.created_at),
    batch: optionalString(record.batch),
    description: optionalString(record.description),
    scope: {
      files: normalizeStringArray(scope.files),
      boundaries: normalizeStringArray(scope.boundaries),
      conflicts_with: normalizeStringArray(scope.conflicts_with)
    },
    deliverables: normalizeDeliverables(record.deliverables),
    eval_strategy: {
      type: isEvalStrategyType(evalStrategy.type) ? evalStrategy.type : "review",
      criteria: normalizeCriteria(evalStrategy.criteria)
    },
    generator,
    evaluator,
    ...(agent ? { agent } : {}),
    max_iterations: Number(record.max_iterations),
    depends_on: normalizeStringArray(record.depends_on)
  };
}

function normalizeAgent(value: unknown): Contract["agent"] | undefined {
  if (!isPlainObject(value)) {
    return undefined;
  }

  const generator = optionalString(value.generator);
  const evaluator = optionalString(value.evaluator);

  if (!generator && !evaluator) {
    return undefined;
  }

  return {
    ...(generator ? { generator } : {}),
    ...(evaluator ? { evaluator } : {})
  };
}

function normalizeDeliverables(value: unknown): ContractDeliverable[] {
  if (!Array.isArray(value)) {
    return [];
  }

  return value.map((deliverable) => {
    if (typeof deliverable === "string") {
      return { description: deliverable.trim() };
    }

    const record = isPlainObject(deliverable) ? deliverable : {};
    const path = optionalString(record.path);
    const description = optionalString(record.description) ?? path ?? "";

    return {
      ...(path ? { path } : {}),
      description
    };
  });
}

function normalizeCriteria(value: unknown): ContractCriterion[] {
  if (!Array.isArray(value)) {
    return [];
  }

  return value.map((criterion) => {
    const record = isPlainObject(criterion) ? criterion : {};

    return {
      id: String(record.id ?? "").trim(),
      desc: String(record.desc ?? "").trim(),
      ...(optionalString(record.method) ? { method: optionalString(record.method) } : {}),
      ...(optionalString(record.threshold)
        ? { threshold: optionalString(record.threshold) }
        : {}),
      ...(typeof record.weight === "number" ? { weight: record.weight } : {})
    };
  });
}

function parseQuotedScalar(raw: string | undefined): string {
  if (!raw) {
    return "";
  }

  return raw.trim().replace(/^["']|["']$/g, "");
}

function requireString(value: unknown, field: string, errors: string[]): void {
  if (typeof value !== "string" || value.trim() === "") {
    errors.push(`Missing or invalid field: ${field}`);
  }
}

function requireStringArray(value: unknown, field: string, errors: string[]): void {
  if (!Array.isArray(value) || !value.every((entry) => typeof entry === "string")) {
    errors.push(`Missing or invalid field: ${field}`);
  }
}

function requireEnum<T extends string>(
  value: unknown,
  field: string,
  allowed: Set<T>,
  errors: string[]
): void {
  if (typeof value !== "string" || !allowed.has(value as T)) {
    errors.push(`Missing or invalid field: ${field}`);
  }
}

function isPlainObject(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function optionalString(value: unknown): string | undefined {
  return typeof value === "string" && value.trim() !== "" ? value.trim() : undefined;
}

function firstNonEmptyString(...values: unknown[]): string | undefined {
  for (const value of values) {
    const normalized = optionalString(value);
    if (normalized) {
      return normalized;
    }
  }

  return undefined;
}

function normalizeStringArray(value: unknown): string[] {
  if (!Array.isArray(value)) {
    return [];
  }

  return value
    .filter((entry): entry is string => typeof entry === "string")
    .map((entry) => entry.trim())
    .filter((entry) => entry !== "");
}

function isContractType(value: unknown): value is ContractType {
  return typeof value === "string" && CONTRACT_TYPES.has(value as ContractType);
}

function isEvalStrategyType(value: unknown): value is EvalStrategyType {
  return typeof value === "string" && EVAL_STRATEGY_TYPES.has(value as EvalStrategyType);
}

export type {
  Contract,
  ContractCriterion,
  ContractDeliverable,
  ContractEvalStrategy,
  ContractScope
};
