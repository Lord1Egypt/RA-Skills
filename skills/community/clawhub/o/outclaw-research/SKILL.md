---
name: outclaw-research
description: >
  Deeply research a specific person or organisation for B2B outreach. Pulls
  from every outreach-relevant tool in the user's inventory (Leadbay/LeadClaw,
  LinkedIn, Twitter/X, web search, company pages, podcasts, news) and writes
  a persistent profile into the OutClaw knowledge base. Also useful for
  discovery ("find me a promising lead at <company>" via Leadbay).
  Triggers on: 'research <person|company>', 'look up <person>', 'who is
  <person>', 'find <person>'s email|linkedin|phone|company', 'tell me about
  <company|person>', 'enrich <person>', 'pull a lead', 'surface a prospect'.
  Normally invoked by the outclaw orchestrator.
version: 2.1.33
metadata:
  openclaw:
    emoji: "🔬"
    homepage: https://github.com/leadbay/outclaw
---

# OutClaw — Research

## FIRST ACTION RULES — read before anything else

**1. Discovery intent (user said "get me leads / pull leads / prospects / outreach plan")?**
Plans are delivered in **daily batches of 10–15 fresh targets**, not 1–3.
Three is noise for a salesperson at a 5% reply rate. Use the batch flow:

```bash
# a) Pull + save the Leadbay response, then let the batch script do the
#    bulk work (tier-1 persist for every lead, fresh-pick top N, emit
#    manifest).
# Agent: call leadbay_pull_leads (no args) → save JSON → /tmp/leadbay-pull.json
bash ~/.openclaw/skills/outclaw/shared/scripts/outclaw_daily_batch.sh --n 15 --stale-after-days 7

# b) DEFAULT: skip Tier-2 for the full batch. Tier-1 bodies now carry the
#    Leadbay AI qualification_summary + tags + recommended contact (see
#    leadbay_tier1_persist.py's richer body format) — enough for Day-1
#    drafts. Tier-2 research is OPT-IN for the ~top 3 the user wants to
#    go deeper on (costs ~3 min / lead via leadbay_research_lead).

# c) Build the Day-1 scaffold for all 15 targets. Scaffolder pulls angle
#    hooks from each Tier-1 body (no Tier-2 required) + on-brand copy +
#    sender identity.
python3 ~/.openclaw/skills/outclaw/shared/scripts/plan_scaffolder.py --max 15
# Output: /tmp/outclaw-plan-draft.md
```

After the scaffold is written, the agent's remaining work is **only**
writing the 15 Day-1 email bodies + Provenance blocks (no research, no
bookkeeping), then running channel_validator.py + draft_checker.py, then
presenting. See outclaw-plan SKILL.

**Tier-2 is opt-in.** When the user says "go deeper on <name>" or
"research <name> more", THEN call `leadbay_research_lead` +
`leadbay_tier2_persist.py` for that specific target. Do NOT Tier-2 the
full batch by default — the turn budget won't cover 15 × 3-min research
calls.

**2. Targeted research intent (user named a specific person/company)?**
Start at "Step 1 — Parse the input into a target" below.

**3. Never fabricate.** Every fact in a KB page body, plan angle, or
draft email MUST be traceable to a raw source file under
`~/.openclaw/outclaw/kb/raw/` or `kb/me/`. If you can't cite the file, you
can't include the fact. (See § Zero-hallucination rule.)

**4. No promise-then-silent turn closes.** Do NOT end a turn with "I'll
spin on that now", "surface shortly", "standby", "more to come". That
pattern is a silent failure — the agent yields control and never returns.
Either finish the work in this turn and present the results, or stop
cleanly at the last completed step with a short "I've done X / Y is next
— want me to continue?". The `draft_checker.py` promises-regex rejects
plans containing these phrases.

---

Your job: given a person (name, LinkedIn, email, company) or a discovery
intent ("find me someone at Acme worth talking to"), use every available tool
to build a **rich, persistent profile** and store it in the KB.

Output quality bar: **≥3 concrete, recent (≤30 day) signals** per target +
a section cross-referencing the target with `kb/me/` (mutual orgs, schools,
topics, connections). If you can't hit that bar, explicitly say what you were
blocked on — never paper over thin research with fluff.

## Use the tools you actually have

Check your **own tool list** at session start. Your ordering preference:

1. `leadbay_research_lead` / `leadbay_research_company` — if available, use first
2. `web_search` + `web_fetch` — baseline every OpenClaw agent has these
3. `read` (for local caches under `kb/raw/`)
4. User-provided text pasted into the conversation

If `leadbay_*` isn't in your tool list, that's fine — use `web_search` to
find the target's LinkedIn/Twitter/company page, `web_fetch` the specific
pages, and write what you actually learn into `raw/<slug>-<ts>.md`.
**Never insist on a tool that isn't in your active tool list.** Stating
"Leadbay isn't connected" is correct; pretending you used it is a
hallucination failure.

## Resolver mandate (non-negotiable)

Before creating or modifying any page under `~/.openclaw/outclaw/kb/` or
any entry in `memory/<tenant>/memory.jsonl`, read
`shared/references/RESOLVER.md` and file by primary subject, not by source
format or skill name. Use `shared/scripts/kb_ingest.py` + `kb_page.py` —
do not hand-craft file paths. Research facts go in `kb/{people,orgs,topics,places}/`;
runtime observations ("email bounced") go in per-tenant memory, not the KB.

## Zero-hallucination rule (non-negotiable)

Every signal, hook, career fact, org fact, and connection point MUST be
traceable to a real source — either a URL you fetched or a file you wrote
under `~/.openclaw/outclaw/kb/raw/`. If you cannot point at a real source,
do NOT write the fact. Leave the field empty and list it under `gaps[]`
in your return.

**Specifically forbidden:**
- Inventing a date ("March 2026 post", "€5M Series A in April 2026") without
  a URL or raw/ file that says so.
- Inventing a connection point ("HEC Paris alum", "both at Stripe") unless
  you can cite a line in `kb/me/self.md` or `kb/me/org.md`.
- Claiming you wrote a KB page without running the write command and
  reading the file back.

Producing plausible-sounding content you can't source is a hard failure
caught by the verification gate below.

## Preamble (skip if called from orchestrator)

```bash
SHARED="$(dirname "$(dirname "$(cd "$(dirname "$0")" && pwd)")")/shared"
bash "$SHARED/scripts/memory_search.sh" --type tool_inventory --limit 1
cat ~/.openclaw/outclaw/kb/me/self.md 2>/dev/null
cat ~/.openclaw/outclaw/kb/me/org.md  2>/dev/null
```

## Flow

### Step 1 — Parse the input into a target

The user gave you some combination of: name, LinkedIn URL, email, company,
title, company URL. From these, compute:

- `slug` — `kb_page.py` style: lower-case name, non-alnum → `-`, e.g.
  `alice-chen`. Disambiguate with company if needed (`alice-chen-stripe`).
- `display_name`
- `company` (if known) → compute an org slug the same way (`acme-corp`)

**Discovery intent** (e.g. "get me some leadbay leads", "pull a promising
lead", "purchase contacts for the best ones"):

**Leadbay is a sales inbox, not a queryable database.** See
`shared/references/leadbay-integration.md` for the full mental model.
Key rules:

1. **NEVER ask the user for "targeting criteria"** (industry, company
   size, geography, lead count, job titles). The user's ICP is already
   configured inside Leadbay. Asking for criteria = you're thinking of
   Leadbay as a DB, which it isn't.
2. **NEVER ask which titles to enrich** when the user says "recommended
   contacts" or "the best contacts" — `leadbay_enrich_titles` auto-picks
   based on the ICP. Recommended means Leadbay chooses.
3. **Verify your tool list FIRST.** Before attempting any Leadbay
   operation, check that `leadbay_pull_leads` (or at minimum
   `leadbay_account_status`) is in YOUR active tool list — not just
   `plugins.entries.leadclaw`. If the composite tools aren't bound to
   your agent, refuse per the template in `leadbay-integration.md`
   §"What to do when the composite tools aren't in your tool list".

**The canonical flow — four tool-call blocks, no improvisation:**

The flow is written so the agent only decides which lead_ids to deep-research.
Everything else is driven by helper scripts. Execute each block; paste the
literal stdout to the user. Do not paraphrase.

```bash
# --- Block 1: pre-counts + pull ---
BEFORE_ORGS=$(ls ~/.openclaw/outclaw/kb/orgs/ 2>/dev/null | wc -l | tr -d ' ')
BEFORE_PEOPLE=$(ls ~/.openclaw/outclaw/kb/people/ 2>/dev/null | wc -l | tr -d ' ')
echo "before: orgs=$BEFORE_ORGS people=$BEFORE_PEOPLE"
```

Then call the MCP tool `leadbay_account_status`, followed by `leadbay_pull_leads`
(no args). Save the pull response JSON to `/tmp/leadbay-pull.json` using your
Write tool.

```bash
# --- Block 2: Tier-1 persist + verification gate (MANDATORY) ---
python3 ~/.openclaw/skills/outclaw/shared/scripts/leadbay_tier1_persist.py \
  --from-file /tmp/leadbay-pull.json

AFTER_ORGS=$(ls ~/.openclaw/outclaw/kb/orgs/ | wc -l | tr -d ' ')
AFTER_PEOPLE=$(ls ~/.openclaw/outclaw/kb/people/ | wc -l | tr -d ' ')
N_LEADS=$(python3 -c 'import json; print(len(json.load(open("/tmp/leadbay-pull.json")).get("leads",[])))')
echo "after: orgs=$AFTER_ORGS (+$((AFTER_ORGS-BEFORE_ORGS))) people=$AFTER_PEOPLE (+$((AFTER_PEOPLE-BEFORE_PEOPLE))) / leads_pulled=$N_LEADS"
# GATE: the orgs delta MUST be > 0 while N_LEADS > 0. If zero, STOP — the
# persist step was skipped. Do not continue to block 3.

# --- Block 3: pick top N to deep-research (freshness-aware) ---
python3 ~/.openclaw/skills/outclaw/shared/scripts/leadbay_top_picks.py \
  --from-file /tmp/leadbay-pull.json --n 15 --stale-after-days 7
```

This returns `{ids: [...], summaries: [...], skipped_recent: [...]}`.
The `skipped_recent` array names any orgs we drafted a plan for in the
last 7 days — they are INTENTIONALLY deprioritised so the user sees
fresh targets day-to-day. Show the skipped list to the user with a note:
"Still in flight from <date> — include anyway?" Only re-add to the plan
if the user says yes.

**Tier-2 research is OPT-IN — do NOT run it for the full batch by default.**
The Tier-1 body already carries the Leadbay AI qualification excerpt +
tags + contact, which is enough for a Day-1 draft. Only call
`leadbay_research_lead` when the user says "go deeper on <X>" for a
specific target.

```bash
# --- Block 4: Tier-2 persist (per researched lead) ---
for f in /tmp/leadbay-research-*.json; do
  python3 ~/.openclaw/skills/outclaw/shared/scripts/leadbay_tier2_persist.py --from-file "$f"
done

# Final audit
ls ~/.openclaw/outclaw/kb/orgs/ | wc -l
ls ~/.openclaw/outclaw/kb/people/ | wc -l
tail -6 ~/.openclaw/outclaw/kb/log.md
```

After block 4, hand off to `outclaw-plan` with the list of slugs for the
top picks. Plan draws EVERY concrete fact from the Tier-2 org/person
pages — no improvised claims, no `[Your Name]` / `[Your Company]`
placeholders, no fabricated "recent Series C" unless it's on the page.

**Non-negotiable rules:**
- Block 2's gate must pass before you touch block 3. Orgs delta zero = STOP.
- Never paraphrase a script's stdout. Paste it as-is.
- Never claim a KB write that isn't visible in the post-counts or log tail.
- Use `enrich_titles` only when the user asks for richer contact coverage —
  `leadbay_pull_leads` already returns a recommended contact per lead.

If you find yourself writing the words *"what industry"*, *"what size"*,
*"which titles"*, STOP. You're asking the wrong question. Read
`shared/references/leadbay-integration.md` again.

### Step 2 — Check KB first

```bash
python3 "$SHARED/scripts/kb_search.py" --slug person:$SLUG
```

If an entry exists and its `last_updated` is ≤30 days, return it and ask the
user if they want a refresh. If yes, proceed. If no entry, proceed.

### Step 2.25 — Email-domain discipline

If you have an email address for the target, classify the domain BEFORE
deriving a company from it:

```bash
python3 "$SHARED/scripts/domain_classifier.py" "<email>"
```

- `private` (gmail, hotmail, yahoo, proton, yandex, icloud, …): the email
  is a personal mailbox. **Do NOT set `company` from this domain.** Use
  LinkedIn / Leadbay / the target's own statements instead.
- `isp` (comcast, bt, verizon, cox, …): residential internet provider —
  same rule. Do NOT infer employer.
- `school` (.edu, .ac.uk, hec.fr, mit.edu, stanford.edu, …): academic
  affiliation. Note it on the page as `## Affiliations` (school, not
  current employer) but do NOT treat as employer unless the target is
  confirmed faculty/staff.
- `corporate`: the domain IS the company. Use `company_slug_from_domain`
  result as the `kb/orgs/<slug>.md` target. Confirm by cross-checking
  LinkedIn / company URL when available.

Example wrong inference to avoid: "alice@gmail.com" → org slug "gmail".
The classifier catches that; the skill must ACTUALLY call the classifier,
not eyeball the domain.

### Step 2.5 — Cross-reference: past conversations + same-company people

Before running fresh external research, **sweep local context you already
have**:

**a. Past conversations with THIS person.** Query every connected
communication-capable tool for threads where the target appears as
sender or recipient. Priority order:

| Tool in inventory | Query |
|-------------------|-------|
| `gog` (Gmail)     | `gog gmail messages search "from:<email> OR to:<email>" --max 50 -j` |
| `email-mcp`       | same search via the MCP's search endpoint |
| `slack-mcp-server` / `slack` | `slack search --user <slack_id_or_email> --max 50` |
| `whatsapp-mcp-ts` / `wacli` | search conversation history by phone |
| `telegram-mcp`    | search chats where counterparty matches handle |
| `mac_messages_mcp` / `imsg` | iMessage/SMS history by phone or contact |
| `discord-mcp`     | DM history by user id |
| `linkedin-cli`    | InMail / message history with the profile URL |
| `apple-notes` / `things-mac` | search for user's own prior notes about the target |

For every match, record:
- Date of last interaction
- Direction (sent-by-user | received-from-target)
- Channel
- A one-line summary (don't paste the body — PII)

Drop a `raw/` snippet if the thread is substantive:
`kb_ingest.py begin person <slug> --note "prior-thread-<channel>-<date>: <summary>"`.

Under `## Prior conversations` on the target's page, list each match:
```
- 2025-11-14 · Gmail · user → target · "Intro from David, re: ICP pilot"
- 2026-02-03 · LinkedIn DM · target → user · "Circling back after SaaStr Annual"
```

**b. Signature extraction.** When a past email from the target exists,
parse the signature block. Useful fields to harvest INTO the KB
frontmatter (not prose):

- `phone` (if present)
- `linkedin_url` (if present — updates a missing field)
- `company` (only if the domain check said `corporate` AND the signature's
  stated company matches the domain; otherwise flag the conflict)
- `address`
- Confirmed current `title`

If the signature is an IMAGE (.png / .jpg attachment inline), transcribe
it via an available OCR-capable tool in your inventory:

| Tool | How |
|------|-----|
| `gemini` | `gemini describe --image <path> --prompt "Transcribe this email signature verbatim. Return fields: name, title, company, phone, email, address, socials."` |
| `image_generate` / multimodal fallback | pass the image bytes + the same prompt |
| `openai-whisper-api` | audio only — not applicable |

Write extracted fields onto the KB frontmatter via `kb_page.py upsert`.
Never invent fields — if the OCR result is unclear, log a gap, don't guess.

**c. People from the same company (if known).** If `company_slug` is
known (from email or LinkedIn), pull every page in the KB for that org:

```bash
# List all people with this org in their connections
grep -l "orgs: .*\b<company-slug>\b" ~/.openclaw/outclaw/kb/people/*.md
# Or the org's own backlinks:
python3 "$SHARED/scripts/kb_search.py" --slug org:<company-slug>
```

For each of those people, surface a one-line summary on the target's
page under `## Same-company context`:
```
- Bob Smith (CTO, kb/people/bob-smith.md) — active thread Mar 2026, warm
- Carol Wong (VP Sales, kb/people/carol-wong.md) — opted out 2025-10
```

If ANY same-company person has `contact_status: opt_out`, surface it
prominently — opt-outs propagate to company-level wariness but NOT to
automatic blocking (one person's opt-out doesn't ban outreach to their
whole org).

**d. Prior interactions with the ORG.** Same idea but at org-level —
reach into `kb/orgs/<slug>.md`'s existing body for any `## Update` or
`## Prior interactions` sections.

The summary of Step 2.5 goes into the target's page body BEFORE the
external-research sections you'll fill from Step 3. Past conversations +
same-company context are often the most valuable signals — they beat a
fresh LinkedIn scrape every time.

### Step 3 — Enrich, category-by-category

Read `references/research-playbook.md` for the full matrix. Summary:

1. For **each** outreach-relevant category present in the inventory, query
   **at least once**. Don't skip a category that's `ready` — if you do, plan
   quality suffers later and the evaluation will catch it.
2. Signals you're hunting for, in order of value:
   - Recent public posts / talks / podcasts (≤30 days)
   - Career trajectory (current role tenure, prior companies)
   - Topic interests (inferred from what they share / write)
   - Mutual connections with the user (from `kb/me/self.md`)
   - Contact info (for later planning only — never use it here)
3. Never fabricate. If a source doesn't yield a signal, move on.

Categories → tools (from inventory):
- `crm` → LeadClaw for full enrichment + ICP + relationship graph
- `professional_network` → LinkedIn for posts, tenure, connections
- `social` → Twitter/Bluesky for recent posts
- `research_web` → `browse`, `summarize` for company blog, podcasts, news
- `research_contacts` → `apple-notes`, `things-mac` if the user kept prior notes

### Step 4 — Write the KB

Delegate the file-writing to `shared/scripts/kb_ingest.py` + `kb_page.py`.

**Every target MUST:**
1. Begin with `kb_ingest.py begin person <slug> --name "<Display>"` — creates
   a raw/ entry tagged with the first source.
2. Have a body containing sections: `## Role & trajectory`, `## Recent activity
   (≤30 days)`, `## Topics & interests`, `## Connection points with <user>`,
   `## Sources`. Write via `kb_page.py upsert person <slug> --body <path>`.
3. Touch the org: `kb_ingest.py touch org <org-slug> --name "<Org>" --connection person:<slug>`.
   Also append a `## Update <date>` section to the org page with whatever you
   learned about it while researching the person.
4. Touch topics: for each interest, `kb_ingest.py touch topic <topic-slug>
   --connection person:<slug>`. Create stubs if missing.
5. Rebuild index: `python3 "$SHARED/scripts/kb_index_rebuild.py"`.
6. Log: `kb_ingest.py log ingest "<slug> research — <one-line summary>"
   --pages people/<slug>.md orgs/<org>.md topics/<topic>.md`.

### Step 4.5 — Verification gate (MANDATORY)

After every `kb_page.py upsert` and `kb_ingest.py touch`, **cat the file back
and include the first 40 lines under a `## Verified writes` section** in
your response. Example:

```bash
for p in ~/.openclaw/outclaw/kb/people/<slug>.md \
         ~/.openclaw/outclaw/kb/orgs/<orgslug>.md \
         ~/.openclaw/outclaw/kb/index.md \
         ~/.openclaw/outclaw/kb/log.md; do
  echo "--- $p ---"
  /usr/bin/head -40 "$p" 2>/dev/null || echo "MISSING: $p"
done
```

If any file is missing, STOP. Do not proceed to return. Report the failure
in plain language — "I couldn't write the KB page because X" — and exit.
Do NOT continue to Step 5 with fake content.

### Step 5 — Return

Return to caller:
- The KB page paths (relative to `~/.openclaw/outclaw/kb/`)
- An executive paragraph: role / why-now / 2-3 specific hooks / 1-2 connection
  points with the user
- What you *couldn't* find and why (blocked on LinkedIn auth? LeadClaw has no
  match? Their Twitter is private?)

Delegate deep multi-tool work to the `agents/person-researcher.md` sub-agent
when the target is rich enough to justify it.

## Degraded mode (no LeadClaw)

When the inventory has `crm=[leadclaw:missing]` or `:needs_setup]`:
- Skip ICP scoring + relationship-graph
- Rely on web search + LinkedIn + social for everything
- Quality score #3 (research breadth) will drop — that's expected and the
  user has been warned at setup time. Mention in the returned summary that
  Leadbay would unlock richer signals.

## What this skill does NOT do

- Does not plan outreach — that's `outclaw-plan`.
- Does not contact anyone.
- Does not fabricate signals. When in doubt, say "I couldn't find …".
