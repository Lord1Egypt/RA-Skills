import { readFileSync, statSync } from "node:fs";

export const MAX_DEPLOY_HTML_BYTES = 64 * 1024 * 1024;

const SAFE_REFERENCE = /^(?:https?:|data:|mailto:|tel:|#|\/\/)/i;

function isLocalReference(value) {
  const ref = value.trim();
  return ref.length > 0 && !SAFE_REFERENCE.test(ref);
}

function srcsetReferences(value) {
  const refs = [];
  let index = 0;
  while (index < value.length) {
    while (index < value.length && (value[index] === "," || /\s/.test(value[index]))) {
      index += 1;
    }
    if (index >= value.length) break;

    const start = index;
    const isData = value.slice(index, index + 5).toLowerCase() === "data:";
    while (
      index < value.length &&
      !/\s/.test(value[index]) &&
      (isData || value[index] !== ",")
    ) {
      index += 1;
    }
    refs.push(value.slice(start, index));

    while (index < value.length && value[index] !== ",") index += 1;
    if (value[index] === ",") index += 1;
  }
  return refs;
}

export function hasLocalAssetReference(html) {
  const attributePattern =
    /\b(srcset|src|href|poster)\s*=\s*(?:(["'])([\s\S]*?)\2|([^\s"'`=<>]+))/gi;
  for (const match of html.matchAll(attributePattern)) {
    const name = match[1].toLowerCase();
    const value = match[3] ?? match[4] ?? "";
    const refs = name === "srcset" ? srcsetReferences(value) : [value];
    if (refs.some(isLocalReference)) return true;
  }

  const cssUrlPattern = /\burl\(\s*(?:(["'])([\s\S]*?)\1|([^)"]*?))\s*\)/gi;
  for (const match of html.matchAll(cssUrlPattern)) {
    if (isLocalReference(match[2] ?? match[3] ?? "")) return true;
  }

  const cssImportPattern = /@import\s+(["'])([\s\S]*?)\1/gi;
  for (const match of html.matchAll(cssImportPattern)) {
    if (isLocalReference(match[2] ?? "")) return true;
  }
  return false;
}

try {
  const inputPath = process.argv[2];
  if (!inputPath) throw new Error("missing HTML path");
  const inputBytes = statSync(inputPath).size;
  if (inputBytes > MAX_DEPLOY_HTML_BYTES) {
    console.error(
      `error: deck HTML is too large for safe asset inspection (max ${MAX_DEPLOY_HTML_BYTES} bytes)`,
    );
    process.exitCode = 2;
  } else {
    process.exitCode = hasLocalAssetReference(readFileSync(inputPath, "utf8")) ? 0 : 1;
  }
} catch (error) {
  const detail = error instanceof Error ? `: ${error.message}` : "";
  console.error(`error: could not safely inspect deck HTML${detail}`);
  process.exitCode = 2;
}
