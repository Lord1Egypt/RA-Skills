import test from "node:test";
import assert from "node:assert/strict";

import {
  getVideoErrorMessage,
  getVideoPollDelay,
  getVideoRequestId,
  getVideoStatusValue,
  shouldUseJsonOutput,
} from "../src/cli.js";

test("shouldUseJsonOutput respects configured json output", () => {
  assert.equal(shouldUseJsonOutput("json"), true);
  assert.equal(shouldUseJsonOutput("text"), false);
  assert.equal(shouldUseJsonOutput(undefined), false);
});

test("getVideoRequestId prefers requestId over runId", () => {
  assert.equal(
    getVideoRequestId({
      requestId: "req_123",
      runId: "run_123",
    }),
    "req_123",
  );
});

test("getVideoPollDelay clamps to the remaining timeout budget", () => {
  assert.equal(getVideoPollDelay(1000, 5000, 1500), 500);
  assert.equal(getVideoPollDelay(1500, 5000, 1500), 0);
  assert.equal(getVideoPollDelay(200, 5000), 5000);
});

test("video status helpers read nested data fields", () => {
  const status = {
    data: {
      status: "FAILED",
      userFriendlyError: "render failed",
      output: {
        video: {
          url: "https://cdn.example/video.mp4",
        },
      },
    },
  };

  assert.equal(getVideoStatusValue(status), "FAILED");
  assert.equal(getVideoErrorMessage(status), "render failed");
});
