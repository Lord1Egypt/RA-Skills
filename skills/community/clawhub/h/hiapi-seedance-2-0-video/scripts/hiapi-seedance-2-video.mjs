#!/usr/bin/env node
import { generateVideo, parseArgs, resolveConfig, usage, warnOrRequireSkillUpdate } from "./lib/seedance-2-video.mjs";

async function main() {
  const options = parseArgs(process.argv.slice(2));
  if (options.help) {
    console.log(usage());
    return;
  }

  await warnOrRequireSkillUpdate();

  const config = resolveConfig();
  const result = await generateVideo(options, config);
  console.log(JSON.stringify(result, null, 2));
}

main().catch((error) => {
  console.error(error.message);
  process.exitCode = 1;
});
