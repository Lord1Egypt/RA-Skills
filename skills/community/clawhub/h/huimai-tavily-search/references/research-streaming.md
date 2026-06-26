> ## Documentation Index
> Fetch the complete documentation index at: https://docs.tavily.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Streaming

> Stream real-time research progress and results from Tavily Research API

## Overview

When using the Tavily Research API, you can stream responses in real-time by setting `stream: true` in your request. This allows you to receive research progress updates, tool calls, and final results as they're generated, providing a better user experience for long-running research tasks.

Streaming is particularly useful for:

* Displaying research progress to users in real-time
* Monitoring tool calls and search queries as they execute
* Receiving incremental updates during lengthy research operations
* Building interactive research interfaces

## Enabling Streaming

To enable streaming, set the `stream` parameter to `true` when making a request to the Research endpoint:

```json  theme={null}
{
  "input": "What are the latest developments in AI?",
  "stream": true
}
```

The API will respond with a `text/event-stream` content type, sending Server-Sent Events (SSE) as the research progresses.

## Event Structure

Each streaming event follows a consistent structure compatible with the OpenAI chat completions format:

```json  theme={null}
{
  "id": "123e4567-e89b-12d3-a456-426614174111",
  "object": "chat.completion.chunk",
  "model": "mini",
  "created": 1705329000,
  "choices": [
    {
      "delta": {
        // Event-specific data here
      }
    }
  ]
}
```

### Core Fields

| Field     | Type    | Description                                           |
| --------- | ------- | ----------------------------------------------------- |
| `id`      | string  | Unique identifier for the stream event                |
| `object`  | string  | Always `"chat.completion.chunk"` for streaming events |
| `model`   | string  | The research model being used (`"mini"` or `"pro"`)   |
| `created` | integer | Unix timestamp when the event was created             |
| `choices` | array   | Array containing the delta with event details         |

## Event Types

The streaming response includes different types of events in the `delta` object. Here are the main event types you'll encounter:

### 1. Tool Call Events

When the research agent performs actions like web searches, you'll receive tool call events:

```json  theme={null}
{
  "id": "evt_002",
  "object": "chat.completion.chunk",
  "model": "mini",
  "created": 1705329005,
  "choices": [
    {
      "delta": {
        "role": "assistant",
        "tool_calls": {
          "type": "tool_call",
          "tool_call": [
            {
              "name": "WebSearch",
              "id": "fc_633b5932-e66c-4523-931a-04a7b79f2578",
              "arguments": "Executing 5 search queries",
              "queries": ["latest AI developments 2024", "machine learning breakthroughs", "..."]
            }
          ]
        }
      }
    }
  ]
}
```

**Tool Call Delta Fields:**

| Field                 | Type   | Description                                                        |
| --------------------- | ------ | ------------------------------------------------------------------ |
| `type`                | string | Either `"tool_call"` or `"tool_response"`                          |
| `tool_call`           | array  | Details about the tool being invoked                               |
| `name`                | string | Name of the tool (see [Tool Types](#tool-types) below)             |
| `id`                  | string | Unique identifier for the tool call                                |
| `arguments`           | string | Description of the action being performed                          |
| `queries`             | array  | *(WebSearch only)* The search queries being executed               |
| `parent_tool_call_id` | string | *(Pro mode only)* ID of the parent tool call for nested operations |

### 2. Tool Response Events

After a tool executes, you'll receive response events with discovered sources:

```json  theme={null}
{
  "id": "evt_003",
  "object": "chat.completion.chunk",
  "model": "mini",
  "created": 1705329010,
  "choices": [
    {
      "delta": {
        "role": "assistant",
        "tool_calls": {
          "type": "tool_response",
          "tool_response": [
            {
              "name": "WebSearch",
              "id": "fc_633b5932-e66c-4523-931a-04a7b79f2578",
              "arguments": "Completed executing search tool call",
              "sources": [
                {
                  "url": "https://example.com/article",
                  "title": "Example Article",
                  "favicon": "https://example.com/favicon.ico"
                }
              ]
            }
          ]
        }
      }
    }
  ]
}
```

**Tool Response Fields:**

| Field                 | Type   | Description                                                     |
| --------------------- | ------ | --------------------------------------------------------------- |
| `name`                | string | Name of the tool that completed                                 |
| `id`                  | string | Unique identifier matching the original tool call               |
| `arguments`           | string | Completion status message                                       |
| `sources`             | array  | Sources discovered by the tool (with `url`, `title`, `favicon`) |
| `parent_tool_call_id` | string | *(Pro mode only)* ID of the parent tool call                    |

### 3. Content Events

The final research report is streamed as content chunks:

```json  theme={null}
{
  "id": "evt_004",
  "object": "chat.completion.chunk",
  "model": "mini",
  "created": 1705329015,
  "choices": [
    {
      "delta": {
        "role": "assistant",
        "content": "# Research Report\n\nBased on the latest sources..."
      }
    }
  ]
}
```

**Content Field:**

* Can be a **string** (markdown-formatted report chunks) when no `output_schema` is provided
* Can be an **object** (structured data) when an `output_schema` is specified

### 4. Sources Event

After the content is streamed, a sources event is emitted containing all sources used in the research:

```json  theme={null}
{
  "id": "evt_005",
  "object": "chat.completion.chunk",
  "model": "mini",
  "created": 1705329020,
  "choices": [
    {
      "delta": {
        "role": "assistant",
        "sources": [
          {
            "url": "https://example.com/article",
            "title": "Example Article Title",
            "favicon": "https://example.com/favicon.ico"
          }
        ]
      }
    }
  ]
}
```

**Source Object Fields:**

| Field     | Type   | Description                  |
| --------- | ------ | ---------------------------- |
| `url`     | string | The URL of the source        |
| `title`   | string | The title of the source page |
| `favicon` | string | URL to the source's favicon  |

### 5. Done Event

Signals the completion of the streaming response:

```
event: done
```

## Tool Types

During research, you'll encounter the following tool types in streaming events:

| Tool Name          | Description                                                    | Model    |
| ------------------ | -------------------------------------------------------------- | -------- |
| `Planning`         | Initializes the research plan based on the input query         | Both     |
| `Generating`       | Generates the final research report from collected information | Both     |
| `WebSearch`        | Executes web searches to gather information                    | Both     |
| `ResearchSubtopic` | Conducts deep research on specific subtopics                   | Pro only |

### Research Flow Example

A typical streaming session follows this sequence:

1. **Planning** tool\_call → Initializing research plan
2. **Planning** tool\_response → Research plan initialized
3. **WebSearch** tool\_call → Executing search queries (with `queries` array)
4. **WebSearch** tool\_response → Search completed (with `sources` array)
5. *(Pro mode)* **ResearchSubtopic** tool\_call/response cycles for deeper research
6. **Generating** tool\_call → Generating final report
7. **Generating** tool\_response → Report generated
8. **Content** events → Streamed report chunks
9. **Sources** event → Complete list of all sources used
10. **Done** event → Stream complete

## Handling Streaming Responses

### Python Example

```python  theme={null}
from tavily import TavilyClient

# Step 1. Instantiating your TavilyClient
tavily_client = TavilyClient(api_key="tvly-YOUR_API_KEY")

# Step 2. Creating a streaming research task
stream = tavily_client.research(
    input="Research the latest developments in AI",
    model="pro",
    stream=True
)

for chunk in stream:
    print(chunk.decode('utf-8'))
```

### JavaScript Example

```javascript  theme={null}
const { tavily } = require("@tavily/core");

const tvly = tavily({ apiKey: "tvly-YOUR_API_KEY" });

const stream = await tvly.research("Research the latest developments in AI", {
  model: "pro",
  stream: true,
});

for await (const chunk of result as AsyncGenerator<Buffer, void, unknown>) {
    console.log(chunk.toString('utf-8'));
}
```

## Structured Output with Streaming

When using `output_schema` to request structured data, the `content` field will contain an object instead of a string:

```json  theme={null}
{
  "delta": {
    "role": "assistant",
    "content": {
      "company": "Acme Corp",
      "key_metrics": ["Revenue: $1M", "Growth: 50%"],
      "summary": "Company showing strong growth..."
    }
  }
}
```

## Error Handling

If an error occurs during streaming, you may receive an error event:

```json  theme={null}
{
  "id": "1d77bdf5-38a4-46c1-87a6-663dbc4528ec",
  "object": "error",
  "error": "An error occurred while streaming the research task"
}
```

Always implement proper error handling in your streaming client to gracefully handle these cases.

## Non-Streaming Alternative

If you don't need real-time updates, set `stream: false` (or omit the parameter) to receive a single complete response:

```json  theme={null}
{
  "request_id": "123e4567-e89b-12d3-a456-426614174111",
  "created_at": "2025-01-15T10:30:00Z",
  "status": "pending",
  "input": "What are the latest developments in AI?",
  "model": "mini",
  "response_time": 1.23
}
```

You can then poll the status endpoint to check when the research is complete.
