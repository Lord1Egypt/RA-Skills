# Migrating from Local to Remote PostgreSQL

Migrate your pg-memory database from a local PostgreSQL instance to a remote server (e.g., Synology NAS).

---

## Quick Migration (2 Steps)

### Step 1: Export Local Database

```bash
# On your local machine (current pg-memory)

# 1. Create backup directory
mkdir -p ~/pg-memory-backup

# 2. Export full database
pg_dump -h localhost -p 5432 -U postgres -d openclaw_memory > ~/pg-memory-backup/migration_$(date +%Y%m%d).sql

# Alternative: Compressed (recommended for large databases)
pg_dump -h localhost -p 5432 -U postgres -d openclaw_memory | gzip > ~/pg-memory-backup/migration_$(date +%Y%m%d).sql.gz

# Verify
ls -lh ~/pg-memory-backup/
```

### Step 2: Import to Remote Server

**On your Synology NAS (or remote server):**

```bash
# SSH into your NAS
ssh admin@100.98.247.27

# Install PostgreSQL if not installed
# (On Synology: Package Center → PostgreSQL)

# Create database
sudo -u postgres createdb openclaw_memory

# Enable extensions
sudo -u postgres psql -d openclaw_memory -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"
sudo -u postgres psql -d openclaw_memory -c "CREATE EXTENSION IF NOT EXISTS \"pg_trgm\";"
sudo -u postgres psql -d openclaw_memory -c "CREATE EXTENSION IF NOT EXISTS \"vector\";"

# Create user
sudo -u postgres createuser -P openclaw_user
# Enter password when prompted

# Grant privileges
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE openclaw_memory TO openclaw_user;"
```

**Import the data from your backup:**

```bash
# Copy backup file to NAS
scp ~/pg-memory-backup/migration_*.sql admin@100.98.247.27:/tmp/

# On NAS, import
sudo -u postgres psql -d openclaw_memory < /tmp/migration_*.sql

# Or if compressed:
gunzip -c /tmp/migration_*.sql.gz | sudo -u postgres psql -d openclaw_memory
```

### Step 3: Reconfigure Client

**On your local machine:**

```bash
# 1. Backup current config
cp ~/.config/pg-memory/config.env ~/.config/pg-memory/config.env.local.backup

# 2. Update config
# Edit ~/.config/pg-memory/config.env:

PG_MEMORY_HOST=100.98.247.27
PG_MEMORY_PORT=5432
PG_MEMORY_DB=openclaw_memory
PG_MEMORY_USER=openclaw_user
PG_MEMORY_PASSWORD=your_syndb_password
OPENCLAW_NAME=arty
```

### Step 4: Test Connection

```bash
cd ~/.openclaw/workspace/skills/pg-memory
python3 -c "
from scripts.pg_memory import PostgresMemory
mem = PostgresMemory()
result = mem.capture(
    content='Migration test - connected to remote database',
    tags=['migration', 'test']
)
print(f'✅ Connected! Instance: {result.get(\"instance_id\", \"N/A\")[:8]}...')
print(f'✅ Test observation: {result.get(\"id\", \"N/A\")[:8]}...')
"
```

### Step 5: Verify Data

```bash
# Check data migrated
psql -h 100.98.247.27 -U openclaw_user -d openclaw_memory -c "
SELECT 
    agent_label,
    COUNT(*) as observations,
    MAX(timestamp) as last_capture
FROM observations
GROUP BY agent_label
ORDER BY last_capture DESC;
"
```

---

## Synology NAS Specific

### Install PostgreSQL on Synology

```bash
# Via SSH

# Option 1: Using Package Center GUI
# 1. Open DSM → Package Center
# 2. Search "PostgreSQL"
# 3. Install version 14+ (with pgvector support)

# Option 2: Using Docker (more control)
docker run -d \
    --name pg-memory \
    -e POSTGRES_DB=openclaw_memory \
    -e POSTGRES_USER=openclaw_user \
    -e POSTGRES_PASSWORD=your_password \
    -p 5432:5432 \
    -v /volume1/pg-memory-data:/var/lib/postgresql/data \
    ankane/pgvector:latest
```

### Enable Remote Access on Synology

**Edit postgresql.conf:**
```bash
# Find config (location varies)
sudo find / -name "postgresql.conf" 2>/dev/null

# Example: /var/packages/Postgresql/target/var/postgresql.conf

# Edit:
listen_addresses = '*'
port = 5432
```

**Edit pg_hba.conf:**
```bash
# Find location
sudo find / -name "pg_hba.conf" 2>/dev/null

# Add:
host  all  all  0.0.0.0/0  md5

# More secure (restrict to your network):
host  all  all  192.168.1.0/24  md5
host  all  all  100.98.247.0/24  md5
```

**Restart:**
```bash
# DSM → Package Center → PostgreSQL → Stop/Start
# Or
sudo synopkgctl restart PostgreSQL
```

### Synology Firewall

```bash
# DSM → Control Panel → Security → Firewall
# Allow port 5432
```

---

## Alternative: pgAdmin Migration (GUI)

If you prefer GUI:

1. **Install pgAdmin 4** on your local machine
2. **Connect to both databases:**
   - Source: localhost:5432/openclaw_memory
   - Target: 100.98.247.27:5432/openclaw_memory
3. **Right-click** source → Backup
4. **Right-click** target → Restore
5. **Update config.env** to point to remote

---

## Connection Testing

```bash
# Test from local machine
psql -h 100.98.247.27 -U openclaw_user -d openclaw_memory -c "SELECT version();"

# Should return PostgreSQL version
```

**If connection fails:**
| Issue | Fix |
|-------|-----|
| Connection refused | Check firewall on NAS |
| Connection timeout | Check `listen_addresses = '*'` in postgresql.conf |
| Password failed | Reset with `ALTER USER openclaw_user WITH PASSWORD 'newpass';` |
| Permission denied | Run `GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO openclaw_user;` |

---

## Rollback (If Needed)

```bash
# Restore local config
cp ~/.config/pg-memory/config.env.local.backup ~/.config/pg-memory/config.env

# Back to local PostgreSQL
PG_MEMORY_HOST=localhost
```

---

## Your Specific Setup

**Target:** `100.98.247.27:5432` (Synology NAS)

**Connection test from your machine:**
```bash
# Check if reachable
nc -zv 100.98.247.27 5432

# Or
psql -h 100.98.247.27 -U openclaw_user -d openclaw_memory -c "SELECT 1;"
```

**Notes:**
- Synology PostgreSQL package may use port 5432 or 5433 (check)
- User `admin` has limited PostgreSQL access — use `postgres` or created `openclaw_user`
- pgvector extension requires manual install on Synology (or use Docker)

---

*Need help? Check logs: `/var/packages/PostgreSQL/target/var/log/`*
