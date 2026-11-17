#!/usr/bin/env node
import {
  callSciverse, encodePathSegment, ensureAllowedKeys, failArgument, isMain, optionalBoolean,
  optionalInteger, optionalString, optionalStringArray, pickDefined, readJsonArg,
  requireEnum, runTool,
} from "./_common.mjs";

const ACTIONS = ["search", "get"];
const GROUPS = ["evidence_score", "schema_unit", "reference_semantics", "reference_core", "comparison_detail", "citation_signal", "formula", "core_claim_result", "table_evidence", "resource"];

export function buildRequest(args) {
  const action = requireEnum(args.action, "action", ACTIONS);
  if (action === "search") {
    ensureAllowedKeys(args, ["action", "groups", "group_operator", "schema_ids", "query", "key", "path_bucket", "value_number_min", "value_number_max", "value_bool", "hydrate_schema_papers", "size", "cursor"]);
    const groups = optionalStringArray(args.groups, "groups", { max: 5 });
    if (!groups?.length) failArgument("Evidence search requires at least one group.");
    const unknown = groups.filter((group) => !GROUPS.includes(group));
    if (unknown.length) failArgument(`Unknown evidence groups: ${unknown.join(", ")}.`);
    if (args.group_operator !== undefined) requireEnum(args.group_operator, "group_operator", ["any", "all"]);
    optionalStringArray(args.schema_ids, "schema_ids", { max: 100 });
    optionalString(args.query, "query", { max: 500 });
    optionalString(args.key, "key", { max: 300 });
    optionalString(args.path_bucket, "path_bucket", { max: 500 });
    optionalBoolean(args.value_bool, "value_bool");
    optionalBoolean(args.hydrate_schema_papers, "hydrate_schema_papers");
    optionalInteger(args.size, "size", { min: 1, max: 100 });
    optionalString(args.cursor, "cursor", { max: 4_000 });
    const narrowed = [args.schema_ids?.length, args.query, args.key, args.path_bucket, args.value_number_min !== undefined, args.value_number_max !== undefined, args.value_bool !== undefined].some(Boolean);
    if (!narrowed) failArgument("Evidence search requires groups plus one narrowing condition.");
    return { method: "POST", path: "/paper-schema/evidence/search", body: pickDefined(args, ["groups", "group_operator", "schema_ids", "query", "key", "path_bucket", "value_number_min", "value_number_max", "value_bool", "hydrate_schema_papers", "size", "cursor"]) };
  }

  ensureAllowedKeys(args, ["action", "schema_id", "evidence_id"]);
  const schemaId = encodePathSegment(args.schema_id, "schema_id");
  const evidenceId = encodePathSegment(args.evidence_id, "evidence_id");
  return { method: "GET", path: `/paper-schema/schemas/${schemaId}/evidence/${evidenceId}` };
}

if (isMain(import.meta.url)) {
  await runTool(async () => {
    const request = buildRequest(readJsonArg());
    return callSciverse(request.method, request.path, { body: request.body });
  });
}
