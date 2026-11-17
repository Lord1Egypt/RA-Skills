#!/usr/bin/env node
import {
  callSciverse, ensureAllowedKeys, failArgument, isMain, optionalInteger,
  optionalString, readJsonArg, requireObject, runTool,
} from "./_common.mjs";

const KEYS = ["query", "filters", "sort", "size", "cursor"];
const FILTER_KEYS = ["schema_ids", "dois", "authors", "venues", "published_year_gte", "published_year_lte", "has_code", "has_data", "is_oa", "metadata_status"];

export function buildRequest(args) {
  ensureAllowedKeys(args, KEYS);
  optionalString(args.query, "query", { max: 500 });
  optionalString(args.cursor, "cursor", { max: 4_000 });
  optionalInteger(args.size, "size", { min: 1, max: 100 });
  const filters = args.filters === undefined ? {} : requireObject(args.filters, "filters");
  ensureAllowedKeys(filters, FILTER_KEYS, "filters");
  if (!args.query && Object.values(filters).every((value) => value === undefined || value === null || (Array.isArray(value) && value.length === 0))) {
    failArgument("search requires query or at least one metadata filter.");
  }
  if (args.sort !== undefined && !Array.isArray(args.sort)) failArgument("sort must be an array.");
  for (const [index, spec] of (args.sort ?? []).entries()) {
    ensureAllowedKeys(spec, ["field", "order"], `sort[${index}]`);
  }
  return { method: "POST", path: "/paper-schema/search", body: args };
}

if (isMain(import.meta.url)) {
  await runTool(async () => {
    const request = buildRequest(readJsonArg());
    return callSciverse(request.method, request.path, { body: request.body });
  });
}
