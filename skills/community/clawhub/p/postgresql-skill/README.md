# PostgreSQL Skill

Pure Python PostgreSQL operations using psycopg2.

## Quick Start

```bash
# 1. Install dependencies
pip install psycopg2-binary pyyaml

# 2. Configure
cp config.example.yaml config.yaml
vim config.yaml

# 3. Use
python scripts/pgsql_skill.py list-tables
python scripts/pgsql_skill.py describe-table users
python scripts/pgsql_skill.py execute-sql "SELECT * FROM users LIMIT 10"
python scripts/pgsql_skill.py schema-summary
```

## Commands

| Command | Description | Output |
|---------|-------------|--------|
| `list-tables` | List all tables | JSON |
| `describe-table <table>` | Describe table | JSON |
| `execute-sql "<SQL>"` | Execute SQL | JSON |
| `schema-summary` | Schema summary | Text |

## Safety

- Blocked: DROP/TRUNCATE/ALTER
- INSERT: single row only
- UPDATE/DELETE: WHERE required

See [SKILL.md](SKILL.md) for details.
