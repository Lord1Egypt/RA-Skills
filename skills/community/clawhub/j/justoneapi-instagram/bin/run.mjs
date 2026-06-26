#!/usr/bin/env node
const manifest = {
  "baseUrl": "https://api.justoneapi.com",
  "description": "Analyze Instagram workflows with JustOneAPI, including user Profile, post Details, and user Published Posts across 5 operations.",
  "displayName": "Instagram",
  "openapi": "3.1.0",
  "platformKey": "instagram",
  "primaryTag": "Instagram",
  "skillName": "justoneapi_instagram",
  "slug": "justoneapi-instagram",
  "sourceTitle": "OpenAPI definition",
  "operations": [
    {
      "description": "Get Instagram post Details data, including post caption, media content (images/videos), and publish time, for analyzing engagement metrics (likes/comments) for a specific post and archiving post content and media assets for content analysis.",
      "method": "GET",
      "operationId": "getInstagramPostDetailV1",
      "parameters": [
        {
          "defaultValue": null,
          "description": "Access token for the API service.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "The unique shortcode (slug) for the Instagram post (e.g., 'DRhvwVLAHAG').",
          "enumValues": [],
          "location": "query",
          "name": "code",
          "required": true,
          "schemaType": "string"
        }
      ],
      "path": "/api/instagram/get-post-detail/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Post Details",
      "tags": [
        "Instagram"
      ]
    },
    {
      "description": "Get Instagram user Profile data, including follower count, following count, and post count, for obtaining basic account metadata for influencer vetting, tracking follower growth and audience reach over time, and mapping user handles to specific profile stats.",
      "method": "GET",
      "operationId": "getInstagramUserDetailV1",
      "parameters": [
        {
          "defaultValue": null,
          "description": "Access token for the API service.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "The Instagram username whose profile details are to be retrieved.",
          "enumValues": [],
          "location": "query",
          "name": "username",
          "required": true,
          "schemaType": "string"
        }
      ],
      "path": "/api/instagram/get-user-detail/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "User Profile",
      "tags": [
        "Instagram"
      ]
    },
    {
      "description": "Get Instagram user Published Posts data, including post code, caption, and media type, for monitoring recent publishing activity of a specific user and building a historical record of content for auditing or analysis.",
      "method": "GET",
      "operationId": "getInstagramUserPostsV1",
      "parameters": [
        {
          "defaultValue": null,
          "description": "Access token for the API service.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "The Instagram username whose published posts are to be retrieved.",
          "enumValues": [],
          "location": "query",
          "name": "username",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": "",
          "description": "Token used for retrieving the next page of results.",
          "enumValues": [],
          "location": "query",
          "name": "paginationToken",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/instagram/get-user-posts/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "User Published Posts",
      "tags": [
        "Instagram"
      ]
    },
    {
      "description": "Get Instagram hashtag Posts Search data, including caption, author profile, and publish time, for competitive analysis of trending topics and hashtags and monitoring community discussions and public opinion on specific tags.",
      "method": "GET",
      "operationId": "searchHashtagPostsV1",
      "parameters": [
        {
          "defaultValue": null,
          "description": "Access token for the API service.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "The hashtag or keyword to search for.",
          "enumValues": [],
          "location": "query",
          "name": "hashtag",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": "",
          "description": "Cursor used for retrieving the next page of results.",
          "enumValues": [],
          "location": "query",
          "name": "endCursor",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/instagram/search-hashtag-posts/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Hashtag Posts Search",
      "tags": [
        "Instagram"
      ]
    },
    {
      "description": "Get Instagram reels Search data, including post ID, caption, and author profile, for tracking trends and viral content via specific keywords or hashtags and discovering high-engagement reels within a particular niche.",
      "method": "GET",
      "operationId": "searchReelsV1",
      "parameters": [
        {
          "defaultValue": null,
          "description": "Access token for the API service.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "The search keyword or hashtag to filter Reels.",
          "enumValues": [],
          "location": "query",
          "name": "keyword",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": "",
          "description": "Token used for retrieving the next page of results.",
          "enumValues": [],
          "location": "query",
          "name": "paginationToken",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/instagram/search-reels/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Reels Search",
      "tags": [
        "Instagram"
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
