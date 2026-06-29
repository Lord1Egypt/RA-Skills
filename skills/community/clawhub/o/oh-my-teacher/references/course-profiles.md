# Course Profiles

Build a course profile before major review work. If the user provided enough clues, infer silently and state assumptions briefly.

## Snapshot Template

Maintain and update a compact snapshot across turns. Show it at the start of major tasks (`/materials`, `/diagnose`, `/plan`, `/map`, `/mock`, `/grade`, `/fix`, `/quiz`, `/oral`, `/group-quiz`, `/summary`) unless the same course context is already clear in the current session.

```markdown
## Current Course Snapshot
- **Course**: [name + subject family]
- **Assessment**: [format]
- **Days left**: [N days or unknown]
- **Level**: [beginner / shaky / basic ok / high-score / pass-only]
- **Environment**: [agent-shell / rag-notebook / notes-app / plain-chat / unknown]
- **Materials**: [uploaded sources or gaps]
- **LaTeX**: [rendered / plain-text / not applicable]
- **Weak points**: [tag1, tag2]
- **Completed**: [topics already practiced or mastered this session]
- **Accuracy**: [recent performance, e.g. "7/10 on limits, 3/5 on series"]
- **Last action**: [last command or task]
- **Next recommended**: [one concrete next step]
```

Update rules:

- After `/materials`: refresh **Materials**, knowledge priorities, and **Next recommended**
- After `/diagnose`: write ranked weak-point results to **Weak points** and **Accuracy**, calibrate **Level**, set **Last action**, update **Next recommended**
- After `/grade`, `/mock`, `/quiz`, or `/fix`: append or refine **Weak points**, update **Completed** and **Accuracy**, set **Last action**, update **Next recommended**
- After `/oral`: same as `/quiz`; additionally note confidence and structure quality in **Accuracy**
- After `/group-quiz`: aggregate per-participant weak points; update active student's **Weak points** and **Accuracy**
- After `/summary`: consolidate session topics into **Completed**, refresh **Accuracy** summary, set **Last action** to `/summary`, update **Next recommended**
- After `/profile` or new course info: rebuild the full snapshot; set **Level** from user declaration (high-score / pass-only are goals, not performance metrics)
- After environment detection or a clear environment change: refresh **Environment** using `references/environment-adaptation.md`
- For mathematics courses, ask at session start which LaTeX rendering the user needs (rendered / plain-text); set **LaTeX** accordingly
- Keep **Weak points** short: topic labels, not paragraphs

## Required Fields

- Course name and subject family
- Assessment format: paper exam, lab exam, coding/on-machine exam, oral exam, open-book, closed-book, course project, mixed assessment
- Course nature: theoretical proof, computation/application, programming practice, lab operation, memorization/essay, case analysis
- User level: beginner, learned but shaky, can solve basic problems, high-score target, pass-only target
  - **Note**: `pass-only` and `high-score` are user-declared goals (set during `/profile`), not inferred from performance. They override performance-based level assignments.
- Constraints: exam date, daily available time, target score, materials available, past papers, teacher emphasis

## Paper Exam Optimization

Use when the assessment is written, closed-book/open-book, or likely traditional final exam.

Prioritize:

- Exam map: chapters, weights, likely question types
- Definitions, theorem conditions, formulas, templates, standard steps
- Timed drills, mock papers, answer rubrics
- Last-page review sheet for final 30 minutes
- Common traps and scoring opportunities

For open-book exams, emphasize navigation, index pages, problem-solving templates, and avoiding time lost searching materials.

## Lab Exam Optimization

Use when the assessment involves experiments, operation, reports, practical demonstrations, or lab viva.

Prioritize:

- Experiment principle and what variable each step controls
- Instrument setup, operation sequence, safety/handling notes
- Data recording table, calculation workflow, uncertainty/error analysis
- Common failed operations and how to recover
- Lab report structure and oral defense questions

Subject-specific lab emphasis:

- Chemistry: reagents, reaction mechanism, color/phase observations, safety, contamination, yield/error.
- Biology/medicine: sample handling, staining/assay steps, controls, observation criteria, contamination, interpretation.
- Physics/electronics: circuit/setup diagram, calibration, measurement range, uncertainty, graph fitting, units.
- Computer labs: environment setup, input/output format, test cases, debugging checklist, edge cases.

## Coding or On-Machine Exam

Prioritize:

- Known language subset and allowed libraries
- Common input/output patterns
- Boundary cases, time complexity, debugging and test construction
- Small runnable examples before large solutions
- Exam scoring: partial credit for algorithm idea, data structure, correctness, and complexity

## Oral Exam

Prioritize:

- Short explainable definitions and examples
- Progressive questioning: basic, application, edge case, comparison
- Response templates: "definition -> condition -> example -> common pitfall"
- Confidence repair through short repeated answers

## Unknown Course

Ask at most these three questions:

1. What course and assessment format is this?
2. How much time remains and what score goal do you have?
3. What is currently hardest: concepts, proofs, calculations, coding, experiments, or memorization?

## Snapshot On-Disk Format

In agent shells, prefer `scripts/snapshot.py` for deterministic save/load/list/set-active operations instead of hand-rolling snapshot paths. Use the Markdown snapshot format below as the content passed to the script.

The script also maintains `.oh-my-teacher/state.json` in agent shells. Treat the Markdown snapshot as the human-facing format and `state.json` as the machine-readable state for scripts and future automation.

When persisting the Current Course Snapshot to `.oh-my-teacher/snapshot.md` (agent shell) or as a copyable block (plain chat), use the exact Markdown format below. The LLM must parse and write this structure byte-for-byte — do not add extra headings, YAML front matter, or narrative text outside the fenced block.

```markdown
## Current Course Snapshot
- **Course**: 数据结构与算法 / Computer Science
- **Assessment**: 机考（闭卷，2小时，OJ自动评测）
- **Days left**: 7
- **Level**: shaky
- **Environment**: agent-shell
- **Materials**: 课件PPT（12章全）、实验报告x4、往年OJ题库x3套
- **LaTeX**: not applicable
- **Weak points**: [图论-Dijkstra堆优化, 动态规划-状态设计]
- **Completed**: [线性表, 栈与队列, 二叉树遍历]
- **Accuracy**: "排序 8/10, 图最短路 4/10, DP 2/5"
- **Last action**: /fix on Dijkstra with negative-weight confusion
- **Next recommended**: /quiz on DP state design
```

File naming convention for single-course mode:

- Write to `.oh-my-teacher/snapshot.md` in the workspace root.
- Preferred helper: `python scripts/snapshot.py save < snapshot.md` and `python scripts/snapshot.py load`.
- To inspect machine-readable state, use `python scripts/snapshot.py load --json`.
- On session start, read this file and confirm with the user before continuing.
- After `/profile`, `/materials`, `/diagnose`, `/plan`, `/grade`, `/mock`, `/quiz`, `/fix`, `/oral`, `/group-quiz`, or `/summary`, overwrite the file with the updated snapshot.

For multi-course mode (see Multi-Course Independent Snapshots below), use:

- `.oh-my-teacher/snapshots/<course-slug>.md` per course.
- Keep a `.oh-my-teacher/snapshots/_active` file containing only the slug of the active course.
- Preferred helper: `python scripts/snapshot.py save --course "Course Name" --active < snapshot.md`, `python scripts/snapshot.py load --active`, `python scripts/snapshot.py list`, and `python scripts/snapshot.py set-active --course "Course Name"`.
- Multi-course saves also update `.oh-my-teacher/state.json` with the active slug and parsed snapshot fields.

When reading back a snapshot, parse the bullet fields exactly as written. If a field is missing, leave it blank in the restored snapshot — do not guess.

## Multi-Course Independent Snapshots

When the user is juggling multiple courses, do not discard data from previous courses. Instead, maintain one snapshot file per course under `.oh-my-teacher/snapshots/`.

### Activation

- If `.oh-my-teacher/snapshots/` directory does not exist, create it on first multi-course switch.
- When the user switches to course X, read `.oh-my-teacher/snapshots/<slug>.md` if it exists; otherwise treat it as a new course and build the profile from scratch.
- Write `.oh-my-teacher/snapshots/_active` containing only the slug of the currently active course (no newline, no Markdown).
- The legacy single-file `.oh-my-teacher/snapshot.md` is still supported as the fallback when only one course is in play.

### Slug Convention

`scripts/snapshot.py` provides a `slugify()` helper. The rule is:

- Lowercase, strip non-word Unicode punctuation, replace whitespace/underscores with hyphens, collapse multiple hyphens.
- Unicode letters (including Chinese characters) are preserved — the function does **not** romanize.
- English names stay English; Chinese names stay Chinese (with punctuation stripped).

Examples:

| Course name | `slugify()` output |
|---|---|
| `Data Structures` | `data-structures` |
| `Linear Algebra` | `linear-algebra` |
| `数据结构与算法` | `数据结构与算法` |
| `数学分析` | `数学分析` |
| `操作系统（OS）` | `操作系统os` |

If the user provides an explicit slug via `--slug`, that value is used verbatim and bypasses `slugify()`.

### Snapshot File Content

Each `snapshots/<slug>.md` uses the same format as the single-file snapshot (see Snapshot On-Disk Format above). It is a self-contained record of one course.

### Switching Workflow

1. Detect the switch signal: new course name, new subject family, or user says "切换到XX".
2. Save the current course's snapshot to `snapshots/<old-slug>.md`.
3. Load (or create) `snapshots/<new-slug>.md`.
4. Update `_active` with the new slug.
5. Confirm the switch with the user: "已切换到 [课程名]，之前的 [旧课程] 进度已保存。"
6. Show the new course's snapshot and next recommended action.

### Multi-Course Overview Command

When the user asks for an overview of all tracked courses (e.g., "/plan multi" or "我有哪些课在复习"), scan all `snapshots/*.md` files, extract Course, Days left, Level, and Weak points from each, and present a ranked priority table as shown in the Multi-Course Plan example in `examples/sample-course-profile.md`.
