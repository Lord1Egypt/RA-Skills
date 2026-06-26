#!/usr/bin/env node

import { spawn } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import process from "node:process";

function usage() {
  console.log(`nanobanana-plus

Usage:
  node nanobanana-plus.mjs init
  node nanobanana-plus.mjs check
  node nanobanana-plus.mjs models
  node nanobanana-plus.mjs generate --prompt "..." [--filename out.png] [--aspect-ratio 16:9] [--model MODEL] [--output-count 1]

Options:
  --prompt       Image description (required for generate)
  --filename     Output file path
  --aspect-ratio  Image aspect ratio (16:9, 9:16, 1:1, 4:3, 3:4)
  --model        Model to use (gemini-3.1-flash-image-preview, gemini-3-pro-image-preview, etc.)
  --output-count Number of images to generate (1-8)
`);
}

function parseArgs(argv) {
  const args = [...argv];
  let command = "generate";
  if (args[0] && !args[0].startsWith("-")) {
    command = args.shift();
  }

  const options = {};
  while (args.length > 0) {
    const current = args.shift();
    if (!current) {
      continue;
    }

    if (current === "--help" || current === "-h") {
      options.help = true;
      continue;
    }

    if (!current.startsWith("--")) {
      throw new Error(`Unknown argument: ${current}`);
    }

    const key = current.slice(2);
    const value = args.shift();
    if (!value || value.startsWith("--")) {
      throw new Error(`Missing value for --${key}`);
    }
    options[key] = value;
  }

  return { command, options };
}

function inferFileFormat(filename) {
  if (!filename) {
    return "png";
  }
  const ext = path.extname(filename).toLowerCase();
  if (ext === ".jpg" || ext === ".jpeg") {
    return "jpeg";
  }
  return "png";
}

function resolveNanobanana() {
  const scriptDir = path.dirname(path.resolve(process.argv[1]));
  const skillDir = path.dirname(scriptDir);
  const baseDir = path.dirname(skillDir);
  const possibleBin = path.resolve(baseDir, "bin", "nanobanana-plus.js");

  if (fs.existsSync(possibleBin)) {
    return possibleBin;
  }

  return "nanobanana-plus";
}

function buildCliArgs(command, options) {
  const args = [command];

  if (options.prompt) {
    args.push("--prompt", options.prompt);
  }
  if (options.filename) {
    args.push("--filename", options.filename);
  }
  if (options["aspect-ratio"]) {
    args.push("--aspect-ratio", options["aspect-ratio"]);
  }
  if (options.model) {
    args.push("--model", options.model);
  }
  if (options["output-count"]) {
    args.push("--output-count", options["output-count"]);
  }
  if (options["file-format"]) {
    args.push("--file-format", options["file-format"]);
  }
  if (options.seed) {
    args.push("--seed", options.seed);
  }

  return args;
}

async function runCli(command, options) {
  return new Promise((resolve, reject) => {
    const exePath = resolveNanobanana();
    const args = buildCliArgs(command, options);

    const child = spawn(process.execPath, [exePath, ...args], {
      stdio: ["inherit", "pipe", "pipe"],
      env: process.env,
    });

    let stdout = "";
    let stderr = "";

    child.stdout.on("data", (data) => {
      const text = data.toString();
      stdout += text;
      process.stdout.write(text);
    });

    child.stderr.on("data", (data) => {
      const text = data.toString();
      stderr += text;
      process.stderr.write(text);
    });

    child.on("error", (error) => {
      reject(new Error(`Failed to spawn nanobanana-plus: ${error.message}`));
    });

    child.on("close", (code) => {
      if (code === 0) {
        resolve({ stdout, stderr, code });
      } else {
        reject(new Error(`nanobanana-plus exited with code ${code}`));
      }
    });
  });
}

async function main() {
  const { command, options } = parseArgs(process.argv.slice(2));

  if (options.help) {
    usage();
    return;
  }

  if (command === "init") {
    const exePath = resolveNanobanana();
    console.log("nanobanana-plus CLI is ready (no server needed).");
    console.log("");
    console.log("Usage:");
    console.log(
      `  node nanobanana-plus.mjs generate --prompt "a cat" --filename cat.png`,
    );
    console.log("");
    console.log(
      "The CLI will use NANOBANANA_GEMINI_API_KEY or GEMINI_API_KEY from environment.",
    );
    return;
  }

  if (command === "check") {
    console.log("nanobanana-plus CLI is available.");
    return;
  }

  if (command === "models") {
    console.log("Models (set via --model flag at generate time):");
    console.log("  gemini-3.1-flash-image-preview  (Nano Banana 2 - default)");
    console.log("  gemini-3-pro-image-preview     (Nano Banana Pro)");
    console.log("  imagen-4.0-ultra-generate-001 (Imagen 4 Ultra)");
    console.log("  imagen-4.0-fast-generate-001 (Imagen 4 Fast)");
    return;
  }

  if (command === "generate") {
    if (!options.prompt) {
      throw new Error("--prompt is required for generate");
    }

    await runCli("generate", options);
    return;
  }

  if (command === "edit" || command === "restore") {
    throw new Error(
      `${command} is not supported in CLI mode. Use MCP server for image editing features.`,
    );
  }

  usage();
  throw new Error(`Unknown command: ${command}`);
}

main().catch((error) => {
  console.error(`Error: ${error.message}`);
  process.exit(1);
});
