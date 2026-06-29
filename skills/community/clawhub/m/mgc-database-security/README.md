# Database Credential Security (Zero‑Exposure Edition)

Secure database credential management using MGC Blackbox. Supports MySQL, PostgreSQL, SQLite, MariaDB and more.

## What This Skill Does

This skill provides a pattern for managing database credentials securely:
- Store credentials encrypted in MGC Blackbox
- Retrieve at runtime without AI seeing plaintext
- Execute database operations safely

## Prerequisites

- Python 3.10+
- pip install mgc-blackbox
- MGC service running

## Quick Start

### 1. Install MGC

```bash
pip install mgc-blackbox
mgc
```

### 2. Store Credentials

Create `db_creds.json`:

```json
{
  "host": "localhost",
  "port": 3306,
  "database": "my_db",
  "user": "db_user",
  "password": "your_password"
}
```

Store in MGC:

> **Important:** Use **MCP tools** for AI agents. CLI may have port conflicts.

**Recommended (MCP):** Use `mgc_save` tool  
**Alternative (CLI):**
```bash
mgc_save info_type=config info_owner=my_database < db_creds.json
```

### 3. Use in Your Script

Your local script retrieves credentials from MGC, connects to database, and executes queries - all without exposing credentials to AI.

## What's Inside

- Database credential storage pattern
- MGC API reference
- Conceptual connection code
- Security best practices

## Security

- Credentials never exposed to AI
- Encrypted storage via MGC
- Runtime credential retrieval only
- No plaintext in logs

## License

MIT