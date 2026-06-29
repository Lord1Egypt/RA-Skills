#!/usr/bin/env node

import { readFile } from "node:fs/promises";
import { request } from "node:https";
import { parseArgs } from "node:util";

const TTL_VALUES = new Set(["1h", "1d", "3d", "once"]);
const CUSTOM_PATH_PATTERN = /^[a-z0-9](?:[a-z0-9-]{1,61}[a-z0-9])$/;
const API_URL = "https://pagedrop.io/api/upload";

function fail(message) {
  console.error(`PageDrop upload failed: ${message}`);
  process.exit(1);
}

function postJson(url, body) {
  const requestBody = JSON.stringify(body);

  return new Promise((resolve, reject) => {
    const uploadRequest = request(
      url,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Content-Length": Buffer.byteLength(requestBody),
          "User-Agent": "make-html-pagedrop-uploader/1.2",
        },
      },
      (uploadResponse) => {
        const chunks = [];
        uploadResponse.setEncoding("utf8");
        uploadResponse.on("data", (chunk) => chunks.push(chunk));
        uploadResponse.on("end", () => {
          const status = uploadResponse.statusCode ?? 0;
          resolve({
            ok: status >= 200 && status < 300,
            status,
            text: chunks.join(""),
          });
        });
      },
    );

    uploadRequest.setTimeout(30_000, () => uploadRequest.destroy(new Error("request timed out")));
    uploadRequest.on("error", reject);
    uploadRequest.end(requestBody);
  });
}

let values;
let positionals;

try {
  ({ values, positionals } = parseArgs({
    allowPositionals: true,
    options: {
      ttl: { type: "string", default: "1h" },
      "custom-path": { type: "string" },
      "password-env": { type: "string" },
    },
  }));
} catch (error) {
  fail(error instanceof Error ? error.message : String(error));
}

if (positionals.length !== 1) {
  fail(
    "usage: node scripts/pagedrop-upload.mjs <file.html> [--ttl 1h|1d|3d|once] [--custom-path slug] [--password-env NAME]",
  );
}

if (!TTL_VALUES.has(values.ttl)) {
  fail(`unsupported TTL "${values.ttl}"; use 1h, 1d, 3d, or once`);
}

const customPath = values["custom-path"];

if (customPath && !CUSTOM_PATH_PATTERN.test(customPath)) {
  fail("custom path must be 3-63 lowercase letters, numbers, or hyphens with no edge hyphens");
}

const passwordEnvironmentVariable = values["password-env"];
const password = passwordEnvironmentVariable
  ? process.env[passwordEnvironmentVariable]
  : undefined;

if (passwordEnvironmentVariable && password === undefined) {
  fail(`password environment variable "${passwordEnvironmentVariable}" is not set`);
}

if (password !== undefined && (password.length === 0 || password.length > 128)) {
  fail("password must be 1-128 characters");
}

let html;

try {
  html = await readFile(positionals[0], "utf8");
} catch (error) {
  fail(error instanceof Error ? error.message : String(error));
}

if (!html.trim()) {
  fail("the HTML file is empty");
}

let response;
const requestPayload = { html, ttl: values.ttl };

if (customPath) {
  requestPayload.customPath = customPath;
}

if (password !== undefined) {
  requestPayload.password = password;
}

try {
  response = await postJson(API_URL, requestPayload);
} catch (error) {
  fail(error instanceof Error ? error.message : String(error));
}

const responseText = response.text;
let responsePayload;

try {
  responsePayload = JSON.parse(responseText);
} catch {
  responsePayload = null;
}

const url = responsePayload?.data?.url ?? responsePayload?.url ?? responsePayload?.link;

if (!response.ok || !url) {
  const message =
    responsePayload?.error?.message ??
    responsePayload?.error ??
    responsePayload?.message ??
    (responseText.trim() || `HTTP ${response.status}`);
  fail(String(message));
}

console.log(url);
