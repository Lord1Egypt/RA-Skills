# Incoming Handoff

Identify the project root, applicable instructions, receiving scope, and available handoff records. Use old chats and private memory only when accessible and relevant. If no package exists, perform a first takeover; do not require one. Complete these five stages in order, and never skip the final confirmation gate.

## 1. Local file scan and change identification

Record investigation time and the identity, timestamp, and coverage of any baseline. Inventory files and Git state. Separate tracked, untracked, ignored, staged, and unstaged changes. Do not rely only on `git diff`; it normally excludes untracked content.

Compare against an explicit old state:

- With a content baseline: list added, modified, and deleted files, rename candidates, and unified text diffs or saved complete diffs. Do not silently truncate large changes.
- With only a readable Git commit: compare its files with the current staged and working-tree state, and state that old uncommitted and untracked state cannot be reconstructed.
- With only an inventory or file hash: report only changes supported by the evidence; explain why specific content is unavailable.
- With no baseline: establish a current inventory and compare any old description. Mark historical changes and timing unknown when evidence cannot establish them. Git changes relative to the current commit are not automatically changes since handoff.

Identify the full scope, then inspect source, configuration, documentation, and lock files first. Summarize dependency directories, build output, and caches and state what was skipped. Compare binaries by attributes or hashes. For sensitive files, report only safe state and never expose secrets. List submodules, LFS objects, symbolic links, and inaccessible files as limitations. If the project changes during scanning, re-check affected state and state the time boundary.

## 2. Development-document reading

Read applicable `AGENTS.md`, `CLAUDE.md`, README, CHANGELOG, design, architecture, development-rule, plan, test, and acceptance documents. For a large project, index documents first and state what was not read.

Extract goals, non-goals, architecture, responsibilities, constraints, progress, acceptance criteria, and verification methods. Record paths and locations. Check whether documents match implementation: implementation proves current behavior, not that it matches the user's goal. A newer document is not automatically an approved decision.

## 3. Dependency and remote-repository analysis

Inspect actual manifests, lock files, workspace configuration, and toolchain declarations such as `package.json`, `requirements.txt`, `pyproject.toml`, and `go.mod`. Compare dependencies, ranges, locked versions, scripts, and environment requirements. Separate lock-file changes from installed-state evidence. Without a baseline, report current state and unknown history only. Do not install or rewrite lock files.

Record repository identity, branch or detached HEAD, HEAD, recent commits, upstream, ahead/behind state, and dirty-worktree state. Useful read-only references include `git log`, `git status`, `git remote`, and `git branch -vv`; redact remote URLs.

Prefer available repository connectors or CLIs for current remote state and open PRs. When needed, use a normal `git fetch` without force or prune options; never merge it. Distinguish cached state from live query results. For relevant PRs, record target branch, source branch, status, and relationship to current work.

If access fails, record the failure and unverified scope, then continue local investigation. Do not claim there are no PRs or that the remote is consistent. Do not repeatedly retry or request credentials. If Git or a remote is absent, mark it not applicable.

## 4. Memory and goal update

Create an independent receiving report using the record template. Update current-session understanding with verified facts plus goals awaiting confirmation. Mark old memories that can no longer be treated as current facts; do not code from stale descriptions.

Separate verified ordinary facts, goal/rule/acceptance changes requiring user confirmation, and inferences or unknowns. Use the existing record location or create an independent report under `handoff/<timestamp>/` when appropriate. If writing is unavailable, present the report in chat. A report is an investigation record, not approval. Update formal goals and tasks only after confirmation; update private memory only when explicitly authorized and technically available.

## 5. Conflict questions and human confirmation

List every conflict with an identifier, old record, current evidence, impact, possible decisions, and recommendation. Recommendations are not user decisions. Ordinary evidence-backed progress remains in the report but needs no separate decision question.

End by showing file changes, document conclusions, dependency and repository state, updated understanding, unresolved conflicts, verification limits, and the exact proposed next task. Then ask:

> Please decide each conflict above (or confirm that there are none), confirm this verification report, and confirm whether I may continue with [specific task]. Until you explicitly confirm, I will perform only necessary read-only investigation.

If there is no next task, ask the user to confirm the takeover result without inventing more work. After a complete report, a clear reply such as “Yes, continue with the login page” confirms both the report and task; no fixed phrase is required. An ambiguous reply or one addressing only a single conflict does not confirm unrelated items. Record partial decisions without marking the entire takeover confirmed. After confirmation, record wording and scope, then update formal understanding. If a material change occurs, explain it and obtain confirmation for affected conclusions.

### Example

The old summary says “offline and no account system,” the current README says cloud sync requires login, the workspace contains an untracked `auth.ts`, and the user says “take over and quickly continue the login page.” Report a goal conflict. Call `auth.ts` “currently untracked”; if the old workspace did not record untracked files, do not call it a post-handoff addition. Compare the readable old commit if available, explain any remote verification failure, ask whether the cloud-sync goal should govern, and wait for confirmation of both the report and continuing the login-page work. Even when all sources agree, keep the final confirmation gate.

