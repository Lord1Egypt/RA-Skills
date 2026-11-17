## Description:

Convert between American odds, decimal odds, fractional odds, implied probability, and Kalshi contract prices. Use when asked to convert odds formats, explain what odds mean, or compare odds across platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rsquaredsolutions2026](https://clawhub.ai/user/rsquaredsolutions2026)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to convert odds values across sportsbook, probability, and Kalshi-style price formats and to explain what a given odds value means in plain English.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports that command examples can turn a malicious odds value into local Python code execution.

Mitigation: Review before installing and rewrite usage so inputs are parsed as data, validated as numeric values, and passed to Python without code substitution.

## Reference(s):

- [ClawHub Odds Converter release](https://clawhub.ai/rsquaredsolutions2026/skills/odds-converter)
- [AgentBets OpenClaw Odds Converter tutorial](https://agentbets.ai/guides/openclaw-odds-converter-skill/)
- [OpenClaw Skills series](https://agentbets.ai/guides/#openclaw-skills)
- [Agent Betting Stack](https://agentbets.ai/guides/agent-betting-stack/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks and conversion tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Conversion output is expected to show all five odds formats and plain-English explanations when requested.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
