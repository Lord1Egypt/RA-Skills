## Description:

Agent personality diagnosis and configuration optimization system for diagnosing an agent's MBTI-style personality type, comparing it with user expectations, and generating configuration modification suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[torchesfrms](https://clawhub.ai/user/torchesfrms)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to run a staged MBTI-style assessment of an agent, compare the observed profile with user preferences, and produce configuration guidance or patch suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may direct the agent to automatically modify a persistent SOUL.md configuration file without clear confirmation, scope, or rollback controls.

Mitigation: Review the exact generated diff before allowing any SOUL.md change, and prefer applying recommendations or patches manually after approval.

Risk: The server security verdict is suspicious because the skill can affect persistent agent behavior.

Mitigation: Review and scan the skill before installation, and use it in a controlled workspace until the configuration-change behavior is understood.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/torchesfrms/skills/mbti)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown and command-line text with configuration patch suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose changes to persistent agent configuration; review generated patches before applying them.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
