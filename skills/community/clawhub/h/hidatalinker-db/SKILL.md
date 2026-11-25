---
name: hidatalinker-db
description: >-
  Operate the local HiDataLinker desktop database app to inspect saved MySQL,
  PostgreSQL, SQL Server, and Oracle connections. Use when the user asks to
  query, inspect, describe, or explain a database that HiDataLinker manages,
  or mentions 查库, 表结构, SQL, HiDataLinker, or this database client. Do not
  use for writes, dumps, migrations, or creating connections.
---

# HiDataLinker database skill

HiDataLinker owns the saved connections and the live sessions. This skill drives that desktop app. It does not open its own database driver and it does not take a connection string.

## Before any call

1. The HiDataLinker window must be open. If a tool says it is not running, ask the user to open the app. Do not try to connect with a host, user, or password yourself.
2. The MCP service must be on. In HiDataLinker open **Settings** and turn on **MCP service** / **MCP 服务**. The same switch is on the activity bar. If a tool returns `MCP service is turned off in HiDataLinker settings`, ask the user to turn that switch on. Turning it off rejects tool calls; it does not remove saved connections.
3. Use a saved `connectionId` from `list_connections`. Never ask the user for a database password. Never read `~/.hidatalinker/connections/` or `~/.hidatalinker/agent/endpoint.json`. The MCP process reads the endpoint itself.
4. If `connect` says the connection has no saved password, ask the user to connect that profile once in the desktop app. Do not request the password in chat.

## How to call

Prefer the `hidatalinker-db` MCP server. Its tools are the only operations this skill may use. Tool arguments and results are JSON.

Cursor (`.cursor/mcp.json`) and Claude Code (`~/.claude.json` or the project's MCP config):

```json
{
  "mcpServers": {
    "hidatalinker-db": {
      "command": "skills/hidatalinker-db/scripts/run-agent-mcp.sh"
    }
  }
}
```

Use an absolute path to the script when the skill is installed outside this repository. The script runs `src-tauri/target/debug/agent-mcp` or `agent-mcp` from `~/.hidatalinker/bin`. Build it with:

```sh
cargo build --bin agent-mcp --manifest-path src-tauri/Cargo.toml
mkdir -p ~/.hidatalinker/bin
cp src-tauri/target/debug/agent-mcp ~/.hidatalinker/bin/agent-mcp
```

The packaged desktop binary also accepts `--agent-mcp` and speaks the same protocol. On Windows, register `agent-mcp.exe`, not the windowed app.

A service that cannot load MCP can `POST http://127.0.0.1:<port>/v1/tools/<name>` with `Authorization: Bearer <token>`. The desktop app writes `port` and `token` to `~/.hidatalinker/agent/endpoint.json` (owner-read only) when it starts. Do not print that token into the conversation.

## Work order

1. `list_connections`. Pick the saved connection by name, engine, host, and port. The list has no username and no password.
2. If `connected` is false, call `connect` with that id. The same session then shows as connected in the desktop window.
3. `list_databases`, then `list_tables` / `list_views` / `get_columns` / `get_ddl` before writing a query. Do not guess column names.
4. `preview_table` for a small page, or `query` for one read-only statement.
5. Answer from the tool result. Mention when the result is truncated.

## query rules

`query` accepts one statement that starts with `SELECT`, `WITH`, `EXPLAIN`, `SHOW`, `DESCRIBE`, `DESC`, `TABLE`, or `VALUES`.

- A `WITH` query must end in `SELECT`, `TABLE`, or `VALUES`.
- Do not send a second statement, even after a comment.
- Do not disguise a write as a query. `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, `MERGE`, `REPLACE INTO`, `SELECT … INTO`, `FOR UPDATE`, and file functions such as `pg_read_file` or `LOAD_FILE` are rejected.
- Pass `schema` when the statement should run in a specific database or schema.
- The engine caps result rows at 5000. `preview_table` caps `limit` at 1000.

This skill cannot create or delete connections, dump, migrate, or change data. If the user asks for a write, say that agent access is read-only and they can run the change in the HiDataLinker SQL editor.

## Tool catalog

See [references/tools.md](references/tools.md) for arguments. Names:

- `list_connections`
- `connect`
- `list_databases`
- `list_tables`
- `list_views`
- `list_indexes`
- `list_triggers`
- `list_routines`
- `get_columns`
- `get_ddl`
- `preview_table`
- `query`
