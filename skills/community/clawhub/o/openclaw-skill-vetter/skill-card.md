## Description:

Skill Vetter provides a pre-install security review protocol for AI agent skills, checking source trust, code red flags, permission scope, and risk classification before installation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[donovanpankratz-del](https://clawhub.ai/user/donovanpankratz-del)

### License/Terms of Use:

MIT

## Use Case:

Developers, engineers, and agent operators use this skill to evaluate ClawHub, GitHub, or otherwise shared agent skills before installation. It guides reviewers through source checks, code review, permission analysis, and a markdown-friendly risk report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill suggests installing untrusted ClawHub skills into a temporary directory before inspection.

Mitigation: Use a non-executing extraction mode, inert archive, or source snapshot; verify publisher, version, and integrity before isolated review, and install only after explicit approval.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/donovanpankratz-del/skills/openclaw-skill-vetter)
- [ClawHub](https://clawhub.com)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown review reports, checklists, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq for optional repository and package metadata checks.]

## Skill Version(s):

1.0.0 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
