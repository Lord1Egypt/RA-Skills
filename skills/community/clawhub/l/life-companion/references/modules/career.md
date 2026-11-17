# Module: Career fit & job-match (工作匹配)

Help the person see what kind of work fits them, how well their current or an
aspiration job matches, and concrete next steps — grounded in real vocational
frameworks, scored honestly with **coarse bands, never fabricated precision**.

**v1 status — shipped.** The scoring engine is live:
`scripts/career_match.py` scores the person against the shipped O\*NET occupation
data (`data/career/occupations.json`, **188 real occupations, CC BY 4.0**) using the
interest-check items in `data/career/assessment_items.json`. **All 188 carry numeric
O\*NET Occupational-Interest ratings** (1–7, O\*NET 31.0 Database) and **173 also carry
Work Values** (ipsative rank, O\*NET 30.2, the last release to publish them), so the
values blend is a live, data-backed component, not a hypothetical. The set is densely
weighted toward the user's data-science / ML / research / computing / medical-imaging
field, then spread across all six RIASEC areas; common jobs such as preschool teachers,
patrol officers and couriers are not in it. See the **Data reality** note below before
you describe a result.

## Computed vs interpretive (the skill's one rule, applied here)
- **Computed (facts).** The RIASEC-6 vector from the person's answers, the
  interest correlation, the band, the confidence note — all from
  `career_match.py`. Deterministic, offline. **Never hand-score it.**
- **Interpretive (a lens).** What a "Strong on Investigative, softer on your #1
  value" result *means* for them. Always "one way to read this", never a verdict.

## What this module is (and isn't)
- It runs a **transparent, self-built interest check** (Holland/RIASEC), plus an
  **optional** light Big Five read and an **optional** work-values ranking.
- It scores the person's profile against the shipped O\*NET occupation data using
  `career_match.py`, and reports **Low / Moderate / Strong** bands with a
  **confidence note** — no "87% match", no invented salary/demand/percentile.
- Say clearly: the interest check is **grounded in RIASEC (a real framework) but
  is not the O\*NET Interest Profiler or any validated instrument**. Moderately
  informative about interest & satisfaction fit; **does not predict hiring**;
  **not a label**. Show the disclaimer once (disclaimers.md, "Career fit").

## Assessment flow (interests first)
**Preferred: the HTML form.** Run `scripts/form_server.py --form career` (see
`references/forms.md`) — the 21 Likert items + the 6-value ranking are far nicer in a
form than in chat. On submit it writes `career_intake` (`companion.py cache --module
career_intake` → `latest.answers` 0–4 per id + `latest.values_rank` + jobs); score it
with `career_match.py --score-intake`. Fall back to the chat flow below only if the user can't use
a browser — an equally valid path, not a downgrade. When using chat, always give
**selectable options** (`AskUserQuestion` where the harness has it, otherwise a
numbered list they answer with numbers) — never free text for a choice.

1. **Interest check first (RIASEC-6).** Present the 21 activity-liking items
   (source: `data/career/assessment_items.json`). Each item is one
   one options question with the 5-point liking scale: Strongly dislike / Dislike /
   Neutral / Like / Strongly like (stored 0–4). You may batch items and lean on
   the journal/profile to pre-fill or skip obvious ones, but keep it honest about
   what was inferred.
   - Frame (verbatim intent): "This is a quick interest check, not an official
     test — built on the real Holland/RIASEC model, but not a validated
     instrument. Answer for what you'd *enjoy*."
   - Short on time? A 12-item subset (2 per type) is a valid run — the confidence
     note will shrink accordingly, and you must say so.
2. **Traits & values only on request** (or when they want a sharper read).
   - Big Five: five pole-description sliders (light read, not a personality test,
     no label, no percentile).
   - Work Values: force-ranked ordering of the six O\*NET values (ipsative).
   - Both optional; interests-only is a complete, valid run.

Score the collected profile with `career_match.py --answers '<json>' [--values …]`
(the form path uses `--score-intake`). Report the **band + the
confidence note together**, and name which components were used and the
**disclosed weights** applied (Interests 0.45 / Values 0.30 / Traits 0.25 when
all present, renormalized over whatever is present).

## Two modes

### Mode A — Current-job congruence coaching
Map the person's RIASEC top types (and, if collected, values/traits) against the
current role's occupation vector from the shipped data.
- Report where the role **fits** (congruent types/values) and where the
  **friction** is — decomposed, e.g. "strong on the Investigative pull the role
  feeds, softer on the Independence you ranked #1".
- This is **congruence coaching, not a verdict.** Offer concrete adjustments
  (craft the role toward the strong types, protect the top value), not
  "quit/stay".

### Mode B — Aspiration-job fit + honest gap sketch

**First, map their words to an actual occupation — don't eyeball it.** They say
「产品经理」/「MRI 重建算法」/"something in UX"; the engine scores against a SOC code.
Guessing that mapping is a wrong answer that looks right, because every downstream
number is then about a job they didn't mean.
```bash
python3 "$D/scripts/career_match.py" --find "产品经理"        # ranked candidates + data quality
```
Show the top candidates, **confirm with them** («你说的X，我按 O*NET 的「<title>」来算，
行吗?»), and note whether the chosen one carries numeric interests or is code-only —
that sets the confidence you may claim. If it returns **no match**, no shipped title
shares a word with what they said. That is not proof the role is missing from the
188-occupation dataset: ask what the work is day to day and try `--find` with those words,
ask which shipped occupation is closest in *day-to-day work* (not job title), or give an
interests-only read with **no** occupation congruence at all. Never substitute the
nearest-looking title.

Every candidate carries `match`. **`strong`** means the title is the job they named: an
exact title, or one that explains *everything* they said, whose own role is among the
matched words, and that two separate parts of what they said fit (or that they named whole).
「牙医助理」 leaves 助理 unexplained against Dentists, so that hit is weak; First-Line
Supervisors of Police and Detectives are supervisors, so "police detective" is weak there
too. **`weak`** means less than that: one shared word (「司机」 shares only "drivers" with
Heavy and Tractor-Trailer Truck Drivers), a word the title doesn't explain, or an alias that
points at neighbours because O\*NET has no such occupation (产品经理, 运营, 研究员). A title
never matches on the group its "Except" clause leaves out, and a title whose matched words
another strong title covers and more is weak too (for 「中学老师」, Elementary School
Teachers). When more than one title is strong they are all marked `tied`: ask which one is
their work, and `matched_on` shows which of the title's words matched. Present a weak
candidate as a neighbour, never as their job, and when every
candidate is weak say that none of them is the job they named. Traditional script,
full-width letters and spaces are folded first, so 軟體工程師 and ＵＩ设计师 find the same
titles as their plain forms.

**No scored check yet? Then there is no fit to report.** Answer what can be known without
one: what `--find` matched and whether it is the job itself, what the role involves day to
day, and which parts of their background carry over, as questions to test rather than a
verdict. Don't open with 适合/不适合 or call it 很对口: a fit is what `career_match.py`
measures, and the gate blocks a fit verdict in a career reply that carries no band. Offer the
interest check as options (the form, the 21 items in chat, or not now), and score it before
saying where they fit.

Then, two separate outputs, never merged into one number:
1. **Fit** — congruence band of the person against the aspiration occupation
   vector (same engine), with confidence note.
2. **Gap sketch** — an *honest, qualitative* list of what typically stands
   between them and that role (skills, credentials, experience). The occupation's
   **Job Zone** (in the data) is a useful anchor for typical prep/education, used
   qualitatively — never as a readiness percentage. Framed as "worth pursuing,
   here's a plausible path" or "here's what would need to be true" — never a
   rejection, never a fabricated readiness number.

## Scoring engine (`scripts/career_match.py`)
Person RIASEC-6 vector vs each occupation's RIASEC vector via a **centered
correlation**: the interest fit is `(r + 1) / 2`, with `r` the Pearson correlation of the
two six-score profiles. Occupations given only a 3-letter high-point code (`riasec: null`)
are expanded **3-2-1** and flagged **lower-confidence**; occupations with full
six-value ratings use `(x-1)/6`. Optional **values** (ipsative cosine, **rescaled** — see below) and
**traits** (soft mean-abs-difference over mapped traits only) blend in with the
disclosed default weights, **renormalized** when components are absent.

The interest fit used to be the plain cosine of the two vectors. Every score is
non-negative, so any two profiles already point roughly the same way: answering all 21
items at random put a median of about 70% of the 188 occupations in Strong, and a person
with one clear favourite who answered the other types 3 instead of 0 saw other types enter
their top five (for a Realistic favourite, Strong grew from 15 occupations to 163).
Centering each profile compares shape, not level: the same random answers put about 11% in
Strong, and a clear favourite reads the same at any level. On the interest fit the bands
mean `r ≥ 0.5` for Strong and `r ≥ 0.1` for Moderate; a flat profile has no shape and is
not scorable.

The values cosine needed rescaling because an ipsative rank vector cannot point near
the origin: over all 720 orderings its minimum is **0.615**, not 0. Fed straight into
bands built for a [0,1] metric, an **exactly reversed** value ranking still read
"Moderate" — the component could not report a mismatch at all. It is now stretched onto
[0,1] against that verified floor, so opposite rankings read Low. An exhaustive test
pins the floor, so changing the vector definition can't silently skew every score. Values an
occupation rates equally share the average rank (two tied for second are both 2.5): 141 of
the 173 rated occupations have a tie, and breaking it by value name, as the file once did,
let the alphabet move occupations between bands. Output is
a **band** (thresholds 0.55 / 0.75, disclosed as tunable) plus a **confidence
note** that shrinks on short/partial assessments and on code-only occupations.
Raw floats stay internal; the person-facing layer emits **bands + language only**.

**The result comes back as two lists, and they are not comparable.** Use
`score_person_grouped()`, which returns `numeric_interests` and `code_only`, ranked and
banded separately. Since the O\*NET 31.0 rebuild all 188 occupations are in
`numeric_interests` and `code_only` is empty. It stays because the two kinds score on
differently-shaped distributions: when 120 occupations were code-only, one person's
numeric set came out 63% "Strong" and the code-only set 20%. **If a code-only occupation
ever appears, never merge the lists into one table, and never say a code-only
occupation fits better than a numeric one.**

**An answer set with no shape is refused, not scored.** Under the old cosine, answering
the same value to all 21 items produced the vector [k,k,k,k,k,k] — identical in direction
for every k — and still yielded a full ranking, always topped by whichever occupation sits
nearest the uniform direction. A correlation reads only shape, so a flat set has none, and
type scores that barely differ would stretch noise into a full-strength shape.
`score_person_grouped` now returns
`{"refused": true, …}` when the six type scores barely differ, and the same way when a
type has fewer than two answers: assessment_items.json's short form is two items per type,
and a skipped item is no information, not dislike. Say what it says: this is
**"can't measure"**, not "low match". Offer to redo the check, or drop the instrument
and talk about what they've actually done and when they were most absorbed.

**Data reality (be honest about which read you gave):** say which kind of match the
person actually got:
- **Interest ratings (all 188).** O\*NET's 1–7 interest ratings → a genuine shape match,
  `moderate`+ confidence even before values. O\*NET marks them as model estimates
  (Machine Learning/Expert), so present them as O\*NET's estimates, not survey results.
- **Work Values (173 of the 188).** If the person supplied a Work-Values ranking, the
  **values blend engages** (Interests 0.60 / Values 0.40) and lifts confidence to
  `higher`. Naming it is honest — *"this one's scored on both your interests and your
  values"*. The **15 without a Work-Values rating stay interest-only**
  (`work_values:null`, never fabricated) — say so if one lands high; don't imply its
  values were checked.
- **Code-only occupations (none today).** `career_match.py` still accepts an occupation
  with only a 3-letter high-point code, expands it 3-2-1, and scores it in `code_only` at
  **lower confidence, interests only**. Call such a result an interest-fit sketch.

Never describe a result as values-weighted when the occupation carried no
`work_values`; the payload's `components_used` / `weights_applied` tell you exactly
which components fired — read them, don't assume. **A values ranking only engages if it
ranks all six values 1 to 6, each once.** An incomplete or repeated one (a value left
blank, two values both ranked 1) degrades to interests-only rather than erroring, and the
payload's `values_note` says why; the career form says so on its own page too.

**Localization — O\*NET is US labour-market data.** The RIASEC interest-fit itself is
not country-specific and transfers fine (a person's Investigative pull is the same in
Berlin as in Ohio). What does **not** transfer: occupation *titles*, licensing, typical
pay, demand, and whether a role even exists the same way in the person's country. So:
score and interpret **fit** anywhere, but the moment the talk turns to **market,
availability, pay, or credentials in a specific country**, that's a rule-6 fact — verify
it live for *that* country (see the deep-analysis section), don't read it off US data.
When `locale` is `zh`, keep the O\*NET title in English and add a short Chinese gloss;
don't invent a localized occupation name.

```bash
python3 "$D/scripts/career_match.py" --score-intake                  # score what the career form saved
python3 "$D/scripts/career_match.py" --answers '{"1":3,"2":1,…,"21":0}' \
    --values "Independence,Achievement,Working Conditions,Recognition,Support,Relationships"
                                                                    # answers collected in chat
python3 "$D/scripts/career_match.py" --score-intake --soc 15-2041.00  # one occupation, code from --find
python3 "$D/scripts/career_match.py" --selftest   # verify the math
```
**Always score through this command.** It runs `score_person_grouped`, so an answer set
with no shape comes back refused (exit 3; say "can't measure", not "low match") and the
two occupation groups arrive separately. There used to be no command, and the line here
said to import `score_person`, which skips both guards: a model following it reported
"Strong" matches for someone who had answered "neutral" to all 21 items. Exit 2 means
the input is missing or malformed, and the payload says which.

## Honesty guardrails
- Bands and qualitative language only — never a precise percentage, salary,
  demand, or percentile.
- Decompose, don't collapse: "strong interest, softer on values" beats one score.
- Always pair a band with its confidence note; say what you don't know.
- The interest check is RIASEC-grounded but **not** the O\*NET Interest Profiler
  or a validated test; never present it as one.
- Not a hiring predictor, not a personality label, not destiny.
- Occupation data ships with its **CC BY 4.0 O\*NET attribution**
  (`data/career/occupations.json`); keep it intact.
- **Machine backstop:** `python3 "$D/scripts/selfcheck.py" --module career --file draft.md` — exit 1 means a blocker; fix it before sending. Passing is not proof it's honest, only that it's free of the known bad shapes.

## Deep employment / relocation analysis — applying safety.md §1 rule 6

This is the highest-stakes place this module hits **safety.md §1 rule 6 (verify, don't
assume on high-stakes checkable facts)**: a plausible-but-wrong answer on a visa, a
tax ruling, or an employer's hiring status does real harm. When the person asks
about working / relocating to a specific country ("can I stay / work in X", a visa,
job prospects there), a fit reading is **not** enough — the answer turns on
**policy eligibility** and **current market reality**, both changeable, neither
assumable. Run §1 rule 6's research + verify pass (a workflow if available). Its rules,
applied to this domain:

1. **Enumerate EVERY pathway — from the destination authority's own route list,
   not memory.** The best option is often not the first work permit; someone with
   years already in-country may be near PR, which removes sponsor dependency
   entirely. *NL examples (illustrative only — verify for the actual country):*
   each work-permit route, the job-search/orientation-year route, permanent/
   long-term residence, naturalization, EU routes, family routes. Other systems
   have their own primitives — student→work conversion, self-employed/startup/
   entrepreneur visas, points-based/express or regional-nominee programs,
   intra-company transfer, shortage-occupation or global-talent routes. Missing a
   pathway is a real failure.

2. **Test each policy's eligibility conditions against THIS person — don't default
   the answer.** State the conditions, then check each against what you actually
   know; **ask the deciding fact rather than guessing** (§1 rule 6b). *Worked example
   that must never be gotten wrong:* the Dutch **30% ruling requires being recruited
   FROM ABROAD** (a residence/distance test), so a graduate who **studied in-country
   generally does NOT qualify** — even the PhD exception is tested at the moment
   they first came for the PhD. The pivot fact is "were you recruited from outside
   NL, or already resident here?" — elicit it; never collapse to a guess in either
   direction.

3. **Pin the person-specific axes that flip eligibility (ask if unknown).**
   **Nationality** (EU vs non-EU; treaty routes) — and note that some countries,
   **including China, bar dual nationality, so naturalization may require
   renouncing current citizenship**: an irreversible cost, not a clean "pathway."
   Also: current permit/status, arrival/graduation date, **years of continuous
   legal residence and any time spent abroad** (which breaks the PR clock), salary,
   **age** (age-capped schemes), field/shortage-list, and family status. Watch
   **time windows** — e.g. an orientation-year permit must be applied for within a
   fixed window post-graduation; permits expire.

4. **Check the CURRENT status of employers and the market, not their reputation.**
   A good "fit" is not the same as hiring. Check dated, recent signals — hiring
   freezes, layoffs, restructuring, local/domestic-first or non-EU-tightening.
   **If a specific employer's current hiring status can't be confirmed, say so —
   never infer "probably hiring" from reputation or silence.** Present today's
   reality, dated, with the source.

5. **Route to the official / primary source and date it — no bare numbers.**
   IND.nl, Belastingdienst, the government immigration portal (NL examples) — not relocation
   blogs, agency SEO pages, or forums as a sole source. Any threshold, salary
   figure, fee, processing time, or residence-duration must be quoted from a
   fetched official source with its effective year ("as of <date>, may have
   changed; many update every 1 Jan"), or given as "verify at source."
   Adversarially verify eligibility conclusions, thresholds, and employer status
   before presenting.

Deliver honestly, per §1 rule 6. For each realistic pathway make the reasoning
auditable — **conditions | the person's facts (confirmed / needs-confirm /
unknown) | verified against source (source + as-of date) | cost · time · risk ·
reversibility · sponsor-dependency** — then rank by realistic feasibility *and*
whole cost, never legal openness alone. Frame the output as **informational, not
legal or tax advice** (safety.md rule 5); for a binding determination on a
high-stakes move, recommend the official authority or a licensed immigration
lawyer / tax advisor. Never let optimism outrun what you verified. **Attach the
`references/factcheck.md` "来源 · 时效 · 你需自己确认" block — it doesn't ship without it.**

## If they also have a 命盘 read
Both lenses can speak to 事业, and they are not the same kind of claim (SKILL.md, "When
two lenses touch the same question"). Naming where they **rhyme** is worth doing —
「八字那边读出来的『深耕、要有作品感』，跟你兴趣量表上 Investigative 最高，是同一个人的
两种说法」 — it lands precisely because the two came from different places.

What must not happen: the chart **certifying** the fit result, or a career decision
resting on 大运. The occupation data and their own answers own this question; the chart
says what they *want it to feel like*. If they arrive with 「我八字适合做技术，所以…」,
that's safety.md §1 rule 7 — say so, and run the actual assessment.

A clash is information, not a problem to resolve: a symbol read leaning 表达/作品 against
a data read leaning 分析/独处 usually means the pull and the daily work differ — which
is exactly the useful thing to say out loud.

## Hand-off
When the person moves toward a **specific role/application**, route to the
**`job-hunt` skill** (its *apply* mode) for CV building/tailoring and motivation
letters — that skill owns the honest CV work, and also covers discovering and judging
postings and rehearsing interviews. (`job-application` is the older, narrower skill
covering only the apply step; use it if `job-hunt` isn't installed.) This module owns
fit & direction, not CVs.
