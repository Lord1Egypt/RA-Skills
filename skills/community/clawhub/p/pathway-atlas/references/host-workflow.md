# Host workflow command guide

Use the first-response and quiet-preparation rules in [SKILL.md](../SKILL.md)
before this command guide. Ask the current student question first; perform
necessary authorized setup or wrapper maintenance while awaiting the answer
when the host actually supports background work. Keep one intake draft and
track real jobs internally. Without asynchronous execution, ask first and do
necessary preparation in later turns; do not invent a running background job.
Only a verified blocker requiring the user's action warrants an interruption.
Successful preparation resumes the existing flow without another start choice.

This facade serves the confirmed anonymous profile. Default delivery uses the
quick planning branch; the full receipt loop below is optional deep verification. Every command, JSON file, saved source and returned path stays inside a
host-owned private workspace. The family sees the current question, profile
confirmation, decision-relevant findings and the final report. Routine setup,
test output, wrapper changes and tool diagnostics stay internal.

For failed tools, inaccessible pages, missing parsers or evidence gaps, use the
[research recovery guide](research-recovery.md). Probe actual source reading;
preflight records declarations and discoverable modules, not a successful browser
launch or website request. `browse` includes a working host page reader or HTTP
reader, not just Chrome. With `browse` but no `search`, `standard` can read known
official sources and their public navigation while disclosing limited discovery.
Only when no source-reading route works should live evidence collection stop;
search snippets alone cannot establish facts. Explicit `offline` stays offline.

## Normalize the confirmed intake

New CLI sessions require `--intake <private-workspace>/intake.json` and a real
profile confirmation. Follow [the bounded questionnaire](questionnaire.md):
24 thematic prompts, one clarification per theme and six total. The 72 fields
are storage coverage, not separate conversational turns. `scripts.intake_progress`
returns `question_id`, `question_fields`, `next_question` and the current phase.
Use its `--record` action to append one actual reply and host-extracted field
quotes to a private schema 1.1 state. Reuse volunteered answers across fields.
Do not resubmit the same reply after a tool timeout; inspect saved state first.

`deferred_fields` are details left uncollected after a covered question; they
are distinct from explicit unknown, skipped or an unasked topic. Disclose these
limits in the profile confirmation and map them to unknown values in v3 while
retaining the raw progress record. A deferred fact is never a positive/negative
eligibility decision, an exact number or a claim that the parent answered.
`confirming` means summarize once; bind the actual reply to the profile and
progress digests. Only `ready_for_planning=true` permits CLI start. Existing
schema 1.0 confirmed receipts remain valid; in-progress records keep all facts
and may migrate with retained genuine question history. Initialized sessions
resume normally. Restore missing internal files from actual dialogue, not by
asking the family again. The low-level API does not bypass intake requirements.

Before rendering a grade question, use the July 1 cohort rule in
the questionnaire above, section 年级与高考年份.
`python -m scripts.questionnaire_intake --grade-options` supplies current
Asia/Shanghai date-based labels without opening a session or altering any
profile. It is an intake helper, not a new startup prerequisite. Preserve an
explicit exam year in topic 4; never derive it from `research_year` or
recalculate it during session replay. Without execution, apply the same rule
using the host's reliable current date; without that date, omit years from
the grade options and ask the expected exam year next.

Keep all twenty topic keys regardless of conversational question order. After
collection, `scripts.questionnaire_intake.build_profile_from_questionnaire(...)`
accepts a Python mapping with **integer keys 1–20** and produces a v3
`PlanningProfile`. `parse_numbered_questionnaire(...)` is only compatibility
import for a complete numbered document volunteered by the user, not an intake
prerequisite. JSON answer files use string keys; the `start --answers` CLI
converts them internally. Prefer `--profile` if a confirmed v3 export exists.

For topic 8, preserve school rank as the primary observation and keep each joint
exam rank in `additional_observations`: `scope` is `city_joint` or
`province_joint`, and `source` is `joint_exam_report`. Do not replace several
observations with one. Topic 20 readiness keys are `english_readiness`,
`interview_readiness` and `physical_readiness`; unanswered readiness, strengths
or research experience remain `unknown` or empty. Read `ProvinceConfig.mode`
from the trusted province registry and use the canonical subject key. Do not
hard-code province modes or change the student's selected subjects.

`scripts/host_workflow.py` calls `scripts/planning_session.py` to retain one
state and replay typed receipts across processes. It only consumes the confirmed
profile, canonical QueryPlan and fresh evidence bundle. Maintenance checks may
run before confirmation on isolated test data; student-specific planning and
research begin only after the user confirms the collected profile.

## Command loop

Run the Python module commands with the installed Skill root as the command's
working directory. Keep all session files in the separate private workspace.

After profile confirmation, `start` performs `init`, `confirm`, capability
preflight, canonical QueryPlan binding and a journal checkpoint internally.
Pass only truly callable `search`, `browse` and `vision` capabilities;
`local_exec` and `file_output` are separate workflow gates. Preflight tiers are
`full`, `standard` and `offline`; reduced capability lowers coverage, not evidence
standards. Exit code `2` means invalid input, extraction, evidence or host
operation; `3` means an optional capability is unavailable. Neither code proves
that a checkpoint or report was written. Verify saved state before claiming it.
Successful initialization reaches `query_plan_ready` and returns the session ID
and `initial_delivery_action=collect_sources_then_brief`. Follow `first_delivery`
only before the first report; reuse an existing delivered brief on resume.
`next` contains optional deep-research tasks, not a requirement for the initial
report. Its time budget includes setup and repair from user confirmation.
Initialization details alone are not a report.

Expected runtime failures emit one JSON object to stderr with `ok=false`,
`report_generated=false`, `error_code`, `user_message`, `host_action` and
`user_action_required=false`. The latter means the exception alone does not
establish a need for family intervention. Execute `host_action` privately using
the recovery guide, preserving validation boundaries and existing data. If a
limitation affects the delivered result, use the short Chinese `user_message`
and the actual next step; do not paste the JSON into chat. A genuinely verified
user-only access gate can still require minimal action. Routine failures do not
require the family to choose a recovery route. Argument/help output remains a
developer interface, not a family-facing answer.

Create a private workspace and a UTF-8 normalized-answer file, then start once:

```text
python -m scripts.host_workflow start --workspace <private-workspace> --answers <private-workspace>/answers.json --intake <private-workspace>/intake.json --confirmed [--host-capability search] [--host-capability browse] [--host-capability vision]
```

`--answers` accepts the normalized mapping with keys `1` through `20`.
If the host already has the user's confirmed `PlanningProfile.to_dict()` v3
export, use `--profile <private-workspace>/profile.json` instead. For recovery
from older host calls, `--answers` also detects this exported profile shape.
Its digest and mode are checked; never rebuild answered questions just to change
the input format. An existing session should be resumed, not initialized again.

For recovery, reuse the original workspace and session with `brief`. Use `next`
to inspect the stage and resume `ingest`, `unavailable` or `finish` only for
requested deep verification. `PlanningWorkflow.resume` calls
`journal.load(session_id)` with `PlanningSessionReplayContext` as the sole replay
context; its methods handle `finalize_evidence`, `calculate` and `publish`.
`status` snapshots, session/manifest digests and caller-rebuilt JSON do not
restore completed receipts or replace factory replay. Keep the same private
journal and validated evidence bundle; preserve the last valid checkpoint if
loading fails, without re-asking already answered questions.

`start` and `next` return `report_generated=false`: they have not generated a
report. `first_delivery` is workflow guidance, not proof of a brief run.
`brief` must succeed with `report_generated=true` and nonempty `report_text`,
which the host then delivers in chat. A downloaded spreadsheet or saved session
does not satisfy delivery. Routine source choices and fallbacks do not require
the user to choose whether the host should continue.

For the default first delivery, read [quick planning](quick-planning.md), prepare its
source-linked input from a bounded round of research, and run:

```text
python -m scripts.host_workflow brief --workspace <private-workspace> --session <session-id> --submission <private-workspace>/brief.json
```

Deliver the returned `report_text` in its fixed order. `delivery.mode` is
`planning_reference`; it is not an authenticated deep-research receipt. This
command preserves the journal, completed evidence and pending research tasks.
Do not mark unattempted deep tasks unavailable just to deliver a brief.

For optional deep verification, continue the following loop.

Read `session_id` and `next` from stdout JSON. Keep both internal. Resume and get
the current bounded task list with:

```text
python -m scripts.host_workflow next --workspace <private-workspace> --session <session-id> --limit 3
```

Every command other than `brief` and `finish` returns the same status shape: `pending` is the total
number of unfinished tasks, while `next` contains only the requested display
slice. The default limit is 3 and the accepted range is 1 through 100. Hidden
pending tasks remain in the journal. The slice is ordered by newest year first,
then kind and task ID. There is no separate `status` command.

`research_summary` accompanies every status and `finish` response:

```json
{
  "total": 72,
  "completed": 1,
  "unavailable": 3,
  "pending": 68,
  "unavailable_by_reason": {"newer_comparable_year_accepted": 3}
}
```

These illustrative counts describe task outcomes, not successful source requests
or qualified pathways. `older_year_resolution` is a list of hints, each containing
`newer_task`, `task_ids` and `reason: "newer_comparable_year_accepted"`. Each hint
passes the existing same-family, newer-year and usable official receipt checks.
It does not change the journal or remove pending tasks. Inspect comparability,
then explicitly pass those IDs to `unavailable`; the command rechecks the receipt.
There is no hint when a partial or otherwise unusable receipt cannot justify it.

For one returned task, search only within its declared kind, year, province,
subject context and candidate limit. Open each retained public page or attachment,
save it in the private workspace, write one submission file, then run:

```text
python -m scripts.host_workflow ingest --workspace <private-workspace> --session <session-id> --task <task-id> --submission <private-workspace>/submission.json
```

When the bounded search cannot produce an admissible extraction, record the real
reason and continue:

```text
python -m scripts.host_workflow unavailable --workspace <private-workspace> --session <session-id> --task <task-id> [--task <task-id>] --reason <stable-reason>
```

After a newer comparable task in the same family has completed, close an older
pending task only with the completed task's receipt-backed ID:

```text
python -m scripts.host_workflow unavailable --workspace <private-workspace> --session <session-id> --task <older-task-id> --reason newer_comparable_year_accepted --newer-task <completed-task-id>
```

The facade loads that typed receipt from the journal and lets the state machine
verify its family and year. Do not pass `--newer-task` for another reason. The
facade never skips older tasks automatically.

The multi-year matrix is bounded fallback work, not a requirement for every year
to succeed. Process each family's newest year first and continue other families
when one stalls. A shared, actually observed outage may close the affected tasks
in one command; do not retry a broken browser separately for every task. First
consume any already saved, admissible material and try the available alternative
routes described in the recovery guide. For example, after all applicable online
readers have failed and neither pending task has readable saved evidence:

```text
python -m scripts.host_workflow unavailable --workspace <private-workspace> --session <session-id> --task <affected-task-1> --task <affected-task-2> --reason network_unavailable
python -m scripts.host_workflow next --workspace <private-workspace> --session <session-id> --limit 100
```

Repeat only for the remaining affected IDs. Use `capability_unavailable` for a
format with no working extractor, not every task in the plan. An inaccessible
page does not establish `current_year_not_published`, and a tool failure says
nothing about the student's eligibility.

Repeat `next` after every `ingest` or `unavailable`. When `pending` is zero,
publish through the same facade:

```text
python -m scripts.host_workflow finish --workspace <private-workspace> --session <session-id> --format markdown
python -m scripts.host_workflow finish --workspace <private-workspace> --session <session-id> --format docx
```

Exit `0` returns JSON status or the report path. Exit `2` keeps the last checkpoint
after invalid input, extraction, evidence or filesystem state. Exit `3` means an
optional format or adapter capability is unavailable; retain the Markdown path or
record the affected task unavailable. Re-run any command with the same workspace
and session after process loss; the facade replays its journal and typed receipts.

`finish` returns `report_text`: the complete UTF-8 Markdown report body rebuilt
from the authenticated calculation checkpoint, for both Markdown and DOCX exports.
This is the host's source material for its detailed, reader-friendly final answer
in the conversation. A `report` path is an optional attachment location; a file
link or a short summary alone does not complete delivery. If a tool truncates the
JSON output, the Agent reads the full returned report itself before explaining it.

Follow SKILL.md and references/conversation-output.md: explain all conclusions,
school and major choices, pathway decisions, priority actions, staged plans,
risks and evidence gaps directly in chat. Translate internal labels into readable
Chinese while preserving every decision, number and uncertainty. File export
success is separate from completion of that user-facing explanation.

`finish` also returns `sources`: the original public URL, publisher, tier,
publication date and retrieval date for each authenticated `source_id`. Use
those links next to the corresponding numbers, policies and recommendations in
the conversation. Source IDs alone are not sufficient citations. Never ask the
family to open internal evidence files to understand the conclusion.

`finish` also returns `delivery`, derived from the authenticated calculation:

```json
{"mode": "profile_only", "evidence_fact_count": 0, "degraded": true}
```

`mode` is `profile_only` when the evidence snapshot has no facts, `partial` when
it has facts but the calculation is degraded, and `evidence_supported` otherwise.
Fact count is not a count of verified eligibility conclusions. Read every actual
fact's state and coverage; even `evidence_supported` is not an admission guarantee.
`delivery` also appears in status after the calculation checkpoint is complete,
not while research remains pending.

All-unavailable is a supported outcome: call the same `finish` after pending is
zero. It returns the full report text, `sources: []`, the truthful research summary
and `profile_only`; an empty evidence bundle does not fabricate a fact. Explain a
preparation version based on the confirmed profile, with useful actions and review
points, while keeping unsupported ranks, school tiers, deadlines and eligibility
unknown. With partial evidence, deliver the supported portions and specific gaps.
Do not ask the family to choose between repairing the machine and receiving an
unsupported expert estimate. Keep both repeated technical actions and audit detail
inside the host; follow the conversation guide for a readable, complete answer.

## Complete normalized twenty-answer file

The host collects answers through the one-question-at-a-time conversation in
SKILL.md, saving the draft and next pending item privately after each user reply.
Only after every topic and subitem is answered or explicitly skipped does the
host normalize the accumulated explicit meanings under keys `1` through `20`.
A complete numbered document volunteered by the user can optionally be segmented
with `parse_numbered_questionnaire`; conversational replies need no numbering.
Explicitly unknown or skipped values stay `null`, `unknown` or empty, while
unasked items remain pending. Confirm the resulting profile before `start`.
This valid sample shows the complete metadata shape, not values to copy into a
different student's profile:

```json
{
  "1": "不便回答",
  "2": "湖北",
  "3": {"city": "武汉", "high_school": "武汉市示例中学"},
  "4": {"grade": "高二", "exam_year": 2028},
  "5": "重点班",
  "6": {"mode": "3+1+2", "primary": "历史", "secondary": ["政治", "地理"], "score_basis": "原始分"},
  "7": {"date": "2026-06-01", "scope": "school", "score": 610, "max_score": 750, "source": "school_report"},
  "8": {
    "rank": 120,
    "cohort_size": 1000,
    "additional_observations": [
      {"scope": "province_joint", "rank": 18200, "cohort_size": 210000, "source": "joint_exam_report"}
    ]
  },
  "9": {"best_rank": 80, "usual_rank": 140},
  "10": {"subject_strengths": [], "awards": ["示例学科奖项"]},
  "11": {"research_experiences": [], "activities": ["示例志愿活动"]},
  "12": ["示例甲大学"],
  "13": ["专业实力强"],
  "14": ["历史学"],
  "15": ["自己感兴趣"],
  "16": {"targets": ["武汉"], "excluded": []},
  "17": "postgraduate",
  "18": ["院校定位", "多元路径"],
  "19": ["院校范围", "多元路径", "当前行动"],
  "20": {
    "budget": "moderate",
    "institution_types": ["public"],
    "service": "reject",
    "adjustment": "consider",
    "risk": "balanced",
    "health": [],
    "school_vs_major": "balanced",
    "pathways": {
      "strong_foundation": "interested",
      "comprehensive_evaluation": "interested",
      "special_program": "unknown",
      "service_oriented": "unknown",
      "uniformed_service": "not_applicable",
      "cross_border": "unknown",
      "arts_sports": "not_applicable"
    },
    "eligibility": ["完成高考报名"],
    "readiness": {"english_readiness": "unknown", "interview_readiness": "unknown", "physical_readiness": "unknown"}
  }
}
```

If question 8 has no explicit joint-exam observation, omit
`additional_observations`. Do not derive readiness, strengths or research from
subjects and activities. Unknown score/rank values may be `null`; the four
question-7/8 numeric values are omitted from `rank_observations` only when all are
null.

The question-7 `scope` describes the real exam, not who stamped its report.
School monthly exams, school term exams and school mock exams stay `school`;
explicit province/city joint exams use `province_joint` / `city_joint`.
`province_official` is only for the student's actual formal provincial gaokao
result. A 750-point maximum, an official-looking school report or a need to make
calculation succeed never changes that scope. Unclear exam scope remains pending
clarification while independent research continues.

## Submission envelope and source metadata

Every submission has `sources`. Non-pathway tasks also have `records`; each
`rows` list selects one zero-based extracted row per source. Pathway tasks instead
use each source's `options.field_map`. The facade calculates `content_hash` from
the saved bytes, so omit it from host metadata unless independently computed and
exactly equal.

Each `candidate` contains all other `SourceCandidate` metadata:

```json
{
  "source_id": "stable-public-id",
  "url": "https://publisher.example.edu.cn/public-page",
  "publisher": "公开发布机构",
  "tier": "A",
  "published_at": "2026-06-25",
  "retrieved_at": "2026-09-06T08:00:00Z",
  "citation_root": "https://publisher.example.edu.cn/",
  "summary": "公开材料的简短匿名说明"
}
```

Use the source-policy tier derived from the actual publisher. `published_at` may
be `null`; `retrieved_at`, canonical URL, publisher and citation root remain
required provenance. One source ID always refers to the same saved material.

## HTML submission

This complete score-table submission selects the first data row. `columns` maps
canonical extraction fields to exact page headers; `roles` and `score_scale`
activate numeric validation.

```json
{
  "sources": [
    {
      "path": "<private-workspace>/sources/score-2026.html",
      "adapter": "html",
      "candidate": {
        "source_id": "score-table-2026",
        "url": "https://eea.example.gov.cn/score/2026.html",
        "publisher": "示例教育考试院",
        "tier": "A",
        "published_at": "2026-06-25",
        "retrieved_at": "2026-09-06T08:00:00Z",
        "citation_root": "https://eea.example.gov.cn/",
        "summary": "2026 一分一段公开表"
      },
      "options": {
        "table_index": 1,
        "caption": null,
        "columns": {"score": "分数", "cumulative_count": "累计人数"},
        "roles": {"score": "score", "cumulative_count": "rank"},
        "score_scale": [0, 750]
      }
    }
  ],
  "records": [{"rows": [0], "coverage_status": "official"}]
}
```

## XLSX submission

This complete admission-row submission maps exact worksheet headers. The facade
adds the task's canonical year, province, subject group and empty remarks before
building the validated admission row.

```json
{
  "sources": [
    {
      "path": "<private-workspace>/sources/admission-2026.xlsx",
      "adapter": "xlsx",
      "candidate": {
        "source_id": "admission-2026",
        "url": "https://eea.example.gov.cn/admission/2026.xlsx",
        "publisher": "示例教育考试院",
        "tier": "A",
        "published_at": "2026-07-20",
        "retrieved_at": "2026-09-06T08:00:00Z",
        "citation_root": "https://eea.example.gov.cn/",
        "summary": "2026 普通批投档公开表"
      },
      "options": {
        "sheet": "普通批",
        "columns": {
          "school_code": "院校代码",
          "school_name": "院校名称",
          "program_group": "专业组",
          "min_score": "最低分",
          "min_rank": "最低位次"
        },
        "roles": {"min_score": "score", "min_rank": "rank"},
        "score_scale": [0, 750]
      }
    }
  ],
  "records": [{"rows": [0], "coverage_status": "official"}]
}
```

## Legacy XLS submission

For an actual legacy workbook, use `adapter: "xls"` and the original `.xls` path.
The `sheet`, `columns`, `roles`, `score_scale` and `records` fields are the same as
the XLSX submission above. The facade calls
`scripts.adapters.xls.extract_xls(path, sheet=..., mapping=...)`, records
`xls-worksheet` and hashes the original bytes. The optional reader is `xlrd`;
XLSX continues to use `openpyxl`. Hidden, merged, formula and error cells are not
promoted to exact values. Never rename XLS to XLSX or rewrite it as a different
file to make the evidence appear supported. Missing readers return exit `3` and
retain the checkpoint, so the host can use another readable source or close only
the affected tasks.

## PDF policy-text submission

Use `adapter: "pdf_text"` for a saved original `.pdf` and one of the pathway
task kinds: `strong_foundation`, `comprehensive_evaluation`, `hk_macao_admission`
or `special_pathway`. The facade calls `extract_pdf_text`; its available parser
records `pdfplumber-text` or `pypdf-text`, retaining page numbers and warnings.
It does not perform OCR on an image-only page.

Inspect the actual normalized page text before selecting fields. Each
`options.field_map` value is `[one_based_page_number, exact_supporting_text]`.
For example, the options for a real page that contains those two unique strings
could be:

```json
{
  "field_map": {
    "institution": [1, "示例大学"],
    "year": [1, "2026"]
  }
}
```

Use the full source metadata envelope above, omit absent fields and do not provide
`records` for these pathway tasks. Partial field maps retain missing conditions;
an absent or ambiguous quote cannot establish a value. Do not fill unknown fees,
qualifications or language requirements from memory. This prose adapter cannot
stand in for a numeric score/admission table.

## PDF integer-table submission

Use `adapter: "pdf_table"` only for an unambiguous integer table in the actual
output of `extract_pdf_text`. It accepts exactly one page, an explicit header line
and an inclusive range of data lines. Page and line numbers are one-based; the
submission's `records[].rows` indexes remain zero-based extracted rows. Example
options for a previously inspected, matching region are:

```json
{
  "columns": {"score": "分数", "cumulative_count": "累计人数"},
  "roles": {"score": "score", "cumulative_count": "rank"},
  "score_scale": [0, 750],
  "headers": ["分数", "人数", "累计人数"],
  "page_number": 1,
  "header_line": 2,
  "first_data_line": 3,
  "last_data_line": 20,
  "column_group": 1,
  "caption": null
}
```

The facade calls `extract_pdf_table(path, mapping=..., headers=..., page_number=...,
header_line=..., first_data_line=..., last_data_line=..., column_group=...,
expected_caption=...)`, with `options.caption` passed as `expected_caption`.
It records `pdf-text-table`, the actual parser and original page/line/group
locations. `headers` is one complete ordered group of exact single-token labels;
the physical header may repeat that entire group side by side. `column_group`
selects one group, starting at 1, while every source row must still contain all
physical columns. Every mapped field needs a numeric score/rank role.

The adapter rejects missing/extra columns, masked ranges, noninteger values and
image-only pages. It neither guesses table boundaries nor repairs layout. Its
coverage is only the selected page and range, not the whole PDF or province.
For a genuinely exact row admitted from an official source, the surrounding
submission may use `records: [{"rows": [0], "coverage_status": "official"}]`, as
in the HTML example. This record state does not declare the entire PDF extracted:
the adapter's explicit score/rank bounds and page/line selection retain that
separate limit. Do not set `partial` merely because a verified region is a subset;
the rank bridge rejects a non-consumable record state. Conversely, never promote
uncertain cells or an unqualified source to `official` to make ingestion pass.
The largest cumulative count in an excerpt is not the province's total cohort.
Inspect each source with the active parser before reusing line selections; a
different parser may change the layout. Complex admission tables with school names
need an appropriate HTML/XLS/XLSX source or genuinely verified visual extraction.
No converted prose, imagined OCR or guessed columns may be labeled exact.

## OCR-row submission

Use `ocr_rows` when the public source is an image or image-only PDF and the host
can produce the normalized OCR JSON accepted by `normalize_ocr_rows`. `path`
always names the downloaded original public image/PDF whose bytes bind the
candidate `content_hash`; `options.ocr_path` names the separate absolute,
host-owned normalized JSON. The facade fixes `min_exact_confidence` at 0.95 and
validates page/image/bbox cells plus spatial verification anchors. Low confidence,
cropped, partial-page, or invalid-anchor material cannot become exact evidence.

```json
{
  "sources": [
    {
      "path": "<private-workspace>/sources/score-2026.png",
      "adapter": "ocr_rows",
      "candidate": {
        "source_id": "score-image-2026",
        "url": "https://eea.example.gov.cn/score/2026.png",
        "publisher": "示例教育考试院",
        "tier": "A",
        "published_at": "2026-06-25",
        "retrieved_at": "2026-09-06T08:00:00Z",
        "citation_root": "https://eea.example.gov.cn/",
        "summary": "2026 一分一段公开图片"
      },
      "options": {
        "ocr_path": "<private-workspace>/normalized/score-2026.ocr.json",
        "columns": {"score": "分数", "cumulative_count": "累计人数"},
        "roles": {"score": "score", "cumulative_count": "rank"},
        "score_scale": [0, 750]
      }
    }
  ],
  "records": [{"rows": [0], "coverage_status": "official"}]
}
```

## Public-text submission

Use `public_text` for saved UTF-8 prose such as an HTML page's visible text.
Every non-null typed value has an exact supporting `quote`. A unique quote needs
no offsets; repeated prose requires zero-based `start` and exclusive `end`, and
the slice must equal the quote. Numeric values and list items must occur in the
quote. The facade reads with UTF-8-sig and normalizes CRLF and CR to LF before
binding fields, so compute every span against that normalized text. The candidate
hash still covers the original saved bytes. `field_map` maps pathway canonical
names to arbitrary observed names.

```json
{
  "sources": [
    {
      "path": "<private-workspace>/sources/pathway-2026.txt",
      "adapter": "public_text",
      "candidate": {
        "source_id": "pathway-policy-2026",
        "url": "https://university.example.edu.cn/admission/pathway-2026.html",
        "publisher": "示例大学招生办公室",
        "tier": "A",
        "published_at": "2026-04-10",
        "retrieved_at": "2026-09-06T08:00:00Z",
        "citation_root": "https://university.example.edu.cn/admission/",
        "summary": "2026 强基计划公开简章正文"
      },
      "options": {
        "fields": {
          "school": {"value": "示例大学", "quote": "招生学校：示例大学"},
          "region": {"value": "湖北", "quote": "面向湖北考生"},
          "mode": {"value": "3+1+2", "quote": "适用3+1+2模式"},
          "policy_year": {"value": 2026, "quote": "2026年强基计划"},
          "eligibility": {"value": ["完成高考报名"], "quote": "申请人须完成高考报名"},
          "majors": {"value": ["历史学", "哲学"], "quote": "招生专业为历史学、哲学"}
        },
        "field_map": {
          "institution": "school",
          "province": "region",
          "subject_mode": "mode",
          "year": "policy_year",
          "eligibility_requirements": "eligibility",
          "professional_options": "majors"
        }
      }
    }
  ]
}
```

Omit fields that the page does not state and omit their `field_map` entries. The
adapter writes them as source-bound missing values, so the pathway policy remains
partial. Use `{"value": null, "status": "uncertain", "quote": "..."}` only
when prose exists but cannot support an exact semantic value. Never write a quote
for absent material or turn a missing field into affirmative prose.

## Year fallback

Treat the year on each returned task as authoritative. For every data family,
try `Y`, then `Y-1`, `Y-2`, and `Y-3` only through the separate tasks returned by
`next`. If `Y` is unavailable, record that task with a reason such as
`current_year_not_published`, call `next`, and ingest the next comparable year
with its real `year` field or row. Once a newer comparable task is completed,
close each older pending task in that family with
`--reason newer_comparable_year_accepted --newer-task <completed-task-id>`.
The receipt proves the newer task; there is no caller-authored or automatic skip.

Each family falls back independently. Retain a current-year third-party source as
current reference and the previous-year official source as historical baseline
when both are useful. Stop numeric aggregation when policy or measurement changes
make years incomparable, and record the unavailable reason. The facade preserves
the selected task year, evidence status, source provenance and coverage in every
checkpoint.
