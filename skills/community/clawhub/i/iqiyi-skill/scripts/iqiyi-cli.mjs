#!/usr/bin/env node
import { fileURLToPath } from "node:url";
import { buildOperationRequest, executeOperation } from "./iqiyi-skill-catalog.mjs";
import { playByTitle6 } from "./qips-build.mjs";

const OPERATION_MAP = new Map([
  ["video search", "video.search"],
  ["video recommend", "video.recommend"],
  ["video details", "video.details"],
  ["video related", "video.related"],
  ["video episode", "video.episode"],
  ["video play", "video.play"],
  ["star search", "star.search"],
]);

const NUMBER_KEYS = new Set(["pageNum", "season", "year", "episode"]);
const ARRAY_KEYS = new Set(["style"]);
const LOCAL_QIPS_OPERATIONS = new Set(["video.play"]);

function usage() {
  return [
    "Usage:",
    "  iqiyi-cli video search --q <query> [--pageNum 1]",
    "  iqiyi-cli video recommend --type <type> [--style <style>] [--kind suggest]",
    "  iqiyi-cli video play --title <title> [--season 2] [--episode 5] [--year 2024]  # prints qips, no network",
    "  iqiyi-cli video details|related|episode --title <title> [--season 2] [--year 2024]",
    "  iqiyi-cli star search --q <name>",
    "",
    "Options:",
    "  --json <object>       Merge a JSON object into input.",
    "  --authorization <v>   Pass an external Authorization header.",
    "  --dry-run             Print request JSON without network.",
    "  --text                Print formatted text from the response.",
    "  --raw                 Print raw response JSON.",
    "  --formatted           Print formatted response JSON.",
    "  --request             Print request JSON after executing.",
  ].join("\n");
}

function coerceValue(key, value) {
  if (NUMBER_KEYS.has(key)) return Number(value);
  return value;
}

function assignInput(input, key, value) {
  const coerced = coerceValue(key, value);
  if (!ARRAY_KEYS.has(key)) {
    input[key] = coerced;
    return;
  }

  const values = String(coerced)
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
  input[key] = [...(Array.isArray(input[key]) ? input[key] : []), ...values];
}

export function parseIqiyiCliArgs(argv) {
  const [domain, action, ...rest] = argv;
  const operationId = OPERATION_MAP.get(`${domain || ""} ${action || ""}`);

  if (!operationId) {
    throw new Error(`Unsupported iqiyi-cli command: ${argv.slice(0, 2).join(" ")}\n${usage()}`);
  }

  const input = {};
  const options = {
    dryRun: false,
    output: "json",
  };

  for (let index = 0; index < rest.length; index += 1) {
    const token = rest[index];
    if (!token.startsWith("--")) {
      throw new Error(`Unexpected positional argument: ${token}`);
    }

    const key = token.slice(2);
    if (key === "dry-run") {
      options.dryRun = true;
      continue;
    }
    if (["text", "raw", "formatted", "request"].includes(key)) {
      options.output = key;
      continue;
    }

    const value = rest[index + 1];
    if (value === undefined || value.startsWith("--")) {
      throw new Error(`Missing value for --${key}`);
    }
    index += 1;

    if (key === "json") {
      Object.assign(input, JSON.parse(value));
    } else if (key === "authorization") {
      options.authorization = value;
    } else {
      assignInput(input, key, value);
    }
  }

  return { operationId, input, options };
}

export function buildCliRequest(argv) {
  const { operationId, input, options } = parseIqiyiCliArgs(argv);
  if (LOCAL_QIPS_OPERATIONS.has(operationId)) {
    return buildLocalQipsResult(operationId, input, options);
  }
  return buildOperationRequest(operationId, input, options);
}

function buildLocalQipsResult(operationId, input) {
  if (operationId !== "video.play") {
    throw new Error(`Unsupported local qips operation: ${operationId}`);
  }

  const qips = playByTitle6({
    title: input.title,
    season: input.season,
    year: input.year,
    episode: input.episode,
  });

  return {
    kind: "qips",
    operationId,
    qips,
    text: qips,
    input,
    network: false,
  };
}

function selectOutput(result, options) {
  if (options.dryRun) return result;
  if (options.output === "text") return result.formatted.text || "";
  if (options.output === "raw") return result.raw;
  if (options.output === "formatted") return result.formatted;
  if (options.output === "request") return result.request;
  return result;
}

export async function runIqiyiCli(argv, runtime = {}) {
  const { operationId, input, options } = parseIqiyiCliArgs(argv);

  if (LOCAL_QIPS_OPERATIONS.has(operationId)) {
    const result = buildLocalQipsResult(operationId, input, options);
    if (options.output === "formatted" || options.output === "request" || options.output === "raw") {
      return result;
    }
    return result.qips;
  }

  if (options.dryRun) {
    return buildOperationRequest(operationId, input, options);
  }

  const result = await executeOperation(operationId, input, {
    authorization: options.authorization,
    fetchImpl: runtime.fetchImpl,
  });

  return selectOutput(result, options);
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  try {
    const output = await runIqiyiCli(process.argv.slice(2));
    if (typeof output === "string") {
      console.log(output);
    } else {
      console.log(JSON.stringify(output, null, 2));
    }
  } catch (error) {
    console.error(error.message);
    process.exit(1);
  }
}
