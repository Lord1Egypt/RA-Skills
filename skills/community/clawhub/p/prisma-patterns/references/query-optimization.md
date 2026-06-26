# Prisma Query Optimization Patterns

## Select vs Include

```typescript
// ❌ Over-fetching: returns all fields including large ones
const users = await prisma.user.findMany({
  include: { posts: true }
})

// ✅ Only fetch what you need
const users = await prisma.user.findMany({
  select: {
    id: true,
    name: true,
    email: true,
    posts: {
      select: { id: true, title: true },
      where: { published: true },
      take: 5,
    }
  }
})
```

## Cursor-Based Pagination (better than offset for large datasets)

```typescript
const getCursorPage = async (cursor?: string, limit = 20) => {
  const posts = await prisma.post.findMany({
    take: limit + 1,  // Fetch one extra to know if there's a next page
    ...(cursor && {
      cursor: { id: cursor },
      skip: 1,
    }),
    orderBy: { createdAt: 'desc' },
    select: { id: true, title: true, createdAt: true },
  })

  const hasNextPage = posts.length > limit
  const items = hasNextPage ? posts.slice(0, -1) : posts
  const nextCursor = hasNextPage ? items[items.length - 1].id : null

  return { items, nextCursor, hasNextPage }
}
```

## Batch Operations

```typescript
// Create many (faster than loop)
await prisma.tag.createMany({
  data: [
    { name: 'typescript', slug: 'typescript' },
    { name: 'prisma', slug: 'prisma' },
    { name: 'nextjs', slug: 'nextjs' },
  ],
  skipDuplicates: true,
})

// Update many with same value
await prisma.post.updateMany({
  where: { authorId: userId, published: false },
  data: { published: true },
})

// Delete many
await prisma.post.deleteMany({
  where: {
    createdAt: { lt: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000) },
    published: false,
  },
})
```

## Raw Queries (when Prisma can't express it)

```typescript
// Raw SQL with type safety
const result = await prisma.$queryRaw<{ count: bigint }[]>`
  SELECT COUNT(*) as count
  FROM users
  WHERE created_at > ${new Date('2025-01-01')}
    AND metadata->>'plan' = 'pro'
`

// Execute raw (no return value)
await prisma.$executeRaw`
  UPDATE posts SET view_count = view_count + 1
  WHERE id = ${postId}
`
```

## Aggregations

```typescript
const stats = await prisma.post.aggregate({
  _count: { id: true },
  _avg: { viewCount: true },
  _max: { createdAt: true },
  where: { published: true },
})

// Group by
const tagCounts = await prisma.post.groupBy({
  by: ['status'],
  _count: { id: true },
  orderBy: { _count: { id: 'desc' } },
})
```

## Performance Tips

1. **Index strategy**: Add `@@index` for any field used in `where`, `orderBy`, or `JOIN`
2. **Limit depth**: Avoid nesting includes more than 2 levels deep
3. **Use `select` in production**: Never return full objects when partial is enough
4. **Connection pooling**: Set `connection_limit` in DATABASE_URL; use PgBouncer for serverless
5. **Avoid `findMany` without limits**: Always add `take` to prevent runaway queries
6. **Monitor slow queries**: Enable `log: ['query']` in dev; use `EXPLAIN ANALYZE` for slow ones

## Serverless Considerations

```typescript
// PrismaClient in serverless (avoid cold start connection exhaustion)
// Option 1: Prisma Accelerate (recommended)
// DATABASE_URL="prisma://accelerate.prisma-data.net/?api_key=..."

// Option 2: Manual connection limit
const prisma = new PrismaClient({
  datasources: {
    db: {
      url: process.env.DATABASE_URL + '?connection_limit=1&pool_timeout=20',
    },
  },
})

// Always disconnect in serverless handlers if not using Accelerate
export const handler = async (event: any) => {
  try {
    const result = await prisma.user.findMany()
    return result
  } finally {
    await prisma.$disconnect()
  }
}
```
