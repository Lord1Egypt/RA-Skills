#!/usr/bin/env bun
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";

const sharedScript = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../shared-image-generation/scripts/main.ts");

const packageJsonDir = process.env.npm_package_json
  ? path.basename(path.dirname(process.env.npm_package_json))
  : null;
const packageName = process.env.npm_package_name?.trim();
const cwdBase = path.basename(process.cwd()).trim();
const skillNamespace = process.env.IMAGE_SKILL_NAMESPACE?.trim() || packageJsonDir || cwdBase || packageName || "image-generation";
const result = spawnSync(process.execPath, [sharedScript, ...process.argv.slice(2)], {
  stdio: "inherit",
  env: {
    ...process.env,
    IMAGE_SKILL_NAMESPACE: skillNamespace,
    IMAGE_SKILL_LABEL: process.env.IMAGE_SKILL_LABEL?.trim() || packageName || skillNamespace,
  },
});

process.exit(result.status ?? 1);
