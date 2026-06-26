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
    name: "company-search",
    version: "1.0.0",
});
server.tool("search", "Search for companies by jurisdiction and name in corporate registries.", {
    jurisdiction: zod_1.z.string().describe("Jurisdiction code (e.g. us_de, gb, sg)"),
    name: zod_1.z.string().describe("Company name or partial name to search"),
}, async ({ jurisdiction, name }) => {
    try {
        const result = await apiFetch(`/api/v1/company/search?jurisdiction=${encodeURIComponent(jurisdiction)}&name=${encodeURIComponent(name)}`);
        return {
            content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
        };
    }
    catch (error) {
        const message = error instanceof Error ? error.message : String(error);
        return {
            content: [{ type: "text", text: JSON.stringify({ error: `Failed to search companies: ${message}` }) }],
            isError: true,
        };
    }
});
server.tool("jurisdictions", "List all available jurisdictions for company search.", {}, async () => {
    try {
        const result = await apiFetch(`/api/v1/company/jurisdictions`);
        return {
            content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
        };
    }
    catch (error) {
        const message = error instanceof Error ? error.message : String(error);
        return {
            content: [{ type: "text", text: JSON.stringify({ error: `Failed to fetch jurisdictions: ${message}` }) }],
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