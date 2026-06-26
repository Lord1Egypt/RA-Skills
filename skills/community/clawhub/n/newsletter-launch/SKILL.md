---
name: newsletter-launch
description: >
  Plug-and-play newsletter launcher. Runs a short setup wizard, then
  scaffolds all project files and wires up all automation crons for a
  fully operational newsletter in one conversation.
  Use when starting a new newsletter from scratch or setting up a second
  newsletter on a new topic.
  Triggers on: 'launch a newsletter', 'new newsletter', 'start a newsletter',
  'set up a newsletter', 'create a newsletter', 'second newsletter',
  'newsletter on [topic]'.
  NOT for: editing an existing newsletter, writing issues, or keyword research.
  Requires: newsletter-seo-pipeline skill must be installed.
---

# Newsletter Launch

## Phase 1 — Dependency Check

Before the wizard starts, run this check silently. Do not narrate it.

Check whether each of these 7 skill folders exists under `~/.openclaw/workspace/skills/`:

| # | Skill folder | ClawHub slug | What it does |
|---|-------------|-------------|---------------|
| 1 | `newsletter-seo-pipeline` | `newsletter-seo-pipeline` | Core production workflow — SEO validation, AI scoring, paste doc generation (quality gates built-in) |
| 2 | `serp-analysis` | `serp-analysis` | Analyzes Google search results for your keyword so we know what we're competing with |
| 3 | `seo-content-engine` | `seo-content-engine` | Builds a keyword-optimized article outline with H2/H3 structure |
| 4 | `article-writing` | `article-writing` | Writes long-form content in a consistent, human voice |
| 5 | `de-ai-ify` | `de-ai-ify` | Strips AI-sounding language and restores human tone (required if AI score < 8/10) |
| 6 | `markdown-formatter` | `markdown-formatter` | Cleans up formatting so the final article pastes cleanly into beehiiv |

**If all 6 are present:** proceed silently to Phase 2 (wizard).

**If any are missing:** show the user this message, listing only the missing ones by number:

> *"Before setting up your newsletter, I need to install [N] tool(s). Here's what's needed:*
>
> [list only missing skills with their number and one-liner from the table above]
>
> *Reply with the numbers you want to install (e.g. "1 2 3"), "all" to install everything, or "skip [number]" to leave one out. I'll explain any you're unsure about."*

For each approved skill:
- Run: `openclaw skills install <clawhub-slug>` (use the ClawHub slug column from the table above)
- Confirm install succeeded before moving to the next
- If install fails, tell the user: *"[Skill name] failed to install — you can try manually with `openclaw skills install <slug>` or skip it for now. The workflow will still run but [specific step] won't work without it."*
- Note: quality gates are built into `newsletter-seo-pipeline` — no separate QVP install needed.

Only proceed to Phase 2 once all approved installs are complete (or skipped with the user's consent).

Also verify `python3` is available: run `python3 --version`. If missing, stop and tell the user Python 3 is required.

## Phase 2 — Setup Wizard

On first run (no config file at `skills/newsletter-launch/.skill-config/<slug>.json`):

Tell the user: *"I'll ask you 11 quick questions — takes about 2 minutes. I'll handle everything after that: project files, writing style guide, automation, crons. Let's go."*

Ask these questions **one at a time**, in order. Do not batch them.

---

**Q1 — Newsletter name**
*"What's the name of your newsletter?"*

---

**Q2 — Audience**
*"Who is it for? One sentence — who reads it and what do they do?"*

---

**Q3 — Topic / niche**
*"What's the core topic? (e.g. HVAC contractor business tips, personal finance for nurses, SaaS growth tactics)"*

---

**Q4 — Writing style**

*"A few quick questions to set your newsletter's voice. Answer in plain words — there's no wrong answer:"*

Ask all three sub-questions together (this is the one exception to one-at-a-time):

> a) *Who is your reader, really? (e.g. busy solo operators who skim on mobile, corporate managers who expect data, hobbyists who love detail)*
>
> b) *What tone fits your brand? (e.g. direct and no-fluff, warm and encouraging, dry and witty, authoritative and formal)*
>
> c) *Any words or phrases your audience uses that you definitely want included? Any they'd hate? (e.g. 'our readers say ROI not revenue, and hate the word leverage')*

Store answers as `style_reader`, `style_tone`, `style_vocab` in config.
These feed directly into the generated `writing-style.md`.

---

**Q5 — Monetization**
*"How do you plan to make money from it? (e.g. sponsorships, affiliate links, paid tier, or not sure yet)"*

---

**Q6 — Seed keywords**
*"Give me 3–5 keywords your audience would search for. These seed your SEO research. (e.g. 'hvac contractor pricing guide, flat rate plumbing pricing, home service business tips')"*

---

**Q7 — Beehiiv setup**
*"Is your Beehiiv account already created?"*

- **Yes** → proceed to Q7
- **No** → say: *"No problem. Here's what to do: go to beehiiv.com, click Get Started, create your publication. Takes 5 minutes. Come back when it's done and we'll continue."* Then pause and wait.
- **Need instructions** → show contents of `references/beehiiv-setup.md`, then wait.

---

**Q8 — Beehiiv credentials**
*"Two things from your Beehiiv settings:*
*1. Publication ID — Settings → Publication → scroll to Publication ID (looks like pub\_xxxx...)*
*2. API Key — Settings → Integrations → API → New API Key → copy it immediately."*

Accept both values. If user can't find them, reference `references/beehiiv-setup.md`.

---

**Q9 — Auto-publishing**
*"Are you on Beehiiv's Scale or Enterprise plan? ($39+/month)*
*If yes, I can configure auto-publishing — issues go live automatically, no copy-pasting.*
*If no (free plan), I'll generate a paste-ready doc each issue instead."*

- **Yes (Scale/Enterprise)** → set `auto_post: true`. Note: full API write access enabled.
- **No / Not sure** → set `auto_post: false`. Paste-ready docs will be generated.

---

**Q10 — Affiliate tag (optional)**
*"Do you have an affiliate tag to include in recommendations? (e.g. Amazon Associates tag like 'mynewsletter-20') — skip if not applicable."*

---

**Q11 — Timezone**

*"What timezone should your newsletter run on? This controls when crons fire (e.g. Monday 9AM will be 9AM in your timezone). Examples: America/New_York, America/Chicago, America/Los_Angeles, Europe/London, Australia/Sydney. Skip to default to America/Chicago (US Central).*"

Store as `timezone` in config. Pass to `build_crons.py` for all cron schedules.

---

**Confirmation**

Summarize all answers clearly, then ask: *"Does this look right? I'll build everything once you confirm."*

Wait for explicit confirmation before proceeding.

---

## Phase 3 — Build

### Step 1: Write config
Assemble the config JSON matching the schema in `references/config-schema.md`.
Generate the slug from the newsletter name: lowercase, hyphens, no special chars.
Write config to the **newsletter project folder** (not the skill):
`projects/<slug>/<slug>-config.json`
This keeps each newsletter's configuration isolated and prevents collisions when multiple newsletters are created.
After writing, verify the file exists and contains the config. If verified, **remove any config file from the skill's `.skill-config/` directory** to prevent stale config from interfering with future newsletter setups.

### Step 2: Generate writing style guide
Using the `style_reader`, `style_tone`, and `style_vocab` answers from Q4, write a custom `writing-style.md` to:
`projects/<slug>/writing-style.md`

**This file lives in the newsletter's project folder** — each newsletter has its own. The scaffold script (Step 3) generates a base version from the config; the agent should also generate it directly here using the full wizard answers for richer output.

Use this structure:
```
# Writing Style Guide — [Newsletter Name]

## Reader Profile
[Expand style_reader into 2-3 sentences describing who is reading, their context, how they consume content]

## Tone
[Expand style_tone into 4-6 concrete tone rules, e.g. "Active voice always", "Lead with the dollar figure or business impact"]

## Language Rules
**Use:**
[3-5 words/phrases from style_vocab the audience uses or expects]

**Never use:**
[3-5 words/phrases the audience dislikes or that sound generic/AI]

## Structure
- Short paragraphs: 2-3 sentences max
- One actionable takeaway per section
- Single CTA at close
- [Add 1-2 structure rules specific to the tone/reader]

## The Skim Test
[Write a one-sentence skim test tailored to this audience — e.g. "If a contractor can skim in 90 seconds and know what to do, it passes."]
```

After writing the file, confirm its path to the user.

### Step 3: Scaffold project files
Use the absolute path to the script (resolved from this skill's directory) and point it to the config in the **newsletter project folder**:
```
python3 <skill_dir>/scripts/scaffold_newsletter.py projects/<slug>/<slug>-config.json
```
Verify all files were created (check output).

### Step 4: Build and create crons
Generate the cron definitions, pointing to the config in the **newsletter project folder**:
```
python3 <skill_dir>/scripts/build_crons.py projects/<slug>/<slug>-config.json
```
Read the JSON output. Create each of the 4 crons using the OpenClaw cron tool.

Cron type rules (critical — wrong type will break the cron):
- `sessionTarget: isolated` + `payload.kind: agentTurn` — Research and Quarterly Keywords crons
- `sessionTarget: main` + `payload.kind: systemEvent` — Write and Evergreen crons

Create all fields from the JSON: name, schedule, sessionTarget, payload, delivery, failureAlert.
Confirm each cron was created successfully before moving to the next.

### Step 5: Test scripts
Resolve the newsletter-seo-pipeline skill directory. Create a minimal test file and run the validator:
```
echo 'Meta Title: Test\nMeta Description: Test description here for validation purposes only.\nURL Slug: test\nPrimary Keyword: test\n# Test' > /tmp/nsp-test.md
python3 <newsletter_seo_pipeline_skill_dir>/scripts/validate_seo.py /tmp/nsp-test.md test
```
- If output contains 'SEO Validation Report': scripts are working correctly
- If output is `python3: can't open file` or `No such file or directory`: the script path is wrong — check that newsletter-seo-pipeline installed correctly with `ls <skill_dir>/scripts/`
- If `python3` itself errors: Python 3 is not installed or not on PATH

Clean up: `rm -f /tmp/nsp-test.md`

### Step 6: Confirm to user

Send a summary:

```
✅ [Newsletter Name] is live and automated.

📁 Project files (all in projects/<slug>/):
  • project.md — project memory
  • writing-style.md — your custom voice guide
  • issue-log.md
  • issue-template.md
  • seo-research-brief.md (seeded with your keywords)
  • issue-001-collection.json (ready for research)

⚙️ Crons active (all times CT):
  • Research: Tue/Thu/Sat 9AM — collects items for next issue
  • Write: Monday 9AM — full skill stack, alerts you when ready
  • Evergreen: 1st of month 9AM — monthly SEO guide
  • Keyword refresh: Jan/Apr/Jul/Oct 1st — replenishes keyword bank

📋 Next steps for you:
  [ ] Submit sitemap to Google Search Console:
      https://<slug>.beehiiv.com/sitemap.xml
      (Settings in Google Search Console → Sitemaps)
  [ ] Add welcome email sequence in Beehiiv
      (Settings → Automations → New subscriber)
  [ ] Confirm Beehiiv posts are set to publish as Web + Email

First issue will be written next Monday at 9AM.
Research collection starts today (next Tue/Thu/Sat pass).
```

## Resuming an Existing Newsletter (skip Phase 1 & 2)

If config already exists at `projects/<slug>/<slug>-config.json`:
Load it silently and proceed directly to whatever the user needs (update config, re-scaffold, add crons).
Do not re-run the full wizard.

**⚠️ Migration:** If you find an old config in `skills/newsletter-launch/.skill-config/`, copy it to `projects/<slug>/<slug>-config.json` and remove the old file to prevent conflicts.

## Reference Files
- `references/config-schema.md` — full config JSON schema and field notes
- `references/beehiiv-setup.md` — step-by-step Beehiiv account setup
