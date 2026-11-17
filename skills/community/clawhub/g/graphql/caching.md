# Caching — HTTP, CDN, Persisted Queries, And The Entity Layer

GraphQL gave up the free cache. One URL, one verb, a body that varies per client: every layer that cached REST for you by default now caches nothing. This file is how to get each layer back deliberately. The client-side normalized cache is a different mechanism and lives in `client.md`.

Contents: The Five Layers · Why HTTP Caching Broke · GET And Persisted Queries · APQ Versus Trusted Documents · Cache Hints · Entity Cache · Invalidation · Private Data · Stampedes · Traps

## The Five Layers

| Layer | Keyed by | Wins | Invalidated by |
|---|---|---|---|
| CDN / HTTP | URL (query hash + variables) | Public, repeated, identical documents | TTL, purge by key |
| Whole-response cache in the server | Document + variables + viewer scope | Repeated identical requests | TTL, or the shortest field hint |
| Entity / object cache (Redis) | Type + id | Reads shared across many operations | Explicit, on write |
| Per-request loader cache | Type + id, one request | Duplicate ids inside one document | End of request (`n-plus-one.md`) |
| Client normalized cache | `__typename` + id | Repeat views in one session | Mutation payloads, refetch, eviction (`client.md`) |

- Work upward: the entity cache pays off first in most systems, because it is shared across every operation shape. The CDN pays off last and only for public data.
- Two layers caching the same value with different TTLs produce a stale value that outlives the shorter TTL — decide which layer owns each object.

## Why HTTP Caching Broke

- Everything is `POST` to one path: shared caches ignore it, browsers ignore it, `Cache-Control` on the response is irrelevant to a request nobody will match again.
- Responses vary by document *and* variables *and* viewer, so the cache key has to be computed from the body, which is exactly what URL-keyed caches cannot do.
- Partial responses (`data` plus `errors`) are cacheable-looking and often should not be cached at all: caching a response containing an upstream timeout serves that timeout to everyone for the TTL.
- The fix is to make the request cacheable, not to make the cache smarter: a `GET` whose URL contains a stable document hash.

## GET And Persisted Queries

```
GET /graphql?extensions={"persistedQuery":{"version":1,"sha256Hash":"<hash>"}}&variables={"id":"42"}
```

- The document hash plus the variables *are* the cache key, so any ordinary CDN caches the response with no GraphQL awareness at all.
- Only queries may go over `GET`. A mutation over `GET` is triggerable by an image tag (`security.md`).
- URL length is the practical ceiling: hash plus variables must stay under the limits of every proxy in the path (8 KB is a common one). Large variable payloads force you back to `POST`.
- The variables must be serialized deterministically — key order changes the URL and splits the cache. Sort keys before encoding, on every client.
- `POST` with the same hash still works and skips the CDN; keep it as the fallback for long variables and for mutations.

## APQ Versus Trusted Documents

Same wire mechanism, opposite purposes. Confusing them is the common mistake.

| | Automatic persisted queries | Trusted documents |
|---|---|---|
| Registration | At runtime, first time the server sees the document | At build time, from client source |
| Unknown document | Server replies `PersistedQueryNotFound`; client retries with the full text | Rejected |
| Buys | Bandwidth, `GET`-ability, CDN caching | All of that, plus arbitrary queries become impossible |
| Security value | None — any document can register itself | The strongest DoS defense available (`security.md`) |

- The `PersistedQueryNotFound` handshake costs one extra round trip per new document per server instance, then nothing. Seeing it *in a loop* means a mismatch: the client hashes differently than the server (whitespace, a codegen change), or a CDN is caching the negative response, or instances do not share the registry.
- Share the APQ registry across instances (Redis, or preload the manifest at boot). Per-instance in-memory registries make the handshake fire on every deploy and on every scale-out.
- Moving to trusted documents is the same client change plus a manifest published at build time — start with APQ if you must, but know it is a performance feature wearing a security-looking name.

## Cache Hints

- Field-level hints (`@cacheControl(maxAge:, scope:)` in Apollo-family servers, equivalents elsewhere) let the server compute one `Cache-Control` header for the whole response.
- The rule that surprises everyone: the response's overall `maxAge` is the **minimum** across every field selected. One field with `maxAge: 0` makes the entire response uncacheable, no matter how cacheable everything else was.
- Default `maxAge` is typically 0, i.e. nothing is cacheable until you say so. Annotate the cacheable types (reference data, public content) rather than trying to exclude the rest.
- `scope: PRIVATE` marks anything viewer-specific and must propagate into the cache key, or one user's response is served to another. A private field inside an otherwise-public response poisons the whole response.
- Hints belong on *types* where possible (`Country`, `Currency` are cacheable everywhere they appear) and on fields where the value depends on the parent.

## Entity Cache

- Cache by type and id, below the loader: `user:42` in Redis, read by the loader's batch function on a miss, written on load.
- This is the layer that survives across requests and across operation shapes, which is why it beats response caching in a graph where every client sends a different document.
- Serialize the *entity*, not the GraphQL result. Caching a field's resolved output ties the cache to one selection set and one nullability decision.
- Never cache the authorization decision with the entity: cache the row, check the viewer on every read (`authorization.md`).
- Bound it: a maximum entry size and an eviction policy, or one large entity type crowds out everything else.

## Invalidation

- Write-through on mutation is the only invalidation that stays correct without a job: the mutation writes the row and deletes (or updates) `type:id` in the same code path, then clears the request loader (`mutations.md`).
- Cross-entity effects are the hard part: publishing a post invalidates the post, the author's post count, the feed of every follower. Model the dependency explicitly (tag-based invalidation) or accept a TTL on derived values and document the staleness.
- CDN purge by key requires the key: emit a surrogate key per entity id on the response and purge by that key. Without it, purging means purging everything.
- TTL is the fallback, not the design. Pick it from how stale the data may be for the *user*, and write that number where the field is defined.
- After any invalidation strategy is chosen, ask what happens on the write path failing halfway: a committed database write with a failed cache delete serves stale data until the TTL. Deleting the cache entry *before* and *after* the write shrinks the window.

## Private Data

- Anything viewer-specific must never enter a shared cache without the viewer in the key. The catastrophic failure mode in this whole file is a CDN caching a personalized response.
- Simplest safe posture: two endpoints or two paths — one for anonymous, cacheable, public queries; one for authenticated traffic that no shared cache touches. Coarse and very hard to get wrong.
- If you must mix, `Vary` on the authentication header and mark every private field `scope: PRIVATE`; then verify with an actual test that an anonymous request cannot receive an authenticated response.
- Never key a shared cache on a user id supplied by a header a client controls.

## Stampedes

- A popular key expiring under load sends every concurrent request to the origin at once. GraphQL amplifies it: one expired entity can be requested by fifty different operation shapes simultaneously.
- Single-flight per key (one in-flight fill, everyone else awaits it) is the fix that requires no tuning. The per-request loader already does this within a request; the entity cache needs it across requests.
- Stale-while-revalidate serves the expired value while one background fill runs — the right default for reference data where a few seconds of staleness is harmless.
- Add jitter to TTLs. Ten thousand entries cached in the same warmup expire in the same second otherwise.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Expecting CDN caching from `POST` | Shared caches do not cache `POST` | Persisted query over `GET` with a hash in the URL |
| Treating APQ as a security control | Any document registers itself on first sight | Trusted documents from a build-time manifest |
| Per-instance APQ registry | Handshake fires on every deploy and scale-out | Shared registry, or preload the manifest at boot |
| One uncacheable field in a cacheable response | Overall `maxAge` is the minimum across fields | Split the operation, or annotate that field's type |
| Caching a personalized response in a shared cache | One user receives another's data | `scope: PRIVATE`, `Vary`, or a separate anonymous endpoint |
| Caching the authorization result with the entity | Permissions change; the cache does not | Cache the row, check the viewer per read |
| Unsorted variable keys in a `GET` URL | Same query, different URLs, no cache hits | Deterministic serialization on the client |
| TTL as the only invalidation | Users see their own writes disappear | Write-through on mutation, TTL as backstop |
