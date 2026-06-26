#!/usr/bin/env node
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const mcp_js_1 = require("@modelcontextprotocol/sdk/server/mcp.js");
const stdio_js_1 = require("@modelcontextprotocol/sdk/server/stdio.js");
const zod_1 = require("zod");
const BASE_URL = process.env.NAUTDEV_BASE_URL || "https://api.nautdev.com";
async function apiFetch(path, options) {
    const response = await fetch(`${BASE_URL}${path}`, {
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        ...options,
    });
    if (!response.ok) {
        throw new Error(`API error: ${response.status} ${response.statusText}`);
    }
    return response.json();
}
const server = new mcp_js_1.McpServer({
    name: "llm-inference",
    version: "1.0.0",
});
server.tool("chat", "Send a chat completion request to an LLM. Provide a model name and an array of messages with role and content.", {
    model: zod_1.z.string().describe("Model identifier (e.g. llama3, mistral, gemma)"),
    messages: zod_1.z
        .array(zod_1.z.object({
        role: zod_1.z.enum(["system", "user", "assistant"]).describe("Message role"),
        content: zod_1.z.string().describe("Message content"),
    }))
        .describe("Array of chat messages"),
    stream: zod_1.z.boolean().optional().describe("Whether to stream the response (default: false)"),
}, async ({ model, messages, stream }) => {
    try {
        const body = { model, messages };
        if (stream !== undefined)
            body.stream = stream;
        const result = await apiFetch(`/api/v1/llm/chat`, {
            method: "POST",
            body: JSON.stringify(body),
        });
        return {
            content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
        };
    }
    catch (error) {
        const message = error instanceof Error ? error.message : String(error);
        return {
            content: [{ type: "text", text: JSON.stringify({ error: `Failed to complete chat: ${message}` }) }],
            isError: true,
        };
    }
});
server.tool("generate", "Generate text from a prompt using an LLM.", {
    model: zod_1.z.string().describe("Model identifier (e.g. llama3, mistral, gemma)"),
    prompt: zod_1.z.string().describe("Text prompt for generation"),
    stream: zod_1.z.boolean().optional().describe("Whether to stream the response (default: false)"),
}, async ({ model, prompt, stream }) => {
    try {
        const body = { model, prompt };
        if (stream !== undefined)
            body.stream = stream;
        const result = await apiFetch(`/api/v1/llm/generate`, {
            method: "POST",
            body: JSON.stringify(body),
        });
        return {
            content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
        };
    }
    catch (error) {
        const message = error instanceof Error ? error.message : String(error);
        return {
            content: [{ type: "text", text: JSON.stringify({ error: `Failed to generate text: ${message}` }) }],
            isError: true,
        };
    }
});
server.tool("models", "List all available LLM models.", {}, async () => {
    try {
        const result = await apiFetch(`/api/v1/llm/models`);
        return {
            content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
        };
    }
    catch (error) {
        const message = error instanceof Error ? error.message : String(error);
        return {
            content: [{ type: "text", text: JSON.stringify({ error: `Failed to list models: ${message}` }) }],
            isError: true,
        };
    }
});
async function main() {
    const transport = new stdio_js_1.StdioServerTransport();
    await server.connect(transport);
}
main().catch((error) => {
    console.error("Server error:", error);
    process.exit(1);
});
//# sourceMappingURL=index.js.map