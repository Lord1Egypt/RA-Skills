import test from "node:test";
import assert from "node:assert/strict";

import { mergeConfig, redactConfig } from "../src/config.js";

test("mergeConfig applies precedence flags over env over file", () => {
  const resolved = mergeConfig(
    {
      apiKey: "file-key",
      defaultModel: "file-model",
      defaultImageModel: "file-image",
      defaultVideoModel: "file-video",
      outputFormat: "text",
      baseUrl: "https://file.example",
    },
    {
      NANO_GPT_API_KEY: "env-key",
      NANO_GPT_MODEL: "env-model",
      NANO_GPT_IMAGE_MODEL: "env-image",
      NANO_GPT_VIDEO_MODEL: "env-video",
      NANO_GPT_OUTPUT_FORMAT: "json",
      NANO_GPT_BASE_URL: "https://env.example/",
    },
    {
      apiKey: "flag-key",
      defaultModel: "flag-model",
    },
  );

  assert.equal(resolved.apiKey, "flag-key");
  assert.equal(resolved.defaultModel, "flag-model");
  assert.equal(resolved.defaultImageModel, "env-image");
  assert.equal(resolved.defaultVideoModel, "env-video");
  assert.equal(resolved.outputFormat, "json");
  assert.equal(resolved.baseUrl, "https://env.example");
});

test("redactConfig masks the stored API key", () => {
  const redacted = redactConfig({
    apiKey: "abcdefgh12345678",
  });

  assert.equal(redacted.apiKey, "abcd...5678");
});
