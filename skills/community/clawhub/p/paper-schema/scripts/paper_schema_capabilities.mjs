#!/usr/bin/env node
import { callSciverse, ensureAllowedKeys, isMain, readJsonArg, runTool } from "./_common.mjs";

export function buildRequest(args) {
  ensureAllowedKeys(args, []);
  return { method: "GET", path: "/paper-schema" };
}
if (isMain(import.meta.url)) {
  await runTool(async () => {
    const request = buildRequest(readJsonArg());
    return callSciverse(request.method, request.path);
  });
}
