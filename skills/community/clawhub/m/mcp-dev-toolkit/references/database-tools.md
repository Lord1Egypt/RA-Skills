# Database MCP Tool Patterns

## PostgreSQL

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import pg from "pg";

const pool = new pg.Pool({ connectionString: process.env.DATABASE_URL });

server.tool("pg_query", { sql: z.string().describe("SQL query to execute") }, async ({ sql }) => {
  // Safety: only allow SELECT
  if (!sql.trim().toUpperCase().startsWith("SELECT")) {
    return { content: [{ type: "text", text: "Error: Only SELECT queries allowed" }] };
  }
  const result = await pool.query(sql);
  return { content: [{ type: "text", text: JSON.stringify(result.rows, null, 2) }] };
});

server.tool("pg_list_tables", {}, async () => {
  const result = await pool.query("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'");
  return { content: [{ type: "text", text: result.rows.map(r => r.table_name).join("\n") }] };
});

server.tool("pg_describe_table", { table: z.string() }, async ({ table }) => {
  const result = await pool.query(
    "SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name = $1",
    [table]
  );
  return { content: [{ type: "text", text: JSON.stringify(result.rows, null, 2) }] };
});
```

## SQLite

```python
import sqlite3
from mcp.server import Server

server = Server("sqlite-tools")

@server.tool("sqlite_query")
async def sqlite_query(sql: str) -> str:
    """Execute a SQL query against the SQLite database."""
    if not sql.strip().upper().startswith("SELECT"):
        return "Error: Only SELECT queries allowed"
    conn = sqlite3.connect(os.environ.get("SQLITE_PATH", "data.db"))
    cursor = conn.execute(sql)
    rows = [dict(zip([d[0] for d in cursor.description], row)) for row in cursor.fetchall()]
    conn.close()
    return json.dumps(rows, indent=2)
```

## MongoDB

```typescript
server.tool("mongo_find", {
  collection: z.string(),
  query: z.record(z.any()).default({}),
  limit: z.number().default(10)
}, async ({ collection, query, limit }) => {
  const docs = await db.collection(collection).find(query).limit(limit).toArray();
  return { content: [{ type: "text", text: JSON.stringify(docs, null, 2) }] };
});
```
