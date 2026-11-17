# v0.8 Summary-First Prototype Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Test whether a compatible agent can answer common questions from a short file summary and correctly escalate to the full document when the summary is insufficient, without changing Persistent Memory behavior or any personal memory file.

**Architecture:** This is a private, pre-release experiment, not a v0.8 feature release. Four public-safe synthetic Markdown fixtures model stable document shapes: a legacy guide, an event record, a completed course brief, and a completed web project. A Node contract test keeps fixture summaries structurally consistent; a manual two-agent scorecard measures answer accuracy and correct full-text escalation.

**Tech Stack:** Markdown, Node.js built-in `node:test`, Git.

## Global Constraints

- Work in an isolated worktree created from `C:\Users\Yui\.agents\skills\persistent-memory` before implementation.
- Do not read, copy, modify, or commit any file from `C:\Users\Yui\.persistent-memory` during implementation or evaluation.
- Do not use strategic, Web3, Zhiban, Persistent Memory project, course-progress, profile, relationship, or any other active personal memory as a fixture.
- All four fixtures must be newly written, fictionalized, and free of names, contacts, precise locations, credentials, and user-identifying facts.
- Do not modify `SKILL.md`, `SKILL_zh.md`, `README.md`, `README_zh.md`, `CHANGELOG.md`, or release versioning in this experiment.
- Do not claim token savings, automatic section reading, or a v0.8 feature release from this experiment alone.
- A summary query may be answered from `## Summary`; a body-only query must make the agent read the full fixture before answering or explicitly state that the summary is insufficient.

---

## File Structure

- Create: `tests/fixtures/v08-summary-first/legacy-guide.md` — synthetic historical guide, 120+ lines, with a 6-bullet summary and details that are not in the summary.
- Create: `tests/fixtures/v08-summary-first/event-record.md` — synthetic one-time event record, 120+ lines, with a 6-bullet summary and detail-only agenda material.
- Create: `tests/fixtures/v08-summary-first/course-brief.md` — synthetic completed course brief, 120+ lines, with a 6-bullet summary and detail-only rubric material.
- Create: `tests/fixtures/v08-summary-first/completed-web-project.md` — synthetic completed project record, 120+ lines, with a 6-bullet summary and detail-only implementation notes.
- Create: `tests/v08-summary-first-fixtures.test.mjs` — verifies fixture length, summary placement, bullet count, and the presence of a body-only section.
- Create: `docs/experiments/v08-summary-first-prototype.md` — exact controlled prompts, expected facts, scorecard, and promotion gate.
- Create after the manual run: `docs/experiments/v08-summary-first-results.md` — completed scorecard; this records observed results rather than rewriting personal memory.

### Task 1: Create a failing fixture-contract test

**Files:**
- Create: `tests/v08-summary-first-fixtures.test.mjs`
- Test: `tests/v08-summary-first-fixtures.test.mjs`

**Interfaces:**
- Consumes: four UTF-8 fixture files under `tests/fixtures/v08-summary-first/`.
- Produces: `node --test tests/v08-summary-first-fixtures.test.mjs`; each fixture must have a title, a `## Summary` directly after introductory metadata, exactly six summary bullets, at least 120 lines, and a `## Full Details` heading.

- [ ] **Step 1: Write the failing test**

Create `tests/v08-summary-first-fixtures.test.mjs` with this exact code:

```js
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';

const fixtures = [
  'legacy-guide.md',
  'event-record.md',
  'course-brief.md',
  'completed-web-project.md',
];

const readFixture = (name) =>
  readFile(new URL(`./fixtures/v08-summary-first/${name}`, import.meta.url), 'utf8');

const summaryBullets = (text) => {
  const match = text.match(/^## Summary\r?\n([\s\S]*?)(?=^## (?!Summary)|\z)/m);
  assert.ok(match, 'fixture must include a Summary section');
  return match[1].match(/^- .+$/gm) ?? [];
};

for (const name of fixtures) {
  test(`${name} is a long, summary-first synthetic fixture`, async () => {
    const text = await readFixture(name);
    assert.match(text, /^# .+/m);
    assert.match(text, /^## Summary\r?\n/m);
    assert.equal(summaryBullets(text).length, 6);
    assert.match(text, /^## Full Details\r?\n/m);
    assert.ok(text.split(/\r?\n/).length >= 120, 'fixture must be at least 120 lines');
  });
}
```

- [ ] **Step 2: Run the test to verify it fails**

Run:

```powershell
node --test tests/v08-summary-first-fixtures.test.mjs
```

Expected: FAIL with `ENOENT` because no fixture file exists yet.

### Task 2: Add four synthetic, long-form fixtures

**Files:**
- Create: `tests/fixtures/v08-summary-first/legacy-guide.md`
- Create: `tests/fixtures/v08-summary-first/event-record.md`
- Create: `tests/fixtures/v08-summary-first/course-brief.md`
- Create: `tests/fixtures/v08-summary-first/completed-web-project.md`
- Test: `tests/v08-summary-first-fixtures.test.mjs`

**Interfaces:**
- Consumes: the fixture contract from Task 1.
- Produces: four fictional documents with exactly six summary bullets and at least one fact deliberately available only in `## Full Details`.

- [ ] **Step 1: Create the shared fixture shape**

Use this exact heading order in every fixture:

```markdown
# [Fictional document title]

> Status: Historical synthetic fixture for v0.8 testing only.
> Privacy: Contains no personal-memory content.

## Summary

- [Fact 1 needed by the summary query.]
- [Fact 2 needed by the summary query.]
- [Fact 3 needed by the summary query.]
- [Fact 4 needed by the summary query.]
- [Fact 5 needed by the summary query.]
- [Fact 6 needed by the summary query.]

## Full Details
```

- [ ] **Step 2: Fill the four fixtures with the following facts**

| File | Summary-query facts | Body-only fact; keep it out of `## Summary` |
|---|---|---|
| `legacy-guide.md` | The active operating rules live in `CURRENT_RULES.md`; `LEGACY_MEMORY.md` is historical only; the guide is not a current source of truth. | The retired folder name was `daily-scratch/`. |
| `event-record.md` | The event was a one-time planning workshop; its outcome was a three-part follow-up checklist; the record contains incomplete transcript passages. | The second workshop activity lasted 17 minutes. |
| `course-brief.md` | The fictional course used a team project; evaluation emphasized a usable deliverable and evidence of user need; the semester is complete. | The rubric assigns 15% to the process log. |
| `completed-web-project.md` | The fictional project is complete; it used Vite and Three.js; its primary route is `explore`; the public count differs from the confirmed delivery count and must be described as unresolved. | The detail panel used a 240 ms fade transition. |

For every file, write 120 or more lines in `## Full Details` using neutral, fictional paragraphs, tables, and lists. Do not pad with repeated sentences. The full-details material must support the body-only fact and must not contradict the six summary bullets.

- [ ] **Step 3: Run the fixture contract test**

Run:

```powershell
node --test tests/v08-summary-first-fixtures.test.mjs
```

Expected: PASS with 4 tests, one for each fixture.

### Task 3: Add the controlled evaluation protocol

**Files:**
- Create: `docs/experiments/v08-summary-first-prototype.md`
- Create after evaluation: `docs/experiments/v08-summary-first-results.md`
- Test: `tests/v08-summary-first-fixtures.test.mjs`

**Interfaces:**
- Consumes: the four fixtures from Task 2.
- Produces: a repeatable human-run protocol for two compatible agents, with one summary query and one body-only query per fixture.

- [ ] **Step 1: Write the protocol opening and operating rule**

Create `docs/experiments/v08-summary-first-prototype.md` with this opening:

```markdown
# v0.8 Summary-First Prototype Protocol

## Purpose

Measure whether an agent can use a short summary for ordinary routing questions and correctly escalate to the full document for detail-only questions.

## Non-production status

This protocol does not change Persistent Memory. Its fixtures are fictional and must not be replaced with personal-memory files.

## Agent rule for every run

First read only the title, metadata, and `## Summary`. Answer only if the requested fact is present there. If it is absent, say that the summary is insufficient, then read `## Full Details` before giving the answer. Do not invent a missing detail.
```

- [ ] **Step 2: Add these eight prompt rows to the protocol**

| Fixture | Query type | Prompt | Pass condition |
|---|---|---|---|
| `legacy-guide.md` | Summary | “Which file governs current operations, and should `LEGACY_MEMORY.md` be treated as current?” | Names `CURRENT_RULES.md` and says the legacy file is historical, not current. |
| `legacy-guide.md` | Body-only | “What was the retired folder name?” | States that the summary is insufficient before answering `daily-scratch/` from full details. |
| `event-record.md` | Summary | “What was this event for, and what came out of it?” | Identifies a one-time planning workshop and a three-part follow-up checklist. |
| `event-record.md` | Body-only | “How long did the second activity last?” | States that the summary is insufficient before answering `17 minutes` from full details. |
| `course-brief.md` | Summary | “What did the course evaluate most, and is it still active?” | Names a usable deliverable plus user-need evidence and says the semester is complete. |
| `course-brief.md` | Body-only | “How much is the process log worth?” | States that the summary is insufficient before answering `15%` from full details. |
| `completed-web-project.md` | Summary | “What was built, what tools were used, and what uncertainty remains?” | Names Vite, Three.js, `explore`, and the unresolved public-versus-delivery count. |
| `completed-web-project.md` | Body-only | “What transition duration did the detail panel use?” | States that the summary is insufficient before answering `240 ms` from full details. |

- [ ] **Step 3: Add this results-file template**

Create `docs/experiments/v08-summary-first-results.md` only after the manual runs, using this exact table:

```markdown
# v0.8 Summary-First Prototype Results

| Agent | Fixture | Query type | Summary read first | Escalated when required | Correct answer | Unsupported claim | Notes |
|---|---|---:|---:|---:|---:|---:|---|
| [agent name] | [fixture] | [summary/body-only] | yes/no | yes/no/not applicable | yes/no | yes/no | [one sentence] |
```

- [ ] **Step 4: Run the fixture contract test again**

Run:

```powershell
node --test tests/v08-summary-first-fixtures.test.mjs
```

Expected: PASS with 4 tests.

### Task 4: Run the two-agent prototype and make the release decision

**Files:**
- Modify after execution: `docs/experiments/v08-summary-first-results.md`
- Test: the eight protocol rows in `docs/experiments/v08-summary-first-prototype.md`

**Interfaces:**
- Consumes: the protocol, four fixtures, and two compatible agents that can read the same temporary fixture directory.
- Produces: sixteen scored runs: eight prompts per agent.

- [ ] **Step 1: Prepare the non-personal test directory**

Place only `tests/fixtures/v08-summary-first/` in a temporary shared directory. Do not point either agent at `C:\Users\Yui\.persistent-memory`.

- [ ] **Step 2: Run the protocol with the first compatible agent**

For each fixture, give the agent the operating rule and the two matching prompts from Task 3. Record one results row per prompt.

- [ ] **Step 3: Run the same protocol with a second compatible agent**

Use the same fixture files and prompts. Record one results row per prompt. Do not revise the fixture summaries between the first and second agent.

- [ ] **Step 4: Apply the promotion gate**

Start a separate v0.8 product-release plan only if all of these conditions hold:

1. All 8 summary queries are correct without reading `## Full Details`.
2. All 8 body-only queries either explicitly say the summary is insufficient before reading full details or demonstrably read full details before answering.
3. All 16 answers contain no unsupported factual claim.
4. Neither agent attempts to update, archive, delete, or otherwise mutate any fixture.

If any condition fails, keep v0.7.1 unchanged. Record the exact failed row and revise only the synthetic fixture or experiment protocol; do not make a production claim or modify personal memory.

- [ ] **Step 5: Run final repository checks and commit the experiment package**

Run:

```powershell
node --test tests/v08-summary-first-fixtures.test.mjs
git diff --check
git status --short
```

Expected: the fixture test passes, `git diff --check` has no output, and the changed files are limited to the four fixtures, one fixture test, the protocol, the completed results file, and this plan.

Commit only after the result file is complete:

```powershell
git add tests/fixtures/v08-summary-first tests/v08-summary-first-fixtures.test.mjs docs/experiments/v08-summary-first-prototype.md docs/experiments/v08-summary-first-results.md docs/superpowers/plans/2026-07-15-v08-summary-first-prototype.md
git commit -m "test: add summary-first prototype fixtures"
```

## Self-Review

- Scope coverage: Tasks 1–2 create synthetic long documents and structural checks; Task 3 defines the same controlled prompts for both agents; Task 4 measures the only claim that matters before a feature release: correct summary use and correct escalation.
- Active-memory protection: The global constraints prohibit all personal-memory reads, copies, and mutations during implementation. Fixtures are fictional and stay in the project test directory.
- No production overclaim: No published behavior or release file changes until the two-agent promotion gate passes; a failed gate leaves v0.7.1 untouched.
- Placeholder scan: This plan contains no implementation placeholders. Every file, command, query, expected fact, and gate condition is specified.
