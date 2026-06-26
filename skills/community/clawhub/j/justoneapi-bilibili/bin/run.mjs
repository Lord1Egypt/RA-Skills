#!/usr/bin/env node
const manifest = {
  "baseUrl": "https://api.justoneapi.com",
  "description": "Analyze Bilibili workflows with JustOneAPI, including video Details, user Published Videos, and user Profile across 9 operations.",
  "displayName": "Bilibili",
  "openapi": "3.1.0",
  "platformKey": "bilibili",
  "primaryTag": "Bilibili",
  "skillName": "justoneapi_bilibili",
  "slug": "justoneapi-bilibili",
  "sourceTitle": "OpenAPI definition",
  "operations": [
    {
      "description": "Get Bilibili user Profile data, including account metadata, audience metrics, and verification-related fields, for analyzing creator's profile, level, and verification status and verifying user identity and social presence on bilibili.",
      "method": "GET",
      "operationId": "getUserDetailV2",
      "parameters": [
        {
          "defaultValue": null,
          "description": "Access token for the API.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Bilibili User ID (UID).",
          "enumValues": [],
          "location": "query",
          "name": "uid",
          "required": true,
          "schemaType": "string"
        }
      ],
      "path": "/api/bilibili/get-user-detail/v2",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "User Profile",
      "tags": [
        "Bilibili"
      ]
    },
    {
      "description": "Get Bilibili user Relation Stats data, including following counts, for creator benchmarking and audience growth tracking.",
      "method": "GET",
      "operationId": "getUserRelationStat",
      "parameters": [
        {
          "defaultValue": null,
          "description": "Access token for the API.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Bilibili User ID (WMID).",
          "enumValues": [],
          "location": "query",
          "name": "wmid",
          "required": true,
          "schemaType": "string"
        }
      ],
      "path": "/api/bilibili/get-user-relation-stat/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "User Relation Stats",
      "tags": [
        "Bilibili"
      ]
    },
    {
      "description": "Get Bilibili user Published Videos data, including titles, covers, and publish times, for creator monitoring and content performance analysis.",
      "method": "GET",
      "operationId": "getBilibiliUserVideoListV2",
      "parameters": [
        {
          "defaultValue": null,
          "description": "Access token for the API.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Bilibili User ID (UID).",
          "enumValues": [],
          "location": "query",
          "name": "uid",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Pagination parameter from previous response.",
          "enumValues": [],
          "location": "query",
          "name": "param",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/bilibili/get-user-video-list/v2",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "User Published Videos",
      "tags": [
        "Bilibili"
      ]
    },
    {
      "description": "Get Bilibili video Captions data, including caption data, for transcript extraction and multilingual content analysis.",
      "method": "GET",
      "operationId": "getVideoCaptionV1",
      "parameters": [
        {
          "defaultValue": null,
          "description": "Access token for the API.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Bilibili Video ID (BVID).",
          "enumValues": [],
          "location": "query",
          "name": "bvid",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Bilibili AID.",
          "enumValues": [],
          "location": "query",
          "name": "aid",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Bilibili CID.",
          "enumValues": [],
          "location": "query",
          "name": "cid",
          "required": true,
          "schemaType": "string"
        }
      ],
      "path": "/api/bilibili/get-video-caption/v2",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Video Captions",
      "tags": [
        "Bilibili"
      ]
    },
    {
      "description": "Get Bilibili video Comments data, including commenter profiles, text, and likes, for sentiment analysis and comment moderation workflows.",
      "method": "GET",
      "operationId": "getVideoCommentV2",
      "parameters": [
        {
          "defaultValue": null,
          "description": "Access token for the API.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Bilibili Archive ID (AID).",
          "enumValues": [],
          "location": "query",
          "name": "aid",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Pagination cursor.",
          "enumValues": [],
          "location": "query",
          "name": "cursor",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/bilibili/get-video-comment/v2",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Video Comments",
      "tags": [
        "Bilibili"
      ]
    },
    {
      "description": "Get Bilibili video Danmaku data, including timeline positions and comment text, for audience reaction analysis and subtitle-style comment review.",
      "method": "GET",
      "operationId": "getVideoDanmuV2",
      "parameters": [
        {
          "defaultValue": null,
          "description": "Access token for the API.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Bilibili Archive ID (AID).",
          "enumValues": [],
          "location": "query",
          "name": "aid",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Bilibili Chat ID (CID).",
          "enumValues": [],
          "location": "query",
          "name": "cid",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Page number for pagination.",
          "enumValues": [],
          "location": "query",
          "name": "page",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/bilibili/get-video-danmu/v2",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Video Danmaku",
      "tags": [
        "Bilibili"
      ]
    },
    {
      "description": "Get Bilibili video Details data, including metadata (title, tags, and publishing time), for tracking video performance and engagement metrics and analyzing content metadata and uploader information.",
      "method": "GET",
      "operationId": "getBilibiliVideoDetailV2",
      "parameters": [
        {
          "defaultValue": null,
          "description": "Access token for the API.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Bilibili Video ID (BVID).",
          "enumValues": [],
          "location": "query",
          "name": "bvid",
          "required": true,
          "schemaType": "string"
        }
      ],
      "path": "/api/bilibili/get-video-detail/v2",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Video Details",
      "tags": [
        "Bilibili"
      ]
    },
    {
      "description": "Get Bilibili video Search data, including matched videos, creators, and engagement metrics, for topic research and content discovery.",
      "method": "GET",
      "operationId": "searchBilibiliVideoV2",
      "parameters": [
        {
          "defaultValue": null,
          "description": "Access token for the API.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Search keyword.",
          "enumValues": [],
          "location": "query",
          "name": "keyword",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Page number for pagination.",
          "enumValues": [],
          "location": "query",
          "name": "page",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": "general",
          "description": "Sorting criteria for search results.\n\nAvailable Values:\n- `general`: General\n- `click`: Most Played\n- `pubdate`: Latest\n- `dm`: Most Danmaku\n- `stow`: Most Favorite",
          "enumValues": [
            "general",
            "click",
            "pubdate",
            "dm",
            "stow"
          ],
          "location": "query",
          "name": "order",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/bilibili/search-video/v2",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Video Search",
      "tags": [
        "Bilibili"
      ]
    },
    {
      "description": "Get Bilibili share Link Resolution data, including resolved video and page identifier, for converting shortened mobile share links to standard bvid/metadata and automating content extraction from shared social media links.",
      "method": "GET",
      "operationId": "shareBilibiliUrlTransferV1",
      "parameters": [
        {
          "defaultValue": null,
          "description": "Access token for the API.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Bilibili share URL (must start with https://b23.tv/).",
          "enumValues": [],
          "location": "query",
          "name": "shareUrl",
          "required": true,
          "schemaType": "string"
        }
      ],
      "path": "/api/bilibili/share-url-transfer/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Share Link Resolution",
      "tags": [
        "Bilibili"
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
