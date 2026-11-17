# Action contract

triage: file (JSON array), asOf (timezone-aware ISO), staleDays (1..3650, default30). Required row fields number,title,url,updatedAt; optional state(OPEN/CLOSED/MERGED), labels([{name}] or strings), assignees(array). URLs must be github.com/OWNER/REPO/issues|pull/NUMBER and match number. One repository per request; <=707 items for bounded pairwise comparison. Output JSON/HTML/CSV with title similarity hints.

## Request example

```json
{
  "action": "triage",
  "file": "samples/issues.json",
  "asOf": "2026-10-26T00:00:00Z",
  "staleDays": 30
}
```

## Runtime and boundaries

Python 3.10+ standard library. Paths must be relative to the active workspace; absolute paths, parent traversal, symbolic links and junctions are rejected. This is a path guard, not OS-level isolation: retain the host container/sandbox. A helper field does not grant permission to access another account or send information.

If gh is already authenticated, export read-only data using gh issue list --repo OWNER/REPO --state all --limit 500 --json number,title,url,updatedAt,state,labels,assignees. Save its JSON in the workspace. Do not log tokens or create comments, labels, closes or PR merges. gh login and private repository access follow the user’s authorization.
