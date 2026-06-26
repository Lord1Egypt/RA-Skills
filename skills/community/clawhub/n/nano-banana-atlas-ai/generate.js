#!/usr/bin/env node

/**
 * atlas-banana-imagetoimage
 * Edits/combines images using the AtlasCloud Nanobanana Edit model.
 *
 * Usage:
 *   node generate.js <TOKEN> <PARAMS_JSON_FILE>
 */

const axios = require("axios");
const fs    = require("fs");
const path  = require("path");

const BASE_URL = "https://api.atlascloud.ai/api/v1";
const MODEL    = "google/nano-banana-2/edit";

function log(...args) { console.log(...args); }

function sleep(ms) { return new Promise((r) => setTimeout(r, ms)); }

// ─── Step 1: Submit ───────────────────────────────────────────────────────────

async function createJob(params, apiKey) {
  // NOTE: never send media_resolution together with resolution — causes HTTP 500
  const payload = {
    model:                MODEL,
    prompt:               params.prompt,
    images:               params.images,
    aspect_ratio:         params.aspect_ratio         ?? "16:9",
    enable_base64_output: params.enable_base64_output ?? false,
    enable_sync_mode:     params.enable_sync_mode     ?? false,
    enable_web_search:    params.enable_web_search    ?? false,
    enable_image_search:  params.enable_image_search  ?? false,
    output_format:        params.output_format        ?? "png",
    resolution:           params.resolution           ?? "1k",
  };

  log("Submitting request...");
  log(`Model  : ${MODEL}`);
  log(`Images : ${payload.images.length} URL(s)`);
  payload.images.forEach((u, i) => log(`  [${i}] ${u.substring(0, 80)}${u.length > 80 ? "…" : ""}`));
  log(`Prompt : ${payload.prompt.substring(0, 80)}${payload.prompt.length > 80 ? "…" : ""}`);

  const res = await axios.post(`${BASE_URL}/model/generateImage`, payload, {
    headers: { Authorization: `Bearer ${apiKey}`, "Content-Type": "application/json" },
  });

  const predictionId = res.data?.data?.id;
  if (!predictionId) {
    console.error("Failed to start job:", JSON.stringify(res.data, null, 2));
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

    const res    = await axios.get(`${BASE_URL}/model/prediction/${predictionId}`, {
      headers: { Authorization: `Bearer ${apiKey}` },
    });
    const data   = res.data?.data ?? res.data;
    const status = data?.status ?? "unknown";

    // Log the full GET response on every poll
    log(`Attempt ${i}/${maxAttempts} | status: ${status} | response: ${JSON.stringify(res.data)}`);

    if (status === "completed" || status === "succeeded") {
      const imageUrl = (data?.outputs ?? [])[0];
      if (!imageUrl) {
        console.error("Completed but no output URL:", JSON.stringify(res.data, null, 2));
        process.exit(1);
      }

      log("=".repeat(60));
      log("IMAGE_URL: " + imageUrl);
      log("=".repeat(60));

      return imageUrl;
    }

    if (status === "failed" || status === "error") {
      console.error("Job failed:", JSON.stringify(res.data, null, 2));
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
  if (!Array.isArray(params.images) || params.images.length < 1) {
    console.error("'images' must be an array with at least 1 URL.");
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
    images:        params.images,
  }, null, 2));

  fs.writeFileSync(urlPath, imageUrl + "\n");

  log("Result saved to: " + resultPath);
  log("URL saved to:    " + urlPath);
}

main().catch((err) => {
  const msg = err.response?.data ? JSON.stringify(err.response.data, null, 2) : err.message;
  console.error("Unexpected error:", msg);
  process.exit(1);
});
