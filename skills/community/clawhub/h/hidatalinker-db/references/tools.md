# HiDataLinker agent tools

All tools except `list_connections` require `connectionId` from `list_connections`. Call `connect` first when `connected` is false.

`list_connections` returns `id`, `name`, `engine`, `host`, `port`, `connected`.

| Tool | Required arguments | Notes |
| --- | --- | --- |
| `list_connections` | none | No secrets |
| `connect` | `connectionId` | Uses the password saved in the desktop app |
| `list_databases` | `connectionId` | Databases or schemas |
| `list_tables` | `connectionId`, `schema` | |
| `list_views` | `connectionId`, `schema` | |
| `list_indexes` | `connectionId`, `schema` | |
| `list_triggers` | `connectionId`, `schema` | |
| `list_routines` | `connectionId`, `schema` | Functions and procedures |
| `get_columns` | `connectionId`, `schema`, `table` | Tables and views |
| `get_ddl` | `connectionId`, `schema`, `kind`, `name` | `kind`: `table`, `view`, `index`, `trigger`, `function`, `procedure` |
| `preview_table` | `connectionId`, `schema`, `table` | Optional `limit` (max 1000), `offset` |
| `query` | `connectionId`, `sql` | Optional `schema`. One read-only statement. Max 5000 rows |

HTTP shape, used by the MCP proxy:

```http
POST /v1/tools/query HTTP/1.1
Authorization: Bearer <token>
Content-Type: application/json

{"connectionId":"<id>","schema":"app","sql":"SELECT id FROM orders WHERE paid = 0"}
```

Success:

```json
{"ok":true,"result":{}}
```

Failure:

```json
{"ok":false,"error":"read-only queries cannot use DELETE"}
```

`GET /v1/health` needs no token and returns `ok`, `enabled`, and `port`.
