# Research Quality Rubric

Use this rubric to judge whether a run is decision-ready.

## 1) Scope Completeness

Pass criteria:

- All sub-questions in `plan.json` appear in `findings.json`.
- Every sub-question has either evidence-backed findings or explicit unresolved gaps.

Failure signals:

- Missing question IDs.
- Generic findings that do not answer the question.

## 2) Evidence Strength

Pass criteria:

- Each sub-question has at least 3 sources when web search is enabled.
- Sources include primary references when available (official data, standards, filings, vendor docs).

Failure signals:

- Circular citations across low-quality reposts.
- Claims without links or with broken URLs.

## 3) Source Reliability Mix

Target mix:

- High reliability: official docs, government portals, standards bodies, audited financial filings.
- Medium reliability: reputable analysis institutions, major media with named sources.
- Low reliability: anonymous posts, marketing-only pages, derivative summaries.

Action:

- If low-reliability sources dominate, rerun with tighter prompt constraints.

## 4) Contradiction Handling

Pass criteria:

- Conflicting evidence is explicitly listed in `report.md`.
- Report explains which source is preferred and why.

Failure signals:

- Report presents certainty where sources disagree.

## 5) Recommendation Usability

Pass criteria:

- Recommendations include clear actor, action, and condition.
- Recommendations reference supporting evidence sections.

Failure signals:

- Vague statements such as "continue monitoring" without trigger conditions.

## Iteration Playbook

When quality fails, iterate with one focused change at a time:

1. Lower `--depth` when questions are too broad.
2. Increase `--depth` when important dimensions are missing.
3. Switch `--research-model` when evidence extraction quality is weak.
4. Reduce `--parallel` if endpoint rate limits are frequent.
5. Add explicit domain constraints into topic wording for narrower evidence.
