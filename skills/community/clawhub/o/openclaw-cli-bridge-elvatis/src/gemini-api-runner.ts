/**
 * gemini-api-runner.ts
 *
 * Direct Gemini API integration via @google/genai SDK.
 * Supports native text + image generation (responseModalities: ["TEXT", "IMAGE"]).
 *
 * Unlike CLI runners, this calls the Gemini API directly — no subprocess overhead.
 * Images are returned as base64 data URIs in OpenAI-compatible content_parts format.
 */

import { GoogleGenAI } from "@google/genai";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { homedir } from "node:os";
import type { ToolDefinition, ToolCall } from "./tool-protocol.js";
import { generateCallId } from "./tool-protocol.js";
import type { ChatMessage } from "./cli-runner.js";

// ──────────────────────────────────────────────────────────────────────────────
// Types
// ──────────────────────────────────────────────────────────────────────────────

export interface ContentPart {
  type: "text" | "image_url";
  text?: string;
  image_url?: { url: string };
}

export interface GeminiApiResult {
  /** String for text-only, array for multimodal (text + images) */
  content: string | ContentPart[];
  finishReason: string;
  promptTokens?: number;
  completionTokens?: number;
  tool_calls?: ToolCall[];
}

// ──────────────────────────────────────────────────────────────────────────────
// API Key resolution
// ──────────────────────────────────────────────────────────────────────────────

let cachedApiKey: string | null = null;

export function getApiKey(): string {
  if (cachedApiKey) return cachedApiKey;

  // 1. Environment variable
  if (process.env.GOOGLE_API_KEY) {
    cachedApiKey = process.env.GOOGLE_API_KEY;
    return cachedApiKey;
  }

  // 2. Read from OpenClaw .env file
  const envPath = join(homedir(), ".openclaw", ".env");
  try {
    const envContent = readFileSync(envPath, "utf-8");
    const match = envContent.match(/^GOOGLE_API_KEY=(.+)$/m);
    if (match?.[1]) {
      cachedApiKey = match[1].trim();
      return cachedApiKey;
    }
  } catch {
    // File not found — fall through
  }

  throw new Error(
    "GOOGLE_API_KEY not found. Set it as an environment variable or add it to ~/.openclaw/.env"
  );
}

/** Reset cached key (for testing). */
export function _resetApiKeyCache(): void {
  cachedApiKey = null;
}

// ──────────────────────────────────────────────────────────────────────────────
// Singleton client
// ──────────────────────────────────────────────────────────────────────────────

let client: GoogleGenAI | null = null;

function getClient(): GoogleGenAI {
  if (!client) {
    client = new GoogleGenAI({ apiKey: getApiKey() });
  }
  return client;
}

/** Reset client (for testing). */
export function _resetClient(): void {
  client = null;
}

// ──────────────────────────────────────────────────────────────────────────────
// Message conversion: OpenAI → Gemini
// ──────────────────────────────────────────────────────────────────────────────

interface GeminiContent {
  role: "user" | "model";
  parts: GeminiPart[];
}

type GeminiPart =
  | { text: string }
  | { inlineData: { mimeType: string; data: string } }
  | { functionCall: { name: string; args: Record<string, unknown> } }
  | { functionResponse: { name: string; response: Record<string, unknown> } };

/**
 * Convert OpenAI-format messages to Gemini API format.
 * System messages → systemInstruction. Tool results → functionResponse parts.
 */
export function convertMessages(messages: ChatMessage[]): {
  systemInstruction?: { parts: Array<{ text: string }> };
  contents: GeminiContent[];
} {
  const systemParts: Array<{ text: string }> = [];
  const contents: GeminiContent[] = [];

  for (const msg of messages) {
    const role = msg.role;

    if (role === "system") {
      const text = typeof msg.content === "string"
        ? msg.content
        : Array.isArray(msg.content)
          ? msg.content.map((p: Record<string, unknown>) => String(p.text ?? "")).join("\n")
          : "";
      if (text) systemParts.push({ text });
      continue;
    }

    if (role === "tool") {
      // Tool result → functionResponse
      const toolMsg = msg as ChatMessage & { tool_call_id?: string; name?: string };
      const name = toolMsg.name ?? toolMsg.tool_call_id ?? "unknown";
      const responseText = typeof msg.content === "string" ? msg.content : JSON.stringify(msg.content);
      let responseObj: Record<string, unknown>;
      try {
        responseObj = JSON.parse(responseText);
        if (typeof responseObj !== "object" || responseObj === null) {
          responseObj = { result: responseText };
        }
      } catch {
        responseObj = { result: responseText };
      }
      contents.push({
        role: "user",
        parts: [{ functionResponse: { name, response: responseObj } }],
      });
      continue;
    }

    // assistant → model, user → user
    const geminiRole: "user" | "model" = role === "assistant" ? "model" : "user";
    const parts: GeminiPart[] = [];

    // Handle tool_calls in assistant messages
    const assistantMsg = msg as ChatMessage & { tool_calls?: Array<{ function: { name: string; arguments: string } }> };
    if (assistantMsg.tool_calls?.length) {
      for (const tc of assistantMsg.tool_calls) {
        let args: Record<string, unknown> = {};
        try { args = JSON.parse(tc.function.arguments); } catch { /* empty */ }
        parts.push({ functionCall: { name: tc.function.name, args } });
      }
      if (typeof msg.content === "string" && msg.content) {
        parts.unshift({ text: msg.content });
      }
      contents.push({ role: geminiRole, parts });
      continue;
    }

    // Regular content
    if (typeof msg.content === "string") {
      if (msg.content) parts.push({ text: msg.content });
    } else if (Array.isArray(msg.content)) {
      for (const part of msg.content as Array<Record<string, unknown>>) {
        if (part.type === "text" && typeof part.text === "string") {
          parts.push({ text: part.text });
        } else if (part.type === "image_url") {
          const imageUrl = part.image_url as { url?: string } | undefined;
          const url = imageUrl?.url ?? "";
          const match = url.match(/^data:(image\/[\w+]+);base64,(.+)$/);
          if (match) {
            parts.push({ inlineData: { mimeType: match[1], data: match[2] } });
          } else if (url) {
            parts.push({ text: `[Image: ${url}]` });
          }
        }
      }
    }

    if (parts.length > 0) {
      contents.push({ role: geminiRole, parts });
    }
  }

  return {
    systemInstruction: systemParts.length > 0 ? { parts: systemParts } : undefined,
    contents,
  };
}

// ──────────────────────────────────────────────────────────────────────────────
// Tool conversion: OpenAI → Gemini
// ──────────────────────────────────────────────────────────────────────────────

export function convertTools(tools: ToolDefinition[]): Array<{
  functionDeclarations: Array<{
    name: string;
    description: string;
    parameters: Record<string, unknown>;
  }>;
}> {
  return [
    {
      functionDeclarations: tools.map((t) => ({
        name: t.function.name,
        description: t.function.description,
        parameters: t.function.parameters,
      })),
    },
  ];
}

// ──────────────────────────────────────────────────────────────────────────────
// Response parsing
// ──────────────────────────────────────────────────────────────────────────────

function parseResponseParts(
  parts: Array<Record<string, unknown>> | undefined
): { content: string | ContentPart[]; tool_calls?: ToolCall[] } {
  if (!parts?.length) return { content: "" };

  const textParts: string[] = [];
  const imageParts: ContentPart[] = [];
  const toolCalls: ToolCall[] = [];

  for (const part of parts) {
    if (typeof part.text === "string") {
      textParts.push(part.text);
    }
    if (part.inlineData) {
      const data = part.inlineData as { mimeType: string; data: string };
      imageParts.push({
        type: "image_url",
        image_url: { url: `data:${data.mimeType};base64,${data.data}` },
      });
    }
    if (part.functionCall) {
      const fc = part.functionCall as { name: string; args: Record<string, unknown> };
      toolCalls.push({
        id: generateCallId(),
        type: "function",
        function: {
          name: fc.name,
          arguments: JSON.stringify(fc.args ?? {}),
        },
      });
    }
  }

  if (toolCalls.length > 0) {
    return { content: textParts.join("") || null as unknown as string, tool_calls: toolCalls };
  }

  // Multimodal: text + images → content_parts array
  if (imageParts.length > 0) {
    const contentParts: ContentPart[] = [];
    const joinedText = textParts.join("");
    if (joinedText) contentParts.push({ type: "text", text: joinedText });
    contentParts.push(...imageParts);
    return { content: contentParts };
  }

  // Text-only
  return { content: textParts.join("") };
}

// ──────────────────────────────────────────────────────────────────────────────
// Non-streaming completion
// ──────────────────────────────────────────────────────────────────────────────

export interface GeminiApiOptions {
  model: string;
  timeoutMs?: number;
  tools?: ToolDefinition[];
  log?: (msg: string) => void;
}

export async function geminiApiComplete(
  messages: ChatMessage[],
  opts: GeminiApiOptions
): Promise<GeminiApiResult> {
  const ai = getClient();
  const modelId = stripPrefix(opts.model);
  const { systemInstruction, contents } = convertMessages(messages);

  const config: Record<string, unknown> = {};

  // Enable image generation for models that support it
  if (!opts.tools?.length) {
    config.responseModalities = ["TEXT", "IMAGE"];
  }

  const requestOpts: Record<string, unknown> = {
    model: modelId,
    contents,
    config: {
      ...config,
      ...(systemInstruction ? { systemInstruction } : {}),
      ...(opts.tools?.length ? { tools: convertTools(opts.tools) } : {}),
    },
  };

  opts.log?.(`[gemini-api] ${modelId} · non-streaming · tools=${opts.tools?.length ?? 0}`);

  const controller = new AbortController();
  const timer = opts.timeoutMs
    ? setTimeout(() => controller.abort(), opts.timeoutMs)
    : null;

  try {
    const response = await ai.models.generateContent(requestOpts as Parameters<typeof ai.models.generateContent>[0]);

    const candidate = response.candidates?.[0];
    const parts = candidate?.content?.parts as Array<Record<string, unknown>> | undefined;
    const parsed = parseResponseParts(parts);

    const finishReason = mapFinishReason(candidate?.finishReason as string);

    return {
      content: parsed.content,
      finishReason,
      promptTokens: response.usageMetadata?.promptTokenCount,
      completionTokens: response.usageMetadata?.candidatesTokenCount,
      tool_calls: parsed.tool_calls,
    };
  } finally {
    if (timer) clearTimeout(timer);
  }
}

// ──────────────────────────────────────────────────────────────────────────────
// Streaming completion
// ──────────────────────────────────────────────────────────────────────────────

export async function geminiApiCompleteStream(
  messages: ChatMessage[],
  opts: GeminiApiOptions,
  onToken: (token: string) => void
): Promise<GeminiApiResult> {
  const ai = getClient();
  const modelId = stripPrefix(opts.model);
  const { systemInstruction, contents } = convertMessages(messages);

  const config: Record<string, unknown> = {};

  // Image generation not supported in streaming — use text only
  // (Gemini streams text tokens but images arrive as complete blobs)

  const requestOpts: Record<string, unknown> = {
    model: modelId,
    contents,
    config: {
      ...config,
      ...(systemInstruction ? { systemInstruction } : {}),
      ...(opts.tools?.length ? { tools: convertTools(opts.tools) } : {}),
    },
  };

  opts.log?.(`[gemini-api] ${modelId} · streaming · tools=${opts.tools?.length ?? 0}`);

  const controller = new AbortController();
  const timer = opts.timeoutMs
    ? setTimeout(() => controller.abort(), opts.timeoutMs)
    : null;

  try {
    const stream = await ai.models.generateContentStream(requestOpts as Parameters<typeof ai.models.generateContentStream>[0]);

    let fullText = "";
    const allImageParts: ContentPart[] = [];
    const allToolCalls: ToolCall[] = [];
    let finishReason = "stop";
    let promptTokens: number | undefined;
    let completionTokens: number | undefined;

    for await (const chunk of stream) {
      const candidate = chunk.candidates?.[0];
      const parts = candidate?.content?.parts as Array<Record<string, unknown>> | undefined;

      if (parts) {
        for (const part of parts) {
          if (typeof part.text === "string") {
            fullText += part.text;
            onToken(part.text);
          }
          if (part.inlineData) {
            const data = part.inlineData as { mimeType: string; data: string };
            allImageParts.push({
              type: "image_url",
              image_url: { url: `data:${data.mimeType};base64,${data.data}` },
            });
          }
          if (part.functionCall) {
            const fc = part.functionCall as { name: string; args: Record<string, unknown> };
            allToolCalls.push({
              id: generateCallId(),
              type: "function",
              function: {
                name: fc.name,
                arguments: JSON.stringify(fc.args ?? {}),
              },
            });
          }
        }
      }

      if (candidate?.finishReason) {
        finishReason = mapFinishReason(candidate.finishReason as string);
      }
      if (chunk.usageMetadata) {
        promptTokens = chunk.usageMetadata.promptTokenCount;
        completionTokens = chunk.usageMetadata.candidatesTokenCount;
      }
    }

    let content: string | ContentPart[];
    if (allImageParts.length > 0) {
      const parts: ContentPart[] = [];
      if (fullText) parts.push({ type: "text", text: fullText });
      parts.push(...allImageParts);
      content = parts;
    } else {
      content = fullText;
    }

    return {
      content,
      finishReason,
      promptTokens,
      completionTokens,
      tool_calls: allToolCalls.length > 0 ? allToolCalls : undefined,
    };
  } finally {
    if (timer) clearTimeout(timer);
  }
}

// ──────────────────────────────────────────────────────────────────────────────
// Helpers
// ──────────────────────────────────────────────────────────────────────────────

/** Strip provider prefix: "gemini-api/gemini-2.5-flash" → "gemini-2.5-flash" */
function stripPrefix(model: string): string {
  const slash = model.indexOf("/");
  return slash >= 0 ? model.slice(slash + 1) : model;
}

/** Map Gemini finish reasons to OpenAI format. */
function mapFinishReason(reason?: string): string {
  switch (reason) {
    case "STOP": return "stop";
    case "MAX_TOKENS": return "length";
    case "SAFETY": return "content_filter";
    case "RECITATION": return "content_filter";
    default: return "stop";
  }
}
