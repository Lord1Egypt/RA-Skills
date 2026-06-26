/**
 * Home Assistant MCP Server - Simple HTTP JSON-RPC
 * Compatible with any MCP client via HTTP POST
 */

import http from "http";
import { readFileSync } from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const envPath = path.resolve(__dirname, "../.env");
const env = {};
try {
  const lines = readFileSync(envPath, "utf8").split("\n");
  for (const line of lines) {
    const [key, ...vals] = line.split("=");
    if (key && vals.length) env[key.trim()] = vals.join("=").trim();
  }
} catch (e) { /* no .env */ }

const HA_URL = env.HA_URL || "http://localhost:8123";
const HA_TOKEN = env.HA_TOKEN || "";
const PORT = parseInt(env.PORT || "3002", 10);
const ALLOWED_ORIGIN = "http://localhost"; // Only allow localhost for CORS

// Simple bearer token auth: must send "Authorization: Bearer <HA_TOKEN>" header
function checkAuth(req) {
  const auth = req.headers["authorization"] || req.headers["Authorization"];
  if (!auth || !auth.startsWith("Bearer ")) return false;
  const token = auth.slice("Bearer ".length);
  return token === HA_TOKEN;
}

// ============================================================================
// HA API
// ============================================================================

async function haFetch(endpoint, options = {}) {
  const url = `${HA_URL}/api${endpoint}`;
  const response = await fetch(url, {
    ...options,
    headers: {
      "Authorization": `Bearer ${HA_TOKEN}`,
      "Content-Type": "application/json",
      ...options.headers,
    },
  });
  if (!response.ok) throw new Error(`HA API error: ${response.status}`);
  return response.json();
}

const getEntity = (id) => haFetch(`/states/${id}`);
const callService = (d, s, data) => haFetch(`/services/${d}/${s}`, { method: "POST", body: JSON.stringify(data) });
const getAllEntities = () => haFetch("/states");

// ============================================================================
// Tool Implementations
// ============================================================================

const tools = {
  // Lights
  light_turn_on: async ({ entity_id, brightness }) => {
    const data = { entity_id };
    if (brightness !== undefined) data.brightness = brightness;
    await callService("light", "turn_on", data);
    return textResult(`Light ${entity_id} turned on${brightness ? ` (brightness: ${brightness})` : ""}`);
  },
  light_turn_off: async ({ entity_id }) => {
    await callService("light", "turn_off", { entity_id });
    return textResult(`Light ${entity_id} turned off`);
  },
  get_light_state: async ({ entity_id }) => {
    const e = await getEntity(entity_id);
    return textResult(`${e.entity_id}: ${e.state} (brightness: ${e.attributes.brightness ?? "N/A"})`);
  },

  // Climate / AC
  climate_set_temperature: async ({ entity_id, temperature }) => {
    await callService("climate", "set_temperature", { entity_id, temperature });
    return textResult(`${entity_id} set to ${temperature}°C`);
  },
  climate_set_mode: async ({ entity_id, mode }) => {
    await callService("climate", "set_hvac_mode", { entity_id, hvac_mode: mode });
    return textResult(`${entity_id} mode set to ${mode}`);
  },
  get_climate_state: async ({ entity_id }) => {
    const e = await getEntity(entity_id);
    const a = e.attributes;
    return textResult(`${e.entity_id}: ${e.state}, temp: ${a.current_temperature}°C, target: ${a.temperature}°C`);
  },

  // Fans
  fan_turn_on: async ({ entity_id }) => {
    await callService("fan", "turn_on", { entity_id });
    return textResult(`${entity_id} turned on`);
  },
  fan_turn_off: async ({ entity_id }) => {
    await callService("fan", "turn_off", { entity_id });
    return textResult(`${entity_id} turned off`);
  },
  fan_set_speed: async ({ entity_id, speed }) => {
    await callService("fan", "set_percentage", { entity_id, percentage: speed });
    return textResult(`${entity_id} speed set to ${speed}%`);
  },
  get_fan_state: async ({ entity_id }) => {
    const e = await getEntity(entity_id);
    return textResult(`${e.entity_id}: ${e.state} (speed: ${e.attributes.percentage ?? "N/A"}%)`);
  },

  // Switches
  switch_turn_on: async ({ entity_id }) => { await callService("switch", "turn_on", { entity_id }); return textResult(`${entity_id} turned on`); },
  switch_turn_off: async ({ entity_id }) => { await callService("switch", "turn_off", { entity_id }); return textResult(`${entity_id} turned off`); },
  get_switch_state: async ({ entity_id }) => { const e = await getEntity(entity_id); return textResult(`${e.entity_id}: ${e.state}`); },

  // Locks
  lock_lock: async ({ entity_id }) => { await callService("lock", "lock", { entity_id }); return textResult(`${entity_id} locked`); },
  lock_unlock: async ({ entity_id }) => { await callService("lock", "unlock", { entity_id }); return textResult(`${entity_id} unlocked`); },
  get_lock_state: async ({ entity_id }) => { const e = await getEntity(entity_id); return textResult(`${e.entity_id}: ${e.state}`); },

  // Sensors
  get_sensor_reading: async ({ entity_id }) => { const e = await getEntity(entity_id); return textResult(`${e.entity_id}: ${e.state} ${e.attributes.unit_of_measurement ?? ""}`); },
  list_sensors: async () => {
    const entities = await getAllEntities();
    const sensors = entities.filter(e => e.entity_id.startsWith("sensor.") || e.entity_id.startsWith("binary_sensor."));
    const list = sensors.slice(0, 30).map(e => `  - ${e.entity_id}: ${e.state} ${e.attributes.unit_of_measurement ?? ""}`).join("\n");
    return textResult(`Sensors (${sensors.length} total):\n${list}`);
  },

  // Humidifier
  humidifier_turn_on: async ({ entity_id }) => { await callService("humidifier", "turn_on", { entity_id }); return textResult(`${entity_id} turned on`); },
  humidifier_turn_off: async ({ entity_id }) => { await callService("humidifier", "turn_off", { entity_id }); return textResult(`${entity_id} turned off`); },
  get_humidifier_state: async ({ entity_id }) => { const e = await getEntity(entity_id); return textResult(`${e.entity_id}: ${e.state}, humidity: ${e.attributes.current_humidity ?? "N/A"}%`); },

  // Cover / Blinds
  cover_open: async ({ entity_id }) => { await callService("cover", "open_cover", { entity_id }); return textResult(`${entity_id} opened`); },
  cover_close: async ({ entity_id }) => { await callService("cover", "close_cover", { entity_id }); return textResult(`${entity_id} closed`); },
  get_cover_state: async ({ entity_id }) => { const e = await getEntity(entity_id); return textResult(`${e.entity_id}: ${e.state}`); },

  // Vacuum
  vacuum_start: async ({ entity_id }) => { await callService("vacuum", "start", { entity_id }); return textResult(`${entity_id} started`); },
  vacuum_stop: async ({ entity_id }) => { await callService("vacuum", "stop", { entity_id }); return textResult(`${entity_id} stopped`); },
  vacuum_return_to_base: async ({ entity_id }) => { await callService("vacuum", "return_to_base", { entity_id }); return textResult(`${entity_id} returning to base`); },

  // Devices
  list_all_devices: async (args = {}) => {
    const entities = await getAllEntities();
    const filtered = args.domain ? entities.filter(e => e.entity_id.startsWith(args.domain + ".")) : entities;
    const list = filtered.slice(0, 50).map(e => `  - ${e.entity_id}: ${e.state}`).join("\n");
    return textResult(`${filtered.length} entities (showing 50):\n${list}`);
  },
  get_device_state: async ({ entity_id }) => {
    const e = await getEntity(entity_id);
    return textResult(`${e.entity_id}\nState: ${e.state}\nAttributes: ${JSON.stringify(e.attributes, null, 2)}`);
  },

  // Scene
  trigger_scene: async ({ entity_id }) => { await callService("scene", "turn_on", { entity_id }); return textResult(`Scene ${entity_id} triggered`); },

  // XiaoAI TTS Announce
  xiaoai_announce: async ({ message, entity_id }) => {
    const target = entity_id || "notify.xiaomi_cn_501481700_l16a_play_text_a_7_3";
    await haFetch("/services/notify/send_message", {
      method: "POST",
      body: JSON.stringify({ message, entity_id: target }),
    });
    return textResult(`XiaoAI announced: ${message}`);
  },

  // HA status
  ping_ha: async () => { await haFetch("/config"); return textResult("Home Assistant is reachable and running"); },
  get_ha_config: async () => { const c = await haFetch("/config"); return textResult(`Home Assistant version: ${c.version}`); },
};

function textResult(text) {
  return { content: [{ type: "text", text }] };
}

// ============================================================================
// HTTP Server
// ============================================================================

const server = http.createServer(async (req, res) => {
  if (req.method === "OPTIONS") {
    res.writeHead(200, { "Access-Control-Allow-Origin": ALLOWED_ORIGIN, "Access-Control-Allow-Methods": "POST, GET, OPTIONS", "Access-Control-Allow-Headers": "Content-Type, Authorization" });
    res.end();
    return;
  }
  // Reject requests from non-localhost origins
  const origin = req.headers["origin"] || req.headers["Origin"];
  if (origin && !origin.startsWith(ALLOWED_ORIGIN)) {
    res.writeHead(403, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ error: "Forbidden: cross-origin request denied" }));
    return;
  }
  // Require authentication for all tool calls
  if (req.method === "POST" && !checkAuth(req)) {
    res.writeHead(401, { "Content-Type": "application/json", "WWW-Authenticate": "Bearer" });
    res.end(JSON.stringify({ error: "Unauthorized: valid Bearer token required" }));
    return;
  }
  if (req.method === "GET" && req.url === "/health") {
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ status: "ok" }));
    return;
  }
  if (req.method !== "POST") { res.writeHead(404); res.end(); return; }

  let body = "";
  req.on("data", chunk => body += chunk);
  req.on("end", async () => {
    try {
      const json = JSON.parse(body);
      const jsonrpc = json.jsonrpc || "2.0";
      const method = json.method;
      const params = json.params || {};
      const responseId = json.id;

      if (method === "tools/list") {
        const toolList = Object.keys(tools).map(name => ({ name, description: "", inputSchema: { type: "object" } }));
        res.writeHead(200, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ jsonrpc, id: responseId, result: { tools: toolList } }));
        return;
      }
      if (method === "tools/call") {
        const toolName = params.name;
        const args = params.arguments || {};
        if (!tools[toolName]) {
          res.writeHead(200, { "Content-Type": "application/json" });
          res.end(JSON.stringify({ jsonrpc, id: responseId, error: { code: -32601, message: `Tool ${toolName} not found` } }));
          return;
        }
        try {
          const result = await tools[toolName](args);
          res.writeHead(200, { "Content-Type": "application/json" });
          res.end(JSON.stringify({ jsonrpc, id: responseId, result }));
        } catch (err) {
          res.writeHead(200, { "Content-Type": "application/json" });
          res.end(JSON.stringify({ jsonrpc, id: responseId, error: { code: -32603, message: err.message } }));
        }
        return;
      }
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ jsonrpc, id: responseId, error: { code: -32601, message: "Method not found" } }));
    } catch (e) {
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ jsonrpc: "2.0", id: null, error: { code: -32700, message: "Parse error" } }));
    }
  });
});

server.listen(PORT, () => {
  console.error(`HA MCP Server running on http://localhost:${PORT}`);
});
