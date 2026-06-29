# Sanitize

Pre-publish validation for any text destined for a GitHub repository (issue body, PR body, comments). Two concerns: **personal-data leak** (PUBLIC repos — permanently indexed once leaked; even `gh issue edit` leaves the original in edit history) and **internal artifact paths** (PUBLIC *and* PRIVATE — `.ralph/`/`.omc/` render as dead links in any GitHub medium).

## When to Use

- Before `gh issue create`, `gh issue edit`, `gh pr create`, `gh pr edit`, `gh issue comment`, `gh pr comment` — **PUBLIC and PRIVATE** (the internal-artifact-path scan runs for PRIVATE too; personal-data scan is PUBLIC-only)
- Inside `plan-to-issue` (Step 5.5), `pr` (body assembly), `review` (review comment), `merge` (squash commit message)
- Whenever an issue-draft from `.ralph/issue-drafts/` is being posted

## Two distinct concerns — different visibility scopes

| Concern | What | Visibility scope |
|---------|------|------------------|
| **Personal-data leak** | Session UUIDs, user home paths, external tool names, internal hostnames, metrics from user data | **PUBLIC repo only** (permanently indexed once leaked) |
| **Internal artifact paths** | `.ralph/`, `.omc/`, `~/.claude/` workflow-generated paths (links, `Artifacts` / equivalent localized sections, doc references) | **EVERY repo — PUBLIC and PRIVATE** (dead-links / noise in any GitHub medium, not a leak concern) |

The internal-artifact-path scan is **not** a personal-data concern — those paths are meaningless dead references in any PR/issue/comment regardless of visibility. Do NOT skip it for PRIVATE repos.

## Repository visibility check (always first)

```bash
gh repo view --json isPrivate -q '.isPrivate'
```

- `true` → PRIVATE repo. Personal-data sanitization not enforced (still recommended for shared repos). **Internal-artifact-path scan STILL mandatory** (see below).
- `false` → PUBLIC repo. **Both personal-data sanitization AND internal-artifact-path scan are mandatory.**

## Internal artifact path scan (HARD STOP — runs for PRIVATE repos too)

Workflow-generated paths leak into PR/issue bodies via `Artifacts` (or equivalent localized) sections, supporting-analysis links, and copied research/plan references. They render as **dead links** on GitHub (the path exists only in the local workspace). Run this scan **regardless of repo visibility**, on every `gh ... create/edit/comment`:

```bash
BODY="$(cat /path/to/body.md)"  # or whatever holds the prepared body
# Matches bare (.ralph/...), relative (../../x/.ralph/...), and tilde (~/.ralph) forms
echo "$BODY" | grep -nE '(^|[^A-Za-z0-9_.-])(\.\./)*\.(ralph|omc)/|~/\.(claude|ralph|omc)/|\.claude/(skills|plugins|hooks|projects)/' && echo "BLOCKED: internal artifact path"
```

On match → **abort the post**, remove the offending link/section (or inline the substantive content), re-scan. An `## Artifacts` (or equivalent localized) section that only lists `.ralph/docs/generated/*.md` files must be **removed entirely** — the content belongs in the body prose, not as a path reference.

| # | Don't | Do |
|---|-------|-----|
| 1 | Skip the internal-path scan because the repo is PRIVATE | Internal paths are dead-links in ANY repo. Scan PRIVATE too |
| 2 | Rely on the `~/`-anchored personal-data grep to catch `.ralph/` | That pattern misses bare (`.ralph/docs/`) and relative (`../../x/.ralph/`) forms. Use the dedicated internal-path grep above |
| 3 | Keep an `Artifacts` (or equivalent localized) section listing `.ralph/docs/generated/*.md` | Remove the section; fold any needed substance into body prose |
| 4 | Link a workspace analysis doc via relative path (`[doc](../../x/.ralph/...)`) | Drop the link; inline the analysis conclusion as text |

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

The **internal-artifact-path scan** (see section above) runs for **every** repo, including PRIVATE — run it first. The four `grep` checks below are the **PUBLIC-only personal-data** scans. On a PUBLIC repo, run all (internal-path + the four below + Hangul). Each must produce **no output** (exit code 1):

```bash
BODY="$(cat /tmp/issue-body.md)"  # or whatever holds the prepared body

# (0) Internal artifact paths — RUN FOR PRIVATE TOO (visibility-agnostic)
echo "$BODY" | grep -nE '(^|[^A-Za-z0-9_.-])(\.\./)*\.(ralph|omc)/|~/\.(claude|ralph|omc)/|\.claude/(skills|plugins|hooks|projects)/' && echo "BLOCKED: internal artifact path"

# (1)-(4) PUBLIC-repo personal-data scans
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
4. **Re-scan**. Only proceed when all six scans return zero matches (internal-artifact-path + four personal-data + Hangul).

Do **not** "translate-as-you-write" or "sanitize while typing" — produce a fully cleaned draft first, scan, then post.

## Editing an existing PR body — re-validate the Test Plan category invariant (HARD STOP)

Sanitizing a PR body is a **body mutation**. Before re-posting, if the body contains a `## Test Plan` section, re-run the **Test Plan category self-check** ([pr.md](./pr.md) "Test Plan category classification"). A pre-existing flat (uncategorized) Test Plan must be prefixed now — do not preserve legacy flat items verbatim just because the edit's purpose was path-stripping.

```bash
# Flag any Test Plan item lacking a category prefix (**[general]** / **[UI]** / **[e2e]** / **[post-merge]**)
echo "$BODY" | grep -nE '^- \[.\] ' | grep -vE '\*\*\[(general|UI|e2e|post-merge|deploy)\]\*\*' && echo "WARN: uncategorized Test Plan item — apply prefixes before re-posting"
```

The category invariant holds across the body's lifetime, not just at creation. Any flow that edits a body (sanitize, review-apply, milestone, label) inherits this re-validation.

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
