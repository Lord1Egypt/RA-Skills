import { readFile } from "node:fs/promises";

import type {
  Contract,
  ContractCriterion,
  ContractEvalStrategy,
  ContractScope,
  ContractType,
  EvalStrategyType
} from "./types";

type YamlValue = string | number | boolean | null | YamlValue[] | YamlObject;

interface YamlObject {
  [key: string]: YamlValue;
}

interface ParsedLine {
  indent: number;
  lineNumber: number;
  text: string;
}

const CONTRACT_TYPES = new Set<ContractType>(["coding", "task", "creative"]);
const EVAL_STRATEGY_TYPES = new Set<EvalStrategyType>([
  "unit",
  "integration",
  "review"
]);

export async function parseContract(filePath: string): Promise<Contract> {
  const source = await readFile(filePath, "utf8");
  const parsed = parseYaml(source);

  if (!isPlainObject(parsed)) {
    throw new Error(`Contract root must be an object: ${filePath}`);
  }

  return parsed as unknown as Contract;
}

export function validateContract(contract: Contract): string[] {
  const errors: string[] = [];
  const record = contract as unknown as Record<string, unknown>;

  requireString(record.id, "id", errors);
  requireString(record.name, "name", errors);
  requireEnum(record.type, "type", CONTRACT_TYPES, errors);
  requireString(record.created_at, "created_at", errors);
  requireString(record.generator, "generator", errors);
  requireString(record.evaluator, "evaluator", errors);

  if (typeof record.max_iterations !== "number") {
    errors.push("Missing or invalid field: max_iterations");
  }

  const scope = record.scope;
  if (!isPlainObject(scope)) {
    errors.push("Missing or invalid field: scope");
  } else {
    requireStringArray(scope.files, "scope.files", errors);
    requireStringArray(scope.boundaries, "scope.boundaries", errors);
    requireStringArray(scope.conflicts_with, "scope.conflicts_with", errors);
  }

  requireStringArray(record.deliverables, "deliverables", errors);
  requireStringArray(record.depends_on, "depends_on", errors);

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
        requireString(criterion.method, `eval_strategy.criteria[${index}].method`, errors);
        requireString(criterion.threshold, `eval_strategy.criteria[${index}].threshold`, errors);
      });
    }
  }

  return errors;
}

function parseYaml(source: string): YamlValue {
  const lines = tokenize(source);

  if (lines.length === 0) {
    return {};
  }

  const state = { index: 0, lines };
  const root = parseBlock(state, lines[0].indent);

  if (state.index !== lines.length) {
    const line = lines[state.index];
    throw new Error(`Unexpected content at line ${line.lineNumber}`);
  }

  return root;
}

function tokenize(source: string): ParsedLine[] {
  return source
    .split(/\r?\n/u)
    .map((line, index) => ({ line, lineNumber: index + 1 }))
    .filter(({ line }) => line.trim() !== "" && !line.trimStart().startsWith("#"))
    .map(({ line, lineNumber }) => {
      if (line.includes("\t")) {
        throw new Error(`Tabs are not supported in YAML at line ${lineNumber}`);
      }

      const indent = line.length - line.trimStart().length;

      return {
        indent,
        lineNumber,
        text: line.trimStart()
      };
    });
}

function parseBlock(
  state: { index: number; lines: ParsedLine[] },
  indent: number
): YamlValue {
  const line = state.lines[state.index];

  if (!line || line.indent < indent) {
    throw new Error("Unexpected end of YAML input");
  }

  if (line.text.startsWith("-")) {
    return parseSequence(state, indent);
  }

  return parseMapping(state, indent);
}

function parseSequence(
  state: { index: number; lines: ParsedLine[] },
  indent: number
): YamlValue[] {
  const values: YamlValue[] = [];

  while (state.index < state.lines.length) {
    const line = state.lines[state.index];

    if (line.indent < indent) {
      break;
    }

    if (line.indent !== indent || !line.text.startsWith("-")) {
      break;
    }

    const itemText = line.text.slice(1).trimStart();

    if (itemText === "") {
      state.index += 1;
      values.push(parseChildBlock(state, indent, line.lineNumber));
      continue;
    }

    if (hasUnquotedColon(itemText)) {
      const item = parseInlineMapping(itemText, line.lineNumber);
      state.index += 1;

      if (state.index < state.lines.length && state.lines[state.index].indent > indent) {
        const extra = parseMapping(state, state.lines[state.index].indent);
        Object.assign(item, ensureObject(extra, line.lineNumber));
      }

      values.push(item);
      continue;
    }

    values.push(parseScalar(itemText));
    state.index += 1;
  }

  return values;
}

function parseMapping(
  state: { index: number; lines: ParsedLine[] },
  indent: number
): YamlObject {
  const object: YamlObject = {};

  while (state.index < state.lines.length) {
    const line = state.lines[state.index];

    if (line.indent < indent) {
      break;
    }

    if (line.indent !== indent || line.text.startsWith("-")) {
      break;
    }

    const colonIndex = findUnquotedColon(line.text);

    if (colonIndex < 0) {
      throw new Error(`Expected key/value mapping at line ${line.lineNumber}`);
    }

    const key = line.text.slice(0, colonIndex).trim();
    const rawValue = line.text.slice(colonIndex + 1).trimStart();

    state.index += 1;

    if (rawValue === "") {
      object[key] = parseChildBlock(state, indent, line.lineNumber);
    } else {
      object[key] = parseScalar(rawValue);
    }
  }

  return object;
}

function parseChildBlock(
  state: { index: number; lines: ParsedLine[] },
  parentIndent: number,
  lineNumber: number
): YamlValue {
  const nextLine = state.lines[state.index];

  if (!nextLine || nextLine.indent <= parentIndent) {
    throw new Error(`Expected indented block after line ${lineNumber}`);
  }

  return parseBlock(state, nextLine.indent);
}

function parseInlineMapping(text: string, lineNumber: number): YamlObject {
  const colonIndex = findUnquotedColon(text);

  if (colonIndex < 0) {
    throw new Error(`Expected key/value mapping at line ${lineNumber}`);
  }

  const key = text.slice(0, colonIndex).trim();
  const rawValue = text.slice(colonIndex + 1).trimStart();

  return {
    [key]: rawValue === "" ? null : parseScalar(rawValue)
  };
}

function parseScalar(text: string): YamlValue {
  const value = text.trim();

  if (value === "null") {
    return null;
  }

  if (value === "true") {
    return true;
  }

  if (value === "false") {
    return false;
  }

  if (/^-?\d+$/u.test(value)) {
    return Number.parseInt(value, 10);
  }

  if (/^-?\d+\.\d+$/u.test(value)) {
    return Number.parseFloat(value);
  }

  if (value.startsWith("\"") && value.endsWith("\"")) {
    return JSON.parse(value);
  }

  if (value.startsWith("'") && value.endsWith("'")) {
    return value.slice(1, -1);
  }

  if (value.startsWith("[") && value.endsWith("]")) {
    return parseInlineArray(value);
  }

  if (value.startsWith("{") && value.endsWith("}")) {
    return {};
  }

  return value;
}

function parseInlineArray(value: string): YamlValue[] {
  const content = value.slice(1, -1).trim();

  if (content === "") {
    return [];
  }

  const parts: string[] = [];
  let current = "";
  let inSingleQuote = false;
  let inDoubleQuote = false;

  for (const character of content) {
    if (character === "\"" && !inSingleQuote) {
      inDoubleQuote = !inDoubleQuote;
      current += character;
      continue;
    }

    if (character === "'" && !inDoubleQuote) {
      inSingleQuote = !inSingleQuote;
      current += character;
      continue;
    }

    if (character === "," && !inSingleQuote && !inDoubleQuote) {
      parts.push(current.trim());
      current = "";
      continue;
    }

    current += character;
  }

  if (current.trim() !== "") {
    parts.push(current.trim());
  }

  return parts.map((part) => parseScalar(part));
}

function hasUnquotedColon(text: string): boolean {
  return findUnquotedColon(text) >= 0;
}

function findUnquotedColon(text: string): number {
  let inSingleQuote = false;
  let inDoubleQuote = false;

  for (let index = 0; index < text.length; index += 1) {
    const character = text[index];

    if (character === "\"" && !inSingleQuote) {
      inDoubleQuote = !inDoubleQuote;
      continue;
    }

    if (character === "'" && !inDoubleQuote) {
      inSingleQuote = !inSingleQuote;
      continue;
    }

    if (character === ":" && !inSingleQuote && !inDoubleQuote) {
      return index;
    }
  }

  return -1;
}

function ensureObject(value: YamlValue, lineNumber: number): YamlObject {
  if (!isPlainObject(value)) {
    throw new Error(`Expected object value at line ${lineNumber}`);
  }

  return value;
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

export type { Contract, ContractCriterion, ContractEvalStrategy, ContractScope };
