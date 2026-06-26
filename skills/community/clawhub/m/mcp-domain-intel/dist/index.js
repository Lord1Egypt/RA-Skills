#!/usr/bin/env node
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const mcp_js_1 = require("@modelcontextprotocol/sdk/server/mcp.js");
const stdio_js_1 = require("@modelcontextprotocol/sdk/server/stdio.js");
const zod_1 = require("zod");
const BASE_URL = process.env.NAUTDEV_BASE_URL || "https://api.nautdev.com";
async function apiFetch(path) {
    const response = await fetch(`${BASE_URL}${path}`, {
        headers: { Accept: "application/json" },
    });
    if (!response.ok) {
        throw new Error(`API error: ${response.status} ${response.statusText}`);
    }
    return response.json();
}
const server = new mcp_js_1.McpServer({
    name: "domain-intel",
    version: "1.0.0",
});
server.tool("lookup", "Look up WHOIS and DNS intelligence for a domain name.", {
    domain: zod_1.z.string().describe("Domain name to look up (e.g. example.com)"),
}, async ({ domain }) => {
    try {
        const result = await apiFetch(`/api/v1/domain/lookup?domain=${encodeURIComponent(domain)}`);
        return {
            content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
        };
    }
    catch (error) {
        const message = error instanceof Error ? error.message : String(error);
        return {
            content: [{ type: "text", text: JSON.stringify({ error: `Failed to look up domain: ${message}` }) }],
            isError: true,
        };
    }
});
server.tool("available", "Check if a domain name is available for registration.", {
    domain: zod_1.z.string().describe("Domain name to check availability (e.g. example.com)"),
}, async ({ domain }) => {
    try {
        const result = await apiFetch(`/api/v1/domain/available?domain=${encodeURIComponent(domain)}`);
        return {
            content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
        };
    }
    catch (error) {
        const message = error instanceof Error ? error.message : String(error);
        return {
            content: [{ type: "text", text: JSON.stringify({ error: `Failed to check availability: ${message}` }) }],
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