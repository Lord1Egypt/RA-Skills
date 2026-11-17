# LinkedIn Profile Refresh

Recruiters don't read LinkedIn — they search it. LinkedIn
Recruiter queries run on title tokens, exact skill tokens, and
location; your profile either matches the queries for the jobs
you want or it's invisible. Most profiles fail this test before
a human ever sees them: a title-only headline ("Senior
Manager"), an About section opening with "results-driven
professional," bullets that list duties instead of outcomes.

## The Problem

- Headline and skills index for search; almost nobody writes
  them as search bait. "Senior Manager" matches nothing.
- Every bullet without a number reads as padding to the
  6-second human skim that follows the search hit.
- Employed job seekers face a second problem: refreshing a
  profile WRONG announces the job search to their employer.
  The settings order matters and almost nobody knows it.
- What people want in a profile refresh is exactly what's hard
  to self-supply: an outside editor's audit and rewrites that
  preserve their real voice.

## What This Skill Does

- **audit** — scores headline structure, About hook (cliche
  detection, first-line number), and every experience bullet
  (duty-phrase detection + metric/scale marker check)
- **rewrite-headline** — builds a role + domain + keyword +
  scope headline from your inputs, with the pivot variant
  ("ex-Analytics Lead") for career changers; enforces the
  220-char budget
- **bullets** — converts duty phrases ("responsible for",
  "worked on") into outcome scaffolds you complete with real
  numbers — never invents metrics
- **stealth** — the ordered checklist that refreshes a profile
  without tipping off the current employer (which settings
  first, recruiter-only vs green banner, why edits spread over
  3-5 days)
- **scripts-list** — connection requests, recruiter replies,
  same-day follow-ups — fill-in templates with length caps

## Example

```
$ python3 scripts/profile_refresh.py audit --headline "Senior Manager" \
    --about-first "I am a results-driven professional with a passion..."
HEADLINE: too short (<40 chars) - loads no keywords
ABOUT HOOK: cliche opener - replace with what you do + a number

$ python3 scripts/profile_refresh.py rewrite-headline \
    --role "Product Manager" --domain "B2B SaaS" \
    --keywords "platform,API,strategy" --scope "team of 8, Series A-D"
HEADLINE (79/220 chars):
  Product Manager | B2B SaaS | platform, API, strategy | team of 8, Series A-D
```

## Who Needs This

Anyone whose next job will find them through LinkedIn — which
is most white-collar hiring now. Especially: quietly-looking
employed people (stealth sequence), career pivots (keyword
re-weighting), and the promoted-but-stale ("employed 3 years,
profile says 2019").

Runs 100% locally; no LinkedIn API, no data leaves the machine.

MIT License.
