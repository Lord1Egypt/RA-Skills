# LLM agent worked recipes

Three end-to-end recipes for the `llm-agent` skill. Each shows the scenario, the request, and the response in **OpenAI chat-completions format** over Runware's OpenAI-compatible endpoint at `https://api.runware.ai/v1`. This is not the `imageInference` task shape. Point any OpenAI client at the base URL with your Runware API key and set `model` to the AIR.

Field reminders:

- `model` is the AIR. The recipes below use `google:gemini@3.1-pro`, `moonshotai:kimi@k2.6`, and `anthropic:claude@sonnet-4.6`. Confirm each is `live` against `runware-models` before calling.
- A `tool_calls` finish means `message.content` is null and the calls live in `message.tool_calls`.
- `function.arguments` is a JSON-encoded **string**, not an object. Parse it before use.
- Every `tool` reply needs a `tool_call_id` equal to the call's `id`. That pairing is how the model matches your result to its request.
- Append both the assistant message that requested the calls and your `tool` replies to `messages` before the next request.

## Recipe 1: Basic chat completion (Gemini 3.1 Pro)

Scenario: a plain question with no tools. One request, one text answer. This is the floor every agent builds on.

Request:

```json
{
  "model": "google:gemini@3.1-pro",
  "messages": [
    { "role": "system", "content": "You are a concise technical assistant. Answer in two sentences." },
    { "role": "user", "content": "What is the difference between a process and a thread?" }
  ],
  "temperature": 0.3,
  "max_completion_tokens": 256
}
```

Response:

```json
{
  "id": "chatcmpl-7a2f1c9b04e8d1f2a6b3c0d9",
  "object": "chat.completion",
  "model": "google:gemini@3.1-pro",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "A process is an independent program with its own memory space, while a thread is a unit of execution that runs inside a process. Threads within the same process share that memory, so they are cheaper to create and switch between but require synchronization to avoid data races."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": { "prompt_tokens": 38, "completion_tokens": 61, "total_tokens": 99 }
}
```

Notes:

- No `tools` and no `tool_choice`. `finish_reason` is `stop` and `message.content` carries the full answer.
- Read the text from `choices[0].message.content`.
- Swap `model` to `anthropic:claude@sonnet-4.6` for a cheaper, faster tier, or to `google:gemini@3.1-pro` for the strongest reasoning. The request shape does not change.

## Recipe 2: Single tool-call loop (Kimi K2.6)

Scenario: an on-call assistant answers a question about live service health. Define one function as a JSON schema, the model returns a `tool_calls` message, you run the function and return the result as a `tool` message, the model finalizes. This is the four-message round-trip.

Step 1, request with `tools`:

```json
{
  "model": "moonshotai:kimi@k2.6",
  "messages": [
    { "role": "system", "content": "You are an on-call site-reliability assistant. Use the provided tools to inspect live service health before answering. Be concise, cite the numbers you found, and recommend one concrete next action." },
    { "role": "user", "content": "What is the current error rate on the payments service?" }
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_service_health",
        "description": "Return the current health of a service: status, error rate, and p95 latency.",
        "parameters": {
          "type": "object",
          "properties": {
            "service": { "type": "string", "enum": ["checkout", "payments", "search"] }
          },
          "required": ["service"]
        }
      }
    }
  ],
  "tool_choice": "auto",
  "temperature": 0.2,
  "max_completion_tokens": 1024
}
```

Step 2, model returns a tool call (`finish_reason: "tool_calls"`, `content` is null):

```json
{
  "id": "chatcmpl-1fb9303b72d3939c40a33ecd",
  "object": "chat.completion",
  "model": "moonshotai:kimi@k2.6",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": null,
        "tool_calls": [
          {
            "id": "functions.get_service_health:0",
            "type": "function",
            "function": {
              "name": "get_service_health",
              "arguments": "{\"service\":\"payments\"}"
            }
          }
        ]
      },
      "finish_reason": "tool_calls"
    }
  ],
  "usage": { "prompt_tokens": 144, "completion_tokens": 17, "total_tokens": 161 }
}
```

Step 3, run the function and append the result. Append the assistant message from step 2 first, then the `tool` reply whose `tool_call_id` matches the call's `id`:

```json
{
  "role": "tool",
  "tool_call_id": "functions.get_service_health:0",
  "content": "{\"status\":\"healthy\",\"healthy\":true,\"errorRate\":0.002,\"p95LatencyMs\":180}"
}
```

Step 4, send the full history back. The model finalizes (`finish_reason: "stop"`):

```json
{
  "id": "chatcmpl-2ac8411e93f5040db511fd4e",
  "object": "chat.completion",
  "model": "moonshotai:kimi@k2.6",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "The payments service is healthy: error rate is 0.2% (0.002) and p95 latency is 180 ms. No action is required right now."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": { "prompt_tokens": 198, "completion_tokens": 36, "total_tokens": 234 }
}
```

Notes:

- The `arguments` value `"{\"service\":\"payments\"}"` is a string. Run `JSON.parse` (TS) or `json.loads` (Python) before calling the function.
- Bound the loop. Cap iterations and stop with a clear error at the cap rather than trusting the model to always finish.
- On a tool failure, return `{ "error": "..." }` as the `tool` message content so the model can read it and adjust. A thrown exception just ends the loop.
- The `enum` on `service` is why the model never invents a service name. Constrain arguments as tightly as the real inputs allow.

## Recipe 3: Parallel tool calls (Claude Sonnet 4.6)

Scenario: the user asks for a health snapshot of all three services at once. When the model needs several independent pieces of information, it returns **multiple entries in one `tool_calls` array** instead of one round at a time. Iterate every entry and append one `tool` message per call. Because each result is matched by its own `tool_call_id`, you can run the calls concurrently and append results in any order.

Step 1, request (same `tools` block as Recipe 2):

```json
{
  "model": "anthropic:claude@sonnet-4.6",
  "messages": [
    { "role": "system", "content": "You are an on-call site-reliability assistant. Use the provided tools to inspect live service health before answering. Be concise and cite the numbers you found." },
    { "role": "user", "content": "Give me a health snapshot of checkout, payments, and search." }
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_service_health",
        "description": "Return the current health of a service: status, error rate, and p95 latency.",
        "parameters": {
          "type": "object",
          "properties": {
            "service": { "type": "string", "enum": ["checkout", "payments", "search"] }
          },
          "required": ["service"]
        }
      }
    }
  ],
  "tool_choice": "auto",
  "temperature": 0.2
}
```

Step 2, one assistant message with three tool calls:

```json
{
  "id": "chatcmpl-9d4e7c2a18b6053fc922ae71",
  "object": "chat.completion",
  "model": "anthropic:claude@sonnet-4.6",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": null,
        "tool_calls": [
          { "id": "toolu_01a", "type": "function", "function": { "name": "get_service_health", "arguments": "{\"service\":\"checkout\"}" } },
          { "id": "toolu_01b", "type": "function", "function": { "name": "get_service_health", "arguments": "{\"service\":\"payments\"}" } },
          { "id": "toolu_01c", "type": "function", "function": { "name": "get_service_health", "arguments": "{\"service\":\"search\"}" } }
        ]
      },
      "finish_reason": "tool_calls"
    }
  ],
  "usage": { "prompt_tokens": 152, "completion_tokens": 64, "total_tokens": 216 }
}
```

Step 3, append the assistant message, then one `tool` reply per call. Each `tool_call_id` matches its call's `id`:

```json
[
  { "role": "tool", "tool_call_id": "toolu_01a", "content": "{\"status\":\"degraded\",\"errorRate\":0.182,\"p95LatencyMs\":4200}" },
  { "role": "tool", "tool_call_id": "toolu_01b", "content": "{\"status\":\"healthy\",\"errorRate\":0.002,\"p95LatencyMs\":180}" },
  { "role": "tool", "tool_call_id": "toolu_01c", "content": "{\"status\":\"healthy\",\"errorRate\":0.001,\"p95LatencyMs\":95}" }
]
```

Step 4, send the full history back. The model answers in one line (`finish_reason: "stop"`):

```json
{
  "id": "chatcmpl-3f1b8e6044a2079de4c1b3a5",
  "object": "chat.completion",
  "model": "anthropic:claude@sonnet-4.6",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Checkout is degraded (18.2% error rate, 4.2s p95 latency); payments and search are healthy. Next action: investigate checkout immediately and roll back its most recent deploy if one landed in the regression window."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": { "prompt_tokens": 268, "completion_tokens": 52, "total_tokens": 320 }
}
```

Notes:

- All three calls arrive in one message. The loop that handles Recipe 2 already handles this: iterate `message.tool_calls`, append one `tool` per call, send back.
- Run the three independent calls concurrently. The `tool_call_id` pairing makes order irrelevant.
- The model may also batch calls across rounds. It reads the results, decides whether it has enough, and either calls more tools or finishes with `stop`.
