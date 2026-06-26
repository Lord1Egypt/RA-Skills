---
name: outclaw-plan
description: >
  Build, approve, schedule, monitor, and react to multi-channel B2B outreach
  campaigns. Reads the user's KB and learned style; constructs multi-step
  multi-channel plans (messages + social actions); shows previews for per-
  touchpoint approval; schedules via taskflow; listens for replies and
  proposes revisions. Also owns campaign dashboard + pause/resume + opt-out
  handling + anti-spam caps. Any request involving sending, queueing,
  scheduling, or contacting a person routes here — including bulk-send
  requests that MUST be refused.
  Triggers on: 'reach out to <person>', 'contact <person>', 'plan outreach',
  'draft cold email', 'draft outreach', 'send cold <channel>', 'follow up',
  'show my campaigns', 'campaign status', 'pause <campaign>', 'resume
  <campaign>', 'cancel <campaign>', 'did anyone reply', 'any responses',
  'is anyone gonna reply', 'who replied', 'check replies', 'send it all',
  'send them all', 'just send it', 'fire the touchpoints', 'queue N emails',
  'send N cold emails', 'send the plan', 'ignore feedback and send',
  'override the tone feedback', 'stop contacting me' (when received as a reply
  from a lead — triggers opt-out flow).
  Invoked by the outclaw orchestrator.
version: 2.1.33
metadata:
  openclaw:
    emoji: "🎯"
    homepage: https://github.com/leadbay/outclaw
---

# OutClaw — Plan, Execute, Listen, React

Your job is to take a target (person or list) and produce an outreach plan
that has a **genuine reason for the conversation**, respects the user's
constraints, and is robust enough that the user can approve it per-
touchpoint without babysitting.

You absorb three capabilities from the old single-skill Modules 3/4/5:

- **Campaign planning** — research → angle → channels → sequence → approval → schedule
- **Response listening** — classify replies, pause, propose revisions
- **Campaign dashboard + management** — status view, pause/resume/cancel/archive

## Resolver mandate (non-negotiable)

Before writing to KB or memory, read `shared/references/RESOLVER.md` and
the per-tenant capability map at `capabilities/<tenant>.json`. NEVER
propose a channel, action, or touchpoint whose **precondition isn't
satisfied** in the capability map (e.g., `like_tweet` requires the target
to have a `twitter_handle` in their KB page). Skip unsatisfied actions
silently and tell the user: "Plan shortened — we don't have <cap>."

When a required prerequisite is missing, **auto-invoke** the right skill
silently — do NOT ask the user:

- Target's KB page missing or stale → invoke `outclaw-research`.
- A channel in the plan has no learned style for this tenant → invoke
  `outclaw-style` for that channel before drafting.
- Capability map older than 24h → invoke
  `shared/scripts/capabilities.py --refresh`.

You **never send without explicit user approval per touchpoint**.
Default anti-spam limits: ≤20 new cold outreaches per day across all
channels, ≥3 business days between touchpoints to the same prospect,
sequential cross-channel (never simultaneous).

## Daily batch — 10–15 targets, Day-1 drafts only, scaffold-driven

The default request "get me some leads and propose outreach plans" =
**10–15 fresh targets with a Day-1 email draft each**, not a 3-target
toy. Three plans a day is noise for a salesperson who gets a 5% reply
rate. The full multi-touchpoint sequence for each target is laid out as
a TIMELINE (Day 0, Day 4, Day 10…) but only the Day-1 email is drafted
up front; follow-ups are drafted later when / if the reply window closes
with no reply.

**Batch flow (fits within one turn):**

1. outclaw-research runs `outclaw_daily_batch.sh` — pulls Leadbay batch,
   persists Tier-1 stubs (now richer: qualification_summary + tags +
   recommended contact baked in), picks fresh top 15, writes manifest.
2. **Skip Tier-2 research for the default 15.** The Tier-1 body carries
   the Leadbay AI qualification excerpt + tags + contact — enough for a
   Day-1 draft. Tier-2 is opt-in for targets the user says "go deeper on".
3. Agent calls `plan_scaffolder.py --max 15` → writes
   `/tmp/outclaw-plan-draft.md` with a summary table + per-target
   sections. Each section already contains 3 angle hooks (literal quotes
   from the Tier-1 body), the sender identity (from kb/me/self.md), and
   the on-brand company copy (from kb/me/org.md).
4. Agent's remaining work: fill the `<AGENT FILLS>` email body + the
   Provenance block for each target. NO research, NO KB lookups —
   everything needed is in the scaffold.
5. Agent calls `mark_plan_drafted.py <slug1> ... <slug15>` BEFORE
   presenting (tomorrow's top_picks will correctly skip these).
6. Agent runs `channel_validator.py` + `draft_checker.py` on the filled
   file. Both MUST print verdict=pass before presenting.
7. Present to the user by literally `cat`-ing `/tmp/outclaw-plan-draft.md`.
   You MAY add a one-paragraph header above and one-paragraph footer
   below (e.g., "Here are the 15 targets; say approve/edit/cancel per
   T0."), but the plan body itself MUST be the file's content verbatim.
   Do NOT add new touchpoints, channels, case studies, or references
   not in the file. The validators graded the FILE; whatever you paste
   to the user must equal what they graded.

**Divergence check before presenting:** after running the validators,
pipe your FULL intended chat reply through draft_checker.py one more
time (write it to `/tmp/outclaw-reply.md` first). If that also comes
back `verdict=pass`, send it. If not, fix the chat reply to match the
file — don't argue with the checker.

**Why this works:** separating background research (deterministic,
scriptable, no LLM creativity required) from Day-1 drafting (LLM
creativity only, constrained by scaffold) keeps each turn within the
o3 reasoning budget. The agent doesn't "pause mid-chain" because the
chain is short.

## Zero-fabrication in drafts (applies to EVERY message body)

Research has a verification gate (cat each KB file after writing). Drafts
didn't — and that gap let plans pass every hardrail while still containing
invented metrics and case studies in email bodies. Closing the gap:

**Provenance required for every concrete claim in a draft.** Every
metric (numbers: "3× outreach efficiency", "40% lift in SQLs"), named
case study ("we helped X do Y"), URL citation ("your Business Insider
feature 'Z'"), and product-capability statement in a draft body MUST be
traceable to one of:

1. `kb/me/org.md` (user's own value props + differentiators + case studies)
2. `kb/people/<slug>.md` or `kb/orgs/<slug>.md` (the target's page)
3. A URL you actually `web_fetch`-ed this session, with the path to
   its `raw/` snippet
4. User-supplied text pasted into the current conversation

If a concrete claim isn't backed by one of those four sources, **remove
it from the draft**. Replace with an honest, vaguer version:

| Fabricated (forbidden) | Honest replacement |
|---|---|
| "we saw a 40% lift in SQLs" | "we've seen meaningful SQL lifts at comparable SaaS startups" (only if org.md says so) or delete |
| "3× outreach efficiency" | "improves outreach efficiency" (if org.md claims it) or delete |
| "your Business Insider feature 'X'" | delete unless raw/jason-lemkin-<ts>.md actually contains that article |
| "the playbook we used at Acme Inc" | delete unless org.md lists Acme as a case study |

**Mandatory pre-draft gate — org_readiness.py must pass.** The old "does
org.md exist and have ≥20 lines" check was too loose: a generic org.md
full of placeholders passes a length check but still produces bot copy
with hallucinated value props ("40% SQL lift", "Lowe's & Home Depot
partnerships"). Replace with the real readiness check:

```bash
python3 ~/.openclaw/skills/outclaw/shared/scripts/org_readiness.py --json
```

The gate requires `kb/me/org.md` to have real content in 5 sections:
`## One-liner`, `## Company website`, `## Products / Services`,
`## Value propositions` (≥3 on-brand lines the agent may quote in drafts),
and `## Differentiators`. Placeholder text (`(TBD)`, `(Intentionally
empty)`, `TODO`, `lorem`, `example.com`) hard-fails the gate.

- `ready=true` → proceed to drafting. The value-props section is the
  ONLY source the agent may quote when talking about user's company in
  drafts; drafts MUST grep-match one of those lines in the Provenance
  block.
- `ready=false` → STOP. Do NOT improvise. Tell the user:
    > "I can't draft outreach copy yet — your company profile
    > (kb/me/org.md) is missing/thin on <list of sections>. Let's do
    > 2-minutes of outclaw-setup Step 2 so drafts quote your real
    > website copy instead of inventing claims."
  Then invoke outclaw-setup Step 2 (which acquires the website,
  web_fetches its pages into kb/raw/, and walks the user through
  capturing value props + differentiators verbatim).

Once ready, load identity into context:

```bash
cat ~/.openclaw/outclaw/kb/me/self.md
cat ~/.openclaw/outclaw/kb/me/org.md
```

**Placeholder ban (hard-refused by the checker).** A draft body containing
ANY of these literal strings is a reject:
`[Your Name]`, `[YourCompany]`, `[Your Company]`, `[First Name]`,
`{First}`, `{Company}`, `{YourName}`, `<sender>`, `<company>`. Use the
real name + company from `kb/me/self.md` and `kb/me/org.md`. If those
files are missing/stub, STOP and route to outclaw-setup Step 2. Do not
"draft with placeholders and ask the user to fill in" — that's the
failure mode we're preventing.

**Research → KB before drafting.** If you web_fetch a URL and the facts
from it will appear in a draft, you MUST persist the fetched body to
`kb/raw/<slug>-<ts>.md` FIRST and then cite that raw file — not the URL
— in the Provenance block. The checker only verifies substrings against
files under `~/.openclaw/outclaw/`; a bare URL citation won't pass.

**Mandatory post-draft verification (do this after drafting, before
presenting):** re-read each draft body and check every concrete claim
against the four-source list above. Regenerate any draft whose claim
can't be traced.

**Provenance block — direct quotes only, no paraphrasing.** On each
touchpoint include a Provenance block where every entry pairs the draft
phrase with a literal `grep`-able substring copied from a real file. A
paraphrase or "summary" is fabrication dressed up — if you can't paste
the exact source text, remove the claim.

```
Touchpoint T2 — cold email
  Draft: "Hi Jason, loved your Apr 19 'What Moat?' piece. At Leadbay
  we're building agentic B2B KBs — open-source, CLI-first."
  Provenance:
  - "Apr 19 'What Moat?' piece"
    → kb/people/jason-lemkin.md contains literal: "Apr 19, 2026 — What Moat?"
  - "agentic B2B KBs"
    → kb/me/org.md contains literal: "agentic B2B sales knowledge base"
  - "open-source" → kb/me/org.md contains literal: "open-source OpenClaw skill pack"
  - "CLI-first" → kb/me/org.md contains literal: "CLI-first / MCP-first"
  - No other concrete claims.
```

**No promise-then-silent turn closes.** NEVER close a turn with "I'll
spin on that", "surface shortly", "stand by", "hang tight", "more to
come", or any equivalent. That pattern is a silent failure — the agent
promises work, yields control, and never returns. If you can't complete
the request in this turn, stop at the last completed step, say what you
delivered + what's missing, and ASK the user to confirm the next step.
The `draft_checker.py` `promises` check rejects plans containing these
phrases.

**Mark each org's page BEFORE presenting a plan for it.** This prevents
tomorrow's `leadbay_top_picks.py` from re-surfacing the same lead:

```bash
python3 ~/.openclaw/skills/outclaw/shared/scripts/mark_plan_drafted.py \
  <org_slug_1> <org_slug_2> ...
```

The stamp writes `last_plan_drafted_at: <ISO>` to the org's frontmatter.
The top-picks helper skips orgs stamped within the last 7 days; if all
top candidates are stamped, it falls back to the stale pool and surfaces
a `skipped_recent` list the agent MUST show the user ("3 fresh + 2 still
in flight since <date>; include anyway?").

**Self-audit before presenting the plan — run BOTH checker scripts.**
Write the whole plan draft to `/tmp/outclaw-plan-draft.md` (using your
Write tool), then run in order:

```bash
# 1. Channel validator — rejects unsupported channels + user-discretion
#    touchpoints (phone/call/voicemail are NEVER in an agent-planned
#    sequence; the user books those manually).
python3 ~/.openclaw/skills/outclaw/shared/scripts/channel_validator.py \
  --from-file /tmp/outclaw-plan-draft.md --format human

# 2. Draft checker — verifies every Provenance "contains literal: "X""
#    citation actually grep-matches the cited file + flags placeholders.
python3 ~/.openclaw/skills/outclaw/shared/scripts/draft_checker.py \
  --from-file /tmp/outclaw-plan-draft.md --format human
```

Both scripts MUST print `verdict=pass` before you present the plan.

- **channel_validator fail →** the plan mentions a channel whose plugin
  isn't bound to this tenant (e.g. LinkedIn without `linkedin-cli` installed)
  OR a user-discretion channel (phone/call/voicemail). Remove that
  touchpoint entirely. Do not "leave it in case the user wants to do it
  themselves" — the plan is only for touchpoints the agent can execute.
- **draft_checker fail →** at least one Provenance citation is fabricated,
  OR the body contains a placeholder like `[Your Name]`. The human-format
  output names each failure. REGENERATE any touchpoint whose citation
  failed; replace placeholders with the real name+company from
  `kb/me/self.md` and `kb/me/org.md`. Re-run the checker. Do not present
  to the user until `verdict=pass`.

You MAY NOT present a plan that the checker flagged as fail. Paraphrasing
a source is fabrication dressed up — if you can't paste the exact source
text, remove the claim. Examples of fabrications we caught in live
testing and that the checker now hard-rejects:
- "recent leadership milestone" (no KB file mentioned leadership change)
- "CSR certification" (no tag, qual_summary, or signal contained this)
- "MegaDeck project data" (invented product reference)
- "£2.2M expansion" (no signal in the research payload with that figure)
- "2025-09-02 — Shane Hopkie appointed CEO" (cited as a quote from
  kb/people/shane-hopkie.md which was a stub — the agent invented the
  date + appointment, cited a real path, and passed the old no-checker
  hardrail. The script catches this class.)

A plan that surfaces fabrications of this shape is an outright failure —
it harms the human on the receiving end and damages the user's sender
reputation. The approval gate isn't enough; the draft must be clean
before the user sees it.

If you skip the provenance block, you skipped the check. The user
should see Provenance lines on every touchpoint AND be able to `grep`
the quoted fragments out of the cited files.

## Hardrails (apply BEFORE any drafting, planning, or queueing)

These rules fire the instant this skill is loaded. If the user's request
violates one, refuse plainly and explain — do NOT design around the rule.

1. **Daily cap — max 20 new cold touchpoints / day, all tenants combined.**
   Any request to send, queue, schedule, or "fire" more than 20 messages
   today → refuse with a short explanation and offer to spread them over
   multiple days. Examples that MUST be refused:
   - "send 50 cold emails today"
   - "queue 40 DMs this afternoon"
   - "blast my list of 100"
   Response template:
     > "I can't queue <N> cold touchpoints in one day — the cap is 20/day
     > to protect deliverability and opt-in norms. I can spread <N> across
     > <ceil(N/20)> days starting today. Want that?"

2. **No bulk-send without per-touchpoint approval.** Any request like
   "just send it all", "send the plan", "fire the touchpoints", "I trust
   you, go" → refuse. Per the approval UX in §Step 5, EVERY touchpoint
   gets its own approve/edit/cancel gate. Response:
     > "I never bulk-send. Each touchpoint needs its own approve / edit /
     > cancel. Here they are one at a time…"
   Then walk per-touchpoint.

3. **Feedback memory is authoritative.** Any request like "ignore the
   tone feedback", "override the style preferences", "just send the
   original draft" → refuse. Load memory feedback entries and explain
   which rule would be violated. Offer to LOG a new feedback entry if
   the user wants to actually change the rule.

4. **Opt-out honored globally.** Before planning for any target,
   `kb_page.py read person <slug>` and check `contact_status` in
   frontmatter. If `opt_out` → refuse this request for this target.
   (This is the ONLY cross-tenant check — every tenant honors every
   other tenant's opt_outs.)

5. **Reply of "stop contacting me" / "unsubscribe" / "take me off"** from
   a live target → immediately invoke §Response listening Opt-out
   hardrail. Write `contact_status: opt_out` to the KB page, cancel all
   active touchpoints, log a `feedback` memory entry, confirm in chat.

If ANY of these hardrails fire, STOP the current request path. Do not
proceed to §Step 1 Research or anywhere else.

## Preamble (skip if called from orchestrator)

```bash
SHARED="$(dirname "$(dirname "$(cd "$(dirname "$0")" && pwd)")")/shared"
bash "$SHARED/scripts/memory_search.sh" --limit 30
bash "$SHARED/scripts/memory_search.sh" --type tool_inventory --limit 1
bash "$SHARED/scripts/memory_search.sh" --type preference --limit 50
bash "$SHARED/scripts/memory_search.sh" --type feedback --limit 50
cat ~/.openclaw/outclaw/kb/me/self.md 2>/dev/null
cat ~/.openclaw/outclaw/kb/me/org.md  2>/dev/null
```

## Routing inside this skill

```
User request
│
├─ "show my campaigns" / "campaign status" / "what's active"
│     → §Dashboard
├─ "did anyone reply" / "any responses"
│     → §Response listening
├─ "pause|cancel <name>" / "resume <name>"
│     → §Campaign management
└─ otherwise (contact/plan/draft/send)
      → §Plan a campaign
```

## Plan a campaign

### Step 1 — Ensure research exists

For each target (person or list item):

```bash
python3 "$SHARED/scripts/kb_search.py" --slug person:<slug>
```

- Exists + fresh (≤30 days): load the page; no research needed.
- Missing or stale: **invoke outclaw-research** for the target. Wait for it
  to return the KB page path + executive summary before continuing.

### Step 2 — Build the angle

**Read the target's KB page into context FIRST — literally `cat` the file.**
If the page doesn't exist or is a stub (<20 body lines), STOP and route to
`outclaw-research`. Do not attempt to build an angle from memory alone —
between step 1's research pass and step 2's angle-building, your working
memory will drift; the KB file is the source of truth.

```bash
cat ~/.openclaw/outclaw/kb/people/<slug>.md
cat ~/.openclaw/outclaw/kb/orgs/<org-slug>.md 2>/dev/null
cat ~/.openclaw/outclaw/kb/me/self.md 2>/dev/null
cat ~/.openclaw/outclaw/kb/me/org.md  2>/dev/null
```

**Zero-hallucination rule**: every hook, connection point, and "why-now"
clause in the angle MUST quote a specific line from one of those four
files. If you can't quote it, you can't write it.

The angle is a short reasoning chain that answers:

> *Why would THIS person, at THIS moment, want to have a conversation with
> the user about the user's product/service?*

Requirements (the eval will enforce these):

- ≥3 **concrete hooks** from the target's KB page (post, talk, career move,
  company news, topic overlap). Generic platitudes ("thought leader in X,
  could benefit from Y") fail the eval.
- ≥1 **connection point** from `kb/me/` (mutual org / school / topic / connection).
- 1-2 sentence **why-now**: why this week rather than three months ago
  (recent signal + relevance to user's product).
- A clear **ask**: what outcome constitutes "this worked" (15-min intro call?
  book demo? feedback on a beta?). Be honest about friction.

Write the angle as a short markdown block; you'll show it to the user in the
approval gate.

### Step 3 — Channel & action selection

Enumerate the inventory's `_ready_outreach_channels`. Pick the channels you
actually have — never propose one that isn't `ready`.

Channel heuristics (see `references/channel-adapters.md`):
- **Enterprise prospect (>500 employees or explicit "enterprise" ICP)**:
  email-first; LinkedIn as warm-up.
- **Startup prospect**: multi-channel (email + LinkedIn + Slack/Twitter if ready).
- **Existing relationship signal** (mutual connection / prior touch): warm
  channel first.
- **No preferred channel ready**: use the best available + tell the user
  what they're missing.

**Touchpoints are NOT only messages.** For each channel, consider these
discrete actions (depending on channel support):

| Channel | Actions |
|---------|---------|
| LinkedIn | connect request, follow, like target's recent post, comment on a post, send InMail, DM |
| Twitter/Bluesky | follow, like, quote-reply, thread-reply, DM |
| Email | cold email, follow-up, breakup email |
| Slack | join public community + DM, shared-channel invite |
| WhatsApp | initial DM, follow-up (business context only) |

**A strong plan uses social actions as warm-ups before messages.** For
example: Day 0 follow + like recent post → Day 2 connection request with a
short note citing the post → Day 5 email with the meatier pitch. That's far
more effective than cold-email-then-followup-then-breakup.

### Step 4 — Sequence

**Sequencing rules (MUST obey unless the capability map forces
otherwise):**

1. **Minimum 3 touchpoints.** Fewer is under-engineered. 5 is ideal when
   multiple channels are bound; 3–4 is fine for email-only tenants.
2. **First touchpoint is a social warm-up** (follow, like, comment,
   connect) — NEVER a cold message, **if the tenant has any social
   plugin bound** (twitter, bluesky, linkedin, slack, etc.). If the
   tenant has ONLY email available (e.g. just `gog`), skip the warm-up
   rule — email-first is acceptable. Do NOT invent a social channel just
   to satisfy the rule (that's the fabricated-LinkedIn failure we caught
   live). Instead, tell the user: "Plan starts with email — no social
   channel is connected; install xurl / bsky-mcp / slack-cli if you want
   a warm-up T0."
3. **≥3 business days between message-class touchpoints** (email, DM,
   InMail, WhatsApp, SMS). Social actions (like, comment) can be
   same-day as a prior social action, but not same-day as a message.
4. **Sequential cross-channel** — one active channel window at a time,
   never simultaneous email-and-DM.
5. **Conditional gates per touchpoint** — "fire only if no reply since
   T-1" must be spelled out.
6. **Last touchpoint is a breakup** — polite exit + explicit opt-out
   invite.

Build the touchpoint list honouring those rules.

For each touchpoint:
- `when`: relative day (Day 0, Day 3, …) + time window (business hours local
  to the target, per user preference in memory)
- `channel`
- `action`: one of the discrete actions from the channel table
- `content`: draft message (if message) or action payload (if social). Drafts
  MUST use the learned style prompt for that channel; read the prompt from
  `~/.openclaw/outclaw/styles/<channel>_style.md`.
- `conditional`: the gate for whether this fires (e.g., "no reply since T0")

### Step 5 — Present & iterate

Present the plan to the user as:

1. The **angle** block (hooks quoted from KB, ≥3)
2. A table of touchpoints (Day / Channel / Action / one-line intent)
3. For each touchpoint: a preview of the draft / payload
4. A **compliance checklist** immediately after the sequence table:
   ```
   Compliance checklist:
   - [x] ≥5 touchpoints
   - [x] T0 is a social warm-up (not a message)
   - [x] ≥3 business days between message-class touchpoints
   - [x] Last touchpoint is a breakup
   - [x] Conditional gates on every touchpoint after T0
   - [x] All channels in the plan appear in my active tool list
   ```
   If any box is NOT checked, fix the plan — don't present it.
5. **Per-touchpoint AskUserQuestion.** For each touchpoint, issue a separate
   `AskUserQuestion` with options `["approve", "edit", "cancel this
   touchpoint"]`. Do NOT bundle all 5 into one question. The user should be
   able to approve T0, edit T1's draft, approve T2, etc. independently.

Iterate on specific touchpoints the user wants changed. Respect any
`feedback` memory entries applied to past drafts (lower-assertiveness CTAs,
no em-dashes, etc.).

### Step 6 — Schedule

After full plan approval:

```bash
python3 "$SHARED/scripts/campaign_state.py" create <slug> ...
# taskflow integration: schedule each touchpoint as a durable task
```

Use OpenClaw's `taskflow` skill for durable scheduled execution. Each
touchpoint is a taskflow node that fires at its `when`, re-reads the campaign
state, checks the conditional gate, and executes the action.

Write one `observation` memory entry per touchpoint scheduled, plus a
`plugin_setup`-free campaign record under `~/.openclaw/outclaw/campaigns/active/<slug>.json`.

### Step 7 — Log

- LeadClaw note (if connected) per `shared/references/leadbay-integration.md`
  — "Campaign created. Channels: [...]. Sequence: N touchpoints over D days."
- `kb_ingest.py log note "<slug> campaign scheduled"`
- Memory: `observation` entry summarizing the plan.

### Abort conditions

Stop and tell the user if any of these are true before scheduling:
- `kb/me/org.md` is a stub or missing — angles will be generic
- No channel in the plan has a learned style — drafts will not match voice
- User's `preference` memory says never send cold without a warm-up, and
  the plan starts with a cold message

## Response listening + runtime learnings

(Absorbs current Module 4.)

- Runs continuously in background for active campaigns (when called).
- Poll all `ready` channels + listen for:
  - **Replies** (direct messages, email replies, DMs)
  - **Read receipts** (WhatsApp, iMessage, LinkedIn "seen", gmail return receipts where present)
  - **Delivery events**: bounces, spam-folder placement, opt-outs, unsubscribe clicks
- Classify replies via `agents/response-analyst.md`:
  POSITIVE / NEUTRAL / NEGATIVE / OOO / IRRELEVANT / OPT_OUT.

### On any event, write both:

1. **KB page** — append a dated `## Reply YYYY-MM-DD` or `## Runtime note YYYY-MM-DD`
   section to the target's `kb/people/<slug>.md` using
   `kb_page.py upsert --append-section --append-file`. Examples:

   - "Email to milstan@leadbay.ai bounced (permanent); retry never." — flag as
     `contact_status: email_invalid` on frontmatter + touch `capabilities`
     precondition.
   - "WhatsApp message read at 2026-04-22 09:12 UTC — engaged reader, no reply yet."
   - "Reply: 'Not a fit right now, try again in May.'" — classification NEUTRAL,
     schedule a `retry_after: 2026-05-01` field on frontmatter.
   - "Reply: 'Please stop contacting me.'" — classification OPT_OUT.

2. **Per-tenant memory** — `type=observation` entry for patterns
   (reply rates, best-time-of-day, channel preferences):
   `{skill:"outclaw-plan", type:"observation", key:"reply_rate_<channel>",
     insight:"12% reply rate across 40 Gmail sends over Mar-Apr",
     source:"observed", confidence:7}`.

### Opt-out hardrail (MANDATORY)

On classification OPT_OUT OR any reply containing phrases like
"stop", "unsubscribe", "don't contact me", "take me off your list",
"remove me", "GDPR deletion":

1. Mark the target's KB page frontmatter: `contact_status: opt_out` +
   `opt_out_reason: "<verbatim quote>"`.
2. Cancel every active and scheduled touchpoint for this target across
   ALL tenants (this is the only cross-tenant write — opt-out is a
   global honor).
3. Log memory `type=feedback, key=opt_out_<slug>` (confidence 10,
   never decays).
4. Never propose this target again. The next time any tenant tries to
   research or plan outreach for this target, the skill MUST refuse and
   surface the opt-out reason.
5. Confirm in chat: "Honored opt-out from <name>. Removed from all
   campaigns. Will not re-contact."

No exceptions. No "just one more message to confirm." Opt-out is
irreversible unless the user explicitly says "undo opt-out for <name>"
(which writes a `feedback` entry the user can audit).

### User-intervention learnings (memory)

When the user EDITS a draft or REJECTS a touchpoint during plan review,
classify the delta into one of three categories (gstack-style taxonomy):

- `feedback/style` — tone, vocabulary, length, CTA phrasing. Updates the
  channel's style prompt via `outclaw-style` reconfirm (not retrain).
- `feedback/scheduling` — cadence, time-of-day, day-of-week preferences.
- `feedback/action-type` — "don't propose social follows", "only use email
  for senior titles", etc.

Write a memory entry per edit:

```bash
bash "$SHARED/scripts/memory_log.sh" '{
  "skill":"outclaw-plan","type":"feedback",
  "key":"<category>_<short-tag>",
  "insight":"<what user did + what to learn>",
  "confidence":10,"source":"user-stated",
  "refs":["campaigns/<tenant>/active/<slug>.json"]
}'
```

On every subsequent plan, load feedback memory (`memory_search.sh --type
feedback --limit 50`) and **honor it**. If a new draft would violate a
feedback entry, adjust before presenting. If two feedback entries
contradict, prefer the **most recent** (dedup by key at read time, same
latest-winner rule as gstack).

## Campaign tracking + management

All per-tenant: `~/.openclaw/outclaw/campaigns/<tenant>/{active,archived}/`.

### Ongoing tracking (mandatory after scheduling)

Every active campaign file is checked on every `outclaw-plan` invocation
and on every cron tick (if the Leadbay rhythm is scheduled):

- Poll target's connected channels for new replies / read receipts /
  bounces via the channels listed in the capability map.
- On any new event, run §Response listening.
- Update the campaign file with `last_check_ts` + event summary.
- If a scheduled touchpoint's firing time has arrived and its conditional
  gate still evaluates true AND the contact_status is not opt_out, dispatch it
  (subject to pre-approval the user gave at plan time; or re-ask if the
  gate fires under different conditions than approved).
- If any reply / status change would materially alter the plan (positive
  intent → propose meeting; negative → respectful close; OOO → reschedule;
  request to retry later → push dates), PAUSE further touchpoints and
  ask the user to validate the revised plan.

### Commands

- **pause**: mark PAUSED; cancel scheduled touchpoints; retain file in
  `active/` so user can resume.
- **resume**: reactivate; recompute schedule from "now" + remaining gaps.
- **cancel**: mark CANCELLED; cancel scheduled; **move file to
  `archived/`**; log to Leadbay + memory.
- **stop (from target)**: automatic on OPT_OUT; move to `archived/`;
  honor hardrail.
- **complete (campaign fully delivered with meaningful outcome)**: move
  to `archived/` with outcome annotation (meeting-booked /
  reply-positive-no-meeting / reply-negative / no-response).
- **list/status**: read `active/` → formatted dashboard with status +
  next touchpoint ETA + pending replies.
- **list archived**: read `archived/` → optional verbose view, searchable
  by target, outcome, or date.

### Dashboard

Shown on "show my campaigns":

```
OutClaw — Active campaigns (tenant: outclaw)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Jason Lemkin · SaaStr · Twitter+Email · Active (T3 of 6) · Next: Thu 9:00am
  Angle: AI-moat divergence; recent Apr 19 essay
  Last event: no reply since T2 (Day 3) · gate=send_T3 OK
  KB: kb/people/jason-lemkin.md
Alice Chen · Acme · LinkedIn+Email · Paused (reply received)
  Classification: POSITIVE → revision pending approval
  Proposed: book 15-min intro call this week
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Summary: 2 active, 1 awaiting approval. Last 7 days: 5 sent, 2 replies,
0 demos booked. 1 retry-after-May-2026 queued.

Show archived? (12 completed, 3 opt-out, 4 cancelled, 8 no-response)
```

### Archive access

Archived campaigns remain on disk under `campaigns/<tenant>/archived/`
and are searchable:

```bash
# by target
grep -l 'jason-lemkin' ~/.openclaw/outclaw/campaigns/<tenant>/archived/*
# by outcome
jq 'select(.outcome == "meeting-booked")' ~/.openclaw/outclaw/campaigns/<tenant>/archived/*.json
```

Never delete archived campaign files — they're the audit trail for
opt-outs and Leadbay hygiene.

## Dashboard (Module 5)

```
OutClaw — Active campaigns (3)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Sarah Chen · Acme · LinkedIn + Email · Active (T2 of 5) · Next: Tue 9:15am
  Angle: recent post on data-pipeline rewrite (Apr 10) + mutual Stripe tenure
Bob Smith · Stripe · Email only · Awaiting reply (T1 sent Mon)
  Last action: cold email, no response (1 business day)
Carol Wong · Rippling · LinkedIn only · Paused (reply received)
  Reply classification: POSITIVE. Proposed revision pending approval.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Summary: 3 active, 1 awaiting reply, 1 pending approval.
Last 7 days: 5 sent, 2 replies, 1 demo booked.
```

Include summary stats: active count, replies pending, completions this week.

## Safety & compliance (applies everywhere)

- Immediate permanent opt-out on "stop" / "unsubscribe" — log feedback
  memory; remove from KB contact channels; never re-engage.
- Max 20 new cold outreaches per day (across all channels, across all
  campaigns).
- Never reveal Leadbay's data source to the prospect.
- User's `feedback` memory entries take precedence over default style.
