#!/usr/bin/env node
const manifest = {
  "baseUrl": "https://api.justoneapi.com",
  "description": "Analyze Social Media workflows with JustOneAPI, including cross-Platform Search.",
  "displayName": "Social Media",
  "openapi": "3.1.0",
  "platformKey": "search",
  "primaryTag": "Social Media",
  "skillName": "justoneapi_search",
  "slug": "justoneapi-search",
  "sourceTitle": "OpenAPI definition",
  "operations": [
    {
      "description": "Get cross-platform social media search data, including Xiaohongshu, Douyin, Kuaishou, WeChat, Bilibili, Weibo and Zhihu results, for trend research and monitoring.",
      "method": "GET",
      "operationId": "searchCrossPlatformV1",
      "parameters": [
        {
          "defaultValue": null,
          "description": "Access token for this API service.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Search query string. Supports:\n- Multiple keywords (AND): keyword1 keyword2\n- Multiple keywords (OR): keyword1~keyword2\n- Excluded keywords (NOT): required_keyword -excluded_keyword",
          "enumValues": [],
          "location": "query",
          "name": "keyword",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": "ALL",
          "description": "Target social media platform for search filtering.\n\nAvailable Values:\n- `ALL`: All platforms\n- `NEWS`: News\n- `WEIBO`: Sina Weibo\n- `WEIXIN`: Weixin (WeChat)\n- `ZHIHU`: Zhihu\n- `DOUYIN`: Douyin (TikTok China)\n- `XIAOHONGSHU`: Xiaohongshu (Little Red Book)\n- `BILIBILI`: Bilibili\n- `KUAISHOU`: Kuaishou",
          "enumValues": [
            "ALL",
            "NEWS",
            "WEIBO",
            "WEIXIN",
            "ZHIHU",
            "DOUYIN",
            "XIAOHONGSHU",
            "BILIBILI",
            "KUAISHOU"
          ],
          "location": "query",
          "name": "source",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Start time of the search period (yyyy-MM-dd HH:mm:ss). Required for initial request.",
          "enumValues": [],
          "location": "query",
          "name": "start",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "End time of the search period (yyyy-MM-dd HH:mm:ss). Required for initial request.",
          "enumValues": [],
          "location": "query",
          "name": "end",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Pagination cursor provided by the 'nextCursor' field in the previous response.",
          "enumValues": [],
          "location": "query",
          "name": "nextCursor",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/search/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Cross-Platform Search",
      "tags": [
        "Social Media"
      ]
    }
  ]
};
const args = parseArgs(process.argv.slice(2));

if (!args.operation) {
  fail("Missing required --operation argument.");
}

const operation = manifest.operations.find((item) => item.operationId === args.operation);
if (!operation) {
  fail(`Unknown operation "${args.operation}".`, { availableOperations: manifest.operations.map((item) => item.operationId) });
}

const params = parseParams(args.paramsJson);
applyDefaults(operation, params);
injectToken(operation, params, args.token);
validateRequired(operation, params);

const baseUrl = manifest.baseUrl;
const url = new URL(operation.path, ensureBaseUrl(baseUrl));
applyPathParams(operation, params, url);
applyQueryParams(operation, params, url);

const requestInit = {
  headers: {
    "accept": "application/json",
  },
  method: operation.method,
};

if (operation.requestBody && params.body !== undefined) {
  requestInit.body = JSON.stringify(params.body);
  requestInit.headers["content-type"] = operation.requestBody.contentType || "application/json";
}

let response;
try {
  response = await fetch(url, requestInit);
} catch (error) {
  fail("Network request failed.", {
    cause: error instanceof Error ? error.message : String(error),
    operationId: operation.operationId,
  });
}

const rawBody = await response.text();
let parsedBody;
try {
  parsedBody = rawBody ? JSON.parse(rawBody) : null;
} catch (error) {
  if (!response.ok) {
    fail("Backend returned a non-JSON error response.", {
      body: rawBody,
      operationId: operation.operationId,
      status: response.status,
      statusText: response.statusText,
    });
  }
  fail("Backend returned invalid JSON.", {
    body: rawBody,
    operationId: operation.operationId,
    status: response.status,
    statusText: response.statusText,
  });
}

if (!response.ok) {
  fail("Backend request failed.", {
    body: parsedBody,
    operationId: operation.operationId,
    status: response.status,
    statusText: response.statusText,
  });
}

process.stdout.write(`${JSON.stringify(parsedBody, null, 2)}\n`);

function parseArgs(argv) {
  const parsed = { operation: null, paramsJson: "{}", token: null };
  for (let index = 0; index < argv.length; index += 1) {
    const flag = argv[index];
    const value = argv[index + 1];
    if (flag === "--operation") {
      parsed.operation = value;
      index += 1;
      continue;
    }
    if (flag === "--params-json") {
      parsed.paramsJson = value;
      index += 1;
      continue;
    }
    if (flag === "--token") {
      parsed.token = value;
      index += 1;
      continue;
    }
    fail(`Unknown argument "${flag}".`);
  }
  return parsed;
}

function parseParams(input) {
  try {
    const parsed = JSON.parse(input || "{}");
    if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) {
      fail("--params-json must decode to a JSON object.");
    }
    return parsed;
  } catch (error) {
    fail("Failed to parse --params-json.", {
      cause: error instanceof Error ? error.message : String(error),
    });
  }
}

function applyDefaults(operation, params) {
  for (const parameter of operation.parameters) {
    if (params[parameter.name] === undefined && parameter.defaultValue !== null) {
      params[parameter.name] = parameter.defaultValue;
    }
  }
}

function injectToken(operation, params, cliToken) {
  const tokenParam = operation.parameters.find((parameter) => parameter.name === "token");
  if (!tokenParam || params.token !== undefined) {
    return;
  }
  if (!cliToken) {
    fail("--token is required for this operation.", {
      operationId: operation.operationId,
    });
  }
  params.token = cliToken;
}

function validateRequired(operation, params) {
  const missing = [];
  for (const parameter of operation.parameters) {
    if (parameter.required && params[parameter.name] === undefined) {
      missing.push(parameter.name);
    }
  }
  if (operation.requestBody?.required && params.body === undefined) {
    missing.push("body");
  }
  if (missing.length) {
    fail("Missing required parameters.", {
      missing,
      operationId: operation.operationId,
    });
  }
}

function applyPathParams(operation, params, url) {
  let pathname = url.pathname;
  for (const parameter of operation.parameters.filter((item) => item.location === "path")) {
    const value = params[parameter.name];
    if (value === undefined) {
      continue;
    }
    pathname = pathname.replace(`{${parameter.name}}`, encodeURIComponent(String(value)));
  }
  url.pathname = pathname;
}

function applyQueryParams(operation, params, url) {
  for (const parameter of operation.parameters.filter((item) => item.location === "query")) {
    const value = params[parameter.name];
    if (value === undefined) {
      continue;
    }
    appendValue(url.searchParams, parameter.name, value);
  }
}

function appendValue(searchParams, name, value) {
  if (Array.isArray(value)) {
    for (const item of value) {
      appendValue(searchParams, name, item);
    }
    return;
  }
  if (value && typeof value === "object") {
    searchParams.append(name, JSON.stringify(value));
    return;
  }
  searchParams.append(name, String(value));
}

function ensureBaseUrl(value) {
  return value.endsWith("/") ? value : `${value}/`;
}

function fail(message, details = null) {
  const payload = { message };
  if (details) {
    payload.details = details;
  }
  process.stderr.write(`${JSON.stringify(payload, null, 2)}\n`);
  process.exit(1);
}
