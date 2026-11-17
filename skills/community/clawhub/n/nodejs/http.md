# HTTP — Servers, Clients, and the Timeouts Between Them

Most "flaky network" incidents in Node are one of three things: a timeout ordered wrong, a socket pool too small or never reused, or a body nobody consumed.

## Server Timeouts (the 502 factory)

Defaults on node >=18: `keepAliveTimeout` 5 s, `headersTimeout` 60 s, `requestTimeout` 300 s, `server.timeout` 0 (disabled).

```js
const server = http.createServer(app);
server.keepAliveTimeout = 65_000;   // proxy idle + 5 s (SKILL.md rule 5)
server.headersTimeout   = 66_000;   // keepAliveTimeout + 1 s
server.requestTimeout   = 30_000;   // a request that cannot finish in 30 s is not finishing
```

- The failure signature of getting this wrong: a small, steady percentage of 502s with no error in your logs — the proxy reused a socket in the microsecond Node was closing it. Nothing in the application is broken, which is why it survives so many deploys.
- `headersTimeout` below `keepAliveTimeout` closes idle keep-alive connections early and produces the same symptom from the other direction; keep the order in the ladder (SKILL.md Timeout Ladder).
- `requestTimeout` covers the whole request including a slow body upload; it is the Slowloris defense. Disabling it (0) to fix a large-upload route is how a single client holds every socket.
- Behind AWS ALB the idle default is 60 s → 65 s / 66 s. Behind nginx the upstream `keepalive_timeout` default is 75 s → 80 s / 81 s. Read the proxy's value; never assume.

## Client Connections

- Global `fetch` (undici, node >=18) pools connections by origin and keeps them alive. `http.Agent` defaults to `keepAlive: true` on node >=19; on older majors, an agent without it opens a fresh TCP+TLS handshake per request — the single cheapest latency win in legacy services.
- Every response body must be consumed or discarded, even when you only wanted the status: an unread body keeps the connection checked out until GC. `await res.body.cancel()` or `await res.text()` on the paths that ignore the payload.
- Per-origin concurrency is capped by the agent/dispatcher, not by your `Promise.all` — issuing 5k requests just queues 5k promises in memory. Cap at the source (SKILL.md rule 4).
- Timeouts on every outbound call: `fetch(url, { signal: AbortSignal.timeout(3000) })`. A hung upstream with no deadline holds a socket, a descriptor, and one of your request slots until the process restarts.
- Proxies: global `fetch` ignores `HTTP_PROXY`/`HTTPS_PROXY` by default. Set an undici `ProxyAgent` as the global dispatcher when the environment requires one; corporate TLS interception additionally needs the root CA (`NODE_EXTRA_CA_CERTS=/path/ca.pem`).
- `NODE_TLS_REJECT_UNAUTHORIZED=0` disables certificate verification process-wide, including calls you did not write. It is never the fix — install the CA instead.

## Retries That Help Instead Of Hurt

- Retry only idempotent requests (GET, PUT, DELETE, or POST carrying an idempotency key). Retrying a non-idempotent POST on timeout double-charges customers; the request may have succeeded and only the response was lost.
- Retry only on connection errors and 5xx/429 — never on 4xx, which will fail identically forever.
- Exponential backoff with jitter: `delay = min(cap, base × 2^attempt) × (0.5 + random()/2)`, base 100-250 ms, cap 5-10 s, 2-3 attempts. Without jitter every client retries in lockstep and re-creates the outage it is recovering from.
- Total budget: `attempts × per_try_timeout` must stay under the inbound `requestTimeout`, or you time out your own caller while still retrying.
- Add a circuit breaker when a dependency's failure rate is sustained: retries against a dead upstream multiply load exactly when it can least take it.

## Bodies, Streaming, and Limits

- Cap request body size at the edge and in the app; without a limit, one client streaming an endless body is a memory exhaustion attack.
- Large responses stream: `pipeline(fileStream, res)` respects backpressure and cleans up on client disconnect (→ `streams.md`). Buffering a 200 MB export into a string can exceed V8's string cap (`ERR_STRING_TOO_LONG`) before it ever reaches the socket.
- Client disconnect mid-response is normal, not an error to alert on: it surfaces as `ECONNRESET`/`ERR_STREAM_PREMATURE_CLOSE` on the response stream. Abort the underlying work (`res.on('close')` → cancel the query) or you keep paying for output nobody will read.
- `Content-Length` and a stream do not mix unless you know the length; let Node use chunked encoding rather than lying about the size.

## DNS and Connection Setup

- `dns.lookup` (used by `http`, `net`, `fetch`) calls the system resolver on the libuv threadpool — 4 slots by default (SKILL.md rule 3), so a slow resolver serializes connection setup across the whole process. `dns.resolve*` uses async c-ares and does not consume the pool.
- Node >=17 returns DNS results in resolver order (no IPv4-first reordering), so a host with a broken IPv6 path can hang or refuse until the fallback. Happy-eyeballs (`autoSelectFamily`, default on from node >=20) fixes it; on older majors, pin `family: 4`.
- A DNS cache is not built in: long-lived processes re-resolve per connection, and pooled keep-alive connections never re-resolve at all — which is why a failover that changed DNS does not reach a Node service until the sockets recycle. Set a max socket lifetime for hosts behind failover.

## Headers, Proxies, and Client IP

- Behind a proxy, the socket address is the proxy. Trust `X-Forwarded-For` only from known proxy IPs and read the correct position in the list — trusting the whole header lets any client forge its own IP for rate limiting and audit logs.
- HTTP header names are case-insensitive and arrive lowercased in `req.headers`; comparing against `'Content-Type'` silently misses.
- Duplicate headers arrive as an array for some names and a joined string for others. `req.headers.set-cookie` is always an array; treat everything else as "string or array".
- Reflecting user input into a header value invites response splitting; Node rejects CR/LF in header values, so the failure surfaces as `ERR_INVALID_CHAR` rather than a silent injection — handle it, do not strip and continue.

## Long-Lived Connections (WebSocket and SSE)

- An upgraded WebSocket leaves the HTTP timeout regime entirely: `requestTimeout` and `keepAliveTimeout` no longer apply, so a peer that vanishes without a FIN can hold the socket until the OS gives up — minutes, or never. Your own ping/pong heartbeat is the only reliable liveness signal; terminate a connection that misses two consecutive pongs.
- Set the heartbeat below the proxy's idle timeout, not near it: `ping_interval ≈ proxy_idle ÷ 2` (60 s idle → 30 s pings), or the proxy closes connections it considers idle and the client sees random disconnects.
- `send()` buffers without bound when the peer reads slowly. Check the socket's buffered amount before sending and drop or disconnect the slow consumer — otherwise one stalled client grows the process's memory for as long as it stays connected.
- Every connection costs a descriptor and a per-connection buffer: 10k concurrent sockets needs the descriptor limit raised deliberately and a memory budget per connection (SKILL.md rule 4, → `filesystem.md`).
- Connection state lives in one process. Across replicas or cluster workers, subscriptions and presence need an external pub/sub bus, and the handshake needs sticky routing (→ `concurrency.md`).
- Server-Sent Events are simpler — an HTTP response held open — but need three things: a `requestTimeout` exemption for that route, a flush per event, and response buffering disabled at the proxy, or events arrive in bursts when the buffer fills. Clients reconnect on their own and resume with `Last-Event-ID`, so the server must be able to replay from an id.
- Shutdown must close these explicitly: they are exactly the connections that never end on their own, and they will hold the process open until the backstop timer fires (→ `errors.md`).

## Graceful Restart Under Traffic

1. Fail the readiness probe first, so the balancer stops sending new requests.
2. `server.close()` — stops accepting, keeps in-flight requests.
3. Close idle keep-alive sockets (`server.closeIdleConnections()`, node >=18.2); otherwise a pooled client holds the process open for the full keep-alive window.
4. Drain, close pools, exit with the backstop timer from SKILL.md's Timeout Ladder. Full sequence: `errors.md`.
