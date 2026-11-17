# Assessment schema and agent commands

`OMNI` means the installed `python .../scripts/omni_learning.py --project /absolute/course`. These are agent operations. Data stays under course/learning, never the installed bundle. No quiz command schedules jobs, sends notifications or changes delivery state.

## Definition

```json
{
  "key": "Day01", "revision": 1, "estimated_minutes": 3,
  "questions": [{
    "id": "q1", "kind": "choice", "prompt": "Which option is supported by the lesson?",
    "objective": "Distinguish evidence from an unsupported assertion",
    "response_hint": "Choose one option; a short explanation is optional.",
    "actions": ["select"],
    "source_refs": [{"source_id":"S1","section_index":0,"quote":"EXACT TEXT FROM THE ACTUAL LESSON"}],
    "hints": ["Compare each claim with the cited passage."],
    "explanation": "AUTHOR A SOURCE-SUPPORTED EXPLANATION [S1]",
    "options": [
      {"id":"evidence","text":"FIRST DISPLAYED OPTION","feedback":"PRIVATE OPTION EXPLANATION"},
      {"id":"assertion","text":"SECOND DISPLAYED OPTION","feedback":"PRIVATE OPTION EXPLANATION"}
    ], "answer_id":"evidence"
  }]
}
```

Replace illustrative text with actual authored content. Use 1–3 questions per round. Default estimated time is 1–5 minutes. `kind` is `choice`, `short` or `open`; short/open replace `options` and `answer_id` with `expected_answer` text and `rubric:[{"id":"criterion1","description":"Observable required point"}]`. Empty hints are valid. Question/option/criterion IDs are stable, letter-led and use letters/digits/underscore/hyphen/dot. Choice options have unique normalized text and IDs; answer_id is an option ID, never a displayed letter.

Light actions: `select`, `brief_text`, `conversation`. Heavy actions: `long_writing`, `operate_device`, `write_code`, `experiment`, `project`. Heavy/longer checks require the top-level nonempty `practice_request` quoting the learner's actual explicit practical-training request. This is a recorded host attestation, not automatic permission verification. Accurate semantic effort classification is required.

Each source anchor must name an existing lesson source, a zero-based section index, and a quote actually in that section alongside its citation. This anchors to course teaching text, not a claim that a web passage has been freshly fetched. The host must check that the source supports the question/answer. The frozen definition binds config, plan, reviewed manifest and lesson input hashes. `prepare` may precede publication; `start` requires verified lesson delivery. Repeated identical preparation is idempotent; changed content needs a higher revision. Source/config changes block assessment actions, preserving old records for export/recovery.

## Commands

```sh
OMNI quiz prepare --input /private/Day01-quiz.json
# Only on the learner's actual request; --extra-time only after disclosed extra-time consent:
OMNI quiz start --key Day01 --request-id user-message-1 --consent 'Finished reading; test me'
OMNI quiz next --attempt ACTUAL_ATTEMPT_ID
OMNI quiz answer --attempt ACTUAL_ATTEMPT_ID --question q1 --event-id user-message-2 --input /private/answer.json
OMNI quiz hint --attempt ACTUAL_ATTEMPT_ID --question q1 --event-id hint-request
OMNI quiz reveal --attempt ACTUAL_ATTEMPT_ID --question q1 --event-id solution-request
OMNI quiz skip --attempt ACTUAL_ATTEMPT_ID --question q1 --event-id skip-request
OMNI quiz pause --attempt ACTUAL_ATTEMPT_ID --event-id later-request
# Resume through start with a new actual request ID; it keeps the active attempt.
OMNI quiz status
OMNI quiz export --output /private/my-answers.json --format json
OMNI quiz export --output /private/my-answers.csv --format csv
# Only when the learner explicitly requests removal:
OMNI quiz forget --confirm --scope attempts
```

Answers: `{"choice_id":"evidence"}` or `{"text":"A"}` for choice, `{"text":"My original response"}` for text/dialogue. Full-width letters and exact normalized option text are supported. Prefer canonical IDs for card submissions. Do not infer an ambiguous free-form selection; ask. Keep original explanation in `text` alongside choice_id if supplied. A further explicit answer after grading uses `quiz answer ... --revise`; earlier text remains. A finished retake uses `quiz start ... --new-attempt` and a new stable request ID.

For short/open pending answers, the host receives private grading context and writes:

```json
{
 "criteria":[{"id":"criterion1","result":"met","note":"Explain the correspondence to the actual answer."}],
 "strengths":["An observed strength"], "gaps":[],
 "explanation":"Grounded feedback [S1]", "source_ids":["S1"],
 "next_step":"One small review or follow-up suggestion"
}
```

```sh
OMNI quiz feedback --attempt ACTUAL_ATTEMPT_ID --question q1 --event-id grade-event --answer-id ACTUAL_LATEST_ANSWER_ID --input /private/feedback.json
OMNI quiz correct --attempt ACTUAL_ATTEMPT_ID --question q1 --event-id correction-event --replaces ACTUAL_LATEST_GRADE_ID --reason-file /private/dispute.txt --input /private/corrected-feedback.json
```

Every frozen criterion is covered once: `met`, `partly_met`, `not_met` or `uncertain`. Verdict derives from those judgments: all met → correct; all not_met → incorrect; any uncertain → needs_review; otherwise partial. Strengths/gaps may be empty; source_ids must reference the question's anchors. No `score` field. A choice correction instead supplies `verdict: "withdrawn"` or `"needs_review"` and the same explanation/strengths/gaps/source_ids/next_step fields, without criteria. A choice's original automatic grade ID is its answer event ID.

Use stable IDs on retry; conflicting reuse is rejected. Missing/failed feedback never discards a raw answer. Pause and skip produce no failure grade. `next` returns only the current public question before response; private grading context appears only after an actual answer. Do not copy private tool output wholesale into a learner card.
