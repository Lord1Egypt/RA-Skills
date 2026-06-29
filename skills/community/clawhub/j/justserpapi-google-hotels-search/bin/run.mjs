#!/usr/bin/env node
const manifest = {
  "baseUrl": "https://api.justserpapi.com",
  "description": "Call GET /api/v1/google/hotels/search for Google SERP Hotels Search through Just Serp API with check_in_date, check_out_date, and query.",
  "displayName": "Google SERP Hotels Search",
  "openapi": "3.1.0",
  "platformKey": "google",
  "primaryTag": "Google SERP",
  "skillName": "justserpapi_google_hotels_search",
  "slug": "justserpapi-google-hotels-search",
  "sourceTitle": "API Shop Documentation",
  "operations": [
    {
      "description": "Get Google hotels Search data, including prices, ratings, and availability details, for travel comparison and hospitality market analysis.",
      "method": "GET",
      "operationId": "hotelsSearch",
      "parameters": [
        {
          "defaultValue": null,
          "description": "The destination or specific hotel name you are searching for (e.g., 'Paris', 'Hilton New York').",
          "enumValues": [],
          "location": "query",
          "name": "query",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "The hotel check-in date in 'YYYY-MM-DD' format (e.g., '2026-05-20').",
          "enumValues": [],
          "location": "query",
          "name": "check_in_date",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "The hotel check-out date in 'YYYY-MM-DD' format (e.g., '2026-05-25').",
          "enumValues": [],
          "location": "query",
          "name": "check_out_date",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "The token used to retrieve the next page of hotel results. This token is found in the 'next_page_token' field of a previous response.",
          "enumValues": [],
          "location": "query",
          "name": "next_page_token",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "The number of adults staying in the room.",
          "enumValues": [],
          "location": "query",
          "name": "adults",
          "required": false,
          "schemaType": "integer"
        },
        {
          "defaultValue": null,
          "description": "The number of children staying in the room.",
          "enumValues": [],
          "location": "query",
          "name": "children",
          "required": false,
          "schemaType": "integer"
        },
        {
          "defaultValue": null,
          "description": "The ages of the children, separated by commas (e.g., '5,10'). The number of ages must match the 'children' parameter.",
          "enumValues": [],
          "location": "query",
          "name": "children_ages",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Set to true to return the raw HTML of the Google search results page alongside the structured data.",
          "enumValues": [],
          "location": "query",
          "name": "html",
          "required": false,
          "schemaType": "boolean"
        },
        {
          "defaultValue": null,
          "description": "Set the language for the results using its two-letter code (e.g., 'en' for English, 'fr' for French). See <a href=\"/reference/google-language\">Google Language</a>.",
          "enumValues": [],
          "location": "query",
          "name": "language",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Set the target country code (e.g., 'us', 'uk') to localize results. See <a href=\"/reference/google-countries\">Google Countries</a>.",
          "enumValues": [],
          "location": "query",
          "name": "country",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "The three-letter ISO currency code for displaying prices (e.g., 'USD', 'EUR'). See <a href=\"/reference/hotels/google-hotels-currency\">Google Hotels Currency</a>.",
          "enumValues": [],
          "location": "query",
          "name": "currency",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "The criteria to sort hotel results. Supported values: '3' (Lowest price), '8' (Highest rating), '13' (Most reviews).",
          "enumValues": [],
          "location": "query",
          "name": "sort_by",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Minimum price filter for the hotel stay.",
          "enumValues": [],
          "location": "query",
          "name": "min_price",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Maximum price filter for the hotel stay.",
          "enumValues": [],
          "location": "query",
          "name": "max_price",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Filter by hotel property types. See the <a href=\"/reference/hotels/google-hotels-property-types\">Google Property Types</a> for the full list of supported hotel property types. For vacation rentals, refer to the <a href=\"/reference/hotels/google-hotels-vacation-rentals-property-types\">Google Hotels Vacation Rentals Property Types</a>.",
          "enumValues": [],
          "location": "query",
          "name": "property_types",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Filter by specific amenities (e.g., '35' for free Wi-Fi). <a href=\"/reference/hotels/google-hotels-amenities\">Google Hotels Amenities</a> (hotel amenities). <a href=\"/reference/hotels/google-hotels-vacation-rentals-amenities\">Google Hotels Vacation Rentals Amenities</a> (vacation rental amenities)",
          "enumValues": [],
          "location": "query",
          "name": "amenities",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Filter by minimum guest rating. Supported values: '7' (3.5+), '8' (4.0+), '9' (4.5+).",
          "enumValues": [],
          "location": "query",
          "name": "rating",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Filter by specific hotel brand IDs. IDs can be comma-separated.",
          "enumValues": [],
          "location": "query",
          "name": "brands",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Filter by hotel star ratings. Supported values: '2', '3', '4', '5'. Can be comma-separated.",
          "enumValues": [],
          "location": "query",
          "name": "hotel_class",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Filter for hotels that offer free cancellation. Set to '1' or 'true' to enable.",
          "enumValues": [],
          "location": "query",
          "name": "free_cancellation",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Filter for hotels currently offering special deals or discounts. Set to '1' or 'true' to enable.",
          "enumValues": [],
          "location": "query",
          "name": "special_offers",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Filter for hotels that are eco-certified. Set to '1' or 'true' to enable.",
          "enumValues": [],
          "location": "query",
          "name": "eco_certified",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Set to true to search for vacation rentals instead of standard hotels.",
          "enumValues": [],
          "location": "query",
          "name": "vacation_rentals",
          "required": false,
          "schemaType": "boolean"
        },
        {
          "defaultValue": null,
          "description": "Minimum number of bedrooms required (applies to vacation rentals).",
          "enumValues": [],
          "location": "query",
          "name": "bedrooms",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Minimum number of bathrooms required (applies to vacation rentals).",
          "enumValues": [],
          "location": "query",
          "name": "bathrooms",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "The unique token for a specific hotel property to fetch detailed information.",
          "enumValues": [],
          "location": "query",
          "name": "property_token",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/v1/google/hotels/search",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        },
        {
          "description": "Authentication failed: API Key is invalid or missing",
          "statusCode": "401"
        },
        {
          "description": "Access denied: Insufficient credits or quota exceeded",
          "statusCode": "403"
        },
        {
          "description": "Internal server error or upstream service exception",
          "statusCode": "500"
        }
      ],
      "summary": "Search",
      "tags": [
        "Google Hotels"
      ]
    }
  ],
  "endpointPath": "hotels/search",
  "skillType": "interface"
};
const args = parseArgs(process.argv.slice(2));

if (!args.operation) {
  fail("Missing required --operation argument.");
}

const operation = manifest.operations.find((item) => item.operationId === args.operation);
if (!operation) {
  fail(`Unknown operation "${args.operation}".`, { availableOperations: manifest.operations.map((item) => item.operationId) });
}

if (!args.apiKey) {
  fail("Missing required --api-key argument.");
}

const params = parseParams(args.paramsJson);
applyDefaults(operation, params);
validateRequired(operation, params);

const baseUrl = manifest.baseUrl;
const url = new URL(operation.path, ensureBaseUrl(baseUrl));
applyPathParams(operation, params, url);
applyQueryParams(operation, params, url);

const requestInit = {
  headers: {
    "accept": "application/json",
    "X-API-Key": args.apiKey,
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
  const parsed = { apiKey: null, operation: null, paramsJson: "{}" };
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
    if (flag === "--api-key") {
      parsed.apiKey = value;
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
