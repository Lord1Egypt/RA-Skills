# golive CLI — full reference

Everything `golive --help` exposes, with the flags that matter in
practice. Run `golive <command> --help` for the authoritative list on the
installed version.

Global flags, valid before any subcommand:

| Flag | Meaning |
|---|---|
| `--version` | print the installed version and exit |
| `--config PATH` | use a specific `golive.yaml` |

Config lookup order: `--config` → `$GOLIVE_CONFIG` → `./golive.yaml` →
`$GOLIVE_HOME/golive.yaml` → built-in defaults. Environment variables
always beat database overrides, which beat the file. Admin settings are
stored in the local registry; listener/backend settings take effect after
a restart, while settings marked hot apply immediately.

## publish

```bash
golive publish <source> [options]
```

`<source>` is an HTML file, a project directory, or a `.zip` / `.tar.gz`
archive.

| Flag | Effect |
|---|---|
| `--name TEXT` | site name (defaults to the page `<title>`) |
| `--slug TEXT` | short URL: `/report`. Omit and the site is only at `/s/<site_id>` |
| `--update REF` | republish over an existing site (slug or site_id) and snapshot the old content |
| `--entry FILE` | entry HTML for directory / archive sources |
| `--style NAME` | inject a built-in CSS theme (`golive styles`) |
| `--owner EMAIL` | record the site owner |
| `--data-model CODE` | data-layer namespace; comma-separated for several |
| `--enable-editor` | inject the in-browser editor and mark the site editable |
| `--watermark [TEXT]` | inject a page watermark |
| `--compress` | recompress inline images |
| `--skip-content-scan` | silence content warnings only, on explicit request; credentials still block |
| `--skip-scan` | deprecated alias of `--skip-content-scan`; never bypasses credentials |
| `--port N` | port used when printing the resulting URL |

Publishing prints `site_id`, `slug` and the URL. Quote them verbatim
back to the user.

## list

```bash
golive list
```

Every registered site with id, slug, name and last update. Run this
before any update or rollback to resolve the right target.

## rollback

```bash
golive rollback <site> [--snapshot TS] [--dry-run] [--yes]
```

`<site>` is a slug or site_id. `--dry-run` lists snapshots without
changing anything — do this first. Without `--snapshot` the newest
snapshot is restored. Snapshots are created by each `publish --update`;
the most recent ones per site are retained.

## serve

```bash
golive serve [--port 8787] [--host 127.0.0.1]
```

Serves every published site plus `/admin`. Built-in defaults use loopback;
saved configuration can override the listener. For local verification use
`golive serve --host 127.0.0.1 --port 8787` explicitly.
`--host 0.0.0.0` publishes to the whole network — pair it with
`GOLIVE_TOKEN` or OIDC. Single-process stdlib server; use a real reverse
proxy for TLS or load.

Routes: `/` index · `/<slug>` · `/s/<site_id>` · `/health` ·
`/admin` · `/api/admin/*` · `/api/data/<table>` (server-proxied data backends: sqlite, postgres, mysql).

## preview

```bash
golive preview [file] [--dir DIR] [--entry FILE] [--site REF]
               [--css-style NAME] [--port 18765] [--host 127.0.0.1]
               [--no-open]
```

Local live-reload preview with a style switcher. Nothing is published.

## styles

```bash
golive styles
```

Lists the built-in CSS themes usable with `publish --style`.

## maintainer

```bash
golive maintainer list   <site>
golive maintainer add    <site> <email>
golive maintainer remove <site> <email>
```

Maintainers may edit and roll back a site; they cannot delete or
transfer it.

## admin

```bash
golive admin open [--port 8787]
```

Prints the admin portal URL. The portal itself needs `serve` running.

## data

```bash
golive data list   --model-code CODE [--name PREFIX] [--limit N]
golive data get    --id ID
golive data create --model-code CODE --name NAME [--content JSON] [--desc TEXT]
golive data upsert --model-code CODE --name NAME [--content JSON]
golive data update --id ID [--name NAME] [--content JSON] [--desc TEXT]
golive data delete --id ID
```

`--content` takes inline JSON or `@file.json`. Operates on whichever
data backend is configured (sqlite by default).

## db

```bash
golive db init [--print-sql]
```

With local backends this confirms the SQLite files are ready (tables are
created automatically on first use). `--print-sql` emits the Supabase
schema for the registry and templates tables — PostgREST cannot execute
DDL, so run it in the Supabase SQL editor.

## clone

```bash
golive clone <url> [--name N] [--slug S] [--headless]
              [--analyze-only] [--save-only] [--backend-origin URL]
              [--skip-backend-rewrite]
```

Fetches a public page, localises its assets and publishes it.
`--headless` renders JS-heavy pages first. `--analyze-only` reports what
would happen without publishing.

## migrate-check

```bash
golive migrate-check <file.html>
```

Scans an HTML file for references that will not resolve on this
deployment and reports data-layer call statistics.

## doctor

```bash
golive doctor [--port 8787]
```

Checks `$GOLIVE_HOME` writability, registry readability, site-content
consistency, port availability and optional dependencies. First stop for
any environmental failure.

## skill

```bash
golive skill install [--target DIR] [--from-github] [--force]
golive skill status
golive skill path
```

Installs this skill into an AI agent's skills directory. `install`
auto-detects common locations and asks for `--target` when it cannot.
`status` compares the installed skill version against the running golive
version; `path` prints the bundled source directory.

## Environment variables

| Variable | Purpose |
|---|---|
| `GOLIVE_HOME` | data directory (default `~/.golive/`) |
| `GOLIVE_CONFIG` | explicit config file path |
| `GOLIVE_TOKEN` | static bearer token for `serve` / admin API |
| `GOLIVE_ADMINS` | comma-separated builtin superadmin emails |
| `GOLIVE_SUPABASE_URL` | Supabase project URL |
| `GOLIVE_SUPABASE_ANON_KEY` | anon key (embedded in published pages) |
| `GOLIVE_SUPABASE_SERVICE_KEY` | service key (CLI only) |
| `GOLIVE_EDITOR_TOKEN` | token for the in-browser editor |
| `GOLIVE_S3_*` | S3 storage / uploader credentials |
| `GOLIVE_LLM_BASE_URL` | OpenAI-compatible endpoint for AI review |

## export

```bash
golive export [-o PATH] [--sites-only] [--data-only] [--site REF]
```

Exports the full instance state (sites, HTML, data rows) to a single
tar.gz archive. The archive contains `manifest.json`, `registry.jsonl`,
`data.jsonl`, and `sites/<site_id>.html` files. Pagination is handled
transparently — every site and every data row is included, and counts
are cross-checked against the backend before writing.

| Flag | Effect |
|---|---|
| `-o, --output PATH` | output path (default: `golive-export-<ts>.tar.gz`) |
| `--sites-only` | export site metadata and HTML, not data rows |
| `--data-only` | export data rows, not sites |
| `--site REF` | export only a single site (by slug or site_id) |

## import

```bash
golive import <archive> [--dry-run] [--on-conflict skip|overwrite|rename] [--yes] [--json]
```

Restores an archive produced by `golive export`. Slug conflicts (a site
with the same slug already exists) are handled by the `--on-conflict`
strategy: `skip` (default — leave existing untouched), `overwrite`
(replace), or `rename` (create with a modified slug). Importing the
same archive twice with `skip` is idempotent. Archives are validated
against path traversal before extraction.

DATA-01 development source preserves business IDs, content, sort indices and
timestamps on empty targets; older published/candidate artifacts regenerate IDs.
Use the exact fix commit/wheel. `--json` reports `ok`, `code`, identity maps,
`data_exact_restore`, metadata defaults, per-record errors and uncertain writes.
Require exit zero and inspect exactness; `ok:true` alone also permits explicit
skip/clone operations. Overwrite refuses a different ID for the same logical key;
rename creates new IDs and never rewrites opaque references. Import may be partial;
after transient failure retry with skip and independently verify records.

`--dry-run` validates the archive without opening target backends; target
conflicts/connectivity remain unknown. Exports exclude config/credentials,
audit/session state, page history and external resources; pause source writers
for a consistent backup. Registry timestamps are outside the exact data contract.

## migrate

```bash
golive migrate <data|registry> --to sqlite|postgres|mysql|supabase [--dry-run] [--json]
```

Copies data or registry rows from the current backend to a target
backend. The source is never modified — migration copies, it does not
move. After migration, update `golive.yaml` to point at the new backend
and restart `golive serve`. Row counts are verified before and after; a
mismatch aborts with a clear message. If the target backend is
unavailable, migration fails with an explicit diagnostic. Business IDs and
metadata are preserved, identical records are skipped and conflicting targets
are not silently overwritten. `--json` includes added/skipped counts and failure
codes. Preview reads the source but does not inspect or initialize the target.
Migration of registry rows does not move page files. Parser/config-loading
errors retain the existing CLI behavior; the JSON contract covers these
commands' archive/backend operation results.

## data directory layout

```
$GOLIVE_HOME/
├── sites/<site_id>/index.html    published content
├── backups/<site_id>/            rollback snapshots
├── registry.db                   sites + managed superadmins
├── data.db                       data layer rows (sqlite backend)
├── audit.log                     admin action trail
├── logs/                         operation logs
└── cache/                        style backups and caches
```

## Environment and verification

Use `golive init` for guided setup, `golive context --json` for effective
configuration, `golive doctor --json` for health, and `golive verify --help`
for a temporary end-to-end data check. `golive demo install` publishes
a sample CRUD page. Check each command with `--help` before automation.
