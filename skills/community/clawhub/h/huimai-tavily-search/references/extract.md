> ## Documentation Index
> Fetch the complete documentation index at: https://docs.tavily.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Tavily Extract

> Extract web page content from one or more specified URLs using Tavily Extract.



## OpenAPI

````yaml POST /extract
openapi: 3.0.3
info:
  title: Tavily Search and Extract API
  description: >-
    Our REST API provides seamless access to Tavily Search, a powerful search
    engine for LLM agents, and Tavily Extract, an advanced web scraping solution
    optimized for LLMs.
  version: 1.0.0
servers:
  - url: https://api.tavily.com/
security: []
tags:
  - name: Search
  - name: Extract
  - name: Crawl
  - name: Map
  - name: Research
  - name: Usage
paths:
  /extract:
    post:
      summary: Retrieve raw web content from specified URLs
      description: >-
        Extract web page content from one or more specified URLs using Tavily
        Extract.
      requestBody:
        description: Parameters for the Tavily Extract request.
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                urls:
                  oneOf:
                    - type: string
                      description: The URL to extract content from.
                      example: https://en.wikipedia.org/wiki/Artificial_intelligence
                    - type: array
                      items:
                        type: string
                      description: A list of URLs to extract content from.
                      example:
                        - https://en.wikipedia.org/wiki/Artificial_intelligence
                        - https://en.wikipedia.org/wiki/Machine_learning
                        - https://en.wikipedia.org/wiki/Data_science
                query:
                  type: string
                  description: >-
                    User intent for reranking extracted content chunks. When
                    provided, chunks are reranked based on relevance to this
                    query.
                chunks_per_source:
                  type: integer
                  description: >-
                    Chunks are short content snippets (maximum 500 characters
                    each) pulled directly from the source. Use
                    `chunks_per_source` to define the maximum number of relevant
                    chunks returned per source and to control the `raw_content`
                    length. Chunks will appear in the `raw_content` field as:
                    `<chunk 1> [...] <chunk 2> [...] <chunk 3>`. Available only
                    when `query` is provided. Must be between 1 and 5.
                  minimum: 1
                  maximum: 5
                  default: 3
                extract_depth:
                  type: string
                  description: >-
                    The depth of the extraction process. `advanced` extraction
                    retrieves more data, including tables and embedded content,
                    with higher success but may increase latency.`basic`
                    extraction costs 1 credit per 5 successful URL extractions,
                    while `advanced` extraction costs 2 credits per 5 successful
                    URL extractions.
                  enum:
                    - basic
                    - advanced
                  default: basic
                include_images:
                  type: boolean
                  description: >-
                    Include a list of images extracted from the URLs in the
                    response. Default is false.
                  default: false
                include_favicon:
                  type: boolean
                  description: Whether to include the favicon URL for each result.
                  default: false
                format:
                  type: string
                  description: >-
                    The format of the extracted web page content. `markdown`
                    returns content in markdown format. `text` returns plain
                    text and may increase latency.
                  enum:
                    - markdown
                    - text
                  default: markdown
                timeout:
                  type: number
                  format: float
                  description: >-
                    Maximum time in seconds to wait for the URL extraction
                    before timing out. Must be between 1.0 and 60.0 seconds. If
                    not specified, default timeouts are applied based on
                    extract_depth: 10 seconds for basic extraction and 30
                    seconds for advanced extraction.
                  minimum: 1
                  maximum: 60
                  default: None
                include_usage:
                  type: boolean
                  description: >-
                    Whether to include credit usage information in the response.
                    `NOTE:`The value may be 0 if the total successful URL
                    extractions has not yet reached 5 calls. See our [Credits &
                    Pricing
                    documentation](https://docs.tavily.com/documentation/api-credits)
                    for details.
                  default: false
              required:
                - urls
      responses:
        '200':
          description: Extraction results returned successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  results:
                    type: array
                    description: A list of extracted content from the provided URLs.
                    items:
                      type: object
                      properties:
                        url:
                          type: string
                          description: The URL from which the content was extracted.
                          example: >-
                            https://en.wikipedia.org/wiki/Artificial_intelligence
                        raw_content:
                          type: string
                          description: >-
                            The full content extracted from the page. When
                            `query` is provided, contains the top-ranked chunks
                            joined by `[...]` separator.
                          example: >-
                            "Jump to content\nMain
                            menu\nSearch\nAppearance\nDonate\nCreate
                            account\nLog in\nPersonal tools\n        Photograph
                            your local culture, help Wikipedia and win!\nToggle
                            the table of contents\nArtificial intelligence\n161
                            languages\nArticle\nTalk\nRead\nView source\nView
                            history\nTools\nFrom Wikipedia, the free
                            encyclopedia\n\"AI\" redirects here. For other uses,
                            see AI (disambiguation) and Artificial intelligence
                            (disambiguation).\nPart of a series on\nArtificial
                            intelligence (AI)\nshow\nMajor
                            goals\nshow\nApproaches\nshow\nApplications\nshow\nPhilosophy\nshow\nHistory\nshow\nGlossary\nvte\nArtificial
                            intelligence (AI), in its broadest sense, is
                            intelligence exhibited by machines, particularly
                            computer systems. It is a field of research in
                            computer science that develops and studies methods
                            and software that enable machines to perceive their
                            environment and use learning and intelligence to
                            take actions that maximize their chances of
                            achieving defined goals.[1] Such machines may be
                            called AIs.\nHigh-profile applications of AI include
                            advanced web search engines (e.g., Google Search);
                            recommendation systems (used by YouTube, Amazon, and
                            Netflix); virtual assistants (e.g., Google
                            Assistant, Siri, and Alexa); autonomous vehicles
                            (e.g., Waymo); generative and creative tools (e.g.,
                            ChatGPT and AI art); and superhuman play and
                            analysis in strategy games (e.g., chess and
                            Go)...................
                        images:
                          type: array
                          example: []
                          description: >-
                            This is only available if `include_images` is set to
                            `true`. A list of image URLs extracted from the
                            page.
                          items:
                            type: string
                        favicon:
                          type: string
                          description: The favicon URL for the result.
                          example: >-
                            https://en.wikipedia.org/static/favicon/wikipedia.ico
                  failed_results:
                    type: array
                    example: []
                    description: A list of URLs that could not be processed.
                    items:
                      type: object
                      properties:
                        url:
                          type: string
                          description: The URL that failed to be processed.
                        error:
                          type: string
                          description: >-
                            An error message describing why the URL couldn't be
                            processed.
                  response_time:
                    type: number
                    format: float
                    description: Time in seconds it took to complete the request.
                    example: 0.02
                  usage:
                    type: object
                    description: Credit usage details for the request.
                    example:
                      credits: 1
                  request_id:
                    type: string
                    description: >-
                      A unique request identifier you can share with customer
                      support to help resolve issues with specific requests.
                    example: 123e4567-e89b-12d3-a456-426614174111
        '400':
          description: Bad Request
          content:
            application/json:
              schema:
                type: object
                properties:
                  detail:
                    type: object
                    properties:
                      error:
                        type: string
              example:
                detail:
                  error: <400 Bad Request, (e.g Max 20 URLs are allowed.)>
        '401':
          description: Unauthorized - Your API key is wrong or missing.
          content:
            application/json:
              schema:
                type: object
                properties:
                  detail:
                    type: object
                    properties:
                      error:
                        type: string
              example:
                detail:
                  error: 'Unauthorized: missing or invalid API key.'
        '429':
          description: Too many requests - Rate limit exceeded
          content:
            application/json:
              schema:
                type: object
                properties:
                  detail:
                    type: object
                    properties:
                      error:
                        type: string
              example:
                detail:
                  error: >-
                    Your request has been blocked due to excessive requests.
                    Please reduce rate of requests.
        '432':
          description: Key limit or Plan Limit exceeded
          content:
            application/json:
              schema:
                type: object
                properties:
                  detail:
                    type: object
                    properties:
                      error:
                        type: string
              example:
                detail:
                  error: >-
                    <432 Custom Forbidden Error (e.g This request exceeds your
                    plan's set usage limit. Please upgrade your plan or contact
                    support@tavily.com)>
        '433':
          description: PayGo limit exceeded
          content:
            application/json:
              schema:
                type: object
                properties:
                  detail:
                    type: object
                    properties:
                      error:
                        type: string
              example:
                detail:
                  error: >-
                    This request exceeds the pay-as-you-go limit. You can
                    increase your limit on the Tavily dashboard.
        '500':
          description: Internal Server Error - We had a problem with our server.
          content:
            application/json:
              schema:
                type: object
                properties:
                  detail:
                    type: object
                    properties:
                      error:
                        type: string
              example:
                detail:
                  error: Internal Server Error
      security:
        - bearerAuth: []
      x-codeSamples:
        - lang: python
          label: Python SDK
          source: >-
            from tavily import TavilyClient


            tavily_client = TavilyClient(api_key="tvly-YOUR_API_KEY")

            response =
            tavily_client.extract("https://en.wikipedia.org/wiki/Artificial_intelligence")


            print(response)
        - lang: javascript
          label: JavaScript SDK
          source: >-
            const { tavily } = require("@tavily/core");


            const tvly = tavily({ apiKey: "tvly-YOUR_API_KEY" });

            const response = await
            tvly.extract("https://en.wikipedia.org/wiki/Artificial_intelligence");


            console.log(response);
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: >-
        Bearer authentication header in the form Bearer <token>, where <token>
        is your Tavily API key (e.g., Bearer tvly-YOUR_API_KEY).

````
