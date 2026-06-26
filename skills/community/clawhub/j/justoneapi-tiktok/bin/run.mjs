#!/usr/bin/env node
const manifest = {
  "baseUrl": "https://api.justoneapi.com",
  "description": "Analyze TikTok workflows with JustOneAPI, including user Published Posts, post Details, and user Profile across 7 operations.",
  "displayName": "TikTok",
  "openapi": "3.1.0",
  "platformKey": "tiktok",
  "primaryTag": "TikTok",
  "skillName": "justoneapi_tiktok",
  "slug": "justoneapi-tiktok",
  "sourceTitle": "OpenAPI definition",
  "operations": [
    {
      "description": "Get TikTok post Comments data, including comment ID, user information, and text content, for sentiment analysis of the audience's reaction to specific content and engagement measurement via comment volume and quality.",
      "method": "GET",
      "operationId": "getPostCommentV1",
      "parameters": [
        {
          "defaultValue": null,
          "description": "Security token for API access.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "The unique ID of the TikTok post (awemeId).",
          "enumValues": [],
          "location": "query",
          "name": "awemeId",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": "0",
          "description": "Pagination cursor. Start with '0'.",
          "enumValues": [],
          "location": "query",
          "name": "cursor",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/tiktok/get-post-comment/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Post Comments",
      "tags": [
        "TikTok"
      ]
    },
    {
      "description": "Get TikTok post Details data, including video ID, author information, and description text, for content performance analysis and metadata extraction and influencer evaluation via specific post metrics.",
      "method": "GET",
      "operationId": "getTiktokPostDetailV1",
      "parameters": [
        {
          "defaultValue": null,
          "description": "Security token for API access.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "The unique ID of the TikTok post.",
          "enumValues": [],
          "location": "query",
          "name": "postId",
          "required": true,
          "schemaType": "string"
        }
      ],
      "path": "/api/tiktok/get-post-detail/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Post Details",
      "tags": [
        "TikTok"
      ]
    },
    {
      "description": "Get TikTok comment Replies data, including reply ID, user information, and text content, for understanding detailed user interactions and threaded discussions and identifying influencers or active participants within a comment section.",
      "method": "GET",
      "operationId": "getPostSubCommentV1",
      "parameters": [
        {
          "defaultValue": null,
          "description": "Security token for API access.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "The unique ID of the TikTok post.",
          "enumValues": [],
          "location": "query",
          "name": "awemeId",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "The unique ID of the comment to retrieve replies for.",
          "enumValues": [],
          "location": "query",
          "name": "commentId",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": "0",
          "description": "Pagination cursor. Start with '0'.",
          "enumValues": [],
          "location": "query",
          "name": "cursor",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/tiktok/get-post-sub-comment/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Comment Replies",
      "tags": [
        "TikTok"
      ]
    },
    {
      "description": "Get TikTok user Profile data, including nickname, unique ID, and avatar, for influencer profiling and audience analysis, account performance tracking and growth monitoring, and identifying verified status and official accounts.",
      "method": "GET",
      "operationId": "getTiktokUserDetailV1",
      "parameters": [
        {
          "defaultValue": null,
          "description": "Security token for API access.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": "",
          "description": "The unique handle/username of the user (e.g., 'tiktok').",
          "enumValues": [],
          "location": "query",
          "name": "uniqueId",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": "",
          "description": "The unique security ID of the user.",
          "enumValues": [],
          "location": "query",
          "name": "secUid",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/tiktok/get-user-detail/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "User Profile",
      "tags": [
        "TikTok"
      ]
    },
    {
      "description": "Get TikTok user Published Posts data, including video ID, description, and publish time, for user activity analysis and posting frequency tracking, influencer performance evaluation, and content trend monitoring for specific creators.",
      "method": "GET",
      "operationId": "getUserPostV1",
      "parameters": [
        {
          "defaultValue": null,
          "description": "Security token for API access.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "The unique security ID of the TikTok user (e.g., MS4wLjABAAAAonP2...).",
          "enumValues": [],
          "location": "query",
          "name": "secUid",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": "0",
          "description": "Pagination cursor. Use '0' for the first page, then use the 'cursor' value returned in the previous response.",
          "enumValues": [],
          "location": "query",
          "name": "cursor",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": "_0",
          "description": "Sorting criteria for the user's posts.\n\nAvailable Values:\n- `_0`: Default (Mixed)\n- `_1`: Highest Liked\n- `_2`: Latest Published",
          "enumValues": [
            "_0",
            "_1",
            "_2"
          ],
          "location": "query",
          "name": "sort",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/tiktok/get-user-post/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "User Published Posts",
      "tags": [
        "TikTok"
      ]
    },
    {
      "description": "Get TikTok post Search data, including key details such as video ID, description, and author information, for trend monitoring and content discovery and keyword-based market analysis and sentiment tracking.",
      "method": "GET",
      "operationId": "searchPostV1",
      "parameters": [
        {
          "defaultValue": null,
          "description": "Security token for API access.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Search keywords (e.g., 'deepseek').",
          "enumValues": [],
          "location": "query",
          "name": "keyword",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": 0,
          "description": "Pagination offset, starting from 0 and stepping by 20.",
          "enumValues": [],
          "location": "query",
          "name": "offset",
          "required": false,
          "schemaType": "integer"
        },
        {
          "defaultValue": "RELEVANCE",
          "description": "Sorting criteria for search results.\n\nAvailable Values:\n- `RELEVANCE`: Relevance (Default)\n- `MOST_LIKED`: Most Liked",
          "enumValues": [
            "RELEVANCE",
            "MOST_LIKED"
          ],
          "location": "query",
          "name": "sortType",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": "ALL",
          "description": "Filter posts by publishing time.\n\nAvailable Values:\n- `ALL`: All Time\n- `ONE_DAY`: Last 24 Hours\n- `ONE_WEEK`: Last 7 Days\n- `ONE_MONTH`: Last 30 Days\n- `THREE_MONTHS`: Last 90 Days\n- `HALF_YEAR`: Last 180 Days",
          "enumValues": [
            "ALL",
            "ONE_DAY",
            "ONE_WEEK",
            "ONE_MONTH",
            "THREE_MONTHS",
            "HALF_YEAR"
          ],
          "location": "query",
          "name": "publishTime",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": "US",
          "description": "ISO 3166-1 alpha-2 country code (e.g., 'US', 'GB').",
          "enumValues": [],
          "location": "query",
          "name": "region",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/tiktok/search-post/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Post Search",
      "tags": [
        "TikTok"
      ]
    },
    {
      "description": "Get TikTok user Search data, including basic profile information such as user ID, nickname, and unique handle, for discovering influencers in specific niches via keywords and identifying target audiences and conducting competitor research.",
      "method": "GET",
      "operationId": "searchUserV1",
      "parameters": [
        {
          "defaultValue": null,
          "description": "Security token for API access.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Search keywords (e.g., 'deepseek').",
          "enumValues": [],
          "location": "query",
          "name": "keyword",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": "0",
          "description": "Pagination cursor. Start with '0'.",
          "enumValues": [],
          "location": "query",
          "name": "cursor",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": "",
          "description": "The 'logid' returned from the previous request for consistent search results.",
          "enumValues": [],
          "location": "query",
          "name": "searchId",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/tiktok/search-user/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "User Search",
      "tags": [
        "TikTok"
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
