# App query commands

List installed apps and inspect a single app's metadata. Both support `--json` for structured output.

---

## `list`

List all apps installed via PlayCover.

| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Emit JSON instead of text. |

### Text output

One line per app, tab-separated:

```
<AppName>\t<bundleId>\t<version>
```

### JSON output

An array of objects, pretty-printed with keys sorted:

```json
[
  {
    "bundleIdentifier": "com.example.app",
    "name": "Example",
    "path": "/Users/me/Library/Containers/io.playcover.PlayCover/Library/.../Example.app",
    "version": "1.2.3"
  }
]
```

### Scripting

```bash
# Just the bundle IDs of all installed apps
PlayCover.app/Contents/MacOS/PlayCover list --json | jq -r '.[].bundleIdentifier'

# Count installed apps
PlayCover.app/Contents/MacOS/PlayCover list --json | jq 'length'
```

## `info <bundleId>`

Show detailed metadata for one installed app.

| Arg/Flag | Type | Description |
|----------|------|-------------|
| `bundleId` (positional) | `String` | Bundle identifier. |
| `--json` | flag | Emit JSON instead of text. |

### Text output

```
Name: <name>
Bundle ID: <bundleId>
Version: <version>
Category: <category or "(none)">
Minimum OS: <minOS>
PlayTools: <installed | not installed>
Container: <container path>
Path: <app bundle path>
```

### JSON output

A single object with the same fields, pretty-printed, keys sorted.

### Behavior

- Exit `3` (`appNotFound`) if no installed app matches `bundleId`.
- The `--json` shape is stable across versions; prefer it for agents and scripts.

```bash
# Look up one app's install path
PlayCover.app/Contents/MacOS/PlayCover info com.example.app --json | jq -r '.path'
```
