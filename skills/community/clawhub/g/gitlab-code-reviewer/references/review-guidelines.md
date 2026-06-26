# Code Review Guidelines

## Table of Contents

1. [Review Principles](#1-review-principles)
2. [Java & Spring Boot](#2-java--spring-boot)
3. [MongoDB](#3-mongodb)
4. [PostgreSQL](#4-postgresql)
5. [React & TypeScript](#5-react--typescript)
6. [Cross-Cutting: Clean Code & SOLID](#6-cross-cutting-clean-code--solid)
7. [Severity Classification](#7-severity-classification)
8. [Comment Format](#8-comment-format)

---

## 1. Review Principles

- Analyze only the modified lines in the diff. Do not comment on code outside the diff.
- Be concrete: reference exact line numbers, method names, class names.
- Propose a fix whenever a defect is identified. Prefer code snippets over prose.
- No generic praise ("looks good", "nice work"). Every comment must carry signal.
- Group findings by severity before publishing.

---

## 2. Java & Spring Boot

### 2.1 Clean Code

- Methods longer than ~20 lines are a signal to extract responsibilities.
- Avoid boolean flag parameters; prefer method overloads or a strategy.
- Return early (guard clauses) instead of deep nesting.
- Do not expose implementation types in public APIs (return `List<T>` not `ArrayList<T>`).
- Checked exceptions should not leak across layer boundaries; wrap in domain exceptions.

### 2.2 Spring-Specific

- `@Autowired` on fields is discouraged; prefer constructor injection.
- `@Transactional` must be applied at the service layer, not the repository layer.
- `@Transactional(readOnly = true)` for all read-only operations.
- Avoid `@Transactional` on `private` methods — Spring AOP proxies cannot intercept them.
- Do not call a `@Transactional` method from within the same bean (self-invocation bypasses proxy).
- `@Async` methods must be `public` and called from a different bean.
- `@Value` injection: validate at startup with `@PostConstruct` or use `@ConfigurationProperties`.
- REST controllers must not contain business logic; delegate to a service.
- Use `ResponseEntity<T>` for explicit HTTP status control; avoid `@ResponseStatus` on controllers where dynamic status is needed.
- Avoid `@SuppressWarnings("unchecked")` without a comment explaining why it is safe.

### 2.3 Exception & Error Handling

- Every caught exception must either be rethrown (wrapped) or logged with context. Never silently swallow.
- Do not log and rethrow the same exception — leads to duplicate stack traces.
- Use `Optional<T>` return types for lookups; do not return `null` from public methods.

### 2.4 Concurrency

- Shared mutable state in `@Service`/`@Component` (singleton scope) must be thread-safe.
- `HashMap` is not thread-safe; use `ConcurrentHashMap` or synchronize explicitly.
- `@Scheduled` tasks run in a single thread by default; confirm no shared state mutations.

### 2.5 Performance

- Avoid loading collections into memory for counting — use `COUNT` queries.
- Prefer `Pageable` for large result sets; never do `findAll()` on unbounded collections.
- Avoid N+1: use join fetch or `@BatchSize`; check generated SQL in logs during review.
- `Lazy` vs `Eager` fetch types: `EAGER` on collections is almost always wrong.
- Avoid `Optional.get()` without `isPresent()` check.

---

## 3. MongoDB

### 3.1 Query Correctness

- Filter fields used in queries must be indexed. Flag missing index definitions.
- Avoid `find({})` (full collection scan) in production code paths.
- Use projection to limit returned fields when only a subset is needed.
- `$where` and JavaScript operators are slow and disable index use — flag as critical.

### 3.2 Document Design

- Embedding vs referencing: large, unbounded arrays embedded in documents cause document growth and slow reads — flag as major.
- Avoid deeply nested documents (>3 levels) in mutable data.
- Field names should be short but meaningful (MongoDB stores field names per document).

### 3.3 Atomicity & Transactions

- MongoDB multi-document transactions are available since 4.0 but have overhead. Flag unnecessary use.
- Single-document operations are atomic; multi-step operations across documents require explicit transactions or idempotent design.
- `findAndModify` / `findOneAndUpdate` for compare-and-swap patterns (avoids lost-update).

### 3.4 Index Guidelines

- Compound index field order: equality fields first, range fields last, sort fields last.
- `{ a: 1, b: 1 }` does NOT cover a query on `{ b: 1 }` alone.
- `$text` index required for full-text search; regular index cannot substitute.
- TTL indexes for expiring documents (session, temp data) — verify `expireAfterSeconds`.

---

## 4. PostgreSQL

### 4.1 SQL Correctness

- `SELECT *` in production queries is a defect: fragile, may return excessive data.
- `WHERE` clauses without index-backed columns on large tables are a performance defect.
- Implicit type casts in `WHERE` (e.g., `int_col = '123'`) can prevent index use — flag.
- `ILIKE` and `LIKE '%pattern'` are non-sargable; flag when used on large tables.
- `NULL` comparison: `col = NULL` is always false; must use `IS NULL` / `IS NOT NULL`.

### 4.2 Transactions & Isolation

- Default isolation is `READ COMMITTED` in PostgreSQL. Flag code that assumes `SERIALIZABLE` without setting it.
- Long-running transactions hold locks; flag queries inside transactions that do non-DB work (HTTP calls, file I/O).
- Deadlock risk: flag when two code paths acquire multiple locks in different orders.
- Use `SELECT ... FOR UPDATE` / `FOR SHARE` explicitly when locking rows; do not rely on implicit locking.

### 4.3 Schema & Migrations

- `NOT NULL` constraints must have defaults or be added in two steps on live tables (add nullable, backfill, add constraint).
- Adding an index `CONCURRENTLY` to avoid table lock on large tables — flag missing `CONCURRENTLY`.
- Foreign key constraints without matching index on the referencing column cause slow deletes on the referenced table.
- `ON DELETE CASCADE` must be intentional; flag undocumented cascade chains.

### 4.4 Performance

- N+1 in JPA/Hibernate: check `@OneToMany` without `JOIN FETCH` or batch fetching.
- Avoid `COUNT(*)` inside loops; aggregate at the DB level.
- `EXPLAIN ANALYZE` is the ground truth; flag queries likely to cause sequential scans on large tables.
- Connection pool sizing: `HikariCP` default is 10 connections — flag if pool config is absent in high-concurrency services.

---

## 5. React & TypeScript

### 5.1 TypeScript Correctness

- `any` type disables type checking — flag every occurrence; suggest concrete type or `unknown`.
- Non-null assertion (`!`) is a type-system lie; flag when not obviously safe.
- Avoid `as T` casts unless a type guard is in place.
- Prefer `interface` for object shapes that may be extended; `type` for unions/intersections.
- Enums generate runtime code; prefer `const` enums or union string literals for pure type safety.

### 5.2 React Correctness

- `useEffect` with missing dependencies is a bug; the exhaustive-deps ESLint rule is authoritative.
- Stale closure: variables captured in callbacks or effects must be in the dependency array.
- Avoid setting state inside `useEffect` without a termination condition (infinite loop risk).
- Keys in lists must be stable and unique — do not use array index as key when list can reorder.
- Avoid inline object/array literals in JSX props that trigger reference inequality on each render.

### 5.3 Performance

- `useMemo` and `useCallback` are optimizations, not correctness tools; flag misuse (wrapping cheap computations).
- Large components that re-render on every parent update: suggest `React.memo`.
- Avoid fetching data directly in render; use effects or data-fetching libraries.
- Dynamic imports (`React.lazy`) for code-splitting heavy pages.

### 5.4 State Management

- Derived state (computed from existing state) must not be stored in a separate state variable — recalculate in render.
- `useState` initializer function form (`useState(() => expensiveInit())`) to avoid re-running on each render.
- Prefer lifting state to the lowest common ancestor rather than global state for local UI concerns.

### 5.5 Security

- `dangerouslySetInnerHTML` is a XSS vector — flag every occurrence; require justification and sanitization.
- User-controlled data must not be used directly in `href` without scheme validation (javascript: URLs).
- Avoid `eval`, `new Function`, and `setTimeout(string)`.

---

## 6. Cross-Cutting: Clean Code & SOLID

### Single Responsibility

- A class or function should have one reason to change.
- Flag God classes (>300 lines, >10 public methods with unrelated concerns).
- Flag methods that do orchestration AND business logic AND I/O simultaneously.

### Open/Closed

- Business rules hard-coded with `if/switch` chains on type discriminators are an OCP violation — suggest strategy/polymorphism.

### Liskov Substitution

- Overriding methods that throw `UnsupportedOperationException` violates LSP.
- Subclasses that narrow input contracts (throw on valid base-class inputs) violate LSP.

### Interface Segregation

- Fat interfaces (>7 methods) force implementors to provide no-op stubs — flag, suggest splitting.

### Dependency Inversion

- High-level modules must depend on abstractions, not concrete classes.
- Direct instantiation of services/repositories inside business logic with `new` — flag.

### DDD Alignment

- Domain entities must not contain infrastructure concerns (no `@Entity` annotations inside a clean domain module if ports/adapters are in use).
- Anemic domain model: entities that are only data containers with all logic in services — flag if architectural style is DDD.
- Aggregate boundaries: operations that span multiple aggregates in one transaction are a DDD smell.
- Value objects must be immutable.
- Domain events must be raised by aggregates, not services.

---

## 7. Severity Classification

| Severity | Criteria |
|----------|----------|
| **Critical** | Data loss, security vulnerability, incorrect transaction boundary, race condition, NPE in hot path, broken API contract |
| **Major** | N+1 query, missing index on queried field, OCP/LSP violation, stale closure, missing null check, wrong isolation level, `any` type in API boundary |
| **Minor** | Naming, unnecessary complexity, missing early return, unused import, inconsistent style within the PR |

---

## 8. Comment Format

Each inline GitLab comment must follow this structure:

```
[SEVERITY] <One-line issue description>

<Explanation limited to the diff context. 2-4 sentences max.>

Suggestion:
```<language>
<corrected code snippet>
```
```

Example:

```
[MAJOR] N+1 query risk in UserService.findByOrganization

Each iteration calls `roleRepository.findByUserId(user.getId())` inside a loop.
This produces one SQL query per user. Use a single batch query with `IN` clause
or add `@BatchSize` on the association.

Suggestion:
```java
List<Long> userIds = users.stream().map(User::getId).toList();
Map<Long, List<Role>> rolesByUser = roleRepository.findByUserIdIn(userIds)
    .stream().collect(Collectors.groupingBy(Role::getUserId));
```
```

Omit the Suggestion block only when no concrete fix can be derived from the diff alone.
