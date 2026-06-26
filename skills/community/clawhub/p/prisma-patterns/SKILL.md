---
name: prisma-patterns
description: >
  Use this skill when working with Prisma ORM in Node.js/TypeScript projects.
  Covers schema design, migrations, query optimization, relations, transactions,
  and best practices for production-ready database interactions with Prisma 5+.
---

# Prisma ORM Patterns

## When to Use
- Designing or migrating a Prisma schema
- Writing complex queries with relations, filtering, or pagination
- Handling transactions and error scenarios
- Optimizing N+1 queries and performance
- Setting up Prisma in monorepos or serverless environments

## Core Workflow

### 1. Schema Design Principles
```prisma
// schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  posts     Post[]
  profile   Profile?

  @@index([email])
  @@map("users")
}

model Post {
  id        String   @id @default(cuid())
  title     String
  content   String?
  published Boolean  @default(false)
  authorId  String
  author    User     @relation(fields: [authorId], references: [id], onDelete: Cascade)

  tags      Tag[]    @relation("PostTags")

  @@index([authorId, published])
  @@map("posts")
}
```

### 2. Migration Workflow
```bash
# Development: auto-apply
npx prisma migrate dev --name add_user_profile

# Production: generate SQL only, review, then deploy
npx prisma migrate deploy

# Reset dev database
npx prisma migrate reset

# Introspect existing DB
npx prisma db pull
```

### 3. Client Initialization (Singleton Pattern)
```typescript
// lib/prisma.ts
import { PrismaClient } from '@prisma/client'

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined
}

export const prisma =
  globalForPrisma.prisma ??
  new PrismaClient({
    log: process.env.NODE_ENV === 'development'
      ? ['query', 'error', 'warn']
      : ['error'],
  })

if (process.env.NODE_ENV !== 'production') {
  globalForPrisma.prisma = prisma
}
```

### 4. Common Query Patterns
```typescript
// Paginated query with relations
const getPostsPage = async (page: number, limit = 10) => {
  const [posts, total] = await prisma.$transaction([
    prisma.post.findMany({
      where: { published: true },
      include: {
        author: { select: { id: true, name: true } },
        _count: { select: { tags: true } },
      },
      orderBy: { createdAt: 'desc' },
      skip: (page - 1) * limit,
      take: limit,
    }),
    prisma.post.count({ where: { published: true } }),
  ])
  return { posts, total, pages: Math.ceil(total / limit) }
}

// Upsert pattern
const upsertUser = async (email: string, name: string) => {
  return prisma.user.upsert({
    where: { email },
    update: { name },
    create: { email, name },
  })
}

// Avoid N+1: use include vs separate queries
const postsWithAuthors = await prisma.post.findMany({
  include: { author: true }, // Single JOIN query, not N+1
})
```

### 5. Transactions
```typescript
// Interactive transaction (recommended for complex logic)
const transferCredits = async (fromId: string, toId: string, amount: number) => {
  return prisma.$transaction(async (tx) => {
    const from = await tx.user.findUniqueOrThrow({ where: { id: fromId } })
    if (from.credits < amount) throw new Error('Insufficient credits')

    await tx.user.update({
      where: { id: fromId },
      data: { credits: { decrement: amount } },
    })
    await tx.user.update({
      where: { id: toId },
      data: { credits: { increment: amount } },
    })
  })
}
```

### 6. Error Handling
```typescript
import { Prisma } from '@prisma/client'

const safeCreate = async (data: Prisma.UserCreateInput) => {
  try {
    return await prisma.user.create({ data })
  } catch (e) {
    if (e instanceof Prisma.PrismaClientKnownRequestError) {
      if (e.code === 'P2002') {
        throw new Error(`Unique constraint violated: ${e.meta?.target}`)
      }
    }
    throw e
  }
}
```

## Best Practices
- Always use `select` to limit returned fields in production queries
- Add `@@index` for frequently filtered/sorted columns
- Use `findUniqueOrThrow` / `findFirstOrThrow` to avoid null checks
- Prefer `$transaction` for multi-step operations
- Enable query logging in development only
- Use connection pooling (PgBouncer / Prisma Accelerate) in serverless
