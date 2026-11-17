#!/usr/bin/env node
import {
  callSciverse, encodePathSegment, ensureAllowedKeys, failArgument, isMain,
  optionalBoolean, optionalInteger, optionalString, pickDefined, readJsonArg,
  requireEnum, requireObject, runTool,
} from "./_common.mjs";

const ACTIONS = ["search", "get"];
const PUBLIC_RELATION_TYPES = [
  "part_of", "evaluates", "about", "uses_component", "compares_with",
  "background", "compares_to", "addresses_limitation_of", "resolves",
  "motivates", "analyzes_property_of", "builds_on", "inspired_by",
  "adapts_idea_from", "co_contribution", "supports",
];

export function buildRequest(args) {
  const action = requireEnum(args.action, "action", ACTIONS);
  if (action === "search") {
    ensureAllowedKeys(args, ["action", "filters", "evidence_query", "include_context", "size", "cursor"]);
    const filters = requireObject(args.filters ?? {}, "filters");
    ensureAllowedKeys(filters, ["schema_ids", "source_entity_ids", "target_entity_ids", "relation_types"], "filters");
    const structural = ["schema_ids", "source_entity_ids", "target_entity_ids", "relation_types"]
      .some((key) => Array.isArray(filters[key]) && filters[key].length > 0);
    if (!structural) failArgument("Relation search requires a structural filter.");
    if (Array.isArray(filters.relation_types)) {
      const unsupported = filters.relation_types.filter((value) => !PUBLIC_RELATION_TYPES.includes(value));
      if (unsupported.length) failArgument("filters.relation_types contains unsupported values.");
    }
    optionalString(args.evidence_query, "evidence_query", { max: 500 });
    if (args.include_context !== undefined) requireEnum(args.include_context, "include_context", ["none", "entities"]);
    optionalInteger(args.size, "size", { min: 1, max: 100 });
    optionalString(args.cursor, "cursor", { max: 4_000 });
    return { method: "POST", path: "/paper-schema/relations/search", body: pickDefined(args, ["filters", "evidence_query", "include_context", "size", "cursor"]) };
  }

  ensureAllowedKeys(args, ["action", "schema_id", "relation_id", "include_context"]);
  const schemaId = encodePathSegment(args.schema_id, "schema_id");
  const relationId = encodePathSegment(args.relation_id, "relation_id");
  optionalBoolean(args.include_context, "include_context");
  return {
    method: "GET",
    path: `/paper-schema/schemas/${schemaId}/relations/${relationId}`,
    query: pickDefined(args, ["include_context"]),
  };
}

if (isMain(import.meta.url)) {
  await runTool(async () => {
    const request = buildRequest(readJsonArg());
    return callSciverse(request.method, request.path, { query: request.query, body: request.body });
  });
}
