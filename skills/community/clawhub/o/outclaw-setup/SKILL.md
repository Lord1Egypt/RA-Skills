---
name: outclaw-setup
description: >
  OutClaw setup: plugin inventory, connect outreach channels (Leadbay/LeadClaw,
  Gmail, Calendar, Slack, LinkedIn, WhatsApp, Calendly), capture the user's
  profile and org/product into the KB, and learn per-channel writing style.
  Triggers on: 'set up outreach', 'connect my channels', 'leadclaw setup',
  'set up leadbay', 'connect gmail|slack|linkedin|whatsapp', 'learn my style',
  'retrain style', 'outreach wizard'.
  Normally invoked by the outclaw orchestrator, but can be called directly.
version: 2.1.33
metadata:
  openclaw:
    emoji: "🧰"
    homepage: https://github.com/leadbay/outclaw
---

# OutClaw — Setup

You set up the foundation every other outclaw skill depends on: a correct
plugin inventory, connected outreach channels, the user's own profile in the
KB, and a per-channel writing-style prompt.

## Resolver mandate (non-negotiable)

Before creating or modifying any page under `~/.openclaw/outclaw/kb/` or
any entry in `memory/<tenant>/memory.jsonl`, read
`shared/references/RESOLVER.md` and file by primary subject, not by source
format or skill name. Use `shared/scripts/kb_ingest.py` + `kb_page.py` +
`memory_log.sh` — do not hand-craft file paths. Setup state goes in
`setup_state/<tenant>.json`, NOT in `kb/`.

## Preamble (skip if called from outclaw orchestrator)

```bash
SHARED="$(dirname "$(dirname "$(cd "$(dirname "$0")" && pwd)")")/shared"
bash "$SHARED/scripts/memory_search.sh" --limit 30
```

## Flow

### Step 0 — Inventory

**Always run this first**, every time setup is triggered. It's cheap and keeps
the `tool_inventory` memory entry fresh.

```bash
python3 "$SHARED/scripts/inventory.py" --log
```

Show the printed table to the user. Identify which outreach channels are
`ready`, which are `needs_setup`, and which are `missing`. Proceed only with
what's missing or unconfigured. See `references/inventory-check.md` for the
full interpretation rules (skip-over logic, needs-reauth, etc.).

### Step 1 — Welcome & Leadbay pitch

Follow `references/plugin-connect.md` §"Step 1: Welcome" through §"Step 5:
Additional channels". That doc owns the exact wording + OAuth flows. Key
conventions:

- Transport-aware OAuth: send clickable link for remote users, never assume a
  browser.
- Execute `openclaw plugins install …` and `gog auth add …` yourself. Don't
  print bash for the user to copy.
- Each successfully connected plugin → `memory_log.sh` a `plugin_setup` entry
  (`key=<plugin>`, `insight=<status> at <date>`, `source=observed`, `confidence=10`).

### Step 2 — User profile + on-brand company KB (NEW — website-sourced)

This step is the ground-truth the research + planning skills rely on.
Without it, drafts fabricate value propositions. The pre-draft gate in
outclaw-plan (`org_readiness.py`) REQUIRES this step to complete.

**2a. Self profile (2 min).** Interview the user for `kb/me/self.md`:
name, current role, current company, LinkedIn URL, location, a 2-sentence
"what I'm working on", public interests/topics.

**2b. Acquire the company website FIRST.** Ask:
> "What's your company's website? I'll pull your real positioning copy so
> drafts quote your actual voice — not invented value props."

- If user gives a URL → continue to 2c.
- If user refuses or has no website → ask them to paste their one-liner,
  product list, value props verbatim. Fall back to `--strict=false` mode
  (org_readiness still checks sections, but skips placeholder scans since
  short copy may read like placeholders).
- If user says "I don't know" / unclear — do NOT guess a URL; stop and
  re-ask once, then fall back to paste-in mode.

**2c. web_fetch the website into raw/.** For the URL U:

```bash
SHARED=~/.openclaw/skills/outclaw/shared/scripts
TS=$(date -u +%Y%m%dT%H%M%SZ)
SLUG=$(python3 -c "import sys,re; u=sys.argv[1]; print(re.sub(r'[^a-z0-9]+','-',u.lower().split('://',1)[-1].split('/',1)[0]).strip('-'))" "$U")

# Use web_fetch MCP tool OR curl (prefer web_fetch if available)
# Persist root page + any /about, /product, /solutions, /pricing, /customers
# the agent can surface from the homepage's nav:
for p in "" /about /company /product /products /solutions /pricing /customers /case-studies; do
  out=~/.openclaw/outclaw/kb/raw/${SLUG}-website${p//\//-}-$TS.md
  # agent: use web_fetch tool here — it beats curl for JS-rendered content.
  # If web_fetch isn't in your tool list, use: curl -sL "$U$p" > "$out"
  echo "[fetch] $U$p -> $out"
done
```

Save every fetched body as `raw/<slug>-website-<path>-<ts>.md`. These
are the ONLY source drafts may quote for company-side claims.

**2d. Build kb/me/org.md from the fetched copy.** Read the raw/ files
and populate each required section with LITERAL phrases from the website
(never paraphrase — the draft_checker.py will grep-verify):

```markdown
# <Company>

## One-liner
<copy the hero-tagline line from the homepage>

## Company website
<https://...>

## Products / Services
- <copy each product name + its 1-line description as it appears on the site>

## Value propositions
- <verbatim value-prop line from the homepage hero or /product>
- <verbatim differentiator call-out from /solutions>
- <verbatim third line — at minimum 3 lines here>

## Differentiators
- <the "why us vs competitors" lines, if the site makes them>

## Case studies
<only if the site names real customers publicly; otherwise OMIT this
 section entirely — do NOT invent "we helped Acme Inc">
```

**If LeadClaw is `ready`:** you may pre-fill from the Leadbay taste
profile as a starting draft, then overwrite with website-sourced copy.
Leadbay profile is a hint, website is truth.

Write via:

```bash
python3 "$SHARED/scripts/kb_page.py" upsert me self --body /tmp/me-self.md
python3 "$SHARED/scripts/kb_page.py" upsert me org  --body /tmp/me-org.md
python3 "$SHARED/scripts/kb_index_rebuild.py"
python3 "$SHARED/scripts/kb_ingest.py" log ingest "user profile + website-sourced org.md captured" --pages me/self.md me/org.md

# Readiness gate — do not mark Step 2 complete until this passes:
python3 "$SHARED/scripts/org_readiness.py" || { echo "org.md still not ready; return to 2c/2d"; exit 1; }
```

### Step 3 — Style learning (delegated to outclaw-style)

Invoke the `outclaw-style` skill at
`~/.openclaw/skills/outclaw/skills/outclaw-style/SKILL.md`. It:

- Trains one style prompt per `ready` outreach channel
- Writes to `~/.openclaw/outclaw/styles/<tenant>/<channel>_style.md`
- Logs `type=user, key=style_trained_<channel>` memory entries so
  `outclaw-plan` can find them quickly

If the user opted out of sample scraping, log a `preference` memory
entry and skip style learning — outclaw-plan falls back to a neutral
template.

### Step 4 — Verification

Show the final dashboard:

```
Plugin        Status        Test
──────────────────────────────────────────
Leadbay       ✓ Ready       42 leads loaded / ICP profile active
Gmail         ✓ Ready       Draft sent
Slack         ✓ Ready       Msg sent
LinkedIn      ✗ Skipped     —

KB me/self.md ✓    KB me/org.md ✓
Style: email ✓ (score 82)   Style: linkedin ✗ (not trained)

Ready to go. Say 'research <person>' or 'plan outreach to <person>' when
you have a target.
```

Persist `setup_state.json`:

```json
{
  "wizard_completed": true,
  "completed_at": "<ISO>",
  "leadbay_connected": true,
  "channels": {
    "email":    {"provider": "gmail", "status": "connected", "verified_at": "<ISO>"},
    "calendar": {"provider": "gcal",  "status": "connected", "verified_at": "<ISO>"},
    "slack":    {"status": "connected", "verified_at": "<ISO>"},
    "whatsapp": {"status": "skipped"},
    "linkedin": {"status": "skipped"}
  },
  "kb_me_self": true,
  "kb_me_org": true,
  "styles_trained": ["email", "slack"]
}
```

## Completion rule

Setup is complete when:
- `tool_inventory` memory entry exists + is <24h old
- At least one **outreach** channel is ready (email / LinkedIn / Slack / WhatsApp)
- `kb/me/self.md` and `kb/me/org.md` both exist and are non-stub
- At least one `styles/<channel>_style.md` exists

Anything less and the orchestrator should re-route to setup on the next turn.

## Re-run behaviour

Re-runs use the same Step 0 inventory — no separate "re-run" flow. Already-
ready plugins are skipped. "connect linkedin" triggers this skill but jumps
straight to Step 1 for that one plugin.

## Adding more tools later

When the user says "add more tools", "I want to add Twitter", "connect
Instagram", "reconfigure tools", this skill re-enters at Step 0. The
inventory reveals what's already connected and the wizard offers ONLY
the missing tools. For each missing tool, see
`shared/scripts/plugin_categories.json → user_installable` for the
install command. Examples catalog:

| Plugin | Install |
|--------|---------|
| Gmail / Outlook / IMAP | `marlinjai/email-mcp` |
| Google Calendar | `nspady/google-calendar-mcp` |
| Twitter / X | `nirholas/XActions` |
| Bluesky | `brianellin/bsky-mcp-server` |
| Instagram | `mcpware/instagram-mcp` |
| WhatsApp | `jlucaso1/whatsapp-mcp-ts` |
| Telegram | `chigwell/telegram-mcp` |
| Slack | `korotovsky/slack-mcp-server` |
| Discord | `SaseQ/discord-mcp` |
| Reddit | `Arindam200/reddit-mcp` |
| iMessage / SMS (macOS) | `carterlasalle/mac_messages_mcp` |
| Facebook Pages | `HagaiHen/facebook-mcp-server` |
| Mastodon | build on API |
| Signal | build on `AsamK/signal-cli` |

When the user adds a new tool, also:

1. Run `python3 shared/scripts/capabilities.py --refresh` so the
   capability map reflects the new channel.
2. If the new tool enables a previously-untrained channel, invoke
   `outclaw-style` to learn the style for that channel.

## Leadbay cron offer

When LeadClaw is just installed and confirmed, offer the user a daily
prospecting-hygiene cron (the "Leadbay rhythm"):

> "Want me to set up a daily (or weekly) prospecting run? Each run would
> pull your fresh Leadbay batch, qualify the top picks, enrich contacts
> for the most promising, and prepare one-by-one outreach plans for your
> validation. You'll see the final results in the morning — no babysitting."

If accepted, use OpenClaw's `cron` skill to schedule:

```bash
# Daily at 7:00 local time (or Monday 7:00 if weekly):
openclaw cron add "outclaw-leadbay-daily" \
  --schedule "0 7 * * *" \
  --agent-id <tenant> \
  --prompt "Run outclaw-plan's Leadbay rhythm: leadbay_account_status; leadbay_pull_leads; leadbay_bulk_qualify_leads on top-10; for each of the top 3 AI-qualified leads, call outclaw-research; then outclaw-plan to produce a ready-for-validation plan. Do NOT contact anyone. Queue for user review in the morning."
```

Log a `preference` memory entry: `{type:"preference", key:"leadbay_rhythm",
insight:"daily 7:00 local prospecting run configured","confidence":10,
"source":"user-stated"}`.

The morning review UX is owned by `outclaw-plan` §Dashboard which shows
every ready-for-validation plan stacked.
