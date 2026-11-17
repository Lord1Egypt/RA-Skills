## Description:

Create, manage, and validate SOUL.md personality files for multi-agent systems, including persona definition, collaboration protocols, and soul validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuderu-hub](https://clawhub.ai/user/xuderu-hub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create, audit, and maintain standardized SOUL.md personality files for multi-agent systems. It supports agent persona selection, collaboration protocol design, local validation, and optional local editing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The web editor exposes unauthenticated read and write access to persistent agent instruction files.

Mitigation: Use the editor only in a trusted local environment; bind the server to localhost, add authentication, remove wildcard CORS, validate agent names and paths, and limit request sizes before broader use.

Risk: The documented auto-start behavior can keep the local editor server running in the background.

Mitigation: Avoid enabling auto-start unless operationally required, and disable the startup entry when the editor is not actively needed.

Risk: Editing workflows can overwrite SOUL.md files that define persistent agent behavior.

Mitigation: Back up SOUL.md files before editing and review changes before deploying them to active agents.

## Reference(s):

- [SOUL.md Template](references/soul-template.md)
- [Personality Library](references/personality-library.md)
- [Multi-Agent Collaboration Protocol](references/collaboration-protocol.md)
- [SOUL Editor README](scripts/SOUL-EDITOR-README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with command examples, generated SOUL.md files, and local validation output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and write local agent SOUL.md files when the bundled scripts or editor are run.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
