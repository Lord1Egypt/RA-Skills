
#### Method 3: pipx

Suitable for global installation.

```bash
pipx install postgres-mcp
postgres-mcp "postgresql://user:pass@host:5432/dbname"
```

### 3. Configure MCP Connection

Configure connection based on the client and transport method the user is using.

#### Claude Desktop (stdio mode)

Edit configuration file:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

**Docker method**:

```json
{
  "mcpServers": {
    "postgres": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "ghcr.io/crystaldba/postgres-mcp:latest",
        "postgresql://user:pass@host.docker.internal:5432/dbname"
      ]
    }
  }
}
```

**Python method**:

```json
{
  "mcpServers": {
    "postgres": {
      "command": "uv",
      "args": [
        "run",
        "postgres-mcp",
        "postgresql://user:pass@localhost:5432/dbname"
      ]
    }
  }
}
```

#### Cursor (stdio mode)

Edit `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "postgres": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "ghcr.io/crystaldba/postgres-mcp:latest",
        "postgresql://user:pass@host.docker.internal:5432/dbname"
      ]
    }
  }
}
```

#### SSE Mode (any client)

If using SSE mode, configure HTTP endpoint:

```json
{
  "mcpServers": {
    "postgres": {
      "url": "http://localhost:8000/sse"
    }
  }
}
```

### 4. Verification and Prompts

1. **Prompt user to restart client** — MCP configuration changes require restart to load new MCP tools
2. After restart, check available MCP tools list to confirm postgres-mcp tools are loaded
3. Verification successful → Can start using other postgres skills

## Configuration Options

### Read-Only Mode

Add `--read-only` parameter to enable read-only mode, allowing only SELECT queries:

```bash
postgres-mcp --read-only "postgresql://..."
```

### Environment Variables

- `DATABASE_URL` — Database connection string
- `POSTGRES_MCP_READ_ONLY` — Set to `true` to enable read-only mode
- `POSTGRES_MCP_QUERY_TIMEOUT` — Query timeout (seconds)

## Failure Handling

| Scenario | Solution |
|---|---|
| Docker not installed | Recommend installing Docker or switch to Python method |
| Python version too low | Requires Python 3.12+, recommend upgrading or use Docker |
| Database connection failed | Check connection string, network, firewall, database permissions |
| Password with special characters causing connection failure | Use URL encoding (e.g., `@` → `%40`), refer to encoding table above |
| Tools still unavailable after configuration | Prompt to restart client session |
| Docker cannot access localhost database | Use `host.docker.internal` or `172.17.0.1` |

## Common Error Examples

### Error 1: Password special characters not encoded

**Error log**:
```
WARNING  error connecting in 'pool-1': failed to resolve host '1@192.168.22.113'
```

**Cause**: `@` in password `pass@1` is mistaken as host separator

**Solution**: Encode password as `pass%401`

### Error 2: Port already in use

**Error log**:
```
ERROR: [Errno 98] error while attempting to bind on address ('0.0.0.0', 8001): address already in use
```

**Solution**:
```bash
# Find process using port
lsof -i :8001

# Kill process
kill <PID>

# Or use different port
postgres-mcp --sse-port 8002 "postgresql://..."
```

### Error 3: Database connection refused

**Error log**:
```
WARNING  Could not connect to database: Connection refused
```

**Checklist**:
- [ ] Is database service running
- [ ] Does firewall allow connection
- [ ] Does PostgreSQL `pg_hba.conf` allow remote connections
- [ ] Are username and password correct
