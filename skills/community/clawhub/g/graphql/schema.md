# Schema Design — Types That Survive Their Second Year

A schema is a public contract with no versioning story. Every shape here is chosen for what it costs to change later, not for how it reads on day one.

Contents: Naming · Nullability · Lists · Identity · Input Types · Enums · Custom Scalars · Modelling Money, Time And Files · Interfaces And Unions · Deprecation · Shape Smells

## Naming

- Types `PascalCase`, fields `camelCase`, enum values `SCREAMING_SNAKE_CASE`, arguments `camelCase`. Deviating costs nothing technically and costs every code generator and every reviewer a beat.
- Mutations read `<verb><Entity>`: `createOrder`, `cancelOrder`, `archiveProject`. Never `orderCreate` — the alphabetical grouping people want from that is a tooling problem, not a schema problem.
- One input type per mutation named `<MutationName>Input`, one payload type named `<MutationName>Payload`. Sharing an input between two mutations couples their validation forever (`mutations.md`).
- Field names describe the domain, not the storage: `isPublished`, not `publishedFlag`; `author`, not `authorUserId`. Exposing `userId: ID` beside `user: User` invites clients to fetch both and hand-join.
- Booleans take an `is`/`has`/`can` prefix. A bare `active: Boolean` reads ambiguously in a client conditional a year later.
- Queries are nouns: `user`, `users`, `order`. `getUser` is a REST verb that escaped.

## Nullability

Semantics and propagation live in SKILL.md Null Propagation. This is the design side.

- Default nullable. Non-null is a promise you must keep during an outage, not just during a demo.
- Safe to make non-null: primary keys, `createdAt`, enum discriminators, computed values with no I/O, and fields backed by a `NOT NULL` column in the row you already loaded.
- Keep nullable: anything from another service, anything from a cache that can miss, aggregates, and any field a permission check can deny (`authorization.md`).
- Input and output nullability move in opposite directions for compatibility (full matrix: `schema-evolution.md`). Making an *output* field non-null is safe for existing clients; making an *input* field non-null breaks every caller that omitted it.
- The most common accidental outage: a non-null field served by the default resolver reading a property that is sometimes `undefined`. The field is `String!`, the property is missing, and the parent object disappears from the response.

## Lists

Four shapes, four failure modes:

| Shape | Empty result | One element fails | Whole source fails |
|---|---|---|---|
| `[Post]` | `[]` | that slot `null` | field `null` |
| `[Post!]` | `[]` | whole list `null` | field `null` |
| `[Post]!` | `[]` | that slot `null` | error climbs to parent |
| `[Post!]!` | `[]` | whole list `null`, climbs to parent | error climbs to parent |

- `[Post!]!` is right for a list you own end to end. `[Post]!` is right for a list assembled from a batch loader, where one element can be missing or forbidden without the page being worthless.
- Empty is always `[]`, never `null`. Modelling "no results" as null forces clients into two checks for one condition.
- No unbounded lists. Every list field either takes pagination arguments or is provably bounded by the domain (a user's roles, a country's timezones) — and the bound goes in the field description so nobody has to rediscover it.
- Nested lists (`[[Int]]`) are legal and nearly always a modelling shortcut: introduce the intermediate type so the inner elements can grow fields later.

## Identity

- Every node type carries `id: ID!`. `ID` serializes as a **String**: a numeric database key arrives as `"42"`, and a client comparing it with `42` gets false. Decide once, write it in the description.
- Two schools. Global opaque IDs (base64 of `Type:key`, plus a `node(id: ID!): Node` root field — the Relay contract) buy generic refetch, cache keys that cannot collide across types, and one lookup path; they cost log readability and an encode/decode layer. Type-scoped raw IDs cost none of that and give you none of it.
- Global IDs are not security. Base64 is not encryption; anyone can decode and enumerate. If enumeration matters, use a random key (UUIDv4, ULID) — obfuscating a sequential one buys nothing.
- `node(id:)` is an authorization bypass waiting to happen: it reaches every type in the graph from one entry point, so the permission check belongs in the type's own loader, not in the field that led there (`authorization.md`).
- Expose business keys (`slug`, `sku`) as their own fields with their own root lookups instead of overloading `id` to accept both forms.

## Input Types

- Input objects hold scalars, enums and other input objects only — never output object types. That restriction is what forces the parallel `CreateUserInput`/`User` pair: not redundancy, but the reason input validation can differ from output shape.
- Adding a **required** field to a live input type breaks every existing caller. Add it optional with a server-side default, migrate callers, then consider tightening (`schema-evolution.md`).
- Unset versus explicit null: `updateUser(input: {name: null})` and omitting `name` are different intents and a plain input type cannot distinguish them. Model explicit clears with a dedicated field (`clearAvatar: Boolean`) or a per-field wrapper input, and document which you chose.
- Deeply nested input trees make error paths hard to report against. Flatten to two levels where you can; where you cannot, return errors carrying the input path (`errors.md`).
- Argument defaults declared in the schema (`first: Int = 20`) are visible through introspection; defaults applied inside the resolver are invisible. Prefer the schema default for anything a client should be able to reason about.
- One `filter: XFilterInput` argument beats twelve optional arguments accreted one release at a time — and gives you one place to document how the criteria combine (AND, by default, and say so).

## Enums

- Enums make invalid states unrepresentable for free: status, kind and sort order are enums, not `String`.
- Wire subtlety: enum values are unquoted literals inside a document but quoted strings in JSON variables and responses. Generated clients handle it; hand-rolled ones frequently do not.
- Adding a value is safe in input positions and hazardous in output positions — a client with an exhaustive `switch` receives something it has never seen. The fallback branch belongs in the client, not a `MISC` member in the schema.
- Never model a user-extensible set (tags, customer-created categories) as an enum: every new value becomes a schema deploy.

## Custom Scalars

A custom scalar has three functions, and skipping any of them is the classic hole:

| Function | Direction | Skipping it means |
|---|---|---|
| `serialize` | server → client | Output is whatever the resolver returned, unformatted |
| `parseValue` | variables → server | Variable inputs are unvalidated |
| `parseLiteral` | inline literals → server | Literals written into the document bypass validation entirely |

- Clients see a custom scalar as opaque: code generators map it to `any`/`unknown` until you configure the mapping. Every scalar you add is a typing chore on every client (`codegen.md`).
- Worth defining: `DateTime` (RFC 3339, UTC, offset always present), `URL`, `EmailAddress`, and a `BigInt`/`Decimal` for values outside `Int`.
- `JSON` as a scalar is a hole in the contract — no introspection, no codegen, no field-level deprecation, no validation. Defensible for a genuinely opaque blob you store verbatim; indefensible as a shortcut past modelling.

## Modelling Money, Time And Files

- **Money**: never `Float` — binary floating point cannot represent 0.10 exactly and sums drift. Model `{ amount: String!, currencyCode: CurrencyCode! }`, or minor units in a big-integer scalar with the exponent documented. Currency travels with the amount, always.
- **Int range**: GraphQL `Int` is signed 32-bit, maximum 2147483647. Millisecond epochs, byte counts of large files, and counters on anything popular exceed it and raise a serialization error in production, never in your fixtures.
- **Time**: one `DateTime` scalar, UTC, offset included. Expose the originating timezone as a separate field when it carries meaning (a calendar event's local time). Calendar dates are a *different* scalar — collapsing them into `DateTime` at midnight UTC produces off-by-one-day bugs for every user not on your offset.
- **Durations**: an `Int` of seconds with the unit in the name (`ttlSeconds`) beats a scalar that three teams parse three ways.
- **Files**: model the reference, not the bytes. One mutation issues a presigned upload URL, the client uploads out of band, a second mutation attaches the key (`mutations.md`). Multipart upload through the GraphQL endpoint exists and drags a CSRF surface plus a body parser into the hot path.

## Interfaces And Unions

- Interface = shared fields with shared meaning (`Node`, `Timestamped`, `Actor`). Union = "one of these, no guaranteed common fields" (`SearchResult`, mutation result types).
- Clients must spread a fragment to select anything type-specific: `... on Post { title }`. A selection set containing only `__typename` on a union is legal and returns exactly that — the source of most "my query returns empty objects" reports.
- Always select `__typename` on interfaces and unions: normalized caches need it to key entities, and every generated discriminated union depends on it.
- Adding a member to a union, or a possible type to an interface, is semi-breaking: exhaustive clients hit a branch they do not handle. Announce it like a breaking change even when the checker calls it safe.
- Adding a field to an interface forces every implementing type to add it in the same deploy — across repositories at once in a federated graph (`federation.md`).
- Interfaces implementing interfaces are legal in modern GraphQL and useful for `Node`-plus-domain hierarchies; older client tooling supports them unevenly, so verify your generator before relying on it.

## Deprecation

- `@deprecated(reason: "…")` marks fields, enum values, arguments and input fields. It changes nothing at runtime: the field still resolves, still costs the same, and is still invisible to any client that does not read introspection.
- Deprecating an argument or input field requires it to be optional — you cannot deprecate something callers are forced to send.
- The reason string is the migration instruction and the only place a client author will look. `"Deprecated"` is useless; `"Use publishedAt; same value, always UTC"` is a migration.
- Removal timing and the evidence required: SKILL.md rule 9 and `schema-evolution.md`.

## Shape Smells

| Smell | What it usually means | Better |
|---|---|---|
| `data: JSON` on a domain type | Modelling was deferred and never resumed | Model the fields; keep `JSON` for genuinely opaque blobs |
| One root field per REST resource | The API was transliterated, not designed | Entry points matching how clients start (`viewer`, `node`, search), edges for everything else (`rest-migration.md`) |
| Every field non-null | Types were written from the happy path | SKILL.md rule 2 |
| `success: Boolean` in a payload | The failure model was never designed | Typed user errors or a result union (`errors.md`) |
| A type named `…Data`, `…Info`, `…Object` | The concept has no name yet | Name the concept, or inline its fields into the parent |
| Parallel `user` and `userId` on the same type | Clients are being invited to hand-join | The edge alone; add the raw key only when a client provably needs it without the object |
