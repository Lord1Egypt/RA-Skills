# Outgoing Handoff

## Handoff summary

Confirm the project root and scope. Read applicable project instructions, important development documents, and current repository state. Record:

- User-confirmed goals, non-goals, acceptance criteria, development rules, and each source. Do not present an agent recommendation as a user decision.
- Implementation and plan status: completed, in progress, blocked, and next steps. Include verification commands, results, timestamps, and unverified areas.
- Architecture, entry points, dependencies, environment requirements, document paths, known issues, and questions requiring user decisions.
- Branch, HEAD, workspace and index status, relevant remotes and PR status. Mark live queries versus cached local facts.

## Optional handoff package

Write a package only when the user chooses one. Otherwise provide the summary in chat and explain that later historical comparison may be limited. Never block the next agent because the package is missing.

Use an existing project convention. If none exists, use `handoff/<timestamp>/` under the project root. Confirm the directory's purpose, avoid overwriting an existing package, and record relative paths, timestamp and timezone, repository identity, and scan scope. Exclude the handoff directory from its own baseline and state that exclusion.

Use existing file and Git tools; do not create a custom scanning script:

1. Separate committed, staged, unstaged, untracked, and ignored state. Useful references include `git status --short --branch`, `git diff`, and `git diff --cached`.
2. Record relevant paths, types, and available size, hash, or version source. Distinguish a complete inventory from a sample and state exclusions and unread areas.
3. Preserve recoverable baseline content for source, configuration, lock, and development-document files that need precise comparison: a commit plus patches, necessary untracked text snapshots, or complete text snapshots. HEAD alone does not cover uncommitted or untracked content; a hash alone cannot support a line-level diff.
4. Do not copy dependency directories, caches, or generated output by default. Record scope and state. For binaries, record attributes or hashes; do not claim a textual diff.
5. Do not copy secrets, tokens, credentials, or sensitive environment values. Redact remote URLs that may contain tokens. Record only safely observable changes and mark unsafe comparisons.
6. Record manifests, lock files, toolchain declarations, and verified remote state. Do not install dependencies or modify the workspace.

End with the receiving entry point, package location, baseline coverage, unresolved items, and a reminder that the receiver must re-verify and wait for human confirmation. Handoff does not mean receiving is complete or authorize later development.

