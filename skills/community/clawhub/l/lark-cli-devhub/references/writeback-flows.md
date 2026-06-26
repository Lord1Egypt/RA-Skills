# Writeback Flows

## Bugfix Payload

Write after a meaningful bug fix:

```json
{
  "Title": "Short bug title",
  "Project": "project-name",
  "Area": "module or product area",
  "Status": "Fixed",
  "Symptom": "What failed from the user's or system's point of view.",
  "Evidence": "Logs, test failures, screenshots, command output, or code facts checked.",
  "Root Cause": "The actual cause, not only the visible symptom.",
  "Fix Summary": "What changed and why it fixes the issue.",
  "Changed Files": "path/a.ts, path/b.py",
  "Verification Commands": "pytest tests/foo_test.py",
  "Verification Result": "Passed, failed, skipped with reason, or partially verified.",
  "Regression Risk": "Low/Medium/High plus where to watch.",
  "Next Time Check": "Fast check future agents should run first.",
  "Avoid": "Wrong approach to avoid repeating.",
  "AI Summary": "Dense searchable summary.",
  "Search Keywords": "symptom module error file names"
}
```

Command:

```bash
python3 "$DEVHUB_HOME/bin/devhub.py" record-bugfix --payload /tmp/devhub-bugfix.json
```

## AI Run Payload

Write after bug fixes, releases, large refactors, or investigations:

```json
{
  "Title": "AI run summary",
  "Project": "project-name",
  "Area": "module or product area",
  "Agent": "Codex or Claude Code",
  "Task Intent": "What the user wanted.",
  "Actions Taken": "Concise steps performed.",
  "Evidence Checked": "Files, tests, logs, old records, docs.",
  "Files Changed": "Changed paths.",
  "Verification Commands": "Commands run.",
  "Verification Result": "Result and caveats.",
  "Writeback Status": "Wrote Bugfix/Release/Outbox/Skipped with reason.",
  "AI Summary": "Dense searchable summary.",
  "Search Keywords": "task module command error"
}
```

Command:

```bash
python3 "$DEVHUB_HOME/bin/devhub.py" record-ai-run --payload /tmp/devhub-ai-run.json
```

## Release Payload

Write before pushing `main` or `master`:

```json
{
  "Title": "Release YYYY-MM-DD short name",
  "Project": "project-name",
  "Area": "Release / Main Push",
  "Branch": "main",
  "Commit SHA": "abc123",
  "Summary": "What is being released.",
  "Verification Commands": "test/build commands",
  "Verification Result": "Result and caveats.",
  "Rollback Notes": "How to revert or what to watch.",
  "Related Tasks": "Task titles or URLs",
  "Related Bugfixes": "Bugfix titles or URLs",
  "AI Summary": "Dense searchable release summary.",
  "Search Keywords": "release main deploy area"
}
```

Command:

```bash
python3 "$DEVHUB_HOME/bin/devhub.py" record-release --payload /tmp/devhub-release.json
```

## Outbox Rule

If Feishu write fails, do not fake success. Leave the generated `.devhub/outbox/*.json` item and mention it in the work summary. A later agent can retry with:

```bash
python3 "$DEVHUB_HOME/bin/devhub.py" sync-outbox --cwd "$PWD"
```
