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
  normalizeMediaOptions,
  normalizeRatio,
  normalizeResolution,
  normalizeSeconds,
  parseArgs,
  resolveConfig,
  saveVideoOutput,
} from "../scripts/lib/seedance-2-video.mjs";

test("builds the HiAPI video payload for Seedance 2.0 text-to-video", () => {
  assert.deepEqual(
    buildVideoPayload({
      prompt: "A cinematic ocean cliff shot at golden hour",
      seconds: "5",
      resolution: "720p",
      ratio: "16:9",
    }),
    {
      model: "seedance-2-0",
      input: {
        prompt: "A cinematic ocean cliff shot at golden hour",
        duration: 5,
        resolution: "720p",
        aspect_ratio: "16:9",
      },
    },
  );
});

test("adds input_reference only when an image is provided", () => {
  const payload = buildVideoPayload({
    prompt: "Make this product photo move with soft studio lighting",
    inputReference: "https://example.com/product.png",
  });

  assert.equal(payload.model, "seedance-2-0");
  assert.equal(payload.input.duration, 5);
  assert.equal(payload.input.resolution, "720p");
  assert.equal(payload.input.aspect_ratio, "16:9");
  assert.equal(payload.input.first_frame_url, "https://example.com/product.png");
  assert.equal("generate_audio" in payload.input, false);
});

test("supports first and last frame image-to-video mode", () => {
  const payload = buildVideoPayload({
    prompt: "Move from the first frame to the final product hero shot",
    firstFrameUrl: "asset://first",
    lastFrameUrl: "asset://last",
    resolution: "1080p",
    ratio: "adaptive",
  });

  assert.equal(payload.input.first_frame_url, "asset://first");
  assert.equal(payload.input.last_frame_url, "asset://last");
  assert.equal(payload.input.resolution, "1080p");
  assert.equal(payload.input.aspect_ratio, "adaptive");
});

test("supports multimodal reference mode with validation durations", () => {
  const payload = buildVideoPayload({
    prompt: "Use the product images, motion reference, and audio reference to create a commercial",
    referenceImageUrls: ["asset://image-1", "asset://image-2"],
    referenceVideoUrls: ["asset://video-1", "asset://video-2"],
    referenceVideoDurations: [6, 7],
    referenceAudioUrls: ["asset://audio-1"],
    referenceAudioDurations: [10],
    returnLastFrame: true,
    webSearch: true,
    nsfwChecker: true,
  });

  assert.deepEqual(payload.input.reference_image_urls, ["asset://image-1", "asset://image-2"]);
  assert.deepEqual(payload.input.reference_video_urls, ["asset://video-1", "asset://video-2"]);
  assert.deepEqual(payload.input.reference_audio_urls, ["asset://audio-1"]);
  assert.equal(payload.input.return_last_frame, true);
  assert.equal(payload.input.web_search, true);
  assert.equal(payload.input.nsfw_checker, true);
});

test("rejects mutually exclusive Seedance media modes", () => {
  assert.throws(
    () => buildVideoPayload({
      prompt: "Invalid mix",
      firstFrameUrl: "asset://first",
      referenceImageUrls: ["asset://ref"],
    }),
    /mutually exclusive/i,
  );
  assert.throws(
    () => buildVideoPayload({
      prompt: "Last only",
      lastFrameUrl: "asset://last",
    }),
    /requires a first frame/i,
  );
});

test("validates Seedance reference material limits", () => {
  assert.throws(
    () => normalizeMediaOptions({
      referenceImageUrls: Array.from({ length: 10 }, (_, index) => `asset://image-${index}`),
    }),
    /at most 9 images/i,
  );
  assert.throws(
    () => normalizeMediaOptions({
      referenceVideoUrls: ["asset://v1", "asset://v2", "asset://v3", "asset://v4"],
      referenceVideoDurations: [3, 3, 3, 3],
    }),
    /at most 3 reference videos/i,
  );
  assert.throws(
    () => normalizeMediaOptions({
      referenceAudioUrls: ["asset://a1", "asset://a2", "asset://a3", "asset://a4"],
      referenceAudioDurations: [3, 3, 3, 3],
    }),
    /at most 3 reference audio/i,
  );
});

test("validates Seedance reference video and audio durations", () => {
  assert.throws(
    () => normalizeMediaOptions({
      referenceVideoUrls: ["asset://v1"],
    }),
    /reference-video-duration/i,
  );
  assert.throws(
    () => normalizeMediaOptions({
      referenceVideoUrls: ["asset://v1"],
      referenceVideoDurations: [1],
    }),
    /must be 2-15 seconds/i,
  );
  assert.throws(
    () => normalizeMediaOptions({
      referenceAudioUrls: ["asset://a1", "asset://a2"],
      referenceAudioDurations: [8, 8],
    }),
    /total duration must not exceed 15 seconds/i,
  );
});

test("validates duration, resolution, and ratio before sending a request", () => {
  assert.equal(normalizeSeconds("4"), "4");
  assert.equal(normalizeSeconds(15), "15");
  assert.throws(() => normalizeSeconds("3"), /Unsupported duration/);
  assert.throws(() => normalizeSeconds("16"), /Unsupported duration/);

  assert.equal(normalizeResolution("480p"), "480p");
  assert.equal(normalizeResolution("720P"), "720p");
  assert.equal(normalizeResolution("1080P"), "1080p");

  assert.equal(normalizeRatio("9:16"), "9:16");
  assert.equal(normalizeRatio("adaptive"), "adaptive");
  assert.throws(() => normalizeRatio("2:1"), /Unsupported ratio/);
});

test("parses repeatable multimodal reference arguments", () => {
  assert.deepEqual(
    parseArgs([
      "--prompt", "Use refs",
      "--reference-image-url", "asset://i1,asset://i2",
      "--reference-video-url", "asset://v1",
      "--reference-video-duration", "6",
      "--reference-audio-url", "asset://a1",
      "--reference-audio-duration", "4",
      "--return-last-frame",
      "--web-search",
      "--nsfw-checker",
    ]),
    {
      prompt: "Use refs",
      referenceImageUrls: ["asset://i1,asset://i2"],
      referenceVideoUrls: ["asset://v1"],
      referenceVideoDurations: ["6"],
      referenceAudioUrls: ["asset://a1"],
      referenceAudioDurations: ["4"],
      returnLastFrame: true,
      webSearch: true,
      nsfwChecker: true,
    },
  );
});

test("supports generate_audio tri-state: omitted by default, explicit true/false", () => {
  const omitted = buildVideoPayload({
    prompt: "A coffee shop scene with natural background sound",
  });
  assert.equal("generate_audio" in omitted.input, false);

  const enabled = buildVideoPayload({
    prompt: "A coffee shop scene with natural background sound",
    generateAudio: true,
  });
  assert.equal(enabled.input.generate_audio, true);

  const disabled = buildVideoPayload({
    prompt: "A silent product rotation",
    generateAudio: false,
  });
  assert.equal(disabled.input.generate_audio, false);
});

test("supports seed for reproducible generation and validates its range", () => {
  const payload = buildVideoPayload({
    prompt: "A repeatable shot",
    seed: "12345",
  });
  assert.equal(payload.input.seed, 12345);

  const omitted = buildVideoPayload({ prompt: "Random shot" });
  assert.equal("seed" in omitted.input, false);

  assert.throws(() => buildVideoPayload({ prompt: "Bad seed", seed: "-1" }), /Unsupported seed/);
  assert.throws(() => buildVideoPayload({ prompt: "Bad seed", seed: "2147483648" }), /Unsupported seed/);
  assert.throws(() => buildVideoPayload({ prompt: "Bad seed", seed: "1.5" }), /Unsupported seed/);
});

test("parses audio flags and seed from CLI arguments", () => {
  assert.deepEqual(parseArgs(["--prompt", "p", "--seed", "42"]), { prompt: "p", seed: "42" });
  assert.deepEqual(parseArgs(["--prompt", "p", "--generate-audio"]), { prompt: "p", generateAudio: true });
  assert.deepEqual(parseArgs(["--prompt", "p", "--no-audio"]), { prompt: "p", generateAudio: false });
  assert.deepEqual(parseArgs(["--prompt", "p", "--no-generate-audio"]), { prompt: "p", generateAudio: false });
  assert.deepEqual(parseArgs(["--prompt", "p"]), { prompt: "p" });
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

test("buildHttpErrorMessage gives next actions for key, balance, image, rate, and task failures", () => {
  assert.match(
    buildHttpErrorMessage(401, { error: { message: "Invalid API key" } }),
    /create a new one: https:\/\/www\.hiapi\.ai\/en\/register/,
  );
  assert.match(
    buildHttpErrorMessage(402, { error: { message: "insufficient balance" } }),
    /balance or credits may be insufficient/i,
  );
  assert.match(
    buildHttpErrorMessage(403, { error: { message: "token quota is not enough" } }),
    /balance or credits may be insufficient/i,
  );
  assert.match(
    buildHttpErrorMessage(400, { error: { message: "input_reference is invalid" } }),
    /media mode, reference counts, and reference audio\/video durations/i,
  );
  assert.match(
    buildHttpErrorMessage(429, { error: { message: "Too many requests" } }),
    /wait and retry/i,
  );
  assert.match(
    buildHttpErrorMessage(500, { error: { message: "task failed" } }),
    /try a clearer prompt or a different image/i,
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
      id: "hiapi-seedance-2-0-video",
      version: "0.3.0",
      updatePolicy: {
        latestVersion: "0.3.0",
        minimumVersion: "0.2.0",
        updateCommand: "npx -y github:HiAPIAI/hiapi-seedance-2-0-video-skill -y",
        notice: "New version available.",
        requiredNotice: "Update required.",
      },
    }],
  };
  const fetchImpl = async () => new Response(JSON.stringify(manifest), { status: 200 });

  const required = await checkSkillUpdate({ currentVersion: "0.1.0", fetchImpl });
  assert.equal(required.status, "required");
  assert.match(required.message, /Update required/);
  assert.match(required.message, /Update now: npx -y github:HiAPIAI\/hiapi-seedance-2-0-video-skill -y/);

  const available = await checkSkillUpdate({ currentVersion: "0.2.0", fetchImpl });
  assert.equal(available.status, "available");
  assert.match(available.message, /New version available/);
});
