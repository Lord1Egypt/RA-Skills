---
name: migration-safety-checker
description: Check database migrations for safety — detect data loss risks, locking operations, backward compatibility issues, and deployment ordering problems across SQL and ORM migrations.
metadata:
  tags: ["database", "migration", "safety", "sql", "devops"]
---

# Migration Safety Checker

Check database migrations for data loss risks, table-locking operations, backward compatibility issues, and deployment ordering problems. Works with raw SQL migrations, ORMs (Prisma, Drizzle, Django, Rails, Sequelize, TypeORM), and migration tools (Flyway, Liquibase, golang-migrate).

## Usage

```
"Check this migration for safety"
"Will this migration lock the users table?"
"Is this migration backward compatible?"
"Review the pending migrations before deployment"
```

## How It Works

### 1. Migration Discovery

```bash
find . -path "*/migrations/*.sql" -o -path "*/migrations/*.py" -o -path "*/migrate/*.sql" 2>/dev/null | head -20
ls prisma/migrations/*/migration.sql 2>/dev/null
find . -path "*/migrations/0*.py" 2>/dev/null | tail -10
ls db/migrate/*.rb 2>/dev/null | tail -10
```

### 2. Dangerous Operation Detection

**Data loss risks:**
- `DROP TABLE` / `DROP COLUMN` — irreversible data deletion
- `TRUNCATE TABLE` — removes all rows
- Column type narrowing (VARCHAR(255) → VARCHAR(50))
- Removing NOT NULL without default (existing rows get NULL)
- Renaming columns (breaks existing queries)

**Locking operations (on large tables):**
- `ALTER TABLE ... ADD COLUMN` with DEFAULT (pre-Postgres 11, MySQL)
- `ALTER TABLE ... ADD INDEX` without CONCURRENTLY
- `ALTER TABLE ... MODIFY COLUMN` (MySQL full table rewrite)
- `CREATE INDEX` without CONCURRENTLY (Postgres)
- `ALTER TABLE ... ADD CONSTRAINT` (full table scan)

**Backward compatibility:**
- Adding NOT NULL column without default
- Renaming table/column
- Removing enum values
- Changing primary key
- Dropping index that queries depend on

### 3. Deployment Safety

**Rolling deployment compatibility:**
- Can old code work with new schema? (backward compatible)
- Can new code work with old schema? (forward compatible)
- Does migration need multi-step deployment?

**Safe pattern for risky changes:**
```
Step 1: Add new column (nullable)
Step 2: Deploy code writing to both columns
Step 3: Backfill data
Step 4: Deploy code reading from new column
Step 5: Drop old column
```

### 4. Performance Impact

- Estimate table size and lock duration
- Check if migration can run during traffic
- Recommend maintenance window if needed
- Suggest concurrent/online migration alternatives

### 5. ORM-Specific Checks

- **Prisma:** `prisma migrate diff` for destructive changes
- **Django:** `RunPython` without reverse function
- **Rails:** Non-reversible migrations
- **Sequelize:** `queryInterface.removeColumn` without backup

## Output

```
## Migration Safety Report

**Migrations reviewed:** 3 pending
**Database:** PostgreSQL 15

### Migration 1: 20260430_add_preferences.sql
✅ SAFE — adds nullable column, no lock

### Migration 2: 20260430_add_email_unique.sql
🟠 CAUTION — adds unique constraint on 2M-row table
Lock time: 15-30s | Blocks writes during creation
Fix: CREATE UNIQUE INDEX CONCURRENTLY + ADD CONSTRAINT USING INDEX

### Migration 3: 20260430_remove_legacy_columns.sql
🔴 DANGEROUS — drops 3 columns with 500K non-null values
1. Verify no code references these columns
2. Backup data before dropping
3. Deploy separately from code changes

| Migration | Safety | Lock Risk | Backward Compatible |
|-----------|--------|-----------|-------------------|
| add_preferences | ✅ | None | Yes |
| add_email_unique | 🟠 | 15-30s | Yes |
| remove_legacy | 🔴 | Minimal | NO |
```
