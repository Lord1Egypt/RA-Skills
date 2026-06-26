---
name: openclaw-safe-change-flow
description: Safe OpenClaw config change workflow with backup, minimal edits, validation, health checks, and rollback. Single-instance first; secondary instance optional.
---

# OpenClaw Safe Change Flow

Goal: **avoid outages, keep rollback ready, verify every change**.
Use **single-instance** mode by default. Secondary-instance checks are optional.

---

## Scope

### Default (recommended): single instance

- Main config: `~/.openclaw/openclaw.json`

### Optional (advanced): dual instance

- Secondary config: `~/.openclaw-secondary/openclaw.json` (or your custom path)

If you do not need high-availability validation, single-instance flow is enough.

---

## Required single-instance flow

1. **Backup first**
   - Create timestamped backup: `*.bak.safe-YYYYmmdd-HHMMSS`
2. **Make minimal edits**
   - Change only necessary keys
3. **Validate immediately**
   - Run: `openclaw status --deep`
4. **Auto rollback on failure**
   - Restore backup and restart gateway
5. **Confirm availability**
   - Verify channels/interfaces respond correctly

---

## Agent execution convention (default behavior)

After this skill is installed, treat this as default policy for config changes:

- **Default entrypoint:** run config changes through `safe-change.sh`
- **Avoid direct edits + bare restart**
- **If user explicitly asks to bypass:** allow it, but warn about risk

Mental model:

- Before: edit config directly
- Now: create a small edit script and run `safe-change.sh --main-script ./edit-main.sh`

---

## Optional dual-instance enhancement

On top of single-instance flow, you may also verify a secondary instance:

- `OPENCLAW_HOME=<secondary-home> openclaw gateway health --url <secondary-url> --token "$SECONDARY_TOKEN"`
- If either instance validation fails, rollback

Use this only when change risk is high or HA checks are required.

---

## Automation script (v1.0.2+)

This skill includes `safe-change.sh` to enforce:

**backup → change → validate → rollback on failure**

### Recommended: single-instance usage

```bash
cat > ./edit-main.sh <<'SH'
#!/usr/bin/env bash
python3 edit_main.py
SH
chmod +x ./edit-main.sh

./safe-change.sh --main-script ./edit-main.sh
```

### Optional: dual-instance usage

```bash
cat > ./edit-main.sh <<'SH'
#!/usr/bin/env bash
python3 edit_main.py
SH
chmod +x ./edit-main.sh

cat > ./edit-secondary.sh <<'SH'
#!/usr/bin/env bash
python3 edit_secondary.py
SH
chmod +x ./edit-secondary.sh

export SECONDARY_TOKEN="<your-secondary-token>"
./safe-change.sh \
  --main-script ./edit-main.sh \
  --secondary-script ./edit-secondary.sh
```

When secondary checks are enabled, set `SECONDARY_TOKEN` as an environment variable.

---

## Safety rules

- Never hardcode tokens or secrets
- Validate before announcing success
- Restore service first, investigate later
- Always keep a recent known-good backup in production

---

## Manual quick template (single instance)

```bash
TS=$(date +%Y%m%d-%H%M%S)
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak.safe-$TS

# ...apply minimal config edits...

openclaw status --deep
```

If validation fails:

```bash
cp ~/.openclaw/openclaw.json.bak.safe-$TS ~/.openclaw/openclaw.json
openclaw gateway restart
```
