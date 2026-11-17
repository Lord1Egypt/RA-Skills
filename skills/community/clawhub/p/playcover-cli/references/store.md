# `store` — browse available apps

Browse the catalog of apps available from configured IPA sources. The `store` command is a **group** with one subcommand.

---

## `store list [--source <url>] [--json]`

List apps available across all (or one) configured source(s).

| Flag | Type | Description |
|------|------|-------------|
| `--source <url>` | `String` | Filter to a single source. |
| `--json` | flag | Emit JSON instead of text. |

### Text output

One line per app: `<name>\t<bundleID>\t<version>`.

### JSON output

An array of objects, pretty-printed with keys sorted:

```json
[
  {
    "bundleID": "com.example.app",
    "checksum": "sha256-hex-digest",
    "link": "https://example.com/app.ipa",
    "name": "Example",
    "version": "1.2.3"
  }
]
```

### Notes

- `checksum` is the SHA-256 digest advertised by the source; `download` verifies the downloaded IPA against it.
- Use `--source` to scope a query to one source (useful when sources have overlapping app names).
- Run `source refresh` first to ensure the catalog is up to date.

```bash
# Find all apps named "Example" across sources
PlayCover.app/Contents/MacOS/PlayCover store list --json \
  | jq '.[] | select(.name | test("Example"; "i"))'

# Show download URLs for one source
PlayCover.app/Contents/MacOS/PlayCover store list --source https://example.com/source.json --json \
  | jq -r '.[].link'
```
