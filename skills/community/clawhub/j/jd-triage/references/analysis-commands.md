# Analyze & Plan

Both commands read accumulated history. Both refuse to run on too little data —
a trend drawn from four postings is a horoscope.

| Command | Needs | Below that |
|---|---|---|
| `/jd-triage analyze` | ≥ 8 entries in `jd_history.md` | Say how many exist and how many more are needed. Do not produce a partial report |
| `/jd-triage plan` | `skills` and at least one `target_roles` entry | Point at `/jd-triage update`. If history has ≥ 8 entries, use it to rank gaps; otherwise say the ranking is based on the role description alone |

**Report only what is in the data.** Empty category → "none yet". Never fill a
section by inference.

---

## `/jd-triage analyze`

Read every entry plus the criteria file.

```
📊 <N> roles evaluated, <first date> → <last date>

Where they came from
  <org trait>: <n>          ← grouped by the user's own org_traits vocabulary
  <org trait>: <n>
  unclassified: <n>

Titles that keep appearing
  <title pattern>: <n>

What they ask for
  <requirement>: <n>/<N> postings — you have it (mastered)
  <requirement>: <n>/<N> postings — you're learning it       ← highest ROI
  <requirement>: <n>/<N> postings — gap

Red lines
  "<pattern>": fired <n>× — <k> OUT, <m> CONDITIONAL

Your two dimensions
  Desirability: <n> Strong · <n> Good · <n> Weak · <n> Poor
  Candidacy:    <n> Likely · <n> Plausible · <n> Stretch
  Both high: <n>   ← the roles actually worth your time

Outcomes (of <n> entries with Outcome filled)
  <action tier>: applied <n>, interviewing <n>, rejected <n>, offer <n>

💡 <2-4 observations, each traceable to a number above>
```

### Rules

- **Group by the user's own vocabulary.** Bucket organizations using their
  `org_traits`, not a taxonomy of your own. Anything that fits none is
  `unclassified` — a large unclassified count is itself the finding, and means
  their trait list is missing something.
- **Requirement demand** is counted from stored requirement text across entries,
  cross-referenced with `skills`. Rank by `frequency × (1 − credit)`: something
  asked for constantly that the user is halfway through learning outranks
  something rarer they have not started.
- **Red-line review.** If a red line has fired ≥ 3 times and *never* produced an
  OUT — only CONDITIONAL — say so and offer to demote it to a negative vibe
  anchor. It is behaving like a preference, not a gate.
  If a red line has never fired at all across ≥ 15 entries, mention it once;
  it may be aimed at postings the user is not even seeing.
- **Calibration, only with outcomes.** If ≥ 5 entries have an `Outcome`, compare
  predicted Candidacy against what happened. Report it flatly:
  *"Of 6 rated Stretch, 3 got a first interview — the Candidacy read may be
  running pessimistic."* Fewer than 5 → skip the section entirely, do not hedge
  a guess.
- **Never infer market conditions.** The sample is the user's inbox, not the job
  market. Say "the roles reaching you", never "the market is".

---

## `/jd-triage plan`

Per target role:

```
🎯 <role name>
   Based on <n> matching postings in your history

Requirements this role asks for
   ✅ <requirement>            you have it — <n>/<N> postings asked
   ⚠️ <requirement>            learning — <n>/<N> asked
   ❌ <requirement>            gap — <n>/<N> asked

Next, in order
   1. <item> — asked in <n>/<N> postings, you're already partway
   2. <item> — asked in <n>/<N>, not started
   3. <item> — rarer, but blocks the roles you rated highest

Evidence to build
   <item>: <one concrete artifact that would let you claim it in an interview>
```

### Ranking

Order by demand × proximity: frequency in matching postings, weighted up for
items already in `skills.learning` (finishing beats starting), weighted down for
items appearing only in `preferred` sections.

Say plainly when an item is low-frequency but appears in the highest-desirability
postings — that is a different kind of bet and the user should make it knowingly.

### Evidence suggestions

One per gap, concrete and checkable — something that produces an artifact a
recruiter or interviewer can look at. A shipped thing, a written thing, a
measured thing. Never suggest a course as the artifact; a certificate is not
evidence of the skill.

### What this command does not do

- **No timelines.** Do not estimate months to close a gap. You do not know the
  user's available hours, and a fabricated schedule is worse than none. If they
  ask, ask how much time per week they actually have and reason from that.
- **No aptitude judgments.** Rank by market demand and proximity, never by
  whether the user seems capable of something.
- **No scope creep into career advice.** This command closes named gaps against
  named roles. Whether the target role is the right target is a different
  conversation, and it belongs to the user.
