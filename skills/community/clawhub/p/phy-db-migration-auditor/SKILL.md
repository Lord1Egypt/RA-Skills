---
name: DB Migration Auditor
description: Database migration safety auditor. Parses migration files from Alembic (Python), Flyway (SQL), Django, Rails ActiveRecord, and Prisma Migrate to classify every operation by risk tier — SAFE (add nullable column), CAUTION (add index without CONCURRENTLY, rename column), DANGER (DROP COLUMN, ALTER TYPE, NOT NULL without default, DROP TABLE). Cross-references DOWN/downgrade() functions to flag migrations with no rollback path. Checks backward compatibility by scanning ORM model files for columns being dropped. Detects lock-escalating operations that will block production traffic. Generates a pre-deploy checklist and a post-deploy rollback script. Zero external API — pure local file analysis. Triggers on "migration safety", "schema migration audit", "dangerous migration", "DROP COLUMN safe", "migration rollback", "zero-downtime migration", "/db-migration-audit".
license: Apache-2.0
homepage: https://canlah.ai
metadata:
  author: Canlah AI
  version: "1.0.3"
  tags:
    - database
    - migrations
    - safety
    - alembic
    - django
    - rails
    - prisma
    - flyway
    - developer-tools
    - zero-downtime
---

# Database Migration Safety Auditor

You run the migration. The `ALTER TABLE` takes 4 minutes to acquire a lock. Production traffic hangs. The rollback is a `DROP COLUMN` that your ORM is still reading.

This skill reads your migration file before you run it, classifies every operation by risk, checks that a rollback path exists, and warns you about any operation that will cause downtime — before it happens.

**Supports Alembic, Django, Rails, Flyway, Prisma. Zero external API.**

---

## Trigger Phrases

- "migration safety", "safe to run this migration"
- "schema migration audit", "dangerous migration"
- "DROP COLUMN safe", "ALTER TABLE downtime"
- "migration rollback", "zero-downtime migration"
- "missing rollback", "backward compatible migration"
- "will this migration lock tables"
- "/db-migration-audit"

---

## How to Provide Input

```bash
# Option 1: Audit a specific migration file
/db-migration-audit migrations/2026_03_add_user_index.sql
/db-migration-audit alembic/versions/abc123_add_column.py
/db-migration-audit db/migrate/20260318_add_users.rb

# Option 2: Audit all pending migrations
/db-migration-audit migrations/

# Option 3: Check backward compatibility with ORM models
/db-migration-audit --check-models migrations/2026_drop_legacy.sql

# Option 4: Generate rollback script only
/db-migration-audit --rollback-only migrations/abc123.py

# Option 5: Focus on zero-downtime analysis only
/db-migration-audit --zero-downtime migrations/

# Option 6: Full pre-deploy report
/db-migration-audit --pre-deploy migrations/
```

---

## Step 1: Detect Migration Framework

```bash
python3 -c "
import os, glob

checks = [
    ('Alembic (Python)',  ['alembic/', 'alembic/versions/', 'alembic.ini']),
    ('Django',           ['*/migrations/0*.py', '*/migrations/__init__.py']),
    ('Rails',            ['db/migrate/*.rb', 'db/schema.rb']),
    ('Flyway',           ['src/main/resources/db/migration/*.sql',
                           'flyway.conf', 'db/migration/*.sql']),
    ('Prisma',           ['prisma/migrations/*/migration.sql',
                           'prisma/schema.prisma']),
    ('Liquibase',        ['src/main/resources/db/changelog*.xml',
                           'liquibase.properties']),
    ('Plain SQL',        ['migrations/*.sql', 'db/migrations/*.sql']),
]

for name, patterns in checks:
    for p in patterns:
        matches = glob.glob(p, recursive=True)
        if matches:
            print(f'{name}: {len(matches)} files found')
            for m in sorted(matches)[:3]:
                print(f'  {m}')
            break
"
```

---

## Step 2: Parse Migration Operations

```python
import re
from pathlib import Path
from dataclasses import dataclass
from typing import Literal

@dataclass
class MigrationOp:
    operation: str
    table: str
    column: str | None
    risk_tier: Literal['SAFE', 'CAUTION', 'DANGER', 'CRITICAL']
    reason: str
    line: int
    raw: str
    has_rollback: bool = True


# ── Risk Classification ──────────────────────────────────────────────────────

RISK_RULES = [
    # CRITICAL — will definitely cause downtime or data loss
    ('DROP TABLE',          'CRITICAL', 'Destroys table and all data. Irreversible without backup.'),
    ('TRUNCATE',            'CRITICAL', 'Removes all rows. Cannot be rolled back in some databases.'),
    ('DROP DATABASE',       'CRITICAL', 'Destroys entire database.'),

    # DANGER — likely causes issues
    ('DROP COLUMN',         'DANGER',   'Removes column. ORM code reading this column will fail until deployed.'),
    ('ALTER.*TYPE',         'DANGER',   'Changing column type acquires full table lock and may corrupt data.'),
    ('NOT NULL.*DEFAULT',   'DANGER',   'Adding NOT NULL without DEFAULT fails on existing rows.'),
    ('RENAME.*COLUMN',      'DANGER',   'Old column name breaks ORM code until app is redeployed.'),
    ('RENAME.*TABLE',       'DANGER',   'Old table name breaks all ORM queries until app is redeployed.'),
    ('SET.*NOT NULL',       'DANGER',   'Acquires table lock; fails if any existing row is NULL.'),
    ('DROP.*CONSTRAINT',    'DANGER',   'Removing constraints may violate referential integrity.'),
    ('DROP.*INDEX',         'CAUTION',  'Removes query optimization; queries may slow significantly.'),

    # CAUTION — may cause brief locks or require care
    ('ADD.*COLUMN.*NOT NULL',    'CAUTION', 'NOT NULL column requires DEFAULT or will fail on existing rows.'),
    ('CREATE INDEX(?! CONCURRENTLY)', 'CAUTION',
                             'Non-concurrent index creation locks table for writes during build.'),
    ('ADD.*FOREIGN KEY',    'CAUTION',  'FK constraint check locks both tables; validate first on large tables.'),
    ('ALTER.*DEFAULT',      'CAUTION',  'Changing DEFAULT does not affect existing rows.'),
    ('ADD.*CONSTRAINT.*CHECK', 'CAUTION', 'CHECK constraint validates all existing rows — can be slow on large tables.'),

    # SAFE — generally fine
    ('CREATE TABLE',        'SAFE',     'New table — no impact on existing data.'),
    ('ADD.*COLUMN.*NULL',   'SAFE',     'Adding nullable column is safe on all databases.'),
    ('CREATE INDEX CONCURRENTLY', 'SAFE', 'CONCURRENTLY builds index without locking table for writes.'),
    ('CREATE SEQUENCE',     'SAFE',     'New sequence — no impact on existing data.'),
    ('INSERT INTO',         'SAFE',     'Data insertion — safe if FK/UNIQUE constraints are met.'),
]


def classify_sql_operation(line: str, line_num: int) -> MigrationOp | None:
    """Classify a SQL statement by risk tier."""
    line_upper = line.strip().upper()
    if not line_upper or line_upper.startswith('--'):
        return None

    for pattern, risk, reason in RISK_RULES:
        if re.search(pattern, line_upper):
            # Extract table name
            table_match = re.search(
                r'(?:TABLE|FROM|INTO|INDEX ON)\s+(?:IF EXISTS\s+)?["`]?(\w+)["`]?',
                line_upper
            )
            table = table_match.group(1).lower() if table_match else 'unknown'

            # Extract column name
            col_match = re.search(r'(?:COLUMN|ADD|DROP)\s+["`]?(\w+)["`]?', line_upper)
            col = col_match.group(1).lower() if col_match else None

            return MigrationOp(
                operation=pattern,
                table=table,
                column=col,
                risk_tier=risk,
                reason=reason,
                line=line_num,
                raw=line.strip(),
            )
    return None


def parse_sql_migration(filepath: str) -> list[MigrationOp]:
    """Parse a .sql migration file."""
    ops = []
    with open(filepath) as f:
        lines = f.readlines()

    for i, line in enumerate(lines, 1):
        op = classify_sql_operation(line, i)
        if op:
            ops.append(op)

    return ops


def parse_alembic_migration(filepath: str) -> tuple[list[MigrationOp], bool]:
    """Parse an Alembic Python migration file."""
    content = Path(filepath).read_text()
    ops = []

    # Check if downgrade() function exists and is not just `pass`
    downgrade_match = re.search(r'def downgrade\(\).*?(?=def |\Z)', content, re.DOTALL)
    has_rollback = bool(downgrade_match and
                        'pass' not in downgrade_match.group(0).replace('def downgrade():', '').strip()[:20])

    # Extract Alembic op.* calls
    alembic_ops = re.findall(
        r'op\.([\w]+)\([^)]*\)',
        content
    )

    ALEMBIC_RISK = {
        'drop_table':           ('CRITICAL', 'Destroys table and all data.'),
        'drop_column':          ('DANGER',   'Column removed — ORM reads will fail until app redeployed.'),
        'alter_column':         ('DANGER',   'Column type/nullability change — can cause data loss or table lock.'),
        'execute':              ('CAUTION',  'Raw SQL execute — risk depends on the SQL inside.'),
        'create_table':         ('SAFE',     'New table — no impact on existing data.'),
        'add_column':           ('SAFE',     'Adding column — safe if nullable or has DEFAULT.'),
        'create_index':         ('CAUTION',  'Index creation — use postgresql_concurrently=True for large tables.'),
        'drop_index':           ('CAUTION',  'Removing index — queries may slow.'),
        'create_foreign_key':   ('CAUTION',  'FK constraint validation can lock both tables.'),
        'drop_constraint':      ('DANGER',   'Removing constraint may allow invalid data.'),
        'rename_table':         ('DANGER',   'Old table name breaks existing queries.'),
        'bulk_insert':          ('SAFE',     'Data insertion — safe in transactions.'),
    }

    for op_name in alembic_ops:
        risk, reason = ALEMBIC_RISK.get(op_name.lower(), ('SAFE', 'Unknown operation'))
        ops.append(MigrationOp(
            operation=op_name,
            table='(see file)',
            column=None,
            risk_tier=risk,
            reason=reason,
            line=0,
            raw=f'op.{op_name}(...)',
            has_rollback=has_rollback,
        ))

    return ops, has_rollback
```

---

## Step 3: Check Backward Compatibility

```python
import glob

def check_backward_compatibility(migration_ops: list[MigrationOp], src_dir: str = '.') -> list[dict]:
    """
    For DROP COLUMN / RENAME COLUMN operations, check if the old column
    name still appears in ORM model files, API serializers, or query code.
    """
    issues = []

    dropped_columns = [
        op for op in migration_ops
        if op.operation in ('DROP COLUMN', 'drop_column') and op.column
    ]

    renamed_columns = [
        op for op in migration_ops
        if 'RENAME' in op.operation and op.column
    ]

    source_files = []
    for ext in ['*.py', '*.ts', '*.js', '*.rb', '*.go', '*.java']:
        source_files.extend(glob.glob(f'{src_dir}/**/{ext}', recursive=True))

    # Filter out migrations themselves
    source_files = [f for f in source_files
                    if 'migration' not in f.lower() and 'migrate' not in f.lower()]

    for op in dropped_columns:
        col = op.column
        table = op.table
        references = []
        for fpath in source_files:
            try:
                content = Path(fpath).read_text(errors='replace')
                if col in content:
                    # Find the specific lines
                    for i, line in enumerate(content.splitlines(), 1):
                        if col in line and 'migration' not in line.lower():
                            references.append(f'{fpath}:{i}: {line.strip()[:80]}')
            except Exception:
                continue

        if references:
            issues.append({
                'type': 'BACKWARD_COMPAT_BREAK',
                'operation': f'DROP COLUMN {table}.{col}',
                'severity': 'CRITICAL',
                'description': (
                    f'Column `{col}` on table `{table}` is being dropped, '
                    f'but is still referenced in {len(references)} source file(s). '
                    f'Dropping will break running application code.'
                ),
                'references': references[:5],
                'fix': (
                    f'Deploy code that removes all references to `{col}` BEFORE running this migration. '
                    f'Use the expand/contract pattern: (1) deprecate column in code, (2) deploy, (3) drop column.'
                ),
            })

    return issues
```

---

## Step 4: Generate Pre-Deploy Checklist

```python
def generate_pre_deploy_checklist(ops: list[MigrationOp], issues: list[dict]) -> str:
    """Generate a structured pre-deploy checklist."""

    danger_ops = [op for op in ops if op.risk_tier in ('DANGER', 'CRITICAL')]
    caution_ops = [op for op in ops if op.risk_tier == 'CAUTION']
    no_rollback = [op for op in ops if not op.has_rollback]
    backward_breaks = [i for i in issues if i['type'] == 'BACKWARD_COMPAT_BREAK']

    checklist = ['## Pre-Deploy Migration Checklist\n']

    if danger_ops or backward_breaks:
        checklist.append('### 🔴 MUST DO BEFORE RUNNING\n')
        for op in danger_ops:
            checklist.append(f'- [ ] Verify backup exists (operation: {op.operation} on {op.table})')
        for issue in backward_breaks:
            checklist.append(f'- [ ] Deploy code removing {issue["operation"]} references first')

    if caution_ops:
        checklist.append('\n### 🟠 REVIEW BEFORE RUNNING\n')
        for op in caution_ops:
            checklist.append(f'- [ ] Verify {op.operation} on {op.table}: {op.reason}')

    if no_rollback:
        checklist.append('\n### ⚠️ NO ROLLBACK PATH\n')
        checklist.append('- [ ] Confirm you have a database backup before proceeding')
        checklist.append('- [ ] Write and test the rollback SQL manually before running')

    checklist.append('\n### ✅ STANDARD CHECKS\n')
    checklist.append('- [ ] Migration tested on staging with production-scale data')
    checklist.append('- [ ] Estimated duration recorded (check EXPLAIN on affected tables)')
    checklist.append('- [ ] Maintenance window scheduled if DANGER/CRITICAL ops present')
    checklist.append('- [ ] Rollback plan documented and shared with team')

    return '\n'.join(checklist)
```

---

## Step 5: Output Report

```markdown
## Database Migration Audit
File: alembic/versions/abc1234_drop_legacy_columns.py
Framework: Alembic | Database: PostgreSQL

---

### Risk Summary

| Operation | Table | Risk | Issue |
|-----------|-------|------|-------|
| `op.drop_column('users', 'legacy_token')` | users | 🔴 DANGER | ORM still reads `legacy_token` |
| `op.alter_column('orders', 'status', type_=Text)` | orders | 🔴 DANGER | Type change may acquire full table lock |
| `op.create_index('ix_users_email', 'users', ['email'])` | users | 🟠 CAUTION | Non-concurrent index blocks writes |
| `op.add_column('users', Column('profile_json', JSON))` | users | ✅ SAFE | Nullable column addition |

---

### 🔴 CRITICAL: Backward Compatibility Break

**DROP COLUMN `users.legacy_token`**

The column `legacy_token` is still referenced in production code:

```
src/auth/token_validator.py:34:  if user.legacy_token:
src/api/serializers.py:89:       'legacy_token': user.legacy_token,
src/models/user.py:67:           legacy_token = Column(String, nullable=True)
```

**Deploying this migration before updating application code will cause runtime errors.**

Fix — use the Expand/Contract pattern:
```
Step 1: Remove all legacy_token references from code and deploy
Step 2: Wait for old pods/processes to fully drain
Step 3: Run this migration to drop the column
```

---

### 🔴 DANGER: Type Change Table Lock

**`op.alter_column('orders', 'status', type_=Text)`**

Changing column type in PostgreSQL acquires an `ACCESS EXCLUSIVE` lock — blocks all reads and writes for the duration.

For a large `orders` table, this may take minutes.

**Fix — zero-downtime type change:**
```python
# Step 1: Add a new column (no lock)
op.add_column('orders', Column('status_new', Text, nullable=True))

# Step 2: Backfill in batches (separate migration)
# UPDATE orders SET status_new = status::text WHERE status_new IS NULL LIMIT 5000

# Step 3: Swap (after backfill is complete)
op.alter_column('orders', 'status_new', new_column_name='status')
op.drop_column('orders', 'status_old')
```

---

### 🟠 CAUTION: Non-Concurrent Index

**`CREATE INDEX ix_users_email ON users (email)`**

Non-concurrent index creation locks the table for writes during the entire build.

**Fix:**
```python
# Replace:
op.create_index('ix_users_email', 'users', ['email'])

# With (PostgreSQL — no write lock):
op.create_index('ix_users_email', 'users', ['email'], postgresql_concurrently=True)
# Note: CONCURRENTLY cannot run inside a transaction — wrap with:
# with op.get_context().autocommit_block():
#     op.create_index(...)
```

---

### ⚠️ Rollback Assessment

```python
def downgrade():
    pass  # ← NO ROLLBACK IMPLEMENTED
```

This migration has **no rollback path**. If something goes wrong:
- `legacy_token` column is permanently gone
- `status` type change cannot be trivially reversed

**Generated rollback script (add to downgrade function):**
```python
def downgrade():
    # Re-add the dropped column (data will be NULL — restore from backup)
    op.add_column('users', Column('legacy_token', String, nullable=True))
    # Reverse the type change
    op.alter_column('orders', 'status', type_=sa.Enum('pending', 'complete', 'failed'))
```

---

### Pre-Deploy Checklist

- [ ] Deploy code removing `legacy_token` references BEFORE running
- [ ] Verify backup exists (DROP COLUMN on users)
- [ ] Verify backup exists (ALTER TYPE on orders)
- [ ] Replace `create_index` with `postgresql_concurrently=True`
- [ ] Implement `downgrade()` function
- [ ] Test on staging with production-scale data volume
- [ ] Estimate index build time: `SELECT COUNT(*) FROM users` → estimate ~1 min per 1M rows

---

### Estimated Risk Score: 🔴 HIGH (3 DANGER operations, 0 rollback)
```

---

## Quick Mode Output

```
Migration Audit: alembic/versions/abc1234_drop_legacy_columns.py (Alembic)

🔴 CRITICAL: legacy_token column still referenced in 3 source files — will break production
🔴 DANGER: ALTER TYPE on orders.status → full table lock (potential minutes of downtime)
🟠 CAUTION: Non-concurrent index on users.email → locks writes during build
⚠️  NO ROLLBACK: downgrade() is empty — no way to undo this migration

Verdict: DO NOT RUN in production until backward compat break is resolved.
Run /db-migration-audit --pre-deploy to get full checklist.
```

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)
