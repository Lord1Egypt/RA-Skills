> ## Documentation Index
> Fetch the complete documentation index at: https://docs.tavily.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Get Research Task Status

> Retrieve the status and results of a research task using its request ID.



## OpenAPI

````yaml GET /research/{request_id}
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
  /research/{request_id}:
    get:
      summary: Get research task status and results
      description: Retrieve the status and results of a research task using its request ID.
      parameters:
        - name: request_id
          in: path
          required: true
          description: The unique identifier of the research task.
          schema:
            type: string
          example: 123e4567-e89b-12d3-a456-426614174111
      responses:
        '200':
          description: Research task is completed or failed.
          content:
            application/json:
              schema:
                oneOf:
                  - $ref: '#/components/schemas/ResearchTaskCompleted'
                  - $ref: '#/components/schemas/ResearchTaskFailed'
                discriminator:
                  propertyName: status
                  mapping:
                    completed:
                      $ref: '#/components/schemas/ResearchTaskCompleted'
                    failed:
                      $ref: '#/components/schemas/ResearchTaskFailed'
        '202':
          description: Research task is not yet completed (pending or in_progress).
          content:
            application/json:
              schema:
                type: object
                properties:
                  request_id:
                    type: string
                    description: The unique identifier of the research task.
                    example: 123e4567-e89b-12d3-a456-426614174111
                  status:
                    type: string
                    description: Current status of the research task.
                    enum:
                      - pending
                      - in_progress
                  response_time:
                    type: integer
                    description: Time in seconds it took to complete the request.
                    example: 1.23
                required:
                  - request_id
                  - response_time
                  - status
              example:
                request_id: 123e4567-e89b-12d3-a456-426614174111
                status: in_progress
                response_time: 1.23
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
        '404':
          description: Research task not found
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
                  error: Research task not found
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
                  error: Error getting research status
      security:
        - bearerAuth: []
      x-codeSamples:
        - lang: python
          label: Python SDK
          source: >-
            from tavily import TavilyClient


            tavily_client = TavilyClient(api_key="tvly-YOUR_API_KEY")

            response =
            tavily_client.get_research("123e4567-e89b-12d3-a456-426614174111")


            print(response)
        - lang: javascript
          label: JavaScript SDK
          source: >-
            const { tavily } = require("@tavily/core");


            const tvly = tavily({ apiKey: "tvly-YOUR_API_KEY" });

            const response = await
            tvly.get_research("123e4567-e89b-12d3-a456-426614174111");


            console.log(response);
components:
  schemas:
    ResearchTaskCompleted:
      title: Completed
      type: object
      properties:
        request_id:
          type: string
          description: The unique identifier of the research task.
          example: 123e4567-e89b-12d3-a456-426614174111
        created_at:
          type: string
          description: Timestamp when the research task was created.
          example: '2025-01-15T10:30:00Z'
        status:
          type: string
          description: The current status of the research task.
          enum:
            - completed
        content:
          oneOf:
            - type: string
            - type: object
          description: >-
            The research report content. Can be a string or a structured object
            if output_schema was provided.
        sources:
          type: array
          description: List of sources used in the research.
          items:
            type: object
            properties:
              title:
                type: string
                description: Title or name of the source.
                example: Latest AI Developments
              url:
                type: string
                format: uri
                description: URL of the source.
                example: https://example.com/ai-news
              favicon:
                type: string
                format: uri
                description: URL to the source's favicon.
                example: https://example.com/favicon.ico
        response_time:
          type: integer
          description: Time in seconds it took to complete the request.
          example: 1.23
      required:
        - request_id
        - created_at
        - status
        - content
        - sources
        - response_time
      example:
        request_id: 123e4567-e89b-12d3-a456-426614174111
        created_at: '2025-01-15T10:30:00Z'
        status: completed
        content: >-
          Research Report: Latest Developments in AI


          ## Executive Summary


          Artificial Intelligence has seen significant advancements in recent
          months, with major breakthroughs in large language models, multimodal
          AI systems, and real-world applications...
        sources:
          - title: Latest AI Developments
            url: https://example.com/ai-news
            favicon: https://example.com/favicon.ico
          - title: AI Research Breakthroughs
            url: https://example.com/ai-research
            favicon: https://example.com/favicon.ico
        response_time: 1.23
    ResearchTaskFailed:
      title: Failed
      type: object
      properties:
        request_id:
          type: string
          description: The unique identifier of the research task.
          example: 123e4567-e89b-12d3-a456-426614174111
        status:
          type: string
          description: The current status of the research task.
          enum:
            - failed
        response_time:
          type: integer
          description: Time in seconds it took to complete the request.
          example: 1.23
      required:
        - request_id
        - status
        - response_time
      example:
        request_id: 123e4567-e89b-12d3-a456-426614174111
        status: failed
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: >-
        Bearer authentication header in the form Bearer <token>, where <token>
        is your Tavily API key (e.g., Bearer tvly-YOUR_API_KEY).

````