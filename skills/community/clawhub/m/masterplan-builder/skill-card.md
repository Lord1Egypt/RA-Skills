## Description:

Builds a complete, production-ready Markdown masterplan for a new project or system through a guided interview, live web research, decision validation, and self-audit against production-readiness checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anjasta-tarigan](https://clawhub.ai/user/anjasta-tarigan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product leads, and project owners use this skill to turn an early project idea into an implementation-ready masterplan before building. It is intended for new websites, apps, agents, APIs, extensions, CLI tools, and similar systems that need detailed planning rather than quick one-off scripting or review of an existing plan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes the masterplan under docs/masterplan/ without requiring a final overwrite confirmation, so an existing masterplan at that path could be replaced.

Mitigation: Check whether docs/masterplan/masterplan.md or related files already exist before running, preserve any needed content, and review generated file changes before committing.

Risk: The skill depends on live web research for stack and architecture recommendations, so poor source selection can lead to outdated or unsuitable decisions.

Mitigation: Prefer official documentation and current primary sources for major technical choices, and have a human review cited decisions before treating the masterplan as build-ready.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/anjasta-tarigan/skills/masterplan-builder)
- [Skill Workflow](SKILL.md)
- [README](README.md)
- [Interview Topics](references/interview-topics.md)
- [Production-Readiness Standards](references/production-standards.md)
- [Planning and Governance Gap Checklist](references/gap-checklist.md)
- [Masterplan Document Structure](references/masterplan-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown masterplan file plus concise chat summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes the final plan to docs/masterplan/masterplan.md in the project directory and may split large plans into additional Markdown files under docs/masterplan/.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
