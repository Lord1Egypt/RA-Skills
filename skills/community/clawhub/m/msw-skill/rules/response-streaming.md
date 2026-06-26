---
title: Use ReadableStream for Streaming Responses
impact: HIGH
description: Simulate streaming (SSE, chunked responses) using a ReadableStream body with HttpResponse.
tags: response, streaming, ReadableStream, SSE, event-stream
---

# Use ReadableStream for Streaming Responses

## Problem

Some applications use Server-Sent Events or chunked transfer. Returning the entire body at once doesn't test streaming behavior.

## Incorrect

```typescript
// Not streaming — entire body returned at once
http.get('/api/stream', () => {
  return HttpResponse.text('data: chunk1\n\ndata: chunk2\n\n', {
    headers: { 'Content-Type': 'text/event-stream' },
  })
})
```

## Correct

```typescript
import { http, HttpResponse, delay } from 'msw'

http.get('/api/stream', () => {
  const stream = new ReadableStream({
    async start(controller) {
      controller.enqueue(new TextEncoder().encode('data: chunk1\n\n'))
      await delay(100)
      controller.enqueue(new TextEncoder().encode('data: chunk2\n\n'))
      controller.close()
    },
  })

  return new HttpResponse(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      Connection: 'keep-alive',
    },
  })
})
```

## Why

Using a `ReadableStream` lets you simulate realistic streaming behavior — chunks arrive over time, which is important for testing progress indicators, incremental rendering, and SSE event handling. Returning the full body at once bypasses these code paths.
