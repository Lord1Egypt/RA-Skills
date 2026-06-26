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
  name: "domain-intel",
  version: "1.0.0",
});

server.tool(
  "lookup",
  "Look up WHOIS and DNS intelligence for a domain name.",
  {
    domain: z.string().min(1).describe("Domain name to look up (e.g. example.com)"),
  },
  async ({ domain }) => {
    try {
      const result = await apiFetch(`/api/v1/domain/lookup?domain=${encodeURIComponent(domain)}`);
      return {
        content: [{ type: "text" as const, text: JSON.stringify(result, null, 2) }],
      };
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      return {
        content: [{ type: "text" as const, text: JSON.stringify({ error: `Failed to look up domain: ${message}` }) }],
        isError: true,
      };
    }
  }
);

server.tool(
  "available",
  "Check if a domain name is available for registration.",
  {
    domain: z.string().min(1).describe("Domain name to check availability (e.g. example.com)"),
  },
  async ({ domain }) => {
    try {
      const result = await apiFetch(`/api/v1/domain/available?domain=${encodeURIComponent(domain)}`);
      return {
        content: [{ type: "text" as const, text: JSON.stringify(result, null, 2) }],
      };
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      return {
        content: [{ type: "text" as const, text: JSON.stringify({ error: `Failed to check availability: ${message}` }) }],
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
