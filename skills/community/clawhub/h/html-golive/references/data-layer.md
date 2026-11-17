# Data layer — detailed notes

Extended companion to the *Pages with data* section of `SKILL.md`. Read
this when a page needs more than basic CRUD.

## How injection is decided

At publish time golive scans the HTML:

- the page calls `TemplateAPI.*` → the TemplateAPI layer is injected
- `--data-model CODE` is passed → injected even if no call is detected
  yet (useful when the JS is added later)
- the page calls `SupabaseAPI.*` → the Supabase direct-table layer is
  injected

Injection is idempotent: republishing strips the previous block first,
so the layer never accumulates. The block is marked
`SYSTEM INJECTED CODE — DO NOT MODIFY`; edits there are lost on the next
publish. Keep application logic outside it.

If the configured backend is unusable (e.g. `data.backend: supabase`
with no keys) a **stub** is injected instead. The page still publishes
and still loads; every data call rejects with a console message naming
the exact fix. Publishing is never blocked by a missing backend.

## modelCode

A `modelCode` namespaces rows inside the templates table. One code per
application is the usual shape.

```bash
golive publish app.html --data-model app_v1
golive publish app.html --data-model "app_v1,shared_v1"
```

With several codes, the first is the default and every method accepts an
explicit override:

```js
TemplateAPI.list({ modelCode: 'shared_v1', pageSize: 50 });
```

Calling without an explicit code when several are injected logs a warning
and uses the first. Passing a code that was not injected also warns —
check the spelling and the `--data-model` list.

Bump the version suffix (`app_v1` → `app_v2`) when a schema change would
break old rows; the old namespace stays readable.

## Row shape

`TemplateAPI` returns intranet-compatible field names, which differ from
the database columns:

| Returned field | Column | Notes |
|---|---|---|
| `templateId` | `id` | uuid string |
| `templateName` | `name` | unique per (modelCode, user) |
| `templateDesc` | `description` | |
| `templateContent` | `content` | **JSON string** — `JSON.parse` it |
| `templateContentVersion` | `version` | |
| `modelCode` | `model_code` | |
| `userId` | `user_id` | `''` when anonymous |
| `sortIndex` | `sort_index` | `sort(id, n)` adjusts it |
| `createTime` / `updateTime` | `created_at` / `updated_at` | |

`content` goes in as an object and comes back as a string. Writes accept
either; reads always give the string.

## Ready event

The layer mounts asynchronously and fires `templateapi:ready` on
`document`:

```js
document.addEventListener('templateapi:ready', function (e) {
  console.log('modelCodes:', e.detail.modelCodes);
  loadEverything();
});
```

Register the listener at parse time (a plain inline `<script>`), not
inside `window.onload` — the event may already have fired by then.

`window.TEMPLATE_CONFIG` and `TemplateAPI._config` expose the injected
configuration for debugging; `_blocked: true` means the stub is active.

## Paging and search

```js
TemplateAPI.listAll({ pageNo: 2, pageSize: 20 });          // page through
TemplateAPI.list({ templateName: 'draft_' });              // name prefix
```

`list` filters to the configured `userId`; `listAll` ignores it. With no
`data.user_id` set, every row is anonymous and the two behave alike.

`pageSize` is capped server-side (200). For large sets, page rather than
requesting everything.

## Backends compared

### sqlite (default)

Rows live in `$GOLIVE_HOME/data.db`; the table is created on first
access. The page talks to `golive serve`'s `/api/data/<table>` endpoint
using the same PostgREST wire format, so nothing in the page changes
between backends.

Consequences:

- the page **must** be loaded through `golive serve`; `file://` has no
  endpoint to reach
- no API key is embedded in the HTML
- anyone who can reach the server can call the endpoint — put auth or a
  reverse proxy in front for sensitive data
- data does not travel with the HTML: a page copied to another golive
  instance starts empty

Override the location with `data.sqlite.path`. If the site is served
from a different origin than the golive server, set `data.api_base` to
the absolute endpoint URL.

### postgres

Rows live in your own PostgreSQL. Architecturally identical to sqlite: the
server owns the connection and the page still calls
`golive serve`'s `/api/data/<table>`, so **the DSN never reaches the
browser** and the page JS is byte-for-byte the same as in sqlite mode.

```yaml
data:
  backend: postgres
registry:
  backend: postgres    # optional — site metadata in Postgres as well
```

```bash
pip install 'html-golive[postgres]'
export GOLIVE_PG_DSN='postgresql://user:pass@host:5432/dbname'
```

Consequences:

- the page **must** be loaded through `golive serve` (same as sqlite)
- no API key and no DSN in the HTML
- tables are created on first use; `content` is stored as JSONB
- the DSN lives in the environment, never in `golive.yaml`
- multiple golive instances can share one database — unlike sqlite
- without the `[postgres]` extra, startup fails with the exact install
  command instead of degrading silently


### supabase

Rows live in your Supabase project; the page calls PostgREST directly
with the **anon key embedded in the HTML**.

```yaml
supabase:
  url: https://YOURPROJECT.supabase.co
data:
  backend: supabase
```

```bash
export GOLIVE_SUPABASE_ANON_KEY=...
export GOLIVE_SUPABASE_SERVICE_KEY=...   # CLI only, optional
golive db init --print-sql               # run this SQL in Supabase
```

Row Level Security is **mandatory**: the anon key is public the moment
the page is. The generated SQL includes permissive example policies —
tighten them before real use. Upside: several machines and a page hosted
anywhere can share one dataset.

### none

`data.backend: none` disables the layer. Pages still publish; data calls
reject with a hint. Use when a page should demonstrably have no
persistence.

## Switching backends

Backend choice is baked into the published HTML at publish time.
Changing `golive.yaml` does nothing to already-published pages —
republish them:

```bash
golive publish app.html --update app --data-model app_v1
```

Rows are **not** migrated between backends. Export from the old one
(`golive data list --model-code X --limit 1000`) and re-import if the
content must survive the switch.

## Server-side and CLI access

```bash
golive data list --model-code app_v1 --limit 100
```

The CLI uses the same store the browser layer reaches, so it is the
quickest way to seed fixtures or inspect what a page wrote. The admin
portal's Data view (superadmin only) offers the same operations with a UI.

## `window.SupabaseAPI`

For pages managing their own Supabase tables rather than the templates
table. Requires Supabase configuration regardless of `data.backend`, and
the same RLS warning applies with more force: arbitrary tables are
exposed to whatever the anon key may do.

| Method | Purpose |
|---|---|
| `init()` / `isReady()` / `onReady(fn)` | lifecycle |
| `getUser()` / `logout()` | session |
| `query(table, opts)` | select with PostgREST filters |
| `insert(table, rows)` / `update(table, match, values)` / `delete(table, match)` | writes |

## Debug checklist

1. `TemplateAPI is not defined` → the layer was not injected. Republish
   with `--data-model`, then confirm the `<script>` is in the served
   HTML (view source, not the local file).
2. Calls reject immediately → read the console message; it names the
   cause. `_blocked: true` in `TemplateAPI._config` confirms stub mode.
3. HTTP 401/403 (supabase) → RLS policies reject the anon key.
4. HTTP 404 on `/api/data/...` (sqlite / postgres / mysql) → the page is not being
   served by golive, or `data.backend` on the server is not a server-proxied
   backend (`sqlite`, `postgres` or `mysql`).
5. Writes succeed but reads look empty → `list` is user-scoped; try
   `listAll`, or check `modelCode` matches what was written.
