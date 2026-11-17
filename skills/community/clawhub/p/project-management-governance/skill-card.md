## Description:

Maintain project navigation, persistent context, reusable decisions, handoffs, and optional project documentation setup when requested.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fingolfin2](https://clawhub.ai/user/fingolfin2)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project teams use this skill to maintain project memory, navigation, reusable decisions, and handoffs across agent-assisted work. It can also initialize or adapt lightweight documentation scaffolds when explicitly requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project memory and documentation updates could capture secrets, private chat content, or unrelated sensitive context if requested too broadly.

Mitigation: Use explicit setup, adaptation, or history-import requests, and avoid asking the skill to store secrets or unrelated private content.

Risk: Project scaffolding or governance adaptation could clutter an existing project if applied without a clear request.

Mitigation: Apply setup and adaptation behavior only when explicitly requested, preserve existing files, and use dry-run or read-only detection helpers before creating files.

## Reference(s):

- [Setup and Compatibility](artifact/references/setup.md)
- [History and Handoff](artifact/references/history.md)
- [ClawHub Skill Page](https://clawhub.ai/fingolfin2/skills/project-management-governance)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Files, Shell commands, Configuration]

**Output Format:** [Markdown guidance with optional project files, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update project memory and documentation files only within the user's requested scope.]

## Skill Version(s):

1.1.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
