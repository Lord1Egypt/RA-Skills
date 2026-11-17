# jd-triage

**Two questions, kept apart: do you want it, and can you get it?**

Paste a job posting. Get a verdict against the criteria *you* defined — plus an
honest read on whether you'd clear the bar. Most JD filters collapse both into
one score, which is exactly the information you needed.

A skill for [OpenClaw](https://github.com/openclaw). Works in any market, any
language, any profession.

---

## What it does

- **Scores two independent dimensions.** Desirability from five weighted axes
  against your stored criteria; Candidacy from the posting's stated must-haves
  against your skills. A role you want but can't get is a **stretch**, not a
  skip. A role you can get but don't want is a **backup**, not an apply.
- **Weights red lines by where they appear.** "Owns revenue targets" in the title
  is an instant no. The same phrase in the last bullet, framed as *support*, is a
  question to ask the recruiter — not a rejection.
- **Makes vibe judgments inspectable.** Every vibe rating quotes the posting and
  names the anchor it reasoned from. Anchors carry your *reason*, so the skill
  works on a 12-person studio nobody has heard of, not just famous logos.
- **Turns unknowns into questions.** Missing comp, ambiguous scope, unclear
  remote policy — each becomes a line you can paste into a reply to the recruiter.
- **Logs everything, including rejections.** Over time, `analyze` shows which
  patterns keep reaching you and which requirement you keep almost meeting.

## Starting up

Five questions. Not thirteen.

Quick Start asks for your role family and market, what titles you want, your
floors (comp with basis, locations, remote), your automatic no's, and one to
three organizations you admire *with a line on why each*. That is enough to
evaluate. Everything else is asked once, at the moment it first matters.

Prefer showing over telling? `/jd-triage learn` reads a handful of postings you
liked and a handful you passed on, then proposes your red lines and anchors for
you to accept or edit.

## Commands

| Command | What it does |
|---|---|
| Paste a posting, or `/jd-triage` | Evaluate |
| `/jd-triage quickstart` | The 5-question setup |
| `/jd-triage learn` | Derive criteria from example postings |
| `/jd-triage update` \| `reset` | Edit criteria, current values pre-filled |
| `/jd-triage history [apply\|out]` | Last 10 evaluations |
| `/jd-triage compare <id1> [<id2>]` | Side by side |
| `/jd-triage analyze` | Patterns across everything you've evaluated (needs 8+) |
| `/jd-triage plan` | Which gap to close next, ranked by what postings actually ask for |

Natural language works too, in your language: "should I apply to this",
"和上次对比", "what should I learn next".

## Sample output

```
🎯 STRETCH APPLY        Desirability: Strong   Candidacy: Stretch

Want it
  Role fit     ★★★★★
  Domain       ★★★★★
  Org          ★★★★☆
  Vibe         ★★★★☆   anchor "Basecamp" — why: "small team, no growth theater"
                       triggered by: "we ship deliberately", "no on-call"
  Comp         — (info insufficient)
  → weighted 4.6/5 across 4 axes

Can get it
  Meets 2/5 stated must-haves
  ✅ SQL   ✅ experiment design
  ⚠️ Kubernetes (learning — half credit)
  ❌ 5 years managing a team   ❌ regulated-industry experience

Strong on everything you control; the management requirement is the one real
blocker, and it's the kind they usually probe rather than verify.

Open questions
- Is the team-management requirement firm, or would mentoring experience clear it?
- What's the full package, and is the posted number base or all-in?

Logged: JD-20260725-001
```

## Files it writes

- `~/.openclaw/workspace/jd_criteria.md` — your criteria
- `~/.openclaw/workspace/jd_history.md` — append-only evaluation log

Plain markdown, hand-editable. The skill parses your edits and asks about
anything malformed instead of overwriting it.

## Privacy

History stores verdicts, scores, and a one-line summary — **not the raw posting**.
Set `history_detail: full` to keep raw text; you'll be warned once. Recruiter
contact details and unposted comp live in those postings, so don't turn it on for
a workspace you sync publicly.

## Limitations

- **It does not read your resume.** Candidacy is scored from the skills inventory
  you provide, against what the posting actually states. It will not tell you how
  you compare to other applicants.
- **It does not map seniority across markets.** L5, P7, and Grade 6 are not
  comparable, so it counts stated requirements and ignores the level label.
- **Vibe is only as good as your anchors' reasons.** The `why` is what it reasons
  from. One-word anchors produce weak ratings — that is the design working, not
  failing.
- **The sample is your inbox.** `analyze` describes the roles reaching you, never
  "the market".
- **No comp negotiation advice.** Out of scope.
- **Model support is measured, not assumed.** Verified on GLM-5.2 and Claude
  Sonnet 4.6 — 18 test cases, 100% verdict stability across repeated runs and
  100% compliance with the skill's own rules. Smaller models are simply untested;
  no claim either way.

## Author

Barry Wang ([@bwancoding](https://github.com/bwancoding)) —
[github.com/bwancoding/jd-triage](https://github.com/bwancoding/jd-triage)

MIT licensed.
