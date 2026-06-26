#!/usr/bin/env node
const manifest = {
  "baseUrl": "https://api.justoneapi.com",
  "description": "Analyze Taobao and Tmall workflows with JustOneAPI, including product Details, product Reviews, and shop Product List across 10 operations.",
  "displayName": "Taobao and Tmall",
  "openapi": "3.1.0",
  "platformKey": "taobao",
  "primaryTag": "Taobao and Tmall",
  "skillName": "justoneapi_taobao",
  "slug": "justoneapi-taobao",
  "sourceTitle": "OpenAPI definition",
  "operations": [
    {
      "description": "Get Taobao and Tmall product Reviews data, including ratings, timestamps, and reviewer signals, for feedback analysis and product research.",
      "method": "GET",
      "operationId": "getItemCommentV3",
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
          "description": "AUnique product identifier on Taobao/Tmall (item ID).",
          "enumValues": [],
          "location": "query",
          "name": "itemId",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": "feedbackdate",
          "description": "Sort order for the result set.\n\nAvailable Values:\n- `feedbackdate`: Sort by feedback date\n- `general`: General sorting",
          "enumValues": [
            "feedbackdate",
            "general"
          ],
          "location": "query",
          "name": "orderType",
          "required": false,
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
      "path": "/api/taobao/get-item-comment/v3",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Product Reviews",
      "tags": [
        "Taobao and Tmall"
      ]
    },
    {
      "description": "Get Taobao and Tmall product Details data, including pricing, images, and shop details, for product research, catalog monitoring, and ecommerce analysis.",
      "method": "GET",
      "operationId": "getTaobaoItemDetailV1",
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
          "description": "AUnique product identifier on Taobao/Tmall (item ID).",
          "enumValues": [],
          "location": "query",
          "name": "itemId",
          "required": true,
          "schemaType": "string"
        }
      ],
      "path": "/api/taobao/get-item-detail/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Product Details",
      "tags": [
        "Taobao and Tmall"
      ]
    },
    {
      "description": "Get Taobao and Tmall product Details data through the task-backed v2 flow. If data is not ready within a short wait, the response returns a pending task status.",
      "method": "GET",
      "operationId": "getItemDetailV2",
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
          "description": "AUnique product identifier on Taobao/Tmall (item ID).",
          "enumValues": [],
          "location": "query",
          "name": "itemId",
          "required": true,
          "schemaType": "string"
        }
      ],
      "path": "/api/taobao/get-item-detail/v2",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Product Details",
      "tags": [
        "Taobao and Tmall"
      ]
    },
    {
      "description": "Get Taobao and Tmall product Details data, including pricing, images, and shop details, for product research, catalog monitoring, and ecommerce analysis.",
      "method": "GET",
      "operationId": "getItemDetailV4",
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
          "description": "AUnique product identifier on Taobao/Tmall (item ID).",
          "enumValues": [],
          "location": "query",
          "name": "itemId",
          "required": true,
          "schemaType": "string"
        }
      ],
      "path": "/api/taobao/get-item-detail/v4",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Product Details",
      "tags": [
        "Taobao and Tmall"
      ]
    },
    {
      "description": "Get Taobao and Tmall product Details data, including pricing, images, and shop details, for product research, catalog monitoring, and ecommerce analysis.",
      "method": "GET",
      "operationId": "getItemDetailV5",
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
          "description": "AUnique product identifier on Taobao/Tmall (item ID).",
          "enumValues": [],
          "location": "query",
          "name": "itemId",
          "required": true,
          "schemaType": "string"
        }
      ],
      "path": "/api/taobao/get-item-detail/v5",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Product Details",
      "tags": [
        "Taobao and Tmall"
      ]
    },
    {
      "description": "Get Taobao and Tmall product Details data, including pricing, images, and shop details, for product research, catalog monitoring, and ecommerce analysis.",
      "method": "GET",
      "operationId": "getItemDetailV9",
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
          "description": "AUnique product identifier on Taobao/Tmall (item ID).",
          "enumValues": [],
          "location": "query",
          "name": "itemId",
          "required": true,
          "schemaType": "string"
        }
      ],
      "path": "/api/taobao/get-item-detail/v9",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Product Details",
      "tags": [
        "Taobao and Tmall"
      ]
    },
    {
      "description": "Get Taobao and Tmall shop Product List data, including item titles, prices, and images, for seller research and catalog tracking.",
      "method": "GET",
      "operationId": "getTaobaoShopItemListV1",
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
          "description": "Shop identifier. Also known as Seller ID or User ID (they refer to the same value).",
          "enumValues": [],
          "location": "query",
          "name": "userId",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": "_sale",
          "description": "Sort order for the result set.\n\nAvailable Values:\n- `_sale`: Sales\n- `_default`: Default",
          "enumValues": [
            "_sale",
            "_default"
          ],
          "location": "query",
          "name": "sort",
          "required": false,
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
      "path": "/api/taobao/get-shop-item-list/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Shop Product List",
      "tags": [
        "Taobao and Tmall"
      ]
    },
    {
      "description": "Get Taobao and Tmall shop Product List data, including item titles, prices, and images, for seller research and catalog tracking.",
      "method": "GET",
      "operationId": "getShopItemListV2",
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
          "description": "Shop identifier. Also known as Seller ID or User ID (they refer to the same value).",
          "enumValues": [],
          "location": "query",
          "name": "userId",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Unique shop identifier on Taobao/Tmall (shop ID).",
          "enumValues": [],
          "location": "query",
          "name": "shopId",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": "coefp",
          "description": "Sort order for the result set.\n\nAvailable Values:\n- `coefp`: Comprehensive sorting\n- `hotsell`: Hot selling / Sales volume\n- `oldstarts`: New arrivals / Old starts\n- `bid`: Price: Low to High\n- `_bid`: Price: High to Low",
          "enumValues": [
            "coefp",
            "hotsell",
            "oldstarts",
            "bid",
            "_bid"
          ],
          "location": "query",
          "name": "sort",
          "required": false,
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
      "path": "/api/taobao/get-shop-item-list/v2",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Shop Product List",
      "tags": [
        "Taobao and Tmall"
      ]
    },
    {
      "description": "Get Taobao and Tmall shop Product List data, including item titles, prices, and images, for seller research and catalog tracking.",
      "method": "GET",
      "operationId": "getShopItemListV3",
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
          "description": "Shop identifier. Also known as Seller ID or User ID (they refer to the same value).",
          "enumValues": [],
          "location": "query",
          "name": "userId",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Unique shop identifier on Taobao/Tmall (shop ID).",
          "enumValues": [],
          "location": "query",
          "name": "shopId",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": "coefp",
          "description": "Sort order for the result set.\n\nAvailable Values:\n- `coefp`: Comprehensive sorting\n- `hotsell`: Hot selling / Sales volume\n- `oldstarts`: New arrivals / Old starts\n- `bid`: Price: Low to High\n- `_bid`: Price: High to Low",
          "enumValues": [
            "coefp",
            "hotsell",
            "oldstarts",
            "bid",
            "_bid"
          ],
          "location": "query",
          "name": "sort",
          "required": false,
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
      "path": "/api/taobao/get-shop-item-list/v3",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Shop Product List",
      "tags": [
        "Taobao and Tmall"
      ]
    },
    {
      "description": "Get Taobao and Tmall product Search data, including titles, prices, and images, for product discovery.",
      "method": "GET",
      "operationId": "searchItemListV1",
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
          "defaultValue": "_sale",
          "description": "Sort order for the result set.\n\nAvailable Values:\n- `_sale`: Sales\n- `_bid`: Price: High to Low\n- `bid`: Price: Low to High\n- `_coefp`: General",
          "enumValues": [
            "_sale",
            "_bid",
            "bid",
            "_coefp"
          ],
          "location": "query",
          "name": "sort",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": false,
          "description": "Whether to filter results to Tmall only.",
          "enumValues": [],
          "location": "query",
          "name": "tmall",
          "required": false,
          "schemaType": "boolean"
        },
        {
          "defaultValue": null,
          "description": "Minimum price filter (inclusive).",
          "enumValues": [],
          "location": "query",
          "name": "startPrice",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Maximum price filter (inclusive).",
          "enumValues": [],
          "location": "query",
          "name": "endPrice",
          "required": false,
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
      "path": "/api/taobao/search-item-list/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Product Search",
      "tags": [
        "Taobao and Tmall"
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
