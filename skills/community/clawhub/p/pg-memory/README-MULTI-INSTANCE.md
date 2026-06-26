# Multi-Instance pg-memory Setup

Deploy pg-memory across multiple OpenClaw instances sharing one PostgreSQL database.

---

## Architecture

```
┌────────────────────────────────────────────┐
│              DATABASE SERVER               │
│         (PostgreSQL + pgvector)            │
│                                            │
│  • One database: openclaw_memory          │
│  • Automatic instance tracking              │
│  • Concurrent access safe                 │
└──────────────┬─────────────────────────────┘
               │ Network
    ┌──────────┼──────────┬──────────┐
    │          │          │          │
┌───▼───┐ ┌────▼───┐ ┌───▼───┐ ┌───▼───┐
│ Arty  │ │ Brodie │ │ Maya  │ │ Rich  │
│Client │ │ Client │ │Client │ │Client │
└───────┘ └────────┘ └───────┘ └───────┘

Each client has:
• Unique instance ID (auto-generated)
• Human-readable agent name
• Connection config to shared DB
```

---

## Quick Start

### Step 1: Server Setup (Run Once)

On your database machine:

```bash
# Clone pg-memory
git clone https://github.com/pottertech/pg-memory.git
cd pg-memory

# Run server setup
./server-setup.sh
```

Follow prompts to:
- Install PostgreSQL (if needed)
- Install pgvector extension
- Create database and user
- Set password

**Save the connection string — you'll need it for clients.**

---

### Step 2: Client Setup (Run on Each OpenClaw)

On Arty's machine:
```bash
# Clone pg-memory
git clone https://github.com/pottertech/pg-memory.git
cd pg-memory

# Run client setup
./client-setup.sh
```

Follow prompts:
- Enter database host (e.g., `192.168.1.100`)
- Enter password from server setup
- Choose agent name: `arty`

**Instance ID auto-generated on first run.**

---

On Brodie's machine:
```bash
./client-setup.sh
# Agent name: brodie
```

On Maya's machine:
```bash
./client-setup.sh
# Agent name: maya
```

Each machine gets a **unique instance ID** automatically.

---

## How It Works

### Instance Identification

| Field | Source | Example |
|-------|--------|---------|
| `agent_label` | User-defined | `arty`, `brodie`, `maya` |
| `instance_id` | Auto-generated UUID | `f47ac10b-58cc-4372-a567-0e02b2c3d479` |

**Storage:**
- **macOS:** `~/Library/Application Support/pg-memory/config.env`
- **Linux:** `~/.config/pg-memory/config.env`
- **Windows:** `%APPDATA%/pg-memory/config.env`
- **All platforms:** `instance.json` — unique ID (auto-created, never changes)

### Concurrent Safety

| Operation | Safe? | Notes |
|-----------|-------|-------|
| Capture observations | ✅ Yes | Auto-unique IDs |
| Read/search | ✅ Yes | MVCC handles this |
| Link observations | ✅ Yes | UPSERT pattern |
| Update same observation | ⚠️ Race | Last-writer-wins |

---

## Usage

### From Python

```python
from pg_memory import PostgresMemory

mem = PostgresMemory()  # Auto-loads config

# Captures with this instance's ID
obs = mem.capture(
    content="Important note",
    tags=["test"],
    agent_label="arty"  # Will be set from env
)

print(obs['instance_id'])  # This machine's UUID
```

### From CLI

```bash
# Auto-uses configured agent name
pg-memory capture "Meeting notes" --tags project

# Search all instances can see
pg-memory search "important"
```

### Query by Instance

```sql
-- All Arty's observations
SELECT * FROM observations 
WHERE agent_label = 'arty';

-- Just this specific laptop
SELECT * FROM observations 
WHERE instance_id = 'f47ac10b-58cc-4372-a567-0e02b2c3d479';

-- All instances' data
SELECT agent_label, COUNT(*) 
FROM observations 
GROUP BY agent_label;
```

---

## Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `PG_MEMORY_HOST` | Database server IP/hostname | `localhost` |
| `PG_MEMORY_PORT` | PostgreSQL port | `5432` |
| `PG_MEMORY_DB` | Database name | `openclaw_memory` |
| `PG_MEMORY_USER` | Database username | `openclaw_user` |
| `PG_MEMORY_PASSWORD` | Database password | (none) |
| `OPENCLAW_NAME` | Human-readable agent name | `unknown` |

---

## Troubleshooting

### Connection Refused

```bash
# Check PostgreSQL is listening on all interfaces
# Edit postgresql.conf:
listen_addresses = '*'

# Check pg_hba.conf allows remote connections:
host  all  all  0.0.0.0/0  md5
```

### Permission Denied

```bash
# Grant privileges (on server)
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE openclaw_memory TO openclaw_user;"
```

### Instance ID Lost

If `~/.config/pg-memory/instance.json` is deleted:
- New ID generated on next run
- Old observations still in database but not linked to new ID
- **Keep backups of config files**

---

## Cloud Deployment

### AWS RDS PostgreSQL

1. Create RDS instance with PostgreSQL 15+
2. Enable pgvector extension (may need parameter group)
3. Note endpoint: `mydb.xyz.us-east-1.rds.amazonaws.com`
4. Use as `PG_MEMORY_HOST`

### Docker Compose

```yaml
version: '3.8'
services:
  pg-memory-db:
    image: ankane/pgvector:latest
    environment:
      POSTGRES_DB: openclaw_memory
      POSTGRES_USER: openclaw_user
      POSTGRES_PASSWORD: secure_password
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

---

## Security Checklist

- [ ] Use strong database password
- [ ] Restrict `pg_hba.conf` to specific IP ranges, not `0.0.0.0/0`
- [ ] Enable SSL for remote connections
- [ ] Firewall port 5432
- [ ] Regular backups with `pg_dump`
- [ ] Store config files securely (`chmod 600 ~/.config/pg-memory/config.env`)

---

## Migration from Single Instance

If you have existing pg-memory database and want to share:

```bash
# 1. Backup existing database
pg_dump -U postgres openclaw_memory > backup.sql

# 2. Move to server machine, restore
psql -U postgres -c "CREATE DATABASE openclaw_memory;"
psql -U openclaw_user openclaw_memory < backup.sql

# 3. Add instance_id column (if upgrading)
psql -U openclaw_user openclaw_memory -c "
  ALTER TABLE observations ADD COLUMN IF NOT EXISTS instance_id UUID;
  ALTER TABLE observations ADD COLUMN IF NOT EXISTS agent_label VARCHAR(100);
"

# 4. Run client-setup.sh on each machine
```

---

## FAQ

**Q: What if two machines have the same agent name?**  
A: Perfectly fine! The `instance_id` UUID distinguishes them. You can have multiple "arty" machines.

**Q: Can one OpenClaw use multiple databases?**  
A: Yes — instantiate with different configs: `PostgresMemory(host='db1')` and `PostgresMemory(host='db2')`

**Q: What happens if the database server goes down?**  
A: Clients queue writes locally (if configured) or fail gracefully. Data is not lost on clients.

**Q: Can I delete an instance's data?**  
A: Yes: `DELETE FROM observations WHERE instance_id = '...'` — but this affects all that machine's captures.

---

*Part of pg-memory v2.6.0 — Multi-Instance Support*
