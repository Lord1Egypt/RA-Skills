---
name: html-golive
slug: html-golive
displayName: html-golive
description: Publish, update and manage HTML pages on a self-hosted golive instance through the local `golive` CLI. golive runs entirely on the user's own machine or server — it is not a hosted service and has no relation to any online deployment platform or to any similarly named internal tool. Use when the user wants to put an HTML file, project directory or archive online on their own infrastructure, update or roll back a site they already published, give a static page real data persistence via `window.TemplateAPI`, or administer sites, owners and maintainers. Trigger phrases include "publish this page", "deploy this HTML", "put this on golive", "update the site", "roll it back", "golive".
version: 0.9.8
license: MIT
homepage: https://github.com/Songhonglei/html-golive
---

# html-golive

This Skill targets html-golive 0.9.8. Install the matching CLI from PyPI with `python -m pip install "html-golive==0.9.8"`, and keep the running service and installed Skill on the same version. Use the matching 0.9.8 release assets for manual Skill installation.

`golive` is a **self-hosted** static-HTML deployment tool. One command
turns a local HTML file into a URL served by the user's own machine.
Everything — sites, database, uploads — lives under `$GOLIVE_HOME`
(default `~/.golive/`). There is no vendor account, no cloud tenancy and
no remote control plane.

**Scope boundary — read this first.** This skill covers *only* the local
`golive` CLI documented here. If a command below is missing from
`golive --help`, you are looking at a different tool that happens to
share the name; stop and tell the user instead of guessing. Never
substitute another deployment platform's commands or URLs.

## Step 1 — always probe the environment first

Never assume a path, a port, a config value or that golive is installed.
Run this before your first action in a session:

```bash
golive --version          # installed? which version?
echo "$GOLIVE_HOME"       # empty means the default ~/.golive/
golive doctor             # home writable, registry readable, deps, port
golive list               # sites that already exist
```

Read the output before planning:

- `golive: command not found` → not installed. Suggest
  `pip install html-golive`, then stop; do not fabricate a path.
- `golive doctor` prints ❌ lines → fix those first; publishing on a
  broken home directory produces confusing failures.
- `golive list` shows an existing slug → updating is almost always what
  the user wants, not creating a second site.

The bundled skill and CLI are released together. If an installed skill
reports a different version, use `golive skill install --force --target
<skills-directory>` to refresh it (the old copy is backed up). For a
project virtual environment, activate it before running these commands.
Use `golive context` to inspect effective paths and backends.

For CodeBuddy / WorkBuddy projects, open the project in that agent and run
`golive skill install --target .codebuddy/skills` from its root. Reload the
project so the agent loads this skill. MySQL setup and acceptance:
`references/mysql.md`.

## Step 2 — core workflows

### Publish a new page

```bash
golive publish page.html --name "Report" --slug report
```

- `source` may be an HTML file, a project directory or a `.zip` /
  `.tar.gz` archive. For directories and archives add `--entry
  index.html` when the entry point is not obvious.
- `--slug report` makes the page reachable at `/report`. Without it the
  site is only addressable by its 32-char `site_id` at `/s/<site_id>`.
- `--name` defaults to the page `<title>`.
- `--owner alice@example.com` records who owns the site (drives the
  permission model below).
- `--style <name>` injects a built-in CSS theme; run `golive styles` to
  list them. Only use this when the user asks to restyle the page.
- Output includes `site_id`, `slug` and the URL. Report the URL back.

### Update an existing site

Updating means *republishing to the same site*, which also creates a
rollback snapshot. Find the target first:

```bash
golive list
golive publish page.html --update report      # slug or site_id
```

Do **not** publish a modified copy as a new site to "update" it — that
leaves two live pages and loses the snapshot chain.

### Roll back

```bash
golive rollback report --dry-run    # list snapshots, change nothing
golive rollback report              # restore the newest snapshot
golive rollback report --snapshot 20260130-120000
```

Always run `--dry-run` first and show the user the snapshot list before
restoring.

### Serve

```bash
golive serve --host 127.0.0.1 --port 8787  # explicit local access
golive serve --port 8787 --host 0.0.0.0
```

When `--host` or `--port` is omitted, saved settings and configuration
can change the listener. Pass both explicitly for a local verification.

`--host 0.0.0.0` exposes every published site to the whole network. Only
use it when the user explicitly asks to share, and when you do, say so
and recommend `GOLIVE_TOKEN` or OIDC (see *Permissions*) in the same
breath. It is a single-process stdlib server: put nginx or caddy in
front for TLS or real traffic.

### Preview locally without publishing

```bash
golive preview page.html            # live reload + style switcher
```

## Step 3 — pages with data (`window.TemplateAPI`)

golive can inject a JS data layer so a static page gets real read/write
persistence. Detection is automatic: if the HTML calls `TemplateAPI.*`,
publishing injects the layer. `--data-model <code>` names the storage
namespace (one per app is the norm):

```bash
golive publish app.html --slug notes --data-model notes_v1
```

The page must be served by `golive serve` for the data layer to work —
opening the HTML file directly from disk gives it no endpoint to call.

### Method reference

| Method | Arguments | Resolves to |
|---|---|---|
| `list(opts)` | `{modelCode?, pageNo?, pageSize?, templateName?, userId?}` | `{total, list: Template[]}` — current user only |
| `listAll(opts)` | same; `userId` ignored | `{total, list: Template[]}` — every user |
| `get(id)` | template id | `Template` |
| `create(tpl)` | `{name, content, modelCode?, desc?, version?}` | new id |
| `update(id, patch)` | patch: `name` / `desc` / `content` / `version` | id |
| `upsert(tpl)` | as `create`; matches an existing exact `name` | id |
| `delete(id)` | id | `null` |
| `sort(id, sortIndex)` | — | `null` |

A `Template` row carries `templateId`, `templateName`, `templateDesc`,
`templateContent` (a **JSON string** — parse it), `templateContentVersion`,
`modelCode`, `createTime`, `updateTime`.

### Copy-paste page skeleton

```html
<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Notes</title></head>
<body>
  <input id="note" placeholder="write something">
  <button onclick="save()">Save</button>
  <ul id="list"></ul>

  <script>
    function refresh() {
      TemplateAPI.listAll({ pageSize: 100 }).then(function (r) {
        var list = document.getElementById('list');
        var items = r.list.map(function (t) {
          var item = document.createElement('li');
          item.textContent = JSON.parse(t.templateContent).text;
          return item;
        });
        list.replaceChildren.apply(list, items);
      });
    }
    function save() {
      var text = document.getElementById('note').value;
      TemplateAPI.upsert({ name: 'note_' + Date.now(),
                           content: { text: text } }).then(refresh);
    }
    // wait for the injected layer before the first read
    document.addEventListener('templateapi:ready', refresh);
  </script>
</body></html>
```

Always gate the first call on `templateapi:ready`; calling at parse time
races the injection.

### Inspect and edit rows from the CLI

```bash
golive data list   --model-code notes_v1
golive data create --model-code notes_v1 --name seed --content '{"text":"hi"}'
golive data update --id <row-id> --content @payload.json
golive data delete --id <row-id>
```

## Step 4 — data backends

| Backend | When | Setup |
|---|---|---|
| `sqlite` | **default** | none — rows go to `$GOLIVE_HOME/data.db`, table auto-created |
| `postgres` | the user already has a PostgreSQL they want to use | `pip install 'html-golive[postgres]'` + `GOLIVE_PG_DSN` |
| `mysql` | an existing MySQL 8.4+ database | `pip install 'html-golive[mysql]'` + `GOLIVE_MYSQL_DSN` (MySQL 8.4+) |
| `supabase` | shared across machines, or the page is served elsewhere | Supabase project + schema + keys |
| `none` | disable the data layer entirely | opt-in only |

Stay on `sqlite` unless the user has a concrete reason to leave it.

To use an existing PostgreSQL (same shape as sqlite — the server keeps the
connection, so the DSN never reaches the browser):

```yaml
# golive.yaml
data:
  backend: postgres
registry:
  backend: postgres    # optional: site metadata in Postgres too
```

```bash
pip install 'html-golive[postgres]'
export GOLIVE_PG_DSN='postgresql://user:pass@host:5432/dbname'
```

Tables are created on first use; `content` is stored as JSONB. Never put the
DSN in `golive.yaml` — it carries a password; keep it in the environment.

For MySQL 8.4+, set both backend values to `mysql`, install
`html-golive[mysql]`, and set `GOLIVE_MYSQL_DSN=mysql://user:password@host:3306/dbname`.
Use a real database/user with DDL and CRUD grants. Remote connections verify TLS;
URL-encode reserved characters in credentials. Run `golive db init`,
`golive doctor`, then `golive verify --json`. Restart the server and republish
existing pages after changing backends; switching does not migrate rows.

To switch to Supabase:

```yaml
# golive.yaml
supabase:
  url: https://YOURPROJECT.supabase.co
data:
  backend: supabase
```

```bash
export GOLIVE_SUPABASE_ANON_KEY=...      # public publishable/anon key, embedded in page JS
export GOLIVE_SUPABASE_SERVICE_KEY=...   # CLI only, optional
golive db init --print-sql               # run the SQL in Supabase
```

**Supabase mode embeds the anon key in the published HTML.** Row Level
Security is mandatory there; say so when you set it up. SQLite mode
embeds no key, but anyone who can reach `golive serve` can call
`/api/data` — front it with auth if the data is sensitive.

## Step 5 — administration and permissions

```bash
golive serve --port 8787     # then open http://localhost:8787/admin
golive admin open            # prints the portal URL
```

Roles: **superadmin** (everything) → **owner** (their own sites) →
**maintainer** (edit and roll back, cannot delete or transfer).

```bash
golive maintainer list   report
golive maintainer add    report bob@example.com
golive maintainer remove report bob@example.com
```

Superadmins come from two places:

- **builtin** — `admin.admins` in `golive.yaml` or the `GOLIVE_ADMINS`
  env var. Read-only at runtime, so nobody can lock the operator out.
- **managed** — added through the admin portal, stored in the registry.

Auth for `serve`: `GOLIVE_TOKEN=<secret>` for a shared static token, or
OIDC for real per-user identity. With neither configured, the admin
portal answers only to loopback callers.

## Step 6 — troubleshooting

| Symptom | Check | Fix |
|---|---|---|
| `command not found: golive` | `pip show html-golive` | `pip install html-golive`; confirm the scripts dir is on `PATH` |
| Publish fails on paths/permissions | `golive doctor` line 1 | `$GOLIVE_HOME` unwritable — fix ownership or point it elsewhere |
| Site 404s | `golive list` | slug typo, or `serve` is not running / on another port |
| `TemplateAPI is not defined` | page source for the injected `<script>` | republish with `--data-model`; the file must be opened through `serve`, not `file://` |
| Data calls reject in console | the console message names the cause | usually `data.backend: none`, or Supabase mode without keys |
| Port already in use | `golive doctor` port line | another `serve`; pick a different `--port` |
| Style did not apply | `golive styles` | name mismatch — must be an exact list entry |

`golive doctor` is the first diagnostic for anything environmental. Run
it before speculating.

## Command index

`publish` · `list` · `rollback` · `serve` · `preview` · `styles` ·
`maintainer` · `admin` · `data` · `db` · `clone` · `migrate-check` ·
`doctor` · `skill`

Full CLI reference: `references/cli.md`. Deeper data-layer notes:
`references/data-layer.md`. Both sit next to this file.

## Rules of engagement

1. Probe (`--version`, `doctor`, `list`) before acting.
2. Prefer `--update <slug>` over creating near-duplicate sites.
3. Never pass `--host 0.0.0.0` or `--skip-content-scan` unless the user
   asked; flag the exposure when you do. A credential finding cannot be
   waived by any flag — do not try. Report what was found and let the user
   remove it, or replace the value with a placeholder (`password=***`,
   `API_KEY=<your-key-here>`), which publishes fine.
4. `rollback` and `publish --update` overwrite live content — show the
   plan (`--dry-run` for rollback) and confirm first.
5. Report the actual CLI output, including the real URL. Do not invent
   URLs, slugs or ids.
