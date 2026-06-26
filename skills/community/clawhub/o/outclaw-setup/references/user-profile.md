# Capturing the user's profile into `kb/me/`

This is the NEW step the 1.x wizard was missing. Research + planning ground
themselves in `kb/me/self.md` (the user as a person) and `kb/me/org.md` (the
user's company + products + ICP). Without these, drafts are generic and
angles are shallow.

## When to run

- Unconditionally during initial setup (Step 2 of outclaw-setup).
- Re-run when the user says "update my profile" or the pages are >6 months old.

## `kb/me/self.md`

### Required sections

```markdown
---
name: Milan Stankovic
slug: self
type: me
last_updated: 2026-04-21T16:00:00Z
confidence: 10
---
# Milan Stankovic

## Role
CEO at Leadbay (Apr 2023 – present). Previously founder-in-residence at
[…], principal engineer at […].

## LinkedIn / public presence
- LinkedIn: https://linkedin.com/in/milstan
- Twitter: @milstan
- Blog: blog.example.com

## Location
San Francisco, CA

## What I'm working on right now (2-3 sentences)
Building Leadbay — agentic B2B knowledge base. Main focus: making ICP
scoring actually reliable. Writing publicly about agentic workflows.

## Topics I engage with publicly
- Agentic AI, LLM tooling, ICP scoring, founder ops, sales intelligence

## Education
- PhD, University of X (2016)
- MSc, University of Y (2012)

## Prior companies
- Company A (2018-2022): role
- Company B (2016-2018): role
```

### How to fill it

1. If `gog` is connected, check `gog auth list` for the primary email. Use
   that as a seed for name ("email@company → guess").
2. Ask the user one question at a time, not all at once. Prefer
   AskUserQuestion with 2-3 options where possible ("Is your current role…?")
   and free-form for things like "what are you working on right now".
3. For LinkedIn, ask for the URL. Don't scrape it — the user will confirm the
   role/history manually.
4. For prior companies, ask 1-2 top ones that matter for mutual-connection
   matching. Don't demand a CV.
5. Save draft to `/tmp/me-self.md` then:
   ```bash
   python3 "$SHARED/scripts/kb_page.py" upsert me self --body /tmp/me-self.md --confidence 10
   ```

## `kb/me/org.md`

### Required sections

```markdown
---
name: Leadbay
slug: org
type: me
last_updated: 2026-04-21T16:00:00Z
confidence: 10
---
# Leadbay

## One-liner
Agentic B2B knowledge base for sales and revenue ops teams.

## Products / services (list everything you sell)
- Leadbay platform (SaaS, per-seat)
- LeadClaw — OpenClaw plugin for Leadbay data access
- Agentic workflows for SDR teams (onboarding services)

## Ideal Customer Profile
- Industries: B2B SaaS, developer tools, infrastructure
- Company size: 50-500 employees
- Geography: North America, EU
- Buyer personas: VP of Sales, Head of RevOps, founder-led-sales startups
- Disqualifiers: <10 employees, consumer-only, agencies reselling data

## Value propositions (3 core, ranked by importance)
1. Keep every prospect interaction in one agentic KB so context compounds
2. Reliable ICP scoring that actually holds up when deals close/lose
3. Dev-first: CLI and MCP-accessible, not a UI-only platform

## Differentiators vs. obvious competitors
- vs. Apollo/ZoomInfo: fresher data, CLI-first, agentic-native
- vs. hand-rolled CRM notes: structured, searchable, cross-team

## Recent wins / case studies (1-3, used as social proof in drafts)
- Case A: reduced SDR ramp time from 12 to 4 weeks for <Customer>
- Case B: lifted reply rate 2x for <Customer>'s outbound

## Pricing snippet (if the user wants to share)
$X/mo, Y seats, annual discount, custom enterprise.
```

### How to fill it

1. **If LeadClaw is `ready`**: pull `leadclaw.get_user_org()` (or equivalent
   taste-profile endpoint). Pre-fill the page with what Leadbay already
   knows. Then for each section, ask the user to confirm/edit.
2. **If LeadClaw is missing**: interview the user section by section. Don't
   skip — every section shows up in angle-building later.
3. The ICP section is load-bearing for planning. If the user is uncertain,
   push back: "To plan good outreach I need to know who your ideal customer
   looks like. Let's start with industry — who do you close the most?"
4. Save draft to `/tmp/me-org.md` then upsert.

## Completion check

Before moving to Step 3 (style learning), verify:

```bash
python3 "$SHARED/scripts/kb_page.py" read me self  | /usr/bin/head -20
python3 "$SHARED/scripts/kb_page.py" read me org   | /usr/bin/head -20
```

Both must have non-stub bodies (>20 lines of content). If the user insists on
skipping, set `confidence: 3` on the page and log a `preference` memory entry
warning that planning will degrade.

## Re-entry

"Update my profile" / "my role changed" → read the existing page first and
ask what specifically changed. Don't re-interview from scratch. Append a dated
section if the change is partial; rewrite the page if the change is whole-sale.
