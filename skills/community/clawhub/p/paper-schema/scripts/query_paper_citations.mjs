#!/usr/bin/env node
import {
  callSciverse, encodePathSegment, ensureAllowedKeys, isMain, LONG_TIMEOUT_MS,
  optionalInteger, optionalString, pickDefined, readJsonArg, requireEnum, runTool,
} from "./_common.mjs";

const ACTIONS = ["summary", "list", "graph"];

export function buildRequest(args) {
  const action = requireEnum(args.action, "action", ACTIONS);
  const schemaId = encodePathSegment(args.schema_id, "schema_id");
  if (action === "summary") {
    ensureAllowedKeys(args, ["action", "schema_id"]);
    return { method: "GET", path: `/paper-schema/schemas/${schemaId}/citation-summary` };
  }
  if (action === "list") {
    ensureAllowedKeys(args, ["action", "schema_id", "size", "cursor"]);
    optionalInteger(args.size, "size", { min: 1, max: 100 });
    optionalString(args.cursor, "cursor", { max: 4_000 });
    return { method: "GET", path: `/paper-schema/schemas/${schemaId}/citations`, query: pickDefined(args, ["size", "cursor"]) };
  }
  ensureAllowedKeys(args, ["action", "schema_id", "direction", "depth", "max_nodes", "max_edges"]);
  if (args.direction !== undefined) requireEnum(args.direction, "direction", ["outbound", "inbound"]);
  optionalInteger(args.depth, "depth", { min: 1, max: 3 });
  optionalInteger(args.max_nodes, "max_nodes", { min: 2, max: 500 });
  optionalInteger(args.max_edges, "max_edges", { min: 1, max: 500 });
  return {
    method: "GET",
    path: `/paper-schema/schemas/${schemaId}/citation-graph`,
    query: pickDefined(args, ["direction", "depth", "max_nodes", "max_edges"]),
    timeoutMs: LONG_TIMEOUT_MS,
  };
}
if (isMain(import.meta.url)) {
  await runTool(async () => {
    const request = buildRequest(readJsonArg());
    return callSciverse(request.method, request.path, { query: request.query, timeoutMs: request.timeoutMs });
  });
}
