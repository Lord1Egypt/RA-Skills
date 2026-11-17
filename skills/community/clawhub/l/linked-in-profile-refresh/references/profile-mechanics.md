# LinkedIn Profile Refresh — Deep Reference

## How recruiter search actually sees you

LinkedIn Recruiter / Sales Navigator queries are built from:
- **Title tokens** (current + past titles, weighted to recent)
- **Skills tokens** (exact-match favored)
- **Location + years of experience filters**
- Boolean strings ("product manager" AND (API OR platform))

Consequences:
1. Your HEADLINE overrides your title in search indexing — a
   headline of "Enabling synergies" makes a PM invisible to the
   "product manager" query even with the right job title.
2. Skills are tokens, not prose: "SQL" matches; "database
   wizardry" doesn't. Load exact tokens in Skills, weave
   natural-language variants in About.
3. Past titles still index — pivots must put the TARGET role in
   headline and About, not hope the old title maps.

## Headline formulas by situation

- **Staying in track**: `Role | Domain | 2-3 keyword strengths
  | scope proof` — "Senior Data Analyst | Fintech | SQL,
  dbt, Experimentation | 8-person team, 40M-row warehouse"
- **Pivot**: `Target Role | bridge proof | domain` — "Product
  Manager | ex-Analytics Lead, 3 yrs shipping data products |
  B2B SaaS"
- **Senior/lead**: scope numbers carry the level — "Engineering
  Manager | Payments | 14 engineers, 3 teams | scaling 2M→9M
  MAU"
- **Job seeker (public)**: append "| Open to [role] roles" —
   only when unemployed/fully public search

Char budget: 220. Count them; LinkedIn truncates silently.

## About section skeleton (fill and reorder)

1. **Hook (lines 1-3, visible pre-"see more")**: what you do +
   for whom + one number. "I build onboarding flows that
   convert. Last 12 months: activation 31%→48% at a 40-person
   B2B SaaS."
2. **Proof paragraph**: 2-3 outcomes, one sentence each, each
   with a number.
3. **How I work** (optional, 2 lines): method names that double
   as keywords (A/B testing, JTBD, RFC-driven planning).
4. **Skills paragraph**: natural sentence with your top 8-10
   tokens ("Deep in SQL, dbt, Airflow, and dashboard design in
   Looker and Tableau...").
5. **CTA**: one line. "Open to senior analytics roles in
   fintech" or "Best reached at [email]" (only if public
   search).

## Bullet converter rules

Duty phrase → outcome scaffold:
- "Responsible for X" → "[Verb] X [scale] with [tool],
  [result]"
- "Worked on / helped with" → ownership verb (Led, Built,
  Shipped, Cut, Grew, Automated, Owned)
- "Managed team doing X" → "Grew team 5→9; shipped X across 3
  quarters"
No number available? Use scale words: multi-market, company-
wide, 40+ clients, daily batch, 99.9% uptime. Never invent
percentages — interviewers probe every number and one invented
metric poisons the honest ones.

## Skills section mechanics

- Up to 100 listed; top 3 pinned under your headline — pin the
  EXACT tokens of your target role's job postings (copy from
  5 postings, count frequency, pin the top 3)
- Take the LinkedIn skill quizzes only for top-3 skills (badge
  shows on those; diminishing returns below)
- Endorsements: 3-5 per top skill from people who saw the work
  beats 50 from well-wishers

## The stealth sequence, why each step

1. **Settings BEFORE edits**: "Share profile changes" network
   broadcasts are batched by LinkedIn activity; turning the
   toggle off after a headline change still leaks the first
   edit. Order is not cosmetic.
2. **Recruiter-only Open-to-Work**: your company's recruiters
   CAN still see the flag if they use LinkedIn Recruiter
   (roughly: large-company recruiters do; small companies
   often don't). Residual risk is real; if zero risk is
   required, leave it off and let the refreshed profile do the
   inbound work.
3. **Edit spreading**: 3-5 days. The feed surfaces "X has a
   new position" style updates from clusters of changes even
   with notifications off (profile-view spikes are normal and
   fine).
4. **No job-post liking / company following bursts** during
   stealth mode — the recommendation engine tells more than
   the profile does.

## Scripts (message templates)

**Connection request (300-char limit):** reference one shared
thing + one line of value, no pitch: "Hi [name] — saw your
talk on [topic] (the [specific bit] framing stuck with me).
Would be good to connect here."

**Recruiter reply (interested):** "Hi [name], thanks for
reaching out. [Role] sounds relevant — I'm [1-line fit]. Could
you share the salary band and team size? Happy to set up a
call this week."

**Recruiter reply (not looking, politely open):** "Flattered —
not exploring moves right now, but [role type] is squarely in
my lane for the future; keep me posted on senior versions."

**Follow-up after call, same day:** 3 sentences — thanks,
the one thing that interested you, the asked-for item
attached.

## Quarterly maintenance (10 min)

- Re-pin top-3 skills against 5 fresh target-role postings
- Refresh one About proof line with the newest number
- Prune endorsements on dead skills; add tokens for new tools
- Re-check stealth toggles after any LinkedIn settings
  redesign (they reset more often than anyone admits)
