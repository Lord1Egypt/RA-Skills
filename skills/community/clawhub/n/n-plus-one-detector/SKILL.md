---
name: n-plus-one-detector
description: Detect N+1 query problems in application code and ORM usage. Analyze database query patterns, find loops that generate excessive queries, and recommend fixes using eager loading, joins, batch fetching, and DataLoader patterns.
---

# N+1 Query Detector

Find the N+1 queries silently killing your application performance. Analyze ORM usage, spot loops generating redundant database queries, measure query counts per request, and recommend specific fixes — eager loading, joins, batch fetching, or DataLoader patterns.

Use when: "find N+1 queries", "why is this endpoint slow", "too many database queries", "ORM performance", "optimize queries", "database query count", or when a page makes hundreds of similar queries.

## Commands

### 1. `detect` — Find N+1 Patterns in Code

#### Step 1: Identify ORM and Query Patterns

```bash
# Detect ORM in use
rg "from sqlalchemy|from django\.db|ActiveRecord|prisma|typeorm|sequelize|mongoose|gorm|ent\." \
  --type-not binary -g '!node_modules' -g '!vendor' --stats 2>&1

# Find model definitions
rg "class.*Model|@Entity|schema\.|model\s+\w+\s*\{" \
  --type-not binary -g '!node_modules' -g '!vendor' 2>/dev/null | head -30
```

#### Step 2: Static Analysis — Find Loop + Query Patterns

```bash
# Python (Django/SQLAlchemy) — access related objects in loops
rg -U "for\s+\w+\s+in\s+\w+.*:\s*\n.*\.\w+\.(all|filter|get|first|objects)" \
  --type py -g '!migrations' 2>/dev/null

# JavaScript/TypeScript (Prisma/TypeORM/Sequelize) — await in loop
rg -U "for.*of.*\{[\s\S]*?await.*\.(find|query|get|fetch)" \
  --type ts --type js -g '!node_modules' 2>/dev/null

# Ruby (ActiveRecord) — accessing association in loop
rg -U "\.each\s+do.*\n.*\.\w+\.(where|find|pluck)" \
  --type ruby 2>/dev/null

# Go (GORM/ent) — query in range loop
rg -U "for.*range.*\{[\s\S]*?\.Find\(|\.Where\(|\.First\(" \
  --type go 2>/dev/null
```

#### Step 3: Runtime Detection (if tests/dev server available)

```bash
# Django — enable query logging
DJANGO_DEBUG=1 python3 -c "
import django; django.setup()
from django.db import connection
from django.test.utils import override_settings

# Run the suspect view/function
# ...

queries = connection.queries
print(f'Total queries: {len(queries)}')

# Group by similar query pattern
from collections import Counter
patterns = Counter()
for q in queries:
    # Normalize: remove specific IDs
    import re
    pattern = re.sub(r'= \d+', '= ?', q['sql'])
    patterns[pattern] += 1

for pattern, count in patterns.most_common(10):
    if count > 1:
        print(f'  ⚠️  {count}x: {pattern[:120]}')
"

# Node.js — enable Prisma query logging
# Set DEBUG=prisma:query or use prisma.$on('query')

# Rails — enable query logging
# ActiveSupport::Notifications.subscribe("sql.active_record")
```

#### Step 4: Classify and Fix

For each N+1 found:

**Pattern 1: Lazy-loaded relationship in loop**
```python
# BAD — N+1: 1 query for posts + N queries for authors
for post in Post.objects.all():
    print(post.author.name)  # Each .author triggers a query

# FIX — Eager load with select_related (FK) or prefetch_related (M2M)
for post in Post.objects.select_related('author').all():
    print(post.author.name)  # 1 query total
```

**Pattern 2: Async query in loop**
```typescript
// BAD — N+1: awaiting individual queries
for (const userId of userIds) {
    const user = await prisma.user.findUnique({ where: { id: userId } });
}

// FIX — Batch query
const users = await prisma.user.findMany({ where: { id: { in: userIds } } });
```

**Pattern 3: GraphQL resolver N+1**
```javascript
// BAD — resolver called per parent item
resolve(parent) {
    return db.query('SELECT * FROM comments WHERE post_id = ?', [parent.id]);
}

// FIX — DataLoader pattern
const commentLoader = new DataLoader(async (postIds) => {
    const comments = await db.query('SELECT * FROM comments WHERE post_id IN (?)', [postIds]);
    return postIds.map(id => comments.filter(c => c.post_id === id));
});
resolve(parent) { return commentLoader.load(parent.id); }
```

#### Step 5: Report

```markdown
# N+1 Query Report

## Summary
- Files scanned: 45
- N+1 patterns found: 6
- Estimated excess queries per request: ~200-500

## Critical (high-traffic endpoints)
1. `api/views/orders.py:34` — Order list loads customer for each order
   - Current: 1 + N queries (N = page size, typically 50)
   - Fix: `Order.objects.select_related('customer')`
   - Impact: 50 queries → 1 query

2. `api/resolvers/post.ts:18` — Post resolver loads comments individually
   - Current: 1 + N queries per post listing
   - Fix: DataLoader for comments
   - Impact: N queries → 1 batched query

## Recommendations
1. Add `select_related`/`prefetch_related` to all list views
2. Implement DataLoader for GraphQL resolvers
3. Add query count assertions to integration tests:
   ```python
   with self.assertNumQueries(3):
       response = self.client.get('/api/orders/')
   ```
```

### 2. `monitor` — Add Query Count Guards

Generate test assertions or middleware that counts queries per request and fails when count exceeds threshold:

```python
# Django middleware
class QueryCountMiddleware:
    def __call__(self, request):
        from django.db import connection
        initial = len(connection.queries)
        response = self.get_response(request)
        count = len(connection.queries) - initial
        if count > 20:  # threshold
            logger.warning(f'{request.path}: {count} queries')
        response['X-Query-Count'] = str(count)
        return response
```

### 3. `benchmark` — Measure Query Reduction Impact

Before and after applying fixes, measure:
- Total query count per request
- Response time improvement
- Database load reduction
