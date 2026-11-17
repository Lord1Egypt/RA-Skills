#!/usr/bin/env node
import {
  callSciverse, encodePathSegment, ensureAllowedKeys, failArgument, isMain,
  optionalBoolean, optionalInteger, optionalString, optionalStringArray,
  pickDefined, readJsonArg, requireEnum, requireObject, runTool,
} from "./_common.mjs";

const ACTIONS = ["search", "list", "get"];

export function buildRequest(args) {
  const action = requireEnum(args.action, "action", ACTIONS);
  if (action === "search") {
    ensureAllowedKeys(args, ["action", "query", "filters", "hydrate_schema_papers", "size", "cursor"]);
    optionalString(args.query, "query", { max: 500 });
    const filters = args.filters === undefined ? {} : requireObject(args.filters, "filters");
    ensureAllowedKeys(filters, ["schema_ids", "entity_types", "entity_subtypes", "sections"], "filters");
    const schemaIds = Array.isArray(filters.schema_ids) ? filters.schema_ids : [];
    if (!args.query && schemaIds.length === 0) failArgument("Entity search without schema_ids requires query.");
    optionalBoolean(args.hydrate_schema_papers, "hydrate_schema_papers");
    optionalInteger(args.size, "size", { min: 1, max: 100 });
    optionalString(args.cursor, "cursor", { max: 4_000 });
    return { method: "POST", path: "/paper-schema/entities/search", body: pickDefined(args, ["query", "filters", "hydrate_schema_papers", "size", "cursor"]) };
  }

  if (action === "list") {
    ensureAllowedKeys(args, ["action", "schema_id", "entity_types", "entity_subtypes", "sections", "size", "cursor"]);
    const schemaId = encodePathSegment(args.schema_id, "schema_id");
    optionalStringArray(args.entity_types, "entity_types", { max: 30 });
    optionalStringArray(args.entity_subtypes, "entity_subtypes", { max: 50 });
    optionalStringArray(args.sections, "sections", { max: 50 });
    optionalInteger(args.size, "size", { min: 1, max: 100 });
    optionalString(args.cursor, "cursor", { max: 4_000 });
    return {
      method: "GET",
      path: `/paper-schema/schemas/${schemaId}/entities`,
      query: pickDefined(args, ["entity_types", "entity_subtypes", "sections", "size", "cursor"]),
    };
  }

  ensureAllowedKeys(args, ["action", "schema_id", "entity_id", "include_relations", "relation_limit"]);
  const schemaId = encodePathSegment(args.schema_id, "schema_id");
  const entityId = encodePathSegment(args.entity_id, "entity_id");
  optionalBoolean(args.include_relations, "include_relations");
  optionalInteger(args.relation_limit, "relation_limit", { min: 1, max: 100 });
  return {
    method: "GET",
    path: `/paper-schema/schemas/${schemaId}/entities/${entityId}`,
    query: pickDefined(args, ["include_relations", "relation_limit"]),
  };
}

if (isMain(import.meta.url)) {
  await runTool(async () => {
    const request = buildRequest(readJsonArg());
    return callSciverse(request.method, request.path, { query: request.query, body: request.body });
  });
}
