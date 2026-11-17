## Description:

Multi-turn PRD (Product Requirements Document) creation assistant that asks clarifying questions one at a time to gather requirements, then generates a complete, professional PRD.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Product managers, founders, and development teams use this skill to gather requirements through a guided question flow and produce a structured PRD for a new feature, product, or project.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger phrases may start the PRD workflow when the user's intent is ambiguous.

Mitigation: Prefer explicit invocations such as /prd, write a PRD, or create a PRD before using the skill.

Risk: The skill may propose saving files, creating git commits, handing off to other agents, or searching local transcripts after drafting a PRD.

Mitigation: Review and approve each proposed path, commit, handoff, and local search scope before allowing the action to proceed.

## Reference(s):

- [Phy Prd Writer ClawHub skill page](https://clawhub.ai/phy041/skills/phy-prd-writer)
- [Publisher profile: phy041](https://clawhub.ai/user/phy041)
- [Canlah AI homepage](https://canlah.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands]

**Output Format:** [Markdown PRD document with guided follow-up prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose save locations, git commits, agent handoffs, and local transcript searches after the PRD is generated.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
