/**
 * tool-protocol.ts
 *
 * Translates between the OpenAI tool-calling protocol and CLI text I/O.
 *
 * - buildToolPromptBlock(): injects tool definitions + instructions into the prompt
 * - buildToolCallJsonSchema(): returns JSON schema for Claude's --json-schema flag
 * - parseToolCallResponse(): extracts tool_calls from CLI output text/JSON
 * - generateCallId(): unique call IDs for tool_calls
 */

import { randomBytes } from "node:crypto";

// ──────────────────────────────────────────────────────────────────────────────
// Types
// ──────────────────────────────────────────────────────────────────────────────

export interface ToolDefinition {
  type: "function";
  function: {
    name: string;
    description: string;
    parameters: Record<string, unknown>;
  };
}

export interface ToolCall {
  id: string;
  type: "function";
  function: {
    name: string;
    arguments: string; // JSON-encoded arguments
  };
}

export interface CliToolResult {
  content: string | null;
  tool_calls?: ToolCall[];
}

// ──────────────────────────────────────────────────────────────────────────────
// Prompt building
// ──────────────────────────────────────────────────────────────────────────────

/**
 * Build a text block describing available tools and response format instructions.
 * This block is prepended to the system message (or added as a new system message).
 */
export function buildToolPromptBlock(tools: ToolDefinition[]): string {
  const toolDescriptions = tools
    .map((t) => {
      const fn = t.function;
      const params = JSON.stringify(fn.parameters);
      return `- name: ${fn.name}\n  description: ${fn.description}\n  parameters: ${params}`;
    })
    .join("\n");

  return [
    "You have access to the following tools.",
    "",
    "IMPORTANT: You must respond with ONLY valid JSON in one of these two formats:",
    "",
    'To call one or more tools, respond with ONLY:',
    '{"tool_calls":[{"name":"<tool_name>","arguments":{<parameters as JSON object>}}]}',
    "",
    'To respond with text (no tool call needed), respond with ONLY:',
    '{"content":"<your text response>"}',
    "",
    "Do NOT include any text outside the JSON. Do NOT wrap in markdown code blocks.",
    "",
    "Available tools:",
    toolDescriptions,
  ].join("\n");
}

// ──────────────────────────────────────────────────────────────────────────────
// JSON Schema for Claude's --json-schema flag
// ──────────────────────────────────────────────────────────────────────────────

/**
 * Returns a JSON schema that constrains Claude's output to either:
 * - { "content": "text response" }
 * - { "tool_calls": [{ "name": "...", "arguments": { ... } }] }
 */
export function buildToolCallJsonSchema(): object {
  return {
    type: "object",
    properties: {
      content: { type: "string" },
      tool_calls: {
        type: "array",
        items: {
          type: "object",
          properties: {
            name: { type: "string" },
            arguments: { type: "object" },
          },
          required: ["name", "arguments"],
        },
      },
    },
    additionalProperties: false,
  };
}

// ──────────────────────────────────────────────────────────────────────────────
// Response parsing
// ──────────────────────────────────────────────────────────────────────────────

/**
 * Parse CLI output text into a CliToolResult.
 *
 * Tries to extract JSON from the text. If valid JSON with tool_calls is found,
 * returns structured tool calls. Otherwise returns the text as content.
 *
 * Never throws — always returns a valid result.
 */
export function parseToolCallResponse(text: string): CliToolResult {
  const trimmed = text.trim();

  // Check for Claude's --output-format json wrapper FIRST.
  // Claude returns: { "type": "result", "result": "..." }
  // The inner `result` field contains the actual model output (with tool_calls or content).
  const claudeResult = tryExtractClaudeJsonResult(trimmed);
  if (claudeResult) {
    const inner = tryParseJson(claudeResult);
    if (inner) return normalizeResult(inner);
    // Claude result is plain text
    return { content: claudeResult };
  }

  // Try direct JSON parse (for non-Claude outputs)
  const parsed = tryParseJson(trimmed);
  if (parsed) return normalizeResult(parsed);

  // Try extracting JSON from markdown code blocks: ```json ... ```
  const codeBlock = tryExtractCodeBlock(trimmed);
  if (codeBlock) {
    const inner = tryParseJson(codeBlock);
    if (inner) return normalizeResult(inner);
  }

  // Try finding a JSON object anywhere in the text
  const embedded = tryExtractEmbeddedJson(trimmed);
  if (embedded) {
    const inner = tryParseJson(embedded);
    if (inner) return normalizeResult(inner);
  }

  // Fallback: treat entire text as content
  return { content: trimmed || null };
}

/**
 * Normalize a parsed JSON object into a CliToolResult.
 */
function normalizeResult(obj: Record<string, unknown>): CliToolResult {
  // Check for tool_calls array
  if (Array.isArray(obj.tool_calls) && obj.tool_calls.length > 0) {
    const toolCalls: ToolCall[] = obj.tool_calls.map((tc: Record<string, unknown>) => ({
      id: generateCallId(),
      type: "function" as const,
      function: {
        name: String(tc.name ?? ""),
        arguments: typeof tc.arguments === "string"
          ? tc.arguments
          : JSON.stringify(tc.arguments ?? {}),
      },
    }));
    return { content: null, tool_calls: toolCalls };
  }

  // Check for content field
  if (typeof obj.content === "string") {
    return { content: obj.content };
  }

  // Unknown structure — serialize as content
  return { content: JSON.stringify(obj) };
}

function tryParseJson(text: string): Record<string, unknown> | null {
  try {
    const obj = JSON.parse(text);
    if (typeof obj === "object" && obj !== null && !Array.isArray(obj)) {
      return obj as Record<string, unknown>;
    }
    return null;
  } catch {
    return null;
  }
}

/**
 * Extract the model output from Claude's JSON output wrapper.
 * Claude CLI with --output-format json returns:
 * { "type": "result", "result": "the model output",
 *   "structured_output": { "content": "..." }, ... }
 *
 * When --json-schema is used, the `result` field is the JSON-schema-constrained output.
 * The `structured_output.content` field may also contain the raw output.
 */
function tryExtractClaudeJsonResult(text: string): string | null {
  try {
    const obj = JSON.parse(text);
    if (obj?.type === "result") {
      // Prefer structured_output.content if available
      if (typeof obj.structured_output?.content === "string") {
        return obj.structured_output.content;
      }
      if (typeof obj.result === "string") {
        return obj.result;
      }
    }
    return null;
  } catch {
    return null;
  }
}

/** Extract JSON from ```json ... ``` or ``` ... ``` code blocks. */
function tryExtractCodeBlock(text: string): string | null {
  const match = text.match(/```(?:json)?\s*\n?([\s\S]*?)\n?```/);
  return match?.[1]?.trim() ?? null;
}

/** Find the first { ... } JSON object in text (greedy, balanced braces). */
function tryExtractEmbeddedJson(text: string): string | null {
  const start = text.indexOf("{");
  if (start === -1) return null;

  let depth = 0;
  let inString = false;
  let escaped = false;

  for (let i = start; i < text.length; i++) {
    const ch = text[i];
    if (escaped) {
      escaped = false;
      continue;
    }
    if (ch === "\\") {
      escaped = true;
      continue;
    }
    if (ch === '"') {
      inString = !inString;
      continue;
    }
    if (inString) continue;
    if (ch === "{") depth++;
    if (ch === "}") {
      depth--;
      if (depth === 0) {
        return text.slice(start, i + 1);
      }
    }
  }
  return null;
}

// ──────────────────────────────────────────────────────────────────────────────
// Utilities
// ──────────────────────────────────────────────────────────────────────────────

/** Generate a unique tool call ID: "call_" + 12 random hex characters. */
export function generateCallId(): string {
  return "call_" + randomBytes(6).toString("hex");
}
