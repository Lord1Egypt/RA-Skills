---
name: git-dirty-check
description: Read-only triage for a local git working tree that summarizes uncommitted changes and applies conservative risk flags. Use when a user asks what changed in a repo, what is dirty, what is staged versus unstaged, or which risk flags apply before a commit. Do not use for commit writing, branch management, history analysis, merge conflict resolution, PR review, or general git assistance.
---

# git-dirty-check

A narrow git skill for summarizing uncommitted changes in a local repository. It groups staged, unstaged, untracked, and conflicted entries, applies conservative path- and filename-based risk flags, and suggests up to three next checks without modifying repo state.

`git-dirty-check` is a deliberately narrow skill for one job: understanding the current uncommitted state of a local git repository.

It does not try to manage branches, write commit messages, resolve conflicts, review pull requests, or act as a general git assistant. Instead, it gives a compact, structured triage of the current working tree:

- repo state
- changed entries by category
- conservative risk flags based mostly on paths, filenames, and diff stats
- a few copy-paste-ready next checks
- explicit omissions when details are capped or sensitive

The skill is read-only. It is designed for developers who want a quick operational summary before a commit, handoff, or local review, without granting write access or triggering broader repo assistance.

It also applies strict limits to deeper inspection:
- fail fast if the target is not a git repo
- branch metadata is optional
- deep diff inspection is capped
- secret-bearing filename patterns are handled at filename level only

This skill is most useful when raw git output is technically sufficient, but slower to parse than a stable triage summary.

## Workflow

1. Confirm the target path is inside a git repository.
2. If it is not a git repository, stop immediately and say so.
3. Collect read-only repo state with git status and diff-stat commands.
4. Group changed entries into:
   - staged
   - unstaged
   - untracked
   - conflicted
5. Apply conservative risk flags based mostly on file paths and filenames.
6. Inspect diff content only when filename and diff-stat data are insufficient to assign a listed risk flag, and only for files not matched by the secret-bearing file rule.
7. Return the output in the fixed order defined below.

## Commands to Prefer

Use read-only commands only.

Preferred commands:
- `git rev-parse --show-toplevel`
- `git rev-parse --abbrev-ref HEAD`
- `git status --short`
- `git diff --stat`
- `git diff --cached --stat`

Use targeted diff inspection only under the deep diff inspection cap, and only for files not matched by the secret-bearing file rule.

## Fail-Fast Rule

If the target path is not inside a git repository:
- stop immediately
- report that the path is not a git repository
- do not continue with generic filesystem analysis

## Branch Handling

Branch name is optional metadata only.
If branch name is available from a preferred read-only command, include it in Repo state.
If HEAD is unavailable or branch name lookup fails in an otherwise valid repo, omit branch metadata without error.
Do not give branch advice.

## Deep Diff Inspection Cap

Deep diff inspection is optional and must remain narrow.

Hard limits:
- inspect at most 3 files
- inspect at most 40 lines per file
- never inspect secret-bearing files beyond filename-level detection

Use deep diff inspection only for files not matched by the secret-bearing file rule and only when filename and diff-stat data are insufficient to assign or decline a listed risk flag.

## Secret-Bearing File Rule

Treat files matching these secret-bearing filename patterns as filename-level only.

Examples:
- `.env`
- `.env.*`
- `*.pem`
- `*.key`
- `id_rsa`
- `id_ed25519`
- `secrets.*`

For these files:
- do not inspect diff content
- do not print values
- report only that an entry matched a secret-bearing filename pattern

## Conservative Risk Heuristics

Keep risk flags conservative and mostly path/file based.

Flag examples:
- dependency manifest changed
- lockfile changed
- manifest changed without lockfile
- lockfile changed without manifest
- CI or workflow file changed
- possible deploy or infrastructure file changed
- possible auth or security-related file changed
- possible migration or schema file changed
- more than 10 unique paths changed
- entry matched a secret-bearing filename pattern

Do not over-interpret. Avoid speculative impact claims.

## Output Order

Always return sections in this exact order:

1. **Repo state**
2. **Changed files by category**
3. **Risk flags**
4. **Suggested next checks**
5. **Unknowns or omitted detail**

## Output Guidance

Keep the response brief and structured.

### 1. Repo state
Include:
- repo root
- branch name only as optional metadata
- counts of staged, unstaged, untracked, and conflicted files

### 2. Changed files by category
List entries under:
- staged
- unstaged
- untracked
- conflicted

List entries directly when there are 10 or fewer in a category. Otherwise list the first 10 and summarize the remainder.

### 3. Risk flags
List only conservative flags supported by filenames, paths, diff stats, or tightly capped non-sensitive diff samples.

### 4. Suggested next checks
Give 1 to 3 copy-paste-ready commands.
Prefer read-only commands.

### 5. Unknowns or omitted detail
Say what was intentionally not inspected, such as:
- diff content omitted due to caps
- sensitive files not inspected beyond filename
- large repo details summarized only

## Boundaries

Never:
- modify git state
- stage, unstage, commit, stash, reset, checkout, merge, rebase, or push
- write commit messages
- provide branch strategy
- expand into PR review or general git help
- expose secret-looking values from diffs
- use network operations

Stay narrow. This skill exists to answer: "What changed here, and which conservative risk flags apply?"

## Trigger examples

- “What changed in this repo?”
- “Summarize my uncommitted changes.”
- “What’s dirty here?”
- “Give me a quick git change triage.”
- “Before I commit, what changed and which risk flags apply?”
- “Show staged vs unstaged vs untracked changes in this repo.”

## Anti-trigger examples

- “Write a commit message.”
- “Help me resolve this merge conflict.”
- “Review this PR.”
- “Undo my last commit.”
- “Clean up my branch.”
- “Find the bug in this repo.”
- “Refactor these files.”
- “Explain git rebase.”

## Limitations

- Read-only only, no git state changes
- Focused on current uncommitted state, not history
- Risk flags are conservative and mostly path/file based
- Secret detection uses filename patterns, not full secret scanning
- Deep diff inspection is tightly capped
- Summary usefulness depends on the clarity of repo file naming and layout
- Not a replacement for full code review or git expertise

## Safety notes

- Uses read-only git commands only
- Does not stage, unstage, commit, stash, reset, checkout, merge, rebase, or push
- Does not use network operations
- Fails fast on non-repo paths
- Does not inspect secret-bearing files beyond filename-level detection
- Avoids exposing secret-looking values from diffs
- Keeps output scoped to triage, not general repo management
