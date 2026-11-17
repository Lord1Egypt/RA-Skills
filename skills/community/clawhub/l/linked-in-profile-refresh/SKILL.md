---
name: linkedin-profile-refresh
description: Use when job hunting, quietly re-entering the market, or after a role change — audits each LinkedIn profile section (headline, About, Experience bullets, Skills) against recruiter-search mechanics, rewrites headlines from title-only to keyword-loaded search bait, converts duty-listing bullets into outcome bullets with metrics, sequences SAFE refresh steps that don't trigger "looking for work" signals to your current employer, and drafts connection-request and recruiter-reply scripts.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [career, linkedin, job-search, resume, recruiting, headline, personal-branding]
---

# LinkedIn Profile Refresh

Recruiters don't read LinkedIn profiles — they SEARCH them.
LinkedIn Recruiter filters on title keywords, skills, and years;
your profile either matches the queries run for the jobs you
want or it doesn't exist. Meanwhile the profile most people
have is a resume graveyard: title-only headline ("Senior
Manager"), About section written in third person in 2019, and
bullets that list duties instead of outcomes.

This skill is a section-by-section rebuild with the mechanics
in mind:

1. **Audit** — score each section against what recruiter search
   and the 6-second human skim actually reward
2. **Rewrite** — headline formula (role + scope + domain
   keywords), About structure (hook line, proof paragraph,
   skills paragraph, CTA), bullet converter (duty → outcome +
   metric + tool)
3. **Stealth sequencing** — refresh WITHOUT broadcasting "job
   seeker" to your current employer (settings order matters;
   the wrong toggle pair announces you)
4. **Scripts** — connection requests that don't get ignored,
   recruiter-response templates, follow-up cadence

## When to Use

- Actively job hunting (refresh BEFORE applying — recruiters
  cross-check every application against the profile)
- Quietly open to opportunities while employed (the stealth
  sequence is the whole point)
- After a promotion/role change (the "employed but stale"
  profile costs interviews silently)
- Career pivot (re-weighting keywords toward the TARGET role so
  you appear in ITS searches, not your old one's)
- Returning from a gap (About section framing + experience
  sequencing)
- Layoff (public story line, #OpenToWork settings decision —
  with the employer-visibility tradeoff spelled out)

Don't use for: resume writing (different format, different
truncation rules — though the bullet converter helps both), or
content-creator LinkedIn strategy (posting cadence is a
different skill; this is profile-as-search-target).

## The Mechanics (why each section matters)

- **Headline** (220 chars): indexes for recruiter title search.
  "Senior Manager" matches nothing useful; "Senior Product
  Manager | B2B SaaS | Platform & API Strategy | Team of 8 |
  Series A-D" matches "product manager" + "SaaS" + "platform."
  Current title keywords first, then domain, then scope proof.
- **About** (2,600 chars): first 3 lines show before "see
  more" — the hook lives there. Keywords index here too.
  Structure: hook (what you do + for whom + the number), proof
  (2-3 outcome sentences), skills paragraph (natural-language
  keyword load), CTA (what you want next).
- **Experience bullets**: outcome > activity. Formula:
  `[Action verb] + [what] + [metric: %, $, time, scale] +
  [tool/method]`. Convert "Responsible for reporting" →
  "Built automated weekly reporting (SQL + Looker) cutting
  prep time 6 h/week for a 12-person team."
- **Skills** (top 50): order matters — top 3 pin to your
  headline keywords. Recruiter filters run on exact skill
  tokens; if "SQL" is buried at #47, the filter never sees it.
- **Custom URL + photo + banner**: hygiene, 5 minutes, affects
  profile credibility scores recruiters admit to using.

## The Stealth Refresh Sequence

If employed, do IN THIS ORDER:

1. Toggle "Open to work" ON with **"Recruiters only"** — never
   the green banner if stealth matters (LinkedIn shares
   recruiter-only signals with recruiters using LinkedIn
   Recruiter — which can include YOUR company's recruiters;
   accept that residual risk or skip)
2. Turn OFF "Notify network about profile changes" (Settings →
   Visibility) BEFORE editing anything
3. Make edits spread over 3-5 days, not one hour (activity
   bursts surface in feeds even with notifications off)
4. Do NOT follow a burst of company pages / like job posts —
   the algorithmic tell is real
5. Update photo/banner quietly — network still sees profile
   visits to your refreshed page, which is fine

## Bullet Converter (duty → outcome)

Run your current bullets through `scripts/profile_refresh.py
bullets` — it detects duty-language patterns ("responsible
for", "worked on", "helped with", "managed the") and emits a
rewrite scaffold: [verb] [what] [SCALE?] [TOOL?] [RESULT?].
You fill the bracketed metrics — the script can't invent your
numbers, and invented numbers torpedo interviews.

## Pitfalls

1. **The #OpenToWork green ring while employed.** Visible to
   EVERYONE including colleagues. Recruiter-only mode exists
   precisely for this; the banner is for unemployed search.
2. **Keyword stuffing.** Algorithms rank, humans skim. A
   headline that's 15 comma-separated terms reads as spam to
   the 6-second human pass. 5-7 load-bearing terms max.
3. **Third-person About.** "Jane is a results-driven..." —
   nobody writes about themselves that way; write first
   person, drop "results-driven" (show the result instead).
4. **Bullets with no numbers.** Every bullet needs at least
   ONE of: %, $, count, time-saved, team-size. No data? Use
   scale ("across 4 markets", "for 40+ clients").
5. **Old title keywords when pivoting.** Your last title
   indexes hardest. If pivoting, headline = target role
   (truthfully framed: "Product Manager (transitioning from
   Data Analytics)").
6. **Endorsement theatre.** Collecting 99 endorsements for
   skill #40 does nothing; 3-5 endorsements on your TOP skills
   from colleagues who saw the work is what reads as signal.
7. **One-and-done.** Re-audit quarterly; skills tokens and
   recruiter search terms drift.

## Verification Checklist

- [ ] Headline: role keywords + domain + scope, ≤220 chars
- [ ] About: hook in first 3 lines, proof with numbers,
      keyword paragraph, CTA
- [ ] Every experience bullet has a metric or scale marker
- [ ] Skills reordered: top 3 = headline keywords
- [ ] Stealth sequence executed in ORDER (settings before
      edits, recruiter-only, spread over days)
- [ ] Custom URL set, recent photo, non-default banner

## Quick Recipe

```
python3 scripts/profile_refresh.py audit --headline "Senior Manager" \
    --about-first "I am a results-driven professional..." \
    --bullets-file bullets.txt
python3 scripts/profile_refresh.py rewrite-headline \
    --role "Product Manager" --domain "B2B SaaS" \
    --keywords "platform,API,strategy" --scope "team of 8"
python3 scripts/profile_refresh.py bullets --file bullets.txt
python3 scripts/profile_refresh.py scripts-list
```
