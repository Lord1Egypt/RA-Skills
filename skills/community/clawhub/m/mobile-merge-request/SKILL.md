---
name: mobile-merge-request
description: "Guides the merge request and pull request workflow for mobile teams: branch naming, Conventional Commits, small and stacked MRs, self-review, rebase vs merge, safe conflict resolution for lockfiles, project.pbxproj and version catalogs, MR descriptions with screenshots and rollback, and reviewer etiquette. Use when creating branches, writing commits or MR descriptions, rebasing, resolving conflicts or answering review comments."
license: MIT
metadata:
  author: Ahmad Hussain
  version: "1.0.1"
  pack: mobile-dev-kit
---

# Mobile merge request

Get mobile changes from a branch into main with a clean history, a description a reviewer can act on,
and no lost work along the way. Applies to GitLab merge requests and GitHub pull requests alike;
"MR" below means either.

## When to use

- Creating a branch, writing or cleaning up commit messages before review.
- Opening an MR or PR, writing or improving its title and description.
- Splitting a large change into smaller or stacked MRs.
- Rebasing onto main, resolving conflicts, or force-pushing after review fixes.
- Reviewing someone else's MR, or replying to review comments on your own.
- Checking MR hygiene: branch name, commit messages, size, description, checklist.

Not for: reviewing the code itself for bugs (use `mobile-code-review`), or pipeline configuration
(use `mobile-ci-cd`).

## Workflow

1. Gather facts before writing anything.
   - Branch and target: `git branch --show-current`, `git fetch origin`.
   - Commits: `git log --oneline origin/main..HEAD`.
   - Size and files: `git diff --stat --merge-base origin/main`.
   - Ticket key from the branch name or the user. Never invent a ticket key; leave a placeholder.
2. Check hygiene against the Rules below: branch name, commit messages, size, unrelated changes,
   generated files, secrets in the diff.
3. If the history needs cleanup, propose the commands (fixup, autosquash, rebase) and wait for approval.
   The agent never rewrites history, force-pushes or merges without explicit user consent.
4. Self-review the full diff as a reviewer would. Remove debug logs, commented-out code, stray TODOs.
5. Run the project's build, lint and tests for every affected platform. Report failures honestly.
6. Write the MR title and description from [the MR template](references/mr-template.md).
   Fill only what the diff and the user support; mark unknowns as `TODO` for the author.
7. For conflicts, follow [conflict resolution](references/conflicts.md). Re-run build and tests after.
8. For exact command sequences (stacking, retargeting, recovery), use
   [git commands](references/git-commands.md).

## Rules

### 1. Branch names carry type, owner and ticket

```text
# BAD
ahmad-changes
fix
feature/new-stuff

# GOOD
feature/AH/PROJ-123-ble-reconnect-backoff
fix/AH/PROJ-456-crash-on-empty-scan
chore/AH/PROJ-789-bump-agp
```

- Pattern: `<type>/<initials>/<TICKET>-<kebab-short-title>`. Types: `feature`, `fix`, `chore`,
  `refactor`, `docs`, `test`, `release`, `hotfix`.
- Lowercase after the ticket key, no spaces, under about 60 characters.
- Follow the repository's own convention if it already has one.

```bash
git fetch origin
git switch -c feature/AH/PROJ-123-ble-reconnect-backoff origin/main
```

### 2. Commits follow Conventional Commits

```text
# BAD
fixed stuff
WIP
Update MainActivity.kt

# GOOD
fix(ble): retry GATT connect with exponential backoff
feat(onboarding): add QR pairing screen
refactor(settings): move formatting out of SettingsViewController
```

- Format: `<type>(<optional scope>): <imperative summary>`, summary under about 72 characters, no period.
- Types: `feat`, `fix`, `refactor`, `perf`, `test`, `docs`, `build`, `ci`, `chore`, `style`, `revert`.
- Body explains why, not what the diff already shows. Wrap at 72.
- Footers: `Refs: PROJ-123`, `BREAKING CHANGE: <what breaks and how to migrate>`.

Breaking changes:

```text
# BAD: breaking change hidden in a fix
fix(api): rename deviceId field

# GOOD
feat(api)!: rename deviceId to gatewayId in telemetry payload

BREAKING CHANGE: backend must accept gatewayId; app versions before 3.2 send deviceId.
Refs: PROJ-321
```

- No tool-generated footers, sign-offs or co-author trailers unless the project requires them.

### 3. One concern per MR, small enough to review in one sitting

```text
# BAD: one MR
feat: QR pairing + Gradle 9 upgrade + rename package + fix crash in settings

# GOOD: four MRs
chore(build): upgrade Gradle wrapper
refactor: rename package com.acme.old to com.acme.gateway
feat(onboarding): add QR pairing screen
fix(settings): crash on empty device name
```

- Rough guidance: under about 400 changed lines of hand-written code. Lockfiles, generated code and
  snapshots do not count but must be listed.
- Mechanical changes (renames, formatting, dependency bumps) go in their own MR, never mixed with logic.
- If it cannot be small, stack it (rule 4) or put it behind a feature flag and land it in slices.

### 4. Stacked MRs target their parent, then get retargeted

```bash
# BAD: second MR targets main and shows the first MR's commits too
git switch -c feature/AH/PROJ-124-pairing-ui feature/AH/PROJ-123-pairing-api
# ...opened against main

# GOOD: target the parent branch; after the parent merges, rebase and retarget to main
git switch -c feature/AH/PROJ-124-pairing-ui feature/AH/PROJ-123-pairing-api
# open MR: feature/AH/PROJ-124-pairing-ui -> feature/AH/PROJ-123-pairing-api
```

- Say "Depends on !123" (GitLab) or "Depends on #123" (GitHub) at the top of the description.
- Keep stacks shallow: two or three levels.
- After the parent is squash-merged, replay only your own commits with `git rebase --onto` (see
  [git commands](references/git-commands.md)) and retarget the MR to main.

### 5. Rebase your own branch; never rewrite shared branches

```bash
# BAD
git push --force                  # overwrites whatever is on the remote, including others' commits
git rebase origin/main            # on main, develop or a branch a colleague also pushes to

# GOOD: own branch only, refuses if the remote moved since your last fetch
git fetch origin
git rebase origin/main
git push --force-with-lease
```

- Shared branches (`main`, `develop`, `release/*`, a branch two people push to) only get merge commits
  or new commits, never rewrites.
- Do not rebase in the middle of an active review round without telling reviewers; it resets their
  "changes since last review" view on some platforms. Prefer fixup commits until approval.

### 6. Review fixes are fixup commits, squashed before merge

```bash
# BAD: noise that lands in main
git commit -m "address review comments"
git commit -m "fix typo"

# GOOD
git commit --fixup=a1b2c3d
# after approval, fold fixups into their targets
git rebase -i --autosquash origin/main
git range-diff origin/main @{u} HEAD   # confirm only intended changes before pushing
git push --force-with-lease
```

### 7. Squash policy is explicit

- One logical change per MR: squash-merge. The MR title becomes the commit, so it must be a valid
  Conventional Commit.
- Several atomic, well-written commits (for example a refactor then a feature): rebase-merge or
  fast-forward, no squash, so `git bisect` and `git revert` stay precise.
- Never squash an MR that mixes a dependency bump with a behaviour change; split it instead.

```text
# BAD squash-merge title
Feature/AH/PROJ-123 ble reconnect backoff

# GOOD
fix(ble): retry GATT connect with exponential backoff (PROJ-123)
```

### 8. Conflicts are resolved by understanding both sides, then verified by a build

```bash
# BAD: pick a side blindly for every file
git checkout --theirs .
git add . && git rebase --continue

# GOOD: inspect, resolve per file, regenerate what is generated, then build and test
git status
git diff --name-only --diff-filter=U
# resolve each file; regenerate lockfiles and generated code instead of hand-merging
git add <file>
git rebase --continue
./gradlew assembleDebug testDebugUnitTest
```

- During a rebase `--ours` is the branch being rebased onto (main) and `--theirs` is your commit.
  The opposite of a merge.
- Lockfiles, `project.pbxproj` and version catalogs have specific procedures:
  [conflict resolution](references/conflicts.md).

### 9. The description lets a reviewer review without asking

```markdown
<!-- BAD -->
Fixes the bug.

<!-- GOOD (short form) -->
## Summary
Reconnect to the gateway with exponential backoff after GATT error 133 instead of failing at once.

## Ticket
PROJ-123

## Testing
- Unit: BackoffPolicyTest (new), ConnectionManagerTest (updated)
- Manual: Pixel 8 Android 16, iPhone 15 iOS 26; power-cycled gateway 10 times, reconnected every time
```

- Every user-visible change has Android and iOS screenshots or recordings, before and after.
- Call out explicitly: new permissions, manifest or `Info.plist` keys, entitlements, `minSdk`,
  `targetSdk` or deployment target changes, database migrations, analytics or telemetry changes.
- Full template: [MR template](references/mr-template.md).

### 10. Review comments are labelled and actionable

```text
# BAD
This is wrong.
Why would you do it like this?

# GOOD
issue: `onCharacteristicChanged` runs on a binder thread; `_state.value = ...` here races with the
collector. Use `_state.update {}` or hop to the main dispatcher.

nit (non-blocking): `deviceList` -> `devices` to match the repository naming.

question: Is the 10 s timeout from the firmware spec, or a guess? If a guess, add a constant with a comment.
```

- Labels: `issue:` (blocking), `suggestion:`, `question:`, `nit:` (never blocks), `praise:`, `todo:`.
- Comment on the code, not the person. Explain why, and propose a fix or a suggestion block.
- See [reviewer etiquette](references/mr-template.md#reviewer-etiquette) for both sides of a review.

## Anti-patterns

- "WIP", "fix", "changes" as the final commit or squash title.
- Force-pushing with plain `--force`, or rewriting `main`, `develop` or a colleague's branch.
- Rebasing and force-pushing during review without saying so, so reviewers lose their place.
- One MR containing a feature, a dependency bump and a mass reformat.
- Hand-merging `pubspec.lock`, `Podfile.lock`, `Package.resolved` or generated code.
- Resolving `project.pbxproj` conflicts by taking one side wholesale and losing the other side's files.
- Marking every reviewer thread resolved without replying or changing anything.
- Screenshots for one platform only on a cross-platform UI change.
- Descriptions that repeat the diff file by file instead of explaining why.
- Merging with a red pipeline "because it is flaky".

## Checklist

- [ ] Branch follows `<type>/<initials>/<TICKET>-<short-title>` and is based on current main
- [ ] Every commit is a valid Conventional Commit; breaking changes use `!` and a `BREAKING CHANGE:` footer
- [ ] MR has one concern and is reviewable in one sitting (or is split or stacked)
- [ ] Stacked MRs target their parent and say "Depends on"
- [ ] Self-reviewed: no debug logs, commented-out code, secrets, personal data or unrelated files
- [ ] Build, lint and tests pass for every affected platform after the last rebase or conflict fix
- [ ] Description has Summary, Ticket, Changes, screenshots (Android and iOS), Testing, Risk and rollback
- [ ] Permissions, manifest, `Info.plist`, entitlements, SDK levels and migrations are called out
- [ ] Review fixes are fixup commits; history is cleaned before merge
- [ ] Force pushes use `--force-with-lease`, on the author's own branch only
- [ ] Every review thread has a reply; resolved by the agreed party
- [ ] Squash or rebase-merge chosen deliberately; final commit title is a valid Conventional Commit

## Output format

When asked to write an MR or PR description, produce the title and the filled template:

~~~markdown
Title: fix(ble): retry GATT connect with exponential backoff (PROJ-123)

## Summary
<one or two sentences: what changes for the user or the codebase, and why>

## Ticket
PROJ-123

## Changes
- <grouped by intent, not by file>

## Screenshots / recordings
| Android | iOS |
|---|---|
| TODO | TODO |

## Testing
- <tests added or updated, devices and OS versions, manual steps>

## Risk and rollback
- Risk: <what could break, who is affected>
- Rollback: <revert MR | disable flag X | server config>

## Checklist
- [x] <items verified from the diff>
- [ ] <items the author must confirm>
~~~

When asked to check MR hygiene, produce findings in this shape:

~~~markdown
## MR hygiene: <branch name>

Target: main. Commits: 5. Changed: 612 lines in 14 files (180 in lockfiles and generated code).

### Findings
1. [Must fix] Commit "wip" (a1b2c3d) -- not a Conventional Commit.
   Fix: `git commit --fixup=<target>` or reword before merge.
2. [Must fix] Description has no iOS screenshots for a shared UI change.
3. [Should fix] Gradle wrapper bump mixed with feature code -- split into its own MR.
4. [Note] `Info.plist` gains `NSBluetoothAlwaysUsageDescription` -- call it out under Risk.

### Suggested commands
```bash
git rebase -i --autosquash origin/main
git push --force-with-lease
```

### Verdict
Not ready -- 2 Must fix.
~~~

Severity: Must fix blocks requesting review; Should fix is expected before merge; Note is informational.

## Related skills

- `mobile-code-review` -- reviewing the code inside the MR
- `mobile-ci-cd` -- pipelines, required checks, release branches and signing
- `mobile-security` -- when the diff touches secrets, permissions, network or storage
- `mobile-kotlin`, `mobile-swift`, `mobile-flutter` -- build and test commands per platform
- `mobile-release` -- release notes and readiness before merging a release branch
