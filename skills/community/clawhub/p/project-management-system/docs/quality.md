# Quality Assurance Mechanism

> Quality gates, review standards, verification process, iteration closed loop.
> Core concept: **Quality is a pipeline, not a checkpoint.**

---

## Forced Structured Intermediate Output

_Source: MetaGPT — "Each phase must have standard-compliant output to continue"_

**Problem:** If intermediate output has no structured standard, errors will amplify along the pipeline (hallucination propagation).

**Rule: Each phase has clear output standard, not meeting standard cannot enter next phase.**

| Phase | Required Output | Output Standard | Checker |
|------|---------|---------|--------|
| Initiate project | brief.md | Goal, scope, roles, milestones all filled | Decision Maker |
| Break down | task-spec (all) | Acceptance criteria quantified, dependencies marked, input/output clear | Dispatcher self-check |
| Execute | Output file | At task-spec specified location, format meets requirements | Executor self-check |
| Review | review-record | Item-by-item against acceptance criteria, has conclusion | Dispatcher / Verifier |
| Acceptance | final-report | All tasks accepted, lessons learned filled | Decision Maker |

**Phase Gate:** Previous phase output doesn't meet standard → Cannot start next phase. This is hard constraint, not suggestion.

## Independent Verification Role

_Source: Quality Gate Pipeline — "Verification agent and development agent separation"_

**Problem:** Executor checking their own output has blind spots.

**Rule: Important tasks must be verified by non-executor.**

| Task Importance | Verification Method |
|-----------|---------|
| Low (Simple modification, format adjustment) | Dispatcher direct review |
| Medium (Standard development, research) | Dispatcher review + spot check |
| High (Core functionality, architecture change, data processing) | **Independent Verifier** review |

**Independent Verifier Requirements:**
- Not the person who executed this task
- Only gets output file and acceptance criteria (black-box verification)
- Doesn't need to understand execution process
- Verification result recorded in review-record

**How to Find Independent Verifier:**
- Another agent / subagent
- Another executor
- Decision Maker themselves
- Key is "not the executor themselves"

**Independent Verification Operation Process:**

1. Dispatcher decides need independent verification → Write a verification task's task-spec (can be simplified)
2. Verification task-spec's "Input" only gives two things: **Output file path** + **Original task's acceptance criteria**
3. Verification task-spec's "Acceptance Criteria" is: Item-by-item check against original task acceptance criteria, output review-record
4. Dispatch message uses Ask format, with additional note: "This is a verification task, you don't need to understand execution process, just check output against criteria"
5. Verifier submits review-record → Dispatcher decides pass/rework based on conclusion

**Simplified Verification (Small Tasks):** If task itself is small, acceptance criteria ≤3 items, can skip writing verification task-spec, directly write output path and acceptance criteria in Ask message for verifier to check.

**Anti-Laziness Iron Rule (Written into verification task spec):**
1. Specific criteria — Don't say "ensure it runs", say "run complete tests and report all failures"
2. Comprehensive check — Force coverage of edge cases
3. Reverse testing — Input data that should fail, confirm system actually reports error
4. Explicit instructions — "Must check all acceptance criteria item by item to mark as passed"

## Quality Gate

Task from "Pending Review" to "Accepted", **must have review record** (review-record).

| Phase | Gate | Pass Condition |
|------|------|----------|
| Initiate project → Break down | Requirement confirmation gate | Decision Maker confirms requirements, explicitly says "can start" |
| In execution | Intermediate output gate | User confirmation points all passed (if any)|
| Pending Review → Accepted | Review gate | Review record exists and conclusion is "pass" |
| Project acceptance | Final gate | All tasks accepted + Decision Maker decision |

Skipping review requires Decision Maker explicit exemption (note in task-spec status tracking).

## Acceptance Criteria Measurability

When writing acceptance criteria, try to quantify:
- ❌ "Output format clear" → ✅ "JSON format, contains name/value/timestamp fields"
- ❌ "Good performance" → ✅ "Response time < 2 seconds"
- ❌ "High code quality" → ✅ "No syntax errors, has exception handling, key functions have comments"

Unquantifiable criteria (aesthetics, style, etc.) → Mark as "User Confirmation Point", judged by Decision Maker.

## Task Type Adaptation

Different task types have different review focus:

| Task Type | Example | Review Focus |
|----------|------|----------|
| Code development | Build project, write features, fix bugs | Functionality completeness, code quality, test coverage |
| Research search | Market research, competitive analysis | Information accuracy, coverage, conclusion reliability |
| Data collection | Crawling, monitoring, information gathering | Data completeness, format compliance, deduplication |
| Workflow creation | Automation, scripts, scheduled tasks | Reliability, exception handling, maintainability |
| Content creation | Documentation, PPT, video scripts | Content quality, layout, audience adaptation |
| Design/UI | Interface, interaction, visual | Aesthetics, consistency, usability |
| System operations | Configuration, deployment, monitoring | Security, stability, rollback capability |

_When reviewing, choose appropriate scoring dimensions based on task type._

## Automated Verification

For outputs that can be automatically verified, prioritize tool verification:

| Output Type | Automated Verification Method |
|----------|-------------|
| Code/scripts | Actually run, check output |
| Web/UI | Use browser tool to screenshot, click test |
| Data files | Check row count, format, sample verification |
| API/interface | Send request to verify return value |
| Documentation | Check structural completeness, link validity |

_Automated verification doesn't replace manual review, but can discover obvious problems earlier._

## Delivery Verification

First step before review: Verify output file exists at spec-specified location.
- File doesn't exist → Don't start review, feedback directly
- File exists but format wrong → Record in review record

## Evaluation Optimization Loop

Rework is standard closed-loop iteration: Generate → Evaluate → Optimize → Re-evaluate.

- Each rework is an iteration round, review record marks round number
- Each round records: Which round, previous round feedback, what changed this round, what's still missing
- **Exceed 3 rounds escalate** — Provide 3 rounds of improvement records, stuck reason, alternative plan suggestion

## After Rework Failure Change Plan

Still not meeting standard after 3 rounds, after escalation decide to change plan:

1. Current task marked as "Abandoned", record reason
2. Create replacement task TASK-XXX-v2, reference original task
3. Explain: Why original plan failed, what is new plan
4. Can change executor, tool, implementation method
5. Original task record preserved, as experience reference

## Handling Accepted Tasks After Change

- **Small change (≤30% work):** Reopen old task, modify and re-review
- **Large change (>30%):** Create new task, old task stays accepted
