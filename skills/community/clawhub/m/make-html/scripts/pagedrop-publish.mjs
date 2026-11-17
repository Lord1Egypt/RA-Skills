#!/usr/bin/env node

import { execFile } from "node:child_process";
import { readFile } from "node:fs/promises";
import { basename } from "node:path";
import { promisify, parseArgs } from "node:util";

const execFileAsync = promisify(execFile);
const ROUTES = new Set(["g", "h"]);
const GIST_URL_PATTERN = /^https:\/\/gist\.github\.com\/(?:[^/]+\/)?([a-f0-9]+)$/i;
const PAGEDROP_BOOTSTRAP_URL = "https://pagedrop.ai/pagedrop.js";

function fail(message) {
  console.error(`Pagedrop publish failed: ${message}`);
  process.exit(1);
}

async function runGh(args) {
  try {
    return await execFileAsync("gh", args, {
      encoding: "utf8",
      maxBuffer: 1024 * 1024,
    });
  } catch (error) {
    const detail = error?.stderr?.trim() || error?.message || String(error);
    fail(detail);
  }
}

let values;
let positionals;

try {
  ({ values, positionals } = parseArgs({
    allowPositionals: true,
    options: {
      description: { type: "string" },
      route: { type: "string", default: "g" },
    },
  }));
} catch (error) {
  fail(error instanceof Error ? error.message : String(error));
}

if (positionals.length !== 1) {
  fail(
    'usage: node scripts/pagedrop-publish.mjs <file.html> [--description "Text"] [--route g|h]',
  );
}

if (!ROUTES.has(values.route)) {
  fail(`unsupported route "${values.route}"; use g or h`);
}

const filePath = positionals[0];
const fileName = basename(filePath);

try {
  const html = await readFile(filePath, "utf8");

  if (!html.trim()) {
    fail("the HTML file is empty");
  }

  if (!/<html[\s>]/i.test(html) || !/<\/html>/i.test(html)) {
    fail("the file does not contain a complete HTML document");
  }

  if (values.route === "h" && !html.includes(PAGEDROP_BOOTSTRAP_URL)) {
    fail(`route h requires ${PAGEDROP_BOOTSTRAP_URL} in the HTML`);
  }
} catch (error) {
  fail(error instanceof Error ? error.message : String(error));
}

await runGh(["auth", "status"]);

const requestedDescription = values.description?.trim() || `Pagedrop: ${fileName}`;
const description = /(?:^|\s)#pagedrop(?:\s|$)/i.test(requestedDescription)
  ? requestedDescription
  : `${requestedDescription} #pagedrop`;
const { stdout } = await runGh(["gist", "create", filePath, "--desc", description]);
const gistUrl = stdout.trim().split(/\s+/).find((value) => GIST_URL_PATTERN.test(value));
const match = gistUrl?.match(GIST_URL_PATTERN);

if (!gistUrl || !match) {
  fail(`could not parse Gist URL from gh output: ${stdout.trim() || "(empty output)"}`);
}

const [, gistId] = match;
const { stdout: userOutput } = await runGh(["api", "user", "--jq", ".login"]);
const user = userOutput.trim();

if (!user) {
  fail("could not determine the authenticated GitHub username");
}

console.log(`https://pagedrop.ai/${values.route}/${user}/${gistId}`);
