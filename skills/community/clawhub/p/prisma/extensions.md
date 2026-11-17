# Client Extensions — Cross-Cutting Behavior Without Middleware

`$use` middleware is deprecated (`prisma >=4.16`) in favor of `$extends`. Extensions are typed, composable, and scoped to a client instance instead of mutating a global one — and they inherit middleware's central limitation: they see the operations you call, not the relation loads Prisma performs inside them.

## Contents

- The four components
- Computed fields
- Model and client methods
- Recipes
- The limits that bite
- Migrating from `$use`

## The Four Components

| Component | Adds | Typical use |
|---|---|---|
| `model` | Methods on one model or `$allModels` | `prisma.user.signUp()`, `paginate()`, domain helpers |
| `client` | Top-level client methods | `prisma.$healthCheck()`, `$withTenant()` |
| `query` | An interceptor around operations | Soft delete, tenant scoping, timing, retries |
| `result` | Computed fields on returned objects | `fullName`, formatted money, derived flags |

```ts
export const db = new PrismaClient().$extends({
  name: 'softDelete',
  query: {
    $allModels: {
      async findMany({ args, query }) {
        args.where = { ...args.where, deletedAt: null }
        return query(args)
      },
    },
  },
})
```

- `$extends` returns a **new** client; the original is untouched. Export the extended one and never the base, or half the codebase silently bypasses the extension.
- Extensions compose by chaining, and they apply in the order they were added: the first `query` extension wraps the second. Order matters when two of them modify `args.where`.
- Name every extension (`name:`) — it shows up in error messages and in the stack you will eventually read at 3am.

## Computed Fields

```ts
const db = prisma.$extends({
  result: {
    user: {
      fullName: {
        needs: { firstName: true, lastName: true },
        compute: (u) => `${u.firstName} ${u.lastName}`,
      },
    },
  },
})
```

- `needs` declares the scalar fields the computation requires; Prisma adds them to the underlying `select` automatically, so a `select: { fullName: true }` still works.
- Computation happens in JavaScript on access — it cannot be filtered or sorted by in the database. A computed field you need in a `where` is a real column or a database view, not an extension.

## Model and Client Methods

```ts
const db = prisma.$extends({
  model: {
    $allModels: {
      async exists<T>(this: T, where: Prisma.Args<T, 'findFirst'>['where']): Promise<boolean> {
        const ctx = Prisma.getExtensionContext(this)
        return (await (ctx as any).count({ where, take: 1 })) > 0
      },
    },
  },
})
```

`Prisma.getExtensionContext(this)` is how a generic model method reaches the model it was called on; `Prisma.Args` and `Prisma.Result` keep the signatures typed against the real schema rather than `any`.

## Recipes

**Tenant scoping** — a client per request, bound to one tenant:

```ts
function forTenant(tenantId: string) {
  return prisma.$extends({
    query: {
      $allModels: {
        async $allOperations({ args, query, operation }) {
          if (operation.startsWith('find') || operation === 'count') {
            args.where = { ...args.where, tenantId }
          }
          if (operation === 'create') args.data = { ...args.data, tenantId }
          return query(args)
        },
      },
    },
  })
}
```

Creating a client per request is cheap only because `$extends` does not open a new pool — it wraps the same one. Verify that on your version before adopting it at scale.

**Audit log** — the change and the record of it in one transaction, so neither can land alone:

```ts
function withAudit(actorId: string) {
  return prisma.$extends({
    model: {
      $allModels: {
        async updateAudited<T>(this: T, args: Prisma.Args<T, 'update'>) {
          const model = (Prisma.getExtensionContext(this) as { $name: string }).$name
          const delegate = model.charAt(0).toLowerCase() + model.slice(1)
          return prisma.$transaction(async (tx) => {
            const result = await (tx as any)[delegate].update(args)
            await tx.auditLog.create({
              data: { model, recordId: String((args as any).where.id), actor: actorId },
            })
            return result
          })
        },
      },
    },
  })
}
```

- A `query` interceptor cannot keep that promise: `query(args)` runs on the client the call arrived on, so a `$transaction` opened inside the interceptor wraps the audit row only and the update commits separately. Intercept `update` this way only when a best-effort trail is acceptable.
- The actor is a factory parameter, like `forTenant` above — an extension has no ambient request context to read a `userId` from.
- `update` returns the row **after** the change. A trail that needs the previous values reads the row inside the same transaction before writing it.
- Prefer database triggers when the audit trail must also cover raw SQL and out-of-band writes — an application-level log is only as complete as the paths that go through it.

**Row-level security** — `SET LOCAL` inside an interactive transaction, so the setting dies with the transaction:

```ts
await prisma.$transaction(async (tx) => {
  await tx.$executeRaw`SELECT set_config('app.tenant_id', ${tenantId}, true)`
  return tx.document.findMany()
})
```

Session-scoped `SET` without `LOCAL` leaks across pooled connections and gives the next request someone else's tenant.

**Timing** — measure per operation without a global log:

```ts
query: { $allModels: { async $allOperations({ operation, model, args, query }) {
  const start = performance.now()
  const result = await query(args)
  metrics.observe(`${model}.${operation}`, performance.now() - start)
  return result
} } }
```

## The Limits That Bite

- **Relation loads inside `include` do not pass through model `query` extensions.** A soft-delete filter on `findMany` filters the top-level rows and returns deleted children. There is no configuration that fixes this: filter explicitly at each `include`, or read through a database view that already excludes them.
- Raw calls (`$queryRaw`, `$executeRaw`) bypass model extensions entirely (→ `raw-sql.md`).
- Nested writes are one operation from the extension's point of view: a `create` with nested creates fires the `create` interceptor once, for the parent.
- Mutating `args` mutates the caller's object in some shapes — clone rather than edit in place (`args.where = { ...args.where, ... }`, as above).
- `$extends` and `$transaction` interaction has changed across releases. Write one test asserting that your filter still applies inside a transaction, and run it on every Prisma upgrade — a soft-delete filter that quietly stops applying is the worst possible way to learn this.
- Type inference degrades with deep chains. Export `export type Db = typeof db` once and use that type everywhere instead of restating the extended client's shape.

## Migrating From `$use`

| Middleware pattern | Extension equivalent |
|---|---|
| `params.model` / `params.action` | `model` / `operation` in the `query` component |
| `params.args` mutation | `args` mutation, then `query(args)` |
| `next(params)` | `query(args)` |
| Global registration on the singleton | `$extends` at client construction, exporting the extended client |
| One middleware for every model | `$allModels` + `$allOperations` |

Both mechanisms can coexist during a migration: middleware runs for every query on the base client, extensions only for calls through the extended one. That difference is exactly the bug to look for while both exist — a code path holding the base client gets middleware but no extension.
