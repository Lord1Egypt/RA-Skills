#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

const GENERATED_PATH = path.join(__dirname, "commands.generated.json");
const generated = JSON.parse(fs.readFileSync(GENERATED_PATH, "utf8"));
const BASE_URL = process.env.HUBSTUDIO_BASE_URL || generated.baseUrl || "http://127.0.0.1:6873";
const COMMANDS = generated.commands || [];
const COMMAND_MAP = new Map(COMMANDS.map((c) => [c.command, c]));

const ALIASES = {
  browserCreate: "postV1EnvCreate",
  browserStart: "postV1BrowserStart",
  browserStop: "postV1BrowserStop",
  browserStatus: "postV1BrowserAllBrowserStatus",
  browserForeground: "postV1BrowserForeground",
  browserStopAll: "postV1BrowserStopAll",
  displayAll: "postV1DisplayAll",
  browserArrange: "postV1BrowserArrange",
};

function printHelp() {
  console.log(`HubStudio CLI

Usage:
  node hubstudio.js <command> [args] [--body '{"k":"v"}'] [--query '{"k":"v"}']

Commands:
  browserCreate [name]              Create browser environment
  browserStart <containerCode>      Start browser environment
  browserStop <containerCode>       Stop browser environment
  browserStatus [containerCode]     Query running browser status
  browserForeground <containerCode> Bring browser window to front
  browserStopAll [clearOpening]     Close all environments
  displayAll                        Get all physical screens
  browserArrange [screenId]         Arrange browser windows
  list                              List all generated commands
  testAll                           Test all generated endpoints
  help                              Show this help

Generated commands:
  ${COMMANDS.length} commands are available, e.g.:
  - postV1BrowserStart
  - postV1BrowserStop
  - postV1EnvCreate

Env:
  HUBSTUDIO_BASE_URL           Default: http://127.0.0.1:6873
`);
}

function parseJsonArg(flag, value) {
  if (!value) {
    throw new Error(`Missing value for ${flag}`);
  }
  try {
    return JSON.parse(value);
  } catch (err) {
    throw new Error(`Invalid JSON for ${flag}: ${err.message}`);
  }
}

function parseCommandArgs(rawArgs) {
  const positional = [];
  let bodyOverride = null;
  let queryOverride = null;

  for (let i = 0; i < rawArgs.length; i += 1) {
    const token = rawArgs[i];
    if (token === "--body") {
      bodyOverride = parseJsonArg("--body", rawArgs[i + 1]);
      i += 1;
      continue;
    }
    if (token === "--query") {
      queryOverride = parseJsonArg("--query", rawArgs[i + 1]);
      i += 1;
      continue;
    }
    positional.push(token);
  }

  return { positional, bodyOverride, queryOverride };
}

async function post(endpointPath, body = {}, query = null) {
  const url = new URL(endpointPath, BASE_URL);
  if (query && typeof query === "object") {
    for (const [k, v] of Object.entries(query)) {
      if (v !== undefined && v !== null) {
        url.searchParams.set(k, String(v));
      }
    }
  }

  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  let payload = null;
  try {
    payload = await response.json();
  } catch {
    payload = { raw: await response.text() };
  }

  return { status: response.status, payload };
}

function printResult(result) {
  console.log(JSON.stringify(result, null, 2));
}

function requiredArg(name, value) {
  if (!value) {
    throw new Error(`Missing required argument: ${name}`);
  }
}

function getGeneratedCommand(commandName) {
  const resolved = ALIASES[commandName] || commandName;
  const cmd = COMMAND_MAP.get(resolved);
  if (!cmd) {
    throw new Error(`Unknown command: ${commandName}`);
  }
  return cmd;
}

function resolveCallInputs(commandName, positional, bodyOverride, queryOverride) {
  const generatedCmd = getGeneratedCommand(commandName);
  const body = { ...(generatedCmd.defaultBody || {}) };
  const query = { ...(generatedCmd.defaultQuery || {}) };

  if (commandName === "browserCreate") {
    const name = positional[0] || `NodeAuto-${Date.now()}`;
    body.containerName = name;
    body.asDynamicType = 1;
    body.proxyTypeName = "不使用代理";
  } else if (commandName === "browserStart" || commandName === "browserForeground") {
    requiredArg("containerCode", positional[0]);
    body.containerCode = positional[0];
  } else if (commandName === "browserStop") {
    requiredArg("containerCode", positional[0]);
    body.containerCode = positional[0];
    query.containerCode = positional[0];
  } else if (commandName === "browserStatus") {
    if (positional[0]) {
      body.containerCode = [positional[0]];
    }
  } else if (commandName === "browserStopAll") {
    body.clearOpening = positional[0] ? positional[0] === "true" : false;
  } else if (commandName === "browserArrange" && positional[0]) {
    body.screenId = Number(positional[0]);
  }

  const finalBody = bodyOverride && typeof bodyOverride === "object" ? bodyOverride : body;
  const finalQuery = queryOverride && typeof queryOverride === "object" ? queryOverride : query;
  return { generatedCmd, finalBody, finalQuery };
}

function normalizeResult(command, generatedCmd, result, body, query) {
  return {
    command,
    method: generatedCmd.method,
    path: generatedCmd.path,
    status: result.status,
    code: result.payload && Object.prototype.hasOwnProperty.call(result.payload, "code") ? result.payload.code : null,
    msg: result.payload && Object.prototype.hasOwnProperty.call(result.payload, "msg") ? result.payload.msg : null,
    success:
      result.status < 400 &&
      (!result.payload || !Object.prototype.hasOwnProperty.call(result.payload, "code") || result.payload.code === 0),
    request: { body, query },
    payload: result.payload,
  };
}

async function runTestAll() {
  const results = [];
  for (const cmd of COMMANDS) {
    try {
      const result = await post(cmd.path, cmd.defaultBody || {}, cmd.defaultQuery || {});
      results.push(normalizeResult(cmd.command, cmd, result, cmd.defaultBody || {}, cmd.defaultQuery || {}));
    } catch (err) {
      results.push({
        command: cmd.command,
        method: cmd.method,
        path: cmd.path,
        status: null,
        code: null,
        msg: err.message,
        success: false,
        request: { body: cmd.defaultBody || {}, query: cmd.defaultQuery || {} },
        payload: null,
      });
    }
  }

  const summary = {
    total: results.length,
    success: results.filter((x) => x.success).length,
    failed: results.filter((x) => !x.success).length,
  };
  const report = {
    baseUrl: BASE_URL,
    testedAt: new Date().toISOString(),
    summary,
    results,
  };

  const reportPath = path.join(__dirname, "scripts", "node_test_all_report.json");
  fs.writeFileSync(reportPath, JSON.stringify(report, null, 2), "utf8");
  return { summary, reportPath, report };
}

async function main() {
  const [, , command, ...rawArgs] = process.argv;

  if (!command || command === "help" || command === "--help" || command === "-h") {
    printHelp();
    return;
  }

  if (command === "list") {
    const items = COMMANDS.map((c) => ({
      command: c.command,
      method: c.method,
      path: c.path,
      summary: c.summary,
    }));
    printResult({ total: items.length, commands: items });
    return;
  }

  if (command === "testAll") {
    const out = await runTestAll();
    printResult({
      summary: out.summary,
      reportPath: out.reportPath,
    });
    if (out.summary.failed > 0) {
      process.exitCode = 2;
    }
    return;
  }

  const { positional, bodyOverride, queryOverride } = parseCommandArgs(rawArgs);
  const { generatedCmd, finalBody, finalQuery } = resolveCallInputs(
    command,
    positional,
    bodyOverride,
    queryOverride
  );
  const result = await post(generatedCmd.path, finalBody, finalQuery);
  const normalized = normalizeResult(command, generatedCmd, result, finalBody, finalQuery);
  printResult(normalized);

  if (normalized.status >= 400) {
    process.exitCode = 1;
    return;
  }
  if (normalized.code !== null && normalized.code !== 0) {
    process.exitCode = 2;
  }
}

main().catch((err) => {
  console.error(err.message || String(err));
  process.exit(1);
});
