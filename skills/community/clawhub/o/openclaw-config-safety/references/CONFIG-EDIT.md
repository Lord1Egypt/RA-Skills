# Protocol: openclaw.json Config Edits

**Applies to:** Any write to `~/.openclaw/openclaw.json` — direct edit, scripted update, doctor --fix auto-commit, config token import.

**Why this exists:** Without a pre-write gate, invalid fields (e.g. `status`, `note` in per-model overrides — fields outside the Zod schema) cause gateway crashes. The validator and wizard are the safety net.

---

## Recommended: Use the Wizard

The `openclaw-config-onboard` wizard handles everything in one flow:

```bash
openclaw-config-onboard  # interactive
openclaw-config-onboard --normalize  # normalize in place
openclaw-config-onboard --validate   # validate only
openclaw-config-onboard --import <token>  # import token
```

The wizard:
- Creates automatic timestamped backups before any write
- Validates with `openclaw doctor` before committing
- On gateway restart failure: **automatically restores backup**

---

## Manual Pre-Write Checklist (without wizard)

1. **Backup current config:**
   ```bash
   cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak-$(date +%Y%m%d-%H%M%S)
   ```

2. **Write candidate to temp file** (never edit live config directly)

3. **Validate candidate before writing:**
   ```bash
   OPENCLAW_BIN=~/.nvm/versions/node/v24.14.0/bin/openclaw \
     ~/.openclaw/workspace/skills/openclaw-config-safety/scripts/validate-openclaw-config.sh \
     --file /path/to/candidate.json
   ```
   If exit code ≠ 0: **DO NOT WRITE**. Fix the reported fields first.

4. **Write to live config** only after validation passes.

5. **Restart gateway:**
   ```bash
   openclaw gateway restart
   ```

6. **Verify gateway is up:**
   ```bash
   openclaw sessions
   ```

7. **If gateway fails to start:** restore from backup and re-run validator.
   ```bash
   cp ~/.openclaw/openclaw.json.bak-<timestamp> ~/.openclaw/openclaw.json
   openclaw gateway restart
   ```

---

## Known-Green Fields (safe to use without validation)

These fields are confirmed schema-valid:

| Location | Fields |
|----------|--------|
| `agents.defaults.models[<key>]` | `alias` (string), `params` (record), `streaming` (boolean) |
| `models.providers[<provider>].models[]` | `id`, `name`, `api`, `reasoning`, `input`, `cost`, `contextWindow`, `maxTokens`, `headers`, `compat` |
| `agents.defaults` top-level | `model`, `models`, `timeoutSeconds`, `compaction`, `memorySearch`, `bootstrapMaxChars`, `workspace` |

---

## Known-Red Fields (NEVER add without schema verification)

| Field | Location | Reason |
|-------|----------|--------|
| `status` | Per-model override (`agents.defaults.models[<key>]`) | `.strict()` Zod modifier — instant crash |
| `note` | Per-model override | Not in schema — crash |
| Unknown fields | Any `.strict()` Zod object | Rejected at load time |

---

## Config Tokens

Exported configs are `mrconf:v1:...` tokens — safe to share. Credential values are NEVER included; only `${REFERENCE}` placeholders.

**Export:**
```bash
openclaw-config-onboard --export
```

**Import:**
```bash
openclaw-config-onboard --import mrconf:v1:...
```

Import merges the token config into your existing config (deep merge, preserving keys not in token). Backup is automatic. On gateway restart failure, backup is restored automatically.

---

## openclaw doctor

`openclaw doctor --fix` auto-migrates/fixes some config drift but may introduce unwanted changes (e.g., moving `streamMode` → `streaming`). Always review doctor output before accepting changes.

---

## Schema Drift

OpenClaw version upgrades may change the Zod schema. After any upgrade:
1. Re-run schema extraction from your local openclaw installation
2. Update field registry
3. Update this protocol

Schema extraction (run on host machine with gateway installed):
```bash
grep -n "alias\|status\|note\|streaming\|\.strict()\|z\.string\|z\.boolean\|z\.number" \
  ~/.nvm/versions/node/v24.14.0/lib/node_modules/openclaw/dist/zod-schema*.js \
  ~/.nvm/versions/node/v24.14.0/lib/node_modules/openclaw/dist/io-*.js \
  | grep -v "//\|import\|export" | head -80
```

---

## Backup Strategy

| Tool | Backup Method |
|------|-------------|
| Wizard (`--normalize`, `--import`) | Automatic: `~/.openclaw/openclaw.json.bak-YYYYMMDD-HHMMSS` |
| `validate-openclaw-config.sh` | Manual: `cp` before running |
| Direct edit | Manual: `cp` before editing |

**Restore:**
```bash
# List backups
ls -lt ~/.openclaw/openclaw.json.bak-*

# Restore specific backup
cp ~/.openclaw/openclaw.json.bak-<timestamp> ~/.openclaw/openclaw.json
openclaw gateway restart
```
