#!/usr/bin/env node
const manifest = {
  "baseUrl": "https://api.justoneapi.com",
  "description": "Analyze Facebook workflows with JustOneAPI, including post Search, get Profile ID, and get Profile Posts.",
  "displayName": "Facebook",
  "openapi": "3.1.0",
  "platformKey": "facebook",
  "primaryTag": "Facebook",
  "skillName": "justoneapi_facebook",
  "slug": "justoneapi-facebook",
  "sourceTitle": "OpenAPI definition",
  "operations": [
    {
      "description": "Retrieve the unique Facebook profile ID from a given profile URL.",
      "method": "GET",
      "operationId": "getProfileIdV1",
      "parameters": [
        {
          "defaultValue": null,
          "description": "User security token for API access authentication.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "The path part of the Facebook profile URL. Do not include `https://www.facebook.com`. Example: `/people/To-Bite/pfbid021XLeDjjZjsoWse1H43VEgb3i1uCLTpBvXSvrnL2n118YPtMF5AZkBrZobhWWdHTHl/`",
          "enumValues": [],
          "location": "query",
          "name": "url",
          "required": true,
          "schemaType": "string"
        }
      ],
      "path": "/api/facebook/get-profile-id/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Get Profile ID",
      "tags": [
        "Facebook"
      ]
    },
    {
      "description": "Get public posts from a specific Facebook profile using its profile ID.",
      "method": "GET",
      "operationId": "getProfilePostsV1",
      "parameters": [
        {
          "defaultValue": null,
          "description": "User security token for API access authentication.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "The unique Facebook profile ID.",
          "enumValues": [],
          "location": "query",
          "name": "profileId",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": "",
          "description": "Pagination cursor for fetching the next set of results.",
          "enumValues": [],
          "location": "query",
          "name": "cursor",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/facebook/get-profile-posts/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Get Profile Posts",
      "tags": [
        "Facebook"
      ]
    },
    {
      "description": "Get Facebook post Search data, including matched results, metadata, and ranking signals, for discovering relevant public posts for specific keywords and analyzing engagement and reach of public content on facebook.",
      "method": "GET",
      "operationId": "searchFacebookPostsV1",
      "parameters": [
        {
          "defaultValue": null,
          "description": "User security token for API access authentication.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Keyword to search for in public posts. Supports basic text matching.",
          "enumValues": [],
          "location": "query",
          "name": "keyword",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Start date for the search range (inclusive), formatted as yyyy-MM-dd.",
          "enumValues": [],
          "location": "query",
          "name": "startDate",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "End date for the search range (inclusive), formatted as yyyy-MM-dd.",
          "enumValues": [],
          "location": "query",
          "name": "endDate",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": "",
          "description": "Pagination cursor for fetching the next set of results.",
          "enumValues": [],
          "location": "query",
          "name": "cursor",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/facebook/search-post/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Post Search",
      "tags": [
        "Facebook"
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
