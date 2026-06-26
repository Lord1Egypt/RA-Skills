# Prisma Schema Design Reference

## Field Types & Modifiers

```prisma
model Example {
  // ID strategies
  id        Int      @id @default(autoincrement())
  id        String   @id @default(cuid())       // Collision-resistant
  id        String   @id @default(uuid())       // UUID v4
  id        Bytes    @id @default(dbgenerated("gen_random_uuid()"))

  // Common field patterns
  email     String   @unique
  slug      String   @unique @db.VarChar(100)
  bio       String?  @db.Text                   // Nullable large text
  metadata  Json?                               // Flexible JSON storage
  score     Float    @default(0.0)
  status    Status   @default(ACTIVE)           // Enum

  // Timestamps
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  deletedAt DateTime?                           // Soft delete

  // Composite unique
  @@unique([userId, postId])

  // Multi-column index
  @@index([status, createdAt(sort: Desc)])
}

enum Status {
  ACTIVE
  INACTIVE
  BANNED
}
```

## Relation Patterns

```prisma
// One-to-One
model User {
  id      String   @id @default(cuid())
  profile Profile?
}
model Profile {
  id     String @id @default(cuid())
  userId String @unique
  user   User   @relation(fields: [userId], references: [id])
}

// One-to-Many
model Author {
  id    String @id @default(cuid())
  posts Post[]
}
model Post {
  id       String @id @default(cuid())
  authorId String
  author   Author @relation(fields: [authorId], references: [id])
}

// Many-to-Many (implicit)
model Post {
  id   String @id @default(cuid())
  tags Tag[]
}
model Tag {
  id    String @id @default(cuid())
  posts Post[]
}

// Many-to-Many (explicit — recommended when join table has extra fields)
model PostTag {
  postId    String
  tagId     String
  createdAt DateTime @default(now())
  assignedBy String

  post Post @relation(fields: [postId], references: [id])
  tag  Tag  @relation(fields: [tagId], references: [id])

  @@id([postId, tagId])
}
```

## Soft Delete Pattern

```prisma
model Post {
  id        String    @id @default(cuid())
  deletedAt DateTime?
}
```

```typescript
// Soft delete middleware
prisma.$use(async (params, next) => {
  if (params.model === 'Post') {
    if (params.action === 'delete') {
      params.action = 'update'
      params.args.data = { deletedAt: new Date() }
    }
    if (params.action === 'findMany' || params.action === 'findFirst') {
      params.args.where = {
        ...params.args.where,
        deletedAt: null,
      }
    }
  }
  return next(params)
})
```

## Connection String Formats

```
# PostgreSQL
postgresql://USER:PASSWORD@HOST:PORT/DATABASE?schema=public&connection_limit=5

# MySQL
mysql://USER:PASSWORD@HOST:PORT/DATABASE

# SQLite (dev only)
file:./dev.db

# With SSL (production)
postgresql://USER:PASSWORD@HOST/DATABASE?sslmode=require
```

## Common Prisma Error Codes

| Code  | Meaning                          | Fix                              |
|-------|----------------------------------|----------------------------------|
| P2002 | Unique constraint violation      | Check for duplicate values       |
| P2003 | Foreign key constraint failed    | Ensure related record exists     |
| P2025 | Record not found                 | Use findFirst instead of throw   |
| P2014 | Relation violation               | Check cascade settings           |
| P1001 | Can't reach database server      | Check DATABASE_URL & network     |
