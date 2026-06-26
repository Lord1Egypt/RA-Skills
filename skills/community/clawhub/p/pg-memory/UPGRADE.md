# Upgrading pg-memory

Simple guides for upgrading between versions.

---

## v2.5.0 → v2.7.0 (Direct Upgrade)

**Recommended path** — skips v2.6.0 since it had no database changes.

**Upgrade Type:** Database migration required (adds multi-instance support) + code upgrade

### Quick Direct Upgrade

```bash
# 1. Backup your data
cd pg-memory
pg_dump -U $(whoami) -d openclaw_memory > backup_pre_27_$(date +%Y%m%d).sql

# 2. Pull latest code (gets v2.6.0 + v2.7.0)
git pull origin main

# 3. Run the v2.7.0 database migration
psql -U $(whoami) -d openclaw_memory -f scripts/schema_v2_7_multi_instance.sql

# 4. Verify columns exist
psql -U $(whoami) -d openclaw_memory -c "
SELECT column_name FROM information_schema.columns 
WHERE table_name = 'observations' 
AND column_name IN ('instance_id', 'agent_label');
"
# Expected: instance_id, agent_label (2 rows)

# 5. Test the connection and generate instance ID
python3 -c "
import sys; sys.path.insert(0, 'scripts')
from pg_memory import PostgresMemory
mem = PostgresMemory()
print(f'Agent: {mem.agent_label}')
print(f'Instance: {mem.instance_id}')
print(f'Status: v2.7.0 ready!')
"

# 6. Tag existing data (CRITICAL!)
psql -U $(whoami) -d openclaw_memory -c "
UPDATE observations 
SET agent_label = 'pre-v2.7.0', 
    instance_id = '00000000-0000-0000-0000-000000000000'::UUID
WHERE agent_label IS NULL OR agent_label = '';
"

# 7. Verify tagging
psql -U $(whoami) -d openclaw_memory -c "
SELECT agent_label, COUNT(*) 
FROM observations 
GROUP BY agent_label 
ORDER BY count DESC;
"
```

### What You Get

From v2.6.0:
- **Duplicate Detection** — Find similar observations
- **Tag Autocomplete** — Suggest relevant tags
- **Backup & Restore** — Full database snapshots
- **JSON Export/Import** — Portable data format
- **Install Script** — One-command setup

From v2.7.0:
- **Multi-Instance Support** — Share database across machines
- **Auto Instance IDs** — Unique UUID per machine
- **Agent Labeling** — Human-readable names
- **Concurrent Safety** — UPSERT patterns prevent conflicts

---

## v2.6.0 → v2.7.0

**Upgrade Type:** Database migration required (adds multi-instance support)

### What's New in v2.7.0

- **Multi-Instance Support** — Multiple OpenClaw instances sharing one database
- **Auto-Generated Instance IDs** — Unique UUID per machine (auto-created)
- **Agent Labeling** — Human-readable instance names (e.g., "arty", "brodie")
- **Concurrent Access Safety** — UPSERT patterns prevent duplicate links
- **Instance Statistics** — Query data by machine/agent
- **Migration to Remote DB** — Move from local to shared PostgreSQL server

### Upgrade Steps

```bash
# 1. Backup your data first
cd pg-memory
pg_dump -U [user] -d openclaw_memory > backup_pre_27.sql

# 2. Pull latest code
git pull origin main

# 3. Run database migration
psql -U [user] -d openclaw_memory -f scripts/schema_v2_7_multi_instance.sql

# 4. Verify new columns exist
psql -U [user] -d openclaw_memory -c \"
SELECT column_name FROM information_schema.columns 
WHERE table_name = 'observations' 
AND column_name IN ('instance_id', 'agent_label');
\"
# Expected: instance_id, agent_label

# 5. Test the upgrade
python3 -c \"
from pg_memory import PostgresMemory
mem = PostgresMemory()
print(f'Agent: {mem.agent_label}')
print(f'Instance: {mem.instance_id}')
\"
```

### 6. Tag Existing Data (CRITICAL!)

**Existing observations from before v2.7.0 have `NULL` values for `instance_id` and `agent_label`.**

**You MUST update your existing data to tag it with your instance ID:**

**Option A: Tag all existing observations as "pre-v2.7.0"**

```bash
psql -U [user] -d openclaw_memory -c "
UPDATE observations 
SET agent_label = 'pre-v2.7.0', 
    instance_id = '00000000-0000-0000-0000-000000000000'::UUID
WHERE agent_label IS NULL OR agent_label = '';
"
```

**Option B: Tag all existing observations with YOUR instance**

```bash
# Get your instance_id
python3 -c "
import sys
sys.path.insert(0, 'scripts')
from pg_memory import PostgresMemory
mem = PostgresMemory()
print(f'UPDATE observations SET instance_id = \\'' + mem.instance_id + \\'::UUID, agent_label = \\'' + mem.agent_label + \\'\\' WHERE agent_label IS NULL;')
" > update_sql.sql

# Run the update
psql -U [user] -d openclaw_memory -f update_sql.sql
```

**Verify tagging worked:**

```sql
SELECT 
    agent_label, 
    COUNT(*) as count,
    CASE 
        WHEN instance_id IS NULL THEN 'NULL'
        ELSE 'SET'
    END as instance_status
FROM observations 
GROUP BY agent_label, instance_id IS NULL
ORDER BY count DESC;
```

**Expected result:**
- `arty` : X observations (your current instance)
- `pre-v2.7.0` : Y observations (historical data) OR 
- `arty` : X+Y observations (if you tagged all as your instance)

---

### Multi-Instance Setup (New)

**Option A: Server + Client Setup**

```bash
# On database server (once)
./server-setup.sh

# On each OpenClaw machine
./client-setup.sh
```

**Option B: Migrate Local to Remote**

```bash
# 1. Export local database
pg_dump -h localhost -U postgres -d openclaw_memory > migration.sql

# 2. Import to shared server
psql -h 192.168.1.100 -U openclaw_user -d openclaw_memory < migration.sql

# 3. Update local config
# Edit ~/.config/pg-memory/config.env
# PG_MEMORY_HOST=192.168.1.100
```

### New Python Methods

```python
from pg_memory import PostgresMemory

mem = PostgresMemory()

# Access instance info
print(mem.instance_id)   # 'f47ac10b-...'
print(mem.agent_label)   # 'arty'

# Get stats by instance
stats = mem.get_instance_stats()
for stat in stats:
    print(f"{stat['agent_label']}: {stat['observation_count']} observations")

# Capture with auto-tracking
mem.capture(
    content="Test observation",
    tags=["test"]
    # instance_id and agent_label auto-added
)
```

---

## v2.5.0 → v2.6.0

**Upgrade Type:** Code-only (no database migration required)

### What's New in v2.6.0

1. **Duplicate Detection** — Check for similar observations before inserting
2. **Tag Autocomplete** — Suggest tags based on content or existing tags  
3. **Backup & Restore** — Full database backup and restore functionality
4. **JSON Export/Import** — Machine-readable data portability
5. **Install Script** — One-command installation for new users

### Upgrade Steps

```bash
# 1. Navigate to your pg-memory directory
cd pg-memory

# 2. Pull the latest code
git pull origin main

# 3. Verify the upgrade
python3 scripts/pg-memory-cli --version
# Expected: pg-memory v2.6.0

# 4. Test new features
pg-memory-cli duplicate "test content" --threshold 0.8
pg-memory-cli tags --content "test"
```

### No Database Changes Required

v2.6.0 uses your existing database schema. No migration scripts needed.

### Verify New Features Work

```python
# Test duplicate detection
from pg_memory import PostgresMemory

mem = PostgresMemory()

# Should find similar observations
duplicates = mem.find_similar("test query", min_similarity=0.5)
print(f"Found {len(duplicates)} similar observations")

# Test tag suggestions
tags = mem.suggest_tags("Netflix streaming merger")
print(f"Suggested tags: {tags}")

# Test backup
from pg_memory import backup
path = backup()
print(f"Backup created: {path}")
```

---

## v2.4.x → v2.5.0

**Upgrade Type:** Database migration required

### What's New in v2.5.0

- **Table Partitioning** — `raw_exchanges` table partitioned by month
- **Performance indexes** — 13 new indexes on observations
- **Auto-trigger** — Automatic partition creation

### Upgrade Steps

```bash
# 1. Pull latest code
git pull origin main

# 2. Run migration script
./scripts/pg_memory.py --version
```

### Database Migration

```bash
# Apply partitioning migration using your PostgreSQL credentials
psql -U [your_user] -d openclaw_memory -f scripts/schema_v2_5_partitioning.sql
```

### Verify Migration

```sql
-- Check partitions exist
SELECT schemaname, tablename 
FROM pg_tables 
WHERE tablename LIKE 'raw_exchanges_%';
```

---

## v2.0 → v2.4.x

**Upgrade Type:** Database migration required

### Upgrade Steps

```bash
# 1. Backup your data first
pg_dump -U [user] -d openclaw_memory > backup_pre_24.sql

# 2. Pull latest code
git pull origin main

# 3. Run migration
python3 scripts/pg_memory.py
```

---

## Troubleshooting

### "pg-memory-cli: command not found"

```bash
# Make CLI executable
chmod +x scripts/pg-memory-cli

# Or use full path
./scripts/pg-memory-cli --version
```

### "ModuleNotFoundError: No module named 'pg_memory'"

```bash
# Ensure scripts directory is in Python path
cd scripts
python3 pg-memory-cli --version
```

### PostgreSQL Connection Issues

```bash
# Verify PostgreSQL is running
brew services list | grep postgresql

# Expected: postgresql@18 started
```

---

## Quick Reference

| From Version | To Version | Action Required |
|--------------|------------|-----------------|
| v2.6.0 | v2.7.0 | Run `schema_v2_7_multi_instance.sql` |
| v2.5.0 | v2.6.0 | `git pull` only |
| v2.4.x | v2.5.0 | Run `schema_v2_5_partitioning.sql` |
| v2.0 | v2.4.x | Run `pg_memory.py` for auto-migration |
| < v2.0 | v2.0+ | Fresh install recommended |

---

## Need Help?

- **Check version:** `pg-memory-cli --version`
- **Test connection:** `pg-memory-cli status`
- **Full documentation:** See `README.md` or `SKILL.md`

---

*Last updated: v2.6.0*
