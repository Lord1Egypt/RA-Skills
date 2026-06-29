#!/usr/bin/env node
import { resolveConfig } from "./lib/seedance-2-video.mjs";

async function main() {
  const config = resolveConfig();
  console.log(`HiAPI configuration looks ready.`);
  console.log(`Base URL: ${config.baseUrl}`);

  if (process.argv.includes("--live")) {
    const response = await fetch(`${config.baseUrl}/api/pricing`);
    if (!response.ok) throw new Error(`Live check failed: HTTP ${response.status}`);
    console.log("Live check reached HiAPI pricing.");
  }
}

main().catch((error) => {
  console.error(error.message);
  process.exitCode = 1;
});
