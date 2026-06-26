#!/usr/bin/env node
const manifest = {
  "baseUrl": "https://api.justoneapi.com",
  "description": "Analyze Amazon workflows with JustOneAPI, including product Details, product Top Reviews, and best Sellers across 4 operations.",
  "displayName": "Amazon",
  "openapi": "3.1.0",
  "platformKey": "amazon",
  "primaryTag": "Amazon",
  "skillName": "justoneapi_amazon",
  "slug": "justoneapi-amazon",
  "sourceTitle": "OpenAPI definition",
  "operations": [
    {
      "description": "Get Amazon best Sellers data, including rank positions, product metadata, and pricing, for identifying trending products in specific categories, market share analysis and category research, and tracking sales rank and popularity over time.",
      "method": "GET",
      "operationId": "getBestSellersV1",
      "parameters": [
        {
          "defaultValue": null,
          "description": "Authentication token for this API service.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Best sellers category to return products for (e.g. 'baby-products' or 'baby-products/166777011'). The value is derived from the URL path of the Amazon Best Sellers page, such as: https://www.amazon.com/Best-Sellers-Baby-Baby-Toddler-Feeding-Supplies/zgbs/baby-products/166777011",
          "enumValues": [],
          "location": "query",
          "name": "category",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": "US",
          "description": "Country code for the Amazon product.\n\nAvailable Values:\n- `US`: United States\n- `AU`: Australia\n- `BR`: Brazil\n- `CA`: Canada\n- `CN`: China\n- `FR`: France\n- `DE`: Germany\n- `IN`: India\n- `IT`: Italy\n- `MX`: Mexico\n- `NL`: Netherlands\n- `SG`: Singapore\n- `ES`: Spain\n- `TR`: Turkey\n- `AE`: United Arab Emirates\n- `GB`: United Kingdom\n- `JP`: Japan\n- `SA`: Saudi Arabia\n- `PL`: Poland\n- `SE`: Sweden\n- `BE`: Belgium\n- `EG`: Egypt\n- `ZA`: South Africa\n- `IE`: Ireland",
          "enumValues": [
            "US",
            "AU",
            "BR",
            "CA",
            "CN",
            "FR",
            "DE",
            "IN",
            "IT",
            "MX",
            "NL",
            "SG",
            "ES",
            "TR",
            "AE",
            "GB",
            "JP",
            "SA",
            "PL",
            "SE",
            "BE",
            "EG",
            "ZA",
            "IE"
          ],
          "location": "query",
          "name": "country",
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
      "path": "/api/amazon/get-best-sellers/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Best Sellers",
      "tags": [
        "Amazon"
      ]
    },
    {
      "description": "Get Amazon products By Category data, including title, price, and rating, for category-based product discovery and returns product information such as title, price, and rating.",
      "method": "GET",
      "operationId": "getProductsByCategoryV1",
      "parameters": [
        {
          "defaultValue": null,
          "description": "Authentication token for this API service.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "For example: https://amazon.com/s?node=172282 - the Amazon Category ID is 172282",
          "enumValues": [],
          "location": "query",
          "name": "categoryId",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": "US",
          "description": "Country code for the Amazon product.\n\nAvailable Values:\n- `US`: United States\n- `AU`: Australia\n- `BR`: Brazil\n- `CA`: Canada\n- `CN`: China\n- `FR`: France\n- `DE`: Germany\n- `IN`: India\n- `IT`: Italy\n- `MX`: Mexico\n- `NL`: Netherlands\n- `SG`: Singapore\n- `ES`: Spain\n- `TR`: Turkey\n- `AE`: United Arab Emirates\n- `GB`: United Kingdom\n- `JP`: Japan\n- `SA`: Saudi Arabia\n- `PL`: Poland\n- `SE`: Sweden\n- `BE`: Belgium\n- `EG`: Egypt\n- `ZA`: South Africa\n- `IE`: Ireland",
          "enumValues": [
            "US",
            "AU",
            "BR",
            "CA",
            "CN",
            "FR",
            "DE",
            "IN",
            "IT",
            "MX",
            "NL",
            "SG",
            "ES",
            "TR",
            "AE",
            "GB",
            "JP",
            "SA",
            "PL",
            "SE",
            "BE",
            "EG",
            "ZA",
            "IE"
          ],
          "location": "query",
          "name": "country",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": "RELEVANCE",
          "description": "Sort by.\n\nAvailable Values:\n- `RELEVANCE`: Relevance\n- `LOWEST_PRICE`: Lowest Price\n- `HIGHEST_PRICE`: Highest Price\n- `REVIEWS`: Reviews\n- `NEWEST`: Newest\n- `BEST_SELLERS`: Best Sellers",
          "enumValues": [
            "RELEVANCE",
            "LOWEST_PRICE",
            "HIGHEST_PRICE",
            "REVIEWS",
            "NEWEST",
            "BEST_SELLERS"
          ],
          "location": "query",
          "name": "sortBy",
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
      "path": "/api/amazon/get-category-products/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Products By Category",
      "tags": [
        "Amazon"
      ]
    },
    {
      "description": "Get Amazon product Details data, including title, brand, and price, for building product catalogs and enriching item content (e.g., images), price monitoring and availability tracking, and e-commerce analytics and competitor tracking.",
      "method": "GET",
      "operationId": "getAmazonProductDetailV1",
      "parameters": [
        {
          "defaultValue": null,
          "description": "Authentication token for this API service.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "ASIN (Amazon Standard Identification Number).",
          "enumValues": [],
          "location": "query",
          "name": "asin",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": "US",
          "description": "Country code for the Amazon product.\n\nAvailable Values:\n- `US`: United States\n- `AU`: Australia\n- `BR`: Brazil\n- `CA`: Canada\n- `CN`: China\n- `FR`: France\n- `DE`: Germany\n- `IN`: India\n- `IT`: Italy\n- `MX`: Mexico\n- `NL`: Netherlands\n- `SG`: Singapore\n- `ES`: Spain\n- `TR`: Turkey\n- `AE`: United Arab Emirates\n- `GB`: United Kingdom\n- `JP`: Japan\n- `SA`: Saudi Arabia\n- `PL`: Poland\n- `SE`: Sweden\n- `BE`: Belgium\n- `EG`: Egypt\n- `ZA`: South Africa\n- `IE`: Ireland",
          "enumValues": [
            "US",
            "AU",
            "BR",
            "CA",
            "CN",
            "FR",
            "DE",
            "IN",
            "IT",
            "MX",
            "NL",
            "SG",
            "ES",
            "TR",
            "AE",
            "GB",
            "JP",
            "SA",
            "PL",
            "SE",
            "BE",
            "EG",
            "ZA",
            "IE"
          ],
          "location": "query",
          "name": "country",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/amazon/get-product-detail/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Product Details",
      "tags": [
        "Amazon"
      ]
    },
    {
      "description": "Get Amazon product Top Reviews data, including most helpful) public reviews, for sentiment analysis and consumer feedback tracking, product research and quality assessment, and monitoring competitor customer experience.",
      "method": "GET",
      "operationId": "getProductTopReviewsV1",
      "parameters": [
        {
          "defaultValue": null,
          "description": "Authentication token for this API service.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "ASIN (Amazon Standard Identification Number).",
          "enumValues": [],
          "location": "query",
          "name": "asin",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": "US",
          "description": "Country code for the Amazon product.\n\nAvailable Values:\n- `US`: United States\n- `AU`: Australia\n- `BR`: Brazil\n- `CA`: Canada\n- `CN`: China\n- `FR`: France\n- `DE`: Germany\n- `IN`: India\n- `IT`: Italy\n- `MX`: Mexico\n- `NL`: Netherlands\n- `SG`: Singapore\n- `ES`: Spain\n- `TR`: Turkey\n- `AE`: United Arab Emirates\n- `GB`: United Kingdom\n- `JP`: Japan\n- `SA`: Saudi Arabia\n- `PL`: Poland\n- `SE`: Sweden\n- `BE`: Belgium\n- `EG`: Egypt\n- `ZA`: South Africa\n- `IE`: Ireland",
          "enumValues": [
            "US",
            "AU",
            "BR",
            "CA",
            "CN",
            "FR",
            "DE",
            "IN",
            "IT",
            "MX",
            "NL",
            "SG",
            "ES",
            "TR",
            "AE",
            "GB",
            "JP",
            "SA",
            "PL",
            "SE",
            "BE",
            "EG",
            "ZA",
            "IE"
          ],
          "location": "query",
          "name": "country",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/amazon/get-product-top-reviews/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Product Top Reviews",
      "tags": [
        "Amazon"
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
