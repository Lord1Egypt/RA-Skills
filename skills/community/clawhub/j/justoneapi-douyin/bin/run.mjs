#!/usr/bin/env node
const manifest = {
  "baseUrl": "https://api.justoneapi.com",
  "description": "Analyze Douyin (TikTok China) workflows with JustOneAPI, including user Profile, user Published Videos, and video Details across 8 operations.",
  "displayName": "Douyin (TikTok China)",
  "openapi": "3.1.0",
  "platformKey": "douyin",
  "primaryTag": "Douyin (TikTok China)",
  "skillName": "justoneapi_douyin",
  "slug": "justoneapi-douyin",
  "sourceTitle": "OpenAPI definition",
  "operations": [
    {
      "description": "Get Douyin (TikTok China) user Profile data, including follower counts, verification status, and bio details, for creator research and account analysis.",
      "method": "GET",
      "operationId": "getUserDetailV3",
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
          "description": "The unique user ID (sec_uid) on Douyin.",
          "enumValues": [],
          "location": "query",
          "name": "secUid",
          "required": true,
          "schemaType": "string"
        }
      ],
      "path": "/api/douyin/get-user-detail/v3",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "User Profile",
      "tags": [
        "Douyin (TikTok China)"
      ]
    },
    {
      "description": "Get Douyin (TikTok China) user Published Videos data, including captions, covers, and publish times, for account monitoring.",
      "method": "GET",
      "operationId": "getUserVideoListV3",
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
          "description": "The unique user ID (sec_uid) on Douyin.",
          "enumValues": [],
          "location": "query",
          "name": "secUid",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": 0,
          "description": "Pagination cursor; use 0 for the first page, and the `max_cursor` from the previous response for subsequent pages.",
          "enumValues": [],
          "location": "query",
          "name": "maxCursor",
          "required": false,
          "schemaType": "integer"
        }
      ],
      "path": "/api/douyin/get-user-video-list/v3",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "User Published Videos",
      "tags": [
        "Douyin (TikTok China)"
      ]
    },
    {
      "description": "Get Douyin (TikTok China) video Comments data, including authors, text, and likes, for sentiment analysis and engagement review.",
      "method": "GET",
      "operationId": "getVideoCommentV1",
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
          "description": "The unique video identifier (aweme_id).",
          "enumValues": [],
          "location": "query",
          "name": "awemeId",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": 1,
          "description": "Page number (starting from 1).",
          "enumValues": [],
          "location": "query",
          "name": "page",
          "required": false,
          "schemaType": "integer"
        }
      ],
      "path": "/api/douyin/get-video-comment/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Video Comments",
      "tags": [
        "Douyin (TikTok China)"
      ]
    },
    {
      "description": "Get Douyin (TikTok China) video Details data, including author details, publish time, and engagement counts, for video research, archiving, and performance analysis.",
      "method": "GET",
      "operationId": "getDouyinVideoDetailV2",
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
          "description": "The unique video identifier (aweme_id or model_id).",
          "enumValues": [],
          "location": "query",
          "name": "videoId",
          "required": true,
          "schemaType": "string"
        }
      ],
      "path": "/api/douyin/get-video-detail/v2",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Video Details",
      "tags": [
        "Douyin (TikTok China)"
      ]
    },
    {
      "description": "Get Douyin (TikTok China) comment Replies data, including text, authors, and timestamps, for thread analysis and feedback research.",
      "method": "GET",
      "operationId": "getVideoSubCommentV1",
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
          "description": "The unique identifier of the top-level comment.",
          "enumValues": [],
          "location": "query",
          "name": "commentId",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": 1,
          "description": "Page number (starting from 1).",
          "enumValues": [],
          "location": "query",
          "name": "page",
          "required": false,
          "schemaType": "integer"
        }
      ],
      "path": "/api/douyin/get-video-sub-comment/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Comment Replies",
      "tags": [
        "Douyin (TikTok China)"
      ]
    },
    {
      "description": "Get Douyin (TikTok China) user Search data, including profile metadata and follower signals, for creator discovery and account research.",
      "method": "GET",
      "operationId": "searchDouyinUserV2",
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
          "description": "The search keyword.",
          "enumValues": [],
          "location": "query",
          "name": "keyword",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": 1,
          "description": "Page number (starting from 1).",
          "enumValues": [],
          "location": "query",
          "name": "page",
          "required": false,
          "schemaType": "integer"
        },
        {
          "defaultValue": null,
          "description": "Filter by user type.\n\nAvailable Values:\n- `common_user`: Common User\n- `enterprise_user`: Enterprise User\n- `personal_user`: Verified Individual User",
          "enumValues": [
            "common_user",
            "enterprise_user",
            "personal_user"
          ],
          "location": "query",
          "name": "userType",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/douyin/search-user/v2",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "User Search",
      "tags": [
        "Douyin (TikTok China)"
      ]
    },
    {
      "description": "Get Douyin (TikTok China) video Search data, including metadata and engagement signals, for content discovery, trend research, and competitive monitoring.",
      "method": "GET",
      "operationId": "searchVideoV4",
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
          "description": "The search keyword.",
          "enumValues": [],
          "location": "query",
          "name": "keyword",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": "_0",
          "description": "Sorting criteria for search results.\n\nAvailable Values:\n- `_0`: General\n- `_1`: More likes\n- `_2`: Newest",
          "enumValues": [
            "_0",
            "_1",
            "_2"
          ],
          "location": "query",
          "name": "sortType",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": "_0",
          "description": "Filter by video publish time range.\n\nAvailable Values:\n- `_0`: No Limit\n- `_1`: Last 24 Hours\n- `_7`: Last 7 Days\n- `_180`: Last 6 Months",
          "enumValues": [
            "_0",
            "_1",
            "_7",
            "_180"
          ],
          "location": "query",
          "name": "publishTime",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": "_0",
          "description": "Filter by video duration.\n\nAvailable Values:\n- `_0`: No Limit\n- `_1`: Under 1 Minute\n- `_2`: 1-5 Minutes\n- `_3`: Over 5 Minutes",
          "enumValues": [
            "_0",
            "_1",
            "_2",
            "_3"
          ],
          "location": "query",
          "name": "duration",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": 1,
          "description": "Page number (starting from 1).",
          "enumValues": [],
          "location": "query",
          "name": "page",
          "required": false,
          "schemaType": "integer"
        },
        {
          "defaultValue": null,
          "description": "Search ID; required for pages > 1 (use the search_id value returned by the last response).",
          "enumValues": [],
          "location": "query",
          "name": "searchId",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/douyin/search-video/v4",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Video Search",
      "tags": [
        "Douyin (TikTok China)"
      ]
    },
    {
      "description": "Get Douyin (TikTok China) share Link Resolution data, including helping extract canonical IDs, for downstream video and comment workflows.",
      "method": "GET",
      "operationId": "shareDouyinUrlTransferV1",
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
          "description": "The Douyin short share URL.",
          "enumValues": [],
          "location": "query",
          "name": "shareUrl",
          "required": true,
          "schemaType": "string"
        }
      ],
      "path": "/api/douyin/share-url-transfer/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Share Link Resolution",
      "tags": [
        "Douyin (TikTok China)"
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
