/**
 * HA MCP Client - Call tools via HTTP JSON-RPC
 * Usage: node call-tool.mjs <tool_name> [args_json]
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

const HOST = process.env.HA_MCP_HOST || "localhost";
const PORT = process.env.HA_MCP_PORT || "3002";
const HA_TOKEN = env.HA_TOKEN || "";

function rpc(method, params = {}) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify({ jsonrpc: "2.0", id: 1, method, params });
    const headers = {
      "Content-Type": "application/json",
      "Content-Length": Buffer.byteLength(body),
      "Authorization": `Bearer ${HA_TOKEN}`,
    };
    const options = { hostname: HOST, port: PORT, path: "/", method: "POST", headers };
    const req = http.request(options, res => {
      let data = "";
      res.on("data", chunk => data += chunk);
      res.on("end", () => {
        try {
          const json = JSON.parse(data);
          if (json.error) reject(new Error(json.error.message));
          else resolve(json.result);
        } catch (e) { reject(e); }
      });
    });
    req.on("error", reject);
    req.write(body);
    req.end();
  });
}

const tool = process.argv[2];
const args = process.argv[3] ? JSON.parse(process.argv[3]) : {};

if (!tool) {
  console.error("Usage: node call-tool.mjs <tool_name> [args_json]");
  process.exit(1);
}

rpc("tools/call", { name: tool, arguments: args })
  .then(result => {
    const text = result.content?.[0]?.text || JSON.stringify(result);
    console.log(text);
  })
  .catch(err => {
    console.error("Error:", err.message);
    process.exit(1);
  });
