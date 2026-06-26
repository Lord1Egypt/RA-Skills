#!/usr/bin/env node
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const mcp_js_1 = require("@modelcontextprotocol/sdk/server/mcp.js");
const stdio_js_1 = require("@modelcontextprotocol/sdk/server/stdio.js");
const zod_1 = require("zod");
const NOAA_BASE = "https://api.weather.gov";
const USER_AGENT = "mcp-marine-weather/1.0.0 (velocibot)";
async function noaaFetch(url) {
    const response = await fetch(url, {
        headers: {
            "User-Agent": USER_AGENT,
            Accept: "application/geo+json",
        },
    });
    if (!response.ok) {
        throw new Error(`NOAA API error: ${response.status} ${response.statusText}`);
    }
    return response.json();
}
async function getMarineForecast(lat, lon) {
    // Step 1: Get the grid point info for this location
    const point = await noaaFetch(`${NOAA_BASE}/points/${lat.toFixed(4)},${lon.toFixed(4)}`);
    // Step 2: Get the forecast
    const forecast = await noaaFetch(point.properties.forecast);
    // Step 3: Get active alerts for this area
    const alerts = await noaaFetch(`${NOAA_BASE}/alerts/active?point=${lat.toFixed(4)},${lon.toFixed(4)}`);
    // Extract current conditions from the first forecast period
    const current = forecast.properties.periods[0];
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
    const warnings = alerts.features
        .filter((a) => {
        const event = a.properties.event.toLowerCase();
        return (event.includes("marine") ||
            event.includes("wind") ||
            event.includes("storm") ||
            event.includes("hurricane") ||
            event.includes("tropical") ||
            event.includes("tsunami") ||
            event.includes("surf") ||
            event.includes("rip") ||
            event.includes("flood") ||
            event.includes("water") ||
            event.includes("coastal"));
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
const server = new mcp_js_1.McpServer({
    name: "marine-weather",
    version: "1.0.0",
});
server.tool("marine_forecast", "Get marine weather forecast for a given latitude/longitude. Returns current conditions, multi-day forecast, and active marine warnings from NOAA.", {
    lat: zod_1.z.number().min(-90).max(90).describe("Latitude (-90 to 90)"),
    lon: zod_1.z.number().min(-180).max(180).describe("Longitude (-180 to 180)"),
}, async ({ lat, lon }) => {
    try {
        const result = await getMarineForecast(lat, lon);
        return {
            content: [
                {
                    type: "text",
                    text: JSON.stringify(result, null, 2),
                },
            ],
        };
    }
    catch (error) {
        const message = error instanceof Error ? error.message : String(error);
        return {
            content: [
                {
                    type: "text",
                    text: JSON.stringify({
                        error: `Failed to fetch marine forecast: ${message}`,
                        suggestion: "Ensure coordinates are within NOAA coverage (US territories). NOAA API may be temporarily unavailable.",
                    }),
                },
            ],
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