#!/usr/bin/env node

import { execFile } from "child_process";
import { promisify } from "util";

const execFileAsync = promisify(execFile);

type Mode = "mirror" | "direct" | "auto";

async function main() {
  const [userContext, channel, mode = "auto", caption = "Raya 的自拍 ✨"] = process.argv.slice(2);

  if (!userContext || !channel) {
    console.log(`Usage: node clawra-selfie.ts <user_context> <channel> [mode] [caption]`);
    process.exit(1);
  }

  const scriptPath = "/home/Jaben/.openclaw/skills/clawra-selfie/scripts/clawra-selfie.sh";

  try {
    const { stdout, stderr } = await execFileAsync(scriptPath, [userContext, channel, mode as Mode, caption], {
      env: process.env,
      maxBuffer: 20 * 1024 * 1024,
    });

    if (stdout) process.stdout.write(stdout);
    if (stderr) process.stderr.write(stderr);
  } catch (error: any) {
    if (error.stdout) process.stdout.write(error.stdout);
    if (error.stderr) process.stderr.write(error.stderr);
    console.error(`[ERROR] ${error.message}`);
    process.exit(error.code || 1);
  }
}

main();
