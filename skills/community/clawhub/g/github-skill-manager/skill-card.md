## Description:

Manage agent skills sourced from GitHub repositories, including installation, update checks, updates, uninstallation, and REGISTRY.yaml tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qvshuo](https://clawhub.ai/user/qvshuo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to manage GitHub-hosted skills, check for updates, apply updates, uninstall skills, and maintain REGISTRY.yaml records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install, update, or delete persistent agent skills from mutable GitHub sources without enough validation or review controls.

Mitigation: Review this skill before installing, use it only with trusted repositories, and prefer immutable commit references.

Risk: Unattended broad updates or unclear skill names and paths could modify or remove unintended local skills.

Mitigation: Avoid unattended broad updates and confirm exact skill names and paths before update or uninstall actions.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/qvshuo/skills/github-skill-manager)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with tables and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May result in persistent skill files and REGISTRY.yaml changes when executed by an agent.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
