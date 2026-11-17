#!/usr/bin/env node
import {
  callSciverse, ensureAllowedKeys, failArgument, isMain, LONG_TIMEOUT_MS, optionalBoolean,
  optionalInteger, optionalString, pickDefined, readJsonArg, requireEnum,
  requireObject, requireString, runTool,
} from "./_common.mjs";

const ACTIONS = ["provenance", "search", "hydrate"];

export function buildRequest(args) {
  const action = requireEnum(args.action, "action", ACTIONS);
  if (action === "provenance") {
    ensureAllowedKeys(args, ["action", "schema_id", "marker_nums", "paragraph_ids", "window", "max_segments"]);
    const markerMode = Boolean(args.schema_id && Array.isArray(args.marker_nums) && args.marker_nums.length);
    const paragraphMode = Boolean(Array.isArray(args.paragraph_ids) && args.paragraph_ids.length);
    if (markerMode === paragraphMode) failArgument("Use exactly one provenance mode: schema_id + marker_nums, or paragraph_ids.");
    optionalInteger(args.window, "window", { min: 0, max: 5 });
    optionalInteger(args.max_segments, "max_segments", { min: 1, max: 100 });
    return { method: "POST", path: "/paper-schema/resolve-provenance", body: pickDefined(args, ["schema_id", "marker_nums", "paragraph_ids", "window", "max_segments"]) };
  }

  if (action === "search") {
    ensureAllowedKeys(args, ["action", "schema_id", "query", "section_hint", "prefer_url", "prefer_code", "top_k", "window"]);
    requireString(args.schema_id, "schema_id");
    requireString(args.query, "query", { max: 500 });
    optionalString(args.section_hint, "section_hint", { max: 300 });
    optionalBoolean(args.prefer_url, "prefer_url");
    optionalBoolean(args.prefer_code, "prefer_code");
    optionalInteger(args.top_k, "top_k", { min: 1, max: 20 });
    optionalInteger(args.window, "window", { min: 0, max: 5 });
    return { method: "POST", path: "/paper-schema/search-in-schema", body: pickDefined(args, ["schema_id", "query", "section_hint", "prefer_url", "prefer_code", "top_k", "window"]) };
  }

  ensureAllowedKeys(args, ["action", "items", "window", "max_segments_per_item", "prefer_url_or_code"]);
  if (!Array.isArray(args.items) || args.items.length < 1 || args.items.length > 50) failArgument("items must contain 1 to 50 hydration objects.");
  for (const [index, item] of args.items.entries()) {
    requireObject(item, `items[${index}]`);
    ensureAllowedKeys(item, ["schema_id", "paragraph_ids", "marker_nums", "hydration_query", "key", "value_text"], `items[${index}]`);
  }
  optionalInteger(args.window, "window", { min: 0, max: 5 });
  optionalInteger(args.max_segments_per_item, "max_segments_per_item", { min: 1, max: 20 });
  optionalBoolean(args.prefer_url_or_code, "prefer_url_or_code");
  return { method: "POST", path: "/paper-schema/hydrate-items", body: pickDefined(args, ["items", "window", "max_segments_per_item", "prefer_url_or_code"]), timeoutMs: LONG_TIMEOUT_MS };
}

if (isMain(import.meta.url)) {
  await runTool(async () => {
    const request = buildRequest(readJsonArg());
    return callSciverse(request.method, request.path, { body: request.body, timeoutMs: request.timeoutMs });
  });
}
