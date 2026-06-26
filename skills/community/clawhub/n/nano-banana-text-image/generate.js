#!/usr/bin/env node

/**
 * atlas-banana-textimage
 * Generates images from text prompts using the AtlasCloud Nanobanana model.
 *
 * Usage:
 *   node generate.js <TOKEN> <PARAMS_JSON_FILE>
 */

const https = require("https");
const http  = require("http");
const fs    = require("fs");
const path  = require("path");

const BASE_URL = "https://api.atlascloud.ai/api/v1";
const MODEL    = "google/nano-banana-2/text-to-image";

function log(...args) { console.log(...args); }

// ─── API request ──────────────────────────────────────────────────────────────

function apiRequest(url, method, apiKey, body) {
  return new Promise((resolve, reject) => {
    const parsed  = new URL(url);
    const lib     = parsed.protocol === "https:" ? https : http;
    const options = {
      hostname: parsed.hostname,
      path:     parsed.pathname + parsed.search,
      method,
      headers: {
        Authorization:  `Bearer ${apiKey}`,
        "Content-Type": "application/json",
      },
    };
    const req = lib.request(options, (res) => {
      let data = "";
      res.on("data", (c) => (data += c));
      res.on("end", () => {
        try   { resolve({ status: res.statusCode, body: JSON.parse(data) }); }
        catch { resolve({ status: res.statusCode, body: data }); }
      });
    });
    req.on("error", reject);
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

function sleep(ms) { return new Promise((r) => setTimeout(r, ms)); }

// ─── Step 1: Submit ───────────────────────────────────────────────────────────

async function createJob(params, apiKey) {
  // NOTE: never send media_resolution together with resolution — causes HTTP 500
  const payload = {
    model:                MODEL,
    prompt:               params.prompt,
    aspect_ratio:         params.aspect_ratio         ?? "16:9",
    enable_base64_output: params.enable_base64_output ?? false,
    enable_sync_mode:     params.enable_sync_mode     ?? false,
    enable_web_search:    params.enable_web_search    ?? false,
    enable_image_search:  params.enable_image_search  ?? false,
    output_format:        params.output_format        ?? "png",
    resolution:           params.resolution           ?? "2k",
  };

  log("Submitting request...");
  log(`Prompt: ${payload.prompt.substring(0, 80)}${payload.prompt.length > 80 ? "…" : ""}`);

  const res          = await apiRequest(`${BASE_URL}/model/generateImage`, "POST", apiKey, payload);
  const predictionId = res.body?.data?.id;

  if (!predictionId) {
    console.error("Failed to start job:", JSON.stringify(res.body, null, 2));
    process.exit(1);
  }

  log(`Job started: ${predictionId}`);
  return predictionId;
}

// ─── Step 2: Poll ─────────────────────────────────────────────────────────────

async function pollResult(predictionId, apiKey, maxAttempts = 60, intervalMs = 3000) {
  log("Polling for result...");

  for (let i = 1; i <= maxAttempts; i++) {
    await sleep(intervalMs);

    const res    = await apiRequest(`${BASE_URL}/model/prediction/${predictionId}`, "GET", apiKey);
    const data   = res.body?.data ?? res.body;
    const status = data?.status ?? "unknown";

    // Log the full GET response on every poll
    log(`Attempt ${i}/${maxAttempts} | status: ${status} | response: ${JSON.stringify(res.body)}`);

    if (status === "completed" || status === "succeeded") {
      const imageUrl = (data?.outputs ?? [])[0];
      if (!imageUrl) {
        console.error("Completed but no output URL:", JSON.stringify(res.body, null, 2));
        process.exit(1);
      }

      log("=".repeat(60));
      log("IMAGE_URL: " + imageUrl);
      log("=".repeat(60));

      return imageUrl;
    }

    if (status === "failed" || status === "error") {
      console.error("Job failed:", JSON.stringify(res.body, null, 2));
      process.exit(1);
    }
  }

  console.error(`Timed out after ${maxAttempts} attempts.`);
  process.exit(1);
}

// ─── Main ─────────────────────────────────────────────────────────────────────

async function main() {
  const apiKey     = process.argv[2];
  const paramsFile = process.argv[3];

  if (!apiKey) {
    console.error("Missing token. Usage: node generate.js <TOKEN> <PARAMS_JSON_FILE>");
    process.exit(1);
  }

  if (!paramsFile || !fs.existsSync(paramsFile)) {
    console.error("Missing or invalid params file. Usage: node generate.js <TOKEN> <PARAMS_JSON_FILE>");
    process.exit(1);
  }

  const params = JSON.parse(fs.readFileSync(paramsFile, "utf8"));

  if (!params.prompt) {
    console.error("'prompt' is required in params file.");
    process.exit(1);
  }

  const predictionId = await createJob(params, apiKey);
  const imageUrl     = await pollResult(predictionId, apiKey);

  // Save result files next to this script
  const resultPath = path.join(__dirname, "last_result.json");
  const urlPath    = path.join(__dirname, "last_url.txt");

  fs.writeFileSync(resultPath, JSON.stringify({
    prediction_id: predictionId,
    image_url:     imageUrl,
    timestamp:     new Date().toISOString(),
  }, null, 2));

  fs.writeFileSync(urlPath, imageUrl + "\n");

  log("Result saved to: " + resultPath);
  log("URL saved to:    " + urlPath);
}

main().catch((err) => {
  console.error("Unexpected error:", err.message);
  process.exit(1);
});
