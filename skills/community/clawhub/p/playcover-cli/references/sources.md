# `source` — manage IPA sources

Manage the list of IPA sources PlayCover pulls apps from. The `source` command is a **group** with six subcommands. `<url>` is the source's HTTP(S) URL.

> Looking for a source to add? See [where-to-get-ipas.md](where-to-get-ipas.md) — Mac Club (<https://www.maclub.net>) is the recommended catalog.

---

## `source list [--json]`

List all configured sources.

| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Emit JSON instead of text. |

- Text: one line per source: `[x] <url> (<status>)`. `[x]` = enabled, `[ ]` = disabled.
- JSON: array of `{ url, enabled, status }`.
- Status reflects the last refresh (`refreshed`, `error`, etc.).

## `source add <url>`

Add a new IPA source.

| Arg | Type | Description |
|-----|------|-------------|
| `url` (positional) | `String` | Source URL. |

- Output: `Added source <url>`.
- Exit `2` if the URL is invalid or the source already exists.

## `source remove <url>`

Remove a configured source.

| Arg | Type | Description |
|-----|------|-------------|
| `url` (positional) | `String` | Source URL. |

- Output: `Removed source <url>`.
- Exit `2` if the source is not configured.

## `source refresh`

Re-fetch the app list from every configured source.

- Output: one progress line per source, then `Sources refreshed`.
- Safe to run periodically (e.g. before `store list`).

## `source enable <url>`

Enable a disabled source (it will be included in `store list` and `download`).

| Arg | Type | Description |
|-----|------|-------------|
| `url` (positional) | `String` | Source URL. |

## `source disable <url>`

Disable a source without removing it (it will be excluded from `store list` and `download`).

| Arg | Type | Description |
|-----|------|-------------|
| `url` (positional) | `String` | Source URL. |

---

## Workflow

```bash
BIN="PlayCover.app/Contents/MacOS/PlayCover"

# Add a source, refresh, list what's available
$BIN source add https://example.com/source.json
$BIN source refresh
$BIN store list --json | jq -r '.[].name'
```
