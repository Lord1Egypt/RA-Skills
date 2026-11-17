# Subscriptions — Realtime Without A Distributed-Systems Project

A subscription is a long-lived operation that pushes one payload per event. Everything hard about it is state you now hold per connection: transport, fan-out, auth lifetime, and what happens when the socket drops. Decide you need it before you build it.

Contents: Do You Need One · Protocol Confusion · Schema Rules · The Two Halves · Scaling Fan-Out · Filtering · Auth Over Time · Reconnection And Gaps · Backpressure · Serverless · Testing · Traps

## Do You Need One

| Need | Cheapest thing that works |
|---|---|
| A number that refreshes every minute | Polling. One line, no state, no reconnect logic |
| A notification badge | Polling with a long interval, or SSE |
| Live collaboration, chat, trading, presence | Subscriptions or a purpose-built realtime service |
| "The mutation finished" for a long job | Poll the job entity, or subscribe to that one job |
| Cache invalidation across tabs | Client-side broadcast, not the server |

- Polling is not the embarrassing answer. At one request per 30 seconds per user it is cheaper than holding a socket, and it fails safe: a missed poll self-heals on the next one.
- The cost of subscriptions is not the protocol, it is that every server instance now holds state proportional to connected users, and every deploy disconnects all of them.
- Recorded under Platform preferences: transport choice (WebSocket, SSE, polling) changes every example below.

## Protocol Confusion

The single most wasted afternoon in GraphQL:

| Library | WebSocket subprotocol it speaks | Status |
|---|---|---|
| `subscriptions-transport-ws` | `graphql-ws` | Legacy, unmaintained |
| `graphql-ws` | `graphql-transport-ws` | Current |

The names are crossed. A client using the modern library against a server running the legacy one negotiates nothing and the socket closes with no useful error. Check the *subprotocol* on both ends, not the package name.

- Symptom of a mismatch: the connection opens and immediately closes, or hangs after the handshake with no message, and both sides log nothing meaningful.
- Migration path: servers can accept both subprotocols during a transition; run both, watch which one drains to zero, then remove the legacy handler.
- SSE (`graphql-sse`) is the third option: one-directional, plain HTTP, passes through proxies that mangle WebSockets, and reconnects natively with `Last-Event-ID`. For server→client push with no client→server chatter it is the simpler choice.

## Schema Rules

- A subscription operation must have **exactly one root field**. Two root subscription fields in one document is invalid — clients open two subscriptions instead.
- The root field returns the event payload type. Return the *entity*, not a diff: clients then update their normalized cache for free (`client.md`).
- Include enough identity for the client to act: `__typename` and `id` on everything, plus the id of any list the item joined or left.
- Model the event type as a union or with an explicit action enum (`ADDED`, `UPDATED`, `REMOVED`) when the same subscription reports several kinds of change. Inferring "it must be an update" from a payload shape breaks the first time you add a delete.
- Arguments on the subscription field are the *filter*, and they are fixed for the life of the subscription — a client that wants different filters resubscribes.

## The Two Halves

Every subscription resolver has two parts, and conflating them is a common bug:

1. **`subscribe`** — returns an async iterator over the raw events (usually a pub/sub topic). Runs once, at subscription time.
2. **`resolve`** — maps each raw event to the payload the schema promises. Runs per event, with a per-event execution context.

- Publish *identifiers*, not fully-rendered payloads: the publisher sends `{postId}`, and `resolve` loads the current entity. The alternative — publishing a fat payload — races with concurrent writes and ships stale data to some subscribers.
- Loaders are per *message*, not per connection. A loader created in the connection context caches the first event's data for the life of the socket, and subscribers slowly diverge from reality (`n-plus-one.md`).
- Errors thrown in `resolve` produce an error payload for that message; errors thrown in `subscribe` fail the whole subscription. Handle transient failures inside `resolve` so one bad event does not end the stream.

## Scaling Fan-Out

- An in-memory event emitter works on exactly one instance. The moment you run two, a mutation on instance A never reaches a subscriber on instance B — and it works perfectly in development, which is why this ships.
- The standard fix is a shared broker (Redis pub/sub, NATS, a cloud pub/sub service): publishers write to a topic, every instance subscribes and filters for its local subscribers.
- Redis pub/sub is **at-most-once and has no persistence**: a subscriber that is disconnected during the publish never receives it, and there is no replay. That is acceptable for presence and progress bars, and unacceptable for anything the user must not miss (`Reconnection And Gaps`).
- Topic granularity is the tuning knob: one global topic makes every instance filter every event; one topic per entity id makes broker subscription churn dominate. Start per entity *type* plus a coarse key (tenant, channel) and measure.
- Sticky sessions are not required for WebSockets backed by a shared broker — any instance can serve any subscriber. They are required if you kept the in-memory emitter, which is a reason not to.

## Filtering

- Filter server-side, always. Pushing everything and filtering in the client leaks data to anyone with dev tools and multiplies bandwidth by the number of subscribers.
- Filter as early as possible: at the topic (cheapest), then at the instance before execution, then in `resolve` (most expensive, one execution per event per subscriber).
- The filter predicate must re-check authorization on every event, not only at subscribe time (`Auth Over Time`).
- A subscription with a filter that matches almost nothing still costs one predicate evaluation per event per subscriber. Ten thousand idle subscribers on a busy topic is real CPU.

## Auth Over Time

- Authentication happens once at the handshake, in the connection init payload. The connection then lives for hours — a token that expires in fifteen minutes keeps working forever unless you enforce it.
- Store the token expiry on the connection and close the socket when it passes; well-behaved clients reconnect with a fresh token. A re-auth message in the protocol is the alternative if you control both ends.
- Permissions change while the socket stays open: the user leaves the channel, the document is unshared, the role is revoked. Authorize each published event against the current state of the subscriber, not against a decision cached at subscribe time (`authorization.md`).
- Never accept the token as a query parameter in the WebSocket URL: it lands in proxy and access logs. Send it in the connection init payload.
- Check the `Origin` header in the upgrade handler — CORS does not apply to WebSocket handshakes (`security.md`).

## Reconnection And Gaps

- A reconnect does not restore subscriptions: the client must re-send every subscription after the socket comes back. Client libraries usually do it; verify rather than assume.
- Events published during the gap are lost with an at-most-once broker. Every subscription therefore needs a re-sync story: on (re)connect, fetch current state with a query, then apply the live stream on top.
- The idempotency requirement follows: an event delivered twice (once in the re-sync query, once from the stream) must not double-apply. Include a sequence number or a version on the entity so the client can discard what it has already seen.
- Deploys disconnect every client at once. Stagger instance restarts and jitter the client reconnect backoff, or the reconnect storm becomes the outage.
- SSE gives you `Last-Event-ID` for free, which is the cheapest replay mechanism available if your broker can serve from an offset.

## Backpressure

- A slow client (a backgrounded phone, a throttled tab) cannot drain the socket; the server buffers, and memory grows per connection. Bound the per-connection buffer and drop or disconnect when it is exceeded — a dropped subscriber that resyncs beats an out-of-memory that drops all of them.
- Coalesce high-frequency events server-side: for a value changing 100 times a second, publish the latest state at a fixed interval rather than every change. The client cannot render faster than the display anyway.
- Cap concurrent subscriptions per connection and per user; unlimited subscriptions is a resource exhaustion with no HTTP request to rate-limit (`security.md`).
- Always send protocol-level pings: a dead TCP connection with no traffic can persist for a long time, holding a subscription that will never deliver. Missed pongs close the socket.

## Serverless

- Subscriptions need a long-lived process. A request-scoped runtime cannot hold one, so the options are: a separate long-lived subscription service, a managed realtime product that keeps the connections, or not using subscriptions.
- Managed WebSocket gateways (the API-Gateway-style model) invert the design: the platform holds the socket, your function is invoked per message and must store subscription state externally. Workable, and a different architecture from everything above.
- If the rest of the API is serverless and one subscription is needed, polling that one field is usually cheaper than introducing a second runtime (`Do You Need One`).

## Testing

- Test the async iterator directly: publish an event, assert the next iteration yields the mapped payload. That covers `subscribe` and `resolve` without a socket.
- Test the multi-instance case explicitly — two server instances against one broker, subscribe on A, mutate on B. This is the failure that never reproduces locally with one process.
- Test auth expiry and permission revocation mid-stream: subscribe, revoke, publish, assert nothing is delivered.
- Test reconnect: drop the socket, publish during the gap, reconnect, assert the client's re-sync produces correct state with no duplicates (`testing.md`).

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| In-memory event emitter with more than one instance | Subscribers on other instances never receive events | Shared broker, filter locally |
| `graphql-ws` client against a `subscriptions-transport-ws` server | Crossed subprotocol names; the socket closes with no error frame | Match the subprotocol, not the package name |
| Publishing the full payload | Races with concurrent writes; subscribers get stale data | Publish ids, load in `resolve` |
| Loader created in the connection context | Caches the first event's data for the life of the socket | Per-message loaders |
| Auth checked only at handshake | Expired tokens and revoked permissions keep streaming | Enforce expiry, re-authorize per event |
| Token in the WebSocket URL | Lands in every proxy log | Connection init payload |
| Assuming a reconnect restores state | Events during the gap are gone with at-most-once delivery | Re-sync query on connect plus idempotent apply |
| Two root fields in one subscription | Invalid operation | One root field; open two subscriptions |
| No per-connection limits | One client opens thousands of subscriptions | Cap per connection and per user |
