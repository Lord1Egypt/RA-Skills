# Built-in course pathways

Read this when the learner names a course or reference, asks what is included, or has no learning direction during installation or first use. The [catalog](course-catalog.json) contains 53 university courses, 12 AI organization courses and two open references. The learner chooses the language of the plan and lessons independently of the source language.

## Discover and choose

The agent handles this through ordinary chat; commands are internal helpers, not learner homework:

```sh
python scripts/omni_learning.py courses welcome
python scripts/omni_learning.py courses list
python scripts/omni_learning.py courses search --query '我想学习哈佛积极心理学'
python scripts/omni_learning.py courses show --id harvard-positive-psychology
```

If installation just finished or this is the first invocation and no topic is known, briefly explain the available routes and offer 3–5 varied choices in the learner's language. Offer the full list or any other subject. Use suitable native choice cards when available, otherwise chat. Show this once in the current interaction; do not repeat it, interrupt an existing course, infer a choice from silence, or launch a new conversation/job. A Skill cannot independently run a welcome screen when its host has no install callback. An explicit course/topic goes directly to matching/intake, without a promotional detour.

`search` is conservative alias retrieval, not semantic proof. Interpret the request as an agent, inspect candidates and preserve institution/teacher/edition. A broad “幸福课”, an unknown course, conflicting institution or a different year needs clarification or explicit research; do not force it into the nearest built-in entry. Ask only what changes the course, reusing already supplied settings. An unmatched course may still be researched as a custom course; never advertise it as built in before verification.

## Establish the original-course evidence

Open the selected original source and the relevant lecture/reading material before writing teaching content. Catalog dates document the catalog audit, not fresh source access for a lesson. At actual generation, record fresh checked dates and source metadata as usual. If a link fails, try another actual official/university archive source or the learner's authorized copy; disclose the gap. Do not silently substitute a modern edition, a different professor, a similarly named paid course or an unofficial video reupload.

Read `provider_type`, `source_access` and `original_language` when present. Show relevant access conditions in the learner's language during selection and in the plan. For a registration-gated course or one with only a public outline, offer a clearly labeled outline-based guide using separately verified supplementary sources, or ask for authorized materials if the learner wants to follow the original in detail. Treat public enrollment pages and restricted activities as evidence of course identity and structure. For example, OpenAI Academy's public sequence anchors the course and assessment, while the course itself requires sign-in. Original course completion, assessments and badges follow the provider's rules.

Use `pathway_type` to separate courses from open references when presenting results. For `reference`, agree on chapters or sections and the learner's reading pace. Use the same binding and source checks, choose light practice, and describe the result as an independent reading guide. Public access to the reference text does not grant permission to redistribute third-party images or recordings. In first-aid and law pathways, anchor procedural or legal claims to current applicable primary sources and keep the original course's outline separate from those updates.

In particular, `harvard-positive-psychology` is Tal Ben-Shahar's **Spring 2006 PSY 1504 syllabus**, hosted by Penn's Positive Psychology Center. That syllabus establishes topic order and original assessment rhythm; it does not establish lecture transcripts, a professor's exact examples, or every assigned reading. Its original outline is not the widely circulated later video sequence or Harvard Health/Arthur Brooks courses. State the scope and request original materials if precise lecture-specific treatment is required. Otherwise offer independent original explanations anchored to the verified syllabus and clearly identified supplementary primary sources.

Catalog `units` are **editorial groups of original sessions**. Their locators show which original dates, weeks or lectures are included; a grouped unit is not necessarily one original lecture. Explain prerequisites from the original course separately from the learner's background. For advanced courses, offer prerequisite preparation with approval; do not silently turn CS229 into a beginner no-math course.

## Bind the chosen version and scope

```sh
python scripts/omni_learning.py courses bind --id harvard-positive-psychology
python scripts/omni_learning.py courses bind --id mit-linear-algebra --unit u01 --unit u02 --pace adapted --practice light
```

Copy the returned object into `config.json.course_pathway`. It contains a full course snapshot, SHA256, selected ordered unit IDs, pacing and practice choices. `unit_ids` defaults to all groups; a shorter taster must explicitly select fewer. In `plan.json.days`, add `course_units: ["u01"]` (or the actual consecutive mapped IDs) to every day. Units may repeat while being split across days; they must not move backwards, disappear or introduce unselected groups. A lesson repeats its approved day's `course_units` field.

Use `adapted` by default. Keep original order and pedagogical progression, split the relevant original sessions into manageable parts, and explicitly show the mapping and what the selected duration does/does not cover. Original lecture, reading and assignment workloads remain visible in the proposal. Do not promise full course equivalence for a 10-minute daily guide. `original_units` is a follow-along mode with one **catalog group** per day; it still is not the original academic calendar or workload. To follow the exact original session timetable, show the individual session locators and agree the required time; use an appropriately split `adapted` plan and describe the correspondence explicitly.

`light` retains the existing learner-started 1–3 choice/short-answer/discussion checks. A coding course name alone does not authorize extensive programming exercises. `original_assignments` requires the learner's explicit choice, sufficient time, actual permitted source access and the original course's academic honesty rules. Never automate assessed submissions, generate unasked answer keys, or imply enrollment, grading or credit.

Run `courses check --config /actual/config.json --plan /actual/plan.json` before initialization. It validates structure/order/selected coverage, not teaching fidelity, source access, consent or mastery. The usual actual user plan approval remains required.

## Original sources and rendering

Course mode requires at least one original-course source bound to the configured snapshot and covering the document's mapped units. Existing source fields remain `id: S1`, `title`, `url`, `publisher`, `note`, `published_at`, and fresh `checked_at`. Include `course_ref`:

```json
{"course_id":"harvard-positive-psychology","sha256":"ACTUAL_SNAPSHOT_SHA256","source_id":"O1","unit_ids":["u01"]}
```

Use the actual binding SHA and source ID; `omni_courses.source_ref(binding, source_id, unit_ids)` constructs it. The source URL must equal that original source's stored URL. Source references cover all selected groups for a plan, or just the day's groups for a lesson. Add real lecture/reading sources for substantive claims and distinguish independent examples and supplements. A syllabus citation is evidence for the outline, not proof that it supports every teaching claim. Do not force five unrelated expansion links into course mode. Original sources and their locators remain visible in all exported formats; renderers prepend localized scope/pacing disclosure without changing canonical input files.

If the learner also selected personal materials, their existing source policy and evidence checks still apply. Do not introduce unapproved external supplements under a strict material policy. The same source may carry both valid material and course references when its provenance actually supports both.

The snapshot is validated independently of the current installed catalog. Existing approved courses retain their selected edition, source locators and plan; a catalog upgrade cannot retarget them. Choose another course/scope/edition through the existing new-course-version review flow. Never overwrite an active course, approval, quiz history or saved delivery destination.
