# Sanitize

Pre-publish validation that strips personal data from any text destined for a PUBLIC GitHub repository (issue body, PR body, comments). Issue/PR/comment text on GitHub is permanently recorded — once leaked, even `gh issue edit` leaves the original in the edit history.

## When to Use

- Before `gh issue create`, `gh issue edit`, `gh pr create`, `gh pr edit`, `gh issue comment`, `gh pr comment` on a PUBLIC repo
- Inside `plan-to-issue` (Step 5.5), `pr` (body assembly), `review` (review comment), `merge` (squash commit message)
- Whenever an issue-draft from `.ralph/issue-drafts/` is being posted

## Repository visibility check (always first)

```bash
gh repo view --json isPrivate -q '.isPrivate'
```

- `true` → PRIVATE repo. Sanitization not enforced (still recommended for shared repos).
- `false` → PUBLIC repo. **Sanitization is mandatory.**

## Forbidden patterns (HARD STOP — abort posting if any match)

| Category | Pattern | Example | Replace with |
|----------|---------|---------|--------------|
| Session/resource UUID v4 | `[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}` | `<uuid-v4>` | `session-id`, `abc-1234-...` |
| User home path | `/Users/<name>/`, `/home/<name>/` | `/Users/<name>/<sync-folder>/...` | `~/`, `<user-home>/`, `/path/to/...` |
| Internal working paths | `~/.claude/`, `~/.ralph/`, `~/.omc/` | `~/.ralph/issue-drafts/foo.md` | Remove or generalize |
| External tooling (unrelated to the issue) | file-sync daemon, dotfile manager, version manager, identity provider, automation server, secrets store, journal app, git GUI, cloud account, edge CDN | "file-sync daemon `.sync-conflict` resolution" | "file synchronization tool" or remove |
| Internal hostnames/IPs | `<private-IP>`, `<internal-host>`, `<internal-domain>` | `<private-IP>` | "internal server" or remove |
| Metrics extracted from user data | "N lines, M unique UUIDs" | "1000+ duplicates in my session" | "hundreds or thousands of records" |
| Real file names from user data | `<uuid>.jsonl` | The user's actual session file | "test fixture file" |
| First-person environmental anecdotes | "in my environment", "across my cwd's" | Real workflow description | Generic scenario phrasing |

## Sanitization scan command

Run all four `grep` checks before `gh ... create/edit/comment`. Each must produce **no output** (exit code 1):

```bash
BODY="$(cat /tmp/issue-body.md)"  # or whatever holds the prepared body

echo "$BODY" | grep -P '[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}' && echo "BLOCKED: UUID detected"
echo "$BODY" | grep -E '/Users/[a-z]+|/home/[a-z]+|~/.claude|~/.ralph|~/.omc' && echo "BLOCKED: user/internal path"
echo "$BODY" | grep -iE "${PII_TOOL_KEYWORDS:-<tool-keyword-set>}" && echo "BLOCKED: external tool name"
echo "$BODY" | grep -E "${PII_INTERNAL_HOST_RE:-<internal-host-prefix>}" && echo "BLOCKED: internal hostname/IP"
```

Also run the **Korean character scan** (PUBLIC repo English-only rule):

```bash
echo "$BODY" | grep -P '\p{Hangul}' && echo "BLOCKED: Hangul detected"
```

## HARD STOP behavior

When any scan matches:

1. **Abort** the `gh ... create/edit/comment` call immediately.
2. **Report** to fix_plan: `BLOCKED: <category> found in PUBLIC repo content (<line snippet>)`.
3. **Rewrite** the offending lines in the source draft (issue-draft or working buffer).
4. **Re-scan**. Only proceed when all five scans return zero matches.

Do **not** "translate-as-you-write" or "sanitize while typing" — produce a fully cleaned draft first, scan, then post.

## Origin of personal data in drafts

Personal data typically enters `.ralph/issue-drafts/*.md` because:

- The user pasted real debugging output (real session file) into the draft as evidence
- Ralph wrote down "what I observed in my session" verbatim while researching
- A copied-from-elsewhere example contained another project's identifiers

**Drafts are allowed to contain debugging notes**, but the **publish step must sanitize**. Generalize the bug scenario: "construct a fixture .jsonl with intentionally duplicated lines" instead of "session `<uuid>` has N lines".

## Post-publish discovery

If personal data is discovered **after** `gh issue create/edit`:

1. Immediately `gh issue edit <N> --body "<sanitized>"` to overwrite — do not delay.
2. Note in fix_plan: GitHub `edit history` is permanent; the leak is recorded even after edit. Consider whether the exposure level warrants further action (GitHub Support request, etc.).
3. Update the source `.ralph/issue-drafts/*.md` to the sanitized version so re-publishing won't regress.

## Ralph autonomous mode

Same rule applies in autonomous loops. No `--no-confirm` or speed-pressure exemption. The four `grep` scans are non-negotiable.

## Reference

Linked from:

- `plan-to-issue.md` Step 5.5
- `pr.md` body assembly step
- `review.md` review comment posting step
- `merge.md` squash commit message preparation
- `~/.agents/rules/opensource.md` "PUBLIC repository personal data ban"
- Ralph `PROMPT.md.template` and project-local `.ralph/PROMPT.md` inline rule

Recorded violation pattern: a PUBLIC-repo issue contained user session UUIDs, raw metrics, and an external tool name verbatim — required sanitization after the fact.
