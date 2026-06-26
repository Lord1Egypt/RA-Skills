#!/usr/bin/env node

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const BASE_URL = process.env.NAUTDEV_BASE_URL || "https://api.nautdev.com";

async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    ...options,
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status} ${response.statusText}`);
  }

  return response.json() as Promise<T>;
}

const server = new McpServer({
  name: "llm-inference",
  version: "1.0.0",
});

server.tool(
  "chat",
  "Send a chat completion request to an LLM. Provide a model name and an array of messages with role and content.",
  {
    model: z.string().min(1).describe("Model identifier (e.g. llama3, mistral, gemma)"),
    messages: z
      .array(
        z.object({
          role: z.enum(["system", "user", "assistant"]).describe("Message role"),
          content: z.string().describe("Message content"),
        })
      )
      .min(1)
      .describe("Array of chat messages"),
  },
  async ({ model, messages }) => {
    try {
      const body: Record<string, unknown> = { model, messages };

      const result = await apiFetch(`/api/v1/llm/chat`, {
        method: "POST",
        body: JSON.stringify(body),
      });
      return {
        content: [{ type: "text" as const, text: JSON.stringify(result, null, 2) }],
      };
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      return {
        content: [{ type: "text" as const, text: JSON.stringify({ error: `Failed to complete chat: ${message}` }) }],
        isError: true,
      };
    }
  }
);

server.tool(
  "generate",
  "Generate text from a prompt using an LLM.",
  {
    model: z.string().min(1).describe("Model identifier (e.g. llama3, mistral, gemma)"),
    prompt: z.string().describe("Text prompt for generation"),
  },
  async ({ model, prompt }) => {
    try {
      const body: Record<string, unknown> = { model, prompt };

      const result = await apiFetch(`/api/v1/llm/generate`, {
        method: "POST",
        body: JSON.stringify(body),
      });
      return {
        content: [{ type: "text" as const, text: JSON.stringify(result, null, 2) }],
      };
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      return {
        content: [{ type: "text" as const, text: JSON.stringify({ error: `Failed to generate text: ${message}` }) }],
        isError: true,
      };
    }
  }
);

server.tool(
  "models",
  "List all available LLM models.",
  {},
  async () => {
    try {
      const result = await apiFetch(`/api/v1/llm/models`);
      return {
        content: [{ type: "text" as const, text: JSON.stringify(result, null, 2) }],
      };
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      return {
        content: [{ type: "text" as const, text: JSON.stringify({ error: `Failed to list models: ${message}` }) }],
        isError: true,
      };
    }
  }
);

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch((error) => {
  console.error("Server error:", error);
  process.exit(1);
});
