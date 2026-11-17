## Description:

Skill Router analyzes user requests, selects one or more matching skills, and proposes or executes ordered skill chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mupengi-bot](https://clawhub.ai/user/mupengi-bot)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to route user requests to available skills, compose multi-step workflows, and coordinate approval-gated downstream actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The router can execute and chain other skills broadly, increasing the impact of an incorrect routing decision or unsafe downstream skill.

Mitigation: Install it only in environments where downstream skills are trusted and constrained by an external policy or approval layer.

Risk: Approval boundaries for side effects may be insufficient for sensitive actions such as repository changes, email, social posting, or recovery tooling.

Mitigation: Require explicit human approval for external actions and avoid granting access to credentials, repositories, social accounts, email, or system-recovery tools unless separately governed.

Risk: The skill describes event and log persistence that may retain operational context.

Mitigation: Use it only where event and log persistence is acceptable, and review retention paths before handling sensitive data.

## Reference(s):

- [Skill Chain Templates](artifact/chains.md)
- [ClawHub Skill Page](https://clawhub.ai/mupengi-bot/skills/mupeng-skill-router)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May coordinate downstream skill execution and event or log persistence depending on the routed skills.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
