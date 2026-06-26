import test from "node:test";
import assert from "node:assert/strict";
import { cleanLosslessLines } from "../src/pipeline/clean-lossless-lines.js";

test("cleanLosslessLines removes tool payloads, paths, and code vomit", () => {
  const cleaned = cleanLosslessLines([
    '{"type":"toolCall","id":"abc"}',
    'partialJson: {"foo":"bar"}',
    'Created: /home/adminul/.openclaw/workspace/openclaw-mindkeeper/src/index.js',
    '/home/adminul/.openclaw/workspace/openclaw-mindkeeper/src/delivery/build-email-message.js',
    'Final user request at end of segment: trimitemi mie mailul',
    'We decided the final product name is Mindkeeper.',
    'Remaining open loop: improve LCM scoping for the real day brief.',
  ]);

  assert.deepEqual(cleaned, [
    'We decided the final product name is Mindkeeper.',
    'Remaining open loop: improve LCM scoping for the real day brief.',
  ]);
});
