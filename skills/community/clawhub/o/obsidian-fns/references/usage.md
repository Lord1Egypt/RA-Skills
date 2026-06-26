# obsidian-fns usage reference

## Validated environment

Use your own Fast Note Sync deployment and vault settings. Example placeholders:

- Base URL: `https://your-fast-note-sync.example.com/api`
- Vault: `MyVault`
- Auth flow: login obtains token, later requests use Bearer token

## File layout

```text
obsidian-fns/
├── SKILL.md
├── _meta.json
├── references/
│   └── usage.md
└── scripts/
    ├── fns.py
    └── fns_actions.py
```

## High-level actions

Use these for most OpenClaw-facing tasks.

### Search notes

```bash
python3 {baseDir}/scripts/fns_actions.py search-notes --keyword "OpenClaw"
```

### Read note body

```bash
python3 {baseDir}/scripts/fns_actions.py read-note --path "OpenClaw/API-Test.md"
```

### Write note

```bash
python3 {baseDir}/scripts/fns_actions.py write-note \
  --path "OpenClaw/API-Test.md" \
  --content "# hello"
```

### Append note

```bash
python3 {baseDir}/scripts/fns_actions.py append-note \
  --path "OpenClaw/API-Test.md" \
  --content "\n- one more line"
```

## Low-level CLI

Use this layer for debugging or for operations that are not wrapped by `fns_actions.py`.

```bash
python3 {baseDir}/scripts/fns.py doctor
python3 {baseDir}/scripts/fns.py login
python3 {baseDir}/scripts/fns.py user-info
python3 {baseDir}/scripts/fns.py vaults
python3 {baseDir}/scripts/fns.py search --keyword OpenClaw
python3 {baseDir}/scripts/fns.py get --path "OpenClaw/API-Test.md" --content-only
python3 {baseDir}/scripts/fns.py put --path "OpenClaw/API-Test.md" --content "# hello"
python3 {baseDir}/scripts/fns.py append --path "OpenClaw/API-Test.md" --content "\n- hello"
```

## Configuration sources

Priority from high to low:

1. CLI arguments
2. Environment variables
3. `~/.openclaw/openclaw.json` under `skills.entries.fast-note-sync` (legacy-compatible)
4. `~/.config/fast-note-sync/config.json` (legacy-compatible)

Supported config keys:

- `baseUrl`
- `credentials`
- `password`
- `vault`
- `token`
- `timeoutSeconds`

Environment variables:

- `FNS_BASE_URL`
- `FNS_CREDENTIALS`
- `FNS_PASSWORD`
- `FNS_VAULT`
- `FNS_TOKEN`
- `FNS_TIMEOUT_SECONDS`

## Verified capabilities

Real integration and regression testing already covered:

- login
- user-info
- vaults
- tree
- search
- get
- get with `--content-only`
- put
- append
- prepend
- replace
- rename
- move
- histories
- Chinese paths and spaced paths

Regression report example:

- `outputs/obsidianfns-test-report.json`

## Productization notes

This skill was renamed from `ObsidianFNS` to `obsidian-fns` to satisfy packaging and validation rules for distributable skills.

Compatibility-sensitive implementation details remain in scripts/config behavior; the rename here is primarily for the published skill package structure and trigger metadata.
