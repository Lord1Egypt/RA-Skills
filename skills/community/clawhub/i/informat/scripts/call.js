#!/usr/bin/env node

/**
 * Informat Platform - Unified System Method Calling
 * Usage:
 *   call.js <methodName> --file params.json
 *   call.js <methodName> '{"key":"value"}'
 *   call.js <methodName>
 */

var https = require("https");
var http = require("http");
var fs = require("fs");
var nodePath = require("path");
var urlMod = require("url");

// ---- Load configuration from .env file ----
function loadEnv() {
  var envPath = nodePath.join(__dirname, ".env");
  var config = {};
  try {
    var lines = fs.readFileSync(envPath, "utf-8").split("\n");
    for (var i = 0; i < lines.length; i++) {
      var trimmed = lines[i].trim();
      if (!trimmed || trimmed.charAt(0) === "#") continue;
      var idx = trimmed.indexOf("=");
      if (idx === -1) continue;
      config[trimmed.slice(0, idx).trim()] = trimmed.slice(idx + 1).trim();
    }
  } catch (e) {
    console.error("Failed to read .env file: " + envPath);
    process.exit(1);
  }
  return config;
}

// ---- HTTP POST ----
function post(targetUrl, headers, body, callback) {
  var parsed = new urlMod.URL(targetUrl);
  var mod = parsed.protocol === "https:" ? https : http;
  var req = mod.request(parsed, {
    method: "POST",
    headers: Object.assign({}, headers, { "Content-Length": Buffer.byteLength(body) }),
  }, function (res) {
    var chunks = [];
    res.on("data", function (c) { chunks.push(c); });
    res.on("end", function () {
      var text = Buffer.concat(chunks).toString("utf-8");
      if (res.statusCode < 200 || res.statusCode >= 300) {
        callback(new Error("Request failed (" + res.statusCode + "): " + text));
      } else {
        callback(null, text);
      }
    });
  });
  req.on("error", function (e) { callback(e); });
  req.write(body);
  req.end();
}

// ---- Main Flow ----
var cliArgs = process.argv.slice(2);

if (cliArgs.length === 0 || cliArgs[0] === "-h" || cliArgs[0] === "--help") {
  console.error("Usage:");
  console.error("  call.js <methodName> --file params.json");
  console.error("  call.js <methodName> '{\"key\":\"value\"}'");
  console.error("  call.js <methodName>");
  console.error("  call.js <methodName> <appId> --file params.json");
  console.error("  call.js <methodName> <appId> '{\"key\":\"value\"}'");
  console.error("  call.js <methodName> <appId>");
  console.error("\nNote:");
  console.error("  - Methods starting with _company will automatically use the team agent interface");
  console.error("  - Other methods require specifying appId and use the application agent interface");
  process.exit(2);
}

var methodName = cliArgs[0];
var restArgs = cliArgs.slice(1);

// Parse arguments
var methodArgs = {};
var appId = null;

// Check if appId is required
if (!methodName.startsWith("_company")) {
  if (!restArgs[0]) {
    console.error("Missing appId for non-company methods");
    process.exit(1);
  }
  appId = restArgs[0];
  restArgs = restArgs.slice(1);
}

if (restArgs[0] === "--file" || restArgs[0] === "-f") {
  if (!restArgs[1]) { console.error("Missing file path after --file"); process.exit(1); }
  var filePath = nodePath.resolve(restArgs[1]);
  try {
    methodArgs = JSON.parse(fs.readFileSync(filePath, "utf-8"));
  } catch (e) {
    console.error("Failed to read/parse file: " + filePath + " - " + e.message);
    process.exit(1);
  }
} else if (restArgs[0]) {
  try { methodArgs = JSON.parse(restArgs[0]); } catch (e) { console.error("Invalid JSON: " + e.message); process.exit(1); }
}

var env = loadEnv();
var host = (env.host || "").trim();
if (!host) { console.error("Missing host in .env"); process.exit(1); }
var agentToken = (env.agentToken || "").trim();
if (!agentToken) { console.error("Missing agentToken in .env"); process.exit(1); }
if (host.charAt(host.length - 1) !== "/") host += "/";

// Build API path
var apiPath;
if (methodName.startsWith("_company")) {
  apiPath = "web0/aiagent/company_agent";
} else {
  apiPath = "web0/aiagent/app_agent/" + appId;
}

var url = host + apiPath;
var body = JSON.stringify({
  jsonrpc: "2.0", id: 1,
  params: { name: methodName, arguments: methodArgs },
});

post(url, {
  "Content-Type": "application/json",
  "X-INFORMAT-AGENT-TOKEN": agentToken,
}, body, function (err, text) {
  if (err) { console.error(err.message); process.exit(1); }
  var data;
  try { data = JSON.parse(text); } catch (e) { console.log(text); return; }
  if (data.error) {
    console.error("Error (" + data.error.code + "): " + data.error.message);
    process.exit(1);
  }
  var contents = (data.result && data.result.content) || [];
  for (var i = 0; i < contents.length; i++) {
    var item = contents[i];
    if (item.type === "text") {
      try { console.log(JSON.stringify(JSON.parse(item.text), null, 2)); } catch (_) { console.log(item.text); }
    } else {
      console.log(JSON.stringify(item, null, 2));
    }
  }
});
