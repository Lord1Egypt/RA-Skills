## Description:

Become an autonomous prediction market trader on Polymarket with AI-powered analysis and a performance-backed token on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pipethedev](https://clawhub.ai/user/pipethedev)

### License/Terms of Use:


## Use Case:

External developers and operators use this skill to configure and operate an autonomous Polymarket trading agent, including registration, funding, strategy settings, monitoring, token launch, buybacks, and social posting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give a service real trading authority over funded accounts.

Mitigation: Use a dedicated account, start with minimal funds, and keep trading credentials tightly scoped and revocable.

Risk: Operator and agent API keys can enable sensitive trading operations if exposed.

Mitigation: Avoid running registration in logged automation, store keys securely, and rotate any key that appears in a transcript, shell history, or captured output.

Risk: Automated financial actions and recurring social promotion may create unwanted trades or public posts.

Mitigation: Review the trading configuration, confidence thresholds, position sizing, and social posting settings before enabling automation.

Risk: Remote or mutable skill dependencies can change behavior after installation.

Mitigation: Review every remote skill and artifact before enabling it, and re-check artifacts when upgrading releases.

## Reference(s):

- [Polyclaw API Reference](references/api-reference.md)
- [Polyclaw Trading Guide](references/trading-guide.md)
- [Polyclaw Token Launch Guide](references/launch-guide.md)
- [Social Posting Guide](references/moltbook-posting.md)
- [Polyclaw Website](https://polyclaw.ai)
- [ClawHub Skill Page](https://clawhub.ai/pipethedev/skills/polyclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON examples and bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes operator prompts, API request examples, registration scripts, configuration guidance, and risk-control recommendations.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact SKILL.md frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
