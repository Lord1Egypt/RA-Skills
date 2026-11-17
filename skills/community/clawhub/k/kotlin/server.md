# Server-Side Kotlin — Spring, Ktor, JPA, And Thread-Bound Context

Server frameworks were built for Java's defaults: open classes, no-arg constructors, thread-local context. Kotlin's defaults are the opposite of all three, and the resulting bugs are quiet — a lost transaction, an empty log field, a pool that deadlocks under load.

## Symptom → Cause

| Symptom | Cause | Fix |
|---|---|---|
| "No default constructor for entity" | Kotlin classes have no no-arg constructor | `kotlin-jpa` (no-arg) compiler plugin |
| Proxy/`@Transactional`/`@Configuration` silently not applied | Kotlin classes are final; the framework cannot subclass them | `kotlin-spring` (all-open) compiler plugin |
| Entity behaves oddly in a `Set`, or updates the wrong row | `data class` `equals`/`hashCode` over mutable fields and a post-persist id | Regular class, id-based `equals`, `hashCode` a constant or the natural key |
| MDC/trace id empty in logs after a suspension | Thread-local context does not follow a coroutine across dispatchers | `MDCContext` / a `ThreadContextElement` in the coroutine context |
| Transaction lost after `withContext` | The transaction is bound to the original thread | Keep the transactional work on one context; do not switch dispatchers inside it |
| Under load: everything waits, CPU idle | More coroutines than connections in the pool, on 64 IO threads | `Dispatchers.IO.limitedParallelism(poolSize)` (SKILL.md rule 7) |
| Request keeps processing after the client disconnects | Work escaped the request scope | Structured concurrency inside the handler; no detached scopes |
| Startup fails: "Could not autowire" with a nullable property | Field injection plus `lateinit` hiding a real missing bean | Constructor injection, so the failure names the parameter |
| `@ConfigurationProperties` values all null | Missing no-arg/setter path for a `class` with `var` | Constructor binding with a `data class` and `@ConstructorBinding` where the version requires it |

## Spring With Kotlin

- Two compiler plugins are effectively mandatory: `kotlin-spring` (opens `@Component`, `@Configuration`, `@Transactional` classes) and `kotlin-jpa` (adds the no-arg constructor for `@Entity`). Without them everything compiles and half the annotations do nothing.
- Constructor injection with `val` properties is the idiomatic form: immutable, testable, and the failure happens at construction with the parameter named.
- Configuration as an immutable `data class` bound at startup beats `@Value` scattered through the code — one place to see every setting and one failure point when one is missing.
- Bean definition DSL (`beans { bean<Service>() }`) is the Kotlin-native alternative to component scanning: explicit, reflection-free, faster to start.
- `suspend` controller functions are supported in Spring MVC and WebFlux. Mixing a blocking JDBC call inside a suspend handler without moving it off the event loop is the classic WebFlux performance bug.
- Testing: `@SpringBootTest` for the wiring, plain unit tests for the logic. A test that boots the context to assert a branch is a slow unit test.

## JPA And Persistence

- Do not model an entity as a `data class`. Generated `equals`/`hashCode` read every constructor property, which triggers lazy loading, breaks against Hibernate proxies, and changes once the id is assigned on persist — an entity added to a `HashSet` before saving becomes unreachable after.
- The standard shape: a regular class, `id` nullable until persisted, `equals` comparing ids when both are non-null, `hashCode` a class-level constant.
- Lazy associations are proxies: touching one outside a transaction throws `LazyInitializationException`. Fetch what the caller needs in the query, do not open a transaction around the view layer.
- Nullability: a `var name: String` on an entity claims non-null but the ORM writes it by reflection — align the Kotlin type with the column's nullability or the invariant is fiction.
- Alternatives worth naming: Exposed and jOOQ for SQL-first Kotlin, SQLDelight for compile-time-checked SQL, R2DBC for real non-blocking access. Blocking JDBC inside coroutines is fine when bounded (below); pretending it is non-blocking is not.
- Blocking calls in a coroutine handler: `withContext(Dispatchers.IO.limitedParallelism(pool.maxSize)) { … }`. Matching the slice to the pool means excess load waits as cheap suspended coroutines rather than as blocked threads.

## Ktor

- Handlers are `suspend` by default and run in the call's coroutine: when the client disconnects, structured concurrency cancels the work — provided nothing was launched in a detached scope.
- Plugins (`install(ContentNegotiation) { json(json) }`, `StatusPages`, `CallLogging`, `Authentication`) are the composition model; the same configured `Json` instance should be shared with the rest of the app.
- `StatusPages` is the single place to map domain failures to HTTP status codes — a `when` over the sealed error hierarchy, so a new error variant is a compile error instead of a 500.
- Routing is code, not annotations: extract route groups into extension functions on `Route` to keep a large API navigable.
- The Ktor client belongs to the app lifecycle: create one, close it on shutdown. One client per request exhausts sockets.
- Testing with `testApplication { }` runs the whole pipeline in-process with no port binding, which makes route tests fast enough to keep.

## Context Propagation

- Coroutine context is inherited by children; a `ThreadLocal` is not. Anything thread-bound — MDC, tracing spans, security context, transaction handles — needs an explicit `ThreadContextElement` (the `MDCContext` from `kotlinx-coroutines-slf4j` is the ready-made one).
- The failure mode is silent: logs lose their correlation id after the first `withContext`, traces break into disconnected spans, and the security context reads as anonymous.
- Add the element once, at the scope where the request context is created, so every child inherits it.
- Coroutine names (`CoroutineName("import-job")`) show up in debug output and thread dumps — cheap, and worth it in a service with many concurrent jobs.

## Concurrency And Resource Limits

- A coroutine is not a permit. Rate limits, connection pools and downstream quotas need an explicit `Semaphore` or a `limitedParallelism` slice; without one, elasticity in the coroutine layer just moves the queue to the resource.
- Timeouts belong at every network boundary: the client's own timeout *and* a `withTimeout` around the call, because a client timeout that the library ignores leaves the coroutine hanging.
- Graceful shutdown: cancel application scopes, `join` the in-flight work with a bounded timeout, then close clients and pools. A `runBlocking` in a shutdown hook without a timeout turns a deploy into an outage.
- Long-running background jobs get their own supervised scope with a name and a cancellation path, never `GlobalScope` (SKILL.md rule 3).
- Virtual threads (JDK 21+) and coroutines solve the same blocking problem differently; mixing them is legal but the reasoning about pools changes — pick one model per service and write down which.

## Review Checklist

- `kotlin-spring` and `kotlin-jpa` applied wherever the framework subclasses or instantiates your classes.
- No `data class` entities; entity equality is id-based.
- Every blocking call inside a dispatcher slice sized to its pool.
- Request-scoped context carried by a `ThreadContextElement`, not assumed.
- Every outbound call has a timeout, and every domain failure has an HTTP mapping in one place.
- Shutdown cancels scopes and closes clients with a bounded wait.
