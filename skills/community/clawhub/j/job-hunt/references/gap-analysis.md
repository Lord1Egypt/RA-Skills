# Gap Analysis Reference

A deterministic procedure to compare a candidate's profile against extracted job requirements and produce a tailoring plan. Every rule here is actionable with no ambiguity left to resolve at runtime.

---

## 1. The Comparison Procedure

Work through every `must_have` and `nice_to_have` from the extracted schema (see `job-posting-extraction.md`). For each requirement, classify the candidate as `strong`, `partial`, or `missing`, and cite the evidence.

### Classification definitions

| Label | Meaning |
|---|---|
| `strong` | The profile clearly and directly satisfies the requirement. Evidence is explicit (named tool, quantified outcome, relevant title/role). |
| `partial` | The profile has adjacent or transferable experience that partly covers the requirement, but there is a gap in depth, recency, or exact match. |
| `missing` | The profile has no evidence of meeting this requirement. May be a genuine gap or an omission from the CV — see §3 to determine which. |

**Recency matters.** A must-have evidenced only by **stale** experience — used heavily 5+ years ago with nothing since (e.g. "Python 2012–2017, nothing after") — is `partial`, not `strong`: it satisfies the keyword but reads as rusty to a human. Flag it, and if the candidate has any recent touch (a side project, a course, a current-role mention), surface that to restore currency. Do not invent recent use.

### Output: the gap table

Produce this table after comparing every requirement:

| Requirement | Label | Evidence from profile |
|---|---|---|
| 5+ years backend engineering experience | strong | 7 years across Role A (2017–2021) and Role B (2021–present) |
| Proficiency in Go or Python | strong | Python throughout roles; Go used in Role B side project (confirmed by user) |
| Experience designing distributed systems | partial | Worked on microservices at Role B but as a consumer, not architect — see §3 |
| Experience with Kafka | missing | No mention in CV — ask user before classifying as genuine gap |
| Prior work in fintech | missing | Retail e-commerce background only; fintech is a genuine gap |
| Mentoring junior engineers | partial | One bullet mentions code review; no explicit mentoring language |

Build the full table — do not skip nice-to-haves. Label each one even if obviously missing. Nice-to-haves with `strong` evidence are differentiators; surface them.

### How to find evidence

Look in this order:
1. Work experience bullets (most authoritative — real context, real scope)
2. Skills section (take note: skills listed without context bullets carry weaker weight for `strong` classification)
3. Education / coursework (valid evidence for academic or early-career candidates, or for foundational knowledge)
4. Projects / publications / open-source (valid for technical depth claims)
5. Summary / profile statement (evidence of framing, not of fact — do not use as sole evidence for `strong`)

### Responsibility-evidence pass (align to the day-job, not just the checklist)

Requirements are the *eligibility* filter; the posting's `responsibilities[]` describe the **actual work** — and a CV whose lead bullets visibly mirror that work reads as "already doing this job" to a hiring manager. Must-have coverage is necessary but not sufficient; this pass is what turns a *covered* CV into an *aligned* one. Run it after the requirement table.

For each `responsibility` in the posting, find the candidate's single strongest **real** evidence of having done that kind of work — a bullet, project, or paper — and classify `demonstrated` / `adjacent` / `none`:

| Responsibility (from posting) | Match | Strongest real evidence |
|---|---|---|
| Design & maintain high-throughput data pipelines | demonstrated | Built the ETL pipeline at Role B (5M-row datasets) |
| Mentor junior engineers | adjacent | Code-reviewed peers; no formal mentoring |
| Own model deployment to production | none | Research-only; never shipped to prod |

This drives tailoring directly: a `demonstrated` responsibility whose evidence is **buried** is a LEAD-WITH instruction (surface it into the top third — §4). An `adjacent` one is a REFRAME or honest-gap candidate. A `none` on a **core** responsibility is a real fit gap the user should know about (and the cover letter may address honestly). Never invent evidence to fill a `none`.

### Enrich from the candidate's papers and repositories — fetch before you ask

When the profile names a **paper** (title, DOI, arXiv ID, venue) or links a **repository** (GitHub/GitLab project the candidate owns or contributed to), that artifact is primary evidence of the candidate's real work. **Fetch and read it to extract concrete, truthful detail — do not make the user retype what a tool can read.**

- **How:** use `WebFetch`/`WebSearch` for a paper (abstract, method, headline results, the candidate's listed authorship position); for a repo, fetch the README / project page (and `gh` CLI if available) for what it does, the tech stack, scale signals (stars, downloads, dataset size), and the candidate's specific contribution.
- **What to extract:** the kind of detail that makes a bullet specific and credible — what was built, the techniques/tools actually used, quantified results, and scope. This turns a thin line ("worked on a segmentation model") into an evidenced one ("lightweight SAM variant trained on a single GPU in ~1 day; published in MELBA") — all sourced from the candidate's own artifact, not invented.
- **Honesty (critical):** the artifact being in the candidate's profile is their assertion of authorship — extract only **their** real contribution. For a multi-author paper or a shared repo, attribute honestly (co-author, contributor) and never claim sole credit for collective scope. Pull facts about the work; do not borrow a co-author's part as the candidate's own.
- **Restricted access is the only reason to ask the user.** If the paper is paywalled, the repo is private, or the fetch is blocked, *then* ask the user for the specific facts you need (method, your contribution, the numbers) — phrased honestly, never as an invitation to embellish. Fetching first, asking second.

---

## 2. The Honest-Reframing Decision Rules

Every tailoring decision must pass through these rules before the plan is written. These rules have no exceptions.

### ALLOWED

**Reordering and reprioritising bullets within a role.**
Move the most relevant bullet to the top. If a role had five accomplishments and one is directly relevant to the posting, lead with it. Do not change the dates or the role title.

**Rewording real achievements using the posting's exact terminology.**
If the candidate "built automated deployment scripts" and the posting wants "CI/CD experience", rewrite the bullet to say "built and maintained CI/CD pipelines" — provided the scripts were genuinely part of a deployment workflow. Use `keywords[]` from the extracted schema as the target vocabulary.

> Example:
> Original bullet: "Wrote Python scripts to automate data cleaning."
> Posting keywords: "data pipeline automation", "ETL"
> Rewritten: "Automated ETL data-cleaning pipeline in Python, reducing pre-processing time by 60%."
> ✓ Allowed: same real work, terminology now matches the posting.

**Surfacing transferable skills with honest framing.**
If the candidate has not used the exact tool but has used a directly comparable one, note it transparently.

> Example: Posting requires "Tableau". Candidate has used "Power BI" extensively.
> Honest framing: "Experienced with Power BI for executive dashboards; familiar with Tableau's interface from evaluations."
> ✓ Allowed: the framing is true and the transferability is real.

**Equivalence test — claim true equivalences at full strength (don't under-sell).** Honest ≠ timid. Before hedging an adjacency into "familiar with…", ask: is the candidate's real experience *functionally equivalent* to the requirement, just named differently? — e.g. "REST API design" vs. "building HTTP services"; "Postgres" vs. "relational databases"; one major cloud vs. another for a cloud-agnostic skill; "deep learning" vs. "neural networks". **If yes, claim it at full strength using the posting's term** — that is honest reframing, not a stretch. Reserve hedged "familiar with…" language for genuine *partials* (a real gap in depth/recency/exact-match). Weakening a true equivalence into a `partial` costs the interview with no honesty benefit — it is its own failure mode.

**Adding real-but-omitted detail the user confirms.**
A CV may omit things that are genuinely part of the candidate's background. If gap analysis reveals a potential gap, ask the user first (see §3). If they confirm real experience, add it.

> Example: CV does not mention Docker. User confirms: "Yes, I use Docker every day locally." Add Docker to the skills list and to relevant bullets where accurate.
> ✓ Allowed: real experience, just not yet documented.

**Quantifying vaguely-stated real impact.**
If a bullet says "improved system performance" and the user can supply the actual numbers, update the bullet. When exact numbers are unavailable, use this fallback ladder in order — stop at the most specific level the user can honestly confirm:

| Level | Form | Example |
|---|---|---|
| 1 — Exact number | `X%`, `$X`, `Xms` | "Reduced latency by 38%" |
| 2 — Honest range | "X–Y%" | "Cut processing time by 20–30%" |
| 3 — Scope / scale | "~N users", "Xk records" | "Serving ~200k monthly users" |
| 4 — Before → after | qualitative direction | "Reduced review cycle from days to hours" |
| 5 — Team / org size as proxy | headcount or org scale | "Across a 40-person engineering org" |

Never invent a precise figure. Level 5 is a last resort — a vague but honest scale claim is better than silence, but only barely. Push back up the ladder if the user can recall more.

> ✓ Allowed: honest quantification is better than vague language, and honest approximation is better than silence.

**Not every role is quantified in numbers — match the evidence to the profession.** This ladder is built for measurable-output work (engineering, sales, ops, growth) where a percentage or a dollar figure is the natural currency. Much of the labour market is not like that, and forcing a metric onto it reads as inauthentic or tips into fabrication. For **care (nursing, social work), education, creative/design, legal, public-sector, hospitality, and skilled trades**, the strongest *honest* evidence is usually qualitative and concrete rather than a number: scope and responsibility ("ran a 32-bed ward's night shift solo"), caseload/volume ("managed a 60-client caseload"), outcomes and recognition ("led the unit to its first 'Outstanding' CQC rating"), named results ("won the Henderson appeal"), credentials, inspection/audit ratings, repeat clients, or a portfolio. A specific qualitative statement beats a bolted-on percentage — do **not** manufacture a soft metric ("improved morale by 30%") to satisfy a numbers reflex; that violates the NOT-ALLOWED rules below. Use the number when it's real and natural to the role; otherwise reach for concrete scope, outcome, or credential.

---

### NOT ALLOWED

These actions constitute misrepresentation. Do not do them, do not suggest them, and do not accept user instructions to do them.

| Action | Why it is not allowed |
|---|---|
| Inventing a skill or tool the user has never used | Creates a falsehood the candidate cannot defend in an interview |
| Inflating a title ("Senior Engineer" when the contract says "Engineer II") | Verifiable via background check; also dishonest |
| Dropping a subordinate-rank word ("Assistant Manager" → "Manager", "副总监" → "总监") or shortening an employer or institution into a different one ("Google Developer Student Club" → "Google") | Same inflation; `check_claims.py` reports `QUALIFIER_STRIPPED` / `ORG_TRUNCATED` |
| Relabelling one role with another role's real title (an earlier "Analyst" written as the later "Data Scientist") | Misdates the post; `check_claims.py` reports `TITLE_FROM_OTHER_ENTRY` |
| Changing employment dates to hide a gap or shorten a short tenure | Employment dates are checked; altering them is fraud |
| Claiming sole credit for team accomplishments | Use "Co-led", "contributed to", "part of the team that" |
| Adding a posting keyword the candidate has no genuine experience with | Keyword stuffing that the interview will immediately expose |
| Claiming a degree, certification, or licence not held | Verifiable; fraudulent |
| Implying seniority, scope, or leadership not earned | "Led a cross-functional team" when the candidate was a participant, not the lead |
| Fabricating metrics ("improved performance by 40%") when the user cannot confirm any real number | An invented metric is a lie, not an approximation |

**The one-line rule:** Emphasis and honest reframing — yes. Misrepresentation — no.

**When in doubt:** If you are unsure whether a reframing crosses the line, ask the user. Do not make the call yourself; surface the question explicitly.

### Claim-provenance checkpoint (mandatory)

Before writing any REFRAME or KEYWORD-INSERT that introduces a skill, tool, technology, or scope claim that is not already explicitly in the CV:

**Trace the claim to one of these three sources:**

1. A specific line or field in the candidate's source profile (CV, LinkedIn, portfolio, upload). Cite the exact location.
2. An answer the user gave during this session when asked a supplementary question (§3).
3. A **primary artifact the candidate authored or contributed to** — a paper in their publications list, or a repository they own/contributed to — that you fetched and read this session (see §1, "Enrich from the candidate's papers and repositories"). Extracted facts are valid, strong evidence. For multi-author papers or shared repos, the claim must reflect only the candidate's real contribution — never sole credit for collective scope.

**If none of these sources exists, the claim does NOT enter the CV.** Place it in HONEST-GAPS instead.

> Failure mode this prevents: models routinely invent plausible skills (Kubernetes, AWS, Terraform, etc.) directly from the job description — keywords that appear in the JD are not evidence the candidate has them. Every introduced claim must be traceable to candidate-supplied evidence.

**Where the trace is written down.** The checkpoint is not a habit of mind; it is a
file. Append a row to `<workspace>/claims.yaml` at the moment you write each
REFRAME or KEYWORD-INSERT — `scripts/check_claims.py` reads it, and a term in the
tailored CV that is neither in the master profile nor sourced by a row there is
`UNSOURCED`, which `check_apply.py` will not let a package be delivered over.

The three sources above are exactly the three legal `source_kind` values —
`profile-line`, `session-answer`, `fetched-artifact` — and there is no fourth.
The six required keys, the append-only/`retracted` rule, and a worked example are
in `modes/apply.md` Step 4 and `assets/claims.example.yaml`.

This is written here as well as there on purpose: this file owns the rule, and a
rule whose only remedy is documented in a mode file loaded for a *different* mode
is a rule a run can obey and still be unable to satisfy.

**In the review loop** the checkpoint runs again on every edit made to answer a judge,
before re-rendering. That step, including what to do with an ATS keyword the
candidate does not have, is `modes/apply.md` Step 6, "If `REJECT`", step 1.

---

## 3. Phrasing Gaps to the User and Supplementary Questions

For every `missing` or `partial` requirement, decide which of two cases applies before writing anything into the tailoring plan.

### Case A: The CV may simply omit real experience

The requirement looks like something the candidate might have done but just never wrote down. Ask a targeted question.

**Decision signal:** The skill is foundational for the candidate's level/domain, or it appears in a context (a tool, a methodology) that is common in roles the candidate has held.

**Example supplementary questions by requirement type:**

| Gap type | Question to ask the user |
|---|---|
| Specific tool (e.g. Docker) | "Have you used Docker, even in personal projects, coursework, or a non-primary work context?" |
| Methodology (e.g. Agile/Scrum) | "Did any of your teams run sprints, standups, or retrospectives? Even informally?" |
| Leadership/mentoring | "Did you ever review others' code, onboard a new colleague, or lead a project even informally?" |
| Domain knowledge (e.g. fintech) | "Have you worked with financial data, payment flows, or regulatory requirements in any project or role?" |
| Degree/certification listed as required | "Do you hold this degree or certification, or anything equivalent? If not, are you currently pursuing it?" |
| Quantifiable outcome | "Do you recall the actual numbers for [outcome]? Even an approximate range is fine." |

Ask each question once, clearly, and wait for the answer before writing the tailoring plan. Do not ask the user to speculate about whether they could learn something quickly — the question is strictly about existing experience.

### Case B: A genuine gap

The candidate has genuinely never done this thing and cannot honestly claim related experience. Do not fabricate. Instead:

1. Record it in the tailoring plan as an `HONEST-GAP`.
2. Determine the mitigation from the options in §4.
3. Note the mitigation in the tailoring plan.

**Do not tell the user to pretend the gap does not exist in the cover letter.** The cover letter can address gaps directly and positively (see §4, HONEST-GAPS mitigation option: cover letter).

### Case C: A hard disqualifier (a wall, not a gap)

If the failed requirement is a `[disqualifier]` (work authorization/visa, a legally required licence or clearance, a hard on-site/location requirement, language fluency, a regulated experience floor — see `job-posting-extraction.md`), it is **not** a HONEST-GAP to mitigate with framing. No reframing closes a legal barrier. Instead: **tell the user plainly and let them decide** — "This role requires X, which you don't currently meet; applying anyway is your call, but be aware it's likely an automatic screen-out." Never spend a cover-letter "mitigation" pretending a hard barrier is a soft framing problem. (A disqualifier the candidate *does* meet just needs to be made visible — e.g. a one-line work-authorization note — which the recruiter judge will otherwise flag.)

---

## 4. The Tailoring Plan

The tailoring plan is the structured output of gap analysis. It has exactly four lists. Produce it after the gap table is complete and all supplementary questions have been answered.

### Structure

```
TAILORING PLAN — [Role Title] at [Company]

─── AMPLIFY ─────────────────────────────────────────────────────
Move up / expand these real strengths; they are strong matches:
  Include both must-haves AND strong nice-to-haves. A nice-to-have with `strong`
  evidence is a differentiator — surface it prominently in the CV and mention it
  in the cover letter, especially if it is rare in the applicant pool. Do not
  treat strong nice-to-haves as mere checkboxes.
  1. [Requirement matched] → [Which experience to lead with; where to move it in the CV]
  2. …

─── REFRAME ─────────────────────────────────────────────────────
Reword these real experiences using the posting's vocabulary:
  1. [Current bullet / section] → [Suggested rewording] (target keyword: [keyword])
  2. …

─── KEYWORD-INSERT ──────────────────────────────────────────────
Weave these exact posting terms into the CV where truthful:
  (Only include a keyword here if the candidate has genuine experience with it)
  Placement priority: Skills section FIRST (ATS NER models weight a dedicated
  Skills section more than the same keyword buried in a bullet), then reinforce
  in relevant bullets for the human reader. See cv-craft.md §4 (Keyword placement
  priority) for full guidance.
  1. [Keyword] → Skills section; reinforce in [specific bullet / summary]
  2. …

─── HONEST-GAPS ─────────────────────────────────────────────────
These requirements remain weak after honest tailoring:
  1. [Requirement] — Genuine gap / partial coverage
     Mitigation: [choose one or more]
       • Transferable framing: "[Honest framing sentence to use in the CV or cover letter]"
       • Address in cover letter: "Acknowledge the gap; explain adjacent strength and learning trajectory."
       • Leave: "Do not mention. The gap is minor relative to strong matches and addressing it draws attention."
  2. …
```

### Prioritization under the length limit (LEAD-WITH)

Coverage is necessary, not sufficient — **placement is the other half.** A CV that covers every keyword but buries its best evidence on page two loses the 6–10-second skim to a 70%-coverage CV that leads with its strongest, on-target work. After building AMPLIFY, rank its items by *signal to this role* (not by recency) and decide what lands in the scarce **top third of page one** — the summary plus the first role's first two bullets, which *is* the screen. State explicitly:

- **Summary opening line** — the single most role-relevant identity + the candidate's real standout signal (their marquee employer/lab, rare relevant skill, shipped-at-scale product, or top-venue publication). This is the first thing read; make it specific, not boilerplate.
- **First bullet of the most recent relevant role** — the strongest quantified, on-target achievement.
- **What gets cut or compressed** to make room (per `cv-craft.md §5`): off-target bullets, stale roles, generic skills. Name the cuts; do not silently keep everything and let the page overflow.

This is honest-only: prioritization reorders and trims *real* content — it never invents a standout signal the candidate lacks. If the Hiring Manager review later reports a buried `STANDOUT_SIGNAL`, surfacing it here is the fix.

### FIT SNAPSHOT — show before tailoring (baseline) and after (delta)

A lone coverage count misleads: a CV can cover most must-haves while the candidate is under-leveled or off-domain (both kill the application), or miss several and still be a strong apply on a perfect responsibility + seniority match. Keep a small internal **fit snapshot** — still no fake precision, every line evidence-backed:

```
FIT SNAPSHOT — [Role Title] at [Company]

Must-have coverage:  X of N strongly evidenced (Y partial, Z missing)

| Must-have requirement | In CV? | Evidence |
|---|---|---|
| [Requirement 1] | Yes / Partial / No | CV-nnn |
| … | … | … |

Responsibility match: M of K core responsibilities demonstrated (from the §1 responsibility-evidence pass)
Seniority fit:        step_up / lateral / step_down / unclear — [one line]
Domain fit:           same-domain / adjacent / cross-over — [one line]

APPLY VERDICT: strong_apply / worth_applying / stretch / likely_screen_out / blocked — [one honest sentence why]
```

Record it before tailoring (baseline) and after in `fit-snapshot.md`; explain the meaningful changes in the client report. The apply verdict is the north-star question — it tells the user whether this is worth their time, not just whether the words matched.

**This snapshot and the advice block below are the same judgement in two places, so they must not disagree.** The snapshot is apply mode's before/after view; the advice block is the shape used in internal `fit-assessment.md`. Both carry the same five verdicts from `scripts/vocab.py` — `blocked` included, because a legal barrier is not a weak `likely_screen_out` — and `insufficient_evidence` replaces the whole thing rather than appearing as a sixth level. Both carry the required disclaimer verbatim.

**Computation & labels (avoid two conflicting numbers):** the **"strongly evidenced" count** = must-haves where CV evidence is `strong` (count `partial` and `missing` separately; do not merge them into one "covered" number). **Evidence that is only `dated` counts as `partial`, never `strong`** — stale experience satisfies the keyword and reads as rusty to a human (`gap-analysis.md`, "Recency matters"). That clause is not decoration: `count_coverage.py` applies the same downgrade mechanically, and a snapshot that counts a stale-but-strong must-have as evidenced disagrees with it on the same rows. **When a `fit-assessment.yaml` exists, run `count_coverage.py` and use its numbers rather than counting again by hand** — two paths are tolerable only while they give one answer. This is *not* the same as the ATS screener's coverage formula (which gives partials half-weight: `(present + 0.5·partial)/total`) — label them distinctly ("evidenced must-haves" here vs. "ATS coverage %" from Judge 1) so the user never sees two unreconciled percentages. Be honest about `partial`: a keyword in the Skills list with no supporting bullet is partial, not strong.

**Required disclaimer in the internal snapshot:**

> ⚠️ This is a count of evidence, not a forecast of the outcome. Every must-have is
> printed with the evidence reference behind it, so the denominator can be audited row
> by row and you can object to one line rather than to the whole number. `strongly
> evidenced` counts `strong` only — `partial` and `gap` are never merged into a covered
> number, because merging them needs a weight for a partial match and any weight would
> be invented. This is not a prediction about a screening system: keyword stuffing
> (adding terms not backed by real experience) backfires at interview and with
> sophisticated ATS, and no count here estimates an interview or hiring outcome.
> Whether to apply is your call.

### Mitigation options for HONEST-GAPS

| Option | When to use it |
|---|---|
| **Transferable framing** | A directly adjacent skill exists and can be honestly stated (e.g. Power BI → Tableau). The framing must be true. |
| **Address in cover letter** | The gap is material and likely to be noticed; proactively framing it with strength is better than leaving silence. E.g. "No fintech experience, but direct experience with high-volume transaction data in e-commerce." |
| **Leave** | The gap is minor (a nice-to-have, not a must-have), and the candidate is otherwise strong. Calling attention to a small gap where the rest is strong costs more than it gains. |

Never use "address in cover letter" for a fabricated or exaggerated claim. The cover letter can only say true things.

### Example tailoring plan (abbreviated)

```
TAILORING PLAN — Data Analyst at FinCo (London, hybrid)

─── AMPLIFY ─────────────────────────────────────────────────────
1. SQL proficiency → Lead the Role B bullet with the complex query work;
   move to top of that role's bullet list.
2. Stakeholder communication → Add a bullet to Role A about the quarterly
   board presentation (user confirmed this is real; not yet in CV).

─── REFRAME ─────────────────────────────────────────────────────
1. "Wrote Python scripts to automate data cleaning" →
   "Built Python-based ETL pipeline to automate data cleaning for 5M-row
   event datasets, cutting analyst prep time by 3 hours per sprint."
   (target keywords: ETL, event data, Python)

─── KEYWORD-INSERT ──────────────────────────────────────────────
1. "dbt" → Add to skills section (user confirmed: used dbt in a side
   project to model data for a personal analytics dashboard).
2. "SQL" → Already present; ensure it appears in the summary and the
   skills list, not just in a buried bullet.

─── HONEST-GAPS ─────────────────────────────────────────────────
1. Fintech/payments background — Genuine gap.
   Mitigation (address in cover letter):
   "My analytical work has been in e-commerce at scale (10M+ transactions/
   month), giving me direct exposure to high-volume transactional data
   quality and funnel analysis — skills that transfer directly to a
   fintech Growth team."

2. Looker familiarity — Nice-to-have; partial (used Tableau, not Looker).
   Mitigation (transferable framing):
   "Experienced with Tableau for executive reporting; familiar with Looker's
   data-model approach through self-directed evaluation."
```

### Post-tailoring AI-uniformity check

After completing all REFRAME and KEYWORD-INSERT edits, review the **full CV** for mechanical uniformity before presenting it to the user:

1. **Verb variety:** Are the same stock verbs ("spearheaded", "leveraged", "drove", "utilized") repeated across multiple bullets or roles? Replace repetitive openers with alternatives from the action-verb bank in `cv-craft.md §3`.
2. **Sentence structure variety:** Do bullets follow an identical grammatical template (verb → noun phrase → result → percentage)? Vary the structure — some bullets can lead with the outcome, some with the scope, some with the action.
3. **Voice and specificity:** Does the CV read as one person's work history, or as a generic template filled in with different nouns? Each role should have at least one detail that is unmistakably that candidate's experience.
4. **Prose quality:** Flawless-but-voiceless prose signals AI generation to experienced recruiters. Preserve natural sentence rhythms even when the grammar is corrected.

5. **The 2026 vocabulary:** `spearheaded`, `pivotal`, `intricate`, `showcasing`, `delve`, `realm`, `robust`, `cutting-edge`, `seamless`, "a valuable asset". These are the terms recruiters currently report flagging, and `scripts/lint_cv.py` reports them as `AI_VOCABULARY` — over the **whole document**, not only the bullets, because the summary is the line a recruiter reads first and it used to be the one line nothing checked.
   Skills, certification and publication lines are not scanned for it: there the word is part of a product name or a citation ("Pivotal Cloud Foundry").

If the uniformity check fails on any dimension, make targeted repairs before delivering the final CV.

The lint is the floor, not the check. It sees the word `pivotal`; it cannot see that three roles were written to the same template, and dimensions 1–4 above are exactly the part no gate measures. Passing `lint_cv` cleanly is not evidence the CV reads as a person's.

Cross-reference: `motivation-letter.md §6` (AI-Authenticity) for the same principle applied to the cover letter — including the structural tells (em-dash density, "not just X, but Y", tricolon density; `check_letter.py` reports them as `EM_DASH_DENSITY`, `NOT_JUST_PIVOT`, `TRICOLON_DENSITY`) that are checked on a letter and deliberately **not** on a CV: a skills line reads "Python, C++, MATLAB" and a bullet is terse by design, so those checks would fire on every correct CV.

---

## 5. Cross-References

**`cv-craft.md`** — consult for:
- Bullet pattern and action-verb bank when rewriting bullets in REFRAME
- ATS keyword mirroring rules and keyword placement priority (§4 of cv-craft.md) — the same principle drives KEYWORD-INSERT
- Honest reframing rules in §7 of cv-craft.md — identical standard governs this file
- AI-generated uniformity note in §7 of cv-craft.md

**Motivation letter / cover letter** — the same honest-reframing rule that governs the CV governs the cover letter. HONEST-GAPS mitigations that involve the cover letter must still be factually accurate. The cover letter may frame, contextualise, and project forward — it may not invent.

**Interaction between gap analysis and the final CV** — the tailoring plan is the bridge. Once approved, each item in AMPLIFY, REFRAME, and KEYWORD-INSERT translates to a specific edit in the CV. HONEST-GAPS drive the cover-letter strategy. Do not edit the CV before the tailoring plan is confirmed by the user.

## Hard disqualifiers are a wall

Some must-haves are **non-negotiable barriers** the candidate cannot close by tailoring or learning: **work authorization / visa** for the country, a **legally required license or security clearance**, a **hard on-site/location** requirement, **language fluency**, or a **regulated experience floor**. Tag these `[disqualifier]` (distinct from an ordinary must-have like "Kubernetes", which is recoverable).

Surface `[disqualifier]` items **first** in the §4 confirmation and ask the user directly: *"These look non-negotiable — do you meet them? If not, this may not be worth a full application."* This protects the user's time on day one (the recruiter judge would otherwise only catch a logistics wall after a whole package is built), and it keeps a genuine legal barrier from being mis-handled downstream as a soft "framing" gap (see `gap-analysis.md §3`).

## The advice block, and the disclaimer that is not optional

In the internal `fit-assessment.md`, state the assessment in exactly this
shape — counted facts, then one word, then the disclaimer. Client `report.md` is
written separately using `references/report-writing.md`; it does not copy this block. **The block follows the
user's language, not the market's**, so both shapes are here; `scripts/count_coverage.py`
emits them with `--lang zh` and `--lang en` and is the only path that produces the counts.

    必备条件有充分证据：   X 项，共 N 项   （部分符合 P，存在缺口 G，无证据 U）
    核心职责已证实：     M 项，共 K 项
    职级匹配：           <上跳 | 平级 | 下沉 | 不明>
    可补缺口所需投入：   <当天 | 一晚 | 数日 | 补不上>
    投递建议：           <强烈建议投 | 值得投 | 可以冲刺 | 大概率被筛掉 | 硬性阻断>

    must-haves strongly evidenced:   X of N   (partial P, gap G, no evidence U)
    core responsibilities demonstrated: M of K
    level match:                     <step_up | lateral | step_down | unclear>
    effort to close the gaps:        <quick | evening | multi_day | not_closable>
    apply verdict:                   <strong_apply | worth_applying | stretch |
                                      likely_screen_out | blocked>

**Immediately under the internal block, keep the matching disclaimer unchanged.** Counts and
required report text support zh, en, ja, ko and es. Read
[report-localization.md](report-localization.md) for Japanese, Korean or
Spanish headings, disclaimers, notices and discover disclosure templates. The gate
checks the language's explicit anchor; a free paraphrase may still fail as `NO_DISCLAIMER`.

> ⚠️ 以上是对证据的清点，不是对结果的预判。每一项都连同它的证据引用一起印出，分母可以逐条审计；
> 本 skill 不给出面试或录用的可能性估计，也不给 0–100 分。要不要投，由你决定。

> ⚠️ This is a count of evidence, not a forecast of the outcome. Every item is printed
> with its evidence reference so the denominator can be audited row by row. This skill
> states no interview or hiring outcome estimate and no 0–100 score. Whether to apply
> is your call.

Every item inside N and K is printed with its evidence reference, so the denominator
is auditable. The strongly evidenced count takes only `strong`; `partial` and `gap` are never folded into
a "covered" number; evidence that is only `dated` counts as `partial`, never `strong`.
When the input cannot support a conclusion at all, the whole block is replaced by
the refusal, `insufficient_evidence` (zh `证据不足—不出结论`), and the reason. That is
a refusal, not a sixth level, and it is never softened into `stretch`.

## Words this skill does not put in its output

No percentages of fit. No self-invented scales (`7/10`, `B+`, "score: 82"). No
probability language at all: `概率`, `chance`, `odds`, `likely to be hired`,
`likely to be interviewed`, `strong candidate`, `would pass`. There is no data
behind any of them — "interview probability 45–65%" is a number someone made up,
and a weighted total is the same fabrication with arithmetic on top. The advice is
one word from the five, and the counts beside it are counts of evidence.

**The one exception, and its shape.** When the employer has published its own rubric
— a UK Civil Service Success Profiles level named in the advert, an NHS values
framework, a university person specification — this skill may walk the candidate
through **that** scale, in the employer's own wording, with the source named, framed
as "what the panel is asked to look at". Quoting the employer's scale is reporting.
Using it as a conclusion is fabrication. Never assert a score on it.

## The grounding contract

```
  Original source             Referenced claim              Check
  posting-source.txt --> JD-001…JD-080 --> requirement row --> check_evidence_refs.py
  cv.md / profile    --> CV-001…CV-080 --> requirement row --> resolves or is dropped

  profile.yaml field       --|
  answer in this session   --|--> claims.yaml --> each REFRAME / KEYWORD-INSERT
  candidate artifact read  --|                                |
                                                             v
                                                      check_claims.py

  Human-authored commit --> market-conventions/<key>.yaml
                                       |
                            allowlisted IDs; verbatim text
                            no model paraphrase
                                       v
                               check_conventions.py
```

1. **Evidence blocks tie the analysis to the source text.** The model may only cite
   blocks that exist; a reference that will not resolve is **dropped, not fatal**. An
   empty evidence list is not an error — rejecting it would punish the honest shape,
   and a *fabricated* reference lands in that same empty array and passes anyway.
   Carry the honest boundary into the skill's own output:
   **this is a floor on credibility, not a proof — it guarantees a claim points at
   something that really exists, not that the claim follows from it.**
2. **Claim provenance ties the output to source facts.** Three permitted sources,
   and there is no fourth. `claims.yaml` is the first thing that makes it a diffable
   artifact instead of a habit.
3. **Market tables tie down the one class of claim with no citable source.** In this
   whole skill exactly one kind of statement cannot be traced to text the user gave
   us: what this market screens for that the posting does not say. So it is written
   by a person, dated, with its source kind, whitelisted by id, and **rendered
   verbatim** — the model may not strengthen "usually" into "must", may not attach a
   number to it, and may not invent a row.

**Restate the fence next to the field that tempts the violation.** A rule at the top
of fifty instructions is not where the model is standing when it writes the dangerous
field. The no-fabrication rule is restated in exactly three places: the KEYWORD-INSERT
step, mock-interview question generation (a question premise the CV does not support is
a fabrication the candidate then repeats back), and the shortlist's `why_matched` field.
