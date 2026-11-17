## Description:

Guides agents to use ripgrep or grep to locate symbols, calls, definitions, errors, and code usage before reading or editing files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to narrow code investigations with local search, follow definitions and call sites, and report precise file and line locations before making changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local search output can reveal sensitive strings already present in a workspace.

Mitigation: Use the skill only in workspaces the agent is allowed to inspect, and avoid sharing search results that contain secrets or private data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-grep)
- [Publisher profile](https://clawhub.ai/user/zhaobod1)

## Skill Output:

**Output Type(s):** [guidance, shell commands, markdown]

**Output Format:** [Markdown with inline shell commands and file-line references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only search workflow; no required external binaries declared by package metadata.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
