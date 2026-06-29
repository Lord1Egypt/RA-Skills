#!/usr/bin/env node
const manifest = {
  "baseUrl": "https://api.justserpapi.com",
  "description": "Call GET /api/v1/google/search for Google SERP Search through Just Serp API with query.",
  "displayName": "Google SERP Search",
  "openapi": "3.1.0",
  "platformKey": "google",
  "primaryTag": "Google SERP",
  "skillName": "justserpapi_google_search",
  "slug": "justserpapi-google-search",
  "sourceTitle": "API Shop Documentation",
  "operations": [
    {
      "description": "Get Google search SERP data, including organic results, ads, and knowledge panels, for keyword tracking and SERP analysis across markets.",
      "method": "GET",
      "operationId": "search",
      "parameters": [
        {
          "defaultValue": null,
          "description": "The search query for Google Search (e.g., 'coffee shops', 'how to bake a cake').",
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
          "description": "Set to true to return the raw HTML of the Google search results page alongside the structured data.",
          "enumValues": [],
          "location": "query",
          "name": "html",
          "required": false,
          "schemaType": "boolean"
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
          "description": "Restrict results to one or more languages using the 'lang_{language_code}' format (e.g., 'lang_en'). See <a href=\"/reference/google-lr-language\">Google LR Language</a>.",
          "enumValues": [],
          "location": "query",
          "name": "lr",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "The Google domain to use for the search (e.g., 'google.com', 'google.co.uk'). See <a href=\"/reference/google-domains\">Google Domains</a>.",
          "enumValues": [],
          "location": "query",
          "name": "domain",
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
          "description": "Limits results to search results from specific countries. Format: 'countryXX'. See <a href=\"/reference/google-cr-countries\">Google CR Countries</a>.",
          "enumValues": [],
          "location": "query",
          "name": "cr",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Encoded location string (UULE) used to precisely localize Google search results. This is an advanced/technical parameter — if you’re not familiar with it, you can leave it empty and omit it.",
          "enumValues": [],
          "location": "query",
          "name": "uule",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "The textual location name (e.g., 'New York, NY') to localize the search results.",
          "enumValues": [],
          "location": "query",
          "name": "location",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Google local business CID (place identifier). Used to target a specific Google Business Profile / local listing. Advanced parameter — if you don’t know it, you can omit it.",
          "enumValues": [],
          "location": "query",
          "name": "ludocid",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Signature parameter (lsig) sometimes required for certain Knowledge Graph / local map view features. This is an advanced technical parameter — if you’re not familiar with it, you can leave it empty.",
          "enumValues": [],
          "location": "query",
          "name": "lsig",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Knowledge Graph entity/listing ID (KGMID) used to retrieve details for a specific entity. This is an advanced technical parameter — if you’re not familiar with it, you can leave it empty.",
          "enumValues": [],
          "location": "query",
          "name": "kgmid",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Cached search context parameter (si) used to reproduce specific Google search result views/context (e.g. some Knowledge Graph tabs). This is an advanced technical parameter — if you’re not familiar with it, you can leave it empty.",
          "enumValues": [],
          "location": "query",
          "name": "si",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Parameter (ibp) used to control certain Google UI expansions or rendering modes (commonly in local/business result views). This is an advanced technical parameter — if you’re not familiar with it, you can leave it empty.",
          "enumValues": [],
          "location": "query",
          "name": "ibp",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Advanced filter token (uds) used for specific Google search sub-filters. This is an advanced technical parameter, usually provided by Google in filter options/results — if you’re not familiar with it, you can leave it empty.",
          "enumValues": [],
          "location": "query",
          "name": "uds",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Advanced search filter parameter (tbs) used to apply Google result filters (e.g. time range). This is an advanced parameter — if you’re not familiar with it, you can leave it empty.",
          "enumValues": [],
          "location": "query",
          "name": "tbs",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "SafeSearch filter setting. Set to 'active' to filter adult content, or 'off' to disable it.",
          "enumValues": [],
          "location": "query",
          "name": "safe",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Controls Google's auto-correction. Set to '1' to exclude corrected results, '0' to include them.",
          "enumValues": [],
          "location": "query",
          "name": "nfpr",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Toggle 'Similar Results' and 'Omitted Results' filters. Set to '1' (default) to enable, '0' to disable.",
          "enumValues": [],
          "location": "query",
          "name": "filter",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/v1/google/search",
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
        "Google"
      ]
    }
  ],
  "endpointPath": "search",
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
