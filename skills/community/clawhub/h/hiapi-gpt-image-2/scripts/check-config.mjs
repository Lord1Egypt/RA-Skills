#!/usr/bin/env node
import { resolveConfig } from "./lib/gpt-image-2.mjs";

function parseArgs(argv) {
  return {
    live: argv.includes("--live"),
    help: argv.includes("--help") || argv.includes("-h"),
  };
}

function printHelp() {
  console.log(`Usage:
  hiapi-gpt-image-2-check [--live]

Checks HIAPI_API_KEY and HIAPI_BASE_URL. Use --live to make a network request.`);
}

async function main() {
  const options = parseArgs(process.argv.slice(2));
  if (options.help) {
    printHelp();
    return;
  }

  const config = resolveConfig();

  if (!options.live) {
    console.log(
      JSON.stringify(
        {
          ok: true,
          baseUrl: config.baseUrl,
          apiKeyConfigured: true,
          liveChecked: false,
        },
        null,
        2,
      ),
    );
    return;
  }

  const response = await fetch(`${config.baseUrl}/api/pricing`, {
    headers: {
      Authorization: `Bearer ${config.apiKey}`,
      Accept: "application/json",
    },
  });

  if (!response.ok) {
    throw new Error(`Live HiAPI check failed with HTTP ${response.status}.`);
  }

  console.log(
    JSON.stringify(
      {
        ok: true,
        baseUrl: config.baseUrl,
        apiKeyConfigured: true,
        liveChecked: true,
      },
      null,
      2,
    ),
  );
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exitCode = 1;
});
