#!/usr/bin/env node
const manifest = {
  "baseUrl": "https://api.justoneapi.com",
  "description": "Analyze Douyin Creator Marketplace (Xingtu) workflows with JustOneAPI, including creator Profile, creator Link Structure, and creator Visibility Status across 46 operations.",
  "displayName": "Douyin Creator Marketplace (Xingtu)",
  "openapi": "3.1.0",
  "platformKey": "douyin-xingtu",
  "primaryTag": "Douyin Creator Marketplace (Xingtu)",
  "skillName": "justoneapi_douyin_xingtu",
  "slug": "justoneapi-douyin-xingtu",
  "sourceTitle": "OpenAPI definition",
  "operations": [
    {
      "description": "Get Douyin Creator Marketplace (Xingtu) author Commerce Seeding Base Info data, including baseline metrics, commercial signals, and seeding indicators, for product seeding analysis, creator vetting, and campaign planning.",
      "method": "GET",
      "operationId": "getAuthorCommerceSeedingBaseInfoV1",
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
          "description": "KOL ID.",
          "enumValues": [],
          "location": "query",
          "name": "kolId",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Time range.",
          "enumValues": [],
          "location": "query",
          "name": "range",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": false,
          "description": "Enable cache.",
          "enumValues": [],
          "location": "query",
          "name": "acceptCache",
          "required": false,
          "schemaType": "boolean"
        }
      ],
      "path": "/api/douyin-xingtu/get-author-commerce-seed-base-info/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Author Commerce Seeding Base Info",
      "tags": [
        "Douyin Creator Marketplace (Xingtu)"
      ]
    },
    {
      "description": "Get Douyin Creator Marketplace (Xingtu) author Commerce Spread Info data, including spread metrics, for creator evaluation for campaign planning and media buying.",
      "method": "GET",
      "operationId": "getAuthorCommerceSpreadInfoV1",
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
          "description": "KOL ID.",
          "enumValues": [],
          "location": "query",
          "name": "kolId",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": false,
          "description": "Enable cache.",
          "enumValues": [],
          "location": "query",
          "name": "acceptCache",
          "required": false,
          "schemaType": "boolean"
        }
      ],
      "path": "/api/douyin-xingtu/get-author-commerce-spread-info/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Author Commerce Spread Info",
      "tags": [
        "Douyin Creator Marketplace (Xingtu)"
      ]
    },
    {
      "description": "Get Douyin Creator Marketplace (Xingtu) kOL Content Keyword Analysis data, including core metrics, trend signals, and performance indicators, for content theme analysis and creator positioning research.",
      "method": "GET",
      "operationId": "getAuthorContentHotKeywordsV1",
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
          "description": "KOL ID.",
          "enumValues": [],
          "location": "query",
          "name": "kolId",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": "0",
          "description": "Type of keywords.",
          "enumValues": [],
          "location": "query",
          "name": "keywordType",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": false,
          "description": "Enable cache.",
          "enumValues": [],
          "location": "query",
          "name": "acceptCache",
          "required": false,
          "schemaType": "boolean"
        }
      ],
      "path": "/api/douyin-xingtu/get-author-content-hot-keywords/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "KOL Content Keyword Analysis",
      "tags": [
        "Douyin Creator Marketplace (Xingtu)"
      ]
    },
    {
      "description": "Get Douyin Creator Marketplace (Xingtu) kOL Comment Keyword Analysis data, including core metrics, trend signals, and performance indicators, for audience language analysis and comment-topic research.",
      "method": "GET",
      "operationId": "getAuthorHotCommentTokensV1",
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
          "description": "KOL ID.",
          "enumValues": [],
          "location": "query",
          "name": "kolId",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": false,
          "description": "Enable cache.",
          "enumValues": [],
          "location": "query",
          "name": "acceptCache",
          "required": false,
          "schemaType": "boolean"
        }
      ],
      "path": "/api/douyin-xingtu/get-author-hot-comment-tokens/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "KOL Comment Keyword Analysis",
      "tags": [
        "Douyin Creator Marketplace (Xingtu)"
      ]
    },
    {
      "description": "Get Douyin Creator Marketplace (Xingtu) audience Distribution data, including demographic and interest-based audience segmentation, for creator evaluation, campaign planning, and marketplace research.",
      "method": "GET",
      "operationId": "getKolAudienceDistributionV1",
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
          "description": "KOL ID.",
          "enumValues": [],
          "location": "query",
          "name": "kolId",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": false,
          "description": "Enable cache.",
          "enumValues": [],
          "location": "query",
          "name": "acceptCache",
          "required": false,
          "schemaType": "boolean"
        }
      ],
      "path": "/api/douyin-xingtu/get-kol-audience-distribution/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Audience Distribution",
      "tags": [
        "Douyin Creator Marketplace (Xingtu)"
      ]
    },
    {
      "description": "Get Douyin Creator Marketplace (Xingtu) conversion Analysis data, including conversion efficiency and commercial performance indicators, for creator evaluation, campaign planning, and marketplace research.",
      "method": "GET",
      "operationId": "getKolConvertAbilityV1",
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
          "description": "KOL ID.",
          "enumValues": [],
          "location": "query",
          "name": "kolId",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Time range.\n\nAvailable Values:\n- `_1`: Last 7 days\n- `_2`: Last 30 days\n- `_3`: Last 90 days",
          "enumValues": [
            "_1",
            "_2",
            "_3"
          ],
          "location": "query",
          "name": "range",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": false,
          "description": "Enable cache.",
          "enumValues": [],
          "location": "query",
          "name": "acceptCache",
          "required": false,
          "schemaType": "boolean"
        }
      ],
      "path": "/api/douyin-xingtu/get-kol-convert-ability/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Conversion Analysis",
      "tags": [
        "Douyin Creator Marketplace (Xingtu)"
      ]
    },
    {
      "description": "Get Douyin Creator Marketplace (Xingtu) conversion Resources data, including products tied to a Douyin Xingtu creator's conversion activity, for commerce analysis and campaign optimization.",
      "method": "GET",
      "operationId": "getKolConvertVideosOrProductsV1",
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
          "description": "KOL ID.",
          "enumValues": [],
          "location": "query",
          "name": "kolId",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Resource type.\n\nAvailable Values:\n- `_1`: Video Data\n- `_2`: Product Data",
          "enumValues": [
            "_1",
            "_2"
          ],
          "location": "query",
          "name": "detailType",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Page number.",
          "enumValues": [],
          "location": "query",
          "name": "page",
          "required": true,
          "schemaType": "integer"
        },
        {
          "defaultValue": false,
          "description": "Enable cache.",
          "enumValues": [],
          "location": "query",
          "name": "acceptCache",
          "required": false,
          "schemaType": "boolean"
        }
      ],
      "path": "/api/douyin-xingtu/get-kol-convert-videos-or-products/v1",
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
    },
    {
      "description": "Get Douyin Creator Marketplace (Xingtu) cost Performance Analysis data, including pricing, exposure, and engagement efficiency indicators, for creator evaluation, campaign planning, and marketplace research.",
      "method": "GET",
      "operationId": "getKolCpInfoV1",
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
          "description": "KOL ID.",
          "enumValues": [],
          "location": "query",
          "name": "kolId",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": false,
          "description": "Enable cache.",
          "enumValues": [],
          "location": "query",
          "name": "acceptCache",
          "required": false,
          "schemaType": "boolean"
        }
      ],
      "path": "/api/douyin-xingtu/get-kol-cp-info/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Cost Performance Analysis",
      "tags": [
        "Douyin Creator Marketplace (Xingtu)"
      ]
    },
    {
      "description": "Get Douyin Creator Marketplace (Xingtu) follower Growth Trend data, including historical audience changes over time, for creator evaluation, campaign planning, and marketplace research.",
      "method": "GET",
      "operationId": "getKolDailyFansV1",
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
          "description": "KOL ID.",
          "enumValues": [],
          "location": "query",
          "name": "kolId",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Start Date (yyyy-MM-dd).",
          "enumValues": [],
          "location": "query",
          "name": "startDate",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "End Date (yyyy-MM-dd).",
          "enumValues": [],
          "location": "query",
          "name": "endDate",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": false,
          "description": "Enable cache.",
          "enumValues": [],
          "location": "query",
          "name": "acceptCache",
          "required": false,
          "schemaType": "boolean"
        }
      ],
      "path": "/api/douyin-xingtu/get-kol-daily-fans/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Follower Growth Trend",
      "tags": [
        "Douyin Creator Marketplace (Xingtu)"
      ]
    },
    {
      "description": "Get Douyin Creator Marketplace (Xingtu) follower distribution data, including audience demographics, interests, and distribution metrics, for creator evaluation, campaign planning, and marketplace research.",
      "method": "GET",
      "operationId": "getKolFansDistributionV1",
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
          "description": "KOL ID.",
          "enumValues": [],
          "location": "query",
          "name": "kolId",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": "_1",
          "description": "Fans type.\n\nAvailable Values:\n- `_1`: Fans Portrait\n- `_2`: Fans Group Portrait\n- `_5`: Iron Fans Portrait",
          "enumValues": [
            "_1",
            "_2",
            "_5"
          ],
          "location": "query",
          "name": "fansType",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": false,
          "description": "Enable cache.",
          "enumValues": [],
          "location": "query",
          "name": "acceptCache",
          "required": false,
          "schemaType": "boolean"
        }
      ],
      "path": "/api/douyin-xingtu/get-kol-fans-distribution/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Follower Distribution",
      "tags": [
        "Douyin Creator Marketplace (Xingtu)"
      ]
    },
    {
      "description": "Get Douyin Creator Marketplace (Xingtu) creator Profile data, including audience and pricing data, for influencer vetting, benchmark analysis, and campaign planning.",
      "method": "GET",
      "operationId": "getDouyinXingtuKolInfoV1",
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
          "description": "KOL ID.",
          "enumValues": [],
          "location": "query",
          "name": "kolId",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": "_1",
          "description": "Platform channel.\n\nAvailable Values:\n- `_1`: Short Video\n- `_10`: Live Streaming",
          "enumValues": [
            "_1",
            "_10"
          ],
          "location": "query",
          "name": "platformChannel",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": false,
          "description": "Enable cache.",
          "enumValues": [],
          "location": "query",
          "name": "acceptCache",
          "required": false,
          "schemaType": "boolean"
        }
      ],
      "path": "/api/douyin-xingtu/get-kol-info/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Creator Profile",
      "tags": [
        "Douyin Creator Marketplace (Xingtu)"
      ]
    },
    {
      "description": "Get Douyin Creator Marketplace (Xingtu) creator Link Metrics data, including creator ranking, traffic structure, and related performance indicators, for creator evaluation, campaign planning, and marketplace research.",
      "method": "GET",
      "operationId": "getKolLinkInfoV1",
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
          "description": "KOL ID.",
          "enumValues": [],
          "location": "query",
          "name": "kolId",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": "",
          "description": "Industry Tag.",
          "enumValues": [],
          "location": "query",
          "name": "industryTag",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": false,
          "description": "Enable cache.",
          "enumValues": [],
          "location": "query",
          "name": "acceptCache",
          "required": false,
          "schemaType": "boolean"
        }
      ],
      "path": "/api/douyin-xingtu/get-kol-link-info/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Creator Link Metrics",
      "tags": [
        "Douyin Creator Marketplace (Xingtu)"
      ]
    },
    {
      "description": "Get Douyin Creator Marketplace (Xingtu) creator Link Structure data, including engagement and conversion metrics, for creator performance analysis.",
      "method": "GET",
      "operationId": "getKolLinkStructV1",
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
          "description": "KOL ID.",
          "enumValues": [],
          "location": "query",
          "name": "kolId",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": false,
          "description": "Enable cache.",
          "enumValues": [],
          "location": "query",
          "name": "acceptCache",
          "required": false,
          "schemaType": "boolean"
        }
      ],
      "path": "/api/douyin-xingtu/get-kol-link-struct/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Creator Link Structure",
      "tags": [
        "Douyin Creator Marketplace (Xingtu)"
      ]
    },
    {
      "description": "Get Douyin Creator Marketplace (Xingtu) marketing metrics data, including rate card details and commercial service metrics, for creator evaluation, campaign planning, and marketplace research.",
      "method": "GET",
      "operationId": "getKolMarketingInfoV1",
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
          "description": "KOL ID.",
          "enumValues": [],
          "location": "query",
          "name": "kolId",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": "_1",
          "description": "Platform channel.\n\nAvailable Values:\n- `_1`: Short Video\n- `_10`: Live Streaming",
          "enumValues": [
            "_1",
            "_10"
          ],
          "location": "query",
          "name": "platformChannel",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": false,
          "description": "Enable cache.",
          "enumValues": [],
          "location": "query",
          "name": "acceptCache",
          "required": false,
          "schemaType": "boolean"
        }
      ],
      "path": "/api/douyin-xingtu/get-kol-marketing-info/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Marketing Metrics",
      "tags": [
        "Douyin Creator Marketplace (Xingtu)"
      ]
    },
    {
      "description": "Get Douyin Creator Marketplace (Xingtu) recommended videos data, including video performance metrics, for creator evaluation, campaign planning, and marketplace research.",
      "method": "GET",
      "operationId": "getKolRecVideosV1",
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
          "description": "KOL ID.",
          "enumValues": [],
          "location": "query",
          "name": "kolId",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": false,
          "description": "Enable cache.",
          "enumValues": [],
          "location": "query",
          "name": "acceptCache",
          "required": false,
          "schemaType": "boolean"
        }
      ],
      "path": "/api/douyin-xingtu/get-kol-rec-videos/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Recommended Videos",
      "tags": [
        "Douyin Creator Marketplace (Xingtu)"
      ]
    },
    {
      "description": "Get Douyin Creator Marketplace (Xingtu) showcase items data, including core metrics, trend signals, and performance indicators, for creator evaluation, campaign planning, and marketplace research.",
      "method": "GET",
      "operationId": "getKolShowItemsV2V1",
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
          "description": "KOL ID.",
          "enumValues": [],
          "location": "query",
          "name": "kolId",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": false,
          "description": "Whether true is Xingtu video, false is personal video.",
          "enumValues": [],
          "location": "query",
          "name": "onlyAssign",
          "required": false,
          "schemaType": "boolean"
        },
        {
          "defaultValue": false,
          "description": "Enable cache.",
          "enumValues": [],
          "location": "query",
          "name": "acceptCache",
          "required": false,
          "schemaType": "boolean"
        }
      ],
      "path": "/api/douyin-xingtu/get-kol-show-items-v2/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Showcase Items",
      "tags": [
        "Douyin Creator Marketplace (Xingtu)"
      ]
    },
    {
      "description": "Get Douyin Creator Marketplace (Xingtu) spread metrics data, including audience, content performance, and commercial indicators, for quick evaluation.",
      "method": "GET",
      "operationId": "getKolSpreadInfoV1",
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
          "description": "KOL ID.",
          "enumValues": [],
          "location": "query",
          "name": "kolId",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": "_1",
          "description": "Spread info type.\n\nAvailable Values:\n- `_1`: Personal Video\n- `_2`: Xingtu Video",
          "enumValues": [
            "_1",
            "_2"
          ],
          "location": "query",
          "name": "type",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": "_2",
          "description": "Time range.\n\nAvailable Values:\n- `_2`: Last 30 days\n- `_3`: Last 90 days",
          "enumValues": [
            "_2",
            "_3"
          ],
          "location": "query",
          "name": "range",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": "1",
          "description": "Flow type.",
          "enumValues": [],
          "location": "query",
          "name": "flowType",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": false,
          "description": "Only assigned notes.",
          "enumValues": [],
          "location": "query",
          "name": "onlyAssign",
          "required": false,
          "schemaType": "boolean"
        },
        {
          "defaultValue": false,
          "description": "Enable cache.",
          "enumValues": [],
          "location": "query",
          "name": "acceptCache",
          "required": false,
          "schemaType": "boolean"
        }
      ],
      "path": "/api/douyin-xingtu/get-kol-spread-info/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Spread Metrics",
      "tags": [
        "Douyin Creator Marketplace (Xingtu)"
      ]
    },
    {
      "description": "Get Douyin Creator Marketplace (Xingtu) audience touchpoint distribution data, including segment breakdowns, audience composition, and distribution signals, for traffic analysis and existing integration compatibility.",
      "method": "GET",
      "operationId": "getKolTouchDistributionV1",
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
          "description": "KOL ID.",
          "enumValues": [],
          "location": "query",
          "name": "kolId",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": false,
          "description": "Enable cache.",
          "enumValues": [],
          "location": "query",
          "name": "acceptCache",
          "required": false,
          "schemaType": "boolean"
        }
      ],
      "path": "/api/douyin-xingtu/get-kol-touch-distribution/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Audience Touchpoint Distribution",
      "tags": [
        "Douyin Creator Marketplace (Xingtu)"
      ]
    },
    {
      "description": "Get Douyin Creator Marketplace (Xingtu) video Details data, including performance fields from the legacy Douyin Xingtu endpoint, for content review and integration compatibility.",
      "method": "GET",
      "operationId": "getDouyinXingtuVideoDetailV1",
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
          "description": "Video detail ID.",
          "enumValues": [],
          "location": "query",
          "name": "detailId",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": false,
          "description": "Enable cache.",
          "enumValues": [],
          "location": "query",
          "name": "acceptCache",
          "required": false,
          "schemaType": "boolean"
        }
      ],
      "path": "/api/douyin-xingtu/get-video-detail/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Video Details",
      "tags": [
        "Douyin Creator Marketplace (Xingtu)"
      ]
    },
    {
      "description": "Get Douyin Creator Marketplace (Xingtu) author Commerce Seeding Base Info data, including baseline metrics, commercial signals, and seeding indicators, for product seeding analysis, creator vetting, and campaign planning.",
      "method": "GET",
      "operationId": "gwApiAggregatorGetAuthorCommerceSeedBaseInfoV1",
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
          "defaultValue": "DAY_90",
          "description": "Time range.\n\nAvailable Values:\n- `DAY_30`: Last 30 days\n- `DAY_90`: Last 90 days",
          "enumValues": [
            "DAY_30",
            "DAY_90"
          ],
          "location": "query",
          "name": "range",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/douyin-xingtu/gw/api/aggregator/get_author_commerce_seed_base_info/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Author Commerce Seeding Base Info",
      "tags": [
        "Douyin Creator Marketplace (Xingtu)"
      ]
    },
    {
      "description": "Get Douyin Creator Marketplace (Xingtu) author Commerce Spread Info data, including spread metrics, for creator evaluation for campaign planning and media buying.",
      "method": "GET",
      "operationId": "gwApiAggregatorGetAuthorCommerceSpreadInfoV1",
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
        }
      ],
      "path": "/api/douyin-xingtu/gw/api/aggregator/get_author_commerce_spread_info/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Author Commerce Spread Info",
      "tags": [
        "Douyin Creator Marketplace (Xingtu)"
      ]
    },
    {
      "description": "Get Douyin Creator Marketplace (Xingtu) creator Order Experience data, including commercial history and transaction-related indicators, for creator evaluation, campaign planning, and marketplace research.",
      "method": "GET",
      "operationId": "gwApiAggregatorGetAuthorOrderExperienceV1",
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
          "defaultValue": "DAY_30",
          "description": "Time period.\n\nAvailable Values:\n- `DAY_30`: Last 30 days\n- `DAY_90`: Last 90 days",
          "enumValues": [
            "DAY_30",
            "DAY_90"
          ],
          "location": "query",
          "name": "period",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/douyin-xingtu/gw/api/aggregator/get_author_order_experience/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Creator Order Experience",
      "tags": [
        "Douyin Creator Marketplace (Xingtu)"
      ]
    },
    {
      "description": "Get Douyin Creator Marketplace (Xingtu) creator Profile data, including audience and pricing data, for influencer vetting, benchmark analysis, and campaign planning.",
      "method": "GET",
      "operationId": "gwApiAuthorGetAuthorBaseInfoV1",
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
        }
      ],
      "path": "/api/douyin-xingtu/gw/api/author/get_author_base_info/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Creator Profile",
      "tags": [
        "Douyin Creator Marketplace (Xingtu)"
      ]
    },
    {
      "description": "Get Douyin Creator Marketplace (Xingtu) marketing metrics data, including rate card details and commercial service metrics, for creator evaluation, campaign planning, and marketplace research.",
      "method": "GET",
      "operationId": "gwApiAuthorGetAuthorMarketingInfoV1",
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
        }
      ],
      "path": "/api/douyin-xingtu/gw/api/author/get_author_marketing_info/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Marketing Metrics",
      "tags": [
        "Douyin Creator Marketplace (Xingtu)"
      ]
    },
    {
      "description": "Get Douyin Creator Marketplace (Xingtu) creator Channel Metrics data, including platform distribution and channel performance data used, for creator evaluation.",
      "method": "GET",
      "operationId": "gwApiAuthorGetAuthorPlatformChannelInfoV2V1",
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
        }
      ],
      "path": "/api/douyin-xingtu/gw/api/author/get_author_platform_channel_info_v2/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Creator Channel Metrics",
      "tags": [
        "Douyin Creator Marketplace (Xingtu)"
      ]
    },
    {
      "description": "Get Douyin Creator Marketplace (Xingtu) showcase Items data, including products and videos associated with the account, for creator evaluation, campaign planning, and marketplace research.",
      "method": "GET",
      "operationId": "gwApiAuthorGetAuthorShowItemsV2V1",
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
          "defaultValue": false,
          "description": "Whether to only include assigned items.",
          "enumValues": [],
          "location": "query",
          "name": "onlyAssign",
          "required": false,
          "schemaType": "boolean"
        },
        {
          "defaultValue": "EXCLUDE",
          "description": "Flow type filter.\n\nAvailable Values:\n- `EXCLUDE`: Exclude\n- `INCLUDE`: Include",
          "enumValues": [
            "EXCLUDE",
            "INCLUDE"
          ],
          "location": "query",
          "name": "flowType",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/douyin-xingtu/gw/api/author/get_author_show_items_v2/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Showcase Items",
      "tags": [
        "Douyin Creator Marketplace (Xingtu)"
      ]
    },
    {
      "description": "Get Douyin Creator Marketplace (Xingtu) audience Distribution data, including demographic and interest-based audience segmentation, for creator evaluation, campaign planning, and marketplace research.",
      "method": "GET",
      "operationId": "gwApiDataSpAuthorAudienceDistributionV1",
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
          "defaultValue": "CONNECTED",
          "description": "Link type filter.\n\nAvailable Values:\n- `CONNECTED`: Connected\n- `AWARE`: Aware\n- `INTERESTED`: Interested\n- `LIKE`: Like\n- `FOLLOW`: Follow",
          "enumValues": [
            "CONNECTED",
            "AWARE",
            "INTERESTED",
            "LIKE",
            "FOLLOW"
          ],
          "location": "query",
          "name": "linkType",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/douyin-xingtu/gw/api/data_sp/author_audience_distribution/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Audience Distribution",
      "tags": [
        "Douyin Creator Marketplace (Xingtu)"
      ]
    },
    {
      "description": "Get Douyin Creator Marketplace (Xingtu) cost Performance Analysis data, including pricing, exposure, and engagement efficiency indicators, for creator evaluation, campaign planning, and marketplace research.",
      "method": "GET",
      "operationId": "gwApiDataSpAuthorCpInfoV1",
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
        }
      ],
      "path": "/api/douyin-xingtu/gw/api/data_sp/author_cp_info/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Cost Performance Analysis",
      "tags": [
        "Douyin Creator Marketplace (Xingtu)"
      ]
    },
    {
      "description": "Get Douyin Creator Marketplace (Xingtu) creator Link Structure data, including engagement and conversion metrics, for creator performance analysis.",
      "method": "GET",
      "operationId": "gwApiDataSpAuthorLinkStructV1",
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
        }
      ],
      "path": "/api/douyin-xingtu/gw/api/data_sp/author_link_struct/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Creator Link Structure",
      "tags": [
        "Douyin Creator Marketplace (Xingtu)"
      ]
    },
    {
      "description": "Get Douyin Creator Marketplace (Xingtu) recommended Videos data, including content references used, for creator evaluation.",
      "method": "GET",
      "operationId": "gwApiDataSpAuthorRecVideosV2V1",
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
        }
      ],
      "path": "/api/douyin-xingtu/gw/api/data_sp/author_rec_videos_v2/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Recommended Videos",
      "tags": [
        "Douyin Creator Marketplace (Xingtu)"
      ]
    },
    {
      "description": "Get Douyin Creator Marketplace (Xingtu) audience Touchpoint Distribution data, including segment breakdowns, audience composition, and distribution signals, for creator evaluation, campaign planning, and marketplace research.",
      "method": "GET",
      "operationId": "gwApiDataSpAuthorTouchDistributionV1",
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
        }
      ],
      "path": "/api/douyin-xingtu/gw/api/data_sp/author_touch_distribution/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Audience Touchpoint Distribution",
      "tags": [
        "Douyin Creator Marketplace (Xingtu)"
      ]
    },
    {
      "description": "Get Douyin Creator Marketplace (Xingtu) video Distribution data, including content performance breakdowns across published videos, for creator evaluation, campaign planning, and marketplace research.",
      "method": "GET",
      "operationId": "gwApiDataSpAuthorVideoDistributionV1",
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
        }
      ],
      "path": "/api/douyin-xingtu/gw/api/data_sp/author_video_distribution/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Video Distribution",
      "tags": [
        "Douyin Creator Marketplace (Xingtu)"
      ]
    },
    {
      "description": "Get Douyin Creator Marketplace (Xingtu) creator Visibility Status data, including availability status, discovery eligibility, and campaign display signals, for creator evaluation, campaign planning, and marketplace research.",
      "method": "GET",
      "operationId": "gwApiDataSpCheckAuthorDisplayV1",
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
        }
      ],
      "path": "/api/douyin-xingtu/gw/api/data_sp/check_author_display/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Creator Visibility Status",
      "tags": [
        "Douyin Creator Marketplace (Xingtu)"
      ]
    },
    {
      "description": "Get Douyin Creator Marketplace (Xingtu) conversion Analysis data, including conversion efficiency and commercial performance indicators, for creator evaluation, campaign planning, and marketplace research.",
      "method": "GET",
      "operationId": "gwApiDataSpGetAuthorConvertAbilityV1",
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
        }
      ],
      "path": "/api/douyin-xingtu/gw/api/data_sp/get_author_convert_ability/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Conversion Analysis",
      "tags": [
        "Douyin Creator Marketplace (Xingtu)"
      ]
    },
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
    },
    {
      "description": "Get Douyin Creator Marketplace (Xingtu) follower Growth Trend data, including historical audience changes over time, for creator evaluation, campaign planning, and marketplace research.",
      "method": "GET",
      "operationId": "gwApiDataSpGetAuthorDailyFansV1",
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
          "defaultValue": null,
          "description": "Start Date (yyyy-MM-dd).",
          "enumValues": [],
          "location": "query",
          "name": "startDate",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "End Date (yyyy-MM-dd).",
          "enumValues": [],
          "location": "query",
          "name": "endDate",
          "required": true,
          "schemaType": "string"
        }
      ],
      "path": "/api/douyin-xingtu/gw/api/data_sp/get_author_daily_fans/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Follower Growth Trend",
      "tags": [
        "Douyin Creator Marketplace (Xingtu)"
      ]
    },
    {
      "description": "Get Douyin Creator Marketplace (Xingtu) follower Distribution data, including audience segmentation and location and demographic breakdowns, for creator evaluation, campaign planning, and marketplace research.",
      "method": "GET",
      "operationId": "gwApiDataSpGetAuthorFansDistributionV1",
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
          "defaultValue": "FAN",
          "description": "Author type filter.\n\nAvailable Values:\n- `FAN`: Fan\n- `DIE_HARD_FAN`: Die Hard Fan",
          "enumValues": [
            "FAN",
            "DIE_HARD_FAN"
          ],
          "location": "query",
          "name": "authorType",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/douyin-xingtu/gw/api/data_sp/get_author_fans_distribution/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Follower Distribution",
      "tags": [
        "Douyin Creator Marketplace (Xingtu)"
      ]
    },
    {
      "description": "Get Douyin Creator Marketplace (Xingtu) creator Link Metrics data, including creator ranking, traffic structure, and related performance indicators, for creator evaluation, campaign planning, and marketplace research.",
      "method": "GET",
      "operationId": "gwApiDataSpGetAuthorLinkInfoV1",
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
          "description": "Industry tag.\n\nAvailable Values:\n- `ALL`: All\n- `ELECTRONICS_AND_APPLIANCES`: Electronics and Appliances\n- `FOOD_AND_BEVERAGE`: Food and Beverage\n- `CLOTHING_AND_ACCESSORIES`: Clothing and Accessories\n- `HEALTHCARE_AND_MEDICAL`: Healthcare and Medical\n- `BUSINESS_SERVICES`: Business Services\n- `LOCAL_SERVICES`: Local Services\n- `REAL_ESTATE`: Real Estate\n- `HOME_AND_BUILDING_MATERIALS`: Home and Building Materials\n- `EDUCATION_AND_TRAINING`: Education and Training\n- `TRAVEL_AND_TOURISM`: Travel and Tourism\n- `PUBLIC_SERVICES`: Public Services\n- `GAMES`: Games\n- `RETAIL`: Retail\n- `TRANSPORTATION_EQUIPMENT`: Transportation Equipment\n- `AUTOMOTIVE`: Automotive\n- `AGRICULTURE_FORESTRY_FISHERY`: Agriculture Forestry Fishery\n- `CHEMICAL_AND_ENERGY`: Chemical and Energy\n- `ELECTRONICS_AND_ELECTRICAL`: Electronics and Electrical\n- `MACHINERY_EQUIPMENT`: Machinery Equipment\n- `CULTURE_SPORTS_ENTERTAINMENT`: Culture Sports Entertainment\n- `MEDIA_AND_INFORMATION`: Media and Information\n- `LOGISTICS`: Logistics\n- `TELECOMMUNICATIONS`: Telecommunications\n- `FINANCIAL_SERVICES`: Financial Services\n- `CATERING_SERVICES`: Catering Services\n- `SOFTWARE_TOOLS`: Software Tools\n- `FRANCHISING_AND_INVESTMENT`: Franchising and Investment\n- `BEAUTY_AND_COSMETICS`: Beauty and Cosmetics\n- `MOTHER_BABY_AND_PET`: Mother Baby and Pet\n- `DAILY_CHEMICALS`: Daily Chemicals\n- `PHYSICAL_BOOKS`: Physical Books\n- `SOCIAL_AND_COMMUNICATION`: Social and Communication\n- `MEDICAL_INSTITUTIONS`: Medical Institutions",
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
          "name": "industryTag",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/douyin-xingtu/gw/api/data_sp/get_author_link_info/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Creator Link Metrics",
      "tags": [
        "Douyin Creator Marketplace (Xingtu)"
      ]
    },
    {
      "description": "Get Douyin Creator Marketplace (Xingtu) spread metrics data, including exposure, spread, and related performance indicators, for creator evaluation, campaign planning, and marketplace research.",
      "method": "GET",
      "operationId": "gwApiDataSpGetAuthorSpreadInfoV1",
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
          "defaultValue": "PERSONAL_VIDEO",
          "description": "Video type.\n\nAvailable Values:\n- `PERSONAL_VIDEO`: Personal video\n- `XINTU_VIDEO`: Xingtu video",
          "enumValues": [
            "PERSONAL_VIDEO",
            "XINTU_VIDEO"
          ],
          "location": "query",
          "name": "type",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": false,
          "description": "Whether to only include assigned videos.",
          "enumValues": [],
          "location": "query",
          "name": "onlyAssign",
          "required": false,
          "schemaType": "boolean"
        },
        {
          "defaultValue": "EXCLUDE",
          "description": "Flow type filter.\n\nAvailable Values:\n- `EXCLUDE`: Exclude\n- `INCLUDE`: Include",
          "enumValues": [
            "EXCLUDE",
            "INCLUDE"
          ],
          "location": "query",
          "name": "flowType",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/douyin-xingtu/gw/api/data_sp/get_author_spread_info/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Spread Metrics",
      "tags": [
        "Douyin Creator Marketplace (Xingtu)"
      ]
    },
    {
      "description": "Get Douyin Creator Marketplace (Xingtu) item Report Details data, including key metrics and report fields used, for item performance analysis.",
      "method": "GET",
      "operationId": "gwApiDataSpItemReportDetailV1",
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
          "description": "Item's unique ID.",
          "enumValues": [],
          "location": "query",
          "name": "itemId",
          "required": true,
          "schemaType": "string"
        }
      ],
      "path": "/api/douyin-xingtu/gw/api/data_sp/item_report_detail/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Item Report Details",
      "tags": [
        "Douyin Creator Marketplace (Xingtu)"
      ]
    },
    {
      "description": "Get Douyin Creator Marketplace (Xingtu) item Report Analysis data, including performance interpretation, for creator evaluation, campaign planning, and marketplace research.",
      "method": "GET",
      "operationId": "gwApiDataSpItemReportThAnalysisV1",
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
          "description": "Item's unique ID.",
          "enumValues": [],
          "location": "query",
          "name": "itemId",
          "required": true,
          "schemaType": "string"
        }
      ],
      "path": "/api/douyin-xingtu/gw/api/data_sp/item_report_th_analysis/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Item Report Analysis",
      "tags": [
        "Douyin Creator Marketplace (Xingtu)"
      ]
    },
    {
      "description": "Get Douyin Creator Marketplace (Xingtu) item Report Trend data, including time-based changes in item performance metrics, for creator evaluation, campaign planning, and marketplace research.",
      "method": "GET",
      "operationId": "gwApiDataSpItemReportTrendV1",
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
          "description": "Item's unique ID.",
          "enumValues": [],
          "location": "query",
          "name": "itemId",
          "required": true,
          "schemaType": "string"
        }
      ],
      "path": "/api/douyin-xingtu/gw/api/data_sp/item_report_trend/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Item Report Trends",
      "tags": [
        "Douyin Creator Marketplace (Xingtu)"
      ]
    },
    {
      "description": "Get Douyin Creator Marketplace (Xingtu) kOL Comment Keyword Analysis data, including core metrics, trend signals, and performance indicators, for audience language analysis and comment-topic research.",
      "method": "GET",
      "operationId": "gwApiDataGetAuthorHotCommentTokensV1",
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
        }
      ],
      "path": "/api/douyin-xingtu/gw/api/data/get_author_hot_comment_tokens/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "KOL Comment Keyword Analysis",
      "tags": [
        "Douyin Creator Marketplace (Xingtu)"
      ]
    },
    {
      "description": "Get Douyin Creator Marketplace (Xingtu) kOL Content Keyword Analysis data, including core metrics, trend signals, and performance indicators, for content theme analysis and creator positioning research.",
      "method": "GET",
      "operationId": "gwApiGauthorGetAuthorContentHotKeywordsV1",
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
        }
      ],
      "path": "/api/douyin-xingtu/gw/api/gauthor/get_author_content_hot_keywords/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "KOL Content Keyword Analysis",
      "tags": [
        "Douyin Creator Marketplace (Xingtu)"
      ]
    },
    {
      "description": "Get Douyin Creator Marketplace (Xingtu) creator Search data, including filters, returning profile, and audience, for discovery, comparison, and shortlist building.",
      "method": "GET",
      "operationId": "gwApiGsearchSearchForAuthorSquareV1",
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
          "defaultValue": "",
          "description": "Search keyword.",
          "enumValues": [],
          "location": "query",
          "name": "keyword",
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
        },
        {
          "defaultValue": "NICKNAME",
          "description": "Search criteria type.\n\nAvailable Values:\n- `NICKNAME`: By Nickname\n- `CONTENT`: By Content",
          "enumValues": [
            "NICKNAME",
            "CONTENT"
          ],
          "location": "query",
          "name": "searchType",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Follower range (e.g., 10-100).",
          "enumValues": [],
          "location": "query",
          "name": "followerRange",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "KOL price type.\n\nAvailable Values:\n- `视频1_20s`: Video 1-20s\n- `视频21_60s`: Video 21-60s\n- `视频60s以上`: Video > 60s\n- `定制短剧单集`: Mini-drama episode\n- `千次自然播放量`: CPM naturally\n- `短直种草视频`: Short-live seeding video\n- `短直预热视频`: Short-live warm-up video\n- `短直明星种草`: Celebrity short-live seeding\n- `短直明星预热`: Celebrity short-live warm-up\n- `明星视频`: Celebrity video\n- `合集视频`: Collection video\n- `抖音短视频共创_主投稿达人`: Douyin short video co-creation - main creator\n- `抖音短视频共创_参与达人`: Douyin short video co-creation - participant",
          "enumValues": [
            "视频1_20s",
            "视频21_60s",
            "视频60s以上",
            "定制短剧单集",
            "千次自然播放量",
            "短直种草视频",
            "短直预热视频",
            "短直明星种草",
            "短直明星预热",
            "明星视频",
            "合集视频",
            "抖音短视频共创_主投稿达人",
            "抖音短视频共创_参与达人"
          ],
          "location": "query",
          "name": "kolPriceType",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "KOL price range (e.g., 10000-50000).",
          "enumValues": [],
          "location": "query",
          "name": "kolPriceRange",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Content tag filter.",
          "enumValues": [],
          "location": "query",
          "name": "contentTag",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/douyin-xingtu/gw/api/gsearch/search_for_author_square/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Creator Search",
      "tags": [
        "Douyin Creator Marketplace (Xingtu)"
      ]
    },
    {
      "description": "Get Douyin Creator Marketplace (Xingtu) kOL Keyword Search data, including matching creators and discovery data, for creator sourcing and shortlist building.",
      "method": "GET",
      "operationId": "searchKolSimpleV1",
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
          "description": "Search keywords.",
          "enumValues": [],
          "location": "query",
          "name": "keyword",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Platform source.\n\nAvailable Values:\n- `_1`: Douyin\n- `_2`: Toutiao\n- `_3`: Xigua",
          "enumValues": [
            "_1",
            "_2",
            "_3"
          ],
          "location": "query",
          "name": "platformSource",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Page number.",
          "enumValues": [],
          "location": "query",
          "name": "page",
          "required": true,
          "schemaType": "integer"
        },
        {
          "defaultValue": false,
          "description": "Enable cache.",
          "enumValues": [],
          "location": "query",
          "name": "acceptCache",
          "required": false,
          "schemaType": "boolean"
        }
      ],
      "path": "/api/douyin-xingtu/search-kol-simple/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "KOL Keyword Search",
      "tags": [
        "Douyin Creator Marketplace (Xingtu)"
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
