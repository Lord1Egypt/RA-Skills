---
name: github-clawhub-launcher
description: Review GitHub and ClawHub release plans, metadata, tags, release notes, and final publish order before a human runs any commands.
---

# GitHub + ClawHub Release Reviewer

Use this skill to review a local project release plan for GitHub and ClawHub.
Keep the work to structured review, metadata QA, release-note drafting, and a
human-run checklist. Do not create repositories, stage files, push branches,
create releases, publish ClawHub packages, or read unrelated local logs.

## Inputs

Ask only for missing release-critical details:

- repository name and intended owner,
- skill folder path and ClawHub slug,
- public display name and one-line description,
- version, changelog, license, tags, and GitHub topics,
- README and support-policy status,
- current `git status` summary if the user has it,
- intended publish order and any known blockers.

Do not request credentials, tokens, session cookies, recovery data, private
repository contents, private session transcripts, or unrelated local logs.

## Review Workflow

1. Confirm the release target: repo owner, repo name, skill path, ClawHub slug,
   display name, version, and license.
2. Check public metadata: README presence, SKILL.md presence, agents metadata,
   short description, tags, topics, and changelog.
3. Check release-surface risk: accidental secrets, local paths, private project
   names, private customer data, private prompts, unpublished screenshots, or
   wording that should not appear in a public listing.
4. Check command readiness at a high level. The human should review `git status`,
   inspect staged files, run tests, push intentionally, create the GitHub
   release, and publish the ClawHub package only after the checklist is clean.
5. Draft release notes from user-provided facts. Keep them concise and avoid
   claims that are not backed by the repo or release artifacts.
6. Return a final readiness verdict and a human-run checklist.

## Output

Return:

- verdict: `ready`, `needs edits`, or `do not publish`,
- metadata fixes,
- public-surface wording fixes,
- release-note draft,
- test and audit checklist,
- final human-run publish order.

## Guardrails

- Do not run, generate, or encourage blind execution of shell commands.
- Do not stage all files automatically or recommend publishing from a dirty
  tree without inspection.
- Do not create public repos, releases, tags, or ClawHub versions.
- Do not read browser profiles, credentials, private logs, or unrelated local
  files.
- Do not include non-release process wording in public release notes, package
  descriptions, or listing metadata.
