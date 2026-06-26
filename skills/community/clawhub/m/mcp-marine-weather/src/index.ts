#!/usr/bin/env node

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const NOAA_BASE = process.env.NOAA_BASE_URL || "https://api.weather.gov";
const USER_AGENT = "mcp-marine-weather/1.0.0 (velocibot)";

interface NOAAPoint {
  properties: {
    forecast: string;
    forecastHourly: string;
    forecastGridData: string;
    forecastZone: string;
    county: string;
    fireWeatherZone: string;
    gridId: string;
    gridX: number;
    gridY: number;
  };
}

interface NOAAForecastPeriod {
  number: number;
  name: string;
  startTime: string;
  endTime: string;
  isDaytime: boolean;
  temperature: number;
  temperatureUnit: string;
  windSpeed: string;
  windDirection: string;
  shortForecast: string;
  detailedForecast: string;
}

interface NOAAForecast {
  properties: {
    periods: NOAAForecastPeriod[];
  };
}

interface NOAAAlert {
  properties: {
    event: string;
    headline: string;
    description: string;
    severity: string;
    urgency: string;
    areas: string;
    effective: string;
    expires: string;
  };
}

interface NOAAAlerts {
  features: NOAAAlert[];
}

async function noaaFetch<T>(url: string): Promise<T> {
  const response = await fetch(url, {
    headers: {
      "User-Agent": USER_AGENT,
      Accept: "application/geo+json",
    },
  });

  if (!response.ok) {
    throw new Error(`NOAA API error: ${response.status} ${response.statusText}`);
  }

  return response.json() as Promise<T>;
}

async function getMarineForecast(lat: number, lon: number) {
  // Step 1: Get the grid point info for this location
  const point = await noaaFetch<NOAAPoint>(
    `${NOAA_BASE}/points/${lat.toFixed(4)},${lon.toFixed(4)}`
  );

  // Step 2: Get the forecast
  const forecast = await noaaFetch<NOAAForecast>(point.properties.forecast);

  // Step 3: Get active alerts for this area
  const alerts = await noaaFetch<NOAAAlerts>(
    `${NOAA_BASE}/alerts/active?point=${lat.toFixed(4)},${lon.toFixed(4)}`
  );

  // Extract current conditions from the first forecast period
  const periods = forecast.properties.periods;
  if (!periods || periods.length === 0) {
    return {
      conditions: null,
      forecast: [],
      warnings: [],
      error: "No forecast periods available for this location.",
    };
  }

  const current = periods[0];
  const conditions = {
    summary: current.shortForecast,
    temperature: current.temperature,
    temperatureUnit: current.temperatureUnit,
    windSpeed: current.windSpeed,
    windDirection: current.windDirection,
    detailed: current.detailedForecast,
    period: current.name,
  };

  // Build forecast array from remaining periods
  const forecastPeriods = forecast.properties.periods.slice(0, 7).map((p) => ({
    name: p.name,
    startTime: p.startTime,
    endTime: p.endTime,
    temperature: p.temperature,
    temperatureUnit: p.temperatureUnit,
    windSpeed: p.windSpeed,
    windDirection: p.windDirection,
    forecast: p.shortForecast,
    details: p.detailedForecast,
  }));

  // Extract marine-relevant warnings
  const warnings = (alerts.features || [])
    .filter((a) => {
      const event = a.properties.event.toLowerCase();
      return (
        event.includes("marine") ||
        event.includes("wind") ||
        event.includes("storm") ||
        event.includes("hurricane") ||
        event.includes("tropical") ||
        event.includes("tsunami") ||
        event.includes("surf") ||
        event.includes("rip") ||
        event.includes("flood") ||
        event.includes("water") ||
        event.includes("coastal")
      );
    })
    .map((a) => ({
      event: a.properties.event,
      headline: a.properties.headline,
      severity: a.properties.severity,
      urgency: a.properties.urgency,
      description: a.properties.description,
      effective: a.properties.effective,
      expires: a.properties.expires,
    }));

  return { conditions, forecast: forecastPeriods, warnings };
}

const server = new McpServer({
  name: "marine-weather",
  version: "1.0.0",
});

server.tool(
  "marine_forecast",
  "Get marine weather forecast for a given latitude/longitude. Returns current conditions, multi-day forecast, and active marine warnings from NOAA.",
  {
    lat: z.number().min(-90).max(90).describe("Latitude (-90 to 90)"),
    lon: z.number().min(-180).max(180).describe("Longitude (-180 to 180)"),
  },
  async ({ lat, lon }) => {
    try {
      const result = await getMarineForecast(lat, lon);

      return {
        content: [
          {
            type: "text" as const,
            text: JSON.stringify(result, null, 2),
          },
        ],
      };
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      return {
        content: [
          {
            type: "text" as const,
            text: JSON.stringify({
              error: `Failed to fetch marine forecast: ${message}`,
              suggestion:
                "Ensure coordinates are within NOAA coverage (US territories). NOAA API may be temporarily unavailable.",
            }),
          },
        ],
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
