# Types — Deriving Everything From the Schema

Prisma's value is that the schema is the single source of truth for types. Every hand-written interface describing a query result is a copy that will drift, silently, on the next migration.

## Contents

- Derive, never declare
- Runtime types that are not JavaScript primitives
- Three kinds of null
- tsconfig that makes Prisma's types work
- Typed raw queries
- Common type errors and what they actually mean
- The boundary generated types do not cover

## Derive, Never Declare

```ts
import { Prisma } from '@prisma/client'

// The exact shape of a query with relations
type PostWithAuthor = Prisma.PostGetPayload<{
  include: { author: { select: { id: true; name: true } } }
}>

// Reusable query fragment + its type, defined once
const postDetail = Prisma.validator<Prisma.PostDefaultArgs>()({
  include: { author: true, comments: { take: 5 } },
})
type PostDetail = Prisma.PostGetPayload<typeof postDetail>
const post = await prisma.post.findFirst(postDetail)     // arg and type cannot diverge

// The return type of a function that queries
type Loaded = Prisma.PromiseReturnType<typeof loadDashboard>
```

| Need | Generated type |
|---|---|
| Result of a query with `select`/`include` | `Prisma.<Model>GetPayload<T>` |
| Input to `create` | `Prisma.<Model>CreateInput` (`UncheckedCreateInput` when you set FK scalars directly) |
| Input to `update` | `Prisma.<Model>UpdateInput` |
| A `where` object passed around | `Prisma.<Model>WhereInput`, or `WhereUniqueInput` |
| An `orderBy` from an API layer | `Prisma.<Model>OrderByWithRelationInput` |
| Args or result of any operation | `Prisma.Args<typeof prisma.post, 'findMany'>`, `Prisma.Result<...>` |
| Enum values | `$Enums.Role` (also exported top-level as `Role`) |

The plain model type (`import type { Post }`) contains scalars only — no relations, no computed fields. Using it as the return type of a function that returns `include`d data compiles and throws away the relations from the type.

## Runtime Types That Are Not JavaScript Primitives

| Column | Arrives as | Consequence |
|---|---|---|
| `Decimal` | `Prisma.Decimal` (decimal.js) | `+`, `===` and `toFixed` on it do not do what they look like: use `.plus()`, `.equals()`, `.toFixed(2)`. `.toNumber()` re-introduces the float error you avoided |
| `BigInt` | JS `BigInt` | `JSON.stringify` throws; arithmetic with a `number` throws |
| `DateTime` | `Date` | Always UTC from the database; formatting in a local zone is the application's job |
| `Json` | `Prisma.JsonValue` | No structure: cast at the boundary, and validate if it came from outside |
| `Bytes` | `Buffer` (`prisma <6`) / `Uint8Array` (`prisma >=6`) | An upgrade break for anything calling Buffer-only methods |

Serialization, once, at the edge — not scattered through handlers:

```ts
// Global, in one bootstrap file
;(BigInt.prototype as any).toJSON = function () { return this.toString() }

// Or map explicitly where the response is built
const dto = { ...order, total: order.total.toFixed(2), views: Number(order.views) }
```

Choose one and enforce it; two serialization conventions in one codebase produce a field that is a string in one endpoint and a number in another.

## Three Kinds of Null

```ts
data: { meta: Prisma.JsonNull }   // JSON null stored inside the column
data: { meta: Prisma.DbNull }     // SQL NULL — the column has no value
where: { meta: Prisma.AnyNull }   // match either, when filtering
```

Passing plain `null` to a nullable `Json` field is ambiguous and Prisma rejects it. For every other column type, `null` means SQL NULL and `undefined` means "field absent" — which in a `where` means the filter disappears (`SKILL.md` rule 6).

## tsconfig That Makes Prisma's Types Work

- `strict: true` is a hard requirement — without `strictNullChecks`, every nullable column silently becomes non-null and the type system stops helping at exactly the place it was needed.
- `exactOptionalPropertyTypes: true` surfaces the `undefined`-in-`where` hazard at compile time for objects you build explicitly. It also makes optional-property code noisier; adopt it deliberately.
- Turn on `no-floating-promises` in the linter. A missing `await` on a Prisma call is a type-correct no-op, and it is the one bug the compiler cannot show you.
- Path resolution: if the generator has a custom `output`, the client is imported from that path, not `@prisma/client`. Mixing both imports in one codebase gives you two copies of every type and error messages that compare a type to itself.

## Typed Raw Queries

`$queryRaw<T[]>` is an assertion — nothing verifies it. TypedSQL (`prisma >=5.19`) generates the types from the SQL itself and is the version to prefer for anything shipped (→ `raw-sql.md`).

## Common Type Errors and What They Actually Mean

| Error | Cause |
|---|---|
| "Property 'author' does not exist on type 'Post'" | The plain model type is being used for an `include`d result — switch to `GetPayload` |
| "Type 'string \| undefined' is not assignable to 'string'" in a `where` | The exact hazard from rule 6: validate the value before the query |
| "Object literal may only specify known properties" on `select` | Client generated from an older schema (`SKILL.md` rule 2) |
| "Excessively deep and possibly infinite" | A deeply chained `$extends` or a very wide recursive include — extract the fragment with `Prisma.validator` and name its type |
| Types resolve to `any` after `$extends` | Importing the base client somewhere; export and use `type Db = typeof db` (→ `extensions.md`) |
| Types differ between editor and CI | Two generated clients: check the `output` path and whether CI ran `prisma generate` (→ `deployment.md`) |

## The Boundary Generated Types Do Not Cover

Prisma types describe the database, not the request. Data arriving from HTTP is `unknown` until something validates it at runtime:

```ts
const body = CreateUser.parse(req.body)            // runtime validation (Zod, Valibot, ...)
await prisma.user.create({ data: body })           // now the generated type is meaningful
```

Generating validators from the schema is a legitimate shortcut for internal tools, and a trap for public APIs: the database shape and the API contract change for different reasons and should be free to diverge.
