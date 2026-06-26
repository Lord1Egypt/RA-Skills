# postgres-mcp-skills

Agent Skills collection based on [postgres-mcp](https://github.com/crystaldba/postgres-mcp), providing complete management and optimization capabilities for PostgreSQL databases. Compatible with [Agent Skills Open Standard](https://agentskills.io), supporting platforms like OpenClaw and Claude Code.

## Features

| Skill | Description |
|---|---|
| **setup-postgres-mcp** | Install and deploy postgres-mcp service |
| **pg-health** | Database health check (index health, connection utilization, cache, vacuum, replication lag, etc.) |
| **pg-index-tuning** | Index optimization recommendations and performance tuning |
| **pg-query-plan** | Query execution plan analysis and optimization |
| **pg-schema** | Database schema query and intelligent SQL generation |
| **pg-execute** | Safe SQL execution (supports read-only mode and access control) |

## Prerequisites

- [postgres-mcp](https://github.com/crystaldba/postgres-mcp) service installed and running
- If not installed, use the `setup-postgres-mcp` skill for guided setup

## Installation

### OpenClaw

After downloading this project locally, copy the `SKILL.md` file and `reference/` directory to OpenClaw's SKILLS directory and restart the session.

### Claude Code

```bash
# Project level
cp SKILL.md .claude/skills/postgres.md
cp -r reference/ .claude/skills/postgres-reference/

# Or global level
cp SKILL.md ~/.claude/skills/postgres.md
cp -r reference/ ~/.claude/skills/postgres-reference/
```

Use `/postgres` to invoke, it will automatically route to the appropriate functional module based on your intent.

## Usage Examples

```
# First time use: Install MCP service
/setup-postgres-mcp

# Health check
/pg-health

# Index optimization
/pg-index-tuning

# Query plan analysis
/pg-query-plan

# Execute SQL
/pg-execute
```

## License

MIT
