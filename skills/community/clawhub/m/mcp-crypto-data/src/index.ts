#!/usr/bin/env node

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const BASE_URL = process.env.NAUTDEV_BASE_URL || "https://api.nautdev.com";

async function apiFetch<T>(path: string): Promise<T> {
  const response = await fetch(`${BASE_URL}${path}`, {
    headers: { Accept: "application/json" },
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status} ${response.statusText}`);
  }

  return response.json() as Promise<T>;
}

const server = new McpServer({
  name: "crypto-data",
  version: "1.0.0",
});

server.tool(
  "price",
  "Get the current price for a cryptocurrency (e.g. bitcoin, ethereum).",
  {
    coin: z.string().min(1).describe("Cryptocurrency identifier (e.g. bitcoin, ethereum, solana)"),
  },
  async ({ coin }) => {
    try {
      const result = await apiFetch(`/api/v1/crypto/price?coin=${encodeURIComponent(coin)}`);
      return {
        content: [{ type: "text" as const, text: JSON.stringify(result, null, 2) }],
      };
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      return {
        content: [{ type: "text" as const, text: JSON.stringify({ error: `Failed to fetch price: ${message}` }) }],
        isError: true,
      };
    }
  }
);

server.tool(
  "fees",
  "Get current network transaction fees across major cryptocurrencies.",
  {},
  async () => {
    try {
      const result = await apiFetch(`/api/v1/crypto/fees`);
      return {
        content: [{ type: "text" as const, text: JSON.stringify(result, null, 2) }],
      };
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      return {
        content: [{ type: "text" as const, text: JSON.stringify({ error: `Failed to fetch fees: ${message}` }) }],
        isError: true,
      };
    }
  }
);

server.tool(
  "lightning_stats",
  "Get current Lightning Network statistics — node count, channel count, capacity, and more.",
  {},
  async () => {
    try {
      const result = await apiFetch(`/api/v1/crypto/lightning/stats`);
      return {
        content: [{ type: "text" as const, text: JSON.stringify(result, null, 2) }],
      };
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      return {
        content: [{ type: "text" as const, text: JSON.stringify({ error: `Failed to fetch Lightning stats: ${message}` }) }],
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
