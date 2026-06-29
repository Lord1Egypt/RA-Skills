# Options Reference

Options can be passed to the `Crawler()` constructor (global) or to individual
`crawler.add()` calls (per-task, overriding globals).

- A plain URL string is accepted as a shorthand.
- An array of options adds multiple tasks at once.
- All native [got options](https://github.com/sindresorhus/got/blob/main/documentation/2-options.md)
  are accepted and passed through. Only Crawler-specific options are listed below.

## Global-only options

These can only be set on the constructor.

### `silence`

- **Type:** `boolean`
- **Default:** `false`
- Mute all warning and error messages from the crawler. Request errors are still reported to the callback.

### `maxConnections`

- **Type:** `number`
- **Default:** `10`
- Maximum number of concurrent requests.

### `priorityLevels`

- **Type:** `number`
- **Default:** `10`
- Number of priority levels. Can only be set at construction time.

### `rateLimit`

- **Type:** `number`
- **Default:** `0`
- Minimum gap (ms) between two requests on the default rate limiter.
  **Note:** This sets the default value for limiter 0. Change it at runtime
  with `crawler.setLimiter()`. Do not pass a redundant `rateLimit` in per-task
  options — use `options.rateLimiterId` instead.
- When `rateLimit > 0`, `maxConnections` is forced to `1`.

```js
crawler.on("schedule", options => {
  options.rateLimiterId = Math.floor(Math.random() * 15);
});
```

### `skipDuplicates`

- **Type:** `boolean`
- **Default:** `false`
- If `true`, skip tasks that are already in the queue (by URL).

### `homogeneous`

- **Type:** `boolean`
- **Default:** `false`
- If `true`, dynamically reallocate tasks from head-of-line-blocked queues to
  other queues.

### `userAgents`

- **Type:** `string | string[]`
- **Default:** `undefined`
- If set, rotate the User-Agent header for each request. Must be an array.

## General options

These can be set globally or per-task.

### `url | method | headers | body | searchParams | form | ...`

Standard [got options](https://github.com/sindresorhus/got/blob/main/documentation/2-options.md).
Pass through directly to the underlying request.

### `forceUTF8`

- **Type:** `boolean`
- **Default:** `false`
- Detect charset from HTTP headers or HTML `<meta>` tags and convert to UTF-8.

### `jQuery`

- **Type:** `boolean`
- **Default:** `true`
- Parse response body with Cheerio and expose as `res.$`.

### `encoding`

- **Type:** `string`
- **Default:** `"utf8"`
- Response body encoding. Set to `null` for binary downloads (keeps body as `Buffer`).

### `rateLimiterId`

- **Type:** `number`
- **Default:** `0`
- Which rate limiter to use for this task. Useful for per-proxy limiting.

### `retries`

- **Type:** `number`
- **Default:** `2`
- Number of times to retry on failure.

### `retryInterval`

- **Type:** `number`
- **Default:** `3000`
- Milliseconds to wait before retrying.

### `timeout`

- **Type:** `number`
- **Default:** `20000`
- Request timeout in milliseconds.

### `priority`

- **Type:** `number`
- **Default:** `5`
- Task priority within the range `[0, priorityLevels)`.

### `skipEventRequest`

- **Type:** `boolean`
- **Default:** `false`
- If `true`, suppress the `'request'` event for this task.

### `html`

- **Type:** `boolean`
- **Default:** `true`
- Parse response body as HTML.

### `proxies`

- **Type:** `string[]`
- **Default:** `[]`
- Array of proxy URLs, rotated per request. **Recommended:** use the
  `'schedule'` event instead for more control.

### `proxy`

- **Type:** `string`
- **Default:** `undefined`
- Proxy URL for this task. Overrides `proxies`.

### `http2`

- **Type:** `boolean`
- **Default:** `false`
- Use HTTP/2 protocol.

### `autoSelectFamily`

- **Type:** `boolean`
- **Default:** `true` (Node default)
- Controls Node's "Happy Eyeballs" (races IPv6 and IPv4). Set to `false` on
  networks with broken/slow IPv6 to avoid `ETIMEDOUT` errors.
- **Note:** Node sets this process-wide.

### `autoSelectFamilyAttemptTimeout`

- **Type:** `number`
- **Default:** `250` (Node default)
- How long (ms) "Happy Eyeballs" waits for one address family before trying the
  next. Raise it (e.g. `5000`) for high-latency hosts.
- **Note:** Node sets this process-wide.

### `referer`

- **Type:** `string`
- **Default:** `undefined`
- HTTP `Referer` header value.

### `userParams`

- **Type:** `any`
- **Default:** `undefined`
- Arbitrary data to attach to the task. Accessible in the callback via
  `res.options.userParams`. This is the only supported way to pass custom data.

### `preRequest`

- **Type:** `(options, done) => void`
- **Default:** `undefined`
- Hook called before each request (queue mode only, not `send()`). Call
  `done()` to proceed.

### `callback`

- **Type:** `(error, res, done) => void`
- The callback for this task.
  - `error` — caught by the crawler
  - `res` — response object with:
    - `res.options` — Options for this task
    - `res.$` — Cheerio instance (if `jQuery` is not `false`)
    - `res.statusCode` — HTTP status code
    - `res.body` — Response body (Buffer | string)
    - `res.headers` — Response headers
  - `done` — must be called to signal task completion

## Events

| Event | Signature | Description |
|-------|-----------|-------------|
| `'schedule'` | `(options)` | Emitted when a task is added to the scheduler |
| `'limiterChange'` | `(options, rateLimiterId)` | Emitted when the limiter changes |
| `'request'` | `(options)` | Emitted right before a request is sent |
| `'drain'` | `()` | Emitted when the queue is empty |

## Class API

### `crawler.add(url | options)`

Add a task to the queue. Accepts a URL string, an options object, or an array
of either.

### `crawler.send(options)`

Send a direct request (bypasses queue, rate limiter, and events). Supports
both Promise and callback forms.

### `crawler.setLimiter(id, property, value)`

Modify a rate limiter's property at runtime. Currently only `"rateLimit"` is
supported.

```js
crawler.setLimiter(0, "rateLimit", 1000);
```

### `crawler.queueSize`

- **Type:** `number` (read-only)
- Number of tasks currently in the queue.
