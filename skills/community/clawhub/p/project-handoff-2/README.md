# Project Handoff

`project-handoff` is a tool-agnostic skill for transferring project context between AI agents, tools, and sessions.

It helps a receiving agent rebuild its understanding from current evidence instead of relying on stale memory or assuming that the newest document automatically represents the user's intent.

## What it verifies

When receiving a project, the skill requires the agent to:

1. Scan local files and compare them with any available handoff baseline.
2. Read project instructions and development documentation.
3. Inspect dependency manifests, lock files, Git state, remote branches, and relevant pull requests.
4. Update its understanding of the project's facts, goals, progress, and unknowns.
5. Identify conflicts and ask the user to resolve them.

Even when no conflict is found, the agent must present the verification report and obtain explicit user confirmation before continuing development.

## Handoff package is optional

The receiving agent can work with or without a handoff package.

When a package exists, it provides a comparison baseline for files, project goals, dependencies, and repository state. When it does not exist, the agent performs a first takeover and clearly marks historical changes that cannot be reconstructed as unknown.

## Two operating modes

- **Outgoing handoff:** records confirmed goals, development rules, progress, repository state, and an optional file baseline.
- **Incoming handoff:** verifies the current project and waits for human confirmation before continuing.

## Repository layout

```text
project-handoff/
├── SKILL.md
└── references/
    ├── incoming.md
    ├── outgoing.md
    └── record-templates.md
```

The skill itself is defined in `SKILL.md`. The reference files contain the detailed outgoing and incoming workflows and reusable record templates.

## Usage

To create a handoff package:

```text
Use $project-handoff to prepare an outgoing handoff for this project.
```

To receive a project:

```text
Use $project-handoff to receive this project, verify its current state, and wait for my confirmation before continuing.
```

The skill does not require a custom script or a specific AI agent product. It can be copied into any environment that supports the `SKILL.md` format.

