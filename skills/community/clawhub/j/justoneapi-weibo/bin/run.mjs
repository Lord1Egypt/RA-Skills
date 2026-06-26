#!/usr/bin/env node
const manifest = {
  "baseUrl": "https://api.justoneapi.com",
  "description": "Track Weibo hot search boards, keyword results, creator profiles, fan or follower graphs, and post or video detail endpoints through JustOneAPI.",
  "displayName": "Weibo",
  "openapi": "3.1.0",
  "platformKey": "weibo",
  "primaryTag": "Weibo",
  "skillName": "justoneapi_weibo",
  "slug": "justoneapi-weibo",
  "sourceTitle": "OpenAPI definition",
  "operations": [
    {
      "description": "Get Weibo user Fans data, including profile metadata and verification signals, for audience analysis and influencer research.",
      "method": "GET",
      "operationId": "getFansV1",
      "parameters": [
        {
          "defaultValue": null,
          "description": "API access token.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Weibo User ID (UID).",
          "enumValues": [],
          "location": "query",
          "name": "uid",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": 1,
          "description": "Page number, starting with 1.",
          "enumValues": [],
          "location": "query",
          "name": "page",
          "required": false,
          "schemaType": "integer"
        }
      ],
      "path": "/api/weibo/get-fans/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "User Fans",
      "tags": [
        "Weibo"
      ]
    },
    {
      "description": "Get Weibo user Followers data, including profile metadata and verification signals, for network analysis and creator research.",
      "method": "GET",
      "operationId": "getFollowersV1",
      "parameters": [
        {
          "defaultValue": null,
          "description": "API access token.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Weibo User ID (UID).",
          "enumValues": [],
          "location": "query",
          "name": "uid",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": 1,
          "description": "Page number, starting with 1.",
          "enumValues": [],
          "location": "query",
          "name": "page",
          "required": false,
          "schemaType": "integer"
        }
      ],
      "path": "/api/weibo/get-followers/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "User Followers",
      "tags": [
        "Weibo"
      ]
    },
    {
      "description": "Get Weibo post Comments data, including text, authors, and timestamps, for feedback analysis.",
      "method": "GET",
      "operationId": "getWeiboPostCommentsV1",
      "parameters": [
        {
          "defaultValue": null,
          "description": "API access token.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Weibo post mid.",
          "enumValues": [],
          "location": "query",
          "name": "mid",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": "TIME",
          "description": "Sort order for the result set.\n\nAvailable Values:\n- `TIME`: Time\n- `HOT`: Hot",
          "enumValues": [
            "TIME",
            "HOT"
          ],
          "location": "query",
          "name": "sort",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Pagination cursor returned by the previous response.",
          "enumValues": [],
          "location": "query",
          "name": "maxId",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/weibo/get-post-comments/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Post Comments",
      "tags": [
        "Weibo"
      ]
    },
    {
      "description": "Get Weibo user Profile data, including follower counts, verification status, and bio details, for creator research and account analysis.",
      "method": "GET",
      "operationId": "getUserProfileV3",
      "parameters": [
        {
          "defaultValue": null,
          "description": "API access token.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Weibo User ID (UID).",
          "enumValues": [],
          "location": "query",
          "name": "uid",
          "required": true,
          "schemaType": "string"
        }
      ],
      "path": "/api/weibo/get-user-detail/v3",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "User Profile",
      "tags": [
        "Weibo"
      ]
    },
    {
      "description": "Get Weibo user Published Posts data, including text, media, and publish times, for account monitoring.",
      "method": "GET",
      "operationId": "getUserPublishedPostsV1",
      "parameters": [
        {
          "defaultValue": null,
          "description": "API access token.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Weibo User ID (UID).",
          "enumValues": [],
          "location": "query",
          "name": "uid",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": 1,
          "description": "Page number, starting with 1.",
          "enumValues": [],
          "location": "query",
          "name": "page",
          "required": false,
          "schemaType": "integer"
        },
        {
          "defaultValue": null,
          "description": "Pagination cursor (since_id). Required if page > 1.",
          "enumValues": [],
          "location": "query",
          "name": "sinceId",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/weibo/get-user-post/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "User Published Posts",
      "tags": [
        "Weibo"
      ]
    },
    {
      "description": "Get Weibo user Video list data (waterfall), including pagination cursor for next page.",
      "method": "GET",
      "operationId": "getWeiboUserVideoListV1",
      "parameters": [
        {
          "defaultValue": null,
          "description": "API access token.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Weibo User ID (UID).",
          "enumValues": [],
          "location": "query",
          "name": "uid",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Pagination cursor returned by the previous response.",
          "enumValues": [],
          "location": "query",
          "name": "cursor",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/weibo/get-user-video-list/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "User Video List",
      "tags": [
        "Weibo"
      ]
    },
    {
      "description": "Get Weibo post Details data, including media, author metadata, and engagement counts, for post analysis, archiving, and campaign monitoring.",
      "method": "GET",
      "operationId": "getWeiboDetailsV1",
      "parameters": [
        {
          "defaultValue": null,
          "description": "API access token.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Weibo post ID.",
          "enumValues": [],
          "location": "query",
          "name": "id",
          "required": true,
          "schemaType": "string"
        }
      ],
      "path": "/api/weibo/get-weibo-detail/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Post Details",
      "tags": [
        "Weibo"
      ]
    },
    {
      "description": "Get Weibo hot Search data, including ranking data, for trend monitoring, newsroom workflows, and topic discovery.",
      "method": "GET",
      "operationId": "hotSearchV1",
      "parameters": [
        {
          "defaultValue": null,
          "description": "API access token.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        }
      ],
      "path": "/api/weibo/hot-search/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Hot Search",
      "tags": [
        "Weibo"
      ]
    },
    {
      "description": "Get Weibo keyword Search data, including authors, publish times, and engagement signals, for trend monitoring.",
      "method": "GET",
      "operationId": "searchAllV2",
      "parameters": [
        {
          "defaultValue": null,
          "description": "API access token.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Search Keywords.",
          "enumValues": [],
          "location": "query",
          "name": "q",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Start Day (yyyy-MM-dd).",
          "enumValues": [],
          "location": "query",
          "name": "startDay",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Start Hour (0-23).",
          "enumValues": [],
          "location": "query",
          "name": "startHour",
          "required": true,
          "schemaType": "integer"
        },
        {
          "defaultValue": null,
          "description": "End Day (yyyy-MM-dd).",
          "enumValues": [],
          "location": "query",
          "name": "endDay",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "End Hour (0-23).",
          "enumValues": [],
          "location": "query",
          "name": "endHour",
          "required": true,
          "schemaType": "integer"
        },
        {
          "defaultValue": false,
          "description": "Hot sort, true for hot sort, false for time sort. Default is false.",
          "enumValues": [],
          "location": "query",
          "name": "hotSort",
          "required": false,
          "schemaType": "boolean"
        },
        {
          "defaultValue": "ALL",
          "description": "Contains filter for the result set.\n\nAvailable Values:\n- `ALL`: All\n- `PICTURE`: Has Picture\n- `VIDEO`: Has Video\n- `MUSIC`: Has Music\n- `LINK`: Has Link",
          "enumValues": [
            "ALL",
            "PICTURE",
            "VIDEO",
            "MUSIC",
            "LINK"
          ],
          "location": "query",
          "name": "contains",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": 1,
          "description": "Page number, starting with 1.",
          "enumValues": [],
          "location": "query",
          "name": "page",
          "required": false,
          "schemaType": "integer"
        }
      ],
      "path": "/api/weibo/search-all/v2",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Keyword Search",
      "tags": [
        "Weibo"
      ]
    },
    {
      "description": "Get Weibo search User Published Posts data, including matched results, metadata, and ranking signals, for author research and historical content discovery.",
      "method": "GET",
      "operationId": "searchProfileV1",
      "parameters": [
        {
          "defaultValue": null,
          "description": "API access token.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Weibo User ID (UID).",
          "enumValues": [],
          "location": "query",
          "name": "uid",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Search Keywords.",
          "enumValues": [],
          "location": "query",
          "name": "q",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Start Day (yyyy-MM-dd).",
          "enumValues": [],
          "location": "query",
          "name": "startDay",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "End Day (yyyy-MM-dd).",
          "enumValues": [],
          "location": "query",
          "name": "endDay",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": 1,
          "description": "Page number, starting with 1.",
          "enumValues": [],
          "location": "query",
          "name": "page",
          "required": false,
          "schemaType": "integer"
        }
      ],
      "path": "/api/weibo/search-profile/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Search User Published Posts",
      "tags": [
        "Weibo"
      ]
    },
    {
      "description": "Get Weibo tV Video Details data, including media URLs, author details, and engagement counts, for video research, archiving, and performance analysis.",
      "method": "GET",
      "operationId": "tvComponentV1",
      "parameters": [
        {
          "defaultValue": null,
          "description": "API access token.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Weibo video/object ID.",
          "enumValues": [],
          "location": "query",
          "name": "oid",
          "required": true,
          "schemaType": "string"
        }
      ],
      "path": "/api/weibo/tv-component/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "TV Video Details",
      "tags": [
        "Weibo"
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
