# OpenSpec workflow patterns

## Starting a new change

User: "Let's add dark mode to the dashboard."

1. `openspec_list { projectPath, kind: "changes" }` — confirm no in-flight dark-mode change.
2. `openspec_status { projectPath }` — see what's already in motion.
3. Create folder `openspec/changes/add-dark-mode/` with the four artifacts. Use the agent's own writing — these are markdown files, no CLI helper needed for creation.
4. `openspec_validate { projectPath, name: "add-dark-mode" }`.

## Picking up an in-flight change

User: "Continue the auth refactor."

1. `openspec_list { projectPath, kind: "changes" }` — confirm the change exists and grab its name.
2. `openspec_show { projectPath, name: "<name>", includeFiles: true }` — read all four artifacts.
3. Look at `tasks.md` for the first unchecked item and start there.

## Closing out a change

User: "We shipped dark mode."

1. Verify `tasks.md` is fully checked.
2. `openspec_validate { projectPath, name: "add-dark-mode" }` — last sanity pass.
3. `openspec_archive { projectPath, changeName: "add-dark-mode", yes: true }`.

## Bootstrapping a project

User: "Set up OpenSpec on this repo."

1. Confirm which AI tools the project targets (Claude Code, Cursor, OpenCode, etc.).
2. `openspec_init { projectPath, tools: ["claude", "cursor"], profile: "core" }`.
3. After install, run `openspec_update { projectPath }` whenever the package is upgraded.

## Pairing with other workflows

- With Serena: use `serena_*` for code understanding inside the change's apply phase. OpenSpec covers planning; Serena covers semantic navigation.
- With TaskFlow: long-running detached implementations can be modelled as a TaskFlow whose owner conversation manages the change folder.
