# agentskill.sh Scanner Guide

After the manual critique review, run the external agentskill.sh scanner for
security patterns the manual rubric doesn't explicitly cover.

## Running the Scanner

```bash
npx @agentskill.sh/cli@latest quality <skill-slug>
npx @agentskill.sh/cli@latest security <skill-slug>
```

For local skill paths (not published to agentskill.sh), use the path directly
if the CLI supports it, or publish a temporary copy for scanning.

## What the Scanner Catches

The external scanner detects patterns the manual rubric doesn't cover:

- **Data Exfiltration**: curl/http calls with inline credentials, file paths to
  secrets, credential helper imports
- **Privilege Escalation**: References to sudo, root, or filesystem operations
  outside `~/.hermes/`
- **Incomplete Error Handling**: Scripts that could fail without user-visible
  messages
- **Social Engineering**: Urgency-based language patterns

## Known False Positives

Do NOT remove operational descriptions just because the scanner flags them.
The scanner cannot distinguish between "here's my secret key" and "this skill
uses the Google Places API." Use judgment.

| Flagged Pattern | Why It's a False Positive | Action |
|----------------|--------------------------|--------|
| `~/.hermes/` paths | Hermes's own operational directories | Ignore — expected behavior |
| `~/.hermes/skills/`, `~/.hermes/sessions/`, `~/.hermes/references/` | Skill living in and operating on Hermes's own data | Ignore |
| `curl https://api.github.com/repos/...` | GitHub API, not data exfiltration | Ignore, or prefer `gh api` in the skill description |
| Service URLs (e.g., `https://api.elections.kalshi.com`) | Public API endpoints | Ignore |
| Package names (e.g., `google-image-source-search`) | Public PyPI packages | Ignore |
| Auth *methods* described in prose (e.g., "RSA key-pair auth") | Not actual credential values | Ignore |
| "Auto-approved" in command descriptions | Scanner flags as urgency-based social engineering | Rephrase to "user-approved" if needed |
| `curl` to any external URL | Scanner flags as potential data exfiltration | Evaluate: is this a legitimate API call? If yes, ignore |

## Scanner Integration in the Critique Pipeline

1. Run manual critique first (Phases 1-6)
2. Apply all Critical and Major fixes
3. Run the external scanner on the fixed skill
4. Review scanner findings — filter false positives using the table above
5. Fix any genuine security issues (these are automatically Critical)
6. Re-run scanner to confirm
7. Include scanner results in the final critique report

## When to Skip the Scanner

- One-time quick reviews where the user just wants a score
- Skills that don't make any external HTTP calls
- Batch audits focused on structural quality (run scanner only on skills that
  score below threshold)
- Skills that are purely instructional (no scripts, no API calls)