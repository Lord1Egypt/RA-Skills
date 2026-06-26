---
name: incident-dossier
description: Build a concise incident dossier from operational logs, audits, JSON/JSONL files, and state snapshots. Use when investigating failures, duplicate events, stuck jobs, queue anomalies, regressions, or any situation where Codex must turn raw evidence into a structured incident report with timeline, suspected root cause, blast radius, and recommended next actions.
---

# Incident Dossier

Use this skill to turn messy operational artifacts into a usable incident report.

## Workflow

1. Identify the evidence set first: logs, JSON/JSONL audit trails, state snapshots, screenshots, or reports.
2. Prefer summarizing from parsed artifacts instead of hand-reading long raw logs.
3. Run `scripts/build_incident_dossier.js` with explicit inputs when at least one JSON/JSONL source exists.
4. Verify the generated timeline against a few raw lines before trusting it.
5. State uncertainty explicitly when timestamps are missing or conflicting.

## Output contract

Always include:
- Incident summary
- Scope / blast radius
- Timeline
- Evidence list
- Hypotheses / likely root cause
- Recovery status
- Recommended next actions

## Script

Use `scripts/build_incident_dossier.js` to parse mixed JSON/JSONL evidence and emit a Markdown dossier. Give it multiple `--input` paths and one `--out` path.

Example:

```bash
node skills/incident-dossier/scripts/build_incident_dossier.js \
  --input memory/job-audit.jsonl \
  --input out/job_consistency_audit_report.json \
  --out out/incident-dossier.md
```

## Guardrails

- Do not fabricate timestamps.
- Do not collapse distinct incidents into one unless the evidence clearly links them.
- Keep the dossier evidence-first; interpretation comes after observed facts.
