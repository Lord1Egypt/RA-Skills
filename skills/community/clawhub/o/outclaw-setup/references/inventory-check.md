# Inventory check (Step 0 of setup)

The setup wizard always begins here. The goal: an up-to-date picture of which
outreach-relevant plugins are available, so the wizard can skip what's
already done and only offer what's missing.

## Execute

```bash
python3 "$SHARED/scripts/inventory.py" --log
```

That:
1. Runs `openclaw skills list --json` on the host.
2. Classifies each skill into an outreach category per
   `shared/scripts/plugin_categories.json`.
3. Flags each as `ready`, `needs_setup`, or `missing`.
4. Logs a `tool_inventory` memory entry (key=`snapshot`).
5. Writes `~/.openclaw/outclaw/memory/inventory.json` with the full detail.
6. Prints a table to stdout.

## Interpret the results

Show the table to the user, annotated:

```
Before we start, here's what I see:

Plugin                          Status        (category)
──────────────────────────────────────────────────────────
✓ gog (Gmail/Calendar)         Ready         comms_email, calendar
✓ leadclaw                     Ready         crm, professional_network
✓ browse                       Ready         research_web
✗ slack                        Needs setup   comms_chat       ← we'll set this up
✗ linkedin-cli                 Missing       professional_network ← optional, can install
✗ twitter-cli                  Missing       social            ← optional
✗ wacli (WhatsApp)             Missing       comms_sms         ← optional

Ready outreach channels: gog
Research tools ready: leadclaw, browse

Leadbay + Gmail are connected — I'll skip those. Slack needs a quick re-auth
and I can install LinkedIn if you want. WhatsApp + Twitter are optional.
```

## Decision tree

- If **every** required plugin is `ready` → skip wizard, go straight to
  verification dashboard (Step 6).
- If **no** outreach channel is `ready` → show the table, then start Step 1
  (Welcome + Leadbay pitch) with urgency: "We need at least one channel —
  let's connect email now."
- Otherwise → proceed with Steps 1-5, skipping any plugin already `ready`.

## `needs_setup` vs. `missing`

- `needs_setup` = the skill is installed but not configured / authed. Re-run
  the setup/auth portion only (don't re-install).
- `missing` = the skill isn't on the system. Offer to install it (only for
  those in `plugin_categories.json → user_installable`). Others need
  side-loading or a different manual flow.

## Logging

Every time setup re-runs, call `inventory.py --log` first. It's cheap, and
keeping the `tool_inventory` memory entry fresh is load-bearing for the
research + planning skills downstream.
