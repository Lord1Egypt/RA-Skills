#!/usr/bin/env node
const manifest = {
  "baseUrl": "https://api.justserpapi.com",
  "description": "Call GET /api/v1/google/patents/search for Google SERP Patents Search through Just Serp API with query.",
  "displayName": "Google SERP Patents Search",
  "openapi": "3.1.0",
  "platformKey": "google",
  "primaryTag": "Google SERP",
  "skillName": "justserpapi_google_patents_search",
  "slug": "justserpapi-google-patents-search",
  "sourceTitle": "API Shop Documentation",
  "operations": [
    {
      "description": "Get Google patent Search data, including filters, for patent discovery and portfolio monitoring.",
      "method": "GET",
      "operationId": "patentSearch",
      "parameters": [
        {
          "defaultValue": null,
          "description": "The search query for patents (e.g., 'autonomous vehicles', 'blockchain security').",
          "enumValues": [],
          "location": "query",
          "name": "query",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "The results page number. Use 0 for the first page, 1 for the second, and so on.",
          "enumValues": [],
          "location": "query",
          "name": "page",
          "required": false,
          "schemaType": "integer"
        },
        {
          "defaultValue": null,
          "description": "The number of results to return per page (range: 1-100).",
          "enumValues": [],
          "location": "query",
          "name": "num",
          "required": false,
          "schemaType": "integer"
        },
        {
          "defaultValue": null,
          "description": "Sorting order for patent results. Supported values: 'new' (Newest), 'old' (Oldest).",
          "enumValues": [],
          "location": "query",
          "name": "sort",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "If set to true, results will be grouped by classification.",
          "enumValues": [],
          "location": "query",
          "name": "clustered",
          "required": false,
          "schemaType": "boolean"
        },
        {
          "defaultValue": null,
          "description": "Deduplication method. Supported values: 'language' (by Publication).",
          "enumValues": [],
          "location": "query",
          "name": "dups",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Whether to include Google Patents results.",
          "enumValues": [],
          "location": "query",
          "name": "patents",
          "required": false,
          "schemaType": "boolean"
        },
        {
          "defaultValue": null,
          "description": "Whether to include Google Scholar results.",
          "enumValues": [],
          "location": "query",
          "name": "scholar",
          "required": false,
          "schemaType": "boolean"
        },
        {
          "defaultValue": null,
          "description": "Latest date to include. Format: 'type:YYYYMMDD' (e.g., 'publication:20230101').",
          "enumValues": [],
          "location": "query",
          "name": "before",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Earliest date to include. Format: 'type:YYYYMMDD' (e.g., 'filing:20200101').",
          "enumValues": [],
          "location": "query",
          "name": "after",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Filter by patent inventor(s). Multiple values can be comma-separated.",
          "enumValues": [],
          "location": "query",
          "name": "inventor",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Filter by patent assignee(s). Multiple values can be comma-separated.",
          "enumValues": [],
          "location": "query",
          "name": "assignee",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Set the target country code (e.g., 'us', 'uk') to localize results. See <a href=\"/reference/google-countries\">Google Countries</a>.",
          "enumValues": [],
          "location": "query",
          "name": "country",
          "required": false,
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
          "description": "Filter by patent status. Supported values: 'GRANT', 'APPLICATION'.",
          "enumValues": [],
          "location": "query",
          "name": "status",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Filter by patent type. Supported values: 'PATENT', 'DESIGN'.",
          "enumValues": [],
          "location": "query",
          "name": "type",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Filter by litigation status. Supported values: 'YES', 'NO'.",
          "enumValues": [],
          "location": "query",
          "name": "litigation",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/v1/google/patents/search",
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
        "Google Patent"
      ]
    }
  ],
  "endpointPath": "patents/search",
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
