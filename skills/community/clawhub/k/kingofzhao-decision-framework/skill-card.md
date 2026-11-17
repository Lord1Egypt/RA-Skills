## Description:

KingOfZhao Decision Framework is a Chinese-language decision framework for structuring choices around knowns, unknowns, confidence-weighted tradeoffs, red-line checks, and decision memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kingofzhao](https://clawhub.ai/user/kingofzhao)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to compare options with KUWR known/unknown analysis, confidence-weighted scoring, red-line checks, and recorded decision rationales.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installed package could differ from the intended ClawHub release.

Mitigation: Confirm the package name, publisher handle, and version resolve to kingofzhao/kingofzhao-decision-framework version 1.0.0 before installation.

Risk: Decision-memory behavior may create local notes about decisions and outcomes.

Mitigation: Allow decision-memory files only in workspaces where retaining those records is intended.

Risk: The skill instructions are primarily Chinese-language.

Mitigation: Use the skill only when the operator can review the Chinese-language guidance directly or through an approved translation workflow.

Risk: A confidence-weighted recommendation can be mistaken for an objective or guaranteed outcome.

Mitigation: Review assumptions, confidence values, unknowns, and red-line checks before acting on high-impact or irreversible decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kingofzhao/skills/kingofzhao-decision-framework)
- [Project homepage](https://github.com/KingOfZhao/AGI_PROJECT)
- [A Survey of Self-Evolving Agents](https://arxiv.org/abs/2507.21046)
- [SAGE: Multi-Agent Self-Evolution](https://arxiv.org/abs/2603.15255)
- [Memory in the Age of AI Agents](https://arxiv.org/abs/2512.13564)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text decision analysis with ranked options, red-line checks, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local decision-memory notes when the user asks to record outcomes.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
