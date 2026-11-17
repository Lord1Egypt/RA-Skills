#!/usr/bin/env node
import {
  callSciverse, encodePathSegment, ensureAllowedKeys, failArgument, isMain, optionalBoolean, optionalInteger,
  optionalString, optionalStringArray, pickDefined, readJsonArg, requireEnum,
  requireString, runTool,
} from "./_common.mjs";

const ACTIONS = ["entity", "seed"];

export function buildRequest(args) {
  const action = requireEnum(args.action, "action", ACTIONS);
  if (action === "entity") {
    ensureAllowedKeys(args, ["action", "query", "entity_types", "entity_subtypes", "exclude_schema_ids", "size", "cursor"]);
    requireString(args.query, "query", { max: 500 });
    optionalStringArray(args.entity_types, "entity_types", { max: 30 });
    optionalStringArray(args.entity_subtypes, "entity_subtypes", { max: 50 });
    optionalStringArray(args.exclude_schema_ids, "exclude_schema_ids", { max: 100 });
    optionalInteger(args.size, "size", { min: 1, max: 100 });
    optionalString(args.cursor, "cursor", { max: 4_000 });
    return {
      method: "POST",
      path: "/paper-schema/entities/related-papers",
      body: pickDefined(args, ["query", "entity_types", "entity_subtypes", "exclude_schema_ids", "size", "cursor"]),
    };
  }

  ensureAllowedKeys(args, ["action", "schema_id", "signals", "exclude_same_work", "size"]);
  const schemaId = encodePathSegment(args.schema_id, "schema_id");
  const signals = optionalStringArray(args.signals, "signals", { max: 3 });
  if (signals?.some((signal) => !["term", "entity", "citation"].includes(signal))) {
    failArgument("signals contains unsupported values.");
  }
  optionalBoolean(args.exclude_same_work, "exclude_same_work");
  optionalInteger(args.size, "size", { min: 1, max: 50 });
  return {
    method: "POST",
    path: `/paper-schema/schemas/${schemaId}/related-papers`,
    body: pickDefined(args, ["signals", "exclude_same_work", "size"]),
  };
}

if (isMain(import.meta.url)) {
  await runTool(async () => {
    const request = buildRequest(readJsonArg());
    return callSciverse(request.method, request.path, { body: request.body });
  });
}
