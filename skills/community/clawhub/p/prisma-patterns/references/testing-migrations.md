# Prisma Testing & Migrations Reference

## Testing with Prisma

### Setup: Test Database Isolation

```typescript
// test/setup.ts
import { execSync } from 'child_process'
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

beforeAll(async () => {
  // Use a separate test database
  process.env.DATABASE_URL = process.env.TEST_DATABASE_URL
  execSync('npx prisma migrate deploy', { stdio: 'inherit' })
})

afterEach(async () => {
  // Clean tables in dependency order
  const tableNames = ['post', 'profile', 'user']
  for (const table of tableNames) {
    await prisma.$executeRawUnsafe(`DELETE FROM "${table}"`)
  }
})

afterAll(async () => {
  await prisma.$disconnect()
})
```

### Factory Pattern for Test Data

```typescript
// test/factories/user.factory.ts
import { prisma } from '@/lib/prisma'
import { Prisma } from '@prisma/client'

let emailCounter = 0

export const createUser = async (
  overrides: Partial<Prisma.UserCreateInput> = {}
) => {
  return prisma.user.create({
    data: {
      email: `user-${++emailCounter}@test.com`,
      name: 'Test User',
      ...overrides,
    },
  })
}

export const createPost = async (
  authorId: string,
  overrides: Partial<Prisma.PostCreateInput> = {}
) => {
  return prisma.post.create({
    data: {
      title: 'Test Post',
      published: true,
      author: { connect: { id: authorId } },
      ...overrides,
    },
  })
}
```

### Mocking Prisma (unit tests)

```typescript
// Use jest-mock-extended
import { mockDeep, DeepMockProxy } from 'jest-mock-extended'
import { PrismaClient } from '@prisma/client'

jest.mock('@/lib/prisma', () => ({
  prisma: mockDeep<PrismaClient>(),
}))

const prismaMock = prisma as DeepMockProxy<PrismaClient>

test('creates user', async () => {
  prismaMock.user.create.mockResolvedValue({
    id: 'cuid1',
    email: 'test@test.com',
    name: 'Test',
    createdAt: new Date(),
    updatedAt: new Date(),
  })

  const user = await createUser({ email: 'test@test.com' })
  expect(user.email).toBe('test@test.com')
})
```

## Migration Best Practices

### Naming Conventions
```bash
# Good: descriptive names
npx prisma migrate dev --name add_user_roles
npx prisma migrate dev --name create_audit_log_table
npx prisma migrate dev --name add_post_view_count

# Bad: vague names
npx prisma migrate dev --name update
npx prisma migrate dev --name fix
```

### Custom Migration SQL

```sql
-- migrations/20250101_add_full_text_search/migration.sql
-- Add after Prisma-generated SQL

-- Create GIN index for full-text search (PostgreSQL)
CREATE INDEX posts_content_search_idx ON posts
  USING GIN (to_tsvector('english', title || ' ' || COALESCE(content, '')));
```

### Zero-Downtime Migration Checklist

1. **Add nullable column** → deploy app → backfill data → add NOT NULL constraint
2. **Rename column** → add new column → dual-write → migrate reads → drop old
3. **Add index** → use `CREATE INDEX CONCURRENTLY` (PostgreSQL) to avoid locks
4. **Drop column** → remove from code first → deploy → then run migration

```prisma
// Step 1: Make nullable (safe)
model User {
  newField String?  // Nullable first
}

// Step 2: After backfill (separate migration)
model User {
  newField String  // Then make required
}
```

## Useful CLI Commands

```bash
# View migration status
npx prisma migrate status

# Generate Prisma Client without migrating
npx prisma generate

# Open Prisma Studio (GUI)
npx prisma studio

# Format schema file
npx prisma format

# Validate schema without migrating
npx prisma validate

# Seed database
npx prisma db seed

# Push schema without migration history (prototyping only)
npx prisma db push
```

## package.json Scripts

```json
{
  "scripts": {
    "db:migrate": "prisma migrate deploy",
    "db:migrate:dev": "prisma migrate dev",
    "db:reset": "prisma migrate reset",
    "db:seed": "prisma db seed",
    "db:studio": "prisma studio",
    "db:generate": "prisma generate",
    "postinstall": "prisma generate"
  },
  "prisma": {
    "seed": "ts-node --compiler-options {\"module\":\"CommonJS\"} prisma/seed.ts"
  }
}
```
