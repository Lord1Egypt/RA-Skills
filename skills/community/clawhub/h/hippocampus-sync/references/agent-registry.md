# Agent Domain Registry
<!-- Each agent's track/exclude lists, framing questions, voice notes, source paths -->
<!-- hippocampus-sync reads this at Step 2 to detect the current agent's domain config -->

Each entry: ID, BU, target size, framing question, sections, track/exclude, voice, sources. Abbreviations: `ADV` = `~/.openclaw/areas/advisory/workspace`, `JDN` = `~/.openclaw/areas/jdn/workspace`, `MSR` = `~/.openclaw/areas/msr`, `OC` = `~/.openclaw`. All memory reads use 14-day window filtered by filename `YYYY-MM-DD*.md`.

---

### main (Ruka) — Portfolio — 5-8K

**Q:** "What is Sachee focused on across the portfolio? What needs his attention? What's the energy?"
**Sections:** BU Health Snapshot, Todoist Patterns
**Track:** All BU summaries, escalations, cross-BU coordination, Sachee's priorities, behavioral patterns (building-over-selling, deferral clustering)
**Exclude:** Deep domain details, day-to-day ops, specific drafts/prospects/tickets, named contact pipelines (→ Bobo), content queues (→ Malcolm/Ananda), e-commerce metrics (→ Ananda)
**Voice:** Sachee-centric emotional texture. Use his words. Name behavioral patterns. Top of Mind = emotional state + tensions, not KPIs. Test: replace every noun with a placeholder — does the file still communicate Sachee's state of mind?
**Peer compression rule:** GM HIPPOCAMPUS files give you BU state. Compress each to 1-2 sentences in BU Health Snapshot. Do NOT reproduce contact tables, deal stages, or pipeline detail — the GM's hippocampus already carries that.
**Sources:** `HIPPOCAMPUS.md` | `memory/` (14d, excl `todoist-activity/`) | `JOURNAL/2026-WXX.md` (2 wks) | `artifacts/portfolio-pulse/` (latest) | `artifacts/portfolio-review/` (latest, if <14d) | `memory/todoist-activity/` (14d) | GM HIPPOCAMPUS (read for BU state, compress to 1-2 lines per BU): `OC/areas/advisory/agents/bobo/workspace/HIPPOCAMPUS.md`, `OC/areas/msr/workspace/HIPPOCAMPUS.md`, `OC/areas/jdn/agents/ananda/workspace/HIPPOCAMPUS.md`, `OC/agents/cyclawps/workspace/HIPPOCAMPUS.md` | BU captures (curr wk): `ADV/artifacts/capture/`, `JDN/artifacts/capture/`, `MSR/workspace/artifacts/capture/`, `OC/agents/cyclawps/workspace/artifacts/capture/`, `OC/workspace/artifacts/capture/` | Cron logs: `OC/cron/runs/<id>.jsonl` (last 20 lines)

### cyclawps — OpenClaw — 3-5K

**Q:** "What's the platform state? What broke? What's in flight? What decisions does Sachee owe?"
**Lead:** Platform Health (HEALTHY/DEGRADED/CRITICAL)
**Sections:** Cron Health (14d), Roadmap Snapshot
**Track:** Platform health, agent status, cron success rates, skills ecosystem, config changes, infra issues, shipping velocity
**Exclude:** Advisory pipeline, JDN metrics, MSR analytics, business domain data
**Voice:** Diagnostic, consequence-driven. "If this stays below 80%, Sachee stops trusting cron output." Conditional triggers. Connect threads.
**Sources:** `HIPPOCAMPUS.md` | `memory/` (14d) | `artifacts/reports/health-check/` (14d) | `artifacts/reports/auto-update/` (14d) | `artifacts/capture/` (curr+prev wk) | `OC/cron/runs/<id>.jsonl` (8 jobs, last 20 lines) | `OC/docs/ROADMAP.md` | `OC/docs/CHANGELOG.md`

### bobo — Advisory — 4-5K

**Q:** "What are the portfolio patterns? Who needs attention? What commitments are owed? Is the practice healthy?"
**Lead:** Pipeline Health
**Sections:** Task Context, Relationships, CRM Health
**Track:** Portfolio patterns (deals, companies), pipeline mix, leverage across engagements, thesis fit, charter progress, practice health, town hall synthesis, deal pipeline (lead stage+), relationship warmth, SPICED state, commitments (both directions), CRM quality, interaction recency, follow-ups due
**Exclude:** Prospect queue, research backlog, outreach drafting, signal quality, content pipeline, content cron status, content signal scans, content seeds
**Voice:** Strategic altitude. Stakes language. Connect to thesis. Quote Sachee on strategic intent. Relationship-first layer: person before company. Warmth: hot/warm/cool/cold.
**Peer compression rule:** Do NOT maintain a "Peer Agent Activity" section. Renee and Malcolm have their own hippocampus files. If advisory peer state matters to a deal or commitment, reference it in ONE LINE within the relevant deal thread (e.g. "Renee: outreach paused during Sydney trip"). Never reproduce their pipeline counts, signal scans, or content queues.
**Sources:** `HIPPOCAMPUS.md` | `memory/` (14d) | `ADV/data/INDEX.md` | CRM hubs **SELECTIVELY** (Open Threads + active deals): `ADV/data/contacts/{slug}/_hub.md`, `ADV/data/companies/{slug}/_hub.md` | `ADV/CHARTER.md`, `ADV/REGISTER.md` | `ADV/artifacts/capture/` (curr wk) | Peer HIPPOCAMPUS (1-line context only): `ADV/agents/malcolm/workspace/HIPPOCAMPUS.md`, `ADV/agents/renee/workspace/HIPPOCAMPUS.md`

### renee — Advisory — 3-5K

**Q:** "What's the pipeline state? What's the research-to-outreach ratio? Where are the signals?"
**Sections:** Pipeline Status
**Track:** Prospect queue (SCAN results), research backlog, outreach sent/pending, responses, signal quality by vertical, source performance, research-to-outreach ratio, top of funnel, inbound leads
**Exclude:** Existing leads/deals, meetings, relationship warmth, SPICED, commitments, calendar, CRM quality, meeting counts, meeting prep/debrief, brain dump status, deal conversion tracking, travel schedules
**Voice:** Operational, signal-focused. Conversion ratios grounded in tracker files.
**Capture log filter:** When reading `ADV/artifacts/capture/`, include ONLY entries tagged `[prospect]`, `[research]`, `[outreach]`, `[signal]`. Ignore `[deals]`, `[meeting]`, `[strategy]`, `[content]`, `[marketing]`, `[ops]` entries.
**Sources:** `HIPPOCAMPUS.md` | `memory/` (14d) | `MEMORY.md` | `ADV/CHARTER.md`, `ADV/REGISTER.md` | `ADV/artifacts/prospect-pipeline-tracker.md` | `ADV/artifacts/outreach-connection-list.md` | `data/outreach/` (14d) | `ADV/artifacts/capture/` (curr wk, filtered — see above)

### malcolm — Advisory — 3-5K

**Q:** "What's the content pipeline? What's performing? What voice corrections have been made?"
**Sections:** Content Pipeline, Voice Consistency, Publication Status
**Track:** Content pipeline (published/drafts/seeds), publication cadence, pillar rotation, voice calibration, quality gates (Resonance, Sachee Test, Only-One), story library, engagement
**Exclude:** Prospect queue, lead/deal pipeline, meetings, SPICED, outreach, deal status changes, pipeline hygiene, inbound leads, disqualifications, relationship warmth, meeting prep/debrief, infrastructure changes (Telegram routing, skills refactor, model changes)
**Voice:** Editorial strategist. Name editorial tension. Sachee's edits = most valuable signal. Deal detail ONLY as content signal, never pipeline status.
**Capture log filter:** When reading `ADV/artifacts/capture/`, include ONLY entries tagged `[content]` or `[marketing]`. Ignore `[deals]`, `[pipeline]`, `[strategy]`, `[sales]`, `[meeting]`, `[network]`, `[operations]`, `[ops]` entries — those belong to Bobo, Renee, or Dealio Dan. If an entry is tagged `[malcolm]` but the content is a deal/meeting/pipeline event, it was mis-tagged — still exclude it.
**Sources:** `HIPPOCAMPUS.md` | `memory/` (14d) | `voice-rules.md` | `artifacts/content/source/story-seeds.md`, `artifacts/content/ideas/`, `artifacts/content/drafts/`, `artifacts/content/published/` | `ADV/artifacts/capture/` (curr wk, filtered — see above) | `ADV/CHARTER.md`

### ananda — JDN — 3-5K

**Q:** "What's the state of conversations with Dad? How are sales tracking? What marketing is in play?"
**Lead:** Business Health
**Sections:** Dad Intel, Team Output
**Track:** Dad conversations (Mr Jayantha), sales, marketing, content, engineering, ops, consultation, strategic direction, business development, seasonal timing
**Exclude:** Day-to-day fulfillment, platform infra
**Voice:** Business-centric with family warmth. Dad = ground truth (15+ years). Quote him. Seasonal awareness (wedding, festival calendars). Connect output to charter.
**Sources:** `HIPPOCAMPUS.md` | `memory/` (14d) | `data/dad-whatsapp.md` (scan `## YYYY-MM-DD` headers, 14d) | `artifacts/capture/` (curr+prev wk) | `CHARTER.md`, `REGISTER.md`

### billy — MSR — 3-5K

**Q:** "What's the website traffic? How are signups trending? Where's the funnel breaking?"
**Lead:** Platform State
**Sections:** Market Intelligence
**Track:** Traffic (weekly), signups (vendors/users), top 5 products by traffic, SEO impressions/clicks (GSC), funnel friction, user journeys
**Exclude:** Advisory pipeline, client delivery, platform infra, advisory content
**Voice:** Sharp, opinionated. State the recommendation. Name market timing. Don't hedge. Billy operates solo.
**Sources:** `HIPPOCAMPUS.md` | `memory/` (14d) | `artifacts/capture/` (curr+prev wk) | `CHARTER.md`, `REGISTER.md` | `OC/cron/runs/<id>.jsonl` (9 jobs, last 20 lines)

### bobina — Portfolio — 2-4K

**Q:** "What's the public narrative? Is brand consistency maintained? What's been published?"
**Sections:** News Pipeline, Signal Tracker, Learning Progress, Engagement Summary
**Track:** Public narrative, cross-BU public content, brand consistency, territory signal strength, engagement quality
**Exclude:** Advisory deals/prospects, JDN internal ops, MSR internal metrics, private business data
**Voice:** Field agent brief. Honest self-assessment. Territory drift. Downstream signal impact.
**CRITICAL: Sandboxed.** ALL paths RELATIVE to workspace root. No absolute paths, no `../`. Skip activity feed.
**Sources (relative only):** `HIPPOCAMPUS.md` | `memory/` (14d) | `content-drafts/news-scan-YYYY-MM-DD.md` (14d) | `learning-agenda.md`

### ink — The Markdown — 3-5K

**Q:** "What's the editorial pipeline? What content-worthy events have other agents produced? Publication schedule?"
**Lead:** Editorial Status
**Sections:** Content Pipeline, Source Material Freshness
**Track:** The Markdown (blog, newsletter), content strategy, ideation from monitoring Cyclawps/Fernando/docs/Journal, development, performance
**Exclude:** Advisory LinkedIn (Malcolm), JDN content (Ananda), MSR analytics (Billy), platform infra
**Voice:** Editor's board. Editorial consequence of delay. What unlocks movement. Cross-workspace sources as pipeline opportunities. Sachee's edits = calibration.
**Sources:** `HIPPOCAMPUS.md` | `memory/` (14d) | `OC/areas/the-markdown/workspace/drafts/brief-*.md`, `OC/areas/the-markdown/workspace/drafts/YYYY-MM-DD-*.md`, `OC/areas/the-markdown/workspace/ideas/*.md`, `OC/areas/the-markdown/workspace/published/*.md` | `CONTENT.md` | Journal: `OC/workspace/JOURNAL/2026-W*.md` (14d) | CHANGELOG: `OC/docs/CHANGELOG.md` (14d) | Cyclawps town hall: `OC/agents/cyclawps/workspace/artifacts/town-hall/` (latest) | `artifacts/capture/` (curr wk) | `OC/cron/runs/ink-*.jsonl` (4 jobs)

### fernando — LCC — 3-5K

**Q:** "What's the LCC roadmap status? What opportunities exist? What's blocking progress?"
**Lead:** Build Health
**Track:** Roadmap status, feature backlog, user feedback, opportunities, implementation, bugs, tech debt, git activity
**Exclude:** Advisory pipeline, JDN metrics, MSR analytics, business domain data
**Voice:** Build agent. What's built, blocked, next. Git log = first-class source. Link to files, don't duplicate.
**Sources:** `HIPPOCAMPUS.md` | `memory/` (14d) | `../../workspace/artifacts/capture/` (curr+prev wk) | `../../workspace/REGISTER.md` | `~/Vibecoding Projects/lovabo-central/docs/CHANGELOG.md` | `~/Vibecoding Projects/lovabo-central/docs/ROADMAP.md` | git log (14d): `cd "~/Vibecoding Projects/lovabo-central" && git log --oneline --since="14 days ago"` | git branches | `~/Vibecoding Projects/lovabo-central/CLAUDE.md`
