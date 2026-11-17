## Description:

Extends the org-cli skill so the agent also persists its own memory (knowledge, observations, daily notes) to an org workspace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dcprevere](https://clawhub.ai/user/dcprevere)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use org-memory to give an OpenClaw agent a separate org-mode workspace for durable memory, daily notes, TODOs, and graph-structured knowledge while keeping the user's org-cli workspace distinct.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent raw memory is reloaded into future agent sessions, so saved secrets or untrusted instructions can affect later behavior.

Mitigation: Install only when durable agent memory is intended, avoid saving secrets or untrusted instructions, and review memory.org plus daily notes periodically.

Risk: Configured workspace paths and the org binary control where the skill reads and writes durable files.

Mitigation: Restrict ORG_MEMORY_DIR, ORG_MEMORY_ROAM_DIR, ORG_MEMORY_DB, and ORG_CLI_BIN to trusted values; add path-containment validation before treating the skill as low risk.

## Reference(s):

- [Memory architecture](references/memory-architecture.md)
- [org-cli homepage](https://github.com/dcprevere/org-cli)
- [org-cli releases](https://github.com/dcprevere/org-cli/releases)
- [ClawHub skill page](https://clawhub.ai/dcprevere/skills/org-memory)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with org shortcut syntax and text results from org CLI operations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Loads configured memory files into agent context and uses configured org workspaces for search, TODOs, notes, appends, and roam upserts.]

## Skill Version(s):

1.0.2 (source: SKILL.md frontmatter, plugin package metadata, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
