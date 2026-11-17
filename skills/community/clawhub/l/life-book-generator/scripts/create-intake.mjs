#!/usr/bin/env node
import { parseArgs, printJson, readJsonInput, requestJson, resolveBaseUrl, resolveTimeoutMs } from "./_shared.mjs";

const HELP = `Usage:
  node skills/life-book-generator/scripts/create-intake.mjs --input-file <path>
  node skills/life-book-generator/scripts/create-intake.mjs --input '{"version":"intake@1", ...}'
  cat intake.json | node skills/life-book-generator/scripts/create-intake.mjs
`;

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    process.stdout.write(HELP);
    return;
  }
  const baseUrl = resolveBaseUrl(args);
  const timeoutMs = resolveTimeoutMs(args);
  const payload = await readJsonInput(args);
  const body = await requestJson(baseUrl, "/api/intakes", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(payload),
  }, timeoutMs);

  printJson({
    ok: true,
    baseUrl,
    intakeId: body.intakeId,
    checkoutPath: body.next,
    checkoutUrl: `${baseUrl}${body.next}`,
  });
}

main().catch((error) => {
  process.stderr.write(`${error instanceof Error ? error.message : "CREATE_INTAKE_FAILED"}\n`);
  process.exit(1);
});
