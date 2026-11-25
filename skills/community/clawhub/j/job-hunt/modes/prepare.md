# Mode: prepare

**Entry:** the user wants to prepare for interviews in their field and market, with no
specific posting needed: what to study and how, or to practise knowledge questions,
ability-test items or coding. Examples: "help me prepare for nursing interviews in
the UK", "秋招后端岗要准备什么", "I have Assessment-Center interviews for trainee
programmes coming up", "drill me on accounting fundamentals". When they have a
specific posting and an interview for it, that is interview mode: offer it instead.

**Writes:** one workspace, `<profile>/prep/<YYYY-MM-DD>-<direction>/`, holding
`direction.yaml`, `cv.md`, `prep-plan.md`, drills under `mock/`, and `report.md`.
It never modifies the master profile, `answer-bank.md` or any application workspace.
What a drill teaches is knowledge, not experience, so nothing from it becomes a CV
line, a claim or a story.

This mode serves **every profession**. The software rows are one family among
many. Read `references/preparation.md` before assuming a loop has a coding round.

## 0. Enter

```bash
python3 scripts/paths.py --name "<name>" --prep "<direction in a few words>"
python3 scripts/enter_mode.py --workspace <workspace> --mode prepare \
    --because "<why prepare, in one line, from what the user asked>"
```

Then read `references/interview-shapes.md` and `references/preparation.md` **in full**.
The first holds what each market's loop consists of, with provenance labels. The
second holds the plan format, both drill procedures and the family catalogue. The
plan cannot be written without either.

If `paths.latest_prep_plan(<name>)` returns a plan, read it. This session revises that
plan rather than starting over: copy it into the new workspace and change what the
new direction or the last drills call for.

## 1. Intake — one message, selectable options

Confirm, in one message:

1. **Target roles**: the titles, and the family from §4 of `references/preparation.md`.
   Ask. Never infer the target from the CV's latest job, which is the job they may be
   leaving.
2. **Market**: `cn | nl | de | uk | us | other`. Ask; never infer it from a place
   name. Note that `other` means the shapes file has no rows for that market, and the
   plan will say so.
3. **Level**: campus or new graduate (校招), early career, experienced (社招), senior or
   lead. For the public sector, which route (e.g. 国考 / 省考, a Civil Service grade).
4. **This session**: a plan only, a plan and a first drill, or a drill on the existing
   plan.
5. **Known weak spots or worries**, optional.

The CV: the master profile if one exists (`scripts/paths.py`, read-only), else the CV
or background the user gives. Save the text this session uses as `cv.md`. With
neither, the plan uses `direction:`, `shape:` and `family:` reasons only.

Write `direction.yaml` in the user's own words:

```yaml
target_titles: ["Staff Nurse (Band 5)"]
family: clinical
market: uk
level: newly qualified
timeline: interviews expected within two months
weak_spots: ["clinical scenario questions"]
```

## 2. The plan — `prep-plan.md`

Follow `references/preparation.md` §1. Open with **the loop being prepared for**: the
stages for this market, family and level in order, each from its shapes row (an `[S]`
row is phrased as commonly seen, never quoted as fact). The order matters. A 公务员
candidate prepares the written exam first. A UK graduate prepares ability tests and an
assessment centre before the final interview. A German trainee prepares the
Assessment-Center exercises and a 2–3 minute Selbstpräsentation. A Dutch candidate
prepares STARR answers with reflectie. Then list the topics, most important first.

```bash
python3 scripts/check_prep_plan.py --workspace <workspace>
```

Exit 0 = the plan holds up. Exit 1 = findings, one per line: fix the plan, never the
source files. Exit 2 = it could not run.

## 3. Drills — optional, `knowledge` or `coding` only

A drill is a knowledge round (facts, procedures, rules, calculations, ability-test
practice items, from any field) or a coding round, run exactly as
`references/preparation.md` §2–3 describes. A story, values, case or role-play round
needs the story rules and both assessors, so it belongs in interview mode with a
posting. Say so and offer it, rather than running a thin version here.

Run it **inline**, the interviewer being you. Flush `mock/transcript-<n>.md` after
every answer, with a header (`Round type:`, `Market:`, `Family:`) and one
`## Q<n> — <question>` heading per question. Log every hint as `**Hint (<level>):**`.
Run code only through `scripts/run_mock_tests.py`.

**Assess with one pass.** Dispatch `agents/mock-assessor-transcript.md`, in a fresh
context (`Agent`; on other hosts `references/portability.md` §2), never yourself, with the
transcript, `direction.yaml`, `cv.md` and, for coding, each
`mock/code/round-<n>/Q<n>/result.json`. Copy its `MOCK-ASSESSMENT-V1` block verbatim
into `mock/assessment-<n>.md`. There is no posting, so no `COVERAGE` rows, and no
provenance pass, because a drill writes nothing about the candidate's experience. An
invalid block gets the interview mode §4 recovery: at most one corrective re-dispatch,
the failed output kept under `mock/raw/`.

Write `mock/study-notes-<n>.md` (`references/preparation.md` §5), then:

```bash
python3 scripts/check_drill.py --workspace <workspace> --round <n>
```

Then revise `prep-plan.md` with what the drill exposed, and re-run
`check_prep_plan.py`.

If the candidate states an experience in passing that is not in `cv.md`, it is not
evidence for the plan. Mention it in the report as something to add to the CV,
through apply mode, if it is true.

## 4. Report and delivery

Follow SKILL.md "Client deliverables". Read `references/report-writing.md` first.
`report.md` carries:

- the plan in full, in reader form;
- each drill's results: per question, what was right and what was missed, the hints
  used, and for code the executed case counts;
- what to practise next.

Render and review it, run `lint_no_prediction.py`, then
`python3 scripts/deliver.py --workspace <workspace>` last. Do not start another mode
automatically.

## Self-check before reporting the session complete

- [ ] `references/interview-shapes.md` and `references/preparation.md` were read this session
- [ ] `direction.yaml` and `cv.md` hold what the user said and gave; nothing was written to the master profile or the answer bank
- [ ] the plan opens with the loop for this market, family and level; `scripts/check_prep_plan.py` exited 0 and its receipt is in `journal.jsonl`
- [ ] every drill: transcript flushed after each answer, hints logged, code run only by `scripts/run_mock_tests.py`, one assessor block copied verbatim, study notes per question, `scripts/check_drill.py` exited 0 with a receipt
- [ ] `report.md` carries the plan and the drill results; `deliver.py` ran

**Hand-off:** offer `discover` (roles to apply to), or `interview` once a posting and
an interview exist.
