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
  name: "aviation-weather",
  version: "1.0.0",
});

server.tool(
  "metar",
  "Fetch current METAR weather observation for an aviation station (e.g. KJFK, EGLL).",
  {
    station: z.string().min(1).describe("ICAO station identifier (e.g. KJFK, EGLL)"),
  },
  async ({ station }) => {
    try {
      const result = await apiFetch(`/api/v1/weather/aviation/metar?station=${encodeURIComponent(station)}`);
      return {
        content: [{ type: "text" as const, text: JSON.stringify(result, null, 2) }],
      };
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      return {
        content: [{ type: "text" as const, text: JSON.stringify({ error: `Failed to fetch METAR: ${message}` }) }],
        isError: true,
      };
    }
  }
);

server.tool(
  "taf",
  "Fetch Terminal Aerodrome Forecast (TAF) for an aviation station.",
  {
    station: z.string().min(1).describe("ICAO station identifier (e.g. KJFK, EGLL)"),
  },
  async ({ station }) => {
    try {
      const result = await apiFetch(`/api/v1/weather/aviation/taf?station=${encodeURIComponent(station)}`);
      return {
        content: [{ type: "text" as const, text: JSON.stringify(result, null, 2) }],
      };
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      return {
        content: [{ type: "text" as const, text: JSON.stringify({ error: `Failed to fetch TAF: ${message}` }) }],
        isError: true,
      };
    }
  }
);

server.tool(
  "nearby_stations",
  "Find nearby aviation weather stations by latitude, longitude, and optional radius in nautical miles.",
  {
    lat: z.number().min(-90).max(90).describe("Latitude (-90 to 90)"),
    lon: z.number().min(-180).max(180).describe("Longitude (-180 to 180)"),
    radius: z.number().positive().optional().describe("Search radius in nautical miles (default: 50)"),
  },
  async ({ lat, lon, radius }) => {
    try {
      let path = `/api/v1/weather/aviation/stations?lat=${lat}&lon=${lon}`;
      if (radius !== undefined) path += `&radius=${radius}`;
      const result = await apiFetch(path);
      return {
        content: [{ type: "text" as const, text: JSON.stringify(result, null, 2) }],
      };
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      return {
        content: [{ type: "text" as const, text: JSON.stringify({ error: `Failed to fetch stations: ${message}` }) }],
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
