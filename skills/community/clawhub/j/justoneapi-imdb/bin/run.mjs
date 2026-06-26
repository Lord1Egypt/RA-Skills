#!/usr/bin/env node
const manifest = {
  "baseUrl": "https://api.justoneapi.com",
  "description": "Analyze IMDb workflows with JustOneAPI, including release Expectation, extended Details, and top Cast and Crew across 19 operations.",
  "displayName": "IMDb",
  "openapi": "3.1.0",
  "platformKey": "imdb",
  "primaryTag": "IMDb",
  "skillName": "justoneapi_imdb",
  "slug": "justoneapi-imdb",
  "sourceTitle": "OpenAPI definition",
  "operations": [
    {
      "description": "Get IMDb keyword Search data, including matched results, metadata, and ranking signals, for entity discovery and entertainment research.",
      "method": "GET",
      "operationId": "mainSearchQuery",
      "parameters": [
        {
          "defaultValue": null,
          "description": "User's authentication token.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "The term to search for (e.g., 'fire').",
          "enumValues": [],
          "location": "query",
          "name": "searchTerm",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": "Top",
          "description": "Category of results to include in search.\n\nAvailable Values:\n- `Top`: Top Results\n- `Movies`: Movies\n- `Shows`: TV Shows\n- `People`: People\n- `Interests`: Interests\n- `Episodes`: Episodes\n- `Podcast`: Podcasts\n- `Video_games`: Video Games",
          "enumValues": [
            "Top",
            "Movies",
            "Shows",
            "People",
            "Interests",
            "Episodes",
            "Podcast",
            "Video_games"
          ],
          "location": "query",
          "name": "type",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": 25,
          "description": "Maximum number of results to return (1-300).",
          "enumValues": [],
          "location": "query",
          "name": "limit",
          "required": false,
          "schemaType": "integer"
        },
        {
          "defaultValue": "en_US",
          "description": "Language and country preferences.\n\nAvailable Values:\n- `en_US`: English (US)\n- `fr_CA`: French (Canada)\n- `fr_FR`: French (France)\n- `de_DE`: German (Germany)\n- `hi_IN`: Hindi (India)\n- `it_IT`: Italian (Italy)\n- `pt_BR`: Portuguese (Brazil)\n- `es_ES`: Spanish (Spain)\n- `es_US`: Spanish (US)\n- `es_MX`: Spanish (Mexico)",
          "enumValues": [
            "en_US",
            "fr_CA",
            "fr_FR",
            "de_DE",
            "hi_IN",
            "it_IT",
            "pt_BR",
            "es_ES",
            "es_US",
            "es_MX"
          ],
          "location": "query",
          "name": "languageCountry",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/imdb/main-search-query/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Keyword Search",
      "tags": [
        "IMDb"
      ]
    },
    {
      "description": "Get IMDb news by Category data, including headlines, summaries, and source metadata, for media monitoring and news research.",
      "method": "GET",
      "operationId": "newsByCategoryQuery",
      "parameters": [
        {
          "defaultValue": null,
          "description": "User's authentication token.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "News category to filter by.\n\nAvailable Values:\n- `TOP`: Top News\n- `MOVIE`: Movie News\n- `TV`: TV News\n- `CELEBRITY`: Celebrity News",
          "enumValues": [
            "TOP",
            "MOVIE",
            "TV",
            "CELEBRITY"
          ],
          "location": "query",
          "name": "category",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": "en_US",
          "description": "Language and country preferences.\n\nAvailable Values:\n- `en_US`: English (US)\n- `fr_CA`: French (Canada)\n- `fr_FR`: French (France)\n- `de_DE`: German (Germany)\n- `hi_IN`: Hindi (India)\n- `it_IT`: Italian (Italy)\n- `pt_BR`: Portuguese (Brazil)\n- `es_ES`: Spanish (Spain)\n- `es_US`: Spanish (US)\n- `es_MX`: Spanish (Mexico)",
          "enumValues": [
            "en_US",
            "fr_CA",
            "fr_FR",
            "de_DE",
            "hi_IN",
            "it_IT",
            "pt_BR",
            "es_ES",
            "es_US",
            "es_MX"
          ],
          "location": "query",
          "name": "languageCountry",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/imdb/news-by-category-query/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "News by Category",
      "tags": [
        "IMDb"
      ]
    },
    {
      "description": "Get IMDb streaming Picks data, including curated titles available across streaming surfaces, for content discovery and watchlist research.",
      "method": "GET",
      "operationId": "streamingPicksQuery",
      "parameters": [
        {
          "defaultValue": null,
          "description": "User's authentication token.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": "en_US",
          "description": "Language and country preferences.\n\nAvailable Values:\n- `en_US`: English (US)\n- `fr_CA`: French (Canada)\n- `fr_FR`: French (France)\n- `de_DE`: German (Germany)\n- `hi_IN`: Hindi (India)\n- `it_IT`: Italian (Italy)\n- `pt_BR`: Portuguese (Brazil)\n- `es_ES`: Spanish (Spain)\n- `es_US`: Spanish (US)\n- `es_MX`: Spanish (Mexico)",
          "enumValues": [
            "en_US",
            "fr_CA",
            "fr_FR",
            "de_DE",
            "hi_IN",
            "it_IT",
            "pt_BR",
            "es_ES",
            "es_US",
            "es_MX"
          ],
          "location": "query",
          "name": "languageCountry",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/imdb/streaming-picks-query/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Streaming Picks",
      "tags": [
        "IMDb"
      ]
    },
    {
      "description": "Get IMDb title Awards Summary data, including nominations, for title benchmarking and awards research.",
      "method": "GET",
      "operationId": "titleAwardsSummaryQuery",
      "parameters": [
        {
          "defaultValue": null,
          "description": "User's authentication token.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "The unique IMDb ID of the title (e.g., tt12037194).",
          "enumValues": [],
          "location": "query",
          "name": "id",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": "en_US",
          "description": "Language and country preferences.\n\nAvailable Values:\n- `en_US`: English (US)\n- `fr_CA`: French (Canada)\n- `fr_FR`: French (France)\n- `de_DE`: German (Germany)\n- `hi_IN`: Hindi (India)\n- `it_IT`: Italian (Italy)\n- `pt_BR`: Portuguese (Brazil)\n- `es_ES`: Spanish (Spain)\n- `es_US`: Spanish (US)\n- `es_MX`: Spanish (Mexico)",
          "enumValues": [
            "en_US",
            "fr_CA",
            "fr_FR",
            "de_DE",
            "hi_IN",
            "it_IT",
            "pt_BR",
            "es_ES",
            "es_US",
            "es_MX"
          ],
          "location": "query",
          "name": "languageCountry",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/imdb/title-awards-summary-query/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Awards Summary",
      "tags": [
        "IMDb"
      ]
    },
    {
      "description": "Get IMDb title Base Info data, including title text, release year, and type, for catalog enrichment and title lookup workflows.",
      "method": "GET",
      "operationId": "titleBaseQuery",
      "parameters": [
        {
          "defaultValue": null,
          "description": "User's authentication token.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "The unique IMDb ID of the title (e.g., tt12037194).",
          "enumValues": [],
          "location": "query",
          "name": "id",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": "en_US",
          "description": "Language and country preferences.\n\nAvailable Values:\n- `en_US`: English (US)\n- `fr_CA`: French (Canada)\n- `fr_FR`: French (France)\n- `de_DE`: German (Germany)\n- `hi_IN`: Hindi (India)\n- `it_IT`: Italian (Italy)\n- `pt_BR`: Portuguese (Brazil)\n- `es_ES`: Spanish (Spain)\n- `es_US`: Spanish (US)\n- `es_MX`: Spanish (Mexico)",
          "enumValues": [
            "en_US",
            "fr_CA",
            "fr_FR",
            "de_DE",
            "hi_IN",
            "it_IT",
            "pt_BR",
            "es_ES",
            "es_US",
            "es_MX"
          ],
          "location": "query",
          "name": "languageCountry",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/imdb/title-base-query/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Base Info",
      "tags": [
        "IMDb"
      ]
    },
    {
      "description": "Get IMDb title Box Office Summary data, including grosses and related performance indicators, for revenue tracking and title comparison.",
      "method": "GET",
      "operationId": "titleBoxOfficeSummary",
      "parameters": [
        {
          "defaultValue": null,
          "description": "User's authentication token.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "The unique IMDb ID of the title (e.g., tt12037194).",
          "enumValues": [],
          "location": "query",
          "name": "id",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": "en_US",
          "description": "Language and country preferences.\n\nAvailable Values:\n- `en_US`: English (US)\n- `fr_CA`: French (Canada)\n- `fr_FR`: French (France)\n- `de_DE`: German (Germany)\n- `hi_IN`: Hindi (India)\n- `it_IT`: Italian (Italy)\n- `pt_BR`: Portuguese (Brazil)\n- `es_ES`: Spanish (Spain)\n- `es_US`: Spanish (US)\n- `es_MX`: Spanish (Mexico)",
          "enumValues": [
            "en_US",
            "fr_CA",
            "fr_FR",
            "de_DE",
            "hi_IN",
            "it_IT",
            "pt_BR",
            "es_ES",
            "es_US",
            "es_MX"
          ],
          "location": "query",
          "name": "languageCountry",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/imdb/title-box-office-summary/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Box Office Summary",
      "tags": [
        "IMDb"
      ]
    },
    {
      "description": "Get IMDb title Chart Rankings data, including positions in lists such as Top 250 and related charts, for ranking monitoring and title benchmarking.",
      "method": "GET",
      "operationId": "titleChartRankings",
      "parameters": [
        {
          "defaultValue": null,
          "description": "User's authentication token.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "Type of rankings chart to retrieve.\n\nAvailable Values:\n- `TOP_250`: Top 250 Movies\n- `TOP_250_TV`: Top 250 TV Shows",
          "enumValues": [
            "TOP_250",
            "TOP_250_TV"
          ],
          "location": "query",
          "name": "rankingsChartType",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": "en_US",
          "description": "Language and country preferences.\n\nAvailable Values:\n- `en_US`: English (US)\n- `fr_CA`: French (Canada)\n- `fr_FR`: French (France)\n- `de_DE`: German (Germany)\n- `hi_IN`: Hindi (India)\n- `it_IT`: Italian (Italy)\n- `pt_BR`: Portuguese (Brazil)\n- `es_ES`: Spanish (Spain)\n- `es_US`: Spanish (US)\n- `es_MX`: Spanish (Mexico)",
          "enumValues": [
            "en_US",
            "fr_CA",
            "fr_FR",
            "de_DE",
            "hi_IN",
            "it_IT",
            "pt_BR",
            "es_ES",
            "es_US",
            "es_MX"
          ],
          "location": "query",
          "name": "languageCountry",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/imdb/title-chart-rankings/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Chart Rankings",
      "tags": [
        "IMDb"
      ]
    },
    {
      "description": "Get IMDb title Contribution Questions data, including specific IMDb title, for data maintenance workflows and title metadata review.",
      "method": "GET",
      "operationId": "titleContributionQuestions",
      "parameters": [
        {
          "defaultValue": null,
          "description": "User's authentication token.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "The unique IMDb ID of the title (e.g., tt12037194).",
          "enumValues": [],
          "location": "query",
          "name": "id",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": "en_US",
          "description": "Language and country preferences.\n\nAvailable Values:\n- `en_US`: English (US)\n- `fr_CA`: French (Canada)\n- `fr_FR`: French (France)\n- `de_DE`: German (Germany)\n- `hi_IN`: Hindi (India)\n- `it_IT`: Italian (Italy)\n- `pt_BR`: Portuguese (Brazil)\n- `es_ES`: Spanish (Spain)\n- `es_US`: Spanish (US)\n- `es_MX`: Spanish (Mexico)",
          "enumValues": [
            "en_US",
            "fr_CA",
            "fr_FR",
            "de_DE",
            "hi_IN",
            "it_IT",
            "pt_BR",
            "es_ES",
            "es_US",
            "es_MX"
          ],
          "location": "query",
          "name": "languageCountry",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/imdb/title-contribution-questions/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Contribution Questions",
      "tags": [
        "IMDb"
      ]
    },
    {
      "description": "Get IMDb title Countries of Origin data, including country names and regional metadata, for catalog enrichment and regional content analysis.",
      "method": "GET",
      "operationId": "titleCountriesOfOrigin",
      "parameters": [
        {
          "defaultValue": null,
          "description": "User's authentication token.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "The unique IMDb ID of the title (e.g., tt12037194).",
          "enumValues": [],
          "location": "query",
          "name": "id",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": "en_US",
          "description": "Language and country preferences.\n\nAvailable Values:\n- `en_US`: English (US)\n- `fr_CA`: French (Canada)\n- `fr_FR`: French (France)\n- `de_DE`: German (Germany)\n- `hi_IN`: Hindi (India)\n- `it_IT`: Italian (Italy)\n- `pt_BR`: Portuguese (Brazil)\n- `es_ES`: Spanish (Spain)\n- `es_US`: Spanish (US)\n- `es_MX`: Spanish (Mexico)",
          "enumValues": [
            "en_US",
            "fr_CA",
            "fr_FR",
            "de_DE",
            "hi_IN",
            "it_IT",
            "pt_BR",
            "es_ES",
            "es_US",
            "es_MX"
          ],
          "location": "query",
          "name": "languageCountry",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/imdb/title-countries-of-origin/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Countries of Origin",
      "tags": [
        "IMDb"
      ]
    },
    {
      "description": "Get IMDb title Critics Review Summary data, including review highlights, for review analysis and title comparison.",
      "method": "GET",
      "operationId": "titleCriticsReviewSummaryQuery",
      "parameters": [
        {
          "defaultValue": null,
          "description": "User's authentication token.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "The unique IMDb ID of the title (e.g., tt12037194).",
          "enumValues": [],
          "location": "query",
          "name": "id",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": "en_US",
          "description": "Language and country preferences.\n\nAvailable Values:\n- `en_US`: English (US)\n- `fr_CA`: French (Canada)\n- `fr_FR`: French (France)\n- `de_DE`: German (Germany)\n- `hi_IN`: Hindi (India)\n- `it_IT`: Italian (Italy)\n- `pt_BR`: Portuguese (Brazil)\n- `es_ES`: Spanish (Spain)\n- `es_US`: Spanish (US)\n- `es_MX`: Spanish (Mexico)",
          "enumValues": [
            "en_US",
            "fr_CA",
            "fr_FR",
            "de_DE",
            "hi_IN",
            "it_IT",
            "pt_BR",
            "es_ES",
            "es_US",
            "es_MX"
          ],
          "location": "query",
          "name": "languageCountry",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/imdb/title-critics-review-summary-query/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Critics Review Summary",
      "tags": [
        "IMDb"
      ]
    },
    {
      "description": "Get IMDb title Details data, including metadata, release info, and cast, for deep title research and catalog enrichment.",
      "method": "GET",
      "operationId": "titleDetailsQuery",
      "parameters": [
        {
          "defaultValue": null,
          "description": "User's authentication token.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "The unique IMDb ID of the title (e.g., tt12037194).",
          "enumValues": [],
          "location": "query",
          "name": "id",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": "en_US",
          "description": "Language and country preferences.\n\nAvailable Values:\n- `en_US`: English (US)\n- `fr_CA`: French (Canada)\n- `fr_FR`: French (France)\n- `de_DE`: German (Germany)\n- `hi_IN`: Hindi (India)\n- `it_IT`: Italian (Italy)\n- `pt_BR`: Portuguese (Brazil)\n- `es_ES`: Spanish (Spain)\n- `es_US`: Spanish (US)\n- `es_MX`: Spanish (Mexico)",
          "enumValues": [
            "en_US",
            "fr_CA",
            "fr_FR",
            "de_DE",
            "hi_IN",
            "it_IT",
            "pt_BR",
            "es_ES",
            "es_US",
            "es_MX"
          ],
          "location": "query",
          "name": "languageCountry",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/imdb/title-details-query/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Details",
      "tags": [
        "IMDb"
      ]
    },
    {
      "description": "Get IMDb title 'Did You Know' Insights data, including trivia, for editorial research and title insight enrichment.",
      "method": "GET",
      "operationId": "titleDidYouKnowQuery",
      "parameters": [
        {
          "defaultValue": null,
          "description": "User's authentication token.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "The unique IMDb ID of the title (e.g., tt12037194).",
          "enumValues": [],
          "location": "query",
          "name": "id",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": "en_US",
          "description": "Language and country preferences.\n\nAvailable Values:\n- `en_US`: English (US)\n- `fr_CA`: French (Canada)\n- `fr_FR`: French (France)\n- `de_DE`: German (Germany)\n- `hi_IN`: Hindi (India)\n- `it_IT`: Italian (Italy)\n- `pt_BR`: Portuguese (Brazil)\n- `es_ES`: Spanish (Spain)\n- `es_US`: Spanish (US)\n- `es_MX`: Spanish (Mexico)",
          "enumValues": [
            "en_US",
            "fr_CA",
            "fr_FR",
            "de_DE",
            "hi_IN",
            "it_IT",
            "pt_BR",
            "es_ES",
            "es_US",
            "es_MX"
          ],
          "location": "query",
          "name": "languageCountry",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/imdb/title-did-you-know-query/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "'Did You Know' Insights",
      "tags": [
        "IMDb"
      ]
    },
    {
      "description": "Get IMDb title Extended Details data, including title info, images, and genres, for title enrichment and catalog research.",
      "method": "GET",
      "operationId": "titleExtendedDetailsQuery",
      "parameters": [
        {
          "defaultValue": null,
          "description": "User's authentication token.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "The unique IMDb ID of the title (e.g., tt12037194).",
          "enumValues": [],
          "location": "query",
          "name": "id",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": "en_US",
          "description": "Language and country preferences.\n\nAvailable Values:\n- `en_US`: English (US)\n- `fr_CA`: French (Canada)\n- `fr_FR`: French (France)\n- `de_DE`: German (Germany)\n- `hi_IN`: Hindi (India)\n- `it_IT`: Italian (Italy)\n- `pt_BR`: Portuguese (Brazil)\n- `es_ES`: Spanish (Spain)\n- `es_US`: Spanish (US)\n- `es_MX`: Spanish (Mexico)",
          "enumValues": [
            "en_US",
            "fr_CA",
            "fr_FR",
            "de_DE",
            "hi_IN",
            "it_IT",
            "pt_BR",
            "es_ES",
            "es_US",
            "es_MX"
          ],
          "location": "query",
          "name": "languageCountry",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/imdb/title-extended-details-query/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Extended Details",
      "tags": [
        "IMDb"
      ]
    },
    {
      "description": "Get IMDb title Recommendations data, including related titles and suggestion metadata, for content discovery and recommendation analysis.",
      "method": "GET",
      "operationId": "titleMoreLikeThisQuery",
      "parameters": [
        {
          "defaultValue": null,
          "description": "User's authentication token.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "The unique IMDb ID of the title (e.g., tt12037194).",
          "enumValues": [],
          "location": "query",
          "name": "id",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": "en_US",
          "description": "Language and country preferences.\n\nAvailable Values:\n- `en_US`: English (US)\n- `fr_CA`: French (Canada)\n- `fr_FR`: French (France)\n- `de_DE`: German (Germany)\n- `hi_IN`: Hindi (India)\n- `it_IT`: Italian (Italy)\n- `pt_BR`: Portuguese (Brazil)\n- `es_ES`: Spanish (Spain)\n- `es_US`: Spanish (US)\n- `es_MX`: Spanish (Mexico)",
          "enumValues": [
            "en_US",
            "fr_CA",
            "fr_FR",
            "de_DE",
            "hi_IN",
            "it_IT",
            "pt_BR",
            "es_ES",
            "es_US",
            "es_MX"
          ],
          "location": "query",
          "name": "languageCountry",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/imdb/title-more-like-this-query/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Recommendations",
      "tags": [
        "IMDb"
      ]
    },
    {
      "description": "Get IMDb title Plot Summary data, including core metrics, trend signals, and performance indicators, for displaying a detailed description of the storyline for a movie or TV show.",
      "method": "GET",
      "operationId": "titlePlotQuery",
      "parameters": [
        {
          "defaultValue": null,
          "description": "User's authentication token.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "The unique IMDb ID of the title (e.g., tt12037194).",
          "enumValues": [],
          "location": "query",
          "name": "id",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": "en_US",
          "description": "Language and country preferences.\n\nAvailable Values:\n- `en_US`: English (US)\n- `fr_CA`: French (Canada)\n- `fr_FR`: French (France)\n- `de_DE`: German (Germany)\n- `hi_IN`: Hindi (India)\n- `it_IT`: Italian (Italy)\n- `pt_BR`: Portuguese (Brazil)\n- `es_ES`: Spanish (Spain)\n- `es_US`: Spanish (US)\n- `es_MX`: Spanish (Mexico)",
          "enumValues": [
            "en_US",
            "fr_CA",
            "fr_FR",
            "de_DE",
            "hi_IN",
            "it_IT",
            "pt_BR",
            "es_ES",
            "es_US",
            "es_MX"
          ],
          "location": "query",
          "name": "languageCountry",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/imdb/title-plot-query/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Plot Summary",
      "tags": [
        "IMDb"
      ]
    },
    {
      "description": "Get IMDb title Redux Overview data, including key summary fields and linked metadata, for get a concise summary and overview of a movie or TV show's key attributes.",
      "method": "GET",
      "operationId": "titleReduxOverviewQuery",
      "parameters": [
        {
          "defaultValue": null,
          "description": "User's authentication token.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "The unique IMDb ID of the title (e.g., tt12037194).",
          "enumValues": [],
          "location": "query",
          "name": "id",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": "en_US",
          "description": "Language and country preferences.\n\nAvailable Values:\n- `en_US`: English (US)\n- `fr_CA`: French (Canada)\n- `fr_FR`: French (France)\n- `de_DE`: German (Germany)\n- `hi_IN`: Hindi (India)\n- `it_IT`: Italian (Italy)\n- `pt_BR`: Portuguese (Brazil)\n- `es_ES`: Spanish (Spain)\n- `es_US`: Spanish (US)\n- `es_MX`: Spanish (Mexico)",
          "enumValues": [
            "en_US",
            "fr_CA",
            "fr_FR",
            "de_DE",
            "hi_IN",
            "it_IT",
            "pt_BR",
            "es_ES",
            "es_US",
            "es_MX"
          ],
          "location": "query",
          "name": "languageCountry",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/imdb/title-redux-overview-query/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Redux Overview",
      "tags": [
        "IMDb"
      ]
    },
    {
      "description": "Get IMDb title Release Expectation data, including production status, release dates, and anticipation signals, for release monitoring and title research.",
      "method": "GET",
      "operationId": "titleReleaseExpectationQuery",
      "parameters": [
        {
          "defaultValue": null,
          "description": "User's authentication token.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "The unique IMDb ID of the title (e.g., tt12037194).",
          "enumValues": [],
          "location": "query",
          "name": "id",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": "en_US",
          "description": "Language and country preferences.\n\nAvailable Values:\n- `en_US`: English (US)\n- `fr_CA`: French (Canada)\n- `fr_FR`: French (France)\n- `de_DE`: German (Germany)\n- `hi_IN`: Hindi (India)\n- `it_IT`: Italian (Italy)\n- `pt_BR`: Portuguese (Brazil)\n- `es_ES`: Spanish (Spain)\n- `es_US`: Spanish (US)\n- `es_MX`: Spanish (Mexico)",
          "enumValues": [
            "en_US",
            "fr_CA",
            "fr_FR",
            "de_DE",
            "hi_IN",
            "it_IT",
            "pt_BR",
            "es_ES",
            "es_US",
            "es_MX"
          ],
          "location": "query",
          "name": "languageCountry",
          "required": false,
          "schemaType": "string"
        },
        {
          "defaultValue": false,
          "description": "Whether to accept cached data.",
          "enumValues": [],
          "location": "query",
          "name": "acceptCache",
          "required": false,
          "schemaType": "boolean"
        }
      ],
      "path": "/api/imdb/title-release-expectation-query/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Release Expectation",
      "tags": [
        "IMDb"
      ]
    },
    {
      "description": "Get IMDb title Top Cast and Crew data, including names, roles, and profile references, for talent research and title enrichment.",
      "method": "GET",
      "operationId": "titleTopCastAndCrew",
      "parameters": [
        {
          "defaultValue": null,
          "description": "User's authentication token.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "The unique IMDb ID of the title (e.g., tt12037194).",
          "enumValues": [],
          "location": "query",
          "name": "id",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": "en_US",
          "description": "Language and country preferences.\n\nAvailable Values:\n- `en_US`: English (US)\n- `fr_CA`: French (Canada)\n- `fr_FR`: French (France)\n- `de_DE`: German (Germany)\n- `hi_IN`: Hindi (India)\n- `it_IT`: Italian (Italy)\n- `pt_BR`: Portuguese (Brazil)\n- `es_ES`: Spanish (Spain)\n- `es_US`: Spanish (US)\n- `es_MX`: Spanish (Mexico)",
          "enumValues": [
            "en_US",
            "fr_CA",
            "fr_FR",
            "de_DE",
            "hi_IN",
            "it_IT",
            "pt_BR",
            "es_ES",
            "es_US",
            "es_MX"
          ],
          "location": "query",
          "name": "languageCountry",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/imdb/title-top-cast-and-crew/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "Top Cast and Crew",
      "tags": [
        "IMDb"
      ]
    },
    {
      "description": "Get IMDb title User Reviews Summary data, including aggregated review content and counts, for audience sentiment analysis.",
      "method": "GET",
      "operationId": "titleUserReviewsSummaryQuery",
      "parameters": [
        {
          "defaultValue": null,
          "description": "User's authentication token.",
          "enumValues": [],
          "location": "query",
          "name": "token",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": null,
          "description": "The unique IMDb ID of the title (e.g., tt12037194).",
          "enumValues": [],
          "location": "query",
          "name": "id",
          "required": true,
          "schemaType": "string"
        },
        {
          "defaultValue": "en_US",
          "description": "Language and country preferences.\n\nAvailable Values:\n- `en_US`: English (US)\n- `fr_CA`: French (Canada)\n- `fr_FR`: French (France)\n- `de_DE`: German (Germany)\n- `hi_IN`: Hindi (India)\n- `it_IT`: Italian (Italy)\n- `pt_BR`: Portuguese (Brazil)\n- `es_ES`: Spanish (Spain)\n- `es_US`: Spanish (US)\n- `es_MX`: Spanish (Mexico)",
          "enumValues": [
            "en_US",
            "fr_CA",
            "fr_FR",
            "de_DE",
            "hi_IN",
            "it_IT",
            "pt_BR",
            "es_ES",
            "es_US",
            "es_MX"
          ],
          "location": "query",
          "name": "languageCountry",
          "required": false,
          "schemaType": "string"
        }
      ],
      "path": "/api/imdb/title-user-reviews-summary-query/v1",
      "requestBody": null,
      "responses": [
        {
          "description": "OK",
          "statusCode": "200"
        }
      ],
      "summary": "User Reviews Summary",
      "tags": [
        "IMDb"
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
