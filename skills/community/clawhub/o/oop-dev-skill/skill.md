---
name: oop-coding-standards
description: Apply universal object-oriented programming standards derived from battle-tested engineering practices. Use this skill when the user asks to review code quality, enforce coding standards, write production-grade OOP code, design class/module structure, handle exceptions, write unit tests, design database schemas, or structure multi-layer applications. Applies to any OOP language (Python, Java, C#, Go, TypeScript, Kotlin, Ruby, Swift, PHP, etc.) without language-specific lock-in.
license: Derived from Alibaba Java Coding Guidelines (educational use). Original © Alibaba Group.
---

This skill encodes universal engineering standards for object-oriented software. When applied, Claude enforces these rules across **any OOP language** — the principles are language-agnostic unless a specific rule maps naturally to the target language's idioms.

The user may ask for code review, generation, refactoring, architecture design, test writing, or database schema design. Apply whichever sections are relevant.

---

## 1. Naming Conventions

### Hard Rules (enforce always)
- **No leading/trailing underscores or special symbols** in public identifiers. Names like `_name`, `name_`, `$obj` are forbidden.
- **No mixing of local language phonetics with a foreign language** in the same identifier. Use either full English or full native language — never a hybrid like `getUserPingfen()`.
- **Class names**: Use `UpperCamelCase`. Exception: well-known domain abbreviations (e.g. `DTO`, `VO`, `BO`) may retain their canonical form.
  - Good: `UserAccount`, `OrderService`, `XmlParser`
  - Bad: `userAccount`, `XMLparser`, `order_service`
- **Methods, parameters, local variables**: Use `lowerCamelCase`.
  - Good: `getUserById`, `localValue`, `inputUserId`
- **Constants**: All uppercase with underscore separators. Prefer full descriptive names.
  - Good: `MAX_RETRY_COUNT`, `DEFAULT_TIMEOUT_SECONDS`
  - Bad: `MAX`, `TIMEOUT`
- **Abstract classes**: Prefix with `Abstract` or `Base`.
- **Exception classes**: Suffix with `Exception` (e.g. `PaymentException`).
- **Test classes**: Named after the class under test, suffixed with `Test` (e.g. `OrderServiceTest`).
- **Boolean fields in data objects**: Do NOT prefix with `is`. Many serialization frameworks will misread `isDeleted` as field `deleted`, causing runtime failures.
  - Good: `deleted`, `active`, `enabled`
  - Bad: `isDeleted`, `isActive`
- **Packages/modules**: All lowercase, single semantic word per segment, singular form.
- **No opaque abbreviations**: `condi` for `condition`, `abs` for `abstract` — forbidden. Names must be self-explanatory.

### Recommended
- **Encode design patterns in names** when applicable: `OrderFactory`, `LoginProxy`, `ResourceObserver`.
- **Interface capability names**: Use adjective form where natural (e.g. `Translatable`, `Serializable`, `Configurable`).
- **Service/DAO implementation classes**: Suffix with `Impl` to distinguish from the interface (e.g. `UserServiceImpl implements UserService`).
- **Enums**: Suffix with `Enum`; members are all-uppercase with underscores (e.g. `OrderStatusEnum.PENDING_PAYMENT`).

### Layer Naming Conventions
| Layer | Method prefix convention |
|---|---|
| DAO/Repository | `get` (single), `list` (multiple), `count`, `save`/`insert`, `remove`/`delete`, `update` |
| Domain models | `XxxDO` (data object), `XxxDTO` (transfer), `XxxVO` (view), `XxxBO` (business) |

---

## 2. Constants and Magic Values

- **No magic values** — never embed unexplained literals directly in logic.
  - Bad: `cache.put("Id#order_" + orderId, value)`
  - Good: define `ORDER_CACHE_KEY_PREFIX = "Id#order_"` as a named constant
- **Long/integer literals**: Use uppercase suffix where the language requires it (e.g. `2L` not `2l`; `2.0f` not `2.0F` ambiguously).
- **Split constants by concern** — do not create one monolithic `Constants` class. Group into `CacheConstants`, `SecurityConstants`, `ConfigConstants`, etc.
- **Constant scoping levels** (from broadest to narrowest): cross-application shared → application-wide → module-level → package-level → class-private.
- **Use enums for named value sets** — especially when values carry semantic meaning beyond their raw type (e.g. days of week, order statuses).

---

## 3. Code Formatting

- **Brace style**: Opening brace on the same line as the statement; closing brace on its own line. Empty bodies may be written as `{}` inline.
- **Indentation**: 4 spaces. Never use tabs (or configure tabs as 4 spaces if the language convention mandates them).
- **Spaces around operators**: All binary and ternary operators must have one space on each side (`=`, `&&`, `+`, etc.).
- **No space** between a function/method name and its opening parenthesis. No space after `(` or before `)`.
- **Reserved words** (`if`, `for`, `while`, `switch`) require a space before the opening parenthesis.
- **Line length limit**: 120 characters. When wrapping:
  - Indent the second line by 4 spaces; subsequent continuation lines stay at the same indent as line 2.
  - Break *after* commas; break *before* method-chaining dots.
  - Never break immediately before an opening parenthesis.
- **Comment spacing**: One space between the comment marker and content (`// comment`, `# comment`).
- **File encoding**: UTF-8. Line endings: Unix (`LF`).
- **Blank lines**: One blank line between logically distinct blocks within a method. No need for multiple blank lines as separators.

---

## 4. OOP Principles

### Hard Rules
- **Access statics via class name**, not via an instance reference.
- **Always annotate overridden methods** (e.g. `@Override` in Java/Kotlin, explicit `override` keyword in others). This surfaces signature mismatches at compile time.
- **Wrapper/boxed types for data object fields** — primitive defaults can mask missing data (a `0` looks like valid data; `null` clearly signals "not set"). Use primitives only for local variables where performance matters.
- **Data objects (DTOs, POJOs, etc.)**: Do not assign default values to fields at declaration. Defaults hide missing assignments and cause subtle bugs.
- **No business logic in constructors**. Use an explicit `init()` or factory method.
- **All data objects must implement a human-readable string representation** (`__repr__`, `toString`, etc.) for easier debugging.
- **Restrict access as tightly as possible**:
  - Private constructors for utility/singleton classes.
  - Private fields unless subclass sharing is intentional.
  - Private methods unless they form part of an inheritance contract.

### Recommended
- **Validate split() / split-like results** before index access — trailing delimiters yield fewer elements than expected.
- **Group related constructors and overloads together** in the class body.
- **Class member ordering**: public/protected methods → private methods → getters/setters.
- **No logic in getters/setters** — these must be pure accessors.
- **String concatenation inside loops**: Use a mutable buffer (`StringBuilder`, list join, etc.) — never `+=` string in a loop body.
- **Use `final`/`const`/`val` liberally**: for classes not meant to be subclassed, for fields that must not be reassigned, for local variables that should not change.
- **Be cautious with shallow clone/copy** — if your language's default copy is shallow, explicitly implement deep copy when needed.

---

## 5. Collection Handling

- **Always override both equality and hash together** when using objects as map keys or set members.
- **Do not cast sub-list / sub-collection views** to their parent collection type — they are views, not independent copies.
- **Modifying the original collection while a view (subList, etc.) is live** throws a concurrent modification error. Avoid.
- **When converting arrays to resizable collections**, use the proper API that yields a fully mutable collection — not a fixed-size adapter.
- **Do not mutate (add/remove/clear) adapter-backed collections** returned by utilities like `Arrays.asList()` or equivalent — they are fixed-size adapters.
- **Producer/Consumer generics** (where applicable): read-heavy → use upper-bounded type; write-heavy → use lower-bounded type.
- **Never remove/add during a for-each loop** — use an explicit iterator and call `iterator.remove()`.
- **Comparator contracts**: When implementing comparison, handle the equal case explicitly. Comparators that only return `1` or `-1` (never `0`) violate contract and cause sort instability.
- **Pre-size collections** when the final count is known. For hash maps: `capacity = (expected_count / load_factor) + 1`.
- **Iterate maps with entry-set** (key+value in one pass), not key-set (two lookups per entry).
- **Know your collection's null policy**: Some concurrent/sorted implementations reject null keys or values outright. Do not assume HashMap/dict behavior universally.

---

## 6. Concurrency

- **Singleton objects and their methods must be thread-safe**.
- **Name all threads/thread-pools** with meaningful identifiers for traceback in production.
- **Never create raw threads outside a pool**. Always use a managed executor/thread pool.
- **Size your thread pools explicitly** — avoid framework defaults that allow unbounded queues or unbounded thread counts (both cause OOM).
- **Date/time formatters are not thread-safe** in most languages. Do not share a single formatter instance across threads. Use thread-local storage or the language's thread-safe alternatives.
- **Lock granularity**: prefer lock-free structures → fine-grained locks → coarse locks. Minimize code inside locked sections. Never make remote calls inside a lock.
- **Consistent lock ordering** across all code paths to prevent deadlock (if thread A locks X then Y, thread B must never lock Y then X).
- **Concurrent record updates**: use optimistic locking (version field) when conflict probability < 20%; otherwise use pessimistic locking. Retry at least 3 times on optimistic lock failure.
- **Scheduled task runners**: use robust executor implementations that isolate task failures — one failing task must not silently kill sibling tasks.
- **Double-checked locking**: the target field must be declared `volatile` (or equivalent) to prevent CPU/compiler reordering.
- **Atomic counters**: for simple increment/decrement shared counters, use atomic integer types rather than synchronized blocks.
- **Thread-local state**: mark thread-local variables as static; they are per-thread, not per-instance.

---

## 7. Control Flow

- **`switch` statements**: every `case` must either `break`/`return` or have an explicit fall-through comment. Always include a `default` branch, placed last.
- **Always use braces** for `if`/`else`/`for`/`while`/`do` — even single-line bodies.
- **Minimize `if-else` nesting** — prefer early return / guard clauses over deeply nested branches. Max 3 levels of nesting; beyond that, refactor with guard clauses, strategy pattern, or state pattern.
- **Extract complex conditions** into a well-named boolean variable before the `if`. Inline complex boolean expressions hurt readability.
- **Move invariants out of loops**: object creation, DB connection acquisition, and avoidable try-catch blocks should live outside loop bodies.
- **Validate batch API inputs** — enforce upper bounds on input sizes to prevent memory exhaustion.
- **Parameter validation rules**:
  - Validate at: low-frequency methods, expensive operations, high-stability requirements, all public/RPC/HTTP entry points, permission gates.
  - Skip validation at: hot inner-loop methods (document the contract instead), deeply internal private methods with confirmed-safe callers.

---

## 8. Comments and Documentation

- **Class-level, field-level, and method-level documentation** must use the language's structured doc format (docstring, Javadoc, JSDoc, etc.) — not inline `//` comments.
- **All abstract methods / interface methods** require doc comments explaining purpose, parameters, return values, exceptions, and any implementation constraints.
- **Every class must record** its author and creation date.
- **Inline comments** go on the line *above* the code they describe, not at the end of the line.
- **All enum members must have comments** explaining their purpose.
- **Prefer clear native language comments** over broken English — domain terms and keywords stay in English; explanations can be in the team's working language.
- **Keep comments in sync with code** — stale comments are worse than no comments.
- **Do not comment out dead code silently** — either delete it (version control preserves history) or leave a clear explanation above it with `TODO`/`FIXME` markers.
- **Annotation markers**:
  - `TODO(author, date)` — functionality not yet implemented.
  - `FIXME(author, date)` — known broken code needing urgent fix.
- **Comment quality target**: comments should convey *why* and *business meaning*, not restate *what* the code does. Self-explanatory code needs no comment.

---

## 9. Exception Handling

- **Prevent exceptions via pre-checks** where possible — do not use exceptions as flow control.
- **Catch narrow exception types** — avoid blanket `catch(Exception)` except at application boundaries.
- **Never swallow exceptions silently** — either handle them or re-throw. An empty catch block is always wrong.
- **Transaction rollback**: if an exception occurs inside a transaction, explicitly trigger rollback — don't rely on implicit behavior.
- **Always close resources** in `finally` blocks (or use language-level resource management: `with`, `try-with-resources`, `using`, RAII, etc.).
- **Never `return` from a `finally` block** — it silently swallows exceptions from the `try` block.
- **Caught exception type must match or be a parent of** the thrown exception type.
- **NPE / null-safety discipline**:
  - Return values may be null — document when and protect callers.
  - Unbox wrapper types only after null-check.
  - Guard against null from: DB queries, remote calls, session data, chained calls.
  - Prefer optional/maybe types where the language supports them.
- **Error propagation strategy**:
  - HTTP/public APIs: return structured error codes + messages.
  - Internal application logic: throw typed exceptions.
  - Cross-service RPC: return a result wrapper with `isSuccess()`, error code, and error message.
- **DRY principle**: extract repeated validation or error-handling logic into shared private methods or base classes.

---

## 10. Logging

- **Use an abstraction layer** (logging facade/interface) — do not bind directly to a specific logging library. This makes the implementation swappable.
- **Log retention**: keep at least 15 days of logs (weekly-pattern anomalies require this window).
- **Log file naming convention**: `{appName}_{logType}_{description}.log` — e.g. `orderservice_monitor_paymentTimeout.log`.
- **Guard log statements** at `debug`/`trace` level to avoid string interpolation cost when the level is inactive:
  ```
  if logger.is_debug_enabled():
      logger.debug(f"Processing order {order_id}")
  ```
  Or use lazy interpolation syntax provided by the logging framework.
- **Prevent duplicate log propagation** — configure appenders to avoid the same log entry appearing multiple times.
- **Exception log entries must include**: context parameters AND the full stack trace.
- **Production log level discipline**: no `debug` in production; `info` selectively; `warn` for recoverable anomalies; `error` for genuine system faults only.

---

## 11. Unit Testing

### Hard Rules (AIR Principles)
- **Automatic** — tests run fully without human intervention. No `print`/console assertions — use framework assertions only.
- **Independent** — test cases must not call each other or depend on execution order.
- **Repeatable** — tests must produce identical results regardless of environment, time, or external state. Inject or mock all external dependencies (DB, network, filesystem, time).
- **Granularity**: one test = one method or one behavior. Tests do not verify cross-class interaction (that is integration testing).
- **All new code in critical paths must have passing unit tests** before merging.
- **Test code lives in the designated test directory** (e.g. `src/test/`, `tests/`), never in the production source tree.

### Recommended (BCDE Principles)
- **Border** — test boundary values: loop edges, empty collections, max/min values, date boundaries.
- **Correct** — test the happy path with valid inputs and verify expected output.
- **Design** — derive test cases from the design specification, not just from the implementation.
- **Error** — test with invalid inputs, illegal states, and exception paths.

Additional recommendations:
- Code coverage target: 70%+ statement coverage overall; 100% branch + statement coverage for core modules.
- Use programmatic data setup, not manually inserted DB rows — hand-inserted data often violates business rules and makes tests fragile.
- Database-touching tests should auto-rollback or use clearly prefixed test data.
- Refactor untestable code (excessive globals, deep external dependencies, complex constructors) rather than writing workarounds.

---

## 12. Database Design (SQL / Relational)

### Table Structure
- **Boolean/flag fields**: named `is_xxx`, type unsigned tiny integer (0/1). All non-negative numeric fields must be unsigned.
- **Table and column names**: lowercase letters and digits only. No uppercase, no leading digits, no double-underscore-with-digit patterns (e.g. `level_3_name` is bad; `level3_name` is acceptable).
- **Table names**: singular noun (e.g. `user`, `order_item` — not `users`).
- **Reserved words**: never use DB-reserved words as identifiers.
- **Index naming**: `pk_` prefix for primary keys; `uk_` for unique indexes; `idx_` for regular indexes.
- **Decimal precision**: use `DECIMAL`/`NUMERIC` — never `FLOAT`/`DOUBLE` for stored values that require exact comparison.
- **Variable-length strings**: use variable-length type up to a reasonable limit (e.g. 5000 chars). Beyond that, store in a separate text-type column in its own table linked by primary key.
- **Mandatory audit columns on every table**: `id` (unsigned bigint, auto-increment primary key), `gmt_create` (datetime), `gmt_modified` (datetime).
- **Table naming**: `{business_domain}_{entity_role}` (e.g. `payment_task`, `trade_config`).
- **Split tables** only when a single table exceeds 5 million rows or 2 GB — not preemptively.

### Index Design
- **Unique constraints for business-unique fields** — even composite uniqueness should be enforced at DB level, not just application level.
- **No more than 3-table JOINs** in a single query. All joined columns must have matching types and indexes.
- **Partial indexes on long string columns** — index a prefix of sufficient cardinality, not the full column.
- **No left-side or full wildcard pattern matching** in queries intended to use indexes (e.g. `LIKE '%value%'` defeats the index). Route full-text search to a search engine.
- **Composite index column order**: highest-cardinality / equality-condition columns first; range-condition columns last.
- **Covering indexes**: design indexes that satisfy a query's projection without a table lookup.
- **Pagination on large offsets**: use keyset pagination (seek method) or a subquery to locate the ID range before fetching rows.
- **SQL optimization target levels** (best to worst): constant lookup → ref (index) → range → full scan. Avoid full scans.

### SQL Statements
- **Never use `SELECT *`** — always name columns explicitly.
- **`COUNT(*)`** is the standard row count; `COUNT(col)` skips NULLs. Use accordingly.
- **NULL comparisons**: use `IS NULL` / `IS NOT NULL` or the equivalent function — direct equality comparison with NULL always yields NULL, not true/false.
- **Skip the pagination query entirely when the count is 0** — avoid executing the offset query unnecessarily.
- **No database-level foreign key constraints or cascades** in high-concurrency distributed systems — enforce referential integrity in the application layer.
- **No stored procedures** — they are opaque, hard to test, and non-portable.
- **Before any DELETE or UPDATE**: run a SELECT first to verify the target rows, then execute the mutation.
- **`IN` lists**: keep under 1000 elements.
- **Character encoding**: use UTF-8 universally. Use UTF-8 MB4 (or equivalent) when emoji/4-byte characters must be stored.

### ORM Mapping
- **Always define explicit result mappings** — never use dynamic hash maps as query result types.
- **Use parameterized queries exclusively** — string-interpolated SQL is a SQL injection vector.
- **Update only changed fields** — do not emit an update for every field on every save. This avoids errors, reduces load, and keeps audit logs clean.
- **Always update `gmt_modified`** when writing a record.
- **Avoid overly broad update interfaces** that blindly write every field regardless of what changed.

---

## 13. Application Layering

Recommended layer hierarchy (each layer depends only on layers below it):

```
[ Open API / Gateway Layer ]   [ Frontend / Template Layer ]
              ↓
       [ Web / Controller Layer ]
              ↓
       [ Service Layer ]
              ↓
       [ Manager Layer ]
              ↓
       [ DAO / Repository Layer ]
              ↓
       [ Data Source / External APIs ]
```

**Layer responsibilities:**
- **Open API**: Expose service methods as RPC/HTTP; handle auth, rate limiting, input validation.
- **Web/Controller**: Route requests, basic parameter validation, no complex business logic.
- **Service**: Core business logic.
- **Manager**: Cross-cutting concerns — caching, middleware integration, orchestrating multiple DAOs.
- **DAO/Repository**: Data access only. No business logic.

**Exception handling by layer:**
- DAO: catch broadly, wrap in a typed data-access exception, do not log (Service will log).
- Service: catch and log with context. This is the primary error recording boundary.
- Web/Controller: never propagate exceptions upward past the boundary — convert to user-friendly error responses.
- API Gateway: convert all exceptions to structured error code + message responses.

**Domain model types:**
| Type | Meaning |
|---|---|
| DO / Entity | Maps 1:1 to a DB table row |
| DTO | Data transferred between service boundaries |
| BO | Encapsulates business logic output |
| VO | Data shaped for the view/UI layer |
| Query object | Encapsulates query parameters (2+ params → object, not map) |

---

## 14. Dependency and Build Management

- **Version format**: `MAJOR.MINOR.PATCH` — start at `1.0.0`. Major = breaking change; Minor = backward-compatible features; Patch = bug fixes.
- **No SNAPSHOT/pre-release dependencies in production builds**.
- **When adding or upgrading a dependency**, verify that transitive dependency versions have not silently shifted. Audit and lock the full dependency tree.
- **Enums in shared libraries**: safe to use in parameters; do not use as return types across service boundaries (deserialization failures on version skew).
- **Unified version variables** for dependency groups (e.g. all modules of the same framework should reference a single version variable).
- **No duplicate `groupId + artifactId` with different versions** within the same build graph.

---

## 15. Server / Runtime Configuration

- **TCP TIME_WAIT timeout**: reduce from OS default (often 240 s) to ~30 s on high-concurrency servers to avoid connection exhaustion.
- **File descriptor limits**: increase the OS limit well above the default (often 1024) to accommodate concurrent connections.
- **Heap dump on OOM**: configure the runtime to emit a heap dump on out-of-memory events — these are rare and the dump is invaluable for diagnosis.
- **Heap min == heap max**: set initial and maximum heap sizes to the same value in production to eliminate GC-triggered heap resize pauses.
- **Internal redirects**: use server-side forwarding. External redirects must use a URL-building utility — never hand-concatenate redirect URLs.
