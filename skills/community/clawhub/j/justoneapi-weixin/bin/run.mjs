#!/usr/bin/env node
const manifest = {
  "baseUrl": "https://api.justoneapi.com",
  "description": "Analyze WeChat Official Accounts workflows with JustOneAPI, including user Published Posts, article Engagement Metrics, and article Comments across 5 operations.",
  "displayName": "WeChat Official Accounts",
  "openapi": "3.1.0",
  "platformKey": "weixin",
  "primaryTag": "WeChat Official Accounts",
  "skillName": "justoneapi_weixin",
  "slug": "justoneapi-weixin",
  "sourceTitle": "OpenAPI definition",
  "operations": [
    {
      "description": "Get WeChat Official Accounts article Comments data, including commenter details, comment text, and timestamps, for feedback analysis.",
      "method": "GET",
      "operationId": "getArticleComment",
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
          "description": "The URL of the Weixin article.",
          "enumValues": [],
          "location": "query",
          "name": "articleUrl",
          "required": true,
          "schemaType": "string"
        }
      ],
      "path": "/api/weixin/get-article-comment/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Article Comments",
      "tags": [
        "WeChat Official Accounts"
      ]
    },
    {
      "description": "Get WeChat Official Accounts article Details data, including body content, for article archiving, research, and content analysis.",
      "method": "GET",
      "operationId": "getWeixinArticleDetailV1",
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
          "description": "The URL of the Weixin article.",
          "enumValues": [],
          "location": "query",
          "name": "articleUrl",
          "required": true,
          "schemaType": "string"
        }
      ],
      "path": "/api/weixin/get-article-detail/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Article Details",
      "tags": [
        "WeChat Official Accounts"
      ]
    },
    {
      "description": "Get WeChat Official Accounts article Engagement Metrics data, including like, share, and comment metrics, for article performance tracking and benchmarking.",
      "method": "GET",
      "operationId": "getArticleFeedback",
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
          "description": "The URL of the Weixin article.",
          "enumValues": [],
          "location": "query",
          "name": "articleUrl",
          "required": true,
          "schemaType": "string"
        }
      ],
      "path": "/api/weixin/get-article-feedback/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Article Engagement Metrics",
      "tags": [
        "WeChat Official Accounts"
      ]
    },
    {
      "description": "Get WeChat Official Accounts user Published Posts data, including titles, publish times, and summaries, for account monitoring.",
      "method": "GET",
      "operationId": "getUserPost",
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
          "description": "The ID of the Weixin Official Account (e.g., 'rmrbwx').",
          "enumValues": [],
          "location": "query",
          "name": "wxid",
          "required": true,
          "schemaType": "string"
        }
      ],
      "path": "/api/weixin/get-user-post/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "User Published Posts",
      "tags": [
        "WeChat Official Accounts"
      ]
    },
    {
      "description": "Get WeChat Official Accounts keyword Search data, including account names, titles, and publish times, for content discovery.",
      "method": "GET",
      "operationId": "searchWeixinV1",
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
          "description": "The search keyword.",
          "enumValues": [],
          "location": "query",
          "name": "keyword",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": 0,
          "description": "Pagination offset (starts with 0, increment by 20).",
          "enumValues": [],
          "location": "query",
          "name": "offset",
          "required": false,
          "schemaType": "integer"
        },
        {
          "defaultValue": "_0",
          "description": "Type of search results (accounts, articles, etc.).\n\nAvailable Values:\n- `_0`: All\n- `_1`: WeChat Official Account\n- `_2`: Article\n- `_7`: WeChat Channel\n- `_262208`: Wechat Mini Program\n- `_384`: Emoji\n- `_16777728`: Encyclopedia\n- `_9`: Live\n- `_1024`: Book\n- `_512`: Music\n- `_16384`: News\n- `_8192`: Wechat Index\n- `_8`: Moments",
          "enumValues": [
            "_0",
            "_1",
            "_2",
            "_7",
            "_262208",
            "_384",
            "_16777728",
            "_9",
            "_1024",
            "_512",
            "_16384",
            "_8192",
            "_8"
          ],
          "location": "query",
          "name": "searchType",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": "_0",
          "description": "Sorting criteria for search results.\n\nAvailable Values:\n- `_0`: Default\n- `_2`: Latest\n- `_4`: Hot",
          "enumValues": [
            "_0",
            "_2",
            "_4"
          ],
          "location": "query",
          "name": "sortType",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/weixin/search/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Keyword Search",
      "tags": [
        "WeChat Official Accounts"
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
