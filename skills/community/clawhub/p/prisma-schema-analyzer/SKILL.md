---
name: prisma-schema-analyzer
description: Analyze Prisma schemas for performance, relation design, index strategy, migration safety, and query optimization — audit schema.prisma for production readiness.
metadata:
  tags: ["prisma", "orm", "database", "typescript", "performance"]
---

# Prisma Schema Analyzer

Analyze Prisma schemas for performance issues, relation design problems, missing indexes, migration risks, and query optimization opportunities. Audit `schema.prisma` for production readiness and recommend improvements.

## Usage

```
"Analyze my Prisma schema for issues"
"Check for missing indexes in my Prisma schema"
"Review Prisma relations for N+1 risks"
"Audit migration safety for my schema changes"
```

## How It Works

### 1. Schema Discovery

```bash
cat prisma/schema.prisma 2>/dev/null
find . -name "schema.prisma" 2>/dev/null
# Check migrations
ls prisma/migrations/ 2>/dev/null | tail -10
```

### 2. Model Analysis

**Field design:**
- Proper types for each field (String vs Int vs DateTime)
- Missing `@default` values where applicable
- `@updatedAt` on models that need update tracking
- Optional fields (`?`) that should be required
- Enum usage vs string for fixed-value fields
- JSON fields where structured models would be better

**ID strategy:**
- `@id` type: autoincrement vs cuid vs uuid
- Composite keys where appropriate (`@@id`)
- Performance implications of UUID PKs vs integer

**Naming conventions:**
- Model names: PascalCase
- Field names: camelCase
- Relation names: descriptive
- `@@map` and `@map` for DB-native naming

### 3. Index Strategy

- Missing indexes on foreign key fields
- Missing indexes on fields used in `where` clauses
- Composite indexes for multi-column queries (`@@index`)
- Unique constraints for business rules (`@@unique`)
- Full-text indexes for search fields
- Index on `createdAt` / `updatedAt` for time-based queries

### 4. Relation Analysis

- Implicit many-to-many (Prisma auto-creates join table — OK for simple cases)
- Explicit many-to-many needed for extra fields on the relation
- One-to-one relations: which side owns the FK?
- Cascade delete configuration (`onDelete: Cascade` vs `SetNull` vs `Restrict`)
- Self-relations (tree structures, followers)
- Relation loading patterns (include vs select)

### 5. Query Optimization

Review Prisma Client usage in codebase:

```bash
grep -rn "prisma\.\w\+\.find\|prisma\.\w\+\.create\|prisma\.\w\+\.update" src/ | head -30
grep -rn "include:" src/ | head -20
```

- N+1 queries: loops with individual `findUnique`
- Over-fetching: `findMany` without `select`
- Missing pagination: `findMany` without `take`/`skip`
- Raw queries that could use Prisma Client
- Transaction usage for multi-step operations

### 6. Migration Safety

```bash
npx prisma migrate diff --from-schema-datamodel prisma/schema.prisma --to-schema-datasource prisma/schema.prisma --script 2>/dev/null
```

- Destructive changes: dropped columns, renamed fields
- Locking operations: new indexes on large tables
- Data migration needed: type changes, default additions
- Backward compatibility: can old code run with new schema?

## Output

```
## Prisma Schema Analysis

**Models:** 14 | **Relations:** 22 | **Indexes:** 8 | **Enums:** 5

### 🔴 Critical (2)
1. **Missing index on Order.userId** — prisma/schema.prisma:45
   `userId String` without `@@index([userId])`
   Orders table has FK queries on every page load
   → Add `@@index([userId])` to Order model

2. **Cascade delete on User → Orders** — prisma/schema.prisma:12
   Deleting a user cascades to all orders (financial records!)
   → Change to `onDelete: Restrict` or `SetNull`

### 🟡 Improvements (4)
3. Missing `@updatedAt` on 8 models
4. Using String for `status` fields — use enum OrderStatus
5. Implicit many-to-many Tag-Post — add explicit for metadata
6. No composite index on `[userId, createdAt]` (common query pattern)

### 📊 Schema Metrics
- Average fields per model: 8.2
- Models with indexes: 6/14 (43%)
- Relations with explicit cascade: 4/22 (18%)
- Optional fields: 23 (review if all truly optional)

### ✅ Good Practices
- cuid() for all primary keys (distributed-safe)
- Enum types for status fields
- @map/@@ for Postgres naming conventions
- Proper DateTime fields with @default(now())
```
