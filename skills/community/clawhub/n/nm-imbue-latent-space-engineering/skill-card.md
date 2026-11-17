## Description:

Shapes agent behavior via instruction framing and style transfer

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent authors use the skill to write delegation prompts and skill instructions, choose instruction-framing techniques, and match an existing code or writing style.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Named-register guidance may fade during long sessions, and its effect depends on the model's prior knowledge of the named standard.

Mitigation: Test the register before relying on it and use deterministic checks for critical style requirements.

Risk: Competitive review framing can encourage inflated issue counts without evidence requirements.

Mitigation: Require evidence for each finding and prioritize findings by severity rather than count.

## Reference(s):

- [Emotional Framing](modules/emotional-framing.md)
- [Style Gene Transfer](modules/style-gene-transfer.md)
- [Competitive Review Framing](modules/competitive-review.md)
- [Named Register Invocation](modules/named-register-invocation.md)
- [Know Your Delegate](modules/know-your-delegate.md)
- [Claude Night Market imbue plugin page](https://github.com/athola/claude-night-market/tree/master/plugins/imbue)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown]

**Output Format:** [Natural-language guidance and prompt text, commonly in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advice is tailored to the task type and the delegate's context.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
