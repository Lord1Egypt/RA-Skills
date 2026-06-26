#!/usr/bin/env node
const manifest = {
  "baseUrl": "https://api.justoneapi.com",
  "description": "Search Xiaohongshu notes, inspect creator profiles, resolve share links, and drill into note comments, replies, and note detail endpoints through JustOneAPI.",
  "displayName": "Xiaohongshu (RedNote)",
  "openapi": "3.1.0",
  "platformKey": "xiaohongshu",
  "primaryTag": "Xiaohongshu (RedNote)",
  "skillName": "justoneapi_xiaohongshu",
  "slug": "justoneapi-xiaohongshu",
  "sourceTitle": "OpenAPI definition",
  "operations": [
    {
      "description": "Get Xiaohongshu (RedNote) note Comments data, including text, authors, and timestamps, for feedback analysis.",
      "method": "GET",
      "operationId": "getNoteCommentV2",
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
          "description": "Unique note identifier on Xiaohongshu.",
          "enumValues": [],
          "location": "query",
          "name": "noteId",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Pagination cursor from the previous page (use the cursor value returned by the last response).",
          "enumValues": [],
          "location": "query",
          "name": "lastCursor",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": "latest",
          "description": "Sort order for the result set.\n\nAvailable Values:\n- `normal`: Normal\n- `latest`: Latest",
          "enumValues": [
            "normal",
            "latest"
          ],
          "location": "query",
          "name": "sort",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/xiaohongshu/get-note-comment/v2",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Note Comments",
      "tags": [
        "Xiaohongshu (RedNote)"
      ]
    },
    {
      "description": "Get Xiaohongshu (RedNote) note Comments data, including comment text, author profiles, and interaction data, for sentiment analysis and community monitoring.",
      "method": "GET",
      "operationId": "getNoteCommentV4",
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
          "description": "Unique note identifier on Xiaohongshu.",
          "enumValues": [],
          "location": "query",
          "name": "noteId",
          "required": true,
          "schemaType": "string"
        }
      ],
      "path": "/api/xiaohongshu/get-note-comment/v4",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Note Comments",
      "tags": [
        "Xiaohongshu (RedNote)"
      ]
    },
    {
      "description": "Get Xiaohongshu (RedNote) note Details data, including media and engagement metrics, for content analysis, archiving, and campaign research.",
      "method": "GET",
      "operationId": "getXiaohongshuNoteDetailV1",
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
          "description": "Unique note identifier on Xiaohongshu.",
          "enumValues": [],
          "location": "query",
          "name": "noteId",
          "required": true,
          "schemaType": "string"
        }
      ],
      "path": "/api/xiaohongshu/get-note-detail/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Note Details",
      "tags": [
        "Xiaohongshu (RedNote)"
      ]
    },
    {
      "description": "Get Xiaohongshu (RedNote) note Details data, including media and engagement metrics, for content analysis, archiving, and campaign research.",
      "method": "GET",
      "operationId": "getNoteDetailV3",
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
          "description": "Unique note identifier on Xiaohongshu.",
          "enumValues": [],
          "location": "query",
          "name": "noteId",
          "required": true,
          "schemaType": "string"
        }
      ],
      "path": "/api/xiaohongshu/get-note-detail/v3",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Note Details",
      "tags": [
        "Xiaohongshu (RedNote)"
      ]
    },
    {
      "description": "Get Xiaohongshu (RedNote) note Details data, including media and engagement metrics, for content analysis, archiving, and campaign research.",
      "method": "GET",
      "operationId": "getNoteDetailV7",
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
          "description": "Unique note identifier on Xiaohongshu.",
          "enumValues": [],
          "location": "query",
          "name": "noteId",
          "required": true,
          "schemaType": "string"
        }
      ],
      "path": "/api/xiaohongshu/get-note-detail/v7",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Note Details",
      "tags": [
        "Xiaohongshu (RedNote)"
      ]
    },
    {
      "description": "Get Xiaohongshu (RedNote) comment Replies data, including text, authors, and timestamps, for thread analysis and feedback research.",
      "method": "GET",
      "operationId": "getNoteSubCommentV2",
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
          "description": "Unique note identifier on Xiaohongshu.",
          "enumValues": [],
          "location": "query",
          "name": "noteId",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Unique comment identifier on Xiaohongshu.",
          "enumValues": [],
          "location": "query",
          "name": "commentId",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Pagination cursor from the previous page (use the cursor value returned by the last response).",
          "enumValues": [],
          "location": "query",
          "name": "lastCursor",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/xiaohongshu/get-note-sub-comment/v2",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Comment Replies",
      "tags": [
        "Xiaohongshu (RedNote)"
      ]
    },
    {
      "description": "Get Xiaohongshu (RedNote) user Published Notes data, including note metadata, covers, and publish times, for account monitoring.",
      "method": "GET",
      "operationId": "getUserNoteListV2",
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
          "description": "Unique user identifier on Xiaohongshu.",
          "enumValues": [],
          "location": "query",
          "name": "userId",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Pagination cursor from the previous page (the last note's cursor value).",
          "enumValues": [],
          "location": "query",
          "name": "lastCursor",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/xiaohongshu/get-user-note-list/v2",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "User Published Notes",
      "tags": [
        "Xiaohongshu (RedNote)"
      ]
    },
    {
      "description": "Get Xiaohongshu (RedNote) user Published Notes data, including note metadata, covers, and publish times, for account monitoring.",
      "method": "GET",
      "operationId": "getUserNoteListV4",
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
          "description": "Unique user identifier on Xiaohongshu.",
          "enumValues": [],
          "location": "query",
          "name": "userId",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Pagination cursor from the previous page (the last note's cursor value).",
          "enumValues": [],
          "location": "query",
          "name": "lastCursor",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/xiaohongshu/get-user-note-list/v4",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "User Published Notes",
      "tags": [
        "Xiaohongshu (RedNote)"
      ]
    },
    {
      "description": "Get Xiaohongshu (RedNote) user Profile data, including follower counts and bio details, for creator research, account analysis, and competitor monitoring.",
      "method": "GET",
      "operationId": "getUserV3",
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
          "description": "Unique user identifier on Xiaohongshu.",
          "enumValues": [],
          "location": "query",
          "name": "userId",
          "required": true,
          "schemaType": "string"
        }
      ],
      "path": "/api/xiaohongshu/get-user/v3",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "User Profile",
      "tags": [
        "Xiaohongshu (RedNote)"
      ]
    },
    {
      "description": "Get Xiaohongshu (RedNote) user Profile data, including follower counts and bio details, for creator research, account analysis, and competitor monitoring.",
      "method": "GET",
      "operationId": "getUserV4",
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
          "description": "Unique user identifier on Xiaohongshu.",
          "enumValues": [],
          "location": "query",
          "name": "userId",
          "required": true,
          "schemaType": "string"
        }
      ],
      "path": "/api/xiaohongshu/get-user/v4",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "User Profile",
      "tags": [
        "Xiaohongshu (RedNote)"
      ]
    },
    {
      "description": "Get Xiaohongshu (RedNote) note Search data, including snippets, authors, and media, for topic discovery.",
      "method": "GET",
      "operationId": "getSearchNoteV2",
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
          "description": "Search keyword.",
          "enumValues": [],
          "location": "query",
          "name": "keyword",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": 1,
          "description": "Page number for pagination.",
          "enumValues": [],
          "location": "query",
          "name": "page",
          "required": false,
          "schemaType": "integer"
        },
        {
          "defaultValue": "general",
          "description": "Sort order for the result set.\n\nAvailable Values:\n- `general`: General\n- `popularity_descending`: Popularity Descending\n- `time_descending`: Time Descending\n- `comment_descending`: Comment Descending\n- `collect_descending`: Collect Descending",
          "enumValues": [
            "general",
            "popularity_descending",
            "time_descending",
            "comment_descending",
            "collect_descending"
          ],
          "location": "query",
          "name": "sort",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": "_0",
          "description": "Note type filter.\n\nAvailable Values:\n- `_0`: General\n- `_1`: Video\n- `_2`: Normal",
          "enumValues": [
            "_0",
            "_1",
            "_2"
          ],
          "location": "query",
          "name": "noteType",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Note publish time filter. This parameter is for reference only and does not have much effect.\n\nAvailable Values:\n- `一天内`: Within one day\n- `一周内`: Within a week\n- `半年内`: Within half a year",
          "enumValues": [
            "一天内",
            "一周内",
            "半年内"
          ],
          "location": "query",
          "name": "noteTime",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/xiaohongshu/search-note/v2",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Note Search",
      "tags": [
        "Xiaohongshu (RedNote)"
      ]
    },
    {
      "description": "Get Xiaohongshu (RedNote) note Search data, including snippets, authors, and media, for topic discovery.",
      "method": "GET",
      "operationId": "getSearchNoteV3",
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
          "description": "Search keyword.",
          "enumValues": [],
          "location": "query",
          "name": "keyword",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": 1,
          "description": "Page number for pagination.",
          "enumValues": [],
          "location": "query",
          "name": "page",
          "required": false,
          "schemaType": "integer"
        },
        {
          "defaultValue": "general",
          "description": "Sort order for the result set.\n\nAvailable Values:\n- `general`: General\n- `popularity_descending`: Hot\n- `time_descending`: New",
          "enumValues": [
            "general",
            "popularity_descending",
            "time_descending"
          ],
          "location": "query",
          "name": "sort",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": "_0",
          "description": "Note type filter.\n\nAvailable Values:\n- `_0`: General\n- `_1`: Video\n- `_2`: Normal",
          "enumValues": [
            "_0",
            "_1",
            "_2"
          ],
          "location": "query",
          "name": "noteType",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/xiaohongshu/search-note/v3",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Note Search",
      "tags": [
        "Xiaohongshu (RedNote)"
      ]
    },
    {
      "description": "Get Xiaohongshu (RedNote) keyword Suggestions data, including suggested queries, keyword variants, and query metadata, for expanding keyword sets for content research and seo/pseo workflows and improving search coverage by using platform-recommended terms.",
      "method": "GET",
      "operationId": "searchRecommendV1",
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
          "description": "Search keyword.",
          "enumValues": [],
          "location": "query",
          "name": "keyword",
          "required": true,
          "schemaType": "string"
        }
      ],
      "path": "/api/xiaohongshu/search-recommend/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Keyword Suggestions",
      "tags": [
        "Xiaohongshu (RedNote)"
      ]
    },
    {
      "description": "Get Xiaohongshu (RedNote) user Search data, including profile metadata and public signals, for creator discovery and account research.",
      "method": "GET",
      "operationId": "getSearchUserV2",
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
          "description": "Search keyword.",
          "enumValues": [],
          "location": "query",
          "name": "keyword",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": 1,
          "description": "Page number for pagination.",
          "enumValues": [],
          "location": "query",
          "name": "page",
          "required": false,
          "schemaType": "integer"
        }
      ],
      "path": "/api/xiaohongshu/search-user/v2",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "User Search",
      "tags": [
        "Xiaohongshu (RedNote)"
      ]
    },
    {
      "description": "Get Xiaohongshu (RedNote) share Link Resolution data, including helping extract note IDs, for downstream note and comment workflows.",
      "method": "GET",
      "operationId": "shareXiaohongshuUrlTransferV1",
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
          "description": "RedNote share link URL to be resolved (short link or shared URL).",
          "enumValues": [],
          "location": "query",
          "name": "shareUrl",
          "required": true,
          "schemaType": "string"
        }
      ],
      "path": "/api/xiaohongshu/share-url-transfer/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Share Link Resolution",
      "tags": [
        "Xiaohongshu (RedNote)"
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
