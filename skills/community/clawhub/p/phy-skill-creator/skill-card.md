## Description:

Create new skills, modify and improve existing skills, and measure skill performance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to draft, update, evaluate, benchmark, optimize, and package agent skills. It supports iterative skill development with test prompts, qualitative review, quantitative checks, and packaging guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may create local evaluation workspaces and run Python helper commands.

Mitigation: Review workspace paths and confirm helper scripts come from the intended skill package or another trusted environment before execution.

Risk: The skill may spawn evaluation agents where available.

Mitigation: Review generated prompts, inputs, and outputs before relying on results or using them to revise a published skill.

Risk: The skill may launch a temporary local review UI.

Mitigation: Use the review UI only for the intended local evaluation session and stop the viewer process when review is complete.

## Reference(s):

- [Phy Skill Creator on ClawHub](https://clawhub.ai/phy041/skills/phy-skill-creator)
- [Canlah AI](https://canlah.ai)
- [Publisher Profile](https://clawhub.ai/user/phy041)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code blocks, JSON examples, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local skill files, evaluation workspaces, benchmark artifacts, packaged skill archives, and static review HTML when the workflow is run.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
