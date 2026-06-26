# API Integration MCP Tool Patterns

## REST API Wrapper

```typescript
server.tool("api_get", {
  url: z.string().describe("Full URL to fetch"),
  headers: z.record(z.string()).optional()
}, async ({ url, headers: extraHeaders }) => {
  const resp = await fetch(url, {
    headers: { "Accept": "application/json", ...extraHeaders }
  });
  const data = await resp.json();
  return { content: [{ type: "text", text: JSON.stringify(data, null, 2) }] };
});

server.tool("api_post", {
  url: z.string(),
  body: z.record(z.any()),
  headers: z.record(z.string()).optional()
}, async ({ url, body, headers: extraHeaders }) => {
  const resp = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...extraHeaders },
    body: JSON.stringify(body)
  });
  const data = await resp.json();
  return { content: [{ type: "text", text: JSON.stringify(data, null, 2) }] };
});
```

## GraphQL

```typescript
server.tool("graphql_query", {
  endpoint: z.string(),
  query: z.string().describe("GraphQL query string"),
  variables: z.record(z.any()).optional()
}, async ({ endpoint, query, variables }) => {
  const resp = await fetch(endpoint, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, variables })
  });
  const data = await resp.json();
  return { content: [{ type: "text", text: JSON.stringify(data, null, 2) }] };
});
```

## Rate-Limited API Client

```python
import asyncio
from functools import wraps

def rate_limit(calls_per_second: float = 1.0):
    semaphore = asyncio.Semaphore(1)
    min_interval = 1.0 / calls_per_second
    last_call = 0.0

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            nonlocal last_call
            async with semaphore:
                now = asyncio.get_event_loop().time()
                wait = max(0, min_interval - (now - last_call))
                if wait > 0:
                    await asyncio.sleep(wait)
                last_call = asyncio.get_event_loop().time()
                return await func(*args, **kwargs)
        return wrapper
    return decorator
```
