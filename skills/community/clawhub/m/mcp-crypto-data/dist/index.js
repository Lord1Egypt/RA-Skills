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
    name: "crypto-data",
    version: "1.0.0",
});
server.tool("price", "Get the current price for a cryptocurrency (e.g. bitcoin, ethereum).", {
    coin: zod_1.z.string().describe("Cryptocurrency identifier (e.g. bitcoin, ethereum, solana)"),
}, async ({ coin }) => {
    try {
        const result = await apiFetch(`/api/v1/crypto/price?coin=${encodeURIComponent(coin)}`);
        return {
            content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
        };
    }
    catch (error) {
        const message = error instanceof Error ? error.message : String(error);
        return {
            content: [{ type: "text", text: JSON.stringify({ error: `Failed to fetch price: ${message}` }) }],
            isError: true,
        };
    }
});
server.tool("fees", "Get current network transaction fees across major cryptocurrencies.", {}, async () => {
    try {
        const result = await apiFetch(`/api/v1/crypto/fees`);
        return {
            content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
        };
    }
    catch (error) {
        const message = error instanceof Error ? error.message : String(error);
        return {
            content: [{ type: "text", text: JSON.stringify({ error: `Failed to fetch fees: ${message}` }) }],
            isError: true,
        };
    }
});
server.tool("lightning_stats", "Get current Lightning Network statistics — node count, channel count, capacity, and more.", {}, async () => {
    try {
        const result = await apiFetch(`/api/v1/crypto/lightning/stats`);
        return {
            content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
        };
    }
    catch (error) {
        const message = error instanceof Error ? error.message : String(error);
        return {
            content: [{ type: "text", text: JSON.stringify({ error: `Failed to fetch Lightning stats: ${message}` }) }],
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