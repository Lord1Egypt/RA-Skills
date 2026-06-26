import test from "node:test";
import assert from "node:assert/strict";

import { parseChatCompletionStream } from "../src/stream.js";

test("parseChatCompletionStream emits content chunks from SSE payloads", async () => {
  const encoder = new TextEncoder();
  const stream = new ReadableStream<Uint8Array>({
    start(controller) {
      controller.enqueue(
        encoder.encode(
          [
            'data: {"choices":[{"delta":{"content":"Hello"}}]}',
            "",
            'data: {"choices":[{"delta":{"content":" world"}}]}',
            "",
            "data: [DONE]",
            "",
          ].join("\n"),
        ),
      );
      controller.close();
    },
  });

  const chunks: string[] = [];
  for await (const chunk of parseChatCompletionStream(stream)) {
    chunks.push(chunk);
  }

  assert.deepEqual(chunks, ["Hello", " world"]);
});
