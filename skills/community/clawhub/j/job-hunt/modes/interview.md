# Mode: interview

**Entry:** the workspace holds an application package, **or** the user has a posting plus
a CV and says they have an interview.

**Reads:** `posting.yaml`, `cv.md`, `tailored-profile.yaml`, `fit-assessment.*`,
`interview-brief.md`, `claims.yaml`.
**Interview artifacts:** `mock/`. Also author the client `report.md` required by
the delivery contract below. Plus two append-only write-backs: a `## Walk-back list`
section on `interview-brief.md`, and `source_kind: session-answer` rows on `claims.yaml`.
Nothing else in the workspace is modified, and `profile.yaml` is never touched.

## Supplementary public research

Use `references/supplementary-sources.md` when official web/news, WeChat
public accounts or relevant GitHub projects can fill a concrete career evidence
gap. It defines source selection, availability checks and evidence quality.
These sources supplement formal posting evidence; select only what the current
question needs.

## 0. Before the first question

**Without an application package** (the user brought a posting and a CV but no apply run):
create the workspace with `paths.workspace(...)` as assess does, extract the posting into
`posting.yaml` per `modes/assess.md` §3, and save the CV the user gave you as `cv.md`.
`python3 scripts/paths.py --name … --company … --role …` creates it and prints its absolute path.
`check_mock.py` requires `posting.yaml` (`NO_POSTING` otherwise), and the first assessment
pass reads `cv.md`.

**Record the mode entry first, before reading anything else:**

```bash
python3 scripts/enter_mode.py --workspace <workspace> --mode interview \
    --because "<why interview, in one line, from what the user asked>"
```

`scripts/check_mock.py` fails the round with `NO_MODE_ENTRY` without this record and
`MODE_FILE_CHANGED` if this file changed after you read it.

Then read `references/interview-shapes.md` in full. It holds the market × family loop
shapes, the four band descriptors, and both closed tag sets — you cannot write
`mock/assessment-<n>.md` without them, and you cannot pick a realistic round order without
the shapes.

Then confirm three things with the user, in one message:

1. **Market** — ask; never infer it from a place name. `cn | nl | de | uk | us | other`.
2. **Role family** — from `references/role-families.md`. If it is not one of the nine, ask
   the one question that resolves the shape: *"In your field, what does the employer make
   you do live — talk, demonstrate, be scored against written criteria, or be role-played
   at?"*
3. **Round type for this session** — `behavioural | technical | design | hr`. One per
   session; see §3.

## 1. Fix the shape

From `references/interview-shapes.md`, state the loop the candidate is walking into: the
rounds, in the local vocabulary, with who is in the room. Say plainly which rounds this
mode **cannot** simulate (手撕代码 under a watching interviewer, an in-person MMI circuit,
a whiteboard chalk talk) rather than running a thin imitation of them.

Give the interviewer a **named persona** drawn from that shape — a 交叉面 interviewer from
another department who has not read the CV closely; a Bar Raiser from outside the team; a
panel member scoring one named Success Profiles behaviour at the grade in the advert; a
Dutch hiring manager who will ask about anything questionable on the CV without preamble.
The persona costs nothing and is most of what makes a text interview feel like anything.

## 2. Seed `mock/question-log.yaml`

Each question records its source: `generated`, `scraped`, `judge-supplementary`
(carried over from the CV judges' `SUPPLEMENTARY_QUESTIONS_FOR_CANDIDATE`), or
`user-provided` (questions or an existing transcript supplied by the user).

For `user-provided` questions, preserve the original input in the workspace and
keep the questions and answers verbatim. They are user-supplied material, not
independently verified evidence of the employer's process. When asked to debrief
an existing round, analyse those answers; do not invent a new conversation or
relabel them as generated questions. All assessment and provenance checks still apply.

**Generated questions are the high-value ones.** *"You wrote that you cut deploy time 40% —
how did you measure that?"* exists in no archive, and it is the question that catches an
over-tailoring the three CV judges passed. Build the generated set to cover every must-have
in `posting.yaml`.

**Scraped material sets SHAPE; generated material sets CONTENT.** They are not competing
sources of the same thing. Reach for a scraped item when you need a fact about the
employer's process you cannot derive from the posting: a named ritual (交叉面, HRBP面, Bar
Raiser, 宣讲会, 群面, a specific take-home), the round count and order, who is in the room,
the pacing.

### Scraped material — the rules

```
Every scraped item is (a) opened with `detail` for untruncated text — a `search` row is
  elided and must never be quoted, (b) stamped with its `time` in question-log.yaml, and
  (c) shown to the candidate with that date.
Anything older than ~12 months may be used for SHAPE (round count, order, ritual names)
  but is never quoted as a specific technical question.
COUNTRY RULE. Never use a scraped item whose company entity sits in a different country
  from the posting, unless the post itself names that country. Log it under `rejected:`
  with `reason: wrong_country` so the filter is visible.
Never paste a scraped post's ANSWER to the candidate — questions only. A 面经 that
  includes the poster's own answer is a script, and handing over a script is the exact
  thing the anti-coaching rules forbid.
Filter advertising. Posts that open with a course pitch, a 辅导 offer, or a contact email
  are commercial material wearing a 面经 costume. Log them `reason: advertising`.
If the adapter returns 403 or "need login", report the source as unavailable and generate
  instead. Do not log in to work around it.
`nowcoder papers --company/--job` filters are inert (verified: three different filter
  values returned byte-identical rows). Use `papers` as a company/role index only.
```

**The COUNTRY RULE comes first:** `opencli nowcoder search "ASML 面试"` returns genuine
posts about the company's China entity — matching name, wrong process, nothing that
looks wrong.

### `mock/question-log.yaml`

`check_mock.py` reads this file. Keys marked **scraped-only** are required on any row with
`source: scraped` and ignored elsewhere.

| Key | Meaning |
|---|---|
| `round` | integer, the round this log belongs to |
| `posting_country` | ISO-2 country of the **posting** — without it the country rule cannot fire |
| `questions[].id` | `Q1`, `Q2`, … — must match the transcript's `## Q<n>` headings |
| `questions[].text` | the question as it will be asked |
| `questions[].source` | `generated` \| `scraped` \| `judge-supplementary` \| `user-provided` |
| `questions[].asked` | whether it was actually put to the candidate |
| `questions[].source_site` | **scraped-only** — e.g. `nowcoder` |
| `questions[].source_id` | **scraped-only** — the id `detail` was called with |
| `questions[].source_url` | **scraped-only** |
| `questions[].source_time` | **scraped-only** — the ISO timestamp from `detail`, verbatim |
| `questions[].entity_country` | **scraped-only** — ISO-2 of the entity the post describes |
| `questions[].country_named_in_post` | **scraped-only** — true only if the post itself names the posting's country |
| `questions[].use` | **scraped-only** — `question` (may be quoted) or `shape` (structure only) |
| `rejected[].reason` | `wrong_country` \| `stale_specific` \| `advertising` \| `needs_login` \| `answer_included` |

<!-- example: question-log.yaml -->
```yaml
round: 2
posting_country: NL
questions:
  - id: Q1
    text: Walk me through the reconstruction pipeline you owned.
    source: generated
    asked: true
  - id: Q2
    text: You wrote that you rewrote the recon loop for GPU batching — how did you measure the change?
    source: judge-supplementary
    asked: true
  - id: Q3
    text: 讲一下 variational network 的展开步数怎么定的
    source: scraped
    source_site: nowcoder
    source_id: "ce23c4da4205"
    source_url: https://www.nowcoder.com/discuss/ce23c4da4205
    source_time: "2026-08-03T11:12:22"
    entity_country: NL
    country_named_in_post: true
    use: question
    asked: true
rejected:
  - id: R1
    text: "ASML 宣讲会 → 笔试 → 二面 → HR 电话面 timeline"
    source: scraped
    source_site: nowcoder
    source_id: "057523b2ca9d"
    source_time: "2026-08-06T11:06:49"
    entity_country: CN
    reason: wrong_country
  - id: R2
    text: "27届秋招…可以了解下算法项目辅导"
    source: scraped
    source_site: nowcoder
    source_id: "a1b2c3d4e5f6"
    source_time: "2026-07-30T08:00:00"
    entity_country: CN
    reason: advertising
```

## 3. Run ONE round, inline

**The interviewer is you, in this conversation** — a spawned subagent has no channel
to ask a question and wait for the human.

**One round per dispatch.** Finish the round, assess it, write the artifacts, and stop.
Round n+1 starts fresh.

**FLUSH THE TRANSCRIPT AFTER EVERY ANSWER.** Append the question and the answer to
`mock/transcript-<n>.md` the moment the candidate finishes speaking — not at the end of the
round. This buys pause/resume for free, keeps the assessors reading a *file* rather than
this conversation, and means a crashed session loses one answer instead of a round. The
transcript is a raw capture: **never edit it.** Every downstream claim's source chain
terminates here.

**One `## Q<n> — <the question>` heading per question, and the `<n>` matches
`question-log.yaml`.** Those headings are the only thing `ref=` can point at: without
them `check_mock.py` has nothing to check an assessor's references against, and it says
so with `NO_QUESTION_HEADINGS` rather than passing them all in silence.

Ask from the log, then go where the answer leads. The log is seed material — its coverage
value is realised by **auditing it after the round**, not by reading from it during. A
question bank cannot follow up on an answer it did not anticipate, and "held under probe"
is the only band above `asserted` that means anything.

While you interview, the anti-coaching rules below ("Mock interview — the anti-coaching line") bind on every turn: never write an
answer for the candidate, never ask a leading question, never build a question on a premise
the CV does not support, and never rehearse a gap into a non-gap.

<!-- example: transcript-<n>.md -->
```markdown
# Mock transcript — round 2
Round type: technical
Market: nl
Family: ml-engineering
Persona: Sanne de Vries, MR reconstruction team lead — direct, asks for numbers

## Q1 — Walk me through the reconstruction pipeline you owned.
**Interviewer:** Walk me through the reconstruction pipeline you owned.
**Candidate:** At the university hospital I owned the offline recon pipeline for a 3T scanner study.

## Q2 — What did you change about it, and what happened as a result?
**Interviewer:** What did you change about it, and what happened as a result?
**Candidate:** I replaced the per-slice loop with a batched GPU implementation.
```

## 4. Assess — two passes, deliberately different inputs

Dispatch **both** assessors in one message (two `Agent` calls, in parallel). Each gets
exactly the files in its row and nothing else:

| Pass | Agent file | Given | **Deliberately NOT given** |
|---|---|---|---|
| 1 — transcript | `agents/mock-assessor-transcript.md` | `mock/transcript-<n>.md`, `posting.yaml`, `cv.md` | `interview-brief.md`, `claims.yaml` — so it cannot credit the candidate for a source fact they never said out loud |
| 2 — provenance | `agents/mock-assessor-provenance.md` | `mock/transcript-<n>.md`, `claims.yaml`, `interview-brief.md` | the rubric — so it cannot drift into grading, which is what makes a provenance-holding assessor lenient |

Two passes fed different inputs is what turns the honesty tripwire from an intention into a
mechanism. Do not "helpfully" hand pass 1 the brief.

Then assemble `mock/assessment-<n>.md`: **both output blocks copied in verbatim**, plus a
short human-readable summary above them. Never hand-edit an assessor's block.

Keep copies and SHA-256 hashes of the exact input packs dispatched to each
assessor. The final brief may gain the prescribed walk-back list after review,
but retain the assessed version separately. If a later edit changes a fact,
provenance mapping or a question that affects the assessment, rerun the affected
independent pass on that revision. For purely editorial changes, preserve the
diff and describe the change honestly; do not claim all reviewed files stayed
byte-identical.

### Recover an invalid assessor block

If `scripts/check_mock.py` reports `PARSE_FAIL`, `MISSING_BLOCK`, or
`QUOTE_NOT_IN_TRANSCRIPT`, use this bounded recovery:

1. Identify the failed pass from the block name in the diagnostic:
   `MOCK-ASSESSMENT-V1` is transcript; `MOCK-PROVENANCE-V1` is provenance. A quote can
   exist elsewhere in the transcript and still be invalid: `ref=Q1` must quote the
   candidate's answer under that same heading, not Q2 or the interviewer.
2. Preserve the original failed assessment, raw assessor output, gate stdout/stderr,
   and journal receipt under `mock/raw/recovery-<n>/` before replacing anything. The
   `raw/` directory keeps failed drafts and audit logs out of `deliver.py` exports.
   Keep the original receipt in `journal.jsonl`; the recovery adds evidence, never
   erases it.
3. Re-dispatch only the failed pass, in a fresh context, with the same agent prompt and
   byte-identical source files from its row above. Add only that pass's gate diagnostics
   and an instruction to produce a complete block whose quotes belong to their cited
   candidate answers. Never supply the other pass's output, diagnostics, or input pack.
   Keep any valid pass's block byte-identical. If both failed, reassess each separately
   with its own permitted pack. Allow **at most one corrective reassessment per failed
   pass per round**, including parse, missing-block, and quote failures together.
4. Preserve the corrective dispatch inputs and raw output alongside the failure. Copy
   its new block verbatim, update session artifacts under §5–6 where required, and
   re-run the full gate. Never hand-edit a block, including its `ref=` or `quote=`.
   Never change the transcript or candidate facts to make a quote validate.
5. If it still fails, stop and report the remaining findings and both gate receipts.
   Do not loop until green or call the round complete. A new assessor finding is handled
   honestly under §5–6; it is not a reason to erase the finding or reroll the assessor.

<!-- example: assessment-<n>.md -->
```markdown
# Mock assessment — round 2

Two passes ran on this transcript with deliberately different inputs.

MOCK-ASSESSMENT-V1
ROUND: 2
ROUND-TYPE: technical
MARKET: nl
FAMILY: ml-engineering
FINDING: tag=VAGUE-OUTCOME | ref=Q2 | quote=It went really well after that.
BAND: dimension=outcome | value=asserted | ref=Q2 | quote=It went really well after that.
COVERAGE: status=evidenced | must_have=MRI reconstruction pipelines in a clinical setting
SHAPE: status=rehearsed | round_name=technisch gesprek met de vakinhoudelijke manager
END-MOCK-ASSESSMENT-V1

MOCK-PROVENANCE-V1
ROUND: 2
FINDINGS: none
END-MOCK-PROVENANCE-V1
```

## 5. Write the session artifacts

**`~/.claude/job-profiles/<name>/answer-bank.md`** — the profile-level file, not a
per-application one. It is the only artifact that compounds across applications. One entry
per real story, in the candidate's **own words as actually spoken**, with a `- source:` line
that traces the load-bearing fact to `profile.yaml`, to `interview-brief.md`'s provenance
map, or to a session answer with its date. `check_mock.py` fails an entry with no
`- source:` line: an entry the candidate cannot trace is worse than no entry, because they
will say it out loud in the real room believing it was vetted.

<!-- example: answer-bank.md -->
```markdown
# Answer bank

## Batched GPU reconstruction on the 3T study
- serves: "tell me about an optimisation you made"; round 2 Q2
- source: profile.yaml:experience[0].bullets[2] — "rewrote the recon loop for GPU batching"
- session: 2026-08-09 — applications/asml-mr-recon-engineer-2026-08-09/mock/transcript-2.md#Q2
- S: offline recon for a 3T scanner study at the university hospital
- T: the per-slice loop was the bottleneck in the nightly batch
- A: replaced the per-slice loop with a batched GPU implementation
- R: open loop — the measured change was not stated in the room
- R2 (reflectie): profile before optimising, and write the baseline down first
```

**`mock/open-loops.md`** — every question the candidate could not answer, in **three
buckets**, because they have three completely different actions:

1. **a fact you have but did not recall** → go and find it before the real interview;
2. **a genuine gap** → use the honest framing already chosen in `interview-brief.md`;
3. **a tailoring error** → the claim comes off the CV (this bucket feeds §6).

Merging them into one "weak areas" list destroys the artifact.

**`mock/answer-guide.md`** — per-question guidance, and the one artifact in this mode
where being useful pulls directly against the load-bearing rule. A question list with
nothing about what a good answer contains is half a deliverable. But the questions that
most need a model answer are exactly the ones the candidate has no evidence for, and a
satisfying answer to those can only be written by inventing the experience — so the
distinction is made mechanical rather than left to tone.

**Never write the candidate's answer in their voice.** What ships is a skeleton they
fill: the STARR slots carrying only facts already in the profile, what the interviewer
is listening for, and which defect tag the answer fails on. A first-person paragraph is
a script, it gets recited, and a recited answer collapses on the first Dutch follow-up —
which is `PROBE-COLLAPSE`, arriving in the real room instead of this one.

`## ` is reserved for entries. A section divider written as a heading is read as an
entry with no fields and fails — which is the right way round: letting some `## `
headings be exempt would make "call it a divider" a way to ship guidance with no
source. Use bold prose or `### ` for structure.

Every entry carries three lines `check_mock.py` reads:

| Line | Meaning |
|---|---|
| `- row:` | the requirement id(s) in `fit-assessment.yaml` this answer serves; several are comma-separated |
| `- basis:` | `evidenced` \| `honest_gap` — there is no third value and no default |
| `- source:` | where the load-bearing fact comes from: a `profile.yaml` path, or a session answer with its date |

The gate reads `fit-assessment.yaml` and fails `GUIDE_GAP_AS_EVIDENCED` when an entry
serves a row scored `gap` or `no_evidence` and declares itself `evidenced`. There is no
default for `basis` on purpose: defaulting picks a side of the honesty distinction on
the author's behalf, and the safe-looking default is the unsafe one. An entry naming an
evidenced row alongside a gapped one does not launder the second through the first.

For a `honest_gap` entry the content is the framing from `references/interview-prep.md`
§2 — the nearest real thing the candidate HAS done, then how they would come at the
requirement — and never a narrated instance of work they have not done. That is not
rehearsing a gap into a non-gap; it is the only honest answer to the question, and
withholding it leaves the candidate to improvise on exactly the questions that will
decide the round.

When the workspace has no `fit-assessment.yaml` the cross-check cannot run and says so
on stderr (`NO_ASSESSMENT_TO_CHECK_AGAINST`); the shape checks still run.

**`mock/cheatsheet.md`** — one page. The stories, one line each; the 2–4 honest gaps with
their exact framing; the questions still unanswered; the candidate's questions for them;
the loop shape with round names in the local vocabulary. If it exceeds one page it has
failed.

## 6. Write-backs

**(a) Walk-back list.** Append a `## Walk-back list` section to `interview-brief.md` for
every CV claim that collapsed under **one** follow-up. Then **offer to re-run the tailoring
edit and re-render** — that is the point of the section; a list nobody acts on is a note.

An undefendable claim is a **CV bug, not a rehearsal topic.** This is the mechanism that
fires `references/interview-prep.md`'s over-reach rule, which until now had no trigger: the
three CV judges read a page, and the page does not stammer.

<!-- example: walk-back list -->
```markdown
## Walk-back list

### WB-1 — "Rewrote the offline reconstruction loop for GPU batching, cutting runtime 40%."
- transcript: mock/transcript-2.md — Q3
- quote: Honestly it might have been closer to a third, I am not sure any more.
- defect: PROBE-COLLAPSE
- softened: "Rewrote the offline reconstruction loop for GPU batching (measured speed-up; exact figure not retained)."
- status: proposed
```

`check_mock.py` requires this section whenever `PROBE-COLLAPSE`, `OVER-CLAIM`, or
`CONTRADICTED` fired, and requires an entry quoting **each** such finding.
A proposed walk-back records an open issue; it does not resolve an
`UNSOURCED-FACT`, even when the same quote also triggered `OVER-CLAIM`. Resolve
that fact only after the candidate confirms it or withdraws it. For a completed
withdrawal or correction, record `status: withdrawn` or `status: applied` and
retain the actual confirmation or edit evidence. Never relabel `proposed` merely
to satisfy the gate.

**(b) Promote a confirmed-but-absent fact.** An `UNSOURCED-FACT` usually resolves to "it's
true, it's just not on my CV". Ask the candidate where it came from **before** it enters the
answer bank. If the answer is that it is real, that is a genuine gap-analysis finding: append
a row to `claims.yaml` with `source_kind: session-answer` — an already-permitted provenance
— and route it back into the tailoring plan.

```yaml
- term: PACS export
  where: tailoring-plan.md:promoted-from-mock
  source_kind: session-answer
  source_ref: mock/transcript-2.md#Q1
  session_date: "2026-08-09"
  retracted: null
```

If instead it was drift under pressure, it goes on the walk-back list. Either way it is
resolved, never silently kept.

## 7. Gate

Run:

```
python3 scripts/check_mock.py --workspace <workspace> --round <n>
```

Exit 0 = the round holds up. Exit 1 = findings on stdout, one per line. Exit 2 = it could
not run — fix the input, never proceed. **Do not report the round as complete without
quoting the `check_mock` receipt from `<workspace>/journal.jsonl`.** A gate that was skipped
produces no output, and that looks exactly like a gate that passed.

The `MOCK-ASSESSMENT-V1` block must actually assess something: at least one `BAND:`
(`NO_BANDS`), at least one `SHAPE:` (`NO_SHAPE`), and one `COVERAGE:` row per must-have in
`posting.yaml` (`NO_COVERAGE_ROW`, which names the uncovered one). `mock/open-loops.md` and
`mock/cheatsheet.md` must exist and be non-empty (`NO_OPEN_LOOPS`, `NO_CHEATSHEET`). None of
these applies to `MOCK-PROVENANCE-V1`: `ROUND:` plus `FINDINGS: none` is its documented clean

## 8. Round n+1

Carry forward an **open-loops summary** only — the unresolved probes and the questions that
wobbled — not the full transcript. The transcript is on disk; the assessors read it there.
That is the context-cost mitigation, and it is why the transcript is flushed after every
answer rather than held in this conversation.

## Published employer rubric — the one place a number is honest

Where the employer publishes its own scale — UK Civil Service Success Profiles behaviours at
the grade named in the advert, an NHS values framework, a university person specification —
you may walk the candidate through **that** scale, in the employer's own wording, **attributed**,
as a checklist of what the panel is told to look for:

> the Civil Service scale used here reads: 4 = "Adequate positive evidence and any negative
> evidence would not cause concern"

**Never as a prediction of the mark.** Quoting an employer's scale is reporting; applying it
as a verdict is fabrication. Everywhere else, no score, no percentage, no probability, no
"strong candidate", no invented scale — see the banned-vocabulary block in references/gap-analysis.md.

## Hand the artifacts over — `deliver.py`, not a sentence in the final message

Deliver the debrief report. The CV used by the assessors remains source material;
`deliver.py` does not copy or render it in this mode unless the user explicitly
requests the existing application documents and you pass `--include-applications`.

`deliver.py` also delivers the current `interview-brief.md` in this mode, because the
walk-back list was just appended to it and the copy apply delivered does not have it.
The quick-reference body must still fit on the actual PDF's first page
(`INTERVIEW_BRIEF_TOO_LONG`). The complete structured `## Walk-back list` follows
as an appendix in the same Markdown/PDF and may span further pages; retain every
record and put no further quick-reference sections after it. In the final
message, point the candidate at the new `面试准备/` copy and say the earlier one is
superseded.

Then follow SKILL.md "Client deliverables": write `report.md` (read
`references/report-writing.md` first), render and review it, run
`lint_no_prediction.py`, then `python3 scripts/deliver.py --workspace <ws>` last (client files go to `~/Downloads/<workspace-name>/`). Do
not start another mode automatically.

## Self-check before reporting the session complete

- [ ] `references/interview-shapes.md` was read this session
- [ ] `mock/transcript-<n>.md` was appended to after **every** answer, and never edited
- [ ] both assessors were dispatched, each with exactly its own pack (`agents/mock-assessor-transcript.md`, `agents/mock-assessor-provenance.md`)
- [ ] `mock/assessment-<n>.md` contains both blocks verbatim
- [ ] `mock/question-log.yaml`, `mock/open-loops.md`, `mock/answer-guide.md`, `mock/cheatsheet.md` and the profile-level `answer-bank.md` are written
- [ ] every `answer-guide.md` entry carries `- row:`, `- basis:` and `- source:`, no entry is a first-person script, and no entry serving a gapped row claims `evidenced`
- [ ] every walk-back and every promoted claim from §6 is on disk
- [ ] `scripts/check_mock.py` exited 0 and its receipt is in `journal.jsonl`

**Voice.** The debrief tells someone what they got wrong. `references/report-writing.md`, "How this skill writes to the user", governs its prose — quote them rather than characterise them, and say the finding before the cushioning.

## Mock interview — the anti-coaching line

### Rehearse retrieval, never rehearse content

A mock interview may help the candidate FIND, ORDER, and COMPRESS a true story they
already lived. It may not help them ACQUIRE one. The test is where the fact came from:

- If a detail traces to the profile, to the provenance map in `interview-brief.md`, or to
  something the candidate told you earlier in this session — helping them say it better is
  preparation.
- If a detail first appears in YOUR mouth — a number, a tool, a scope, a motive, a
  result — it is fabrication, however plausible, and it stays fabrication after the candidate
  agrees with it.

**Four hard rules.**

1. **Never write an answer for the candidate.** You may name what is missing ("your answer
   never said what changed as a result"). You may not supply the missing part. Naming a gap
   is feedback; filling it is ghostwriting a lie.

2. **A leading question is a fabrication vector.** "So you'd say you owned the migration?"
   hands the candidate an over-claim they will repeat in the real room and will not be able
   to defend. Ask "who owned the migration?" — open, and let the answer be whatever it is.
   This applies to your interview questions too: never build a question on a premise the CV
   does not support ("when you led that team of twelve").

3. **An undefendable claim is a CV bug, not a story to drill.** If the candidate cannot
   truthfully support a CV claim under ONE follow-up, that is a tailoring error. Log it to
   the walk-back list and change the CV. This is `references/interview-prep.md`'s over-reach
   rule — the mock interview is the stage where it actually fires, because the three CV
   judges only read the page and the page does not stammer.

4. **Never rehearse a gap into a non-gap.** For an HONEST-GAP the only preparation is the
   truthful framing already chosen in the tailoring plan. Do not produce a smoother version
   that implies experience the candidate lacks. "I haven't done X" must survive rehearsal
   intact; only the sentence around it may improve.

**The tripwire.** Any figure, tool, employer, title, or scope that appears in the
candidate's answer and is in NEITHER the profile, NOR `interview-brief.md`, NOR an earlier
answer this session, is tagged `UNSOURCED-FACT` (or `OVER-CLAIM` if it exceeds a recorded
source fact) and the candidate is asked where it came from BEFORE it may enter the answer
bank. Usually the answer is "it's true, it's just not on my CV" — that is a real finding and
it should probably go on the CV. Sometimes it is drift under pressure. Either way it gets
resolved, never silently kept: an answer-bank entry containing an unsourced fact is worse
than no answer bank, because the candidate will say it out loud in the real interview
believing you vetted it.

### Mock-interview session mechanics

- Flush the transcript after every answer; the first assessment pass does not see
  `interview-brief.md` or `claims.yaml` (see §3–§4).
- **Bands, not scores.** `not_present` / `asserted` / `instanced` / `held_under_probe`, plus
  the non-band flag `contradicted`. They are unnumbered so they cannot be averaged, and
  `held_under_probe` is the ceiling on purpose: a higher band would require knowing what
  this employer expects at this level, and this skill does not.
- **The interviewer and both assessors may not emit** a score, grade, percentage or invented
  "X out of Y"; a probability, likelihood or odds; "you would pass / fail / they would hire
  you"; "strong candidate" / "weak candidate" / "hire" / "no-hire"; any comparison to other
  candidates; any claim about what the interviewer thought or would conclude; or a rating on
a scale the employer did not publish (the published-rubric exception above applies).
  Predicting the **questions** is the job ("大概率会被问到系统设计", "likely to be asked
  about…"); predicting the **outcome** is not, and that includes numberless certainty
  ("你肯定能过", "you will definitely pass").
