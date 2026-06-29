import assert from "node:assert/strict";
import { test } from "node:test";

import {
  buildImagePayload,
  buildHttpErrorMessage,
  checkSkillUpdate,
  compareVersions,
  createImageTask,
  extractTaskFailureSummary,
  extractTaskId,
  extractImageOutputs,
  normalizeModel,
  normalizeAspectRatio,
  resolveConfig,
} from "../scripts/lib/gpt-image-2.mjs";

test("builds the HiAPI task payload for gpt-image-2", () => {
  const payload = buildImagePayload({
    prompt: "Create a product poster",
    aspectRatio: "16:9",
    resolution: "1K",
  });

  assert.deepEqual(payload, {
    model: "gpt-image-2",
    input: {
      prompt: "Create a product poster",
      aspect_ratio: "16:9",
      resolution: "1K",
    },
  });
});

test("builds GPT Image 2 image-to-image task payloads with input_urls", () => {
  const payload = buildImagePayload({
    model: "gpt-image-2-image-to-image-pro",
    prompt: "Restyle this product photo as a premium catalog image",
    inputUrls: ["https://example.com/reference-1.png", "https://example.com/reference-2.png"],
    aspectRatio: "auto",
    resolution: "2K",
  });

  assert.deepEqual(payload, {
    model: "gpt-image-2-image-to-image-pro",
    input: {
      prompt: "Restyle this product photo as a premium catalog image",
      input_urls: ["https://example.com/reference-1.png", "https://example.com/reference-2.png"],
      aspect_ratio: "auto",
      resolution: "2K",
    },
  });
});

test("validates GPT Image 2 model variants and image-to-image inputs", () => {
  assert.equal(normalizeModel("gpt-image-2"), "gpt-image-2");
  assert.equal(normalizeModel("gpt-image-2-pro"), "gpt-image-2-pro");
  assert.equal(normalizeModel("gpt-image-2-image-to-image"), "gpt-image-2-image-to-image");
  assert.equal(normalizeModel("gpt-image-2-image-to-image-pro"), "gpt-image-2-image-to-image-pro");
  assert.throws(() => normalizeModel("gpt-image-2-beta"), /Unsupported model/);
  assert.throws(
    () => buildImagePayload({
      model: "gpt-image-2-image-to-image",
      prompt: "Restyle this",
      inputUrls: [],
    }),
    /requires 1-5 input image URLs/,
  );
  assert.throws(
    () => buildImagePayload({
      model: "gpt-image-2-image-to-image-pro",
      prompt: "Restyle this",
      inputUrls: Array.from({ length: 6 }, (_, index) => `https://example.com/${index}.png`),
    }),
    /requires 1-5 input image URLs/,
  );
});

test("accepts the current GPT Image 2 aspect ratio set", () => {
  assert.equal(normalizeAspectRatio("2:1"), "2:1");
  assert.equal(normalizeAspectRatio("9:21"), "9:21");
  assert.throws(() => normalizeAspectRatio("10:7"), /Unsupported aspect ratio/);
});

test("extracts task ids and image outputs from task responses", () => {
  assert.equal(extractTaskId({ data: { taskId: "tk-hiapi-123" } }), "tk-hiapi-123");
  assert.equal(extractTaskId({ task_id: "task_456" }), "task_456");

  assert.deepEqual(
    extractImageOutputs({
      data: {
        output: [
          { type: "image", url: "https://cdn.example.com/out.png" },
          { type: "image", data: "data:image/png;base64,AAA" },
        ],
      },
    }),
    [
      { kind: "url", value: "https://cdn.example.com/out.png" },
      { kind: "data-uri", mimeType: "image/png", value: "data:image/png;base64,AAA" },
    ],
  );
});

test("extracts task failure reason from failed task detail instead of outer success message", () => {
  assert.equal(
    extractTaskFailureSummary({
      code: 200,
      message: "success",
      data: {
        status: "fail",
        taskId: "tk-hiapi-failed",
        error: {
          code: "TASK_FAILED",
          message: "task failed",
        },
      },
    }),
    "TASK_FAILED: task failed",
  );
});

test("creates image tasks through the unified tasks endpoint", async () => {
  let requestedUrl = "";
  let requestedInit = {};
  const fetchImpl = async (url, init) => {
    requestedUrl = url;
    requestedInit = init;
    return new Response(JSON.stringify({ data: { taskId: "tk-hiapi-123" } }), {
      status: 200,
    });
  };

  const payload = buildImagePayload({ prompt: "Create a poster", aspectRatio: "1:1" });
  const response = await createImageTask(payload, {
    config: { apiKey: "test-key", baseUrl: "https://api.hiapi.ai" },
    fetchImpl,
  });

  assert.equal(requestedUrl, "https://api.hiapi.ai/v1/tasks");
  assert.equal(requestedInit.method, "POST");
  assert.equal(requestedInit.headers.Authorization, "Bearer test-key");
  assert.deepEqual(JSON.parse(requestedInit.body), payload);
  assert.equal(extractTaskId(response), "tk-hiapi-123");
});

test("keeps markdown image extraction for legacy responses", () => {
  const response = {
    choices: [
      {
        message: {
          content:
            "Result: ![image](data:image/png;base64,AAA) and ![alt](https://cdn.example.com/out.png)",
        },
      },
    ],
  };

  assert.deepEqual(extractImageOutputs(response), [
    { kind: "data-uri", mimeType: "image/png", value: "data:image/png;base64,AAA" },
    { kind: "url", value: "https://cdn.example.com/out.png" },
  ]);
});

test("resolveConfig requires HIAPI_API_KEY and normalizes base URL", () => {
  assert.throws(
    () => resolveConfig({}),
    /Get one at https:\/\/www\.hiapi\.ai\/en\/register/,
  );

  assert.deepEqual(
    resolveConfig({
      HIAPI_API_KEY: "test-key",
      HIAPI_BASE_URL: "https://api.hiapi.ai/",
    }),
    {
      apiKey: "test-key",
      baseUrl: "https://api.hiapi.ai",
    },
  );
});

test("buildHttpErrorMessage guides users to configure a HiAPI API key", () => {
  const message = buildHttpErrorMessage(401, {
    error: { message: "Invalid API key" },
  });

  assert.match(message, /HTTP 401/);
  assert.match(message, /API key/);
  assert.match(message, /https:\/\/www\.hiapi\.ai\/en\/register/);
});

test("buildHttpErrorMessage guides users to add credits when balance is insufficient", () => {
  const message = buildHttpErrorMessage(402, {
    error: { message: "insufficient balance" },
  });

  assert.match(message, /HTTP 402/);
  assert.match(message, /balance|credits/i);
  assert.match(message, /https:\/\/www\.hiapi\.ai\/en\/dashboard/);
});

test("buildHttpErrorMessage handles rate limits and content policy errors", () => {
  assert.match(
    buildHttpErrorMessage(429, { error: { message: "Too many requests" } }),
    /wait and retry/i,
  );

  assert.match(
    buildHttpErrorMessage(400, {
      error: { message: "content_policy_violation" },
    }),
    /revise the prompt/i,
  );
});

test("compares semver-like skill versions", () => {
  assert.equal(compareVersions("0.1.0", "0.1.0"), 0);
  assert.equal(compareVersions("0.2.0", "0.1.9"), 1);
  assert.equal(compareVersions("0.1.0", "0.2.0"), -1);
});

test("checks skill update policy without affecting current versions", async () => {
  const fetchImpl = async () => new Response(JSON.stringify({
    skills: [{
      id: "hiapi-gpt-image-2",
      version: "0.1.0",
      updatePolicy: {
        latestVersion: "0.1.0",
        minimumVersion: "0.1.0",
        updateCommand: "npx -y github:HiAPIAI/hiapi-gpt-image-2-skill -y",
        notice: "New version available.",
        requiredNotice: "Update required.",
      },
    }],
  }), { status: 200 });

  assert.equal((await checkSkillUpdate({ fetchImpl })).status, "current");
});

test("reports soft and required skill updates from the manifest", async () => {
  const manifest = {
    skills: [{
      id: "hiapi-gpt-image-2",
      version: "0.3.0",
      updatePolicy: {
        latestVersion: "0.3.0",
        minimumVersion: "0.2.0",
        updateCommand: "npx -y github:HiAPIAI/hiapi-gpt-image-2-skill -y",
        notice: "New version available.",
        requiredNotice: "Update required.",
      },
    }],
  };
  const fetchImpl = async () => new Response(JSON.stringify(manifest), { status: 200 });

  const required = await checkSkillUpdate({ currentVersion: "0.1.0", fetchImpl });
  assert.equal(required.status, "required");
  assert.match(required.message, /Update required/);
  assert.match(required.message, /Update now: npx -y github:HiAPIAI\/hiapi-gpt-image-2-skill -y/);

  const available = await checkSkillUpdate({ currentVersion: "0.2.0", fetchImpl });
  assert.equal(available.status, "available");
  assert.match(available.message, /New version available/);
});

test("enforces documented cross-field constraints for non-pro models", () => {
  assert.throws(
    () => buildImagePayload({ prompt: "p", aspectRatio: "auto", resolution: "2K" }),
    /aspect_ratio "auto" only supports resolution "1K"/,
  );
  assert.throws(
    () => buildImagePayload({ prompt: "p", aspectRatio: "1:1", resolution: "4K" }),
    /cannot be combined with resolution "4K"/,
  );
  assert.throws(
    () => buildImagePayload({
      model: "gpt-image-2-image-to-image",
      prompt: "p",
      inputUrls: ["https://example.com/a.png"],
      aspectRatio: "auto",
      resolution: "4K",
    }),
    /aspect_ratio "auto" only supports resolution "1K"/,
  );

  // Allowed combinations still pass.
  assert.equal(buildImagePayload({ prompt: "p", aspectRatio: "auto", resolution: "1K" }).input.resolution, "1K");
  assert.equal(buildImagePayload({ prompt: "p", aspectRatio: "1:1", resolution: "2K" }).input.resolution, "2K");
  assert.equal(buildImagePayload({ prompt: "p", aspectRatio: "16:9", resolution: "4K" }).input.resolution, "4K");
  // Pro models are not subject to the auto/4K rules (auto+2K is a documented pro i2i combo).
  assert.equal(
    buildImagePayload({
      model: "gpt-image-2-image-to-image-pro",
      prompt: "p",
      inputUrls: ["https://example.com/a.png"],
      aspectRatio: "auto",
      resolution: "2K",
    }).input.resolution,
    "2K",
  );
});
