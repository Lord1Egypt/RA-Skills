#!/usr/bin/env node
const manifest = {
  "baseUrl": "https://api.justoneapi.com",
  "description": "Analyze Kuaishou workflows with JustOneAPI, including user Search, user Published Videos, and video Details across 7 operations.",
  "displayName": "Kuaishou",
  "openapi": "3.1.0",
  "platformKey": "kuaishou",
  "primaryTag": "Kuaishou",
  "skillName": "justoneapi_kuaishou",
  "slug": "justoneapi-kuaishou",
  "sourceTitle": "OpenAPI definition",
  "operations": [
    {
      "description": "Get Kuaishou user Profile data, including account metadata, audience metrics, and verification-related fields, for creator research and building creator profiles and monitoring audience growth and account status.",
      "method": "GET",
      "operationId": "getUserProfileV1",
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
          "description": "The unique user ID on Kuaishou.",
          "enumValues": [],
          "location": "query",
          "name": "userId",
          "required": true,
          "schemaType": "string"
        }
      ],
      "path": "/api/kuaishou/get-user-detail/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "User Profile",
      "tags": [
        "Kuaishou"
      ]
    },
    {
      "description": "Get Kuaishou user Published Videos data, including covers, publish times, and engagement metrics, for creator monitoring and content performance analysis.",
      "method": "GET",
      "operationId": "getKuaishouUserVideoListV2",
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
          "description": "The unique user ID on Kuaishou.",
          "enumValues": [],
          "location": "query",
          "name": "userId",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Pagination cursor for subsequent pages.",
          "enumValues": [],
          "location": "query",
          "name": "pcursor",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/kuaishou/get-user-video-list/v2",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "User Published Videos",
      "tags": [
        "Kuaishou"
      ]
    },
    {
      "description": "Retrieves public comments of a Kuaishou video, including comment content,\nauthor info, like count, and reply count.\n\nTypical use cases:\n- Sentiment analysis and community feedback monitoring\n- Gathering engagement data for specific videos",
      "method": "GET",
      "operationId": "getVideoCommentsV1",
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
          "description": "The unique ID of the Kuaishou video, e.g. `3xbknvct79h46h9` or refer_photo_id `177012131237`",
          "enumValues": [],
          "location": "query",
          "name": "videoId",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Pagination cursor for subsequent pages.",
          "enumValues": [],
          "location": "query",
          "name": "pcursor",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/kuaishou/get-video-comment/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Video Comments",
      "tags": [
        "Kuaishou"
      ]
    },
    {
      "description": "Get Kuaishou video Details data, including video URL, caption, and author info, for in-depth content performance analysis and building databases of viral videos.",
      "method": "GET",
      "operationId": "getVideoDetailsV2",
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
          "description": "The unique ID of the Kuaishou video, e.g. `3xg9avuebhtfcku`",
          "enumValues": [],
          "location": "query",
          "name": "videoId",
          "required": true,
          "schemaType": "string"
        }
      ],
      "path": "/api/kuaishou/get-video-detail/v2",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Video Details",
      "tags": [
        "Kuaishou"
      ]
    },
    {
      "description": "Get Kuaishou user Search data, including profile names, avatars, and follower counts, for creator discovery and account research.",
      "method": "GET",
      "operationId": "searchKuaishouUserV2",
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
          "description": "The search keyword to find users.",
          "enumValues": [],
          "location": "query",
          "name": "keyword",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": 1,
          "description": "Page number for results, starting from 1.",
          "enumValues": [],
          "location": "query",
          "name": "page",
          "required": false,
          "schemaType": "integer"
        }
      ],
      "path": "/api/kuaishou/search-user/v2",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "User Search",
      "tags": [
        "Kuaishou"
      ]
    },
    {
      "description": "Get Kuaishou video Search data, including video ID, cover image, and description, for competitive analysis and market trends and keywords monitoring and brand tracking.",
      "method": "GET",
      "operationId": "searchKuaishouVideoV2",
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
          "description": "The search keyword to find videos.",
          "enumValues": [],
          "location": "query",
          "name": "keyword",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": 1,
          "description": "Page number for results, starting from 1.",
          "enumValues": [],
          "location": "query",
          "name": "page",
          "required": false,
          "schemaType": "integer"
        }
      ],
      "path": "/api/kuaishou/search-video/v2",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Video Search",
      "tags": [
        "Kuaishou"
      ]
    },
    {
      "description": "Get Kuaishou share Link Resolution data, including resolved content identifier and target object data, for resolving shared links for automated content processing.",
      "method": "GET",
      "operationId": "shareLinkResolutionV1",
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
          "description": "Kuaishou share URL (must start with 'https://v.kuaishou.com/').",
          "enumValues": [],
          "location": "query",
          "name": "shareUrl",
          "required": true,
          "schemaType": "string"
        }
      ],
      "path": "/api/kuaishou/share-url-transfer/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Share Link Resolution",
      "tags": [
        "Kuaishou"
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
