import assert from "node:assert/strict";
import { test } from "node:test";

import {
  buildHttpErrorMessage,
  buildVideoPayload,
  checkSkillUpdate,
  compareVersions,
  extractTaskId,
  extractTaskFailureSummary,
  extractVideoUrl,
  normalizeResolution,
  normalizeSeconds,
  normalizeSeed,
  normalizeSize,
  resolveConfig,
  saveVideoOutput,
} from "../scripts/lib/happyhorse-1-video.mjs";

test("builds the HiAPI video payload for HappyHorse 1.0 text-to-video", () => {
  assert.deepEqual(
    buildVideoPayload({
      prompt: "A wuxia swordswoman leaps across temple rooftops at dusk",
      seconds: "5",
      resolution: "1080p",
      size: "16:9",
    }),
    {
      model: "happyhorse-1-0",
      input: {
        prompt: "A wuxia swordswoman leaps across temple rooftops at dusk",
        duration: 5,
        resolution: "1080p",
        aspect_ratio: "16:9",
      },
    },
  );
});

test("validates duration, resolution, and size before sending a request", () => {
  assert.equal(normalizeSeconds("3"), "3");
  assert.equal(normalizeSeconds("4"), "4");
  assert.equal(normalizeSeconds(15), "15");
  assert.throws(() => normalizeSeconds("2"), /Unsupported duration/);
  assert.throws(() => normalizeSeconds("16"), /Unsupported duration/);

  assert.equal(normalizeResolution("720p"), "720p");
  assert.equal(normalizeResolution("1080P"), "1080p");
  assert.throws(() => normalizeResolution("480p"), /Unsupported resolution/);

  assert.equal(normalizeSize("9:16"), "9:16");
  assert.throws(() => normalizeSize("21:9"), /Unsupported size/);
});

test("supports optional seed for reproducible HappyHorse generations", () => {
  const payload = buildVideoPayload({
    prompt: "A product teaser with cinematic lighting",
    seed: "12345",
  });

  assert.equal(payload.input.seed, 12345);
  assert.equal(normalizeSeed(0), 0);
  assert.equal(normalizeSeed(2147483647), 2147483647);
  assert.equal(normalizeSeed(""), undefined);
  assert.throws(() => normalizeSeed("-1"), /Unsupported seed/);
  assert.throws(() => normalizeSeed("2147483648"), /Unsupported seed/);
});

test("supports ratio as an alias for the API size field", () => {
  const payload = buildVideoPayload({
    prompt: "A product teaser with cinematic lighting",
    ratio: "1:1",
  });

  assert.equal(payload.input.aspect_ratio, "1:1");
});

test("extracts task ids and video URLs from common HiAPI response shapes", () => {
  assert.equal(extractTaskId({ data: { taskId: "tk-hiapi-123" } }), "tk-hiapi-123");
  assert.equal(extractTaskId({ id: "video_task_123" }), "video_task_123");
  assert.equal(extractTaskId({ task_id: "task_456" }), "task_456");

  assert.equal(
    extractVideoUrl({ data: { output: [{ type: "video", url: "https://cdn.example.com/out.mp4" }] } }),
    "https://cdn.example.com/out.mp4",
  );
  assert.equal(
    extractVideoUrl({ metadata: { url: "https://cdn.example.com/meta.mp4" } }),
    "https://cdn.example.com/meta.mp4",
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

test("buildHttpErrorMessage gives next actions for key, balance, invalid request, rate, and task failures", () => {
  assert.match(
    buildHttpErrorMessage(401, { error: { message: "Invalid API key" } }),
    /create a new one: https:\/\/www\.hiapi\.ai\/en\/register/,
  );
  assert.match(
    buildHttpErrorMessage(403, { error: { message: "token quota is not enough" } }),
    /balance or credits may be insufficient/i,
  );
  assert.match(
    buildHttpErrorMessage(400, { error: { message: "invalid size" } }),
    /duration, resolution, size, and seed/i,
  );
  assert.match(
    buildHttpErrorMessage(429, { error: { message: "Too many requests" } }),
    /wait and retry/i,
  );
  assert.match(
    buildHttpErrorMessage(500, { error: { message: "task failed" } }),
    /try a clearer prompt/i,
  );
});

test("returns null when remote video download fails", async () => {
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async () => {
    throw new Error("fetch failed");
  };

  try {
    assert.equal(await saveVideoOutput("https://cdn.example.com/out.mp4"), null);
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test("compares semver-like skill versions", () => {
  assert.equal(compareVersions("0.1.0", "0.1.0"), 0);
  assert.equal(compareVersions("0.2.0", "0.1.9"), 1);
  assert.equal(compareVersions("0.1.0", "0.2.0"), -1);
});

test("reports soft and required skill updates from the manifest", async () => {
  const manifest = {
    skills: [{
      id: "hiapi-happyhorse-1-0-video",
      version: "0.3.0",
      updatePolicy: {
        latestVersion: "0.3.0",
        minimumVersion: "0.2.0",
        updateCommand: "npx -y github:HiAPIAI/hiapi-happyhorse-1-0-video-skill -y",
        notice: "New version available.",
        requiredNotice: "Update required.",
      },
    }],
  };
  const fetchImpl = async () => new Response(JSON.stringify(manifest), { status: 200 });

  const required = await checkSkillUpdate({ currentVersion: "0.1.0", fetchImpl });
  assert.equal(required.status, "required");
  assert.match(required.message, /Update required/);
  assert.match(required.message, /Update now: npx -y github:HiAPIAI\/hiapi-happyhorse-1-0-video-skill -y/);

  const available = await checkSkillUpdate({ currentVersion: "0.2.0", fetchImpl });
  assert.equal(available.status, "available");
  assert.match(available.message, /New version available/);
});
