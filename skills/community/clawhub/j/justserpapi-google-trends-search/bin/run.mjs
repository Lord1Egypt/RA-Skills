#!/usr/bin/env node
const manifest = {
  "baseUrl": "https://api.justserpapi.com",
  "description": "Call GET /api/v1/google/trends/search for Google SERP Trends Search through Just Serp API with query.",
  "displayName": "Google SERP Trends Search",
  "openapi": "3.1.0",
  "platformKey": "google",
  "primaryTag": "Google SERP",
  "skillName": "justserpapi_google_trends_search",
  "slug": "justserpapi-google-trends-search",
  "sourceTitle": "API Shop Documentation",
  "operations": [
    {
      "description": "Get Google trends Search data, including interest over time, geo breakdowns, and related queries, for demand analysis and seasonal trend monitoring.",
      "method": "GET",
      "operationId": "TrendsSearch",
      "parameters": [
        {
          "defaultValue": null,
          "description": "The search term or topic ID to analyze in Google Trends (e.g., 'iPhone', '/m/027lnzs' for Bitcoin). You can provide up to 5 terms separated by commas for comparisons.",
          "enumValues": [],
          "location": "query",
          "name": "query",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Set the language for the results using its two-letter code (e.g., 'en' for English, 'fr' for French). See <a href=\"/reference/google-language\">Google Language</a>.",
          "enumValues": [],
          "location": "query",
          "name": "language",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "The geographic location code to filter trends (e.g., 'US', 'GB'). Omit for worldwide trends. See <a href=\"/reference/google-trends-locations\">Google Trends Locations</a>.",
          "enumValues": [],
          "location": "query",
          "name": "geo",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Refines results for region charts. Supported values: 'COUNTRY', 'REGION', 'DMA', 'CITY'.",
          "enumValues": [],
          "location": "query",
          "name": "region",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "The type of trend data to retrieve. Supported values: 'TIMESERIES' (Interest over time), 'GEO_MAP' (Breakdown by region).",
          "enumValues": [],
          "location": "query",
          "name": "data_type",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Time zone offset in minutes (e.g., '420' for PDT). Range: -1439 to 1439.",
          "enumValues": [],
          "location": "query",
          "name": "tz",
          "required": false,
          "schemaType": "integer"
        },
        {
          "defaultValue": null,
          "description": "The search category code (e.g., '0' for all categories).",
          "enumValues": [],
          "location": "query",
          "name": "cat",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "The Google property to filter trends. Supported values: 'images', 'news', 'froogle' (Shopping), 'youtube'.",
          "enumValues": [],
          "location": "query",
          "name": "gprop",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Date range filter for the search. Supports predefined values (now 1-H, now 4-H, now 1-d, now 7-d, today 1-m, today 3-m, today 12-m, today 5-y, all) and custom ranges: yyyy-mm-dd yyyy-mm-dd (e.g. 2021-10-15 2022-05-25) or hourly yyyy-mm-ddThh yyyy-mm-ddThh within 1 week (e.g. 2022-05-19T10 2022-05-24T22, based on tz).",
          "enumValues": [],
          "location": "query",
          "name": "date",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/v1/google/trends/search",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        },
        {
          "description": "Authentication failed: API Key is invalid or missing",
          "statusCode": "401"
        },
        {
          "description": "Access denied: Insufficient credits or quota exceeded",
          "statusCode": "403"
        },
        {
          "description": "Internal server error or upstream service exception",
          "statusCode": "500"
        }
      ],
      "summary": "Search",
      "tags": [
        "Google Trends"
      ]
    }
  ],
  "endpointPath": "trends/search",
  "skillType": "interface"
};
const args = parseArgs(process.argv.slice(2));

if (!args.operation) {
  fail("Missing required --operation argument.");
}

const operation = manifest.operations.find((item) => item.operationId === args.operation);
if (!operation) {
  fail(`Unknown operation "${args.operation}".`, { availableOperations: manifest.operations.map((item) => item.operationId) });
}

if (!args.apiKey) {
  fail("Missing required --api-key argument.");
}

const params = parseParams(args.paramsJson);
applyDefaults(operation, params);
validateRequired(operation, params);

const baseUrl = manifest.baseUrl;
const url = new URL(operation.path, ensureBaseUrl(baseUrl));
applyPathParams(operation, params, url);
applyQueryParams(operation, params, url);

const requestInit = {
  headers: {
    "accept": "application/json",
    "X-API-Key": args.apiKey,
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
  const parsed = { apiKey: null, operation: null, paramsJson: "{}" };
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
    if (flag === "--api-key") {
      parsed.apiKey = value;
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
