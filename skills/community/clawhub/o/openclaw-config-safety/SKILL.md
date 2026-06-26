---
name: openclaw-config-safety
version: 2.0.0
description: Validate openclaw.json config changes safely. Use when editing openclaw.json, changing model config, modifying gateway settings, running openclaw doctor, planning version upgrades, exporting or importing config tokens, or normalizing config fields. Triggers on: config edit, gateway config, openclaw.json, model override, config validation, gateway restart, openclaw update, version upgrade, config export, config import, config token.
---

# OpenClaw Config Safety v2

Safe config management for openclaw.json — validate, normalize, export as tokens, import from tokens.

## Tools

### `openclaw-config-onboard` — Config wizard

Interactive or non-interactive config management.

```bash
openclaw-config-onboard              # Interactive wizard
openclaw-config-onboard --audit     # Print config summary
openclaw-config-onboard --validate  # Run validation checks
openclaw-config-onboard --export    # Export token to stdout
openclaw-config-onboard --normalize # Normalize config in place
openclaw-config-onboard --import <token>  # Import a config token
openclaw-config-onboard --help      # Show usage
```

Exit codes: 0 = success, 1 = failure, 2 = invalid arguments.

### `validate-openclaw-config.sh` — Pre-write validator

Run before any direct edit to openclaw.json:

```bash
OPENCLAW_BIN=~/.nvm/versions/node/v24.14.0/bin/openclaw \
  ~/.openclaw/workspace/skills/openclaw-config-safety/scripts/validate-openclaw-config.sh \
  --file /path/to/candidate.json
```

## When to Use

- Any edit to `~/.openclaw/openclaw.json`
- Changing model config, adding/removing models or providers
- Modifying gateway, agent, or plugin settings
- Planning OpenClaw version upgrades
- Running `openclaw doctor --fix`
- Exporting config to share as a `mrconf:v1:...` token
- Importing a config token from another machine

## Pre-Write Protocol

1. **Backup current config** (automatic with wizard, manual otherwise):
   ```bash
   cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak-$(date +%Y%m%d-%H%M%S)
   ```

2. **Write candidate to temp file** (never edit live config directly)

3. **Validate before writing**:
   ```bash
   openclaw-config-onboard --validate
   ```
   Or use the wizard for interactive flow: `openclaw-config-onboard`

## Token Format

Exported configs are `mrconf:v1:...` tokens — base64url-encoded JSON. Credential values are NEVER included; only `${REFERENCE}` placeholders are embedded. Tokens are safe to share.

Token structure:
```
mrconf:v1:<base64url>{
  "version": 1,
  "exportedAt": "ISO-8601",
  "normalizerVersion": "1.0.0",
  "config": { ... },
  "credentialRefs": ["VAR_NAME", ...]
}
```

## Import Protocol

When importing a token:
1. Wizard creates automatic backup
2. Merges token config into existing config (deep merge, preserving keys not in token)
3. Validates merged result
4. On gateway restart failure: **automatically restores backup**

## Normalization

The normalize step fixes:
- String whitespace/alias normalization (e.g. `"  m2.7  "` → `"minimax/MiniMax-M2.7"`)
- Type coercion (`"true"` → `true`, `"60"` → `60`)
- Empty array/object cleanup
- Deprecated field detection

## Known-Green Fields

| Location | Fields |
|----------|--------|
| `agents.defaults.models[<key>]` | `alias` (string), `params` (record), `streaming` (boolean) |
| `models.providers[<provider>].models[]` | `id`, `name`, `api`, `reasoning`, `input`, `cost`, `contextWindow`, `maxTokens`, `headers`, `compat` |
| `agents.defaults` top-level | `model`, `models`, `timeoutSeconds`, `compaction`, `memorySearch`, `bootstrapMaxChars`, `workspace` |

## Known-Red Fields

| Field | Location | Reason |
|-------|----------|--------|
| `status` | Per-model override | `.strict()` Zod modifier — instant crash |
| `note` | Per-model override | Not in schema — crash |
| Unknown fields | Any `.strict()` Zod object | Rejected at load time |

## Backup & Restore

```bash
# List backups
ls -lt ~/.openclaw/openclaw.json.bak-*

# Restore
cp ~/.openclaw/openclaw.json.bak-<timestamp> ~/.openclaw/openclaw.json
openclaw gateway restart
```

The wizard creates timestamped backups automatically: `~/.openclaw/openclaw.json.bak-YYYYMMDD-HHMMSS`

## Architecture

```
src/
  alias-map.js       — model alias → canonical name
  audit.js           — config summary generator
  base64url.js      — base64url encode/decode
  config-patch.js   — safe deep merge for import
  doctor-check.js   — openclaw doctor wrapper
  errors.js         — NormalizationError
  export.js         — config → token
  import.js         — token → config
  normalize.js      — field normalization
  prompt.js         — TTY readline helpers
  resolve-refs.js   — env/pass credential resolution
  restore-backup.js — timestamped backup + restore
  token-errors.js   — token error classes

bin/
  openclaw-config-onboard  — main wizard CLI
```

## References

- `NORMALIZATION-SPEC.md` — field normalization spec
- `EXPORT-TOKEN-SPEC.md` — token format spec
- `ONBOARDING-SPEC.md` — wizard behavior spec
- `CONFIG-EDIT.md` — pre-write protocol (same directory)
