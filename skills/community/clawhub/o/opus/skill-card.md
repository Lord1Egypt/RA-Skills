## Description:

Auto-routes Claude tasks across Haiku, Sonnet, and Opus by starting with cheaper models and escalating for code, analysis, architecture, debugging, strategic planning, and other complex work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[victorking2005](https://clawhub.ai/user/victorking2005)

### License/Terms of Use:


## Use Case:

Agents and developers use this skill to choose an appropriate Claude model for each task, reducing cost while reserving stronger models for complex or high-impact work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The model-routing thresholds are subjective and may under-select model capability for ambiguous, high-impact, production, legal, financial, medical, or security-sensitive work.

Mitigation: Treat the routing rules as guidance and manually choose a stronger model for ambiguous or high-impact tasks.

Risk: The skill provides guidance only and does not enforce routing decisions through code or policy controls.

Mitigation: Review agent behavior after installation and apply local model-selection safeguards where strict routing is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/victorking2005/skills/opus)
- [ClawHub homepage](https://clawhub.com)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration]

**Output Format:** [Markdown guidance with inline command examples and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces routing recommendations; it does not execute model switches directly.]

## Skill Version(s):

1.0.0 (source: server release and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
