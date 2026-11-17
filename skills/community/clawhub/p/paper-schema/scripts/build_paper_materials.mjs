#!/usr/bin/env node
import {
  callSciverse, ensureAllowedKeys, failArgument, isMain, LONG_TIMEOUT_MS, optionalBoolean,
  optionalInteger, optionalStringArray, readJsonArg, requireEnum, runTool,
} from "./_common.mjs";

const KEYS = ["schema_ids", "goal", "include_relation_context", "per_schema_entity_limit", "per_schema_relation_limit", "per_schema_attribute_limit", "per_schema_term_limit"];

export function buildRequest(args) {
  ensureAllowedKeys(args, KEYS);
  const schemaIds = optionalStringArray(args.schema_ids, "schema_ids", { max: 20 });
  if (!schemaIds?.length) failArgument("schema_ids must contain 1 to 20 values.");
  if (args.goal !== undefined) requireEnum(args.goal, "goal", ["overview", "benchmark", "method", "reproduction", "survey"]);
  optionalBoolean(args.include_relation_context, "include_relation_context");
  optionalInteger(args.per_schema_entity_limit, "per_schema_entity_limit", { min: 0, max: 150 });
  optionalInteger(args.per_schema_relation_limit, "per_schema_relation_limit", { min: 0, max: 150 });
  optionalInteger(args.per_schema_attribute_limit, "per_schema_attribute_limit", { min: 0, max: 200 });
  optionalInteger(args.per_schema_term_limit, "per_schema_term_limit", { min: 0, max: 100 });
  return { method: "POST", path: "/paper-schema/materials", body: args, timeoutMs: LONG_TIMEOUT_MS };
}

if (isMain(import.meta.url)) {
  await runTool(async () => {
    const request = buildRequest(readJsonArg());
    return callSciverse(request.method, request.path, { body: request.body, timeoutMs: request.timeoutMs });
  });
}
