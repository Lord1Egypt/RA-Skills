# Handoff Record Templates

Use sections relevant to the mode; do not fill unused sections with guesses. Write “Unknown: [reason]” when evidence is insufficient and “Not applicable: [reason]” when a category does not apply. Include timezone-aware timestamps and evidence paths, commits, or query times. Never include secret values.

## Outgoing summary or package index

- Project and scope: root, repository identity, timestamp, handoff agent, and baseline identifier.
- Confirmed goals, non-goals, acceptance criteria, and sources.
- Architecture and rules: document index, module responsibilities, and environment requirements.
- Progress: completed, in progress, pending, and blocked; latest verification commands, results, and limits.
- File baseline: inventory, snapshots or patch locations, HEAD, staged/unstaged/untracked coverage, exclusions, and sensitive-content handling.
- Dependencies and remote: manifest/lock state, branch, upstream, recent commits, relevant PRs, query time, and failures.
- Unresolved conflicts and recommended next steps.
- Receiving note: verification entry point; this package does not replace live verification or human confirmation.

## Incoming verification report

Status: Awaiting human confirmation. Project, investigation time, old baseline used, scope covered, and report location.

### File comparison

| Path | Comparison baseline | Status/change | Content diff or diff file | Evidence limitation |
|---|---|---|---|---|

Distinguish handoff-period changes, changes relative to the current Git commit, and current untracked status. List excluded directories, unreadable files, and changes observed during scanning.

### Documents and project understanding

Goals/non-goals, rules, architecture, progress, acceptance requirements, and implementation consistency; give a source for each. List documents read and important unread scope.

### Dependencies and repository

Manifest/lock changes; branch/HEAD/upstream/recent commits; relevant PRs; cached versus live remote results; network and permission limits.

### Understanding comparison

| Item | Old record and source | Current evidence | Verified fact/inference/unknown/pending decision | Impact on goals or next work |
|---|---|---|---|---|

### Conflicts and confirmation

| ID | Old record | New evidence | Impact | Possible decisions and recommendation | User response |
|---|---|---|---|---|---|

State “No conflicts found” explicitly when applicable. Name the proposed next task and request confirmation of the report and permission to continue; only read-only investigation may continue while waiting.

## Confirmation addendum

- Confirmation timestamp, user response, decision IDs, and unresolved items.
- Confirmed goals, rules, progress, next steps, and authorized task scope.
- Formal-record update location; whether private-memory synchronization was authorized and actually completed.
- Original baseline and incoming report remain available for traceability; new conclusions do not overwrite old evidence.

