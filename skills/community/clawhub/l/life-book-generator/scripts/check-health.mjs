#!/usr/bin/env node
import { parseArgs, printJson, requestJson, resolveBaseUrl, resolveTimeoutMs } from "./_shared.mjs";

const HELP = `Usage:
  node skills/life-book-generator/scripts/check-health.mjs [--base-url <url>] [--timeout-ms <ms>]
`;

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    process.stdout.write(HELP);
    return;
  }
  const baseUrl = resolveBaseUrl(args);
  const timeoutMs = resolveTimeoutMs(args);
  const body = await requestJson(baseUrl, "/api/health", { method: "GET" }, timeoutMs);
  printJson({
    ok: body.status === "ok",
    baseUrl,
    timeoutMs,
    health: body,
  });
  if (body.status !== "ok") process.exit(1);
}

main().catch((error) => {
  process.stderr.write(`${error instanceof Error ? error.message : "CHECK_HEALTH_FAILED"}\n`);
  process.exit(1);
});
