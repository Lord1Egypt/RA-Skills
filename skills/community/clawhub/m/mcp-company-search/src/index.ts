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
  name: "company-search",
  version: "1.0.0",
});

server.tool(
  "search",
  "Search for companies by jurisdiction and name in corporate registries.",
  {
    jurisdiction: z.string().min(1).describe("Jurisdiction code (e.g. us_de, gb, sg)"),
    name: z.string().min(1).describe("Company name or partial name to search"),
  },
  async ({ jurisdiction, name }) => {
    try {
      const result = await apiFetch(
        `/api/v1/company/search?jurisdiction=${encodeURIComponent(jurisdiction)}&name=${encodeURIComponent(name)}`
      );
      return {
        content: [{ type: "text" as const, text: JSON.stringify(result, null, 2) }],
      };
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      return {
        content: [{ type: "text" as const, text: JSON.stringify({ error: `Failed to search companies: ${message}` }) }],
        isError: true,
      };
    }
  }
);

server.tool(
  "jurisdictions",
  "List all available jurisdictions for company search.",
  {},
  async () => {
    try {
      const result = await apiFetch(`/api/v1/company/jurisdictions`);
      return {
        content: [{ type: "text" as const, text: JSON.stringify(result, null, 2) }],
      };
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      return {
        content: [{ type: "text" as const, text: JSON.stringify({ error: `Failed to fetch jurisdictions: ${message}` }) }],
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
