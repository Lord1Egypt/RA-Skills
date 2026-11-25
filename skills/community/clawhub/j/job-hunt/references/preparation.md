# Interview preparation: the plan, knowledge drills, coding drills

Read this **in full** in prepare mode, and in interview mode before the first question
whenever the round type is `knowledge` or `coding` or a posting plan is written.
`modes/prepare.md` and `modes/interview.md` §0 both name it, and the gates check what
it defines: the plan (`check_prep_plan.py`), the `RECALL` / `SOLVE` rows, the hint
log, `result.json` and `study-notes-<n>.md` (`check_drill.py`, `check_mock.py`).

**This is for every profession.** A nurse is asked about deterioration and
safeguarding, an accountant about revenue recognition, an electrician about safe
isolation, a teacher to teach part of a lesson, a consultant to crack a case, a German
trainee to sit an Assessment-Center, a Chinese 公务员 candidate to pass 行测 and 申论
before any interview. Software fundamentals and LeetCode are one row of §4, not the
default. A plan that hands an algorithm list to someone whose loop has none is the
failure this file exists to prevent.

Story rounds rehearse what the candidate **lived** and must never supply it. Knowledge
and coding drills test what can be **learned**, and there teaching is the point.
`modes/interview.md` "Knowledge and coding rounds — teaching is allowed" holds the
binding rules. They apply in prepare mode unchanged.

## 1. The preparation plan

Two plans, one format:

- **The general plan**, `prep-plan.md` in a prepare workspace (`<profile>/prep/<date>-<direction>/`).
  It is built from the target direction and the CV, with no posting, and is reused
  across applications. The newest one is `paths.latest_prep_plan(<name>)`.
- **The posting plan**, `mock/prep-plan.md` in an interview workspace. Read the
  general plan first and list only what this posting adds: named technologies,
  procedures or standards, a named test or assessment day, and CV claims this
  application will be probed on. With no general plan, the posting plan is the whole
  plan.

**Build it from, in this order:**

1. **The loop for this market and family**, from `references/interview-shapes.md`.
   Which stages exist and what each weighs: a written exam or ability test, an
   Assessment-Center or assessment day, a structured or values-based interview, a
   case, a taught lesson, a coding round. Also the register: 八股 at speed for China
   tech, STARR with reflectie for the Netherlands, a 2–3 minute Selbstpräsentation and
   CV-consistency questions for Germany, values-based questions for the NHS, the
   identical structured questions of US federal hiring. **Only that file's
   provenance labels decide what may be said about a market**: an `[S]` row may set
   the plan's shape and never be quoted as fact, and a `[U]` row is not stated.
   For a market with no rows there (`other`), say so in the plan and build from the
   family alone.
2. **The direction** (`direction.yaml`): the target titles, the level (campus /
   new graduate / experienced / senior), the timeline.
3. **The CV.** Anything on it can be asked about in depth, and a listed skill the
   candidate cannot explain under one "why" looks worse than one they left off.
   Topics behind CV claims go near the top. For story rounds, the plan names **which
   real CV lines** answer which competency. It never writes the story.
4. **The family catalogue** (§4) fills what the first three leave open. It is a
   starting checklist of commonly tested areas, not a claim about any employer.

One entry per topic, most important first:

```markdown
## Recognising and escalating a deteriorating patient
- why: cv: "Recognised a deteriorating patient on placement"
- be able to: name the early signs of sepsis, explain how an early-warning score
  triggers escalation, and hand over with SBAR
- practise: knowledge
```

| Field | Rule |
|---|---|
| `- why:` | **Required.** One of `direction: "<words copied from direction.yaml>"`, `posting: "<words copied from posting.yaml>"`, `cv: "<words copied from cv.md>"`, `shape: <the interview-shapes row>`, `family: <the §4 area>`. A quoted reason must really be in that file: `check_prep_plan.py` fails `PREP_WHY_NOT_IN_SOURCE` otherwise, and `PREP_WHY_NO_SOURCE` for a `posting:` reason in a session that has no posting |
| `- be able to:` | **Required.** Concrete abilities, not a topic name. "Know accounting" is a reading list. "Explain when revenue is recognised over time rather than at a point in time" is preparation |
| `- practise:` | **Required.** `knowledge` or `coding` (drilled in prepare mode, or in interview mode for a posting); `behavioural`, `case`, `role-play`, `presentation` or `design` (rehearsed in interview mode once there is a posting, or alone with the plan's pointers); `self-study` |
| other lines | Optional: a drill suggestion, the CV line that raises the stakes, a pattern list for coding, a format note (timed test, panel size) taken from a shapes row |

Keep it to what decides this loop. Ten well-chosen topics beat forty. For coding,
list **patterns** (two pointers, sliding window, BFS/DFS, binary search, heaps,
intervals, dynamic programming) with the reason each one fits, not problem numbers.

**Honesty.** No link that was not opened this session. Name a resource only when you
are certain it exists, by title. Never write "this employer asks X" unless the
provenance rules allow it. Predicting **topics** is the job; predicting the outcome
is not, and the no-prediction lint scans the plan.

Run `python3 scripts/check_prep_plan.py --workspace <ws>`, then put the plan in the
session's `report.md` as its own section (the client never sees `mock/` or the
workspace files).

## 2. Knowledge drill — `ROUND-TYPE: knowledge`

Questions with a **checkable** answer: facts, mechanisms, procedures, rules,
calculations. Every field has them: clinical guidelines and drug safety, accounting
standards, legal doctrine and procedure, electrical and building regulations,
safeguarding procedure, product metrics, database isolation levels. Original
**ability-test practice items** (numerical, verbal, logical reasoning; 行测-style) are
knowledge drills too. Say plainly that they are not the real test: its timing, norms
and difficulty cannot be reproduced here.

A question without one right answer (a values scenario, a case, a role-play, "tell me
about a time") is **not** a knowledge drill. Those are rehearsed in interview mode,
where the story rules and both assessors apply.

**Pick the questions** from the plan, or from the family area and the CV when there
is none. Mix recall ("what does SBAR stand for?") with mechanism ("why does a fast
breathing rate matter more than a single high temperature?") and one "what goes
wrong" question per topic.

**The register follows the market.** For a China 技术一面, run 八股 as it is run: many
short questions at pace, each followed by one 追问 ("为什么？", "那如果…呢？"). Elsewhere,
ask fewer questions and go deeper, with the follow-up that tests whether the answer
was understood or memorised.

**Ask up front** whether the candidate wants the explanation after each answer or at
the end. After-each is better for learning, at-the-end is closer to the real room.
Either way, **never teach before the answer**: the question is asked cold.

**Hints only when asked.** Three levels, each logged as its own transcript turn so the
gate can count them:

```markdown
**Hint (nudge):** Think about what the body does first when an infection spreads.
**Hint (approach):** Look at the vital signs one by one: which change early?
**Hint (solution):** Breathing rate, heart rate and new confusion change early.
```

Escalate one level per request and never skip ahead. An explanation after the answer
is an `**Explanation:**` turn, not a hint.

**Assess** with one `RECALL` row per question heading:
`RECALL: result=<r> | hint=<highest level given> | ref=Q<n> | quote=<the candidate's words>`

| `result` | When |
|---|---|
| `correct` | The checkable core is right and nothing wrong was stated |
| `partial` | Some of it right, with something missing or one wrong claim (quote the wrong claim) |
| `incorrect` | The core is wrong |
| `no_answer` | The candidate did not know or declined (quote what they said) |

A follow-up asked under its own `## Q<n>b` heading needs its own row. A follow-up kept
inside the parent heading does not.

## 3. Coding drill — `ROUND-TYPE: coding`

For families whose loop has code in it (§4). The part of 手撕代码 / a live coding
interview this skill **can** run: the candidate writes real code, it runs against
hidden cases, and the follow-ups probe it. What it **cannot** run is someone watching
them type under time pressure. Say so, and offer a clock: note the start and end time
in the transcript if the candidate wants it timed.

**1. The problem.** Write it yourself in the style of the family's platform: a
statement, the input/output format, constraints, one worked example. Do not paste a
LeetCode or 牛客 statement. Naming the pattern after the round is fine. Size it so an
approach, the code and the follow-ups fit inside the round length the loop shape
gives (the China rows say 30–45 minutes per round). Default to stdin/stdout
(ACM-style, as China 笔试 use). For a function-style problem, give the signature and
write a small driver file beside the solution that reads stdin, calls the function and
prints the answer.

**2. The hidden cases, before the candidate's code is seen.** In
`mock/code/round-<n>/Q<n>/cases.json`, a list of `{"name", "stdin", "expected"}`: the
worked example, then the edge cases that separate a solution from an attempt (empty
input, one element, all equal, duplicates, negatives, the boundary values in the
constraints), and one large case sized so the intended complexity finishes and a brute
force does not. Every answer must have one canonical printed form (sorted, fixed
precision), because the runner compares text.

**3. Approach first.** Ask for the approach and its complexity before any code. If the
candidate skips it, ask once.

**4. The code.** The candidate saves the solution into that directory, or pastes it in
chat and you save it **byte for byte**. Never fix a typo while saving it: the bug is
the finding.

**5. Run it:**

```bash
python3 scripts/run_mock_tests.py --dir <ws>/mock/code/round-<n>/Q<n> \
    --cmd "python3 <solution file>"     # or: --build "g++ -O2 -o sol sol.cpp" --cmd ./sol
```

`--cmd` and `--build` run through the system shell, which on Windows is `cmd.exe`:
write `python <solution file>` or the built `.exe` there, not `python3` or `./<binary>`.

Log the outcome as an interviewer turn, `**Test run:** 2 of 3 cases passed (failed:
empty input)`. Name the failed cases and keep their inputs hidden: revealing a failing
input is a `nudge` hint and is logged as one. The candidate may fix and resubmit;
re-run, log each run, and the `SOLVE` row reports the **final** run.

**6. Follow-ups**, inside the same heading or as `Q<n>b`: complexity, "what if the
input does not fit in memory?", "what if the values can repeat?".

**Assess** with one `SOLVE` row per question heading:
`SOLVE: tests=<t> | complexity=<c> | hint=<highest level given> | ref=Q<n> | quote=<the candidate's approach or complexity statement>`

- `tests` is what `result.json` records: `all_passed`, `some_failed`, `none_passed`,
  or `not_run` when no code was executed. The gates recompute the status from the
  per-case outcomes and the hashes of the cases and the code, so `TESTS_MISREPORTED`
  and `STALE_TEST_RESULT` catch a pass that was never run, or a run of code that has
  since changed.
- `complexity`: `stated_correct`, `stated_wrong` or `not_stated`, for the code as
  written.

## 4. Family catalogue — what is commonly tested

A starting checklist of the areas each family's interviews commonly draw on, for the
gaps the loop shape, the direction and the CV leave open. **General knowledge, not a
sourced claim about any employer or market**: it never overrides a shapes row or a
posting and is never quoted to the candidate as "they will ask". The families follow
`references/role-families.md`, plus the technical ones.

| Family | Knowledge areas | Live exercise to expect |
|---|---|---|
| Clinical / licensed healthcare | Recognising deterioration and escalation, infection control, medication safety, safeguarding, consent and confidentiality, handover structures, the profession's code of conduct | Values-based questions; clinical scenarios; sometimes an assessment day or multiple mini-interviews |
| Sales / business development | The sales process and qualification, pipeline and quota metrics, the product and the buyer's industry | A role-played discovery call or pitch; objection handling |
| Skilled trades | Safety regulations and safe working practice, the trade's codes and standards, tools and testing procedures | A practical test or task; a safety scenario |
| Legal | Core doctrine for the practice area, procedure, professional conduct rules, recent cases in the area | Discussing a matter; a drafting or research exercise |
| Finance / accounting | Accounting standards, the three statements and how they link, valuation basics, tax or audit basics for the role | Technical questions; a case or modelling exercise; ability tests at graduate level |
| Consulting / strategy | Structured problem-solving, market sizing, unit economics | A case interview; a personal-experience interview |
| Public sector / government | The published behaviours or competencies, the department's remit; in China 行测 and 申论 content | Structured interviews against named criteria; written exercises; ability tests |
| Creative / design | Design process and critique, tools, accessibility basics, the employer's product | A portfolio walkthrough; a critique or take-home brief |
| Education / teaching | Safeguarding procedure, behaviour management, assessment for learning, the curriculum for the subject and phase | Teaching a lesson or activity; safeguarding scenarios |
| Hospitality / retail / service | Service standards, food and health safety, handling complaints, cash and stock basics | A role-played customer situation; a trial shift |
| Product management | Product sense, metrics and experiments, prioritisation, working with engineering and design | A product or metrics case; a prioritisation exercise |
| Software / backend | Data structures and complexity; operating systems (processes vs threads, memory, concurrency); networking (TCP vs UDP, HTTP); databases (indexes, transactions, isolation levels); the main language's internals | Coding; system design from mid level |
| Frontend | The JavaScript runtime and event loop, browser rendering, CSS layout, framework state and rendering, web performance and security | Coding (often UI or DOM); component design |
| ML / AI engineering | ML fundamentals (bias–variance, regularisation, losses, metrics, validation); deep learning (backpropagation, optimisers, attention and transformers); LLM topics (fine-tuning, retrieval, evaluation); serving and data pipelines | Coding; ML system design; implementing a component from scratch |
| Data science / analytics | Probability and statistics, hypothesis tests and A/B experiments, regression, product metrics | Live SQL; a metrics case |
| Data engineering | SQL, data modelling, batch vs streaming, distributed processing, data quality | SQL; pipeline design |
| Quant | Probability, statistics, mental arithmetic | Coding; probability questions at speed |
| Embedded / hardware | C and memory layout, interrupts, concurrency and RTOS basics, digital logic, buses | Low-level coding |
| SRE / DevOps / security | Linux, networking, containers, observability, incident debugging; for security, web vulnerabilities, authentication, threat modelling | A troubleshooting or bug-finding walkthrough |
| Research / imaging / signal processing | Linear algebra, Fourier analysis and sampling, inverse problems and regularisation, optimisation, the domain's physics (e.g. MRI: k-space, undersampling, parallel imaging, compressed sensing) | A job talk; defending a past paper; coding |

For a family not listed, ask the one question from `references/interview-shapes.md`:
**"In your field, what does the employer make you do live — talk, demonstrate, be
scored against written criteria, or be role-played at?"**

## 5. Study notes — `mock/study-notes-<n>.md`

The debrief for a drill, one `## Q<n>` entry per question heading (the gates fail
`STUDY_NOTE_MISSING` otherwise), each with:

- the correct answer or a model solution (code in fenced blocks: the no-prediction
  lint skips code, not prose), with its complexity for code;
- what the candidate's answer missed, quoting their words: the wrong claim, the
  missing item, the failed case names;
- the concept or pattern to study next, and a follow-up drill **described**, not a
  numbered link.

Everything here is public knowledge, which teaching may supply. None of it is the
candidate's experience: it never enters `answer-bank.md`, `claims.yaml` or the CV.

In interview mode, `open-loops.md` still gets the round's unanswered questions. In
prepare mode, what the drills exposed goes back into the plan: revise `prep-plan.md`
(move a weak topic up, add the missing concept) and say what changed in the report.
