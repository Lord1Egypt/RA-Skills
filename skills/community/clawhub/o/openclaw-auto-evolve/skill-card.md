## Description:

OpenClaw 自进化系统 helps an agent check workspace health, summarize learned rules, and record learning notes for an OpenClaw workspace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejianjun000](https://clawhub.ai/user/xiejianjun000)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to check workspace health, inspect learned-rule summaries, and record learning notes as part of an agent self-improvement workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist learning notes and encourage automatic rule or memory behavior without clear user controls.

Mitigation: Review before installation, make learning or memory updates opt-in, and inspect the configured OpenClaw workspace for persisted notes.

Risk: The description claims broad self-evolution capabilities that exceed the lightweight implementation.

Mitigation: Treat it as a health, rule-summary, and learning-note helper unless additional controls and validation are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiejianjun000/skills/openclaw-auto-evolve)

## Skill Output:

**Output Type(s):** [text, JSON, markdown, guidance]

**Output Format:** [JSON status responses and Markdown learning records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist learning notes under the configured OpenClaw workspace.]

## Skill Version(s):

1.0.0 (source: server release metadata and OpenClaw frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
