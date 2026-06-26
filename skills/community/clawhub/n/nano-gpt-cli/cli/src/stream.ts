import { extractTextContent } from "./messages.js";
import type { ChatCompletionResponse } from "./types.js";

export async function* parseChatCompletionStream(
  stream: ReadableStream<Uint8Array>,
): AsyncGenerator<string> {
  const reader = stream.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) {
      buffer += decoder.decode();
      break;
    }

    buffer += decoder.decode(value, { stream: true });
    const parsed = consumeEvents(buffer);
    buffer = parsed.remaining;
    yield* parsed.chunks;
  }

  const final = consumeEvents(buffer, true);
  yield* final.chunks;
}

function consumeEvents(
  buffer: string,
  flush = false,
): { chunks: string[]; remaining: string } {
  const chunks: string[] = [];
  const separator = /\r?\n\r?\n/g;
  let lastIndex = 0;
  let match: RegExpExecArray | null;

  while ((match = separator.exec(buffer)) !== null) {
    const event = buffer.slice(lastIndex, match.index);
    lastIndex = separator.lastIndex;
    chunks.push(...parseEvent(event));
  }

  if (flush && lastIndex < buffer.length) {
    chunks.push(...parseEvent(buffer.slice(lastIndex)));
    return { chunks, remaining: "" };
  }

  return { chunks, remaining: buffer.slice(lastIndex) };
}

function parseEvent(event: string): string[] {
  const dataLines = event
    .split(/\r?\n/)
    .filter((line) => line.startsWith("data:"))
    .map((line) => line.slice(5).trim())
    .filter(Boolean);

  const chunks: string[] = [];
  for (const line of dataLines) {
    if (line === "[DONE]") {
      continue;
    }

    const payload = JSON.parse(line) as ChatCompletionResponse;
    const text = extractChunkText(payload);
    if (text) {
      chunks.push(text);
    }
  }

  return chunks;
}

function extractChunkText(payload: ChatCompletionResponse): string {
  const choice = payload.choices?.[0];
  return extractTextContent(choice?.delta?.content) || extractTextContent(choice?.message?.content);
}

