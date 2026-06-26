#!/usr/bin/env node
const manifest = {
  "baseUrl": "https://api.justoneapi.com",
  "description": "Call GET /api/douyin-xingtu/gw/api/data_sp/get_author_convert_videos_or_products/v1 for Douyin Creator Marketplace (Xingtu) Conversion Resources through JustOneAPI with oAuthorId.",
  "displayName": "Douyin Creator Marketplace (Xingtu) Conversion Resources",
  "openapi": "3.1.0",
  "platformKey": "douyin-xingtu",
  "primaryTag": "Douyin Creator Marketplace (Xingtu)",
  "skillName": "justoneapi_douyin_xingtu_gw_api_data_sp_get_author_convert_videos_or_products",
  "slug": "justoneapi-douyin-xingtu-gw-api-data-sp-get-author-convert-videos-or-products",
  "sourceTitle": "OpenAPI definition",
  "operations": [
    {
      "description": "Get Douyin Creator Marketplace (Xingtu) conversion Resources data, including products tied to a Douyin Xingtu creator's conversion activity, for commerce analysis and campaign optimization.",
      "method": "GET",
      "operationId": "gwApiDataSpGetAuthorConvertVideosOrProductsV1",
      "parameters": [
        {
          "defaultValue": null,
          "description": "User authentication token.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Author's unique ID.",
          "enumValues": [],
          "location": "query",
          "name": "oAuthorId",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": "SHORT_VIDEO",
          "description": "Platform type.\n\nAvailable Values:\n- `SHORT_VIDEO`: Short video\n- `LIVE_STREAMING`: Live streaming\n- `PICTURE_TEXT`: Picture and text\n- `SHORT_DRAMA`: Short drama",
          "enumValues": [
            "SHORT_VIDEO",
            "LIVE_STREAMING",
            "PICTURE_TEXT",
            "SHORT_DRAMA"
          ],
          "location": "query",
          "name": "platform",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": "ALL",
          "description": "Industry category.\n\nAvailable Values:\n- `ALL`: All\n- `ELECTRONICS_AND_APPLIANCES`: Electronics and Appliances\n- `FOOD_AND_BEVERAGE`: Food and Beverage\n- `CLOTHING_AND_ACCESSORIES`: Clothing and Accessories\n- `HEALTHCARE_AND_MEDICAL`: Healthcare and Medical\n- `BUSINESS_SERVICES`: Business Services\n- `LOCAL_SERVICES`: Local Services\n- `REAL_ESTATE`: Real Estate\n- `HOME_AND_BUILDING_MATERIALS`: Home and Building Materials\n- `EDUCATION_AND_TRAINING`: Education and Training\n- `TRAVEL_AND_TOURISM`: Travel and Tourism\n- `PUBLIC_SERVICES`: Public Services\n- `GAMES`: Games\n- `RETAIL`: Retail\n- `TRANSPORTATION_EQUIPMENT`: Transportation Equipment\n- `AUTOMOTIVE`: Automotive\n- `AGRICULTURE_FORESTRY_FISHERY`: Agriculture Forestry Fishery\n- `CHEMICAL_AND_ENERGY`: Chemical and Energy\n- `ELECTRONICS_AND_ELECTRICAL`: Electronics and Electrical\n- `MACHINERY_EQUIPMENT`: Machinery Equipment\n- `CULTURE_SPORTS_ENTERTAINMENT`: Culture Sports Entertainment\n- `MEDIA_AND_INFORMATION`: Media and Information\n- `LOGISTICS`: Logistics\n- `TELECOMMUNICATIONS`: Telecommunications\n- `FINANCIAL_SERVICES`: Financial Services\n- `CATERING_SERVICES`: Catering Services\n- `SOFTWARE_TOOLS`: Software Tools\n- `FRANCHISING_AND_INVESTMENT`: Franchising and Investment\n- `BEAUTY_AND_COSMETICS`: Beauty and Cosmetics\n- `MOTHER_BABY_AND_PET`: Mother Baby and Pet\n- `DAILY_CHEMICALS`: Daily Chemicals\n- `PHYSICAL_BOOKS`: Physical Books\n- `SOCIAL_AND_COMMUNICATION`: Social and Communication\n- `MEDICAL_INSTITUTIONS`: Medical Institutions",
          "enumValues": [
            "ALL",
            "ELECTRONICS_AND_APPLIANCES",
            "FOOD_AND_BEVERAGE",
            "CLOTHING_AND_ACCESSORIES",
            "HEALTHCARE_AND_MEDICAL",
            "BUSINESS_SERVICES",
            "LOCAL_SERVICES",
            "REAL_ESTATE",
            "HOME_AND_BUILDING_MATERIALS",
            "EDUCATION_AND_TRAINING",
            "TRAVEL_AND_TOURISM",
            "PUBLIC_SERVICES",
            "GAMES",
            "RETAIL",
            "TRANSPORTATION_EQUIPMENT",
            "AUTOMOTIVE",
            "AGRICULTURE_FORESTRY_FISHERY",
            "CHEMICAL_AND_ENERGY",
            "ELECTRONICS_AND_ELECTRICAL",
            "MACHINERY_EQUIPMENT",
            "CULTURE_SPORTS_ENTERTAINMENT",
            "MEDIA_AND_INFORMATION",
            "LOGISTICS",
            "TELECOMMUNICATIONS",
            "FINANCIAL_SERVICES",
            "CATERING_SERVICES",
            "SOFTWARE_TOOLS",
            "FRANCHISING_AND_INVESTMENT",
            "BEAUTY_AND_COSMETICS",
            "MOTHER_BABY_AND_PET",
            "DAILY_CHEMICALS",
            "PHYSICAL_BOOKS",
            "SOCIAL_AND_COMMUNICATION",
            "MEDICAL_INSTITUTIONS"
          ],
          "location": "query",
          "name": "industryId",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": "DAY_30",
          "description": "Time range.\n\nAvailable Values:\n- `DAY_30`: Last 30 days\n- `DAY_90`: Last 90 days",
          "enumValues": [
            "DAY_30",
            "DAY_90"
          ],
          "location": "query",
          "name": "range",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": "VIDEO",
          "description": "Resource type.\n\nAvailable Values:\n- `VIDEO`: Video\n- `PRODUCT`: Product",
          "enumValues": [
            "VIDEO",
            "PRODUCT"
          ],
          "location": "query",
          "name": "detailType",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": 1,
          "description": "Page number.",
          "enumValues": [],
          "location": "query",
          "name": "page",
          "required": false,
          "schemaType": "integer"
        }
      ],
      "path": "/api/douyin-xingtu/gw/api/data_sp/get_author_convert_videos_or_products/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Conversion Resources",
      "tags": [
        "Douyin Creator Marketplace (Xingtu)"
      ]
    }
  ],
  "endpointPath": "gw/api/data_sp/get_author_convert_videos_or_products",
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
