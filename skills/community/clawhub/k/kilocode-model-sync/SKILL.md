---
name: kilocode-model-sync
description: >
  Sync the Kilocode provider model list in openclaw.json with the live Kilo AI API.
  Use when: running the weekly model sync job, checking for new/removed/updated Kilocode
  models, applying approved model patches to openclaw.json, or reporting sync results
  to mission control and Telegram. Requires KILOCODE_API_KEY in ~/.openclaw/.env.
disable-model-invocation: true
---

# ----- THIS SKILL IS DEPRECATED - DON'T RUN -----
# ----- KILOCODE GATEWAY IS NOW BUILT-IN IN OPENCLAW -----

# Kilocode Model Sync

**Workspace:** `~/.openclaw/workspace-steve/`
**Scripts:** `~/.openclaw/workspace/skills/kilocode-model-sync/scripts/`
**Snapshots/diffs/patches:** `~/.openclaw/workspace/kilocode-models/`
**Telegram delivery:** Use the `message` tool with `channel=telegram`, target Guillaume's chat.

---

## Step 1 — Run the sync script

```bash
source ~/.openclaw/.env && python3 ~/.openclaw/workspace/skills/kilocode-model-sync/scripts/sync_models.py
```

Parse the JSON result from stdout. It contains:

| Field | Meaning |
|---|---|
| `status` | `"changed"` \| `"no_change"` \| `"error"` |
| `total_models` | Total models fetched from API |
| `diff.added` | New models not in previous snapshot |
| `diff.removed` | Models that disappeared |
| `diff.updated` | Models with changed fields |
| `snapshot_path` | Where today's snapshot was saved |
| `patch_path` | Path to the `.patch.json` file (only if changed) |
| `diff_path` | Path to the `.diff.json` file (only if changed) |

---

## Step 2 — If `status == "no_change"`

Write a brief memory note and stop. No notification needed.

```
# memory/YYYY-MM-DD.md entry:
## Kilocode Model Sync — YYYY-MM-DD
- Status: no_change
- Total models: X
- No action required.
```

---

## Step 3 — If `status == "changed"`, notify Guillaume via Telegram

Use the `message` tool to send to Guillaume's Telegram:

```
🤖 *Kilocode Model Sync — {date}*

Found changes in the Kilocode model list:
✅ Added: {N} model(s)
❌ Removed: {N} model(s)
🔄 Updated: {N} model(s)

*New models:*
{for each added: • `id` — Name (ctx: Xk tokens, cost: $Y input/$Z output per 1k)}

*Removed models:*
{for each removed: • `id` — Name}

Reply to Grog: `@steve approve` to apply, or `@steve skip` to ignore.
```

Format costs as `$0.001/1k` (multiply the raw per-token value × 1000).
Use `free` for models with 0 cost on both input and output.

---

## Step 4 — Wait for approval signal from Grog

Grog will relay a `sessions_send` message to your session containing either:
- `approve` — proceed to apply
- `skip` — log and stop

---

## Step 5 — If approved, apply the patch

```bash
python3 ~/.openclaw/workspace/skills/kilocode-model-sync/scripts/apply_patch.py <patch_path>
```

The script:
1. Backs up `openclaw.json` with a timestamp
2. Replaces `models.providers.kilocode.models` with the new list
3. Runs `openclaw gateway restart`
4. Polls `openclaw gateway status` until `RPC probe: ok` (up to 30s)

Result fields:
- `status`: `"ok"` | `"applied_restart_failed"`
- `backup_path`: where the backup was saved
- `gateway.ok`: true/false
- `gateway.error`: error message if failed

---

## Step 6 — Write mission control entry

Append to `~/.openclaw/workspace/memory/YYYY-MM-DD.md`:

```markdown
## Kilocode Model Sync — YYYY-MM-DD
- **Status:** Applied ✅
- **Added:** N models — list ids
- **Removed:** N models — list ids
- **Updated:** N models — list ids
- **Backup:** backup_path
- **Gateway restart:** ok / failed (error message)
- **Approved by:** Guillaume (via Telegram)
```

---

## Step 7 — Send Telegram confirmation

```
✅ *Kilocode Model Sync — Applied*

{N} new models added to openclaw.json.
{N} models removed.
Gateway restarted successfully. ✅

Backup saved at: {backup_path}
```

If gateway restart failed:
```
⚠️ *Kilocode Model Sync — Patch Applied, Gateway Restart Failed*

Models were written to openclaw.json but the gateway did not restart cleanly.
Error: {error}
Please restart manually: `openclaw gateway restart`
```

---

## Step 8 — Report summary to Grog (sessions_send to main session)

After completion, send a concise summary to the main agent session so Grog can relay it
to Guillaume if needed. Use `sessions_send` with `label=main` or `sessionKey=agent:main:main`.

---

## Error handling

- If `sync_models.py` exits with status `"error"`: notify Guillaume via Telegram with the error, stop.
- If `apply_patch.py` fails to write config: the script auto-restores from backup; report failure.
- If gateway doesn't come back: report in Telegram, tell Guillaume to restart manually.
- Always write a memory note even on failure.
